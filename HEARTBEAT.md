# HEARTBEAT.md

# Heartbeat tasks (run periodically).

## Gmail watch (watchlist senders only)
- Check Gmail for **new unread** messages that match the watchlist in `memory/email-watchlist.md`.
- Alert Erik on Telegram only when there is a match.
- Include: sender + subject + received time.
- Avoid duplicate alerts: track last check time + last seen thread/message ids in `memory/heartbeat-state.json`.
