---
name: alert-delivery-contract-phase0-09aug
description: "BUILT 09-Aug (uncommitted) — the alert delivery contract (alerts/delivery.py) applied to the two highest-consequence swallows. Invariant 1 kept, invariant 2 gained. Phases 1-5 recorded, not executed."
metadata: 
  node_type: memory
  type: project
  originSessionId: d9595f8a-8cb4-47fd-9b87-a97e7c891339
  modified: 2026-08-09T07:56:19.650Z
---

# 🔒📣 ALERT REMEDIATION — **PHASE 0** · `<BUILT 09-Aug · UNCOMMITTED · NOT PUSHED · NOT DEPLOYED>`

📜 **Rama, 09-Aug: *"Importantly start to fix everything ASAP."*** ⭐ **That authorises DEFECT REPAIR — code that does not do what it claims.** ⛔ **It does NOT authorise POLICY CHANGE** (thresholds, gate removals, retirements — those four are with Rama as ticks and this build pre-empts none of them).

## 🔑 THE INVARIANT — WRITTEN FIRST, THEN BUILT TO
> **① A trading safety action must NEVER depend on a notification succeeding.**
> **② A notification failure must ALWAYS remain observable.**

⭐⭐ **The codebase already satisfied ① — by SWALLOWING, which buys ① at the exact cost of ②.** ⛔ **Phase 0 does NOT remove a single swallow: the swallow is what protects the action.** ⭐ **It makes the swallow RECORD before it passes.**

## ⛔ WHY IT DID NOT START BY DEFINING `send_warning`
That repairs one symptom of a path with no delivery contract. ⭐ **The contract had to answer what happens when a VALID method RAISES**, not only when a missing one is called — and `N9-14` then becomes a trivial instance of a solved problem rather than a special case. **`N9-14` is untouched; it is PHASE 4.**

## 🔑 WHY THE RECORD IS CALLER-SIDE
`TelegramNotifier._audit_send` already writes `delivered`/`failed`/`suppressed` — ⛔ **but it lives INSIDE `send()`, so it can only witness a send that was ATTEMPTED.** A call that never REACHES `send()` (missing method, bad kwarg, swapped adapter) never reaches the audit line either. ⇒ **the record must sit one level up.** ⛔ **And it is a LOG, never an alert: raising an alert about a failed alert, on the channel that just failed, is circular.**

## WHAT WAS BUILT
- **`alerts/delivery.py`** *(new)* — `ALERT_OUTCOMES = ("delivered", "failed", "suppressed")` *(⛔ the SAME three words, no second vocabulary)* and `send_alert_recorded(notifier, log, …)`, which **never raises** and **always records**, event `alert_send_caller` *(⭐ same family as the notifier's `alert_send`, distinguishable suffix ⇒ one `grep` finds both and says which side wrote it)*. ⛔ **The recorder itself cannot raise (§1.3) — wrapped, with a wrapped fallback.**
- **TWO sites converted, ⛔ and only two:** `kill_switch._alert_exit_failed` *(HARD_KILL fired and a position could NOT be exited)* · `order_placer`'s emergency-exit alert *(SL failed permanently, emergency market exit placed)*. ⭐ The two where silence costs money and requires Rama to act.
- ⭐ **`send_alert_recorded`'s return value is IGNORED at both sites, deliberately — invariant ① made STRUCTURAL: there is no value a caller could branch on that would let a failed notification change what the system does.**
- ⭐ **A `None` notifier now records `suppressed`** — previously that case was invisible too.

## ✅ EVIDENCE
- **RED-FIRST, and the red is recorded: 13 failed / 1 passed BEFORE the implementation → 14 passed after.** ⭐ **The single pre-existing PASS is correct, ⛔ not a hole:** it is the must-not-change guard asserting that every exit/kill decision stays OUTSIDE the swallow — a property the 09-Aug trace had already established, so it must be green on the old code.
- ✅ **GATE: `PYTEST_RC=1` · 9 failed · 5,695 passed · 4 skipped · 917 s**, Git Bash, `pytest tests/unit tests/integration` *(⛔ never `run_tests.py`)*. ⭐ **SET-COMPARED: `comm` EMPTY BOTH WAYS** against the recorded 9. ⭐ **Passed arithmetic closes exactly: 5,681 + 14 = 5,695.** 🕛 finished 13:25 IST — ⛔ no midnight crossing.

## ⚠️ PARITY — STATED PER TEST, ⛔ NOT ASSUMED
**Both Phase-0 sites need a BROKER-SIDE failure to arise** (a position that will not flatten; an SL that will not place). ⛔ **Whether the PAPER broker can produce either is UNMEASURED.** ⇒ **every test is a SIMULATION** — the failed-trade list and the raising notifier are supplied directly — and the kill-switch tests are parameterised `PAPER`/`LIVE`. ⛔ **A green paper run is NOT evidence that paper reaches these branches in production, and the test file says so in its own docstring.**

## 🌿 WHERE IT LANDS — ⛔ NOT COMMITTED, and the measurement supports the choice
**(P) all three Phase-0 files are BYTE-IDENTICAL across `main`, `HEAD` and `origin/main`** *(`kill_switch fc2cd4ef` · `order_placer 64c156a5` · `telegram_notifier 6c53830e`)* ⇒ ⭐ **the patch transplants cleanly to a fresh branch off `main`, and the code being changed is exactly what is DEPLOYED.**
⛔ **NOT committed:** the worktree sits on `feat/delivery-config-split` (frozen sizing + schema v46) and a commit there joins the set Monday's gate line 9c must prove non-ancestor; committing to `main` is also forbidden; and switching branches with entangled uncommitted capital-path edits is its own hazard. 🔴 **Rama creates the branch.**
⚠️ **THE FUNDS-SHORT BUILD IS A DIFFERENT CASE and must NOT be bundled:** `capital/fund_manager.py` and `signals/signal_processor.py` **DIFFER** between `main` and `HEAD` ⇒ **that build belongs on the SIZING branch (or a branch off it), ⛔ not on the Phase-0 branch.** ⭐ Two builds, two homes.

## 📋 STAGING — ⛔ RECORDED, NOT EXECUTED (each is its own card, each waits for the previous to be OBSERVED)
**P1** feed death / SOFT_KILL · EOD shutdown deferred with positions open · **P2** `alert_watcher:399`, the one real propagation defect *(⭐ bounded — sentinels persist, next pass retries)* · **P3** the remaining ten swallows, ⛔ each classified deliberate vs accidental FIRST · **P4** `N9-14`, under this contract, ⛔ never as a bare method definition · **P5** the five stamp-before-send limiters as ONE change — ⭐ **including the day-long funds-short one, the longest window of the five.**
⚠️ **Turning several never-fired alerts on at once produces a wall of first-ever alerts on a trading day, and nobody would know which one to believe.**

See also [[alert-delivery-sweep-09aug]] · [[alert-pipeline-tag-funds-short-09aug]] · [[failfast-vs-degrade-discriminator-27jul]]
