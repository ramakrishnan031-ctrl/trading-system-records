---
name: gui-g5-phasea-04jul
description: "G5 ops_dashboard redesign — Phase A investigation+mapping report (22 specs vs live code); read-only, no code changes"
metadata: 
  node_type: memory
  type: project
  originSessionId: b6777fbd-94de-43c3-8dc4-50e6e874dbad
---

# G5 Ops Dashboard Redesign — Phase A (Investigation + Mapping) COMPLETE, 04-Jul-2026

**Report:** `ops_dashboard/docs/G5_REDESIGN_PHASE_A.md` (5 sections + exec summary, fully cited). READ-ONLY investigation — zero code/schema/route/config edits. Redesign-in-place (evolve existing ops_dashboard; Gemini→AGY preserve-first principle). Soak PAUSED for this.

**Specs:** 22 + Consolidation Plan, read in full from **PC** `D:\Projects\trading-system\gui\*.txt` (NOT the VM — no VM copy needed; temp `gui/` folder deletable on Rama's word once G5 lands). Target menu (5 groups): Dashboard · Trading(Strategies/Signals/Orders/Positions/Holdings) · Analytics(Strategy Ranking/Strategy Health/Scanner Attribution/Trade Explorer/P&L/Slippage/Execution) · Operations(Live Activity/System Health/Configuration/Controls) · Investigation(Audit/Trade Logs/System Logs). Recent Events + Alerts = MERGED into screens, not menus.

**Headline (22 target screens = 21 menu + Capital&Risk):** ~9 reuse-as-is (menu/UX only, additive) · ~4 new-frontend over existing data · ~9 new-backend/blocked. **NO new DB schema required** for any buildable screen — redesign is ~90% frontend + additive read-only SQL joins over the ~23 tables already read.

**5 highest-risk / decisions for Rama:**
1. **Controls (spec 16) = architecture wall.** Wants write-actions (strategy/scanner toggles, limit edits, pause). GUI is read-only by design (`test_isolation.py`) + NO control-plane exists (G3.0: kill-switch in-memory, config needs restart). → G3 design, NOT Phase B/C. Only display-only subset (Active-Controls-Summary, Readiness, Sim-mode visibility, Control-History) is read-only-safe. See [[gui_readiness_g3_0_03jul]].
2. **Live broker LTP/MTM/holdings unreachable read-only (G4).** Positions (MTM/current-RR/unrealized) + Holdings (broker-first delta) centrally depend on it → honest two-state shells only. `/api/positions` already renders `—` note "G4". Holdings' nearest future source `eod_broker_reconciliation` (P1/v42) is UNPUSHED/absent from live `core/schema.sql` (EOD-granularity even when shipped). See [[p1_eod_broker_reconcile_impl_02jul]].
3. **238-case contract gate pins exact shapes/counts** (6 units, 13 stages, 8 capacity rows, 6 groups, 4 rankings, strategies count). Subset-checks `<= set(d)` ⇒ ADD keys is safe; rename/remove/count-change breaks. Keep 13 pipeline stages (Dashboard spec's 12 is a visual subset).
4. **Multi-period (week/month) = broad new build** — every current query is today-scoped; needs date-range readers (no schema).
5. **Per-stage exec timings (validation/risk/capital) + Audit user/authorship + System-Health uptime/CPU-RAM NOT persisted** → honest partials. (Exchange-Accept IS available via `order_execution_log.exchange_timestamp`.)

**Preserve-vs-rename: NONE forced** (all endpoints preserved + extended additively; 6 new screens add new routes). Two PLACEMENT flags: **Capital & Risk (spec 07) missing from target menu tree** despite Phase-1 + Alerts-merge-target → needs a home (suggest Operations); **Reports** screen has no target home (replaced by per-screen XLSX export).

**Q3/XLSX:** ~20 screens want "Download XLSX (filtered)" → collides with `reports_download_enabled=FALSE` + copy-gate. Framed as ONE flag-gated shared export component + policy toggle. Rama decides.

**Key schema facts verified (core/schema.sql):** System Score = `screener_results.score` (join signal_id); scanner→trade P&L reachable via `signals.scanner`←`trades.signal_id` (mutual FK); `signals.webhook_payload` = raw Chartink JSON ✓; `orders.order_id` IS broker-assigned (Order ID == Broker Order ID, no separate col); NO distinct "Signal Score" column (spec assumption — flag). Broker RAW response NOT persisted (only `rejection_reason`).

**Biggest reuse:** `strategy_tower` service already emits 7 groups + 4 rankings + scanner_level → backbone for Strategies + Strategy Ranking + Strategy Health + Scanner-level. `log_reader.parse_structured` ref_id filter → powers Trade Logs. `freshness` = global market-clock/poll. Unwired `metrics_client.get_trader_metrics` (`:8080/metrics`) available for Live Activity/System Health.

**Git posture:** HELD — no branch/commit/push (no-push posture + in-flight working-tree changes). Docs written to tree, ready for `gui-g5-phaseA-04jul` when Rama chooses.

**Next:** Web Claude reviews report → issues Phase B (design). No coding until Rama approves the mapping. Related: [[gui_g2c_deploy_prep_03jul]], [[gui_g2b2_complete_03jul]], [[feedback_system_map_first]], [[feedback_paper_live_parity]].
