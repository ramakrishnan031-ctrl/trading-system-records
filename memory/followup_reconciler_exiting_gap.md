---
name: followup_reconciler_exiting_gap
description: RESOLVED (Task 4, 19-Jun-2026) — order_reconciler now auto-resolves trades stuck in EXITING; gap was exposed by the 19-Jun incident
metadata:
  node_type: memory
  type: project
  originSessionId: 6c3b6780-736c-4396-9a65-be6d83862a10
---

**✅ RESOLVED — Task 4 (commit ed8b27a, pushed/deployed; activates next restart).**

**The gap (now closed):** `order_reconciler` had no handling for `EXITING` trades —
CHECK1/G5b only act on OPEN/PARTIAL/PENDING_FILL. After the [[fix_190_incident]]
HARD_KILL flatten set AEROENTER + THELEELA to EXITING (`kill_switch._mark_trade_exiting`)
but the process died mid-exit, the DB stayed EXITING while the broker was flat —
invisible to the reconciler, capital locked. The 19-Jun PM resume needed a **manual
EXITING→OPEN flip** before CHECK1 could finalize them.

**The fix:** new `_check_stuck_exiting` runs every reconcile cycle (startup via
`reconcile_once()` + every 15s) inside the broker-positions guard. For EXITING trades
older than `reconciler.stuck_exiting_timeout_minutes` (default **30**):
- **flat at broker → CHECK1 finalize** (CLOSED_MANUAL + release capital + cancel orphan
  SL/TGT). Enabled by widening `state_store.mark_trade_manually_closed` to accept EXITING
  (EXITING→CLOSED_MANUAL is a valid terminal transition) — no manual flip needed anymore.
- **still holding → revert EXITING→OPEN** (`state_store.revert_exiting_to_open`) + WARNING,
  so SL/TGT / EOD squareoff / an active kill switch's own flatten loop resumes management
  (the generalized form of the manual workaround).
- **fresh EXITING** (younger than the timeout = an exit legitimately in progress) is left
  alone; the normal fill path finalizes it.

Key design notes:
- New `state_store.get_stuck_exiting_trades(cutoff)` mirrors `get_all_open_trades`' JOIN so
  a stuck row feeds straight into CHECK1. Stuck = `updated_at <= now-timeout` (EXITING entry
  stamps `updated_at`; ISO-8601 IST sorts chronologically). `get_all_open_trades` itself was
  NOT widened (fund_manager rehydrate + many tests assume OPEN/PARTIAL only).
- **CHECK2 guard added**: a broker position whose only local record is an EXITING trade is
  ours mid-exit, NOT an orphan — else CHECK2 would mis-adopt a held EXITING position (its
  symbol isn't in the OPEN/PARTIAL `local_symbols` set) before `_check_stuck_exiting` runs.
- `EXITING→OPEN` added to the crash-test state-machine validator as a reconciler recovery
  transition.
- 6 tests (incident replay flat→CLOSED_MANUAL, fresh-not-touched, stale-held→OPEN, + 3 store
  helpers). Related: [[fix_190_incident]] · [[fix_186_orphan_leak]] · [[human_order_policy]]
