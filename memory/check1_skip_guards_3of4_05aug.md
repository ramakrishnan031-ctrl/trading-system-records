---
name: check1-skip-guards-3of4-05aug
description: "CHECK1's delivery skip is trade_id-keyed and guards 3 of 4 paths into _check1_manual_close; _check_stuck_exiting is unguarded. Measured 05-Aug-2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4eb48114-5788-48ac-94d6-e91b992a6fe4
  modified: 2026-08-05T05:36:45.417Z
---

**CHECK1's delivery skip guards 3 of the 4 entry points into `_check1_manual_close`.**
Measured 05-Aug-2026 at `0aad938`; ⭐ **`order_reconciler.py`, `state_store.py`,
`product_resolver.py`, `constants.py` are BYTE-IDENTICAL at deployed `0197923` and HEAD**
(md5 match), so every cite holds at both.

⛔ **THE SKIP IS KEYED ON `trade_id`, NOT SYMBOL AND NOT THE BROKER.** `:855`
`get_active_gtt_states()` (`state_store.py:2250` = `WHERE status='ACTIVE'`) → `:858`
`delivery_trade_ids` → `:871-872` `continue` only if `trade["trade_id"]` is in it.
⇒ **an ACTIVE row with a NULL or MISMATCHED `trade_id` ALSO FAILS TO SKIP** — so
*"is there an ACTIVE row?"* is **not** a sufficient check, and *"the GTT passed at Zerodha"*
is a different fact entirely.

🔴 **THE UNGUARDED PATH: `_check_stuck_exiting` (called `:944`) re-queries its own working set
(`get_stuck_exiting_trades`, `:1516`) with NO delivery exclusion and calls
`_check1_manual_close` at `:1531`** when `broker_qty == 0` — which is what T+1 produces.
The other guards: `:916` CHECK2 (symbol-keyed), `:967-970` CHECK9/G5b (trade_id-keyed).
⚠️ **REACHABILITY UNSETTLED (bucket d):** needs a trade in `EXITING`. No EXITING writer filters
by product (`kill_switch:1478` · `order_placer:3816` · `structure_exit_manager:349`), **but**
`constants.py:42 EMERGENCY_FLATTEN_PRODUCTS={"MIS","CO"}` and Q4 both point away from the kill
path reaching CNC. **Settles it:** (i) `structure_exit_manager`'s product scope, (ii) a live
`SELECT trade_id,product,status FROM trades WHERE product='CNC'`.

⛔ **THE TWO IRREVERSIBLE LINKS RUN *BEFORE* THE PRODUCT READ:** broker cancellation `:1264`
(**not idempotent — destroys the mid-fill evidence**) and the capital release, both ahead of
`product = trade["product"]` at `:1271`. ⇒ **by the time CHECK1 knows the trade is CNC, it has
already cancelled the orders.**
⚠️ **The `gtt_state` read FAILS OPEN** (`:856-857` catches everything → empty skip set) —
deliberate for reconcile availability, but its blast radius changed the day a real CNC position
existed.

✅ **ONE canonical intent→product mapping (`ProductResolver` ← `system_config.yaml product_map`)
and ONE inverse (`core.constants.PRODUCT_TO_INTENT`, 6 importers, none redefining).** ⚠️ But
`_INTRADAY_INTENTS` is defined **twice** (`position_sizer.py:52` · `fund_manager.py:100`) and
they **AGREE** ⇒ latent debt. ⛔ **Never add a third.**
⭐ `product` is **already read inside CHECK1** — no new source of truth is needed by any remedy.

Record: `docs/audit/check1_product_skip_step1_05aug2026.md`. Related: [[reconcile-positions-blind-t1-30jul]],
[[q4-hard-kill-delivery-30jul]], [[paper-cannot-exercise-class-26jul]] (paper nets by SYMBOL ⇒ a
paper drill of any product-keyed change is vacuously green).
