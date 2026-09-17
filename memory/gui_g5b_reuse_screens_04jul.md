---
name: gui_g5b_reuse_screens_04jul
description: "G5 Phase C · G5b — 7 reuse screens converted to G5a components + additive backend fields (scanner attribution, long/short exposure, SL/TGT hits, profit factor, slippage rankings); 306 tests green"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6777fbd-94de-43c3-8dc4-50e6e874dbad
---

# G5b — Reuse Screens BUILT, 04-Jul-2026

Second CODE sub-phase ([[gui_g5a_foundation_04jul]] components). **7 screens** consuming G5a components + **additive-only backend** (new response KEYS, existing keys/lengths frozen). **306 tests green** (both v41+v42) = 279 baseline + 27 G5b. NO schema/trading/broker change; **api/ touched = only `analytics.py`(slippage +keys) + `risk_capital.py`(exposure +by_direction)** — 0 endpoint removed/renamed, 0 schema, 0 renames/deletes; Reports UNTOUCHED. Git HELD (branch `gui-g5b-04jul` off G5a when Rama commits). Deployed VM app `7b1c92d` untouched → soak resumes there.

**Screens (all render 200, ExportButton OFF, mode = displayed attribute only):**
- **Configuration** (`config.html`) — pure frontend; kpi_row + search + export; honest "Change author not captured (G-5)"; /api/config UNCHANGED.
- **System Logs** (`logs.html`) — client-side severity KPI counts; export; honest "resolution status not tracked (G-5)"; /api/logs UNCHANGED.
- **Audit** (`audit.html`) — reflow to `data_table`+`filter_bar`; honest "user/who-changed not captured (G-5)"; /api/audit UNCHANGED.
- **Slippage** (`slippage.html`) — kept breach table; NEW per_scanner/per_symbol/price_buckets/trend panels; period_selector (emit-only, honest "Week/Month arrive G5c"); export.
- **Strategies** (`strategies.html`) — NEW dense `data_table` view (toggle Table/Cards) + family label + SL/TGT-hits + profit_factor in cards; export.
- **Capital & Risk** (`capital_risk.html`, NEW route `/capital-risk` in `app.py:_PAGES`, nav link replaces the G5a placeholder) — L5 consolidation composing PRESERVED /api/risk+capital+exposure+capacity into 4 zones; long/short/net exposure; MTM = `two_state_panel` "Pending Broker Source (G4)"; Recent Risk Events via `events_alerts_panel` (L10); realized-only capital-through-day (honest granularity). **Old /risk /capital /exposure /capacity still 200 by direct URL** (dropped from sidebar only).
- **Dashboard** (`dashboard.html`) — NEW "Today's Trading Summary" kpi_row (clickable deep-links) + Profit Factor + merged Alerts banner (L10); pinned summary-bar + 13-stage pipeline + chip-blink==1 UNMOVED.

**Additive backend (all read-only mode=ro, map to EXISTING tables, NO schema — verified exact on seed):**
- `db_reader.scanner_for_trades(trade_ids)` — shared scanner→trade join `trades.signal_id→signals.scanner` (SHARED with G5c Scanner Attribution). **Fixture note:** conftest now seeds 2 YESTERDAY-dated linking signals (sig_trd_c1/c4) so the join resolves; yesterday-dated ⇒ invisible to all today-scoped signal counts (unmoved).
- `db_reader.strategy_sltgt_hits` (gap_fade_long → {sl:1,tgt:1}) · `exposure_by_direction` (long 40000/short 0/net 40000) · `profit_factor_today` (0.89 = 200/225) · `slippage_trend_today` ([{hour:"10",avg:1.75,n:2}]).
- `/api/slippage` += per_scanner/per_symbol/price_buckets/trend · `/api/exposure` += by_direction · `/api/dashboard` summary.counters += profit_factor · `strategy_tower` per-row += `family`("gap_fade"), `sl_tgt_hits`, `performance.profit_factor`(2.0) — funnel/failures equality-dicts + rankings(4 keys) UNMOVED.

**Honest G-gaps rendered (never fabricated):** G-1 Capital&Risk MTM "Pending Broker Source (G4)" · G-5 Config author / Audit user / (Logs resolution) "not captured/not tracked". Each asserted by a render string test.

**Tests:** `tests/test_g5b_reuse.py` (exact-value readers + additive-endpoint + render + consolidation + honest-gap + export-OFF + no-"Signal Score"). Fixture enrichment in conftest.py (2 yesterday signals).

**Discipline held:** no half-converted screens; every existing key byte-unchanged; additive-only (new data → new keys). Next = Web Claude reviews → G5c (NEW analytics screens: Strategy Ranking/Health, Scanner Attribution, Trade Explorer, P&L Analytics — the scanner→trade join + date-range readers land there). Related: [[gui_g5_phaseB_04jul]], [[feedback_paper_live_parity]].
