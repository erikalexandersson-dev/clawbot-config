#!/usr/bin/env python3
"""One-time Garmin Connect login to create reusable token files.

Usage:
  GARMIN_EMAIL='you@example.com' GARMIN_PASSWORD='secret' python3 scripts/garmin-login.py
  python3 scripts/garmin-login.py --email you@example.com --tokens memory/garmin_tokens
"""

from __future__ import annotations

import argparse
import getpass
import os
from pathlib import Path

import garth


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", default=os.getenv("GARMIN_EMAIL"))
    parser.add_argument("--password", default=os.getenv("GARMIN_PASSWORD"))
    parser.add_argument("--tokens", default="memory/garmin_tokens")
    args = parser.parse_args()

    email = args.email or input("Garmin email: ").strip()
    password = args.password or getpass.getpass("Garmin password: ")

    token_dir = Path(args.tokens)
    token_dir.mkdir(parents=True, exist_ok=True)

    garth.login(email, password)
    garth.save(str(token_dir))

    print(f"✅ Tokens saved to: {token_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
