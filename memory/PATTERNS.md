# Scraping Patterns

Living knowledge base. Agents append new patterns as they discover them. Each entry should include: the pattern, how reliable it is, and where it was first observed.

---

## PMS Detection Patterns

### Dentrix
- `"Dentrix"` in page `<title>` → **high confidence**
- `"Henry Schein"` in footer or about page → **medium confidence** (they sell equipment too)
- Job posting requirement "Dentrix experience required" → **high confidence**

### Eaglesoft
- `"Eaglesoft"` in page source or job posting → **high confidence**
- `"Patterson Dental"` as listed supplier → **medium confidence**

### Curve Dental
- `"Curve Dental"` or `"curve.dental"` in page source → **high confidence**

### Open Dental
- `"Open Dental"` in page source or job posting → **high confidence**

---

## Dental Board URL Patterns

### Wisconsin (DSPS)
- Search portal: `https://licensesearch.wi.gov/` (type: Dentist)
- License type codes: DN = Dentist, DNDH = Dental Hygienist

### Illinois (IDFPR)
- Search portal: `https://online-dfpr.micropact.com/lookup/licenselookup.aspx`
- License type: Dentist

---

## Office Size Proxies
- Google review count > 100 → high-volume practice (likely 4+ chairs)
- Yelp photo count > 20 → established practice
- Job posting "X-chair practice" → direct chair count signal
- "Associates welcome" or listing multiple associate dentists → group practice

---

## Review Theme → Pain Point Mapping
| Review phrase | Likely pain point | Product angle |
|---------------|------------------|---------------|
| "long wait" / "always running behind" | Scheduling inefficiency | Automated scheduling + reminders |
| "billing confusion" / "insurance issues" | Claims/billing manual work | Billing automation |
| "hard to reach" / "never calls back" | Patient communication gap | Automated follow-up |
| "felt rushed" | Intake inefficiency | Digital intake + pre-visit prep |
| "great but expensive" | Pricing sensitivity | ROI framing needed |

---

## New Patterns (Agent-Discovered)
> Agents: append new patterns below with date discovered and source

### Email Address Signals (2026-04-26)
| Email type | Signal | Confidence | Example |
|-----------|--------|-----------|---------|
| `@sbcglobal.net` | Legacy PMS — practitioner has not updated tech stack in 15+ years | **high** | Evanston Dental Center (Dr. Phillip Martini) |
| `@gmail.com` (practice email) | Solo/minimal-tech practice — unlikely to have modern PMS | **medium** | Corinium Dental (coriniumdental@gmail.com) |
| `@outlook.com` (practice email) | Non-corporate stack; small team | **low-medium** | Downtown Dental and Implants of Oswego |
| Domain-matching email (e.g., `info@brawkadental.com`) | Some IT infrastructure in place; not a definitive PMS signal | **low** | Smiles On Seventy One |

### Review Content → Pain Point Signals (2026-04-26)
| Review phrase | Signal | Product angle |
|--------------|--------|---------------|
| "one man show" / "he does everything himself" | Doctor handles admin — overworked, no delegation | Automate patient comms + billing follow-up |
| "scheduling was easy" / "booked online" | Already using some scheduling tech — upsell story | Frame as enhancement, not replacement |
| "waited forever" / "they're always behind" | Scheduling and recall inefficiency | Automated reminders + schedule optimization |

### Practice Network Signals (2026-04-26)
- **Orahh Care membership** → practice is network-oriented and open to third-party partnerships; medium-confidence receptivity signal for new tools
- **DSO affiliation** (e.g., Two Rivers, 1st Family Dental, Dentologie) → purchasing decision is not with the local dentist; deprioritize for direct outreach unless confirmed that location has local autonomy

### Age-of-Practice → PMS Signals (2026-04-26)
- **Founded before 1985** → near-certain Eaglesoft or Dentrix legacy install; use as high-confidence signal even without direct evidence
- **Founded 1985–1995** → likely legacy PMS (Eaglesoft/Dentrix); medium confidence
- **Founded after 2010** → could be any PMS including Curve Dental or Open Dental; do not assume legacy
- **"Providing smiles since [year before 1990]" in website copy** → direct founding-date signal; treat as confirmed

### Credential Signals (2026-04-26)
- **MAGD (Master of the Academy of General Dentistry)** → top 1% of GP dentists; high achiever profile, likely to invest in practice tech; strong credibility angle for product demo
- **Diplomate ABOI/ID** → elite implant credentialing; implant-heavy practice = high revenue per patient = strong ROI story for workflow automation
- **Tufts / Northwestern dental school** → premium practice profile; more receptive to data-driven outreach

