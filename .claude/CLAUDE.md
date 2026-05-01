# Dental Offices MKE/CHI — Agent Instructions

## Goal
Build and maintain a structured knowledge graph of dental offices in the Milwaukee (WI) and Chicago (IL) metro areas. This database supports selling an AI data tool to dental practices. Every action you take should move offices from `stub` → `partial` → `complete` enrichment status and improve the quality of sales intelligence.

## Repository Layout
```
obsidian/Offices/       — one .md note per dental office (the primary data store)
obsidian/Contacts/      — linked nodes for dentists and office managers
obsidian/Areas/         — geographic area nodes (MKE neighborhoods, CHI neighborhoods)
obsidian/Software/      — PMS software nodes (Dentrix, Eaglesoft, Curve, Open Dental)
obsidian/Sales Briefs/  — generated pre-call briefs (one per office)
scripts/                — Python scraping and note-writing scripts
data/raw/               — unprocessed API/scrape responses (JSON)
data/processed/         — normalized records before note creation
memory/                 — agent memory: logs, patterns, progress
```

## Note Schema
Every office note uses YAML frontmatter. The canonical template is at `obsidian/Offices/_template.md`. Key fields:
- `enrichment_status`: `stub` | `partial` | `complete`
- `sales_priority`: `low` | `medium` | `high` — set based on size + software signals
- `pms_software`: the current practice management system — most important sales signal
- `owner_name` / `owner_email` / `owner_linkedin` — the decision maker

## Wikilinks Convention
- Link an office to its area: `[[Milwaukee - East Side]]`
- Link an office to its PMS: `[[Dentrix]]`
- Link contacts to their office: `office: "[[Office Name]]"`

## After Every Scrape or Enrichment
1. Append a row to `memory/SCRAPING_LOG.md`
2. If you discovered a new pattern (e.g., a reliable way to detect a PMS, a dental board URL pattern), append it to `memory/PATTERNS.md`
3. Update the totals in `memory/PROGRESS.md`

## Skills Available
| Skill | Invoke with | Purpose |
|-------|-------------|---------|
| `scrape-office` | `/scrape-office` | Find + scrape one office from all four sources |
| `enrich-office` | `/enrich-office` | Fill gaps in an existing office note |
| `sales-brief` | `/sales-brief` | Generate a pre-call sales brief |

## Sales Context
The buyer is the **office owner** (usually the head dentist) or the **office manager**. The product automates workflows that currently depend on the PMS (Dentrix, Eaglesoft, Curve, Open Dental) — think scheduling, billing follow-up, patient communication, and reporting.

Key qualification signals (highest → lowest):
1. Office owns 2+ locations → higher budget, more pain
2. PMS is Dentrix or Eaglesoft (legacy) → most likely to upgrade
3. Review count > 100 on Google → high patient volume, ROI story is easy
4. Owner is a solo practitioner → faster sales cycle, single decision maker

## What Not To Do
- Never fabricate data. Mark unknown fields as empty, not guessed.
- Never overwrite `enrichment_status: complete` with a lower value.
- Never commit API keys. Load from environment variables only.
- Do not create duplicate office notes. Search `obsidian/Offices/` before creating.
