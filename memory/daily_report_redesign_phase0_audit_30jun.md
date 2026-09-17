---
name: daily_report_redesign_phase0_audit_30jun
description: Daily Report Redesign Phase 0 data-availability audit — Field Inventory Matrix + 8 capture gaps + tiering; full matrix in repo doc
metadata: 
  node_type: memory
  type: project
  originSessionId: 11d8ad87-58b5-45d4-8c5f-fc11018ec234
---

**Daily Report Redesign — Phase 0 (DATA-AVAILABILITY AUDIT) DONE 30-Jun.** AUDIT ONLY (no build/schema/report code). Full Field Inventory Matrix (all 12 sheets, field-by-field EXISTS/DERIVABLE/NEEDS_CAPTURE) = lifetime reference at **`docs/audit/daily_report_redesign_phase0_data_audit_30jun2026.md`** in the repo. DB-only rule applied: any field not written to DB by a system module = NEEDS_CAPTURE (a system file must write it first; report never reads YAML/logs/API).

**Headline:** redesign is ~75% buildable today. `reports/daily_report.py` (16:05 cron, 7 sheets: 0_EOD_Dashboard/1_Signals/2_Orders/3_Capital/4_Candles/5_Telegram/6_Strategy) is already a proto of the 12-sheet target + reuses `reports/style_constants.py`. BUT it already breaks DB-only in 6 places (reads system_config/scoring_weights/broker_costs/strategies/*.yaml + nse_holidays + candles CSV). `reports/daily_review.py` (~16:00, 9 sheets, 100% DB, lighter styling) is the one the redesign REPLACES (new ISO name `daily_trade_review_report_<date>.xlsx`).

**6 high-uncertainty items RESOLVED:** (1) Telegram sends = NOT in DB — `telegram_alerts` table is VESTIGIAL, `TelegramNotifier.send()` only HTTP+sentinel+failed_alerts.log; all 3 ops alerts bypass DB → NEEDS_CAPTURE. (2) MFE/MAE = SPARSE (`trade_excursions` 15/61 closed ~25%; post-EOD reconstruct, historical backfill deferred). (3) Broker blocked margin = fetched live (kite.order_margins().total / kite.margins().used) but in-memory only; only SYSTEM estimate `trades.margin_reserved`(flat 5x per-intent) persists → NEEDS_CAPTURE. (4) Per-trade slippage = FULLY EXISTS+live (`order_execution_log` per-leg + `trade_slippage_log` per-trade; system/actual/delta/`rr_damage_pct`=impact; writer `orders/slippage_recorder.py` wired). (5) Exceptions = order rejections (`orders.status`+`rejection_reason`) + reconciler naked (`orders.reconciliation_status='SL_MISSING'`+`reconciliation_log`) EXIST; broker API timeouts + generic exceptions = LOGS-ONLY → NEEDS_CAPTURE. (6) S&R = computed+stored per-PLACED-signal only (`sr_detector_results` JSON zones, 29 rows backfilled, shadow gated on sr_detector.enabled=true); candles in `analytics.candles`.

**Key DB facts (live VM 30-Jun):** `capital_snapshot`=0 rows DEAD → derive capital from `fm_ledger`(853). `pnl_reconciliation`=0 + no reconcile_pnl cron; `position_reconciliation`=0 (writes mismatch-only) → broker reconciliation side not persisted. Populated-but-unsurfaced: `trade_journal`(26), `strategy_metrics`(53), `eod_squareoff_log`(12), `eod_verification`(8), `control_tower_findings`(3), slippage tables.

**TIERING (confirmed/revised):** Tier-1 (build now, all EXISTS/DERIVABLE) = Dashboard, Signals, Orders-core, Strategies, **Slippage (RAISED in — data fully present)**, Reconciliation-SYSTEM-side. **Config_data = Tier-1 PENDING one decision:** snapshot resolved config to a DB table (DB-pure, recommended) vs accept deterministic config-file reads. Tier-2 (capture gaps) = Telegram, Capital(broker-margin), Reconciliation(broker P&L/pos/margin), Exceptions(broker-API/generic). Tier-3 sub-projects = Candles/S&R (MFE/MAE sparse first), EOD_Action_Items (derivable, value=synthesis).

**8 CAPTURE GAPS → 4 system-side work-items (scope SEPARATELY from the report):** W1 Telegram: `TelegramNotifier.send()` INSERT `telegram_alerts` (no schema). W2 broker margin: add `trades.broker_margin_blocked` (schema +col) at order_placer/position_sizer. W3 broker recon: wire reconcile_pnl→`pnl_reconciliation` + daily `position_reconciliation` OK rows (no schema). W4 exceptions: new `error_events` table OR extend `system_events` event_type for broker-API/generic/after-check failures (schema). Also: config-snapshot table (if option A), MFE/MAE coverage improvement.

**NEXT (Rama-driven):** (a) decide Config capture A-vs-B; (b) design Tier-1 sheets to build first; (c) scope W1-W4 as separate data-capture tasks. Relates to [[db_schema_v28_split]], [[mfe_mae_excursions_empty_28jun]], [[snr_detector_v1_27jun]].
