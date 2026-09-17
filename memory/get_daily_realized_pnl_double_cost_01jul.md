---
name: get_daily_realized_pnl_double_cost_01jul
description: "get_daily_realized_net_pnl double-subtracts costs (real bug, SAFE-conservative); the 0.0 is a by-design EOD reset (not a bug) — INVESTIGATION, fix undecided"
metadata: 
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**INVESTIGATION 01-Jul (no fix yet).** Surfaced while building the Reconciliation CAPITAL block:
`state_store.get_daily_realized_net_pnl(date)` returned **0.0** on 30-Jun while true realized = ₹3.24.
Traced to TWO distinct things:

**Finding A — the 0.0 is NOT a bug (by-design EOD reset).** `fund_manager.reset_daily_pnl()`
(`capital/fund_manager.py:1298`) writes a `RESET_PNL` fm_ledger row with `pnl_delta = −old_pnl` to zero
the running SUM, called **DAILY at EOD** — `orders/eod_squareoff.py:487` **Step 7, AFTER all position
closes**. So `get_daily` is a live intraday running accumulator; the 0.0 is the correct POST-EOD state.
Both daily-loss controls read it LIVE during trading (pre-reset). The report only ever saw 0.0 because it
reads an overnight backup (post-reset) → for a report reading an EOD snapshot, `Σ RELEASE_USED.pnl_delta`
is the right persistent source (survives the reset). No "0.0 disarm" risk: reset is last, no entries/closes
after it that day, next day 0.0 is correct.

**Finding B — REAL BUG: costs double-subtracted.** `release_used` (`fund_manager.py:1020`) computes
`pnl = gross_pnl − costs` (NET) and writes `pnl_delta = pnl` **plus** `costs = costs` separately. But
`get_daily`'s SQL is `SUM(pnl_delta) − SUM(costs)` (`state_store.py:2261`) → **`= Σgross − 2·Σcosts`**
(costs removed twice). Its docstring claims `pnl_delta` is GROSS — contradicts the writer (NET).
Verified per-row (30-Jun: led_pnl == trades.net_pnl exactly; led_pnl+led_costs == trades.gross) and
cross-date (`Σ RELEASE_USED.pnl_delta == Σ trades.net_pnl` every day). 30-Jun: get_daily(pre-reset) =
3.24 − 4.65 = **−1.41** vs true net **+3.24** (off by −Σcosts −4.65).

**Blast radius — TWO decision paths read the buggy value (both daily-loss controls):**
- `fund_manager.release_used` `:1071` — post-close absolute daily-loss breach → `_on_loss_breach()` (kill).
- `risk_engine._run_checks` `:499` (RE7 DAILY_LOSS pre-trade gate) via `get_snapshot().daily_realized_pnl`
  (`fund_manager.py:1251`) → rejects new entries.
- Other call sites are non-decision: `reset_daily_pnl:1308` (reads old_pnl), `rehydrate:1445` (logging).

**Severity = LOW, SAFE direction.** The bias is always MORE NEGATIVE (costs ≥ 0) → both controls trip/block
EARLY = conservative; **never fails to trip / never late**. Magnitude = Σcosts/day (~₹1–5 now vs ~₹300 limit
= 3%×₹10k → <2% of limit). Scales with volume/capital. Failure mode = a spurious EARLY halt/block (e.g. a
high-cost near-flat day showing a fake loss), NOT a missed halt. So it's a genuine correctness bug but not a
safety hole today.

**Verdict:** (A) working-as-designed; (B) real bug worth a permanent fix — either the READ stops subtracting
costs (since `pnl_delta` is already net) OR the WRITE stores gross in `pnl_delta` (per the docstring); pick ONE,
consistently, and update `reset_daily_pnl` (it zeros whatever `get_daily` returns). Parity-safe (pure DB read +
write-convention; same in paper+live). NOT urgent (safe direction, tiny now) but fix before scaling capital/volume.
Tangential: 16-Jun `Σ RELEASE_USED.pnl_delta=−21.45` vs `Σ trades.net=0.0` (NULL-exit CLOSED_MANUAL trades didn't
compute net_pnl — a separate data-quality day). See [[dual_daily_loss_mechanism]], [[capital_operational_note]].
Fix decision pending (Rama). NO code changed.
