---
name: h2-fixed-exiting-close-05jul
description: Wave 1 H-2 FIXED (close_trade now accepts EXITING → an emergency-exit fill closes+releases immediately with real costs). Read before H-3/M-O1 or any emergency-exit / close_trade work.
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 1, H-2 — FIXED (commit `5549fc7`, on main, UNPUSHED; Rama pushes off-market).**

Root cause: an emergency-exit fill for a trade in the transitional EXITING state
could never cleanly close it. `_emergency_market_exit` marks EXITING, then the exit
fill hits `OrderPlacer._handle_exit_fill → OrderManager.close_trade`, whose guard
accepted only OPEN/PARTIAL and RAISED for EXITING. `_handle_exit_fill` caught it as
`exit_fill_already_closed` (order_placer.py:2211-2217) and early-returned → skipped
`_cancel_oco_siblings`, `release_used`, `PositionClosed`, cost/PnL recording.
Finalized only ~30 min later by the reconciler `_check_stuck_exiting` fallback with
costs=0.0 (capital locked, realized loss invisible to BOTH daily-loss mechanisms +
dropped from the B-1 unrealized set, resting siblings live). Designed-in on EVERY
emergency exit that fills, not a race.

Fix (option a, minimal): `orders/order_manager.py::close_trade` guard
`("OPEN","PARTIAL")` → `("OPEN","PARTIAL","EXITING")`. EXITING is TRANSITIONAL
(core/schema.sql:155 — "before the fill handler / reconciler closes the row"), so the
fill is meant to close it. Chose (a) over (b) because close_trade has a SINGLE
production caller (`_handle_exit_fill` — the ONLY `.close_trade(` in prod; the rest are
tests), so the guard is NOT shared → one token + comment, no `_handle_exit_fill`
restructure, and (b) can't complete the close without also relaxing close_trade.
Terminal states (CLOSED/CLOSED_MANUAL/FAILED/CANCELLED/REJECTED*/PENDING*) still raise
→ double-close preserved. Reconciler EXITING-exclusion (THELEELA double-sell guard)
untouched. `_handle_exit_fill` NOT changed (it already runs the full close+release
once close_trade succeeds).

Parity: emergency-exit fill path is mode-agnostic (paper synth + live both dispatch to
the same `_handle_exit_fill`/`close_trade`; only the adapter differs). No paper-specific
duplicate of the fill handler or close logic. One fix covers both.

Test: `tests/unit/test_h2_exiting_close_release.py` (2) — REUSED the H-1 harness
(`tests/conftest.py` `real_schema_store` / RealSchemaStore) + a real OrderManager + the
real `_handle_exit_fill` via a duck-typed OrderPlacer self (recorders for
fm.release_used / _cancel_oco_siblings / PositionClosed; real store + real close path).
Test 1 RED (trade stays EXITING, release not called; log `order_placer.py:2213
exit_fill_already_closed`) → GREEN (CLOSED + release + OCO + PositionClosed + real
charges 25.0, NOT 0.0). Test 2 (CLOSED duplicate fill early-returns, no double-release)
passes both ways. Regression: order_placer + order_manager = 133 passed. NB: the
harness leaves FK OFF but CHECK/NOT NULL ARE enforced — my first insert correctly
failed on missing NOT NULL order_protocol/updated_at (the harness caught it).

Emergency-exit chain: **H-1✓ H-2✓ — H-3 + M-O1 STILL OPEN** (do NOT declare the area
fixed). Also open: twin dead-column `kill_switch.py:977`; H-12 paper qty-sign parity
(Wave 3). Deploy caveat (Wave 0a): live post-receive = checkout only, NO restart;
trading-system inactive now → next start picks it up; a running session needs a manual
`systemctl restart`.

Related: [[h1_fixed_dead_column_05jul]] · [[full_repo_audit_04jul_pending]] · [[wave0a_watchers_healthy_05jul]] · [[d1_close_trade_race_design_03jul]] · [[capital_operational_note]]
