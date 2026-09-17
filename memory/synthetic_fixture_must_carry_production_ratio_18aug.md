---
name: synthetic-fixture-must-carry-production-ratio-18aug
description: A balanced synthetic QA seed hid a real Screen-02 defect; and the plant harness itself reported a false green via stale bytecode. Two verification lessons from 18-Aug-2026.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9c8ec1fe-085c-431e-b80e-8d9622e91ce8
  modified: 2026-08-18T08:52:55.221Z
---

⛔ **A SYNTHETIC FIXTURE MUST CARRY THE PRODUCTION *RATIO*, ⛔ NOT MERELY PRODUCTION *SHAPES*.**

**18-Aug-2026, Screen 02 Recent Events.** The panel was rebuilt onto the real
trading-event feed, browser-verified, tested (59 tests) and committed
(`892ead1`) — all against a QA seed of **~76 signals : 50 orders**, because the
PC dev DB holds **zero** signals, orders and trades. That balanced ratio made a
raw newest-10 feed look correctly mixed.

**(P) PRODUCTION, measured read-only the same day:** signals were **3,568 of
3,747 feed rows (95.2%)**, at 24-50/minute, 44 in the busiest second, 115
distinct seconds carrying ≥10. The feed's own ordering against the production DB
returned **TWELVE IDENTICAL `Signal Received` ROWS SPANNING TWO SECONDS** — one
badge, no orders, no exits, no risk. The shapes were all right; only the
*proportions* were wrong, and the proportions were the whole defect.
Corrected in `d805bb3` (curated digest). See [[UNPUSHED_PENDING_DEPLOY_LEDGER]].

**Why:** every row the balanced fixture produced was individually valid, so no
per-row assertion could fail. Only the MIX was wrong, and nothing measured the
mix.

**How to apply:** when a screen ranks, sorts, caps or selects across sources,
seed the fixture at the **measured** production ratio and make that ratio part
of the test. Measure the ratio first — do not assume it.

---

⛔ **"REACHABLE IN A MAP" ≠ "REACHABLE ON SCREEN".**

The test that passed said the four artwork badges exist in the category→badge
**map**. True, still true, and it does not establish that any badge can *appear*.
Assert the **rendered/selected set** under realistic load, not the lookup table.

---

⛔ **A VERIFICATION HARNESS THAT CAN REPORT A FALSE GREEN IS NOT EVIDENCE — RE-RUN A PLANT HARNESS BEFORE TRUSTING IT.**

The same non-vacuity plant reported **GREEN on one run and RED on the next**.
Cause: CPython validates cached bytecode on **(mtime, size)**, and the harness
rewrites one source file repeatedly (plant → run → restore). Fixed by purging
`__pycache__` and running the child with `-B`; both plant sets were then re-run
**three times each**, 0 vacuous every time.

**How to apply:** a plant harness that mutates source in a loop must purge
bytecode and run at least twice before its result is quoted.
See [[feedback_verify_rc_not_output]] and [[tautological_check_class_05aug]].

---

⛔ **DO NOT ASSERT A BOUND AGAINST THE CONSTANT THE CODE USES.**
Hit **three times** in one day (note cap, signal cap, category cap): raising the
constant raises the assertion with it, so the guard stays green while the
protection is gone. Assert a **literal contract ceiling**, and assert the code's
constant sits under it separately.
