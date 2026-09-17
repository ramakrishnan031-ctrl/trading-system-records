---
name: cron_monitoring_audit_18jun
description: "Pre-\"Cron Officer\" audit — what cron-monitoring already exists (FIX-145 heartbeat + drift) and the miscalibration gap to fix rather than rebuild"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b6e2dc9-1fd2-4420-a210-2ffb31a91a12
---

Investigation 18-Jun-2026 (no code changes) — existing cron-monitoring capability before building a "Cron Officer". **Reuse the FIX-145 infra; do NOT rebuild it. Fix its miscalibration.**

## What already exists (FIX-145, schema v23)
- **`utils/cron_heartbeat.py`** — `record_heartbeat(job_name, status="SUCCESS", duration_sec, message)` + unused `HeartbeatTimer` context manager. Never raises; no-op if DB missing.
- **`cron_heartbeat` table** (`core/schema.sql:901`): id, job_name, executed_at(ISO IST), status(SUCCESS|PARTIAL|FAILED default SUCCESS), duration_sec, message. Indexed on job_name + executed_at. StateStore: `insert_cron_heartbeat` / `get_cron_heartbeats_since` / `get_last_heartbeat_for_job` (`core/state_store.py:2020-2067`).
- **`scripts/check_cron_drift.py`** (cron 18:00 Mon-Fri) — the ONLY heartbeat consumer. Hardcoded `EXPECTED_JOBS` dict (12 jobs). Alerts (Telegram WARNING via `from_config`) only on MISSING heartbeat in last 24h. Binary missing/not — no report, no FAILED/duration awareness.

## THE GAP (headline finding — non-obvious)
The 3 "registries" disagree. Only **11 scripts actually call `record_heartbeat()`**, and the call is always bare (`record_heartbeat("name")`) → status always SUCCESS, duration_sec/message always NULL. `HeartbeatTimer` is used by NOTHING, so a FAILED heartbeat is never written. `get_last_heartbeat_for_job` has no production caller.

Cross-referencing EXPECTED_JOBS (12 monitored) vs emitters: **8 of 12 monitored jobs NEVER emit a heartbeat** → `check_cron_drift` reports them "missing" EVERY weekday (perpetual false-positive Telegram, likely muted as noise):
- FALSE POSITIVE (monitored, no heartbeat): auto_refresh_token, fetch_fno_ban, fetch_daily_candles, reconcile_positions, eod_cleanup, daily_report, trade_journal, compute_strategy_metrics
- Correctly wired (monitored + emits): eod_verify, daily_review, wal_checkpoint, gemini_log_review
- Emit but NOT monitored (heartbeat nobody reads): premarket_healthcheck, gemini_premarket_brief, gemini_trade_coach, gemini_data_integrity_check, gemini_weekly_patterns, capture_metrics_baseline, backup_restore_drill

## Other findings
- **No job registry file** (no YAML/JSON catalog). Sources of truth: `deploy/cron/trading-system.cron` (canonical, ~28 jobs, but live crontab DIVERGES) and the hardcoded EXPECTED_JOBS dict. No DB-backed schedule.
- **No wrapper script.** `deploy/` has only `install_vm_services.sh` + `token_watcher.sh` (neither is a cron wrapper). Exit-code convention 0=ok/1=err is consistent but cron only appends stdout to per-job `logs/cron-*.log`; nothing reads exit codes.
- **Telegram from cron**: ~14 scripts send via `TelegramNotifier.from_env()`; `check_cron_drift` is the lone `from_config()`. **Silent jobs (no Telegram, no alert on failure)**: auto_refresh_token (critical!), eod_cleanup, fetch_daily_candles, trade_journal, compute_strategy_metrics, wal_checkpoint, generate_screened_stocks_csv, refresh_instruments, db_retention.
- **No report summarizes cron execution.** daily_report/daily_review only record their OWN heartbeat; neither tabulates job runs. check_cron_drift is the only (binary) status surface.

## Recommendation for "Cron Officer"
Reuse table + helpers; do NOT duplicate. Build = (1) single source-of-truth job registry replacing the hardcoded EXPECTED_JOBS + reconciling the diverged crontab; (2) wire heartbeats into the 8 unmonitored-monitored jobs (or auto-instrument via wrapper); (3) capture status/duration/exit-code (use HeartbeatTimer or a wrapper) so FAILED is actually recorded; (4) an EOD execution summary. Relates to [[task_4_system_map]] (crontab divergence flagged), [[order_reconciliation_audit_18jun]], [[weekend_cron_protection]] (is_broker_api_available skips return 0 before heartbeat).
