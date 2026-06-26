import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load API key from .env file
load_dotenv()

# Create the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# Create a prompt template
prompt = ChatPromptTemplate.from_template(
    """
    You are a LinkedIn personal branding expert.

    Create 3 strong LinkedIn headline options for this person:

    Role: {role}
    Skills: {skills}
    Target Audience: {audience}

    Keep each headline professional, clear, and powerful.
    """
)

# Connect prompt + LLM
chain = prompt | llm

# Run the chain
response = chain.invoke({
    "role": "Gen AI Learner",
    "skills": "Python, LangChain, Streamlit, Prompt Engineering",
    "audience": "Recruiters, AI professionals, and business leaders"
})

print(response.content)