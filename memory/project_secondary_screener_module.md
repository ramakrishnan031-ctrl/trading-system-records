---
name: Secondary screener module built and locked (SS1-SS15)
description: screening/secondary_screener.py built and tested; schema v7 with screener_results table; SS1-SS15 locked
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
screening/secondary_screener.py built and locked. 23 new tests green. Total: 885 (859 prior + 3 state_store + 23 screener = +26).

**Why:** secondary_screener orchestrates the full 10-step screening pipeline (step_executor + quality_scorer), applies per-strategy min_score override, and persists results per P18. Unblocks signal_processor wiring (Module 30).

**How to apply:** 
```python
screener = SecondaryScreener(step_executor, quality_scorer, state_store, quote_fn, logger)
result = screener.screen(signal_id, symbol, ..., strategy, market_data)
```
Import from `screening`: `from screening import SecondaryScreener, ScreeningResult`.

## Files created/modified
- `screening/secondary_screener.py` — SecondaryScreener + ScreeningResult frozen dataclass
- `screening/__init__.py` — updated to export SecondaryScreener, ScreeningResult
- `core/schema.sql` — v7: TABLE 14 screener_results + 3 indexes
- `core/state_store.py` — EXPECTED_SCHEMA_VERSION 6→7 + insert_screener_result() method
- `tests/unit/test_secondary_screener.py` — 23 tests
- `tests/unit/test_state_store.py` — updated: 14 tables, schema v7, 3 new screener_results tests

## Key design decisions (SS1-SS15)
- SS4: Pipeline: fetch quote → thresholds → run_all → error check → score → min_score → age check → PASSED
- SS4 step 4: error_steps -> REJECTED_STEP_ERROR (P9a fix a: exception = rejection)
- SS4 step 6: effective_min = strategy.min_score if > 0 else global min_pass_score
- SS4 step 7: REJECTED_SIGNAL_AGE is defense-in-depth (step_10=0.0)
- SS5: update_signal_status + insert_screener_result after every screen(); DB failure = log ERROR, still return
- SS7: Quote provides ltp/bid/ask/volume; vwap/atr/rsi etc = None (v2.1 adds data providers)
- SS10: SKIPPED vs REJECTED: SKIPPED = screener couldn't run (not signal's fault)
- SS14: signal_processor wiring deferred to Module 30

## Schema v7
- TABLE 14: screener_results (id, signal_id, score, tier, status, step_results TEXT, latencies TEXT, market_data_snapshot TEXT, ts TEXT)
- Indexes: signal_id, ts, status
- state_store.insert_screener_result() method added

## Test design note
- triggered_at must be derived from patched now_ist (not real now_ist) in tests that need signal_age=1.0
- Pattern: `prime = _prime_time_patch(); triggered_at = prime - timedelta(seconds=N)`
- This prevents false REJECTED_SIGNAL_AGE when tests run before 09:45 IST

## locked_decisions.yaml
- total_decisions: 166 → 181
- screening_module: section extended with SS1-SS15 + SS_SCHEMA
