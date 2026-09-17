---
name: h1-fixed-dead-column-05jul
description: Wave 1 H-1 FIXED (order_placer dead-column broker_order_id→order_id) + the reusable schema-backed test harness now lives in tests/conftest.py. Read before Waves H-2/H-3/M-O1 or any schema-backed test work.
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 1, H-1 — FIXED (commit `168e70d`, on main, UNPUSHED; Rama pushes off-market).**

Root cause: `OrderPlacer._cancel_trade_resting_exits` (orders/order_placer.py:3609)
SELECTed a non-existent column `orders.broker_order_id`. Real orders PK is
`order_id` (the broker-assigned id, core/schema.sql:271); no migration adds
broker_order_id. sqlite raised OperationalError EVERY call; the `except` swallowed
it as a WARNING and returned → FIX-190 Bug E (cancel resting SL/TGT before an
emergency flatten) never ran → resting legs could survive a flatten = naked
reverse risk. Same class as the 01-Jul emergency-exit tag bug.

Fix (permanent, minimal): `SELECT order_id` + read `r["order_id"]` (3 tokens).
NOT caught/widened — the error was ELIMINATED. order_id IS the broker id passed to
adapter.cancel_order (codebase idiom: order_placer.py:701 `broker_order_id = row["order_id"]`).

Parity: SINGLE shared code path — `_emergency_market_exit` (mode-agnostic, same
orders table for paper+live) calls it once; NO paper/shadow duplicate of the query
in order_placer. One fix covers both modes.

⚠️ OUT-OF-SCOPE SURFACE (do NOT fix in H-1; flag for follow-up): there are THREE
`_cancel_trade_resting_exits`:
- orders/order_placer.py:3609 → FIXED here.
- capital/kill_switch.py:977 → **SAME dead-column bug** (`SELECT order_id, broker_order_id, leg` → OperationalError swallowed). HARD_KILL flatten path. NOT a paper duplicate — a separate method / separate finding, still broken. Needs its own fix wave.
- orders/structure_exit_manager.py:365 → already CORRECT (uses order_id; the model for the fix).

**REUSABLE SCHEMA-BACKED TEST HARNESS (built here; later waves reuse):**
Location: `tests/conftest.py` (tests/ is NOT a package, so it's fixtures, not an import module). Provides:
- `build_real_schema_db()` → fresh in-memory sqlite conn with REAL core/schema.sql applied (row_factory=Row).
- `real_schema_db` fixture → yields that connection.
- `real_schema_store` fixture → yields `RealSchemaStore` (thin StateStore-shaped fetch_all/fetch_one/transaction over the real-schema conn).
Point: a query naming a non-existent column FAILS as in prod — NEVER a mock schema / _MockStore. FK enforcement left OFF by default (sqlite default) so single-table tests need no parent chain; `PRAGMA foreign_keys=ON` per-test if needed. Two-DB analytics ATTACH can be added later if a path touches candles/system_metrics.

Test: `tests/unit/test_h1_cancel_resting_exits.py` — 2 tests. Proven RED against
broker_order_id (method never calls _cancel_broker_orders; log: "no such column:
broker_order_id" @order_placer.py:3627) → GREEN against order_id. Regression:
test_order_placer.py 123 passed; new file 2 passed. Env: PC python3.11, pytest 9.0.3.

Emergency-exit chain (H-1/H-2/H-3/M-O1) still IN PROGRESS — H-1 alone does NOT
close the emergency-exit risk. Deploy caveat (Wave 0a): live post-receive hook does
checkout only, no service restart; trading-system is inactive now so the NEXT start
picks up the fix; a running session would need a manual `systemctl restart`.

Related: [[full_repo_audit_04jul_pending]] · [[wave0a_watchers_healthy_05jul]] · [[fix_160_agy_cascade]] · [[t2_halt_investigation_reconciler_tag_bug_01jul]] · [[db_schema_v28_split]]
