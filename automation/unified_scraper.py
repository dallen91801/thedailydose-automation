# unified_scraper.py

from flask import Flask, jsonify
from datetime import datetime, timedelta
from scraper_sources import scrape_all_sources
from markdown_exporter import export_markdown

app = Flask(__name__)

@app.route("/scrape_all")
def scrape_all():
    today = datetime.utcnow().date()
    results = scrape_all_sources(today)
    export_markdown(results, today)
    return jsonify({"status": "success", "date": str(today), "sources": list(results.keys())})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
