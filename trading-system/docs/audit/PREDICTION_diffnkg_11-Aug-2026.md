# FROZEN PREDICTION — WHAT THE 11-Aug-2026 08:15 BOOT WILL DO TO THE DIFFNKG ROW

**WRITTEN 10-Aug-2026, BEFORE THE BOOT.** ⛔ Nothing in this file may be edited after
`2026-08-11 08:15 IST`. Score it tomorrow **before anything else, and before any deploy.**

**CODE UNDER TEST: the DEPLOYED ref `645728d`** — nothing has been pushed or deployed, so tomorrow's
boot runs the OLD code. Every line number and predicate below was read from
`git show 645728d:orders/cnc_gtt_monitor.py` (md5 `025498f4ae05776915da2c242fdcc86e`), ⛔ not from
`main` and ⛔ not from any fix branch. **`M3`: line numbers hold only at their measured SHA.**

**PARITY — LIVE-ONLY, AND IT MUST BE SAID.** This is a **CNC settlement-boundary** event. Paper has
no T+1 settlement model, never calls `get_holdings()`/`get_positions()` for a delivery carry, and
`_announce_paper_carry_blind_spot` exists precisely because a paper run produces artefacts that look
like proof here. ⛔ **No paper rehearsal of this prediction is possible, and none is claimed.**

---

## §1 — THE STATE, WITH EACH FACT'S EVIDENCE CLASS

| # | fact | class | source |
|---|---|---|---|
| 1 | `gtt_state` row `330944932`, DIFFNKG, `exit_side SELL`, **`qty = 1`**, **`status ACTIVE`**, **`needs_review = 0`**, created `2026-08-07T15:20:35` | **(P) MEASURED** | `capture_10aug2026/A_db_capture.txt` §G |
| 2 | `trd_010f8e21…` DIFFNKG **`OPEN`**, `qty_filled 1`, `entry_actual_price 446.1`, `margin_reserved 446.106` | **(P) MEASURED** | same, §C |
| 3 | The ENTRY order is `product = CNC` | **(P) MEASURED** | `C_orders_logs.txt` §I2 |
| 4 | Rama manually deleted broker GTT `330944932` on 10-Aug | **(P) OPERATOR-REPORTED** | `RECURRENCE_CEILING_10-Aug-2026.md` §7 |
| 5 | The monitor **never ran** on 10-Aug — the boot died at `08:15:25.680`, upstream of it | **(P) MEASURED** | `D_boot_logs.txt`; record §6.2 line 326 |
| 6 | **DIFFNKG's broker holdings / positions on 10-Aug** | 🔴 **NOT MEASURED — NO READING EXISTS** | see §1.1 |

### §1.1 — 🔴 A CLAIM IN THE RECORD DOES NOT SURVIVE RE-READING, AND IT IS THE PIVOTAL ONE

The record says DIFFNKG has *"no holding at the broker"* (§7). **That claim is not sourced to any
measurement in the capture, and the one log line that looks like it supports it does not.**

```
08:15:25.689  CRITICAL kill_switch: SPARED delivery position DIFFNKG (product=CNC, qty=1)
```

**(P)** `kill_switch.py` at `645728d` has **two** sites emitting that sentence, distinguished by a
`site=` suffix:

- **`:1668-1691`, `site=local-pass`** — iterates `open_trades` (**the DB**). `qty` is
  `local_qty = abs(trade["qty_filled"])`, and `product` is `trades.product`. **No broker call.**
- **`:1853-1874`, `site=broker-sweep`** — iterates `self._adapter.get_positions()`. Its wording is
  `(broker product=CNC, qty=%d)`.

The quoted line reads `(product=CNC` — ⛔ **not** `(broker product=CNC` — so it is the **local-pass**,
i.e. **a DB read of `trades.qty_filled`, `abs()`-ed.** It says nothing whatever about the broker.

> ## ⛔⛔ **THE ONE DATUM THAT LOOKED LIKE A BROKER READING OF DIFFNKG IS A DB READING.**
> 🏷️ [[counts-db-rows-not-broker-06aug]] striking a third time, inside the evidence for a different
> incident. ⭐ **And `get_holdings` was NEVER CALLED on 10-Aug** — record §6.2 line 326 lists
> `B11–B15 | get_positions → get_holdings → … | NONE emitted by the monitor | absent`.

⚠️ The `broker-sweep` site is **not** suppressed for DIFFNKG (`local-pass` deliberately does **not**
add to `handled_symbols`, `:1693-1696`), so a broker CNC row **would** have produced a
`site=broker-sweep` line. None appears in the record's excerpt — but **an excerpt of three lines is
not a search wide enough to establish absence** ([[feedback-absence-needs-wide-check]]), and the
underlying log is on the VM, which is out of bounds tonight. ⇒ **Recorded as UNKNOWN, not as zero.**

---

## §2 — THE LADDER, AND WHY THE OUTCOME IS A PURE FUNCTION OF ONE INTEGER

`orders/cnc_gtt_monitor.py` @ `645728d`:

```
:451-465  _gather()     held[sym] = Σ holdings.qty            (signed, :456)
                                  + Σ abs(positions.qty)      for product == CNC   (:464)
:473      held    = int(held_qty.get("DIFFNKG", 0))
:474      row_qty = 1                                          (measured, §1 fact 1)
:479      needs_review == 0  ->  NOT stood down; the row IS processed
:481-484  bg = broker_gtts.get("330944932")  ->  None (deleted)
          => triggered = False,  present_active = False
```

With `bg = None` and `row_qty = 1`, branches 1 and 2 are unreachable and **exactly three outcomes
remain**, selected solely by `held`:

| `held` | branch | line | what happens |
|---|---|---|---|
| **0** | 4 — *Holding FLAT* | `:501-510` | `_finalize_gtt_exit(reason="GTT_EXIT")` — **(A) the trade CLOSES** |
| **1** | 5 — *GTT missing, holding intact* | `:513-521` | `in_hours` is **False** at 08:15 ⇒ `_queue_preopen` + a **WARNING** alert; the real `_recreate` fires on the **first in-hours cycle** — **(B) a NEW SELL GTT** |
| **≥ 2** | 3 — *QTY MISMATCH* | `:497-498` | `_qty_mismatch` — CRITICAL, `needs_review := 1`, no recreate — **(C)** |

### ⭐ (C) is a third branch the card did not name — and I am recording it as CONSIDERED AND REFUTED
`held ≥ 2` needs holdings **and** a CNC positions row to both contribute — the shape `holdings = 1`
with `positions = −1` (a sale the settled book has not yet applied) would give `1 + abs(−1) = 2`.
**F6's own commit message (`c39e799`) refutes it by measurement:** *"a negative CNC row is a sale
holdings() has ALREADY applied, so abs() double-counted it and forced **held = 1** on every T+1
exit."* ⇒ holdings is already 0 on the sell side, and the sum is `0 + 1 = 1`, ⛔ never 2. **(C) is
recorded as unreachable in this shape, not as impossible in general.**

---

## §3 — THE PREDICTION

> ## ⭐ **I EXPECT BRANCH (A): `held` reaches 0 and the trade CLOSES with `reason="GTT_EXIT"`.**
> **Confidence: MODERATE. ⛔ NOT a determination — the deciding integer is a broker reading nobody
> has taken, and §1.1 shows the record's own claim about it is unsourced.**

**WHY (A):**

1. ⭐⭐ **The ATULAUTO precedent, on this account, this code, this month — and it is MEASURED:**
   `gtt_state 330657774` (ATULAUTO, qty 1) was created `06-Aug 10:02:13`, last verified
   `06-Aug 15:23:40`, and its status is **`CLEANED`** with `updated_at = 2026-08-07T08:15:41`.
   **`CLEANED` is written by `_finalize_gtt_exit` (`:588`) and by nothing else on this path** ⇒
   **branch 4 fired at the NEXT MORNING'S 08:15 BOOT.** The stranded row self-resolved in one
   settlement cycle.
2. **DIFFNKG has had MORE settlement time than ATULAUTO needed**, not less: the sale is on/before
   07-Aug, and tomorrow is the **second** morning after (10-Aug's boot could not look).
3. **The row's own history says the share was most likely already sold.** `330944932` was *created*
   `07-Aug 15:20:35` by a `_recreate` — branch 5 requires the previous GTT to be **absent from
   `get_gtts()`**, and the ordinary way a resting GTT disappears is that it **triggered and
   executed**. That is the F6 signature exactly, and it is why DIFFNKG is on record as *the*
   live-money item.

**WHY (B) IS STILL LIVE — and this is the part that must not be softened:** the whole of (A) rests on
the `−1` CNC row having aged out of `positions()`. If it has not — a settlement quirk, a partial, or
simply this account behaving unlike the ATULAUTO instance — `abs(−1) = 1` and **(B) fires.** ⛔ **And
if the share was never sold at all** (holdings still 1, positions 0), **held is likewise 1 and (B)
fires** — with the difference that the recreate would then be *legitimate* protection. **Nothing I
can read tonight separates those two.**

### 🔴 FALSIFIERS — score these tomorrow, in this order, before anything else

| branch | fires iff | the log/DB signature that PROVES it |
|---|---|---|
| **(A)** | `held == 0` | `cnc_gtt_monitor.gtt_exit` INFO with `trade_id=trd_010f8e21…`; `trades.status` → `CLOSED`; `gtt_state 330944932` → **`CLEANED`**; a `RELEASE_USED` `fm_ledger` row for `446.106`; a **WARNING** alert *"GTT exit — DIFFNKG"* |
| **(B)** | `held == 1` | at ~08:15 a **WARNING** *"GTT missing pre-open — DIFFNKG"* + action `queued_preopen:DIFFNKG`; then at the **first in-hours cycle** a `_drain_preopen` → `_recreate` and **a NEW gtt_id** on the row |
| **(C)** | `held ≥ 2` | **CRITICAL** *"GTT qty mismatch — DIFFNKG"*, `gtt_state.needs_review` → `1`, no recreate |
| **none** | broker gather raised | `deferred:broker_unavailable` + WARNING *"GTT reconcile deferred"* — ⛔ **and then nothing is learned; do not read it as (A)** |

⚠️ **A prior condition on all four:** the boot must reach the monitor at all. On `₹10,209.80` the
capital invariant passes (`3,062.94 − 907.02 = +2,155.92`), so it should — ⛔ **but if the boot
hard-kills again, every row above is VOID and the answer is `NOT TESTED`, exactly as 10-Aug scored.**

---

## §4 — IF (A) FIRES, THE P&L WRITTEN WILL BE FABRICATED. THE DIRECTION, DERIVED.

`_finalize_gtt_exit` does **not** look up what the share actually sold for. It calls
`_resolve_exit_price` (`:673-692`), a three-step fallback:

1. **`get_trades()`** — the broker's **TODAY-only** trade book, scanned for a DIFFNKG `SELL`.
   **The real sale was on/before 07-Aug ⇒ it will NOT be there ⇒ this step falls through.**
2. **`get_quote(["DIFFNKG"]).last_price`** — ⭐ **this is what will be used.** At 08:15 the market is
   shut, so it is the **last traded price**, i.e. Monday's close.
3. else `entry_price` = `446.106` (would write `pnl ≈ −charges`).

Then `pnl = (exit_price − 446.106) × 1 − CNC round-trip costs`, written to `trades`, to `fm_ledger`
as `pnl_delta`, and published as `PositionClosed`.

> ### 🔑 **A DERIVABLE BRACKET, ⛔ not a guessed number.** The `_recreate` at `07-Aug 15:20:35`
> **succeeded** (the row exists, `ACTIVE`), and it placed `sl_trigger 437.20` / `tgt_trigger 459.45`
> against a freshly-fetched LTP. A GTT whose trigger sits on the wrong side of LTP is rejected ⇒
> **at that instant `437.20 < LTP < 459.45`.** ⇒ absent a move beyond those bounds since, the
> written P&L lands in **`−8.91` to `+13.34`**, minus costs, on 1 share.

**AND THE DIRECTION OF THE *ERROR* IS DETERMINABLE EVEN THOUGH THE P&L IS NOT:**

- If the real exit was the **SL** leg, the true fill was `≤ 437.20` ⇒ the fabricated price is a later,
  higher one ⇒ **the written P&L is OVERSTATED — the loss is recorded as smaller than it was.**
- If the real exit was the **TARGET** leg, the true fill was `≥ 457.15` ⇒ **the written P&L is
  UNDERSTATED.**

⭐ **The SL leg is the likelier of the two** (a protected delivery position that leaves without its
trade closing is the shape F6 was written for), ⇒ **my directional call: the P&L written tomorrow
will be TOO FAVOURABLE.**

> ## ⛔⛔ **SO BRANCH (A) IS *NOT* THE HARMLESS ONE. It closes the row by writing a number nobody
> traded into the daily-loss reader, the EXPECTANCY CORPUS and the win-rate** — F6 cost #7, and
> **a gap is a loss; a manufactured number is a CORRUPTION.**

---

## §5 — 🔴 WHAT RAMA MUST BE TOLD TONIGHT (§1.2)

**Branch (B) is live**, and under it **a NEW real SELL GTT is placed on DIFFNKG** — ⭐ **silently
undoing the deletion he performed deliberately this morning.** He should not discover it back.

**And (A) is not a free pass either** — it writes a fabricated exit price and P&L into the corpus.

**Both are automatic at the 08:15 boot unless the service is stopped.** ⛔ I have taken no action:
no GTT touched, no row hand-closed, nothing deployed, no VM command. **Tomorrow's boot doing it IS
the observation** — the choice to let it run, or to stop the service first and forgo the observation,
is his.

⭐ **There is a usable middle:** under (B) the **WARNING at ~08:15 precedes the GTT** — the recreate
only happens on the **first in-hours cycle** (~09:15+, `_drain_preopen`, `:117`). **That is a ~1-hour
window in which the alert names the outcome and the service can still be stopped before any order
reaches the exchange.**

---

## §6 — SCORING ORDER TOMORROW (⛔ before any deploy)

1. Did the boot reach the monitor at all? If not ⇒ **all of §3 is `NOT TESTED`**, ⛔ not "wrong".
2. Which of (A)/(B)/(C)/deferred fired — by the §3 signature table, ⛔ never by narrative.
3. If (A): record `exit_price`, `pnl`, and **whether the error direction matched §4's call.**
4. If (B): record the **new `gtt_id`** and whether the alert preceded it, as §5 predicts.
5. Only then: anything else, including the deploy decision.

---

# ADDENDUM A — EVIDENCE ARRIVING AFTER THE PREDICTION WAS FROZEN

**Added 10-Aug-2026, still before the boot.** ⛔ **THE CALL, THE CONFIDENCE AND EVERY FALSIFIER ABOVE
ARE UNCHANGED AND MUST STAY UNCHANGED.** ⭐ The expectation was **(A)** before this arrived and it is
**(A)** after; this addendum narrows the *unknown*, it does not move the *call*. Nothing above was
edited — this is appended.

### A.1 — WHAT ARRIVED

**Rama supplied a Zerodha holdings screenshot, `kite.zerodha.com/holdings/equity`, taken ~10:13 IST
on 10-Aug-2026.** It shows:

> **`Holdings (1)` — a single row: `MANINFRA`, `T1: 4`, delivered qty `0`, invested `₹460.92`.
> ⛔ DIFFNKG DOES NOT APPEAR.**

### A.2 — EVIDENCE CLASS, STATED HONESTLY

**(P) MEASURED — but qualified on two axes, and both qualifications matter:**

1. ⚠️ **It is the broker's own UI, ⛔ NOT an API reading.** It is not `get_holdings()` output, it was
   not taken by the system, and it is not reproducible from any artefact in the repo. It is an
   **operator-supplied capture**, and it is recorded as one.
2. ⚠️⚠️ **`holdings` ≠ `positions`, and the term that actually decides is `positions`.**
   `_gather` (`:451-465`) sums **both**: `Σ holdings.qty` (`:456`) **plus** `Σ abs(CNC positions.qty)`
   (`:464`). This screenshot speaks only to the **first** term. ⛔ **It says nothing whatever about
   the CNC positions book.**

### A.3 — WHAT IT SETTLES, AND WHAT IT DOES NOT

> ## ⭐ **`Σ holdings.qty` for DIFFNKG = 0, measured at the broker, before the boot.**
> ⇒ **`held = 0 + Σ abs(CNC positions.qty)`. ONE unknown remains where there were two.**

**ELIMINATED:** the sub-case named in §3 as *"if the share was never sold at all (holdings still 1,
positions 0), `held` is likewise 1 and (B) fires — legitimately."* ⛔ **That branch is now dead: the
share is not in holdings.** ⇒ **if (B) fires, the new SELL GTT would be built against a holding of
zero** — the F6 signature, ⛔ not legitimate protection.

**NOT SETTLED:** whether the `−1` CNC row has aged out of `positions()`. **That, and only that, still
separates (A) from (B).**

**AND IT CORROBORATES §3's third reason** — that `330944932` was created by a `_recreate` on 07-Aug,
which is what the `abs()` defect does to a sold position. ⭐ **A holding of zero is exactly what that
reasoning predicted, and it was written before this screenshot was seen.**

⛔ **(C) `held ≥ 2` is now doubly unreachable** — it required a holdings contribution, and holdings is
zero. **Recorded; the falsifier row stays in the table regardless, because a prediction is scored
against what was written.**

### A.4 — 🔑 ONE SCREEN WOULD SETTLE THE REST, AND IT IS BEING ASKED FOR TONIGHT

**`kite.zerodha.com/positions`:**

- **No DIFFNKG CNC row ⇒ `held = 0` ⇒ (A) is DETERMINED, not expected.**
- **A DIFFNKG CNC row ⇒ `held = 1` ⇒ (B) is DETERMINED** — ⭐ **and Rama gets an hour's warning that a
  new SELL GTT will be built, instead of discovering it after the fact.**

⛔ **NO BROKER CALL WAS MADE OR WILL BE MADE TO OBTAIN THIS.** The service is halted and stays halted;
the screen is Rama's to read.

> ⚠️ **IF IT ARRIVES BEFORE THE BOOT, IT CONFIRMS OR REFUTES A FROZEN PREDICTION.** ⛔ **Record the
> score; do NOT retro-fit the reasoning.** ⭐ A prediction settled by evidence that arrived before the
> event still counts — **but only if the call is left exactly as written**, which it is.

---

# ADDENDUM B — THE POSITIONS SCREEN. **THE INPUT STATE IS NOW DETERMINED.**

**Added 10-Aug-2026, still before the boot.** ⛔ **THE CALL, THE CONFIDENCE AND EVERY FALSIFIER ABOVE
REMAIN UNCHANGED.** ⭐ The expectation was **(A)** before either screen existed; a prediction is scored
against **what was written**, so nothing above is edited. This is appended.

### B.1 — WHAT ARRIVED

> **Rama, 10-Aug-2026 ~14:00 IST:** *"`kite.zerodha.com/positions` = shows zero, since nothing
> traded/sold from holdings [position = today trade items]."*

⇒ **`Σ abs(positions.qty for CNC)` for DIFFNKG = 0.**

### B.2 — BOTH TERMS OF `_gather` ARE NOW MEASURED BEFORE THE BOOT

| term | line | value | source |
|---|---|---|---|
| `Σ holdings.qty` | `:456` | **0** | Addendum A — holdings screen, DIFFNKG absent |
| `Σ abs(CNC positions.qty)` | `:464` | **0** | this addendum — positions screen empty |

> ## **`held = 0 + 0 = 0` ⇒ branch 4 at `:501` ⇒ `_finalize_gtt_exit(reason="GTT_EXIT")`.**
> ⭐ **(A) is DETERMINED as an INPUT state, ⛔ no longer merely expected.**

⇒ **(B) and (C) are both out of reach on this input.** ⛔ Their falsifier rows in §3 **stay exactly as
written** — the table is what the prediction will be scored against.

### B.3 — ⚠️ THREE LIMITS, STATED RATHER THAN GLOSSED

1. **It is the broker's UI, ⛔ not an API reading.** Same class as Addendum A: operator-supplied, not
   `get_positions()` output, not reproducible from any repo artefact.
2. ⚠️ **The field the code consumes is not quite the field the sentence describes.** **(P)
   `broker/zerodha_adapter.py:1228-1239`: `get_positions()` reads `raw["net"]`** — *"kite returns
   `{"day": [...], "net": [...]}` — use `net` for open positions"* — **and drops any row with
   `quantity == 0`.** Rama's gloss (*"position = today trade items"*) names the **day** semantics.
   Here both views are empty and the conclusion is the same either way, ⛔ **but "the page showed
   zero" and "`net` is empty" are not the same statement, and this records them as two.**
3. ⏰ **The reading is ~14:00 on 10-Aug; the boot is 08:15 on 11-Aug.** The market was shut throughout
   and nothing traded — ⛔ **but it is NOT simultaneous with the event, and must not be recorded as
   if it were.**

### B.4 — ⛔ WHAT THIS DOES **NOT** DO

> **It determines the INPUT. ⛔ It is NOT evidence that tomorrow's code executed branch (A).**

The ladder is a claim about what `cnc_gtt_monitor` **does** with `held = 0` — and the monitor has not
run since 07-Aug. **Only tomorrow's boot can supply that, and nothing else can.** ⭐ The observation
still has to happen, and §6's scoring order is unchanged.

⚠️ **AND THE PRIOR CONDITION STILL DOMINATES EVERYTHING:** if the boot hard-kills again, `held` is
never computed, and the whole prediction scores **`NOT TESTED`** — ⛔ not "wrong", exactly as 10-Aug
scored E2.

🔑 **THE SECOND, INDEPENDENT PREDICTION IS UNAFFECTED AND IS NOW THE INTERESTING ONE:** §4's call that
**the P&L written will be TOO FAVOURABLE.** ⛔ Neither screen speaks to it. ⭐ **Score it separately —
it is the one that matters for the expectancy corpus** (F6 cost #7).

---

# ADDENDUM C — A DIRECT API MEASUREMENT. ⭐ **BETTER CLASS THAN A OR B.**

**Added 10-Aug-2026, still before the boot.** ⛔ **CALL, CONFIDENCE AND FALSIFIERS UNCHANGED.**

> **`reconcile_positions`, `2026-08-10T15:45:02.715` IST:**
> **`DIFFNKG: broker=0 system=1 → MISSING_AT_BROKER`** · `MANINFRA: broker=−4 system=4 → QTY_MISMATCH`
> **`cron:reconcile_positions FAILED — exit code 2`**

⭐⭐ **THIS SUPERSEDES ADDENDA A AND B IN EVIDENCE CLASS: it is `(P)` from the BROKER API, produced by
the system's own cron, ⛔ not an operator reading a UI.**

**AND IT MEASURES THE RIGHT FIELD.** `reconcile_positions` reads **`positions()` only** — it is on
record as blind to delivery T+1 — which is **exactly the term `_gather` sums at `:464`**. So
`broker=0` for DIFFNKG is a direct reading of the second term of `held`.

> ## ⇒ **`Σ abs(CNC positions.qty)` = 0 for DIFFNKG, BY API. With Addendum A's holdings = 0, BOTH terms of `held` are now confirmed at the strongest available class. `held = 0` ⇒ `:501` ⇒ (A).**

⚠️ **The two addenda remain complementary, ⛔ not redundant:** `reconcile_positions` speaks to
**positions** only, so **holdings still rests on Addendum A's UI capture.** ⛔ Neither is an
`get_holdings()` call.

⏰ **AND IT IS A 15:45 READING AGAINST AN 08:15 EVENT** — closer than 14:00, still not simultaneous.
⛔ **The call does not move.**

### ⚠️ INCIDENTAL, RECORDED AND ⛔ NOT CHASED TONIGHT

**`reconcile_positions` RAN — and FAILED with exit 2 — while the trading service has been dead since
`08:15:25`.** ⇒ 🔑 **the cron chain is INDEPENDENT of the service**, which is consistent with
`token-watcher` polling a file rather than anything starting the app. ⭐ **So Rama has been receiving
CRITICALs all day from a system that is not running.** ⛔ **Filed, not investigated.**

---

# ADDENDUM D — CROSS-REFERENCE: **THE BOOT IS EXPECTED TO SURVIVE**

**Added 10-Aug-2026, before the boot.** ⛔ **THE CALL, CONFIDENCE AND FALSIFIERS ARE UNCHANGED.**

**(P) Zerodha Funds this morning: available `₹10,209.80` · opening `₹209.80` · payin `₹10,000`** —
Rama added ₹10,000 before any of this was written. With the MANINFRA proceeds, tomorrow's cash is
**≈ `₹10,661 – ₹10,685`** against a `₹3,020.07` requirement ⇒ **`positional_avail ≈ +₹2,291`.**

✅ **§3's "prior condition on all four" is therefore expected to be SATISFIED** — this file's own
line 133 already said *"On `₹10,209.80` the invariant passes"*, and that remains right.
⚠️ ⛔ **`NOT TESTED` stays a valid outcome if the boot dies for any OTHER reason.**

🔴 **AND THE CONSEQUENCE FOR THE *OTHER* ROW: with the boot surviving, `cnc_gtt_monitor` RUNS, so
MANINFRA's phantom-sell risk is LIVE tomorrow.** See `PREDICTION_maninfra_11-Aug-2026.md` §2 and
Addendum B — ⛔ **its §3 forecast (`₹661–685`) is SUPERSEDED and must not be quoted.**
