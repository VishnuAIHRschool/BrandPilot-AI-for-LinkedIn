# BrandPilot AI for LinkedIn

BrandPilot AI is a Generative AI web application built using **Python, LangChain, OpenAI, and Streamlit**.

It helps users improve their LinkedIn profile, generate professional LinkedIn posts, and create a simple content strategy. The app uses user-provided profile details, pasted content, or uploaded PDF documents such as a resume or LinkedIn profile PDF.

## Project Overview

Many professionals struggle to write a strong LinkedIn profile, create consistent posts, and build a clear personal brand. BrandPilot AI solves this by acting as an AI-powered LinkedIn personal branding assistant.

The application includes three main modules:

1. **Profile Intelligence**
2. **Post Studio**
3. **Content Strategy Planner**

## Features

### 1. Profile Intelligence

Users can enter LinkedIn profile details manually or upload a resume/profile PDF.

The AI generates:

* Profile strength score
* Reason for the score
* Missing information checklist
* Improved LinkedIn headline options
* Optimized About section
* Experience section improvement suggestions
* LinkedIn keywords
* Featured section suggestions
* Profile banner tagline ideas
* LinkedIn post ideas based on the profile

### 2. Post Studio

Users can enter a topic, tone, target audience, and post goal.

The AI generates:

* LinkedIn post
* Strong hook
* Call-to-action
* Relevant hashtags

### 3. Content Strategy Planner

Users can enter their role, skills, audience, goal, and posting frequency.

The AI generates:

* Personal brand positioning statement
* Content pillars
* Weekly LinkedIn content plan
* Post ideas
* Recommended post formats
* Growth tips

## Tech Stack

* Python
* Streamlit
* LangChain
* OpenAI
* python-dotenv
* pypdf

## LangChain Concepts Used

This project uses the following LangChain concepts:

* Chat model integration
* Prompt templates
* Chains
* Output parser
* LLM-based text generation

Core flow:

```text
User Input
   ↓
Prompt Template
   ↓
OpenAI Chat Model
   ↓
Output Parser
   ↓
Generated Result
```

## Project Structure

```text
LinkedIn-BrandPilot-AI
│
├── app.py
├── profile_optimizer.py
├── post_generator.py
├── content_strategy.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/VishnuAIHRschool/LinkedIn-BrandPilot-AI.git
cd LinkedIn-BrandPilot-AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

### 5. Create `.env` File

Create a `.env` file in the project folder and add your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## Important Note

This application does not scrape LinkedIn, automate LinkedIn actions, or directly read LinkedIn profiles from URLs.

The LinkedIn profile URL field is used only as an optional reference. The app works with:

* User-entered profile details
* Pasted LinkedIn About section
* Pasted experience or project details
* User-uploaded PDF documents

## Project Type

```text
Project Type: Generative AI Application
Framework: LangChain
Frontend: Streamlit
LLM: OpenAI
Use Case: LinkedIn personal branding and content generation
Technique Used: Prompt Templates, LLM Chains, Output Parsing, PDF Text Extraction
```

## Future Enhancements

* Add resume-to-LinkedIn profile converter
* Add LinkedIn carousel content generator
* Add content calendar export to Excel
* Add user login
* Add database to save generated outputs
* Add RAG-based profile knowledge assistant

## Disclaimer

This project is created for learning and educational purposes. It is not affiliated with LinkedIn. The app does not scrape, automate, or modify LinkedIn profiles.
