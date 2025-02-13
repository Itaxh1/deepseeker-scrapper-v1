import streamlit as st
from services.deepseek import fetch_deepseek_data
from services.fetch_data import fetch_stackoverflow_answers, fetch_medium_answers
from templates.response_template import TEMPLATE

st.title("DeepSeeker with Stack Overflow & Medium Search")

question = st.text_input("Enter your coding question:")

if question:
    st.chat_message("user").write(question)

    # Get AI-generated response and refined search query in one call
    deepseek_response, refined_query = fetch_deepseek_data(question)

    # Fetch Stack Overflow and Medium answers
    stackoverflow_answers = fetch_stackoverflow_answers(refined_query)
    medium_answers = fetch_medium_answers(refined_query)

    final_response = TEMPLATE.format(
        deepseek_response=deepseek_response,
        stackoverflow_answers=stackoverflow_answers,
        medium_answers=medium_answers
    )

    st.chat_message("assistant").write(final_response)
