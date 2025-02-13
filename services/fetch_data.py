import requests
import urllib.parse
from bs4 import BeautifulSoup

STACKOVERFLOW_API = "https://api.stackexchange.com/2.3/search/advanced"
MEDIUM_SEARCH_URL = "https://medium.com/search?q={query}"

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
    response = requests.get(STACKOVERFLOW_API, params=params)
    if response.status_code == 200:
        items = response.json().get("items", [])
        answers = []
        for i, item in enumerate(items[:5], start=1):
            link = item.get("link", "")
            title = item.get("title", "")
            answers.append(f"{i}. [{title}]({link})")
        return "\n".join(answers) if answers else "No relevant Stack Overflow answers found."
    return "Failed to fetch Stack Overflow answers."

def fetch_medium_answers(query):
    search_url = MEDIUM_SEARCH_URL.format(query=urllib.parse.quote_plus(query))
    return f"1. [Click here to see relevant Medium blog posts]({search_url})"

# def fetch_medium_answers(query):
#     """Fetches the top 5 Medium blog post links based on the query."""
#     print(query)
#     search_url = MEDIUM_SEARCH_URL.format(query=urllib.parse.quote_plus(query))
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(search_url, headers=headers)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
#         articles = soup.find_all("article", limit=5)  # Get top 5 articles
#         print(articles)
#         medium_links = []
        
#         for i, article in enumerate(articles, start=1):
#             link = article.find("a", href=True)
#             if link and link["href"].startswith("/"):
#                 post_url = "https://medium.com" + link["href"]
#                 medium_links.append(f"{i}. [Medium Article]({post_url})")
        
#         return "\n".join(medium_links) if medium_links else "No relevant Medium blog posts found."
#     return "Failed to fetch Medium blog posts."
