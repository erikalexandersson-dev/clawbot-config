# Gmail heartbeat alerts

Purpose: during each OpenClaw heartbeat, check Gmail and notify Erik.

## Mode
- ✅ Alert only on **watchlist matches** (not all mail)
- ✅ Also alert on **replies from recipients Erik has emailed in the last 3 days** (rolling window)

## Watchlist (senders / topics)
- Täby Sjöflygklubb
- Martin på Handelsbanken
- KSSS
- Erikssons automekanik
- Uppsala Aerobatic Club (skolning@uppsalaaerobatic.se)
- Michael Käll (michael.kall1984@gmail.com)
- Skysport
- Keyword: "faktura" (match in subject/body)

## Dynamic rule: recent outbound replies (NEW)
- Build a rolling 3-day recipient set from Erik's sent mail.
- If a **new unread** mail arrives from any of those recipients, alert Erik.
- Keep each recipient active in this dynamic watchlist for 72 hours after Erik last emailed them.

## Notes / next refinements
- Add exact matching rules (from email addresses, domains, subject keywords).
- Decide whether alerts should include only `is:unread` (default) or also already-read.
- Use Gmail History API for exact “since last check” (instead of date-based queries).
