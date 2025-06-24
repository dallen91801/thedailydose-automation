import json
from datetime import date

with open("exports/tagged_articles.json", "r") as f:
    articles = json.load(f)

today = date.today().isoformat()
with open(f"exports/daily_digest_{today}.md", "w") as f:
    f.write(f"# The Daily Dose — {today}\n\n")
    for art in articles:
        f.write(f"## {art['title']}\n")
        f.write(f"**Emotion:** {art.get('emotion', 'N/A')}\n\n")
        f.write(f"{art.get('summary', '')}\n\n")
