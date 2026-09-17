---
name: BL-8 / C.2 atomic persist + broker cleanup landed (19-Apr-2026, commit da8fc90)
description: _persist_entry_orders now atomic and propagating; cancel-on-failure + hard_kill on DB-persist-after-broker-success; CoPlusTgt soft-fail cancels CO; 1571 green
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# BL-8 / Phase C.2 Closeout — 19-Apr-2026

**Commit:** `da8fc90`  
**Test count:** 1562 → 1571 green (+9). Phase A integration gate
(15/15, incl. A.3.g LONG+SHORT lifecycle) still green.

## What BL-8 closes

Three failure windows OrderPlacer used to leave to the reconciler:

1. Broker accepted orders, DB write failed — **silent swallow**
   ("reconciler will rebuild") is the exact anti-pattern the audit
   called out. Post-BL-8 the placer cancels the broker orders it
   just placed, releases the reservation, and fires hard_kill.
2. Mid-sequence DB failure — `_persist_entry_orders` used to call
   `insert_order` three times, each in its own transaction. Now
   `OrderManager.insert_orders_atomic(trade_id, specs)` wraps all
   rows in one `state_store.transaction()`. All-or-nothing.
3. CoPlusTgt TGT-fail-CO-live — used to leave CO orphaned and rely
   on reconciler to pick it up. Now OrderPlacer cancels the CO via
   the same `_handle_placement_failure(broker_order_ids=...)` path.

## Architectural locks (BL-8)

- **OMgr11 — `OrderManager.insert_orders_atomic(trade_id, specs)`:**
  Accepts a `Sequence[OrderInsertSpec]` (new `@dataclass(frozen=True)`);
  one `state_store.transaction()` for the whole batch. Empty list is a
  no-op. Nested transactions are NOT supported per StateStore docstring
  — callers MUST NOT wrap this method in their own transaction block.

- **OP-BL8a/b — `_persist_entry_orders` is atomic + propagates:**
  Builds spec list from `EntryResult` fields (ENTRY for both protocols;
  SL only for LIMIT_TRIPLE; TGT for both when present), hands it to
  `insert_orders_atomic`. **No try/except.** Exceptions bubble to
  `place()` which handles cleanup.

- **OP-BL8c — `_handle_placement_failure(broker_order_ids=())`:**
  Single cleanup orchestrator. New optional Iterable parameter.
  Cancel-first (if non-empty) then FAILED → release_reservation. Each
  step has its own try/except; all are best-effort.

- **OP-BL8d — `_cancel_broker_orders(ids, reason)`:**
  Iterates IDs, calls `adapter.cancel_order` (reached through the
  engine's protocol instances — both share the same adapter). On
  `CancelResult.success=False` OR unexpected exception, logs CRITICAL
  with the grep-friendly tag
  `CANCEL_FAILED_MANUAL_INTERVENTION_REQUIRED` and continues to next
  ID. Never raises. If the adapter is unreachable (pathological),
  still logs CRITICAL with the tag so no cancel-failure is silent.

- **OP-BL8e — hard_kill boundary (scope lock):**
  `kill_switch.hard_kill` fires ONLY on DB-persist-after-broker-success
  — the only path where capital tracking has actually broken (orders
  live at broker, no DB rows). Belt-and-braces around the kill call
  (logs CRITICAL `hard_kill_failed` if kill itself throws). **Does
  NOT fire** on:
    - Protocol `BrokerError` (protocol did its own cleanup; capital
      tracking intact — no orders accepted)
    - CoPlusTgt soft-fail (CO cancelled by OrderPlacer before FAILED;
      capital tracking intact after cleanup)
  Locked by `test_protocol_reject_only_does_not_fire_hard_kill`.

- **OP-BL8f — CoPlusTgt soft-fail cancels CO:**
  `OrderPlacer.place()` collects the `entry_broker_order_id` from
  `result` on `success=False` and passes it to
  `_handle_placement_failure(broker_order_ids=...)`. `CoPlusTgtProtocol`
  docstring and inline comment updated: reconciler is backstop, not
  primary. MED #13 reference retained as history.

## Adapter contract confirmed

`ZerodhaAdapter.cancel_order(broker_order_id: str) -> CancelResult`
never raises. Catches broker exceptions and returns
`CancelResult(success=False, reason=str(exc))`. Paper-mode path
short-circuits to `success=True`. OP-BL8d treats `success=False` AND
unexpected Python exceptions identically (CRITICAL log + continue).

## Pre-work wins worth remembering

- **Pre-existing protocol cleanup was better than spec assumed.**
  `LimitTripleProtocol` already cancels ENTRY on SL-fail internally
  (OPL3). `CoPlusTgtProtocol` already returned `success=False` with
  the live CO id surfaced via `entry_broker_order_id`. The "protocol
  refactor" scope the spec worried about was ~0 lines — the protocols
  gave us the hooks we needed.
- **Swallow-dependent tests: 0.** No tests referenced
  `persist_orders_failed` log or mocked `insert_order` to raise. The
  swallow was the "fail safe" for a scenario that shouldn't happen —
  exactly the silent-failure mode BL-8 closes.
- **`insert_order` opens its own nested transaction** — so atomicity
  required a dedicated batch method (`insert_orders_atomic`), not a
  wrapping context manager at the call site. StateStore explicitly
  forbids nesting.

## Files touched

- `orders/order_manager.py` — `OrderInsertSpec` dataclass + OMgr11
  `insert_orders_atomic`
- `orders/order_placer.py` — OP-BL8a–f locks; rewritten
  `_persist_entry_orders`, `_handle_placement_failure`,
  new `_cancel_broker_orders`; `place()` now wraps `_persist_entry_orders`
  with cleanup + hard_kill orchestration; soft-fail passes broker IDs
- `orders/order_protocol_co.py` — OPC4 docstring + TGT-fail inline
  comment rewritten (reconciler backstop language)
- `tests/unit/test_order_placer.py` — +9 tests (`TestBl8AtomicPersist`);
  new `_AdapterCancelFails` and `_RecordingKillSwitch` mocks;
  standalone runner extended

## Next

**C.3 / BL-11** — `live_feed._on_connect` must re-subscribe to all
previously-tracked tokens on reconnect. Small. Phase C closeout
(mempalace persistence) lands in C.3.
