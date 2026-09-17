---
name: PHASE B COMPLETE (19-Apr-2026, commit 6d316c6)
description: Phase B capital-integrity chain done; 6 commits BL-5→BL-1→BL-9→BL-2→BL-3→BL-13; 1554 green; next Phase C error paths
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# Phase B Closeout — 19-Apr-2026

**Final commit:** `6d316c6` (BL-13 / B.6 shadow_tracker EOD restart guard)

**Test count:** 1554 green (1494 at Phase A exit → +60 across Phase B)

**Phase A gate:** 15/15 integration tests green, including A.3.g
full-lifecycle LONG+SHORT capital accounting.

## 6-Commit Chain

| # | Commit  | Item  | What it did                                                 |
|---|---------|-------|-------------------------------------------------------------|
| 1 | e28800c | BL-5  | `fm_ledger` becomes write-ahead; removed dead `capital_ledger` |
| 2 | 814fb23 | BL-1  | `FundManager.rehydrate_from_open_trades`; `_apply_*` refactor; `CapitalStateInconsistent`; EF-5 deferred |
| 3 | ca286cf | BL-9  | Invariant breach → `kill_switch.HARD_KILL`; α-direct DI; exit code 2→3; belt-and-braces |
| 4 | 59fc5fa | BL-2  | `CapitalDriftHandler` source-module filter; abs-₹ thresholds; consecutive-cycle escalation |
| 5 | 10ddf50 | BL-3  | `OrderReconciler._check7_capital_accounting_drift`; `source_module="fund_manager_self_check"` |
| 6 | 6d316c6 | BL-13 | `shadow_tracker` EOD guard persists across restart via `eod_squareoff_log` piggy-back |

## Architectural Locks (from Phase B)

- **Capital ledger:** `fm_ledger` is the single write-ahead source of
  truth for signed `margin_delta` per reservation. `capital_ledger` is
  gone. No entry_type filter on sums (RESERVE +m / RELEASE -m nets
  correctly; load-bearing docstring guards against regression).

- **FundManager rehydration:** On startup, FundManager walks
  `get_open_trades()` and replays reservations. `_apply_reserve` /
  `_apply_release` / `_apply_release_used` are split from public API so
  rehydration doesn't re-write ledger rows. Inconsistency ⇒
  `CapitalStateInconsistent` (non-swallowable).

- **Invariant → kill:** `CapitalInvariantBreach` escalates via
  `kill_switch.hard_kill()`. α-direct DI (`Optional[KillSwitch] = None`
  on FundManager and CapitalDriftHandler). Process exit code 3 on hard
  kill (was 2).

- **Drift source filter:** `CapitalDriftHandler._ESCALATING_SOURCES =
  frozenset({"fund_manager", "fund_manager_self_check"})`. Integer-qty
  deltas from CHECK5 etc. are NOISE/LOG_ONLY tier only. The two
  escalating sources SHARE the consecutive counter (concurrent drift
  on both is strictly worse). Regression-tested.

- **Accounting self-check (BL-3):** `OrderReconciler._check7` compares
  `fm._reservations[rid].margin` vs
  `StateStore.sum_fm_ledger_margin_delta(rid)` every cycle. Publishes
  `CapitalDriftDetected(source_module="fund_manager_self_check")` per
  drifting rid. Reuses `capital_drift_tolerance` (₹1).
  `FundManager.get_live_reservations()` returns full `_Reservation`
  objects (not just margins) under lock; shallow-copy for safe
  iteration.

- **Shadow-tracker EOD guard (BL-13):** `_eod_fired_date: Optional[str]`
  persists the firing date across restarts. On construction,
  `ShadowTracker` reads `eod_squareoff_log` row for today via
  `get_eod_squareoff_log_for_date(today_ist())` and restores
  `_eod_fired=True` if present. Top-of-handler guard
  (`_eod_fired_date == today_iso → skip`) is idempotent per IST date.
  Mark-before-fire ordering is enforced UPSTREAM in `eod_squareoff.py`
  (log row written before event published), so a restart that sees
  the row is guaranteed to have missed the event. Zero schema change.

## Deferred

- **EF-5 (orphan detection):** rids in `fm_ledger` but not in
  `fm._reservations`. Deferred to Phase E. Current BL-3 design is
  unidirectional (fm → ledger only).

## Pre-work discipline wins

- **BL-3:** Grep for `_reservations|def get_live` initially returned no
  matches (pattern quirk); confirmed file locations before
  implementation. Confirmed no entry_type filter needed on ledger sum.
- **BL-13:** The green-light spec described a shadow_tracker timer
  that doesn't exist. Pre-work revealed it's purely event-driven
  (`EodSquareoffComplete` subscriber); the real hole was the 13-min
  post-EOD-pre-close restart window. User approved the revised
  Option C design. User directive for future commits: "If specs
  describe non-existent mechanisms, keep doing this — report 'the
  spec says X but the code does Y; here's the revised design'."

## Next: Phase C

Error paths — BL-4, BL-8, BL-11. Three mechanical commits. No new
architectural territory; mostly tightening exception handling and
ensuring structured logs/alerts on known error modes.
