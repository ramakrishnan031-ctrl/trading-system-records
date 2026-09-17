---
name: BL-1 / B.2 rehydrate_from_open_trades landed green
description: Phase B.2 complete; FundManager replays fm_ledger+trades+orders on startup; 1517 tests
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# BL-1 landed (commit 814fb23, 19-Apr-2026)

**Fact:** FundManager.rehydrate_from_open_trades reconstructs in-memory capital
state at startup from the persistence triangle (fm_ledger + trades + orders).
Wired into main.py between initialize() and PositionSizer construction.

**Why:** Pre-B.2, a mid-day crash left fm_ledger with committed capital but
no way to rebuild in-memory state on restart. FM's _reservations dict, bucket
totals, and daily_pnl all re-initialized to zero -- traded capital was
"invisible" post-restart and daily_loss_limit checks were wrong in either
direction (ref: BL-1 green-light spec, decision b scenario).

**How to apply:** If a future task touches capital-state persistence or
adds new ledger row types, remember:
- _apply_reserve / _apply_release / _apply_commit are pure-mutation helpers
  shared by public methods AND rehydrate. Neither writes the ledger nor
  runs invariant. Public path writes ledger then applies then checks
  invariant; replay only applies.
- Invariant runs ONCE at end of rehydrate, never per-step.
- CapitalStateInconsistent (new, in core/exceptions.py) is the startup-
  replay failure signal; distinct from CapitalInvariantViolation which
  fires inside live mutations. main.py catches and exits with code 2.
- Decision L2: trades+orders join at replay, NOT pure ledger replay.
  Ledger stays minimal (capital transitions only). Position details
  (symbol/qty/price/intent) live in trades+orders.
- Intent mapping lives in module-level _PRODUCT_TO_INTENT dict.
- Phase 2 PnL carryover: ONLY today's RELEASE_USED rows. Applied as
  net lifecycle effect (bucket avail += pnl, _total += pnl,
  _daily_pnl += pnl); does NOT touch reserved/used (cancelled out).
- StateStore.get_all_open_trades now also returns qty_planned and
  entry_target_price (additive extension; reconciler callers unaffected).

**Deviations / known shortcuts:**
- EF-5 recorded: trades table lacks reservation_id column. Lookup is
  two-hop (signal_id -> fm_ledger.RESERVE -> reservation_id) via
  StateStore.get_reservation_id_for_signal. Works correctly; adding
  the column is a Phase E cleanup candidate.

**Test count:** 1503 -> 1517 (14 new, all in tests/unit/test_fund_manager.py).

**Next:** Phase B.3 (BL-9 invariant -> hard_kill) is a ~2-line wire-up;
switch VS Code Claude to Sonnet 4.6 from here on.
