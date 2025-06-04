# scraper_sources.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def is_today(published_date):
    return published_date.date() == datetime.utcnow().date()

# --- Epoch Times ---
def fetch_epoch_times_section(section_url):
    response = requests.get(section_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    articles = []
    for item in soup.select("article"):
        title = item.select_one("h2, h3")
        link = item.find("a", href=True)
        summary = item.select_one("p")
        if title and link:
            articles.append({
                "title": title.get_text(strip=True),
                "url": link['href'],
                "summary": summary.get_text(strip=True) if summary else None,
                "published": str(datetime.utcnow().date())
            })
    return articles

def scrape_epoch_health(today):
    return fetch_epoch_times_section("https://www.theepochtimes.com/health")

def scrape_epoch_science(today):
    return fetch_epoch_times_section("https://www.theepochtimes.com/science")

# --- Stub functions for remaining sources ---
def scrape_fda(today):
    return []

def scrape_cms(today):
    return []

def scrape_hhs(today):
    return []

def scrape_health_canada(today):
    return []

def scrape_nejm(today):
    return []

def scrape_jama(today):
    return []

def scrape_medpage_today(today):
    return []

def scrape_modern_healthcare(today):
    return []

def scrape_fierce_pharma(today):
    return []

def scrape_fierce_biotech(today):
    return []

def scrape_medscape(today):
    return []

def scrape_reuters_health(today):
    return []

def scrape_aha(today):
    return []

def scrape_healthcare_dive(today):
    return []

def scrape_healio(today):
    return []

# --- Aggregate all ---
def scrape_all_sources(today):
    return {
        "EpochTimes_Health": scrape_epoch_health(today),
        "EpochTimes_Science": scrape_epoch_science(today),
        "FDA": scrape_fda(today),
        "CMS": scrape_cms(today),
        "HHS": scrape_hhs(today),
        "HealthCanada": scrape_health_canada(today),
        "NEJM": scrape_nejm(today),
        "JAMA": scrape_jama(today),
        "MedPageToday": scrape_medpage_today(today),
        "ModernHealthcare": scrape_modern_healthcare(today),
        "FiercePharma": scrape_fierce_pharma(today),
        "FierceBiotech": scrape_fierce_biotech(today),
        "Medscape": scrape_medscape(today),
        "ReutersHealth": scrape_reuters_health(today),
        "AHA": scrape_aha(today),
        "HealthcareDive": scrape_healthcare_dive(today),
        "Healio": scrape_healio(today),
    }
