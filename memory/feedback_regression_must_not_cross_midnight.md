---
name: feedback-regression-must-not-cross-midnight
description: "A regression base/mine pair must not cross midnight — _TODAY is captured at collection time and compared against a date computed at execution time, so a run started after ~23:15 IST corrupts attribution silently."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 106a4d20-abb3-49c1-bdf3-ab5c0f4839d0
  modified: 2026-07-18T19:27:33.252Z
---

**"Base and mine in the SAME TIME WINDOW" is NECESSARY BUT NOT SUFFICIENT. Neither run may
cross midnight.** At ~15 min per full-suite run, **any regression started after ~23:15 IST is
unsafe.**

**Why:** several test modules capture the date at **module import (collection) time** —

```
tests/unit/test_risk_engine.py:49                        _TODAY = now_ist().date().isoformat()
tests/unit/test_phase3_delivery_caps_conditional_capital.py:35   _TODAY = now_ist().date().isoformat()
```

— while the engine under test computes the current date at **execution time**. A run that collects
on one date and executes on the next seeds trades the engine then reads as *yesterday's*, so
date-scoped tests fail for a reason that has nothing to do with the change being measured.

**How it presented (19-Jul-2026, the M-C1 batch).** MINE ran 23:30–23:56, BASE 23:57–00:13. The
comparison returned **both `comm` directions non-empty** — `test_risk_engine::test_consecutive_losses_at_limit`,
`test_bugb_restart_floor_via_pending_fill` and `test_daily_delivery_cap_rejects_6th` "failed in base
but passed in mine". **That is impossible for a test-only file addition**: a new test file cannot
make an unrelated unit test pass. The impossibility is what exposed the artefact — the numbers
themselves looked ordinary.

**What to do:** discard the pair and redo both runs inside one date. Redone Sun 00:15–00:44:
BASE 5017 vs MINE 5030, `comm` both directions EMPTY, zero attributable, `xfailed=1/XPASS=0`.

**Why this belongs with the masking rule.** Same family as the git-ignored `config/instruments.csv`
finding: an **environmental asymmetry that corrupts attribution SILENTLY instead of announcing
itself**. Neither produces an error; both produce a plausible-looking failure set. The defence is
the same — make the base and the comparison differ in *exactly one* variable, and treat any
impossible-shaped result as a harness fault before believing it about the code.

Fifth in the permanent-rule series in `docs/SYSTEM_MAP.md`, after *CONFIGURED IS NOT COVERED*,
*WIRED IS NOT REACHABLE*, [[feedback-live-vs-latent-findings]] and
[[feedback-never-classify-by-free-text]]. Sibling of [[verify-check-the-rc-not-the-output]] —
a green (or red) result is evidence only once you know what could have produced it.

Full context: [[q9-live-seed-mc1-wired-19jul]].
