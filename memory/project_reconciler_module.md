---
name: Reconciler module built and locked (RC1-RC20, schema v6)
description: orders/order_reconciler.py + schema v6 reconciliation_log table + 5 new state_store helpers + OrderReconcilerConfig; 29+9+1 tests; 717 total
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
Module 25 build complete. All 717 cumulative tests green.

**Why:** G1 requires hybrid 15s periodic + event-driven reconciliation of local trade state vs broker; G5b requires crash-recovery SL placement; G3 Level 3 requires capital drift detection.

**How to apply:** OrderReconciler wires to adapter/fund_manager/kill_switch/notifier/bus. Start via reconciler.start() at system startup. reconcile_once() is public for testing and callable on demand.

## Files changed

- `orders/order_reconciler.py` (NEW): full reconciler; RC1-RC20
- `core/schema.sql`: added TABLE 13 reconciliation_log; schema v5->v6
- `core/state_store.py`: EXPECTED_SCHEMA_VERSION=6; 7 new methods:
    get_all_open_trades(), get_orders_for_trade(trade_id),
    get_sl_order_for_trade(trade_id), mark_trade_manually_closed(trade_id),
    get_pending_all_products(), insert_reconciliation_log(...)
- `core/config_loader.py`: added OrderReconcilerConfig + SystemConfig.order_reconciler field
- `config/system_config.yaml`: added order_reconciler: section
- `tests/unit/test_state_store.py`: 9 new tests (30->39); table count 12->13
- `tests/unit/test_config_loader.py`: 1 new test (27->28); OrderReconcilerConfig import
- `tests/unit/test_order_reconciler.py` (NEW): 29 tests
- `docs/locked_decisions.yaml`: added RC1-RC20 under order_reconciler_module; total_decisions 93->113

## Test counts (post-Module 25)

| Suite | Count |
|---|---|
| test_order_reconciler.py | 29 (NEW) |
| test_state_store.py | 39 (+9) |
| test_config_loader.py | 28 (+1) |
| Total cumulative | 717 across 29 suites |

## Key design decisions

- RC5: 6 checks: MANUAL_CLOSE, ORPHAN_ADOPTION, HEALTHY, PARTIAL_CLOSE, POSITION_GREW, ORPHAN_ORDER
- RC6: 3-tier: COSMETIC (HEALTHY, not logged) / RECOVERABLE / UNRECOVERABLE
- RC7: G5b crash-recovery SL: LTP vs sl_initial determines SL-M or MARKET exit
- RC8: G3 Level 3: adapter.get_margins().net vs fund_manager.get_snapshot().total
- RC12: per-cycle auth counter (not per-call); soft_kill after 3 consecutive auth-error cycles
- RC13: non-reentrant via Lock.acquire(blocking=False)
- RC18: G5b uses adapter.place_order() directly (no order_placer import); persisted via OrderManager.insert_order()
- MANUAL_CLOSE capital release: entry_actual_price as exit proxy (breakeven PnL = 0)
- broker_orders_fn=None: CHECK 6 skipped silently (adapter has no get_all_orders method)

## Deviations from spec

None. All RC decisions implemented as specified.
