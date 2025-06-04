import requests
from newspaper import Article
from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
import json

# Load state Medicaid/HIE URLs
with open("medicaid_hie_urls.json", "r", encoding="utf-8") as f:
    state_urls = json.load(f)

# Optional NPI header (only if required by the site)
headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": "NPI_ID=1386441038"  # Only relevant if site requires NPI auth
}

# Extract using newspaper3k
def extract_article(url):
    try:
        print(f"🔍 Trying newspaper3k: {url}")
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "source": urlparse(url).netloc,
            "method": "newspaper3k"
        }
    except Exception as e:
        print(f"❌ newspaper3k failed: {e}")
        print("🔁 Trying Playwright fallback...")
        return asyncio.run(extract_with_playwright(url))

# Playwright fallback for JavaScript-heavy sites
async def extract_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout=30000)
            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")

            paragraphs = soup.find_all("p")
            content = "\n".join(p.get_text() for p in paragraphs if len(p.get_text()) > 40)

            title = soup.title.string.strip() if soup.title else "Untitled"
            return {
                "title": title,
                "text": content.strip(),
                "authors": [],
                "source": urlparse(url).netloc,
                "method": "playwright"
            }
        except Exception as e:
            return {
                "title": "Error loading",
                "text": "",
                "authors": [],
                "source": url,
                "method": f"playwright-fail: {e}"
            }
        finally:
            await browser.close()

# Main loop: iterate and extract from each site
if __name__ == "__main__":
    for url in state_urls:
        print("\n" + "=" * 80)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Request failed for {url}: {e}")
            continue

        result = extract_article(url)
        print(f"✅ {result['title']} ({result['method']})")
