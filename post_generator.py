from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Load API key from .env
load_dotenv()

# Create LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.8
)

# Create prompt template
post_prompt = ChatPromptTemplate.from_template("""
You are a professional LinkedIn content writer.

Create a high-quality LinkedIn post based on the user's input.

Important rules:
- Do not make the post too long.
- Make the opening line strong.
- Use simple professional language.
- Make it feel human, not robotic.
- Avoid fake claims.
- Add line breaks for readability.
- Add a clear call-to-action at the end.
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

Please generate:

1. LinkedIn Post
2. Suggested Hook
3. Suggested CTA
4. Relevant Hashtags
""")


# Output parser
output_parser = StrOutputParser()

# Create chain
post_chain = post_prompt | llm | output_parser


print("\n===== LinkedIn Post Generator AI =====\n")

topic = input("Enter post topic: ")
tone = input("Enter tone example: professional / inspiring / storytelling / bold: ")
audience = input("Enter target audience: ")
goal = input("Enter post goal example: educate / inspire / share learning / promote project: ")

print("\nGenerating your LinkedIn post...\n")

response = post_chain.invoke({
    "topic": topic,
    "tone": tone,
    "audience": audience,
    "goal": goal
})

print("\n===== AI Generated LinkedIn Post =====\n")
print(response)