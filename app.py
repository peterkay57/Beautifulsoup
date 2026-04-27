from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

# This is the line that fixes your NameError
app = FastAPI(title="SmartLinker Crawler")

@app.get("/")
def root():
    return {"message": "Crawler is active."}

@app.get("/crawl")
def crawl(url: str, depth: int = 5):
    visited = set()
    queue = [url]
    results = []

    while queue and len(visited) < depth:
        current_url = queue.pop(0)
        if current_url in visited: continue
        
        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results.append({"url": current_url, "title": soup.title.string if soup.title else "N/A"})
            visited.add(current_url)
            
            for link in soup.find_all('a', href=True):
                full_url = urljoin(current_url, link['href'])
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    if full_url not in visited and full_url not in queue:
                        queue.append(full_url)
        except Exception as e:
            continue
            
    return {"pages_crawled": len(visited), "data": results}
