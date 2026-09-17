---
name: schema-product-is-on-orders-05aug
description: "There is no trades.product column — product lives on orders and reaches code via LEFT JOIN on leg='ENTRY'. Any \"FROM trades WHERE product=...\" query errors."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4eb48114-5788-48ac-94d6-e91b992a6fe4
  modified: 2026-08-05T06:15:49.031Z
---

⛔⛔ **THERE IS NO `trades.product` COLUMN.** Measured 05-Aug-2026 against `core/schema.sql`
(the tracked source — ⛔ never the stale PC `.db`).

- `product TEXT NOT NULL -- MIS/CNC/CO` is at **`schema.sql:326`, inside `CREATE TABLE orders`
  (declared `:313`)**. ⚠️ **`:326` is a real line and citing it as `trades.product` is the trap** —
  I made exactly that error and it produced three broken operator commands.
- **ZERO hits for `product` inside `CREATE TABLE trades`** (declared `:117`, scanned 117–255).
- **No migration adds it** — width: `grep -rn "ALTER TABLE trades" --include=*.py --include=*.sql`,
  `venv` excluded → **3 hits, all in `tests/`, all `DROP COLUMN`**.

✅ **HOW THE CODE GETS IT** — `state_store.get_all_open_trades()`:
`SELECT … o.product … FROM trades t LEFT JOIN orders o ON o.trade_id = t.trade_id AND o.leg = 'ENTRY'`.
`get_stuck_exiting_trades()` says *"Same JOIN/columns as get_all_open_trades"* ⇒ same route.

⇒ ⛔ **ANY `SELECT … FROM trades WHERE product = 'CNC'` FAILS with `no such column: product`.**
**Always join:** `LEFT JOIN orders o ON o.trade_id = t.trade_id AND o.leg = 'ENTRY'`.

🔴 **AND IT IS A *LEFT* JOIN, WHICH A COLUMN WOULD NOT BE:** a trade with no `ENTRY` order row gets
**`product IS NULL`** ⇒ **invisible to any `WHERE product='CNC'` filter**, and
`_PRODUCT_TO_INTENT.get(product or "", "")` (`order_reconciler.py:1272`) maps it to the **empty
intent**. ⇒ **a route to a false "no delivery trades" that NO status filter can catch.** LATENT.

📌 **Other schema facts pinned the same day** (all `core/schema.sql`):
`trades.status` CHECK `:158-161` = `PENDING · PENDING_FILL · OPEN · PARTIAL · EXITING · CLOSED ·
CLOSED_MANUAL · CANCELLED · FAILED · UNKNOWN_IN_FLIGHT` **OR `GLOB 'REJECTED*'`** — ⚠️ **filtering
on `('OPEN','PARTIAL','EXITING')` omits `PENDING_FILL` and `UNKNOWN_IN_FLIGHT`, both of which can
hold a REAL broker position while the DB lags.**
Sizing candidates are **their own columns**, ⛔ not a JSON blob and ⛔ there is no `sizing_breakdown`:
`qty_by_risk :218 · qty_by_capital :219 · qty_by_concentration :220 · qty_by_flat :221 ·
binding_constraint :222` (stored **lowercased** — `position_sizer.py:646`).
`gtt_state` `:1217-1236`: `gtt_id :1218 · trade_id :1219 · symbol :1220 · status :1227`
(CHECK `ACTIVE|TRIGGERED|CANCELLED|EXPIRED|REJECTED|CLEANED`, `:1228-1229`) · `created_at :1232`.

⛔ **`HOLDING` IS NOT A TRADE STATUS** — width: `git ls-files '*.py' '*.sql' '*.yaml' | xargs grep -n
HOLDING` → **exactly 1 hit repo-wide**, a *comment* at `order_reconciler.py:420`. It is **Kite's own
UI label**, with no representation in this schema.

🔴🔴 **AND THE JOIN CAN RETURN >1 ROW PER TRADE — ⛔ NO `UNIQUE` ON `orders(trade_id, leg)`.**
`orders.order_id` is the PK; **all three orders indexes are NON-unique** (`idx_orders_trade_id` ·
`idx_orders_status` · `idx_orders_leg`, `schema.sql:368-380`). The schema **expects** multiples:
`leg_index -- 0 for FULL entry; 0/1/2 for SCALE legs`, plus a `superseded_by` replacement chain
(a re-placed / superseded entry). ⇒ ⛔ **ANY `SUM()` OVER THAT JOIN CAN DOUBLE-COUNT.**
**Sum per DISTINCT `trade_id` (subquery), and check for duplicates first:**
`SELECT t.trade_id, COUNT(*) FROM trades t JOIN orders o ON o.trade_id=t.trade_id AND o.leg='ENTRY'
GROUP BY t.trade_id HAVING COUNT(*)>1;`

Related: [[check1-skip-guards-3of4-05aug]], [[db-schema-v28-split]].
