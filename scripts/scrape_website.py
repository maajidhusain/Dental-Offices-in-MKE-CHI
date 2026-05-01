"""
Visit a dental office website and extract: PMS software hints, staff names, owner, chair count.

Usage:
    python scrape_website.py --url "https://lakeshoredentalwi.com"
    python scrape_website.py --url "https://example-dental.com" --output data/processed/example.json
"""

import json
import re
import argparse
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"

PMS_KEYWORDS = {
    "Dentrix": ["dentrix", "henry schein"],
    "Eaglesoft": ["eaglesoft", "patterson dental"],
    "Curve Dental": ["curve dental", "curve.dental"],
    "Open Dental": ["open dental", "opendental"],
    "Carestream": ["carestream", "kodak dental"],
    "Dentsply Sirona": ["dentsply", "sirona", "axium"],
    "Orthotrac": ["orthotrac"],
    "Dolphin": ["dolphin imaging"],
}

STAFF_TITLE_PATTERNS = [
    r"Dr\.\s+[A-Z][a-z]+ [A-Z][a-z]+",
    r"DDS",
    r"DMD",
]

CHAIR_PATTERNS = [
    r"(\d+)[\s\-]+(?:operatories|operatory|chairs|chair|exam rooms?)",
]


def fetch_page(url: str) -> tuple[str, BeautifulSoup]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; DentalResearchBot/1.0)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return resp.text, soup


def find_internal_links(base_url: str, soup: BeautifulSoup, keywords: list[str]) -> list[str]:
    """Find internal page links matching keywords (about, team, staff, etc.)."""
    domain = urlparse(base_url).netloc
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        text = a.get_text(strip=True).lower()
        if any(kw in href or kw in text for kw in keywords):
            full = urljoin(base_url, a["href"])
            if urlparse(full).netloc == domain:
                links.append(full)
    return list(set(links))


def detect_pms(html: str) -> dict:
    """Scan raw HTML for PMS software mentions."""
    html_lower = html.lower()
    found = {}
    for pms_name, keywords in PMS_KEYWORDS.items():
        for kw in keywords:
            if kw in html_lower:
                found[pms_name] = kw
                break
    return found


def extract_staff(text: str) -> list[str]:
    """Extract doctor names from page text using title patterns."""
    names = set()
    for pattern in STAFF_TITLE_PATTERNS[:1]:  # Dr. pattern only
        names.update(re.findall(pattern, text))
    return sorted(names)


def extract_chair_count(text: str) -> int | None:
    for pattern in CHAIR_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def scrape_website(url: str) -> dict:
    result = {
        "website": url,
        "pms_detected": {},
        "staff_names": [],
        "chair_count": None,
        "pages_visited": [url],
        "source": "website",
        "scraped_date": str(date.today()),
    }

    try:
        html, soup = fetch_page(url)
    except Exception as e:
        result["error"] = str(e)
        return result

    result["pms_detected"].update(detect_pms(html))
    result["staff_names"].extend(extract_staff(soup.get_text(" ")))
    result["chair_count"] = extract_chair_count(soup.get_text(" "))

    # Also check about/team pages
    team_links = find_internal_links(url, soup, ["about", "team", "staff", "meet", "doctor", "provider"])
    for link in team_links[:3]:
        try:
            sub_html, sub_soup = fetch_page(link)
            result["pms_detected"].update(detect_pms(sub_html))
            result["staff_names"].extend(extract_staff(sub_soup.get_text(" ")))
            if not result["chair_count"]:
                result["chair_count"] = extract_chair_count(sub_soup.get_text(" "))
            result["pages_visited"].append(link)
        except Exception:
            pass

    result["staff_names"] = sorted(set(result["staff_names"]))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Office website URL")
    parser.add_argument("--output", help="Output JSON path (optional)")
    args = parser.parse_args()

    print(f"Scraping {args.url}...")
    data = scrape_website(args.url)

    print(f"PMS detected: {list(data['pms_detected'].keys()) or 'none'}")
    print(f"Staff found: {data['staff_names']}")
    print(f"Chair count: {data['chair_count']}")

    if args.output:
        out_path = Path(args.output)
    else:
        slug = urlparse(args.url).netloc.replace(".", "_")
        out_path = RAW_DIR / f"website_{slug}_{date.today()}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2))
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
