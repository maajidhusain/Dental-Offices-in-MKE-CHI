# Skill: enrich-office

Fill gaps in an existing dental office note. Targets fields that are most valuable for sales qualification.

## Input
Path to an existing office note in `obsidian/Offices/`, or an office name to look up.

## Enrichment Priority Order
Work through gaps in this order — stop when `enrichment_status` reaches `complete`:

1. **owner_name** — who runs this practice?
2. **owner_linkedin** — LinkedIn profile of the owner/head dentist
3. **owner_email** — direct email (look for contact page, LinkedIn, domain pattern)
4. **pms_software** — what system are they on?
5. **chairs** — how many operatories / chairs?
6. **providers** — full list of dentists at this location
7. **insurance_accepted** — which networks do they participate in?

## Step-by-Step Instructions

### 1. Read the Note
Read `obsidian/Offices/<OfficeName>.md`. List all fields that are empty or `unknown`.

### 2. Find the Owner / Decision Maker
Search: `"<office name>" OR "<doctor name>" dentist <city> owner LinkedIn`
- Check the office About/Team page first
- Check LinkedIn for a dentist with this practice name in their profile
- Check Google Business for listed owner or "from the owner" responses in reviews
- If you find a LinkedIn URL, set `owner_linkedin`
- If you find an email (contact page, LinkedIn, etc.), set `owner_email`

### 3. Detect PMS Software
If `pms_software` is empty:
- Fetch the office website and search page source for: Dentrix, Eaglesoft, Curve Dental, Open Dental, Carestream, Dentsply, Dolphin, Orthotrac
- Search: `"<office name>" "<city>" Dentrix OR Eaglesoft OR "Curve Dental" OR "Open Dental"`
- Check job postings (Indeed, LinkedIn jobs) — they often list required PMS experience
- If found, note confidence: "detected in page source" or "mentioned in job posting"
- Append pattern to `memory/PATTERNS.md` if it's a new detection method

### 4. Estimate Practice Size
If `chairs` is empty:
- Search: `"<office name>" "<city>" operatories OR chairs OR "exam rooms"`
- Check Google Street View description or Yelp photos count as a size proxy
- Check job postings for "X chair practice"
- If `providers` list is known: solo (1) → estimate 2–4 chairs; group (3+) → estimate 6+ chairs

### 5. Update Enrichment Status
After filling gaps, re-evaluate:
- `complete`: owner_name + owner contact (email or LinkedIn) + pms_software + providers
- `partial`: at least 3 of the 4 above
- `stub`: fewer than 3

### 6. Re-score Sales Priority
If new data warrants a change:
- `high`: pms_software is Dentrix or Eaglesoft AND google_review_count > 50
- `medium`: any PMS OR multi-provider OR review count 20–50
- `low`: no PMS, solo, low volume

### 7. Log the Enrichment
Append to `memory/SCRAPING_LOG.md`:
```
| YYYY-MM-DD | <Office Name> | enrich: <fields filled> | <new status> | <notes> |
```

Add to `## Enrichment History` section in the note:
```
- YYYY-MM-DD: filled owner_name, pms_software via website source
```

## Output
Updated office note with filled fields and new enrichment_status.
