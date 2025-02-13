from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import re
import streamlit as st

# Precompile regex for filtering responses
THINK_PATTERN = re.compile(r"<think>.*?</think>", re.DOTALL)

@st.cache_resource
def load_model():
    """Lazy-loads the DeepSeek model only when needed."""
    return OllamaLLM(model="deepseek-r1:1.5b")

def clean_text(text: str) -> str:
    """Removes <think> tags and trims whitespace."""
    return THINK_PATTERN.sub("", text).strip() or "No valid response."

@st.cache_data
def fetch_deepseek_data(question: str):
    """Runs a single DeepSeek call to get both the AI response and search query in one step."""
    model = load_model()
    
    prompt = ChatPromptTemplate.from_template("""
        Given the following coding question:
        {question}
        
        1. Provide the best AI-generated answer.
        2. Generate a concise search query (under 300 characters) for Stack Overflow & Medium.

        Format: 
        <answer>
        [AI Response Here]
        </answer>
        <query>
        [Search Query Here]
        </query>
    """)

    response = (prompt | model).invoke({"question": question}).strip()

    # Extract AI response and search query
    answer_match = re.search(r"<answer>(.*?)</answer>", response, re.DOTALL)
    query_match = re.search(r"<query>(.*?)</query>", response, re.DOTALL)

    ai_response = clean_text(answer_match.group(1)) if answer_match else "No valid response."
    search_query = query_match.group(1).strip()[:300] if query_match else question

    return ai_response, search_query
