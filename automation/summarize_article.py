# summarize_article.py (Ollama-ready, Qwen2-Instruct optimized)

import requests
from parse_articles import parse_article

LLM_API_URL = "http://localhost:11434/api/generate"
PROMPT_TEMPLATE = """You are a professional medical editor. Summarize the following article in 2-3 sentences:\n\n"""

def summarize_with_ollama(article_text):
    payload = {
        "model": "qwen2:7b-instruct",  # ✅ Correct model for Ollama
        "prompt": PROMPT_TEMPLATE + article_text.strip() + "\n\nSummary:",
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 512,
        "stop": ["\n\n", "User:"]
    }
    try:
        response = requests.post(LLM_API_URL, json=payload, timeout=45)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        print(f"[LLM error] {e}")
        return None

def summarize_article(url):
    parsed = parse_article(url)
    if not parsed or not parsed.get("text"):
        print(f"[Parse error] Could not extract article from: {url}")
        return None

    summary = summarize_with_ollama(parsed["text"])
    return {
        "url": url,
        "title": parsed.get("title", "Untitled"),
        "summary": summary or "⚠️ Summary generation failed.",
        "source": parsed.get("source", "Unknown")
    }

if __name__ == "__main__":
    test_url = "https://www.theepochtimes.com/health/example-health-article"
    result = summarize_article(test_url)
    if result:
        print(f"Title: {result['title']}")
        print(f"Source: {result['source']}")
        print(f"Summary:\n{result['summary']}")
