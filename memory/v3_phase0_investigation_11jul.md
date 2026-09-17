---
name: v3_phase0_investigation_11jul
description: "V3 Shared-Engine Phase-0 READ-ONLY investigation + gap analysis (Common Utils + 03.01-03.09) — ADAPT/NEW map, drives every V3 build step"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Shared-Engine — Phase 0 (11-Jul-2026, READ-ONLY, no code/commit/VM change).** Source-verified gap analysis against `main`@`8116b74` mapping each existing component to the new V3 modules, ADAPT vs NEW. **Report: `docs/v3/V3_PHASE0_INVESTIGATION_GAP_ANALYSIS.md`** (self-contained for Web Claude + ChatGPT; deliverables A–F). Method: read config/screening/quality_scorer/step_executor/entry_gate + PATHS/SYSTEM_MAP + THREE sequential read-only investigation agents (execution/exit; ingestion/risk/sizing; config/delivery/S&R/regime/utils) — no parallel fan-out (per [[feedback_sequential_agents_only]]).

**ADAPT/NEW verdicts (the headline):**
- **Common Utilities → ADAPT** (`orders/price_math.py`, `sr_detector/pivots.find_swing_pivots`, `sr_detector/models.Candle`, `data/candle_store.py`, `core/time_authority`, `core/market_windows`, `core/logger`, `core/config_loader.load_all`) **+ NEW ATR/true-range helper (does NOT exist — ATR only consumed pre-computed; ATR-SL/TGT unimplemented, falls back FIXED_PCT) + NEW timeframe-resample util.**
- **03.01 S&R Detection → ADAPT** `sr_detector/` (per-TF day/60m/30m swings+zones+confidence+PDH/PDL/PDC anchors; ENABLED but SHADOW/observer-only, never gates).
- **03.02 Market Regime → NEW** (repo-wide grep negative — no index regime/confidence/extreme flag anywhere).
- **03.03 Hard Gate → ADAPT-by-EXTRACTION** — circuit + signal_age logic exists ENTANGLED in `secondary_screener.py` (`_circuit_proximity_reason` pre-fill hard reject + signal_age step-7 defense-in-depth L275) AND as score steps 9/10 in `step_executor.py`. Extract circuit/age/R:R/freshness/liquidity into a pre-scoring gate; do NOT add a parallel path.
- **03.04 Scoring → ADAPT** `quality_scorer.py`+`scoring_weights.yaml` (10 steps=100, proportional, min_pass 60, tiers 80/65). Re-scale surviving weights as Execution SEED; `circuit_check`+`signal_age` MOVE OUT to gates (changes proportional denominator + all historical scores — do together).
- **03.05 Portfolio Allocator → NEW core + ADAPT primitives** — **NO ranked admission exists; admission is FCFS/concurrent** (5-worker ThreadPool, no candidate set assembled; "Priority rank #1 of 1" is hardcoded placeholder `signal_processor.py:439`). **`max_concentration_pct 0.10` is PER-TRADE not shared/aggregate** (only shared cap = sector 0.40). Build ranked-admit + shared-conc ON `fund_manager.resolve_bucket_allocation` (70/30 absolute, no-borrow) + `risk_engine`. **Biggest lift; touches hot path.**
- **03.06 Risk & Sizing → ADAPT** `position_sizer.py` (min(risk,capital,conc); tier ON/OFF `enabled:true`; mult 1.0/0.70/0.50) + `risk_engine.py` (10 gates; mostly fail-CLOSED, 2 deliberate fail-OPEN: unknown-sector admit+WARN, kill_switch=None skip).
- **03.07 Entry → ADAPT** (`order_placer.place`+`full_entry_engine`+protocols; software OCO; MIS coercion; **idempotency behavioral not DB-UNIQUE** — hardening candidate).
- **03.08 Trade Mgmt → ADAPT** (only-tighten trail 3 ways: `smart_tgt_manager` CO, `breakeven_manager` LIMIT_TRIPLE 60/80%, `structure_exit_manager` structure; modify-in-place not cancel-replace).
- **03.09 Exit → ADAPT** (`_handle_exit_fill`+`_cancel_oco_siblings`; `eod_squareoff` 15:17 delivery-exempt; kill_switch; CHECK2 SYSTEM_OVERSELL). **15:15 = ENTRY CUTOFF only, NOT a position flatten** (15:17 is the flatten) — a hard 15:15 flatten would be NEW.

**Key premises corrected vs task:** freshness is 600s intake expiry + >60s screening hard-zero (NOT 90s); 15:15≠force-flat; concentration cap is per-trade not shared. **UNKNOWNS for ChatGPT/Rama:** 15:15 flatten intent? "anchors" = PDH/PDL/PDC or new? authoritative freshness value? ranked-admit = batching window or rank-on-arrival? **Delivery CONFIRMED OFF** (force_intraday_only true / delivery_enabled false / trade_type INTRADAY; 12 WILL/3 WON'T dormant; only GTT-protection carve-out; no CNC ever executed in main). Related: [[trade_type_intent_segregation_investigation_10jul]] [[snr_detector_v1_27jun]] [[full_repo_audit_04jul_pending]]. **NEXT = Step 1 Common Utilities (after Web Claude + ChatGPT review).**
