---
name: h10_place_none_backstop_fixed_05jul
description: Wave-2 H-10 fixed — order_placer.place() result=None backstop; leaked-reservation/stuck-PENDING bug closed; Wave 2 complete
metadata: 
  node_type: memory
  type: project
  originSessionId: 46720e02-4098-4c34-87c3-16d4cb5c52fa
---

**Wave 2 / H-10 FIXED** (commit `ee9f993`, main, UNPUSHED — Rama pushes off-market; push = checkout only, no restart, inactive now). **Last Wave-2 item → WAVE 2 COMPLETE.**

**Root cause:** `orders/order_placer.py::place()` retry loop. The FIX-072 16388 (insufficient-margin) branch does `retried_16388 = True; continue`, borrowing an iteration of the **SHARED** 429 attempt budget. When the FIRST 16388 lands on the FINAL loop attempt (`attempt == max_429_retries`), `continue` steps past `range()`'s last index → `execute()` never re-runs, no rejection handler fires, `result` stays **None** → post-loop `if not result.success` (:1347) derefs None → **AttributeError (not BrokerError)** → `_handle_placement_failure` never runs → trade stuck **PENDING** + reservation **leaked** for the session.

**Fix (a, mandatory):** `if result is None:` backstop before the deref → routes through the SAME `_handle_placement_failure` (release reservation + mark FAILED) then `raise BrokerError(...)`. No AttributeError path remains. 16388 == order REJECTED → no open position → safe to fail without the best-effort retry (no naked exposure).

**Option (b) verdict = NO defect** (investigated, not implemented per no-speculative rule): the shared 429/16388 budget is fine; the 16388 retry is best-effort and its starvation on the final-attempt edge produces a safe, correct rejection once (a) is in place. Budget UNCHANGED.

**Parity:** `place()` is one shared method (paper vs live differ only in the adapter); no paper-specific duplicate; one fix both modes.

**Tests** (`tests/unit/test_order_placer.py::TestBl19PlacerRateLimitRetry`, reuses the BL-19 mock-engine harness `_make_placer_with_mock_engine`): `test_h10_final_attempt_16388_none_result_backstop` (bug; RED = AttributeError@:1347 + stuck PENDING + leaked reservation → GREEN = BrokerError + FAILED + released; verified via revert cycle) · `test_h10_nonfinal_16388_retry_still_succeeds` · `test_h10_429_backoff_unaffected`. Full order_placer + `test_emergency_exit_chain.py` (Wave-1) + `test_hard_kill_flatten_chain.py` (Group-A) = **128 pass, 0 cross-path regression**.

Ref: `docs/audit/full_system_audit_04july2026.md` (H-10). Related: [[groupa_hardkill_validated_05jul]] · [[wave1_chain_validated_e2e_05jul]] · [[mo1_fixed_flatten_quote_key_05jul]] (the M-O1 flatten-quote-key twin) · [[a1e1_orphan_fix_impl_02jul]] (A-1/E-1 prepass — the accidental mitigator).

**Deferred out of Wave 2:** H-6 (CNC orphan un-flattened while delivery-off — surfaced+escalated, not silent), H-12 (paper get_positions strips qty sign — Wave 3), H-11 (`_invalidate_token` wrong path). Await Web Claude Wave-2 closure synthesis + fresh-audit recommendation before any Wave-3 work.
