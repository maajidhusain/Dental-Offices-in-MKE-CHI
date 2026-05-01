"""
Scrape dental offices from Google Places API for a given area.

Requires:
    GOOGLE_PLACES_API_KEY environment variable

Usage:
    python scrape_google_places.py --query "dentist" --location "Milwaukee, WI" --radius 15000
    python scrape_google_places.py --query "dental office" --location "Chicago, IL" --radius 20000
"""

import os
import json
import argparse
import time
from datetime import date
from pathlib import Path
import requests

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
BASE_URL = "https://maps.googleapis.com/maps/api/place"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"


def geocode_location(location: str) -> tuple[float, float]:
    """Convert a city string to lat/lng."""
    url = f"{BASE_URL}/textsearch/json"
    params = {"query": location, "key": API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    result = resp.json()["results"][0]["geometry"]["location"]
    return result["lat"], result["lng"]


def search_nearby(lat: float, lng: float, radius: int, query: str) -> list[dict]:
    """Return all Places results for a dental query near a point, handling pagination."""
    url = f"{BASE_URL}/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": query,
        "type": "dentist",
        "key": API_KEY,
    }
    results = []
    while True:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        next_token = data.get("next_page_token")
        if not next_token:
            break
        time.sleep(2)  # Google requires a short delay before using next_page_token
        params = {"pagetoken": next_token, "key": API_KEY}
    return results


def get_place_details(place_id: str) -> dict:
    """Fetch full details for a single place."""
    url = f"{BASE_URL}/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,opening_hours,address_components",
        "key": API_KEY,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("result", {})


def normalize(detail: dict, search_hit: dict) -> dict:
    """Flatten a Places detail response into our standard schema."""
    addr_components = {
        c["types"][0]: c["long_name"]
        for c in detail.get("address_components", [])
    }
    return {
        "name": detail.get("name") or search_hit.get("name"),
        "address": detail.get("formatted_address", ""),
        "city": addr_components.get("locality", ""),
        "state": addr_components.get("administrative_area_level_1", ""),
        "zip": addr_components.get("postal_code", ""),
        "phone": detail.get("formatted_phone_number", ""),
        "website": detail.get("website", ""),
        "google_rating": detail.get("rating") or search_hit.get("rating"),
        "google_review_count": detail.get("user_ratings_total") or search_hit.get("user_ratings_total"),
        "place_id": search_hit.get("place_id"),
        "source": "google_places",
        "scraped_date": str(date.today()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="dentist", help="Search keyword")
    parser.add_argument("--location", required=True, help="City, State (e.g. Milwaukee, WI)")
    parser.add_argument("--radius", type=int, default=15000, help="Search radius in meters")
    args = parser.parse_args()

    if not API_KEY:
        raise RuntimeError("Set GOOGLE_PLACES_API_KEY environment variable")

    print(f"Geocoding {args.location}...")
    lat, lng = geocode_location(args.location)

    print(f"Searching within {args.radius}m of {lat},{lng}...")
    hits = search_nearby(lat, lng, args.radius, args.query)
    print(f"Found {len(hits)} results. Fetching details...")

    records = []
    for hit in hits:
        detail = get_place_details(hit["place_id"])
        records.append(normalize(detail, hit))
        time.sleep(0.1)

    slug = args.location.lower().replace(", ", "_").replace(" ", "_")
    out_path = RAW_DIR / f"google_{slug}_{date.today()}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2))
    print(f"Saved {len(records)} records to {out_path}")


if __name__ == "__main__":
    main()
