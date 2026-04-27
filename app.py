from urllib.parse import urljoin, urlparse

@app.get("/crawl")
def crawl(url: str, depth: int = 1):
    visited = set()
    queue = [url]
    results = []

    # Simple loop for the crawl
    while queue and len(visited) < depth:
        current_url = queue.pop(0)
        if current_url in visited: continue
        
        try:
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save the page data
            results.append({"url": current_url, "title": soup.title.string if soup.title else "N/A"})
            visited.add(current_url)
            
            # Find all links
            for link in soup.find_all('a', href=True):
                full_url = urljoin(current_url, link['href'])
                # Only crawl links on the same domain
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    if full_url not in visited and full_url not in queue:
                        queue.append(full_url)
                        
        except Exception as e:
            continue # Skip broken links
            
    return {"pages_crawled": len(visited), "data": results}
    
