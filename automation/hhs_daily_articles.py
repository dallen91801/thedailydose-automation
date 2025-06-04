import requests
import json
import datetime
import os

# HHS API endpoint
URL = "https://api.digitalmedia.hhs.gov/api/v2/resources/media.json"
PARAMS = {
    "max": 25,
    "sort": "-dateContentPublished",
    "format": "json",
    "active": "true"
}
HEADERS = {
    "Accept": "application/json"
}

# Make request
response = requests.get(URL, headers=HEADERS, params=PARAMS)
response.raise_for_status()  # throw if error

data = response.json()

# Save raw JSON
today = datetime.date.today().isoformat()
json_filename = f"hhs_articles_{today}.json"

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"✅ Raw JSON saved to {json_filename}")

# Optional: Generate basic Markdown
md_filename = f"hhs_articles_{today}.md"
entries = []

for item in data.get("results", []):
    if item.get("mediaType") != "Html":
        continue

    title = item.get("name", "Untitled")
    description = item.get("description", "")
    source_url = item.get("sourceUrl", "#")
    published = item.get("dateContentPublished", "")[:10]

    entry_md = f"""\
### [{title}]({source_url})
**Published:** {published}

{description}

---
"""
    entries.append(entry_md)

if entries:
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write("# 📰 Latest HHS Articles\n\n")
        f.writelines(entries)
    print(f"✅ Markdown file saved to {md_filename}")
else:
    print("⚠️ No HTML articles found.")

