---
name: alert-remediation-branch-phase1-09aug
description: Branch fix/alert-remediation created off main; Phase 0 and Phase 1 committed there (a41422b, bfd6b5f), each separately gated. NOT pushed. Tick 1 is pending Rama's number and the base mix-up was mine.
metadata:
  node_type: memory
  type: project
---

# 🌿✅ `fix/alert-remediation` — **PHASE 0 + PHASE 1 COMMITTED LOCALLY.** ⛔ NOT PUSHED, ⛔ NOT DEPLOYED

**Branch created FROM `main` (`f963438`) in a SEPARATE GIT WORKTREE at `D:\Projects\trading-system-alertfix`** — ⭐ **the main worktree was never switched, so the entangled uncommitted sizing/funds-short work was never at risk.** venv is a **junction** to the main tree's; `config/instruments.csv` and `.env` staged in (both untracked).
✅ **`a41422b` PHASE 0** · ✅ **`bfd6b5f` PHASE 1**. 🔴 **Rama removes the worktree when done (`git worktree remove`); the branch and its commits live in the main repo's `.git` and survive removal.**

## ⚠️ MY SEQUENCING ERROR, RECORDED
I started the Phase-0 branch gate and then applied Phase 1 **while it was still running** ⇒ that run measured a MOVING TREE and is **⛔ not evidence for either state**. ⭐ **Killed and DELETED rather than reported.** The tree was then reverted to Phase-0-only, gated, committed; Phase 1 restored, gated, committed. **Two separate gates, one per commit** — which is what the card asked for and what I nearly spoiled.

## 📏 THE GATES — ⛔ NEVER THE WORD "CLEAN"
| | RC | result | set-compare |
|---|---|---|---|
| **Phase 0** (`a41422b`) | **`PYTEST_RC=1`** | **9 failed / 5,596 passed / 4 skipped**, 882 s | `NO REGRESSION DELTA — 9 known baseline failures, set-identical, 0 new, 0 disappeared` |
| **Phase 1** (`bfd6b5f`) | **`PYTEST_RC=1`** | **9 failed / 5,607 passed / 4 skipped**, 884 s | same, **and set-identical to the Phase-0 run on this branch** |

⭐ *"Clean" and "no new failures" are DIFFERENT CLAIMS — a future reader takes the first as zero.*
⭐ **Phase 1's arithmetic closes exactly: 5,596 + 11 = 5,607.** ⚠️ **Phase 0's does NOT close arithmetically and that is stated rather than papered over: this branch is off `main`, and no same-day `main`-baseline passed-count was measured** ⇒ **attribution is STRUCTURAL: only 2 tracked executable files differ from `main`, and all 5 files holding the 9 failures are BYTE-IDENTICAL to `main`.** 🕛 13:5x and 14:17 IST — ⛔ no midnight crossing.

## 🔑 PHASE 1 — THE BOUNDARY WAS TRACED, ⛔ NOT ASSUMED FROM PHASE 0
- **`live_feed._on_noreconnect`** — `_log.critical` → `_on_critical_failure(...)` → `kill_switch.soft_kill(...)` **ALL run before the notifier block**, and the callback itself calls `soft_kill` FIRST and only then notifies *(and logs its notifier failure rather than swallowing it)*. ⇒ **a notification failure cannot skip, delay or alter the SOFT_KILL.** ⭐ **Pinned by an ordering test** so a later edit cannot reverse it.
- **`main._start_eod_self_exit_thread`** — the DEFER is the **ABSENCE** of `shutdown_event.set()`, already decided by `_eod_self_exit_due(...)`; the alert only reports it. ⚠️ **The swallow matters here for a SECOND reason and still does: an escaping exception would kill the `eod-self-exit` THREAD and the service would then never self-exit at all.**
- ⭐ **Neither swallow encloses any part of an action** ⇒ **not** the larger finding the card told me to stop and report on.
- ⭐ **`suppressed` stays strictly *"no delivery was attempted"*** — a raise is `failed`, ⛔ never `suppressed`; pinned by test. **Return value ignored at both sites, and a test FORBIDS branching on it** so nobody can later write `if not send_alert_recorded(...): abort`.
- ✅ **RED-first: 5F/6P → 11P.** ⭐ **The 6 pre-existing passes are MUST-NOT-CHANGE GUARDS** (ordering · scope · vocabulary) on properties that already held — ⛔ **not holes, and they must not be deleted as *"already green and irrelevant"***; the same label applies to Phase 0's single pre-existing pass, the one asserting the kill decision stays outside the swallow.
- ⚠️ **PARITY, per test:** both sites need a failure the paper broker may not naturally produce (a websocket that exhausts every reconnect; a book still open past the EOD window) ⇒ **every test SIMULATES it**, both modes where the site allows. ⛔ **A green paper run is NOT evidence that paper reaches these branches in production** — and that wording must not weaken later.

## ⛔ EXCLUSIONS, EACH PINNED BY A TEST
`live_feed`'s reconnect + off-hours-idle alerts · `main`'s **EOD CLEAN shutdown** alert · `alert_watcher:399` · the other ten swallows · `N9-14` · the five stamp-before-send limiters · all four policy ticks. ⭐ **Similarity is not scope.**

## 🌿 TWO BUILDS, TWO HOMES — unchanged and honoured
The **funds-short** build (`fund_manager.py`, `signal_processor.py`, `test_funds_short_alert.py`) stayed in the ORIGINAL worktree on `feat/delivery-config-split`: those two files **DIFFER** between `main` and `HEAD`, so it belongs on the sizing branch. ⛔ **It was not bundled and not committed.**

See also [[alert-delivery-contract-phase0-09aug]] · [[alert-delivery-sweep-09aug]] · [[tick1-threshold-base-mixup-09aug]]
