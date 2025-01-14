import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import re
from dotenv import load_dotenv
import os

load_dotenv()

SERPAPI_KEY = os.getenv('SERP_API')

def search_and_scrape(query):
    params = {
        'q': query + " documentation", 
        'api_key': SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    scraped_data = []
    
    if "answer_box" in results:
        snippet = results["answer_box"]
        
        if "snippet" in snippet:
            scraped_data.append(snippet["snippet"])
        elif "list" in snippet:
            scraped_data.append("\n".join(snippet["list"]))
        elif "table" in snippet:
            table_data = []
            for row in snippet["table"]:
                table_data.append(" | ".join(row))
            scraped_data.append("\n".join(table_data))
            
        if "link" in snippet:
            page_content = scrape_page(snippet["link"])
            if page_content:
                scraped_data.append(page_content[:20000])
                
    if not scraped_data:
        for result in results.get("organic_results", [])[:1]:
            url = result.get("link")
            print(url)
            page_content = scrape_page(url)
            if page_content:
                scraped_data.append(page_content[:20000])
    
    return scraped_data


def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')

        content = []

        for tag in ['p', 'div', 'section', 'article']:
            elements = soup.find_all(tag)
            for elem in elements:
                text = elem.get_text()
                if text.strip(): 
                    
                    cleaned_text = clean_text(text.strip())
                    if cleaned_text:  
                        content.append(cleaned_text)


        return " ".join(content)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def clean_text(text):
    """
    Cleans the input text by:
    - Removing extra spaces, newlines, and tabs.
    - Stripping HTML entities (e.g., &nbsp;, &amp;).
    - Removing special characters (except punctuation).
    - Reducing multiple spaces to a single space.
    """
    text = re.sub(r'&[a-zA-Z0-9#]+;', '', text)

    text = re.sub(r'[^a-zA-Z0-9\s\.,!?\'"()-]', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()
