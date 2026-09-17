---
name: Naive IST timestamp construction in tests
description: Correct pattern for constructing naive IST wall-clock datetimes in tests — avoids double-shift bug
type: feedback
originSessionId: 18d412a9-eda0-4a29-89ce-792433d13f2b
---
Use `now_ist().replace(tzinfo=None)` to produce a naive IST wall-clock datetime in tests.

Do NOT use `datetime.now() + timedelta(hours=5, minutes=30)` — `datetime.now()` returns local time (which may already be IST or UTC depending on the machine), so adding 5h30m double-shifts the timestamp.

**Why:** Caught during test_naive_broker_timestamp_treated_as_ist in time_authority tests. Module source was correct; test was constructing a semantically wrong input. The fix was test-only.

**How to apply:** Any test that needs to simulate a naive IST timestamp (e.g. broker API returning tz-unaware datetimes) should strip tzinfo from a real IST-aware datetime, not add an offset to `datetime.now()`.
