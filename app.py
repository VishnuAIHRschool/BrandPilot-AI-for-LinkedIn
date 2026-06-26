import os
import re
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------
load_dotenv()


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="BrandPilot AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #F5F9FC 0%, #FFFFFF 50%, #EEF5FB 100%);
    color: #111827 !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Force main text visibility */
.main,
.block-container,
.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown span,
.stMarkdown div,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown h6 {
    color: #111827 !important;
    opacity: 1 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #004182 0%, #0A66C2 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-brand {
    padding: 24px 18px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.16);
    border: 1px solid rgba(255, 255, 255, 0.24);
    text-align: center;
    margin-bottom: 22px;
}

.brand-icon {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: #FFFFFF;
    color: #0A66C2 !important;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 15px auto;
    font-size: 33px;
    font-weight: 900;
    letter-spacing: -2px;
}

.brand-title {
    font-size: 25px;
    font-weight: 900;
}

.brand-subtitle {
    font-size: 13.5px;
    line-height: 1.6;
    margin-top: 8px;
}

.sidebar-menu-item {
    padding: 13px 15px;
    border-radius: 16px;
    margin-bottom: 9px;
    background: rgba(255,255,255,0.14);
    font-size: 14px;
    font-weight: 700;
}

.sidebar-note {
    margin-top: 18px;
    padding: 15px;
    border-radius: 18px;
    background: rgba(255,255,255,0.14);
    font-size: 13px;
    line-height: 1.6;
}

/* Hero */
.hero {
    border-radius: 28px;
    padding: 34px 38px;
    background: linear-gradient(135deg, #004182 0%, #0A66C2 100%);
    box-shadow: 0 18px 44px rgba(10,102,194,0.22);
    margin-bottom: 24px;
}

.hero * {
    color: #FFFFFF !important;
}

.hero-pill {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 999px;
    background: rgba(255,255,255,0.18);
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 15px;
}

.hero-title {
    font-size: 44px;
    font-weight: 900;
    letter-spacing: -1.3px;
    line-height: 1.08;
    margin-bottom: 12px;
}

.hero-desc {
    max-width: 850px;
    font-size: 17px;
    line-height: 1.65;
}

/* Feature cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 15px 0 28px 0;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #D9E7F5;
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 8px 26px rgba(15,23,42,0.05);
}

.metric-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.metric-title {
    color: #111827 !important;
    font-size: 16px;
    font-weight: 850;
    margin-bottom: 6px;
}

.metric-text {
    color: #475569 !important;
    font-size: 13.5px;
    line-height: 1.55;
}

/* Tabs */
[data-baseweb="tab-list"] {
    gap: 10px;
    margin-bottom: 18px;
}

[data-baseweb="tab"] {
    background: #FFFFFF;
    border: 1px solid #D8E6F3;
    border-radius: 999px;
    padding: 11px 18px;
    font-weight: 850;
    color: #1F2937 !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    background: #0A66C2;
    color: #FFFFFF !important;
    border-color: #0A66C2;
}

/* Module headers */
.module-title {
    font-size: 29px;
    color: #111827 !important;
    font-weight: 900;
    letter-spacing: -0.6px;
    margin-bottom: 4px;
}

.module-subtitle {
    color: #475569 !important;
    font-size: 15.5px;
    margin-bottom: 18px;
}

.guidance-box {
    padding: 16px 18px;
    border-radius: 18px;
    background: #EAF4FF;
    border: 1px solid #BBD8F2;
    color: #1E293B !important;
    font-size: 14.5px;
    line-height: 1.6;
    margin-bottom: 18px;
}

/* Labels */
label {
    font-weight: 800 !important;
    color: #111827 !important;
    font-size: 14px !important;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1.5px solid #B7CBDD !important;
    border-radius: 14px !important;
    box-shadow: none !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 2px solid #0A66C2 !important;
    box-shadow: 0 0 0 3px rgba(10,102,194,0.13) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #7A8797 !important;
    opacity: 1 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 1.5px dashed #8EBCE8 !important;
    border-radius: 18px !important;
    padding: 16px !important;
}

[data-testid="stFileUploader"] section {
    background: #F8FBFF !important;
    border: 1px solid #D6E7F8 !important;
    border-radius: 14px !important;
    color: #111827 !important;
}

[data-testid="stFileUploader"] section * {
    color: #111827 !important;
}

[data-testid="stFileUploader"] button {
    background: #0A66C2 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 800 !important;
}

/* Multiselect visibility */
[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border-radius: 14px !important;
    border: 1.5px solid #B7CBDD !important;
    color: #111827 !important;
}

[data-baseweb="select"] * {
    color: #111827 !important;
}

[data-baseweb="tag"] {
    background-color: #EAF4FF !important;
    border: 1px solid #BBD8F2 !important;
    color: #0A66C2 !important;
    border-radius: 999px !important;
    font-weight: 700 !important;
}

[data-baseweb="tag"] span {
    color: #0A66C2 !important;
}

[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

ul[role="listbox"] {
    background-color: #FFFFFF !important;
}

li[role="option"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
}

li[role="option"]:hover {
    background-color: #EAF4FF !important;
    color: #111827 !important;
}

/* Buttons */
div.stButton > button {
    min-height: 52px;
    padding: 0 28px;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #0A66C2 0%, #004182 100%);
    color: #FFFFFF !important;
    font-size: 15px;
    font-weight: 850;
    box-shadow: 0 12px 28px rgba(10,102,194,0.28);
    transition: all 0.2s ease-in-out;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    color: #FFFFFF !important;
    box-shadow: 0 18px 34px rgba(10,102,194,0.36);
}

div.stDownloadButton > button {
    border-radius: 999px;
    border: 1px solid #0A66C2;
    color: #0A66C2 !important;
    background: #FFFFFF !important;
    font-weight: 800;
}

/* Native result container visibility */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid #D8E6F3 !important;
    border-radius: 24px !important;
    box-shadow: 0 18px 42px rgba(15,23,42,0.08) !important;
}

.result-title {
    color: #0A66C2 !important;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 8px;
}

.footer {
    padding: 28px 0 8px 0;
    text-align: center;
    font-size: 13px;
    color: #667085 !important;
}

@media only screen and (max-width: 950px) {
    .metrics-grid {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 28px;
    }

    .hero-title {
        font-size: 34px;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# API Key Check
# --------------------------------------------------
if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found. Please add your API key inside the .env file.")
    st.code("OPENAI_API_KEY=your_api_key_here")
    st.stop()


# --------------------------------------------------
# Session State
# --------------------------------------------------
if "profile_result" not in st.session_state:
    st.session_state.profile_result = None

if "post_result" not in st.session_state:
    st.session_state.post_result = None

if "strategy_result" not in st.session_state:
    st.session_state.strategy_result = None


# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def is_valid_linkedin_url(url: str) -> bool:
    if not url:
        return True

    pattern = r"^(https?:\/\/)?(www\.)?linkedin\.com\/in\/[A-Za-z0-9\\-_%]+\/?.*$"
    return re.match(pattern, url.strip()) is not None


def extract_pdf_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    try:
        pdf_bytes = uploaded_file.read()
        reader = PdfReader(BytesIO(pdf_bytes))

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as error:
        st.error(f"Could not read PDF file: {error}")
        return ""


def show_result(title: str, response: str, file_name: str):
    with st.container(border=True):
        st.markdown(f"<div class='result-title'>{title}</div>", unsafe_allow_html=True)
        st.markdown(response)
        st.download_button(
            label="⬇️ Download Output",
            data=response,
            file_name=file_name,
            mime="text/plain"
        )


# --------------------------------------------------
# LLM Setup
# --------------------------------------------------
@st.cache_resource
def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7
    )


llm = get_llm()
output_parser = StrOutputParser()


# --------------------------------------------------
# LangChain Prompts
# --------------------------------------------------
profile_prompt = ChatPromptTemplate.from_template("""
You are a senior LinkedIn profile strategist, personal branding consultant, and professional positioning expert.

Your task is to analyze and improve the user's LinkedIn profile using only the content provided by the user.

Important rules:
- Do not claim that you opened, visited, scraped, or verified the LinkedIn URL.
- The LinkedIn URL is only a reference field.
- Use uploaded PDF text, pasted About section, and experience details as the source.
- Do not invent fake experience, fake metrics, fake brands, or fake achievements.
- If information is missing, clearly say what is missing.
- Make the final output polished, practical, credible, and ready to copy into LinkedIn.
- Focus on clarity, positioning, discoverability, keyword strength, and professional trust.

User Information:

LinkedIn Profile URL:
{profile_url}

Name:
{name}

Current Role / Title:
{role}

Skills:
{skills}

Target Audience:
{target_audience}

Current LinkedIn About Section:
{about_section}

Experience / Projects / Achievements:
{experience}

Uploaded Profile / Resume / LinkedIn PDF Text:
{uploaded_text}

Generate the output in this structure:

## 1. Profile Strength Score

Give a score out of 100.

## 2. Executive Summary

Give a short summary of the current profile quality.

## 3. What Is Working Well

List the strengths.

## 4. What Is Missing

List missing details, weak areas, and improvement opportunities.

## 5. 5 Premium LinkedIn Headline Options

Make them clear, professional, keyword-rich, and under 220 characters.

## 6. Optimized About Section

Write a polished LinkedIn About section using a professional but human tone.

## 7. Experience Section Rewrite Suggestions

Give improved bullet points and structure.

## 8. Top LinkedIn Keywords

Give 15 keywords that can improve profile discoverability.

## 9. Featured Section Suggestions

Suggest what the user should add to the Featured section.

## 10. Banner Tagline Ideas

Give 5 clean banner text ideas.

## 11. Profile Improvement Action Plan

Give a practical step-by-step improvement checklist.

## 12. LinkedIn Content Ideas

Give 8 post ideas based on the profile.
""")


post_prompt = ChatPromptTemplate.from_template("""
You are a senior LinkedIn content strategist and executive ghostwriter.

Your task is to create a high-quality LinkedIn post that feels human, clear, credible, and professional.

Important rules:
- Do not make fake claims.
- Do not exaggerate achievements.
- Do not sound robotic or generic.
- Keep the post suitable for LinkedIn.
- Use short paragraphs and strong readability.
- Start with a strong hook.
- Include a clear story, insight, or point of view.
- End with a useful call-to-action.
- Make the post practical and industry-standard.
- Avoid overusing emojis.
- Avoid too many hashtags.

User Input:

Topic:
{topic}

Selected Tone Preferences:
{tone}

Target Audience:
{audience}

Selected Post Goals:
{goal}

Additional Context:
{context}

Generate the output in this structure:

## 1. Final LinkedIn Post

Write a polished, ready-to-copy LinkedIn post.

## 2. Why This Post Works

Explain briefly why the hook, flow, tone, and CTA are effective.

## 3. Alternative Hook Options

Give 5 strong hook options.

## 4. Suggested CTA Options

Give 3 CTA options.

## 5. Hashtags

Give 5 relevant hashtags.

## 6. Content Quality Score

Give a score out of 100 and explain the score.
""")


strategy_prompt = ChatPromptTemplate.from_template("""
You are a senior LinkedIn growth strategist and personal branding consultant.

Create a practical, professional LinkedIn content strategy for the user.

Important rules:
- Keep it realistic and beginner-friendly.
- Do not suggest fake achievements.
- Do not give generic advice.
- Make the strategy clear, structured, and executable.
- Focus on positioning, trust-building, consistency, and audience relevance.
- Make the output suitable for a professional LinkedIn creator.

User Details:

Name:
{name}

Current Role / Identity:
{role}

Skills / Interests:
{skills}

Target Audience:
{audience}

Main LinkedIn Goal:
{goal}

Posting Frequency and Style:
{frequency}

Generate the output in this structure:

## 1. Personal Brand Positioning

Write a clear positioning statement.

## 2. Target Audience Understanding

Explain what this audience cares about.

## 3. 5 Content Pillars

Give 5 content pillars with explanation.

## 4. Weekly Content Plan

Create a weekly plan based on the selected posting frequency.

## 5. 15 LinkedIn Post Ideas

Give practical, realistic post ideas.

## 6. Recommended Post Formats

Suggest formats like story post, lesson post, checklist, framework, project update, opinion post, etc.

## 7. 30-Day Growth Plan

Give a practical 30-day action plan.

## 8. Engagement Strategy

Explain how the user should comment, connect, and engage professionally.

## 9. Content Quality Rules

Give rules the user should follow before posting.

## 10. Success Metrics

Suggest what the user should track.
""")


profile_chain = profile_prompt | llm | output_parser
post_chain = post_prompt | llm | output_parser
strategy_chain = strategy_prompt | llm | output_parser


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">in</div>
        <div class="brand-title">BrandPilot AI</div>
        <div class="brand-subtitle">
            AI workspace for profile optimization, post creation, and content strategy.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-menu">
        <div class="sidebar-menu-item">👤 Profile Intelligence</div>
        <div class="sidebar-menu-item">📄 PDF Profile Review</div>
        <div class="sidebar-menu-item">✍️ Post Studio</div>
        <div class="sidebar-menu-item">📅 Strategy Planner</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-note">
        Safe design: this app does not scrape LinkedIn URLs. 
        Use pasted profile content or upload your own PDF/resume for analysis.
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# Hero Section
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-pill">💼 AI Personal Branding Workspace</div>
    <div class="hero-title">BrandPilot AI for LinkedIn</div>
    <div class="hero-desc">
        Optimize your professional profile, generate stronger posts, and build a consistent content strategy using Python, LangChain, OpenAI, and Streamlit.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Feature Cards
# --------------------------------------------------
st.markdown("""
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-icon">👤</div>
        <div class="metric-title">Profile Review</div>
        <div class="metric-text">Analyze headline, About section, keywords, and experience quality.</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📄</div>
        <div class="metric-title">PDF Upload</div>
        <div class="metric-text">Upload your resume or LinkedIn profile PDF for deeper personalization.</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">✍️</div>
        <div class="metric-title">Post Studio</div>
        <div class="metric-text">Create professional LinkedIn posts with hooks, CTA, and hashtags.</div>
    </div>
    <div class="metric-card">
        <div class="metric-icon">📅</div>
        <div class="metric-title">Strategy Planner</div>
        <div class="metric-text">Build content pillars, weekly plan, and practical post ideas.</div>
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "👤 Profile Intelligence",
    "✍️ Post Studio",
    "📅 Content Strategy"
])


# --------------------------------------------------
# Tab 1 - Profile Intelligence
# --------------------------------------------------
with tab1:
    st.markdown('<div class="module-title">👤 Profile Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="module-subtitle">Use pasted profile content or upload your own PDF. URL is reference only.</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="guidance-box">
        LinkedIn profile URL is optional. This app does not open or scrape that URL. 
        For best results, paste your About section, experience details, or upload your own LinkedIn profile PDF / resume.
    </div>
    """, unsafe_allow_html=True)

    profile_url = st.text_input(
        "LinkedIn Profile URL - optional reference only",
        placeholder="https://www.linkedin.com/in/your-profile/"
    )

    if profile_url and not is_valid_linkedin_url(profile_url):
        st.warning("Please enter a valid LinkedIn profile URL, for example: https://www.linkedin.com/in/your-profile/")

    uploaded_file = st.file_uploader(
        "Upload LinkedIn profile PDF or resume PDF - optional",
        type=["pdf"]
    )

    uploaded_text = ""
    if uploaded_file:
        uploaded_text = extract_pdf_text(uploaded_file)
        if uploaded_text:
            st.success("PDF uploaded and text extracted successfully.")
            with st.expander("Preview extracted PDF text"):
                st.write(uploaded_text[:2500])

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", placeholder="Example: Vishnu")
        role = st.text_input("Current Role / Title", placeholder="Example: Gen AI Learner")
        skills = st.text_area(
            "Skills",
            placeholder="Example: Python, LangChain, Streamlit, Prompt Engineering",
            height=130
        )
        target_audience = st.text_input(
            "Target Audience",
            placeholder="Example: AI learners, recruiters, founders"
        )

    with col2:
        about_section = st.text_area(
            "Current LinkedIn About Section",
            placeholder="Paste your LinkedIn About section here...",
            height=155
        )

        experience = st.text_area(
            "Experience / Projects / Achievements",
            placeholder="Paste experience, projects, certifications, achievements, or portfolio details...",
            height=155
        )

    generate_profile = st.button("🚀 Analyze Profile & Generate Improvements")

    if generate_profile:
        has_profile_content = bool(about_section.strip()) or bool(experience.strip()) or bool(uploaded_text.strip())

        if profile_url and not is_valid_linkedin_url(profile_url):
            st.warning("Please fix the LinkedIn URL or remove it.")
        elif not has_profile_content:
            st.warning("Please paste profile content or upload a PDF. URL alone cannot be analyzed.")
        elif not name or not role or not skills or not target_audience:
            st.warning("Please fill Name, Role, Skills, and Target Audience.")
        else:
            with st.status("Building your profile optimization report...", expanded=True) as status:
                st.write("Reviewing profile inputs...")
                st.write("Identifying profile gaps...")
                st.write("Generating improved headline, About section, keywords, and content ideas...")

                response = profile_chain.invoke({
                    "profile_url": profile_url if profile_url else "Not provided",
                    "name": name,
                    "role": role,
                    "skills": skills,
                    "target_audience": target_audience,
                    "about_section": about_section if about_section else "Not provided",
                    "experience": experience if experience else "Not provided",
                    "uploaded_text": uploaded_text if uploaded_text else "Not provided"
                })

                st.session_state.profile_result = response
                status.update(label="Profile optimization completed.", state="complete", expanded=False)

    if st.session_state.profile_result:
        show_result(
            "✅ Profile Optimization Report",
            st.session_state.profile_result,
            "brandpilot_profile_optimization.txt"
        )


# --------------------------------------------------
# Tab 2 - Post Studio
# --------------------------------------------------
with tab2:
    st.markdown('<div class="module-title">✍️ Post Studio</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="module-subtitle">Generate professional LinkedIn posts with better hooks, CTA, and hashtags.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.15, 0.85])

    with col1:
        topic = st.text_area(
            "Post Topic",
            placeholder="Example: Future of AI in HR",
            height=150
        )

        context = st.text_area(
            "Additional Context - optional",
            placeholder="Example: I want to share how AI will change skills, productivity, and decision-making.",
            height=110
        )

    with col2:
        audience = st.text_input(
            "Target Audience",
            placeholder="Example: HR professionals and HR students"
        )

        tone_options = st.multiselect(
            "Tone Preferences",
            [
                "Professional",
                "Inspiring",
                "Storytelling",
                "Educational",
                "Bold",
                "Simple",
                "Thought Leadership",
                "Personal Journey",
                "Industry Insight"
            ],
            default=["Professional", "Educational"]
        )

        goal_options = st.multiselect(
            "Post Goals",
            [
                "Educate",
                "Inspire",
                "Share Learning",
                "Promote Project",
                "Build Personal Brand",
                "Start Conversation",
                "Share Opinion",
                "Create Awareness"
            ],
            default=["Educate", "Build Personal Brand"]
        )

    generate_post = st.button("✨ Generate Professional Post")

    if generate_post:
        if not topic or not audience or not tone_options or not goal_options:
            st.warning("Please enter Post Topic, Target Audience, Tone Preferences, and Post Goals.")
        else:
            with st.status("Creating your LinkedIn post...", expanded=True) as status:
                st.write("Understanding topic and audience...")
                st.write("Applying selected tone and goals...")
                st.write("Writing hook, body, CTA, and hashtags...")

                response = post_chain.invoke({
                    "topic": topic,
                    "tone": ", ".join(tone_options),
                    "audience": audience,
                    "goal": ", ".join(goal_options),
                    "context": context if context else "Not provided"
                })

                st.session_state.post_result = response
                status.update(label="LinkedIn post generated.", state="complete", expanded=False)

    if st.session_state.post_result:
        show_result(
            "✅ Generated LinkedIn Post",
            st.session_state.post_result,
            "brandpilot_linkedin_post.txt"
        )


# --------------------------------------------------
# Tab 3 - Content Strategy
# --------------------------------------------------
with tab3:
    st.markdown('<div class="module-title">📅 Content Strategy</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="module-subtitle">Create positioning, content pillars, weekly plan, and post ideas.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        strategy_name = st.text_input("Your Name", key="strategy_name", placeholder="Example: Vishnu")
        strategy_role = st.text_input(
            "Current Role / Identity",
            key="strategy_role",
            placeholder="Example: Gen AI learner and AI app builder"
        )
        strategy_skills = st.text_area(
            "Skills / Interests",
            key="strategy_skills",
            placeholder="Example: Python, LangChain, Streamlit, AI tools",
            height=150
        )

    with col2:
        strategy_audience = st.text_input(
            "Target Audience",
            key="strategy_audience",
            placeholder="Example: AI beginners, recruiters, business professionals"
        )
        strategy_goal = st.text_area(
            "LinkedIn Goal",
            key="strategy_goal",
            placeholder="Example: Build my personal brand and share my Gen AI learning journey",
            height=100
        )

        frequency_options = st.multiselect(
            "Posting Frequency / Style",
            [
                "2 posts per week",
                "3 posts per week",
                "4 posts per week",
                "5 posts per week",
                "Short posts",
                "Story-based posts",
                "Educational posts",
                "Project update posts",
                "Thought leadership posts"
            ],
            default=["3 posts per week", "Educational posts", "Project update posts"]
        )

    generate_strategy = st.button("📌 Build My Content Strategy")

    if generate_strategy:
        if not strategy_name or not strategy_role or not strategy_skills or not strategy_audience or not strategy_goal or not frequency_options:
            st.warning("Please fill all fields before generating.")
        else:
            with st.status("Building your content strategy...", expanded=True) as status:
                st.write("Understanding your audience and goal...")
                st.write("Creating content pillars...")
                st.write("Building weekly plan and 30-day growth plan...")

                response = strategy_chain.invoke({
                    "name": strategy_name,
                    "role": strategy_role,
                    "skills": strategy_skills,
                    "audience": strategy_audience,
                    "goal": strategy_goal,
                    "frequency": ", ".join(frequency_options)
                })

                st.session_state.strategy_result = response
                status.update(label="Content strategy generated.", state="complete", expanded=False)

    if st.session_state.strategy_result:
        show_result(
            "✅ LinkedIn Content Strategy",
            st.session_state.strategy_result,
            "brandpilot_content_strategy.txt"
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
<div class="footer">
    Built with Python, LangChain, OpenAI, Streamlit and user-provided profile data · No scraping · No automation
</div>
""", unsafe_allow_html=True)