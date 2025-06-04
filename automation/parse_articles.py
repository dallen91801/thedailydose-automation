# parse_articles.py

import requests
from readability import Document
from trafilatura import fetch_url, extract
from bs4 import BeautifulSoup

def parse_with_readability(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        doc = Document(response.text)
        title = doc.short_title()
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, 'html.parser')
        text = soup.get_text(separator='\n').strip()
        return {
            "source": "readability-lxml",
            "title": title,
            "text": text
        }
    except Exception as e:
        print(f"[Readability failed] {url} → {e}")
        return None

def parse_with_trafilatura(url):
    try:
        html = fetch_url(url)
        if html:
            result = extract(html, include_comments=False, include_tables=False, output_format='json')
            if result:
                import json
                data = json.loads(result)
                return {
                    "source": "trafilatura",
                    "title": data.get("title"),
                    "text": data.get("text")
                }
    except Exception as e:
        print(f"[Trafilatura failed] {url} → {e}")
    return None

def parse_article(url):
    result = parse_with_readability(url)
    if result:
        return result
    return parse_with_trafilatura(url)

# Example usage (manual test)
if __name__ == "__main__":
    import json

    with open("enriched_articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)

    for i, article in enumerate(articles[:50], start=1):  # Test first 50 articles
        url = article.get("link")
        print(f"\n=== [{i}] {url} ===\n")
        parsed = parse_article(url)
        if parsed:
            print(f"✅ Parsed with: {parsed['source']}")
            print(f"📌 Title: {parsed['title']}")
            print(f"📄 Snippet:\n{parsed['text'][:500]}...\n")
        else:
            print("❌ Failed to parse.\n")

