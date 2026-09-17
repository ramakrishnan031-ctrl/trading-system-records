---
name: project-fix124-db-only-report
description: "FIX-124: daily_report.py refactored to DB-only pipeline (commit 4ac1238, 2026-05-19)"
metadata: 
  node_type: memory
  type: project
  originSessionId: a628a08a-10ee-4779-a049-1cc44f23b748
---

FIX-124 complete — daily_report.py is now a DB-only pipeline (2026-05-19, commit 4ac1238).

## What changed

**Deleted functions:**
- `_compute_cost_breakdown()` — was computing costs at report-time from broker_costs.yaml rates
- `_build_strategy_min_scores()` — was reading all strategy YAML files for min_score per strategy
- `_load_candle_data()` — was reading candle_data_YYYY-MM-DD.csv files

**Removed CLI flag:** `--candle-dir` no longer exists

**ReportData dataclass:** removed `config: dict` and `strategy_min_scores: Dict[str, int]`; added `candle_map: Dict[Tuple[str, str], dict]` and `excursion_map: Dict[str, dict]`

**Data sources → now DB columns (schema v14):**
- Sheet 2 cost breakdown → `trades.cost_brokerage/cost_stt/cost_exchange_txn/cost_stamp_duty/cost_gst`
- Sheet 2 trail count → `trades.sl_trail_count` (was counting SL orders at report-time)
- Sheet 1+2 eligible_score → `screener_results.eligible_score` (was YAML-derived per-strategy min_score)
- Sheet 4 entry candle OHLC → `candles` table via `candle_map`
- Sheet 4 MFE/MAE → `trade_excursions` table via `excursion_map` (was innings-based approximation)

**New state_store helpers:**
- `get_candles_for_date(date_iso)` — all candle rows for a date
- `get_trade_excursions_for_date(date_iso)` — excursions joined to trades on date

**Remaining non-DB reads (intentional):**
- `nse_holidays_YYYY.yaml` — needed for holiday check, not trade data
- `system_config.yaml` — only for `excluded_symbols` list, not stored in DB

## Test results
- 48 tests in test_daily_report.py: all green
- VM full suite: 2090 passed, 66 pre-existing failures (test_main/test_startup_checks AttributeError)

**Why:** Previously costs were re-derived from rates at report-time — fragile if rates changed mid-period. Schema v14 stores all cost components at trade close time. Report now shows exactly what was computed at the time.
**How to apply:** When adding new report columns, always source from DB. If data isn't in DB, show "—" rather than computing at report-time.
