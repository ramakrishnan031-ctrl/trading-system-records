---
name: task_3_cron_officer
description: TASK
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b6e2dc9-1fd2-4420-a210-2ffb31a91a12
---

**TASK #3 — Cron Officer COMPLETE & DEPLOYED (18-Jun-2026).** Builds on [[cron_monitoring_audit_18jun]] (which found FIX-145 heartbeat/drift existed but was miscalibrated — 8/12 monitored jobs never emitted heartbeats).

## What shipped (commits: 3 chunks ending 6fd0ed9, pushed/deployed)
- **`config/cron_registry.yaml`** = SINGLE SOURCE OF TRUTH (30 jobs; fields: script/schedule/type/critical/market_day_only/cadence/monitored/weekday/day_of_month). Loader **`core/cron_registry.py`** (Pydantic, `extra=forbid`; cadence + NSE-holiday + due-time logic).
- **`scripts/cron_officer.py`**: `--briefing` (04:55; holiday-aware schedule), `--eod-summary` (18:30; completed/failed/skipped/missed + runtime, CRITICAL on critical-miss), `--check-change` (registry vs live `crontab -l` diff).
- **`scripts/check_cron_drift.py`** now reads the registry (hardcoded `EXPECTED_JOBS` removed); flags only monitored, due-by-now jobs; SKIPPED counts as ran.
- **Universal heartbeats**: `HeartbeatTimer(alert=True)` (in `utils/cron_heartbeat.py`) sends per-job alerts on exit; `record_heartbeat()` kept PURE. 8 silent jobs instrumented (fetch_fno_ban, fetch_daily_candles [+sys.path fix], reconcile_positions, eod_cleanup, trade_journal, compute_strategy_metrics, refresh_instruments, generate_screened_csv) + auto_refresh_token already done ([[fix_187_headless_totp]]).
- **Alert policy** `alerts/cron_alerts.py`: FAILED+critical→CRITICAL (sentinel→[[smtp_alert_watcher_config]] email fallback + Telegram), FAILED+non-critical→ERROR, SUCCESS+critical→INFO, else silent. Reuses existing `TelegramNotifier` tiers — NO new SMTP code.
- **Holiday guard** `skip_if_non_trading_day()` records a SKIPPED heartbeat (Layer 6). The 4 scripts with pre-existing `is_broker_api_available` guards ([[weekend_cron_protection]]) were left intact.

## Decisions (deviations from the spec, approved)
- Alerting lives in **HeartbeatTimer**, not inside `record_heartbeat()` (avoids layering/network-in-primitive).
- **Kill switch wins**: when `telegram.enabled` is OFF, cron alerts are FULLY silent (did NOT override it to email). Email fallback triggers only on Telegram *delivery failure*.
- `db_retention` **ACTIVATED** in the live crontab (Rama's call; protected by 01:00/01:05 backups).

## Crontab (synced + INSTALLED on VM; old crontab backed up to `data_store/crontab_backups/`)
Live `crontab -l` now == `deploy/cron/trading-system.cron` (33 lines). Changes vs prior live: `auto_refresh_token` 08:00→**08:15**; **+`cron_officer` briefing(04:55)/eod(18:30)**; **+`analytics_backup`(01:05)** (analytics.db was un-backed-up); **+`db_retention`(02:30 + Sun --vacuum)**; backup-retention now also clears `analytics-*.db`. To change cron: edit the registry → regenerate the file → `crontab deploy/cron/trading-system.cron`.

## Tests: 40 new (registry 18 + alerts/timer 12 + officer 10); 69 instrumented-script tests + 76 state_store still green. (Full VM suite recommended before next trading day.)

NOTE (separate, pre-existing): `scripts/fetch_daily_candles.py:28` has a HARDCODED Zerodha `API_KEY` in source — flag for cleanup (out of TASK #3 scope).
