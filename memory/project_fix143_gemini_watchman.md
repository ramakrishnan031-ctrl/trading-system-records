---
name: fix143-gemini-watchman
description: FIX-143 Gemini live watchman + EOD review via Gemini CLI (replaces API)
metadata: 
  node_type: memory
  type: project
  originSessionId: 6591cd1c-16df-4ff5-aec0-9c762da1597e
---

FIX-143 shipped (2026-06-02, commit a6d15bb): Two-mode Gemini log analysis.

**Mode A — Live Watchman** (`scripts/gemini_watchman.py`):
- Tails `system_YYYY-MM-DD.log` during 09:15-16:30 IST
- Batches WARNING+ entries every 5 min (or 20+ lines early trigger)
- Pipes to Gemini CLI (`gemini -p "prompt"` with stdin data)
- Appends analysis to `reports/watchman/watchman_YYYY-MM-DD.md`
- Critical findings → Telegram alert
- Runs as systemd service: `trading-watchman.service` (BindsTo trading-system)

**Mode B — EOD Review** (`scripts/gemini_log_review.py`):
- Rewritten from Gemini Python API to Gemini CLI (no API key needed)
- Reads full day's log + watchman notes for structured report
- Output: `reports/log_review/eod_review_YYYY-MM-DD.md`
- Cron: `20 16 * * 1-5`

**VM Setup:**
- Node.js 20 (nodesource) + `@google/gemini-cli@0.44.1`
- Installed at `/home/ubuntu/tools/gemini/` (isolated from systems/)
- Symlinked: `/usr/local/bin/gemini`
- Auth: Google OAuth credentials at `~/.gemini/gemini-credentials.json`

**Why:** Replaces the FIX-142 stub that used `google.generativeai` Python SDK (required API key). CLI uses Google account auth already on the VM.

**How to apply:** Both scripts use `GEMINI_BIN` env var (default: `gemini`). If CLI breaks, check Node.js version (needs 20+) and auth at `~/.gemini/`.

**Auth note (2026-06-02):** Re-authenticated with new Gmail account — test passed, no script changes needed. The `gemini` command handles OAuth transparently regardless of which Google account is used.
