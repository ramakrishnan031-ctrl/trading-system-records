---
name: BL-9 / B.3 invariant -> hard_kill landed green
description: Phase B.3 complete; FundManager.kill_switch injection; _check_invariant fires hard_kill before raise; 1524 tests
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# BL-9 landed (commit ca286cf, 19-Apr-2026)

**Fact:** CapitalInvariantViolation in any FundManager mutation path
(reserve, release, commit_to_used, release_used) now triggers
kill_switch.hard_kill BEFORE firing the legacy on_critical_failure
callback and BEFORE the exception propagates. α-direct pattern:
kill_switch is an explicit optional constructor dependency, not a
callback indirection.

**Why:** Pre-BL-9, invariant violations propagated as exceptions but
no kill wiring fired -- a provably corrupted bin-card state could
leave in-flight orders uncancelled. On-critical-failure callback
existed but in production was not wired for FundManager (only
live_feed used it), and even where wired it routed to soft_kill
which only blocks NEW trades rather than cancelling existing ones.
Accounting corruption is exactly the scenario hard_kill exists for.

**How to apply:** If a future task adds a new mutation path that
calls _check_invariant, the hard_kill wiring is automatic -- no
additional plumbing needed. If touching _check_invariant itself:
- Order is load-bearing: hard_kill FIRST (time-critical), on_critical
  SECOND (preserves legacy wiring), raise LAST (callers always see
  CapitalInvariantViolation).
- hard_kill is wrapped in try/except so the invariant exception
  always propagates even if the kill engine itself is broken
  (belt-and-braces). Do NOT remove this inner try/except without
  a matching regression test.
- on_critical_failure callback is ALSO wrapped in try/except for
  the same reason (preserves the promise that callers always see
  the invariant exception, not a callback failure).
- kill_switch=None is a supported config (existing tests, lightweight
  fixtures). Do not make it required without auditing every
  FundManager() construction site.
- TYPE_CHECKING import of KillSwitch keeps capital.fund_manager
  free of runtime coupling to capital.kill_switch; no circular
  import today but defensive.

**Exit code fix bundled:** main.py rehydrate CapitalStateInconsistent
path now returns 3 (was 2). Rationale: 2 is reserved for the
generic unexpected-exception path (sys.exit(2) in __main__); 3 is
the distinct "startup check failure" semantic. B.2 used wrong code;
fixed as part of B.3 commit.

**Test count:** 1517 -> 1524 (7 new, all in tests/unit/test_fund_manager.py).
Phase A integration gate (test_long_happy_path_full_lifecycle_capital_accounting)
still green.

**Zero fixture churn:** kill_switch=Optional[KillSwitch]=None means
all existing FundManager() construction sites (11 files incl. 6 test
files) continue unchanged. Only _make_fm helper in test_fund_manager.py
extended with optional kill_switch kwarg.

**Pre-work surprise:** Initial pre-work report claimed on_critical_failure
was already wired for FundManager via main.py L921. That was wrong -- L921
wires the callback for live_feed, not fund_manager. In production pre-B.3,
FundManager had NO kill wiring of any kind on invariant violation. Does
not change the implementation (Option α-direct is still the right call;
the regression-guard test still makes sense because it locks the behavior
that BOTH callbacks fire WHEN both are provided), but worth noting that
BL-9 is the FIRST kill wiring for capital-invariant violations, not an
upgrade from soft to hard.

**Next:** B.4 (BL-2 CapitalDriftDetected subscriber). Smaller still.
