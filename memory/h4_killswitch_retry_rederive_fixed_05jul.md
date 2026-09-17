---
name: h4-killswitch-retry-rederive-fixed-05jul
description: "Wave 2 H-4 FIXED — HARD_KILL retry loop re-derives (side,qty) via determine_close_direction per attempt (was stale full-qty re-fire → oversell). Group-A still open (H-5 + validation)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 2, H-4 — FIXED (commit `5f116c0`, main, UNPUSHED).**

Root cause: the HARD_KILL flatten's retry loop (`KillSwitch._exit_all_trades_indestructible`)
re-fired the STALE full qty captured at first-pass time (the `failed_trades` tuple), gated only by a
binary `_is_position_flat` check. If the first exit raised AFTER transmission (BrokerTimeoutError — the
A-2 ambiguity class, fixed in order_placer but never applied here) and PARTIALLY filled, the position
is non-flat → the retry re-fired the FULL qty → oversell → new naked reverse. The first pass is
broker-net-aware (`determine_close_direction`); the retry was not.

Fix (mirror the first pass): re-derive `(close_side, close_qty)` via `determine_close_direction` from a
FRESH signed broker-position read on EVERY retry attempt; fire exactly that residual side+qty. `(None,0)`
flat result SUBSUMES the binary `_is_position_flat` gate (now UNUSED — left in place; a follow-up cleanup
can delete it); the broker-error fallback to the captured (exit_side, qty) preserves err-toward-flattening.
No extra broker call (the fresh get_positions is the same one the flat pre-check already made).

Parity: single shared method → one fix both modes; no paper duplicate. **H-12 clarification (NOT in
scope):** determine_close_direction consumes broker_net_qty (SIGNED). LIVE = correct. PAPER: get_positions
strips the sign (H-12) → for a SHORT the DIRECTION is wrong — but PRE-EXISTING (the first pass already uses
determine_close_direction), H-12's fix (Wave 3), NOT introduced by H-4. H-4 makes both passes consistent.

Test: `tests/unit/test_h4_killswitch_retry_rederive.py` (3) — drives the REAL
`_exit_all_trades_indestructible` over the real schema + a recording adapter (first exit = A-2 timeout
after partial fill; get_positions returns a correctly-SIGNED residual; time.sleep patched). T1 LONG
residual 40 → retry SELL 40 not 100; T2 SHORT residual 40 → retry BUY 40 (direction re-derive) — both RED
against the stale-qty loop → GREEN; T3 flat → retry fires nothing (PASS both). kill_switch 52 pass.

Group-A HARD_KILL flatten STILL OPEN: **977✓ H-4✓ — H-5 (CNC/product sweep hardcodes intent=INTRADAY → a
CNC position swept as MIS = naked MIS short) + the Group-A validation remain. H-5 next.** H-12 still blocks
a paper drill of the HARD_KILL direction (Wave 3). A-2 timeout discipline now consistent across
order_placer + kill_switch. Deploy caveat: live post-receive = checkout only, no restart; trading-system
inactive now → next start picks it up.

Related: [[p1_killswitch_dead_column_fixed_05jul]] · [[wave1_chain_validated_e2e_05jul]] · [[a2_timeout_retry_impl_02jul]] · [[full_repo_audit_04jul_pending]]
