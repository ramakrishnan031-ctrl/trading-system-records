---
name: project-fix128-p0-fixes
description: "FIX-128 five P0 critical fixes — slippage guard, P&L recon, circuit breaker, daily loss kill sequence, token expiry detection"
metadata: 
  node_type: memory
  type: project
  originSessionId: 66b1f409-4cb9-4036-9b0e-6084605cf8fc
---

FIX-128 committed 2026-05-30 (commit 0cd1b14). All 5 P0 fixes implemented and tested. Schema bumped to v15.

**Why:** Five critical production gaps identified for live trading safety before next live session.

**How to apply:** These are permanent fixes; no temp changes to revert.

## Fix A: Entry Slippage Guard
- `order_placer.py`: new `signal_trigger_price` param + `max_entry_slippage_pct` (default 1%)
- If `abs(ltp - trigger) / trigger * 100 > max_entry_slippage_pct` → REJECTED, Telegram WARNING
- Gate path reuses `release_ltp`; direct path fetches fresh LTP from live_feed
- Wired via `config.system.entry_gate.max_entry_slippage_pct` (system_config.yaml)
- `signal_trigger_price` passed from signal_processor `_process_one` and `continue_from_gate`

## Fix B: Broker P&L Reconciliation
- **Schema v15**: new `pnl_reconciliation` table
- `state_store.get_today_closed_pnl()` / `upsert_pnl_reconciliation()` / `get_pnl_reconciliation()`
- `scripts/reconcile_pnl.py`: standalone EOD script; run at 16:15 IST via cron
- variance > Rs 10 → CRITICAL log + Telegram; variance > Rs 100 → SOFT_KILL (exit code 2)
- Paper mode: PAPER_SKIPPED (no broker fetch); `--dry-run` mode supported

## Fix C: Position-Level Circuit Breaker
- New `CircuitBreakerConfig` (partial_fill_timeout_minutes=5, force_close_time=15:15, max_api_failures=3)
- `order_monitor.py`: `_consecutive_api_fails` counter → `on_critical_failure` (hard_kill) after 3 general errors
- `_WatchEntry.partial_since` → cancel ENTRY stuck in PARTIAL > 5 min
- `_check_force_close()`: cancels ENTRY orders at force_close_time, fires `on_force_close` callback
- `main.py`: `_make_api_failure_hard_kill_cb` + `_make_force_close_cb` callbacks wired at construction

## Fix D: Daily Loss Limit Kill Sequence
- `main._make_daily_loss_cb()` replaces bare `lambda: kill_switch.soft_kill()`
- Sequence: (1) Telegram CRITICAL alert → (2) `eod.fire_now()` (closes positions) → (3) SOFT_KILL
- Late-binding `_eod_ref = {"eod": None}` dict avoids FundManager/EodSquareoff circular dependency
- `_eod_ref["eod"] = eod` set right after EodSquareoff construction in main()
- eod.fire_now() failure does not abort soft_kill (belt-and-braces)

## Fix E: Token Expiry Mid-Session Detection
- New `broker/token_monitor.py`: daemon thread calling `kite.profile()` every 30 min in market hours
- On expiry: CRITICAL log + Telegram CRITICAL + SOFT_KILL (NOT hard_kill; order_monitor manages exits)
- `_expiry_fired` flag ensures callback fires exactly once per session
- Paper mode: `start()` is no-op; `check_now()` always True
- Wired in main.py: starts after `order_monitor.start()`, stops in `_shutdown()`

## Test counts
- Fix A: 8 tests in `test_order_placer.py::TestFix128EntrySlippageGuard`
- Fix B: 13 tests in `tests/unit/test_fix128_pnl_reconciliation.py`
- Fix C: 12 tests in `tests/unit/test_fix128_circuit_breaker.py`
- Fix D: 8 tests in `tests/unit/test_fix128_daily_loss_sequence.py`
- Fix E: 12 tests in `tests/unit/test_fix128_token_monitor.py`

## VM deployment needed
- Schema v15 migration: run `ALTER TABLE` or wipe+recreate DB (new table only)
- Add cron at 16:15 IST: `cd /home/ubuntu/systems/trading-system && source ../venv/bin/activate && python scripts/reconcile_pnl.py --mode live`
