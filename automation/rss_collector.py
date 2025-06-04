import feedparser
import json
from datetime import datetime
import hashlib
import logging

# Setup main logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("rss_collector.log"),
        logging.StreamHandler()
    ]
)

# Separate log file for failed feeds
FAILED_LOG_PATH = "failed_feeds.log"
failed_log = open(FAILED_LOG_PATH, "a", encoding="utf-8")

# RSS Sources
RSS_FEEDS = {
    "HHS": "https://www.hhs.gov/rss/blog.xml",
    "CDC": "http://www.cdc.gov/mmwr/rss/rss.xml",
    "FDA": "https://www.fda.gov/news-events/press-announcements.rss",
    "CMS": "https://www.cms.gov/newsroom/rss-feed",
    "NIH": "https://www.nih.gov/news-releases/feed.xml",
    "HealthCanada": "https://www.canada.ca/en/health-canada/news.rss",
    "AHA": "https://www.aha.org/rss.xml",
    "KFF": "https://www.kff.org/feed",
    "HealthAffairs": "https://www.healthaffairs.org/action/showFeed?type=etoc&feed=rss&jc=hlthaff",
    "BeckersHospitalReview": "https://www.beckershospitalreview.com/feed",
    "THCB": "https://thehealthcareblog.com/feed",
    "HealthcareDive": "https://www.healthcaredive.com/feeds/news",
    "MedPageToday": "https://www.medpagetoday.com/rss",
    "STATNews": "https://www.statnews.com/feed",
    "NEJM": "https://www.nejm.org/nejm/rss.xml",
    "JAMA": "https://jamanetwork.com/rss/site_12/0.xml",
    "Healio": "https://www.healio.com/rss",
    "ModernHealthcare": "https://www.modernhealthcare.com/section/rss",
    "FiercePharma": "https://www.fiercepharma.com/rss",
    "FierceBiotech": "https://www.fiercebiotech.com/rss",
    "EndpointsNews": "https://endpts.com/feed",
    "BioPharmaDive": "https://www.biopharmadive.com/feeds/news",
    "Medscape": "https://www.medscape.com/rss/public",
    "Reuters_HealthNews": "http://feeds.reuters.com/reuters/healthNews",
    "EpochTimes_Health": "https://www.theepochtimes.com/c-health/feed",
    "EpochTimes_Science": "https://www.theepochtimes.com/c-science/feed",
    "WHO_EMRO_News": "https://www.emro.who.int/index.php?option=com_mediarss&feed_id=1&format=raw",
    "WHO_EMRO_Publications": "https://www.emro.who.int/index.php?option=com_mediarss&feed_id=2&format=raw",
    "WHO_EMRO_Events": "https://www.emro.who.int/index.php?option=com_mediarss&feed_id=3&format=raw",
    "WHO_EMRO_Statements": "https://www.emro.who.int/index.php?option=com_mediarss&feed_id=4&format=raw",
    "WHO_EMRO_PressReleases": "https://www.emro.who.int/index.php?option=com_mediarss&feed_id=5&format=raw",
    "HealthcareITNews": "https://www.healthcareitnews.com/rss",
    "HealthITAnalytics": "https://healthitanalytics.com/rss",
    "HIMSS": "https://www.himss.org/news/rss",
    "HealthcareInformatics": "https://www.hcinnovationgroup.com/rss",
    "MedTechDive": "https://www.medtechdive.com/rss",
    "FierceHealthcare": "https://www.fiercehealthcare.com/rss",
    "HealthDataManagement": "https://www.healthdatamanagement.com/rss",
    "JournalAHIMA": "https://journal.ahima.org/rss",
    "HealthcareITToday": "https://www.healthcareittoday.com/feed",
    "ONC": "https://www.healthit.gov/rss",
    "MedCityNews": "https://medcitynews.com/feed",
    "HITConsultant": "https://hitconsultant.net/feed",
    "HealthTechMagazine": "https://healthtechmagazine.net/rss",
    "MobiHealthNews": "https://www.mobihealthnews.com/rss",
    "HealthcareEconomist": "https://healthcare-economist.com/feed",
    "HealthITSecurity": "https://healthitsecurity.com/rss",
    "HealthcareFinanceNews": "https://www.healthcarefinancenews.com/rss",
    "NEJMCatalyst": "https://catalyst.nejm.org/rss",
    "HarvardHealthBlog": "https://www.health.harvard.edu/blog/feed",
    "DigitalHealth": "https://www.digitalhealth.net/feed"
}


def hash_entry(entry):
    base = entry.get("title", "") + entry.get("link", "")
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def collect_articles(limit_per_feed=5):
    collected = []
    seen_hashes = set()

    for source, url in RSS_FEEDS.items():
        logging.info(f"Fetching feed: {source}")
        try:
            feed = feedparser.parse(url)

            if not feed.entries:
                warning_msg = f"[❌] {source}: NO entries"
                logging.warning(warning_msg)
                failed_log.write(f"{datetime.utcnow().isoformat()} | NO ENTRIES | {source}: {url}\n")
                continue

            for entry in feed.entries[:limit_per_feed]:
                h = hash_entry(entry)
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                collected.append({
                    "source": source,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", ""),
                    "published": entry.get("published", str(datetime.utcnow())),
                    "hash": h
                })

        except Exception as e:
            error_msg = f"[ERROR] {source}: {e}"
            logging.error(error_msg)
            failed_log.write(f"{datetime.utcnow().isoformat()} | ERROR | {source}: {url} | {e}\n")

    return collected


if __name__ == "__main__":
    articles = collect_articles()
    output_file = "rss_articles.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    logging.info(f"✅ Saved {len(articles)} articles to {output_file}")

    # ➕ Append to enriched_articles.json
    enriched_path = Path("enriched_articles.json")
    if enriched_path.exists():
        with open(enriched_path, "r+", encoding="utf-8") as f:
            existing = json.load(f)
            f.seek(0)
            json.dump(existing + articles, f, indent=2)
            f.truncate()
    else:
        with open(enriched_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2)

    logging.info(f"✅ Appended RSS articles to enriched_articles.json")

    failed_log.close()
    logging.info(f"Failed feeds logged to {FAILED_LOG_PATH}")