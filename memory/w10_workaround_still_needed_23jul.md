---
name: w10-workaround-still-needed-23jul
description: "OPEN QUESTION (not a finding) — now W10's double-subtract is fixed, are the get_daily_realized_net_pnl avoidance-workarounds still needed? Go reader-by-reader; do NOT bulk-remove."
metadata: 
  node_type: memory
  type: project
  originSessionId: 14bf9b40-85f2-431c-9374-2b011a05b93b
  modified: 2026-07-23T07:48:00.430Z
---

§D observation from the 23-Jul label-layer batch — RECORDED, NOT acted on. Explicitly out of scope: it would be a behaviour change on a capital-adjacent read path.

The stale W10 comments were the **justification for a workaround**. Several readers compute realized P&L a different way *specifically to avoid* `get_daily_realized_net_pnl` — that is what "W10 avoided" means, and it is still an accurate description of the code:
- `ops_dashboard/backend/api/risk_capital.py:44` `realized_loss_today` (source_note "W10 avoided", test-pinned — left alone by the batch on purpose)
- `ops_dashboard/backend/services/capacity.py` daily-loss "used"
- `reports/daily_trade_review.py` "3 · CAPITAL" reconciliation block

The reason for the avoidance was the double-subtract — and that is **fixed** (2026-07-17, `state_store.py:2447`; `fm_ledger.pnl_delta` is NET, the reader now sums `pnl_delta` only). So the open question: is each workaround still necessary, or could that reader now call the function directly and shed the indirection?

⚠️ It is a **QUESTION, not a finding** — do NOT assert they should change, and do NOT bulk-remove. Two reasons the answer is **reader-specific** (both surfaced while correcting the 5th doc carrier):
1. The `daily_trade_review` reconciliation block **STILL must avoid it**: at report time (16:05, post-15:17) `get_daily_realized_net_pnl` sums the EOD `RESET_PNL` counter-entry too, which zeroes the day's realized. Its avoidance reason **survives** the W10 fix — just a different reason now. Removing this one would be a regression.
2. The intraday loss readers (`realized_loss_today`, capacity) read DURING the day (pre-`RESET_PNL`) with a **LOSS-ONLY** semantic (D2: only RELEASE_USED losses), which differs from the function's net-including-gains. Their avoidance may still be justified by the loss-only semantic, independent of the double-subtract.

**Why:** the comment explaining a workaround was corrected, but the code it justified was not revisited — the kind of thing that otherwise stays forever. Now the justifying bug is gone, the indirection deserves a deliberate keep-or-shed check.

**How to apply:** register as a SMALL investigation only — "are the W10 workarounds still needed now that W10 is fixed?" Go reader-by-reader; each is a capital-path read ⇒ CAREFUL-LOOP queue, never a sweep. Relate to decision 01 (E4/W10 contract) and D1/leverage. NOT the 23-Jul batch.

Related: [[e4-w10-done-17jul]] [[e4-w10-outcome-impact-19jul]]
