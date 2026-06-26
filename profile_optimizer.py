import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Load environment variables from .env file
load_dotenv()

# Create LLM model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# Create prompt template
profile_prompt = ChatPromptTemplate.from_template("""
You are a LinkedIn personal branding expert.

Your task is to analyze and improve a LinkedIn profile for better clarity, professionalism, visibility, and personal branding.

Important:
- Do not assume information that the user has not provided.
- If the profile details are weak or incomplete, clearly mention that.
- The profile score should be based only on the information provided by the user.
- Keep the language professional, simple, and LinkedIn-friendly.

User Details:

Name:
{name}

Current Role:
{role}

Skills:
{skills}

Target Audience:
{target_audience}

Current LinkedIn About Section:
{about_section}

Please generate the following:

1. Profile Score out of 100
2. Reason for the Score
3. Improved LinkedIn Headline - give 3 options
4. Improved LinkedIn About Section
5. Top 10 LinkedIn Keywords
6. 5 Profile Improvement Suggestions
7. 3 Content Ideas the user can post on LinkedIn
""")


# Convert AI output into plain text
output_parser = StrOutputParser()

# Create LangChain chain
profile_chain = profile_prompt | llm | output_parser


print("\n===== LinkedIn Profile Optimizer AI =====\n")

name = input("Enter your name: ")
role = input("Enter your current role/title: ")
skills = input("Enter your skills separated by comma: ")
target_audience = input("Enter your target audience: ")

print("\nPaste your current LinkedIn About section below.")
print("If you do not have one, type: I do not have an About section yet\n")

about_section = input("LinkedIn About Section: ")

print("\nGenerating your optimized LinkedIn profile...\n")

response = profile_chain.invoke({
    "name": name,
    "role": role,
    "skills": skills,
    "target_audience": target_audience,
    "about_section": about_section
})

print("\n===== AI Optimized LinkedIn Profile =====\n")
print(response)