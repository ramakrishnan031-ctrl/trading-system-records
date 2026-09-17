---
name: gui_g5c_analytics_04jul
description: "G5 Phase C · G5c — 5 NEW analytics screens (Strategy Ranking/Health, Scanner Attribution, Trade Explorer, P&L Analytics) + multi-period layer + 6 new endpoints; 333 tests green"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6777fbd-94de-43c3-8dc4-50e6e874dbad
---

# G5c — NEW Analytics Screens BUILT, 04-Jul-2026

Third CODE sub-phase ([[gui_g5b_reuse_screens_04jul]]). **5 NEW analytics screens** on a shared **multi-period layer**, all read-only + additive (new routes/endpoints/readers; existing endpoints UNTOUCHED). **333 tests green** (both v41+v42) = 306 baseline + 27 G5c. NO schema/trading/broker change; **0 core/trading files, 0 renames/deletes, 0 Reports lines; `/api/pnl` (today-scoped) untouched**. Git HELD (branch `gui-g5c-04jul` off G5b). Deployed VM `7b1c92d` untouched.

**Period layer (foundation, built first):** `freshness.resolve_period(period,from,to,now)` → (from,to) YYYY-MM-DD IST. **today**=(today,today) · **week**=trailing-7d incl today · **month**=trailing-30d incl today · **custom**=(from,to). **Trailing windows (not calendar)** — deterministic, IST-anchored; flagged for review. Period-scoped readers wrap existing today-logic WITHOUT mutating it: `db_reader.closed_trades_range` (spine) · `trades_in_range` · `signals_scanner_funnel_range` · `strategy_signal_counts_range` · `webhook_by_scanner_range` · `screener_scores` (System Score, L8) · `trade_story_parts`. All map to EXISTING tables, mode=ro, NO schema.

**Service `analytics_period.py`** (documented formulas): win_rate=100×wins/decided · **expectancy**=(win%×avgWin)−(loss%×|avgLoss|) · **profit_factor**=Σwin/Σ|loss| · roi=100×net/Σmargin · **opportunity_quality(scanner,0-100)**=100×accept_rate×trade_conversion×win_rate (each factor 0 when its denominator is 0 — no evidence, never fabricated) · **health_state** precedence: Disabled(enabled False)→Silent(silence RED)→Warning(badge RED)→Quiet(badge YELLOW|silence YELLOW)→Healthy(badge GREEN); health_score Healthy90/Quiet70/Warning40/Silent20/Disabled null.

**NEW endpoints** (blueprint `api/analytics2.py`, registered in app.py; all login_required, read-only): `/api/strategy-ranking` · `/api/strategy-health` · `/api/scanner-attribution` · `/api/trades` (Trade Explorer) · `/api/trade-story/<id>` · `/api/analytics/pnl` (distinct from today-scoped `/api/pnl`). All take `?period&from&to`.

**Screens** (routes in `app.py:_PAGES`; 5 Analytics nav placeholders → live links): `strategy_ranking.html` (period + mode toggle Net/ROI/Win%/PF/Trades re-sorts same dataset + medals) · `strategy_health.html` (5-state chips + health score + period signal-trend + merged Warnings/Alerts) · `scanner_attribution.html` (funnel + quality score + medals + "scanner-level (shared)" for unmapped) · `trade_explorer.html` (filter_bar + data_table + trade-story drill via lifecycle_timeline; Validation/Risk/Capital timings = honest "not captured (G-2)"; raw Chartink payload from signals.webhook_payload) · `pnl_analytics.html` (period totals + per strategy/scanner/direction + realized equity curve + **MTM two_state_panel "Pending Broker Source (G4)"**).

**Fixture (conftest):** +`screener_results` table + scores 72 for sig_trd_c1/c4; +3 multi-day gap_fade_long closed trades (trd_w1/w2 YDAY, trd_m1 TENDAYS) + their signals — ALL older than today's 14:50 win ⇒ loss-streak assertions (global + per-strategy) UNMOVED; created/exit dated ⇒ invisible to today-scoped counts. Verified: closed trades today=4/week=6/month=7.

**Exact-verified values:** ranking today gap_fade_long net 100/PF 2.0/ROI 1.0; week net 150 (4 trades). P&L week totals net 25/6 trades/expectancy 4.17. Scanner gap_fade_long received 58/accepted 50/trades 2/net 100/quality 1.7; momentum_combo "scanner-level (shared)". Trade story trd_c1 score 72/scanner gap_fade_long/Validation "not captured". Trade explorer today 8 rows (trd_c1 score 72, trd_o1 null).

**Additive-only HELD:** pinned 6/13/8/6/4 + HARD_KILL blink unmoved (`test_pinned_shapes_frozen_after_g5c`); ExportButton OFF; ScoreChip single-score (frontend grep clean); parity (no mode branch). tests `test_g5c_analytics.py`; updated `test_nav.py` `_SOON` → (Live Activity, System Health, Trade Logs) = remaining G5d placeholders. Next = Web Claude reviews formulas → G5d (two-state Positions/Holdings · Live Activity · Trade Logs · Controls read-only summary). Related: [[gui_g5_phaseB_04jul]], [[feedback_paper_live_parity]].
