# Imgflip integration notes

Updated: 2026-03-07

## What is ready now
- Public template discovery works without credentials.
- Helper script added:
  - `scripts/imgflip-templates.py`
- Verified live API call:
  - `python3 scripts/imgflip-templates.py --search drake --top 5`

## What remains (needs Erik input)
- Credentials for image generation endpoint (`caption_image`):
  - Imgflip username
  - Imgflip password

## Planned next step once creds exist
- Add script for caption generation (template id + text lines -> meme URL)
- Wire into routine assistant flow for "make meme" requests
