"""
Scrape dental offices from Yelp Fusion API for a given location.

Requires:
    YELP_API_KEY environment variable (get from https://www.yelp.com/developers)

Usage:
    python scrape_yelp.py --location "Milwaukee, WI"
    python scrape_yelp.py --location "Chicago, IL" --limit 200
"""

import os
import json
import argparse
from datetime import date
from pathlib import Path
import requests

API_KEY = os.environ.get("YELP_API_KEY")
BASE_URL = "https://api.yelp.com/v3/businesses"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
MAX_RESULTS = 1000  # Yelp hard cap per query
PAGE_SIZE = 50


def search_businesses(location: str, total: int) -> list[dict]:
    """Paginate through Yelp business search results for dentists."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    results = []
    offset = 0
    while offset < total:
        params = {
            "term": "dentist",
            "location": location,
            "categories": "dentists,generaldentistry,cosmeticdentists,orthodontists,periodontists,oralsurgeons,pediatricdentists",
            "limit": PAGE_SIZE,
            "offset": offset,
        }
        resp = requests.get(f"{BASE_URL}/search", headers=headers, params=params, timeout=10)
        if resp.status_code == 429:
            print("Rate limited — reduce request frequency")
            break
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("businesses", [])
        if not batch:
            break
        results.extend(batch)
        offset += PAGE_SIZE
        total = min(data.get("total", 0), MAX_RESULTS)
    return results


def get_business_reviews(business_id: str) -> list[dict]:
    """Fetch up to 3 review excerpts for a business."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.get(f"{BASE_URL}/{business_id}/reviews", headers=headers, timeout=10)
    if resp.status_code != 200:
        return []
    return resp.json().get("reviews", [])


def normalize(biz: dict, reviews: list[dict]) -> dict:
    location = biz.get("location", {})
    return {
        "name": biz.get("name"),
        "address": " ".join(filter(None, location.get("display_address", []))),
        "city": location.get("city", ""),
        "state": location.get("state", ""),
        "zip": location.get("zip_code", ""),
        "phone": biz.get("display_phone", ""),
        "website": biz.get("url", ""),  # Yelp URL — website is behind detail call
        "yelp_rating": biz.get("rating"),
        "yelp_review_count": biz.get("review_count"),
        "yelp_id": biz.get("id"),
        "categories": [c["alias"] for c in biz.get("categories", [])],
        "review_excerpts": [r.get("text", "") for r in reviews],
        "source": "yelp",
        "scraped_date": str(date.today()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", required=True, help="City, State (e.g. Milwaukee, WI)")
    parser.add_argument("--limit", type=int, default=200, help="Max results to fetch")
    args = parser.parse_args()

    if not API_KEY:
        raise RuntimeError("Set YELP_API_KEY environment variable")

    print(f"Searching Yelp for dentists in {args.location}...")
    businesses = search_businesses(args.location, args.limit)
    print(f"Found {len(businesses)} businesses. Fetching reviews...")

    records = []
    for biz in businesses:
        reviews = get_business_reviews(biz["id"])
        records.append(normalize(biz, reviews))

    slug = args.location.lower().replace(", ", "_").replace(" ", "_")
    out_path = RAW_DIR / f"yelp_{slug}_{date.today()}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2))
    print(f"Saved {len(records)} records to {out_path}")


if __name__ == "__main__":
    main()
