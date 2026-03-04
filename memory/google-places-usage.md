# Google Places Usage Log

Purpose: keep a lightweight manual log of Places/Geocoding API usage to monitor cost.

## Pricing guardrails (manual)
- Check GCP Billing budget alerts (25/50/90/100%).
- Keep API key restricted to server IP + only needed APIs.

## Entries

| Date (UTC) | Task | API calls (est.) | Notes |
|---|---:|---:|---|
| 2026-03-04 | Initial setup + verification | 3 | 1x Find Place (address), 1x Nearby Search (Volvo service), 1x geocode-style verification |
