---
name: gemini_agy_auth_check
description: gemini_*.py crons auth via the agy CLI binary + OAuth (no API key); GEMINI_API_KEY is unused; crons working; no gemini->agy rename needed
metadata: 
  node_type: memory
  type: reference
  originSessionId: 34eb8dba-9799-4234-a8dc-bb8ca1411fa8
---

**INVESTIGATION 19-Jun-2026 (report-only).** Does the missing GEMINI_API_KEY matter, and
are the gemini/agy crons working? **Answer: GEMINI_API_KEY is a NON-ISSUE; crons work; no fix.**

## How the gemini crons authenticate
- All `scripts/gemini_*.py` (log_review, trade_coach, data_integrity_check, premarket_brief,
  weekly_patterns, watchman) delegate to **`scripts/agy_runner.py`**.
- `agy_runner` invokes the **`agy` CLI binary** via `subprocess.run([agy_bin, "--model", model,
  "--print", prompt, "--dangerously-skip-permissions"])` with a Tier-1/Tier-2 model cascade
  (Claude Sonnet → Gemini Pro / Gemini Flash; Opus + GPT-OSS forbidden) and quota-text detection.
- **NO API key. NO `google.generativeai`/`genai` SDK.** Auth is the agy CLI's own **OAuth**
  (browser Google login) — tokens in `~/.gemini/oauth_creds.json` (refresh cred, Jun 3) +
  `~/.gemini/antigravity-cli/antigravity-oauth-token` (active token, refreshed 19-Jun 16:20).
- Binary resolved by `get_agy_bin()`: `GEMINI_BIN` env → `which agy` → known paths. On VM:
  **`GEMINI_BIN=/home/ubuntu/tools/antigravity/agy`** in `.env` (164 MB binary, present); `agy` is
  NOT in PATH but the known-path `/home/ubuntu/tools/antigravity/agy` also covers it. `agy_runner`
  calls `load_dotenv()` itself at import, so GEMINI_BIN reaches it regardless of the cron env-export.

## Currently working? YES
- `cron_heartbeat` gemini_* today: **SUCCESS** for the scheduled afternoon runs — log_review 16:2x,
  trade_coach 16:30/16:45, data_integrity_check 17:00 (plus 12:2x-12:39 manual test runs).
- Those 16:20-17:00 SUCCESS runs were under the OLD crontab (plain `. ./.env`, pre [[cron_env_export_fix]])
  → PROVES the gemini crons do NOT depend on cron env-export (agy_runner self-loads .env). My env-export
  fix neither broke nor was needed by them.

## Verdicts
- **Missing GEMINI_API_KEY matters? NO.** Repo-wide grep: GEMINI_API_KEY appears only in docs/comments
  (incl. my own SYSTEM_MAP env-export note + cron header example) — **zero functional code reads it**.
  The env-export probe's "GEMINI_API_KEY MISSING" was a false alarm. (Minor doc cleanup: SYSTEM_MAP line
  ~80 lists GEMINI_API_KEY as a .env secret + my env-export note cites it as an example — both misleading.)
- **gemini→agy rename needed? NO (functional).** The code already invokes `agy` (GEMINI_BIN→agy;
  module is `agy_runner`; cascade is the AGY/Antigravity stack). Only COSMETIC legacy naming remains:
  `gemini_*.py` filenames, the `GEMINI_BIN` env-var name, and the unused `/usr/local/bin/gemini` node
  symlink. Renaming would touch cron registry + crontab + imports for zero functional gain → not worth it.
- **Fix needed? NO.** Optional cosmetic-only: drop GEMINI_API_KEY from docs; (later) rename gemini→agy.

Related: [[cron_env_export_fix]], [[fix_160_agy_cascade]], [[agy_automation_status]], [[task_3_cron_officer]].
