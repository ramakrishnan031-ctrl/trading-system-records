---
name: project-fix136-batch9
description: FIX-136 batch9 complete (Items 44fix+50-56); 2625 green (+54); commit e55cb59; deployed to VM
metadata: 
  node_type: memory
  type: project
  originSessionId: f6dc0b34-b28a-4065-8bcc-d317b22c1ef2
---

FIX-136 batch9 shipped 2026-05-31, commit e55cb59, pushed + deployed to VM.

## Items completed

- **Item 44 fix**: F&O ban URL moved to config (FnoBanConfig); fail-closed sentinel `__FETCH_FAILED__` blocks ALL F&O when fetch fails; response schema validation; CRITICAL Telegram alert
- **Item 50**: `check_holiday_calendar()` validates nse_holidays_YYYY.yaml (min 10, correct year, no dupes); check #11 in startup; WARNING only
- **Item 51**: `expires_at` now correctly = `received_at + expiry_sec` (was just received_at); Telegram WARNING on expired signals (rate-limited 60s)
- **Item 52**: Dashboard completion: Avg R:R, Max Drawdown %, Kill Switch Events, Rejection Breakdown
- **Item 53**: Score Breakdown column in Sheet 1_Signals; Score Breakdown by Strategy section in Sheet 6
- **Item 54**: R:R enforcement gate in OrderPlacer; `min_effective_rr=1.0` in entry_gate config; OrderRejectedError on poor R:R
- **Item 55**: `check_sdk_version()` startup check; BLOCKING on version mismatch; kiteconnect pin comment updated
- **Item 56**: `--backfill --from --to` flags for fetch_daily_candles.py; refactored to _fetch_single_day()

## Test counts
- Baseline: 2571 passed, 12 skipped
- After: 2625 passed, 12 skipped (+54 new, 0 failures)
- New test files: test_fix136_batch9.py (44 tests), test_fix135_fno_ban.py (+7 = 19 total)

## Config changes
- system_config.yaml: `fno_ban` section (url, fail_closed, min_expected_fields); `entry_gate.min_effective_rr: 1.0`
- config_loader.py: FnoBanConfig class; min_effective_rr on EntryGateConfig
- Cron: 17 entries synced (last synced 2026-05-31)

**Why:** Audit batch 9 — hardening signal pipeline, risk controls, observability, and historical data.
**How to apply:** All items are permanent fixes. R:R gate and SDK pin are BLOCKING startup checks.
