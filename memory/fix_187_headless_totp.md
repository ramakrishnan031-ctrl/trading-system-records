---
name: fix_187_headless_totp
description: FIX-187 headless Zerodha TOTP auto-refresh — implemented+deployed (commit ff0984b); live login NOT yet verified (TOTP secret .env issue); never brute-force TOTP
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b6e2dc9-1fd2-4420-a210-2ffb31a91a12
---

**FIX-187 (18-Jun-2026): headless Zerodha TOTP token refresh** — eliminates the daily manual OTP step. Commit **ff0984b** (pushed/deployed to VM working tree; cron script, NOT the main service → no restart needed, see [[deploy_requires_restart]]).

## What was built (scripts/auto_refresh_token.py rewrite)
- Fixed **P0-A** (token format): now reuses `scripts/zerodha_login.py` `exchange_request_token` + `save_token`, so the token JSON carries `account_id/broker/api_key/date/expires_at`. Old minimal format `{access_token,user_id,login_time}` failed `is_token_valid()` (main.py:1541 live startup → exit 6) and lacked `api_key` (paper quote provider KeyError, main.py:336).
- Fixed **P0-B** (request_token): obtained from the `connect/login?v=3&api_key=` **redirect chain** (Location header), not the `/api/twofa` body. Browser User-Agent set ([[fix_184_scanner_ua_403]] lesson).
- Creds resolved **account-specific (accounts.csv `*_env`) → generic fallback** via `AccountRegistry`. Script does its own `load_dotenv()`, so `.env` does NOT need `export` (works with bare `KEY=value`).
- Telegram CRITICAL/INFO, 3× network backoff, 1× TOTP clock-skew retry, records cron heartbeat (status+duration → fixes the `auto_refresh_token` drift false-positive in [[cron_monitoring_audit_18jun]]).
- `pyotp==2.9.0` added to requirements.txt AND installed in VM venv (was NOT installed). `account_registry.totp_secret_env` doc updated (no longer "UNUSED"). 20 unit tests pass; `test_zerodha_login`+`test_account_registry` 39 pass.

## STATUS: ✅ VERIFIED LIVE (2026-06-18 20:36 IST)
Headless login succeeded end-to-end: `exit=0`, token `is_token_valid(LFL836)=True` (account_id/date/api_key/access_token/expires_at all correct), live `kite.profile()` OK (broker=ZERODHA), heartbeat SUCCESS (0.25s). Daily manual OTP step eliminated; runs 08:00 Mon-Fri via existing cron.

### The TOTP-secret saga (lesson — cost 2 of N login attempts)
1. Two DIFFERENT 32-char secrets existed: stale `ZERODHA_TOTP_LFL836` (prior enrollment, invalidated when Kite TOTP was re-enrolled) + the correct freshly-enrolled one added (per task PRE-WORK) as generic `ZERODHA_TOTP_SECRET`. Script correctly preferred the account-specific canonical name → used the STALE one → "Invalid TOTP".
2. First .env fix removed BOTH (no `ZERODHA_TOTP_LFL836` line at all → empty → would have wasted another attempt; caught offline).
3. Resolved: re-added `ZERODHA_TOTP_LFL836=<correct secret>`; verified OFFLINE (`pyotp.verify(authenticator_code, valid_window=1)=True`) BEFORE the live run. Single source of truth now = `ZERODHA_TOTP_LFL836` (generic dup removed).

## Operational rules (hard-won)
- **NEVER brute-force TOTP** — Kite locks the account after N bad codes. Before ANY live login attempt, verify the secret OFFLINE: `pyotp.TOTP(secret).now()` vs the Google Authenticator code (use `verify(code, valid_window=2)`). Mobile-app login validates account/password but NOT the secret string in `.env`.
- Single source of truth for the TOTP secret = the account-specific var `ZERODHA_TOTP_LFL836`; do not keep generic `ZERODHA_TOTP_SECRET` duplicates.
- VM clock was synced (IST) — skew ruled out. Login/reads are unaffected by the order-IP allowlist ([[kite_ip_allowlist_dependency]]).
- Cron unchanged: 08:00 Mon-Fri `auto_refresh_token.py`. After live verify: update SYSTEM_MAP (TOTP env note + "daily ops now headless") and this note's STATUS.
