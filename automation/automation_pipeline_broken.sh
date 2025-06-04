#!/bin/bash

cd /volume1/docker/thedailydose/automation

# === Log start ===
echo -e "\n\n🟢 [$(date '+%Y-%m-%d %H:%M:%S')] Starting automation pipeline..." >> automation.log

# === 1. RSS Feeds Collector ===
echo "📡 Running rss_collector.py..." >> automation.log
/volume1/@appstore/Python3.9/usr/bin/python3 rss_collector.py >> automation.log 2>&1

# === 2. External APIs (HHS Media, NCBI PubMed, CMS) ===
echo "📦 Pulling API content from HHS Media, PubMed, CMS..." >> automation.log

# HHS Media API
curl --silent 'https://api.digitalmedia.hhs.gov/api/v2/resources/media.json?max=25&sort=-dateContentPublished' \
    -H 'Accept: application/json' \
    -o "exports/hhs_media_$(date +%F).json" >> automation.log 2>&1

# NCBI PubMed API
curl --silent 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed&api_key=2692b0e316f89eceb30ba874ad75ed4d2709' \
    -H 'Accept: application/json' \
    -o "exports/ncbi_pubmed_$(date +%F).json" >> automation.log 2>&1

# CMS API Token (Sandbox - Placeholder)
curl --silent --request POST 'https://sandbox.ab2d.cms.gov/tokenQRMbwEhn1AFxBEmA5mA6AbNsZBtQdnOO' \
    -H 'Accept: application/json' \
    -o "exports/cms_token_$(date +%F).json" >> automation.log 2>&1

# === 3. Parse External JSON Files into Enriched Format ===
echo "🧩 Parsing external API content (HHS Media, PubMed, CMS)..." >> automation.log
/volume1/@appstore/Python3.9/usr/bin/python3 parse_external_sources.py >> automation.log 2>&1

# === 4. HHS Article Scraper ===
echo "🗞 Pulling HHS daily articles..." >> automation.log
/volume1/@appstore/Python3.9/usr/bin/python3 hhs_daily_articles.py >> automation.log 2>&1

# === 5. Docker Web Scraper ===
echo "🕷 Running web scraper container..." >> automation.log
curl --silent http://localhost:8082/scrape_all >> automation.log 2>&1

# === 6. Consolidated Parsing Pipeline ===
echo "🧼 Running main parser (main.py)..." >> automation.log
/volume1/@appstore/Python3.9/usr/bin/python3 main.py >> automation.log 2>&1

# === 7. Summarization Process ===
echo "🧠 Summarizing enriched articles..." >> automation.log
/volume1/@appstore/Python3.9/usr/bin/python3 batch_summarizer.py >> automation.log 2>&1

# === 8. Copy Digest for Email ===
today=$(date +%F)
cp exports/daily_digest_${today}.md daily_digest_latest.md
echo "📄 Copied daily digest to daily_digest_latest.md" >> automation.log

# === 9. Email Digest ===
echo "✉️ Sending email digest..." >> automation.log
/volume1/@appstore/Python3.9/usr/bin/python3 send_digest_email.py >> automation.log 2>&1

# === Done ===
echo "✅ Pipeline completed: $(date)" >> automation.log
