---
name: h12_paper_positions_signed_06jul
description: "Wave-3 H-12 DONE (06-Jul, commit 18b0a74 unpushed) — paper adapter get_positions now returns SIGNED net qty (was abs), fixing paper flatten-direction parity; unlocks Wave-1/2 paper drills of the reverse-aware flatten path."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-3 H-12 FIXED** (commit `18b0a74`, main, UNPUSHED — Rama pushes off-market). One fix = one commit (`broker/zerodha_adapter.py` + `tests/unit/test_h12_paper_positions_signed.py` ONLY; H-13/H-11/H-8/H-9 untouched). Ref finding H-12 in `docs/audit/full_system_audit_04july2026.md`.

**Root cause:** the paper branch of `zerodha_adapter.get_positions` (`:1077`) returned `qty=abs(info["qty"])`; the live branch (`:1105-1115`) returns kite's signed `"net"` `quantity`. The paper book ALREADY tracks a signed net — at the fill site (`_synth_fill` `:2114-2136`) `new_qty = old_qty + qty` (BUY) / `old_qty - qty` (SELL), stored `"qty": new_qty` with `side` sign-derived, popped when 0. So a paper SHORT nets −qty in the book but surfaced +qty through get_positions. `abs()` was the ONLY sign-stripping site.

**Fix (at the source, mirror live):** `qty=abs(info["qty"])` → `qty=info["qty"]` (returns the book's already-signed net, not a sign-flip patch). Live adapter + all consumers UNCHANGED. `side` was already sign-derived so only qty needed it.

**Consumer scan (the point of the fix) — TWO categories, ZERO workarounds:**
- **Category A — magnitude-only (`abs()`/`!=0`/`==0`), byte-identical after fix:** `kill_switch._is_position_flat:874` + sweep order-qty `:1181`; `order_reconciler:813,1224,2239(==0),2292(abs)`; `eod_squareoff:1011,1379/1407,1533`; `structure_exit_manager._broker_mis_qty:631` (its docstring even documents the divergence + defends with abs — now stale comment, code still correct, left per no-refactor rule).
- **Category B — sign-for-direction, was BROKEN in paper, CORRECTED by fix (victims, not workarounds):** `position_helpers.broker_net_qty:38`→`determine_close_direction` (net<0→BUY); `kill_switch` HARD_KILL orphan sweep `:1159` (`"SELL" if pqty>0`); `order_reconciler._flatten_broker_position:1739`; `eod_squareoff._place_marketable_limit_exit:1450`. In paper a short read +qty → SELL → **doubled the short** (THELEELA oversell FIX-190 prevents).
- `cnc_gtt_monitor:355` filters `product!="CNC"` → paper positions are all hardcoded MIS → no-op in paper (live CNC unaffected). `get_positions` = single shared method, one `if self._paper:` branch, no per-strategy override.

**Tests** (`tests/unit/test_h12_paper_positions_signed.py`, drive REAL `place_order`→`_synth_fill`→book, assert REAL `get_positions`+`determine_close_direction`; wait polls the signed book so it's stable under RED+GREEN; no mocks in the assertion path — paper never calls kite): T1 long +100 · **T2 short −60 (RED before fix: returned +60)** · T3 flat=no-row + net 0 · T4 partial 100−40=+60 residual · **T5 determine_close_direction paper short→("BUY",60) == live-signed stub (RED before fix: ("SELL",60))**. RED proven by reverting the one line → T2+T5 fail with `('SELL',60)`, then restored. **248 tests green** across H-12 + full paper-adapter suite + Wave-1 `test_emergency_exit_chain` + Group-A `test_hard_kill_flatten_chain` + fix190/kill_switch/reconciler/eod/structure_exit/ramcoind-oversell consumers; 0 regressions.

**Parity:** paper output now matches live's signed convention (+long/−short) exactly. Wave-1/2 fixes ASSUMED this; H-12 makes it true in paper.

**PAYOFF (separate future step, NOT run today):** with H-12 live in paper, the Wave-1 emergency-exit and Wave-2 HARD_KILL reverse-flatten paths can now be **paper-drilled for DIRECTION** (a paper short flattens BUY, not SELL). Related: [[groupa_hardkill_validated_05jul]] · [[wave1_chain_validated_e2e_05jul]] · [[h10_place_none_backstop_fixed_05jul]]. **Wave-3 status: H-12✓ · H-13/H-11/H-8/H-9 PENDING.** STOP after H-12 (did not start H-13); await review.
