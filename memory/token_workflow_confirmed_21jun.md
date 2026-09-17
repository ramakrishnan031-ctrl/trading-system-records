---
name: token_workflow_confirmed_21jun
description: Monday morning token workflow — fully automated (no PC push needed); auto_refresh_token.py at 08:15 via TOTP; token-watcher starts trading-system automatically
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b70d7c0-75fd-4f0b-9d69-93adc5e82b95
---

**Monday morning token workflow (confirmed 21-Jun-2026):**

**PC manual step: NO** — Rama does nothing for the token. The entire flow is automatic
on the VM.

**Full automated sequence (no Rama action needed):**
1. **05:00** — cron deletes yesterday's token (forces fresh login today)
2. **08:15 Mon-Fri** — `auto_refresh_token.py` (FIX-187) runs headless via cron:
   - logs into kite.zerodha.com with username + password + **pyotp TOTP** (secret
     stored in `.env` as `ZERODHA_TOTP_LFL836`) — no browser, no manual OTP, no
     phone needed
   - obtains `request_token` via the connect/login redirect
   - exchanges it for an `access_token` via `exchange_request_token()`
   - saves to `data_store/session/zerodha_token.json` (date=today, has access_token)
   - log: `logs/cron-auto-token.log`
3. **08:15-ish** — `token-watcher.service` (polls every 30s) detects fresh token
   + `within_service_window()` (08:00-16:00) → `systemctl start trading-system.service`
   → app boots headlessly (no `--resume` needed unless same-day kill-switch active)

**What Rama should actually watch Monday morning:**
- If the app DOESN'T start by ~08:20: check `logs/cron-auto-token.log` (TOTP failure
  or Kite IP-403 is the most likely cause). See [[kite_ip_allowlist_dependency]].
- Pre-flight **Phase A 08:30** will flag `kite_token_file_exists` FAIL and
  `kite_token_fresh_today` FAIL if the token didn't generate — alert email will arrive.
- `refresh_instruments.py` runs at 09:00 and requires a live Kite session (uses the
  same token). The Cron Officer morning briefing banner at 09:20 will confirm it ran.

**If Kite IP changes (e.g. OCI VM gets a new public IP):** order placement will 403.
The system self-heals alerting (1 CRITICAL/hr with the current VM IP + Kite console
steps). This is the only routine Monday manual step Rama may need to take.

**Browserless auto-token status: DONE (FIX-187, commit ff0984b, verified LIVE).** This
was the v2.1 item — it's already active. There is no future step; the daily manual
OTP has been eliminated.
