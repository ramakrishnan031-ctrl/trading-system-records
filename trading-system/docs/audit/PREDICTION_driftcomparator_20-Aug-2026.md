# FROZEN PREDICTION — G3 CAPITAL-DRIFT COMPARATOR (`7fc5d5a`)

**Frozen:** 20-Aug-2026, before the full gate was run and before any deploy decision.
**Unit:** `7fc5d5a9d063c9fba3622c5ced2c6ba1c87d65d7` on `fix/capital-drift-comparator-20aug`, base `08b462b`.
**Status at freeze:** BUILT · ⛔ NOT DEPLOYED · ⛔ NOT PUSHED.

⛔ Scored by **signature**, not narrative. ⛔ A day that does not reach the stated
precondition scores `NOT TESTED`, never `PASS`.

---

## PRECONDITION FOR SCORING

At least one trading session runs with the unit deployed **and** at least one
position open, so that `held > 0` at a reconciler cycle. A flat-book day cannot
score this — it is the condition under which the defect cannot express.

---

## WHAT SHOULD CHANGE

**P1.** The next in-session capital-drift alarm, if any fires, reports
`delta` measured against **expected broker net**, not against real capital.
Concretely: on a day resembling 20-Aug, the delta that was **₹1,155–₹1,573**
falls to the **single- to low-double-digit rupees** band.
**Falsifier:** a delta still in the hundreds or thousands while the book is
merely open and nothing is actually missing.

**P2.** The ERROR log line gains its new operands and is greppable as:
`G3 CAPITAL_DRIFT: expected_net=… actual_net=… delta=… … [real_capital=… held=… realised_pnl=… held_today=… broker_used=… margin_residual=…]`
**Falsifier:** the old `expected=… actual=…` form still appears.

**P3.** The Telegram body no longer labels the expectation `Local:`. It reads
`Broker net: … | Expected net: …` plus a `Real capital / Held / Realised P&L`
line and a `Margin recon:` line.
**Falsifier:** an alert arrives still saying `Local: ₹10,6xx`.

**P4.** `G3 MARGIN_RECON:` appears at DEBUG every reconciler cycle in live.
**Falsifier:** absent while the service is running in live inside market hours.

---

## WHAT SHOULD **NOT** CHANGE

**N1. CHECK 2's residual stays non-zero and stays reported.** It must not be
absorbed into CHECK 1. Expected magnitude on a MIS-bearing book: **order ₹0.3–₹1**
per open MIS leg (broker per-instrument MIS margin vs flat `leverage_map 5.0`).
**Falsifier:** `margin_residual` is identically 0.00 across a session that held
an MIS position — that would mean it is being computed from our own figure on
both sides rather than against the broker.

**N2. Real capital is unchanged by opening a position.** `snapshot.total` at any
cycle still equals INIT total + realised P&L (+ carry), never reduced by a
reserve or commit.
**Falsifier:** `real_capital=` in the new log line falls when a position opens.

**N3. Sizing is byte-identical.** Same `qty` for the same signal inputs;
`position_sizer` and `fund_manager` are not in the diff at all.
**Falsifier:** any sizing change attributable to this unit.

**N4. No new alert class.** The only alert remains
`[LIVE] ⚠️ Capital Drift Detected`, same severity, same 30-min throttle.
**Falsifier:** a new title string appears.

**N5. Kill escalation unchanged.** G3 still publishes
`source_module="order_reconciler"`, still outside `_ESCALATING_SOURCES`, so
`drift_handler` still logs at INFO and never escalates from it.
**Falsifier:** any drift-driven kill transition traced to G3.

**N6. Tolerance untouched.** `capital_drift_tolerance: 50.0` and
`capital_drift_tolerance_pct: 0.10` are unchanged in config. The alarms go quiet
because the comparison was corrected, ⛔ **not because the band was widened.**
**Falsifier:** either config value differs post-deploy.

**N7. Paper produces no new alert class** — and this is **NOT TESTABLE by
observation**, because paper is retired (Rama, 20-Aug: *"ignore paper trade, no
longer going back to paper trade anymore"*) and the retained log corpus contains
**zero `[PAPER]` alert titles of any kind** against 1,041 `[LIVE]`. Scored by
code inspection only: the guard returns before any publish or send.

---

## KNOWN RESIDUALS — PREDICTED PRESENT, ⛔ NOT DEFECTS

**R1.** Flat `leverage_map.INTRADAY: 5.0` vs the broker's per-instrument,
marked-to-market MIS margin. ~₹0.32 on one leg, 20-Aug. ⚠️ **INFERRED**
— `order_margins()` was never called, so this attribution is **not proven** and
must not be reported as such.

**R2.** The 5% RESERVE buffer inflates `held` between placement and fill.
Measured ₹21.64 at 11:07:14 on 20-Aug; cleared at COMMIT 19 s later.
**Prediction:** the largest new deltas will cluster in RESERVE→COMMIT windows
and will be **transient**, disappearing on the next cycle.
**Falsifier:** a placement-window delta that persists after the fill.

**R3.** Mid-session restart. `initialize()` sets `_total` from broker cash and
`_intraday_carry` is deliberately left `0.0` (`fund_manager.py:1832`, "NOT
MEASURED"), so a restart holding an intraday position leaves a residual of
intraday_held + today's realised P&L. **Pre-existing structure, surfaced by this
change, ⛔ not created by it.** Predicted to be below the ₹50 base on a book of
today's size, so it should not alarm — but it will be visible in the new log line.

---

## THE ONE THING THAT WOULD FALSIFY THE WHOLE DESIGN

The identity `margins.net == total − held − daily_realized_pnl` was derived from
**one day, with carry = 0**. The first **carry day** (a CNC position held
overnight into the next session) is its real test, because that is when the
`_total`-lift and the carry cancellation actually engage.

⛔ **If the first carry day shows a CHECK 1 delta of roughly the carried
position's value, the carry-cancellation algebra is wrong** and this unit must be
reverted, not tuned. That is the single decisive falsifier and it cannot be
evaluated before such a day occurs.

---

## SCORING NOTE

⛔ The gate result does **not** score any of the above — the gate is a
regression check on a PC, not evidence about live behaviour. `DEPLOYED` is the
ceiling until a live session with `held > 0` produces the artefacts in P1–P4.
