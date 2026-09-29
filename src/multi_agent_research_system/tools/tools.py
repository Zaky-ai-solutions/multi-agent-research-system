from langchain.tools import tool
from dotenv import load_dotenv
import os
import requests 
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import re 
import trafilatura

load_dotenv() 

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent reliable information on a topic
    , Returns Titles, URLs and contents
    """
    results = tavily.search(query= query,
                            max_results=5,)

    out = []

    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\n Snippet: {r['content'][:300]}\n")

    return "\n---------------------------------\n".join(out)

@tool
def scrape_url(url:str)->str:
    """
    scrape and extract clean readable content from a url.
    uses multiple extraction strategies for better reliability.
    """
    headers = {
        "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.3"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referrer": "https://www.google.com/",
    }
    try:
        response= requests.get(
            url, 
            headers=headers,
            timeout=15
                  )
        response.raise_for_status()  # Raise an error for bad responses
        html = response.text
        # ________________________________________________
        # Strategy 1 -> trafilatura (BEST for articles/logs)
        # ________________________________________________
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )
        if extracted and len(extracted.strip())>200:
            cleaned = re.sub(r'\s+', ' ', extracted)
            return cleaned[:5000]
        # ──────────────────────────────────────────────────
        # Strategy 2 → readability
        # ──────────────────────────────────────────────────
        doc = Document(html)
        clean_html = doc.summary()
        soup = BeautifulSoup(clean_html, 'html.parser')
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text and len(text.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', text)
            return cleaned[:5000]
        # ──────────────────────────────────────────────────
        # Strategy 3 → fallback full page extraction
        # ──────────────────────────────────────────────────
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        cleaned = re.sub(r'\s+', ' ', text)
        if cleaned:
            return cleaned[:5000]
        return "Could not extract meaningful content from the page."
    
    
    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
 


