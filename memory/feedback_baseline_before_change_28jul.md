---
name: feedback-baseline-before-change-28jul
description: "ORDERING RULE — when a job's output is ALREADY in doubt, let it run UNCHANGED first to get a baseline, THEN deploy the change. One observation cannot separate two candidate causes. Proven 28-Jul-2026: the 18:45 EOD run was allowed to go first, on old code, and it CLOSED a suspect."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 58e849b5-81c5-4b96-89bc-182326b7fbbc
  modified: 2026-07-28T13:22:04.935Z
---

# ⏱️ LET THE BASELINE RUN FIRST — one observation cannot separate two candidate causes

⛔ **DO NOT add a check to a job that is already failing, or deploy into a job whose output is
already in doubt.** If the job then misbehaves you have **two candidate causes and one
observation**, and you cannot tell them apart. Run it UNCHANGED first, bank the baseline, then push.

**Why:** this is the confound the deploy calendar exists to prevent. It costs one cycle to avoid
and cannot be recovered after the fact — once the change is in, the clean observation is gone.

**How to apply:**
- Before deploying into any scheduled job, ask: *is this job's last run explained?* If **no**, let
  the next run go on the OLD code and treat it as the baseline.
- ⭐ The **absence** of the new thing in that baseline run is the **CONTROL** — check it is absent
  and say so. An unrun detector's missing section is evidence, not a failure.
- Confirm the job **FINISHED** (heartbeat/artifact), not merely started, before a deploy replaces
  its own source file.
- Timing is the weaker reason; **diagnosticity is the stronger one.** Say which one you are acting on.

**MEASURED 28-Jul-2026.** 27-Jul's `reports/system_manager/<date>.txt` never appeared (the v45
schema-refusal night), so *"is the 18:45 EOD job broken at all?"* was genuinely open while a new
11th check sat ready to push. A power-down moved the clock to 18:40, and the order was **reversed
deliberately**: 18:45 ran on old code → report **PRESENT** (4,242 B, `system_manager_eod SUCCESS
18:45:05`, `check_failed`=0) ⇒ **the job works, and 27-Jul's absence is explained by the schema
refusal ALONE** — a suspect eliminated, not merely set aside. Control held: **zero `STRAY` lines**,
because the detector was not deployed yet. Push followed at 18:46:19 (`ce08668`).

⭐ **Corollary that saved a false alarm the same night:** a threshold measured mid-day is not a
full-day threshold. The "5 errors and all explained" baseline was taken at 10:20 — before the
15:15 kill and the 17:35 shutdown — so a full-day census could **never** be 5. Classify against
**prior comparable days**, not against a number captured in a different window.
[[feedback-no-fixed-test-baseline]] [[feedback-verify-rc-not-output]] [[feedback-status-label-rule-27jul]]
