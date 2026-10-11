# AI Resume Analyzer

An AI-powered app that analyzes PDF and DOCX resumes and gives actionable feedback. Built with LangGraph, LangChain, OpenAI and Streamlit.

## Features
- Upload a resume in PDF or DOCX format
- Get clear, actionable feedback to improve it
- LangGraph workflow with separate analysis and review steps
- Conditional edges and a bounded retry loop to improve output quality
- Simple web interface built with Streamlit

## How It Works
1. The resume text is extracted from the uploaded file
2. An analysis step generates feedback using the LLM
3. A review step checks the feedback quality
4. If the review fails, the workflow retries a limited number of times
5. The final feedback is shown in the app

## Tech Stack
Python, Streamlit, LangGraph, LangChain, OpenAI API, PyPDFLoader, python-docx

## Setup
1. Clone the repo
   git clone https://github.com/prabal-chaurasia/AI-Resume-Analyzer.git
   cd AI-Resume-Analyzer
2. Install dependencies
   pip install -r requirements.txt
3. Create a `.env` file and add your key
   OPENAI_API_KEY=your_key_here
4. Run the app
   streamlit run App_V1.py
