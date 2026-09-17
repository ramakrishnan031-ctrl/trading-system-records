---
name: exit_alert_sign_fix_30jun
description: "Real-time exit alert SIGN fix (was hardcoded \"+\") — branch fix-exit-alert-consistency-30jun 9d9e1ae, NOT pushed; label relabel PAUSED"
metadata: 
  node_type: memory
  type: project
  originSessionId: 064a7869-6371-4c00-a7fc-cd5fd33d479a
---

**Real-time exit-alert SIGN fix — BUILT, branch `fix-exit-alert-consistency-30jun` `9d9e1ae`, NOT pushed.** Display-only, parity-safe.

**Trigger:** the 30-Jun CGCL manual-close test. Rama modified the TGT sell-leg to marketable; it filled at 224.80 vs entry 227.60 = a **−₹6.07 loss**. The order_placer real-time Telegram alert showed **"🎯 TARGET HIT +₹6.07"** (WRONG), while shadow_tracker showed −5.60 (correct).

**Root cause = ALERT-ONLY display bug, NOT a P&L bug.** `trades.net_pnl=−6.07`, `fm_ledger.pnl_delta=−6.07`, and the EOD summary were ALL correct (the P&L uses the actual fill 224.80, signed). The bug was solely in `order_placer._handle_exit_fill`'s alert (`:2199-2222`): the **TGT_HIT branch hardcoded `pnl_sign="+"`** (`:2204`) + printed `abs(net_pnl)` → a loss rendered as a gain. The SL_HIT branch already derived the sign correctly.

**Step-1 reconcile (IMPORTANT — corrects a premise):** the claim "the EOD summary shows (MAN)" is **FALSE**. `eod_squareoff._exit_tag("TGT_HIT")="TGT"` (`:561`), and the summary reads `trades.exit_reason=TGT_HIT` (`:783`) → it renders **`(TGT)`**, the SAME leg-based label as the alert + stored field. So **all three** representations (alert / stored `exit_reason` / summary) share the leg-based label; the **only** real divergence was the alert SIGN. The exit-reason DETERMINATION is leg-based everywhere: `exit_reason = _LEG_TO_EXIT_REASON[fill_entry.leg]` (`order_placer.py:2092`). No "manual" determination exists anywhere.

**Fix (done):** extracted a pure testable staticmethod `OrderPlacer._format_exit_alert(...)→(title,body)`; SIGN now derived from the SIGNED `net_pnl` in BOTH branches (loss→"-₹X"); label still `exit_reason`-derived so the alert stays consistent with the stored field + summary. No schema/stored-data change. 7 tests `tests/unit/test_exit_alert_sign.py`; order_placer suite 123 green.

**PAUSED (separate decision, needs review):** relabeling a loss-making TGT-leg fill as MANUAL/off-target would require changing the exit-reason DETERMINATION at source (`order_placer.py:2092`, leg-based) — which changes the STORED `trades.exit_reason` AND the summary (to keep the single-source agreement). That is a stored-data/logic change → NOT done; pending Web Claude review. After this fix the alert reads "🎯 TARGET HIT −₹6.07" (consistent with stored TGT_HIT + summary (TGT) −6.07 — the leg-label oddity is consistent, the egregious sign-flip is gone). Relates to the manual-intervention/OCO safety review (CGCL sibling-SL cancelled cleanly in 0.7s; capital released; only the alert was wrong).
