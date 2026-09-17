---
name: Process lock — test-count reporting must use pytest --co, never delta arithmetic
description: E.6 drift investigation root cause + binding rule for every future landing report
type: feedback
originSessionId: daf7a7d0-49f5-49f6-8f12-9791b8824592
---
**Rule:** Every landing report MUST include actual collected count from:

    venv/Scripts/python -m pytest --co -q 2>&1 | tail -1

Do NOT compute the landing count by adding "new tests" to the prior report's
number. Run `pytest --co` against the new commit, report what it says, match
the number to the commit body. No exceptions.

**Why:** On 2026-04-19 the E.6 drift investigation traced a +15 unexplained
test-count drift (1627→1645 with only +3 EF-2 tests) back to E.3 (commit
`27e40da`). E.3's landing report stated "1607 green (net −6 obsolete H-6
tests removed)." Neither half was true — no tests were removed, and 9 new
tests were added (all in `tests/unit/test_e3_hygiene.py`, legitimate H-6/
H-15/H-21/M-2 coverage). The absolute was miscomputed by −15.

E.4 and E.5 then inherited the wrong baseline by reporting deltas off the
wrong anchor. The deltas themselves were correct (E.4: +16, E.5: +4), but
the absolute counts stayed −15 low because nobody re-ran `pytest --co` and
re-anchored. E.6 finally broke the chain by reporting the actual collected
number (1645).

Three memory files (project_e3_hygiene.md, project_e4_event_loop_safety.md,
project_e5_cleanup.md) now carry correction blocks with the real counts:
1622 at E.3, 1638 at E.4, 1642 at E.5. No test or code change — just an
audit-trail correction.

**How to apply:**

- Before writing the commit body's "N tests green" line, run the command
  above and paste the number.
- If the number diverges from the pre-work prediction by more than ±3,
  STOP. Investigate before committing. Baseline corrections land in a
  standalone commit, not bundled with feature work.
- If the drift is legitimate (tests were genuinely added in an earlier
  commit and undercounted), file a correction note in that earlier
  commit's memory file. Do not silently adjust tests to match a wrong
  baseline.

**Tolerance:** ±3 around pre-work prediction. Anything wider is a STOP
condition — the same one listed in pre-work templates as the 6th stop.
