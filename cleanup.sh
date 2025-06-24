#!/bin/bash
set -e

echo "🧹 Starting cleanup..."

# Delete deprecated folders and zip
rm -rf /volume1/docker/thedailydose/wp-data
rm -f /volume1/docker/thedailydose/automation/automation_modular_pipeline_gpu.zip

# Delete old .py scripts replaced by modular pipeline
cd /volume1/docker/thedailydose/automation
rm -f rss_collector.py scraper_sources.py scrape_pubmed.py hhs_daily_articles.py parse_articles.py generate_digest_full.py daily_4am_pipeline.sh send_summary_email.py

echo "✅ Cleanup complete!"
