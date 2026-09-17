---
name: q9-batch3-capital-invariant-18jul
description: "18-Jul Q9 batch 3 DONE+DEPLOYED — the capital invariant is asserted at every lifecycle stage on the wired path (incl. a WINNER and multi-position), anti-vacuity guarded, bite-proven against an internally-consistent wrong value. ⭐ E4/W10 EVIDENCE FOR RAMA: on ad34ee4 the contract invariant PASSES and the delta goes to EXACTLY 0."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**⚖️✅🚀 Q9 BATCH 3 — THE CAPITAL INVARIANT IS WIRED. DONE + DEPLOYED 18-Jul-2026.**
Report `docs/audit/q9_batch3_capital_invariant_18jul2026.md`. Tag **`deploy-18jul-q9-batch3`→`5fac11a`**;
PC == VM bare == tag. **TEST-ONLY — zero production files; no runtime behaviour change.**

## ⭐⭐ THE HEADLINE FOR RAMA — E4/W10 EVIDENCE (§C, read-only; nothing merged)
Ran the new test in a **throwaway worktree** on `e4-w10-pnl-contract`@`ad34ee4`:
```
ON e4-w10 @ad34ee4:  reader=-1052.4000  truth=-1052.4000  costs=52.4000  DELTA = 0.000000
[XPASS(strict)] test_reader_equals_independent_ground_truth      4 passed, 2 failed
```
⇒ **E4/W10 makes the reader EQUAL the independent ground truth; the delta goes to EXACTLY ZERO**
(vs `−52.40 == −costs` on main). **The structural invariants stay green there** — the fix doesn't disturb
I1/I2. The 2 "failures" are **the design working**: the strict xfail XPASSes (deliberate announcement) and
the exactness guard correctly objects that the delta is no longer `−costs` because it is now `0`.
**⇒ E4/W10 is verified correct against an INDEPENDENT computation on the wired path, not just its own unit
tests.** This is evidence for the pending risk-posture sign-off; it approves/merges nothing.
**When it lands, the migration is TWO edits in the test file:** drop the `xfail` marker, and change the
exactness assertion from `−SUM(costs)` to `0`.

## ⚠️ THE HYPOTHESIS WAS WRONG TWICE (verified against real code + runtime, not assumed)
* **I1 holds GLOBALLY** — `(intraday+positional) avail + reserved + used == _total`. This is what
  **production itself asserts** (`fund_manager.py:2268`, `cash_floor=_total`, `realized=0.0`; docstring
  `:2209` "tracks _total directly").
* **🔴 I1 PER-BUCKET DOES *NOT* HOLD — never assert it.** `fund_manager.py:2235` guards the per-bucket
  checks behind *"only when a partition is already negative"*, and its own comment says a legitimate
  PnL-shifted per-bucket split (`avail+reserved+used != total*pct`) **is never reached**.
* **I2 holds**, and **`_total` moves by the FULL P&L INCLUDING PROFITS** (runtime-verified: a winner took
  `_total` 500000 → 501945.70, exactly +net). **⚠️ P7a's `cash_floor + min(0, realized)`
  (`capital/invariant.py:89`) is a DIFFERENT QUANTITY — the *tradable balance*, where profits are withheld
  until T+1. DO NOT CONFLATE THEM.**

## §A3/A4 — independent ground truth + the EXACT delta
**Ground truth = `SUM(trades.net_pnl)`** — a different table written by a different path
(`state_store.py:2268`) from the `fm_ledger` aggregation the reader uses (`fund_manager.py:2365`). Two
computations sharing a source can't cross-check; these don't.
**⭐ THE DELTA IS EXACT, on BOTH sides of zero:** LOSS `reader−truth = −52.400000` vs `−costs = −52.400000`;
WIN `−54.300000` vs `−54.300000`. Algebraically `pnl_delta = gross−costs` (already net) ⇒
`reader = truth − SUM(costs)` ⇒ **`reader − truth ≡ −SUM(costs)`**. That pins it to E4/W10, not "some
mismatch".

## §B — what the test covers
Stages: fresh → reserve → ENTRY fill → close(LOSS) · a **REJECTED** signal that moves nothing ·
**2 concurrent positions ACROSS DIFFERENT STRATEGIES** (aggregation errors only appear with >1; the
per-strategy cap `signal_processor.py:624-640` fires BEFORE the risk engine — batch 2's fix) ·
**a WINNING round-trip** (nothing wired had EVER driven a winner through the capital path — **a P&L sign
error is invisible to a losses-only test**; the winner asserts `_total` *increases* by exactly the net).
**ANTI-VACUITY (the negative half for an identity):** an identity holds trivially on a system that did
nothing, so each stage also asserts the quantities MOVED, in the right DIRECTION, and that the ones which
shouldn't move didn't.
**Hazards designed around:** the daily-loss breach is **NOT passive** (`main.py:757-800` force-closes via
EOD `fire_now` + arms `soft_kill`) ⇒ scenarios stay far below the fixture's ₹10,000 limit and **every stage
asserts the kill never armed**. **Parity:** `FundManager` has no mode argument or paper/live branch;
divergence is downstream at `zerodha_adapter.py:348` ⇒ proven in paper = holds in live.

## §B3 — the contract-invariant design (strict xfail + exactness guard)
`xfail(strict=True)` on the true contract, naming `e4-w10-pnl-contract@ad34ee4`, PAIRED with a
**plain-green** test asserting the delta is **exactly `−SUM(costs)`**. Meets all four: green today ·
**cannot silently start passing** (strict turns the XPASS into a FAILURE ⇒ deliberate migration — **verified
in §C: it did exactly that**) · no rewrite, no hard-coded figure · **a NEW value bug can't hide behind the
old one**. Rejected: `skip` (hides it), asserting current buggy behaviour (bakes the bug in), a warning
(ignorable).

## §B5 — ⭐ BITE PROOF, and what the FIRST attempt revealed
**Attempt 1 (instructive):** skewing `reserve` was caught by **production's OWN runtime guard** first —
`CapitalInvariantViolation: ... after 'reserve': lhs=499895.0000 rhs=500000.0000 delta=-105.0000`. Good news
about the guard, but it proves nothing about *this* test.
**Attempt 2 (the meaningful plant):** apply `pnl*1.10` to **BOTH** the bucket **AND** `_total`, so
`avail+reserved+used == _total` **still holds** ⇒ **production's guard fired 0 TIMES**, yet the test failed:
**`I2 BROKEN: total moved by -1157.6400 but realized net P&L is -1052.4000`**. Restored ⇒ 5 passed/1 xfailed,
`capital/`+`orders/` clean.
**⇒ THAT IS THE WHOLE POINT: an internally-consistent wrong VALUE (the E4/W10 shape) is invisible to correct
column-level writes AND to the structural runtime guard; only a cross-checked end-to-end value assertion
catches it.**

## ⚠️ REGRESSION — a NEW failure appeared and was ATTRIBUTED (not waved through)
`test_interactive_startup.py::test_holiday_guard_missing_yaml_proceeds` — **NOT mine**, proven 3 ways:
isolation · **fails identically on the pre-change tree (`worktree` at `40db66a`, my file absent — never
`git stash`)** · **mechanism found: `main.py:1686-1695` — outside the service window `main()` prints "Not
starting (clean exit 0)" and returns 0, but the test expects 5.** It was **16:24 IST**; the morning baseline
was **10:55**, *inside* the window ⇒ the documented **TIME-OF-DAY-gated** PC-env class.
**⇒ Took a FRESH base run in the SAME window:** BASE `40db66a` **42F/4909P/7S** vs MINE **12F/4946P/5S/1xf**.
**`comm -13` EMPTY ⇒ ZERO ATTRIBUTABLE**, and the service-window test IS in the base set.
**Totals reconcile EXACTLY: 4958 vs 4964 = +6 = this file's 6 tests.** `xfailed=1` (marker visible),
`XPASS=0` (genuinely xfailing). **📌 LESSON: always re-baseline in the SAME time window — a morning
baseline is not valid for an evening run.**

Backup `pre_deploy_q9b3_20260718.db` sound (`quick_check=ok`, v44, 361 trades); schema v44, integrity ok,
0 FK; **kill-switch INACTIVE**; **on the VM: 5 passed, 1 xfailed (XFAIL, not XPASS)**.

## Remaining Q9 queue
**#4 sizing floors/caps** (min-lot · M-C6 zero-multiplier SKIP · `max_position_value` · tier multiplier —
batchable) · **#5 post-restart capital restoration** · back-fill the coverage-matrix metadata for the
remaining layers. **Separate, larger:** HARD-kill order cancellation + flatten-worker verification (the
first LIVE hard kill is its real test).

## Board carried forward (unchanged)
**RAMA DECISIONS:** **E4/W10 risk-posture sign-off — §C above is the evidence** · `cleanup.py` live-reset as
a `scripts/` operator tool? · security-watcher systemd-timer hygiene (offered, NOT applied — refused as
not-a-bug: a documented 60s heartbeat) · D1–D4 · the regime strategic choice · **FREEZE `min_pass_score`
while measuring**.
**RAMA ACTIONS:** **Kite token refresh (blocks Q10 Part B)** · rotate the Telegram token · 2FA seed VM-only ·
offsite backup · rpcbind · SSH→Tailscale · `require_hmac` (safe to flip now) · arm `pre-receive`?
**⚠️ MONDAY 20-Jul 08:15 = the FIRST REAL BOOT after the S4 fix — WATCH IT**; the strategy-registry officer's
first live run is **Mon 16:22**. **The 6 destructive CTs are UNBLOCKED but NOT RUN.**

Related: [[q9-batch2-killswitch-toctou-18jul]] · [[q9-batch1-daily-loss-wired-18jul]] ·
[[q9-money-path-coverage-18jul]] · [[e4-w10-done-17jul]] · [[capital-operational-note]].
