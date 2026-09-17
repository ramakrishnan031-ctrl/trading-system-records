---
name: h9_candle_offbyone_landmine_06jul
description: "Wave-3 H-9 DONE (06-Jul, commit beb8278 unpushed) — CandleStore _last_closed_window off-by-one fixed + dead exchange_timestamp late-tick discard DELETED (landmine) + synthetic-only guard added. Wave-3 COMPLETE."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-3 H-9 FIXED** (commit `beb8278`, main, UNPUSHED — Rama pushes off-market). One fix = one commit (`data/candle_store.py` + new `tests/unit/test_h9_candle_offbyone_landmine.py` + `tests/unit/test_candle_store.py` [removed the 2 dead discard tests]). Ref finding H-9 in `docs/audit/full_system_audit_04july2026.md`. **This is the LAST Wave-3 item → Wave-3 COMPLETE.**

**Two defects (on the candle data every strategy consumes):**
- (a) **Off-by-one:** `_close_candles` stamped `_last_closed_window = window_being_closed` = the window that STARTS now (timer fires at 10:01:00 → 10:01), not the one that just CLOSED (10:00).
- (b) **Dead late-tick discard + LANDMINE:** the FIX-049 `exchange_timestamp` discard in `on_tick` (:184-196) + `_Accumulator.update` never ran — the live dispatcher (`main.py:2157-2159`) passes `ts=t.get("timestamp") or now_ist()` into the unused `ts` slot and leaves `exchange_timestamp=None`. Combined with (a), had anyone wired `exchange_timestamp`, every current-minute tick would satisfy `tick_window(10:01) <= last_closed(10:01)` → discarded → store 100% synthetic (+ a latent naive/aware TypeError in `_Accumulator.update:63`).

**DECISION = DELETE (not wire).** Rationale: `exchange_timestamp` is only reliably populated in KiteTicker `full` mode (None in ltp/quote; `live_feed.py:289` = `raw.get("exchange_timestamp") or raw.get("timestamp")`); the discard is 100% dead so removal has ZERO runtime effect and closes the landmine by construction; wiring would risk dropping real ticks on money-path data with no proven production problem; receive-time (clock-driven `now_ist`) windowing has been correct since go-live.

**Fix:** (1) off-by-one unconditional → `_last_closed_window = window_being_closed - timedelta(seconds=interval)`; (2) removed the `exchange_timestamp` param + discard from `on_tick` + `_Accumulator.update` (real ticks can never be dropped as "late"); **`ts` kept** for the caller interface but documented INFORMATIONAL-ONLY (it never gated/windowed anything — `main.py` dispatcher UNCHANGED, lower money-path risk than removing it); (3) **synthetic-only guard** — WARN after 3 (then every 30) consecutive closes emitting only carry-forward candles (zero real ticks), so a starved feed is LOUD not silently synthetic. `_last_closed_window` now has no live tick-gate reader but is kept correct + used in the guard log.

**Consumer scan:** live candle consumer = `smart_tgt_manager.get_candles` (OHLC history); `reports/daily_report` reads a separate DB path. NOTHING reads `_last_closed_window` except the (deleted) discard → the off-by-one had no runtime consumer impact; fixed for correctness + landmine-defusal.

**Parity:** single `CandleStore` instance (`main.py:2131`), one tick-dispatch path, no paper-specific duplicate — mode-agnostic aggregation.

**Tests** (`test_h9_candle_offbyone_landmine.py`; REAL `CandleStore.on_tick`/`_close_candles`/`_Accumulator`/`get_candles`; `now_ist` patched to a fixed instant only for the boundary assertion; logger MagicMock): T1 off-by-one → last_closed=10:00 not 10:01 (**RED before fix**) · T2 real ticks → REAL non-synthetic candle + all ticks accepted (no discard) · T3 synthetic-only guard WARNs after 3 tick-less closes + resets on a real tick · T4 consumer reads correct OHLC. The 2 FIX-049 tests asserting the deleted discard were REMOVED (tested removed behavior); `test_fix049_no_exchange_timestamp_no_crash` retained. RED proven by reverting the off-by-one. **125 green** (H-9 + candle_store + smart_tgt_manager + secondary_screener; 0 regressions).

**Residual:** candle-window bookkeeping now correct; landmine closed by construction; a starved feed is now alerted. Follow-up (optional, NOT done): `ts` remains an unused-but-documented param — could be removed in a later cleanup (ripples to `main.py` + tests); left to minimize money-path blast radius.

Related: [[h8_shadow_tracker_strategy_column_06jul]] · [[h11_invalidate_token_path_06jul]] · [[h13_token_monitor_relatch_06jul]] · [[h12_paper_positions_signed_06jul]]. **Wave-3 COMPLETE: H-12✓ H-13✓ H-11✓ H-8✓ H-9✓.** Web Claude gives the Wave-3 closure assessment next.
