# generate_html_digest.py

import json
from pathlib import Path
from datetime import date

EXPORTS_DIR = Path("exports")
today = date.today().isoformat()
html_file = EXPORTS_DIR / f"daily_digest_{today}.html"
source_file = Path("enriched_articles.json")

def group_by_source(articles):
    grouped = {}
    for item in articles:
        src = item.get("source", "Unknown Source")
        grouped.setdefault(src, []).append(item)
    return grouped

def export_html(results, today):
    EXPORTS_DIR.mkdir(exist_ok=True)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Daily Dose – {today}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; line-height: 1.6; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ border-bottom: 1px solid #ccc; margin-top: 2em; }}
        .article {{ margin-bottom: 1.5em; }}
        .meta {{ font-size: 0.9em; color: #555; }}
        .summary {{ margin-top: 0.5em; }}
    </style>
</head>
<body>
<h1>The Daily Dose – {today}</h1>
""")
        for source, articles in results.items():
            f.write(f"<h2>{source}</h2>\n")
            for art in articles:
                title = art.get("title", "Untitled")
                link = art.get("link", "#")
                summary = art.get("summary", "No summary provided.")
                published = art.get("published", "N/A")
                f.write(f"""<div class="article">
    <a href="{link}" target="_blank"><strong>{title}</strong></a>
    <div class="meta">Published: {published}</div>
    <div class="summary">{summary}</div>
</div>\n""")
        f.write("</body>\n</html>")

    print(f"✅ HTML digest written to {html_file}")

if __name__ == "__main__":
    if not source_file.exists():
        print(f"❌ Missing source file: {source_file}")
        exit(1)

    with open(source_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not isinstance(articles, list) or not articles:
        print("❌ No articles found in enriched_articles.json")
        exit(1)

    grouped_results = group_by_source(articles)
    export_html(grouped_results, today)
