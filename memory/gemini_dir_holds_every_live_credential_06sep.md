---
name: gemini_dir_holds_every_live_credential_06sep
description: /home/ubuntu/.gemini holds every live Zerodha + Telegram credential in plaintext across ~28 world-readable files; rotating .env alone never rotated them.
metadata: 
  node_type: memory
  type: project
  originSessionId: 9f103ec2-6ea8-4b32-a0ca-586e0765e2af
  modified: 2026-09-05T20:55:06.016Z
---

🔴🔴 **VERIFIED 06-Sep-2026 ON PRODUCTION. LIVE. UNREMEDIATED.**

`/home/ubuntu/.gemini` — **1.2 GB, 7,029 files, 6,835 of them group/other-readable**
(modes 644 / 444 / 664), versus `.env` at **600**.

🔬 **Every live secret in `.env` was found there, by exact-value match, counting
files only (no value printed):**

| Secret | Files in `.gemini` |
|---|---|
| `ZERODHA_API_KEY_LFL836` | **31** |
| `ZERODHA_API_SECRET_LFL836` · `ZERODHA_TOTP_LFL836` | **28** each |
| `ZERODHA_API_KEY/SECRET/TOTP` for **DR6114, D351962, ZA004, ZA005** | **28** each |
| `ZERODHA_PASSWORD` | **28** |
| `TELEGRAM_BOT_TOKEN` | **28** |
| `TELEGRAM_CHANNEL_PRIMARY` | **318** |
| `ALERT_EMAIL_USER` / `_TO` | **59** |

⭐ **THE POSITIVE CONTROL — this zero could have been red and was:**
🔬 the **OLD** (pre-rotation) `WEBHOOK_SECRET` appears in **28** files; the **NEW**
one in **0**. ⇒ ⭐ The scan demonstrably fires, and the 06-Sep rotation is the
**only** credential that escaped — because it post-dates these files.
🔬 `ALERT_SMTP_PASSWORD` and `ALERT_EMAIL_PASSWORD` are also **0**, so the match is
selective, ⛔ not a false-positive carpet → [[feedback_verify_rc_not_output]].

🔴 **THE CONSEQUENCE THAT MATTERS: rotating `.env` DOES NOT ROTATE THESE.**
⭐ 5 accounts × (api_key + api_secret + totp_seed) + the account password + the
Telegram bot token are sitting in plaintext, world-readable, in a directory nobody
audits. ⛔ Any backup, `rsync`, home-dir copy, or process running as any user
carries the full live set.

⏸ **OWED (independent of any sandbox, and overdue):** rotate both Zerodha API
secrets in use, **all** TOTP seeds, the account password, and the Telegram bot
token — then re-run the scan above and confirm the counts go to 0.
⛔ **A `**/*.db` exclusion glob covers only 2 of the ~28 files** (the mix is ~22
`.env`, 4 `.jsonl`, 1 `.db`, 1 `.db-wal`). ⭐ Exclude the **whole directory**, always.

⚠️ **Self-disclosure:** this was found by subagents that read the real values to
do the matching, so the plaintext passed through their transcripts under
`.claude/projects/.../subagents/`. ⭐ Treat those transcripts as secret-bearing.
