---
name: fix1-carried-position-accounting-10aug
description: "FIX 1 BUILT (e70e004, branch fix/capital-carry-rehydrate, UNPUSHED): a carried delivery position was counted twice when the FundManager re-bases from broker cash — once by its absence from net, once as a replayed reservation against that same reduced cash."
metadata: 
  node_type: memory
  type: project
  modified: 2026-08-10T08:07:55.210Z
  originSessionId: a7c87fd2-1ff0-402f-9ae5-74de99732728
---

**`<BUILT · TESTED · REBASED ONTO THE DEPLOYED REF · ⛔ NOT PUSHED · ⛔ NOT DEPLOYED>`**
Branch **`fix/capital-carry-rehydrate`**, **sixth worktree** `D:\Projects\trading-system-capcarry`.
🔴 `git worktree remove` when done — the commits live in the main repo's `.git` and survive removal.

| | SHA | base |
|---|---|---|
| **NOW (rebased 10-Aug)** | **`63caa52`** fix · **`2e1f109`** test | **`645728d` = THE DEPLOYED REF** |
| before the rebase | `e70e004` fix · `2e7de7f` test | `f963438` (local `main`, carries F6) |

🔒 **The pre-rebase tip is kept as tag `fix1-prerebase-10aug`.** ✅ **`git range-diff` prints `=` on
BOTH commits ⇒ the rebase altered NOTHING; the patches are identical.**

---

## ① ROOT CAUSE — ⛔ ACCOUNTING SEMANTICS, NOT CORRUPTION

> ## 🔑 **A CARRIED DELIVERY POSITION IS COUNTED TWICE THE MOMENT THE FUND MANAGER RE-BASES FROM BROKER CASH.**
> **Once by its ABSENCE from `net`** — the broker took the money when the shares were
> bought *(MEASURED 10-Aug: `net=209.80` alongside `907.02` of CNC stock; Rama: an
> account of ~`₹1,117`)*. **Once by its PRESENCE** as a replayed reservation deducted
> from a bucket whose base is a fraction of that same, already-reduced cash.
> ⇒ `0.30 × 209.80 − 907.02 = −844.08` and INV6's non-negativity guard fired.

⛔⛔ **THE GLOBAL IDENTITY WAS NEVER BROKEN** — `−697.22 + 0 + 907.02 == 209.80 ==
`_total`, delta `5.68e-14`. **Only the PARTITION went negative.** ⭐ That is why this is
semantics and ⛔ not a ledger repair. [[delivery-book-ceiling-10aug]]

🔑 **AND `_check_invariant`'s OWN COMMENT WAS DECISIVE: the per-bucket EQUALITY IS NEVER
EVALUATED** — INV6 raises on the negative field *before* the equality check, by design
*("a legitimate PnL-shifted per-bucket split … is never reached")*. ⇒ **the only contract
that must hold is the GLOBAL `Σ == _total`, and it did.** ⭐ That collapsed the fix.

---

## ② THE RULE — BEFORE → AFTER

| | rule |
|---|---|
| **BEFORE** | a bucket's base is `_total × pct`, where `_total` is broker CASH |
| **AFTER** | a bucket's base is **its share of CASH + the margin the broker has ALREADY removed from that cash for THAT bucket's carried positions** (`_bucket_base()`), and `_total` is cash + carry |

⭐ **The carry enters the base and is IMMEDIATELY consumed by `reserved`/`used` ⇒ net
effect on free capital is ZERO.** ⛔ It does not create capacity; it stops a second
deduction. **With no carry, `_bucket_base()` returns `_total × pct` — the previous
expression, unchanged.**

🔴 **ITS OWN CARRY, ⛔ NEVER A PRO-RATA SLICE.** Lifting `_total` and keeping `_total ×
pct` **DOES NOT WORK** — on 10-Aug it leaves positional at `0.30 × 1,116.82 − 907.02 =
−571.97`, still negative — **and it would hand the intraday bucket 70 % of money locked
in delivery stock.** ⭐ Measured before adopting; the obvious model is the wrong one.

✅ **ONE SEMANTIC, TWO CALL SITES:** boot `rehydrate_from_open_trades` and the 09:15
`sync_from_broker` now use the identical rule and the identical fields. ⛔ Two meanings
WAS the defect.

⚠️ **A PRECONDITION NOW EXISTS AND MUST NOT BE VIOLATED: the seed fed to `initialize`
must be CASH, ⛔ not cash+holdings.** Production satisfies it (`compute_live_seed()` =
`broker.net − pnl_carryover`). ⭐ Fed an un-debited balance the correction over-states by
the carry — which is exactly how the old fixture hid the bug.

---

## ③ 🔴 SCOPED TO THE POSITIONAL BUCKET — DELIBERATELY, AND IT IS THE CONSERVATIVE HALF

**(P) MEASURED:** delivery cash leaves `net`. **(I) NOT MEASURED:** whether a *blocked
INTRADAY* margin also leaves it. ⛔ **The `margins()` capture that would prove it —
MONDAY §3.6b — NEVER RAN**, because no delivery entry occurred.

> ⭐ **Leaving intraday alone is FAIL-SAFE in the only direction that matters: today it
> UNDER-states intraday availability on a same-day crash restart, so the system trades
> SMALLER, never larger.** ⛔ Correcting it on an inference would change live sizing using
> a broker property we have never observed.
> 🔑 **To extend: take the §3.6b readings FIRST. The field (`_intraday_carry`) and
> `_bucket_base()` already carry the semantics; only ONE assignment changes.**

---

## ④ 🚨 A PHANTOM ALARM WAS CAUGHT ON THE WAY

`sync_from_broker` compared `broker_balance − old_total`, but `old_total` already
includes the carry. ⇒ **the first 09:15 sync after ANY rehydrate would have published a
`CapitalDriftDetected` of EXACTLY the carry — a guaranteed false `CAPITAL_DRIFT` every
morning a position is held.** ✅ Now differences like with like. ⭐ Not in the card; found
by auditing every remaining use of the raw broker figure inside the function.

---

## ⑤ 🧪 A FIXTURE WAS ASSERTING WHAT PRODUCTION CONTRADICTS

**`test_fund_manager::test_rehydrate_preserves_post_snapshot_equality` restarted `fm2` on
the SAME cash `fm1` opened with** — modelling a broker that **never debits a delivery
purchase**. ⛔ Production is the opposite, and it is measured.

> ⭐⭐ **PROVEN, ⛔ not asserted: with the fixture corrected to production shape, the OLD
> code FAILS — the restart reconstructs `total = 94,250` instead of `100,250`, silently
> LOSING the ₹6,000 holding.** 🔑 **The fixture had been hiding this the whole time: two
> errors cancelled (cash that still contained the purchase, minus a reservation replayed
> against it).** 🏷️ The named class — *a fixture asserting what its own data cannot
> support makes a wrong reader look right.* [[capital-readers-fixed-25jul]]

⚠️ **The same shape sits in `test_mc1_live_seed_rehydrate`**, whose simulated
`broker_net = BASE + pnl` also never subtracts open-position margin. ⛔ **NOT touched** —
its assertions survive because the carry is positional-only and M-C1's trades are
intraday. 📌 **Recorded: if the intraday half is ever corrected, M-C1's fixture must be
re-shaped FIRST.**

---

## ⑥ WHAT THE CARD ASKED, ANSWERED

⭐⭐ **§3's preferred response falls OUT of the accounting, with NO new mechanism:** after
the fix the positional bucket holds `0.30 × 209.80 = ₹62.94` free — **which refuses new
delivery commitments by ordinary capital constraint** *(a ₹446 share is unbuyable)*
**while leaving intraday untouched.** ⛔ **No governor, no scoped-kill, no threshold was
built** — the card's *"refuse new delivery commitments, do not halt intraday"* is what
correct accounting already produces.

⛔ **`max_open_delivery_positions` NOT touched. No percentage limit invented. No tolerance
raised, no INV6 disabled, no symbol special-case, no rupee threshold.**

---

## ⑦ GATE — ⛔ never the word "clean"

**`PYTEST_RC=1` · 9 failed / 5,589 passed / 4 skipped · 877 s.**
✅ **`NO NEW FAILURES` — CONTROL RUN, SET-IDENTICAL: the same 9 fail with
`capital/fund_manager.py` reverted to `main`; 0 new, 0 disappeared.** ⭐ **Arithmetic
closes exactly: 5,582 baseline passed + 7 new tests = 5,589.**
⚠️ **The tree MOVED mid-gate once (a comment tidy) — that run was KILLED AND DISCARDED,
⛔ not reported**; the reported gate ran on a tree fingerprinted by md5 before and after.
✅ **7 new tests, RED-first** — all 7 red pre-fix, and case A reproduces the live failure
mode exactly (`NEGATIVE_MARGIN_AVAILABLE`, same `invariant.py:237` guard).
🧪 **PARITY: LIVE-ONLY. Paper has no T+1 settlement model and never calls `margins()`, so
a paper run CANNOT reach this state.** ⛔ No paper claim is made.

---

## ⑧ ⛔ WHAT IS STILL OPEN

- 🔴 **THE 3-SLOT CEILING IS `FIX 3`, ⛔ NOT MIXED IN** *(⚠️ this bullet said `FIX 2` when written;
  the card then scoped **Fix 2 = the two preflight checks** and named the book-growth problem
  **Fix 3** — ⛔ corrected, not silently overwritten)*. The corrected model still lets the
  delivery book grow across days *(each morning the split re-applies to the remaining
  cash)*, bounded only by `max_open_delivery_positions` and concentration.
  [[delivery-book-ceiling-10aug]]
- ✅ **The two tautological checks WERE `FIX 2` — now BUILT, `13df9cd`**, and ⛔ nothing of Fix 1
  was touched by it. [[fix2-preflight-capital-checks-10aug]]
- 🔴 **THE INTRADAY RESIDUAL (§⑨) IS OPEN AND BELONGS TO §3.6b** — ⛔ not Fix 2, ⛔ not Fix 3.
- ✅ **Deploy sequencing — the REBASE IS DONE (§⑩); the DECISION remains Rama's.**

---

## ⑨ 🔴 CASE 8 — THE SWEEP. THE ANSWER IS *SURVIVES*, AND IT IS STRUCTURAL — **FOR DELIVERY ONLY**

⭐⭐ **`positional_avail` reduces to `pct × cash` for ANY cash ≥ 0**, because the carry enters its own
bucket's base and is IMMEDIATELY consumed by `used`. **MEASURED at five sweep depths INCLUDING ₹0, on
BOTH paths** *(boot-rehydrate and the 09:15 `sync_from_broker`)*. ⛔ **Not a property of these numbers.**

🔑 **THE CARD'S STATED REASON FOR WORRYING WAS THE REJECTED MODEL.** It read *"the corrected base is
`0.30 × (cash + carry)`, so a large drop in cash shrinks the base while the carry stays whole"* — but
that is the **pro-rata** model §② measured and REJECTED. The implemented rule is `pct × CASH + ITS OWN
carry`, so a cash drop cannot strand the carry. ⭐ **The worry was well-aimed; the mechanism named was
not the one built.**

### ⛔ **AND THE BOOT HALF ALREADY EXISTED — the card's premise is HALF WRONG, stated plainly**
**Case A IS the sweep on the boot path:** `_DAY0_CASH = 10_000` establishes the carry, `_SWEPT_CASH =
500` boots the next morning *(and the file's own constant is commented `# after the quarterly
settlement sweep`)*. ⇒ *"None of them reproduces cash leaving AFTER the carry was established"* is
**false for the boot half**. ✅ **The card's SECOND sentence found a REAL hole: case E exercised
`sync_from_broker` at UNCHANGED and at RISING cash only. A FALLING sync was never tested** — and it is
an INDEPENDENT firing site aimed at a **RUNNING session with the market open**, not at a dead boot.

**NEW: `H`** *(the sweep at 09:15; RED pre-fix with `NEGATIVE_MARGIN_AVAILABLE −1850.00` raised **out of
`sync_from_broker`**, ⛔ not out of the boot — its precondition is a HEALTH check, not a post-fix value,
so it can ONLY go red at the sync)* · **`H2`** *(both paths × 5 depths)*.
✅ **H also pins that the sweep is STILL published as `CapitalDriftDetected` — real money did leave —
while NOT publishing `fund_manager_bucket_overflow`.** ⭐ Surviving it ≠ not noticing it.

### 🔴🔴 **THE RESIDUAL — FIX 1 IS CORRECT BUT INCOMPLETE, AND THIS IS THE FINDING**
> ## ⛔ **THE SAME SWEEP STILL HARD-KILLS THROUGH THE *INTRADAY* BUCKET.** It has no carry field, so a
> replayed intraday margin is still deducted from a cash base that may already exclude it.

**MEASURED** *(probe, `C₀ = 10,000`, `INTRADAY` leverage 5.0)*: with a ₹2,000 intraday book open, a
sweep to **₹2,000 / ₹500 / ₹0** gives `NEGATIVE_MARGIN_AVAILABLE −600 / −1,650 / −2,000`, while the
**identical** sweeps with a ₹2,000 DELIVERY book give `positional_avail 600 / 150 / 0` — ✅ all survive.
**Same-day CRASH RESTART, no sweep at all:** kills once `M > 0.4118 × C₀` = **58.8 % of the intraday
bucket** *(0.70·C₀ ≥ 1.70·M)*. ⭐ **Tighter than delivery's old 76.9 % ceiling.**
🔑🔑 **BUT IT IS ENTIRELY GATED ON THE UNMEASURED PREMISE: with `net` still CONTAINING blocked intraday
margin, NOTHING kills — survives even at 97.1 % of the bucket.** ⇒ ⭐ **This is the sharpest possible
statement of why §3.6b matters: the whole intraday exposure is one unmeasured broker property.**
🏷️ **LATENT, ⛔ not LIVE** *(needs a same-day restart or a sweep landing on an open intraday book)* ⇒
[[feedback-live-vs-latent-findings]] says CONTINUE + document. ⛔ **NOT built — that is the §3.6b
decision, ⛔ not Fix 1, ⛔ not Fix 2.**

### 🧪 **AND TWO CLAIMED CONTROLS DID NOT EXIST**
**The committed docstring said *"B, F and G pass pre-fix"*. MEASURED against `f963438`: all three
FAILED.** B on a post-fix expectation · **F on `AttributeError: 'CapitalSnapshot' object has no
attribute 'intraday_carry'`** *(the field is NEW — asserting it destroys the control)* · **G because its
own setup raised in `_boot_next_morning` before ever reaching the assertion under test.**
⇒ 🏷️ **A GUARD THAT CANNOT REACH ITS ASSERTION ON THE OLD TREE IS NOT A GUARD** — the file claimed two
two-tree controls it did not have. ✅ **REPAIRED: F now asserts nothing that did not exist pre-fix**
*(its new-field assertions moved to `F2`, post-fix-only by construction)*; **G boots on HIGH cash and
overdraws RELATIVE to the reported available**, so both are green on BOTH trees. **The docstring now
carries the MEASURED per-case RED/GREEN table instead of the claim.**
📏 **Control run: `12 failed / 2 passed` pre-fix (F, G the two greens) · `14 passed` post-fix.**
⛔ **Fix 1's logic UNCHANGED — §⑨ is tests only.** [[feedback-verify-rc-not-output]]

---

## ⑩ ✅ THE REBASE ONTO THE DEPLOYED REF — CLEAN, AND THE SEQUENCING ARGUMENT

⭐⭐ **F6 WAS `NO-GO` BECAUSE *"the invariant kills the boot ~60 s UPSTREAM of `cnc_gtt_monitor`"* ⇒
🔑 FIX 1 REMOVES THAT GATE. It does not compete with F6 — IT IS F6's PRECONDITION.**

✅ **`git rebase --onto 645728d f963438` — NO CONFLICTS.** The prediction held: the only
`capital/fund_manager.py` delta between the deployed ref and the old base is **F6 D-3**
*(`_resolve_release_reservation_id`, ~`:1278`/`:1353`)*, clear of every Fix 1 hunk.
⚠️ **The rebase DROPS 29 commits** — F6 (`c39e799`) itself, and also `9fdfe41`'s *"refuse to run when
bash is the WSL stub"* test-env guard. ⭐ **That is the POINT (Fix 1 ships alone), but it is why the
gate's counts differ from the pre-rebase run and ⛔ must not be read as a regression.**
🔴 **⛔ NOT DECIDED HERE, and the evening decision is Rama's: Fix 1 alone first, then F6.**
