---
name: gui_g5d_operations_04jul
description: "G5 Phase C · G5d — Controls(read-only)/Trade-Logs/Live-Activity + two-state Positions/Holdings + final 5-group nav; 354 tests green. G5 build COMPLETE, only G5e deploy remains."
metadata: 
  node_type: memory
  type: project
  originSessionId: b6777fbd-94de-43c3-8dc4-50e6e874dbad
---

# G5d — Operations/Investigation + Final Nav BUILT, 04-Jul-2026

Fourth (final build) CODE sub-phase ([[gui_g5c_analytics_04jul]]). **5 screens + final nav consolidation**; all read-only + additive. **354 tests green** (v41+v42) = 333 baseline + 21 G5d. NO schema/trading/broker change; **0 core/trading/schema files, 0 renames/deletes, 0 Reports lines** (git-proven). Git HELD (branch `gui-g5d-04jul` off G5c). Deployed VM `7b1c92d` untouched. **The whole G5 redesign build is now COMPLETE — only G5e (VM deploy + resume soak) remains.**

**Two-state contract (the core of G5d — permanent architecture, L3/L9):** broker-derived data stays honestly UNAVAILABLE until G4/P1, NEVER faked/inferred:
- **Positions** (`positions.html`, route preserved): SYSTEM side full (date/time/strategy/**scanner**/symbol/dir/qty/entry/SL/TGT/risk/margin/age/inning) + `two_state_panel` "Live LTP/MTM/Unrealized/Current RR — Pending Broker Source (G4)"; MTM cell renders "—" (`/api/positions` additive: `unavailable`{fields,reason} + per-row `scanner`; existing keys frozen, unrealized still "—").
- **Holdings** (`holdings.html`, route preserved, broker-first L3): SYSTEM side = enriched `gtt_state` mirror (date/time/strategy/symbol/product/qty/avg — `holdings_list` +LEFT JOIN trades, additive) + `two_state_panel` "Broker Qty/Delta/Reconciliation Status — Pending Broker Source (G4/P1)"; broker/delta/recon cells render "—" (P1 `eod_broker_reconciliation` unpushed → activates when P1 ships; no fabricated qty/delta).

**Controls = READ-ONLY summary (L4 — ZERO write path, grep-proven no form/button/POST):** `controls.html` composes NEW `/api/controls-summary` (`services/operations.build_controls_summary` from config + kill-switch + strategy flags). 8 fields: Trade Type (Intraday Only), Strategies Enabled (4/5), Telegram (honest None — config-only, bot not probed after 03-Jul shadow fix), Max Trades/Positions/Concentration/Daily-Loss, Kill-Switch state. "G3 Future Controls" = disabled placeholder, no buttons.

**Trade Logs** (NEW `/trade-logs`, `/api/trade-logs`): trade-centric forensic feed — `trades_in_range` + `scanner_for_trades` + `screener_scores` + NEW `db_reader.recon_actions_for_trades` (reconciliation_log actions per trade). Full attribution (strategy/scanner/date/time/exit_reason/System Score). Raw log-line drill reuses `/api/logs?id=` (log_reader ref_id, UNTOUCHED). Distinct from System Logs.

**Live Activity** (NEW `/live-activity`, `/api/activity`, L10): single merged reverse-chron feed over 7 sources (`operations.build_activity` reuses list_signals/list_orders/closed_trades_today/recent_events/ledger_entries + kill) — types SIGNAL/ORDER/TRADE/SYSTEM/CAPITAL/RISK; per-min pulse; deep-links; `types` field = sources present. No standalone Alerts screen (/alerts still 200).

**FINAL 5-group nav COMPLETE (no nv-soon left):** Dashboard · Trading(5) · Analytics(7) · Operations(Live Activity/**System Health→/services carried**/Capital&Risk/Configuration/Controls) · Investigation(Audit/Trade Logs/System Logs). **System Health = carried** — nav points to the existing `/services` screen; the full services+vm consolidation was never assigned a sub-phase (deferred, flagged). **Carried-not-redesigned (still on pre-G5 templates, render+200):** Signals, Orders, Execution Analytics, Services(=System Health), VM. Non-menu direct-URL (still 200): /risk /capital /exposure /capacity /pnl /vm /statistics /reports /alerts.

**NEW endpoints** (blueprint `api/operations.py`, registered): `/api/controls-summary`, `/api/trade-logs`, `/api/activity` — read-only, login_required, EXISTING tables, NO schema. NEW readers `holdings_list`(extended +join), `recon_actions_for_trades`.

**Additive-only HELD:** pinned 6/13/8/6/4 + HARD_KILL chip-blink==1 unmoved (`test_pinned_shapes_frozen_after_g5d` + `test_hard_kill_blink_still_single`); ExportButton OFF; ScoreChip single-score (grep clean); parity (no mode branch). tests `test_g5d_operations.py`; `test_nav.py` updated (menu fully live, no placeholders). Verified: controls enabled 4/5, trade-logs week 10 rows (trd_c3 1 recon action), activity ≥5 source types newest-first, positions unavailable{mtm,ltp,unrealized,current_rr}. Next = Web Claude reviews two-state honesty → **G5e (VM deploy + resume soak)**. Related: [[gui_g5c_analytics_04jul]], [[gui_g2c_deploy_prep_03jul]], [[gui_readiness_g3_0_03jul]].
