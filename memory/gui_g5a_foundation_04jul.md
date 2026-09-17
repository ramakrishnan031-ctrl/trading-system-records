---
name: gui_g5a_foundation_04jul
description: "G5 Phase C · G5a — shared component framework + 5-group nav + AlgoCore rebrand BUILT (frontend-only, additive; 279 tests green)"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6777fbd-94de-43c3-8dc4-50e6e874dbad
---

# G5a — Shared Foundation + Navigation + Component Framework, BUILT 04-Jul-2026

First CODE sub-phase of the G5 redesign ([[gui_g5_phaseB_04jul]] design). **Frontend-only + one additive backend context-processor; zero schema/trading/broker/endpoint/reader/service changes.** 279 tests pass (both v41+v42 fixtures) = 238 baseline + new G5a tests. Base HEAD `80be23a`; deployed VM app (`7b1c92d`) UNTOUCHED (G5a not deployed → soak resumes there). Git HELD (no branch/commit/push); formalize on `gui-g5a-04jul` when Rama chooses.

**What G5b+ can now assume (the deliverable):**
- **13 shared components exist, styled, tested render-only.** Markup = `frontend/templates/components.html` (Jinja macros); behaviour = `frontend/static/components.js` (`tableMixin`/`filterMixin`/`periodMixin`, loaded sync before Alpine in base.html); styles = `style.css` `/* == G5a component framework == */`; contracts doc = `ops_dashboard/docs/COMPONENTS.md`.
  - `data_table(id,columns,rows_expr)` + `tableMixin` (sort ▲▼ every col, rows-per-page 50/100/200/500, `tCell` fmt) · `filter_bar(filters,on_change)` + `filterMixin` (fVals/fReset/fQuery) · `kpi_row`/`kpi_card(label,value_expr,tone,href)` · `period_selector` + `periodMixin` (Today/Week/Month/Custom→pQuery) · `events_alerts_panel` (L10 merged) · `two_state_panel(available_expr,reason)` (L3/L9 honest, `{% call %}` slot) · `export_button` (L7 flag-gated OFF) · `score_chip` (L8 System Score only) · `medal` (🥇🥈🥉) · `status_chip` · `funnel_pipeline_card` (renders given stages 1:1) · `lifecycle_timeline`.
  - Consumption: `Object.assign(pageBase(url), tableMixin(), filterMixin(), {...})` then `{% from "components.html" import ... %}` (example in COMPONENTS.md).
- **Nav = 5 groups** in base.html: Dashboard(landing `/`) · Trading(Strategies/Signals/Orders/Positions/Holdings) · Analytics(5 `nv-soon` placeholders + Slippage/Execution links) · Operations(Live Activity/System Health/Capital&Risk = soon; Configuration/Controls links) · Investigation(Audit link, Trade Logs soon, System Logs link). **Not-yet-built screens = dimmed `nv-soon` placeholders (no href → no 404).** A G5b screen flips its placeholder to `{% block nav_X %}active{% endblock %}` + adds its `_PAGES` route. Non-menu screens (risk/capital/exposure/capacity/pnl/services/vm/statistics/reports/alerts) dropped off the sidebar but their routes/endpoints are UNTOUCHED + still 200 by direct URL.
- **`gui_flags` in every template context** (app.py context processor): `table_export_enabled`/`reports_download_enabled`, both DEFAULT False. ExportButton reads it → disabled until Rama's Q3 call.
- **AlgoCore rebrand = LABEL layer only** (base.html brand+title, login.html, dashboard.html title). Internal name unchanged: folder `ops_dashboard`, module `backend.*`, all routes/config keys. Git shows no R/D (nothing renamed/deleted).

**THE additive-only invariant HELD (proven by `test_pinned_contract_counts_unmoved` + existing contract tests):** equality-pinned counts unmoved — service_health==6, pipeline stages==13, capacity rows==8/groups==6, rankings=={4 keys}. New data goes in NEW fields only. 13-stage pipeline guarantee lives in the untouched `/api/pipeline`; `funnel_pipeline_card` renders whatever it's given.

**Tests added:** `tests/test_nav.py` (routes render in new shell, 5 groups, landing=Dashboard, soon-placeholders no-404, non-menu reachable, mobile media-query, rebrand label-only) · `tests/test_g5a_components.py` (each component renders + L7/L8/L9 rules + pinned counts + no "Signal Score" frontend-wide grep + components.js URL-free). Isolation I7 (AST + CDN gate) auto-covers new files. **Note:** JS sort/pagination BEHAVIOUR isn't unit-tested (stack has no JS runner) → verified in Rama's interactive browser pass (deviation, stated).

**Reconciliation flagged:** G5a instruction T5 named "Alerts" a mobile-priority nav item, but L10 (locked) merges Alerts into screens → I honored L10 (Alerts NOT a sidebar item; `/alerts` still 200 by direct URL; surfaces via EventsAlertsPanel in G5b). Reported for Web Claude.

**Discipline:** no half-converted screens — every screen keeps its CURRENT table until its own sub-phase (G5b/c/d) converts it to `data_table`. Next: Web Claude reviews component contracts + preservation proof → issues G5b (reuse screens). Related: [[gui_g5_phaseA_04jul]], [[gui_g2b3_ui_polish_03jul]], [[feedback_paper_live_parity]], [[feedback_system_map_first]].
