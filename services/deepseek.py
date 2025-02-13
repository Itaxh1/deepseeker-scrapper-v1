from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(model="deepseek-r1:1.5b")

def generate_deepseek_response(question):
    """Generates AI-based coding responses using DeepSeek."""
    prompt = ChatPromptTemplate.from_template("Question: {question}\nAnswer:")
    chain = prompt | model
    return chain.invoke({"question": question})

def refine_search_query(question):
    """Uses DeepSeek to generate a concise search query (max 300 chars)."""
    prompt = ChatPromptTemplate.from_template("""
    Given the following coding question:
    {question}
    
    Generate the best possible search query under 300 characters, optimized for finding relevant answers on Stack Overflow and Medium.
    Return only the query without explanations, examples, or any extra text.
    """)
    chain = prompt | model
    response = chain.invoke({"question": question}).strip()
    
    # Extract the first valid line that is not a <think> tag or explanation
    refined_query = response.split("\n")[0][:300]
    if "<think>" in refined_query.lower() or len(refined_query) < 5:
        refined_query = question  # Use the original question if DeepSeek fails
    
    return refined_query
