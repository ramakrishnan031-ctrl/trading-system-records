---
name: capital-drift-is-operand-mismatch-05aug
description: "The order_reconciler capital-drift CRITICAL compares total capital against broker free cash — it cannot escalate, and its 10% tolerance is an intraday-leverage calibration."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4eb48114-5788-48ac-94d6-e91b992a6fe4
  modified: 2026-08-05T12:29:24.659Z
---

**`⚠️ Capital Drift Detected` (CRITICAL, `Module: order_reconciler`) fired 3× on 05-Aug — the day
delivery went live. ⛔ NOT a loss.** Measured at the DEPLOYED `0197923` (⭐ `order_reconciler.py` and
`drift_handler.py` are **byte-identical** at `0197923` and HEAD, so cites hold at both).

⛔⛔ **IT CANNOT KILL ANYTHING, AND IT IS STRUCTURAL — NOT LUCK.** Published as
`source_module="order_reconciler"` (`order_reconciler.py:3667`);
**`drift_handler._ESCALATING_SOURCES` (`:66-70`) = `{fund_manager, fund_manager_self_check,
fund_manager_bucket_overflow}` — the reconciler is NOT in it.** A non-escalating source writes **one
INFO line and RETURNS** (`:147-161`) — before any tier, the DH4 counter, `soft_kill` or `hard_kill`.
⇒ **DH1's 3rd instance, and its FIRST on a book carrying real delivery positions.** [[kill-ladder-never-fired-28jul]]

🔑 **THE TWO OPERANDS ARE DIFFERENT QUANTITIES** (`:3590-3591`): **`expected = snapshot.total`**
(TOTAL capital — reservations reduce the *available* buckets, ⛔ **not** the total) vs
**`actual = margins.net`** = Kite's **`equity.net`**, which is **NET OF BLOCKED MARGIN**
(`zerodha_adapter.py:1452`; ⭐ `available.cash` is parsed **separately** at `:1453`).
⇒ **the delta IS the deployed capital.**

⭐⭐ **THE TOLERANCE IS AN INTRADAY-LEVERAGE CALIBRATION, AND THAT IS THE FINDING.**
`:3629-3631` → `effective_tolerance = max(₹50, abs(expected) × 0.10)` in session
(`system_config.yaml:368-369`). **FIX-190 (Bug I)'s own comment says why it exists:** *"in-session,
broker margin legitimately drops by the deployed capital, so the tight Rs tolerance fires
constantly"*. ⛔ **Intraday ~5× ⇒ blocked margin is a FRACTION of position value, inside 10%.
DELIVERY IS 1× AND BLOCKS THE FULL PURCHASE VALUE ⇒ a delivery book deploying >~10% of capital
BREACHES BY CONSTRUCTION** — and the positional bucket is **30% of total.**
⛔ **No delivery-specific tolerance exists** — width: `capital_drift_tolerance` across every tracked
`.py`/`.yaml` → **only a GLOBAL ₹ floor + a GLOBAL pct, zero variant hits.**

⛔⛔ **NEVER "VERIFY" IT WITH `delta == (opening − actual) + (expected − opening)` — THE IDENTITY IS
VACUOUS.** `opening` cancels; it reduces to `delta == expected − actual`, the **definition** of
delta ⇒ **it closes to the paisa for ANY `opening`, including a wrong one.** ⭐ **A check that cannot
go red is not a check.** **Falsifiable instead:** does `opening − actual` match the broker's **used
margin READ AT THE SAME TIME**, and does `expected − opening` match the day's booked P&L?
⚠️ **Alert values and a later Funds screenshot are DIFFERENT MOMENTS — comparing them is not a
finding.**

🌙🔴 **AND THE REGIME THAT MATTERS FOR CARRY — MEASURED 05-Aug EVENING, 5 MORE ALARMS.**
The 10% widening is **IN-SESSION ONLY**. `system_config.yaml:368` `capital_drift_tolerance: 50.0` is
labelled *"Production threshold (**out-of-session / overnight**)"*. ⇒ ⛔ **THE BAND COLLAPSES FROM
~₹993 TO ₹50 THE MOMENT THE SESSION ENDS — and overnight is the ONLY time a delivery position can be
held.** Measured 05-Aug: 3 in-session breaches at `tolerance≈990`, then **5 out-of-session at
`tolerance=50.00`, exactly 30 min apart, identical operands, ALL DELIVERED as CRITICAL.**
⚠️ **It does not stop at the next boot — it repeats for every hour the position is held**, because
the service stays up ([[delivery-carry-blocks-shutdown-05aug]]) and keeps the emitter alive.
⚠️ **AR9 accepted this CRITICAL for ONE session against the in-session regime only; the overnight
regime was never scored.**

✅⭐ **THE DELTA DECOMPOSES EXACTLY — USE THIS, NOT THE VACUOUS IDENTITY BELOW.** 05-Aug 17:46:
`expected 9928.31 = 9883.70 fm_ledger INIT + 44.61 day realised P&L`; `actual 9296.30 = 9883.70 −
587.40 CNC block`; `delta 632.01 = 587.40 deployed + 44.61 unsettled realised`. **To the paisa.**
⭐ **It CAN go red:** the three operands were measured hours earlier from `fm_ledger`, the two totals
emitted by a different subsystem reading the broker API. ⇒ **deployed capital + unsettled realised
P&L, zero residual.**

⏱️ **Repeats throttled to 1 / 30 min** (`capital_drift_alert_interval_sec: 1800`) ⇒ **3 emails = ONE
episode.** ⛔ **Silence after has THREE causes: still in-window · drift returned within tolerance
(which RESETS the throttle, `:3636-3643`) · the check STOPPED RUNNING.**

📌 Registered: `MASTER_PENDING` **§B#7** (4th two-pipeline coupling member — ⭐ **the first that did
NOT wait to be predicted**) · **§B#5** (DH1 exercised live) · `docs/expected_alarms.md` **§3a** with a
6-condition discriminator. Worksheet: `docs/audit/ADDENDUM_capital_drift_05-Aug-2026.md`.
⛔ ~~**NO FIX AUTHORISED**~~ → **SUPERSEDED 20-Aug-2026: A FIX IS NOW AUTHORISED AND BUILT.**
The 05-Aug diagnosis above was re-measured independently on 20-Aug (4 alarms, residual 0.00 each)
and **held exactly**. ⇒ [[drift-comparator-fix-20aug]] — `7fc5d5a`, **BUILT · ⛔ UNPUSHED · ⛔ UNDEPLOYED**.
⭐ Everything ABOVE this line remains accurate as the diagnosis; only the *"no fix"* status expired.
(Original context: money-path governor, careful loop; its home is the delivery configuration
surface (**A-DEC-3 item 5**), itself gated on item 4.)

Related: [[t2-shared-cash-seam-29jul]], [[capital-vocabulary]], [[dual-daily-loss-mechanism]].
