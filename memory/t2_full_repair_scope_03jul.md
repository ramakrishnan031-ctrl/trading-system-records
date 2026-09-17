---
name: t2_full_repair_scope_03jul
description: "T2 proof-script FULL repair spec (03-Jul one-pass audit) — exactly 3 drifts (no new), store wiring = throwaway StateStore (prod-store is FK-broken for trade_id='t2'), dry-run FAIL today→PASS after fix; build weekend, run Monday"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54ecd864-01af-4fbe-b453-740efca8a1e9
---

**T2 full-repair investigation (03-Jul, read-only, one pass vs main==9becf8c). STEP-1 state:**
`f009cc7` ensure-flat IS ancestor of 9becf8c → deployed (Phase-0a prereq ✅). Script on main ==
local copy. Parked `fix-t2-import-02jul`@b826ae0 is based on STALE 59f83b5 → **do NOT reuse;
branch fresh off post-batch main.** `--dry-run` TODAY = FAIL (L71 import dies at
`_build_live_adapter` L305, BEFORE the dry-run branch L312); after drifts #1+#2 a clean dry-run is
achievable (dry-run never builds the placer → #3 irrelevant to it).

**COMPLETE drift list — exactly the 3 known, NO new drift (full static audit):**
1. **L71** `from core.order_state_machine import` → module moved; `core/` ABSENT, correct =
   `broker.order_state_machine` (main.py:1621 pattern).
2. **L83** `RateLimiter(cfg.broker_limits.rate_limits)` → AttributeError (BrokerLimitsConfig has
   order/quote/historical/margins buckets, no `.rate_limits`). Current sig
   `RateLimiter(limits: BrokerLimitsConfig, *, max_wait_sec=30, shutdown_event=None)`
   (rate_limiter.py:148-154); main:1623 passes `app_config.broker_limits`. Fix:
   `RateLimiter(cfg.broker_limits)`.
3. **L319-22** CncGttPlacer built WITHOUT `store=` → None → `_persist_state` degrades to
   in-memory (cnc_gtt.py:76-79) → NO gtt_state row → the P2-lifecycle pass criterion
   unverifiable. main:2199-2211 passes `store=store` + calls `hydrate_from_store()`.

**Verified ALIGNED (no drift):** ZerodhaAdapter ctor — all 8 T2 kwargs exist incl.
`delivery_enabled:375`, no new required params; ProductResolver/CostCalculator/OrderStateMachine
== main:1621-25; `load_all` (config_loader:1615); config paths `system.capital.
{gtt_sl_limit_offset_pct, sl_limit_offset_pct}` == main:2201-02; `place_order(symbol,side,qty,
price,order_type,intent,tag)` (:470-81, returns PlacedOrder.broker_order_id:143);
`place_for_fill(*, symbol, exit_side, qty, sl_price, tgt_price, trade_id, tag="")` + CncGttResult
fields gtt_id/sl_trigger/sl_limit/tgt_trigger/tgt_limit(+modified) (cnc_gtt.py:36-43,94-104);
`get_quote:1537`; `_resolve_tick:1210` = FAIL-SAFE without instrument_cache (DEFAULT_TICK 0.05 +
throttled WARN — placeable, NOT a drift; optional set_instrument_cache polish).

**STEP-3 store wiring — DESIGN DECIDED: throwaway StateStore, NOT prod.** Placer contract =
`store.insert_gtt_state:2039 / update_gtt_state_legs:2070 / get_active_gtt_states:2104`.
**Prod store is BROKEN for T2 by design:** `gtt_state.trade_id` FK → trades(trade_id)
(schema.sql:1173) + `PRAGMA foreign_keys=ON` per connection (state_store.py:109) → synthetic
`trade_id="t2"` ⇒ FK violation ⇒ best-effort catch logs "persist FAILED" ⇒ still no row; plus
stale-ACTIVE contamination risk (T2 deletes GTT via kite directly → row would stay ACTIVE → next
trader boot would hydrate a dead gtt_id). **Fix:** `store = StateStore("data_store/t2_proof_
<date>.db")` (fresh file self-migrates full schema) → seed ONE minimal synthetic trades row
('t2') → `CncGttPlacer(..., store=store)` + `hydrate_from_store()` (mirrors main; 0 on fresh) →
criterion check = SELECT gtt_state row (ACTIVE, legs match get_gtt) → cleanup marks row CANCELLED
via direct UPDATE (no placer status API exists — that's SmartTgt's prod job). Same class/code
path/FK semantics as prod = parity; prod DB untouched; zero Monday-boot risk.

**Repair plan:** weekend off-market, branch fresh off post-batch main → apply #1/#2/#3 + store
blocks → py_compile + import-smoke → clean `--dry-run` on VM → commit+push → **Monday mid-session
run COMPLETE T2** per runbook. SYSTEM_MAP/PATHS updates ride the repair commit (tree frozen
tonight for the batch+GUI push — deferral flagged, consistent with the other 03-Jul tasks).
