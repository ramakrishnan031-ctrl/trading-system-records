---
name: feedback-verify-the-finding-premise
description: "An audit finding is a hypothesis, not a work order — verify its premise against live evidence BEFORE implementing the fix; on 17-Jul two of three batch items had wrong or incomplete premises."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8c00bd7-f7a4-4643-bf7d-9bab09ae2c49
  modified: 2026-07-19T05:30:22.169Z
---

**Before implementing any audit/queue item, verify the finding's PREMISE against live evidence.
A finding is a hypothesis, not a work order. Implementing a fix for a false premise creates
duplicate machinery and hides the truth.**

**Why:** on 17-Jul (BATCH-2, [[batch2-done-17jul]]) **two of three** items had defective premises,
and both defects were only visible by checking the live box rather than the repo:
- **ITEM 2 (§2.3 "logs unbounded, no retention") was entirely FALSE.** `log_cleanup` already
  existed, was in the live crontab, and worked. The audit's own strongest evidence — *"oldest log
  is ~30 days old"* — is the **signature of a working 30-day retention**, and it was read as proof
  of its absence. Building the requested prune would have duplicated a working mechanism.
- **ITEM 1 (§1.1 token leak) was UNDERCOUNTED by 41%.** The audit grepped for the *known `.env`
  value*; scanning by token **shape** found a second, older token (678 lines / 9 files) it was blind
  to. (It turned out 401-revoked, so severity held — but the purge scope changed 10 → 19 files.)
- A third: deleting the ITEM 3 file exposed that **FIX-065's guard had never been live**, something
  no one had noticed because its 12 tests assert against an inline mock.

**⭐ 17-Jul (later, [[s4-boot-outage-17jul]]) — THE STRONGEST INSTANCE, and a NEW VARIANT: a premise
that is literally TRUE but whose implied CAUSE is wrong.** The P3-s14 instruction opened with
*"System DOWN today; off-market gating waived; book flat"* — stated as harmless background. It was
**true**. But the author meant *the planned pause*, whereas the system was actually **shut down by
S4 at 08:16:09** and had taken **0 trades on a live trading day**. Verifying that throwaway line
against the VM — instead of accepting it, as every prior session had — is the **only** reason a live
outage was found at all; nothing else was alarming (the canary read `nrestarts: 0` = healthy).
**⇒ The dangerous premise is not the one you doubt, it is the one nobody thought to state as a
claim.** Ask "true for the reason you think?", not just "true?". Same day, P3-s14's own instruction
had **2 more** wrong premises (old response = 500 not 200; an immediate retry is IN_PROCESS not
DUPLICATE) — caught only by the RED-on-old run actually being executed and *read*.

**⭐⭐ 19-Jul — THE PATTERN NAMED, AND A PROCESS CHANGE (Rama's own words).** Briefs **inherit
premises from earlier reports and restate them as fact**. **Four briefs in four batches carried a
premise that measurement corrected**: the daily-report `3,098 → 0` (MISLABELLED, not miscounted) ·
the NTP tolerance sized by the ULP (the physical term is ~38x larger) · the consecutive-losses
collision (INVERTED — `DAILY_LOSS` is check 7, *after* `CONSECUTIVE_LOSSES` at 6, so it cannot
mask it) · the `_drive_close` loss figure (borrowed from the wrong helper: −9,000, not ~−1,000).
**⇒ Rama now marks inherited claims `INHERITED — UNVERIFIED`. CHECK THEM ANYWAY, regardless of
how they are labelled** — the label tells you what is load-bearing, not what is true.
**The 19-Jul census made this concrete: ALL THREE inherited claims were wrong in some part**
([[signal-mortality-census-19jul]]) — and the most instructive was the *~249/day silently-dropped
KeyError*, **carried as fact for weeks and never once measured**. It was **never silent** (it was
`ERROR` + full traceback, the noisiest line in the log), **not a separate killer** (same
`SKIPPED_QUOTE_UNAVAILABLE` as the claim next to it ⇒ adding them double-counts), and **already
fixed 14-Jul in `c22a25c`**. **A number repeated across reports acquires authority it never
earned.**
📌 **New sub-rule — DISTINGUISH THE COUNT FROM ITS INTERPRETATION.** Claim 1 that day had the
number **exactly right (63)** and its meaning **backwards**: "the system stopped pricing at 10:22"
was **survivorship bias from a status-selective retention prune**, and acceptance actually
*accelerated* after 10:22. **Verify the inference, not just the figure** — a correct number with a
wrong story is the harder error, because the number checks out.

**⭐⭐ 20-Aug — THE `WC-PATTERN`, NAMED: A REVIEWER ASSERTED A **MECHANISM** IT HAD NOT MEASURED — AND
THE NEW VARIANT IS THAT THE **CONCLUSION WAS RIGHT WHILE THE MECHANISM WAS WRONG.**** A ChatGPT
addendum reasoned that a broker-flat book might not self-exit *because* F6's
`orders/cnc_gtt_monitor.py:464` applies `abs(int(qty))`, making `held==0` unreachable. **The cited
line is real and present at the deployed SHA** — so the premise LOOKED verified. ⛔ **But the
self-exit never consults `cnc_gtt_monitor.held` at all:** `main._eod_self_exit_due` (`main.py:1109`)
reads `store.count_active_positions()` → `core/state_store.py:652-655` =
`SELECT COUNT(*) FROM trades WHERE status IN ('OPEN','PARTIAL','PENDING_FILL')` — **product-agnostic
DB row status.** F6 is real but sits on the **GTT-RELEASE** path. ⭐ **The conclusion SURVIVED for a
sharper reason: the stay-up gate is a DB ROW STATUS, ⛔ not the broker** — so a stuck row, or
`flatten_in_progress_fn()` returning True/raising (`main.py:1102-1107`, *“cannot confirm → stay
up”*), does it just as well as a carried CNC.
🔑 **THE STANDING RULE THIS SETS: source-verified measurement OVERRIDES reviewer reasoning, and a
cited line number is NOT a verified mechanism — a real line can sit on a path the conclusion never
travels.** ⛔ **Trace the call chain to the decision point; do not stop at “the cited code exists”.**
⚠️ **And do NOT discard the conclusion with the mechanism** — re-derive it; here it came back
stronger and more precisely stated.

**How to apply:**
0. **Verify the premises stated as BACKGROUND, not just the ones stated as findings** — especially
   about live state ("system is down", "book is flat", "nothing changed"). Cheap to check, and it
   is where the real surprises hide. If a stated fact is safety-relevant, confirm the *cause*.
1. **Reproduce the premise before writing the fix.** "No X exists" → look for X *on the live box*
   (crontab, systemd, running process), not just in the repo. The audit read the repo.
2. **Prefer shape/pattern scans over known-value scans** when hunting secrets or duplicates — a
   known-value grep only finds what you already knew about.
3. **When the premise is false, REFUSE the item and report the evidence.** Do not invent work to
   satisfy a checkbox; "no change needed, here's the proof" is a valid, valuable outcome.
4. Ask what the evidence *would* look like if the mechanism were working — then check for that.
   Sibling rule: [[feedback-verify-rc-not-output]] (a green check is evidence only if it could
   have been red). This one is its mirror: **a red finding is evidence only if its premise holds.**
