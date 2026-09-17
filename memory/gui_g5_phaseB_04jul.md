---
name: gui-g5-phaseb-04jul
description: "G5 ops_dashboard redesign — Phase B design doc (22 screens, components, API/reader matrices, G5a-e rollout); design-only, no code"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6777fbd-94de-43c3-8dc4-50e6e874dbad
---

# G5 Ops Dashboard Redesign — Phase B (DESIGN) COMPLETE, 04-Jul-2026

**Doc:** `ops_dashboard/docs/G5_REDESIGN_PHASE_B.md` (sections A–K). DESIGN ONLY — zero code/schema/route/config edits. Builds on Phase A ([[gui_g5_phaseA_04jul]], ACCEPTED). Bound by Rama's **10 LOCKED DECISIONS** L1-L10 (redesign-in-place · preserve-first labels-may-rebrand · Broker→System→Delta honest-unavailable · Controls read-only-summary-only+G3-placeholder · Capital&Risk=one screen under Operations · Reports endpoint untouched · XLSX shared+flag-OFF · single System Score=screener_results.score drop "Signal Score" · Positions/Holdings two-state · Events+Alerts merged).

**THE load-bearing design invariant:** contract tests use **equality** checks (`rankings`==4 keys, `service_health`==6, `stages`==13, capacity `rows`==8/`groups`==6) → **all new data lands in NEW response fields, never mutating existing keys/lengths** (new ranking modes → `rankings_extra`, NOT `rankings`). This keeps all 238 cases green while every screen gains data. Additive-only everywhere.

**Menu (final, L5):** Dashboard · Trading(Strategies/Signals/Orders/Positions/Holdings) · Analytics(Strategy Ranking/Strategy Health/Scanner Attribution/Trade Explorer/P&L/Slippage/Execution) · **Operations(Live Activity/System Health/Capital&Risk/Configuration/Controls)** · Investigation(Audit/Trade Logs/System Logs). 21 menu + Login = 22 screens designed.

**Headlines:**
- **Components:** 13 shared — **9 NEW** (DataTable, FilterBar, KpiRow, PeriodSelector, EventsAlertsPanel, TwoStatePanel, ExportButton, ScoreChip, LifecycleTimeline, LeaderboardMedals — that's 10; NavShell/FunnelPipeline/StatusChip extended) / 4 existing-extended. Build-once → ~17 screens = low-risk bulk.
- **API matrix:** 5 PRESERVE-as-is · 12 EXTEND-additive · 6-7 NEW endpoints (`/api/scanner-attribution`, `/api/trades`, `/api/trade-story/<id>`, `/api/analytics/pnl`, `/api/activity`, `/api/strategy-{ranking,health}`). Zero existing field renamed/removed.
- **Readers/services:** all read-only mode=ro, **NO new schema**. NEW: `scanner_attribution` (scanner→trade P&L join), `trade_story` (per-trade assembly, feeds Trade Explorer+Trade Logs+all lifecycle timelines), `pnl_analytics` (multi-period), `activity_feed` (merged Live feed), `broker_reconcile_reader` (graceful — lights up if P1 ships).

**Rollout G5a-e (Phase C sub-phases, each own branch off deployed tag `7b1c92d`, soak resumable):** G5a shared foundation+nav+rebrand+global-table+ExportButton-flag-OFF (L) · G5b 7 reuse screens+additive backend (M) · G5c 5 NEW analytics screens+new services (L) · G5d two-state Positions/Holdings+Live/Logs+Controls-A (M) · G5e deploy+resume soak (S). Section K = ordered itemized backlog (29 units) Phase-C instruction files draw from.

**Honest-unavailable (L3/L9) designed as explicit states, NEVER faked:** G-1 Positions live MTM/LTP/current-RR · G-2 Holdings broker side (`eod_broker_reconciliation` P1 unpushed) · G-3 Execution per-stage validation/risk/capital timings · G-4 Orders broker raw response · G-5 Audit user/authorship + auth events · G-6 System Health CPU/RAM (psutil sentinel). Each = TwoStatePanel "Pending Broker Source (G4/P1)" / "Not instrumented" / "Not captured".

**Rama-decision gates (do NOT auto-build):** Q3/XLSX = ship `table_export_enabled` DEFAULT OFF (enabling = Rama's call). **Schema-pause PROPOSALS P-1..P-4** stay PROPOSALS, need explicit trigger: P-1 per-stage timings · P-2 change-author/control/auth audit rows · P-3 ship P1 broker-reconcile · P-4 GUI-readable unrealized-MTM table. Honest UNAVAILABLE until triggered.

**Parity:** `mode` displayed attribute everywhere, no mode branch introduced (per screen where rendered). **Controls (L4):** (A) read-only summary designed now (composes config/risk/preflight/audit — all readable); (B) G3 future controls = labeled disabled placeholder, NO write path, NO isolation exception. See [[gui_readiness_g3_0_03jul]].

**Git posture:** HELD — no branch/commit/push (no-push posture + in-flight tree changes). Ready for `gui-g5-phaseB-04jul`. Next: Web Claude reviews → issues Phase C sub-phase instruction files ONE at a time (G5a first). No coding until Rama approves Phase B. Related: [[gui_g2c_deploy_prep_03jul]], [[feedback_paper_live_parity]], [[feedback_system_map_first]].
