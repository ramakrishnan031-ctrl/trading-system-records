# FILE 21 — MIS AUTO-SQUARE-OFF · THE 27-Aug ₹59 RECONCILED

🔬 MEASURED · 📄 EVIDENCE · 💭 INFERENCE · 👤 RAMA'S · 🏷️ VACUOUS / NOT EXERCISED.

> ## 🔴 **VERDICT: A GAP IS PROVEN — AND IT IS A *TIMING* GAP, ⛔ NOT A SELECTION GAP.**
> ✅ **H-1 (CAS) — CONFIRMED.** ⛔ **H-2 (SHORT) — REFUTED, from the code.**
> ✅ The selector is already correct: MIS/CO only · `qty != 0` · direction-aware ·
> broker-authoritative product. ⛔ **Nothing in D-2 / D-3 needs building.**
> 🔴 The single defect: **the system's square-off runs at `15:17`; a CAS stock's
> broker cutoff is `15:12`.** ⇒ For any F&O stock the system is **5 minutes late,
> structurally, every time.**

---

## §1 — THE BROKER FACTS, SEARCHED AND RECORDED

📄 **Source, fetched 28-Aug:** `support.zerodha.com` →
*"What are the auto square-off timings for open intraday positions?"*
(`/category/trading-and-markets/trading-faqs/market-sessions/articles/intraday-auto-square-off-timings`).
⚠️ FILE 21's cited URL 404s; the live path is the one above. ⛔ Not recall, ⛔ not a
Copilot summary.

| segment | cutoff |
|---|---|
| **CAS stocks** | **3:12 PM** |
| Non-CAS stocks | 3:25 PM |
| F&O contracts | 3:26 PM |
| MCX | 10 minutes before market close |

📄 Verbatim: *"a ₹50 + 18% GST for each order squared off"* ·
*"Zerodha's risk management team may adjust these timings based on market volatility."*
⇒ ⛔ **These are NOT constants.**

⚠️ Also standing: *"the selection and sequence of such square-offs are at Zerodha's
sole discretion"* and *"Zerodha may square off positions, it is under no obligation
to do so"* ⇒ ⛔ **broker square-off is NOT a safety net.**

### ⭐ WHAT "CAS" MEANS — and it is the whole answer

📄 **CAS = SEBI's Closing Auction Session.** 📄 Zerodha: *"Since continuous trading
for CAS stocks ends at 3:15 PM, Zerodha adjusts the intraday (MIS and CO)
auto-square-off timings for these securities"* → **3:12 PM**; and *"Zerodha does not
change the auto square-off timings for non-F&O stocks"* → **3:25 PM as usual.**

> 🔴 ⭐ **CAS MEMBERSHIP KEYS OFF F&O MEMBERSHIP — AND THE SYSTEM ALREADY HOLDS THAT
> ATTRIBUTE.** 🔬 `config/instruments.csv` column **`is_fno`**.
> ⇒ R-4 is answerable **locally**, ⛔ no list to scrape, ⛔ no inference.

⚠️ 🏷️ **PARTIALLY MEASURED:** the support page links a CAS article but ⛔ does **not**
publish the constituent list. `is_fno` is the best available proxy and is 📄 *directly*
supported by Zerodha's own wording ("non-F&O stocks"). ⛔ It is not a copy of NSE's
CAS register.

### 🔬 THE ARITHMETIC

```
₹50 × 1.18 = ₹59.00      27-Aug ledger line = ₹59.00      ⇒ EXACTLY ONE ORDER
```

⚠️ **CAVEAT RETAINED, ⛔ not dropped:** a large position can split into multiple
square-off orders (30,000-qty chunks), each charged. ⭐ At **1–2 share** sizes that
cannot apply here — but the caveat stands for any future reading.

---

## §2 — THE RECONCILIATION · R-1 … R-8

### R-1 · THE LEDGER LINE — permanent wording

> *"27-Aug Zerodha ledger shows ₹59.00 debit, 'Call and Trade charges(Auto Square
> Off) for 2026-08-27' — 🔬 **MEASURED BROKER-LEDGER EVIDENCE**. ⭐ ₹50 + 18% GST per
> order ⇒ exactly **ONE** order. ⛔ Causal mapping to a specific MIS position NOT YET
> PROVEN. ⛔ Failure of system-side MIS square-off NOT YET PROVEN."*

⛔ *"Our auto-square-off failed"* is **not** written, and §2 below shows the truer
statement is different in kind: **the system never got the chance.**

### R-2 · EVERY 27-Aug MIS POSITION, RECONSTRUCTED FROM RECORD

🔬 Product read the HAZ-4-safe way — `orders.product` via `LEFT JOIN … leg='ENTRY'`.
⭐ **The five symbols in the screenshots are confirmed against the DB, ⛔ not trusted
from the screenshot:** BIKAJI · MOSCHIP · OAL · SHANTIGOLD · TATAPOWER.

| symbol | dir | qty | entry | exit | `exit_reason` | `status` | closed by | `is_fno` |
|---|---|---|---|---|---|---|---|---|
| **TATAPOWER** | **SHORT** | 1 | 10:02:25 | **15:12:47** | `MANUAL` | `CLOSED_MANUAL` | 🔴 **EXTERNAL** | **true** |
| SHANTIGOLD | **SHORT** | 2 | 10:03:18 | 10:30:59 | `SL_HIT` | `CLOSED` | ✅ system SL | false |
| OAL (MIS) | LONG | 1 | 10:07:18 | 10:09:35 | `SL_HIT` | `CLOSED` | ✅ system SL | false |
| BIKAJI | LONG | 1 | 10:10:25 | 10:55:54 | `SL_HIT` | `CLOSED` | ✅ system SL | false |
| **MOSCHIP** | LONG | 2 | 13:13:41 | **15:16:35** | `MANUAL` | `CLOSED_MANUAL` | 🔴 **EXTERNAL** | false |

⚠️ **`OAL` APPEARS TWICE ON 27-Aug AND THEY ARE DIFFERENT TRADES** — an **MIS** trade
(10:07:18 → `SL_HIT` 10:09:35) and a **CNC** trade (10:14:21 → `GTT_EXIT` 14:33:41).
⛔ Do not conflate them in any future reading.

🔬 **Order legs for both externally-closed trades:**

| trade | ENTRY | SL | TGT | any EXIT order? |
|---|---|---|---|---|
| TATAPOWER | `SELL` `COMPLETE` 10:02:25 | `BUY` **`CANCELLED`** | `BUY` **`CANCELLED`** | 🔴 **NONE** |
| MOSCHIP | `BUY` `COMPLETE` 13:13:41 | `SELL` **`CANCELLED`** | `SELL` **`CANCELLED`** | 🔴 **NONE** |

⇒ 🔬 **The system placed NO square-off order for either position.**

🔬 Both carry `closure_source = EXTERNAL_UNATTRIBUTED`, `exit_mechanism` **empty**,
`exits_verified = 1`, `exits_verify_detail = ok`.

### 🔬 THE 27-Aug TIMELINE, FROM THE LOG

```
15:12:14.697  order_placer   terminal_status_exit_leg_skipped  ×2 (TATAPOWER SL, TGT)
15:12:17.349  reconciler     G5b CRASH_RECOVERY_SL: TATAPOWER SHORT has no active SL order
15:12:32.547  reconciler     (same warning, next cycle)
15:12:47.724  reconciler     check1: exit_price resolved from broker trades: 352.10
15:12:48.349  CRITICAL       CHECK1 MANUAL_CLOSE: TATAPOWER local=OPEN/PARTIAL
                             broker=no_position closure_source=EXTERNAL_UNATTRIBUTED
────────────────────────────────────────────────────────────────────────────────
15:15:01.422  order_monitor  force_close_triggered  force_close_time=15:15  watched_count=2
15:15:01.422  CRITICAL main  circuit_breaker.force_close_triggered: soft_kill,
                             EOD squareoff handles positions
15:15:01.424  CRITICAL       SOFT_KILL ACTIVATED reason=circuit_breaker_force_close_15:15
────────────────────────────────────────────────────────────────────────────────
15:16:35.410  reconciler     Orphan order …815 (SL) cancelled at broker  [MOSCHIP]
15:16:35.448  reconciler     Orphan order …817 (TGT) cancelled at broker [MOSCHIP]
15:16:36.121  CRITICAL       CHECK1 MANUAL_CLOSE: MOSCHIP broker=no_position
                             closure_source=EXTERNAL_UNATTRIBUTED
────────────────────────────────────────────────────────────────────────────────
15:17:02.836  eod_squareoff  EOD square-off triggered for 2026-08-27
15:17:04.869  eod_squareoff  broker-position filter kept 0/0 trades (broker open symbols=0)
15:17:04.887  eod_squareoff  EOD Pass 2 complete: 0 open positions exited.
```

> 🔴 ⭐ **BOTH POSITIONS WERE ALREADY GONE BEFORE THE SYSTEM'S SQUARE-OFF EVER RAN.**
> TATAPOWER by **4m 15s**; MOSCHIP by **27s**. The `0/0` at 15:17:04 is therefore
> **CORRECT BEHAVIOUR ON AN EMPTY BOOK**, ⛔ not a failure to act.

### R-3 · BROKER SIDE — 🏷️ **NOT AVAILABLE**

⛔ Kite's `orders()` / `trades()` return **same-day** records only, so 27-Aug broker
order ids, fill records and any auto-square-off flag are **not retrievable through
the API today**. 🔬 The only broker-side artefact in existence is the ledger line.
⛔ No broker query was run against the live account for this.

🔴 **AND THAT IS ITSELF A FINDING:** `closure_source = EXTERNAL_UNATTRIBUTED` is the
terminal label for **both** *"the broker auto-squared it"* and *"a human closed it in
Kite"*. ⭐ **The system cannot distinguish them**, so causal attribution can never come
from system records alone.

### R-4 · 🔴 **H-1 (CAS) — ✅ CONFIRMED**

🔬 `is_fno` for all five, from `config/instruments.csv`:

| symbol | `is_fno` | ⇒ CAS? | its cutoff | externally closed at | match? |
|---|---|---|---|---|---|
| **TATAPOWER** | **true** | ✅ **YES** | **15:12** | **15:12:47** | ✅ **MATCHES** |
| SHANTIGOLD | false | no | 15:25 | — | — |
| OAL | false | no | 15:25 | — | — |
| BIKAJI | false | no | 15:25 | — | — |
| MOSCHIP | false | no | 15:25 | 15:16:35 | 🔴 **9 min EARLY — no match** |

> ✅ **TATAPOWER is the ONLY CAS stock of the five, and the ONLY one whose external
> closure lands on a published broker cutoff.**
> 🔬 **MOSCHIP was closed 9 minutes BEFORE its own 15:25 cutoff** ⇒ ⛔ it cannot have
> been a cutoff-driven auto-square-off.

🧮 **⇒ THE ARITHMETIC CLOSES:** ₹59 = **one** order · exactly **one** of the two
external closures matches a cutoff · that one is TATAPOWER.

🏷️ **RECONSTRUCTED FROM RECORD** — ⛔ **not broker-confirmed.** The final link (which
order the ledger line names) rests on the four measured facts above, ⛔ not on a
broker record naming TATAPOWER. ⭐ Per R-6 that distinction is preserved, ⛔ not
smoothed over.

🔬 **Recurrence, measured across the whole DB** — `EXTERNAL_UNATTRIBUTED` MIS
closures, all time: **three.**

| date | symbol | exit (IST) | matches a cutoff? |
|---|---|---|---|
| 27-Aug | TATAPOWER | 15:12:47 | ✅ CAS 15:12 |
| 27-Aug | MOSCHIP | 15:16:35 | ⛔ no |
| 21-Aug | HDFCSILVER | 15:15:01 | ⛔ no (⛔ not in `instruments.csv`) |

⇒ ⭐ **Exactly ONE external MIS closure in the system's entire history matches a
published broker cutoff.** ⛔ This is not yet a pattern; it is one clean instance.

### R-5 · 🔴 **H-2 (SHORT) — ⛔ REFUTED**

⭐ Answered from the **code**, because the behavioural evidence is 🏷️ **VACUOUS** —
both positions were already closed when the square-off ran, so 27-Aug cannot show
whether shorts are selected.

🔬 `orders/eod_squareoff.py:1086` — the selection predicate, quoted:

```python
if int(p.qty) != 0 and p.product in EMERGENCY_FLATTEN_PRODUCTS
```

⇒ **`qty != 0`, ⛔ NOT `qty > 0`** ⇒ a negative (short) quantity **IS** selected.

🔬 `orders/eod_squareoff.py:1168-1169` — the exit side, quoted:

```python
# Determine exit side: LONG position -> SELL exit; SHORT -> BUY
exit_side = "SELL" if direction == "LONG" else "BUY"
```

⇒ **a SHORT is closed with a BUY.**

✅ **BEHAVIOURALLY EVIDENCED too:** 🔬 SHANTIGOLD (**SHORT**, MIS, qty 2) was closed by
the system's own `BUY` SL leg at 10:30:59 on the same day. ⭐ The short path works.

> ⛔ **H-2 IS REFUTED. `qty != 0` and the direction-aware exit side are already in the
> shipped code.** ⇒ ⭐ **D-3 needs no work.**

### R-6 · THE CHAIN

```
SYSTEM MIS POSITION ────────► ✅ TATAPOWER SHORT 1, MIS, entry 10:02:25
SYSTEM SQUARE-OFF ATTEMPT ──► 🔴 NONE. Window opens 15:17:02; position gone 15:12:47
BROKER ORDER ───────────────► 🏷️ NOT RETRIEVABLE (same-day API only)
BROKER AUTO-SQUARE-OFF ─────► 🏷️ RECONSTRUCTED (CAS cutoff match), ⛔ not confirmed
₹59 LEDGER CHARGE ──────────► ✅ MEASURED
```

⇒ 🏷️ **"BROKER AUTO-SQUARE-OFF CHARGE OBSERVED; CAUSAL MAPPING TO A SYSTEM MIS
POSITION RECONSTRUCTED FROM RECORD BUT ⛔ NOT BROKER-CONFIRMED."**

**CLASSIFICATION:**

| position | case | why |
|---|---|---|
| **TATAPOWER** | 🔴 **CASE A — never attempted** | ⭐ and for a **structural** reason: the system's window opens **5 min after** the CAS cutoff. ⛔ Not a defect in the close logic. |
| **MOSCHIP** | **CASE A** (never attempted) **+ CASE C** (charge belongs elsewhere) | closed externally 27s before the system's pass and 9 min before its own cutoff ⇒ ⛔ no auto-square-off charge attributable |

### R-7 · THE EXISTING IMPLEMENTATION — TRACED

🔴 **THE TWO CONTROLS ARE DIFFERENT AND MERELY COINCIDE IN TIME. FILE 21 WAS RIGHT TO
FORBID THE ASSUMPTION.**

🔬 `main.py:693-698`, quoted:

```python
"circuit_breaker.force_close_triggered: soft_kill, EOD squareoff handles positions"
kill_switch.soft_kill(reason="circuit_breaker_force_close_15:15",
                      triggered_by="order_monitor")
```

⇒ ⭐ **The 15:15 event sets SOFT_KILL and closes NOTHING.** 🔬 The file even carries
`⛔ Do NOT restore "will close all positions"` at `:704`.

| element | 🔬 measured |
|---|---|
| scheduler (positions) | `eod_squareoff`, config `trading_hours.eod_squareoff_time` |
| **the configured time** | 🔴 **`"15:17"`** (`config/system_config.yaml:49`) |
| its stated design premise | 📄 *"3-min buffer before RMS auto-sq at **15:20** (P1)"* |
| the 15:15 control | `order_monitor` `force_close_time: "15:15"` (`:675`) — SOFT_KILL only |
| entry cutoff | `entry_end: "15:00"` (`:47`) — ⭐ already separate (D-7 satisfied) |
| MIS detection | broker position `product in {MIS, CO}` |
| retry | EOD Pass 1 (cancels) → 2 s → Pass 2 (exits) |
| reconciliation | `check1` vs broker positions/trades |
| failure handling | `CHECK1 MANUAL_CLOSE` CRITICAL + Telegram (⭐ both fired 27-Aug) |

> 🔴 **THE DEFECT, NAMED:** the design premise **"RMS auto-sq at 15:20"** matches
> **NONE** of the four published cutoffs. Against the real ones:
> * vs **CAS 15:12** → **15:17 is 5 MINUTES LATE.** ⛔ Structurally unbeatable.
> * vs non-CAS 15:25 → 8 min early ✅ · vs F&O 15:26 → 9 min early ✅

⚠️ **THIS CORRECTS FILE 21's OWN §1.** FILE 21 reasoned from `15:15` and concluded
*"3 minutes late"* vs CAS. 🔬 **The position-closing pass is `15:17`, not `15:15`** —
15:15 closes nothing — so the true gap is **5 minutes**, and 👤 Rama's *"our
square-off runs AFTER Zerodha's"* is **CONFIRMED for CAS** (⛔ refuted for non-CAS,
where 15:17 is comfortably early).

⚠️ 🔬 A **second** 15:20 belief lives at `orders/eod_squareoff.py:1162-1164`:
*"CO positions … Zerodha rejects and auto-squares at 15:20 with a ₹50+GST penalty."*
🏷️ **RECORDED, ⛔ NOT RESOLVED** — the fetched page lists segments, not products, so
whether CO has its own 15:20 cutoff is **CANNOT DETERMINE** from today's source.
⭐ Two independent places encode `15:20`; ⛔ neither is traceable to the current page.

### R-8 · THE PRODUCT-SOURCE QUESTION — ✅ **ALREADY CORRECT**

🔬 The selector reads the **BROKER position's** product:

```python
broker_qty = {p.symbol: abs(int(p.qty)) for p in broker_positions
              if int(p.qty) != 0 and p.product in EMERGENCY_FLATTEN_PRODUCTS}
```

🔬 `core/constants.py:42` — `EMERGENCY_FLATTEN_PRODUCTS = frozenset({"MIS", "CO"})`.

| requirement | status |
|---|---|
| uses the AUTHORITATIVE product field | ✅ broker-side `p.product` |
| ⛔ never infers MIS from strategy intent | ✅ intent is not read here |
| ⛔ never uses GTT presence as a product proxy | ✅ no GTT reference in the path |
| ⛔ does not read `trades.product` (HAZ-4) | ✅ that column does not exist and is not read |
| CNC/NRML never touched | ✅ `:23`/`:34`/`:1073` EOD6, enforced by the frozenset |

⇒ ⭐ **D-2's product boundary is already implemented and already correct.**

---

## §3 — THE DESIGN · ⭐ NARROWED BY WHAT §2 ACTUALLY PROVED · ⛔ NOTHING CODED

⭐ §2 proves **one** gap. ⭐ Most of FILE 21 §3 is therefore **already satisfied** and
must **not** be rebuilt — building a second selector would be the larger risk.

| item | status after §2 |
|---|---|
| **D-1** per-segment cutoff | 🔴 **THE ONLY REAL WORK** |
| **D-2** MIS-only enforcement | ✅ **ALREADY CORRECT** (R-8) — ⭐ add only the scan telemetry |
| **D-3** handle shorts | ✅ **ALREADY CORRECT** (R-5) — ⛔ nothing to build |
| **D-7** entry cutoff separate | ✅ already `entry_end: 15:00` vs `eod_squareoff_time: 15:17` |
| **D-8** separate from GTT_EXIT | ✅ already separate modules |
| D-4/5/6, D-9, D-10 | ⭐ genuine hardening, ⛔ not blocking |

### 🔴 D-1 — THE PROPOSAL

```yaml
trading_hours:
  mis_squareoff_cutoff:          # broker-adjustable — ⛔ NEVER a code constant
    cas:      "15:12"            # F&O-listed equities (continuous trade ends 15:15)
    non_cas:  "15:25"
    fno:      "15:26"
    mcx:      "close_minus_10m"
  mis_squareoff_first_offset:  "5m"
  mis_squareoff_second_offset: "2m"
```

⇒ `CHECK_1 = cutoff − 5m` · `CHECK_2 = cutoff − 2m`, **DERIVED per segment**:

| segment | CHECK_1 | CHECK_2 | vs today's single 15:17 |
|---|---|---|---|
| **CAS** | **15:07** | **15:10** | 🔴 **both EARLIER than 15:17** — this is the fix |
| non-CAS | 15:20 | 15:23 | later than 15:17, still safe |
| F&O | 15:21 | 15:24 | — |

⭐ **Segment resolution needs no new data source:** `instruments.csv.is_fno`
⇒ `cas` when true, `non_cas` when false. ⚠️ A symbol **absent** from `instruments.csv`
(e.g. HDFCSILVER) must **fail closed to the EARLIEST cutoff**, ⛔ never default to the
latest.

⭐ **Fail-closed on a missing/invalid cutoff (F1's pattern).** ⚠️ Record in config that
these are broker-adjustable and that `is_fno` is a **proxy** for CAS membership, ⛔ not
the NSE register.

🔴 ⭐ **A SINGLE GLOBAL OFFSET CANNOT FIX THIS** — 👤 Rama's 5-min/2-min design assumes
one cutoff; there are four, and one already sits **before** today's pass.

⚠️ **⛔ NOT PROPOSED: moving the single `eod_squareoff_time` earlier to 15:07.** That
would pull the **non-CAS** square-off 18 minutes earlier than needed and surrender
trading time on every non-F&O position — ⭐ the per-segment split exists precisely to
avoid that.

---

## §4 — TODAY

| | |
|---|---|
| **T-1** | 🔬 **CNC book: OAL + RAMRAT open**, `D = ₹1,025.69` (2/3). TEJASNET exited `GTT_EXIT` 10:30:21.803, SL leg ₹558.00. `max_open_delivery_positions: 3` ENFORCED and `margin_reserved` fixed at entry ⇒ ⭐ **D can only fall.** |
| **T-2** | 🔴 **The 15:00 HOLD/CLOSE call is 👤 RAMA'S and remains open.** ⭐ The four-element notice went out in chat at ~10:10 and ~10:20. ⛔ Not re-asked. ⛔ Not decided. |
| **T-3** | ⚠️ **The ₹59 changes NOTHING about OAL/RAMRAT** — they are CNC/DELIVERY, and `EMERGENCY_FLATTEN_PRODUCTS = {MIS, CO}` puts them **outside MIS auto-square-off scope entirely**. ⛔ Not to be closed because of this finding. |
| **T-4** | ⭐ The 14:45 watch is running; last sample 10:48:43 unchanged. |
| **T-5** | ⚠️ The `orders.qty_filled=0` on a `COMPLETE` order stays an **observation**. ⛔ Not chased. 🔬 Note it recurs on **every** 27-Aug order row too, so it is systemic to that column, ⛔ not specific to today. |

---

## §5 — WHAT WAS NOT MEASURED, PLAINLY

1. ⛔ **No broker-side 27-Aug record.** Same-day API only; the ledger line is the sole
   broker artefact. The ₹59→TATAPOWER mapping is 🏷️ **RECONSTRUCTED**, ⛔ not confirmed.
2. ⛔ **What actually closed MOSCHIP at 15:16:35** — 🏷️ **CANNOT DETERMINE.**
   `EXTERNAL_UNATTRIBUTED` cannot separate a broker action from a human one.
3. ⛔ **The NSE/Zerodha CAS constituent list** was not obtained. `is_fno` is a proxy,
   📄 supported by Zerodha's own "non-F&O stocks" wording.
4. ⛔ **Whether CO has its own 15:20 cutoff** — 🏷️ **CANNOT DETERMINE** from the fetched
   page; two places in the tree encode `15:20` and neither is traceable to it.
5. ⛔ **The proposed D-1 change is NOT built, NOT tested, NOT pushed.**
6. ⛔ **No auto-square-off code was modified**, per FILE 21's standing prohibition.
7. 🏷️ **VACUOUS on 27-Aug:** whether the square-off selects shorts — the book was
   empty when it ran. ⭐ Answered from code and from SHANTIGOLD instead.

---

⛔ push ≠ boot · ⛔ boot ≠ the changed line executed · ⛔ loaded ≠ executed ·
⛔ executed ≠ exercised · ⛔ executed ≠ load-bearing · ⛔ exists ≠ correct ·
⛔ green ≠ red-capable · ⛔ system record ≠ broker confirmation ·
⛔ **a ledger charge ≠ a proven system failure** ·
⭐ **measure or search the authoritative source before judging.**

## END OF FILE 21 RECORD
