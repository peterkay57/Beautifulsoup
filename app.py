from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI(title="BeautifulSoup API", description="Extract data from any website")

# ========== WEB INTERFACE (UI) ENDPOINT ==========
@app.get("/ui", response_class=HTMLResponse)
async def ui():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())
# ========== END OF UI ENDPOINT ==========

# ========== SCRAPE ENDPOINT ==========
@app.get("/scrape")
def scrape(url: str):
    """
    Extract text from any website URL
    Example: /scrape?url=https://example.com
    """
    try:
        # Fetch the webpage
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style tags
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Get title
        title = soup.find('title')
        title_text = title.text if title else "No title found"
        
        return {
            "url": url,
            "title": title_text,
            "content": text[:5000],  # First 5000 characters
            "content_length": len(text),
            "success": True
        }
    
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "success": False
        }

# ========== ROOT ENDPOINT ==========
@app.get("/")
def root():
    return {"message": "BeautifulSoup API is running. Use /scrape?url=YOUR_URL or go to /ui for web interface"}

# ========== HEALTH ENDPOINT ==========
@app.get("/health")
def health():
    return {"status": "ok"}
