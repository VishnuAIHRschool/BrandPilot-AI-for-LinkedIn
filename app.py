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
# Page Config
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
    background: linear-gradient(135deg, #F4F8FC 0%, #FFFFFF 48%, #EEF5FB 100%);
    color: #111827 !important;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Force readable text in main page */
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
    color: #FFFFFF !important;
}

.sidebar-brand {
    padding: 24px 18px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.22);
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
    background: rgba(255,255,255,0.13);
    font-size: 14px;
    font-weight: 700;
}

.sidebar-note {
    margin-top: 18px;
    padding: 15px;
    border-radius: 18px;
    background: rgba(255,255,255,0.13);
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

/* Top cards */
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

.form-card {
    background: #FFFFFF;
    border: 1px solid #D9E7F5;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 14px 36px rgba(15,23,42,0.06);
    margin-top: 10px;
}

/* Labels */
label {
    font-weight: 800 !important;
    color: #111827 !important;
    font-size: 14px !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #111827 !important;
    border: 1.5px solid #B7CBDD !important;
    border-radius: 14px !important;
    box-shadow: none !important;
    caret-color: #111827 !important;
}

.stTextInput > div > div > input:focus,
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

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {
    background: #FFFFFF !important;
    border-radius: 14px !important;
    border-color: #B7CBDD !important;
    color: #111827 !important;
}

.stSelectbox * {
    color: #111827 !important;
}

/* Buttons */
div.stButton > button {
    width: auto;
    min-height: 52px;
    padding: 0 26px;
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
    background: #FFFFFF;
    font-weight: 800;
}

/* Loading card */
.loading-card {
    margin-top: 22px;
    padding: 22px 24px;
    border-radius: 22px;
    background: #FFFFFF;
    border: 1px solid #BBD8F2;
    border-left: 7px solid #0A66C2;
    box-shadow: 0 16px 36px rgba(15,23,42,0.08);
}

.loading-title {
    color: #0A66C2 !important;
    font-size: 19px;
    font-weight: 900;
    margin-bottom: 6px;
}

.loading-text {
    color: #334155 !important;
    font-size: 14.5px;
    line-height: 1.6;
}

/* Result card */
.result-box {
    margin-top: 24px;
    padding: 30px;
    border-radius: 26px;
    background: #FFFFFF !important;
    border: 1px solid #D8E6F3;
    border-left: 8px solid #0A66C2;
    box-shadow: 0 18px 42px rgba(15,23,42,0.10);
}

.result-box,
.result-box *,
.result-box p,
.result-box li,
.result-box span,
.result-box div,
.result-box h1,
.result-box h2,
.result-box h3,
.result-box h4,
.result-box strong,
.result-box em {
    color: #111827 !important;
    opacity: 1 !important;
}

.result-box h1,
.result-box h2,
.result-box h3 {
    color: #0F172A !important;
    font-weight: 900 !important;
}

.result-box h4 {
    color: #0A66C2 !important;
    font-weight: 850 !important;
}

.result-heading {
    color: #0A66C2 !important;
    font-size: 24px;
    font-weight: 900;
    margin-bottom: 14px;
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


def show_loading(message: str):
    return st.empty().markdown(
        f"""
        <div class="loading-card">
            <div class="loading-title">⏳ Generating with AI...</div>
            <div class="loading-text">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_result(title: str, response: str, file_name: str):
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="result-heading">{title}</div>', unsafe_allow_html=True)
    st.markdown(response)
    st.download_button(
        label="⬇️ Download Output",
        data=response,
        file_name=file_name,
        mime="text/plain"
    )
    st.markdown('</div>', unsafe_allow_html=True)


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
You are a senior LinkedIn personal branding strategist and profile optimization expert.

Your task is to analyze and improve the user's LinkedIn profile based only on the content they provide.

Important rules:
- Do not claim that you opened, visited, scraped, or verified the LinkedIn URL.
- The LinkedIn URL is only a reference field.
- Use the uploaded PDF text, pasted About section, and experience details as the source.
- Do not invent fake experience, fake metrics, fake brands, or fake achievements.
- If information is missing, say what is missing and suggest what the user should add.
- Keep the final output professional, practical, polished, and ready to copy into LinkedIn.
- Use a premium, clear, executive-style tone.

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

Generate the following in clear Markdown:

## 1. Profile Strength Score out of 100
## 2. Reason for the Score
## 3. Missing Information Checklist
## 4. 5 Improved LinkedIn Headline Options
## 5. Optimized LinkedIn About Section
## 6. Experience Section Rewrite Suggestions
## 7. Top 15 LinkedIn Keywords
## 8. Featured Section Suggestions
## 9. Profile Banner Tagline Ideas
## 10. 5 LinkedIn Post Ideas Based on This Profile
""")


post_prompt = ChatPromptTemplate.from_template("""
You are a professional LinkedIn content writer.

Create a polished LinkedIn post based on the user's input.

Important rules:
- Make the opening line strong.
- Use simple, professional, human language.
- Avoid fake claims.
- Keep it readable with short paragraphs.
- Add a clear CTA.
- Add 3 to 5 relevant hashtags.

User Input:

Topic:
{topic}

Tone:
{tone}

Target Audience:
{audience}

Post Goal:
{goal}

Additional Context:
{context}

Generate in clear Markdown:

## 1. LinkedIn Post
## 2. Suggested Hook
## 3. Suggested CTA
## 4. Relevant Hashtags
""")


strategy_prompt = ChatPromptTemplate.from_template("""
You are a LinkedIn personal branding strategist.

Create a practical LinkedIn content strategy for the user.

Rules:
- Keep it realistic.
- Do not suggest fake achievements.
- Make it beginner-friendly but professional.
- Focus on consistency and clear positioning.

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

Posting Frequency:
{frequency}

Generate in clear Markdown:

## 1. Personal Brand Positioning Statement
## 2. 4 Content Pillars
## 3. Weekly LinkedIn Content Plan
## 4. 12 LinkedIn Post Ideas
## 5. Best Post Formats for This User
## 6. 5 Practical Growth Tips
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
# Metric Cards
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
# App Tabs
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "👤 Profile Intelligence",
    "✍️ Post Studio",
    "📅 Content Strategy"
])


# --------------------------------------------------
# Tab 1 - Profile Optimizer
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
            loading = st.empty()
            loading.markdown("""
            <div class="loading-card">
                <div class="loading-title">⏳ Building your profile optimization report...</div>
                <div class="loading-text">
                    AI is reviewing your profile inputs, identifying gaps, and generating better headlines, About section, keywords, and content ideas.
                </div>
            </div>
            """, unsafe_allow_html=True)

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

            loading.empty()
            st.session_state.profile_result = response

    if st.session_state.profile_result:
        show_result(
            "✅ Profile Optimization Report",
            st.session_state.profile_result,
            "brandpilot_profile_optimization.txt"
        )


# --------------------------------------------------
# Tab 2 - Post Generator
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
            placeholder="Example: I built my first LangChain application",
            height=150
        )

        context = st.text_area(
            "Additional Context - optional",
            placeholder="Example: I am learning LangChain step by step and built a Streamlit app.",
            height=110
        )

    with col2:
        audience = st.text_input(
            "Target Audience",
            placeholder="Example: AI learners and beginners"
        )

        tone = st.selectbox(
            "Tone",
            ["Professional", "Inspiring", "Storytelling", "Educational", "Bold", "Simple"]
        )

        goal = st.selectbox(
            "Post Goal",
            ["Educate", "Inspire", "Share Learning", "Promote Project", "Build Personal Brand"]
        )

    generate_post = st.button("✨ Generate Professional Post")

    if generate_post:
        if not topic or not audience:
            st.warning("Please enter Post Topic and Target Audience.")
        else:
            loading = st.empty()
            loading.markdown("""
            <div class="loading-card">
                <div class="loading-title">⏳ Writing your LinkedIn post...</div>
                <div class="loading-text">
                    AI is creating a clear post with a strong hook, CTA, and hashtags.
                </div>
            </div>
            """, unsafe_allow_html=True)

            response = post_chain.invoke({
                "topic": topic,
                "tone": tone,
                "audience": audience,
                "goal": goal,
                "context": context if context else "Not provided"
            })

            loading.empty()
            st.session_state.post_result = response

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
        frequency = st.selectbox(
            "Posting Frequency",
            ["2 posts per week", "3 posts per week", "4 posts per week", "5 posts per week"]
        )

    generate_strategy = st.button("📌 Build My Content Strategy")

    if generate_strategy:
        if not strategy_name or not strategy_role or not strategy_skills or not strategy_audience or not strategy_goal:
            st.warning("Please fill all fields before generating.")
        else:
            loading = st.empty()
            loading.markdown("""
            <div class="loading-card">
                <div class="loading-title">⏳ Building your content strategy...</div>
                <div class="loading-text">
                    AI is creating your positioning, content pillars, weekly plan, and post ideas.
                </div>
            </div>
            """, unsafe_allow_html=True)

            response = strategy_chain.invoke({
                "name": strategy_name,
                "role": strategy_role,
                "skills": strategy_skills,
                "audience": strategy_audience,
                "goal": strategy_goal,
                "frequency": frequency
            })

            loading.empty()
            st.session_state.strategy_result = response

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