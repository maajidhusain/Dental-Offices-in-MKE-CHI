# Skill: scrape-office

Scrape a single dental office from all four sources and create or update its Obsidian note.

## Input
An office name and city, or a free-text search query (e.g. "Lakeview Dental Chicago" or "123 Main St Milwaukee dentist").

## Step-by-Step Instructions

### 1. Prevent Duplicates
Before doing anything, search `obsidian/Offices/` for an existing note that matches this office name (fuzzy match is fine). If one exists, switch to the `enrich-office` skill instead.

### 2. Google Maps / Places
Search: `<office name> dental <city> site:google.com/maps OR google.com/search`
Capture:
- `name` — canonical business name
- `address`, `city`, `state`, `zip`
- `phone`
- `website`
- `google_rating` (e.g. 4.7)
- `google_review_count`
- Business hours (add to `## Notes` section)

### 3. Yelp
Search: `<office name> <city> site:yelp.com`
Capture:
- `yelp_rating`
- `yelp_review_count`
- Categories (e.g. "General Dentistry", "Cosmetic Dentists", "Orthodontists") → add to `services`
- Top 2–3 review themes (positive and negative) → add to `## Review Themes`

### 4. State Dental Board
- **Wisconsin**: search `<doctor name> Wisconsin dental license` or use DSPS lookup
- **Illinois**: search `<doctor name> Illinois dental license IDFPR`
Capture:
- Licensed dentist names at this address → add to `providers`
- `board_license_verified: true` if confirmed
- License numbers and status → create linked Contact notes in `obsidian/Contacts/`

### 5. Office Website
Fetch the office website (from step 2). Scan for:
- **PMS software**: look for "Dentrix", "Eaglesoft", "Curve Dental", "Open Dental", "Carestream", "Dentsply Sirona" in page source, footer, or blog posts
- **Staff page**: extract dentist names and any listed roles (owner, associate)
- **Owner/doctor name**: usually on About or Meet the Team page
- **Number of providers**: count unique dentist names found
- **Insurance**: look for "Insurance" or "Plans We Accept" page

If PMS is detected from website source, set confidence note in `## Notes`.

### 6. Write the Note
- File path: `obsidian/Offices/<OfficeName>.md` (use sanitized office name, no special chars)
- Use the schema from `obsidian/Offices/_template.md`
- Set `enrichment_status`:
  - `stub` — only name/address captured
  - `partial` — has phone + website + at least one of (pms_software, owner_name, providers)
  - `complete` — has owner contact + pms_software + providers + reviews
- Set `last_scraped` to today's date (YYYY-MM-DD)
- Set `sales_priority` using these rules:
  - `high`: pms_software is Dentrix or Eaglesoft AND google_review_count > 50
  - `medium`: any PMS detected OR review count 20–50
  - `low`: no PMS signal, low review volume

### 7. Create Linked Nodes
- For each dentist found: create `obsidian/Contacts/<DoctorName>.md` if it doesn't exist
- For the PMS found: confirm `obsidian/Software/<PMSName>.md` exists (create stub if not)
- For the city/neighborhood: confirm `obsidian/Areas/<AreaName>.md` exists (create stub if not)

### 8. Update Memory
Append to `memory/SCRAPING_LOG.md`:
```
| YYYY-MM-DD | <Office Name> | Google, Yelp, Board, Website | <stub/partial/complete> | <any notes> |
```

## Output
Path to the created/updated office note.
