import json
import requests
from datetime import date
from pathlib import Path

EXPORTS_DIR = Path("exports")
EXPORTS_DIR.mkdir(exist_ok=True)
today = date.today().isoformat()
PUBMED_API_KEY = "2692b0e316f89eceb30ba874ad75ed4d2709"

# === Fetch & Save HHS Media ===
def fetch_hhs_media():
    url = "https://api.digitalmedia.hhs.gov/api/v2/resources/media.json?max=25&sort=-dateContentPublished"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        with open(EXPORTS_DIR / f"hhs_media_{today}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data.get("results", [])
    except Exception as e:
        print(f"❌ HHS API failed: {e}")
        return []

# === Fetch & Save PubMed ===
def fetch_pubmed_metadata():
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed&api_key={PUBMED_API_KEY}&retmode=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        with open(EXPORTS_DIR / f"ncbi_pubmed_{today}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data.get("einforesult", {}).get("dblist", [])
    except Exception as e:
        print(f"❌ PubMed API failed: {e}")
        return []

# === Fetch & Save CMS Token ===
def fetch_cms_token():
    url = "https://sandbox.ab2d.cms.gov/tokenQRMbwEhn1AFxBEmA5mA6AbNsZBtQdnOO"
    try:
        response = requests.post(url, headers={"Accept": "application/json"}, timeout=10)
        response.raise_for_status()
        data = response.json()
        with open(EXPORTS_DIR / f"cms_token_{today}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data.get("access_token", None)
    except Exception as e:
        print(f"❌ CMS token API failed: {e}")
        return None

# === Merge all into enriched_articles.json ===
def merge_external_articles():
    all_articles = []

    for item in fetch_hhs_media():
        all_articles.append({
            "source": "HHS Media",
            "title": item.get("title"),
            "link": item.get("url"),
            "summary": item.get("description"),
            "published": item.get("dateContentPublished"),
            "authors": [item.get("creator", "HHS")],
            "method": "api"
        })

    for db in fetch_pubmed_metadata():
        all_articles.append({
            "source": "PubMed API",
            "title": db,
            "link": f"https://pubmed.ncbi.nlm.nih.gov/?term={db}",
            "summary": "Metadata category from PubMed DB list",
            "published": today,
            "authors": ["NCBI"],
            "method": "api"
        })

    token = fetch_cms_token()
    all_articles.append({
        "source": "CMS API",
        "title": "CMS Token Retrieval",
        "link": "https://sandbox.ab2d.cms.gov",
        "summary": f"CMS API token retrieved: {token[:10]}..." if token else "Token not available",
        "published": today,
        "authors": ["CMS"],
        "method": "api"
    })

    enriched_path = Path("enriched_articles.json")
    if enriched_path.exists():
        with open(enriched_path, "r+", encoding="utf-8") as f:
            existing = json.load(f)
            f.seek(0)
            json.dump(existing + all_articles, f, indent=2)
            f.truncate()
    else:
        with open(enriched_path, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2)

    print(f"✅ Parsed and merged {len(all_articles)} external articles into enriched_articles.json")

# === Main trigger ===
if __name__ == "__main__":
    merge_external_articles()
