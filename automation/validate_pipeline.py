# validate_pipeline.py

import json
from datetime import date
from pathlib import Path

REQUIRED_SOURCES = {
    "rss": ["KFF", "HealthAffairs", "NEJM", "JAMA", "CMS", "CDC", "NIH"],
    "scraped": ["STATNews", "EndpointsNews", "FiercePharma", "ModernHealthcare", "MedPageToday", "Reuters", "BioPharmaDive", "Healio"]
}

def normalize(source_name):
    return source_name.lower().replace(" ", "")

def check_sources(file_path):
    if not Path(file_path).exists():
        return [], f"❌ File not found: {file_path}"
    
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            return [], f"❌ Invalid JSON: {e}"

    sources_seen = {normalize(item.get("source", "")) for item in data}
    missing = []

    for category, sources in REQUIRED_SOURCES.items():
        for source in sources:
            if normalize(source) not in sources_seen:
                missing.append(f"{source} ({category})")
    
    return missing, "✅ Source check complete."

if __name__ == "__main__":
    today = date.today().isoformat()
    input_file = f"enriched_articles.json"  # could later parameterize this
    missing, msg = check_sources(input_file)
    print(msg)
    if missing:
        print("⚠️ Missing expected sources:")
        for src in missing:
            print(f" - {src}")
    else:
        print("🎉 All expected sources are present.")
