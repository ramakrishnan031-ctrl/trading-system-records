---
name: PHASE C COMPLETE (19-Apr-2026, commit de22a04)
description: Three-commit error-path hardening chain landed — BL-4 capital hard_kill + BL-8 atomic persist + BL-11 live_feed reconnect; 1576 green
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# PHASE C COMPLETE — 19-Apr-2026

**Final commit:** `de22a04` (BL-11)
**Commit chain:**
  - `fa5c6c9` — BL-4 capital.commit_to_used → hard_kill + re-raise
  - `da8fc90` — BL-8 _persist_entry_orders atomic + cancel broker orders on failure
  - `de22a04` — BL-11 live_feed._on_connect re-subscribe wrapped in try/except
**Test count:** 1554 → 1576 green (+22). Phase A integration gate
(15/15, incl. A.3.g LONG+SHORT lifecycle) still green.

## Phase C closed three silent-failure classes

All three are places where a downstream error used to disappear into
a log line while capital/broker state drifted from truth:

1. **BL-4** — `FundManager.commit_to_used` failure during entry
   placement. Pre-BL-4: failure was caught + logged; broker orders
   remained live with no capital commitment. Post-BL-4: hard_kill
   fires (positions visible, trading halted) before exception
   propagates.
2. **BL-8** — `_persist_entry_orders` mid-sequence failure. Pre-BL-8:
   three separate INSERT transactions; a failure on row 2 or 3 left
   the broker orders live with a partial DB state and a silent swallow
   ("reconciler will rebuild"). Post-BL-8: single atomic transaction
   via `OrderManager.insert_orders_atomic`; on failure OrderPlacer
   cancels broker orders and fires hard_kill (DB-broker split is
   the one path where capital tracking is genuinely broken).
3. **BL-11** — `_on_connect` re-subscribe failure on reconnect.
   Pre-BL-11: bare `ws.subscribe` / `ws.set_mode`; a broker rejection
   propagated into the kiteconnect ticker thread, crashing it and
   leaving the feed silently dead. Post-BL-11: wrapped in try/except,
   grep-friendly CRITICAL tag, next reconnect cycle retries.

## Phase C architectural locks (snapshot)

### BL-4 (commit_to_used → hard_kill)
- `capital/fund_manager.commit_to_used` catches the state_store
  exception, fires `kill_switch.hard_kill(...)` (best-effort try/except
  around the kill itself), then re-raises the original exception so
  OrderPlacer's cleanup path runs.
- α-direct DI: `Optional[KillSwitch] = None` — fund_manager remains
  instantiable without a kill switch (tests, preflight, bootstrap).
- Exit code on kill propagates as 3 (was 2 before B.3).

### BL-8 (atomic persist + broker cancel)
- **OMgr11** — `OrderManager.insert_orders_atomic(trade_id, specs)`:
  `Sequence[OrderInsertSpec]`, one `state_store.transaction()` for
  the whole batch. Empty list = no-op. **Cannot be nested** (StateStore
  forbids nested transactions).
- **OP-BL8a/b** — `_persist_entry_orders` atomic + propagates. No
  try/except inside; exceptions bubble to `place()`.
- **OP-BL8c** — `_handle_placement_failure(broker_order_ids=())` is
  the single cleanup orchestrator. Optional Iterable param; cancel
  first (if non-empty), then FAILED → release_reservation. Each step
  independently try/except'd; all best-effort.
- **OP-BL8d** — `_cancel_broker_orders(ids, reason)` iterates IDs,
  calls `adapter.cancel_order`. On `CancelResult.success=False` OR
  unexpected exception: CRITICAL with grep tag
  `CANCEL_FAILED_MANUAL_INTERVENTION_REQUIRED`. Never raises.
- **OP-BL8e** — hard_kill boundary (SCOPE LOCK): fires ONLY on
  DB-persist-after-broker-success. Does NOT fire on protocol
  `BrokerError` (protocol cleanup intact) or CoPlusTgt soft-fail
  (OrderPlacer cancels CO before FAILED). Locked by
  `test_protocol_reject_only_does_not_fire_hard_kill`.
- **OP-BL8f** — CoPlusTgt soft-fail cancels CO: `OrderPlacer.place()`
  surfaces `entry_broker_order_id` on `success=False` and passes it to
  `_handle_placement_failure(broker_order_ids=...)`. Reconciler is
  backstop, not primary.

### BL-11 (live_feed reconnect error handling)
- `_on_connect` wraps `ws.subscribe(tokens)` + `ws.set_mode(MODE_LTP, tokens)`
  in try/except.
- INFO log `re-subscribing to N tokens after connect` (grep-friendly
  token-count enumeration for incident triage).
- On failure: `log_exception` first (consistent with B.3/B.4/C.1/C.2
  cleanup-logging pattern), then CRITICAL with grep tag
  `re-subscribe after connect FAILED`.
- No manual retry loop — next `_on_connect` cycle retries. Feed is
  live at the socket level but carries no ticks until re-subscribe
  succeeds.

## Spec-discipline wins worth remembering

Two C-phase specs described mechanisms that were already in place or
didn't exist:

- **C.2 / BL-8 protocol refactor** — spec worried about ~100 LOC
  of protocol refactor scope. Reality: `LimitTripleProtocol` already
  cancels ENTRY on SL-fail (OPL3); `CoPlusTgtProtocol` already
  returned `success=False` with the live CO id in
  `entry_broker_order_id`. Protocol refactor scope: ~0 lines.
- **C.3 / BL-11 re-subscribe** — spec assumed `_on_connect` needed
  new re-subscribe logic. Reality: LF3/LF4 locks already tracked
  `_subscribed` and re-pushed on `_on_connect`. The real gap was
  narrower (error handling + logging).

Both cases: reported "spec says X, code does Y, here's the revised
scope" and got green-light to proceed with narrower change. Reinforced
rule: **when spec and code disagree, code wins.**

## EF-5 status

EF-5 (invariant check after rehydrate) — DEFERRED. B.2/BL-1 rehydrate
landed (commit `814fb23`); EF-5 is post-rehydrate invariant wiring
that was explicitly deferred in B.2 close out. Remains deferred; not
part of Phase C.

## Files touched (Phase C total)

- `capital/fund_manager.py` (BL-4)
- `orders/order_manager.py` (BL-8 — OrderInsertSpec + insert_orders_atomic)
- `orders/order_placer.py` (BL-8 — atomic persist, cleanup orchestrator,
  _cancel_broker_orders, hard_kill wiring)
- `orders/order_protocol_co.py` (BL-8 — OPC4 docstring + TGT-fail comment)
- `data/live_feed.py` (BL-11 — _on_connect try/except + logging)
- `tests/unit/test_fund_manager.py` (BL-4)
- `tests/unit/test_order_placer.py` (BL-8 — +9 tests; TestBl8AtomicPersist)
- `tests/unit/test_live_feed.py` (BL-11 — +5 tests)

## Next

**Phase D — BL-6 + BL-19 + BL-21** (per road-map). Rama kicks off.
