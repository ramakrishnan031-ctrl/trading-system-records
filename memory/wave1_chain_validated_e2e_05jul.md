---
name: wave1-chain-validated-e2e-05jul
description: "Wave 1 emergency-exit chain (H-1/H-2/H-3/M-O1) VALIDATED end-to-end (test_emergency_exit_chain, PASS — the four fixes compose on the real flatten). Read before Wave 2."
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 1 emergency-exit chain VALIDATED end-to-end (commit `d8795fe`, tests-only, UNPUSHED). Result: PASS — the four fixes compose.**

Test: `tests/integration/test_emergency_exit_chain.py` (1) drives the REAL
`OrderPlacer._emergency_market_exit` for a LONG OPEN trade with resting SL+TGT and asserts, in
sequence on ONE flatten: (H-1) resting SL+TGT cancelled at broker BEFORE the flatten; (cap) flatten
is a FIX-181 marketable LIMIT not raw MARKET; (H-2) the exit fill drives the EXITING trade to CLOSED
immediately with `release_used` once at REAL non-zero costs + `PositionClosed` (not the ~30-min
costs=0.0 stuck-exiting fallback); (H-3) a stale exit-retry on the now-closed trade places NO second SL.

REAL: OrderPlacer, OrderManager, engine+LIMIT/CO protocols, StateStore over real core/schema.sql, real
CostCalculator (broker_costs.yaml), EventBus, and the close/cancel/retry/capped-limit methods.
SIMULATED (legit broker + capital seams): the broker adapter (records place/cancel IN ORDER, returns a
signed LONG position + a live LTP) + the fund manager (records release_used); order_monitor is a stub.

Load-bearing (proven, not vacuous): each assertion maps to a distinct fix and fails if reverted.
Verified concretely by ONE revert cycle on H-2 — the integration test FAILED at the close assertion
with the guard reverted, then restored via `git checkout` (commit stayed tests-only).

H-12-independent: direction resolved from an injected correctly-signed LONG position (net +qty→SELL),
NOT the real paper adapter (get_positions strips the sign = H-12). A LONG is unambiguous either way; a
PAPER DRILL of the SHORT reverse-flatten direction still waits for H-12 (Wave 3).

Nuance (observation, NOT a defect): the OrderPlacer emergency-exit cap is fed by `_fetch_ltp` →
`get_quote_raw`, which returns {} in the REAL paper adapter → MARKET in paper (harmless: no real
slippage in paper). The test supplies a live LTP (LIVE-representative) to validate the LIMIT branch.
M-O1's reconciler-flatten cap (get_quote) works in paper via the quote_provider. Pre-existing parity
nuance, not a Wave-1 regression.

Optional reconciler-flatten (M-O1) integration scenario: DEFERRED (M-O1 already has its own unit test
`test_mo1_flatten_quote_key`; separate path). Full affected suite: 230 passed. Residual risks unchanged
from the Part-B chain review: twin `kill_switch.py:977` (HARD_KILL H-1-class bug), H-4/H-5 (Wave 2),
H-12 (Wave 3), H-3 TOCTOU, M-O3 (exit-retry no time-based escalation).

Related: [[mo1_fixed_flatten_quote_key_05jul]] · [[h1_fixed_dead_column_05jul]] · [[h2_fixed_exiting_close_05jul]] · [[h3_fixed_exit_retry_guard_05jul]] · [[full_repo_audit_04jul_pending]]
