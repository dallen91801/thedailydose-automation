import json, gzip, shutil, requests
from multiprocessing import Pool, cpu_count
from tenacity import retry, stop_after_attempt, wait_fixed
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen:7b"

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def summarize_article(article):
    prompt = f"Summarize the following article in 8th grade reading level:

{article.get('content', article.get('summary', ''))}"
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return {
            "title": article["title"],
            "summary": data.get("response", "").strip()
        }
    except Exception as e:
        raise RuntimeError(f"Ollama error: {str(e)}")

def process_article(article):
    try:
        return summarize_article(article)
    except Exception as e:
        return {"title": article.get("title", "UNKNOWN"), "error": str(e)}

with open("exports/parsed_articles.json", "r") as f:
    articles = json.load(f)

with Pool(cpu_count()) as pool:
    results = pool.map(process_article, articles)

with open("exports/summarized_articles.json", "w") as f:
    json.dump(results, f, indent=2)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open("exports/parsed_articles.json", "rb") as f_in:
    with gzip.open(f"exports/parsed_articles_{timestamp}.json.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
