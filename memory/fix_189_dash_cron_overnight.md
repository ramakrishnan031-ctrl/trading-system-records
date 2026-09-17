---
name: fix_189_dash_cron_overnight
description: FIX-189 — dash-cron source bug (all crons silently dead) + overnight-run + false-alert suppression; deployed+recovered 19-Jun
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c3b6780-736c-4396-9a65-be6d83862a10
---

FIX-189 (19-Jun-2026 morning). Root cause of the morning incident + two overnight false CRITICAL emails (04:24 capital drift, 07:07 KiteTicker reconnect exhausted).

**ROOT CAUSE (P0-A):** cron's default `/bin/sh` is **dash**, and dash's `.` (source) builtin will NOT load a relative path without a slash → the bare `. .env` in every market job failed with `sh: .: .env: not found` and the job **died before Python ran** (no 08:15 token refresh, no heartbeats, no per-cron logs — `cron-auto-token.log`/`cron-officer.log`/`cron-disk-monitor.log` simply never existed). [[fix_187_headless_totp]]'s "verified live" had only ever been exercised via a **manual bash run**, so the dash path was never tested. Fix: `deploy/cron/trading-system.cron` now leads with `SHELL=/bin/bash` **and** sources via `. ./.env` (belt-and-suspenders; either alone works). `config/cron_registry.yaml` header documents the rule for regeneration. The crontab is hand-maintained (NO python generator).

**P1-A (overnight run):** the service was started 18-Jun 23:22 by token-watcher on a leftover evening-refreshed token and ran all night; token expired ~04:30 → false alerts. Now `main.py` exits 0 outside the broad service window **[08:00–16:00 IST]** (`_within_service_window`, constants `SERVICE_WINDOW_START/END`; bypass: `--status`/`--dry-run`/`--interactive`/`--resume` or `TS_IGNORE_MARKET_WINDOW=1`), and `deploy/token_watcher.sh` `within_service_window()` gates every start site. See [[deploy_requires_restart]] — deploy ≠ restart, so the guard only took effect after the resume/restart.

**P1-A completion — EOD window-end self-exit (RESOLVED 19-Jun, commit d61ece9):** found while verifying that the assumed "EOD self-exit" did NOT exist — `main.py`'s loop is `_shutdown_event.wait()`, set ONLY by SIGINT/SIGTERM, webhook-unreachable, and shutdown; EOD squareoff just trips a scheduled SOFT_KILL; no timer/cron stops the process. So the startup guard prevented overnight *starts* but a service started in-window ran all night (harmless after P1-B, but not clean). FIX: added an `eod-self-exit` daemon thread (`_start_eod_self_exit_thread` + pure decision `_eod_self_exit_due`): once past `SERVICE_WINDOW_END` (16:00 IST) AND flat (`StateStore.count_active_positions()==0` over OPEN/PARTIAL/PENDING_FILL) it sets `_shutdown_event` → `main()` exits 0 → systemd (Restart=on-failure) won't restart → token-watcher exit-0-today skips restart → clean overnight + clean 08:30 start. **Safety guard: NEVER exits while a position is open** (stays up to manage residual; count error → stays up, fail-safe). Armed only for normal starts (skipped for `--interactive`/`--resume`/`TS_IGNORE_MARKET_WINDOW=1` so operator overrides aren't auto-stopped). Parity-safe (count is mode-agnostic). 6 tests. **Activates on next restart (≈08:30 tomorrow)** — deploy ≠ restart, so the process running since 09:28 today (old code) still runs tonight overnight (harmless via P1-B); the self-exit is live from the next start.

**P1-B (false alerts):** `order_reconciler._g3_capital_drift` skips the alert when broker `get_margins().net == 0.0` AND real capital expected AND outside market hours (Zerodha funds endpoint returns 0 overnight) — surgical, in-session net=0 still alerts; paper unaffected. `live_feed._on_noreconnect` downgrades max-reconnect-exhausted to WARNING (no SOFT_KILL / no CRITICAL) when `_market_windows.is_market_open()` is False; in-session still escalates; fail-safe escalates if no market_windows injected. Ties to [[dual_daily_loss_mechanism]] / [[capital_operational_note]] (drift reads broker margin).

**P2:** token-watcher start is window-gated + already idempotent on `ActiveState` (the 30s "Starting" hammer in the logs was the pre-FIX-188 script).

**Status:** 4 commits on main (2ac32ae P0-A, 0f722f7 P1-A/P2, 5603013 P1-B, 66380b6 doc) pushed+deployed. Crontab installed (backup `data_store/crontab_backups/crontab_pre_fix189_*.bak`); dash prefix now `rc=0`. 16 new tests; 22 FIX-189 tests pass on VM. **Recovered:** minted today's token (bash), `deploy/resume.sh` cleared SOFT_KILL, service restarted onto new code (PID 500580, 09:28 IST) → `/health` HEALTHY (db/token/kill_switch all ok), 0 auth errors since. **Remaining (EXTERNAL, Rama):** Kite dev-console IP allowlist — blocks order placement only; see [[kite_ip_allowlist_dependency]].

**Why:** a silent dash bug took out the entire cron layer (token refresh, heartbeats, EOD jobs) the first day it was relied on, and an overnight-running service spammed false CRITICALs.

**How to apply:** any cron command that sources `.env` MUST use `. ./.env` and the crontab MUST keep `SHELL=/bin/bash`; never let a long-lived trading process run outside [08:00–16:00 IST]; gate broker-derived alerts (drift, WS reconnect) on market-hours so off-hours/unauth reads don't escalate.
