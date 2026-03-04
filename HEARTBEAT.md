# HEARTBEAT.md

# Heartbeat tasks (run periodically).

## Gmail watch (important senders)
- Check Gmail for new messages from watchlist senders in `memory/email-watchlist.md`.
- Alert Erik on Telegram if any match since last heartbeat check.
- If match: include sender + subject + received time.
- Avoid duplicate alerts: track last check time + last seen thread/message ids in `memory/heartbeat-state.json`.

