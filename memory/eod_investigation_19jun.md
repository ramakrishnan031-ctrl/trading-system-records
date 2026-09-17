---
name: eod_investigation_19jun
description: "Root cause of the two 19-Jun EOD flags — reconcile_positions FAILED (latent credential bug) and 144 capital-drift events (pre-fix overnight false positives, throttle worked)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 34eb8dba-9799-4234-a8dc-bb8ca1411fa8
---

**INVESTIGATION 19-Jun-2026 EOD.** Two items flagged by Cron Officer + System Manager EOD.
Both root-caused against live VM data. **✅ BOTH FIXED + DEPLOYED 19-Jun** (commits bff0cad
env-export+ItemA, 89c0c20 ItemB, c939ab2 docs). The Item-1 fix uncovered a deeper root cause —
cron jobs got NO `.env` secrets at all; see [[cron_env_export_fix]]. 130 unit tests green;
reconcile verified on VM (exit 0 + heartbeat SUCCESS); crontab reinstalled.

## ITEM 1 — reconcile_positions cron FAILED (exit 1)
- Heartbeat: `2026-06-19T15:45:01 FAILED, exit code 1, 0.23s`. Cron log:
  `reconcile_positions.broker_fetch_failed: ZERODHA_API_KEY and ZERODHA_ACCESS_TOKEN must be set`.
- **ROOT CAUSE = latent credential-wiring bug** in `scripts/reconcile_positions.py`
  `_fetch_broker_positions` (line 81-82): it reads the **generic** `ZERODHA_API_KEY` /
  `ZERODHA_ACCESS_TOKEN` env vars, which are **never set** in this deployment. The system
  uses **per-account** `ZERODHA_API_KEY_LFL836` (.env/accounts.csv) + access_token from
  `data_store/session/zerodha_token.json`. Broker fetch raises → status=ERROR → main()=1.
- **Real issue, NOT an artifact** of today's chaos and NOT the dash bug (the script ran fine:
  loaded config, logged config_sanity). It is the lone broker-cron still on generic env vars —
  `refresh_instruments.py --account` / `fetch_daily_candles.py` / `gemini_data_integrity_check.py`
  all correctly use `account.api_key_env` + `load_token(zerodha_token.json)`.
- Has **NEVER succeeded**: only one heartbeat row ever (today's FAILED — heartbeats added TASK#3
  18-Jun; FIX-189 dash bug blocked crons until 19-Jun), and `position_reconciliation` table is
  **empty** (never wrote a row). Surfaced now only because FIX-189 made crons run + TASK#3 added
  FAILED-heartbeat alerting.
- **Impact today LOW**: system was flat at 15:45 (0 open trades) and the in-process
  order_reconciler (15s) + EOD broker squareoff already cover positions — but EOD broker-vs-system
  cron reconciliation has been silently absent the whole time.
- **FIX NEEDED: YES.** Rewrite `_fetch_broker_positions` to load api_key from `account.api_key_env`
  (LFL836) + access_token from `zerodha_token.json` via `scripts.zerodha_login.load_token` (mirror
  refresh_instruments). Also add `--account LFL836` to the cron command (it currently passes none).
  Secondary: notifier was None ("Telegram env not set" — `TELEGRAM_CHANNEL_PRIMARY` missing from
  cron `.env`; BOT_TOKEN present) so even a real mismatch couldn't Telegram-alert from cron.

## ITEM 2 — 144 capital-drift "events" (NOT 144 alerts)
- "Event" = one row in `reconciliation_log` with check_name='CAPITAL_DRIFT' for the day
  (system_manager `_rl_count`). `order_reconciler._g3_capital_drift` returns a non-COSMETIC
  CAPITAL_DRIFT action **every 15s cycle** that delta>tolerance, and every non-COSMETIC action is
  logged → the row count is **per-cycle**, decoupled from the alert.
- **143 of 144 were overnight/pre-market**: hourly 03h=24, 04h=119, 10h=1; window 03:54→10:00:37.
  Overnight rows are the textbook FIX-189 false positive:
  `Broker capital=0.00 vs local=10009.30 delta=10009.30 tolerance=50.00` (Zerodha funds endpoint
  returns net=0.0 overnight). The lone in-session row at 10:00:37 is
  `Broker=9512.88 vs local=10016.60 delta=503.72 tolerance=50.00` = the "10:00 Δ503 noise" the
  FIX-190 Bug I comment names (deployed-capital drift during the morning burst).
- **Both are pre-fix artifacts.** tolerance shows base 50 (un-widened) → the writing processes
  predate FIX-189 P1-B (net=0.0 skip) and FIX-190 Bug I (in-session widening). Caused by the
  18-Jun 23:22 overnight process + the 09:28 pre-fix morning process. **Zero drift rows after
  10:00:37** — the 13:24 fixed-code resume produced NO drift noise. Proof the fixes work.
- **Throttle (TASK-11, 30 min) WORKED PERFECTLY**: 144 detections → **3 alerts sent**, 141
  suppressed. Alert timestamps 03:54:00 (first), 04:24:25 (+30 min), 10:00:37 (fresh in-session
  after reset). NOT 144 alerts.
- **FIX NEEDED: NO** (already fixed by FIX-189 + FIX-190, active post-restart / Monday 08:30).
  Optional polish only: `_g3_capital_drift` writes a `reconciliation_log` row every suppressed
  cycle, so the "event count" inflates even when alerts are correctly throttled — could log only
  on alert-sent (or on state change) so System Manager's count reflects episodes not cycles.
  Cosmetic/metrics, not a safety issue.

Context: chaotic day (HARD_KILL cleared, 3 manual closes, 1 orphan, SOFT_KILL force_close_15:15
pending resume Mon; 5501 signals recv vs 2870 prev). Related: [[fix_189_dash_cron_overnight]],
[[fix_190_incident]], [[task_11_drift_alert_interval]], [[task_5_system_manager]], [[task_3_cron_officer]].
