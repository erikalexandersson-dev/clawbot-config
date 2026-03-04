# Email watchlist (heartbeat alerts)

Purpose: during each OpenClaw heartbeat, check Gmail for messages from these senders and notify Erik.

## Current watchlist
- Täby Sjöflygklubb
- Martin på Handelsbanken
- KSSS
- Erikssons automekanik

## Notes / next refinements
- Add exact matching rules (from email addresses, domains, subject keywords).
- Decide whether to alert on *any* mail or only `is:unread`.
- Optionally keep last-seen Gmail `historyId` or timestamp to avoid repeat alerts.
