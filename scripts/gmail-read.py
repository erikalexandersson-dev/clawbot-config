#!/usr/bin/env python3
"""
gmail-read.py — Läs brödtext från Gmail via API

Användning:
  python3 gmail-read.py <message-id>
  python3 gmail-read.py <message-id> --json
  python3 gmail-read.py --search "is:unread newer_than:1d" --max 5
"""

import sys
import os
import json
import argparse
import subprocess
import base64
import re
import tempfile
from urllib import request, parse, error

ACCOUNT = "erik.alexandersson@gmail.com"
GOG_KEYRING_PASSWORD = os.environ.get("GOG_KEYRING_PASSWORD", "ERIKSBOTISSTUPID")
CREDENTIALS_PATH = "/root/.config/gogcli/credentials.json"
TOKEN_CACHE = "/tmp/gmail-access-token.json"


def get_access_token():
    """Hämta access token via refresh token + client credentials."""
    # Kolla cache
    if os.path.exists(TOKEN_CACHE):
        try:
            with open(TOKEN_CACHE) as f:
                cached = json.load(f)
            import time
            if cached.get("expires_at", 0) > time.time() + 60:
                return cached["access_token"]
        except Exception:
            pass

    # Exportera refresh token
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = GOG_KEYRING_PASSWORD
    with tempfile.NamedTemporaryFile(suffix=".json", delete=True) as tf:
        token_file = tf.name
    # gog vägrar skriva om befintlig fil – se till att den inte finns
    if os.path.exists(token_file):
        os.unlink(token_file)

    result = subprocess.run(
        ["gog", "auth", "tokens", "export", ACCOUNT, "--out", token_file],
        capture_output=True, text=True, env=env
    )
    if result.returncode != 0:
        print(f"Fel: kunde inte exportera token\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    with open(token_file) as f:
        token_data = json.load(f)
    os.unlink(token_file)

    refresh_token = token_data["refresh_token"]

    # Hämta client credentials
    with open(CREDENTIALS_PATH) as f:
        creds = json.load(f)

    client_id = creds["client_id"]
    client_secret = creds["client_secret"]

    # Byt refresh token mot access token
    body = parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode()

    req = request.Request(
        "https://oauth2.googleapis.com/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with request.urlopen(req) as resp:
        token_resp = json.loads(resp.read())

    import time
    access_token = token_resp["access_token"]
    expires_at = time.time() + token_resp.get("expires_in", 3600)

    # Spara cache
    with open(TOKEN_CACHE, "w") as f:
        json.dump({"access_token": access_token, "expires_at": expires_at}, f)

    return access_token


def gmail_api(token, path, params=None):
    """Anropa Gmail API."""
    base = "https://gmail.googleapis.com/gmail/v1/users/me"
    url = f"{base}/{path}"
    if params:
        url += "?" + parse.urlencode(params)
    req = request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read())
    except error.HTTPError as e:
        body = e.read().decode()
        print(f"API-fel {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def decode_body(part):
    """Avkoda base64url-kodad brödtext."""
    data = part.get("body", {}).get("data", "")
    if not data:
        return ""
    padded = data + "=" * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")


def strip_html(html):
    """Enkel HTML-strippning."""
    text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&#[0-9]+;', '', text)
    text = re.sub(r'&[a-z]+;', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_text(payload):
    """Extrahera plaintext rekursivt, HTML som fallback."""
    mime = payload.get("mimeType", "")
    parts = payload.get("parts", [])

    if mime == "text/plain":
        return decode_body(payload)
    if mime == "text/html" and not parts:
        return strip_html(decode_body(payload))
    if parts:
        # Försök text/plain först
        for part in parts:
            if part.get("mimeType") == "text/plain":
                result = extract_text(part)
                if result:
                    return result
        # Sedan multipart/alternative eller annat
        for part in parts:
            result = extract_text(part)
            if result:
                return result
    return ""


def get_headers(payload):
    headers = {h["name"].lower(): h["value"] for h in payload.get("headers", [])}
    return {
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", ""),
        "date": headers.get("date", ""),
    }


def fetch_message(token, msg_id, as_json=False, max_chars=4000):
    msg = gmail_api(token, f"messages/{msg_id}", {"format": "full"})
    headers = get_headers(msg.get("payload", {}))
    body = extract_text(msg.get("payload", {}))

    if as_json:
        print(json.dumps({
            "id": msg_id,
            "from": headers["from"],
            "to": headers["to"],
            "subject": headers["subject"],
            "date": headers["date"],
            "body": body[:max_chars],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Från:    {headers['from']}")
        print(f"Till:    {headers['to']}")
        print(f"Ämne:    {headers['subject']}")
        print(f"Datum:   {headers['date']}")
        print("─" * 60)
        truncated = body[:max_chars]
        print(truncated)
        if len(body) > max_chars:
            print(f"\n[... {len(body) - max_chars} tecken utelämnade]")


def search_and_show(token, query, max_results=5, as_json=False):
    result = gmail_api(token, "messages", {"q": query, "maxResults": max_results})
    messages = result.get("messages", [])
    if not messages:
        print("Inga mail hittades.")
        return
    for m in messages:
        fetch_message(token, m["id"], as_json=as_json)
        if not as_json:
            print("\n" + "═" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Läs Gmail-brödtext")
    parser.add_argument("message_id", nargs="?", help="Gmail message ID")
    parser.add_argument("--search", "-s", help="Gmail-sökning")
    parser.add_argument("--max", "-m", type=int, default=5, help="Max resultat")
    parser.add_argument("--chars", "-c", type=int, default=4000, help="Max tecken per mail")
    parser.add_argument("--json", "-j", action="store_true", dest="as_json")
    args = parser.parse_args()

    token = get_access_token()

    if args.message_id:
        fetch_message(token, args.message_id, as_json=args.as_json, max_chars=args.chars)
    elif args.search:
        search_and_show(token, args.search, max_results=args.max, as_json=args.as_json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
