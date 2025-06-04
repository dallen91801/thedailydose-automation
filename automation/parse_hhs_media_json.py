# parse_hhs_media_json.py
import requests
import json
from datetime import datetime

API_URL = "https://api.digitalmedia.hhs.gov/api/v2/resources/media.json?max=25&sort=-dateContentPublished"

def fetch_hhs_articles():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []

        for item in data.get("results", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("url"),
                "summary": item.get("description", "No summary provided."),
                "published": item.get("dateContentPublished", datetime.now().isoformat()),
                "source": "HHS Media API"
            })

        with open("exports/hhs_articles.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Saved {len(results)} HHS articles.")

    except Exception as e:
        print(f"❌ HHS fetch failed: {e}")

if __name__ == "__main__":
    fetch_hhs_articles()
