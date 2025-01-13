import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

# SerpAPI key (replace with your actual key)
SERPAPI_KEY = 'API'

def search_and_scrape(query):
    # Use SerpAPI to search the query
    params = {
        'q': query,
        'api_key': SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # Scrape the first 10 URLs
    scraped_data = []
    for result in results.get("organic_results", [])[:10]:
        url = result.get("link")
        page_content = scrape_page(url)
        if page_content:
            scraped_data.append(page_content)

    return scraped_data

def scrape_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to get the main content based on common tags (p, div, article, section)
        content = []

        # Find all relevant text content from different tags
        for tag in ['p', 'div', 'section', 'article']:
            elements = soup.find_all(tag)
            for elem in elements:
                text = elem.get_text()
                if text.strip():  # Only include non-empty text
                    content.append(text.strip())

        # Join all content into a single string
        return " ".join(content)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
