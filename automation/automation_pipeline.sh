#!/bin/bash

cd /volume1/docker/thedailydose/automation

echo ""
echo "[START] $(date '+%Y-%m-%d %H:%M:%S') Starting automation pipeline..." >> automation.log

# Step 1: RSS feeds
/volume1/@appstore/Python3.9/usr/bin/python3 rss_collector.py >> automation.log 2>&1

# Step 2: API fetches
curl --silent "https://api.digitalmedia.hhs.gov/api/v2/resources/media.json?max=25&sort=-dateContentPublished" \
  -H "Accept: application/json" \
  -o "exports/hhs_media_$(date +%F).json" >> automation.log 2>&1

curl --silent "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed&api_key=2692b0e316f89eceb30ba874ad75ed4d2709" \
  -H "Accept: application/json" \
  -o "exports/ncbi_pubmed_$(date +%F).json" >> automation.log 2>&1

curl --silent --request POST "https://sandbox.ab2d.cms.gov/tokenQRMbwEhn1AFxBEmA5mA6AbNsZBtQdnOO" \
  -H "Accept: application/json" \
  -o "exports/cms_token_$(date +%F).json" >> automation.log 2>&1

# Step 3: Parse external data
/volume1/@appstore/Python3.9/usr/bin/python3 parse_external_sources.py >> automation.log 2>&1

# Step 4: HHS article scrape
/volume1/@appstore/Python3.9/usr/bin/python3 hhs_daily_articles.py >> automation.log 2>&1

# Step 5: Web scraper via Docker
curl --silent http://localhost:8082/scrape_all >> automation.log 2>&1

# Step 6: Main processing
/volume1/@appstore/Python3.9/usr/bin/python3 main.py >> automation.log 2>&1

# Step 7: Summarize content
/volume1/@appstore/Python3.9/usr/bin/python3 batch_summarizer.py >> automation.log 2>&1

# Step 8: Copy final digest
today=$(date +%F)
cp exports/daily_digest_${today}.md daily_digest_latest.md >> automation.log 2>&1

# Step 9: Email it out
/volume1/@appstore/Python3.9/usr/bin/python3 send_digest_email.py >> automation.log 2>&1

echo "[DONE] Pipeline completed at $(date)" >> automation.log

