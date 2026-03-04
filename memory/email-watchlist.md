# Gmail heartbeat alerts

Purpose: during each OpenClaw heartbeat, check Gmail and notify Erik.

## Mode
- ✅ Alert only on **watchlist matches** (not all mail)

## Watchlist (senders / topics)
- Täby Sjöflygklubb
- Martin på Handelsbanken
- KSSS
- Erikssons automekanik
- Uppsala Aerobatic Club (skolning@uppsalaaerobatic.se)

## Notes / next refinements
- Add exact matching rules (from email addresses, domains, subject keywords).
- Decide whether alerts should include only `is:unread` (default) or also already-read.
- Use Gmail History API for exact “since last check” (instead of date-based queries).
