#!/usr/bin/env bash
set -euo pipefail

# Weekly OpenClaw auto-update (non-interactive).
# Logs to journald via systemd.

/usr/bin/openclaw update --yes
