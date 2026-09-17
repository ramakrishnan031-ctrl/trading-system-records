---
name: fix_180_complete
description: "FIX-180 — AGY-audit bug fixes (10 items) + alert-spam + weekend-cron guard, done 16-Jun-2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: c451e7dc-8922-4a48-8e2b-40197f2c20a4
---

FIX-180 (16-Jun-2026): fixed the remaining AGY-audit bugs after [[live_day1_zombie_remediation]]. Each bug was independently verified in the current code before fixing (AGY had false claims — e.g. it said the zombies filled and wanted CLOSED_MANUAL with fabricated P&L; evidence disproved that). Bugs A–E were already fixed by FIX-179 (verified present, not re-done).

Code fixes:
- **Bug 7** `orders/sl_breach_monitor.py`: emergency `place_order` used invalid kwargs (`transaction_type=`/`product=`), omitted required `price`/`intent`, and treated the returned `PlacedOrder` as a raw id. Now uses `side/price/intent` + `PRODUCT_TO_INTENT` (fetches position `product` via ENTRY/CO subquery) and reads `.broker_order_id`.
- **Bug 6** `orders/order_placer.py`: slippage guard + price-drift top-up called `self._live_feed.quote()` — LiveFeedManager has no `quote()` (the Jun-15 `'LiveFeedManager' object has no attribute 'quote'` errors). Added `_fetch_ltp()` routing through `adapter.get_quote_raw()` (FIX-166 F08 pattern). Drift block now gated on `self._adapter`. Production passes `broker_adapter` (main.py); tests now wire it too.
- **Bug 3** `orders/order_reconciler._reconcile`: re-query `get_all_open_trades()` after checks 1-5 (which can CLOSE trades in-DB this cycle) and before check9/G5b SL-placement, so recovery SL isn't placed on a just-closed position.
- **Bug 4** `core/state_store.py` + reconciler `_check1_manual_close`: capital/ledger was already correct (release_used with real exit price); the trade ROW lacked exit_price/net_pnl/exit_time. New `record_manual_close_financials()` (guarded to CLOSED_MANUAL rows, costs=0.0 so gross==net) called after release_used → trades.net_pnl now matches fm_ledger.pnl_delta.
- **Bug 8** `scripts/check_vm_state.py`: hardcoded `~/trading-system/...` → `PROJECT_ROOT/data_store` with `DB_PATH` env override.
- **Bug 9** CWD paths: `Path("data_store")` → `_ROOT / "data_store"` in 7 scripts (db_retention, compute_strategy_metrics, eod_cleanup, reconcile_pnl, reconcile_positions, **eod_verify, fetch_fno_ban** — last two found beyond the task list).
- **Bug 10** `scripts/reconcile_pnl.py` + `reconcile_positions.py`: `notifier=None` → `TelegramNotifier.from_env(log)` (WARNING if env missing, no crash).

Feature hardening:
- **Part 11** `capital/kill_switch._exit_all_trades_indestructible`: retry loop now (a) `_is_position_flat(symbol)` broker pre-check → skip-and-resolve if already flat (don't re-fire a MARKET exit that would open a naked position — the SULA spam root cause; note Bug C infinite-loop was already FIX-179), (b) max retry duration `_HARD_KILL_MAX_RETRY_HOURS=2.0` then escalate + return remaining as failed (no infinite thread freeze), (c) `_alert_exit_failed` CRITICAL Telegram with 300s per-trade dedup. Parity: self._adapter is paper/live adapter — same path.
- **Part 12** weekend cron: added `is_market_day()` / `is_broker_api_available()` to **core/market_windows.py** (NOT market_hours.py — doesn't exist). Correct Friday boundary `dt.time() >= time(17,30)` (the AGY-supplied `hour>=17 and minute>=30` was wrong for 18:00-18:29). Guard added to premarket_healthcheck + fetch_daily_candles (default-today run only) + reconcile_positions/reconcile_pnl (live + current-day only, preserves paper + `--date` backfill). gemini_premarket_brief & capture_metrics_baseline have 0 broker refs → no guard. Deliberately NOT holiday-aware (scheduling concern; cron uses 1-5 + MarketWindows.is_trading_holiday).

Cleanup: Part 9 (tests/unit/unit) didn't exist locally. Part 10 deleted empty `/home/ubuntu/trading-system/` (stale tests dirs, 0 files, 0 handles) — distinct from bare repo `~/trading-system.git`.

Tests: new `tests/unit/test_fix180.py` (17 tests: Part 12 boundaries, Bug 4, Part 11 flat-check + dedup, Bug 3 re-query). Updated test_order_placer slippage harness (adapter get_quote_raw) + test_fix134_sl_breach (corrected signature). See [[feedback_paper_live_parity]].

DEPLOY STATUS: committed locally; **push/deploy HELD** — done during live market hours, FIX-180 touches live-critical paths (kill_switch/order_placer/reconciler). Deploy after 15:30 close or on explicit go-ahead. Push to `trading-vm:~/trading-system.git` auto-deploys via post-receive `checkout -f`.
