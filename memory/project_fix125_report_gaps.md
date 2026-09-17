---
name: project-fix125-report-gaps
description: "FIX-125 daily_report 7 bug fixes — eligible score/cost/OHLC fallbacks + numeric zero-fill (2026-05-19, commit b6cd512)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 12782b2c-fa98-463b-b215-14cea83c7453
---

FIX-125 landed (commit b6cd512, pushed to VM).

**7 bugs fixed in daily_report.py:**
- BUG 1/3: eligible_score falls back to strategy YAML min_score when screener_results.eligible_score is NULL
- BUG 5: cost columns back-calculate via `_compute_cost_breakdown()` when DB breakdown NULL but charges exists; show 0 when charges=0; show dash only when charges NULL
- BUG 6: candle OHLC falls back to `data_store/candles/candle_data_YYYY-MM-DD.csv`; `fetch_daily_candles.py` now also INSERTs into candles DB table
- BUG 7: Sheet 6 time-of-day Rejected = `max(0, signals_rcvd - processed - traded)` (was empty)
- General: numeric columns show 0 (not dash/None); dash only for genuinely N/A fields

**Restored as private fallbacks (not deleted):**
- `_build_strategy_min_scores()` — reads strategy YAMLs for eligible_score fallback
- `_compute_cost_breakdown()` — computes Zerodha cost breakdown from broker_costs.yaml rates
- `_load_candle_csv()` — reads CSV candle files when candles DB table is empty

**ReportData extended:** `strategy_min_scores`, `broker_rates` fields added

54 tests green (was 47); 2107 total pass

**Why:** Historical data pre-FIX-123 has NULL eligible_score/cost_brokerage/candle rows; fallbacks ensure reports render correctly for all dates.

**How to apply:** If adding new DB columns to report, always provide a fallback for historical data where the column is NULL.
