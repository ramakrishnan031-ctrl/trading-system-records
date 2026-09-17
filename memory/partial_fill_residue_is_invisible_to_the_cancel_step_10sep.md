---
name: partial_fill_residue_is_invisible_to_the_cancel_step_10sep
description: "A protected-MARKET partial fill leaves a resting LIMIT at the protection price that PASS_2's cancel step is structurally blind to, so PASS_2 would place on top of it and oversell -- latent today only because MARKET is rejected outright"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cd55cfe-fe98-41cd-9f88-2432e9db8b6a
  modified: 2026-09-10T06:08:52.065Z
---

🔴 **PROTECTED MARKET IS NOT BINARY. IT CAN LEAVE SOMETHING BEHIND.**

⚠️ **The broker behaviour is 👤 Rama's, from Zerodha's own documentation — ⛔ NOT
verified by me** (verifying it needs a live order, which is forbidden): when price
moves outside the protection range, **not all shares execute, and the remaining
quantity stays open as a LIMIT order at the protection price.**

⭐ Every design so far — Rama's, ChatGPT's and mine — treated the outcome as
**flat or not flat**. ⛔ It is neither.

🔬 **MEASURED 10-Sep-2026 at `3b15bbf`** (worktree `D:/Projects/wt-mktprot-10sep`;
these files are md5-identical to the deployed tree).

## 🔴 THE CANCEL STEP IS STRUCTURALLY BLIND TO IT — THREE REASONS, EACH SUFFICIENT
1. **It reads the LOCAL DB, ⛔ never the broker.** `mis_autosquareoff.py:586` —
   `resting = self._store.get_open_mis_exit_orders_for_symbol(sym)`.
2. **That query is leg-scoped.** `state_store.py:1200` — `o.leg IN ('SL','TGT')`.
   ⛔ A protection-converted residue is neither leg.
3. ⭐⭐ **The pass's own exit order NEVER GETS AN `orders` ROW AT ALL.**
   `zerodha_adapter.place_order` performs **zero** `_store` writes (grep: 0 refs).
   ⚠️ **COUNT CORRECTED 10-Sep round 3:** there are **SEVEN** orders-table INSERT
   sites, ⛔ not three — my first grep was literal and missed `INSERT OR IGNORE`:
   `eod_squareoff.py:1220/:1336/:1686`, `order_manager.py:312/:365`,
   `sl_breach_monitor.py:273`, `structure_exit_manager.py:486`.
   ⭐ **The conclusion is UNCHANGED and stronger:** ⛔ none is reachable from
   `mis_autosquareoff`, whose only `_store` calls are the two **reads** at `:586`
   and `:705` — a grep for `transaction|execute|INSERT|UPDATE` in that module
   returns **nothing at all**.

⇒ 🔴 **PASS_2 would place on top of a live resting remainder.** That is precisely
what the module's own docstring at `:559-563` exists to prevent — *"MIS SL/TGT are
plain orders, NOT a broker-side OCO … BOTH can fill and a long 1 becomes a short
1"* — re-entering through the one path the cancel step cannot observe.

⭐ **THE CAPABILITY EXISTS 155 LINES AWAY.** `_restore_protection_inner:741` calls
`self._adapter.get_open_orders()` (broker OPEN / TRIGGER PENDING; adapter `:1825`
returns `order_id, symbol, status, transaction_type, quantity, price,
trigger_price`). ⚠️ But note its filter requires **`trigger_price > 0`**, so even
that call would not match a plain converted LIMIT. ⇒ ⛔ a fix cannot just reuse it
unchanged.

## 🟢 QUANTITY DOES SELF-CORRECT — AND THAT IS NOT ENOUGH
🔬 `_run_pass:425-427` calls `self._adapter.get_positions()` **fresh at the top of
EVERY pass** (PASS_1 and PASS_2 share the path; `which` is only a label) → `:438`
`candidates = _find_open_mis_positions_for_auto_squareoff(positions)` → `:570`
`qty = cand["qty"]` → `:582` `requested_qty = abs(qty)`. The comment at `:576-581`
names the hazard itself: *"FRESH BROKER POSITION QUANTITY IS THE REMAINING
QUANTITY. Never trades.qty_filled … and never local_filled − broker_remaining: no
double-subtraction."*

⚠️⚠️ **NECESSARY, ⛔ NOT SUFFICIENT.** A PASS_1 partial of 60/100 leaves the broker
position at 40, so PASS_2 correctly requests 40 — **and the resting 40 is still
live.** Both can fill ⇒ a **40-share SHORT**. ⭐ Getting the quantity right does
nothing about the second live order.

## ⭐ LATENT TODAY — AND THE REPAIR IS WHAT ARMS IT
🔬 PASS_1/PASS_2 send `MARKET`, which Zerodha rejects outright — **0 MARKET rows
ever, 1,401 rows, all time.** ⇒ ⛔ no partial can occur today. 🔴 **Adding
`market_protection` is exactly what makes this reachable for the first time.**
⇒ ⭐ this belongs in the implementation SPEC, ⛔ not in a later fix.

See [[no_order_path_can_send_market_09sep]] ·
[[squareoff_window_protection_band_measured_10sep]] ·
[[a_terminal_mark_can_delete_its_own_retry_04sep]].
