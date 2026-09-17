# S-3 PROVEN LIVE · AND A MEASURED P&L-RESET WINDOW · 28-Aug-2026

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ NOT EXERCISED.
🔬 Read-only observation, `52ccb4f` deployed. ⛔ Nothing was changed to produce it.

> ## ⚠️ **CORRECTED 28-Aug ~16:2x — MY ORIGINAL HEADER OVERSTATED THIS. SEE §1a.**
> ⛔ **RETAINED, SUPERSEDED:** *"S-3 IS NOW BEHAVIOURALLY PROVEN… The 15:17 EOD
> routine ran for the first time ever with a live CNC GTT on the book, and left it
> untouched."*
>
> ⭐ **WHAT THE MEASUREMENT ACTUALLY SUPPORTS:** an **ACTIVE `gtt_state` row**
> existed across the 15:17 routine and was not disturbed by it. 🔴 **The BROKER
> POSITION was already flat** — `get_positions` returned **0 positions** from
> **15:10:53** onward. ⇒ ⛔ The behavioural leg says **nothing** about the product
> filter rejecting a CNC position; ⭐ the product boundary rests on the
> **structural** and **mutation** legs only.

---

## 1 — 🔬 THE OBSERVATION · RAMRAT, CNC, ACTIVE GTT, ACROSS 15:15 AND 15:17

**Pre-state, captured 13:30:24** — armed hours in advance, ⛔ not reconstructed after:

```
open CNC   : RAMRAT | OPEN | CNC
gtt_state  : 333737122 | RAMRAT | ACTIVE | 2026-08-28T13:17:21.979642+05:30
```

**The window, verbatim:**

```
15:15:01.895  order_monitor  force_close_triggered  force_close_time=15:15  watched_count=0
15:15:01.895  CRITICAL main  circuit_breaker.force_close_triggered: soft_kill,
                             EOD squareoff handles positions
15:15:01.897  CRITICAL       SOFT_KILL ACTIVATED reason=circuit_breaker_force_close_15:15
────────────────────────────────────────────────────────────────────────────────
15:17:01.460  eod_squareoff  EOD square-off triggered for 2026-08-28
15:17:01.465  eod_squareoff  EOD Pass 1: canceling all pending orders
15:17:01.466  eod_squareoff  EOD Pass 1 complete: 0 orders cancelled
15:17:03.488  eod_squareoff  broker-position filter kept 0/0 trades (broker open symbols=0)
15:17:03.509  eod_squareoff  EOD Pass 2 complete: 0 open positions exited
15:17:03.523  eod_squareoff  FIX-047: WAL checkpoint complete
15:17:03.528  fund_manager   reset_daily_pnl  previous_pnl=-9.74
────────────────────────────────────────────────────────────────────────────────
15:19:13.288  cnc_gtt_monitor  gtt_exit  RAMRAT  exit_price=592.3  pnl=-2.18
```

### ✅ WHAT THIS PROVES, POINT BY POINT

| claim | 🔬 live evidence |
|---|---|
| the 15:15 control is **SOFT_KILL-only, observed at `watched_count = 0`** | 🔬 `watched_count=0`, SOFT_KILL only, ⛔ no cancel, ⛔ no exit. ⚠️ 🏷️ **W-2: this is proven ON AN EMPTY WATCH LIST.** The stronger case — `watched_count > 0` and it still closes nothing — is **NOT EXERCISED**. ⛔ Do not read this row as fully proven; ⭐ the 15:17 rows below are the strong evidence. |
| 15:17 **Pass 1** cannot reach a CNC GTT | *"canceling all pending orders"* → 🔬 **"0 orders cancelled"**, with `333737122` **ACTIVE** at that instant |
| 15:17 **Pass 2** cannot select CNC | `broker open symbols=0` — the `{MIS, CO}` filter excluded the CNC position |
| the GTT **survived intact and still worked** | RAMRAT exited **15:19:13** through its own `cnc_gtt_monitor` path, **2 min AFTER** the EOD routine, `gtt_state → CLEANED` |

### 🔴 §1a — THE CORRECTION, MEASURED · ⛔ TWO OF MY CLAIMS AND ONE OF FILE 30's WERE WRONG

🔬 **`get_positions` returned `0 positions` at `15:17:03.488`** — and at every sample
from **`15:16:11`** onward. 🔬 The whole-day transition list shows the book went to
zero at **`15:10:53.332`**, ⭐ **six minutes BEFORE** the EOD routine.

| claim | who made it | 🔬 verdict |
|---|---|---|
| *"the 15:17 routine ran with a **live CNC GTT on the book**"* | ⭐ **mine** | ⚠️ **OVERSTATED.** The `gtt_state` row was ACTIVE; ⛔ the **broker position was not** |
| *"the GTT **survived intact and still worked** — RAMRAT exited 2 min AFTER"* | ⭐ **mine** | 🔴 **WRONG.** The sell had **already filled before** 15:17. `15:19:13` was the monitor's **finalisation**, ⛔ not the GTT acting afterwards |
| *"RAMRAT **was open at the broker** at 15:17:03 … `broker open symbols=0` was measured WHILE a broker position existed"* | 👤 **FILE 30 §2** | 🔴 **REFUTED.** 🔬 `0 positions` at `15:17:03.488` |

⇒ ⭐ **`broker open symbols=0` was measured on a GENUINELY EMPTY list.** ⛔ It is
therefore **not** evidence that a CNC position is excluded by the `{MIS, CO}`
predicate — ⭐ my original, weaker reading was the correct one, and FILE 30's
sharpening does not hold.

### ⭐ WHAT THE BEHAVIOURAL LEG DOES STILL SUPPORT

✅ 🔬 An **ACTIVE `gtt_state` row for RAMRAT existed** from `13:17:21` and was still
ACTIVE when EOD Pass 1 ran at `15:17:01`; 🔬 Pass 1 reported **`0 orders cancelled`**;
🔬 the row went `CLEANED` only at **`15:19:13.285`**, by **`cnc_gtt_monitor`**, ⛔ not by
the EOD routine.

⇒ ⭐ **CANONICAL, and nothing stronger:** *"EOD Pass 1 ran while an ACTIVE
`gtt_state` row existed and cancelled nothing; the row was subsequently cleaned by
its own monitor."* ⛔ **NOT** *"a live CNC position survived the product filter."*

### ⭐ THE SEQUENCE, CORRECTED

```
~15:10:53   the GTT's sell leg FILLED at the broker; the position netted to 0
            and dropped out of get_positions (adapter filters quantity != 0)
 15:15:01   SOFT_KILL, watched_count=0
 15:17:01   EOD Pass 1 -> 0 orders cancelled   (gtt_state row still ACTIVE)
 15:17:03   Pass 2 -> broker open symbols=0    (GENUINELY empty)
 15:17:03   reset_daily_pnl  previous_pnl=-9.74
 15:19:13   _gather (the day's LAST, 26th) -> gtt_exit finalises RAMRAT
            gtt_state -> CLEANED ; RELEASE_USED pnl=-2.18
```

> ⭐ **The last row is the strongest part.** ⛔ Not merely *"the EOD did not cancel it"*
> — ⭐ **the GTT went on to do its job afterwards**, which is the only way to
> distinguish *"untouched"* from *"quietly broken"*.

⇒ **Predictions #9 / #16 now hold on three independent legs:** 🔬 structural (both
Pass-1 queries filter `product IN ('MIS','CO')` and read `orders`, never
`gtt_state`) · 🧪 test (2 mutations turn `test_9…` RED) · ✅ **behavioural (today)**.

---

## 2 — 🔴 THE SECOND FINDING · A REALISED P&L LANDED **AFTER** THE DAILY RESET

🔬 `fm_ledger`, quoted:

```
11669 | 2026-08-28T15:17:03.524053 | RESET_PNL     | balance_before -9.74 -> balance_after 0.0
                                                   | "EOD reset: previous pnl=-9.74"
11670 | 2026-08-28T15:19:13.281613 | RELEASE_USED  | "RAMRAT exit: qty=1 price=592.3
                                                   |  pnl=-2.18 costs=1.53"
```

🔬 `SELECT SUM(pnl_delta) FROM fm_ledger WHERE date(ts)='2026-08-28'` → **−2.18**

> ### 🔴 `reset_daily_pnl` ZEROED THE DAY AT 15:17:03, AND RAMRAT'S **−₹2.18** LANDED AT 15:19:13 — **2 MINUTES LATER.**
> ⭐ The day's `SUM(pnl_delta) = 0` invariant that the reset exists to establish is
> **−2.18**, ⛔ not 0.

### ⚠️ WHAT THIS IS, AND WHAT IT IS NOT

* 🏷️ **PRE-EXISTING.** ⛔ **NOT caused by tonight's unit** — the MIS orchestrator
  touches neither `eod_squareoff` nor `reset_daily_pnl`, and 🔬 `eod_squareoff.py`
  is byte-unmodified.
* 🏷️ **MEASURED OBSERVATION, ⛔ NOT a proven defect.** ⛔ Whether anything downstream
  is harmed is **NOT MEASURED**.
* 🔬 **Tonight's practical impact is nil, and that is measurable:** the overnight
  drift comparator's band is **₹50 flat**; |−2.18| ≪ 50 ⇒ ⛔ no alarm expected.
  ⚠️ ⛔ That is an argument about **tonight's magnitude**, ⛔ not about correctness.
* ⛔ **NOT FIXED.** ⭐ Recorded, ⛔ scope not expanded (FILE 28 §8).

### ⭐ AND IT SUPPORTS THE ADD-ALONGSIDE DECISION — ⛔ W-1: *"VINDICATES"* IS WITHDRAWN

⚠️ **W-1 correction.** My earlier wording claimed this *"decisively vindicates"* the
decision and that a 15:07 reset *"would have"* put the event twelve minutes outside
the window. 🔴 **That is a COUNTERFACTUAL. It was never executed.** ⛔ The project's own
rule applies to my own argument: **counterfactual ≠ exercised behaviour.**

⭐ **CANONICAL WORDING, and nothing stronger:**

> *"The live event provides direct behavioural evidence supporting the add-alongside
> decision, and demonstrates that a post-EOD CNC/GTT realisation can occur inside the
> current reset window."*

⛔ **NOT** *"proves that moving the reset would have caused a correctness failure."*

### 🔴 THE WINDOW IS ≈ 13 MINUTES WIDE, ⛔ NOT 2 — AND ITS MAGNITUDE IS BOUNDED

⚠️ *"A 2-minute window"* was **today's observed instance**, ⛔ not the window.

🔬 `reset_daily_pnl` fires at **15:17:03**.

🔴 **AND THE DRIVING MECHANISM IS NOT WHAT EITHER OF US ASSUMED.** ⚠️ It is **not**
*"a GTT can fire until 15:30"*. 🔬 RAMRAT's sell **filled at ~15:10:53** — *before*
the reset — but its `RELEASE_USED` ledger row was written at **15:19:13**, when the
**CNC monitor's ~15-minute `_gather` cadence** next ran (🔬 the day's **26th and
LAST** cycle; ⛔ none after it).

> ## ⇒ 🔴 **THE EXPOSURE IS THE MONITOR'S FINALISATION LAG, ⛔ NOT THE FILL TIME.**
> ⭐ A fill can precede the reset and still be **booked after it**. 🔬 RAMRAT's fill
> led its ledger entry by **≈ 8 minutes**.

### 🔴 THE ORIENTATION WAS BACKWARDS — IN **BOTH** OF OUR VERSIONS

⚠️ My *"≈13 minutes AFTER the reset"* and the original *"2 minutes after"* both
described a window of **executions following** the reset. 🔴 **That is the wrong way
round.**

🔬 The monitor's cadence is **~15 minutes**. ⇒ ⭐ **ANY fill in the ~15 minutes
BEFORE the reset can be finalised AFTER it.**

> ## ⇒ 🔴 **THE CROSSING WINDOW SITS ON THE *FILL* SIDE, POSITIONED *BEFORE* THE RESET.**
> ⛔ It is **not** a window of executions after it. 🔬 RAMRAT is the proof: its fill
> was at **15:10:53**, ~6 minutes **before** the 15:17:03 reset, and its ledger row
> landed **after**.

⭐ **FOUR CLOCKS, ⛔ never substituted for one another:**

| clock | RAMRAT |
|---|---|
| `position_flat_observed_ts` | ~`15:10:53` |
| `monitor_observed_ts` | `15:19:13.226` (the day's 26th and LAST gather) |
| `ledger_release_ts` | `15:19:13.281` |
| `pnl_reset_ts` | `15:17:03.524` |

### 🔴 LABEL CORRECTION — I CALLED A WRITE LATENCY AN "ACCOUNTING LAG"

⛔ **WITHDRAWN:** *"`accounting_lag` ≈ 55 ms."* 🔴 The 55 ms is
`ledger_release_ts − monitor_observed_ts`. ⚠️ The **accounting** lag — fill to ledger
— is **8m 20s**. ⭐ An event-latency number must never stand in for the full
accounting-lag definition.

⭐ **THE FIVE DEFINITIONS, endpoints EXPLICIT, ⛔ never substituted:**

```
observation_lag             = monitor_observed_ts - position_flat_observed_ts     = 8m 19.894s
accounting_lag              = ledger_release_ts   - position_flat_observed_ts     = 8m 19.949s
write_latency               = ledger_release_ts   - monitor_observed_ts=      55 ms   <- was mislabelled
post_reset_finalisation_lag = ledger_release_ts   - pnl_reset_ts       = 2m 09.757s
reset_crossing              = position_flat_observed_ts < pnl_reset_ts < ledger_release_ts  => TRUE
                              (15:10:53.332  <  15:17:03.524  <  15:19:13.281)
```

✅ **The falsifier FILE 32 attached to its own reading is SATISFIED:** it said the
55 ms reading is wrong if `monitor_observed_ts` is not ≈ `15:19:13.226`. 🔬 It **is**
— that is the `get_holdings call_end` of the day's last gather.

### 🔴 AND WHICH LAG *PREDICTS* CROSSING IS NOT THE ONE I CALLED USEFUL

⚠️ I called `post_reset_finalisation_lag` (2m 10s) *"the most operationally
useful."* ⭐ It is the most **descriptive** of today. ⛔ It is **not predictive**.

⭐ Since `release_ts ≈ fill_ts + observation_lag + write_latency`:

> ## ⇒ 🔴 **A FILL CROSSES THE RESET IFF IT OCCURS WITHIN `observation_lag` BEFORE IT.**
> ⭐ **`observation_lag` DETERMINES whether crossing is possible.**
> ⛔ `post_reset_finalisation_lag` merely RECORDS where the fill happened to land.

⇒ ⭐ The orientation flip, one level deeper: the exposure is a window **BEFORE** the
reset, **one gather-cadence wide** — ⛔ not a window after it.

### ⭐ THE CROSSING CONDITION NEEDS **ONE** QUANTITY, ⛔ NOT TWO

⚠️ My *"iff within `observation_lag`"* dropped `write_latency`. ⭐ The exact condition
is `reset_ts − fill_ts < observation_lag + write_latency` — 🔴 **but those two sum to
`accounting_lag` by construction**, verified:

```
observation_lag  8m 19.894s  +  write_latency  0.0556s  =  8m 19.9496s
accounting_lag                                          =  8m 19.950s   OK
```

> ## ⇒ **`crossing_possible  iff  0 < (reset_ts − fill_ts) < accounting_lag`**
> ⭐ ONE quantity. ⛔ Not two, and ⛔ not the decomposition at all.

⇒ 🏷️ **THE AUDIT NEEDS ONE BOUND: the MAXIMUM `accounting_lag`. NOT MEASURED.**
⚠️ Today's single instance is `8m 19.950s` — 🔴 **one observation is not a bound.**
⛔ Do not turn 8m20s into a guaranteed maximum. ⭐ The decomposition stays
**diagnostically** useful (*where* the time goes), ⛔ but is not needed for the test.

### 🔴 THE `position_flat_observed_ts` ANCHOR IS A **DETECTION**, ⛔ NOT A BROKER FILL TIME

⚠️ FILE 37 asked where `15:10:53.332` comes from, and attached the falsifier
*"wrong if it derives from broker order/trade data carrying an exchange-side fill
time."* 🔬 **It does not. The falsifier FIRES.**

🔬 The raw line:

```
15:10:53.315  zerodha_adapter  get_positions call_start
15:10:53.332  zerodha_adapter  get_positions call_end  duration_ms=17  "0 positions"
```

⇒ ⭐ It is a **polling call completion** — the moment the system *first observed*
the book flat. 🔬 And the bracketing samples show the true fill is **unlocated**:

```
15:10:38.192 -> 1 positions      <- OBSERVED open here
15:10:53.332 -> 0 positions      <- FIRST OBSERVED flat here
```

⚠️ 🔴 **AND I OVER-CORRECTED ONCE ALREADY: ⛔ DO NOT WRITE *"the real fill lies in
this ~15.1 s gap."*** ⭐ That silently assumes the poll reflects the broker's true
state without lag. ⛔ Without a broker fill time **or a proven polling invariant**,
the fill could have occurred **earlier and gone unobserved**.

> ⭐ **CANONICAL: *"Fill time UNKNOWN. Position OBSERVED open at 15:10:38.192;
> FIRST OBSERVED flat at 15:10:53.332."***
> ⛔ **"Bracketed by two polls" ≠ "known to be inside the interval."**

### 📜 PROVENANCE OF THIS ONE TIMESTAMP — ⛔ history preserved, not deleted

| stage | value |
|---|---|
| previous label | `broker_fill_ts` ❌ |
| actual source | `get_positions` **call_end** log line |
| correct label | **`position_flat_observed_ts`** |
| previous interpretation | fill-to-ledger ❌ |
| correct interpretation | **detection-to-ledger** |
| broker fill timestamp | 🔴 **UNAVAILABLE** |

⭐ **AND THE STRUCTURAL POINT WORTH KEEPING:** *exact latency may be unmeasurable
while ordering remains provable.* ⭐ Those are different claims and the record must
keep them apart.

🔬 **And there is no broker-supplied exit fill time ANYWHERE in the system for this
trade:** RAMRAT has a single `orders` row — the ENTRY (`260828170275430`,
`filled_at 10:12:22.994975`). ⛔ **No exit-order row exists at all**, because the exit
was a **GTT**, which lives in `gtt_state` and creates no `orders` row.

> ## ⇒ 🔴 **RELABEL: `accounting_lag` IS *DETECTION*-TO-LEDGER, ⛔ NOT FILL-TO-LEDGER.**
> `accounting_lag = ledger_release_ts − first_observed_flat_ts = 8m 19.950s`
> ⚠️ The **true** fill-to-ledger interval is **LONGER by an unknown amount, up to
> ≈ 15.1 s** (one polling interval). 🏷️ **NOT MEASURABLE from available data.**

⚠️ ⭐ **This is the same mislabelling as the 55 ms, one level down** — a measurement
named after the event it *detects* rather than the event it *is*. ⭐ Caught by the
same discipline that caught the first one.

### ✅ WHAT SURVIVES UNCHANGED — and why the audit is still safe

✅ **`reset_crossing = TRUE` survives EITHER anchor**, because the ordering holds
regardless: `fill ≤ 15:10:53.332 < 15:17:03.524 < 15:19:13.281`. ⭐ An earlier true
fill only strengthens it.

✅ **`post_reset_finalisation_lag = 2m 09.758s` is untouched** — its anchors are the
`RESET_PNL` row and the `RELEASE_USED` row, ⭐ neither of which depends on the fill
anchor at all.

⚠️ **But the "two INDEPENDENT anchors" claim for `accounting_lag` must be narrowed:**
⭐ both anchors are **system-side** (an adapter poll and a `fund_manager` ledger
write). ⛔ Neither is broker-supplied. ⭐ They remain independent *measurement points
in different subsystems* — ⛔ but this is **not** a broker-anchored quantity, and must
never be described as one.

⇒ 🏷️ **EVERY lag quantity in this record is now known to rest on SYSTEM DETECTION
anchors.** ⭐ The crossing CONCLUSION is unaffected; ⛔ the MAGNITUDES all carry an
unmeasured detection offset.

### 🔴 ANCHOR HIERARCHY — ⛔ THE FOUR NUMBERS ARE NOT EQUALLY SOLID

🔬 `monitor_observed_ts = 15:19:13.226` is a **`get_holdings` call_end** — a *call
completion*, ⛔ **not** proof that RAMRAT's fill was present in that call's result.
⇒ ⚠️ `observation_lag` and `write_latency` are **both defined from that single
anchor** ⇒ ⛔ they are **not independent** and **stand or fall together**.

| quantity | anchors | status |
|---|---|---|
| `accounting_lag` 8m 19.950s | broker fill + ledger row — **two independent** | ✅ **ROBUST** |
| `post_reset_finalisation_lag` 2m 09.758s | reset row + ledger row — **two independent** | ✅ **ROBUST** |
| `reset_crossing = TRUE` | directly observed | ✅ **ROBUST** |
| `observation_lag` + `write_latency` | ⚠️ **share ONE anchor** | ⚠️ **DERIVED** |

### 🔴 AND THE LINKAGE IS **NOT** ESTABLISHED — ⛔ the pair is DOWNGRADED

⚠️ FILE 34 asked: does that gather's result actually contain the RAMRAT fill?
🔬 **It does not, and it could not.** By `15:19:13` RAMRAT had been flat since
`15:10:53` — 🔬 `get_holdings` returned **0 holdings** and `get_positions` **0
positions**. ⇒ ⭐ the fill manifested as an **ABSENCE**, ⛔ not as a payload entry:
the pass saw an ACTIVE `gtt_state` row with `held == 0` and finalised on that.

> 🏷️ **LABEL: `observation_lag` and `write_latency` are DERIVED FROM A CALL-END
> ANCHOR. Their linkage to this specific fill is by SAME-PASS TEMPORAL ADJACENCY
> (55 ms to the ledger row), ⛔ NOT by observing the fill in the call's result.**
> ⛔ A call-end timestamp must never be upgraded into a per-fill observation
> timestamp.

✅ ⭐ **AND THAT IS WHY THE SIMPLIFICATION MATTERS:** the crossing condition uses
**only `accounting_lag`**, whose two anchors are independent. ⇒ 🔴 **the audit's
primary quantity does not depend on the shakier pair at all** — ⭐ a consequence of
the simplification, ⛔ not luck.

⚠️ **FALSIFIER:** ⛔ wrong if finalisation is **not** gather-driven. ⭐ If some fills
are finalised by an event-driven path rather than the periodic gather,
`observation_lag` would not bound the crossing. 🏷️ **NOT CHECKED.**

⇒ 🏷️ **THE AUDIT'S PRIMARY QUANTITY IS `observation_lag`, and its MAXIMUM is NOT
MEASURED.** ⭐ Today's single instance: ≈ **8m 20s**.

### ⚠️ ON THE ~15-MINUTE CADENCE — what is measured vs what is arithmetic

⭐ My ~15-min figure is **MEASURED**: 🔬 26 gather timestamps across the day
(`09:15:02 · 09:29:54 · 09:45:00 · 10:00:05 · 10:15:13 … 15:04:04 · 15:19:13`),
intervals ≈ 15 min. ⚠️ Note the **first** interval (`08:15:23 → 09:15:02`) is ~60 min
⇒ ⭐ the cadence is **in-hours gated**, ⛔ not free-running.

⛔ **DO NOT inherit `_cnc_monitor_every 60 × poll_interval_sec 15 ⇒ 15 min`** —
⚠️ that is a **multiplication of two config values, ⛔ not a control-flow trace**.
🏷️ What `_cnc_monitor_every` counts, its unit, the market-hours gating, whether a
final gather runs at shutdown, and whether boot reconciliation can consume a stale
`gtt_state` or fill are all **NOT TRACED**. ⭐ The "last gather" question depends on
exactly those semantics. ⛔ Not tonight.

### ⚠️ AND Q6 IS REVISED — ⛔ DO NOT INHERIT THE OLD BOUND

⛔ **WITHDRAWN:** *"`max_open_delivery_positions = 3` bounds the post-reset events."*
⭐ The relevant quantity is **delayed FINALISATIONS**, ⛔ not open positions at the
reset instant. ⚠️ The 3-limit **may** still bound it — 🏷️ that must be **VERIFIED**,
⛔ not assumed.

### 🔴 THE AUDIT'S SHARPEST QUESTION — 🏷️ NOT MEASURED, ⛔ NOT A FINDING, ⛔ NOT TONIGHT

🔬 `15:19:13` was the day's **26th and LAST** in-hours gather; ⛔ none after it.
⚠️ The market runs to **15:30**.

> ### ⇒ **What finalises a CNC fill occurring between the last gather and 15:30?**
> ⛔ There is no further in-hours gather to do it.

💭 Its `RELEASE_USED` would land at some later point — ⛔ possibly across the whole
**day boundary**, ⛔ not merely across the reset.

⭐ **THE FALSIFIER, stated per the standing rule:** ⛔ this concern is **wrong** if a
**shutdown-time or boot-time reconciliation** finalises such fills. ⭐ That is
**checkable**, ⚠️ **and it was not checked.**

⚠️ ⭐ **So the window is bounded by `last in-hours _gather` − `15:17:03`, ⛔ not by
`15:30 − 15:17`.** 🏷️ Today that was ≈ **2m 10s**; ⛔ the general bound is **NOT
MEASURED** — it depends on where the ~15-min cadence lands relative to 15:17, and on
when the monitor stops (🔬 today: no `_gather` after 15:19:13).

✅ **And the magnitude is bounded by measured configuration, ⛔ not open-ended:**
🔬 `max_open_delivery_positions = 3` (ENFORCED, `system_config.yaml:230`), each sized
by the concentration cap. ⇒ ⭐ worst case is **three** delivery P&Ls landing
post-reset, ⛔ not unbounded accumulation.

### 🔴 AND THE CONNECTION TO TONIGHT'S UNIT — ⭐ RECORD THEM AS **RELATED**

⭐ A **`DEADLINE_BREACH`** means an MIS position survives past **15:12** ⇒ Zerodha
auto-squares it at **15:25** (non-CAS) ⇒ 🔴 **that realised P&L lands AFTER the 15:17
reset — inside this exact window.**

⇒ ⭐ **The MIS unit's own failure mode FEEDS the accounting window observed today.**
⛔ Not a reason to change either tonight — ⭐ a reason to record them as **related**, so
a future reader does not treat them as independent.

### 📋 TRACKED AUDIT ITEM (⛔ NOT A FIX) — the questions that must be answered

1. Who **consumes** `reset_daily_pnl` / `get_daily_realized_net_pnl`?
2. Is the daily ledger `SUM(pnl_delta)` **intended** to be zero after the reset?
3. Does a post-reset `RELEASE_USED` belong to the **prior** day or the **next**?
4. Does the overnight drift logic read **−2.18** correctly?
5. The **3-position accumulation bound** — does it hold under every sizing path?
6. What is the **intended accounting boundary**: calendar day / EOD routine / broker session?

⚠️ ⛔ **The ₹50 band only says today's −₹2.18 raises no alarm. It says NOTHING about
accounting correctness.**

⚠️ ⭐ **A CNC GTT can fire at any time, including after the EOD routine.** ⭐ The
reset's placement is therefore a **real** constraint on any future re-timing —
⛔ not a detail to optimise past.

---

## 3 — 👤 RAMA'S 15:00 DECISION · ⭐ RESOLVED BY THE MARKET, ⛔ NOT BY ME

🔬 **RAMRAT exited on its own protective GTT at 15:19:13** (₹592.30 vs entry
₹592.95, `net_pnl` **−₹2.18**, `exit_reason = GTT_EXIT`, `gtt_state → CLEANED`).

⇒ ⭐ **The CNC book is FLAT. `D = ₹0`.** ⛔ No HOLD/CLOSE action was ever taken by me,
⛔ the decision was never re-asked, and ⛔ it was never made on 👤 Rama's behalf —
⭐ the position closed itself through the designed path.

🔬 **Today's CNC round trips, all system-entered and system-exited:**

| symbol | entry | exit | `exit_reason` (🔬 as recorded) | net P&L |
|---|---|---|---|---|
| TEJASNET | ₹568.65 | ₹558.00 | `GTT_EXIT` | **−₹12.11** |
| OAL | ₹432.75 | ₹445.55 | `GTT_EXIT` | **+₹11.68** |
| RAMRAT | ₹592.95 | ₹592.30 | `GTT_EXIT` | **−₹2.18** |

⚠️ **W-3: WHICH GTT LEG FIRED IS ⛔ NOT RECORDED FOR ANY OF THE THREE.** 🏷️ The DB
records `GTT_EXIT` and nothing finer. ⛔ My earlier annotations *"(SL leg)"* and
*"(target leg)"* were 💭 **INFERENCE from price proximity** — they are **WITHDRAWN**.
⛔ Never write "SL" or "target" without raw broker/order evidence.

🏷️ ⇒ **NO OVERNIGHT CARRY.** ⛔ The F6 **T+1 arm remains NOT EXERCISED** — a third
consecutive day on which the qualifying condition did not arise. ⛔ Monday's boot
cannot supply it either, because there is nothing carried into it.

---

## 4 — WHAT IS NOT MEASURED

1. ⛔ Whether the post-reset P&L window has **any** downstream consumer that is
   harmed — 🏷️ **NOT MEASURED**, ⛔ not investigated, ⛔ not fixed.
2. ⛔ How often it occurs: today is 🔬 **one observed instance**, ⛔ not a rate.
3. ⛔ RAMRAT's exit at ₹592.30 sits between its SL (₹581.10) and target (₹610.75).
   🏷️ **The GTT leg that fired is NOT DETERMINED** from the captured line — the
   `reason` field was truncated in the log excerpt. ⛔ Not chased.
4. 🏷️ The 15:07/15:10 passes ⇒ **NOT EXERCISED**; they are unpushed and cannot run
   before Monday.

⛔ executed ≠ exercised · ⛔ untouched ≠ still working (⭐ today proved BOTH
separately) · ⛔ a measured observation ≠ a proven defect · ⛔ small tonight ≠ correct.

## END
