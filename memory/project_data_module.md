---
name: Data module built and locked (LF1-LF18)
description: data/live_feed.py (LiveFeedManager) + data/candle_store.py (CandleStore); 26+25=51 new tests; 768 total
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
Module 26 build complete. All 768 cumulative tests green (764 unit + 4 integration).

**Why:** G6 requires live tick feed + candle building for smart_tgt_manager, screening/entry_gate, secondary_screener. Audit 3.4 requires LTP-only candle OHLC + clock-based close. Audit 3.3 requires single consumer thread (no thread-per-callback).

**How to apply:** LiveFeedManager wires to KiteTicker; CandleStore receives ticks via on_tick(). Wire them: `feed.register_callback(lambda batch: [store.on_tick(t["instrument_token"], t["last_price"], t["timestamp"]) for t in batch])`. Set reconnect callback: `feed.set_on_reconnect_callback(store.mark_reconnect)`.

## Files changed

- `data/__init__.py` (NEW): empty package marker
- `data/live_feed.py` (NEW): LiveFeedManager; LF1-LF8
- `data/candle_store.py` (NEW): CandleStore + CandleData; LF9-LF18
- `tests/unit/test_live_feed.py` (NEW): 26 tests
- `tests/unit/test_candle_store.py` (NEW): 25 tests
- `docs/locked_decisions.yaml`: added LF1-LF18 under data_module:; total_decisions 113->131

## Test counts (post-Module 26)

| Suite | Count |
|---|---|
| test_live_feed.py | 26 (NEW) |
| test_candle_store.py | 25 (NEW) |
| Total unit | 764 across 29 suites |
| Integration | 4 (unchanged) |
| **Cumulative total** | **768** |

## Key design decisions

- LF5: bounded queue capacity 10000; drop oldest on full; single consumer daemon thread
- LF6: tick normalized to {instrument_token, last_price, timestamp, volume}; raw ohlc excluded
- LF7: on_reconnect fires candle_store notification ONCE per disconnect (_reconnect_notified flag); gap > 10min -> on_critical_failure
- LF11: OHLC from LTP only, volume=0 always (Audit 3.4 fix)
- LF12: clock-aligned timer (time.time() // interval_sec arithmetic); no tick-arrival dependency
- LF13: CandleData is frozen dataclass; ts is IST tz-aware datetime
- LF16: mark_reconnect discards _accum, preserves _history
- LF17: two-section lock in _close_candles; callbacks fired outside lock

## Naming note

G6 locked_decisions.yaml `affects` field lists `data/live_feed_manager.py` (old name). Actual file is `data/live_feed.py` per v2_design_spec.md. No architectural conflict.

## Deviations from spec

- LF5 test count: 26 tests (spec said ~25); added test_reconnect_notifies_candle_store_only_once_per_gap as it tests the _reconnect_notified flag (LF7).
- No other deviations.
