---
name: bug_b_daily_cap_race
description: Bug B — reservation-aware DAILY_TRADES cap closes the daily-cap burst race (18-Jun 8-vs-5 overshoot); extends FIX-185
metadata: 
  node_type: memory
  type: project
  originSessionId: fdfc0dce-640b-4e4c-b2f4-1424f338ed1f
---

Bug B FULLY fixed 2026-06-19 (commit 9cf944d, pushed/deployed; activates next restart).

**The prior "B already correct via FIX-181 + FIX-185" audit was half-wrong.** FIX-181
fixed *what* counts (FAILED/CANCELLED excluded → retry) and FIX-190 added funnel
metrics, but the `DAILY_TRADES` check in `capital/risk_engine.py` was still a bare
`count_trades_today` DB read with **no in-flight accounting** — the daily-cap twin of
the position-cap TOCTOU race that FIX-185 closed for `OPEN_POSITIONS`. `approve()` reads
`daily_count` inside `portfolio_lock`, but the candidate's `PENDING_FILL` trade row is
inserted later by `order_placer.place()` **outside** the lock, so a burst all read the
same pre-burst count and passed → daily overshoot (the 18-Jun 8-vs-5).

**Rama's decision (asked, not assumed): extend the FIX-185 reservation pattern, NOT build
a new standalone `BrokerFilledCounter`.** Reuse the proven mechanism, single source of
truth, ~40-line change. (Rama had drafted a `BrokerFilledCounter` class but chose the
reuse path — avoids a second in-memory tally to re-sync on restart / midnight.)

Fix: `effective_daily = max(daily_count, count_settled_trades_today() + count_live_reservations())`,
reject if `>= max_daily`. `settled_today` = today's executed trades MINUS `PENDING_FILL`
(new `core/state_store.count_settled_trades_today()`); `live_reservations` = the in-flight
half (reserved-not-placed + PENDING_FILL). They partition with no double-count (commit
pops the reservation at fill); `daily_count` (incl. PENDING_FILL) is the restart floor.

Key facts learned:
- **`REJECTED` is NOT a valid `trades.status`** (schema CHECK allows PENDING_FILL/OPEN/
  PARTIAL/EXITING/CLOSED/CLOSED_MANUAL/CANCELLED/FAILED/UNKNOWN_IN_FLIGHT). Rejects are
  `FAILED`/`CANCELLED` or never get a trade row.
- The **"5→3 undershoot" was never a counting bug** — rejections already free the quota;
  the system just had no further signals (Chartink bursts are one-shot) and Bug G's
  per-symbol 5-min cooldown blocks same-symbol re-entry.
- 6 new tests in `test_risk_engine.py` (`test_bugb_*`) + 1 in `test_state_store.py`;
  346 green locally. Existing `test_daily_trades_at_limit` never actually hit `approve()`
  (fixed past date the engine never sees) — the new tests use `_TODAY`.

**Metrics gauges added (commit 70b5045):** `/metrics` now exposes `broker_in_flight` /
`broker_filled_today` / `broker_quota_used` / `broker_quota_max` / `broker_quota_available`
via `SignalProcessor.get_runtime_metrics()`, mirroring the gate exactly
(`used = max(daily_count, settled_today + count_live_reservations())`). Best-effort/guarded.

Related: [[bug_g_entry_throttle]] · [[live_test_mode_permanent]] · [[fix_190_incident]] · [[followup_reconciler_exiting_gap]]
