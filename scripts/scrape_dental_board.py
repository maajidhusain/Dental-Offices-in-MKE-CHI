"""
Scrape dentist license data from Wisconsin DSPS and Illinois IDFPR.

No API key required — uses public license lookup portals.

Usage:
    python scrape_dental_board.py --state WI --name "Smith"
    python scrape_dental_board.py --state IL --name "Patel"
    python scrape_dental_board.py --state WI  # scrape full active list (slow)
"""

import json
import argparse
import time
from datetime import date
from pathlib import Path
import requests
from bs4 import BeautifulSoup

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"

WI_SEARCH_URL = "https://licensesearch.wi.gov/api/Licensee/GetLicensees"
IL_SEARCH_URL = "https://online-dfpr.micropact.com/lookup/licenselookup.aspx"


def search_wi_board(last_name: str = "") -> list[dict]:
    """
    Query the Wisconsin DSPS license search for dentists.
    Returns normalized license records.
    """
    params = {
        "professionCode": "DN",  # DN = Dentist
        "lastName": last_name,
        "pageSize": 100,
        "pageNumber": 1,
    }
    headers = {"Accept": "application/json"}
    records = []
    while True:
        resp = requests.get(WI_SEARCH_URL, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("licensees", [])
        if not batch:
            break
        for lic in batch:
            records.append({
                "name": f"{lic.get('firstName', '')} {lic.get('lastName', '')}".strip(),
                "license_number": lic.get("licenseNumber", ""),
                "license_type": lic.get("professionDescription", "Dentist"),
                "license_status": lic.get("licenseStatus", ""),
                "city": lic.get("city", ""),
                "state": "WI",
                "source": "wi_dsps",
                "scraped_date": str(date.today()),
            })
        if len(batch) < params["pageSize"]:
            break
        params["pageNumber"] += 1
        time.sleep(0.5)
    return records


def search_il_board(last_name: str = "") -> list[dict]:
    """
    Query the Illinois IDFPR license lookup for dentists.
    Uses form-based scraping (no JSON API available).
    """
    session = requests.Session()
    resp = session.get(IL_SEARCH_URL, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    viewstate = soup.find("input", {"name": "__VIEWSTATE"})
    eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"})

    payload = {
        "__VIEWSTATE": viewstate["value"] if viewstate else "",
        "__EVENTVALIDATION": eventvalidation["value"] if eventvalidation else "",
        "ctl00$MainContent$tbLastName": last_name,
        "ctl00$MainContent$ddlLicenseType": "DENTIST",
        "ctl00$MainContent$btnSearch": "Search",
    }

    resp = session.post(IL_SEARCH_URL, data=payload, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    records = []
    table = soup.find("table", {"id": "ctl00_MainContent_GridView1"})
    if not table:
        return records

    headers_row = table.find("tr")
    col_names = [th.get_text(strip=True) for th in headers_row.find_all("th")]

    for row in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cells:
            continue
        row_data = dict(zip(col_names, cells))
        records.append({
            "name": row_data.get("Name", ""),
            "license_number": row_data.get("License Number", ""),
            "license_type": "Dentist",
            "license_status": row_data.get("Status", ""),
            "city": row_data.get("City", ""),
            "state": "IL",
            "source": "il_idfpr",
            "scraped_date": str(date.today()),
        })
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, choices=["WI", "IL"])
    parser.add_argument("--name", default="", help="Last name to filter (optional)")
    args = parser.parse_args()

    if args.state == "WI":
        records = search_wi_board(args.name)
    else:
        records = search_il_board(args.name)

    print(f"Found {len(records)} license records")
    slug = f"{args.state.lower()}_{args.name.lower() or 'all'}_{date.today()}"
    out_path = RAW_DIR / f"board_{slug}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(records, indent=2))
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
