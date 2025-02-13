import streamlit as st
import concurrent.futures
from services.deepseek import generate_deepseek_response, refine_search_query
from services.fetch_data import fetch_stackoverflow_answers, fetch_medium_answers
from templates.response_template import TEMPLATE

st.title("DeepSeeker with Stack Overflow & Medium Search")
question = st.text_input("Enter your coding question:")

if question:
    st.chat_message("user").write(question)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_deepseek = executor.submit(generate_deepseek_response, question)
        future_query = executor.submit(refine_search_query, question)
        
        refined_query = future_query.result()
        print("Refined Search Query:", refined_query)  # Debugging output
        
        future_stackoverflow = executor.submit(fetch_stackoverflow_answers, refined_query)
        future_medium = executor.submit(fetch_medium_answers, refined_query)
        
        deepseek_response = future_deepseek.result()
        stackoverflow_answers = future_stackoverflow.result()
        medium_answers = future_medium.result()
    
    final_response = TEMPLATE.format(
        deepseek_response=deepseek_response,
        stackoverflow_answers=stackoverflow_answers,
        medium_answers=medium_answers
    )
    
    st.chat_message("assistant").write(final_response)
