---
name: naked_trades_order_protocol_dead_13jul
description: "LIVE FACT (13-Jul, source+data verified): order_protocol is DEAD CONFIG (order_placer.py:855 uses _default_protocol=LIMIT_TRIPLE) → 100% of trades placed LIMIT_TRIPLE despite 12 strategies declaring CO_PLUS_TGT → NO exit-management engine is active on any live trade (naked entry→fixed SL→fixed TGT→15:17 squareoff). CORRECTS the Step-8 gap-map claim 'SmartTgtManager is the sole live SL owner'."
metadata:
  node_type: memory
  type: project
  originSessionId: 1d1e6c9d-1d21-4715-b704-3b6d175f00db
---

**Every live trade runs NAKED — no exit management. Confirmed 13-Jul-2026 by source + 134 real trades (READ-ONLY). This CORRECTS the Step-8 gap-map.**

**The dead config (V1):** 12 intraday strategies DECLARE `order_protocol: "CO_PLUS_TGT"` (3 positional declare LIMIT_TRIPLE), but the placer IGNORES it: `order_placer.py:855` sets `order_protocol = self._default_protocol` = `"LIMIT_TRIPLE"` (ctor default, lines 518/535). So **100% of live trades are placed LIMIT_TRIPLE** (trades.order_protocol confirms). `order_protocol` is DEAD CONFIG (= Audit-B Phase-7 "LIMIT_TRIPLE always").

**No SL ever managed (V2, counts not inference):** `sl_trail_count = 0` in **134/134** closed trades · `smart_tgt_state` = **0 rows** · orders `superseded_by` = **0** (no SL modification chain) · `entry_mode` = **100% FULL** (no partials).

**Why nothing fires (V3):** `SmartTgtManager` registers ONLY on CO_PLUS_TGT (`order_placer:~2095`) → never (all LIMIT_TRIPLE). `BreakevenManager` needs `trailing_sl_enabled` (FALSE on all 15) → never. `StructureExitManager` needs `structure_exit_enabled` (master FALSE) → never. **⇒ entry → fixed −1R SL → fixed +1.5R TGT → 15:17 squareoff. Nothing trails, moves to BE, or books a partial.**

**Why:** This surfaced only by looking at REAL TRADE OUTCOMES (Q2.7 found winners run to a median TRUE MFE 2.93R while we exit at 1.5R, leaving +1.43R/winner — because nothing manages the exit). The Step-8 gap-map [[v3_step9_exit_engine_12jul]] reasoned from CODE PATHS assuming trades were CO_PLUS_TGT, and concluded "SmartTgtManager = sole live SL owner." **That is WRONG: SmartTgt owns NOTHING; the live SL is a static broker resting order that is never modified.** Not a criticism of Step-8 — it's what only shows up against real fills.

**How to apply:**
- When reasoning about live exits, the truth is: **static SL + static TGT + 15:17 squareoff, no management.** Do NOT cite "SmartTgt is the live SL owner."
- The exit-management infra (SmartTgt/Breakeven/StructureExit) is BUILT but DORMANT. Activating it needs EITHER fixing `order_protocol` (so CO_PLUS_TGT places as CO → SmartTgt fires) OR enabling `trailing_sl_enabled` (→ BreakevenManager fires on LIMIT_TRIPLE).
- **But the Q2.8 backtest says exit-mgmt is only a MODEST lever:** best policy BE-after-0.5R → ~breakeven (−0.010R, +0.09R vs current, overfit-suspect, cuts losers not rides winners); the CONFIG-ONLY BreakevenMgr 60/80 is WORSE (−0.117); trail/partial-runner WHIPSAW on the choppy paths → Q2.7's +1.43R is largely UNCAPTURABLE mechanically. Exit-mgmt does NOT outrank M-S4. Re-derive post-M-S4.
- **SYSTEM_MAP + the Step-8 memory should be annotated** with this correction (not yet done — flagged).

Related: [[v3_step9_exit_engine_12jul]] (the gap-map being corrected) · [[m_s4_dead_scorer_steps_investigation_13jul]] · [[capital_chain_binding_constraint_analysis_13jul]]. Full analyses committed: `docs/audit/{expectancy_autopsy,true_mfe,mae_mfe_structure,exit_policy_backtest}_13jul2026.md` on branch `m-s4-fix-13jul`.
