---
name: ddpi_enabled_26jun
description: DDPI enabled + completed on the Zerodha account LFL836 on 26-Jun-2026 14:11 IST — automated CNC/delivery sells + sell-GTTs now execute WITHOUT CDSL TPIN/OTP; resolves the existential T2 question for headless delivery
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b445dff-c546-4ec1-b292-3ec665699a63
---

**★ DDPI ENABLED + COMPLETED on the Zerodha account (LFL836) on 26-Jun-2026 ~14:11 IST.**

DDPI (Demat Debit & Pledge Instruction) means automated **CNC/delivery SELLs + sell-side GTTs
now execute WITHOUT a CDSL TPIN / OTP**. Previously, selling delivery holdings (or a sell-GTT
firing) required the manual CDSL TPIN/T-PIN authorization — impossible headless.

**Why this matters (resolves the Slice 2.5 go-live blocker):** the durable CNC overnight-protection
OCO-GTT (SLICE2.5-P1/P2: `orders/cnc_gtt.py` + `cnc_gtt_monitor.py`, schema v36 `gtt_state`) places a
SELL leg that must fire **headless** overnight. Without DDPI, that SELL-GTT trigger would have stalled
on a TPIN prompt. **DDPI was the existential T2 question** ("can automated delivery sell without
manual auth?") — now answered YES.

**Status of the delivery go-live gates after DDPI:**
- DDPI (automated delivery sell) — **DONE 26-Jun.**
- T2 (market-hours real-API: real CNC buy + real OCO-GTT + real CNC sell, no TPIN) — the headless-
  sell precondition is now satisfied; the live market-hours proof itself still runs Monday
  (`scripts/t2_cnc_gtt_realtest.py`).
- C1-watch — Monday.
- Then Rama flips `delivery_enabled` / `conditional_allocation_enabled` / `trade_type`.

The entire Slice 2.5 BUILD side is already deployed + dormant (FIX-183 + Phase 3 + Phase 4, on main
`37b3db3`). DDPI removes the last EXTERNAL (broker-side) blocker. See
[[slice25_p1_cnc_gtt_25jun]], [[slice25_p2_gtt_durability_25jun]],
[[slice25_phase3_delivery_caps_conditional_capital_26jun]], [[slice25_phase4_trade_type_gate_26jun]].
