import json
from pathlib import Path
from datetime import date

EXPORTS_DIR = Path("exports")
today = date.today().isoformat()
digest_file = EXPORTS_DIR / f"daily_digest_{today}.md"
source_file = Path("enriched_articles.json")


def group_by_source(articles):
    grouped = {}
    for item in articles:
        src = item.get("source", "Unknown Source")
        grouped.setdefault(src, []).append(item)
    return grouped


def export_markdown(results, today):
    EXPORTS_DIR.mkdir(exist_ok=True)
    with open(digest_file, "w", encoding="utf-8") as f:
        f.write(f"# The Daily Dose – {today}\n\n")
        for source, articles in results.items():
            f.write(f"## {source}\n\n")
            for art in articles:
                f.write(f"### [{art.get('title')}]({art.get('link')})\n\n")
                f.write(f"{art.get('summary', 'No summary provided.')}\n\n")
                f.write(f"*Published:* {art.get('published', 'N/A')}\n\n")
            f.write("\n---\n\n")
    print(f"✅ Markdown digest written to {digest_file}")


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
    export_markdown(grouped_results, today)
