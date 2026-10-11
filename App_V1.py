import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document

load_dotenv()

# Step 1: State
class State(TypedDict):
    resume: str
    analysis: str
    feedback: str
    cnt: int

# Step 2: LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# Step 3: Node Creation
def analyze_resume(state):
    prompt = f"""
        Analyze the following resume and provide detailed improvement suggestions.
        Focus on: 
            - Skills
            - Projects
            - Experience
            - Structure
            - Impact
        Resume:
            {state['resume']}
        Give atleast 5 strong actionable suggestions.
    """

    if state["feedback"]:
        prompt += f"\nPrevious feedback: {state['feedback']}"

    response = llm.invoke(prompt)
    return {
        "analysis": response.content,
        "cnt": state["cnt"]+1
    }

def review_analysis(state):
    text = state["analysis"]
    if len(text)<200:
        return {
            "feedback": "Too short. Add more details."
        }
    if "skills" not in text:
        return {
            "feedback": "Skills missing. Add skills too. "
        }
    return {
        "feedback": "good"
    }

def should_continue(state):
    if state["feedback"]=="good" or state["cnt"]>=3:
        return  "end"
    return "retry"

# Step 4: Build Graph 
builder = StateGraph(State)

builder.add_node("analyze", analyze_resume)
builder.add_node("review", review_analysis)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "review")
builder.add_conditional_edges(
    "review",
    should_continue,
    {
        "retry": "analyze",
        "end": END
    }
)

graph = builder.compile()

# Step 6: Streamlit UI

st.set_page_config(page_title="AI Resume Analyzer",layout="centered")
st.title("🤖 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your reume(PDF, Word, TXT)", type=["pdf", "docx", "txt"])

resume_text = ""

if uploaded_file is not None:
    if uploaded_file.type=="application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        resume_text += text
    elif uploaded_file.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        resume_text = "\n".join(text)
    elif uploaded_file.type=="text/plain":
        resume_text = uploaded_file.read().decode("utf-8")

    st.success("Resume Uploaded Successfully")

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please upload a resume first")
    else:
        with st.spinner("Analyzing resume..."):
            result = graph.invoke(
                {
                    "resume":resume_text,
                    "analysis": "",
                    "feedback": "",
                    "cnt": 0
                }
            )
        st.success("Analysis Completed")
        st.subheader("Suggestions")
        st.write(result["analysis"])
        st.subheader("Attempts used")
        st.write(result["cnt"])