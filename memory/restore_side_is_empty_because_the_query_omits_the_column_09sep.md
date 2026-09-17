---
name: restore_side_is_empty_because_the_query_omits_the_column_09sep
description: The MIS restore can never succeed -- it reads transaction_type from a SELECT that does not include that column, so side is always ''.
metadata:
  type: project
---

**MEASURED 09-Sep-2026 at `3b15bbf`.** `RESTORE FAILED (side must be 'BUY' or
'SELL', got '')` is **100% deterministic, not data-dependent.**

`orders/mis_autosquareoff.py:737` builds the restore order with
`side=str(_row_get(sl_row, "transaction_type", ""))`. `sl_row` comes from
`core/state_store.py:1731 get_orders_for_trade`, whose SELECT (`:1741`) is
**order_id, leg, status, trigger_price, price, qty_requested, qty_filled** --
⛔ **`transaction_type` is not in it.** `_row_get` (`:134`) swallows the
IndexError and returns the `""` default. ⇒ the restore ALWAYS submits `side=""`
and is ALWAYS rejected by validation.

⚠️ The `resting` rows don't carry it either: `get_open_mis_exit_orders_for_symbol`
selects only trade_id, symbol, leg, variety, order_id.

🔬 Fired **twice** on 09-Sep -- 15:03:02 (PASS_1) and 15:06:03 (PASS_2).

⭐ Three other params read from the same narrow row are ALSO absent but have
harmless defaults, which is why only `side` is fatal: `order_type`→"SL"
(accidentally right), `variety`→"regular" (accidentally right), `trade_id`→""
(empty tag). ⛔ Do not "fix" those by widening the SELECT without re-checking
these defaults.

⛔ **NOT reachable elsewhere.** The other `store.get_orders_for_trade` callers
read only `leg`/`status` (`order_placer.py:2698`, `order_reconciler.py:4576`),
and `order_manager.get_orders_for_trade` (`:763`) is `SELECT *`.
⭐ `order_reconciler.py:4582` shows the safe pattern -- derive side from
`trades.direction`, never from a narrow order row. The EXIT path already does
this correctly: `"SELL" if qty>0 else "BUY"` from the fresh BROKER position.

See [[no_order_path_can_send_market_09sep]].
