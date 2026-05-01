# Skill: sales-brief

Generate a one-page pre-call sales brief for a dental office. Used immediately before an outreach call or email.

## Input
Office name or path to `obsidian/Offices/<OfficeName>.md`.

## Prerequisites
If `enrichment_status` is `stub`, run `enrich-office` first. A brief from a stub note will be low quality.

## Step-by-Step Instructions

### 1. Read All Linked Data
- Read the office note: `obsidian/Offices/<OfficeName>.md`
- Read all linked Contact notes (owner, office manager, associate dentists)
- Read the linked Software node (e.g., `obsidian/Software/Dentrix.md`) for talking points
- Read the linked Area node for local market context

### 2. Infer Pain Points from Reviews
Scan `## Review Themes` in the office note. Map common complaints to product value:
- "long wait times" → scheduling automation pitch
- "billing confusion" / "insurance issues" → billing workflow automation
- "hard to reach" / "no response" → patient communication automation
- "felt rushed" → patient intake and follow-up automation
- If review themes are empty, check Yelp/Google directly for the office

### 3. Build the Pitch Angle
Based on PMS software:
- **Dentrix**: "Dentrix handles the basics but lacks modern AI automation — your team is likely doing manual follow-ups and reporting. We layer on top of Dentrix to eliminate that."
- **Eaglesoft**: "Eaglesoft is stable but aging — practices on it spend extra staff hours on tasks we automate in minutes."
- **Curve Dental**: "You're already on cloud-based software — our integration is seamless and you can go live in days."
- **Open Dental**: "Open Dental users are usually tech-forward. Our API integration is deep and your team will pick it up fast."
- **unknown**: "We'd love to understand your current stack — we integrate with all major PMS platforms."

### 4. Generate the Brief
Output to `obsidian/Sales Briefs/<OfficeName>_brief.md`:

```markdown
# Sales Brief — <Office Name>
*Generated: YYYY-MM-DD*

---

## Office Profile
- **Name**: 
- **Address**: 
- **Phone**: 
- **Website**: 
- **Google Rating**: X.X (NNN reviews) | **Yelp**: X.X (NNN reviews)
- **Providers**: N dentists
- **Estimated Chairs**: N
- **Services**: list

---

## Decision Maker
- **Name**: 
- **Role**: 
- **Email**: 
- **LinkedIn**: 
- **Notes**: (any personal context — tenure, specialty, etc.)

> If any contact fields are unknown, mark them as **[unknown — verify before call]**

---

## Current Stack
- **PMS**: 
- **Confidence**: (confirmed in source / detected in job posting / unknown)

---

## Pain Points (from reviews)
- [inferred from review themes]

---

## Recommended Pitch Angle
[2–3 sentences tailored to their PMS and pain points]

---

## Talking Points
1. 
2. 
3. 

---

## Open Questions
- [ ] Confirm decision maker
- [ ] Verify PMS (if unknown)
- [ ] Ask about # of locations
```

### 5. Do Not Fabricate
- If a field is unknown, write `[unknown]` — never guess
- If PMS is unknown, use the generic pitch angle and add "Verify PMS" to Open Questions
- If no reviews exist, skip the Pain Points section rather than inventing them

### 6. Log
Append to `memory/SCRAPING_LOG.md`:
```
| YYYY-MM-DD | <Office Name> | sales-brief generated | — | brief saved to Sales Briefs/ |
```

## Output
Path to the generated brief: `obsidian/Sales Briefs/<OfficeName>_brief.md`
