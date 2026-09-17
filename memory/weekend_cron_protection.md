---
name: weekend_cron_protection
description: is_broker_api_available() guard stops weekend/after-hours Zerodha cron calls (FIX-180 Part 12)
metadata: 
  node_type: memory
  type: reference
  originSessionId: c451e7dc-8922-4a48-8e2b-40197f2c20a4
---

`core/market_windows.py` (NOT `market_hours.py`) has `is_market_day(dt=None)` and `is_broker_api_available(dt=None)`. `is_broker_api_available` returns False on Sat/Sun and Friday at/after 17:30 IST (boundary uses `dt.time() >= time(17,30)`); True Mon-Thu and Fri before cutoff. Weekday/time only — NOT holiday-aware (holiday scheduling stays at cron day-field `1-5` + `MarketWindows.is_trading_holiday`).

Broker-calling cron scripts guard on it at startup: `premarket_healthcheck.py` (top of main), `fetch_daily_candles.py` (default no-arg run only; `--backfill`/date allowed any day), `reconcile_positions.py` & `reconcile_pnl.py` (only when live AND `args.date is None`, so paper mode + `--date` backfills still run). `gemini_premarket_brief.py` and `capture_metrics_baseline.py` make no broker calls → no guard.

All broker-dependent cron entries already use day-field `1-5` (verified). Part of [[fix_180_complete]].
