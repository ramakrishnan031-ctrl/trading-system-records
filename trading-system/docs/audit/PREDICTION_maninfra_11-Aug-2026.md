# FROZEN PREDICTION — WHAT THE 11-Aug-2026 08:15 BOOT WILL DO TO THE MANINFRA ROW

**WRITTEN 10-Aug-2026, BEFORE THE BOOT.** ⛔ No edits after `2026-08-11 08:15 IST`.
⛔ **A SEPARATE PREDICTION. `PREDICTION_diffnkg_11-Aug-2026.md` is untouched by this file, and
neither proves anything about the other.**

**CODE UNDER TEST: the DEPLOYED ref `645728d`** (`orders/cnc_gtt_monitor.py`, md5
`025498f4ae05776915da2c242fdcc86e`). Nothing is deployed; tomorrow's boot runs the old code.

**PARITY — LIVE-ONLY.** A CNC settlement boundary with a broker-side OCO execution. Paper has no T+1
model and never places a real GTT. ⛔ **No paper analogue exists and none is claimed.**

---

## §1 — WHAT HAPPENED, AND THE ONE WORD THAT MUST BE CORRECTED

> **Rama, 10-Aug-2026:** *"existing GTT MANINFRA all 4 qty sold by system just after VS Code finishes
> — meaning zero holdings as of now. Only one position created today (due to GTT sold)."*

> ## ⛔ **NOT "by the system". THE SYSTEM HAS BEEN DEAD SINCE `08:15:25` AND TOOK NO ACTION ALL DAY.**
> ⭐ **ZERODHA executed it.** The OCO GTT `330856765` was resting **broker-side** with triggers
> `112.92 / 118.69`, and price reached one of them. The trading system neither placed nor observed it.

🔑 **That distinction is not pedantry — today's entire incident turned on it.** A broker-side
execution the system does not know about is a *different fact* from a system exit, and the DB still
believes the position is open. **This is exactly the class the `site=local-pass` vs `site=broker-sweep`
catch was about.**

### The resulting state

| | DIFFNKG | MANINFRA |
|---|---|---|
| DB trade row | `OPEN` `₹446.106` | **`OPEN` `₹460.91632`** (`trd_9e709c50…`, qty 4 @ `115.23`) |
| `gtt_state` | `330944932` `ACTIVE` qty 1 | **`330856765` `ACTIVE` qty 4**, `needs_review 0`, `sl 112.92/109.53`, `tgt 118.69/118.09`, last verified `07-Aug 15:20:34` |
| broker holding | **0** (measured, Addendum A) | **0** (operator-reported, today) |
| broker GTT | **deleted by Rama** | **consumed / triggered today** |
| CNC position row | **NONE** (measured ~14:00) | 🔴 **ONE, CREATED TODAY** |

**Evidence classes:** the `gtt_state` and `trades` rows are **(P) MEASURED** from
`capture_10aug2026/A_db_capture.txt`. The holdings/position statements for MANINFRA are
**(P) OPERATOR-REPORTED, broker UI, ⛔ not an API reading, and not timestamped to the minute.**

---

## §2 — THE LADDER: MANINFRA HAS **FOUR** REACHABLE OUTCOMES, NOT TWO

`row_qty = 4`, `needs_review = 0` ⇒ no stand-down. `held = Σ holdings.qty (:456) + Σ abs(CNC
positions.qty) (:464)`. **Two independent unknowns**, so a 2×2:

| | `held = 0` | `held = 4` (the `−4` row still present ⇒ `abs()` ⇒ 4) |
|---|---|---|
| **GTT still in `get_gtts()` as `triggered`** | branch 1a `:487-488` → `_finalize_gtt_exit` — **CLOSES** | 🔴🔴 branch 1b `:489` → **`_reprotect` → `_recreate`, CRITICAL** |
| **GTT gone from `get_gtts()`** | branch 4 `:501-510` → `_finalize_gtt_exit` — **CLOSES** | 🔴 branch 5 `:513-521` → `_queue_preopen` + WARNING, recreate on the first in-hours cycle |

> ## 🚨 **AND THE TWO RECREATE PATHS ARE NOT EQUALLY SURVIVABLE — THIS IS THE PART RAMA NEEDS TONIGHT.**
> **`_reprotect` (`:597-603`) has NO `in_hours` GATE.** It calls `_recreate` directly. ⇒ in the
> **top-right** cell **a REAL SELL GTT FOR 4 SHARES IS BUILT AT ~08:15, IMMEDIATELY** — ⛔ **there is
> NO one-hour warning window**, unlike DIFFNKG's branch 5. The CRITICAL alert and the order are
> simultaneous.

⭐ **DIFFNKG can only ever reach branch 4 or 5** (its GTT was deleted, so `bg = None`). **MANINFRA can
reach branch 1** because its GTT was *consumed*, not deleted. **The two rows exercise different halves
of the same ladder on the same boot** — which is why this is worth writing separately.

---

## §3 — ⛔⛔ **SUPERSEDED BY ADDENDUM B — THIS FORECAST IS WRONG. KEPT VERBATIM, BECAUSE THE ERROR AND ITS CAUSE ARE THE RECORD.**
*(Every figure below is left exactly as written. ⛔ Do not act on it; ⛔ do not delete it.
The corrected arithmetic is in Addendum B, and the boot is now expected to SURVIVE.)*

### ~~🔴 THE PRIOR CONDITION NOW DOMINATES BOTH PREDICTIONS: THE BOOT MAY NOT GET THERE~~

The rehydrate replays **BOTH** open rows — `446.106 + 460.91632 = ₹907.0223` — into the positional
bucket, against **cash**, on the un-deployed old code.

```
INV6 passes iff   0.30 × cash − 907.0223 ≥ −1.0        (tolerance 1.0, measured in today's log)
              ⇒   cash ≥ 3,020.07
```

**Tomorrow's cash, from measured operands:** today's INIT `209.80` **+** the MANINFRA proceeds,
`4 × 112.92 = 451.68` (SL leg) to `4 × 118.69 = 474.76` (target leg), before charges

> ## ⇒ **cash ≈ ₹661 – ₹685, against a ₹3,020.07 requirement.**
> ## 🔴🔴 **WITHOUT A PAYIN, THE 11-Aug BOOT HARD-KILLS AGAIN — `positional_avail ≈ 0.30 × 673 − 907.02 ≈ −705`.**
> **A payin of roughly `₹2,350` is what clears it.** ⛔ **NOT a recommendation to pay in — a
> measurement of the threshold. The decision is Rama's and there may be good reasons not to.**

⚠️ **Uncertainty, named:** how much of a T1-stock sale's proceeds Zerodha releases into
`margins().net` by the next morning is **not measured** — it could be less than the full figure. That
moves the number **down**, ⛔ never up, so the conclusion is unaffected: **without a payin it fails.**

> ### ⭐⭐ **AND THE TWO RISKS ARE MUTUALLY EXCLUSIVE, WHICH IS THE MOST USEFUL THING IN THIS FILE:**
> **If the boot hard-kills, `cnc_gtt_monitor` NEVER RUNS ⇒ no new SELL GTT is created, for either
> symbol, and BOTH predictions score `NOT TESTED`.** ⛔ **The unwanted sell order can only happen on a
> boot that SURVIVES.** ⭐ So "pay in to make the boot work" and "avoid a phantom sell order" pull in
> **opposite** directions, and that trade-off is Rama's to make with the facts in front of him.

---

## §4 — THE CALL

> ## ⭐ **I EXPECT `held = 0` ⇒ MANINFRA CLOSES (`_finalize_gtt_exit`, `GTT_EXIT`) — the LEFT column.**
> **Confidence: MODERATE. ⛔ And this REFUTES the (B)/recreate expectation I was given, on evidence.**

**WHY — the precedent that matches MANINFRA's exact shape, and it is measured on this account:**

| symbol | gtt_id | created | last verified | → `CLEANED` at | shape |
|---|---|---|---|---|---|
| ASKAUTOLTD | `330462987` | 05-Aug 10:13:27 | 05-Aug 10:30:38 | **05-Aug 10:45:51** | same session, ~32 min |
| ASKAUTOLTD | `330660310` | 06-Aug 10:06:27 | 06-Aug 10:32:36 | **06-Aug 10:47:46** | same session, ~21 min |
| **ATULAUTO** | **`330657774`** | 06-Aug 10:02:13 | **06-Aug 15:23:40** | **07-Aug 08:15:41** | 🔑 **sold late in session D → `held = 0` at the D+1 08:15 BOOT** |

**(P) `CLEANED` is written ONLY inside `_finalize_gtt_exit` (`:537`, `:587`)** — nowhere else on this
path — **so every row above proves `held == 0` at that timestamp.**

⇒ ⭐⭐ **ATULAUTO is MANINFRA's shape exactly: healthy with `held = 4` late in the session, sold, and
`held = 0` by the next morning's 08:15 boot. The `−n` CNC row had aged out overnight.** And the two
ASKAUTOLTD rows show `held` reaching 0 within ~20–30 minutes of a sale **intraday**, which is the same
direction.

**WHY (B) IS STILL LIVE — ⛔ and it must not be softened:**

1. **DIFFNKG proves the respawn is real on this account.** `330944932` was itself minted by a
   `_recreate` on **07-Aug 15:20:35** — branch 5, `held == row_qty`, GTT absent. **That is one
   measured respawn against three measured clean exits.**
2. **F6's own commit says the opposite of my call, for the T+1 case:** *"a negative CNC row is a sale
   `holdings()` has ALREADY applied, so `abs()` double-counted it and forced `held = 1` on **every T+1
   exit**"*, producing *"three real SELL orders resting at the exchange against a holding of zero"*.
   ⛔ **I am calling against F6's generalisation and I am naming that I am doing so.** My ground is
   that the `gtt_state` timestamps are direct evidence about **08:15 on D+1**, which is the exact
   moment in question; F6's sentence does not date its window.
3. ⚠️ **MANINFRA was `T1: 4` (unsettled) in this morning's holdings screenshot, so today's sale was of
   T1 stock.** ⛔ **Whether a T1 sale's `−4` ages out on the same schedule as a settled-stock sale is
   NOT MEASURED**, and MANINFRA's sale is one day fresher than any precedent. ⭐ **This is the single
   biggest reason the confidence is MODERATE and not high.**

---

## §5 — FALSIFIERS · score by SIGNATURE, ⛔ never by narrative

| outcome | fires iff | proof |
|---|---|---|
| **CLOSES** | `held == 0` | `cnc_gtt_monitor.gtt_exit` for `trd_9e709c50…`; `trades.status → CLOSED`; `gtt_state 330856765 → CLEANED`; a `RELEASE_USED` `fm_ledger` row for `460.91632`; WARNING *"GTT exit — MANINFRA"* |
| **REPROTECT** (top-right) | `held == 4` **and** GTT present as `triggered` | **CRITICAL** *"GTT partial/no-fill re-protect — MANINFRA"* + a **NEW gtt_id at ~08:15**, ⛔ no queue step |
| **QUEUE→RECREATE** (bottom-right) | `held == 4` **and** GTT absent | `queued_preopen:MANINFRA` + WARNING at ~08:15, then a NEW gtt_id on the first in-hours cycle |
| **QTY MISMATCH** | `held ∉ {0, 4}` — e.g. holdings `4` **and** positions `−4` ⇒ `8` | **CRITICAL** *"GTT qty mismatch — MANINFRA"*, `needs_review → 1`, no recreate |
| **NOT TESTED** | the boot hard-kills first (§3) | `NEGATIVE_MARGIN_AVAILABLE` at ~`08:15:25`, no `cnc_gtt.hydrated` |

⭐ **A prediction set that gets a CLOSE right on one row and a RECREATE right on the other is far
stronger than one that gets CLOSE right twice.** ⛔ **Both calls stay as written regardless.**

---

## §6 — WHAT RAMA NEEDS TONIGHT

1. 🔴 **The most likely outcome is that the boot HARD-KILLS AGAIN** (§3) — cash ≈ ₹661–685 against a
   ₹3,020 requirement — **and then nothing else happens at all.**
2. 🔴 **If it survives and `held = 4`, a REAL SELL GTT for 4 shares he no longer owns is built** — and
   in the `triggered` case **at 08:15, with no warning window.**
3. ⭐ **Those two are mutually exclusive.** A payin makes the boot work *and* makes the phantom-sell
   risk live. ⛔ **His call, not ours.**

---

# ADDENDUM A — A DIRECT API MEASUREMENT. 🔴 **THE `−4` EXISTS.**

**Added 10-Aug-2026, still before the boot.** ⛔ **CALL, CONFIDENCE AND FALSIFIERS UNCHANGED.**

> **`reconcile_positions`, `2026-08-10T15:45:02.715` IST:**
> **`MANINFRA: broker=−4 system=4 → QTY_MISMATCH`** · `DIFFNKG: broker=0 system=1 → MISSING_AT_BROKER`
> **`cron:reconcile_positions FAILED — exit code 2`**

⭐⭐ **`(P)` FROM THE BROKER API, produced by the system's own cron — ⛔ not an operator reading a UI.
It supersedes every screenshot in class, and it measures EXACTLY the field that decides this:**
`reconcile_positions` reads **`positions()` only**, which is the term `_gather` sums at `:464`.

> ## 🔴 **THE NEGATIVE CNC ROW IS REAL AND WAS PRESENT AT 15:45 TODAY.** ⇒ **if it is still there at `08:15`, `held = 0 + abs(−4) = 4` and MANINFRA lands in the RIGHT COLUMN of §2 — the recreate half.**

**AND IT CORROBORATES §1's CORRECTION INDEPENDENTLY:** `system=4` versus `broker=−4` is the DB still
believing it holds 4 while the broker has already sold them — **the signature of an execution the
system never saw.** ⭐ The `QTY_MISMATCH` classification is the reconciler naming that gap in its own
vocabulary.

### ⛔ WHAT IT DOES **NOT** SETTLE — and this is the whole question

> **A `15:45` reading is not an `08:15` reading.** Whether the `−4` **survives overnight** is
> precisely the ATULAUTO question, and ATULAUTO's answer — `held = 0` at the next 08:15 boot — was
> reached **across exactly this boundary.**

⇒ ⛔ **THE CALL IN §4 STANDS UNCHANGED: I still expect `held = 0` and a CLOSE.** ⭐ **This addendum
raises the stakes on that call; it does not decide it.** If the `−4` persists, my call is **wrong**
and the right column fires — **and that is what a falsifiable prediction is for.**

### ⚠️ INCIDENTAL, RECORDED AND ⛔ NOT CHASED TONIGHT

**`reconcile_positions` ran — and FAILED with exit 2 — while the trading service has been dead since
`08:15:25`** ⇒ 🔑 **the cron chain is INDEPENDENT of the service.** ⭐ Rama has been receiving
CRITICALs all day from a system that is not running. ⛔ **Filed, not investigated.**

---

# ADDENDUM B — 🔴 **§3'S FORECAST WAS WRONG. THE BOOT IS EXPECTED TO SURVIVE.**

**Added 10-Aug-2026, before the boot.** ⛔ **NEITHER CALL MOVES** — both are about `held`, ⛔ not about
boot survival. `NOT TESTED` remains valid if the boot dies for any other reason.

### B.1 — THE FACT §3 DID NOT HAVE

> **(P) Zerodha Funds, this morning: available `₹10,209.80` · opening `₹209.80` · payin `₹10,000`.**
> **Rama added ₹10,000 THIS MORNING — before any of this was written.**

### B.2 — CORRECTED ARITHMETIC

```
cash        = 10,209.80 + MANINFRA proceeds (4 × 112.92 … 118.69 = 451.68 … 474.76)
            ≈ 10,661.48 … 10,684.56
positional_avail = 0.30 × cash − 907.0223   ≈ +2,291.42 … +2,298.35
requirement      = cash ≥ 3,020.07          → margin of safety ≈ ₹7,641
```

> ## ✅ **THE 11-Aug BOOT IS EXPECTED TO SURVIVE. ⛔ NO PAYIN IS NEEDED AND NONE SHOULD BE MADE.**

### B.3 — 🔑 HOW THE ERROR HAPPENED, NAMED PRECISELY — **AND IT IS WORSE THAN "A STALE SEED"**

§3 used **today's `fm_ledger` INIT row (`209.80`)** — the seed the boot recorded at `08:15`, **before
the payin** — as a proxy for **tomorrow's fresh `margins().net`**, which is read live and will
include it. **A stale seed used to forecast a fresh one.**

> ## ⛔⛔ **BUT THE SHARPER FACT: I ALREADY HAD THE RIGHT NUMBER, IN MY OWN PRIOR ARTEFACT, AND DID NOT CARRY IT FORWARD.**
> **`PREDICTION_diffnkg_11-Aug-2026.md:133`, written hours earlier the same evening:** *"On
> `₹10,209.80` the invariant passes (`3,062.94 − 907.02 = +2,155.92`), so it should"*. **And the
> memory record `delivery_book_ceiling_10aug.md` carried `₹10,209.80` too.**
> ⇒ 🏷️ **Two prediction files written the same night contradict each other on the same operand, and
> the LATER one is the wrong one.** ⭐ **This is *a practice recorded but not carried* in its data
> form: the figure was not re-derived, it was simply not looked up.**

⚠️ **AND THE MECHANISM IS THE ONE THIS CAMPAIGN ALREADY NAMED:** *the capital drift was an operand
mismatch* — **`fm_ledger` INIT is a DAILY seed, and reading it as "current cash" is exactly the error
the capital-vocabulary rule exists to prevent.** ⛔ Third time this shape has appeared today.

### B.4 — 🔴 THE CONSEQUENCE, AND IT INVERTS §3'S CONCLUSION

§3 said the two risks were mutually exclusive and a dead boot was the likely one. **That is now
inverted: the boot survives, so `cnc_gtt_monitor` RUNS.**

- ⭐ **Both predictions become genuinely testable — the observation happens.**
- 🔴 **THE PHANTOM SELL ORDER IS LIVE.** If MANINFRA's `−4` is still present at `08:15` (and
  Addendum A measured it present at 15:45), `held = 4` ⇒ the **right column** ⇒ **a real SELL GTT for
  4 shares the account no longer owns.**
- 🚨 **In the `triggered` sub-case `_reprotect` has NO `in_hours` gate ⇒ the order is built AT 08:15,
  and the CRITICAL alert and the order are SIMULTANEOUS.** ⛔ **No warning window**, unlike DIFFNKG's
  queued branch.

⛔ **We take no action: no stop, no cancel, no hand-close, no payin.** ⭐ **Tomorrow's boot doing it
IS the observation, and letting it run is Rama's call** — he should simply know before he wakes up,
so an 08:15 alert is *recognised* rather than discovered.
