---
name: slippage_intelligence_phase1
description: "Slippage intelligence Phase 1 — raw data layer (schema v31, 20-Jun, commit 71d4186). 3 append-only tables (order_execution_log, trade_slippage_log w/ rr_damage_pct, market_execution_context); orders/slippage_recorder.py async subscribers (never block execution); analytics on-demand in Phase 2 reports. Activates next restart."
metadata: 
  node_type: memory
  type: project
  originSessionId: e7a6af13-236a-41d8-aca5-213b591647fd
---

**SLIPPAGE INTELLIGENCE PHASE 1 — RAW DATA LAYER (schema v31, 20-Jun-2026, commit 71d4186).** Permanent
execution-intelligence store. **RAW facts only** — band/strategy stats + tolerance recommendations are
computed ON-DEMAND in Phase-2 reports (NO aggregate tables → no stale derived data). Recording **NEVER
blocks/affects trade execution**.

## Schema v31 (MAIN DB; 3 append-only tables, pure additions)
- `order_execution_log` — one row per filled order/leg (ENTRY/SL/TGT).
- `trade_slippage_log` — one row per completed trade; **`rr_damage_pct`** = `(entry_adverse + sl_adverse
  − tgt_favourable) / planned_sl_distance × 100` = % of the risk budget execution ate (THE key metric).
  Sign convention: **adverse = positive** (entry/SL), favourable = positive (TGT, reduces damage).
- `market_execution_context` — Priority-2, ALL nullable bid/ask/spread (best-effort; missing → NULL).
`EXPECTED_SCHEMA_VERSION` 30→31 (state_store.py). New tables need NO migrations.py rebuild — `CREATE TABLE
IF NOT EXISTS` + the executescript path creates them + the trailing INSERT bumps the version. 3
best-effort never-raise insert helpers in state_store (`insert_order_execution_log` /
`insert_trade_slippage_log` / `insert_market_execution_context`; whitelisted columns, return bool).

## Recorder (orders/slippage_recorder.py)
`SlippageRecorder` subscribes **ASYNC** to `OrderFilled` (→ order_execution_log + context) and
`PositionClosed` (→ trade_slippage_log roll-up from the trades table). **Why async is safe:** EventBus
async dispatch runs the handler on a dedicated thread and **logs but NEVER re-raises** handler exceptions
→ the publisher (order path) is fully insulated. Handlers ALSO try/except internally; every insert is
best-effort. Pure tested helpers: `adverse_entry_slip`/`adverse_sl_slip`/`favorable_tgt_slip`,
`calc_rr_damage_pct` (Rama's example: 1+1−0 / 10 = 20%), `get_price_band` ("LO-HI" HI-exclusive, "Nnn+"
open top), `build_trade_slippage_row`. Optional `adapter` for best-effort bid/ask (Priority-2). Wired in
main.py (construction wrapped → can't break startup). `slippage_bands` config (default 0-100..1000+).

## Status
Parity (records paper + live; events fire in both). **Migration v30→v31 verified live on a copy of the
real DB** (3 tables created, 63 trades intact — production untouched). +19 tests; 156 migration/
state_store/config tests pass. Activates next restart (migration at StateStore init, Mon 08:30). Editing
system_config.yaml → 1× security-watcher WARNING (expected). Queries + roadmap in
`docs/slippage_intelligence.md`. **Phase 2 (on-demand reports) + Phase 3 (adaptive tolerance engine:
Global→Band→Strategy→Symbol, feeding entry_gate.slippage_control) PENDING.**
Related: [[tiered_slippage_abort]], [[slippage_calibration_data_20jun]], [[db_schema_v28_split]].
