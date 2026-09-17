---
name: project-fix148-broker-gaps
description: "FIX-148: 6 broker integration gaps — RMS handling, naked position protection, SL fallback, network recovery, partial RMS, modify retry (2026-06-03, commit a0c9a20)"
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

FIX-148 shipped (2026-06-03, commit a0c9a20): 6 broker integration gaps fixed.

**P1 (GAP 5 HIGH): RMS Auto-Squareoff**
- `ZerodhaAdapter.get_trades()` added — wraps `kite.trades()` for today's trade book
- CHECK 1 (`_check1_manual_close`) rewritten:
  - `_resolve_exit_price()`: broker trades → LTP fallback → entry proxy
  - `_cancel_orphaned_orders_for_trade()`: cancels open SL/TGT for closed position
  - CRITICAL Telegram with real PnL (was silent before)
- Paper mode: `get_trades()` returns `[]`

**P2 (GAP 4 MEDIUM): Naked Position Protection**
- CHECK 9 (`_check9_missing_exits`) enhanced:
  - `_emergency_market_close()`: places MARKET exit when SL missing from broker
  - Persists emergency order in DB as leg="EOD"
  - CRITICAL Telegram: "NAKED POSITION — {symbol}"

**P3 (GAP 1 MEDIUM): SL Placement Failure Market Exit**
- `OrderPlacer._emergency_market_exit()` added:
  - Places MARKET opposite-side order via `engine.adapter.place_order()`
  - Persists + tracks via fill_map + order_monitor
  - CRITICAL Telegram: "EMERGENCY EXIT — {symbol}"
- Wired into 3 failure paths:
  - `_place_limit_triple_exits` non-LTP error
  - `_retry_limit_triple_exits` LTP retries exhausted (was soft_kill → now hard_kill)
  - `_retry_limit_triple_exits` non-LTP retry error

**P4 (A2 MEDIUM): Network Recovery Logging**
- `OrderMonitor._process_order()`: logs WARNING on recovery from consecutive auth/API failures
- FIX-089 (chronological inversion guard) already covers state machine transitions

**P5 (A3 MEDIUM): Partial RMS Exit**
- CHECK 4 (`_check4_partial_close`) enhanced:
  - Cancels stale SL/TGT orders (wrong qty for original position)
  - G5b re-places SL at correct qty on next cycle
  - WARNING Telegram: "PARTIAL CLOSE — {symbol}"

**P6 (GAP 2 LOW): BreakevenManager Retry + Alert**
- `_advance_sl()` rewritten with retry loop:
  - `modify_max_retries` (default 3), `modify_retry_backoff_sec` (default 2.0)
  - `_consecutive_failures` counter per trade (resets on success)
  - WARNING Telegram after all retries exhausted
  - Constructor: `notifier`, `modify_max_retries`, `modify_retry_backoff_sec` params added

**GAP 3 (Corporate Actions) SKIPPED** — Chartink handles price adjustments at source.
**A1 (OCO race) SKIPPED** — double-close guard already catches it.

**Tests:** 18 new in `test_fix148_broker_gaps.py`; 2718 total green.
**Also fixed:** 7 pre-existing broken tests (DateTimeEncoder, now_ist monkeypatch, gemini_log_review).

**Why:** Broker integration audit found 5 gaps + 3 additional. RMS squareoff was recording zero PnL; naked positions had 15s detection gap; SL failures had no market-close fallback.
**How to apply:** All changes are in reconciler/order_placer/breakeven_manager. No config changes needed — new BreakevenManager params are optional with defaults.
