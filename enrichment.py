import requests
from bs4 import BeautifulSoup
from functools import lru_cache

@lru_cache(maxsize=200)
def scrape_website(url):
    try:
        if not url.startswith("http"):
            url = "https://" + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        res = requests.get(url, timeout=7, headers=headers)
        
        # Ensure we are using the correct character encoding
        res.encoding = res.apparent_encoding 
        
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""
        meta = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta.get("content", "") if meta else ""

        for script in soup(["script", "style", "noscript"]):
            script.extract()

        # Extract text and clean out weird invisible characters
        raw_text = soup.get_text(" ", strip=True)[:3000]
        
        # THIS IS THE FIX: Forces the text to only use standard readable characters
        clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')

        return {
            "title": title,
            "meta_description": meta_desc,
            "content": clean_text
        }

    except Exception as e:
        print(f"Scraping Error: {e}")
        return {"title": "", "meta_description": "", "content": ""}