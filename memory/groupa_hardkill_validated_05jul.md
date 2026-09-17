---
name: groupa-hardkill-validated-05jul
description: "Wave 2 Group-A HARD_KILL flatten VALIDATED end-to-end (test_hard_kill_flatten_chain, PASS — 977 + H-4 + H-5 compose). Group-A CLOSED. Next = H-10 (Group B)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 2 Group-A HARD_KILL flatten VALIDATED end-to-end (commit `af9e0a4`, tests-only, UNPUSHED). Result: PASS — 977 + H-4 + H-5 compose. Group-A CLOSED.**

Test: `tests/integration/test_hard_kill_flatten_chain.py` (1) drives the REAL
`KillSwitch._exit_all_trades_indestructible` (first pass + orphan sweep + retry) and asserts SIX
together, on one flatten: a TRACKED long (RELIANCE, resting SL+TGT) whose first exit is an A-2
BrokerTimeout after a partial fill (100→residual 40) + an untracked CNC orphan (TCS):
(1) 977 — resting SL+TGT cancelled at broker BEFORE the flatten; (2)+(4) H-4 — retry fires residual
SELL 40 not stale SELL 100 (no oversell); (3)+(5) H-5 — CNC orphan swept as DELIVERY not INTRADAY
(no naked MIS short); (6) delivery-off — the CNC (DELIVERY) exit is REFUSED (SLICE2.5-P1 lock) →
surfaced (queued) → escalated via `_alert_exit_failed`, not swallowed, no MIS substitute.

REAL: KillSwitch, the whole `_exit_all_trades_indestructible`, `_cancel_trade_resting_exits` (977),
determine_close_direction, _marketable_exit_params, _mark_trade_exiting, StateStore(real schema),
EventBus. SIMULATED (legit seams): the broker adapter (ordered place/cancel; signed positions; tracked
first exit = A-2 timeout after partial fill; CNC DELIVERY refusal = the delivery lock) + `_alert_exit_failed`
spy. Deterministic time: now_ist reads a mocked clock, patched time.sleep advances it, retry deadline
shrunk (0.02h) so the escalation converges in ~5 iterations.

Load-bearing: verified by ONE revert cycle on the H-4 keystone — the integration test FAILED at
assertion 2 (the composed retry fired the stale qty) with the re-derivation reverted, then restored via
`git checkout` (commit stayed tests-only). 977 + H-5 covered by reasoning + their unit red/green.
H-12-independent (signed positions). Optional delivery-ENABLED happy-path scenario DEFERRED (delivery is
off by default; the refusal path is the critical one). Full affected suite 58 pass.

**Group-A CLOSED (977✓ H-4✓ H-5✓ + e2e).** Still OUT of Group A: **H-10 (Group B, next)**; H-12 paper
qty-sign still blocks a PAPER DRILL of the HARD_KILL reverse-flatten direction (Wave 3); the H-6
CNC-orphan-un-flattened-while-delivery-off interaction (delivery gate — surfaced+escalated, not silent).

Related: [[h5_killswitch_sweep_product_fixed_05jul]] · [[h4_killswitch_retry_rederive_fixed_05jul]] · [[p1_killswitch_dead_column_fixed_05jul]] · [[wave1_chain_validated_e2e_05jul]]
