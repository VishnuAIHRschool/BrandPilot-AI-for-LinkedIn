from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Load API key from .env file
load_dotenv()

# Create LLM model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.8
)

# Create prompt template
strategy_prompt = ChatPromptTemplate.from_template("""
You are a LinkedIn personal branding strategist.

Your task is to create a simple and practical LinkedIn content strategy for the user.

Important rules:
- Keep the strategy practical for a beginner.
- Do not suggest fake achievements.
- Do not make it too complex.
- Make the content ideas realistic and easy to post.
- Keep the language professional, clear, and LinkedIn-friendly.

User Details:

Name:
{name}

Current Role / Identity:
{role}

Skills / Interests:
{skills}

Target Audience:
{audience}

Main Goal on LinkedIn:
{goal}

Posting Frequency:
{frequency}

Please generate the following:

1. Personal Brand Positioning Statement
2. 4 Content Pillars
3. Weekly LinkedIn Content Plan
4. 10 LinkedIn Post Ideas
5. Best Post Formats for This User
6. 5 Tips to Grow Consistently on LinkedIn
""")


# Convert AI output into plain text
output_parser = StrOutputParser()

# Create chain
strategy_chain = strategy_prompt | llm | output_parser


print("\n===== LinkedIn Content Strategy Assistant AI =====\n")

name = input("Enter your name: ")
role = input("Enter your current role or identity: ")
skills = input("Enter your skills/interests separated by comma: ")
audience = input("Enter your target audience: ")
goal = input("Enter your LinkedIn goal: ")
frequency = input("How many times do you want to post per week?: ")

print("\nGenerating your LinkedIn content strategy...\n")

response = strategy_chain.invoke({
    "name": name,
    "role": role,
    "skills": skills,
    "audience": audience,
    "goal": goal,
    "frequency": frequency
})

print("\n===== AI Generated LinkedIn Content Strategy =====\n")
print(response)