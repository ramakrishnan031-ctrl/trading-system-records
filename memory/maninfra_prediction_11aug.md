---
name: maninfra-prediction-11aug
description: "SEPARATE frozen prediction for MANINFRA's 11-Aug 08:15 boot: its GTT was executed BROKER-SIDE today (not by the system, which was dead), leaving a CNC position row created today. Call is CLOSES (held=0), refuting the recreate expectation on measured precedent. CORRECTED same evening: the boot is EXPECTED TO SURVIVE (Rama paid in Rs10,000 that morning), so the monitor runs and the phantom SELL GTT is LIVE. If it appears, DO NOT DELETE IT - :513 rebuilds it."
metadata: 
  node_type: memory
  type: project
  originSessionId: 55f762b9-1f1c-4ab4-b80b-c1b50da706f7
  modified: 2026-08-10T10:42:41.475Z
---

📄 **`docs/audit/PREDICTION_maninfra_11-Aug-2026.md`** — ⛔ **A SEPARATE FILE. DIFFNKG's prediction is
UNTOUCHED, and ⛔ neither proves anything about the other.** Frozen at `11-Aug 08:15`.
🧪 **PARITY — LIVE-ONLY: a CNC settlement boundary + a broker-side OCO execution. ⛔ No paper
analogue.** [[paper-cannot-exercise-class-26jul]]

---

## ① ⛔ **NOT "SOLD BY THE SYSTEM" — ZERODHA EXECUTED IT**

📜 Rama: *"existing GTT MANINFRA all 4 qty sold by system just after VS Code finishes."*
> ## ⛔ **THE SYSTEM HAS BEEN DEAD SINCE `08:15:25` AND TOOK NO ACTION ALL DAY.** ⭐ **The OCO GTT
> `330856765` was resting BROKER-SIDE (`sl 112.92` / `tgt 118.69`) and price reached a trigger.**

🔑 **⛔ NOT pedantry — TODAY'S ENTIRE INCIDENT TURNED ON THIS DISTINCTION.** A broker-side execution
the system never saw is a **different fact** from a system exit, and **the DB still believes the
position is OPEN.** ⭐ Same class as the `site=local-pass` vs `site=broker-sweep` catch.
[[counts-db-rows-not-broker-06aug]]

---

## ② THE LADDER — MANINFRA HAS **FOUR** REACHABLE OUTCOMES, ⛔ NOT TWO

**`row_qty = 4`, `needs_review = 0`** ⇒ no stand-down. **TWO independent unknowns** *(has the `−4`
aged out? is the consumed GTT still listed as `triggered`?)* ⇒ a 2×2:

| | `held = 0` | `held = 4` |
|---|---|---|
| **GTT listed `triggered`** | `:487` `_finalize_gtt_exit` — **CLOSES** | 🔴🔴 `:489` **`_reprotect` → `_recreate`, CRITICAL** |
| **GTT gone** | `:501` `_finalize_gtt_exit` — **CLOSES** | 🔴 `:513` `_queue_preopen` → recreate in-hours |

> ## 🚨 **`_reprotect` (`:597-603`) HAS **NO `in_hours` GATE** — it calls `_recreate` DIRECTLY.** ⇒ in
> that cell **a REAL SELL GTT FOR 4 SHARES IS BUILT AT ~08:15, IMMEDIATELY: ⛔ NO one-hour warning
> window**, unlike DIFFNKG's branch 5. The CRITICAL and the order are simultaneous.

⭐ **DIFFNKG can only reach branches 4/5 (`bg = None`, Rama deleted it); MANINFRA can reach branch 1
because its GTT was CONSUMED, not deleted** ⇒ **the two rows exercise DIFFERENT HALVES of one ladder
on one boot.** ⭐⭐ **A set that gets a CLOSE right on one and a RECREATE right on the other is far
stronger evidence than one that gets CLOSE right twice.**

---

## ③ ⛔⛔ **SUPERSEDED BY ④c — THIS FORECAST WAS WRONG. KEPT, because the error and its cause ARE the record.**

The rehydrate replays **BOTH** rows — `446.106 + 460.91632 = ₹907.0223` — against **cash**, on the
un-deployed old code. **`INV6` passes iff `0.30 × cash − 907.0223 ≥ −1.0` ⇒ `cash ≥ 3,020.07`.**
**Tomorrow's cash = today's INIT `209.80` + proceeds `4 × 112.92 … 118.69` = `451.68 … 474.76`**

> ## ⇒ **`cash ≈ ₹661 – ₹685` vs a `₹3,020.07` requirement ⇒ 🔴 WITHOUT A PAYIN THE BOOT HARD-KILLS AGAIN** *(`positional_avail ≈ −705`)*. **A payin of ~`₹2,350` clears it.**
> ⛔ **A MEASUREMENT OF THE THRESHOLD, ⛔ NOT a recommendation to pay in.**

⚠️ **How much of a T1-stock sale Zerodha releases into `margins().net` by the next morning is NOT
MEASURED — that moves the figure DOWN, ⛔ never up, so the conclusion is unaffected.**

> ### ⭐⭐ **THE TWO RISKS ARE MUTUALLY EXCLUSIVE, AND THAT IS THE MOST USEFUL LINE HERE:** **a
> hard-killed boot NEVER RUNS the monitor ⇒ NO new SELL GTT, and BOTH predictions score `NOT TESTED`.**
> ⇒ ⛔ **the phantom sell can ONLY happen on a boot that SURVIVES** — so *"pay in to make the boot
> work"* and *"avoid a phantom sell order"* pull in **OPPOSITE directions. Rama's call.**

---

## ④ ⭐ THE CALL — **CLOSES (`held = 0`)**, MODERATE · ⛔ **AND IT REFUTES THE RECREATE EXPECTATION**

**(P) `CLEANED` is written ONLY inside `_finalize_gtt_exit` (`:537`, `:587`)** ⇒ every row below
proves `held == 0` at that timestamp:
**ASKAUTOLTD `330462987` → CLEANED 05-Aug 10:45:51** *(~32 min, same session)* · **ASKAUTOLTD
`330660310` → CLEANED 06-Aug 10:47:46** *(~21 min)* · 🔑 **ATULAUTO `330657774` — healthy
`06-Aug 15:23:40`, CLEANED `07-Aug 08:15:41`** ⇒ ⭐⭐ **sold late in session D, `held = 0` at the D+1
08:15 BOOT — MANINFRA's shape EXACTLY.**

🔴 **(B) STAYS LIVE, ⛔ not softened:** ① **DIFFNKG proves the respawn is real here** — `330944932` was
minted by a `_recreate` on `07-Aug 15:20:35` ⇒ **1 measured respawn vs 3 measured clean exits** ②
⛔ **F6's own commit says the opposite for T+1** *("forced `held = 1` on **every T+1 exit**", "three
real SELL orders … against a holding of zero")* — ⭐ **I am calling AGAINST F6's generalisation and
naming that I am**; my ground is that the `gtt_state` timestamps date the **08:15-on-D+1** moment
exactly, while F6's sentence does not date its window ③ ⚠️ **MANINFRA was `T1: 4` (UNSETTLED) this
morning, so today's sale was of T1 stock — whether a T1 `−4` ages out on the same schedule is NOT
MEASURED, and this sale is one day fresher than any precedent. ⭐ That is why confidence is MODERATE.**

---

## ④b 🔑 ADDENDUM A — A DIRECT **API** MEASUREMENT · 🔴 **THE `−4` EXISTS** · ⛔ CALL UNCHANGED

> **`reconcile_positions` `2026-08-10T15:45:02.715`: `MANINFRA broker=−4 system=4 → QTY_MISMATCH` ·
> `DIFFNKG broker=0 system=1 → MISSING_AT_BROKER` · `cron FAILED exit 2`.**

⭐⭐ **`(P)` FROM THE BROKER API, by the system's OWN CRON — ⛔ not an operator UI reading. It
SUPERSEDES every screenshot in class, and it measures EXACTLY the deciding field:
`reconcile_positions` reads `positions()` ONLY** [[reconcile-positions-blind-t1-30jul]] — **the very
term `_gather` sums at `:464`.**
🔴 **⇒ THE NEGATIVE CNC ROW IS REAL AND WAS PRESENT AT 15:45. If it is still there at `08:15`,
`held = 0 + abs(−4) = 4` ⇒ MANINFRA lands in the RIGHT COLUMN — the recreate half.**
⭐ **It also corroborates ① independently: `system=4` vs `broker=−4` IS the DB believing it holds 4
while the broker has already sold them — the signature of an execution the system never saw.**
> ## ⛔ **WHAT IT DOES NOT SETTLE — THE WHOLE QUESTION: a `15:45` reading is not an `08:15` one.**
> **Whether the `−4` SURVIVES OVERNIGHT is precisely the ATULAUTO question, and ATULAUTO's answer
> (`held = 0` at the next 08:15 boot) was reached across EXACTLY this boundary.**
⇒ ⛔ **THE CALL STANDS: still `held = 0`, still CLOSE.** ⭐ **This RAISES THE STAKES on it, ⛔ it does
not decide it. If the `−4` persists my call is WRONG and the right column fires — ⭐ which is what a
falsifiable prediction is for.**
⚠️ **INCIDENTAL, ⛔ NOT CHASED: `reconcile_positions` RAN AND FAILED (exit 2) while the service has
been DEAD since `08:15:25` ⇒ 🔑 the CRON CHAIN IS INDEPENDENT OF THE SERVICE ⇒ ⭐ Rama has had
CRITICALs all day from a system that is not running.** [[boot-chain-token-watcher-05aug]]

---

## ④c 🔴 **CORRECTION — §③ IS WRONG. THE BOOT IS EXPECTED TO SURVIVE.**

> **(P) Zerodha Funds this morning: available `₹10,209.80` · opening `₹209.80` · payin `₹10,000`.**
> **⛔ RAMA ADDED `₹10,000` THIS MORNING, BEFORE ANY OF THIS WAS WRITTEN.**

**CORRECTED:** cash ≈ `10,209.80 + 451.68…474.76` ≈ **`₹10,661 – ₹10,685`** vs a `₹3,020.07`
requirement ⇒ **`positional_avail ≈ +₹2,291 … +2,298`** *(margin of safety ≈ `₹7,641`)*.
✅ **THE 11-Aug BOOT IS EXPECTED TO SURVIVE. ⛔ NO PAYIN IS NEEDED AND NONE SHOULD BE MADE.**

### 🏷️ **HOW IT HAPPENED — ⛔ WORSE THAN "A STALE SEED"**
§③ used **today's `fm_ledger` INIT (`209.80`)** — the seed recorded at `08:15`, **BEFORE the payin** —
as a proxy for **tomorrow's fresh `margins().net`**.
> ## ⛔⛔ **BUT I ALREADY HAD THE RIGHT NUMBER IN MY OWN PRIOR ARTEFACT AND DID NOT CARRY IT FORWARD:**
> **`PREDICTION_diffnkg_11-Aug-2026.md:133`, written HOURS EARLIER THE SAME EVENING, says *"On
> `₹10,209.80` the invariant passes"* — and [[delivery-book-ceiling-10aug]] §⑥ carried it too.**
> ⇒ 🏷️ **TWO PREDICTION FILES WRITTEN THE SAME NIGHT CONTRADICT EACH OTHER ON ONE OPERAND, AND THE
> *LATER* ONE IS WRONG.** ⭐ **[[feedback-carry-the-countermeasure-09aug]] in its DATA form: the figure
> was not re-derived — it was simply NOT LOOKED UP.**
⚠️ **And the mechanism is one this campaign already named: `fm_ledger` INIT is a DAILY seed, and
reading it as "current cash" is exactly the operand mismatch [[capital-vocabulary]] exists to
prevent.** ⛔ **Third appearance of that shape today.**

### 🔴 **THE CONSEQUENCE — IT INVERTS §③**
**The boot survives ⇒ `cnc_gtt_monitor` RUNS** ⇒ ⭐ **both predictions become genuinely TESTABLE**
⇒ 🔴 **AND THE PHANTOM SELL ORDER IS LIVE: Addendum A measured the `−4` PRESENT at 15:45, so if it
survives to 08:15, `held = 4` ⇒ the RIGHT column ⇒ A REAL SELL GTT FOR 4 SHARES HE NO LONGER OWNS** —
🚨 **and in the `triggered` sub-case `_reprotect` has NO `in_hours` gate ⇒ built AT 08:15, CRITICAL
and order SIMULTANEOUS, ⛔ no warning window.**
⛔ **NOTHING TOUCHED: no GTT, no hand-close of either row, no broker call, no VM command, ⛔ no payin.**
⭐ **He should simply KNOW before he wakes, so an 08:15 alert is RECOGNISED rather than discovered.**

---

## ④d ⛔ **IF THE PHANTOM GTT APPEARS TOMORROW — WHAT TO DO, AND WHAT NOT TO**

> ## ⛔⛔ **DO *NOT* DELETE IT.** **`:513` REBUILDS it** — measured on DIFFNKG on 07-Aug, and **Rama's
> own deletion this morning is why we are here.** 🔑 **The ONLY lever is STOPPING THE SERVICE, and
> that is RAMA'S CALL, ⛔ not ours.**

⚠️ **AND A GENERAL RULE MUST NOT ENTER THE RECORD WITHOUT ITS EXCEPTION.** The rule *"an UNEXPECTED
broker order is not automatically a BAD one — establish provenance before acting"* is **sound in
general** and ⛔ **wrong for this case:**
> ⭐ **A rebuilt MANINFRA GTT is a SELL for 4 shares the account NO LONGER OWNS — ⛔ not
> legitimate-but-surprising, a PHANTOM.** 🔑 **And its provenance is ALREADY ESTABLISHED IN ADVANCE:
> it is the right-hand column of a FROZEN PREDICTION written before the fact, with its signature
> named.**

⇒ 📌 **RECORD THE RULE *WITH* ITS EXCEPTION ATTACHED:**
> **"Establish provenance before acting on an unexpected broker order — ⛔ UNLESS a frozen prediction
> already names the signature, in which case THE PREDICTION *IS* THE PROVENANCE."**

⛔ **Otherwise *"investigate first"* means re-deriving tonight's work tomorrow morning UNDER TIME
PRESSURE.** ⭐ **If it appears with the predicted signature, it IS the phantom — RECORD IT AND SCORE
IT.** [[feedback-verify-the-finding-premise]]
