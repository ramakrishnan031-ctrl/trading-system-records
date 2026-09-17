---
name: Orders module built and locked (OP1–OP11 + OP-LM1/LM2/LM3)
description: orders/ chain + last-mile gaps patched; 36 tests green; total suite 516
type: project
originSessionId: 0f807c82-d3bf-4ec9-9f97-c828b590c13d
---
Orders module chain built and locked (2026-04-15). Last-mile gaps patched (2026-04-16). All 516 tests pass.

Files:
- `orders/__init__.py`
- `orders/entry_engine.py` — `EntryEngine` ABC + `EntryResult` dataclass (EE1–EE5)
- `orders/order_manager.py` — DB CRUD for trades/orders via StateStore (OMgr1–OMgr9)
- `orders/order_protocol_limit.py` — `LimitTripleProtocol`: ENTRY+SL+TGT (OPL1–OPL6)
- `orders/order_protocol_co.py` — `CoPlusTgtProtocol`: CO + LIMIT TGT (OPC1–OPC7)
- `orders/full_entry_engine.py` — routes to CO or LIMIT_TRIPLE by protocol string (FEE1–FEE5)
- `orders/order_placer.py` — main orchestrator; `place()` called by signal_processor (OP1–OP11 + OP-LM1/LM2)
- `tests/unit/test_order_placer.py` — 36 tests (29 original + 7 for LM gaps)

Last-mile decisions (locked in locked_decisions.yaml under `orders_module`):
- OP-LM1: kill_switch.is_active("entry") checked in place() before engine.execute(); on active: FAILED + release + raise OrderRejectedError. KillSwitch injected at construction (Optional, default None).
- OP-LM2: Every failure path (BrokerError, soft failure, kill_switch abort) calls _handle_placement_failure() which does update_trade_status(FAILED) + fm.release(). ALREADY EXISTED in original build.
- OP-LM3: After each adapter.place_order() call in both protocol files: if not placed.broker_order_id → raise OrderRejectedError. Exception: CO_PLUS_TGT TGT empty ID = soft success (same as OPC4 TGT exception path).

Key design facts:
- `place(symbol, side, qty, entry_price, sl_price, intent, signal_id, reservation_id)` — no tgt_price from caller; computed internally as entry ± (entry−sl) × rr_ratio (default 2.0)
- Default protocol: LIMIT_TRIPLE
- `broker_order_id` is DB PK for orders table; `internal_order_id` stays in-memory only (_fill_map)
- `_fill_map: Dict[str, _FillEntry]` keyed by internal_order_id, guarded by threading.Lock (OP5, OP8)
- On fill: `fund_manager.commit_to_used(reservation_id, actual_fill_price, actual_qty)` + `record_entry_fill()`
- On broker failure: `update_trade_status(FAILED)` + `fund_manager.release(reservation_id)` (OP7/OP-LM2)
- EventBus method is `publish()`, not `dispatch()` or `emit()`

**Why:** OP-LM gaps closed per reconciliation session 2026-04-16. locked_decisions.yaml is authoritative; ad-hoc spec conflicts must be flagged, locked wins.

**How to apply:** signal_processor wires order_placer at construction — pass kill_switch instance. Next modules: order_monitor, order_timeout, smart_tgt_manager, eod_squareoff.
