---
name: SmartTgtManager module built and locked (ST1-ST15)
description: Module 32 — orders/smart_tgt_manager.py; trail SL on CO trades; 46 tests green; 1002 total
type: project
originSessionId: fc58fdb1-62db-42d0-abf8-209c7761d163
---
Files created (NEW module):
- orders/smart_tgt_manager.py
- tests/unit/test_smart_tgt_manager.py (46 tests)

Files modified:
- core/schema.sql (TABLE 15: smart_tgt_state; v7->v8)
- core/state_store.py (EXPECTED_SCHEMA_VERSION=8; 5 new helpers)
- data/candle_store.py (added unregister_on_candle_close)
- tests/unit/test_state_store.py (50 tests; was 42)

Locked decisions: ST1-ST15

Key design points:
- Modifies CO trigger_price in place via adapter.modify_order (NOT cancel-replace, P8_P13)
- Ghost SL fix (ST5): internal state + DB updated ONLY after broker confirms modify
- Trail algorithm (ST4): best_price = max(candle.high) for LONG, min(candle.low) for SHORT
  steps = int((distance_pct - trigger_pct) / step_pct)
  new_sl = entry * (1 + trigger_pct + steps * step_pct) for LONG
  SL never lowered (LONG) / raised (SHORT)
- Driven by candle_store callback; no own poll thread (ST11)
- Reconnect protocol (ST7/G6/LF7): on_reconnect() resets best_price, recomputes from history ONCE
- Reconnect chain: main.py calls candle_store.mark_reconnect THEN smart_tgt.on_reconnect (ST13)
- Startup recovery (ST8): start() reads smart_tgt_state table, optional LTP check via quote_fn
- Thread safety: single RLock; broker call outside lock (ST9)
- 3 consecutive failures: CRITICAL + on_critical_failure callback (ST10)
- CO broker_order_id looked up via state_store.get_co_entry_order_for_trade() (ST14)
  Query: SELECT * FROM orders WHERE trade_id=? AND leg='ENTRY' AND variety='co' LIMIT 1

state_store new helpers (ST14+ST15):
- get_co_entry_order_for_trade(trade_id) -> sqlite3.Row | None
- insert_smart_tgt_state(trade_id, symbol, instrument_token, direction, entry_price,
    initial_sl, current_sl, qty, trigger_pct, step_pct, registered_at, ...)
- update_smart_tgt_state(trade_id, current_sl, trail_count, last_trail_ts, best_price)
- delete_smart_tgt_state(trade_id)
- get_all_smart_tgt_states() -> List[sqlite3.Row]

schema v8: smart_tgt_state table (TABLE 15) with 14 columns incl. best_price (nullable)

Deviations: None.

**Why:** Trail SL on profitable CO trades without cancel-replace race conditions.
**How to apply:** Main.py calls mgr.register_trade() after CO entry fills. Wires
candle_store.set_on_reconnect_callback() to call candle_store.mark_reconnect then
smart_tgt.on_reconnect (ST13). Unregister on position close (COMPLETE/CANCELLED).
