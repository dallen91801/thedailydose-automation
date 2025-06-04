# main.py

import json
import time
from content_scraper import extract_article

# Load articles from rss_collector
with open("rss_articles.json", "r", encoding="utf-8") as f:
    rss_articles = json.load(f)

enriched = []

print(f"🔄 Enriching {len(rss_articles)} articles...\n")

for i, item in enumerate(rss_articles, 1):
    print(f"[{i}/{len(rss_articles)}] {item['title']}")
    try:
        result = extract_article(item["link"])
        item.update(result)
        enriched.append(item)
        time.sleep(1)  # Respectful delay
    except Exception as e:
        print(f"❌ Error: {e}")
        continue

# Save to file
with open("enriched_articles.json", "w", encoding="utf-8") as f:
    json.dump(enriched, f, indent=2, ensure_ascii=False)

print(f"\n✅ Done. {len(enriched)} articles saved to enriched_articles.json")
