# HEARTBEAT.md

# Heartbeat tasks (run periodically).

## Gmail watch (all new mail + priority highlight)
- Check Gmail for **all new mail since last heartbeat check**.
- Default: alert on `is:unread` to avoid noise.
- Always include: sender + subject + received time.
- Also “highlight” if it matches any priority senders/topics listed in `memory/email-watchlist.md`.
- Avoid duplicate alerts: track last check time + last seen thread/message ids in `memory/heartbeat-state.json`.
