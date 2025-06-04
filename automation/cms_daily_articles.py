# cms_daily_articles.py

import requests
import json
from datetime import date
from pathlib import Path

# === CONFIG ===
CMS_TOKEN_URL = "https://sandbox.ab2d.cms.gov/token"
CMS_EXPORT_URL = "https://sandbox.ab2d.cms.gov/api/v1/contract/YOUR_CONTRACT_ID/$export"
CMS_CLIENT_ID = "YOUR_CLIENT_ID"
CMS_CLIENT_SECRET = "YOUR_CLIENT_SECRET"

HHS_MEDIA_URL = "https://api.digitalmedia.hhs.gov/api/v2/resources/media.json?max=25&sort=-dateContentPublished"
HHS_HEADERS = {"Accept": "application/json"}


# === CMS OAuth2 Token Fetch ===
def get_cms_token():
    resp = requests.post(
        CMS_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": CMS_CLIENT_ID,
            "client_secret": CMS_CLIENT_SECRET
        },
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


# === CMS Article Export ===
def fetch_cms_articles():
    token = get_cms_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(CMS_EXPORT_URL, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


# === HHS News API Fetch ===
def fetch_hhs_articles():
    response = requests.get(HHS_MEDIA_URL, headers=HHS_HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()


# === Write to daily export ===
def save_json(data, filename_prefix):
    today = date.today().isoformat()
    path = Path(f"exports/{filename_prefix}_{today}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {filename_prefix} data to {path}")


if __name__ == "__main__":
    try:
        cms_data = fetch_cms_articles()
        save_json(cms_data, "cms_articles")
    except Exception as e:
        print(f"❌ CMS API Error: {e}")

    try:
        hhs_data = fetch_hhs_articles()
        save_json(hhs_data, "hhs_api_articles")
    except Exception as e:
        print(f"❌ HHS API Error: {e}")
