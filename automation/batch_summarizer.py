from summarize_article import summarize_article
from pathlib import Path
import json
import datetime

# Load the parsed links (from your scraper output or exported file)
with open("parsed_articles.json") as f:
    articles = json.load(f)

summaries = []
for article in articles:
    result = summarize_article(article["url"])
    if result and result["summary"]:
        summaries.append(result)

# Save all summaries to daily Markdown
today = datetime.date.today().isoformat()
out_path = Path(f"exports/daily_digest_{today}.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# 🧠 Daily Healthcare Briefing\n\n")
    for item in summaries:
        f.write(f"### {item['title']}\n")
        f.write(f"**Source:** {item['source']}  \n")
        f.write(f"{item['summary']}\n\n---\n\n")
