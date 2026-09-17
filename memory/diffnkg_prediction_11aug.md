---
name: diffnkg-prediction-11aug
description: "FROZEN PREDICTION written 10-Aug BEFORE the 11-Aug 08:15 boot: with the GTT deleted and gtt_state row ACTIVE qty=1, the outcome is a pure function of `held`. Expect branch (A) close; branch (B) — a NEW real SELL GTT — is live and Rama was told. Score before anything else."
metadata: 
  node_type: memory
  type: project
  originSessionId: 55f762b9-1f1c-4ab4-b80b-c1b50da706f7
  modified: 2026-08-10T10:26:18.715Z
---

📄 **`docs/audit/PREDICTION_diffnkg_11-Aug-2026.md`** *(main worktree, untracked alongside
`RECURRENCE_CEILING_10-Aug-2026.md`)*. ⛔ **FROZEN — no edit after `11-Aug 08:15 IST`. Score it
BEFORE anything else and BEFORE any deploy.**
🧪 **PARITY — LIVE-ONLY: a CNC settlement boundary.** ⛔ Paper has no T+1 model and
`_announce_paper_carry_blind_spot` exists because a paper run here produces artefacts that look like
proof. **No paper rehearsal is possible and none is claimed.** [[paper-cannot-exercise-class-26jul]]

---

## ① 🔴 THE PIVOTAL FINDING — AN UNSOURCED CLAIM, AND THE DATUM THAT LOOKED LIKE ITS SOURCE

> ## ⛔⛔ **THE ONE DATUM THAT LOOKED LIKE A BROKER READING OF DIFFNKG IS A DB READING.**

**`kill_switch.py` @`645728d` has TWO emitters of *"SPARED delivery position …"*, separated by a
`site=` suffix:** **`:1668-1691` `site=local-pass`** iterates `open_trades` — `qty` is
**`abs(trades.qty_filled)`**, product is `trades.product`, ⛔ **no broker call** · **`:1853-1874`
`site=broker-sweep`** iterates `get_positions()` and words it **`(broker product=CNC, …)`**.
**The quoted line reads `(product=CNC` ⇒ it is the LOCAL-PASS ⇒ a DB read.**
🔑 **And `get_holdings` was NEVER CALLED on 10-Aug** — the monitor never ran, B11-B15 all absent.
⇒ ⛔ **DIFFNKG's broker holdings/positions are UNKNOWN. The record's *"no holding at the broker"* is
WITHDRAWN as unsourced.** 🏷️ [[counts-db-rows-not-broker-06aug]] a THIRD time — ⭐ **this time inside
the EVIDENCE for a different incident, which is the harder place to catch it.**
⚠️ The broker-sweep is **not** suppressed for DIFFNKG *(local-pass deliberately does NOT add to
`handled_symbols`)*, so a broker CNC row WOULD have logged — ⛔ **but a 3-line excerpt is not a search
wide enough to establish absence** [[feedback-absence-needs-wide-check]], and the log is on the VM.

---

## ② THE LADDER — THE OUTCOME IS A PURE FUNCTION OF ONE INTEGER

**(P) MEASURED:** row `330944932` **ACTIVE**, **`qty = 1`**, **`needs_review = 0`** ⇒ ⛔ no stand-down.
Rama deleted the broker GTT ⇒ `bg = None` ⇒ `triggered`/`present_active` both **False** ⇒ branches 1-2
unreachable. **`held = Σ holdings.qty (signed, :456) + Σ abs(CNC positions.qty) (:464)`.**

| `held` | line | outcome |
|---|---|---|
| **0** | `:501` | `_finalize_gtt_exit("GTT_EXIT")` — **(A) CLOSES** |
| **1** | `:513` | `in_hours` **False** at 08:15 ⇒ `_queue_preopen` + WARNING; the real `_recreate` fires on the **FIRST IN-HOURS CYCLE** — **(B) a NEW REAL SELL GTT** |
| **≥2** | `:497` | `_qty_mismatch` — CRITICAL, `needs_review:=1`, no recreate — **(C)** |

⭐ **(C) is a branch the card did not name — CONSIDERED AND REFUTED by F6's own commit `c39e799`:**
*"a negative CNC row is a sale holdings() has ALREADY applied … forced **held = 1** on every T+1
exit"* ⇒ the sum is `0 + 1`, ⛔ never 2. **Unreachable in THIS shape, ⛔ not impossible in general.**

---

## ③ ⭐ EXPECT **(A)**. ⛔ MODERATE CONFIDENCE, ⛔ NOT A DETERMINATION

🔑🔑 **THE PRECEDENT IS MEASURED, ON THIS ACCOUNT, THIS CODE, THIS MONTH:** ATULAUTO `330657774`
(qty 1) created `06-Aug 10:02:13`, last verified `06-Aug 15:23:40`, **status `CLEANED`,
`updated_at = 2026-08-07T08:15:41`.** ⭐ **`CLEANED` is written by `_finalize_gtt_exit` (`:588`) and
by nothing else on this path ⇒ BRANCH 4 FIRED AT THE NEXT MORNING'S 08:15 BOOT.** The stranded row
self-resolved in ONE settlement cycle, and **DIFFNKG has had MORE time, not less.**
⭐ **And `330944932` was itself CREATED by a `_recreate` at `07-Aug 15:20:35`** — branch 5 requires the
previous GTT ABSENT from `get_gtts()`, and the ordinary way a resting GTT vanishes is that it
**TRIGGERED** ⇒ the share was most likely already sold. **That is the F6 signature exactly.**

🔴 **(B) STAYS LIVE, and ⛔ this must not be softened:** all of (A) rests on the `−1` having aged out
of `positions()`. If it has not ⇒ `abs(−1) = 1` ⇒ **(B)**. ⛔ **AND IF THE SHARE WAS NEVER SOLD**
(holdings 1, positions 0) **`held` is likewise 1 and (B) fires** — legitimately. ⛔ **Nothing readable
tonight separates those two.**

---

## ④ 🚨 **BRANCH (A) IS *NOT* THE HARMLESS ONE**

`_finalize_gtt_exit` never looks up what the share actually sold for. `_resolve_exit_price`
(`:673-692`): ① `get_trades()` is **TODAY-only** ⇒ a 07-Aug sale is NOT there ⇒ falls through ②
⭐ **`get_quote().last_price` — THIS is what will be used** *(market shut at 08:15 ⇒ Monday's close)*
③ else `entry_price 446.106`.
> 🔑 **A DERIVABLE BRACKET, ⛔ not a guessed number:** the `07-Aug 15:20:35` recreate SUCCEEDED with
> `sl_trigger 437.20` / `tgt_trigger 459.45`, and a GTT with a trigger on the wrong side of LTP is
> rejected ⇒ **`437.20 < LTP < 459.45` at that instant** ⇒ the written P&L lands in **`−8.91` to
> `+13.34`** minus costs, on 1 share.

⭐ **THE ERROR'S DIRECTION IS DETERMINABLE EVEN THOUGH THE P&L IS NOT:** SL leg ⇒ true fill `≤437.20`
⇒ **P&L OVERSTATED**; TARGET leg ⇒ true fill `≥457.15` ⇒ understated. **SL is the likelier shape**
⇒ 📌 **CALL: the P&L written tomorrow will be TOO FAVOURABLE.**
⇒ ⛔⛔ **(A) closes the row by writing a number NOBODY TRADED into the daily-loss reader, the
EXPECTANCY CORPUS and the win-rate — F6 cost #7. A gap is a loss; a manufactured number is a
CORRUPTION.** [[f6-delivery-exit-abs-defect-06aug]]

---

## ⑤ 🔴 TOLD RAMA TONIGHT · ⭐ AND THERE IS A ~1-HOUR WINDOW

**(B) would silently undo the deletion he performed deliberately, with a REAL SELL GTT. (A) writes a
fabricated P&L. BOTH are automatic at 08:15 unless the service is stopped.**
⭐⭐ **THE USABLE MIDDLE: under (B) the WARNING *"GTT missing pre-open — DIFFNKG"* fires at ~08:15 and
the `_recreate` only happens on the FIRST IN-HOURS CYCLE (`_drain_preopen`, `:117`, ~09:15+)** ⇒
**~1 hour in which the alert NAMES the outcome and the service can still be stopped before any order
reaches the exchange.**
⛔ **NOTHING WAS TOUCHED: no GTT, no hand-close, no deploy, no VM command. Tomorrow's boot doing it
IS the observation** — letting it run vs stopping first is **Rama's call.**

**FALSIFIERS (score by SIGNATURE, ⛔ never by narrative):** **(A)** `cnc_gtt_monitor.gtt_exit` +
`trades.status=CLOSED` + `gtt_state → CLEANED` + a `RELEASE_USED` for `446.106` · **(B)**
`queued_preopen:DIFFNKG` + WARNING, then a **NEW `gtt_id`** on the row · **(C)** CRITICAL *"GTT qty
mismatch"* + `needs_review=1` · **deferred** `deferred:broker_unavailable` ⇒ ⛔ **nothing learned; do
NOT read it as (A).**
---

## ⑥ 📎 ADDENDUM A — EVIDENCE THAT ARRIVED AFTER THE FREEZE · ⛔ THE CALL IS UNCHANGED

⛔⛔ **THE CALL, THE CONFIDENCE AND EVERY FALSIFIER ARE UNCHANGED AND MUST STAY UNCHANGED.** ⭐ The
expectation was **(A)** before this arrived and it is **(A)** after — **it narrows the UNKNOWN, ⛔ it
does not move the CALL.** Appended, ⛔ nothing above edited.

**RAMA SUPPLIED A ZERODHA HOLDINGS SCREENSHOT** (`kite.zerodha.com/holdings/equity`, ~10:13 IST
10-Aug): **`Holdings (1)` — ONE row, `MANINFRA`, `T1: 4`, delivered `0`, invested `₹460.92`.
⛔ DIFFNKG DOES NOT APPEAR.**

⚠️ **CLASS, HONESTLY: (P) but ⛔ NOT an API reading** — the broker's own UI, taken by the operator, ⛔
not `get_holdings()`, ⛔ not reproducible from any repo artefact. ⚠️⚠️ **AND `holdings ≠ positions`:
`_gather` sums BOTH (`:456` + `:464`) and this speaks ONLY to the first term. ⛔ It says NOTHING about
the CNC positions book — which is the term that actually decides.**

⇒ ⭐ **`Σ holdings.qty` for DIFFNKG = 0, MEASURED at the broker, before the boot ⇒ `held = 0 + Σ
abs(CNC positions.qty)` ⇒ ONE unknown where there were two.**
✅ **ELIMINATED: the *"the share was never sold"* sub-case of (B)** ⇒ 🔴 **if (B) fires, the new SELL
GTT is built against a HOLDING OF ZERO — the F6 signature, ⛔ not legitimate protection.**
⛔ **NOT settled: whether the `−1` CNC row has aged out. That, and only that, still separates (A)
from (B).**
⭐ **AND IT CORROBORATES §③'s third reason** *(the 07-Aug `_recreate` is what `abs()` does to a SOLD
position)* — **a holding of zero is exactly what that reasoning predicted, written before the
screenshot was seen.** ⛔ **(C) is now doubly unreachable — but its falsifier row STAYS, because a
prediction is scored against what was WRITTEN.**

🔑 **ONE SCREEN SETTLES THE REST — `kite.zerodha.com/positions`, ASKED OF RAMA TONIGHT:** no DIFFNKG
CNC row ⇒ `held = 0` ⇒ **(A) DETERMINED**; a DIFFNKG CNC row ⇒ `held = 1` ⇒ **(B) DETERMINED, and Rama
gets an HOUR'S WARNING instead of discovering a new SELL GTT.**
⛔ **NO BROKER CALL WAS OR WILL BE MADE FOR IT — the service is halted and stays halted.**
⚠️ **If it arrives pre-boot it CONFIRMS or REFUTES a frozen prediction ⇒ ⛔ RECORD THE SCORE, do NOT
retro-fit the reasoning.** ⭐ **Evidence arriving before the event still counts — but ONLY if the call
is left exactly as written, which it is.**

---

## ⑦ 🟢 ADDENDUM B — THE POSITIONS SCREEN · **THE INPUT STATE IS DETERMINED**

⛔⛔ **CALL, CONFIDENCE AND FALSIFIERS STILL UNCHANGED** — the expectation was **(A)** before either
screen existed, and a prediction is scored against **what was written**.

📜 **RAMA, 10-Aug ~14:00 IST:** *"`kite.zerodha.com/positions` = shows zero, since nothing traded/sold
from holdings [position = today trade items]."* ⇒ **`Σ abs(CNC positions.qty)` = 0.**

> ## ⭐⭐ **BOTH TERMS OF `_gather` ARE NOW MEASURED BEFORE THE BOOT: `held = 0` (`:456`) `+ 0` (`:464`) `= 0` ⇒ `:501` `_finalize_gtt_exit` ⇒ (A) DETERMINED AS AN *INPUT* STATE.**
> ⛔ **(B) and (C) are out of reach on this input — but their falsifier rows STAY exactly as written.**

⚠️ **THREE LIMITS, ⛔ not glossed:** ① **broker UI, ⛔ NOT an API reading** *(operator-supplied, same
class as Addendum A)* ② ⚠️ **the field the CODE consumes is not quite the field the sentence
describes — (P) `broker/zerodha_adapter.py:1228-1239`: `get_positions()` reads `raw["net"]`** *("use
`net` for open positions")* **and drops `quantity == 0`, while Rama's gloss names the DAY semantics.**
⭐ Both views are empty so the conclusion holds either way — ⛔ **but "the page showed zero" and "`net`
is empty" are two statements, recorded as two** ③ ⏰ **taken ~14:00 on 10-Aug; the boot is 08:15 on
11-Aug — market shut and nothing traded between, ⛔ but NOT simultaneous with the event.**

> ## ⛔ **WHAT IT DOES *NOT* DO: it determines the INPUT. ⛔ It is NOT evidence that tomorrow's code EXECUTED branch (A).** The ladder is a claim about what the monitor **does** with `held = 0`, and **the monitor has not run since 07-Aug.** ⭐ **Only tomorrow's boot can supply that.**

🔑 **AND THE SECOND, INDEPENDENT PREDICTION IS UNAFFECTED AND IS NOW THE INTERESTING ONE: *"the P&L
written will be TOO FAVOURABLE."*** ⛔ **Neither screen speaks to it.** ⭐ **Score it SEPARATELY — it
is the one that matters for the EXPECTANCY CORPUS** (F6 cost #7).

## ⑧ 🔑 ADDENDUM C — A DIRECT **API** MEASUREMENT · ⭐ BETTER CLASS THAN A OR B · ⛔ CALL UNCHANGED

> **`reconcile_positions` `2026-08-10T15:45:02.715`: `DIFFNKG broker=0 system=1 → MISSING_AT_BROKER`
> · `MANINFRA broker=−4 system=4 → QTY_MISMATCH` · `cron FAILED exit 2`.**

⭐⭐ **`(P)` FROM THE BROKER API by the system's OWN CRON — ⛔ not an operator UI reading — and it
measures the RIGHT field: `reconcile_positions` reads `positions()` ONLY**
[[reconcile-positions-blind-t1-30jul]], **exactly the term `_gather` sums at `:464`.**
> ## ⇒ **`Σ abs(CNC positions.qty)` = 0 for DIFFNKG BY API. With Addendum A's holdings = 0, BOTH terms of `held` are confirmed at the STRONGEST available class ⇒ `held = 0` ⇒ `:501` ⇒ (A).**
⚠️ **A and C are COMPLEMENTARY, ⛔ not redundant: C speaks to POSITIONS only, so HOLDINGS still rests
on A's UI capture. ⛔ Neither is a `get_holdings()` call.** ⏰ **And 15:45 is closer than 14:00 but
still ⛔ NOT simultaneous with an 08:15 event.**
⚠️ **INCIDENTAL, ⛔ NOT CHASED: the job RAN AND FAILED (exit 2) while the service has been DEAD since
`08:15:25` ⇒ 🔑 the CRON CHAIN IS INDEPENDENT OF THE SERVICE.** [[boot-chain-token-watcher-05aug]]

---

⚠️ **PRIOR CONDITION: the boot must REACH the monitor.** At `₹10,209.80` the invariant passes
(`3,062.94 − 907.02 = +2,155.92`) — ⛔ **but if it hard-kills again, every row is VOID and the answer
is `NOT TESTED`, exactly as 10-Aug scored.**
