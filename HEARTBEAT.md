# HEARTBEAT.md

# Heartbeat tasks (run periodically).

## Gmail watch (watchlist + recent outbound replies)
- Check Gmail for **new unread** messages that match the watchlist in `memory/email-watchlist.md`.
- Also check for unread replies from anyone Erik has emailed within the last 3 days (rolling 72h window).
- Alert Erik on Telegram only when there is a match.
- Include: sender + subject + received time.
- Avoid duplicate alerts: track last check time + last seen thread/message ids in `memory/heartbeat-state.json`.
