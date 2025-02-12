import streamlit as st
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

STACKOVERFLOW_API = "https://api.stackexchange.com/2.3/search/advanced"
QUORA_SEARCH_URL = "https://www.quora.com/search?q={query}"

# Template for AI-generated response
template = """
You are an AI assistant helping users with coding questions. Below is the response generated by DeepSeek followed by relevant answers from Stack Overflow and Quora.

## DeepSeek Response:
{deepseek_response}

## Stack Overflow Answers:
{stackoverflow_answers}

## Quora Answers:
{quora_answers}
"""

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
vector_store = InMemoryVectorStore(embeddings)
model = OllamaLLM(model="deepseek-r1:1.5b")

def fetch_stackoverflow_answers(query):
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "filter": "!9_bDE(fI5"
    }
    response = requests.get(STACKOVERFLOW_API, params=params)
    if response.status_code == 200:
        items = response.json().get("items", [])
        answers = []
        for item in items[:5]:  # Fetch top 5 answers
            link = item.get("link", "")
            title = item.get("title", "")
            answers.append(f"[{title}]({link})")
        return "\n".join(answers)
    return "No relevant Stack Overflow answers found."

def fetch_quora_answers(query):
    search_url = QUORA_SEARCH_URL.format(query=query.replace(" ", "+"))
    return f"[Click here to see relevant Quora discussions]({search_url})"

def generate_deepseek_response(question):
    prompt = ChatPromptTemplate.from_template("Question: {question}\nAnswer:")
    chain = prompt | model
    return chain.invoke({"question": question})

st.title("DeepSeeker with Stack Overflow and Quora Answers")
question = st.text_input("Enter your coding question:")

if question:
    st.chat_message("user").write(question)
    deepseek_response = generate_deepseek_response(question)
    stackoverflow_answers = fetch_stackoverflow_answers(question)
    quora_answers = fetch_quora_answers(question)
    final_response = template.format(deepseek_response=deepseek_response, stackoverflow_answers=stackoverflow_answers, quora_answers=quora_answers)
    st.chat_message("assistant").write(final_response)
