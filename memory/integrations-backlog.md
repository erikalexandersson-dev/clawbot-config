# Integrations & logins to set up (backlog)

Last updated: 2026-03-06

## Messaging
- WhatsApp
  - Goal: (TBD) send/receive messages via OpenClaw
  - Status: disabled in config (safety); requires QR link + decide which number/account

## Weather / aviation tools
- Windy
  - Goal: (TBD) forecasts/meteograms, wind layers, alerts
  - Status: not configured

## Paragliding / XC
- XContest
  - Goal: scrape/search flights, fetch stats; likely needs login for lists/search
  - Status: not configured (public detail pages only without login)

## Flight logging
- flightlog.org
  - Goal: read/update flight logs
  - Status: not configured

## Health / glucose
- Glooko / Sugarmate
  - Goal: view glucose trends/alerts; potential export
  - Status: Glooko login works via browser profile (`eu.my.glooko.com`, Summary/Graphs accessible); automation/reporting still to refine

## Image generation
- DALL·E (OpenAI)
  - Goal: generate images directly from chat prompts in OpenClaw
  - Status: pending OpenAI API key from Erik, then configure tool + run a test generation
- Imgflip API
  - Goal: generate memes from templates/captions directly via OpenClaw
  - Status: helper prepared (`scripts/imgflip-templates.py`) with live template fetch/search working without auth; pending credentials for actual `caption_image` generation and final wiring

## Notes
- For any login-based service: prefer either
  1) API token stored locally (env file + systemd EnvironmentFile), or
  2) server-browser persistent profile + one-time manual login (no passwords in chat).
