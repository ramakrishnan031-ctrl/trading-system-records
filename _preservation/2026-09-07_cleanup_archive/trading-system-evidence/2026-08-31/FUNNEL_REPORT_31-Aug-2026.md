# CAPITAL FUNNEL — MEASURED REPORT

**Deployed SHA `39292d3` · executed-path record, 12-Jun-2026 → 31-Aug-2026**
**191,347 signals · 809 trades · 1,266 orders · 2,105 reservations**

⛔ No replay. ⛔ No stubs. ⛔ No broker calls. ⛔ Nothing written to production.
Harness: `scratchpad/funnel_harness.sh` (read-only `mode=ro` SQL over ssh).
Raw run: `FUNNEL_RUN_31-Aug-2026.txt`.

---

## THE FUNNEL

| stage | N_in | N_out | principal rejections | ₹ at the boundary |
|---|---:|---:|---|---|
| **S1 intake** | — | 191,347 | — | — |
| **S2 gates** | 191,347 | 655 `PROCESSED` (**0.34%**) | SCORE_57 62,398 · SCORE_59 26,865 · STRATEGY_CONTROL 21,430 · CIRCUIT_PROXIMITY 9,888 · STRATEGY_CIRCUIT_BREAKER 7,705 · QUOTE_UNAVAILABLE 7,323 · DAILY_TRADES 5,146 · SIZING_CONCENTRATION 3,862 · SYMBOL_DIRECTION_DAILY_LIMIT **300** | — |
| **S3 scoring** | 191,347 | — | **89,263 (46.7%) rejected at scores 57–59** — i.e. within 3 points of `min_pass=60` | — |
| **S4 tier** | 809 | 746 scored | 63 null | tier weight: **0.5 ×743 · 0.7 ×3 · max 0.7** |
| **S5 sizing** | 746 | 746 | — | **binding = concentration on 746/746 = 100.0%** |
| **S6 reservation** | 809 | **809 (100%)** | **ZERO refusals** | avg margin: MIS ₹93.74 · CNC ₹500.30 |
| **S7 order build** | 809 | 1,266 orders | — | product **MIS 1,166 · CNC 100 · CO 0** · variety **regular 1,266 (100%)** · protocol **LIMIT_TRIPLE 809 (100%)** |
| **S8 placement** | 657 ENTRY | 320 COMPLETE | **337 CANCELLED · 0 REJECTED** | MIS **51.7%** fill · CNC **32.0%** fill |
| **S9 lifecycle** | 809 | — | — | **`sl_trail_count = 0` on 809/809** |
| **S10 release** | 2,105 RESERVE | 1,775 RELEASE + 320 RELEASE_USED | — | **NET_MARGIN_DELTA = +₹3,839.57** |

---

## F4 — CNC FILL RATE

**MEASURED:** ENTRY orders by product — MIS 557 → 288 COMPLETE / 269 CANCELLED /
**0 REJECTED** = **51.7%**. CNC 100 → 32 COMPLETE / 68 CANCELLED / **0 REJECTED**
= **32.0%**. At S6, reservations granted **100/100 CNC and 557/557 MIS — zero
refusals**.

**PROVES:** The ~30%-vs-~52% gap is real and reproduces on the full corpus
(32.0% vs 51.7%). Its cause is **CANCELLATION**, not capital starvation and not
broker rejection: CNC obtains its reservation every time, and the broker rejected
**zero** entry orders in 657.

**DOES NOT PROVE:** why the cancellations occur (timeout, throttle, price drift,
EOD sweep), nor that the two books' cancellations share one cause.

### **DEFECT — localised to order cancellation, NOT starvation.**
Rama's starvation hypothesis is **falsified at S6.**

---

## G2 — SCORE / TIER CEILING

**MEASURED:** `tier_weight_applied` across 746 scored trades: **0.5 on 743, 0.7 on
3. Maximum observed = 0.7.** `perf_weight_applied` = 1.0 min and max. Mode `ON`
on 746, null on 63.

**PROVES:** By execution, **no trade has ever received a tier multiplier above
0.7, and 99.6% received exactly 0.5.** The ceiling is confirmed by the executed
path, not by algebra.

**DOES NOT PROVE:** that raising it would improve P&L. ⚠️ It would raise size on a
book with no measured edge.

### **DEFECT — confirmed by execution. ⛔ Fixing it raises size, not edge.**

---

## F11 — DECLARED-AND-INERT

**MEASURED, four separate results:**

1. 🔴 **`cnc_gtt_monitor.py` receives `kill_switch` (`:65`), stores it
   (`:77 self._ks = kill_switch`), and NEVER CALLS `is_active()` on it.**
   Seven other production sites do call it (`order_placer` ×2, `eod_squareoff`,
   `tgt_retry_manager`, `order_reconciler` ×2, `risk_engine`).
2. **`exit_mechanism` populated on 0 of 809 trades.** `closure_source` populated
   on 138 of 809.
3. **`qty_by_flat` computed on 0 of 809 trades**, while `qty_by_risk`,
   `qty_by_capital` and `qty_by_concentration` are computed on 746 each.
4. **`sl_trail_count = 0` on 809/809 trades.**

**PROVES:**
- (1) is **α — constructor pass-through**: the dependency is injected and never
  consulted. **This fully explains the 15:20:36 observation** — `delete_gtt` ran
  LIVE under a SOFT_KILL active since 15:15:01 because *that path cannot see the
  kill state at all*. ⛔ Not a design decision; an unread injection.
- (2) `exit_mechanism` is **declared in schema v45 and never written** —
  class B. `closure_source` is **not** inert (138 writes).
- (3) `qty_by_flat` is **declared and never computed** — class B.
- (4) the trailing counter has never incremented in 809 trades.

**DOES NOT PROVE:** that any of these *should* fire. Whether the GTT monitor
*ought* to gate on the kill is the design question — the measurement cannot
choose. (3) may be intentional if flat sizing is disabled.

### **DEFECT — (1) confirmed α, highest value. (2) and (3) confirmed class B. (4) explained by UNIT2 below, not independent.**

---

## UNIT2 — `order_protocol` DEAD CONFIG

**MEASURED:** `orders.product` over 1,266 orders: **MIS 1,166 · CNC 100 · CO 0.**
`orders.variety`: **regular 1,266 = 100%.** `trades.order_protocol`:
**LIMIT_TRIPLE on 809 = 100%.**

**PROVES:** **CO has never been emitted, not once, in 1,266 orders.**
`order_protocol` holds exactly one value across every trade ever recorded.
The configuration is **dead by execution.**

⇒ **Smart TGT is fully explained and is NOT a separate candidate.**
`SmartTgtManager` trails **CO orders only** (`smart_tgt_manager.py:72`); CO is
never placed; therefore `sl_trail_count = 0` on 809/809. **Starved, not broken.**
It merges into UNIT2.

**DOES NOT PROVE:** that CO *should* be emitted, nor that `LIMIT_TRIPLE` is the
wrong choice.

### **DEFECT — confirmed by execution. Smart TGT folds into it.**

---

## D-A — KILL SCOPING

**MEASURED (static, this pass):**
- `is_active(intent)` accepts **`entry` / `exit` / `any`** — an action kind, with
  **no book/product dimension**.
- `kill_switch_state` is **one row, `CHECK (id = 1)`, no scope column**.
- `EMERGENCY_FLATTEN_PRODUCTS = frozenset({"MIS","CO"})` — **CNC excluded**, and
  `fire_now() → _fire() → _exit_open_positions()` reaches that filter at `:1086`
  and `:1460`.
- `cnc_gtt_monitor` never reads the kill state (see F11 (1)).

**PROVES:** Positions are **already book-scoped** (delivery survives a kill, by a
deliberate Rama-authored invariant). Authorisation is **not** scoped. And at least
one enforcement surface — the GTT monitor — is **outside kill control entirely**.

**DOES NOT PROVE — and I did not run it:** the two-book SOFT_KILL probe (§3 of the
brief). Executing it requires instantiating `KillSwitch` against the production
DB, which risks a **write** to `kill_switch_state`. There is no isolated DB in
this scratch environment tonight.

### **UNPROVEN — dynamic two-book probe NOT RUN. Reason stated, not stubbed.**

---

## ₹ CONSERVATION — S10

**MEASURED:** `NET_MARGIN_DELTA = +₹3,839.57` across all history with a **flat
book**. 330 RESERVE rows have no `reservation_id`-linked `RELEASE`/`RELEASE_USED`,
totalling **₹48,008.67**, spread across June (70), July (145), August (115).
**All 330 have `trade_id` empty.** Live bucket balances: intraday ₹7,336.29 +
positional ₹3,130.99 = **₹10,467.28 vs real capital ₹10,466.80** (Δ ₹0.48).

**PROVES:** The **₹48,008.67 is NOT missing money** — the buckets reconcile to
real capital within ₹0.48. Those releases happened but are **not linkable to their
RESERVE by `reservation_id`**, so reservation lifecycle **cannot be audited from
the ledger**. This is an **auditability defect**, and it is ongoing (115 in August).

**DOES NOT PROVE:** what the residual **₹3,839.57** is. It is far smaller than the
orphan total and remains unexplained.

### **DEFECT — ledger linkability. Plus ₹3,839.57 UNPROVEN.**

---

## WHAT THIS HARNESS CANNOT DO

It measures **what the code does**. ⛔ It does not measure whether the strategy
makes money. The ~38–39% win rate against ~43.5% breakeven is **untouched by every
finding above**, and none of these fixes changes it.

Two of the findings would **increase** risk if "fixed" naively: G2 raises position
size on a book with no edge, and S3 shows **46.7% of all signals rejected at
scores 57–59** — three points below `min_pass`. Lowering that threshold is the
single largest available change in throughput and is **exactly what the standing
ruling against backfill band rules forbids**.

## STAGES THAT COULD NOT HAVE GONE THE OTHER WAY

None. Every stage above had a measurable alternative outcome: S6 could have shown
refusals and did not; S7 could have shown CO orders and did not; S8's rejections
could have been broker-side and were not; S10's buckets could have failed to
reconcile and did not.
