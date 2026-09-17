---
name: test_order_placer.py standalone runner was incomplete + had Windows encoding bug
description: Standalone __main__ runner only wired 29/36 tests; 16 print() calls used U+2192 arrow causing cp1252 failures on Windows
type: feedback
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
After module 22 build, `python tests/unit/test_order_placer.py` showed 19/29 — not 36/36.

Two defects (pre-existing, exposed during module 22 session):
1. `__main__` runner listed only 29 of 36 test methods — 7 tests from `TestKillSwitchLastMile`, `TestReservationRelease`, `TestEmptyBrokerOrderId` were missing.
2. 16 `print()` calls used `→` (U+2192) which Windows cp1252 terminal cannot encode → UnicodeEncodeError treated as test failure.

**Why:** These defects existed before module 22; they were never caught because the suite was previously only run with `python -m pytest` (not the standalone runner).

**How to apply:** When writing or auditing test standalone runners:
- Verify `__main__` lists ALL test methods (count must match `grep 'def test_' | wc`).
- All `print()` strings must be ASCII-only (no arrows, em-dashes, smart quotes, box-drawing chars).
- Run BOTH `python test_foo.py` and `python -m pytest test_foo.py` to confirm both paths green.
