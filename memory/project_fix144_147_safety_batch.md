---
name: project_fix144_147_safety_batch
description: "Pre-live safety batch FIX-144/145/146/147 — position cap, cron drift monitor, premarket healthcheck, config sanity (2026-06-02, commits f1dc556/aae1543)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e4bad4f2-7a2b-4ba6-b89c-038fc51305f4
---

All 5 pre-live safety items shipped and deployed to VM.

**FIX-144: Position value hard cap**
- New field `max_position_value_rs: 50000.0` in `PositionSizingConfig` (config_loader.py) and system_config.yaml
- `PositionSizer.__init__` gets `max_position_value_rs` param; check fires after lot-size rounding
- If `final_qty * entry_price > max_position_value_rs` → CRITICAL log + `SizingResult(constraint="POSITION_VALUE_CAP")`
- Wired in `main.py` from `ps_cfg.max_position_value_rs`
- 3 new tests in test_position_sizer.py

**FIX-145: Cron drift monitor**
- Schema v23: `cron_heartbeat` table (job_name, executed_at, status, duration_sec, message)
- `core/state_store.py`: `insert_cron_heartbeat()`, `get_cron_heartbeats_since()`, `get_last_heartbeat_for_job()`
- `utils/cron_heartbeat.py`: `record_heartbeat()` + `HeartbeatTimer` context manager
- `scripts/check_cron_drift.py`: runs 18:00 IST Mon-Fri; alerts on 12 expected jobs missing heartbeats
- Heartbeats wired into: `reports/daily_review.py`, `scripts/eod_verify.py`, `scripts/gemini_log_review.py`, `scripts/wal_checkpoint.py`
- 2 new tests in test_state_store.py

**FIX-146: Pre-market health check**
- `scripts/premarket_healthcheck.py`: runs 08:30 IST Mon-Fri (before `fetch_fno_ban` which moved to 08:35)
- Checks: config files present, secrets in env (TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_PRIMARY, WEBHOOK_SECRET), DB accessible + schema version, disk space ≥2GB, clock skew
- Sends Telegram CRITICAL alert on any failure; `--dry-run` flag for testing
- REQUIRED_SECRETS uses actual .env vars (NOT Zerodha keys — those are stored separately, not in .env)

**FIX-147: Config cross-field sanity validator**
- `SystemConfig.model_validator` warns (does NOT block) on:
  - `max_position_value_rs > daily_loss_limit`
  - cumulative risk (risk_per_trade_pct × max_open_positions) exceeds 2× daily_loss_limit_pct
  - entry_end within 15 min of eod_squareoff_time
  - INTRADAY/COVER_ORDER leverage > 10×
  - min_tick_size < 0.01

**Disaster recovery doc**: `docs/disaster_recovery.md` — full restore procedure, quarterly drill checklist

**Cron changes**: 08:30 premarket_healthcheck + 18:00 check_cron_drift added; fetch_fno_ban shifted to 08:35

**Why:** Pre-live safety hardening session before scaling capital beyond Rs 25K micro account.
**How to apply:** Schema is v23 now — any fresh DB or restore needs schema migration awareness. VM crontab is updated.
