---
name: project-schema-v14
description: "Schema v14 migration — 12 new columns + 2 new tables (candles, trade_excursions); commit dfdeec2"
metadata: 
  node_type: memory
  type: project
  originSessionId: a628a08a-10ee-4779-a049-1cc44f23b748
---

Schema v13→v14 landed 2026-05-19 (commit dfdeec2, FIX-123).

## New columns
- **trades**: cost_brokerage, cost_stt, cost_exchange_txn, cost_sebi, cost_gst, cost_stamp_duty, mode (PAPER|LIVE), sl_trail_count
- **orders**: rejection_reason, filled_at
- **signals**: webhook_payload (raw Chartink JSON)
- **screener_results**: eligible_score (per-strategy min_score threshold)

## New tables
- **candles** (table 18): minute OHLC persisted from CandleStore callback; UNIQUE(instrument_token, ts, interval_sec)
- **trade_excursions** (table 19): MFE/MAE computed from candles on trade close; entry candle OHLC

## Code wiring
- `CostCalculator.round_trip_breakdown()` returns CostBreakdown; `close_trade()` stores 6 components
- `OrderPlacer` passes `self._mode` to `create_trade()` → trades.mode
- `OrderMonitor._WatchEntry.status_message` captures Kite rejection text → `OrderStatusChanged.rejection_reason` → orders.rejection_reason
- `_on_order_status_changed` sets `filled_at = now_ist()` on COMPLETE transition
- `webhook_receiver._process_signal` stores raw body in signals.webhook_payload
- `secondary_screener._persist` stores `effective_min` in screener_results.eligible_score (3 post-threshold call sites)
- `_handle_exit_fill` copies smart_tgt_state.trail_count → trades.sl_trail_count before unregister
- `main.py` registers `_persist_candle` callback on candle_store
- `_handle_exit_fill` calls `compute_trade_excursions()` → `insert_trade_excursion()` after close

## VM
- DDL executed directly on live DB; backup created pre-migration
- 187 existing trades backfilled with mode='PAPER'
- 19 tables total (was 17)

**Why:** DB was missing cost breakdown (re-derived in report from rates — fragile), broker rejection text, per-trade mode, and had no candle persistence.
**How to apply:** Schema v14 is the baseline. Any new columns go to v15.
