# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Integrations (as of 2026-02-04)

**Important:** The WhatsApp number **+46708979717 (JP)** shown in an earlier “Active Integrations” list was **an example**. **Do not send** messages from/to that number unless Erik explicitly requests it.

### Messaging Channels
- Telegram — bot, pairing mode (JP, Erik, Nils approved) *(per example list)*

### Telegram handles / contacts
- JP (John Patrick Berlips) — @JohnPatrickBerlips (seen in forwarded message, 2026-02-12)
- WhatsApp — (example list mentioned link to +46708979717; treat as **NOT Erik’s**)
- Discord — @Clawbot in “civic coders” + another guild

### Google Workspace (GOG CLI)
- Gmail, Calendar, Drive, Docs, Sheets, Contacts
- Account (example list): jp.berlips@gmail.com

### APIs
- OpenAI — DALL-E 3, TTS (onyx voice), Whisper
- Perplexity — sonar-pro for search
- Gemini CLI — grunt work/research
- Google Places (goplaces)
- ScraperAPI — web scraping
- Open-Meteo — weather (no auth)

### Integration TODOs
- DALL·E image generation in OpenClaw: pending OpenAI API key from Erik, then configure + test end-to-end.

### Infrastructure
- Proxmox LXC CT 510 on ax102-03-cluster1
- Headless Chromium browser
- GitHub CLI (gh) as jpberlips

### Cron Jobs (6 active) *(per example list)*
- Morning Weather — 11:00 UTC daily
- Email Triage — :00/:30 hourly
- Calendar Warnings — :15/:45 hourly
- HN Daily Top 3 — 13:00 UTC daily
- Git Sync — 23:00 UTC daily
- erik-dev-flapping — disabled

Add whatever helps you do your job. This is your cheat sheet.

### Secrets handling (local convention)
- Cloudflare API token file location on host: `/root/.openclaw/secrets.env`
- Fallback/legacy location seen: `/root/.openclaw/cloudflare.env`
- Never store raw secrets in chat logs, MEMORY.md, or committed repo files.
- Store only paths + procedure notes here, not token values.
