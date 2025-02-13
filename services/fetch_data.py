import requests
import urllib.parse
import streamlit as st
from bs4 import BeautifulSoup

STACKOVERFLOW_API = "https://api.stackexchange.com/2.3/search/advanced"
MEDIUM_SEARCH_URL = "https://medium.com/search?q={query}"

@st.cache_data
def fetch_stackoverflow_answers(query):
    """Fetches top Stack Overflow answers for a given query."""
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "filter": "!9_bDE(fI5",
        "pagesize": 5  # Limit results to 5
    }
    
    try:
        response = requests.get(STACKOVERFLOW_API, params=params, timeout=5)
        response.raise_for_status()
        data = response.json().get("items", [])

        if not data:
            return "No relevant Stack Overflow answers found."

        return "\n".join(
            f"{i+1}. [{item['title']}]({item['link']})"
            for i, item in enumerate(data[:5])
        )
    except requests.RequestException:
        return "Failed to fetch Stack Overflow answers."

@st.cache_data
def fetch_medium_answers(query):
    """Returns a search link for Medium articles based on the query."""
    return f"1. [Click here to see relevant Medium blog posts]({MEDIUM_SEARCH_URL.format(query=urllib.parse.quote_plus(query))})"

# Uncomment below to fetch actual Medium article links via web scraping (if necessary)
# @st.cache_data
# def fetch_medium_answers(query):
#     """Fetches the top 5 Medium blog post links based on the query."""
#     search_url = MEDIUM_SEARCH_URL.format(query=urllib.parse.quote_plus(query))
#     headers = {"User-Agent": "Mozilla/5.0"}
    
#     try:
#         response = requests.get(search_url, headers=headers, timeout=5)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         articles = soup.find_all("article", limit=5)
#         medium_links = [
#             f"{i+1}. [Medium Article](https://medium.com{a['href']})"
#             for i, a in enumerate(
#                 [article.find("a", href=True) for article in articles]
#             ) if a and a["href"].startswith("/")
#         ]
        
#         return "\n".join(medium_links) if medium_links else "No relevant Medium blog posts found."
#     except requests.RequestException:
#         return "Failed to fetch Medium blog posts."
