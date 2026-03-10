# Integrations & logins to set up (backlog)

Last updated: 2026-03-07

## Working integrations (current)
- Telegram channel: active (DM + approved groups)
- Signal channel: active
- Google Calendar via `gog`: active (create/update events works)
- Garmin data pull: active (sleep/HRV/stress/steps/activities + training readiness endpoint)
- DALL·E/OpenAI image generation: active (tested OK)
- Imgflip API: active for caption generation (auth verified)

## Messaging
- WhatsApp
  - Goal: (TBD) send/receive messages via OpenClaw
  - Status: disabled in config (safety); requires QR link + decide which number/account

## Weather / aviation tools
- Windy
  - Goal: point forecasts, wind data for locations (paragliding/sailing/aviation)
  - Status: ✅ Active (2026-03-09) – API key i secrets.env (WINDY_API_KEY). Point Forecast API v2, modeller: gfs/ecmwf/iconEu. Fråga mig om vind/väder för valfri plats.

## Paragliding / XC
- Meteo-Parapente
  - Goal: termik- och paraglidingspecifika prognoser (BL-höjd, termikstyrka, XC-index)
  - Status: inte konfigurerat
  - URL: meteo-parapente.com
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
  - Status: configured and tested successfully (`gpt-image-1` generation OK after credits top-up)
  - Note: OpenAI API key should be used for DALL·E only; chat/model usage stays on OAuth session.
- Imgflip API
  - Goal: generate memes from templates/captions directly via OpenClaw
  - Status: auth verified (caption generation test succeeded); next step is final wiring into assistant flow + safe secret storage path

## Email domain (alexanderssons.org)
- ✅ Fully working (2026-03-09): outbound via msmtp/ForwardEmail, inbound via IMAP (imap.forwardemail.net). Morning/evening inbox checks active.

## Notes
- For any login-based service: prefer either
  1) API token stored locally (env file + systemd EnvironmentFile), or
  2) server-browser persistent profile + one-time manual login (no passwords in chat).
