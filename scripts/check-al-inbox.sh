#!/usr/bin/env bash
# Check al@alexanderssons.org inbox via IMAP (ForwardEmail)
# Returns: JSON with unseen count + recent unseen message envelopes
set -euo pipefail

source /root/.openclaw/secrets.env

IMAP_HOST="imap.forwardemail.net"
USER="$FORWARDEMAIL_USER"
PASS="$FORWARDEMAIL_PASSWORD"

# Get status
STATUS=$(curl -s --ssl-reqd \
  "imaps://${IMAP_HOST}/INBOX" \
  --user "${USER}:${PASS}" \
  -X "STATUS INBOX (MESSAGES UNSEEN)" 2>&1)

UNSEEN=$(echo "$STATUS" | grep -oP 'UNSEEN \K[0-9]+' || echo "0")
TOTAL=$(echo "$STATUS" | grep -oP 'MESSAGES \K[0-9]+' || echo "0")

echo "UNSEEN=$UNSEEN"
echo "TOTAL=$TOTAL"

if [ "$UNSEEN" -gt 0 ]; then
  # Fetch envelopes of all messages (search unseen)
  SEARCH=$(curl -s --ssl-reqd \
    "imaps://${IMAP_HOST}/INBOX" \
    --user "${USER}:${PASS}" \
    -X "SEARCH UNSEEN" 2>&1)
  echo "SEARCH_RESULT=$SEARCH"

  # Extract message numbers
  MSGIDS=$(echo "$SEARCH" | grep -oP '\* SEARCH \K.*' | tr ' ' ',')
  if [ -n "$MSGIDS" ]; then
    curl -s --ssl-reqd \
      "imaps://${IMAP_HOST}/INBOX" \
      --user "${USER}:${PASS}" \
      -X "FETCH ${MSGIDS} (ENVELOPE)" 2>&1
  fi
fi
