# THE MIN RULE, AND THE TWO DELIVERY LIMITS — MEASURED

**22-Aug-2026 late evening, IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **`VERIFY AND REPORT ONLY` · ⛔ NO CODE · ⛔ NO CONFIG EDIT · ⛔ NO KEY DELETED · ⛔ NO PUSH · ⛔ NO DEPLOY.**
All `file:line` measured at **`742d9da`** (`M3` — they hold only there). The sizing math is
byte-identical to the deployed `4568385` (252-point grid, proven earlier), so every finding
applies to what is running today.

# 🔴 VERDICT: **PARTIALLY COMPLIANT**

- ✅ **Steps 1–5 of Rama's rule are implemented** for the three constraints that enter the
  minimum. His worked example reproduces **exactly**: **50 shares / ₹5,000**.
- 🔴 **Step 6 — "that is the final quantity" — is VIOLATED whenever the effective
  multiplier exceeds 1.0.** The multiplier is applied **after** the minimum and only **one**
  cap is re-applied afterwards — and that one **REJECTS rather than clamps**.
- ⚠️ **Today the system complies**, because `perf_weight` is hardcoded 1.0 and
  `tier_mult ≤ 1.0`, so the multiplier can only *reduce*. ⛔ **That is a CONDITION, not a
  property** (`N20-48`).
- ⚠️ Several numeric limits sit **outside** the minimum entirely and therefore do not
  participate in the rule at all.

---

# 🔴 B-1 — THE EXACT ORDER, AND THE CAP THAT IS NOT A CAP

| # | stage | `file:line` |
|---|---|---|
| 1 | `bucket = "intraday" if intent in _INTRADAY_INTENTS else "positional"` | `position_sizer.py:338` |
| 2 | resolve `eff_risk_pct` · `eff_conc_pct` · `eff_max_position_value_pct` — **segment-specific** | `:357-366` |
| 3 | `min_tick_size` guard → **REJECT** | `:411` |
| 4 | `risk_rs = total × eff_risk_pct` ; `qty_by_risk = floor(risk_rs / sl_distance)` | `:438-439` |
| 5 | `qty_by_risk > max_single_order_qty` → **REJECT** | `:443` |
| 6 | `qty_by_capital = floor(avail / margin_per_share)` | `:475-477` |
| 7 | `qty_by_concentration = floor(total × eff_conc_pct / entry_price)` | `:480` |
| 8 | ⭐ **`raw_qty = min(qty_by_risk, qty_by_capital, qty_by_concentration)`** ← **THE MIN** | **`:485`** |
| 9 | `effective_mult = tier_mult × max(0.0, perf_weight)` | `:524-527` |
| 10 | 🔴 **`tiered_qty = floor(raw_qty × effective_mult)`** ← **THE MULTIPLIER, AFTER THE MIN** | **`:584`** |
| 11 | `tiered_qty = max(1, min(tiered_qty, raw_qty × 2))` ← clamps only to **2× raw_qty** | `:587` |
| 12 | `final_qty = (tiered_qty // lot_size) × lot_size` ← **FLOOR** | `:611` |
| 13 | `lot_skew_rejection_threshold` → **REJECT** | `:615-617` |
| 14 | ⭐ **`position_value > eff_max_position_value_pct × total` → REJECT** ← the **only** post-multiplier cap | **`:648-650`** |
| 15 | `final_qty < lot_size or < min_qty_threshold` → **REJECT** | `:681` |

### The three questions, answered

**· Is the multiplier before or after the final cap?**
**AFTER the minimum (`:485` → `:584`)** and **BEFORE** the position-value cap (`:650`).

**· Is any cap re-applied after multiplication?**
**Exactly one** — the position-value cap at `:650`. The **risk** and **concentration** rungs
are ⛔ **never re-applied**. And the one that is re-applied **REJECTS the trade** (`qty=0`)
rather than clamping it to the cap.

**· CAN a capped quantity exceed its cap when `max_multiplier = 2.0`? — 🔴 YES. MEASURED.**

Live config, `total = ₹10,645.60`, entry ₹100, SL ₹99, tier HIGH:

```
concentration rung = 0.10 × 10,645.60 = ₹1,064.56  → 10 shares
perf_weight  raw  tiered  final   notional   constraint
       1.0    10      10     10   1,000.00   CONCENTRATION
       1.5    10      15     15   1,500.00   CONCENTRATION   ← exceeds the rung by 5
       2.0    10      20     20   2,000.00   CONCENTRATION   ← exceeds the rung by 10  (2×)
```

**The RISK budget is breached the same way** (entry ₹100, SL ₹90):
`risk budget = 0.01 × 10,645.60 = ₹106.46`; at `perf_weight=2.0` the delivered
`risk_amount = ₹200.00` — **1.88× the budget**.

**The DELIVERY book behaves identically** — `bucket=positional`, conc rung 10, final 20.

⚠️ **And the `constraint` label is itself misleading:** it still reports `CONCENTRATION`
while the delivered quantity is **twice** the concentration rung. A rejection/attribution
field naming a rung the result exceeds is a trap, not a diagnostic.

⚠️ **The position-value cap does NOT catch this case** — ₹2,000 < the ₹4,258.24 cap. When
it *does* catch it, the outcome is **`qty=0`, trade dropped** (see B-3), ⛔ not clamped.

**Reachability today — measured, and stated as a condition:** `perf_weight` reaches the
sizer only via `signal_processor.py:1009 / :1948 / :2265` as
`self._perf_weights.get(strategy_obj.name, 1.0)`, and `main.py:3141` constructs
`SignalProcessor` with **no `perf_weights` kwarg** ⇒ the dict is empty ⇒ **always 1.0**.
With `tier_mult ≤ 1.0`, `effective_mult ≤ 1.0` ⇒ the multiplier can only reduce.
🔴 **The day the PerformanceAllocator is wired, `max_multiplier: 2.0` makes the above LIVE.**

---

# B-2 — THE COMPLETE SET, IN AND OUT

### ✅ IN the `min()` — exactly THREE

| constraint | `file:line` | segment source |
|---|---|---|
| `qty_by_risk` | `:439` | `eff_risk_pct` — delivery key or global (`:357`/`:364`) |
| `qty_by_capital` | `:476` | `avail` = intraday/positional bucket + `leverage_map[intent]` |
| `qty_by_concentration` | `:480` | `eff_conc_pct` — delivery key or global (`:359`/`:365`) |

⚠️ `qty_by_flat` (`:597-598`) also enters a `min()` — **but only when `position_sizing.enabled = false`**. It is **true** today, so that rung is inert.

### ⛔ OUTSIDE the `min()` — every one of these

| limit | `file:line` | how it acts | delivery twin? |
|---|---|---|---|
| `min_tick_size` | `:411` | REJECT on `sl_distance` | ⛔ none |
| `max_single_order_qty` | `:443` | REJECT — ⚠️ **inspects only `qty_by_risk`**, before the min; a large `qty_by_capital`/`concentration` would not trip it | ⛔ none |
| `tier_multipliers` · `perf_weight` | `:584-587` | **MULTIPLY**, after the min | ⛔ none (one dict, both books) |
| `lot_size` | `:611` | FLOOR rounding | n/a |
| `lot_skew_rejection_threshold` | `:617` | REJECT | ⛔ none |
| `max_position_value_pct` | `:650` | **REJECT** (⛔ not clamp) | ✅ `delivery_max_position_value_pct` |
| `min_qty_threshold` | `:681` | REJECT floor | ⛔ none |
| `max_open_positions` · `max_daily_trades` · `max_open_delivery_positions` · `max_daily_delivery_trades` · `max_sector_exposure_pct` · `daily_loss_limit_pct` · `max_consecutive_losses` | `risk_engine` gates | approve/reject **after** sizing | ✅ for four of them |
| `min_depth_qty` (500) | `order_placer.py:684, :4074` | liquidity check **at placement** | ⛔ none — ⭐ the card was right not to trust its own list: this is **not** a sizing knob at all |

🔴 **A limit outside the `min()` does not participate in Rama's rule.** Of the numeric caps
above, only `max_position_value_pct` constrains the final quantity, and it does so by
**dropping the trade**.

---

# B-3 — RAMA'S EXAMPLE AGAINST THE REAL CODE

⚠️ His literal numbers do not occur at today's live config (`total ₹10,645.60` gives a
₹1,064.56 concentration rung, not ₹5,000), so the example was run with a sizer configured
to **his** numbers — labelled synthetic, and every rung is a real config knob:
`total ₹10,000 · conc 0.50 → 50 sh (₹5,000) · posv 0.70 → ₹7,000 (70 sh) · risk 0.01,
SL distance 1.0 → qty_by_risk 100`.

```
qty_by_risk          = 100      ("system computes 100")
qty_by_capital       = 350
qty_by_concentration = 50       (his 50-share cap, ₹5,000)
position-value cap   = ₹7,000   (= 70 shares)
raw_qty = min(...)   = 50
tiered_qty           = 50
FINAL qty            = 50       notional = ₹5,000.00   constraint=CONCENTRATION  success=True
```

## ⭐ **DOES THE REAL CODE PRODUCE 50? — YES.**

**At `perf_weight = 2.0`, the same example: `FINAL qty = 0`, `constraint = POSITION_VALUE_CAP`.**
The doubled 100 shares (₹10,000) breaches the ₹7,000 cap, so the trade is **rejected
outright**. ⇒ **Neither 50 nor a clamp — the signal is lost.** The exact stage that diverges
is **`:584` (multiply after the min)** with **`:650`** as a reject-only backstop.

⇒ Two distinct failure modes above 1.0: **(a)** doubled quantity stays under the
position-value cap → **placed at up to 2× the binding rung**; **(b)** doubled quantity
breaches it → **trade dropped entirely**.

---

# B-4 — SEGMENT SELECTION

`position_sizer.py:356-366`:

```python
if bucket == "positional":
    eff_risk_pct               = self._require_delivery(self._delivery_risk_per_trade_pct, ...)
    eff_conc_pct               = self._require_delivery(self._delivery_max_concentration_pct, ...)
    eff_max_position_value_pct = self._require_delivery(self._delivery_max_position_value_pct, ...)
else:
    eff_risk_pct = self._risk_per_trade_pct   # …global…
```

✅ **Every rung that uses a percentage takes the SELECTED SEGMENT'S OWN key**, and
`_require_delivery` (`:198-225`) has **no `else` returning a global** — a missing delivery
value **raises**, naming the key. `qty_by_capital` is segment-specific by construction
(`positional_avail` + `leverage_map["DELIVERY"]`). **F1's architecture holds on the live
sizing path.** ⛔ No fallback semantics reintroduced; ⛔ no key deleted; missing is never
"unlimited".

⚠️ **But the segment split is partial, and that is a fact not a complaint:**
`min_tick_size`, `max_single_order_qty`, `lot_skew_rejection_threshold`,
`min_qty_threshold` and `tier_multipliers` are **global for both books** — they have no
delivery twin (the §10 parity list). A delivery order is therefore sized on delivery
percentages but screened on intraday guards.

---

# B-5 — ROUNDING

`final_qty = (tiered_qty // lot_size) * lot_size` — `position_sizer.py:611`.

- **What is rounded:** the post-multiplier quantity, to a whole number of lots.
- **Direction:** **FLOOR** (integer floor-division). ⛔ Never nearest, ⛔ never ceil.
- **Order:** lot normalisation happens **after** the multiplier and **before** the
  position-value cap (`:611` → `:650`), so the cap is evaluated on the *rounded* quantity.
- **Can rounding push the result above a cap? — NO.** Floor can only reduce.

⚠️ One adjacent behaviour worth naming: `:587`'s `max(1, …)` **floors the result at 1
share**, so a multiplier that computes 0 still yields 1. That cannot breach a cap
(`raw_qty ≤ 0` is already rejected at `:506`), but it does mean **the tier multiplier can
never size a signal below one share** — a floor, not a cap violation.

---

# A-1 / A-2 / A-3 — THE TWO DELIVERY LIMITS. ⛔ **DELETE NEITHER.**

## A-1 · Enforcement sites (⛔ config definitions are not enforcement sites)

| limit | enforcement | check |
|---|---|---|
| `max_open_delivery_positions` | **`risk_engine.py:544`**, inside `if sizing_result.bucket == "positional":` at the **OPEN_POSITIONS** gate | `if open_delivery_count >= self._max_open_delivery` |
| `max_daily_delivery_trades` | **`risk_engine.py:632`**, inside `if sizing_result.bucket == "positional":` at the **DAILY_TRADES** gate | `if daily_delivery_count >= self._max_daily_delivery` |

State fetched once at `:311` and `:313`; passed to `_run_checks` at `:384`.

## A-3 · They inspect **DIFFERENT STATE** — proven by the SQL, ⛔ not argued

| | `count_open_delivery_positions()` | `count_daily_delivery_trades(date)` |
|---|---|---|
| **date filter** | ⛔ **none** — all time | ✅ `SUBSTR(t.created_at,1,10) = ?` |
| **status set** | `('OPEN','PARTIAL','PENDING_FILL')` — 3, all *currently live* | `_EXECUTED_TRADE_STATUSES` = `('PENDING_FILL','OPEN','PARTIAL','EXITING','CLOSED','CLOSED_MANUAL')` — **6, including CLOSED** |
| **measures** | **concurrency** | **throughput** |

⭐ **The decisive discriminator:** `CLOSED`, `CLOSED_MANUAL` and `EXITING` are counted by
the daily query and **not** by the open query. A trade opened and closed the same day
**consumes a daily slot but frees the concurrency slot** — which is exactly the worked case
(open 3, all exit by noon, open 2 more ⇒ 5 that day, never more than 3 open).
⇒ 🔴 **NOT aliases. NOT duplicates. ⛔ Neither may be deleted** — and NI-4 has just made
both fail-closed, so deleting either would also undo that.

## A-2 · Has each ever bound? — searched the live record (160,850 signals, 702 trades)

| limit | rejections | detail |
|---|---|---|
| `max_open_delivery_positions` | 🔴 **9** | **2026-08-06** ×7 (TATATECH, KABRAEXTRU ×2, BATLIBOI, VRLLOG, TATATECH, MMP) · **2026-08-12** ×2 (ARE&M, CPCAP) — all *"Delivery position cap reached: 3 open delivery (CNC), max=3"* |
| `max_daily_delivery_trades` | ⚪ **0 — it has NEVER bound** | ⛔ still not a reason to delete it |

**CONTROL — the same query shape is not blind:** any rejection 160,292 · CONCENTRATION
3,766 · global position cap 558 · global daily trade limit 5,146.

### ⚠️ A contradiction I chased rather than glossed

Raw CNC ENTRY rows per day reach **8 (21-Aug)**, 7 (20-Aug), 6 (17-Aug, 05-Aug) — all above
the cap of 5, yet the daily cap recorded **zero** rejections. **Resolved by measurement:**
most of those rows are status **`FAILED`**, which `_EXECUTED_TRADE_STATUSES` **excludes**.
The quantity the cap actually counts was **3 / 3 / 2 / 2** on those days — below 5.

⇒ ✅ **Correct behaviour** (FIX-181's stated design: a trade that never opened must not
consume the slot), ⛔ not a defect. ⭐ And it is a second, empirical proof of A-3: on 21-Aug
the *raw* count was 8 while the *counted* quantity was 3 — the two measures visibly differ.

⭐ **Operational information worth stating plainly: the delivery book has never taken more
than 3 executed CNC entries in a day, against a cap of 5. `max_daily_delivery_trades` has
no observed binding history — it is a bound that has not yet been tested by live traffic.**

---

# RELATIONSHIP TO F1 AND NI-4

⛔ **F1 is not reopened.** F1's contract — *a delivery entry reads only delivery keys, and a
missing one raises* — is **confirmed live** on the sizing path (B-4). ⛔ NI-4 preserved: no
key deleted, no default restored, no cross-segment substitution.

🔴 **NEW FINDING, recorded as its own item — `NI-16`:**

- **FACT** — the tier/perf multiplier is applied at `position_sizer.py:584` **after** the
  `min()` at `:485`, and neither the risk nor the concentration rung is re-applied
  afterwards. The only post-multiplier cap (`:650`) **rejects** instead of clamping.
- **EVIDENCE** — measured on the live config: at `perf_weight=2.0` a 10-share concentration
  rung delivers **20 shares / ₹2,000**, and a ₹106.46 risk budget delivers **₹200.00** of
  risk; in Rama's own example the same input yields **`qty=0, POSITION_VALUE_CAP`**.
- **IMPACT** — `LATENT`, ⛔ not `LIVE`: `perf_weight` is always 1.0 today because
  `main.py:3141` passes no `perf_weights`. It becomes **LIVE the moment the
  PerformanceAllocator is wired**, with `max_multiplier: 2.0` already in config.
- **PROPOSED FIX** — ⛔ **none built, none designed.** The shape would be a re-cap of
  `tiered_qty` against the same rungs after `:584` (a clamp, not a reject). ⛔ Requires its
  own authorisation, its own gate, and a frozen prediction. ⛔ **Not started.**

⭐ This is also the missing half of **NI-2**: C2 now audits the *config* for that hazard;
nothing re-caps the *runtime* result.

---

# ADDENDUM — NI-16's PRECONDITION, THE DESIGN QUESTION, AND THREE SEPARATED FINDINGS

**22-Aug-2026, very late.** ⛔ RECORD ONLY — ⛔ no code, ⛔ no config edit, ⛔ `max_multiplier`
untouched, ⛔ NI-16 not designed and not built, ⛔ no push, ⛔ no deploy.

## 🔴 §0 — FIRST, A CORRECTION TO MY OWN CLAIM: **NI-16's ORDERING IS NOT A NEW DISCOVERY**

`docs/MASTER_PENDING_01-Aug-2026.md` already records it, verbatim:

> The five axes describe **caps**. The **tier multiplier** is applied **after** the caps
> (`raw_qty × tier_multiplier`) and has **no entry anywhere in any inventory** — yet it is a
> permanent ×0.5 on 438/438 trades. ⚠️ **`dynamic_by_winrate` (min 0.5 / max 2.0,
> `system_config.yaml:182-184`) is a SECOND modifier, equally uninventoried — and unlike the
> tier it can move size in both directions.**

⇒ ⛔ **I should not present "the multiplier sits after the caps" as a finding. It was already
on the record**, together with the observation that `dynamic_by_winrate` can move size in
**both** directions.

⭐ **What NI-16 actually adds, and only this:**
1. the **measured consequence** — 20 shares against a 10-share concentration rung; ₹200.00
   of risk against a ₹106.46 budget;
2. that **nothing re-caps** afterwards;
3. that the one post-multiplier cap **REJECTS rather than clamps**, so the same input either
   over-sizes *or* drops the signal.

## 🔴 §1 — THE PRECONDITION, WRITTEN ONTO THE ALLOCATOR WORK

**The allocator item is `N9-10` in the register** — *"The `PerformanceAllocator`
ONE-ALLOCATION CEILING — LOCKED"*, status **CLOSED (decision final)**.

> **PRECONDITION ON ANY PerformanceAllocator WIRING (`N9-10`), TO BE CARRIED ON THAT ITEM'S
> FACE — ⛔ not only in NI-16's row:**
>
> 🔴 **WIRING `PerformanceAllocator` WITHOUT RESOLVING NI-16 FIRST WOULD IMMEDIATELY BREACH
> TWO LIVE RISK LIMITS — CONCENTRATION AND THE RISK BUDGET — ON EVERY HIGH-TIER TRADE,
> SILENTLY, WITH `max_multiplier: 2.0` ALREADY IN THE CONFIG.**
>
> Measured: at `perf_weight=2.0` a 10-share concentration rung delivers **20 shares
> (₹2,000 vs a ₹1,064.56 rung)** and a ₹106.46 risk budget delivers **₹200.00** of risk.
> The `constraint` field still reports `CONCENTRATION`.

⚠️ **`dynamic_by_winrate: true` is already in the config** and F11 records it as *"logging
and gating nothing"* — ⇒ **someone intends to wire this.** The precondition must travel
with the task, ⛔ not sit only in a defect list. A defect in one list and a task in another
is how the 08-Aug build got lost.

### 🔴 §1b — AND `N9-10` MAY ALREADY ANSWER THE DESIGN QUESTION. ⛔ I CANNOT CHECK.

`N9-10`'s locked text:

> *"Performance and tier may move a trade's allocation up or down **WITHIN the single-allocation
> ceiling** — ⛔ they may never spend a second trade's allocation."* ⚠️ NOT "inert":
> LOW/MEDIUM can still be lifted toward full; **only HIGH is fully clipped.**
> …verified by `test_the_multiplier_is_clamped_to_one_and_scaling_is_monotonic`

Three things follow, and they matter:

1. ⭐ **The locked intent is that the multiplier may lift a LOW/MEDIUM trade *toward* full —
   ⛔ NOT above it.** *"Within the single-allocation ceiling"* is exactly the clamp NI-16
   says is missing. On that reading NI-16 is **a deviation from an already-locked decision**,
   ⛔ not an open policy question.
2. ⭐ The named test is **`test_the_multiplier_is_clamped_to_one…`** — *clamped to one*.
3. 🔴 **But `N9-10` is recorded against the allocation model `65b7196`, which is BUILT and
   NEVER DEPLOYED.** So the clamp may exist **only in that tree** and not in the deployed
   code — which is precisely the *"F1 re-implements it"* pattern already on the record.

⛔ **I did NOT read `65b7196`.** The standing instruction — *"not revived, not merged, not
read, not deleted"* — has never been lifted, and the ledger's provenance questions ①②③ are
still open. ⇒ 🔴 **Whether the clamp NI-16 asks for already exists in `65b7196` is
UNRESOLVED, and resolving it requires Rama lifting that instruction.** ⭐ That is a cheaper
question than either fix shape below, and it should probably be asked first.

## §2 — TWO FIX SHAPES. ⛔ NEITHER CHOSEN. ⛔ `max_multiplier` UNTOUCHED.

⚠️ **The tension is at the level of DESIGN, not code.** *"Whichever is low wins"* and a
multiplier that can exceed the minimum are not reconcilable — a ×2.0 exceeding a cap is
**what a ×2.0 is for**.

| | shape | cost | what it decides |
|---|---|---|---|
| **(α)** | **RE-CAP AFTER THE MULTIPLIER** — clamp `tiered_qty` back against the same rungs after `position_sizer.py:584` | **Code**: a unit + its own gate + a frozen prediction | Keeps the ×2.0 capability but makes it unable to exceed anything — ⚠️ which raises what the upside is *for* |
| **(β)** | **CAP `max_multiplier` AT 1.0** — the multiplier may only ever REDUCE | **No code at all** — a one-value config change | NI-16 disappears by construction. ⚠️ But it is a **POLICY** change: it retires an upside capability someone designed in |

⭐ **(β) needs no code; (α) needs a unit.** ⛔ Neither is chosen, ⛔ nothing was changed, and
⛔ `max_multiplier` was not touched. ⚠️ **And per §1b, `N9-10` may mean the policy is already
settled in (β)'s direction — check that before spending anything on (α).**

## §3 — THREE FINDINGS, OPENED SEPARATELY (⛔ not folded into NI-16)

### ⚠️ NI-17 · `max_single_order_qty` INSPECTS THE WRONG QUANTITY
`position_sizer.py:443` tests `qty_by_risk > self._max_single_order_qty` — **before** the
`min()` at `:485`, and against **one rung only**. ⇒ a large `qty_by_capital` or
`qty_by_concentration` would ⛔ **never trip it**. ⭐ A cap that guards one *input* instead of
the *output*. Same family as **NI-2** (a check omitting a term) and **config_auditor group
F** (a guard that skips its own row). 🏷️ `MEASURED · ⛔ NOT FIXED`.

### ⚠️ NI-18 · THE `constraint` LABEL LIES WHEN THE MULTIPLIER IS ACTIVE
It reports `CONCENTRATION` while delivering **twice** the concentration rung (measured).
⭐ An attribution field naming a rung the result exceeds is a **trap, not a diagnostic** —
the same family as **NI-1**, a warning that did not warn. ⚠️ Whoever debugs the allocator
will be actively misled by it, at exactly the moment NI-16 goes live.
🏷️ `MEASURED · ⛔ NOT FIXED`.

### ⚠️ NI-19 · THE SEGMENT SPLIT IS PARTIAL
✅ B-4 confirms F1's contract holds — percentage rungs read the **selected segment's own
keys** and a missing one **raises**. ⚠️ But `min_tick_size`, `max_single_order_qty`,
`lot_skew_rejection_threshold`, `min_qty_threshold` and `tier_multipliers` are **global for
both books**. ⇒ **A DELIVERY ORDER IS SIZED ON DELIVERY PERCENTAGES BUT SCREENED ON INTRADAY
GUARDS.** That is the §10 parity list with a live consequence attached.
🏷️ `MEASURED · ⛔ NOT FIXED · ⛔ NO KEY CREATED`.

## §4 — CLOSED: THE TWO DELIVERY LIMITS · ⛔ DELETE NEITHER

| | `count_open_delivery_positions()` | `count_daily_delivery_trades(date)` |
|---|---|---|
| date filter | ⛔ none | ✅ `SUBSTR(created_at,1,10)=?` |
| statuses | `OPEN, PARTIAL, PENDING_FILL` (3, live) | `_EXECUTED_TRADE_STATUSES` (6, **incl. CLOSED / CLOSED_MANUAL / EXITING**) |
| measures | **CONCURRENCY** | **THROUGHPUT** |
| enforced at | `risk_engine.py:544` (OPEN_POSITIONS) | `risk_engine.py:632` (DAILY_TRADES) |

**History, plainly:** `max_open_delivery_positions` has bound **9 times** (06-Aug ×7,
12-Aug ×2). `max_daily_delivery_trades` has **never bound** — the delivery book has never
taken more than **3** executed CNC entries in a day against a cap of 5.
⚠️ **An untested bound is still not a redundant one.**
✅ The `FAILED`-status resolution is **correct behaviour** per FIX-181 — a trade that never
opened must not consume a slot. ⛔ Not a defect.

## §5 — A POSITIVE RESULT, RECORDED AS ONE

⭐ **F1's contract is CONFIRMED LIVE on the sizing path.** `position_sizer.py:356-366`: a
positional entry resolves all three percentages through `_require_delivery`, which has **no
`else` returning a global**; a missing delivery value **raises and names the key**. ⛔ F1 was
not reopened — this audit **confirms** it. That is a genuine positive and is recorded as one.

⭐ **NI-16 is the missing half of NI-2, and the pairing is the point:** NI-2 made C2 audit
the **config** for this hazard; ⛔ **nothing re-caps the RUNTIME result.** That is the
difference between **an audit and a control** — and it is the F11 shape again.

---

# ADDENDUM 2 — Q-1/Q-2/Q-3, THE PATTERN ROW, AND A CORRECTION TO MY OWN ATTRIBUTION

**22-Aug-2026, very late (into 23-Aug).** ⛔ RECORD ONLY — ⛔ no code, ⛔ no config edit,
⛔ `max_multiplier` untouched at 2.0, ⛔ no push, ⛔ no deploy, ⛔ **`65b7196` NOT read**.

## 🔴 §0 — A CORRECTION I OWE: **N9-10 NAMES NO COMMIT AT ALL**

I reported that *"`N9-10` is recorded against the allocation model `65b7196`"*. **That was
an INFERENCE, and I stated it as fact.** Measured: the `N9-10` row names **no SHA** — it
cites *"build record §4.1"* and the test name
`test_the_multiplier_is_clamped_to_one_and_scaling_is_monotonic`, and its status column says
*"Reopen only by Rama revisiting the allocation model."*

The link to `65b7196` comes from the **ledger's separate** statement that the allocation
model *is* `65b7196` — a reasonable join, but a join. ⇒ ⭐ **`N9-10` cannot be checked by
ancestry at all, because it points at a document and a test name rather than a commit.**
That is a sharper fact than the one I asserted, and it changes §4's question: the answer may
not even be in `65b7196`.

## §1 — Q-1 · THE COUNT, FIRST

Swept all **43** N-id rows in `docs/MASTER_PENDING_01-Aug-2026.md`; **138** SHA-shaped
tokens; every candidate resolved with `git rev-parse` and tested with
`git merge-base --is-ancestor <sha> 4568385`. ⛔ No undeployed tree content was opened —
ancestry is a graph question, not a content question.

| category | count | meaning |
|---|---|---|
| **A** — CLOSED/LOCKED row naming a **non-ancestor** commit, **not** labelled unpushed | 🟢 **0** | **the dangerous class is EMPTY** |
| **B** — same, but the row **itself says NOT PUSHED** | **3** | honestly recorded |
| **C** — CLOSED/LOCKED row naming **no commit at all** | **8** | ancestry **cannot** check them |

**CONTROL** (the machinery is not blind): `4568385` → ANCESTOR · `7fc5d5a` → ANCESTOR ·
`d00e574` → NOT an ancestor. ✅ It distinguishes correctly.

## §2 — Q-3 · **THIS IS HOUSEKEEPING, NOT SYSTEMIC**

⭐ **Category A is ZERO.** ⇒ ⛔ **The register is NOT "describing a system that does not
exist."** No closed decision is quietly recorded against code that never shipped while
presenting itself as delivered. **This does not outrank the NI items.**

### Category B — all three name themselves

| row | commit(s) | the row's own words |
|---|---|---|
| `N9-18` | `0337378`, `43f73b1` | *"TICK 2 BUILT — `<BUILT · TESTED · COMMITTED … · NOT PUSHED>`"* |
| `N9-20` | `071169b` | *"ALERT PHASE 2 — `<BUILT · TESTED · COMMITTED … · NOT PUSHED>`"* |
| `N9-07` | `7649cd8` | *"CLOSED-AS-BUILT — `<BUILT · TESTED · COMMITTED … · NOT PUSHED>`"* |

⇒ ⭐ **The `<BUILT · … · NOT PUSHED>` status label is doing exactly the job it was created
for.** These are not inert entries; they are correctly-labelled unpushed work.

### Q-2 for `N9-07` — ⭐ ancestry says NO, **substance says YES**

```
register names : 7649cd8  2026-08-09 16:27:49  fix(forward-shadow): N9-07 — name the encoding …
deployed       : 4568385  2026-08-20 20:14:10  fix(forward-shadow): N9-07 — name the encoding …
identical patch text : True   (8,539 bytes vs 8,539)
same files           : scripts/forward_shadow_record.py · tests/unit/test_n907_forward_shadow_encoding.py
```

⇒ **A CHERRY-PICK.** Different SHA, byte-identical change, and **the change IS on the
deployed path**. ⚠️ **This is why Q-2 exists and why an ancestry test alone would have been
wrong:** it would have reported N9-07 as undelivered when it is live. `N9-18` and `N9-20`
remain genuinely unpushed.

### Category C — the 8 that ancestry cannot speak to

`N10-02` · `N10-06` · **`N9-10`** · `N9-13` · `N9-15` · `N9-19` · `N9-25` · `N9-26`.

⚠️ These name no commit, so **no mechanical check can confirm or deny their
implementation.** Most are measurement/decision rows for which that is appropriate
(`N9-13` is a withdrawal, `N9-15` is measure-only, `N9-25` is a flapping test). ⭐ **`N9-10`
is the one where it matters**, because it asserts a *behaviour* — a clamp — that the
deployed code **measurably does not have** (NI-16).

## §3 — 🔴 THE PATTERN, AS ITS OWN ROW — **`F12 · THE ALREADY-BUILT ANSWER`**

> **TWICE IN ONE DAY, SOMETHING TREATED AS UNBUILT TURNED OUT TO EXIST IN A BUILT, TESTED,
> NEVER-DEPLOYED TREE — AND BOTH TIMES IT WAS FOUND BY ACCIDENT, WHILE LOOKING FOR SOMETHING
> ELSE.**
>
> 1. **F1's null-fails-closed rule** — `capital/pipeline_policy.py:226-238` in `65b7196`
>    already implements it, for the same three keys, against the same stale scaffold comment.
> 2. **The multiplier clamp** — `N9-10`'s *"within the single-allocation ceiling"*, with a
>    test named `…clamped_to_one…`.
>
> 🔴 **The cost is NOT the rediscovery. It is the risk of building a SECOND, DIFFERENT
> solution to the same problem — two mechanisms for one rule**, which is precisely what this
> campaign exists to avoid.

⚠️ **F12 is distinct from F11.** F11 = *a control that exists, runs, and constrains nothing*.
**F12 = a control that was built and never reached the system at all.** Same family — a
mechanism that is not doing its job — but a different failure mode and a different remedy.

🏷️ `OPENED · ⛔ NOT STARTED · ⛔ NOT DESIGNED.`

## §4 — 🔴 `N9-10`'s STATUS IS A FINDING. ⛔ ITS STATUS WAS NOT CHANGED.

`N9-10` is marked **"✅ CLOSED (decision final) — kept for record"** and asserts a clamp that
the deployed sizer **measurably does not apply** (NI-16: 20 shares against a 10-share rung).

⇒ ⭐ **An inert entry in the GOVERNANCE layer** — a record that reads healthy while nothing
enforces it. Same shape as NI-14 (a threshold that always fires), NI-15 (a watch list that
misses its target), the alert guard, and `config_auditor` group F — ⚠️ **except this one is
one floor up, in the register rather than the code.** A reader trusting the register would
believe the multiplier is clamped. It is not.

⛔ **`N9-10`'s status was NOT changed.** Its status is the finding, ⛔ not an error to correct.

## §5 — THE QUESTION FOR RAMA · ⛔ ASKED, ⛔ NOT ACTED ON

> **"Do you authorise reading `65b7196` — READ ONLY — solely to verify whether `N9-10`'s
> clamp-to-one behaviour is implemented there, and to compare it against the deployed path?"**

- **IF NO** → `65b7196` stays unread; `N9-10` remains **policy evidence only**; the
  multiplier question stays open and ⛔ no fix is designed.
- **IF YES** → read **only** the allocator/multiplier implementation and its provenance.
  ⛔ No merge · ⛔ no revive · ⛔ no deploy · ⛔ no modify · ⛔ no delete · ⛔ nothing beyond
  that scope.

⭐ **The cost, honestly:** this is **cheaper than either fix shape**, and it may show that no
design decision is needed because the project already made it.
⚠️ **But note §0** — `N9-10` names no commit, so `65b7196` is the *likely* home of the clamp,
⛔ not a certain one. The read may come back empty, and that too would be an answer.

⛔ **Until he answers: ⛔ no design choice · ⛔ no code · ⛔ no config change ·
`max_multiplier` UNTOUCHED at 2.0 · `65b7196` UNREAD.**

---

# ADDENDUM 3 — CORRECTIONS RECORDED · THE AUTHORISATION FLAG · THE READ SEQUENCED

**23-Aug-2026 (Sunday), early.** ⛔ RECORD ONLY — ⛔ no code, ⛔ no config edit,
⛔ `max_multiplier` untouched at 2.0, ⛔ no push, ⛔ no deploy, ⛔ **`65b7196` NOT read.**

## §1 — TWO CLAIMS REFUTED, AND THE ONE THAT SURVIVED IS BETTER

| claim | verdict |
|---|---|
| *"`N9-10` is recorded against `65b7196`"* | ⛔ **FALSE** — the row names **no commit**. It cites *"build record §4.1"* + the test name; the `65b7196` link came from the **ledger's separate** statement. ⇒ `N9-10` **cannot be settled by ancestry**, and the clamp **may not even be in `65b7196`** — an empty read is a real possible answer |
| *"the register may be describing a system that does not exist"* | ⛔ **REFUTED** — Category A = **0** across 43 rows / 138 SHA tokens, with a working control. The register is doing its job; all three Category-B rows label themselves `BUILT · TESTED · COMMITTED · NOT PUSHED`. **Housekeeping, ⛔ not systemic, ⛔ does not outrank the NI items** |

⭐ **Both were inferences stated as facts** — the same shape as the `N9-10` attribution
itself. Recorded as instances, ⛔ not smoothed over.

### 🔴 THE SURVIVING RESULT IS A METHOD RULE

`N9-07` names `7649cd8`, **not an ancestor** of deployed `4568385` — yet its patch is
**byte-identical to `4568385`** (8,539 B, same two files). **A cherry-pick.**

> 🔴 **ANCESTRY SAYS NO; SUBSTANCE SAYS YES.**
> ⛔ **NEVER use an ancestry test alone to conclude "not delivered."**

⇒ **`N9-07`'s row has been ANNOTATED in the register** — the cherry-pick equivalence, the
byte-identity, and the method lesson — **with its status label `<BUILT · COMMITTED · NOT
PUSHED · NOT DEPLOYED>` left verbatim and unchanged.** ⛔ A historical decision is not
rewritten to absorb a later measurement.
✅ Register integrity verified after the edit: **2,687 lines before and after**, `N10-` row
count **18 = 18**, **0 CR bytes**. Backup taken first (`md5 4b46dd2e…`).

## §2 — 🔴 THE AUTHORISATION FLAG · **WC-PATTERN #8, RECURRENCE**

ChatGPT's §10 reads: *"ANSWER: YES — AUTHORISED, BUT STRICTLY NARROW."*

⛔ **A reviewer cannot lift a restriction.** The question was **put and remains
UNANSWERED**; Rama has not spoken. This is the **second** instance of the same pattern —
`WC-PATTERN #8` was a reviewer authorising the MIS 3.5× change on his behalf. ⇒ recorded as
a **recurrence of #8**, ⛔ not a new class.

⭐ ChatGPT's scope conditions are **good and should be adopted if he says yes** — ⛔ but they
are a **proposed scope, ⛔ not permission.** The restriction stays in force.

## §3 — 🔴 SEQUENCING THE READ — AND A CORRECTION TO THE CARD'S OWN PREMISE

The card frames **R-1** (*read `docs/audit/order_sizing_allocation_build_08aug2026.md` §4.1*)
as *"a DOCUMENTATION read, narrower than reading code"* that *"may settle the question
without opening a single source file."*

**Measured, by metadata only — ⛔ the file was NOT opened:**

```
git log --diff-filter=A -- docs/audit/order_sizing_allocation_build_08aug2026.md
  -> 65b7196  feat(sizing): the allocation model -- the stop moves the money, not the size
  -> 65b7196 is NOT an ancestor of deployed 4568385
  -> tracked on: feat/delivery-config-split, feat/tier-multipliers-61-62
  -> 32,886 bytes, 545 lines
```

🔴 **THE BUILD RECORD WAS ADDED BY `65b7196` ITSELF. R-1 IS NOT AN ALTERNATIVE TO READING
`65b7196` — R-1 *IS* READING `65b7196`.** It is narrower in *what it reveals*, ⛔ but it is
**inside** the restriction, ⛔ not outside it. **The authorisation gate applies to R-1 exactly
as it does to R-3.**

⚠️ **A second consequence, stated plainly:** the file is **already on disk** in the root
worktree, because that worktree sits on `feat/delivery-config-split` — a descendant of
`65b7196`. ⇒ The restriction protects against **opening** it, ⛔ not against obtaining it.
**I have not opened it.**

⚠️ **And the card's own figure is slightly stale:** it says *"519 lines"*; measured **545**.
Minor, ⛔ but recorded rather than skipped.

### The sequence, unchanged in order and now correctly labelled

| step | scope | gate |
|---|---|---|
| **R-1** | build record **§4.1 only** | 🔴 **needs Rama's authorisation — it is `65b7196` content** |
| **R-2** | only if R-1 inconclusive: the named test `test_the_multiplier_is_clamped_to_one_and_scaling_is_monotonic` | same gate |
| **R-3** | only if R-2 inconclusive: the allocator/multiplier implementation it exercises, ⛔ nothing else | same gate |
| **R-4** | compare **that behaviour only** against deployed `4568385` / `742d9da` — ⚠️ **and per the `N9-07` lesson, check whether an equivalent rule already exists on the deployed path BY ANOTHER MECHANISM. ⛔ Absence from one file is not absence from the system** | no gate — deployed tree |

⭐ Narrowest-first is still the right order. ⛔ **PROHIBITED throughout:** merge · cherry-pick ·
revive · modify · delete · deploy · config change · any exploration of unrelated `65b7196`
content · treating `65b7196` as a candidate implementation.

## §4 — HOLDS

⭐ **`F12` · THE ALREADY-BUILT ANSWER** — opened, distinct from `F11` (**F11** = a control
that *runs* and constrains nothing; **F12** = a control that was *built* and never reached
the system). ⚠️ **Item 2 phrased carefully:** the clamp is **strongly indicated** by `N9-10`'s
build/test citation and **suspected** to live in the allocation model — ⛔ **not a verified
fact about `65b7196`.**

⭐ **`N9-10` — status UNCHANGED** (`CLOSED · decision final`). ⚠️ The discrepancy **is** the
finding: governance asserts a single-allocation ceiling; the deployed runtime measurably
does not enforce it above multiplier 1.0.

⭐ **NI-16 — reframed:** ⛔ not *"we discovered the ordering"* (`MASTER_PENDING` recorded it
verbatim), ⭐ but *"we measured what that known ordering does at multiplier > 1, and proved
nothing re-caps"* — and possibly **a deviation from an already-closed decision** rather than
an open policy question.

⛔ **`max_multiplier` UNTOUCHED at 2.0.** ⛔ Not reduced, ⛔ not re-capped. ⚠️ Changing it now
could **erase the intended LOW/MEDIUM upward scaling toward the ceiling rather than implement
the ceiling** — the two are not the same thing.

⛔ NI-17 · NI-18 · NI-19 — MEASURED, ⛔ NOT FIXED, ⛔ separate. ⛔ Both delivery limits KEPT.
⛔ F1 not reopened. ⛔ No further broad ancestry sweep. ⛔ The read NOT started.
