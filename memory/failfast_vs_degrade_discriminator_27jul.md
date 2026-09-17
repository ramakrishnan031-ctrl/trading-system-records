---
name: failfast-vs-degrade-discriminator-27jul
description: "The rule for choosing fail-fast vs degrade-and-alarm: fail-fast when the failing condition can only arise from a deliberate act; degrade when it can arise from the environment. Answers #16a (BLOCK) and the S4 follow-up (DEGRADE) with opposite verdicts."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9cadf64c-e510-4d81-a606-31dcc47fea07
  modified: 2026-07-27T04:15:55.216Z
---

**⭐ THE DISCRIMINATOR — use this before answering any "should it block the boot or degrade?"**

> **Fail-fast when the failing condition can only arise from a DELIBERATE ACT.
> Degrade + alarm when it can arise from the ENVIRONMENT.**

**Why:** a fail-fast whose precondition is a deliberate act lands in front of the person who just
performed it, minutes later — cost ≈ 60 seconds. A fail-fast whose precondition is environmental
fires on an unattended 08:15 boot — cost = a trading day, and (S4, 17-Jul) behind an `exit 0` that
looks like a normal stop.

**How to apply:** ask *"what has to be true for this check to fail?"* If the answer contains a human
decision, BLOCK. If it contains someone else's uptime, a network, or a clock, DEGRADE — **but only
if something alarms**; degrading without an alarm is just a silent failure.

## Applied 27-Jul — same shape, OPPOSITE answers (the card assumed one answer for both)

- **#16a delivery-flag foot-gun → BLOCK.** `delivery_enabled` has been `false` since 15-Jun, so a
  rule preconditioned on `delivery_enabled=true` **cannot fire on an ordinary morning.**
- **S4 `_shutdown_event.set()` on a non-2xx `/health` → DEGRADE, log CRITICAL, keep booting.**
  ⭐ The safety argument, not convenience: the halt also kills **exit management, the reconciler and
  the 15:17 EOD squareoff**. The check exists only "to confirm Flask is listening", and no Flask
  means no new signals anyway ⇒ blocking converts *"no new entries, protection still running"* into
  *"nothing running at all."* 17-Jul's book was flat by luck. [[s4-boot-outage-17jul]]
  ⭐⭐ **The answer CHANGED because a prerequisite got built:** `liveness_probe` now runs
  `*/5 09-15 Mon-Fri` (verified in the live crontab 27-Jul). Degrading was wrong in July because
  nothing would have noticed; it is right now because something does.

## ⭐⭐ STANDING NOTE — a settled decision can go stale without anyone revisiting it

**A design answer can be correct when made and wrong later — or the reverse — because something
ELSE was built.** S4 is the worked example: *degrade* was the wrong answer in July because a silent
degraded boot would have gone unnoticed; it is the right answer now **only because `liveness_probe`
was built in between.** Nobody revisited the decision; the decision's ground moved.

**How to apply:** when a decision rests on "nothing would notice" / "nothing else covers this" /
"there is no way to detect it", **write the dependency down as part of the answer.** Then a later
session can see that building the missing piece REOPENS the question, instead of inheriting a
verdict whose premise has quietly expired. ⚠️ Sibling of [[feedback-verify-the-finding-premise]] —
there the premise was never checked; here it was true and then stopped being true.

## ⚠️ #16a's rule must be conditioned on the ACTIVE INTENT SET, not the flag pair

MEASURED at `capital/fund_manager.py:139-146`: with `conditional_enabled=TRUE` **and BOTH intents
active**, the function returns **the same config split as FALSE**. ⇒ a naive rule *"delivery_enabled
⇒ require conditional_allocation_enabled"* would **BLOCK `trade_type=BOTH`, a behaviourally
IDENTICAL and likeliest-production config.** Correct rule: BLOCK iff `delivery_enabled=true` AND
`conditional_allocation_enabled=false` AND the active set resolves **delivery-only**.
⭐ Machinery exists — `config_auditor._group_a_contradictions` already takes `strategies` (A4 does
`if strategies:`) and **already BLOCKs a delivery-flag contradiction (A1)**, so this is *which side
of an existing line*, not a new policy.

## ⭐ Sibling rule earned the same day: remove a trap, don't document it

**A documented trap must be remembered; a removed one cannot be fallen into.** The bit-rotted
`scripts/t2_cnc_gtt_realtest.py` (`23aca731…`) should be REPAIRED by merging `fix-t2-repair-07jul`,
**Tue 28-Jul evening** (after the v45 boot is clean, before the 29-Jul arm day) — not tonight, which
belongs to v45 alone. ⭐ **The reason to hold that branch back has EXPIRED**: it was
"live-validation-gated" and the same-day leg PASSED live 10-Jul; only a *flag on the same script* is
unproven. **Holding it back is now what creates the trap.** ⚠️ The sha256 check stays **step zero**
of the T2 day even after the merge. [[slice25-execution-plan-27jul]]
