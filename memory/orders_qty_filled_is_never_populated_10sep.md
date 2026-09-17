---
name: orders_qty_filled_is_never_populated_10sep
description: "orders.qty_filled is 0 and orders.avg_fill_price is NULL on all 1401 production rows, so 'qty_filled=0' is never evidence of a non-fill and the orders table carries no fill-quantity evidence at all"
metadata:
  type: project
---

🔴 **`orders.qty_filled` IS **0** ON EVERY ROW, AND `orders.avg_fill_price` IS
**NULL** ON EVERY ROW.** 🔬 MEASURED 10-Sep-2026, production
`data_store/trading_system.db`, whole table, all time:

```
total_rows  qty_gt0  avgpx_notnull  avgpx_gt0
1401        0        0              0
```

⛔ **THIS RETIRES A READING THAT LOOKS LIKE EVIDENCE AND IS NOT.** *"ORCHPHARMA's
legs were CANCELLED at `qty_filled=0`"* sounds like proof of a non-fill. It is
not: the **360 COMPLETE ENTRY legs also read `qty_filled=0`**. The column is
**universally unpopulated**, so it distinguishes nothing. ⭐ The CANCELLED
**status** is the real signal; ⛔ the `qty_filled=0` beside it is noise.

⭐ **WHAT LOCAL FILL EVIDENCE ACTUALLY EXISTS:** only `orders.status='COMPLETE'`
and `orders.filled_at IS NOT NULL` (they agree — 661 rows each). ⇒ ⚠️ **ChatGPT's
frozen rule — *"attribute to a leg ONLY if that leg has evidence of a fill"* — has
exactly one local predicate available, and it is the same one
`closure_classifier` already uses (`named_by_local`, `:118`).** ⛔ Do not specify a
fix that keys on `qty_filled` or `avg_fill_price`; both are dead columns.

🔬 **PRICES DO EXIST, BUT IN A DIFFERENT TABLE:** `order_execution_log` has
`intended_price` + `actual_price` populated on **618 of 618** rows.

## 🔴 AND ITS `order_id` DOES NOT JOIN TO `orders`
🔬 **0 of 618** `order_execution_log.order_id` values match any `orders.order_id`.
`order_execution_log` stores the **INTERNAL** id (`ord_<uuid32>`); `orders` stores
the **BROKER** id (e.g. `260909170405475`). ⭐ Join on
`order_execution_log.parent_trade_id = orders.trade_id` **plus `leg`**, or on
`fill_timestamp`. ⛔ A naive `ON e.order_id = o.order_id` silently returns **zero
rows** and reads as "no data" rather than as a broken join — that is how this was
nearly missed.

See [[mid_fill_rung_manufactures_own_sl_10sep]] ·
[[schema_product_is_on_orders_05aug]].
