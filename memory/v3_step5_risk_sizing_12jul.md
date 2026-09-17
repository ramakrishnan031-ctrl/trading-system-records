---
name: v3_step5_risk_sizing_12jul
description: V3 Step 5 — 03.06 Risk & Sizing VERIFY + inert delivery-sizing scaffold; LIVE sizing byte-identical; 2 fail-OPEN cases + ATR-into-live-SL flagged for review; BUILT-but-UNPUSHED
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Shared-Engine — Step 5: 03.06 Risk & Position-Sizing (12-Jul-2026). ADAPT = mostly VERIFY + ONE minimal inert scaffold. LIVE sizing BYTE-IDENTICAL. BUILT-but-UNPUSHED.** Ran parallel with the Step-4b OFF→shadow soak. Gap-map + review doc: **`docs/v3/V3_STEP5_RISK_SIZING_GAPMAP.md`**. Follows [[v3_step4b_parity_artifact_12jul]].

**T1 verdict: 03.06 is essentially COMPLETE** in the existing `position_sizer`/`risk_engine`/`fund_manager` (source-verified):
- risk-based sizing from SL DISTANCE ✓ (`position_sizer.calculate`: `sl_distance=abs(entry-sl)`, `qty_by_risk=floor(risk_rs/sl_distance)`; SL is the `sl_price` PARAM = the V3 seam);
- min(risk,capital,conc) ✓; tier ON/OFF + mult HIGH1.0/MED0.7/LOW0.5 ✓; position_value cap 40% ✓; per-trade conc 10% ✓;
- per-bucket caps ✓ (fund_manager intraday70/positional30 absolute no-borrow; risk_engine delivery COUNT caps 3/5 inert; per-strategy cap);
- daily risk ✓ (risk_engine DAILY_LOSS 3% + CONSECUTIVE_LOSSES 4 + DAILY_TRADES 10);
- fail-CLOSED ✓ mostly (2 deliberate fail-OPEN, flagged);
- delivery leverage DELIVERY:1.0 ✓.

**ONLY genuine gap = delivery-specific SIZING knobs** (sizer used ONE global risk_pct + max_position_value_pct). **T3 scaffold (INERT):** added optional `delivery_risk_per_trade_pct` + `delivery_max_position_value_pct` (default None) to `PositionSizingConfig` + `position_sizer` (`eff_*` used ONLY when `bucket=="positional"` AND knob set, else global) + main.py + system_config (`null`). **Provably byte-identical:** default None→global; live bucket is NEVER positional (delivery double-locked OFF + force_intraday_only coerces to INTRADAY). Reuses the sizer (no parallel/delivery sizer). Delivery NOT activated. **No risk_engine/fund_manager code change** (already complete).

**T2 seam:** the sizer's `sl_price` param IS the seam — V3 03.03's S&R-derived `computed_sl` feeds it LATER with NO sizer change. LIVE SL still FIXED_PCT (unchanged this step).

**T5 REVIEW ITEMS (flagged, NOT changed unilaterally — for ChatGPT/Rama):**
- **(a-i) kill_switch=None → KILL_SWITCH gate skipped (fail-OPEN, RE8).** Prod always injects a real ks + order_placer re-checks (last-mile), so live is fine. Runtime fail-CLOSED would break many tests + could halt on a transient. **Rec: boot-time fail-fast assertion in main.py (live) that ks is injected**, not a runtime flip.
- **(a-ii) sector lookup fail → UNKNOWN+admit (fail-OPEN, RE9).** Sharing one UNKNOWN bucket is CONSERVATIVE on the 40% cap (not a blowout). Fail-CLOSED would reject symbols missing from the sector map (over-restrictive on a data-gap). **Rec: KEEP fail-OPEN**; improve sector-map coverage. Low priority.
- **(b) Wire `core/candle_math.atr` into LIVE SL?** Would change every intraday SL distance → change LIVE position sizes (money path, LARGE blast radius). **Rec: DO NOT wire live now**; ATR/S&R SL is the V3-shadow-path intent via the `sl_price` seam + its own parity proof before any live flip.

**G1 byte-identity:** `tests/unit/test_position_sizer_delivery_scaffold.py` (4: None→identical, knob-set-but-intraday→global, delivery-bucket→delivery-risk applies [future path], max-pv scaffold inert-on-intraday). **G2 CONFIRMED (12-Jul, this session — the run interrupted by the power outage was re-run to completion):** targeted regression GREEN — sizer/risk/fund_manager **174 pass** (incl. the 4 new scaffold tests) + config_loader/config_auditor **79 pass**. **Full-suite dirty tree = 4494 pass / 12 fail / 15 skip (716s).** DEFINITIVE clean-vs-dirty stash-diff (stashed all Steps 1-5 tracked mods, re-ran the same 12 node-ids on the clean baseline): **12 fail clean == 12 fail dirty → my changes add ZERO new failures; stash popped, tree restored.** The 12 are the known PC-env baseline (test_main [webhook-secret + ContinueFromGate], order_placer_fix061 ×4, phase17 flask-max-content, state_store fix156, fix181 reconciler-inflight, interactive_startup holiday-guard — deterministic on Windows, green on VM), NONE in a Step-5 area. paper==live. Files: M `capital/position_sizer.py`, `core/config_loader.py`, `main.py`, `config/system_config.yaml`; ?? test + gap-map doc. **BUILT-but-UNPUSHED** (with Steps 1-4b). **NEXT = Step 6 (03.05 Portfolio Allocator — the NEW ranked-admission core) after review.** If the Step-4b shadow soak surfaces divergence, STOP before enforce + report separately.
