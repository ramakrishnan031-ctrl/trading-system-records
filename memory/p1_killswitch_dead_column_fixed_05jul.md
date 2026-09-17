---
name: p1-killswitch-dead-column-fixed-05jul
description: "Wave 2 P1 FIXED — kill_switch:977 HARD_KILL _cancel_trade_resting_exits dead-column (broker_order_id→order_id, the H-1 twin). HARD_KILL flatten now cancels resting SL/TGT. Group-A still open."
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 2, P1 — FIXED (commit `7c4106b`, main, UNPUSHED). The H-1 twin on the HARD_KILL flatten path.**

Root cause (identical to H-1): `KillSwitch._cancel_trade_resting_exits` (capital/kill_switch.py:977,
called by `_exit_all_trades_indestructible` :1091) SELECTed the non-existent column
`orders.broker_order_id` (real PK is `order_id`, broker-assigned, schema.sql:271). sqlite raised
OperationalError every call; the except swallowed it → a HARD_KILL flatten NEVER cancelled the trade's
resting SL/TGT at the broker → they survived + could fill against a now-flat book (naked reverse; the
AEROENTER-orphan class this method exists to prevent).

Fix (mirror H-1 / structure_exit_manager): `SELECT order_id, leg` + cancel & finalize each leg by
`order_id` (order_id IS the broker id the adapter cancels). The old code split `boid`(broker id) vs
`oid`(order id) — same column; collapsed to order_id. No new except, no fallback.

977 is the ONLY dead-column SQL on this path: :1126/1128/1175/1245 are Python `.broker_order_id`
attribute access on order-result objects (legitimate).

Parity: single method, single caller (:1091), mode-agnostic orders query — HARD_KILL fires in both
PAPER+LIVE through this method; no paper duplicate. One fix both.

Test: `tests/unit/test_p1_killswitch_cancel_resting.py` (2, REUSES the H-1 `real_schema_store` harness +
real `KillSwitch._cancel_trade_resting_exits`): RED against broker_order_id (fetch_all raises → nothing
cancelled) → GREEN against order_id (SL_LIVE+TGT_LIVE cancelled by order_id). kill_switch module 49 pass.

Group-A HARD_KILL flatten STILL OPEN: H-4 (retry double-sell — stale full-qty re-fire) + H-5 (CNC/product
sweep → naked MIS short) + the Group-A validation remain. H-4 is next. H-12 (paper get_positions strips
qty sign) still BLOCKS a paper drill of the HARD_KILL reverse-flatten direction (Wave 3). Deploy caveat:
live post-receive = checkout only, no restart; trading-system inactive → next start picks it up.

Related: [[h1_fixed_dead_column_05jul]] · [[wave1_chain_validated_e2e_05jul]] · [[full_repo_audit_04jul_pending]] · [[live_day1_zombie_remediation]]
