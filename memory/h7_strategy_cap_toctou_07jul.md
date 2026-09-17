---
name: h7_strategy_cap_toctou_07jul
description: "Wave-5 H-7 FIXED (07-Jul, main-local 2023948, UNPUSHED) — per-strategy position cap moved INSIDE portfolio_lock (atomic check+reserve) + deduped 3 copies->1; counts open/partial + live strategy reservations (mirrors FIX-185). TOCTOU closed. 252 green, RED->GREEN proven."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a31a746-372a-4611-aae1-88d2cfaa183f
---

**Wave-5 H-7 FIXED — 07-Jul-2026, commit `2023948` on main (LOCAL, UNPUSHED; off-market push later).** The last Audit-A HIGH in scope. Closes the per-strategy position-cap TOCTOU from [[full-repo-audit-04jul-complete]] (finding H-7).

## Root cause
The per-strategy concurrent-position cap was checked OUTSIDE `fm.portfolio_lock`, counting only DB OPEN/PARTIAL with no in-flight/reservation compensation, and the block was **triplicated** across the 3 pipeline entry paths (`signal_processor._process_one` / `continue_from_gate` / `continue_from_retest`). A Chartink burst (one webhook -> N symbols -> up to `worker_count` workers on the SAME strategy) let every worker read the same stale count and all pass -> a cap of N blown (a live-money risk cap defeated in its exact target scenario).

## Fix (atomic + deduped; mirrors the global FIX-185 OPEN_POSITIONS pattern)
- **signals/signal_processor.py**: ONE `_enforce_strategy_position_cap(strategy_name, strategy_obj)`, called INSIDE `portfolio_lock` immediately before `reserve()` in all 3 paths (the 3 outside-lock copies removed). Authoritative count = strategy OPEN/PARTIAL (DB) + live fund_manager reservations, floored by the DB active count (incl. PENDING_FILL) so a restart-lost reservation is still caught, +1 for THIS candidate; reject if `> cap`. Each `reserve()` now passes `strategy=strategy_name`.
- **capital/fund_manager.py**: `_Reservation` carries `strategy`; `reserve()`/`_apply_reserve` thread it; new `count_live_reservations_for_strategy(strategy)` (per-strategy analog of `count_live_reservations`). Read under the existing `RLock` that `portfolio_lock` exposes -> a caller holding portfolio_lock re-acquires safely -> check+reserve is ONE atomic critical section (NO nested/second lock -> no deadlock). Optional `strategy=None` default -> recovery/replay reservations degrade gracefully (counted via the DB floor).

## Parity
Single shared path — both paper and live go through signal_processor + `fm.portfolio_lock` + `reserve()`. No paper-specific cap copy (confirmed; the 3 copies were all mode-agnostic). One fix covers both.

## Tests — `tests/unit/test_h7_strategy_cap_toctou.py` (real StateStore + real FundManager + real lock/reserve)
- **TOCTOU (RED->GREEN, genuine race)**: a 6-thread burst at cap=2 through the REAL critical section — RED = the reproduced old outside-lock pattern admits **>cap**; GREEN = the new inside-lock method admits **exactly cap**; + no-deadlock (all threads finish within timeout) + fm agreement (`count_live_reservations_for_strategy == cap`). `threading.Barrier` maximises contention; only the removed collaborators are mocked (the method reads only `_store`+`_fm`).
- dedup (source-asserted: 1 cap-check location, 3 routed calls, old query gone), normal cap behaviour, reservation-counts-toward-cap, strategy-scoped counting.
- Interface fidelity: `_MockFundManager` (test_signal_processor) + `_FM`/`_Store` (test_sr_v2_continue) raised to the new real interface (`strategy=` kwarg / `count_live_reservations_for_strategy` / aliased query columns). These were the only doubles lagging the real signature.
- **252 green** across capital/risk/signal-processor/integration; 0 regressions.

## Residual / next
- No deadlock (RLock, single critical section, bounded count) and no over-serialization: the cap check is 1 indexed DB read + 1 in-memory dict scan inside the already-held lock — the same critical section that already runs approve+reserve.
- Narrow residual: a reservation created then LOST across a restart before its order reached the broker (no DB row) is untagged on replay (strategy=None) -> uncounted per-strategy; the DB active floor + the global cap mitigate; extremely narrow window; documented, not fixed here.
- **H-6 (CNC exit-day dead-column) remains** — delivery-gated (only matters once delivery is enabled beyond shadow). Other Wave-5 items PENDING (NOT this task): terminal-state guard, FIX-067/M-S1, M-C1. SYSTEM_MAP H-7 changelog edit rides the next off-market doc sync (with the Wave-3/T2 doc edits).
