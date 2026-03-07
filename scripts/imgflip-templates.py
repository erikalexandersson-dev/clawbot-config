#!/usr/bin/env python3
"""Imgflip helper: fetch/search meme templates without auth.

Usage examples:
  python3 scripts/imgflip-templates.py --top 20
  python3 scripts/imgflip-templates.py --search drake --top 10
  python3 scripts/imgflip-templates.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import Any

API_URL = "https://api.imgflip.com/get_memes"


def fetch_templates(timeout: int = 15) -> list[dict[str, Any]]:
    req = urllib.request.Request(API_URL, headers={"User-Agent": "openclaw-imgflip-helper/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if not data.get("success"):
        raise RuntimeError(f"Imgflip API returned failure: {data}")

    memes = data.get("data", {}).get("memes", [])
    if not isinstance(memes, list):
        raise RuntimeError("Unexpected Imgflip response format")
    return memes


def search_templates(memes: list[dict[str, Any]], query: str | None) -> list[dict[str, Any]]:
    if not query:
        return memes
    q = query.strip().lower()
    return [m for m in memes if q in str(m.get("name", "")).lower()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", default=None, help="Filter by name substring")
    parser.add_argument("--top", type=int, default=25, help="Max rows to print")
    parser.add_argument("--json", action="store_true", help="Print full JSON")
    args = parser.parse_args()

    try:
        memes = fetch_templates()
    except Exception as e:
        print(f"Error fetching templates: {e}", file=sys.stderr)
        return 1

    filtered = search_templates(memes, args.search)

    if args.json:
        print(json.dumps(filtered[: args.top], ensure_ascii=False, indent=2))
        return 0

    print(f"Templates: {len(filtered)} match(es)" + (f" for '{args.search}'" if args.search else ""))
    print("id\tname\tbox_count\turl")
    for m in filtered[: args.top]:
        print(f"{m.get('id')}\t{m.get('name')}\t{m.get('box_count')}\t{m.get('url')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
