# Pipeline Progress

Update after each scraping session. Keep totals accurate.

---

## Coverage
- **Total offices**: 74 (CHI metro only; MKE not yet started)
- **MKE area**: 0
- **CHI area**: 74

## Enrichment Status
- `stub` (name/address only): ~10
- `partial` (has phone + website + 1 key signal): ~64
- `complete` (owner contact + PMS + providers): 0

## PMS Distribution
- Dentrix: 0 confirmed
- Eaglesoft: 0 confirmed
- Curve Dental: 0 confirmed
- Open Dental: 0 confirmed
- Other: 0 confirmed
- Unknown: 74 (PMS detection not yet performed)

## Sales Priority
- High: 7
- Medium: ~28
- Low: ~39

---

## Priority Queue
Top offices to enrich next (highest value gaps):

1. **Schaumburg Smiles** — PMS unknown; no email/LinkedIn for Dr. Hardenbergh
2. **Evanston Dental Associates** — PMS unknown; no email for Dr. Silberman
3. **Dental Care of Oak Park** — PMS unknown; no LinkedIn/email for Dr. Perna
4. **Stephens Dentistry** — PMS unknown; no LinkedIn/email for Dr. Montoya; deepened search needed
5. **Oswego Dental Group** — PMS unknown; no personal email/LinkedIn for Dr. Milazzo
6. **Downtown Dental and Implants of Oswego** — PMS unknown (email found)
7. **Smiles On Seventy One** — PMS unknown (email + LinkedIn found)
8. All HIGH priority: run PMS detection script against each website
9. Partial-name providers — Dr. Jackson, Dr. Hermann, Dr. Yoon, Dr. Fairbanks, Dr. Crombie, Dr. Wylde, Dr. Klemma need full names
10. Stub offices — Art of Modern Dentistry, Dentologie, Happy Smiles Schaumburg, Lincoln Park Dental Specialists, Montrose Dental Group, Oak Park Oral Health Care, Royal Dental Care Schaumburg, Schaumburg Dentistry, Smile Clinic of Schaumburg, Town and Country Dental Oak Park

---

## Areas Covered
| Area | Offices Scraped | Notes |
|------|----------------|-------|
| MKE - Downtown | 0 | Not started |
| MKE - East Side | 0 | Not started |
| MKE - South Side | 0 | Not started |
| MKE - West Side | 0 | Not started |
| MKE - North Shore | 0 | Not started |
| Wauwatosa | 0 | Not started |
| Brookfield | 0 | Not started |
| CHI - Loop | ~12 | Complete initial scrape |
| CHI - Lincoln Park | ~10 | Complete initial scrape |
| CHI - Lakeview | ~8 | Complete initial scrape |
| CHI - Wicker Park / Bucktown | ~5 | Complete initial scrape |
| CHI - Rogers Park / Andersonville | ~4 | Complete initial scrape |
| CHI - Edgewater / Uptown | ~3 | Complete initial scrape |
| Evanston | ~7 | Complete initial scrape; 2 HIGH priority |
| Oak Park | ~6 | Complete initial scrape; 1 HIGH priority |
| Naperville | ~5 | Complete initial scrape |
| Schaumburg | ~7 | Complete initial scrape; 1 HIGH priority |
| Oswego | ~7 | Complete initial scrape; 3 HIGH priority |

---

## Session History
| Date | Offices Added | Offices Enriched | Notes |
|------|--------------|-----------------|-------|
| 2026-04-26 | 74 (CHI metro) | 7 HIGH priority | Full Chicagoland build-out complete. Contact nodes created for all identified providers (~104 contacts). HIGH priority enrichment in progress. |
