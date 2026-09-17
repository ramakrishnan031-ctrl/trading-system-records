---
name: v3_step7_entry_engine_12jul
description: V3 Step 7 — 03.07 Entry Engine VERIFY (ADAPT); order/OCO/RAMCOIND path already COMPLETE + battle-tested → ZERO code change; sl_price is the V3 SL seam; ATR-into-live-SL re-flagged
metadata:
  node_type: memory
  type: project
  originSessionId: e31b6e26-79d0-41d6-b1cc-db98a712e270
---

**V3 Shared-Engine — Step 7: 03.07 Entry Engine (12-Jul-2026). ADAPT = pure VERIFY. 03.07 is COMPLETE + RAMCOIND-battle-tested → ZERO code change (do not churn proven code). LIVE entry BYTE-IDENTICAL by construction.** Gap-map: **`docs/v3/V3_STEP7_ENTRY_ENGINE_GAPMAP.md`**. Follows [[v3_step6b_portfolio_allocator_impl_12jul]].

**T1 verdict — every 03.07 requirement PRESENT (source-cited):**
- Entry order type = bounded **LIMIT** (`order_protocol_limit.execute` Phase-1; `entry_order_type` default LIMIT; MARKET only for the off-by-default SNR-V2 retest-confirm); emergency/kill = marketable-LIMIT capped 1% (`price_math.marketable_limit_price`, no raw MARKET); SL leg = SL stop-limit (P0 no SL-M).
- Slippage tolerance = `order_placer._compute_slippage_tolerance` min(SL_dist×0.22, Rs5)+band+**override hierarchy Symbol>Strategy>Band>Global** (`_resolve_effective_sl_fraction`); FIX-128 1% LTP-deviation abort (no chase).
- **TGT recalc from actual fill** (FIX-013 `calc_tgt_price(entry=avg_fill_price…)`) while **SL stays signal-fixed** (`fill_entry.sl_price`).
- Mandatory bracket = 1 SL + 1 TGT **software OCO** (SL-first `place_exits`; on exit fill `close_trade` double-close-guard → `_cancel_oco_siblings`; tgt_retry never makes a 2nd).
- **Naked handling** = `SLUnplaceableError` → CRITICAL `LIMIT_TRIPLE_EXITS_FAILED_POSITION_UNPROTECTED` → `_emergency_market_exit`(FIX-148) → `_fire_hard_kill_for_unprotected_position`; TGT-unplaceable → SL-only+`mark_needs_tgt_retry`; LTP-error → exit-retry queue (FIX-061).
- **Idempotency + reconcile-on-uncertainty** = A-2 timeout → UNKNOWN_IN_FLIGHT, NO retry, reconciler `_recover_in_flight_entries` SOLE owner (authoritative broker book).
- Partial fill = exits at `event.filled_qty`; capital committed at actual_qty. MIS coercion at broker boundary; CNC OCO-GTT path present but delivery double-locked OFF. Circuit-band exit-clamp `clamp_exit_into_band` (3 sites). RAMCOIND 4-layer intact.

**T2 SL seam:** the order path derives NO SL — `sl_price` is a plain param threaded `signal_processor._derive_prices → place → execute → place_deferred_exits → place_exits`. V3 03.03 `computed_sl` feeds `sl_price` at the **signal_processor seam on the V3 path only** (a later playbook step) with NO order-path change. LIVE SL stays FIXED_PCT. **Seam already open — nothing to wire in 03.07.**

**T3:** NO genuine gap → NO code change. **T4 flagged (NOT changed):** (1) ATR-into-LIVE-SL (carried from Step 5 T5b) — LARGE money-path blast radius; belongs to the V3 playbook step + its own parity proof, NOT here. (2) `entry_order_type="MARKET"` retest path is off-by-default (noted). OCO/RAMCOIND machinery must not be restructured.

**Gates:** **G1** — **0 `orders/*.py` files modified by any V3 step (1–6b)** → LIVE entry byte-identical by construction. **G2 RAMCOIND MANDATORY** — `test_ramcoind_dup_exit_fix` + `test_ramcoind_oversell_prevented` + `test_order_placer` + `test_tgt_retry` + `test_fix190_exit_safety` + `test_fix148_broker_gaps` = **209 pass** (4-layer intact). **G3** — no code change → no new failures. paper==live (all shared entry/exit code, no mode branch). **VERIFY-only; nothing built, nothing to push except the gap-map doc (travels with the V3 doc bundle).** NEXT = Web Claude + ChatGPT review → Step 8 (03.08 Trade Management — highest-frequency SL modifier, RAMCOIND-critical). Method: source-verified directly (no fan-out [[feedback_sequential_agents_only]]); SYSTEM_MAP read first [[feedback_system_map_first]].
