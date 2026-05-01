"""
Convert a normalized dental office record (dict) into an Obsidian markdown note.

Can be called standalone to write a single record, or imported as a module
by other scripts that have assembled a complete record.

Usage:
    python write_obsidian_note.py --input data/processed/my_office.json
    python write_obsidian_note.py --input data/processed/my_office.json --force
"""

import json
import argparse
import re
from datetime import date
from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent / "obsidian"
OFFICES_DIR = VAULT_DIR / "Offices"
CONTACTS_DIR = VAULT_DIR / "Contacts"
SOFTWARE_DIR = VAULT_DIR / "Software"
AREAS_DIR = VAULT_DIR / "Areas"


def sanitize_filename(name: str) -> str:
    """Convert office name to a safe filename."""
    return re.sub(r'[^\w\s\-]', '', name).strip().replace(" ", " ")


def compute_enrichment_status(record: dict) -> str:
    has_contact = bool(record.get("owner_name") or record.get("office_manager"))
    has_contact_info = bool(record.get("owner_email") or record.get("owner_linkedin"))
    has_pms = bool(record.get("pms_software") and record["pms_software"] != "unknown")
    has_providers = bool(record.get("providers"))

    if has_contact and has_contact_info and has_pms and has_providers:
        return "complete"
    if bool(record.get("phone")) and bool(record.get("website")) and (has_pms or has_contact or has_providers):
        return "partial"
    return "stub"


def compute_sales_priority(record: dict) -> str:
    pms = (record.get("pms_software") or "").lower()
    review_count = record.get("google_review_count") or 0
    legacy_pms = pms in ("dentrix", "eaglesoft")

    if legacy_pms and review_count > 50:
        return "high"
    if pms and pms != "unknown" or (20 <= review_count <= 50):
        return "medium"
    return "low"


def format_yaml_list(items: list) -> str:
    if not items:
        return "[]"
    return "\n" + "\n".join(f"  - {item}" for item in items)


def build_note_content(record: dict) -> str:
    status = compute_enrichment_status(record)
    priority = compute_sales_priority(record)

    providers_yaml = format_yaml_list(record.get("providers", []))
    insurance_yaml = format_yaml_list(record.get("insurance_accepted", []))
    services_yaml = format_yaml_list(record.get("services", []))
    tags_yaml = format_yaml_list(record.get("tags", []))

    pms = record.get("pms_software") or ""
    pms_link = f"[[{pms}]]" if pms and pms != "unknown" else (pms or "")

    area = record.get("area", "")
    area_link = f"[[{area}]]" if area else ""

    frontmatter = f"""---
name: {record.get('name', '')}
address: {record.get('address', '')}
city: {record.get('city', '')}
state: {record.get('state', '')}
zip: {record.get('zip', '')}
phone: {record.get('phone', '')}
website: {record.get('website', '')}
google_rating: {record.get('google_rating', '')}
google_review_count: {record.get('google_review_count', '')}
yelp_rating: {record.get('yelp_rating', '')}
yelp_review_count: {record.get('yelp_review_count', '')}
providers: {providers_yaml}
chairs: {record.get('chairs', '')}
pms_software: {pms_link}
owner_name: {record.get('owner_name', '')}
owner_email: {record.get('owner_email', '')}
owner_linkedin: {record.get('owner_linkedin', '')}
office_manager: {record.get('office_manager', '')}
insurance_accepted: {insurance_yaml}
services: {services_yaml}
area: {area_link}
board_license_verified: {str(record.get('board_license_verified', False)).lower()}
last_scraped: {record.get('last_scraped') or str(date.today())}
enrichment_status: {status}
sales_priority: {priority}
tags: {tags_yaml}
---"""

    notes = record.get("notes", "")
    review_themes = record.get("review_themes", "")
    enrichment_history = record.get("enrichment_history", f"- {date.today()}: initial note created")

    body = f"""
## Notes
{notes}

## Review Themes
{review_themes}

## Enrichment History
{enrichment_history}
"""
    return frontmatter + "\n" + body


def write_note(record: dict, force: bool = False) -> Path:
    name = record.get("name", "Unknown Office")
    filename = sanitize_filename(name) + ".md"
    out_path = OFFICES_DIR / filename

    if out_path.exists() and not force:
        print(f"Note already exists: {out_path} (use --force to overwrite)")
        return out_path

    OFFICES_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_note_content(record), encoding="utf-8")
    print(f"Written: {out_path}")
    return out_path


def ensure_software_node(pms: str):
    if not pms or pms == "unknown":
        return
    node_path = SOFTWARE_DIR / f"{pms}.md"
    if not node_path.exists():
        SOFTWARE_DIR.mkdir(parents=True, exist_ok=True)
        node_path.write_text(f"---\nname: {pms}\ntags: [pms, software]\n---\n\n## Offices Using This Software\n")
        print(f"Created software node: {node_path}")


def ensure_area_node(area: str):
    if not area:
        return
    node_path = AREAS_DIR / f"{area}.md"
    if not node_path.exists():
        AREAS_DIR.mkdir(parents=True, exist_ok=True)
        node_path.write_text(f"---\nname: {area}\ntags: [area]\n---\n\n## Offices in This Area\n")
        print(f"Created area node: {node_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to normalized JSON record")
    parser.add_argument("--force", action="store_true", help="Overwrite existing note")
    args = parser.parse_args()

    record = json.loads(Path(args.input).read_text())
    write_note(record, force=args.force)
    ensure_software_node(record.get("pms_software", ""))
    ensure_area_node(record.get("area", ""))


if __name__ == "__main__":
    main()
