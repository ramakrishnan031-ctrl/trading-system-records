# PRE-BUILD STEPS S-1 … S-5 + §2 WINDOW · FILE 23 · 28-Aug-2026

⭐ Companion to the frozen `PREBUILD_MIS_SQUAREOFF_28-Aug-2026.md`
(md5 **`db3c7df7cc62ff5d7e2c21a5acc0ddaf`**, 11:34:15). ⛔ That file is **not
modified** — this one carries the S-step answers and FILE 23's predictions 8–11.

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.
🔬 All reads at `52ccb4f`, read-only, 11:49–11:55 IST. ⛔ No production change.

> ## ✅ **NO STOP CONDITION. S-3 and S-4 both clear. ⭐ The build may proceed after 17:45.**

---

## §2 · M-1 / M-2 — THE UNPROTECTED WINDOW · 🔴 **HYPOTHESIS REFUTED**

🔬 **M-1 — the exact cancellation timestamps** (`orders.updated_at`):

| symbol | leg | status | cancelled at | position detected gone |
|---|---|---|---|---|
| TATAPOWER | SL | `CANCELLED` | **15:12:14.696217** | 15:12:47.724 |
| TATAPOWER | TGT | `CANCELLED` | **15:12:14.712309** | ″ |
| MOSCHIP | SL | `CANCELLED` | **15:16:36.304490** | 15:16:35.479 |
| MOSCHIP | TGT | `CANCELLED` | **15:16:36.325097** | ″ |

🔬 **What cancelled them — measured, ⛔ not assumed:**

* **TATAPOWER** — `order_placer.terminal_status_exit_leg_skipped` fires at
  **15:12:14.697**, the *same millisecond* as the SL cancellation. ⇒ the legs went
  terminal because the **trade was already terminal**, ⛔ not because a system
  square-off cancelled them. ⭐ 15:12:14 is **before** the 15:15 SOFT_KILL and
  **before** the 15:17 Pass 1.
* **MOSCHIP** — cancelled at **15:16:36.30**, which is **0.8 s AFTER** the position
  was already detected gone at 15:16:35.48. ⇒ **cleanup, ⛔ not pre-emption.**

> ### 🔬 **M-2 — ANSWER: NO SYSTEM-CREATED UNPROTECTED WINDOW EXISTS.**
> ⛔ **Neither cancellation was performed by the 15:15 SOFT_KILL** (which cancels
> nothing) **nor by the 15:17 Pass 1** — 🔬 which reported *"0 orders cancelled"*.
> ⭐ Both cancellations were **consequences** of positions already closed externally.

⭐ **And for the day a position IS still open at 15:17, the interval is measured, not
guessed: cancel → exit are separated by a DESIGNED `time.sleep(2)`** —
`orders/eod_squareoff.py:417-424`, FIX-063, whose stated purpose is to let a phantom
fill settle before the MARKET exit fires.

> ⇒ **THE INTERVAL IS 2 SECONDS BY DESIGN, ⛔ NOT ~2 MINUTES.** 🏷️ The hypothesised
> daily two-minute hole **does not exist**. ⛔ Nothing to record as a defect, ⛔ nothing
> to fix, ⛔ nothing carried into tonight.

⭐ **M-3 constrains the new unit anyway:** its own cancel→verify→exit must stay
per-symbol and adjacent (FILE 23 C-4), so it does not *introduce* the window that
the old path was suspected of and does not have.

---

## S-3 · 🔴 THE 15:17 PASS-1 CANCELLATION SCOPE · ✅ **CNC/GTT STRUCTURALLY UNTOUCHED**

⭐ Pass 1 calls exactly two functions (`eod_squareoff.py:400`, `:407`). Both are
product-filtered **in SQL**:

🔬 `core/state_store.py:1036` — `get_pending_intraday_orders`:

```sql
JOIN orders o ON o.trade_id = t.trade_id AND o.leg = 'ENTRY'
WHERE t.status = 'PENDING_FILL'
  AND o.product IN ('MIS', 'CO')
```

🔬 `core/state_store.py:1163` — `get_pending_exit_orders_for_open_positions`:

```sql
JOIN orders e ON e.trade_id = t.trade_id AND e.leg = 'ENTRY'
WHERE t.status IN ('OPEN', 'PARTIAL')
  AND e.product IN ('MIS', 'CO')
  AND o.leg IN ('SL', 'TGT')
  AND o.status NOT IN ('COMPLETE','CANCELLED','REJECTED','FAILED')
```

> ⭐ **TWO INDEPENDENT REASONS A CNC GTT CANNOT BE TOUCHED:**
> 1. **Product filter** — `IN ('MIS','CO')` on the ENTRY leg excludes CNC outright.
> 2. **Wrong table entirely** — these queries read `orders` rows with
>    `leg IN ('SL','TGT')`. 🔬 A CNC GTT lives in **`gtt_state`**, is placed through
>    the **GTT API**, and has **no `orders` row**. ⭐ There is no path from this SQL to
>    a GTT.

✅ **⇒ NO STOP CONDITION.** ⭐ Calling 15:17 a backstop **for MIS** is justified; ⛔ it
is not a backstop for anything CNC, and it cannot harm CNC either.

⚠️ 🏷️ **A LIVE PROOF CASE MAY ARRIVE TONIGHT, ⛔ unplanned:** if 👤 Rama HOLDS OAL and
RAMRAT, the 15:17 routine runs for the **first time with ACTIVE CNC GTT legs on the
book**. ⭐ Their `gtt_state` rows staying `ACTIVE` across 15:17 would be direct
behavioural evidence for S-3. ⛔ This is an observation opportunity, ⛔ **not** a reason
to hold them — 👤 the decision remains his and is untouched.

---

## S-4 · 🔴 SEGMENT SCOPE · ✅ **EQUITY-ONLY ⇒ THE GLOBAL 15:12 IS SOUND**

⭐ Answered from the code, ⛔ not asked of 👤 Rama.

| evidence | 🔬 measured |
|---|---|
| the tradable universe | `config/instruments.csv` — **2,228 rows, `exchange` = `NSE` for every one.** ⛔ Zero MCX, zero NFO |
| products ever placed | `SELECT DISTINCT product FROM orders` → **`MIS`, `CNC`** only. ⛔ No NRML, ⛔ no CO has ever been placed |
| order placement | `broker/zerodha_adapter.py:606` hardcodes `exchange="NSE"` |
| GTT placement | `:704`, `:753` hardcode `exchange="NSE"` |
| cost model | `broker/cost_calculator.py:14` — *"Only exchange='NSE' supported; **ValueError** for others (CC5)"* ⇒ ⭐ it **refuses**, ⛔ does not silently accept |

⚠️ **A distinction that must not be muddled:** `is_fno=true` in `instruments.csv` means
*"this **equity** has F&O contracts listed"* (⇒ it is a CAS stock). ⛔ It does **not**
mean the row is a derivative contract. ⭐ That is precisely why `is_fno` is the CAS
proxy and why the F&O-**contract** cutoff (15:26) is out of scope.

> ✅ **⇒ The new MIS selector cannot encounter MCX or F&O-contract positions.
> PROCEED with the single global 15:12.** ⛔ No STOP-AND-REPORT.

---

## S-1 · B-4 · THE `remaining` SEMANTICS · ⚠️ **AN OBSERVATION ON THE OLD PATH**

🔬 `orders/eod_squareoff.py` — the two quantities are **not** the same object:

```python
# :1086  broker_qty — computed, but used ONLY as a membership filter
broker_qty = {p.symbol: abs(int(p.qty)) for p in broker_positions
              if int(p.qty) != 0 and p.product in EMERGENCY_FLATTEN_PRODUCTS}

# :1105-1106  the filter — SYMBOL membership only, the VALUE is never read
rows = [r for r in rows if r["symbol"] in broker_qty]

# :1157  the quantity actually submitted — from the LOCAL DB row
qty = row["qty_filled"]
```

> 🔴 **THE OLD PATH EXITS THE LOCAL ENTRY-FILL QUANTITY, ⛔ NOT THE FRESH BROKER
> REMAINING QUANTITY.** ⭐ `broker_qty`'s **values** are computed and then never used.

⭐ **What protects it today** (⛔ so this is NOT reported as a proven defect):
Pass 1 cancels the SL/TGT legs *before* Pass 2 fires, and FIX-063's 2 s sleep exists
to let a phantom fill reach the DB first. ⇒ the stale-quantity case is designed
against.

🏷️ **PARTIALLY MEASURED · OBSERVATION, ⛔ NOT A PROVEN DEFECT.** 🔬 I searched for any
path that decrements `trades.qty_filled` on a partial **exit** and found none — ⛔ but
*"I did not find one"* is weaker than *"none exists"*, and I am not upgrading it.
⭐ **RECORDED, ⛔ not fixed, ⛔ not chased** — the same treatment FILE 23 prescribes for
an existing separate concern.

> ### ⭐ **BINDING ON THE NEW UNIT:** it MUST read `broker_qty[symbol]` as the
> remaining quantity, per B-4 — **fresh broker position quantity IS the remaining
> state.** ⛔ Never `qty_filled`. ⛔ Never `local_filled − broker_remaining`.
> ⛔ Never double-subtract: broker says **40**, local says 60 filled ⇒ submit **40**.

---

## S-2 · LIVE / PAPER PARITY · ✅ SHARED PATH · ⚠️ **ONE ASYMMETRY FOUND**

✅ 🔬 `orders/eod_squareoff.py` contains **zero** mode branching — `_paper`, `paper`,
`is_live`, `mode ==` are all **absent**. ⇒ ⭐ **one shared code path**, so eligibility,
product boundary, quantity semantics, direction mapping, state machine and
reconciliation are parity **by construction**, ⛔ not by duplication.

🔬 Both adapter branches return the same `Position` shape and both filter `qty != 0`.

> ### ⚠️ 🔴 **THE ASYMMETRY, AND IT LANDS EXACTLY ON THE PRODUCT BOUNDARY:**
>
> | branch | line | product when absent |
> |---|---|---|
> | **live** | `zerodha_adapter.py:1234` | `str(row.get("product", ""))` → **`""`** ⇒ excluded |
> | **paper** | `zerodha_adapter.py:1204` | `info.get("product", **"MIS"**)` → **`"MIS"`** ⇒ **ELIGIBLE** |
>
> ⇒ ⭐ A paper position with **no explicit product** is treated as **MIS and becomes
> selectable**; its live twin would be `""` and excluded. ⛔ The paper default is the
> **permissive** one — the wrong direction for a safety boundary.

⭐ **BINDING ON THE NEW UNIT:** require an **explicit** `product == "MIS"`; ⛔ never
rely on a default. ⭐ Add a paper-mode test for a position with a **missing** product
⇒ it must be **excluded**, ⛔ not defaulted into eligibility.

---

## 🔴 THE B-2 CORRECTION FROM FILE 23, ACCEPTED

⭐ 👤 Rama is right and my FILE 21/22 wording was too broad. 🔬
`EMERGENCY_FLATTEN_PRODUCTS = frozenset({"MIS","CO"})` **admits CO**.

* ✅ What was correct: the **product SOURCE** is broker-authoritative, and the old
  selector is correct **for the old path**.
* 🔴 What was too broad: *"B-2 is already correct"* — ⛔ the **new** unit must narrow to
  `product == "MIS"` explicitly and ⛔ must **not** inherit CO eligibility by reusing
  that constant.
* ⇒ ⭐ **Two mutations, ⛔ not one:** `MIS → CNC` ⇒ RED **and** `MIS → CO` ⇒ RED.

⭐ 🔬 Corroborating that CO is genuinely reachable-in-principle but unused today:
`SELECT DISTINCT product FROM orders` = `{MIS, CNC}` ⇒ 🏷️ **CO has never been placed**,
so the CO arm is **NOT EXERCISED** and the narrowing is a guard against a latent path.

---

## 🔒 FROZEN PREDICTIONS 8–11 (FILE 23 §9) · ⭐ WRITTEN BEFORE THE GATE

⭐ Scored **only after** the tests run. ⛔ No prediction adjusted to fit a result.

8. Wiring the new unit to `EMERGENCY_FLATTEN_PRODUCTS` **without** narrowing to MIS
   ⇒ the **CO mutation turns RED**.
9. If the 15:17 Pass 1 could cancel an active CNC GTT ⇒ the **GTT-separation test
   turns RED**. ⭐ Given S-3, I predict this test is **GREEN and stays green**, and that
   the mutation needed to turn it red must be **artificial** (there is no natural code
   path from that SQL to `gtt_state`).
10. Removing the cancel-before-exit step (§3) ⇒ the **double-exit test turns RED**.
11. `entry_end` moved past CHECK 1 ⇒ **config validation FAILS CLOSED**.

⭐ Plus one of my own, so S-2's finding is falsifiable:

12. A **paper** position with a **missing** product ⇒ excluded by the new unit.
    ⭐ If it is selected, S-2's asymmetry is load-bearing and the unit is unsafe in
    paper mode.

---

## WHAT IS NOT MEASURED

1. ⛔ **Whether any path decrements `trades.qty_filled` on a partial exit** — searched,
   none found; 🏷️ **NOT PROVEN absent.**
2. ⛔ **The CO arm has never run** in production (`orders.product` has no CO row).
3. ⛔ **The 15:07 / 15:10 passes have never run.** No production evidence exists and
   none can before **Monday 31-Aug**.
4. ⛔ **Nothing is built, tested or pushed.** ⛔ No auto-square-off code modified.
5. 🏷️ The 15:17-with-live-CNC-GTT case is **NOT EXERCISED** — it may occur tonight
   only if 👤 Rama holds, and that is ⛔ not a reason to hold.

⛔ push ≠ boot · ⛔ executed ≠ exercised · ⛔ exercised ≠ load-bearing ·
⛔ green ≠ red-capable · ⛔ order accepted ≠ position closed ·
⛔ broker query failure ≠ flat · ⭐ **SIMPLE BY DECISION, ⛔ NOT SIMPLE BY ACCIDENT.**

## END
