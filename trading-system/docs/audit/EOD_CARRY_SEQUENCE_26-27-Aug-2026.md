# EOD LIFECYCLE + OVERNIGHT CARRY SEQUENCE — 26-Aug → 27-Aug-2026

**One audit file, appended per phase.** ⛔ Read-only observation throughout: zero code, config, schema changes; zero DB writes (all reads `file:…?mode=ro`). ⛔ Nothing deployed — the 17:35 observation is only valid on `75e637c` unchanged.

**Anti-duplication check:** searched `docs/audit/` (**299 files**) for `EOD|CARRY|26-27|SEQUENCE`. Found related-but-distinct records — `CARRY_DAY_25-Aug-2026.md`, `EOD_LIFECYCLE_UNIT_25-Aug-2026.md`, `PREDICTION_eodlifecycle_25-Aug-2026.md`, `paper_overnight_carry_26jul2026.md` — none of which is this sequence. `EOD_CARRY_SEQUENCE_26-27-Aug-2026.md` did not exist. New file warranted.

---

## §0 — SESSION START

| | measured | verdict |
|---|---|---|
| **S1** | Ledger `:28` now reads `🟢🧪🔝 26-Aug 08:15 IST — 75e637c BOOT PROVEN ON ITS FIRST EVER RUN. 🏷️ PUSHED · DEPLOYED · BOOT PROVEN`, superseding `:50`'s `⛔ BOOT NOT PROVEN` (retained) | ✅ **BOOT PROVEN confirmed** |
| **S2** | `origin/main` = `75e637c300c1bead4aad3cf549e6dbe9318c6b1f`; VM bare HEAD = same; tracked drift **0**; `main.py` md5 `ea62b0b876489f2897c288548acb2977` | ✅ **unchanged — tonight's test is valid** |
| **S3** | PID **402677**, `NRestarts=0`, started `Wed 2026-08-26 08:15:17`, uptime `03:08:08` at 11:23 | ✅ **SAME process observed this morning — no restart** |

⚠️ **Ledger read declared as STRUCTURAL, not line-by-line** (1,407,080 B / 4,010+ lines), per the 26-Aug precedent.

---

## §PHASE 0 — THE REVERT TRIGGER'S TARGET · **RESOLVED BY MEASUREMENT**

🔴 **The collision is worse than the brief states: there are TWO distinct `CHECK 1`/`CHECK 2` pairs in this codebase**, and the trigger's wording matches one while its cited evidence comes from the other.

### The two pairs

| pair | CHECK 1 | CHECK 2 | produces a "residual"? |
|---|---|---|---|
| **Reconciler position checks** | `_check1_manual_close` — `orders/order_reconciler.py:1188` — *local OPEN/PARTIAL \ broker positions* | `_check2_orphan_adoption` — `:1790` — *broker positions \ locally tracked* | ⛔ **NO** — set differences, no residual |
| **G3 capital-drift checks** | `expected_broker_net` vs `margins.net` — `:3693-3695` | `system_held_capital` vs `margins.used` — `:3701-3702` | ✅ **YES — CHECK 2 only** |

`_g3_capital_drift`'s own docstring, `orders/order_reconciler.py:3573-3576`, verbatim:

```
G3 Level 3 (RC8). TWO checks, deliberately NOT merged:

  CHECK 1 (drift)  expected_broker_net  vs  margins.net
  CHECK 2 (margin) system_held_capital  vs  margins.used
```

### **P0a — the code that produces a value called `residual`**

```python
3691|        # CHECK 1: what broker cash SHOULD read, given real capital, what we are
3692|        # holding, and the realised PnL the broker has not credited yet.
3693|        expected = real_capital - held - snapshot.daily_realized_pnl
3694|        actual = margins.net
3695|        delta = abs(actual - expected)          # <-- CHECK 1's quantity is `delta`
3696|
3697|        # CHECK 2: margin reconciliation, kept SEPARATE so its residual stays
3698|        # visible and is never absorbed into CHECK 1. Carry is excluded: a
3699|        # carried position's margin left the broker's `used` when it settled,
3700|        # but it is still in `held`.
3701|        held_today = held - (snapshot.intraday_carry + snapshot.positional_carry)
3702|        margin_residual = held_today - margins.used      # <-- the ONLY `residual`
```
and the log line that surfaces it, `:3709-3714`:
```python
3709|        self._log.debug(
3710|            "G3 MARGIN_RECON: held=%.2f carry=%.2f held_today=%.2f "
3711|            "broker_used=%.2f residual=%.2f",
3712|            held,
3713|            snapshot.intraday_carry + snapshot.positional_carry,
3714|            held_today, margins.used, margin_residual,
3715|        )
```

⇒ **CHECK 1's quantity is `delta`. The only thing named `residual` anywhere in G3 is CHECK 2's `margin_residual`.**

### 🔬 THE DECISIVE FINGERPRINT — the trigger's own cited numbers

The trigger's justification (ledger `:117`) cites *"`residual = 441.12` on **55 samples** and `residual = 610.37` on **46 samples**, both at `carry = 0.00`"*. Measured against the 24-Aug reconciler log:

```
     55 held=1051.57 carry=0.00 held_today=1051.57 broker_used=610.45 residual=441.12
     46 held=699.56  carry=0.00 held_today=699.56  broker_used=89.18  residual=610.37
```

**Sample counts match exactly — 55 and 46.** Both lines are `G3 MARGIN_RECON`, whose `residual=` field is `margin_residual` = **CHECK 2**. And the arithmetic confirms it: `1051.57 − 610.45 = 441.12` ✓, `699.56 − 89.18 = 610.38 ≈ 610.37` ✓. (Those values are also, exactly, the positions of the day: KAMATHOTEL `2 × 220.56 = 441.12`; BALUFORGE `1 @ 610.45`.)

### **P0b — THE TRIGGER IN ITS CORRECTED FORM**

> **Quantity:** `margin_residual = held_today − margins.used`, where `held_today = held − (intraday_carry + positional_carry)`
> **Source:** G3 **CHECK 2** (margin reconciliation) — `orders/order_reconciler.py:3702`, surfaced as the `residual=` field of the `G3 MARGIN_RECON` DEBUG line at `:3709-3714`
> ⛔ **NOT** `_check1_manual_close` (`:1188`) · ⛔ **NOT** G3 CHECK 1's `delta` (`:3695`)
> **Compared against:** the carried CNC position's value
> **Threshold:** "roughly equal"
> **Precondition (added 25-Aug, ledger `:116`):** **`carry > 0` is MANDATORY.** At `carry = 0`, a residual merely resembling a position value is ⛔ **NOT** a carry failure.

**P0c** — ⛔ meaning, threshold and direction are UNCHANGED. Only the target check was resolved.

**P0d** — Resolved **WITH confidence** (the 55/46 sample-count fingerprint is decisive). ⭐ **But belt-and-braces: PHASE 6 will capture BOTH G3 CHECK 1's `delta` AND CHECK 2's `margin_residual` as raw numbers**, so Rama can rule differently if he reads the label as authoritative over the evidence.

### 🔴 P0-CONFLICT — TWO RECORDS DISAGREE, AND I AM NOT RESOLVING IT

* **The trigger says:** `carry > 0` AND `residual ≈ carried CNC value` ⇒ **REVERT**.
* **The code comment at `:3703-3708` says** the opposite about the same signature: *"broker `used` for a SETTLED CNC holding is unmeasured (it plausibly drops out of utilised.debits while `held` retains it), so alerting here would **fire falsely on the first carry day**. Owed: measure a T+1 carry, then decide a threshold."*

⇒ **On the first carry day, `residual ≈ position value` is simultaneously the trigger's REVERT signature AND the code's own predicted FALSE POSITIVE.** ⛔ I am not resolving this — it is a genuine conflict between two standing records, and 👤 **it is Rama's to rule.** PHASE 6 supplies the numbers; it does not adjudicate.

---

## §FROZEN PREDICTIONS — written 26-Aug ~11:40 IST, BEFORE the events

| # | prediction |
|---|---|
| **P1** | ~15:15 intraday circuit-breaker force-close runs; MIS positions close; SOFT_KILL set with reason `circuit_breaker_force_close_15:15` |
| **P2** | At 17:35, IF only CNC/DELIVERY remain, `_position_requires_service` returns False for each, `active == 0`, service SELF-EXITS with no manual stop |
| **P3** | IF any INTRADAY survives past 17:35, or identity is CONFLICT/UNRESOLVED, or a HARD_KILL flatten runs, or the pipeline-aware read raises ⇒ `active > 0`, service STAYS UP, manual stop required before 08:15 |
| **P4** | If it self-exits, the CNC leg carries overnight with capital still reserved and the broker GTT resting unattended |
| **P5** | At 08:15 on 27-Aug, `get_holdings` returns the carried symbol(s) and `sync_from_broker` reports `carry > 0` — the first non-zero carry ever observed |
| **P6** | 🔴 Overnight drift band is **₹50 FLAT**; a carried CNC is worth far more ⇒ a capital-drift alert is **EXPECTED** on 27-Aug morning, and it is the false positive the G3 comment predicted. ⛔ An alert is NOT automatically the revert condition |
| **P7** | The F6-leg `abs(int(qty))` defect only bites on a T+1 GTT SELL producing a same-day −1 row. If no GTT fires on 27-Aug, it is NOT exercised and must NOT be claimed tested either way |
| **P8** | The 45s morning-check wait faces its first real cold boot at 08:15 on 27-Aug. Expected: no false RED |

### ⭐ MY OWN ADDITIONAL PREDICTIONS, frozen at the same moment

| # | prediction | basis |
|---|---|---|
| **P9** | 🔴 **`cnc_gtt_monitor` will take the ORPHAN branch on FMGOETZE and CLOSE it before 17:35** — `_gather` (`:454-466`) builds `held` from `get_holdings` + `get_positions`, both of which now return **0** for FMGOETZE; with the GTT reading `active` and `held == 0`, `_handle_row` branch 4 (`:503-510`) forensic-logs, `_safe_delete_gtt`s the real protective GTT, and `_finalize_gtt_exit`s the trade as `GTT_EXIT`. 💭 **INFERENCE from code + measured endpoint state — NOT yet observed.** If it holds, **tonight becomes a FLAT EOD and the carry test is lost** |
| **P10** | If P9 does NOT hold, FMGOETZE survives to 17:35 and `active == 0` ⇒ P2 fires |
| **P11** | Tomorrow's `carry` will be non-zero **only if** FMGOETZE is still open at shutdown. If P9 fires, `carry = 0` again and OWED-2 stays unproven |

---

## §PHASE 1 — PRE-CLOSE SNAPSHOT A (26-Aug ~11:25 IST)

### 1a · Every open trade

```sql
SELECT t.trade_id, t.symbol, t.strategy, t.direction, t.qty_filled, o.product,
       t.entry_time, t.entry_actual_price, t.status
FROM trades t LEFT JOIN orders o ON o.trade_id=t.trade_id AND o.leg='ENTRY'
WHERE t.status='OPEN' ORDER BY t.entry_time;
```

| trade_id | symbol | strategy | dir | qty | product | entry | price |
|---|---|---|---|---|---|---|---|
| `trd_e45cfd56…56c` | **FMGOETZE** | positional_sector_rotation | LONG | 1 | **CNC** | `2026-08-26T10:07:48.161368+05:30` | **573.05** |

**Today's full book, for context:** HINDCOPPER (MIS) CLOSED `SL_HIT` 10:47:08 −8.92 · CYIENT (MIS) CLOSED `SL_HIT` 10:59:03 −14.19 · THEMISMED (CNC) CLOSED **`GTT_EXIT` 10:30:34 @ 131.24 +12.94** · FMGOETZE (CNC) **OPEN**.

⭐ **THEMISMED's same-day GTT_EXIT is itself a finding:** its GTT fired ~22 min after entry and finalised cleanly. ⛔ No orphan/forensic/reprotect line was logged for it, so it took branch 1 (`triggered`, `:488-490`), a genuine broker GTT fire — ⛔ not an orphan finalisation.

### 1b · Broker state (raw, timestamped)

```
{"ts":"2026-08-26T11:25:21.212+05:30", …"get_positions call_end", "result_summary":"0 positions"}
{"ts":"2026-08-26T11:16:00.370+05:30", …"get_holdings call_end",  "result_summary":"0 holdings"}
```

### 1c · The resting GTT

| gtt_id | trade | symbol | qty | status | sl_trigger | tgt_trigger |
|---|---|---|---|---|---|---|
| **333377486** | `trd_e45cfd56…` | **FMGOETZE** | 1 | **ACTIVE** | 561.6 | 590.25 |
| 333377731 | `trd_85126218…` | THEMISMED | 4 | CLEANED | 125.12 | 131.49 |

```
{"ts":"2026-08-26T10:07:48.194+05:30","level":"INFO","logger":"cnc_gtt","msg":"cnc_gtt.placed","trade_id":"trd_e45cfd56cebc4527bb9b03ebea48856c","symbol":"FMGOETZE","exit_side":"SELL","gtt_id":"333377486","last_price":573.05,"modified":false,"qty":1,"sl_limit":544.75,"sl_trigger":561.6,"tgt_limit":587.25,"tgt_trigger":590.25}
```

### 1d · Capital

```
{"ts":"2026-08-26T09:15:00.041+05:30",…"fund_manager.sync_from_broker","broker_cash":10567.6,"carry":0.0,"new_total":10567.6,"old_total":10567.6}
{"ts":"2026-08-26T11:25:21.308+05:30",…"G3 MARGIN_RECON: held=573.05 carry=0.00 held_today=573.05 broker_used=18.47 residual=554.58"}
```

### 1e · Kill switch / service
`kill_switch_state` = **INACTIVE** (`auto_clear_stale`, `2026-08-26T08:15:18.791189+05:30`). PID **402677**, `NRestarts=0`, `active`.

### 1f · The M5(d) resolution chain, BY HAND — the prediction the 17:35 gate is judged against

| step | FMGOETZE |
|---|---|
| `trade.strategy` | `positional_sector_rotation` |
| → YAML `intent` | **DELIVERY** (`config/strategies/positional_sector_rotation.yaml`) |
| → entry product (`orders`, leg=ENTRY) | **CNC** |
| → `PRODUCT_TO_INTENT['CNC']` (`core/constants.py:8`) | **DELIVERY** |
| → both sources agree ⇒ `_resolve_position_pipeline` (`main.py:1139-1140`) | **DELIVERY** |
| → `_position_requires_service` (`main.py:1173-1176`): `pipeline == DELIVERY` and `'CNC' ∈ _BROKER_PROTECTED_PRODUCTS` | **False — NOT counted** |

⇒ **PREDICTED `active` at 17:35 = 0 ⇒ `due = True` ⇒ SELF-EXIT.**

### 1g · 🔴 THE DIFFERENCE THAT IS THE WHOLE POINT

| count | value |
|---|---|
| `count_active_positions()` — product-blind (`state_store.py:639-656`) | **1** |
| pipeline-aware `active` (CNC excluded) | **0** |

⇒ ⭐ **The two counts DIFFER right now. Under the pre-`75e637c` product-blind gate the service would STAY UP tonight; under the deployed pipeline-aware gate it will SELF-EXIT. That divergence is precisely what `75e637c` changed, and tonight measures it.**

### 🔴 PHASE 1 FINDING — FMGOETZE IS INVISIBLE TO BOTH BROKER ENDPOINTS

Measured: `get_positions` = **0**, `get_holdings` = **0**, while the DB says OPEN qty 1, `held = 573.05`, and the GTT mirror says ACTIVE.

**This is not an adapter filter.** `zerodha_adapter.py:1229-1240` reads Kite's `net` list and includes **every** row with `quantity != 0`, capturing `product` at `:1235` but ⛔ **never filtering on it**. So `"0 positions"` means Kite's `net` genuinely has no non-zero row for FMGOETZE.

**The broker released its margin intraday.** The `G3 MARGIN_RECON` series shows the transition precisely:

```
     87 held=573.05 carry=0.00 held_today=573.05 broker_used=580.22 residual=-7.17     <- healthy
     22 held=573.05 carry=0.00 held_today=573.05 broker_used=18.47   residual=554.58   <- from 11:21:03
```

⇒ At **11:21:03** `broker_used` collapsed `580.22 → 18.47` while our `held` stayed `573.05`, producing `residual = 554.58` against a position worth `573.05` (**96.8%**).

⚠️ **THIS IS ALREADY THE TRIGGER'S SIGNATURE — and the trigger is NOT MET, because `carry = 0.00`.** Per the 25-Aug rewording (ledger `:116`), at `carry = 0` a residual resembling a position value is explicitly ⛔ **not** a carry failure. Recorded here so that tomorrow's number is read against a known baseline rather than as a novelty.

⭐ **And it is the G3 comment's own mechanism arriving a day early** — *"broker `used` for a SETTLED CNC holding is unmeasured … it plausibly drops out of utilised.debits while `held` retains it"* — observed here **intraday on T, not at T+1**.

### ⚠️ A SECOND, SMALLER FINDING — the ENTRY order row disagrees with its trade row

```
order 260826170282507  leg=ENTRY  BUY  CNC  qty_requested=1  qty_filled=0  avg_fill_price=(null)  status=COMPLETE  filled_at=2026-08-26T10:07:48.160237+05:30
```
The order row says `qty_filled = 0` and carries no `avg_fill_price`, while `status = COMPLETE`, `filled_at` is set, and the **trade** row records `qty_filled = 1 @ 573.05`. 📌 **Recorded, not investigated** — an orders-table population gap, out of tonight's scope.

### PHASE 1 — what was NOT measured
* Snapshot B (~15:10) is not yet due.
* ⛔ I did not call the broker directly — all broker state is read from the service's own logged calls, since an independent call would add API load and is not needed.
* P9 is **INFERENCE from code plus measured endpoint state** — the monitor has ⛔ not been observed acting on FMGOETZE. Only observation settles it.


---

# FILE 4B — REVISED SEQUENCE (supersedes FILE 4A). Appended 26-Aug ~12:47 IST.

⚠️ **FILE 4's PHASE 0 and PHASE 1 remain in force.** PHASE 1's snapshot was accurate **at 11:25** and is now superseded as *current state* by SECTION A below — the book moved four times between 11:25 and 12:39. ⛔ PHASE 1 is retained, not deleted.

## §A — WHAT "HOLDING" MEANS ON THAT ROW

### 🔴 A2 — THE APPARENT CONTRADICTION RESOLVES: MY EARLIER READING WAS **STALE, NOT WRONG**

The brief's screenshot shows 20MICRONS open; my 11:25 measurement showed one open trade (FMGOETZE) and `0 positions`. Measured cause:

**20MICRONS was entered at `2026-08-26T12:05:26.833978+05:30` — 40 minutes AFTER my baseline.** `trd_5cd243e2b2a3410e9abd31fc3e0e6e98`, `positional_swing_long`, CNC, qty 2 @ **227.24**. DCBBANK likewise entered 11:40:26 and closed 11:42:06. ⇒ ⛔ no contradiction; the book simply moved.

**A2 VERDICT: `POSITIONS ONLY`.** At 12:39 `get_positions` = **1**, `get_holdings` = **0** ⇒ a same-day CNC buy not yet settled. ✅ **This does NOT contradict the 26-Aug boot measurement of 0 holdings** — holdings are still 0. ⛔ No STOP condition.

### A1 · Broker endpoints (from the service's own logged calls, timestamped)
```
{"ts":"2026-08-26T12:31:47.103+05:30", …"get_holdings call_end",  "result_summary":"0 holdings"}
{"ts":"2026-08-26T12:39:24.360+05:30", …"get_positions call_end", "result_summary":"1 positions"}
```
⛔ I did not call the broker directly — an independent call adds API load and the service already polls both endpoints continuously.

### A3 · What `_gather` computes for `held` on 20MICRONS — **2**, proven behaviourally
`gtt_state` for GTT `333417200` carries `last_verified_at = 2026-08-26T12:31:47.117466+05:30`. `touch_gtt_state_verified` is reached **only** from `_handle_row` branch 2 (`:494-496`), whose condition is `present_active and held == row_qty`. `row_qty = 2` ⇒ **`held == 2`**. ⭐ Measured from the monitor's own verdict, ⛔ not by instrumenting code and ⛔ not by running the monitor.

### A4 · The entry — ⚠️ **`orders.price` IS NULL AGAIN, AND THE FINDING IS BROADER THAN M6(b) RECORDED**
```
order 260826170592084  ENTRY BUY CNC LIMIT  qty_requested=2  qty_filled=0  price=(null)  avg_fill_price=(null)
                       status=COMPLETE  placed=12:05:25.807321  filled=12:05:26.832886   -> 1.03 s to fill
```
The limit price **does** exist in the log — `{"msg":"limit_triple.entry_placed","symbol":"20MICRONS","broker_order_id":"260826170592084","price":227.57394}` — but is ⛔ **not persisted to `orders.price`**.

🔴 **CORRECTION/EXTENSION TO M6(b):** M6(b) examined only the eight 21-Aug **CNC** orders and reported `orders.price` NULL on all of them. Measured today across **all six** entries — MIS **and** CNC alike — `price` and `avg_fill_price` are **NULL on every one**. ⇒ ⭐ **this is not a CNC-path defect; the limit price is not persisted for ANY order.**

⚠️ Also: an earlier 20MICRONS attempt `trd_0b15222cefd8451fbb14754500a72be1` (11:59:22, entry 226.92285) is `FAILED`. The OPEN trade is the second attempt.

### A5 · The resting GTT — **verified at the broker, not assumed**
```
gtt_id 333417200 · 20MICRONS · qty 2 · ACTIVE · sl_trigger 223.02 · tgt_trigger 233.57
                 · created 12:05:27.453735 · last_verified_at 12:31:47.117466
{"ts":"2026-08-26T12:05:27.455+05:30",…"cnc_gtt.placed","symbol":"20MICRONS","exit_side":"SELL","gtt_id":"333417200","last_price":227.11,"qty":2,"sl_limit":216.32,"sl_trigger":223.02,"tgt_limit":232.4,"tgt_trigger":233.57}
```
⭐ **Broker existence is confirmed by `last_verified_at`**, which only advances when `_gather` found this `gtt_id` in the broker's live `get_gtts()` and matched its qty — ⛔ not from the placement log alone.

### A6 · The M5(d) chain, by hand — **the prediction the 17:35 gate is judged against**
`positional_swing_long` → YAML `intent: DELIVERY` → entry product `CNC` → `PRODUCT_TO_INTENT['CNC'] = DELIVERY` (`core/constants.py:8`) → **both sources AGREE** → pipeline `DELIVERY` → `_position_requires_service(DELIVERY,'CNC')`, `'CNC' ∈ _BROKER_PROTECTED_PRODUCTS` (`main.py:1158`) ⇒ **False, NOT counted**.
⇒ **PREDICTED `active` at 17:35 = 0 ⇒ `due = True` ⇒ SELF-EXIT.**

### A7 · 🔴 BOTH COUNTS — THE DIVERGENCE HOLDS
| count | value |
|---|---|
| product-blind `count_active_positions()` | **1** |
| pipeline-aware `active` | **0** |

⇒ ⭐ **The pre-`75e637c` gate would keep the service up tonight; the deployed gate self-exits. Tonight is still the discriminating case.**

---

## §B — THE CLOSED ROUND TRIPS (perishable evidence, captured today)

### B1 · Entry detail, all six of today's trades

| symbol | product | type | qty | `orders.price` | fill | placed → filled |
|---|---|---|---|---|---|---|
| HINDCOPPER | MIS | LIMIT | 1 | **NULL** | 547.95 | 1.72 s |
| CYIENT | MIS | LIMIT | 1 | **NULL** | 1034.20 | 7.38 s |
| FMGOETZE | CNC | LIMIT | 1 | **NULL** | 573.05 | **30.94 s** |
| THEMISMED | CNC | LIMIT | 4 | **NULL** | 127.67 | 2.06 s |
| DCBBANK | MIS | LIMIT | 2 | **NULL** | 216.50 | 0.52 s |
| 20MICRONS | CNC | LIMIT | 2 | **NULL** | 227.24 | 1.03 s |

### B2 · F4 CONTRAST — ⚠️ the deficit PERSISTS today; ⛔ no root cause declared
Today's ENTRY orders by product: **CNC 3 COMPLETE / 6 CANCELLED (33% fill)** · **MIS 3 COMPLETE / 2 CANCELLED (60%)**.
⇒ ✅ **Consistent with M6's full-history figures (CNC 30.1% / MIS 52.4%).** Today's three CNC fills are therefore ⛔ **not** evidence that the problem has gone away — six CNC entries still failed today.
💭 **INFERENCE, labelled:** the three that filled are mid-cap names during liquid hours; the limit price at placement remains **unmeasured** (A4), so the strongest hypothesis stays untestable. ⛔ No F4 root cause is declared from three fills.

### B3/B4 · 🔴 F5 EXIT ATTRIBUTION — **a clean result, with one real gap**

| symbol | product | `exit_reason` | `closure_source` | `exit_price` | net |
|---|---|---|---|---|---|
| THEMISMED | CNC | `GTT_EXIT` | *(empty)* | 131.24 | +12.94 |
| HINDCOPPER | MIS | `SL_HIT` | **`OWN_SL`** | 539.60 | −8.92 |
| CYIENT | MIS | `SL_HIT` | **`OWN_SL`** | 1021.10 | −14.19 |
| FMGOETZE | CNC | `GTT_EXIT` | *(empty)* | 561.75 | −12.76 |
| DCBBANK | MIS | `TGT_HIT` | **`OWN_TGT`** | 218.80 | +4.14 |

✅ **All five exits are correctly attributed. ZERO `MANUAL` mislabels.** F5's known defect — a system-caused exit mislabelled MANUAL — did ⛔ **NOT** occur today. That is a clean control result on the MIS side.

🔴 **BUT THE GAP IS REAL, ON THE CNC SIDE:** both GTT exits record the **MECHANISM** (`GTT_EXIT`) and leave `closure_source` and `exit_mechanism` **EMPTY** — the system does not record **which leg fired**. The information exists and is unambiguous:
* **FMGOETZE** exit `561.75` against `sl_trigger 561.6` / `tgt_trigger 590.25` ⇒ **the SL leg fired**
* **THEMISMED** exit `131.24` against `sl_trigger 125.12` / `tgt_trigger 131.49` ⇒ **the TGT leg fired**

⇒ ⭐ **an F5-shaped gap: a known-cause exit whose cause is derivable but not recorded.** ⛔ Not fixed.

### B5 · 🔴 DEFECT B — THE EXIT PRICE. **Located exactly; did NOT fire today.**
`_finalize_gtt_exit` (`:528`) takes its price from `_resolve_exit_price` (`:548`), a **three-tier silent fallback** at `orders/cnc_gtt_monitor.py:676-696`:

```python
680|            for t in reversed(self._adapter.get_trades() or []):
681|                if (t.get("tradingsymbol") == symbol
682|                        and t.get("transaction_type") == exit_side
683|                        and float(t.get("quantity", 0)) > 0
684|                        and float(t.get("average_price", 0)) > 0):
685|                    return float(t["average_price"])      # TIER 1 — REAL broker fill
686|        except Exception:  # noqa: BLE001
687|            pass
...
692|            if ltp and float(ltp) > 0:
693|                return float(ltp)                          # TIER 2 — LTP, DERIVED
694|        except Exception:  # noqa: BLE001
695|            pass
696|        return float(entry_price or 0.0)                   # TIER 3 — FABRICATED
```

🔴 **Tier 3 (`:696`) is DEFECT B**: the exit price becomes the **entry** price, forcing `pnl ≈ 0` and producing the `exit_price == entry_price` signature. ⚠️ **Both fallbacks are SILENT** (`except: pass`, `:686-687` and `:694-695`) and the stored row records **no tier indicator** ⇒ **a fabricated exit price is indistinguishable from a real one in the DB.**

✅ **It did NOT fire today.** Both CNC exits differ from their entries (561.75 vs 573.05; 131.24 vs 127.67) and both sit at their respective trigger levels ⇒ **TIER 1, real broker fills.**

### B6 · The clean `held == 0` arm — **branch 1, proven by absence AND by price**
🔬 **Falsifiers that could have fired and did not:** `orphan_active_gtt_flat` = **0** · `forensic` = **0** · `delete_gtt` = **0** · `_reprotect` = **0** · `"F6: GTT triggered"` = **0**, across the whole of today's system log.
⇒ Both CNC exits took **branch 1** (`triggered` **and** `held == 0` → `_finalize_gtt_exit` at `:490`) — a genuine broker GTT fire, ⛔ **not** an orphan finalisation (branch 4, `:503-510`) and ⛔ not a reprotect (`:491`).

⚠️ **STATED EXPLICITLY, as required: this proves NOTHING about the T+1 arm.** The F6-leg `abs(int(qty))` defect needs a **same-day −1 SELL row against a settled holding**. Today's exits were same-day round trips where `held` reached 0 cleanly. ⭐ **The T+1 arm remains UNEXERCISED.**

### B7 · Capital release — ✅ **correct**, and it corrects my own PHASE 1 inference
```
11:26:52  held=573.05  carry=0.00  held_today=573.05  broker_used=18.47   residual=554.58
11:36:59  held=-0.00   carry=0.00  held_today=-0.00   broker_used=18.47   residual=-18.47
11:47:03  held=-0.00   carry=0.00  held_today=-0.00   broker_used=13.87   residual=-13.87
12:07:13  held=454.48  carry=0.00  held_today=454.48  broker_used=468.35  residual=-13.87
```
✅ FMGOETZE's reservation **was released** — `held` 573.05 → −0.00 after the 11:31:10 exit. 20MICRONS then re-holds `454.48 = 2 × 227.24` exactly, with `broker_used` tracking it (`residual −13.87`).
⚠️ Cosmetic: `held=-0.00` — a negative-zero float artefact. 📌 Recorded, not chased.

### 🔴 B7-COROLLARY — **I MUST CORRECT MY OWN PHASE 1 FINDING**
PHASE 1 recorded the `residual = 554.58` window as *"the G3 comment's own predicted mechanism, arriving on T not T+1"* — the settled-CNC `used` dropout. **That was INFERENCE and it was WRONG.**

🔬 **The measured mechanism is simpler:** FMGOETZE's **SL GTT genuinely fired at the broker at ~11:21**, which released the broker's margin (`broker_used` 580.22 → 18.47). Our `held` kept counting the position for the **~10 minutes** until `cnc_gtt_monitor`'s next 15-minute pass finalised it at **11:31:10.805**. ⇒ **That is `broker_used` LAG, exactly what the 25-Aug rewording names for `carry = 0`** — *"it is same-day broker-`used` lag"* — ⛔ **not** the settled-CNC mechanism, which requires an actual T+1 settled holding.

⭐ **AND THE MEASURED CONSEQUENCE IS A REAL FINDING IN ITS OWN RIGHT: a ~10-minute local blindness window.** Between the broker closing a delivery position and the monitor's next pass, `trades.status` reads `OPEN` while the broker is flat. That is the `_cnc_monitor_every = 60` cycles × `poll_interval_sec: 15` = **15-minute** cadence, ⛔ not a defect — but it is the latency, and it is now measured.

### B8 · Today's realised P&L and order census
**5 closed · gross −13.87 · net −18.79 · charges 4.92.**
Orders placed today: CNC ENTRY **6 CANCELLED / 3 COMPLETE** · MIS ENTRY **2 CANCELLED / 3 COMPLETE** · MIS SL 1 CANCELLED / 2 COMPLETE · MIS TGT 2 CANCELLED / 1 COMPLETE.

---

## §SCORED PREDICTIONS SO FAR

| # | prediction | outcome |
|---|---|---|
| **P9** (mine) | `cnc_gtt_monitor` takes the **ORPHAN** branch on FMGOETZE and closes it | 🔴 **FAILED — recorded as failed.** It closed via **branch 1**, a genuine SL-GTT fire (`orphan_active_gtt_flat` = 0; exit 561.75 at `sl_trigger` 561.6). ⭐ **My inference substituted a plausible mechanism for a measurement I had not completed** — precisely the failure the standing rules warn against. The correct reading (B7-COROLLARY) is broker-`used` lag after a real fire. |
| **P11** (mine) | carry non-zero only if a CNC leg survives to shutdown | ⏳ **still open** — 20MICRONS is the candidate |
| P1–P8 | — | ⏳ not yet due |


---

# FILE 4C — ADDENDUM. Record corrections, status vocabulary, and a NEW hazard. Appended 26-Aug ~13:05 IST.

🔴 **FILE 4B remains in force in full.** ⛔ This addendum does not replace it; SECTIONS C, D-A, D-B, D-C, E, F still govern the 15:10 / 15:15 / 15:25 / 17:25 / 17:45 / 08:15 windows exactly as written. ⛔ FILE 4A remains SUPERSEDED.

⛔ **This section RE-LABELS. It does not re-measure.** No query already run was re-run; no extra broker call was made.

## §G — RECORD CORRECTIONS

### G0 · THE STATUS VOCABULARY, adopted from here on and retro-applied
`PROVEN` · `NOT EXERCISED` · `FAILED` · `PARTIALLY MEASURED` · `INFERENCE` · `BEHAVIOURALLY EVIDENCED`
⛔ No item is ever left blank. ⛔ "all done" / "complete" / "closed" is never written while any sub-item is open. ⭐ **Every sub-item carries its own label.**

### G1 · A3 — CLAIM DOWNGRADED
> **SUPERSEDED (26-Aug ~12:47):** *"`_gather` computes `held[20MICRONS] = 2`, **proven behaviourally**"*
> ✅ **CORRECTED:** **`held == 2` — `BEHAVIOURALLY EVIDENCED`** via the monitor's verification path (`last_verified_at` advances only through branch 2, `:494-496`, whose condition is `present_active and held == row_qty`). ⛔ **Raw `_gather` output was NOT captured.**

### G2 · A4 — THE ENTRY ROW, AS STORED VALUES · label **`PARTIALLY MEASURED`**

| field | value |
|---|---|
| `symbol` | `20MICRONS` |
| `trade_id` | `trd_5cd243e2b2a3410e9abd31fc3e0e6e98` |
| `strategy` | `positional_swing_long` |
| entry time | `2026-08-26T12:05:26.833978+05:30` |
| `qty_requested` | `2` |
| `qty_filled` (orders row) | `0` |
| `order_type` | `LIMIT` |
| `product` | `CNC` |
| `orders.price` | **NULL** |
| `orders.avg_fill_price` | **NOT STORED** (NULL) |
| `trades.entry_actual_price` | `227.24` |
| placement-log limit price | `227.57394` (`limit_triple.entry_placed`) |
| spread at placement | **NOT MEASURED** |

### G3 · A5 — 🔴 THE CLEAREST GAP · label **`PARTIALLY MEASURED — DIRECT BROKER CONFIRMATION OUTSTANDING`**

Two statements written in the same report are **not equivalent and must not be merged**:
1. *"GTT `333417200` ACTIVE, broker existence confirmed via `last_verified_at`"*
2. *"I did not call the broker directly — all broker state read from the service's own logged polling"*

⇒ (1) is **service-log evidence of what the monitor concluded**, ⛔ not direct broker evidence. ✅ **Corrected label applied.**
⭐ **Safe closure path, at zero extra API cost:** at the **C1 (15:10)** re-run, capture the **freshest `last_verified_at`** and state **its age in minutes**. ⛔ No extra broker call. ⛔ No GTT delete / modify / recreate.
⚠️ **If it cannot be closed safely today it stays `PARTIALLY MEASURED` permanently — that is an ACCEPTABLE outcome and is ⛔ not to be papered over.**

### G4 · F5 — ⛔ "F5 PASSED" IS WITHDRAWN. Split into four.
> **SUPERSEDED (26-Aug ~12:47):** *"✅ **F5 — clean control result, one real gap**"* and *"✅ **F5 EXIT ATTRIBUTION — a clean result**"*

| sub-item | label |
|---|---|
| MIS attribution control cases — HINDCOPPER `SL_HIT`/`OWN_SL`, CYIENT `SL_HIT`/`OWN_SL`, DCBBANK `TGT_HIT`/`OWN_TGT` | ✅ **PROVEN CORRECT** |
| CNC `closure_source` / `exit_mechanism` recording | 🔴 **GAP / INCOMPLETE** |
| the known MANUAL-mislabel defect | **NOT EXERCISED** today |
| the un-attributable exit case | **NOT EXERCISED** today |

⭐ **Two facts, recorded SEPARATELY for the CNC gap:**
* Which leg fired is unambiguous **FROM PRICE** — FMGOETZE `561.75` vs `sl_trigger 561.6` ⇒ **SL**; THEMISMED `131.24` vs `tgt_trigger 131.49` ⇒ **TGT**.
* It is ⛔ **NOT RECORDED** in the row — `closure_source` and `exit_mechanism` are both empty.
⚠️ **Inference from price is ⛔ NOT the same as a stored attribution.**

### G5 · DEFECT B — split into three, plus the bigger weakness

| sub-item | label |
|---|---|
| location — `_resolve_exit_price`, `orders/cnc_gtt_monitor.py:676-696` | ✅ **PROVEN** |
| the final fallback `return float(entry_price or 0.0)` (`:696`) exists | ✅ **PROVEN** |
| live activation of that fallback today | **NOT EXERCISED** |

🔴 **THE REAL WEAKNESS, AND IT IS BIGGER THAN THE FALLBACK: NO PROVENANCE / TIER MARKER IS PERSISTED.** A future audit sees a number in `trades.exit_price` and ⛔ **cannot tell** whether it came from a broker fill (`:685`), a secondary LTP source (`:693`), the entry-price fallback (`:696`), or zero. ⛔ Not fixed. ⭐ **Becomes its own work item.**

### G6 · F4 — KEPT OPEN, in four separated parts

| part | content |
|---|---|
| **measured fact** | today CNC ENTRY **3 COMPLETE / 6 CANCELLED (33%)**; MIS ENTRY **3 COMPLETE / 2 CANCELLED (60%)** |
| **historical comparison** | 21-Aug **3/8** CNC; full history **CNC 30.1%** vs **MIS 52.4%** |
| **possible explanations** | symbol · time of day · spread · market condition — ⚠️ **every one is HYPOTHESIS** |
| **conclusion** | 🔴 **ROOT CAUSE NOT ESTABLISHED** |

**spread at placement = NOT MEASURED.** ⛔ No inference that time of day or spread caused any difference.
> ⚠️ **CORRECTION TO EARLIER WORDING:** anywhere the record implied today's CNC entries filling was an **improvement** over 21-Aug — ⛔ **it was not.** Today's **33%** is **CONSISTENT** with the historical **30.1%**. ⭐ Three fills are not a trend.

### G7 · THE ~10-MINUTE WINDOW — ⛔ "not a defect" IS WITHDRAWN
> **SUPERSEDED (26-Aug ~12:47):** *"⛔ **not a defect**, but now measured"* / *"Not a defect — but it's the explanation for a residual that looks like the revert signature"*

✅ **CORRECTED, and it asserts neither way:**
> **MEASURED broker/local state-observation lag of approximately 10 minutes** (`_cnc_monitor_every = 60` × `poll_interval_sec = 15`). What was demonstrated is precisely this: **the broker position became flat while the local trade status remained `OPEN` until the monitor's next relevant pass.** 👤 **Acceptability vs defect classification remains a DESIGN DECISION — Rama's.**

🔴 **And it must NOT be closed as harmless:** the same timing class may behave **DIFFERENTLY** during **carry**, **GTT recreation** and **capital reconciliation** — see §H.

### G8 · CAPITAL — CONTEXT PRESERVED
The measured sequence (`held 573.05 → ≈0` after the CNC exit → `454.48 = 2 × 227.24`) is good evidence and proves **ONLY the observed SAME-DAY transition**. It does ⛔ **NOT** prove:

| sub-item | label |
|---|---|
| overnight carry reservation | **NOT EXERCISED** |
| T+1 settled-holding treatment | **NOT EXERCISED** |
| broker used/reserved behaviour after carry | **NOT EXERCISED** |
| F6-leg correctness | **NOT EXERCISED** |

### G9 · P9 — **FAILED, PERMANENTLY, AND NOT SOFTENED**
⛔ Not deleted, ⛔ not softened, ⛔ not removed once superseded. The corrected mechanism (broker-`used` lag after a genuine SL fire) stands alongside it, and the propagation of that self-correction into four records **stays**.
⭐ **THE STANDING RULE IT VIOLATED, reinforced in the record: a plausible mechanism is ⛔ NEVER a substitute for a measurement that has not finished.**

---

## §H — 🔴 NEW HAZARD: THE RESIDUAL SIGNATURE NOW HAS **THREE** CAUSES

⭐ **This is new, it follows directly from P9's correction, and it changes how tomorrow's comparator must be read.** Escalated to Rama **now**, ⛔ not after the trigger fires.

On a carry morning, a residual **roughly equal to the position's value** has **THREE** candidate explanations, ⛔ not two:

| # | cause | evidence basis | meaning |
|---|---|---|---|
| **1** | 🔴 **THE ARMED REVERT SIGNATURE** — the condition the trigger was written for | the standing trigger (ledger `:116`) | ⇒ **REVERT** |
| **2** | ⚠️ **THE G3 PREDICTED FALSE POSITIVE** — broker `used` for a SETTLED CNC holding is unmeasured, so alerting *"would fire falsely on the first carry day"* | `order_reconciler.py:3703-3708`, the code's own comment | ⇒ **expected noise** |
| **3** | ⭐ **BROKER-`used` LAG** — **NEW, and measured TODAY** by P9's correction: a residual ≈ position value produced by broker margin release running ahead of the monitor's next pass, at `carry = 0` | measured 26-Aug 11:21→11:31 (`residual 554.58` vs position `573.05`) | ⇒ **a transient observation window** |

🔴 **THE TRIGGER AS WRITTEN CANNOT DISTINGUISH THESE THREE.** Acting on it blindly could **REVERT on what is actually lag**, or **dismiss a genuine revert condition as noise**. Both are serious.

### H1 · THE DISCRIMINATOR — time behaviour, at zero extra broker cost
| cause | time behaviour |
|---|---|
| **LAG** | resolves at the next monitor pass (**≤ ~15 min**) and **does not return** |
| **SETTLED-CNC noise** | **persists** while the holding is unsettled |
| **GENUINE REVERT** | **persists and does not resolve** |

⇒ **Tomorrow the residual is captured as a TIME SERIES, ⛔ never a single reading**, at a minimum of:
**(a)** at boot ~08:15 · **(b)** at the 09:15 `fund_manager.sync_from_broker` · **(c)** immediately AFTER the first CNC-monitor pass following 09:15 · **(d)** one further reading **~15 minutes after (c)**

⭐ At each point: the **raw number**, the **timestamp**, and the **band in force**. ⛔ Do not average them. ⛔ Do not pick the convenient one.

### H2 · BOTH CHECKS, SEPARATELY, AT EVERY READING
Capture **G3 CHECK 1's `delta`** and **G3 CHECK 2's `margin_residual`** as distinct raw numbers, each named with the check that produced it. ⭐ This is FILE 4 PHASE 0's question and it **stays UNRESOLVED until Rama rules**.

### H3 · APPLY THE TRIGGER EXACTLY AS WRITTEN, AND ⛔ NOTHING MORE
⛔ never tune · ⛔ never widen · ⛔ never add a carry term · ⛔ never touch `_total`, RESERVE, COMMIT or the buckets · ⛔ **never redesign the trigger on the night it first fires**.
⚠️ **IF the raw numbers are consistent with MORE THAN ONE of the three causes ⇒ STOP AT THE AMBIGUITY AND ESCALATE.** ⛔ Do not adjudicate. ⭐ **Halting on a genuine ambiguity is correct behaviour.**

### H5 · STANDING HAZARD
§H is recorded against **OWED-2** and the **P0-CONFLICT** as a standing hazard applying to **EVERY future carry day**, ⛔ not just tomorrow.

---

## §I — CROSS-LINK: THE MISSING PRICE IS **SYSTEM-WIDE**, ⛔ NOT CNC-ONLY

**I1.** M6(b) examined only the eight 21-Aug **CNC** orders. Measured today across **all six** entries, **MIS and CNC alike**, `price` and `avg_fill_price` are **NULL on every one**. The value exists in the log (`limit_triple.entry_placed` carries `price:227.57394`) but never reaches the table. ⇒ ⛔ **NOT a CNC-path defect. It is a SYSTEM-WIDE order-observability gap affecting BOTH pipelines.**

**I2.** Consequences, each on its own line:
* **F4's strongest hypothesis (limit placed through the spread) is UNTESTABLE** until placement price and quote are persisted. ⭐ **That makes observability the FIRST F4 change, ⛔ not an execution rewrite.**
* **Any slippage measurement built on `orders.avg_fill_price` reads NULL.**
* **It compounds DEFECT B (G5): neither the ENTRY price provenance nor the EXIT price provenance is persisted.**

**I3.** ⚠️ **FLAGGED, ⛔ NOT INVESTIGATED:** `trades.entry_actual_price` **does** carry values (e.g. `227.24`) while `orders.avg_fill_price` is **NULL**. **Two stores, one fact, disagreeing in availability.** ⭐ Open question for a later work item. ⛔ Out of scope tonight.

**I4.** ⛔ Not fixed. ⭐ Becomes the **F4 observability work item**.


---

# FILE 4D — TWO CORRECTIONS ACCEPTED + THE MISSING DISCRIMINATOR. Appended 26-Aug ~13:35 IST.

🔴 **FILE 4B in force. FILE 4C in force. ⛔ FILE 4A dead.** This file **amends FILE 4C §H only**. ⛔ Record edits only — no code, no DB writes, no broker calls, no push.

## §C-1 — A FRESH `last_verified_at` IS STILL SERVICE-LOG EVIDENCE · **ACCEPTED**

⭐ **The correction is right and I accept it plainly.** FILE 4C §G3 offered *"capture the freshest `last_verified_at`"* as a **"safe closure path"** for A5. **That was wrong.** Freshness proves only that the service's polling observation is **RECENT**; it ⛔ **does not convert service-log evidence into direct broker confirmation.**

> **SUPERSEDED (FILE 4C §G3, 26-Aug ~13:05):** *"⭐ **THE SAFE WAY TO CLOSE IT**, at no extra API cost: … capture the FRESHEST `last_verified_at` and state its age in minutes."*
> ✅ **CORRECTED:** A5 stays **`PARTIALLY MEASURED`**. At C1 capture the freshest `last_verified_at` **and its age in minutes, labelled explicitly as SERVICE-LOG EVIDENCE** — ⛔ this does **not** close the gap and is ⛔ not offered as closing it. ⛔ **Do not spend an API call to close it.**

### 👤 ACCEPTANCE DECISION — recorded as a DECISION, ⛔ NOT as a relabel
> **Service-log evidence IS accepted as operationally sufficient for GTT liveness**, because the monitor's own 15-minute poll is the mechanism the system actually relies on in production.
> ⛔ **A5's label does NOT change — it remains `PARTIALLY MEASURED`.** ⭐ The decision records that the project is content to *operate* on this evidence class; it does ⛔ not assert the evidence is something it is not. **Reversible in one line.**

## §C-2 — 🔴 MY §H DISCRIMINATOR WAS **OVERCLAIMED**. CORRECTED.

⭐ **This is an error in my own reasoning and I record it as one.** FILE 4C §H stated that time behaviour separates all three causes. ⛔ **It does not.**

> **SUPERSEDED (FILE 4C §H1, 26-Aug ~13:05):** *"**THE DISCRIMINATOR — time behaviour** … LAG resolves at the next monitor pass … SETTLED-CNC noise persists … a GENUINE REVERT persists and does not resolve."* — the table implied the three were thereby separable.
> ✅ **CORRECTED, and this is now the binding statement:**
> * a **TRANSIENT** residual that resolves at the next monitor pass ⇒ **LAG**. ✅ **Cleanly separated by the time series.**
> * a **PERSISTENT** residual ⇒ 🔴 **NOT separated.** **Two causes remain live:**
>   * **A** — the genuine armed **REVERT** signature
>   * **B** — the **G3 predicted settled-CNC false positive**
> 🔴 **PERSISTENCE ALONE MUST NEVER BE READ AS REVERT.**

## §C-3 — THE FAIL-SAFE RULE · **STANDING, ALL FUTURE CARRY DAYS**

> *"Apply the trigger exactly as written"* ⛔ **does NOT mean *"revert automatically whenever it fires."***
> 🔴 **FAIL-SAFE UNDER AMBIGUITY: NO AUTOMATIC REVERT · NO TUNING · NO TRIGGER REDESIGN while the cause cannot be distinguished.** Observe, record, escalate.
> ⭐ **A revert of deployed code is an IRREVERSIBLE TRADING ACTION and must ⛔ never be driven by an observational signal whose cause is unresolved.**

---

## §D — 🔴 THE DISCRIMINATOR THAT **DOES** SEPARATE A FROM B: **CAPACITY CONSERVATION**

⭐ The persistent-residual ambiguity **is decidable**, and the test costs nothing extra. It is ⛔ **not temporal**.

**THE INSIGHT — the two persistent causes differ in exactly one measurable way: whether the carried position's money is still SPOKEN FOR.**

| | cause | what the residual is | capital state |
|---|---|---|---|
| **B** | **G3 settled-CNC noise** | a fully-paid delivery holding blocks **no broker margin**, so broker `used` correctly reports ≈0 while local `held` reports the position's value ⇒ a **COMPARISON ARTEFACT between two differently-defined quantities** | 🔴 **THE CAPITAL IS STILL CORRECTLY RESERVED.** Nothing can be double-spent |
| **A** | **genuine REVERT signature** | the carried position's capital has been **RELEASED back into available capacity while the position is still held** | 🔴 **THE SAME MONEY IS AVAILABLE TWICE.** The next entry can over-allocate — **the actual failure the trigger was armed to catch** |

⇒ ⭐ **THE TEST: DOES THE MONEY STILL ADD UP?**

### D1 · At EVERY reading in the §H time series — (a) boot ~08:15 · (b) the 09:15 sync · (c) immediately after the first CNC-monitor pass following 09:15 · (d) ~15 min after (c) — capture these **ADDITIONAL** fields alongside the residual:
1. `_total`
2. reserved / committed, **per bucket**
3. **AVAILABLE CAPACITY FOR A NEW ENTRY, per pipeline**
4. the carried position's value
5. broker `used`
6. `carry`
7. holdings vs positions state for the symbol

### D2 · Then COMPUTE, **showing the operands**:
> **Is the carried position's value still held OUT of available capacity?**
> i.e. does **`available capacity + carried position value ≈ _total`** ?

### D3 · THE VERDICT RULE
| outcome | cause | action |
|---|---|---|
| ✅ **CAPITAL STILL RESERVED** (the sum conserves) | **B — G3 comparison artefact** | 🔴 **NOT the revert condition.** Record the alert and the not-met trigger as **TWO SEPARATE FACTS**. ⛔ Do not revert · ⛔ do not tune · ⛔ do not widen · ⛔ do not add a carry term · ⛔ do not touch `_total`, RESERVE, COMMIT or the buckets |
| 🔴 **CAPITAL RELEASED WHILE THE POSITION IS HELD** (the sum does **not** conserve) | **A — genuine defect; capital is double-counted** | **STOP EVERYTHING AND REPORT IMMEDIATELY.** ⛔ Still **no automatic revert** (per §C-3) — report and escalate. ⭐ **But this is the real thing and must be flagged within MINUTES, ⛔ not at end of session** |
| ⚠️ **THE SUM CANNOT BE COMPUTED** — a field is absent, or the meanings do not line up | **undetermined** | **STOP AT THE AMBIGUITY AND ESCALATE.** ⛔ Do not estimate · ⛔ do not infer. ⭐ **Report exactly which field was missing — an absent measurement is itself the finding** |

### D4 · Reporting discipline
⛔ Do not average readings. ⛔ Do not select a convenient one. ⭐ **Report all four**, each with: timestamp · raw residual · active band · **G3 CHECK 1 raw `delta`** · **G3 CHECK 2 raw `margin_residual`** · which check produced which number · position state · and **whether the value resolved after the next pass**.

### D5 · SCOPE
⭐ This test applies to **EVERY future carry day**, ⛔ not just tomorrow. It **replaces the overclaimed time-only wording** of FILE 4C §H against **OWED-2** and the **P0-CONFLICT**.


---

# FILE 4E — CONSERVATION TEST: PER-PIPELINE, SAME-UNIT. 🔴 BINDING CORRECTION. Appended 26-Aug ~13:50 IST.

🔴 **FILE 4B · 4C · 4D all in force. ⛔ FILE 4A dead.** This file **amends FILE 4D §2/D3 only**. ⛔ Record edit only — no code, no DB writes, no broker calls, no push.

## §1 — THE CORRECTION · ACCEPTED AND BINDING

> **SUPERSEDED (FILE 4D §D2, 26-Aug ~13:35):** *"does **`available capacity + carried position value ≈ _total`** ?"*

🔴 **That was unsafe as written, on two counts, and both are accepted:**

**F-1 · NO PIPELINE AXIS.** This system is **TWO INDEPENDENT PIPELINES** sharing no capital pool, no reservation state, no config, no counters, no halt. ⛔ A cross-pipeline conservation equation is meaningless, and a pooled number mixing both books is **worse than no number**.

**F-2 · MIXED ACCOUNTING UNITS.** 🔴 **Position notional is NOT the reservation amount.** At 5× MIS a ₹10,000 notional consumes ₹2,000 of reservation — substituting notional would manufacture an ₹8,000 **phantom gap** and report a defect that does not exist. ⚠️ **And it bites even at 1×:** M12(d) measured reservation as `notional / leverage` **plus a ~5% buffer**, so even for DELIVERY at leverage 1.0, **notional ≠ reservation**. ⛔ Do not assume equality because the leverage happens to be 1.

## §2 — 🔬 THE TWO SOURCE QUESTIONS, ANSWERED NOW (source-only; ⛔ no broker call, ⛔ no DB write)

### STEP 3's buffer question — 🔴 **THE ANSWER IS A THIRD OPTION THE BRIEF DID NOT LIST**

The brief posed: *"EITHER the buffer does not apply to CNC, OR `held` is a different quantity from the reservation."* 🔬 **Measured from source: NEITHER, exactly.**

* `capital/fund_manager.py:562` — `slm_buffer = base_margin * self._slm_buffer_pct` is **UNCONDITIONAL**. ⛔ **No intent branch.** ⇒ **the buffer DOES apply to CNC.**
* `capital/fund_manager.py:561` — *"Buffer is held until SL-M is accepted, then **released via `release_slm_buffer()`**"* — and that method exists at **`:689`**, setting **`slm_buffer=0.0`** at **`:754`** (*"Buffer now released"*).

⇒ ⭐ **The buffer applies to CNC, but it is TRANSIENT.** By the time of today's measurement the SL had been accepted and the buffer released, which is why `held = 454.48 = exactly 2 × 227.24` with **no buffer visible**.

🔴 **THE CONSEQUENCE FOR TOMORROW'S TEST: the authoritative reservation is TIME-DEPENDENT.**
* at reserve time ≈ `454.48 × 1.05 = 477.20`
* after `release_slm_buffer` = `454.48`

⚠️ For a **carried** position at T+1 the SL was accepted long ago, so the buffer is released and `reservation = notional / leverage = 454.48 / 1.0 = 454.48`. ⛔ **That numeric coincidence with notional is an artefact of leverage 1.0 PLUS buffer-release — it is ⛔ NOT an identity.** ⭐ **All three of (i) notional, (ii) authoritative reservation, (iii) `held` are still reported SEPARATELY, per STEP 3.**

### §5's question — ✅ **PER-PIPELINE AVAILABLE CAPACITY EXISTS IN THE DEPLOYED CODE. THE TEST IS COMPUTABLE.**

🔬 Measured at `75e637c`, ⛔ not assumed from the F2 design:

| element | location |
|---|---|
| `self._intraday_avail` / `self._positional_avail` | `capital/fund_manager.py:368` / `:373` |
| initialised as `broker_balance × pct` (the 70/30 split) | `:478-481` |
| `_bucket_for_intent(intent)` → INTRADAY / POSITIONAL bucket | `:2337-2342` |
| `_bucket_avail(bucket)` | `:2344-2345` |
| `_bucket_reserved` / `_bucket_used` | `:2347` / `:2350` |

⇒ ✅ **NOT a CANNOT COMPUTE.** The DELIVERY pipeline has its own `_positional_avail`, `_positional_reserved`, `_positional_used`.

### 🔴 AND THE EXACT PAIR THE TEST TURNS ON — `capital/fund_manager.py:1832-1837`

```python
1832|             self._positional_carry = (
1833|                 self._positional_reserved + self._positional_used
1834|                 - _positional_committed_before
1835|             )
1836|             self._positional_avail += self._positional_carry
1837|             self._total += self._positional_carry
```

⭐ **On rehydrate the carry lifts BOTH `_positional_avail` AND `_total` by the same amount.** That is precisely why conservation should hold — and it matches the G3 docstring's *"carry cancels"* algebra (`total = N+C`, `held = C+M`, `expected = (N+C)−(C+M) = N−M`).
🔴 ⇒ **IF `_total` is lifted but `_positional_avail` is NOT (or vice versa), conservation BREAKS — and that is cause A.** ⭐ **These two lines are the specific thing to watch tomorrow.** ⛔ Not asserted as the outcome; recorded as the mechanism to measure.

## §3 — THE CORRECTED TEST · REQUIRED ORDER, ⛔ DO NOT REORDER

🔴 **The question is NOT *"does available + position value equal total?"***
🔴 **It IS: *"According to THIS PIPELINE'S OWN capital model, is the capital attributable to the carried position still ACCOUNTED FOR OUTSIDE that pipeline's available capacity?"***

**STEP 1 · IDENTIFY THE PIPELINE FIRST.** 20MICRONS is CNC ⇒ **DELIVERY** ⇒ use the DELIVERY pipeline's own accounting (`_positional_*`). ⛔ Never combine the two. ⛔ Never use a pooled figure that mixes both books.

**STEP 2 · IDENTIFY THE ACCOUNTING UNIT, and NAME IT in the report.** ⛔ These are **not interchangeable**: real broker cash / cash reservation · effective buying capacity (segment capital) · internal pipeline reserved-committed. ⭐ Measure which unit `_total` is actually expressed in at `75e637c`. ⛔ Do not assume.

**STEP 3 · IDENTIFY THE AUTHORITATIVE RESERVATION from the pipeline's own model (`fund_manager`), ⛔ not from the position row.** Report **all three separately** and ⛔ never substitute one for another:
* **(i)** notional = `qty × price`
* **(ii)** authoritative reservation per `fund_manager`'s model — ⚠️ **time-dependent, see §2**
* **(iii)** `held` as the monitor reports it

**STEP 4 · ONLY THEN compute, ⭐ SHOWING THE OPERANDS WITH THEIR UNIT:**
```
pipeline            : DELIVERY
accounting unit     : <named>
pipeline _total     : <value>
available capacity  : <value>            (_positional_avail)
carried reservation : <value>            <- (ii), NOT (i)
<available> + <reservation> = <sum>   vs   <_total>
```

## §4 — VERDICT RULE (FILE 4D §D3, corrected)

| outcome | cause | action |
|---|---|---|
| ✅ **CONSERVES, in the pipeline's own unit** | **B — G3 comparison artefact** | ⛔ **NOT the revert condition.** Record the alert and the not-met trigger as **TWO SEPARATE FACTS**. ⛔ No revert · ⛔ no tuning · ⛔ no widening · ⛔ no carry term · ⛔ no touching `_total`, RESERVE, COMMIT or the buckets |
| 🔴 **DOES NOT CONSERVE** | **A — genuine capital-release defect becomes the LEADING EXPLANATION.** The same money is available twice; the next entry can over-allocate | **STOP AND REPORT WITHIN MINUTES** (⛔ not at end of session). ⛔ **STILL NO AUTOMATIC REVERT** — C-3's fail-safe stands. Report and escalate |
| ⚠️ **CANNOT COMPUTE** — a field absent, or units do not align | undetermined | **STOP AT THE AMBIGUITY.** Name the **exact** missing/misaligned field **and unit**. ⛔ Do not estimate · ⛔ do not infer. ⭐ An absent measurement is itself the finding |

## §5 — TERMINOLOGY · BINDING

⭐ Write **"capital/reservation remains ACCOUNTED FOR at the `<named>` layer."**
⛔ **Do NOT write "capital is still reserved" unqualified.**
**Reason:** broker `used`, local `held`, effective buying power, position notional and internal reservation are **five different things**. ⚠️ A future reviewer reading *"reserved"* may take it as a broker-side blocked amount when it was an internal pipeline figure. ⭐ **Always name the layer that conserved.**

## §6 — PIPELINE INDEPENDENCE IN THE TEST ITSELF

```
ONE TRADING SYSTEM
  ├── MIS pipeline           — own capital, own limits, own halt
  └── DELIVERY/GTT pipeline  — own capital, own limits, own halt
```
⛔ **No cross-pipeline conservation equation, ever.** ⭐ A capital-release defect found in DELIVERY blocks DELIVERY **by DELIVERY's rules** and ⛔ must not silently stop MIS; the reverse likewise.
⚠️ **MEASURED, ⛔ NOT ASSUMED (§2):** the deployed system **does** separate the buckets — `_intraday_avail` / `_positional_avail` with `_bucket_for_intent` routing. ⇒ the test runs against **deployed reality**, ⛔ not the F2 design.

## §7 — D1 READINGS, EXTENDED

At each of the four readings — **(a)** boot ~08:15 · **(b)** the 09:15 sync · **(c)** immediately after the first CNC-monitor pass following 09:15 · **(d)** ~15 min after (c) — capture, ⛔ **without averaging** and ⛔ **without cherry-picking**:

timestamp · raw residual · active band · **G3 CHECK 1 raw `delta`** · **G3 CHECK 2 raw `margin_residual`** · which check produced which number · **pipeline identity** · **accounting unit** · `_total` · reserved/committed per bucket · **available capacity for that pipeline** · **authoritative carried-position reservation** · position notional (⚠️ **labelled NOT-THE-RESERVATION**) · broker `used` · `carry` · holdings-vs-positions state · **whether the residual resolved at the next pass**

⭐ **Report the EQUATION, ⛔ not just the verdict.**


---

# FILE 4F — 🔴 THE CONSERVATION EQUATION CAN PASS WHILE THE DEFECT IS PRESENT. Appended 26-Aug ~14:20 IST.

🔴 **FILE 4B · 4C · 4D · 4E all in force. ⛔ FILE 4A dead.** Amends the conservation test in 4E; adds one source task (done below) and one baseline to tonight's DB5. ⛔ No code change, no DB writes, no broker calls, no push.

## §1 — 🔴 THE HOLE IN MY OWN TEST · **I WORKED THE ALGEBRA AND IT IS REAL**

⭐ **Accepted, and recorded as my third error in this sequence.** I did not take it on assertion — I worked it:

Rehydrate does `_positional_avail += _positional_carry` and `_total += _positional_carry`.

**CASE 1 — the carried position IS re-reserved:**
```
avail       = avail₀ + carry − R
reservation = R
total       = total₀ + carry
available + reservation = (avail₀ + carry − R) + R = avail₀ + carry     vs  total₀ + carry
```
**CASE 2 — the carried position is NOT re-reserved:**
```
avail       = avail₀ + carry          (the ₹454 is now SPENDABLE)
reservation = 0
total       = total₀ + carry
available + reservation = (avail₀ + carry) + 0 = avail₀ + carry         vs  total₀ + carry
```

🔴 **BOTH CASES PRODUCE THE IDENTICAL SUM.** The equation returns **CONSERVES** in CASE 2 — **while the same money is available twice and the next entry can over-allocate.** That is cause A, undetected, **reported as safe.**

> ⇒ 🔴 **CHECK 1 (the conservation equation) IS NECESSARY BUT NOT SUFFICIENT. ⛔ It must NEVER be reported alone.**

### ✅ CHECK 2 — THE BASELINE-DELTA / SPENDABILITY TEST. **BOTH must pass.**
The position and the capital behind it are the same whether held same-day or carried ⇒ **the pipeline's available capacity should be the same in both states.**

| | |
|---|---|
| **A_sameday** | `_positional_avail` **tonight**, at the last pre-shutdown reading, with 20MICRONS OPEN |
| **A_carry** | `_positional_avail` **tomorrow**, after rehydrate, with 20MICRONS STILL HELD |

| outcome | meaning | action |
|---|---|---|
| ✅ **A_carry ≈ A_sameday** | carried capital is **NOT spendable** ⇒ supports conservation. With CHECK 1 = CONSERVES ⇒ **cause B, artefact** | ⛔ no revert |
| 🔴 **A_carry ≈ A_sameday + carry** | the carry was added to available and **never re-reserved** ⇒ **the same money is available twice** ⇒ **cause A** | **STOP AND REPORT WITHIN MINUTES — even if CHECK 1 said CONSERVES.** ⛔ Still no automatic revert; observe, record, escalate |
| ⚠️ anything else / missing baseline | — | **CANNOT COMPUTE.** Name the exact missing field. ⛔ Do not estimate. ⛔ Do not infer |

⭐ **REPORT CHECK 1 AND CHECK 2 SEPARATELY AT EVERY READING.** ⛔ Never collapse them into one verdict. ⛔ **A CONSERVES from CHECK 1 with a missing CHECK 2 is `PARTIALLY MEASURED`, ⛔ not a pass.**

## §2 — STANDING RULES ADOPTED

**R-1 · A CODE FACT IS NOT AN ECONOMIC INVARIANT.** That `:1836-1837` lift two variables by the same delta is a **MEASURED CODE FACT**. That the resulting accounting is **CORRECT** is a **SEPARATE CLAIM** requiring the surrounding model. ⭐ Keep the two apart in every record. ⛔ A two-line observation never replaces the full measurement.

**R-2 · THE BUFFER/RESERVATION RULE, PERMANENT.** ⛔ Never *"reservation = notional"*. ⭐ Always **"reservation is whatever the authoritative pipeline model says AT THAT STATE AND TIMESTAMP."** Today's numerical equality (454.48) is an artefact of **leverage 1.0 PLUS buffer release** — ⛔ not an identity; it breaks the moment leverage, buffer state, order state or strategy changes. ⇒ **Always report all three and state explicitly whether B and C are equal:** **A** notional · **B** authoritative reservation · **C** monitor `held`. ⛔ **Never silently treat B = C.**

**R-3 · PIPELINE INDEPENDENCE IS A HARD BOUNDARY.** ⛔ Never introduce a shared master halt or shared capital pool to solve anything.

**R-5 · ⛔ DO NOT FORCE AN EQUATION TO PRODUCE A VERDICT.** Unit mismatch ⇒ **`CANNOT COMPUTE — UNIT MISMATCH`**, a **VALID result**, ⛔ not a failure of the investigation.

### R-4 · REQUIRED MINIMUM OUTPUT AT EVERY READING — ⭐ evidence first, ⛔ no explanation before the numbers
```
PIPELINE:
ACCOUNTING UNIT:
TIMESTAMP:
_total =
_available =
authoritative reservation =
held =
notional =
reserved/committed =
broker used =
carry =
EQUATION: <operands with units>
RESULT: CONSERVES / DOES NOT CONSERVE / CANNOT COMPUTE
residual =            G3 CHECK 1 =        G3 CHECK 2 =
position state =      next-pass resolution = yes/no
```

## §3 — 🔬 THE SOURCE TASK · **DONE NOW. IT IS CASE 1.**

⛔ Source-only; no broker call, no DB write.

**S1 · The call path.** Enclosing function **`rehydrate_from_open_trades`**, `capital/fund_manager.py:1720`, called **once at startup, AFTER `initialize()`** (`:1727`).

**S2 · 🔴 THE DECIDING QUESTION — DOES REHYDRATE CREATE A RESERVATION? ✅ YES. Quoted:**
```python
1788|            open_trades = self._store.get_all_open_trades()
1789|            for trade in open_trades:
1790|                if self._replay_open_trade(trade, anomalies):
1791|                    replayed_trades += 1
```
and the docstring, `:1729-1734`:
> *"Walks every OPEN/PARTIAL trade, looks up its `reservation_id` … then **replays the ordered RESERVE/COMMIT chain** for that reservation through **`_apply_reserve` / `_apply_commit` — the same mutation helpers the public `reserve()`/`commit_to_used()` use**"*

🔬 **Corroborated:** `_apply_reserve` is called at **`:2105`** and `_apply_commit` at **`:2128`** inside the replay path. ⇒ **the reservation IS recreated.**

⭐ **And the code states the economic invariant in its own words, `:1803-1807`:**
> *"**The position is NOT forgotten: it stays in reserved/used at full value**, and the carry is now named, so the exposure is more visible than before, not less. **Net effect on free capital is ZERO** — the carry enters the base and is immediately consumed by reserved/used."*

⇒ `_positional_carry` is measured **BY DIFFERENCE** — `:1785-1787` before Phase 1, `:1832-1835` after — so it is **exactly what Phase 1 committed** to the positional bucket. `avail += carry` restores what Phase 1's deduction removed; `total += carry` lifts total from cash to account value.

⚠️ **Historical context in the same comment (`:1799-1800`):** deducting it twice *"drove `positional_avail` to **−844.08 on 10-Aug and hard-killed both books**"* — the FIX-1 origin, and it ties to the standing hazard that a negative bucket `avail` hard-kills both books.

**S3 · THE ACCOUNTING UNIT, NAMED FROM SOURCE.** `_bucket_base`, `:2331-2335`:
```python
2331|        carry_total = self._intraday_carry + self._positional_carry
2332|        cash = self._total - carry_total
2334|        if bucket == _INTRADAY_BUCKET: return cash * self._intraday_pct + self._intraday_carry
2335|        return cash * self._positional_pct + self._positional_carry
```
with its docstring `:2325-2326`: *"the bases still sum to `_total` **exactly** — which is the global identity `_check_invariant` actually enforces."*
⇒ 🔴 **`_total` is ACCOUNT VALUE (cash + carry), ⛔ NOT broker cash.** Confirmed by `:1811-1813`: *"broker `net` was 209.80 while 907.02 of CNC stock was held — an account of ~1,117. **Delivery cash is GONE from `net`; the position is a HOLDING, not a claim on cash.**"*
⇒ **ACCOUNTING UNIT = rupees of ACCOUNT VALUE / segment capacity.** ⛔ Never compare it directly to broker cash.

**S4 · IS THERE A SPENDABLE WINDOW BETWEEN BOOT AND 09:15? ✅ NO.** The 09:15 `sync_from_broker` **recomputes** availability rather than adding to it, `:1465-1466`:
```python
1465|            self._positional_avail = (
1466|                positional_total - self._positional_reserved - self._positional_used
1467|            )
```
where `positional_total = _bucket_base(_POSITIONAL_BUCKET)` (`:1455`), which **includes the carry**. ⇒ because the reservation persists in `reserved`/`used`, availability **excludes it at 09:15 too**. ⛔ **No separate re-establishment is needed and no boot→09:15 spendable window exists in source.**

### ⇒ 🔴 VERDICT ON §3, LABELLED HONESTLY
**`CASE 1 — SUPPORTED BY SOURCE`.** ⛔ **NOT `PROVEN`, and ⛔ NOT `OBSERVED`.** This is source evidence of what the code *should* do; the deployed system has **never** executed a real overnight carry. ⭐ **Tomorrow's measurement runs in FULL regardless — source is ⛔ not a substitute for observing the deployed system.**

## §4 — TONIGHT'S **A_sameday BASELINE** · folds into FILE 4B §D-B / DB5

🔴 **WITHOUT TONIGHT'S BASELINE, CHECK 2 IS NOT COMPUTABLE TOMORROW.** At the **last reading before shutdown**, capture explicitly and by name, labelled **`A_sameday BASELINE`**:

`_total` · `_positional_avail` · `_positional_reserved` / committed · `_positional_carry` · `_intraday_avail` (**for contrast only — ⛔ never in the equation**) · broker `used` · the **authoritative reservation for 20MICRONS at that instant** · notional · `held`

⚠️ **IF BRANCH A RUNS** (20MICRONS closed before the close): CHECK 2 and the whole carry measurement are **`NOT EXERCISED`**. ⛔ **Do not manufacture a baseline from a flat book.** Record as owed and **re-armed for the next carry day**.

## §5 — ERRORS OWNED, ⛔ NOT QUIETLY SUPERSEDED

| # | error | status |
|---|---|---|
| 1 | **P9** — predicted the orphan branch; it was a genuine SL fire. I substituted a plausible mechanism for an unfinished measurement | 🔴 **FAILED**, permanent |
| 2 | **FILE 4D's conservation equation** — no pipeline axis, and it mixed notional with reservation (would have manufactured a phantom gap) | 🔴 **UNSAFE**, withdrawn |
| 3 | **FILE 4E's corrected equation was STILL insufficient alone** — CHECK 1 returns CONSERVES in CASE 2 while cause A is present | 🔴 **INSUFFICIENT**, superseded by CHECK 1 + CHECK 2 |


---

# FILE 4G — CHECK 2a DIRECT. 🔴 THE TEST DESIGN CLOSES HERE. Appended 26-Aug ~14:35 IST.

🔴 **FILE 4B · 4C · 4D · 4E · 4F in force. ⛔ FILE 4A dead.** ⛔ **No further test-design files. The next output is EVIDENCE, ⛔ not analysis.**

## §1 — 🔴 THE CONFOUND IN MY OWN CHECK 2, NAMED · AND WHY 2a REMOVES IT

⭐ **Accepted, and it is my fourth owned error.** CHECK 2 as I wrote it in FILE 4F was a **DELTA test**, and a delta here has a confound I did not name:

`_positional_avail` is recomputed at 09:15 as `positional_total − reserved − used` (`fund_manager.py:1465-1466`), and `positional_total` derives from `_total` via `_bucket_base` (`:1455`, `:2331-2335`).
🔴 **`_total` LEGITIMATELY MOVES OVERNIGHT** — settlement, charges, realised P&L.

🔬 **Confirmed from evidence already in hand, ⛔ no new investigation:** `sync_from_broker` **re-derives** `_total` from broker cash and logs both sides — `:1468-1470` `extra={"old_total": old_total, "new_total": new_total, …}` — and today's live line reads `broker_cash:10567.6, carry:0.0, new_total:10567.6, old_total:10567.6`.

⇒ ⚠️ **Even in a perfectly correct CASE 1, `A_carry` will NOT equal `A_sameday`,** and the delta will be non-zero for reasons that have **nothing to do with the carry**. **A delta test alone can produce a spurious signal in either direction.**

## §2 — 🔴 CHECK 2a · DIRECT RESERVATION ATTRIBUTION · **PRIMARY, SINGLE READING**

> **SUPERSEDED (FILE 4F §1, 26-Aug ~14:20):** CHECK 2 stated as a delta test — *"`A_carry ≈ A_sameday` ⇒ … `A_carry ≈ A_sameday + carry` ⇒ cause A"* — presented as the discriminator. **Retained, marked superseded as PRIMARY; it survives DEMOTED to corroborating (CHECK 2b).**

The source states the invariant in its own words (`:1803-1807`): the position *"stays in reserved/used at full value."* ⭐ **So observe that directly, rather than through a proxy:**

> 🔴 **CHECK 2a — After rehydrate, does `_positional_reserved` / `_positional_used` contain 20MICRONS at its full AUTHORITATIVE value?**

| outcome | meaning | action |
|---|---|---|
| ✅ **YES** | the carried capital is **NOT spendable** ⇒ **CASE 2 is EXCLUDED** | proceed |
| 🔴 **NO / ABSENT** | the carry entered available with **nothing holding it** ⇒ **CASE 2 is LIVE** | **STOP AND REPORT WITHIN MINUTES.** ⛔ Still no automatic revert |
| ⚠️ **not resolvable to the symbol** | — | **CANNOT COMPUTE.** Name the exact missing field |

### ⭐ WHY 2a IS STRONGER THAN 2b — and this is the part that matters
* **IMMUNE to overnight `_total` drift** — a single reading, ⛔ no delta
* **NEEDS NO BASELINE** ⇒ it **survives BRANCH A tonight** and works on **ANY future carry day with no prior setup**
* **It tests the invariant the code actually claims**, ⛔ not a proxy for it

### ⇒ CHECK 2b (the delta) is now **CORROBORATING, ⛔ NOT PRIMARY**
Still run it when a **valid** baseline exists. ⭐ Report **`Δ_total` ALONGSIDE `Δ_avail`**, plus **`Δ_reserved`** and **`Δ_used`**, so legitimate drift is separable from a release. ⛔ **Never report `Δ_avail` alone.**

### 🔴 THE COMBINED RULE
| combination | cause | action |
|---|---|---|
| CHECK 1 ✅ **+ CHECK 2a ✅** (+ 2b consistent) | **B — artefact** | ⛔ no revert · ⛔ no tuning · ⛔ no widening · ⛔ no carry term · ⛔ no touching `_total`/RESERVE/COMMIT/buckets. Alert and not-met trigger as **TWO SEPARATE FACTS** |
| **CHECK 2a 🔴 FAILS** | **A — regardless of what CHECK 1 says** | **STOP AND REPORT WITHIN MINUTES.** ⛔ Still no automatic revert |
| **any check missing** | — | **PARTIALLY MEASURED.** ⛔ Never *"a successful carry test"* |

## §3 — STANDING RULES ADOPTED (N-1 … N-7)

**N-1 · ⛔ "≈" IS NOT A FREE PASS.** ⛔ Never write `A_carry ≈ A_sameday` without the delta. ⭐ Always show `A_sameday` · `A_carry` · `Δ = A_carry − A_sameday` · `C = carry` · classification. ⛔ **Do NOT invent a tolerance — the deployed model defines none.** ⭐ **Classify by RATIO instead — scale-free, invents nothing:**

| ratio | reading |
|---|---|
| `Δ / C ≈ 0` | supports **NOT NEWLY SPENDABLE** |
| `Δ / C ≈ 1` | **strong evidence the carry entered available** |
| `0 < Δ/C < 1` | 🔴 **partial release OR a mix of unrelated changes ⇒ NEEDS INVESTIGATION, ⛔ not a verdict** |

**Report `Δ` and `Δ/C` both.**

**N-2 · THE BASELINE MUST BE A COMPARABLE STATE.** Required: same pipeline (DELIVERY) · same position (20MICRONS) · position still open · same reservations/commitments · the **last VALID** pre-shutdown reading · ⛔ no unrelated new order or reservation inserted between the reading and shutdown. ⭐ Label it exactly **`A_sameday BASELINE — LAST VALID PRE-SHUTDOWN READING`**, ⛔ not "baseline". ⚠️ **If an unrelated order or reservation DID change in between, the baseline is INVALID — say so; ⛔ do not use it anyway.**

**N-3 · THE VERDICT IS ⛔ NOT A BLIND ARITHMETIC TRIGGER.** It rests on four things together: **(1)** the delta · **(2)** reservation/commit state · **(3)** position state · **(4)** any legitimate account/capital change. ⭐ **CHECK 2 is a strong DETECTION test, ⛔ not an automatic classifier.**

**N-4 · LANGUAGE, PERMANENT.** ✅ *"CASE 1 — **SUPPORTED BY SOURCE**"* · ⛔ **NOT** *"CASE 1 — PROVEN IN LIVE OVERNIGHT OPERATION"*. The deployed system has **never** executed a real overnight carry. ⛔ **Do not collapse source support into live proof.**

**N-5 · LIKEWISE.** ✅ *"Source indicates **no INTENDED** boot→09:15 spendable window"* · ⛔ **NOT** *"there can never be a boot→09:15 window."* ⭐ **Measure it tomorrow.**

**N-6 · `_total` IS ACCOUNT VALUE (cash + carry), ⛔ NOT broker cash.** ⛔ Never compare the two unless source defines them identical — measured: **broker net 209.80 while 907.02 of CNC stock was held.** ⭐ **This is the SECOND reason FILE 4D's equation was unsafe.**

**N-7 · PIPELINE INDEPENDENCE, HARD BOUNDARY.** ⛔ No shared master halt · ⛔ no shared capital pool · ⛔ no new capital model · ⛔ no new reconciliation subsystem · ⛔ no new broker API · ⛔ no paper-trading detour. ⭐ **The route is already the shortest correct one: SOURCE TRACE → TONIGHT BASELINE → TOMORROW REHYDRATE → CHECK 1 → CHECK 2a → EVIDENCE-BASED BRANCH.**

## §4 — THE REPORTING TEMPLATE · FINAL FORM

At every reading — **(a)** boot ~08:15 · **(b)** 09:15 sync · **(c)** immediately after the first CNC-monitor pass following 09:15 · **(d)** ~15 min after (c). ⭐ **Evidence first. ⛔ No explanation before the numbers.**

```
PIPELINE:                    ACCOUNTING UNIT:            TIMESTAMP:
_total =                     _available =
authoritative reservation =  held =                      notional =
reserved/committed =         broker used =               carry =
EQUATION: <operands with units>
CHECK 1 RESULT: CONSERVES / DOES NOT CONSERVE / CANNOT COMPUTE

CHECK 2a — 20MICRONS present in reserved/used at full value? YES / NO /
           CANNOT COMPUTE      value found =
CHECK 2b — A_sameday =   A_carry =   Δ_avail =   C =   Δ_avail/C =
           Δ_total =     Δ_reserved =            Δ_used =
           delta classification =

residual =        G3 CHECK 1 =        G3 CHECK 2 =
position state =  next-pass resolution = yes/no
```

⛔ Do not average · ⛔ do not cherry-pick · ⛔ do not replace a missing reading with a later one · ⛔ do not force an equation to produce a verdict — **unit mismatch is `CANNOT COMPUTE — UNIT MISMATCH`, a VALID result.**

## §5 — TONIGHT'S DB5 BASELINE · FULL FIELD LIST

At the **LAST VALID** pre-shutdown reading, capture and name **`A_sameday BASELINE — LAST VALID PRE-SHUTDOWN READING`**, **DELIVERY pipeline only**:

pipeline · timestamp · `_total` · `_positional_avail` · `_positional_reserved`/committed · `_positional_carry` · `_intraday_avail` (**contrast only, ⛔ never in the equation**) · broker `used` · **authoritative reservation for 20MICRONS** · notional · `held` · position state · active reservations/orders

⛔ Do not substitute MIS numbers · ⛔ do not substitute pooled numbers · ⛔ do not manufacture it from a flat book.

⚠️ **IF BRANCH A RUNS:** CHECK 2b = **`NOT EXERCISED — NO OPEN CARRY CANDIDATE`**, re-armed for the next real candidate. ⭐ **CHECK 2a SURVIVES and needs no baseline — it remains available on any future carry day.**

## §6 — ERRORS OWNED · RUNNING LIST

| # | error | status |
|---|---|---|
| 1 | **P9** — plausible mechanism substituted for an unfinished measurement | 🔴 **FAILED**, permanent |
| 2 | **FILE 4D's conservation equation** — no pipeline axis; mixed notional with reservation | 🔴 **UNSAFE**, withdrawn |
| 3 | **FILE 4E's corrected equation still insufficient alone** — CHECK 1 conserves in CASE 2 | 🔴 **INSUFFICIENT**, superseded |
| 4 | **FILE 4F's CHECK 2 was delta-only** and carried an **unnamed overnight `_total`-drift confound** | 🔴 **CONFOUNDED**, demoted to corroborating (2b); CHECK 2a is primary |

## §7 — FINAL OPERATING RULE, STANDING

> ⭐ **SOURCE CAN SUPPORT THE EXPECTED MECHANISM.**
> ⭐ **ONLY THE DEPLOYED MEASUREMENT CAN CONFIRM THE ACTUAL BEHAVIOUR.**
> ⭐ **CHECK 1 proves accounting ARITHMETIC. CHECK 2a tests whether the capital is ACTUALLY HELD. BOTH are required.**

🔴 **THE TEST DESIGN IS CLOSED. GO MEASURE.**


---

# FILE 4H — MAKING CHECK 2a EXECUTABLE. Appended 26-Aug ~15:00 IST. ⛔ No new design.

## §1 — 🔴 U-1 ANSWERED FROM SOURCE: **BOTH.** CHECK 2a RUNS AS **U-2**, ⛔ NOT U-3.

| | finding |
|---|---|
| **Bucket fields ARE scalars** | `_positional_reserved: float` (`:374`), `_positional_used: float` (`:375`) — ⛔ not per-symbol ledgers. The risk in U-1 was real |
| **BUT a per-reservation registry EXISTS** | `self._reservations: dict[str, _Reservation]` — **`capital/fund_manager.py:404`** |
| **And `_Reservation` CARRIES THE SYMBOL** | `:229-241` — `reservation_id` · **`symbol`** · `qty` · `price` · `intent` · **`margin`** · `bucket` · `signal_id` · `ts` · `slm_buffer` · `strategy` |
| **With a public accessor** | `get_live_reservations()` — **`:1543`**, returning a shallow copy under the lock |

⇒ ✅ **CHECK 2a is DIRECTLY EXECUTABLE per-symbol (U-2). ⛔ It does NOT need to fall back to U-3's sum identity.** ⭐ U-3 remains available as a **corroborating** cross-check: `Σ(margin of positional reservations)` vs `_positional_reserved + _positional_used`.

## §2 — 🔴 THE READ-ONLY EXECUTION ROUTE · `fm_ledger` + `trades`

⚠️ `get_live_reservations()` is **in-memory on the running process** — ⛔ not callable externally without touching it. ⭐ **The persisted equivalent is `fm_ledger`, and it is fully sufficient:**

`fm_ledger` columns: `ledger_id · ts · entry_type · amount · bucket · balance_before · balance_after · signal_id · reservation_id · reason · session_id · direction · trade_id · margin_delta · pnl_delta · costs`

**Measured today, 20MICRONS, read-only:**
```
trades.reservation_id  = 74dcc30b517549f1
trades.margin_reserved = 455.14788

fm_ledger WHERE reservation_id = '74dcc30b517549f1':
 11484  12:05:23.128  RESERVE  477.905274  positional  margin_delta=477.905274  bal 3170.46      -> 2692.554726
 11485  12:05:26.834  COMMIT   454.48      positional  margin_delta=0.0         bal 2692.554726  -> 2715.98
```

⇒ ⭐ **Per-symbol attribution, the authoritative reservation, AND `_positional_avail` are ALL readable from the DB, read-only, with ⛔ no broker call and ⛔ no process access.** `balance_after` on the latest positional row **IS** `_positional_avail` (**2715.98** at 12:05:26).

## §3 — 🔴 T-2 PROVES ITSELF CONCRETELY · **FOUR DIFFERENT NUMBERS FOR "THE SAME" QUANTITY**

| quantity | value | what it is |
|---|---|---|
| **RESERVE** (`fm_ledger` 11484) | **477.905274** | base **+ the 5% slm buffer** |
| `trades.margin_reserved` | **455.14788** | the **reserve-time BASE**, at the entry **TARGET** price (`2 × 227.57394`) |
| **COMMIT** (`fm_ledger` 11485) | **454.48** | 🔴 **THE AUTHORITATIVE RESERVATION AT THE CURRENT STATE**, at the **FILL** price (`2 × 227.24`) |
| notional (at fill) / monitor `held` | **454.48** | market value / the monitor's figure |

🔬 **The buffer is confirmed from data, not just source:** `455.14788 × 1.05 = 477.905274` **exactly** ⇒ the 5% slm buffer **IS applied to CNC**, then partially returned at COMMIT (`477.905274 − 454.48 = 23.425274`, matching `2692.554726 → 2715.98`).

> ⚠️ **CORRECTION TO MY OWN FILE 4E/4F WORDING:** I wrote that for a carried position *"reservation numerically equals notional at leverage 1.0"*. 🔴 **That was wrong.** `trades.margin_reserved` (455.14788) equals notional at the **TARGET** price, ⛔ not the **FILL** price. The COMMIT figure (454.48) is the one that matches fill-notional — and it matches **by coincidence of leverage 1.0**, ⛔ still not by identity. ⭐ **Report all of them, always.**

## §4 — STANDING RULES T-1 / T-2 / T-3

**T-1 · 🔴 "YES" MUST MEAN ATTRIBUTION, ⛔ NOT MERELY A NON-ZERO RESERVATION.** A generic non-zero `_positional_reserved` is ⛔ **NOT sufficient** — another position or order could be supplying it while the carried symbol sits unprotected. **Minimum evidence for a YES:** symbol · position state OPEN/HELD · authoritative reservation/commit attribution · value · timestamp · pipeline = DELIVERY. ⇒ If attribution cannot be established: **`CANNOT COMPUTE — POSITION ATTRIBUTION UNRESOLVED`. ⛔ Never YES.**

**T-2 · "FULL AUTHORITATIVE VALUE"** = the reservation the authoritative DELIVERY model gives for **that position at that state and timestamp**. ⛔ NOT market notional · ⛔ not broker cash · ⛔ not monitor `held` · ⛔ not an estimated margin · ⛔ **NOT today's incidental figures**. ⚠️ If tomorrow's authoritative reservation is a **different number** because the state legitimately differs, **THAT is the expected value.** ⛔ Do not anchor on today's.

**T-3 · ⛔ DO NOT INVENT A COMBINED ACCOUNTING FIELD.** Report the **actual** fields as the deployed model represents them: `20MICRONS · authoritative reservation = ₹X · reserved = ₹Y · used/committed = ₹Z · combined = ₹X`. ⭐ **The test is about ATTRIBUTION, ⛔ not about redesigning the accounting.**

⭐ **CHECK 1 STILL RUNS.** It answers *"does the arithmetic conserve?"*; CHECK 2a answers *"is the carried capital actually held?"* ⛔ **Different properties. ⛔ Do not drop CHECK 1 because 2a is stronger. Report both.**

## §5 — 🔴 U-3, RETAINED AS THE FALLBACK FORM (in case tomorrow's state differs)

If per-symbol attribution is ever unavailable, CHECK 2a's executable form becomes the **SUM IDENTITY**:
> **`Σ(authoritative reservation of EVERY open DELIVERY position)` == `_positional_reserved + _positional_used` ?**

⭐ With **ONE** open position — tonight's case — this is **EXACT and fully attributing**: the sum has one term, so a match **IS** attribution.
* ✅ **MATCHES** ⇒ CHECK 2a = YES. ⭐ State that attribution came from the **single-term sum**, ⛔ not a per-symbol field.
* 🔴 **SHORT BY ≈ the carried position's authoritative reservation** ⇒ **CASE 2 LIVE ⇒ STOP AND REPORT WITHIN MINUTES.** ⛔ Still no automatic revert.
* ⚠️ **SHORT BY SOME OTHER AMOUNT** ⇒ **NEEDS INVESTIGATION**, ⛔ not a verdict.

⚠️ **LIMITATION, recorded with the result:** with **more than one** open DELIVERY position on a future carry day, the sum still tests the invariant but ⛔ **cannot isolate WHICH** position is missing — except that a shortfall ≈ one position's reservation localises it.

⛔ U-3 is an **EXECUTABLE FORM of the same test** — ⛔ not a weaker one, ⛔ not a new design. If neither U-2 nor U-3 is possible: **`CANNOT COMPUTE` — name the exact missing field and its unit.**

## §6 — 🔴 THE REHYDRATE PRECONDITION · **CAPTURE TONIGHT**

`rehydrate_from_open_trades` replays **OPEN/PARTIAL** trades only (`:1788-1791`). ⇒ **If 20MICRONS' LOCAL `trades.status` is anything else at shutdown, it is ⛔ NEVER REPLAYED** — and CASE 2 would occur for a **completely different reason**: ⛔ not a rehydrate defect, but a **stale local status**.

⚠️ **This is not hypothetical — a ~10-minute broker/local observation lag was MEASURED today** (FILE 4B §B7-COROLLARY).

* **V-1** — tonight's `A_sameday BASELINE — LAST VALID PRE-SHUTDOWN READING` **must include, named: `20MICRONS` local `trades.status` at shutdown, verbatim.**
* **V-2** — ⚠️ If it is anything other than `OPEN` or `PARTIAL`, **flag IMMEDIATELY — before shutdown if possible.** ⛔ Do not change it. ⛔ Do not correct it. ⭐ It changes how tomorrow's result must be read.
* **V-3** — 🔴 **If CHECK 2a fails tomorrow, FIRST establish which of two causes applies, and report them SEPARATELY:**
  * **(a)** the trade **WAS** replayed and the reservation is still absent ⇒ **a rehydrate/accounting defect**
  * **(b)** the trade was ⛔ **NEVER** replayed because its status disqualified it ⇒ **a status/lag defect**
  ⛔ **Do not merge these. ⛔ Do not report one as the other.**


---

# FILE 4J — ALARM VERIFIED · AND 🔴 W-3 OVERTURNS FILE 4H's §1. Appended 26-Aug ~14:55 IST.

## §1 — THE ALARM · **VERIFIED, ⛔ NOT ASSERTED**

⭐ My previous *"Armed for 15:09"* was an **assertion**. Verified now by command, raw output quoted:

```
9662b0c4 — Every day at 3:09 PM (one-shot) [session-only]: /loop Continue the FILE 4B-4H EOD/CARRY…
```

✅ **ARMED.** Job `9662b0c4`, one-shot, **15:09**. ⚠️ **`[session-only]` — it dies if this session closes.** ⇒ §3's idempotent fallback matters, and is stated to Rama below.

## §2 — 🔴 W-3 ANSWERED FROM SOURCE · **IT OVERTURNS FILE 4H §1 AND W-6**

> **SUPERSEDED (FILE 4H §1, 26-Aug ~15:00):** *"⇒ ✅ **CHECK 2a is DIRECTLY EXECUTABLE per-symbol (U-2). ⛔ It does NOT need to fall back to U-3's sum identity.**"*
> **SUPERSEDED (FILE 4J W-6, as issued):** *"U-1 RESOLVED IN FAVOUR OF PER-SYMBOL (U-2). ⭐ Use the per-symbol route. ⛔ Do not run 4H's bucket-scalar sum identity merely because the file contains it."*

🔴 **BOTH ARE WRONG FOR A *COMMITTED* POSITION, and acting on either would have produced a FALSE CAUSE-A ALARM on the first carry night.**

**The deciding code — `_apply_commit`, `capital/fund_manager.py:2197-2210`:**
```python
2204|        """Pop reservation; deduct full reserved; add actual to used; excess
2205|        (if any) returns to avail."""
2206|        res = self._reservations.pop(reservation_id)          # <-- POPPED
2207|        self._bucket_deduct_reserved(res.bucket, res.margin)
2208|        self._bucket_add_used(res.bucket, actual_margin)
2209|        if excess != 0.0:
2210|            self._bucket_add_avail(res.bucket, excess)
```

🔬 **Corroborated:** `self._reservations[...]` is assigned at exactly **three** sites — `:756` (`release_slm_buffer` updating an existing entry), `:858` (public `reserve`), `:2177` (`_apply_reserve`). ⛔ **None re-adds after a COMMIT.** And `_bucket_add_used` targets `_positional_used` (`:2381`).

⇒ 🔴 **AFTER REHYDRATE REPLAYS `RESERVE → COMMIT` (`:2105`, `:2128`), THE `_Reservation` OBJECT FOR 20MICRONS IS *GONE*. `get_live_reservations()` WILL NOT CONTAIN IT.** The per-symbol registry holds only **reserved-but-not-yet-committed** entries. A **filled** position's margin lives **ONLY in the bucket scalar `_positional_used`.**

### ⇒ W-3's ANSWER — THE AUTHORITATIVE CURRENT HELD RESERVATION

> **For an OPEN, FILLED DELIVERY position after rehydrate, the authoritative CURRENT held reservation is its contribution to `_positional_used` — a BUCKET SCALAR. ⛔ There is NO single per-symbol in-memory field, because the reservation record is popped at COMMIT.**

⭐ **Per-position attribution is still recoverable — from the LEDGER, ⛔ not from memory:** the `fm_ledger` **COMMIT** row for that `reservation_id` carries the exact amount added to `_positional_used` (**454.48** for 20MICRONS, ledger_id `11485`). ⇒ attribution survives in a **table**, which also means it survives shutdown.

### ⇒ CHECK 2a's EXECUTABLE FORM IS **U-3 (SUM IDENTITY)** FOR A FILLED CARRY

> **`Σ(COMMIT amount of every open DELIVERY position)` == `_positional_used` ?** — plus `Σ(RESERVE-still-open)` == `_positional_reserved` for any unfilled entries.

⭐ With **ONE** open position — tonight's case — the sum has a single term, so **a match IS attribution to 20MICRONS**. ⛔ State that the attribution came from the single-term sum, ⛔ not from a per-symbol field.
⚠️ **U-2 remains correct only for a position still in RESERVED state (unfilled).** ⛔ Do not apply it to a committed one.

🔴 **WHY THIS MATTERED:** had CHECK 2a been run as W-6 instructed, `get_live_reservations()` would have returned **no 20MICRONS entry** for a perfectly healthy CASE 1 ⇒ **CHECK 2a = "NO / ABSENT" ⇒ a false "cause A, capital double-counted, STOP AND REPORT" on the first and only carry night.** ⭐ **This is precisely the failure W-3 was written to prevent: naming the wrong field answers a different question with confident-looking numbers.**

## §3 — PERISHABILITY, PRIORITY, AND THE IDEMPOTENT FALLBACK

**RECOVERABLE after the fact** (⭐ `fm_ledger` is a TABLE and survives shutdown): C1 baseline · C2 force-close + SOFT_KILL · C3 branch state · D's 17:35 gate decision and log lines · **DB5's `A_sameday BASELINE` via `fm_ledger.balance_after` on the last pre-shutdown positional row** · today's P&L and order census.
⚠️ **Anything reconstructed is labelled `RECONSTRUCTED FROM RECORD`, ⛔ NEVER `OBSERVED LIVE`.** ⭐ Added to the G0 vocabulary as a distinct evidence grade.

🔴 **GENUINELY PERISHABLE:**
* **P-A — D-C, the manual-stop check.** If the service still runs at 08:15, `token_watcher` reads *"running — nothing to do"* ⇒ **NO BOOT** ⇒ the carry test, resolver check, morning check and boot proof are **ALL forfeited at once.**
* **P-B — in-process state that never reaches a table.** 🔬 **Assessed: for CHECK 1 / 2a / 2b, NOTHING is memory-only.** `_positional_avail` = `fm_ledger.balance_after`; `_positional_used` = Σ COMMIT amounts; `_total`, `carry` and the snapshot fields are logged by `sync_from_broker` and `G3 MARGIN_RECON`. ⇒ **P-B is EMPTY for this test.** ⭐ The one field that is *not* derivable from the ledger is **20MICRONS' local `trades.status` at shutdown (V-1)** — but that is in `trades`, also a table.

⇒ **PRIORITY IF TIME IS SHORT: P-A first · DB5 baseline second · everything else reconstructable.**

**THE IDEMPOTENT FALLBACK (B2):** after ~17:45, if the service is still running, 👤 **Rama runs `sudo systemctl stop trading-system.service`.** ⛔ He runs it; ⛔ I never do. ⭐ **Safe in every branch:** a stop at 17:50+ ⛔ does **not** erase the 17:35 evidence — the self-exit either happened or it did not, and the log records it either way; if it already exited the command is a harmless no-op. ⛔ **No cron, no systemd timer, no VM-side scheduler will be created for this** — that is a system change and out of scope.

## §4 — W-1 … W-6 STANDING

**W-1 · FOUR DISTINCT NUMBERS, ⛔ never one word for all:**
```
trades.margin_reserved   = 455.14788   (reserve-time BASE, at the ENTRY TARGET price 2 x 227.57394)
fm_ledger RESERVE amount = 477.905274  (= 455.14788 x 1.05, base + slm buffer)
fm_ledger COMMIT amount  = 454.48      (at the FILL price -- THE CURRENT HELD FIGURE)
fill notional            = 454.48      (2 x 227.24)
monitor held             = 454.48
```
⚠️ **Three are numerically 454.48 and are ⛔ STILL NOT THE SAME QUANTITY.** ⭐ Report each with **its field name and source line**. ⛔ **Never write "authoritative reservation = ₹454.48" unqualified.**

**W-2 ·** 455.14788 = 2 × 227.57394 = the **TARGET** price. ⇒ *"reservation ≈ notional at leverage 1.0"* was **wrong**; it matched at the target price **by coincidence of that trade**. ⛔ Do not generalise.

**W-4 · ⛔ DO NOT USE MONITOR `held` AS AUTHORITATIVE PROOF.** Corroborating only — otherwise the same derived field becomes both premise and conclusion.

**W-5 · ⛔ THE 5% BUFFER IS AN OBSERVATION OF THIS RECORDED CHAIN, ⛔ not a new policy.** ⛔ No 5% rule, no new capital model, no tolerance, no reconciliation rule is to be built from it.

**W-6 · 🔴 CORRECTED ABOVE** — per-symbol (U-2) applies to a **reserved/unfilled** position; a **committed** one requires **U-3**.

## §5 — CHECK 2a MINIMUM YES EVIDENCE (restated, with the corrected route)

symbol = `20MICRONS` · pipeline = DELIVERY · position state = OPEN/HELD · `reservation_id` identifiable (`74dcc30b517549f1`) · **authoritative CURRENT reservation attribution via the `fm_ledger` COMMIT amount summing to `_positional_used`** · value reported · timestamp reported
⇒ all established ⇒ **CHECK 2a = YES**
⇒ fields exist but cannot be tied to 20MICRONS ⇒ **`CANNOT COMPUTE — POSITION ATTRIBUTION UNRESOLVED`**
🔴 ⛔ **A generic non-zero bucket value is NEVER a YES.**
⭐ **CHECK 1 still runs and is still reported.** `CHECK 1 = CONSERVES` with `CHECK 2a = NO` ⇒ conservation ⛔ does **NOT** rescue the result. **That is exactly why 2a exists.**
⭐ **V-1 stands:** 20MICRONS' local `trades.status` at shutdown, verbatim, in the baseline. If 2a fails: split **CAUSE A** (replayed, reservation absent ⇒ rehydrate/accounting) from **CAUSE B** (not OPEN/PARTIAL ⇒ never replayed ⇒ status/lag). ⛔ Do not merge. ⛔ **Do not change the status tonight to make a test pass.**

## §6 — ERRORS OWNED · RUNNING LIST

| # | error | status |
|---|---|---|
| 1 | **P9** — plausible mechanism for an unfinished measurement | 🔴 FAILED |
| 2 | **4D's equation** — no pipeline axis; notional ≠ reservation | 🔴 UNSAFE |
| 3 | **4E's equation** — insufficient alone | 🔴 INSUFFICIENT |
| 4 | **4F's CHECK 2** — delta-only, unnamed `_total`-drift confound | 🔴 CONFOUNDED |
| 5 | *"reservation ≈ notional at leverage 1.0"* | 🔴 WRONG — matched at the TARGET price |
| 6 | **4H §1's "CHECK 2a is directly executable per-symbol"** | 🔴 **WRONG for a COMMITTED position — `_apply_commit` pops the reservation. Would have produced a FALSE cause-A alarm.** |
| 7 | *"Armed for 15:09"* stated without verifying | 🔴 ASSERTION — now verified by command |


---

# FILE 4N — DEAD-WINDOW WORK. Appended 26-Aug ~15:50 IST. Market closed, book flat.

## §1 — CLASSIFICATION CORRECTIONS (X-1 … X-11)

| # | superseded wording | corrected label |
|---|---|---|
| **X-1** | *"P4 — branch: either branch 1 or branch 4's else-path"* | **OBSERVED LIVE — `GTT_EXIT`/`CLEANED`; exact internal branch NOT DISTINGUISHABLE from available evidence.** Rama's UI observation recorded SEPARATELY as broker-UI evidence, ⛔ not a proven code branch |
| **X-2** | *"lag ≈ 11 min 52 s"* | Four timestamps kept separate: **A** true broker close = ⛔ NOT DIRECTLY MEASURED · **B** first observed `broker_used` collapse `15:08:01.530` · **C** local finalisation `15:19:53.322` · **D** `RELEASE_USED` `15:19:53.319`. ⇒ **B→C = 11 m 51.8 s**, start = B. ⛔ B was never substituted for A |
| **X-3** | *"understated by ~447.91 … could a legitimate entry have been refused"* | *"Available capacity was temporarily lower while the phantom reservation existed; **0** `REJECTED_SIZING_CAPITAL` events observed in the window."* ⛔ The counterfactual was NOT tested. Arithmetic for the figure: `3163.89 − 2715.98 = 447.91` (post-release avail − during-phantom avail) |
| **X-4** | *"a ~10-minute local blindness window"* | **MEASURED CAPITAL OVER-RESERVATION WINDOW; ACCEPTABILITY IS A DESIGN DECISION.** ⛔ Not harmless, ⛔ not a defect |
| **X-5** | — | **CAUSE 3 — BROKER-USED LAG · CONTROLLED / BENIGN EXAMPLE · ⛔ NOT A REVERT CONDITION.** Arithmetic: `454.48 − 19.29 = 435.19`. Preserved as the reference non-revert case |
| **X-6** | — | **C3 PREDICTION NOT MATERIALISED — THE PRECONDITION DISAPPEARED.** Row finalised pre-shutdown; residual `−19.29` inside the ₹50 overnight band ⇒ no 20MICRONS drift alert expected. A clean prediction outcome, ⛔ not a failure |
| **X-9** | *"both CNC exits were TIER 1, real broker fills"* (FILE 4B §B5) | 🔴 **WITHDRAWN — inference presented as measurement.** Now settled by §3 at population scale |
| **X-10** | — | **P9 stays FAILED.** Carry design **PRESERVED · NOT EXERCISED**. ⛔ Because A1 occurred, the A2 phantom-rehydration experiment is ⛔ NOT to be run tomorrow |

### X-11 · ⭐ THE COMPLETE CAPITAL LIFECYCLE — first end-to-end CNC GTT exit ever measured
```
12:05:23.128  RESERVE       477.905274  positional  avail 3170.46 -> 2692.554726
12:05:26.834  COMMIT        454.48      positional  avail 2692.554726 -> 2715.98
   ~15:07:46  broker still holding      broker_used=468.35  residual=-13.87
   ~15:08:01  broker FLAT               broker_used= 19.29  residual=435.19   <- phantom begins
15:19:53.319  RELEASE_USED -454.48      positional  avail 2715.98 -> 3163.89
15:19:53.322  trades -> CLOSED / GTT_EXIT  exit_price 224.53  net_pnl -6.57  costs 1.15
15:19:53.326  cnc_gtt_monitor.gtt_exit     gtt_state -> CLEANED
15:20:09      G3 MARGIN_RECON  held=-0.00  residual=-19.29
```
⭐ `gross = net + costs = −6.57 + 1.15 = −5.42` — **matches the broker UI exactly.**

---

## §2 — FU-1 · 🔴 CHECK 1 WAS SKIPPED **BY DESIGN**. MY F11 CLAIM IS WITHDRAWN.

> **SUPERSEDED (26-Aug ~15:24):** *"§4 — CHECK 1 never fired, and its condition was met for 12 minutes … **Live F11-class observation** — a control whose condition was met and stayed silent."*

**F1a/F1e — the answer, `orders/order_reconciler.py:854-877`:**
```python
854|        # SLICE2.5-P2: delivery (CNC) trades with an ACTIVE overnight GTT are managed
855|        # by CncGttMonitor (holdings + GTT aware), NOT by the position/SL/exit checks
856|        # below — a carried CNC holding lives in holdings() not positions(), so CHECK1
857|        # would wrongly mark it CLOSED_MANUAL and G5b/CHECK9 would place a spurious SL.
860|            _delivery_rows = self._store.get_active_gtt_states()
863|        delivery_trade_ids = {r["trade_id"] for r in _delivery_rows}
875|            for trade in local_trades:
876|                if trade["trade_id"] in delivery_trade_ids:
877|                    continue  # SLICE2.5-P2: delivery trade -> CncGttMonitor owns it
882|                    # CHECK 1: MANUAL_CLOSE (RC5a)
883|                    actions.append(self._check1_manual_close(trade))
```

⇒ 20MICRONS held an **ACTIVE** `gtt_state` row until `15:19:53` ⇒ it was in `delivery_trade_ids` ⇒ **`continue` at `:877` — CHECK 1 never reached it.**

🔴 **VERDICT: `DESIGN PROPERTY`, ⛔ NOT an F11 gap.** CHECK 1 is deliberately scoped to exclude GTT-protected delivery rows; `CncGttMonitor` owns them, and it **did** handle this one at 15:19:53. **The system behaved correctly.** The ~12-minute window is the monitor's 15-min cadence, ⛔ not a silent control.

⭐ **AND THIS IS MY 9th OWNED ERROR — the same failure mode twice in one hour.** I inferred "CHECK 1 did not run" from `CHECK1 = 0` in the logs — **log absence** — which is *precisely* the non-vacuity trap I had correctly avoided minutes earlier for `get_trades`. ⛔ Not softened.

---

## §3 — FU-2 · 🔴 DEFECT B SETTLED AT POPULATION SCALE

**F2a · `_resolve_exit_price`, `orders/cnc_gtt_monitor.py:676-696`** — three tiers: `:685` real broker fill from `get_trades()` · `:693` **LTP via `get_quote()`** · `:696` `return float(entry_price or 0.0)`. Both fallbacks are silent (`except: pass`).

**F2d · SAMPLE SIZE: n = 28** CNC GTT exits with an `exit_price`.

### ⭐ INTERPRETATION FROZEN BEFORE THE QUERY RAN
* **TIER-1 broker fill** ⇒ should cluster **AT or very near a trigger** — a GTT fires and executes at/near its trigger.
* **TIER-2 LTP snapshot** taken at monitor-pass time ⇒ deviation **SCATTERED**, and **GROWING WITH THE LAG**.

### F2b · THE RESULT
```
exactly_at_trigger (dev < 0.005) :  0
strictly_between the two triggers: 19
n                                : 28
```
🔴 **NOT ONE of 28 sits at a trigger. 19 of 28 sit strictly BETWEEN the two trigger levels** — a price that is neither the SL nor the TGT.

### F2c · THE LAG CORRELATION — PRESENT, AND IT IS THE DECISIVE PART
| rows | finalisation | deviation from nearest trigger |
|---|---|---|
| DIFFNKG ×3, ATULAUTO ×4, UTTAMSUGAR, MANINFRA | **`08:15` / `08:16` — boot-time, overnight lag** | **41.65 · 3.90 · 1.61 · 0.72** |
| KRONOX, ASKAUTOLTD ×2, FMGOETZE, THEMISMED, BALUFORGE | **minutes after the fire** | **0.03 · 0.10 · 0.15 · 0.15 · 0.25 · 0.40** |

⇒ ⭐ **The largest deviations are the overnight-lag rows; the smallest are the minutes-lag rows. Exactly the predicted positive relationship.**
🔬 **9 of 28 (32%) were finalised at boot time** (`08:15` ×5, `08:16` ×4) — i.e. the morning *after* the position actually closed.

### 🔴 THE TWO SMOKING GUNS
* **ATULAUTO ×4** — four rows sharing **one price `579.55`** at **one timestamp `08:15:41`**. Four separate broker fills cannot share both. ⇒ **one LTP snapshot applied four times.**
* **DIFFNKG ×3** — `exit_price 395.55` is **BELOW `sl_trigger 437.20` by 41.65 (9.5%)**. ⛔ A SL GTT firing at 437.20 cannot fill at 395.55. It is the next morning's LTP.

⇒ 🔴 **VERDICT: `trades.exit_price` for CNC GTT exits is NOT a broker fill price. DEFECT B's silent TIER-2 fallback is the NORMAL path, ⛔ not an exceptional one.** This is now a distributional result over the whole population, ⛔ no longer an inference from one observation.

### F2e · MAGNITUDE
Σ|deviation × qty| across the 28 ≈ **₹191**. Worst: **DIFFNKG ×3 at ₹41.65 each against a recorded `net_pnl` of −51.63** ⇒ the deviation is **~81% of the recorded P&L** on those rows.
⚠️ **Labelled as a MAGNITUDE PROXY, ⛔ not the exact P&L error** — the true fill need not be exactly at the trigger either (slippage, limit offset). ⭐ It bounds the scale, and the scale is material against typical per-trade P&L of ±₹10–15.

### F2f · 🔴 THE CONTRACT — **THERE ISN'T ONE, AND THAT IS THE FINDING**
* `core/schema.sql:145` — bare `exit_price REAL,`. ⛔ No comment, no contract. (`:753` on another table says only `-- nullable until closed`.)
* 🔴 **AND THERE IS NOTHING TO VALIDATE IT AGAINST:**
```
orders: total 1205 | avg_fill_price NOT NULL: 0 | price NOT NULL: 591
exit legs: SL 288 · TGT 276 · EOD 27  ->  avg_fill_price NULL on ALL
```
⇒ **`orders.avg_fill_price` is NULL on all 1,205 orders**, including every one of the 591 exit legs. **No stored fill price exists anywhere in the database.** That is why the MIS contrast query returned zero rows — the comparison is impossible for **both** pipelines.

> ⚠️ **10th OWNED CORRECTION:** my §I wording — *"the limit price is not persisted for ANY order"* — **over-generalised from today's six rows.** Measured population-wide, `orders.price` **IS** populated on **591 of 1,205**. The field that is universally absent is **`avg_fill_price`**, ⛔ not `price`.

⇒ ⭐ **DAY 3's "F4 observability + DEFECT B provenance marker" is no longer an edge-case fix — it is the unit that makes every CNC exit price interpretable at all.** Flagged forward, ⛔ not acted on tonight.

---

## §4 — REMAINING LABELS

| item | label |
|---|---|
| **X-7** CHECK 1 condition met ~12 min | **OBSERVED LIVE** |
| **X-7** CHECK 1 fired | **NO — BY DESIGN** (`:877`) |
| **X-7** F11 classification | 🔴 **WITHDRAWN — DESIGN PROPERTY** |
| **X-8** F5 provenance — 3 consecutive CNC exits with EMPTY `closure_source`/`exit_mechanism` | **OBSERVED LIVE / REPEATED.** ⛔ Not yet a defect. Narrow open question: *is the absence intentional for `GTT_EXIT`, or is provenance expected to be persisted?* |
| **A1/A2** | **A1 — FINALISED.** Book truly flat ⇒ 17:35 is the TRIVIAL case |
| Carry design | **PRESERVED · NOT EXERCISED** — OWED-2 · carry CHECK 1 · CHECK 2a · CHECK 2b · 4-reading series · three-cause discriminator as a full test · G3 T+1 · F6-leg T+1 · A_sameday baseline · genuine overnight rehydration |


---

# FILE 4P — FU-2 EVIDENCE COMPLETION. Appended 26-Aug ~16:30 IST.

## §0 — 🔴 11th OWNED ERROR: A JOIN FAN-OUT INFLATED MY OWN HEADLINE

> **SUPERSEDED (FILE 4N §3, 26-Aug ~15:50):** *"n = 28"*, *"ATULAUTO ×4 share ONE price `579.55` at ONE timestamp `08:15:41` — four separate broker fills cannot share both ⇒ one LTP snapshot applied four times"*, *"DIFFNKG ×3"*, and *"Σ ≈ ₹191"*.

🔬 `trades JOIN gtt_state ON trade_id` **fans out**: ATULAUTO has **4** `gtt_state` rows, DIFFNKG has **3** — for **ONE trade each**. `4−1 + 3−1 = 5`, and `28 − 5 = 23`. ✅ Exactly reconciles.

⇒ 🔴 **"ATULAUTO ×4 sharing one price and timestamp" is WITHDRAWN — it was the same row repeated by the join, ⛔ not four fills.** ⭐ Caught only because **P-1's independent `COUNT(*) FROM trades` (23) disagreed with the joined count (28)** — which is exactly why the proportionality check was worth running. ⛔ Not softened.

## §1 — WORDING APPLIED (Y-1 … Y-4)

**Y-1** ⇒ **"DEFECT B IS STRONGLY ESTABLISHED BEHAVIOURALLY AT POPULATION SCALE; exact source attribution remains to be confirmed against the per-row data and the contract."** ⛔ Never *"settled / proven conclusively"*.
**Y-2** ⇒ **"CHECK 1 did not fire because the row was intentionally excluded by the ACTIVE-GTT ownership boundary (`order_reconciler.py:876-877`); `CncGttMonitor` was the owning control." ⇒ PROVEN DESIGN PROPERTY.** ⛔ CHECK 1 is not reopened as a bug.
**Y-3** — five distinctions kept intact throughout: strong behavioural evidence ≠ direct broker-fill proof · zero-at-trigger ≠ proof by itself · boot-time clustering ≠ numeric correlation · absent `avg_fill_price` ≠ proof `exit_price` is wrong · the ₹ figure ≠ actual broker P&L error.
**Y-4** ⇒ **"There is no independently stored authoritative fill-price field against which `exit_price` can be validated."** — an **OBSERVABILITY / PROVENANCE failure**, ⛔ not *"the price is wrong"*.

## §2 — Z-1 · THE FULL TABLE, DEDUPLICATED · **n = 23 DISTINCT TRADES**

| symbol | qty | exit_px | sl_trig | tgt_trig | dev from nearest | finalised |
|---|---|---|---|---|---|---|
| DIFFNKG | 1 | 395.55 | 437.20 | 459.45 | **41.65** | 2026-08-11T08:16 |
| SHANTIGOLD | 2 | 266.40 | 259.42 | 272.65 | 6.25 | 2026-08-17T15:20 |
| MMFL | 1 | 684.20 | 656.35 | 689.85 | 5.65 | 2026-08-18T14:49 |
| SOLARA | 1 | 605.40 | 580.50 | 610.10 | 4.70 | 2026-08-20T10:30 |
| ATULAUTO | 1 | 579.55 | 575.65 | 605.00 | 3.90 | 2026-08-07T08:15 |
| MANINDS | 1 | 711.90 | 708.45 | 744.60 | 3.45 | 2026-08-21T15:20 |
| CLSEL | 1 | 287.30 | 284.15 | 298.60 | 3.15 | 2026-08-21T15:20 |
| EPL | 2 | 266.55 | 255.76 | 268.81 | 2.26 | 2026-08-20T14:03 |
| EPL | 2 | 249.74 | 251.38 | 264.21 | 1.64 | 2026-08-12T10:30 |
| UTTAMSUGAR | 1 | 290.32 | 288.71 | 303.44 | 1.61 | 2026-08-19T08:15 |
| 20MICRONS | 2 | 224.53 | 223.02 | 233.57 | 1.51 | 2026-08-26T15:19 |
| KAMATHOTEL | 2 | 228.14 | 216.15 | 227.18 | 0.96 | 2026-08-24T11:31 |
| RATNAVEER | 2 | 245.60 | 234.41 | 246.36 | 0.76 | 2026-08-17T15:20 |
| MANINDS | 1 | 612.10 | 612.85 | 644.10 | 0.75 | 2026-08-12T10:15 |
| MANINFRA | 4 | 113.64 | 112.92 | 118.69 | 0.72 | 2026-08-11T08:16 |
| BALUFORGE | 1 | 628.40 | 598.20 | 628.80 | 0.40 | 2026-08-24T12:47 |
| MANINDS | 1 | 674.45 | 674.80 | 709.20 | 0.35 | 2026-08-20T14:49 |
| THEMISMED | 4 | 131.24 | 125.12 | 131.49 | 0.25 | 2026-08-26T10:30 |
| ASKAUTOLTD | 1 | 596.35 | 567.20 | 596.20 | 0.15 | 2026-08-05T10:45 |
| FMGOETZE | 1 | 561.75 | 561.60 | 590.25 | 0.15 | 2026-08-26T11:31 |
| ASKAUTOLTD | 1 | 676.20 | 643.45 | 676.30 | 0.10 | 2026-08-06T10:47 |
| KRONOX | 2 | 174.00 | 174.09 | 182.96 | 0.09 | 2026-08-12T10:30 |
| KRONOX | 2 | 211.58 | 201.33 | 211.61 | 0.03 | 2026-08-21T14:04 |

```
n_distinct_trades = 23 · exactly_at_trigger = 0 · strictly_between = 16
```
⭐ **The surviving smoking gun: DIFFNKG — ONE real trade, `exit_price 395.55` vs `sl_trigger 437.20` = 41.65 BELOW (9.5%). ⛔ A SL GTT firing at 437.20 cannot fill at 395.55.**

## §3 — Z-2 · GTT FIRE TIMESTAMP · **NOT PERSISTED**
`gtt_state` columns: `gtt_id · trade_id · symbol · exit_side · qty · sl_trigger · sl_limit · tgt_trigger · tgt_limit · status · needs_review · last_verified_at · created_at · updated_at`.
⛔ **No trigger/fire/execution time column exists** (`sl_trigger`/`tgt_trigger` are PRICES). ⇒ **"GTT fire timestamp is not persisted/recoverable; fire→finalisation lag cannot be reconstructed." F2c = `PARTIALLY MEASURED`.** ⛔ No proxy lag was manufactured. ⭐ The absence is itself a provenance finding, in the same family as the missing `avg_fill_price` and the missing contract.

## §4 — Z-3 · 🔴 THE DEPENDENCY IS CONFIRMED · `net_pnl` DERIVES FROM `exit_price`
```
cnc_gtt_monitor.py:548   exit_price = self._resolve_exit_price(symbol, exit_side, entry_price)
                  :560   charges = round_trip_costs_or_zero(..., exit_price=float(exit_price), ...)
                  :567   rr = self._fm.release_used(exit_price=float(exit_price), ...)
                  :572   pnl = float(rr.pnl_delta)
                  :576   record_gtt_close_financials(exit_price=..., net_pnl=pnl,
                  :577                               gross_pnl=pnl + charges, charges=charges)
fund_manager.py:1220     "exit_price:  price at which position was closed"
               :1223     "entry_price: original entry price (for PnL calculation)"
```
⇒ 🔴 **A tier-2 LTP snapshot propagates directly into `net_pnl`, `gross_pnl`, `pnl_delta`, `daily_realized_pnl`, bucket `avail` and `_total`.** ⇒ ⭐ the higher-value framing is confirmed: **this contaminates the metrics the DELIVERY pipeline is judged on**, ⛔ not merely a display field.

**Per-trade estimated delta (deduplicated), TOTAL = ₹96.89 across 23 trades.** ⚠️ Labelled **"estimated trigger-vs-recorded-price P&L delta"**, ⛔ **NEVER "actual broker P&L error"** — the true fill need not sit exactly at a trigger either.
⚠️ **Corrected from ₹191.89** — that figure was fan-out-inflated.

## §5 — Z-4 · THE CONTRACT · **ABSENT / UNSPECIFIED**
* `core/schema.sql:145` — bare `exit_price REAL,`. ⛔ No comment.
* `docs/04_db_schema_reference.md:124` — bare `exit_price REAL`, while the adjacent `:125` **does** document `exit_reason TEXT  -- SL_HIT/TGT_HIT/EOD/MANUAL`. ⇒ ⭐ **the neighbouring field carries semantics and this one does not.**
⇒ **EXIT_PRICE CONTRACT = ABSENT / UNSPECIFIED.** ⭐ The absence is the finding.

## §6 — 🔴 T-1 · THE PRIOR-CLOSE TEST · **INCONCLUSIVE — THE PREDICTION DID NOT HOLD**

⭐ Frozen interpretation, restated: *equal to prior-day close ⇒ LTP origin PROVEN; not equal ⇒ the tier-2 inference WEAKENS.*

| symbol | prior day | candles | last close | recorded exit_px | match |
|---|---|---|---|---|---|
| ATULAUTO | 2026-08-06 | **0** | NONE | 579.55 | — |
| MANINFRA | 2026-08-08 | **0** | NONE | 113.64 | — |
| DIFFNKG | 2026-08-08 | **0** | NONE | 395.55 | — |
| UTTAMSUGAR | 2026-08-18 | 374 | **290.00** | **290.32** | 🔴 **NO** |

⇒ 🔴 **3 of 4 have no prior-day candle coverage; the ONE testable row MISMATCHES by 0.32. T-1 did NOT confirm the LTP-snapshot origin, and it is recorded as a prediction that did not hold.**
💭 **INFERENCE, labelled and ⛔ NOT used as a rescue:** the candle store is tick-built (`data/candle_store.py`), so its last 1-min close is the last tick **the system captured**, which need not equal the official exchange close. ⇒ **T-1 = `INCONCLUSIVE` — it neither proves nor refutes.** ⛔ It is not counted as support.

## §7 — 🔴 T-2 · THE MIS CONTROL GROUP · **ISOLATES THE CNC GTT PATH**

⭐ Frozen interpretation, restated: *MIS near zero + CNC scattered ⇒ isolates the CNC path; MIS scattered too ⇒ system-wide, and DAY 3's scope changes.*

| population | n (distinct) | exactly at the order price | avg dev | max dev |
|---|---|---|---|---|
| **MIS `TGT_HIT`** | 90 | **49 (54%)** | 0.2723 | 9.6223 |
| **MIS `SL_HIT`** | 137 | **15 (11%)** | 0.2924 | 2.672 |
| **CNC `GTT_EXIT`** | 23 | **0 (0%)** | ~4.2 | 41.65 |

🔬 **Fan-out re-checked on T-2 as well:** SL_HIT 137 distinct vs 138 joined · TGT_HIT 90 vs 90 ⇒ **essentially unaffected; the control stands.**

⇒ 🔴 **RESULT: MIS exit prices bear a tight relationship to their exit-order prices — over half of TGT exits land EXACTLY on the order price. CNC exit prices match a trigger ZERO times out of 23.** ⇒ ⭐ **the difference ISOLATES THE CNC GTT PATH. DAY 3's scope stays NARROW — this is ⛔ not system-wide.**
⚠️ **Caveat, stated:** for MIS `TGT_HIT`, an exact match could also arise if the system records the TGT limit price rather than the fill. ⭐ 41 of 90 do **not** match exactly, so it is ⛔ not a blind copy — but this is ⛔ not proof of a real fill either.

## §8 — P-1 · PROPORTIONALITY · ⭐ KEEPING PRIORITY HONEST
```
all trades 762 · filled 302 · CNC GTT exits 23 · MIS-style exits 279
```
⇒ **CNC GTT exits are 23 of 302 filled trades = 7.6%.**
**P-2 — what IS and IS NOT affected:** the **DELIVERY pipeline's per-trade P&L is implicated** (Z-3's dependency is confirmed). Overall win rate and expectancy are **dominated by MIS**, and per **T-2 the MIS path is NOT similarly affected** ⇒ ⭐ **the headline metrics are not invalidated.**
**P-3 — F6e dependency:** F6e's exit work rests on measured MFE and R multiples. ⭐ **If those derive from `exit_price`, F6e's DELIVERY-side inputs inherit this.** ⛔ Dependency reported only; ⛔ not acted on.

## §9 — DAY 3 · THE SHAPE, RECORDED AND STOPPED
The minimum useful fix answers six questions, ⛔ nothing more: what price the broker actually returned · what price triggered the GTT · what fallback the monitor used · which is stored in `trades.exit_price` · which is used for P&L · what provenance was used.
⭐ Conceptually one compact field — `exit_price_source ∈ {BROKER_FILL, GTT_TRIGGER, LTP_FALLBACK, EOD, MANUAL}`.
⛔ **NOT implemented. ⛔ NOT designed. Shape recorded against DAY 3 and stopped.**


---

# FILE 4Q — THE LAST SMOKING GUN TESTED. Appended 26-Aug ~17:05 IST.

## §1 — WORDING CORRECTIONS (W-1 … W-11)

**W-1 · 🔴 MY OWN T-1 FROZEN RULE WAS TOO STRONG.**
> **SUPERSEDED (FILE 4P §6):** *"IF each boot-time `exit_price` EQUALS that symbol's prior-day close ⇒ LTP-snapshot origin is PROVEN."*
> ✅ **CORRECTED:** *"T-1 can **CORROBORATE** an LTP-snapshot hypothesis when a boot-time exit equals an internally recorded prior/latest quote, ⛔ but price equality alone cannot PROVE provenance, because a broker fill can coincidentally occur at the same price."*

**W-2 · T-1 = `INCONCLUSIVE / NO CORROBORATION`**, ⛔ **not "FAILED"** in the sense of disproving the hypothesis. Two reasons, recorded separately: **(a)** 3 of 4 symbols have no usable internal prior-day candle; **(b)** the one available comparison does not match exactly (290.00 vs 290.32). ⇒ Strongest defensible form: *"T-1 did not provide corroborating prior-close evidence; ⛔ it does not refute the LTP hypothesis."* ⚠️ Tick-built-candle caveat retained — 290.00 vs 290.32 is ⛔ not a clean official-close test.

**W-3 · T-2 = STRONGLY SUPPORTIVE OF CNC-PATH SPECIFICITY** — ⛔ not "proves the issue is exclusively CNC", ⛔ not direct broker-fill proof.
**W-4 · Z-2 = PROVEN ABSENCE** of a persisted GTT fire timestamp. **F2c = `PARTIALLY MEASURED`.** ⛔ No proxy manufactured.
**W-5 · Z-3 = PROVEN DEPENDENCY** — *"The observed CNC exit-price behaviour is capable of propagating directly into recorded per-trade P&L, because `net_pnl` derives from `exit_price`."* **Always attached:** *"The exact broker-fill correctness of `exit_price` remains UNRESOLVED because no authoritative persisted fill-price or provenance contract exists."*
**W-6 · Z-4 = PROVEN CONTRACT ABSENCE** — *"Because the contract is absent, the database cannot independently communicate whether `exit_price` represents a broker fill, a GTT trigger, a monitor-time LTP fallback, EOD, or a manual exit."* ⚠️ Sharpened by the neighbour: `docs/04_db_schema_reference.md:125` documents `exit_reason` semantics while `:124` leaves `exit_price` bare.
**W-7 · ₹96.89 = "estimated trigger-vs-recorded-price P&L delta"** — a **SENSITIVITY estimate**. ⛔ NEVER "actual broker P&L error". The **₹191.89 → ₹96.89** fan-out correction stays prominent.
**W-8 · PROPORTIONALITY — explicit denominator: 23 / 302 = 7.62% of FILLED trades in the measured population.** ⛔ Not "of all trading activity". ⭐ Fair form: *"a minority of filled trades — significant but ⛔ not system-wide on current evidence."* ⚠️ MIS-dominance of win rate/expectancy is a **PROPORTIONALITY OBSERVATION**, ⛔ not proof those metrics are unaffected.
**W-9 · F6e = see §5.**
**W-10 · 🔴 PERMANENT QUERY-DISCIPLINE RULE:** *"Population queries involving `gtt_state` MUST deduplicate at trade identity before any distributional claim."* ⭐ Error 11 stays recorded unmodified — it demonstrates exactly why an independent population count is required, and it was caught **only** because P-1's count disagreed with the joined one.
**W-11 · The 23-row table is the EVIDENCE ASSET; the summary is only interpretation.** ⛔ Never let a summary replace it.

## §2 — Z-1 CANONICAL TABLE · VERIFIED PRESENT
The full 23-row table is stored in this record (FILE 4P §2) with symbol · qty · exit_px · sl_trigger · tgt_trigger · deviation · finalisation time. **GTT fire time is blank WITH its explicit reason: Z-2 proved no such column exists.** Sample of 3 rows, quoted:
```
DIFFNKG     1  395.55  sl 437.20  tgt 459.45  dev 41.65  finalised 2026-08-11T08:16
20MICRONS   2  224.53  sl 223.02  tgt 233.57  dev  1.51  finalised 2026-08-26T15:19
KRONOX      2  211.58  sl 201.33  tgt 211.61  dev  0.03  finalised 2026-08-21T14:04
```

## §3 — 🔴 R-1 + R-2 · THE DISTRIBUTION TEST · **THE CLAIM HOLDS WITHOUT DIFFNKG**

### R-1 · Per-leg split
⚠️ **`exit_reason` cannot split them — all 23 are `GTT_EXIT`.** ⇒ split by **nearest-trigger assignment**, method labelled. ⭐ This biases **CONSERVATIVELY** (assigning to the nearer trigger *minimises* the measured deviation, i.e. against the finding).

| population | n | exact matches | avg dev |
|---|---|---|---|
| CNC nearer-**TGT** | 11 | **0 (0%)** | 1.955 |
| CNC nearer-**SL** | 12 | **0 (0%)** | 4.914 |
| **MIS `TGT_HIT`** | 90 | **49 (54%)** | 0.272 |
| **MIS `SL_HIT`** | 137 | **15 (11%)** | 0.292 |

⭐ **R-1's expected asymmetry is confirmed on the MIS side** — TGT is limit-like (fills at the limit or better ⇒ exact matches natural, 54%); SL converts on trigger and fills at whatever is available (⇒ exact matches unlikely, 11%). ⭐ **That asymmetry is order-type behaviour, ⛔ not a defect.**
⇒ 🔴 **LIKE-FOR-LIKE: CNC-TGT 0/11 exact against MIS-TGT 49/90 (54%).** ⚠️ n=11 is small and the split is heuristic — labelled.

### R-2 · Full distributions — ⭐ FROZEN INTERPRETATION RESTATED BEFORE THE NUMBERS
> *IF the CNC MEDIAN is materially larger than the MIS medians ⇒ "scattered" HOLDS on the whole population. IF the CNC median is comparable and only DIFFNKG is extreme ⇒ the claim rests on ONE ROW and must be restated that way.*

| population | n | min | p25 | **MEDIAN** | p75 | max |
|---|---|---|---|---|---|---|
| **CNC `GTT_EXIT`** | 23 | 0.03 | 0.25 | **0.96** | 3.45 | 41.65 |
| **CNC excl. DIFFNKG** | 22 | 0.03 | 0.25 | **0.86** | ~3.30 | **6.25** |
| MIS `TGT_HIT` | 90 | 0.0 | 0.002 | **0.004** | 0.019 | 9.622 |
| MIS `SL_HIT` | 137 | 0.0 | 0.026 | **0.14** | 0.358 | 2.672 |

⇒ 🔴 **RESULT: THE "SCATTERED" CLAIM HOLDS ON THE WHOLE POPULATION.**
* CNC median **0.96** vs MIS-TGT **0.004** — **~240×**
* CNC median **0.96** vs MIS-SL **0.14** — **~7×**
* ⭐ **Removing DIFFNKG moves the CNC median only 0.96 → 0.86, and the max from 41.65 → 6.25.** ⇒ **the claim does NOT rest on one row.**

## §4 — 🔴 DIFFNKG · THE GAP-DOWN ALTERNATIVE · **CANNOT COMPUTE ⇒ WITHDRAWN AS LOAD-BEARING**

**D-1 · Fire day DERIVED (⛔ not measured — Z-2 proved no fire timestamp exists):**
```
entry            2026-08-06T10:03:16  @ 446.10  qty 1
gtt 330658430    created 08-06T10:03:16  status TRIGGERED  last_verified 08-07T14:50:07
gtt 330940420    created 08-07T15:05:26  status TRIGGERED
gtt 330944932    created 08-07T15:20:35  status CLEANED    updated 08-11T08:16:06
trade finalised  2026-08-11T08:16:06  exit_price 395.55
```
⇒ **DERIVED FIRE DAY = 2026-08-07** (first GTT went TRIGGERED; `SYSTEM_MAP.md:52` independently records a DIFFNKG SELL `260807170745584` COMPLETE at 14:50:52 that day — **RECONSTRUCTED FROM RECORD**).

**D-2 · Candle coverage — 🔴 THE FIRE DAY HAS NONE:**
```
2026-08-03  lo 385.10  hi 410.00      2026-08-11  lo 370.00  hi 412.95
2026-08-04  lo 408.25  hi 431.00      2026-08-12  lo 356.75  hi 385.00
2026-08-06  lo 422.05  hi 453.70      2026-08-13  lo 362.70  hi 399.55
   ** 2026-08-07, 08, 09, 10 — ZERO CANDLES **
```
**And the direct test is also unavailable:** the 07-Aug SELL order `260807170745584` is **NOT in the `orders` table** — only the ENTRY row exists for DIFFNKG. ⇒ no fill price is recoverable from any internal source.

**D-3 · VERDICT: `CANNOT COMPUTE`. ⛔ No side picked.**
⚠️ **AND THE GAP EXPLANATION HAS REAL SUPPORT AND CANNOT BE EXCLUDED:** 06-Aug ranged **422.05–453.70**; 11-Aug ranged **370.00–412.95**. The stock fell hard across the unobserved window. **A SL at 437.20 firing on 07-Aug during that decline could ordinarily fill well below its trigger.** ⭐ That is normal stop behaviour.

⇒ 🔴 **DIFFNKG IS WITHDRAWN AS A LOAD-BEARING SMOKING GUN** — ⛔ **not disproved**, but an ordinary explanation cannot be excluded and it was the sole load-bearing row.

**D-4 · ⭐ AND IT DOES NOT MATTER, BECAUSE §3 ALREADY SETTLED IT.** With DIFFNKG removed the CNC median is still **0.86** vs MIS-TGT **0.004**, and CNC-TGT is still **0/11 exact** vs MIS-TGT **49/90**. **DEFECT B is NOT refuted; it now rests on the population statistics, the MIS control, the proven `exit_price → net_pnl` dependency, and the absent contract — ⛔ no longer on any single row.** ⭐ **That is a stronger position than before, not a weaker one.**

## §5 — F6e DEPENDENCY = **PARTIALLY TRACED**
🔬 `compute_trade_excursions` (`core/state_store.py:2079-2091`) selects `symbol, direction, entry_actual_price, entry_time, exit_time` and uses `_parse_ist_dt(trade["exit_time"])` — i.e. **`exit_time` BOUNDS the excursion window; `exit_price` is ⛔ NOT consumed as a value.** ⇒ **MFE appears INSULATED from `exit_price`.**
⛔ **The R-multiple was NOT traced.** ⇒ **F6e DEPENDENCY = PARTIALLY TRACED.** ⛔ F6e is neither declared invalid nor declared safe.

## §6 — DAY 3 REQUIREMENT · RECORDED, ⛔ NOT BUILT
The six questions stand. Conceptual label values: `BROKER_FILL · GTT_TRIGGER · LTP_FALLBACK · EOD · MANUAL`.
🔴 ⭐ **ADDED REQUIREMENT — because a label alone becomes another opaque field:** the implementation must **preserve the RAW SOURCE VALUES that justify the label** — selected exit price · source · broker fill price if available · GTT trigger if applicable · fallback LTP if used · **the timestamp of the source observation**.
⛔ **NOT designed. ⛔ NOT implemented. Recorded against DAY 3 and stopped.**


---

# FILE 7 — CARRY PROTOCOL + 🔴 A COST-MODEL GAP. Appended 26-Aug ~16:50 IST.

## §0 — C2 (owed from FILE 4B) · THE 15:15 FORCE-CLOSE, VERBATIM · **P1 HOLDS**
```
15:15:01.600 WARNING  order_monitor  order_monitor.force_close_triggered  force_close_time:"15:15"  watched_count:0
15:15:01.600 CRITICAL main          circuit_breaker.force_close_triggered: soft_kill, EOD squareoff handles positions
15:15:01.603 CRITICAL main          KillSwitchActivated: INACTIVE -> SOFT_KILL reason=circuit_breaker_force_close_15:15
15:15:01.603 CRITICAL kill_switch   SOFT_KILL ACTIVATED reason=circuit_breaker_force_close_15:15 triggered_by=order_monitor
15:15:02.301 telegram  [LIVE] SOFT KILL — scheduled (circuit_breaker_force_cl…)
15:15:02.981 telegram  [LIVE] CIRCUIT BREAKER — Force Close
```
⭐ **P1 = HELD.** ⚠️ `watched_count: 0` — nothing to close; the book was already flat.

## §1 — 🔴 R-1 · THE PAPER-CARRY ROUTE IS **RULED OUT**, AND IT WAS ALREADY SETTLED ON 26-JUL

**(a) Is a paper instance running?** ⛔ **NO.** ONE unit — `trading-system.service`, described *"Trading System v2 (paper/live mode)"* — running `--mode live`. `ps` shows **no** `--mode paper` process. `crontab -l | grep -ci paper` = **0**. ⇒ a paper carry would require **starting a second process or switching the live one** — a system change, ⛔ not free.

**(b)/(c) Does the paper book survive a restart?** 🔴 **NO — and the source says so itself.** `orders/cnc_gtt_monitor.py:30-35`:
> *"⚠️ ONE THING PAPER CANNOT DO, AND IT SAYS SO (26-Jul-2026): the paper stores are **in-memory and die with the nightly restart** while `gtt_state` survives, so the morning after a paper carry this routine **emits a clean GTT_EXIT for a position that was never held**. … **The carry is a live-only proof**; see `docs/audit/paper_overnight_carry_26jul2026.md`."*

**The dedicated audit exists and leads with it:**
> *"⚠️ **SLICE 2.5's PAPER GATE CANNOT COVER THE OVERNIGHT CARRY, AND THE OVERNIGHT CARRY IS WHAT DELIVERY *IS*.** Every intraday property of a CNC trade is rehearsable in paper. The one property that distinguishes delivery from intraday — that the position, its broker-side OCO GTT, and the capital reserved against it all survive a night and a process restart — is …"*

⇒ 🔴 **R-1 VERDICT: RULED OUT. ⛔ This is NOT a new finding — it was investigated and documented on 26-Jul-2026.** ⭐ A paper carry would produce a **false clean `GTT_EXIT`** for a position that never existed, i.e. it would **manufacture the very artefact** the test is meant to detect.

⇒ ⭐ **REMAINING ROUTES: R-3 (opportunistic, free) and R-2 (one deliberate real carry, priced in advance — 👤 Rama's call).** ⛔ R-1 is closed.

## §2 — 🔴 THE COST MODEL · THE HYPOTHESIS IS REFUTED, AND SOMETHING SHARPER IS UNDERNEATH

**C-1 — `broker_costs.yaml` EXISTS at `75e637c` and prices CNC EXPLICITLY.** ⇒ 🔴 **the pending-items note that it "was never explicitly defined and the system falls back to hardcoded rates" is REFUTED at this SHA.**
```yaml
brokerage_flat_intraday: 20.0   # Flat Rs20 cap per executed order (MIS/CO/CNC SELL)
brokerage_pct_intraday: 0.03    # 0.03% of turnover (MIS/CO/CNC SELL); capped at flat (CC3)
stt_sell_pct:  0.025            # MIS/CO intraday, sell side only          (CC4)
stt_cnc_pct:   0.1              # CNC BOTH SIDES                            (CC4)
stamp_duty_mis_buy_pct: 0.003   # MIS/CO buy side                           (CC8)
stamp_duty_cnc_buy_pct: 0.015   # CNC buy side                              (CC8)
```
`broker/cost_calculator.py` branches on product at `:147-148`, `:169-174` (**CNC BUY → 0 brokerage**), `:190-197` (**CNC both sides at `stt_cnc_pct`**), CC8 (**CNC BUY stamp duty**).

**C-4 — CROSS-CHECK, and it reconciles.** Model for 20MICRONS (2 @ 227.24 → 224.53): brokerage `min(20, 0.03%×449.06)=0.13` + STT `0.1%×454.48 + 0.1%×449.06 = 0.90` + exch `0.00297%×903.54 = 0.03` + stamp `0.015%×454.48 = 0.07` + GST `18%×0.16 = 0.03` ≈ **₹1.16**. **Recorded charge: ₹1.15.** ✅ ⇒ **the CNC (delivery) rate WAS applied, ⛔ not the intraday rate** — a pure-MIS computation would give ≈ ₹0.29.

### 🔴 C-2 — **THE GAP: THERE IS NO DP / DEMAT DEBIT CHARGE**
`CostBreakdown` has exactly **six** components: `brokerage · stt · exchange_txn · gst · sebi · stamp_duty`.
```
dp_ / demat / debit  in broker_costs.yaml : 0
dp_ / demat / debit  in cost_calculator.py: 0
```
(The three `DP` hits are `_TWO_DP = Decimal("0.01")`, a rounding constant.) The **only** source file mentioning demat is `scripts/t2_cnc_gtt_realtest.py` — a test script, ⛔ not the production cost path.

⇒ 🔴 **C-2 ANSWER: NO. The model does NOT include a per-scrip delivery (DP / demat debit) charge.**

⭐ **AND THIS IS EXACTLY THE UNTESTED OVERNIGHT PATH — which is why nothing ever caught it:**
* a **same-day** CNC round trip incurs **no DP charge** (the shares never settle into the demat account) ⇒ **the model is CORRECT for every CNC exit in the population**
* a **genuine T+1 delivery SELL from holdings** incurs a **FLAT per-scrip charge**
* 🔬 **no genuine overnight delivery sale has ever occurred** ⇒ **the gap has never been exercised**

⇒ ⭐ **That reconciles the model's ₹1.15 against 👤 Rama's ₹30+ — a factor of ~26 — with no contradiction: they are charges on two different events.**

### 🔴 C-3 — THE ARITHMETIC CONSEQUENCE (⛔ NOT a claim about realised performance)
**Measured inputs.** All three DELIVERY strategies (`positional_momentum_long`, `positional_sector_rotation`, `positional_swing_long`) carry **identical** sizing:
```
sl_method: "FIXED_PCT"   sl_pct: 0.02        tgt_method: "RISK_REWARD"   tgt_risk_reward: 1.5
=>  target = 2.0% x 1.5 = 3.0%
```
✅ Confirmed against today's live GTTs: 20MICRONS **2.79%** · FMGOETZE **3.00%** · THEMISMED **2.99%**.

**Operands, 👤 Rama's ₹30 figure:**

| position value | ₹30 as % | configured target | outcome at FULL target |
|---|---|---|---|
| ₹454 (20MICRONS today) | **6.61%** | 3.0% | 🔴 loss — target is less than half the charge |
| ₹573 (FMGOETZE today) | **5.24%** | 3.0% | 🔴 loss |
| **₹1,000** | **3.00%** | 3.0% | 🔴 **exact break-even** |
| ₹1,500 | 2.00% | 3.0% | ✅ +1.0% net |
| ₹3,000 | 1.00% | 3.0% | ✅ +2.0% net |

⇒ 🔴 **BREAK-EVEN POSITION SIZE = ₹30 / 0.03 = ₹1,000.** Below it, **a delivery trade that hits its FULL target still loses money on the DP charge alone.**
⚠️ **And current sizing sits right on that line:** the positional bucket is `positional_bucket_pct 0.30` × `_total 10,567.60` ≈ **₹3,170**, across `max_open_delivery_positions: 3` ⇒ **≈ ₹1,057 per scrip at full allocation.**

### ⚠️ LABELLING — ⛔ NOT OVERCLAIMED
* **₹30+ is 👤 RAMA'S figure**, ⛔ not my measurement. I have ⛔ **not** verified Zerodha's exact DP rate.
* This is an **ARITHMETIC CONSEQUENCE of measured inputs**, ⛔ **not** a claim about realised delivery performance.
* The model is **CORRECT for every trade in the population** — all were same-day.
* ⛔ **Nothing was changed:** no config, no rate, no strategy target, no `broker_costs.yaml`.
* ⭐ Per FILE 7 §4 this is **its own small unit** — ⛔ it does **not** belong in DAY 3 and ⛔ must not be merged into the DEFECT B work.

## §3 — STANDING OPERATING RULES · RECORDED PERMANENTLY

**RULE C-1 — THE POSITION-HOLD NOTICE.** If an open position is required for a test, Rama must be told **BEFORE 15:00 IST that day, unprompted**, in ONE short line containing all four of: **(1)** which position · **(2)** why — naming the specific test · **(3)** what it costs him to hold, **in rupees**, ⛔ never "a small cost" · **(4)** what is lost if he closes — **named items**, ⛔ never "some evidence".
⛔ **NEVER wait for him to ask.** ⛔ **NEVER answer a "can I close this?" with a balanced cost/benefit** — ⭐ lead with the ask, or with "no, close it", then the numbers. ⭐ The decision is **entirely his**; ⛔ do not lobby, ⛔ do not repeat, ⛔ do not raise it again once decided.

**RULE C-2 — COST BEFORE TEST.** ⛔ Never propose Rama hold a real position for a test without first stating the **rupee cost**. ⚠️ If the cost is unknown, **say it is unknown** — ⛔ and do not propose the hold until it is measured.

**RULE C-3 — ZERO-COST ROUTE FIRST.** ⭐ Before asking for real capital, establish whether paper, replay, or existing historical data exercises the same code path. ⛔ Only ask for real money when no free route exists, and ⭐ **say which routes were ruled out and why.**

> 🧹 **THE FAILURE THAT PRODUCED THESE RULES, RECORDED:** at 15:05 Rama asked whether he could close 20MICRONS. I led with *"yes, close it"* — ⭐ which C-1 permits — **but I had never given him the pre-15:00 notice, and I did not know the ₹30 holding cost.** ⇒ he made an economically correct decision that I had not equipped him to weigh. ⛔ Not softened.


---

# FILE 8 — COMBINED CLOSE-OUT. Appended 26-Aug ~16:55 IST.

## §1 · A-1 · 🔴 THE PER-LEG COMPARISON, COMPLETED — **BOTH LEGS HOLD**

⚠️ **B-1 LABEL APPLIED THROUGHOUT: "nearer-SL" / "nearer-TGT", ⛔ NEVER "CNC-SL" / "CNC-TGT".** All 23 rows carry `exit_reason = GTT_EXIT`; **the fired leg is NOT STORED ANYWHERE.** Nearest-trigger means *"the recorded `exit_price` is numerically nearer to this trigger"* — ⛔ it does **not** mean *"this leg fired."*

### 🔴 AMBIGUITY, SHOWN RATHER THAN SILENTLY ASSIGNED
```
SHANTIGOLD   d_sl 6.98   d_tgt 6.25   margin 0.73   <-- GENUINELY AMBIGUOUS
MANINFRA     d_sl 0.72   d_tgt 5.05   margin 4.33
(all 21 others: margin >= 5.87 -- unambiguous)
```
⇒ **ONE row (SHANTIGOLD) is genuinely ambiguous** — its exit price sits nearly midway between the two triggers, so assigning it to *nearer-TGT* on a 0.73 margin is arbitrary. **Reported as ambiguous.** ⛔ No row was forced.

### THE LIKE-FOR-LIKE RESULT
| population | n | median | exact matches |
|---|---|---|---|
| CNC **nearer-SL** | 12 | **1.56** | **0** |
| CNC nearer-SL, **excl. DIFFNKG** | 11 | **1.51** | **0** |
| **MIS `SL_HIT`** | 137 | **0.14** | 15 (11%) |
| CNC **nearer-TGT** | 11 | **0.76** | **0** |
| **MIS `TGT_HIT`** | 90 | **0.004** | 49 (54%) |

⇒ 🔴 **BOTH LEGS SHOW CNC MATERIALLY HIGHER: SL leg ~11× · TGT leg ~190×.**
⭐ **The SL comparison (~11×) is the FAIRER and more CONSERVATIVE one** — a SL converts on trigger and fills at whatever is available, so slippage is expected there. **It still shows an order of magnitude.**
⭐ **Neither leg depends on DIFFNKG** (excluding it moves the SL median only 1.56 → 1.51).

## §2 · A-2 · 🔴 F6e = **TRACED**, AND THE ANSWER IS SPLIT

| path | verdict |
|---|---|
| **MFE** — `compute_trade_excursions`, `core/state_store.py:2079-2091` | selects `symbol, direction, entry_actual_price, entry_time, exit_time`; uses `exit_time` to **BOUND the window**. ⇒ **does NOT consume `trades.exit_price` as a value in the inspected code path** |
| **R-multiple** — `ops_dashboard/backend/readers/db_reader.py:2494` | ```def r_multiple(net_pnl, risk_amount): """R-multiple = net_pnl / risk_amount"""``` — called at `:2682`, aggregated as `avg_r_multiple` at `:2752` ⇒ 🔴 **CONSUMES `net_pnl` DIRECTLY** |

⇒ 🔴 **AND Z-3 PROVED `net_pnl` DERIVES FROM `exit_price`. THEREFORE THE R-MULTIPLE INHERITS THE `exit_price` DEPENDENCY IN FULL, TRANSITIVELY — as does `avg_r_multiple`.**
⚠️ **SCOPE BOUNDARY, stated:** this is the **ops_dashboard reader**, ⛔ not the trading core. **Whether F6e's own design work reuses this function or computes its own R-multiple is a SEPARATE, UNTRACED question.** ⛔ F6e is still neither declared invalid nor declared safe.

## §3 · 🔴 THE MECHANISM / CARRY SPLIT — A FREE PARTIAL TEST EXISTS

⭐ The carry design was built assuming it **all** needs a real overnight carry. **That is not true.**

| arm | status |
|---|---|
| ✅ **MECHANISM ARM — TESTABLE FREE, ANY DAY, ON ANY OPEN POSITION (MIS or CNC)** — CHECK 2a's attribution route (`trades.reservation_id` → `fm_ledger` → the bucket aggregate) and CHECK 1's conservation arithmetic both run against **any live state** | ⭐ **AVAILABLE — but ⛔ NOT tonight: the book is flat (0 open trades since 15:19:53).** ⇒ **runs on the first open intraday position tomorrow, at zero cost** |
| 🔴 **BROKER / T+1 ARM — NO SUBSTITUTE EXISTS** — the REHYDRATE arm (a boot replaying an OPEN row) · overnight broker-side position survival · the holdings-vs-positions transition · broker-side GTT/OCO survival · T+1 settlement · F6-leg `abs(int(qty))` · the G3 settled-CNC T+1 measurement | **NOT EXERCISED — awaits an opportunistic or one deliberately priced carry** |

⭐ **ADOPTED RULE:** *"Do not make CHECK 1 / CHECK 2a / CHECK 2b wait for a real carry if their code paths can already be tested by non-live evidence. The real carry is needed specifically for the broker/T+1 properties that cannot otherwise be established."*
⛔ **Do NOT claim the carry test passed because the mechanism verified. TWO ARMS, TWO LABELS, ALWAYS.**

## §4 · B-8 · 🔴 RESOLVED — **NOT AN INCONSISTENCY, TWO DIFFERENT ARTEFACTS**
```
STORED  kill_switch_state.triggered_at = 2026-08-26T15:15:01.600633+05:30
LOG     "KillSwitchActivated: INACTIVE -> SOFT_KILL"  emitted 15:15:01.603
```
⇒ **The stored value is `.600633`; the `.603` is the log-emission timestamp of the CRITICAL, ~2.4 ms later.** Both are correct; they describe **different events**. ⭐ Corrected in every usage — the DB value is the canonical one.
⚠️ **Also observed, recorded not chased:** there is **no SOFT_KILL row in `system_events` today** — only `KILL_AUTO_CLEARED` (08:15:18.793999) and `STARTUP` (08:15:29.559643).

## §5 · WORDING APPLIED — THE 4Q PACKAGE (B-1 … B-7)

**B-2 · FULL DISTRIBUTION RETAINED IN THE CANONICAL RECORD** (⛔ median+max alone loses the outlier answer):
```
CNC GTT_EXIT       n=23   p25 0.25    med 0.96   p75 3.45    max 41.65
CNC excl. DIFFNKG  n=22   p25~0.25    med 0.86   p75~3.30    max  6.25
MIS TGT_HIT        n=90   p25 0.002   med 0.004  p75 0.019   max  9.622
MIS SL_HIT         n=137  p25 0.026   med 0.14   p75 0.358   max  2.672
```

**B-3 · 🔴 THE HEADLINE IS THE OUTLIER RESULT, ⛔ NOT THE 240× RATIO.**
> **USE:** *"After removing DIFFNKG, the CNC median deviation remains **0.86**, against **0.004** for MIS TGT and **0.14** for MIS SL."*
⛔ 240× is a **population-level comparison** (blended CNC vs MIS-TGT median, and the two MIS legs differ by order type) — ⛔ **never the definitive like-for-like statistic.** ⭐ §1's per-leg result supplies the fair comparison.

**B-4 ·** *"R-2 strongly establishes a materially different CNC exit-price deviation distribution from the measured MIS control populations."* ⛔ **NOT** *"R-2 proves the defect mechanism."* ⇒ **BEHAVIOUR = strongly established · MECHANISM = unresolved · BROKER-FILL PROVENANCE = unresolved.**

**B-5 · DIFFNKG:** *"The gap-down alternative could not be tested from available internal data, so DIFFNKG is **WITHDRAWN as load-bearing evidence**."* ⛔ **NOT "disproven". ⛔ NOT "proves LTP fallback".** ⭐ **Recorded as a STRENGTH** — the finding was not protected by confirmation bias and got stronger once the most quotable row was removed.

**B-6 · MFE:** *"The MFE calculation path was traced through `compute_trade_excursions` (`state_store.py:2079-2091`) and **does not consume `trades.exit_price` as a value in the inspected code path**."* ⛔ Not *"appears insulated"*. ⇒ R-multiple answered at §2.

**B-7 · THE SURVIVING LEGS, recorded together so no single row carries the case:** the CNC population distribution · the MIS control · the **proven `exit_price` → `pnl_delta` → `net_pnl` dependency** · the **absent contract** · plus **Z-2's proven absence of any persisted GTT fire timestamp**.

## §6 · WORDING APPLIED — THE FILE 7 PACKAGE (C-1 … C-6)

**C-1 · 🔴 ₹30 IS "RAMA-REPORTED ≈ ₹30", ⛔ NEVER "the DP rate".** ⭐ **"estimated cost" and "broker-confirmed cost" are PERMANENTLY DIFFERENT LABELS.** ⛔ An estimate must never harden into a fact — ⚠️ **that is the same failure family as the eleven owned errors.**
* **ESTABLISHED:** the production `CostBreakdown` has exactly six components — `brokerage · stt · exchange_txn · gst · sebi · stamp_duty` — and ⛔ **no DP/demat-debit component was found** in `broker_costs.yaml` or `cost_calculator.py`.
* ⛔ **NOT ESTABLISHED:** the exact broker tariff for this account · whether it is ₹30 · whether other delivery-sell charges exist · whether every broker/product combination follows the same treatment.

**C-2 · 🔴 HEADLINE REPLACED.**
> **SUPERSEDED (my FILE 7 close):** *"delivery at current position sizes cannot clear its own costs at the configured 3% target"* / *"delivery cannot pay for itself."*
> ✅ **CORRECTED:** *"Under the Rama-reported ≈₹30 delivery-sell charge assumption, the current ~₹1,057 delivery allocation and configured 3% target leave almost no gross margin after that single charge; the economic viability of delivery trades is therefore **QUESTIONABLE until the actual broker charge and the complete delivery-sell cost path are verified**."*
**Arithmetic, operands shown:** `₹30 / 0.03 = ₹1,000` break-even · `0.30 × 10,567.60 = 3,170.28` ÷ 3 = **₹1,056.76** per slot · `1,056.76 × 3% = ₹31.70` ⇒ **≈ ₹1.70 remains after the assumed ₹30 alone.**
⚠️ **₹1.70 is ⛔ NOT profit** — other costs, taxes, spread and slippage can consume it entirely.

**C-3 · TWO SEPARATE STATEMENTS, ⛔ NEVER MERGED:**
* ✅ *"The existing same-day CNC cost model works for the measured same-day CNC case"* — **SUPPORTED** (model ₹1.16 vs recorded ₹1.15).
* ⛔ *"The system correctly models a genuine delivery SELL from settled holdings"* — **NOT EXERCISED / NOT ESTABLISHED.**
⭐ **The ₹1.15 reconciliation validates the same-day calculation ONLY. ⛔ It is not evidence the delivery-sale cost is covered.**

**C-4 ·** *"No genuine overnight delivery sale has occurred in the measured population"* ⇒ **NOT EXERCISED.** ⛔ **NOT** *"the system does not support delivery costs"*, ⛔ **NOT** *"delivery charges never work"* — those are implementation conclusions that have **not been proven**.

**C-5 · 🔴 THE THREE OPTIONS ARE DECISION OPTIONS, ⛔ NOT RECOMMENDATIONS.** Larger position size · wider target · pause delivery. ⛔ **Nothing was changed** — no position sizing, target %, stop %, strategy YAML or broker-cost config. ⚠️ **Specifically: raising position size merely to clear a FIXED charge creates a different risk/capital problem.** ⭐ **Establish the actual charge first; decide economics after.**

**C-6 · R-1 PAPER CARRY = RULED OUT for the broker/T+1 proof.** ⛔ *"Ruled out"* does **not** mean paper is generally useless — ⭐ **it means paper cannot answer THIS overnight broker/T+1 question.** ⛔ Not to be reopened unless 👤 Rama's own decision changes.

## §7 · 🔴 SCOPE SEPARATION — THREE UNITS, ⛔ NEVER MERGED
| unit | question | destination |
|---|---|---|
| **A · DEFECT B** | CNC exit-price behaviour and provenance | **DAY 3** |
| **B · THE COST GAP** | delivery-sell cost modelling | ⭐ **ITS OWN SMALL UNIT.** ⛔ Not DAY 3, ⛔ not part of DEFECT B |
| **C · THE CARRY TEST** | broker/T+1 overnight state transition | ⭐ opportunistic, or one deliberately priced carry |
⭐ All three concern delivery; ⛔ **they answer different questions.** ⛔ **The carry test is NOT a prerequisite for fixing unrelated proven issues.**

**THE COST-GAP INVESTIGATION — ⛔ NOT TONIGHT, and narrow when it runs:** (a) confirm the broker's ACTUAL delivery-sell charge from an **authoritative tariff or statement** · (b) per scrip or per order, and any other mandatory delivery-sell charge · (c) compare against the production `CostBreakdown` fields · (d) determine exactly WHICH production P&L path omits it · (e) **STOP.**
🔴 ⛔ **DO NOT CREATE A REAL DELIVERY TRANSACTION MERELY TO DISCOVER A FEE.**

## §8 · ⚠️ THE ERROR PATTERN — RECORD THE SHAPE, ⛔ NOT JUST THE INSTANCES
**Eleven owned errors today. THREE share one shape: INFERRING FROM ABSENCE.**
1. `get_trades` — nearly concluded from log absence (**caught before publishing**)
2. **CHECK 1** — concluded "did not run" from `CHECK1 = 0` (**published, then withdrawn**)
3. **The join fan-out** — a headline built on duplicated rows, caught only because an **independent population count disagreed**
⭐ **THE PATTERN IS THE LESSON: an absence is evidence only when the thing that would have spoken was PROVEN to be reached, and a population claim is safe only when an INDEPENDENT count agrees.**


---

# FILE 8A — A-1 COMPLETION. Appended 26-Aug ~17:10 IST. VM clock gated at 16:58:23 IST.

## §0 · DECLARED DEFINITIONS (⛔ previously implicit — this is the fix for the whole file)
| element | declaration |
|---|---|
| CNC comparand | `gtt_state.sl_trigger` / `tgt_trigger`. 🔬 **MEASURED: triggers are UNIQUE per trade for ALL 23** — zero trades had differing triggers across their gtt rows |
| MIS SL comparand | `orders.trigger_price` **where `leg='SL'`** (n=138) |
| MIS TGT comparand | `orders.price` **where `leg='TGT'`** (n=90). ⚠️ **`trigger_price` is NULL on every TGT leg** — TGT legs are LIMIT orders |
| deviation | `abs(exit_price - comparand)` |
| **exact** | **deviation < ₹0.005** = agreement to 2 dp = **one tick**. ⛔ NOT bitwise zero |
| classification | **nearer-SL** iff `d_sl < d_tgt`; **nearer-TGT** otherwise |
| ambiguity | `ratio = max(d_sl,d_tgt) / min(d_sl,d_tgt) < 2` |

⚠️ **`orders.leg` vocabulary is `ENTRY · EOD · SL · TGT` — ⛔ there is NO `leg='EXIT'`.**
⭐ **THE 28→23 FAN-OUT IS IMMATERIAL:** DIFFNKG's 3 rows all carry `sl=437.2 tgt=459.45`; ATULAUTO's 4 all carry `sl=575.65 tgt=605.0`. They are **re-protect/re-issue cycles** (TRIGGERED→TRIGGERED→EXPIRED→CLEANED), ⛔ not re-priced ladders. ⇒ **any row-selection rule yields identical triggers; no undeclared choice hides here.**

## §1 · 🔴 THE CANONICAL TABLE — BOTH LEGS, FULL DISTRIBUTIONS
| population | n | exact | min | p25 | **median** | p75 | max |
|---|---|---|---|---|---|---|---|
| **CNC nearer-SL** | 12 | **0** | 0.090 | 0.627 | **1.5600** | 3.225 | 41.650 |
| **CNC nearer-SL excl. DIFFNKG** | 11 | **0** | 0.090 | 0.535 | **1.5100** | 2.395 | 3.900 |
| **MIS `SL_HIT`** (control) | 138 | **15 (11%)** | 0.000 | 0.027 | **0.1459** | 0.367 | 2.672 |
| **CNC nearer-TGT** | 11 | **0** | 0.030 | 0.200 | **0.7600** | 3.480 | 6.250 |
| **MIS `TGT_HIT`** (control) | 90 | **49 (54%)** | 0.000 | 0.002 | **0.0043** | 0.019 | 9.622 |
| **R-2 blended CNC** (retained) | 23 | **0** | 0.030 | 0.25 | **0.96** | 3.45 | 41.65 |
| **R-2 blended excl. DIFFNKG** (retained) | 22 | **0** | 0.030 | ~0.25 | **0.86** | ~3.30 | 6.25 |

⭐ **TOLERANCE SENSITIVITY, measured:** at a **10× looser ₹0.05**, CNC is still **1/23 (4%)** against MIS TGT **83/90 (92%)** and MIS SL **48/138 (35%)**. ⭐ **The smallest CNC deviation in the entire population is ₹0.03 — SIX TICKS.**

## §2 · S-1 · DISPOSITION — SUMS TO 23
```
CNC nearer-SL  classified      12
CNC nearer-TGT classified      11
UNCLASSIFIED / ambiguous        0   (S-3 rows are RETAINED and NAMED, then carried through S-4)
                              ---
                               23  OK
```
⭐ **Every row is classified; the ambiguous rows are NAMED and carried through the S-4 sensitivity rather than silently dropped.**

## §3 · S-2 — ✅ **CONFIRMED FROM DATA, ⛔ not taken on trust**
`SHANTIGOLD exit 266.40 · sl_trigger 259.42 · tgt_trigger 272.65 ⇒ d_sl 6.98 · d_tgt 6.25 ⇒ nearer = TGT at 6.25`
⇒ ⭐ **SHANTIGOLD IS the largest deviation in the population after DIFFNKG** (next: MMFL 5.65, SOLARA 4.70) and **it does sit in nearer-TGT.** Excluding it takes nearer-TGT 11 → 10 and removes that bucket's largest row.
✅ Cross-checks pass: 12 + 11 = 23 · DIFFNKG `d_sl 41.65 < d_tgt 63.90` ⇒ **nearer-SL** ⇒ nearer-SL excl. DIFFNKG = 11.

## §4 · S-3 — 🔴 THE RULE, DECLARED — AND IT **CORRECTS MY OWN EARLIER CALL**
⚠️ **My earlier ambiguity call used ABSOLUTE margin, which is SCALE-DEPENDENT.** MANINFRA *looked* ambiguous (margin 4.33) only because its prices are ~₹113.
⭐ **DECLARED RULE — scale-free:** `ratio = max(d_sl,d_tgt) / min(d_sl,d_tgt)`, ambiguous iff **ratio < 2**.
```
SHANTIGOLD  1.117   <-- ambiguous
DIFFNKG     1.534   <-- ambiguous
CLSEL       3.587   <-- 2.34x jump: the largest multiplicative break in the ordering
EPL         4.774
MMFL        4.929
SOLARA      5.298
20MICRONS   5.987
ATULAUTO    6.526
MANINFRA    7.014   <-- 9th of 23. NOT ambiguous.
```
⇒ 🔴 **AMBIGUITY SET = {SHANTIGOLD, DIFFNKG}. ⛔ MANINFRA IS NOT AMBIGUOUS — my earlier flag is WITHDRAWN.**
⭐ **THE RULE WAS NOT REVERSE-ENGINEERED:** it fails to isolate SHANTIGOLD and instead catches **DIFFNKG** — the row already withdrawn as load-bearing. ⭐ A tuned rule would have produced a flattering set; this one produced an inconvenient one.

## §5 · S-4 — 🔴 THE SENSITIVITY TABLE
⭐ **FROZEN INTERPRETATION, restated BEFORE the numbers:** if `exact = 0` holds in both legs AND both medians stay an order of magnitude above their MIS controls under EVERY treatment ⇒ the conclusion is **INSENSITIVE to classification**, which is stronger than any single split. If any treatment flips a leg ⇒ the conclusion **DEPENDS on an undeclared heuristic** and must be restated as such.

| treatment | nearer-SL n / exact / med | excl. DIFFNKG n / med | nearer-TGT n / exact / med |
|---|---|---|---|
| **(a)** SHANTIGOLD retained in nearer-TGT | 12 / **0** / **1.5600** | 11 / **1.5100** | 11 / **0** / **0.7600** |
| **(b)** SHANTIGOLD excluded | 12 / **0** / **1.5600** | 11 / **1.5100** | 10 / **0** / **0.5800** |
| **(c)** SHANTIGOLD moved to nearer-SL | 13 / **0** / **1.6100** | 12 / **1.5600** | 10 / **0** / **0.5800** |
| **(d)** FILE 8A literal: + MANINFRA excluded | 11 / **0** / **1.6100** | 10 / **1.5600** | 10 / **0** / **0.5800** |
| **(d′)** S-3 rule: SHANTIGOLD + DIFFNKG excluded | 11 / **0** / **1.5100** | 11 / **1.5100** | 10 / **0** / **0.5800** |

⇒ ✅ **`exact = 0` HOLDS IN BOTH LEGS UNDER ALL FIVE TREATMENTS.**
⇒ ✅ **nearer-SL median spans 1.51–1.61 vs MIS SL 0.1459 ⇒ 10.3×–11.0× under every treatment.**
⇒ ✅ **nearer-TGT median spans 0.58–0.76 vs MIS TGT 0.0043 ⇒ 135×–177× under every treatment.**
⇒ 🔴 **VERDICT: NO TREATMENT FLIPS EITHER LEG. THE CONCLUSION IS *INSENSITIVE* TO THE CLASSIFICATION CHOICE.** ⭐ That is a stronger result than any single split, and it retires the undeclared-cutoff objection permanently.

## §6 · ⚠️ A DISCREPANCY I RAISED AGAINST MYSELF, CHASED, AND RESOLVED
Mid-run I measured the MIS controls against **`trades.sl_initial` / `tgt_initial`** and got med 0.1404 / **0.0244** with **2 / 3** bitwise-exact — ⛔ NOT the recorded 0.14 / 0.004 with 15 / 49. **I reported the conflict before resolving it, and stated mid-run that the exact-match argument "largely dissolves".**
✅ **RESOLVED — TWO definitional differences, BOTH MINE, now declared in §0:** the canonical figures use **ORDER-LEVEL comparands** (`orders.trigger_price` leg=SL; `orders.price` leg=TGT), and **"exact" means agreement to 2 dp (< ₹0.005), not bitwise zero.** Re-measured under those definitions they reproduce the record **precisely**: p25 0.002 · med 0.0043 · p75 0.019 · max 9.622; **15/138 = 11%**; **49/90 = 54%**.
⇒ 🔴 **THE EARLIER CANONICAL RECORD STANDS. MY MID-RUN DOUBT IS WITHDRAWN.**
⚠️ **I nearly withdrew a CORRECT finding because I had not declared my own definitions** — which is exactly the defect §0 now fixes, and exactly why §8 exists.
⭐ An interim wrong join (`leg='EXIT'`, which does not exist) returned **EMPTY** and was caught **by the empty result**, ⛔ not by assumption.

## §7 · A-2 · THE TWO LABELS, ADOPTED VERBATIM
> *"Dashboard R-multiple reader path traced: `r_multiple(net_pnl, risk_amount)` at db_reader.py:2494, consumed at :2682, aggregated at :2752. Since `net_pnl` is downstream of `exit_price` (Z-3), the DASHBOARD R-multiple inherits that dependency. ⛔ F6e's own design/runtime consumption of this reader remains UNTRACED unless separately demonstrated."*

⇒ **dashboard-reader R-multiple = TRACED** · ⇒ **F6e design/runtime R-multiple dependency = PARTIALLY TRACED / OPEN**
⛔ A reader-level trace is ⛔ NOT a system-wide provenance claim. ⭐ **MFE unchanged:** traced through `compute_trade_excursions` (`state_store.py:2079-2091`); ⛔ does not consume `exit_price` as a value in the inspected path.

## §8 · 🔴 STANDING RULE — THE NINE ELEMENTS
**Every quantitative finding from now on carries ALL NINE:** 1 population definition · 2 inclusion/exclusion rule · 3 ambiguous or unclassified rows, NAMED · 4 n · 5 exact count · 6 full distribution (min · p25 · median · p75 · max) · 7 the calculation · 8 the interpretation · 9 ⭐ **what it DOES NOT prove**.
⛔ **A finding missing ANY of the nine is PARTIALLY MEASURED, ⛔ never closed.**
⚠️ **FILE 8A is the worked example of why:** A-1 came back incomplete because elements **2, 3, 5 and 6** were unstated — and the undeclared comparand in element 2 is what produced §6's false alarm against my own record.

### ⭐ ELEMENT 9 FOR THIS FINDING — WHAT IT DOES **NOT** PROVE
⛔ It does NOT establish which GTT leg actually fired — **the fired leg is not persisted**; this is nearest-trigger numerical proximity, ⛔ not broker-fire provenance.
⛔ It does NOT prove the mechanism — `_resolve_exit_price`'s three-tier fallback remains **INFERENCE**, ⛔ not measured.
⛔ It does NOT establish broker-fill provenance for any CNC row.
⛔ It does NOT prove the MIS and CNC populations are otherwise comparable — they differ in order type, venue path and holding period.
✅ It DOES establish, at population scale and **insensitively to classification**, that **recorded CNC exit prices sit materially further from their triggers than MIS exit prices do from theirs.**

## §9 · B-8 · THE OBSERVATION RETAINED
✅ Accepted: stored `triggered_at` 15:15:01.600633 vs log emission 15:15:01.603, ~2.4 ms apart — **two artefacts, ⛔ not an inconsistency.**
⚠️ **RETAINED, labelled:** *"`system_events` contained `KILL_AUTO_CLEARED` and `STARTUP`, but no SOFT_KILL row."*
⛔ **DO NOT infer from that absence that the soft kill did not happen** — the stored `kill_switch_state` and the log both establish that it DID. ⭐ **Recorded as a further instance of the never-infer-from-absence rule — the fourth today.**


---

# FILE 8B — SCOPE RESET · A-1 CLOSED · REPORTING PARKED. Appended 26-Aug ~17:30 IST. VM clock gated 17:23:22 IST.

## §1 · 🔴 RAMA'S SCOPE RULING — THIS GOVERNS EVERYTHING
> **ONE SYSTEM → TWO PIPELINES → each trade on its OWN CONFIG AND CONTROL. One pipeline stopping must NEVER stop the other. ⭐ That is sufficient.**

⛔ **OUT OF SCOPE** unless it demonstrably touches a core trading decision, reservation, execution, risk or lifecycle path: CNC profit reporting · price differences between system and broker · exit-price provenance · R-multiples · P&L presentation.
⭐ **THE BROKER IS THE FINAL TRUTH.** The trade happened as the broker says it happened. ⛔ **A reporting discrepancy does not change what was traded.**

⇒ 🔴 **DEFECT B IS PARKED AS NON-CORE.** Recorded complete, all evidence intact. ⛔ **STOP WORKING ON IT. ⛔ Do not reopen.** Status stays exactly as measured — **BEHAVIOURALLY ESTABLISHED, mechanism unresolved** — and it changes nothing about what was traded.
⚠️ **It returns to scope ONLY if shown to affect sizing, reservation, execution, risk or lifecycle. ⛔ Not otherwise.**

⭐ **RAMA'S SLIPPAGE HYPOTHESIS — recorded and PARKED with the rest:** some CNC deviation may be **ENTRY-side**, not exit-side — the system's entry price plus slippage, or a sub-₹1 cushion. ⚠️ It fits deviations near or below ₹1; ⛔ it does **not** fit DIFFNKG's ₹41.65. ⇒ **A FOURTH CANDIDATE** alongside LTP snapshot, gap fill and broker slippage. ⛔ **Do not test it — it is reporting.**

## §2 · 🔴 TWO NEW PERMANENT RULES — STANDING, ALL SESSIONS
**RULE M-1 — MEASURE OR SEARCH BEFORE JUDGING.** ⛔ Never reason to a conclusion from inside the codebase alone. ⭐ Before any judgement: get the input data from **measurement**, OR **search how the thing actually works externally** (broker rules, exchange mechanics, settlement, tariffs). ⚠️ Roaming within the data repeatedly has not helped — **several of today's eleven errors came from exactly that.**

**RULE M-2 — CORE FILTER.** ⭐ Before opening any item ask: *does it affect a core trading decision, reservation, execution, risk, or pipeline lifecycle?* ⛔ **If NO — record it and PARK it.** ⭐ Reporting, presentation and provenance are **not** core. ⛔ The broker is the final truth.

**RULE 9-ELEMENT (FILE 8A §8) stays standing:** population · inclusion/exclusion rule · ambiguous rows · n · exact · full distribution · calculation · interpretation · ⭐ **what it does NOT prove**.

## §3 · A — 🔴 MIS `SL_HIT` FROZEN AT **n = 137**, AND THE 138 WAS **MY JOIN FAN-OUT AGAIN**
🔬 **MEASURED — the differing row NAMED:** neither set-difference is populated (`in B not in A` = [] · `in A not in B` = []). The gap is **RAMCOIND carrying TWO `leg='SL'` order rows** — `260625170412317` and `260625170412443` — **both with the identical `trigger_price = 334.384281`**, exit 334.0, exit_time 2026-06-25T10:12:49. The join emitted the trade twice.
⇒ ⭐ **CANONICAL n = 137, one row per TRADE.** The 138 is a join artefact, ⛔ not a real observation.
⭐ **⛔ THE CHOICE WAS NOT MADE FOR A NICER STATISTIC:** the duplicate is demonstrably the same trade with the same trigger value, and de-duplicating **restores the originally recorded median 0.14** — confirming the original record used 137 correctly.

| population | joined rows | **distinct trades** | dup dropped | exact | min | p25 | **median** | p75 | max |
|---|---|---|---|---|---|---|---|---|---|
| **MIS `SL_HIT`** (FROZEN) | 138 | **137** | **1 — RAMCOIND** | 15 (11%) | 0.000 | 0.026 | **0.1404** | 0.358 | 2.672 |
| **MIS `TGT_HIT`** (FROZEN) | 90 | **90** | **0 — clean** | 49 (54%) | 0.000 | 0.002 | **0.0043** | 0.019 | 9.622 |

⚠️ **OWNED, UNSOFTENED — ERROR #12, AND IT IS A REPEAT OF #11.** The `trades JOIN gtt_state` fan-out was error #11 today; I reproduced the identical shape on `trades JOIN orders` within hours of recording it. ⭐ **A JOIN IS A FAN-OUT UNTIL PROVEN OTHERWISE — de-duplicate by the entity you are counting, ALWAYS, and verify the other leg too** (TGT was checked and is clean; ⛔ that was verified, not assumed).
⭐ Every historical reference to the MIS SL control is corrected to **n = 137 · med 0.1404**. ⛔ The `n=138 · med 0.1459` figures in FILE 8A §1 are **SUPERSEDED**.

## §3 · B — 🔴 THE "RATIO < 2" AMBIGUITY RULE IS **WITHDRAWN**
⚠️ **Rama is right, and the objection is fatal:** I found the threshold **from the observed ordering** — the 2.34× gap between DIFFNKG 1.534 and CLSEL 3.587. **That is a threshold discovered AFTER seeing the data.** ⭐ It is a **useful descriptive observation**, ⛔ **NOT a pre-existing principled rule**, and my FILE 8A defence of it ("it catches an inconvenient row, so it wasn't tuned") ⛔ **does not repair the fact that the cut point came from the data it was applied to.**

⇒ ⭐ **PRIMARY CLASSIFICATION = DETERMINISTIC NEAREST-TRIGGER**, on the smaller absolute deviation. **Every row classified. ⛔ No row called "ambiguous". ⛔ No row dropped.**
⇒ ⭐ **SENSITIVITY = A SEPARATE EXERCISE**, on rows whose classification could reasonably affect the conclusion.

| row | deterministic | sensitivity row? |
|---|---|---|
| **SHANTIGOLD** | **nearer-TGT** (d_tgt 6.25 < d_sl 6.98) | **YES** |
| **DIFFNKG** | **nearer-SL** (d_sl 41.65 < d_tgt 63.90) | **YES** — outlier, already withdrawn as load-bearing |
| **MANINFRA** | **nearer-SL** (d_sl 0.72 < d_tgt 5.05) | ⭐ the ambiguity flag is **WITHDRAWN either way** |

⚠️ **If an ambiguity threshold is ever wanted, ⭐ define it PROSPECTIVELY before the next dataset. ⛔ NEVER reverse-fit one to 23 rows.**

## §3 · C–H — CONFIRMATIONS
**C.** ✅ S-1 stays simple: nearer-SL **12** + nearer-TGT **11** + unclassified **0** = **23** ✓
**D.** ✅ **S-4 RETAINED — it is the real strength, and A and B do not touch it.** Frozen interpretation restated **before** the numbers: *if `exact = 0` holds in both legs and both medians stay an order of magnitude above their controls under EVERY treatment, the conclusion is INSENSITIVE to classification; if any treatment flips a leg, it DEPENDS on an undeclared heuristic.* ⇒ **Five treatments, `exact = 0` in both legs under all five, no flip.**
**E.** ✅ **RATIOS WITH OPERANDS SHOWN, ALWAYS:**
* *CNC nearer-SL median ÷ MIS `SL_HIT` median* = **1.51–1.61 ÷ 0.1404 = 10.8×–11.5×**
* *CNC nearer-TGT median ÷ MIS `TGT_HIT` median* = **0.58–0.76 ÷ 0.0043 = 134.9×–176.7×**
⛔ Never a bare "11×" or "190×". ⛔ **240× is never restored as a headline.** ⭐ Full distribution stays in the canonical record.
**F.** ✅ R-multiple boundary verbatim: dashboard reader **TRACED** · F6e design/runtime **PARTIALLY TRACED / OPEN**. ⛔ Not reopened.
**G.** ✅ **"nearer-SL" / "nearer-TGT" always** — ⛔ never "CNC-SL"/"CNC-TGT". The fired leg is ⛔ not persisted.
**H.** 🔴 **A-1 IS CLOSED.** ⛔ No further queries on the 23 rows. ⛔ No further statistic squeezed out of them.

⭐ **THE ONE METHOD LESSON KEPT FROM TODAY, ⛔ UNSOFTENED:** I raised a discrepancy against my own canonical figures, chased it, and found **both differences were my own undeclared definitions** — then **withdrew my doubt rather than withdrawing a correct record.** ⭐ That is why the nine-element rule exists.

## §4 · K-1 … K-5 — 🔴 CORE SPARE-WINDOW ITEM (⛔ NOT TONIGHT)
👤 **RAMA'S MEASURED FACT:** CNC and MIS charges — tax and brokerage — are settled **OUT OF MARKET by contract note**, debited to capital the same midnight or next day. ⇒ ⭐ **THE BROKER DOES NOT TOUCH CAPITAL DURING MARKET HOURS.**

🔴 **CORE, because it affects RESERVATION and SIZING:**
* **K-1** — Does the system **DEDUCT charges from bucket capital DURING the session**, at trade close, while the broker has not yet debited them? ⭐ **Today's 20MICRONS round trip recorded `charges = ₹1.15`** (closed 15:19:53, `net_pnl − 6.57`) — ⭐ trace exactly **WHEN and WHERE** that ₹1.15 hit `_total` or a bucket, and whether it reduced **AVAILABLE CAPACITY intraday**.
* **K-2** — IF IT DOES: each pipeline's available capacity is **UNDERSTATED intraday** by the day's accumulated charges, which **under-sizes subsequent trades in that pipeline**. ⛔ That is a **core sizing effect**, ⛔ not reporting. ⭐ Also check whether it contributes to the capital-drift residual.
* **K-3** — IF IT APPLIES ONLY AT THE DAILY RECONCILE: ⭐ no intraday sizing effect; **the item drops.** ⭐ Say so plainly and close it.
* **K-4** — ⚠️ **Per RULE M-1:** measure the system side from source and data, **AND confirm the broker side from an authoritative description** of how Zerodha settles contract-note charges. ⛔ **Do not judge from the codebase alone.**
* **K-5** — ⛔ **Do NOT fix anything. Report only.**

## §5 · THE SCHEDULE, RE-SORTED BY CORE
⭐ **CORE — these get the days:**
| item | why core |
|---|---|
| **F2** | two pipelines, own config · own capital · own limits · own counters · own halt. ⭐ **THE core item.** Carries D-3 and NI-16 |
| **F6 lifecycle** | ⛔ **no pipeline-scoped stop exists** — one process, one unit, one EOD decision. ⭐ **the biggest architectural gap found** |
| **F6-leg `abs(int(qty))`** | ⭐ **strands DELIVERY CAPITAL on T+1.** Core |
| **F4** | CNC entries fill **~30%** vs MIS **~52%**. ⭐ If delivery orders do not fill, the delivery pipeline does not work. ⚠️ needs placement price + quote persisted first to be diagnosable |
| **F11 dead config** | `order_protocol` · `dynamic_by_winrate` · `sl_atr_multiplier` · `delivery_max_position_value`. ⭐ "each trade on its own config" is core; ⛔ config declaring what never happens breaks that. **Removal only** |
| **S6** | ATR migration, **DELIVERY only** — own config, own sizing |
| **F9** | sector placeholder; a control that cannot fire. Core-adjacent |
| **K-1..K-5** | ⭐ only if it proves to affect **intraday sizing** |
| **F6e** | the only item that changes P&L. ⭐ **its MFE input is traced and does ⛔ NOT consume `exit_price`, so it is UNAFFECTED by the parked reporting work** |

⛔ **PARKED — recorded, complete, not worked:** DEFECT B provenance · the `exit_price` contract · the ₹96.89 sensitivity · R-multiple provenance · F5 exit attribution · the delivery-cost/₹30 arithmetic (⚠️ blocked on an authoritative tariff anyway) · **the slippage/cushion hypothesis** · the ~12-min phantom window (🔬 measured; classification is a design decision, ⛔ no action) · F10 · Q-1 · Q-5 · G-G · P6-EV · O-3 · O-4 · MEMORY.md rebuild.

⭐ **STILL OWED, BLOCKED ON A REAL CARRY:** OWED-2 · CHECK 1/2a/2b carry arm · the G3 settled-CNC T+1 measurement · F6-leg's T+1 arm · the EOD gate's discriminating case. ⭐ **The mechanism arm is FREE on the next open intraday position.** ⛔ **The carry test does NOT block any core item above.**

## §6 · DB5 — THE PRE-SHUTDOWN BASELINE, ⚠️ **LABELLED POST-MANUAL-CLOSE**
🔬 **OBSERVED LIVE at VM clock 17:24:26 IST:**
```
service trading-system                 : active
kill_switch_state                      : SOFT_KILL
  reason        circuit_breaker_force_close_15:15
  triggered_at  2026-08-26T15:15:01.600633+05:30
  triggered_by  order_monitor
trades WHERE status='OPEN'             : 0          <-- BOOK IS FLAT
20MICRONS  CLOSED  GTT_EXIT  15:19:53.322126  net_pnl -6.57  charges 1.15
gtt_state NOT IN (CLEANED,EXPIRED)     : 4 rows, NONE of them today's
  ATULAUTO 330456580 TRIGGERED / ATULAUTO 330638484 TRIGGERED  (trd_e66e...)
  DIFFNKG  330658430 TRIGGERED / DIFFNKG  330940420 TRIGGERED  (trd_010f...)
```
⚠️ **THIS IS NOT A CARRY BASELINE. It is the LAST VALID PRE-SHUTDOWN READING AFTER RAMA'S MANUAL CLOSE.** ⛔ It must never be presented as the `A_sameday` carry baseline.
⚠️ **OBSERVATION, PARKED PER RULE M-2:** four historical `gtt_state` rows remain `TRIGGERED` and uncleaned, belonging to the same two fan-out trades (ATULAUTO, DIFFNKG) from 05–11 Aug. **Both trades are CLOSED**, so the `order_reconciler:876-877` CNC exclusion is harmless for them. ⛔ **Not chased — no new branch.**

## §7 · WHAT I DID NOT MEASURE
⛔ Whether the four stale `TRIGGERED` gtt rows are returned by `get_active_gtt_states()` — **not checked, parked.**
⛔ K-1's ₹1.15 capital path — **not traced; it is a spare-window item and ⛔ not tonight.**
⛔ The broker-side contract-note settlement mechanics — **requires an authoritative external source per RULE M-1; ⛔ not consulted.**
⛔ Whether the RAMCOIND duplicate SL order pair indicates a re-issue defect — **out of scope, ⛔ not investigated.**


---

# SECTION D — THE 17:35 GATE, OBSERVED LIVE. Appended 26-Aug ~17:45 IST.

## D-1 · 🔴 THE GATE DECISION, VERBATIM — ⚠️ **IT PASSED TRIVIALLY**
```json
{"ts":"2026-08-26T17:35:00.663+05:30","level":"INFO","logger":"main",
 "msg":"eod_self_exit: past 17:35 IST and flat (0 active positions) — clean shutdown
        for the day; auto-restarts tomorrow after the morning token refresh."}
```
⚠️ **FILE 4K'S MANDATORY TRIVIAL LABEL APPLIES, AND THE GATE STATES ITS OWN TRIVIAL CONDITION IN ITS OWN WORDS: `flat (0 active positions)`.** The book had been flat since 15:19:53, so `active == 0` and the `due` predicate was satisfied by the *empty* branch.
⇒ 🔴 **THIS PROVES NOTHING ABOUT THE RESOLVER-FED EXIT PATH.** ⛔ It is **NOT** evidence that the EOD self-exit correctly exits positions. ⭐ **NOT EXERCISED** is the correct label for the discriminating case.

⭐ The configured gate time, confirmed from the boot line (⛔ not from a card):
```json
{"ts":"2026-08-26T08:15:18.776+05:30","logger":"main","msg":"service window: may START in [08:00, 18:15) IST;
  EOD self-exit at 17:35 IST (configured: trading_hours.service_window_end)"}
```

## D-2 · ✅ SHUTDOWN **PROVEN COMPLETE** — the full sequence, OBSERVED LIVE
```
17:35:00.663  main            eod_self_exit: past 17:35 IST and flat (0 active positions)
17:35:01.363  telegram        "[LIVE] EOD Clean Shutdown"            outcome=delivered
17:35:01.365  effect_census   eod_squareoff: acted 1 | active
17:35:01.365  effect_census   cnc_gtt_monitor: acted 21 | event-driven
17:35:01.365  effect_census   cnc_gtt_placer:  acted 3  | event-driven
17:35:01.365  effect_census   MISMATCH: NONE — every zero is an expected zero
17:35:01.365  effect_census   END day=2026-08-26 mismatches=0
17:35:01.365  webhook         WebhookReceiver.stop() called; new requests will return 503
17:35:01.411  signal_processor       SignalProcessor stopped
17:35:01.412  portfolio_allocator    PortfolioAllocator stopped
17:35:04.413  entry_gate / smart_tgt_manager / order_reconciler   stopped
17:35:04.413  order_monitor   order_monitor.shutdown_cancel_complete cancelled=0 total_entry_orders=0
17:35:04.414  token_monitor   token_monitor.stop
17:35:04.459  kiteconnect.ticker  ERROR Connection closed: None - None      <-- expected on teardown
17:35:04.459  live_feed       WARNING LiveFeedManager: disconnected
17:35:05.122  telegram        "[LIVE] 🛑 System Stopping"           outcome=delivered
17:35:05.130  main            WAL checkpoint_wal on shutdown: busy=0 log=374 checkpointed=374
17:35:05.131  main            Shutdown complete
17:35:05     systemd          trading-system.service: Deactivated successfully.
17:35:05     systemd          Consumed 2min 47.784s CPU, 213.0M memory peak, 0B swap peak
```
✅ **`systemctl is-active` ⇒ `inactive` (🔬 measured 17:37:23).** ✅ **WAL fully checkpointed 374/374.** ✅ **`effect_census mismatches=0`.**
⭐ The two teardown lines at 17:35:04 (`ticker ERROR` / `live_feed WARNING`) are **expected artefacts of socket teardown**, ⛔ not failures.

## D-3 · 🔴 **D-C — THE LINE FOR RAMA: NO MANUAL STOP IS NEEDED.**
The service self-exited cleanly at 17:35:05 and reads `inactive`. ⛔ Nothing for Rama to run. ⭐ **The carry hazard does NOT apply tonight** — *a carried delivery position ⇒ no shutdown ⇒ no boot* did not arise, because the book was flat and the shutdown completed.

## D-4 · RESOLVER CRITICAL — BOUNDED SEARCH, ⚠️ WITH ITS NON-VACUITY CAVEAT STATED
🔬 **MEASURED — `"NO strategy resolver was supplied"` occurrences on 26-Aug:**
```
journalctl -u trading-system --since '2026-08-26 00:00' | grep -c   ->  0
grep -rl over EVERY file in logs/                                   ->  (no files)
grep -c  on logs/system_2026-08-26.log (9,254,158 B)                ->  0
```
⇒ **ZERO hits, across three independent surfaces.**
⚠️ 🔴 **BUT THIS IS NOT PROOF THE FIX IS LIVE TODAY.** The 17:35 gate passed on the **flat** branch, so **the resolver path was NEVER EXERCISED**. ⛔ An empty grep cannot prove a silent success path ran. ⭐ **The ONLY evidence on that axis remains this morning's five-step boot chain**, which established that the armed branch executed. ⛔ Today's 17:35 adds nothing to it.

## D-5 · DB3 — ⛔ **SKIPPED, per FILE 8B T-3.** Its preconditions are absent (no carried position, no discriminating exit). ⛔ Not run merely because it appears in an older sequence.

## D-6 · DB5 — already captured at 17:24:26 IST and labelled **POST-MANUAL-CLOSE**. ⛔ Never a carry baseline. See FILE 8B §6.

## D-7 · ⚠️ ONE OBSERVATION RECORDED, ⛔ NOT CHASED — IT CORROBORATES **F6 LIFECYCLE**
```
14:45:00.750  main           eod_pre_alert: sent for 1 open position(s)
14:45:00.750  telegram       "[LIVE] EOD SQUAREOFF IN ~30 MIN"           outcome=delivered
15:15:01.600  main  CRITICAL circuit_breaker.force_close_triggered: soft_kill, EOD squareoff handles positions
15:17:00.032  eod_squareoff  EOD square-off triggered for 2026-08-26
15:17:00.037  eod_squareoff  Kill switch already active (SOFT_KILL); skipping soft_kill
15:17:00.038  eod_squareoff  EOD Pass 1: canceling all pending orders
15:17:00.038  eod_squareoff  EOD Pass 1 complete: 0 orders cancelled
15:17:02.054  eod_squareoff  EOD: broker-position filter kept 0/0 trades (broker open symbols=0, recovery_fire=False)
15:17:02.070  eod_squareoff  EOD Pass 2 complete: 0 open positions exited.
15:17:02.072  eod_squareoff  EOD summary: positions_squared=0/0 cancels=0/0 duration=2.04s
15:19:53.322  (db)           20MICRONS CLOSED  exit_reason=GTT_EXIT
```
⇒ ⚠️ **The 14:45 pre-alert counted 1 OPEN POSITION. The 15:17 EOD square-off found `broker open symbols=0` and squared off NOTHING. 20MICRONS then closed 2m 51s LATER by a different path.**
⇒ ⭐ **A CNC/delivery position is not visible to a broker-*positions* filter** — delivery sits in **holdings**, not positions. ⭐ **This is the F6 LIFECYCLE gap already on the CORE list**, and this is direct corroborating evidence for it.
⛔ **RECORDED, NOT CHASED — per RULE M-2 and FILE 8B's ⛔ NO NEW INVESTIGATION BRANCH.** ⚠️ **PARTIALLY MEASURED:** ⛔ I did **not** establish whether the filter would have excluded a delivery position that still needed action, nor whether `recovery_fire=False` is correct here — that belongs to F6, ⛔ not to tonight.

## D-8 · WHAT I DID NOT MEASURE
⛔ The 18:15 shadow-recorder cron — **not yet due at time of writing.**
⛔ Whether `eod_self_exit` would have exited a live position — **NOT EXERCISED, and unmeasurable tonight.**
⛔ Whether the four stale `TRIGGERED` gtt rows survive the shutdown — ⛔ not checked, parked.
⛔ The F6 broker-position-filter behaviour with a real delivery position — ⛔ belongs to F6.


---

# T-6 — THE 18:15 SHADOW RECORDER. Appended 26-Aug ~18:20 IST. VM clock gated 18:18:10 IST.

## T-6.1 · ✅ **CONFIRMED — IT RAN AND EXITED CLEAN**
🔬 **MEASURED:**
```
data_store/cron_marks/forward_shadow_record.done   ->   0 2026-08-26T18:16:53+05:30
```
⇒ **exit code 0**, completed **18:16:53 IST** — roughly 1 m 53 s after the 18:15 trigger.

⭐ **The cron entry, read ⛔ not assumed:**
```cron
15 18 * * 1-5  cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a
               && /home/ubuntu/systems/venv/bin/python scripts/forward_shadow_record.py
               >> logs/cron-forward-shadow.log 2>&1; rc=$?
               echo "$rc $(date -Iseconds)" > .../cron_marks/forward_shadow_record.done
```
Today is Wednesday ⇒ matches `1-5`. ⭐ The mark carries the **real exit code**, so it is a falsifiable artefact rather than a mere presence check.

## T-6.2 · ⭐ **THE ROW ITSELF, AND WHY THIS GREEN COULD HAVE BEEN RED**
```
forward_shadow: date=2026-08-26 wrote=5257 simulated=5257
                -> /home/ubuntu/systems/trading-system/data_store/v3/forward_shadow_fs-v1.jsonl
```
⭐ **NON-VACUITY ESTABLISHED FROM THE LOG'S OWN HISTORY** — the same log contains
```
forward_shadow: date=2026-08-10 nothing new (0 present)
```
⇒ **the recorder DOES report a null result when there is one.** Therefore today's `wrote=5257` is a **real positive**, ⛔ not an unfalsifiable pass. ⭐ This satisfies *"a green check is evidence only if it could have been red"*.

⛔ **`scripts/forward_shadow_record.py` WAS NEVER INVOKED BY ME.** Only its artefacts — the `.done` mark, the cron line and the append-only log — were read. ⭐ Its output cannot be regenerated; **a gap is a loss, a manufactured day is a CORRUPTION.**

## T-6.3 · ⚠️ TWO OBSERVATIONS RECORDED, ⛔ NOT CHASED (RULE M-2 — non-core)
1. **`shadow_trades` table `total = 0`.** The recorder's output goes to the **JSONL file** (`data_store/v3/forward_shadow_fs-v1.jsonl`), ⛔ not to that DB table. ⛔ Whether the empty table is dead schema or a second unused path was **not investigated**.
2. **`wrote == simulated` exactly today (5257 / 5257)**, as also on 25-Aug (3809/3809) and 31-Jul (3688/3688), whereas most days show `wrote > simulated` (e.g. 19-Aug 4265/3744, 07-Aug 6198/5875). ⛔ The meaning of that difference was **not investigated** — shadow-recorder internals are **non-core**.

## T-6.4 · ✅ TONIGHT'S CHAIN IS COMPLETE
| item | status |
|---|---|
| T-2 · 17:35 gate captured verbatim | ✅ **DONE** — passed **TRIVIALLY** (`flat (0 active positions)`) |
| T-3 · DB3 | ⛔ **SKIPPED** — preconditions absent |
| T-4 · DB5 | ✅ **DONE** — labelled **POST-MANUAL-CLOSE** |
| T-5 · D-C line to Rama | ✅ **DONE** — **no manual stop needed** |
| T-6 · 18:15 shadow cron | ✅ **DONE** — rc 0, `wrote=5257` |
| T-7 · FILE 6 REV 2 | ⏸️ **AWAITING RAMA** — ⛔ nothing pushed; ⛔ BATCH A / UNIT B **not** reconstructed |
| T-8 · 27-Aug 08:15 SECTION E | ⏸️ **PENDING** |

⚠️ **SECTION E EXPECTATIONS, frozen now so they cannot be rationalised in the morning:**
* **`carry` EXPECT ZERO** — the book closed flat and the shutdown completed. 🔴 **A NON-ZERO CARRY WOULD ITSELF BE A FINDING.**
* **Resolver CRITICAL** — bounded search again; ⚠️ **absence still will not prove the fix live** unless the exit path is exercised.
* **The 45 s morning check** — ⭐ **its FIRST REAL COLD BOOT.** GREEN or RED, reported as measured. ⛔ A RED line alone is still not proof of failure — wait 30 s and re-run before concluding anything.
* **The boot must actually occur** — ⛔ nothing in cron starts the service; a failed 08:15 token refresh is SILENT. ⭐ **Check the token file first.**

## T-6.5 · WHAT I DID NOT MEASURE
⛔ The contents of `forward_shadow_fs-v1.jsonl` — only the recorder's own summary line was read.
⛔ Whether the 5257 rows are correct — ⛔ only that they were written.
⛔ The empty `shadow_trades` table's purpose — parked, non-core.
⛔ The `wrote` vs `simulated` divergence on other days — parked, non-core.


---

# FILE 11 PART 1 — SECTION D RECORD CORRECTIONS. Appended 26-Aug ~19:15 IST. VM clock gated 19:07:56 IST.

## D-1 · T-2 = **PROVEN, PASSED TRIVIALLY**
The gate stated its own condition: *"past 17:35 IST and flat (0 active positions)"*.
⛔ **THIS MUST NEVER BECOME EVIDENCE THE RESOLVER FIX WORKS.**

## D-2 · RESOLVER CRITICAL = **NOT EXERCISED / ABSENCE OBSERVED**
⛔ **NOT "PROVEN FIXED".** Zero hits across the journal, all log files and `system_2026-08-26.log` is **useful NEGATIVE evidence only** — ⚠️ **no live position reached the resolver-fed exit path.**
⭐ **This morning's five-step boot chain remains the ONLY evidence on that axis.** ⭐ The distinction is preserved permanently.

## D-3 · 🔴 THE 15:17 OBSERVATION — **MY F6 CORROBORATION IS WITHDRAWN. IT WAS WRONG.**

### The one check, answered from source
`orders/eod_squareoff.py:1117` emits:
```python
"EOD: broker-position filter kept %d/%d trades (broker open symbols=%d, recovery_fire=%s)",
len(rows), before, len(broker_qty), recovery_fire,
```
⇒ `kept 0/0` ⇒ **`before = 0`** ⇒ 🔴 **THE CANDIDATE LIST WAS ALREADY EMPTY BEFORE THE FILTER RAN. Zero candidates — ⛔ NOT one candidate rejected.**

### Why it was empty — the upstream selection
`orders/eod_squareoff.py:1064` — `_exit_open_positions()`:
```python
rows = self._store.get_open_intraday_positions()
```
⇒ the candidate list is **OPEN INTRADAY POSITIONS**, by name and by design. And the source states the intent outright:
> *"FIX-015: Filter to intraday products only (MIS/CO). **EOD6 design mandates DELIVERY (CNC/NRML) positions are never touched.** In live mode, broker may report both intraday and delivery positions; we must exclude delivery to avoid using their qty or symbol presence in the position-filter logic below."*

⇒ 🔴 **20MICRONS (CNC/delivery) WAS NEVER A CANDIDATE.** ⛔ It was not excluded by a filter — it is **OUT OF SCOPE AT THE SOURCE, DELIBERATELY.**

### Falsifiable corroboration
The code emits a per-symbol WARNING for **every** rejected candidate:
```python
"EOD: skipping symbol %s — broker reports zero/missing position (likely closed by RMS
 or earlier exit fill); MARKET reverse would create a naked short. recovery_fire=%s"
```
🔬 **MEASURED: `grep -c 'EOD: skipping symbol' system_2026-08-26.log` → 0.** ⭐ Consistent with `before = 0`; had a candidate been rejected, that line would exist. ⭐ **The check could have come out the other way.**

### A CORRECTION TO THE PREMISE UNDERNEATH D-3
⚠️ **`broker open symbols=0` does NOT mean the broker was flat.** `broker_qty` is built with
`if int(p.qty) != 0 and p.product in EMERGENCY_FLATTEN_PRODUCTS` — **{MIS, CO} only.**
⇒ **A CNC position could never appear in that count, by design.** ⛔ So that figure cannot be read as evidence about delivery either way.

### 🔴 VERDICT
✅ **The filter behaved CORRECTLY.** ⇒ ⛔ **THE F6 CORROBORATION IS WITHDRAWN.**
⚠️ **MY EARLIER WORDING WAS WRONG AS A MECHANISM CLAIM.** I wrote *"a CNC/delivery position is invisible to a broker-*positions* filter — delivery lives in HOLDINGS."* ⭐ **The delivery position is not ACCIDENTALLY INVISIBLE; it is DELIBERATELY OUT OF SCOPE.** That is a **DESIGN PROPERTY**, ⛔ not a gap.
⚠️ **ERROR #13, OWNED UNSOFTENED.** ⛔ Recording this as corroboration of a core architectural gap **would have misled the F6 work** — precisely the outcome Rama predicted. ⭐ **The failure shape: I reached for the interesting explanation before checking the simplest one, and ⛔ I had not read the candidate-selection line.**

## D-4 · THE THREE SEPARATE LABELS
| label | content |
|---|---|
| **OBSERVED** | The broker-position filter returned **`kept 0/0`** at 15:17:02.054, with `broker open symbols=0, recovery_fire=False`. |
| **CORRELATED** | ⛔ **NOTHING.** D-3 established **no** product-based exclusion of a candidate. ⛔ The F6 correlation is withdrawn. |
| **NOT YET PROVEN** | ✅ **Superseded — it IS now proven why the filter returned zero:** `rows = get_open_intraday_positions()` returned an empty list, because delivery is out of scope by EOD6 design and no intraday position was open. |
⛔ **The sentence *"a CNC position is not visible to a broker-positions filter"* is STRUCK from the record as a proven mechanism.** ⭐ The candidates it was competing against — CNC exclusion · broker/system timing divergence · symbol/account/product filtering · another ownership issue — are all moot: **the selection never included the trade.**

## D-5 · T-6 = **PROVEN — THE RECORDER EXECUTED AND PRODUCED POSITIVE OUTPUT**
`rc=0 @ 18:16:53` · `wrote=5257 simulated=5257` · non-vacuity established from the recorder's own history (`2026-08-10 nothing new (0 present)`).
⛔ **NOT promoted to "shadow recorder correctness proven".**
⚠️ **`wrote == simulated` proves the COUNTS MATCH — ⛔ it does not prove every record is correct, that every source trade is represented, that no duplicates or omissions exist, or that the transformation is right.**
⛔ `shadow_trades total=0` and the `wrote == simulated` pattern stay **PARKED**.

## D-6 · SECTION D FINAL STATUS
| item | status |
|---|---|
| **T-2** 17:35 gate | **PROVEN** — passed **TRIVIALLY** (flat) |
| **T-3** DB3 | **SKIPPED** — preconditions absent |
| **T-4** DB5 | **PROVEN** — POST-MANUAL-CLOSE, ⛔ not a carry baseline |
| **T-5** manual stop | **NOT NEEDED** — clean self-exit 17:35:05 |
| **T-6** shadow cron | **PROVEN** — rc=0 + positive output + non-vacuity |
| **T-7** FILE 6 REV 2 | ⭐ **SUPPLIED** — FILE 11 PART 2 |
| **T-8** 08:15 SECTION E | **PENDING** |

## D-7 · OVERNIGHT — ⭐ **STAY INERT**
The service is legitimately stopped, the book is flat, nothing runs but cron. ⇒ ⛔ **hourly ticks have NO measurement value.**
⛔ **Generate no status noise. ⛔ Manufacture no work because a loop exists.** ⭐ **Next substantive measurement is 08:15.**


---

# FILE 11 PARTS 2–4 — BATCH A PUSHED · UNIT B STOPPED PRE-BUILD. Appended 26-Aug ~21:15 IST.

## 🔴 THE BLOCKING DISCOVERY THAT CHANGED THE PUSH — FOUND BEFORE ANY COMMIT
🔬 **MEASURED:** the local branch `feat/delivery-config-split` (HEAD `6d24a83`) is **48 commits AHEAD and 77 commits BEHIND `origin/main`** — **2,122 insertions / 1,025 deletions across 12 files** vs main, including `config/system_config.yaml` (198), `signals/signal_processor.py` (351), `orders/cnc_gtt_monitor.py` (330), `orders/order_reconciler.py` (178). ⚠️ Its 48 commits include `feat(sizing)`, `feat(pipelines)`, `feat(governor)`, `refactor(config)!` — and **`65b7196`, which PART 3 says is READ-ONLY reference.**
⇒ 🔴 **A push from that branch could not fast-forward and would have carried prohibited capital/signal-path work.**

🔴 **AND THE FINDING THAT MATTERED MOST — ⚠️ A CORE OPERATIONAL GAP:**
```
docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md   UNTRACKED - not on main, not on any branch
docs/audit/BOOT_PROOF_75e637c_26-Aug-2026.md        UNTRACKED
docs/audit/EOD_CARRY_SEQUENCE_26-27-Aug-2026.md     UNTRACKED
docs/audit/ on origin/main = 233 files | branch HEAD = 238 | ON DISK = 300
VM: ls docs/audit/ROLLBACK_AND_ATTENDANCE_23-Aug-2026.md -> No such file or directory
```
⇒ 🔴 **THE ENTIRE ROLLBACK PROCEDURE — RB-2, RB-3, the two-clock rule, L-1, the V-7 recipe — EXISTED ONLY IN ONE LOCAL WINDOWS WORKING COPY. It was ⛔ NOT on the VM, which is exactly where an incident is handled and where §2 says Rama is already at an ssh prompt.**
⭐ **62 audit files existed only on disk.** ⭐ 👤 **Rama ruled: fresh branch from `origin/main`, BATCH A doc files only.**

## ✅ BATCH A — PUSHED. `75e637c..bc9a9f5`, FAST-FORWARD, ⛔ NO FORCE.
Base `75e637c` in a separate worktree, branch `batch-a-docs`, so the diverged tree was ⛔ never checked out or disturbed.
| unit | commit | content |
|---|---|---|
| **A1** | `ae6c344` | rollback TREE advanced **`195436b` → `75e637c`**; all seven OPERATIVE recipes corrected; superseded text retained + dated; A1e/A1f written |
| **A2** | `ce29d49` | `docs/RUNBOOK.md` **§9a** — temporary vs durable rollback, the **two-check** verification, the push freeze. ✅ **RUNBOOK still names ZERO SHAs** |
| **A3** | — | ⛔ **CANNOT COMPUTE** — see below |
| **A4** | — | `MEMORY_BOARD.md:6` re-wrapped 829 B → sub-bullets; 🔬 **guard prints NOTHING**; MEMORY.md **8,896 B** |
| **A5** | `272d1d4` | seven formal closures with reason **and measurement source** |
| **A6** | `bc9a9f5` | today's findings at their measured labels |

🔬 **PRE-PUSH GATE:** 4 files, **all `.md`**, **1,261 insertions / 0 deletions**, **zero non-doc files**, `merge-base --is-ancestor` → fast-forward, remote tip **re-measured at push time**.
✅ **POST-PUSH, ALL THREE:** `origin/main` = **`bc9a9f52dc587d4ef841f70741ffd4f3f4a6aa6c`** · VM bare HEAD = **identical** · **tracked drift 0**.
✅ **THE GAP IS CLOSED:** the rollback document now exists **on the VM at 49,703 B**, RUNBOOK §9a is present, and RB-3 on the box reads **`checkout -f 75e637c`**.
⚠️ The hook regenerated the crontab (*"crontab AUTO-INSTALLED from canonical"*) — **expected**, ⛔ not my edit; ⛔ no cron touched.

## 🔴 ⛔ THE ROLLBACK TREE STAYS `75e637c` — IT DOES **NOT** BECOME `bc9a9f5`
⭐ **A PUSH IS NOT A BOOT.** The TREE moves only on a PROVEN BOOT. ⭐ **Tomorrow's 08:15 is the boot that would move it** — and tonight's push is what it would then be proving.

## ⛔ A3 — CANNOT COMPUTE, SAID SO RATHER THAN SKIPPED
`N20-20` asks that register row **`N20-14`** have its column count fixed (5 structural pipes vs 3, pre-existing at `b019540`). 🔬 **The row does not exist.** `N20-14` occurs in exactly three files — `SYSTEM_MAP.md`, `drift_comparator_fix_20aug.md`, the ledger — and **all three are PROSE**; the `SYSTEM_MAP` line has **0 pipe characters**. Main's register holds **zero** `N20-` entries. ⛔ A column count cannot be corrected in a row that is not there. ⭐ **Left OPEN.**

## 🔴 UNIT B — **STOPPED PRE-BUILD. ⛔ NO CODE WRITTEN.** B1 completed and it produced the stop.
### B1 — THE INVESTIGATION, END-TO-END (⛔ no grep-only conclusions)
| question | 🔬 answer |
|---|---|
| Where is sector data READ from? | **`core/instrument_cache.py:262-267`** — *"Returns the sector value from **instruments.csv**, or `UNKNOWN` if blank"*; `return row.sector if row.sector else "UNKNOWN"` |
| `sector_cap_mode: observe` vs other | **`capital/risk_engine.py:746`** — gate-8 `SECTOR_EXPOSURE`. **`observe`** logs `risk_engine.sector_cap_would_reject … verdict=WOULD_REJECT` and **CONTINUES**; **`enforce`** returns `reject("SECTOR_EXPOSURE", …)`. `:202` coerces anything else to `observe` |
| who reads `max_sector_exposure_pct` / `delivery_max_sector_exposure_pct` | both `capital/risk_engine.py` — `:151` / `:189`, `:199`, `:331` (the delivery twin) |
| 🔴 **M8 #1 — the EMPTY-DATA PATH, finally read** | 🔴 **SILENT PASS.** `instrument_cache.py:267` blank → `"UNKNOWN"`; `risk_engine.py:352` **RE9** — `sector_lookup_fn` exception → `"UNKNOWN"`, log WARNING, **do not reject**; `:491` defaults `sector="UNKNOWN"`. ⛔ **Not a silent block. ⛔ Not an exception.** |
⭐ **Config line numbers 254 / 255 / 263 VERIFIED to hold at `75e637c`** — M3 satisfied by measurement, ⛔ not by trust.

### ⚠️ AND THE B3 HAZARD IS SHARPER THAN STATED
With no sector data **every symbol lands in ONE `"UNKNOWN"` bucket**, so `effective_sector_margin` accumulates across the **whole book** against a 0.40 cap. ⇒ **Populating sector SPLITS that mega-bucket.** Harmless under `observe` (which only logs) — 🔴 **but it would change entry decisions the instant anyone set `enforce`.** ⭐ **Exactly the F11 β-starvation family, inverted, that B3 warns about.**

### 🔴 THE TWO BLOCKERS
1. **THE DESIGN PREMISE DOES NOT HOLD.** B2 requires **config-driven, ⛔ no hardcoded map in Python** — but the live source is **`instruments.csv`, GITIGNORED** (`.gitignore:17 data_store/`), absent from a fresh worktree, and at a **different path** in the main tree (`./config/instruments.csv`). ⇒ **Does the placeholder populate an uncommittable CSV (which would vanish on a fresh deploy), or introduce a NEW config-driven map?** ⭐ **That is a design decision — PRE-BUILD REVIEW GATE: VERIFY → REPORT → STOP → WAIT.**
2. **THE GATE CANNOT RUN WHERE THE CODE MUST BE BUILT.** B5 needs before/after counts and B6 a full BASE-vs-WORK differential; a **fresh worktree is NOT runnable** — the known 26-phantom-fail hazard, **whose cause is the very file B1 identified**. Building in the main tree instead is the **M3 trap**: 77 commits diverged ⇒ line numbers and regression surface measured at the wrong SHA.

## 🔴 PART 3 — THE STANDING RULES, NOW PERMANENT
**RULE J-1 — A JOIN IS A FAN-OUT UNTIL PROVEN OTHERWISE.** Before ANY aggregate query on a one-to-many table: **1** declare the business **GRAIN** · **2** assert expected cardinality · **3** compare joined rows vs DISTINCT entities · **4** name the duplicate-producing key if they differ · **5** de-duplicate or aggregate **AT** the grain · **6** ⭐ only then calculate.
**RULE J-2 — GRAIN IS PART OF THE NINE-ELEMENT RULE.** Element 1 becomes *population definition **AND GRAIN***.
**RULE M-3 — CORE TEST FOR ACCOUNTING DISCREPANCIES.** A suspected accounting discrepancy is **CORE only when MEASUREMENT shows it changes an actual sizing, reservation, execution, risk or lifecycle decision.** ⛔ Otherwise record and park.
⭐ **Restated standing:** **M-1** measure or search externally before judging · **M-2** core filter before opening any item · the **nine-element rule** · **C-1/C-2/C-3** position-hold notice before 15:00 **with the rupee cost**, and *estimated* ≠ *broker-confirmed*.
⭐ 🔴 **THE OBJECTIVE IS ⛔ NOT ZERO ERRORS IN THE LOG — an error caught BEFORE it changed a canonical decision is a PROCESS FINDING.**

## 🗂️ PART 3 — PRIORITY, CORE ONLY
**P0** live lifecycle windows (⛔ never delayed) · **P1 F2** · **P2 F6 LIFECYCLE** · **P3 F6-leg** · **P4 F4 EXECUTION** · **P5** F11 dead config (removal only) · **P6** S6 (DELIVERY only) · **P7** F9 · **P8** K-1 (⭐ expected to CLOSE) · **P9** carry-dependent (⛔ blocks nothing above). ⛔ **Everything else PARKED.**

### 🔴 F2 ACCEPTANCE IS **BEHAVIOURAL**, ⛔ NOT STRUCTURAL — THE SEVEN, FROZEN BEFORE THE BUILD
1. **A continues while B is stopped** · 2. **B continues while A is stopped** · 3. each uses its **OWN config** · 4. each uses its **OWN capital/reservation calculation** · 5. each has its **OWN limits and counters** · 6. **a halt in one does ⛔ NOT halt the other** · 7. ⚠️ **shared process/service infrastructure does ⛔ NOT convert independence into a single global stop.**
⛔ **Do not call F2 complete because separate config fields or classes exist.** ⭐ `65b7196` **READ as reference only** — ⛔ no code transplant, ⛔ no dependency import. ⭐ Carries **D-3** and **NI-16**.
**F6 — TRACE BEFORE FIXING:** who OWNS the EOD decision · what STATE it reads · what SCOPE it uses · what STOP it issues · ⚠️ whether another pipeline can be affected. ⭐ **THEN** the smallest correction.
**F4 — OBSERVABILITY BEFORE DIAGNOSIS:** ⛔ do not diagnose why CNC fills are low. FIRST **persist at placement**: placement price · quote/reference price · order type · trigger/limit relationship · outcome. ⚠️ **This is the same observability DEFECT B would have needed — done for a CORE reason. ⛔ The provenance benefit is incidental and must NOT reopen DEFECT B.**

## ⏰ PART 4 — SECTION E ARMED, EXPECTATIONS FROZEN TONIGHT
**E-1** service/process state → **E-2** 🔴 **TOKEN FRESHNESS FIRST** (⚠️ a failed refresh is SILENT and ⛔ nothing in cron starts the service; ⛔ do NOT read a missing boot as a resolver failure until the boot precondition is proven) → **E-3** boot occurrence, `STARTUP` row AFTER `ExecMainStartTimestamp`, same non-vacuity discipline → **E-4** bounded resolver search (⛔ absence still will not prove the fix live) → **E-5** `get_holdings` at boot and `carry` at 09:15 — 🔴 **EXPECT ZERO; a NON-ZERO carry is itself a FINDING; ⛔ carry=0 ≠ resolver fix proven** → **E-6** the 45 s morning check, first real cold boot, GREEN/RED **and elapsed** (⚠️ a single RED is ⛔ NOT proof — wait 30 s, re-run) → **E-7** ⭐ **tonight's push gets its boot proof here, and only then may the TREE be considered for advancing — ⛔ not in this file** → **E-8** ⛔ do NOT run CHECK 1 / 2a / 2b / the four-reading series / G3 T+1 against a flat book.
⭐ **THEN** K-1's tolerance test (⭐ expected CLOSE), then **P1 — F2**.

## WHAT I DID NOT MEASURE
⛔ UNIT B's build — **no code written**, blocked at the design question.
⛔ Whether a fresh worktree could be made runnable by copying `instruments.csv` — ⚠️ **not attempted**; copying gitignored data in to make a gate pass risks a false green.
⛔ The 62 remaining untracked audit files — **still uncommitted**; only 2 were pushed.
⛔ K-1's charge arithmetic — **not tonight, by instruction.**
⛔ `docs/SYSTEM_MAP.md` line 784's `M3` re-anchor at `195436b` — ⚠️ **an F2 INVENTORY anchor, ⛔ NOT a rollback target. I deliberately did NOT change it** — advancing it is an F2 scope decision, ⛔ not mine.


---

# FILE 12 — F2 IS ALREADY BUILT. Appended 26-Aug ~20:15 IST. VM clock gated 20:09:02 IST.

## §1 · TONIGHT SHIPPED — AT MEASURED LABELS
⭐ **DEPLOYED `75e637c` → `bc9a9f5`**, fast-forward, ⛔ no force. **1,261 insertions / 0 deletions**, all `.md`. `origin/main` == VM bare HEAD == `bc9a9f5`, **tracked drift 0**.

⚠️ 🔴 **FOUR GIT COMMITS, ⛔ NOT SIX. ⛔ Do not describe A1–A6 as six commits.**
| unit | commit | note |
|---|---|---|
| **A1** | `ae6c344` | rollback TREE `195436b` → `75e637c` |
| **A2** | `ce29d49` | RUNBOOK §9a rollback semantics |
| **A3** | — | ⭐ **CANNOT COMPUTE** — the `N20-14` row does not exist. ⛔ Nothing invented. |
| **A4** | — | `MEMORY_BOARD` re-wrapped; guard clean. ⛔ **Outside repo scope** — no commit exists or should. |
| **A5** | `272d1d4` | seven formal closures |
| **A6** | `bc9a9f5` | today's findings at measured labels |

🔴 **THE GAP THAT WAS ACTUALLY CLOSED:** the entire rollback procedure — RB-2, RB-3, the two-clock rule, L-1, V-7 — existed **ONLY in one local Windows working copy**. `ls` on the VM returned *No such file or directory*. ⭐ **The box where the incident happens did not have the incident procedure.** ⇒ now present, **49,703 B**, RB-3 reading `checkout -f 75e637c`.

🔴 **TWO-CLOCK STATE — AND IT IS CORRECT:**
```
rollback TREE = 75e637c   (last SHA PROVEN TO BOOT)
origin/main   = bc9a9f5   (tonight's documentation push)
```
⇒ ⭐ **`75e637c` ≠ `bc9a9f5` is EXPECTED, ⛔ not drift.** ⛔ **DO NOT advance the TREE to `bc9a9f5`** — ⭐ a push is not a boot. **Only a PROVEN boot of `bc9a9f5` can move it.**

⭐ **ERROR #13 OWNED — the F6 corroboration is WITHDRAWN.** `kept 0/0` means `before = 0`; `rows = get_open_intraday_positions()`; the source states *"EOD6 design mandates DELIVERY (CNC/NRML) positions are never touched."* ⇒ **20MICRONS was NEVER A CANDIDATE** — ⭐ deliberately out of scope, ⛔ not accidentally invisible ⇒ **DESIGN PROPERTY**, ⛔ not an F6 gap. ⛔ **Do not reopen.**

## §2 · 🔴 THE FINDING THAT OUTWEIGHS EVERYTHING ELSE TONIGHT — **F2 IS ALREADY BUILT**
🔬 `feat/delivery-config-split` is **48 commits AHEAD / 77 BEHIND** `origin/main`, **2,122 insertions / 1,025 deletions across 12 files**. Its commits include:
```
feat(sizing)       the allocation model
feat(pipelines)    delivery and intraday become two independent books
refactor(config)!  the caps become intraday_max_*
feat(governor)     the loss limit cuts off one book
```
and **`65b7196` is one of them.**

⇒ 🔴 **THAT IS F2. F2 — THE P1 CORE ITEM — IS ALREADY BUILT AND HAS NEVER BEEN DEPLOYED.** ⭐ One system → two independent books, own config, own caps, own loss governor: **the core requirement, in commit form, sitting on a local branch.**

⚠️ ⭐ **THIS IS THE F12 PATTERN AGAIN — "the already-built answer", rediscovered a FOURTH time, and this time BY ACCIDENT during a documentation push.** ⛔ **It must not be lost again.**

### ⚠️ WHAT IT IS ⛔ NOT — THREE HARD REASONS IT IS NOT PUSHABLE AS-IS
1. ⛔ **77 commits behind** ⇒ a push is **rejected as non-fast-forward**, and `--force` is prohibited.
2. ⚠️ It carries **capital/signal-path commits** needing the FULL gate and **F2's SEVEN BEHAVIOURAL CRITERIA** — ⛔ not a fast-forward.
3. ⚠️ Written against a tree now **77 commits stale** ⇒ ⛔ its line numbers, regression surface and assumptions are measured at the **WRONG SHA (M3)**.

### 🔴 QUEUED FOR TOMORROW — **INVENTORY ONLY. ⛔ NOT STARTED TONIGHT.**
**F-a** list all 48 commits: SHA · subject · files touched; mark which are F2 (allocation, pipeline split, caps rename, governor) and which are not · **F-b** list main's 77 commits since divergence and **name the merge base** · **F-c** 🔴 **THE COLLISION MAP** — which of the 12 branch files ALSO changed in main's 77; ⭐ **that intersection is the real cost and it decides rebase-vs-reimplement.** ⛔ Report it, ⛔ do not decide it · **F-d** against F2's SEVEN criteria, state for each: satisfied / partial / not at all — **from the DIFF**, ⛔ not from commit messages · **F-e** ⚠️ does the branch contain anything main has since **REVERTED or superseded**? ⭐ a 77-commit gap can make old work **actively wrong** · **F-f** ⭐ present options with measured costs — ⛔ **do not pick one.** 👤 **Rama decides:** rebase · cherry-pick the F2 subset · reimplement fresh using the branch as **specification**.
⛔ **Do NOT touch `feat/delivery-config-split`'s working tree — ⛔ no stash, ⛔ no checkout, ⛔ no clean, ⛔ no prune. ⭐ Read it from git only.**

## §3 · 🔴 TERMINOLOGY COLLISION — RECORDED, ⛔ NOTHING FIXED
⭐ There are **TWO DISTINCT `CHECK 1` / `CHECK 2` FAMILIES**, and merging them would be dangerous. 🔬 **All anchors VERIFIED at the deployed SHA `bc9a9f5`** — M3 by measurement, ⛔ not by inferring *"docs-only push ⇒ code unchanged"*.

| family | member | anchor |
|---|---|---|
| **PAIR A — RECONCILER POSITION CHECKS** (set differences, ⛔ **no residual**) | `CHECK 1` `_check1_manual_close` — local OPEN/PARTIAL **vs** broker positions | `orders/order_reconciler.py:1188` |
| | `CHECK 2` `_check2_orphan_adoption` — broker positions **vs** locally tracked | `orders/order_reconciler.py:1790` |
| **PAIR B — G3 CAPITAL-DRIFT CHECKS** (⭐ **this pair produces the residual**) | `_g3_capital_drift` | `orders/order_reconciler.py:3569` |
| | `CHECK 1` — `expected_broker_net` vs `margins.net` | `:3695` — `delta = abs(actual - expected)` |
| | `CHECK 2` — `system_held_capital` vs `margins.used` | `:3702` — `margin_residual = held_today - margins.used` |

⇒ 🔴 ***"CHECK 1"*, *"CHECK 2"* AND *"residual"* MUST NEVER BE READ WITHOUT NAMING THE OWNING SUBSYSTEM.** ⛔ **Do not merge the families.**

### ⚠️ AND IT IS WORSE THAN TWO — A **THIRD** `delta` EXISTS IN THE SAME FILE
🔬 `orders/order_reconciler.py:2566` — `delta=float(broker_qty - local_qty)`.
⇒ ⭐ **That is a QUANTITY delta measured in SHARES**, entirely unrelated to G3's **CAPITAL delta measured in RUPEES** at `:3695`. **One file, one word, THREE meanings.**
⚠️ ⭐ **A bare *"delta"* in any note, alert or card is therefore AMBIGUOUS BY DEFAULT and must carry its owner and its UNIT.** ⭐ This is the same failure family as the capital-vocabulary rule (*label which capital every rupee figure means*).

### 🔴 THE REVERT-TRIGGER COLLISION — RECORDED PRECISELY, ⛔ UNTOUCHED
⚠️ The armed revert trigger's wording **appears to name one family while the evidence cited for it comes from the other.**
⇒ ⭐ **RECORDED with the owning code paths named** (PAIR A `:1188` / `:1790`; PAIR B `:3569` → `:3695` / `:3702`).
⇒ 🔴 ⛔ **DO NOT TUNE · ⛔ DO NOT WIDEN · ⛔ DO NOT SUPPRESS · ⛔ DO NOT CHANGE THE TRIGGER.**
⇒ ⛔ **Do not infer a production defect from a naming collision** until the actual trigger path is traced end-to-end. ⭐ Normal root-cause workflow, ⛔ not tonight.

## §4 · SECTION E — ARMED, ORDER UNCHANGED, EXPECTATIONS FROZEN TONIGHT
**E-1** service/process state · **E-2** 🔴 **TOKEN FRESHNESS FIRST** — ⚠️ a failed refresh is SILENT and nothing in cron starts the service; ⛔ do NOT read a missing boot as a resolver failure until the boot precondition is proven · **E-3** boot occurrence — `STARTUP` row + `event_id` AFTER `ExecMainStartTimestamp`, ⭐ and **not an earlier same-day row (L-1)**; ⚠️ **THIS BOOT IS `bc9a9f5`'s FIRST RUN and is the proof for tonight's push** · **E-4** bounded search for *"NO strategy resolver was supplied"* — ⛔ absence still will not prove the feature live · **E-5** `get_holdings` at boot, `carry` at 09:15 — 🔴 **FROZEN: EXPECT ZERO; a non-zero carry is itself a FINDING; ⛔ carry=0 ≠ carry correctness** · **E-6** the 45 s morning check, first real cold boot, GREEN/RED **and elapsed** — ⚠️ a single RED is ⛔ NOT proof of failure; wait 30 s and re-run · **E-7** ⭐ **only after E-3 proves it** may the TREE be considered for `75e637c` → `bc9a9f5`; ⛔ not before · **E-8** ⛔ do NOT run CHECK 1 / 2a / 2b / the four-reading series / G3 T+1 against a flat book; ⛔ **do not manufacture a carry.**
⭐ **CLASSIFY EVERY RESULT: PASS / FAIL / UNPROVEN. ⛔ Nothing blank.**

## §5 · ORDER OF WORK AFTER SECTION E
1. 🔴 **§2's F2 branch inventory (F-a…F-f)** — ⭐ highest value available. ⛔ Read only.
2. **K-1 tolerance test** (K-a/K-b/K-c) — ⭐ expected to CLOSE. ⛔ Not an audit.
3. ⚠️ **THE 62 UNCOMMITTED AUDIT FILES** — bounded check, ⭐ same class as the gap just closed (`docs/audit/`: **233 on origin/main vs 300 on disk**). ⭐ Classify each ONLY as **OPERATIVE** (a procedure someone would need **at an ssh prompt during an incident**) or **HISTORICAL** (a dated record). ⭐ Report the OPERATIVE list. ⛔ Do not push them. ⭐ If a pattern settles it, **name the pattern** rather than classifying all 62.
   ⚠️ ⛔ **Do NOT call every uncommitted local file a "missing fix."** ⭐ **THREE CATEGORIES STAY DISTINCT: pushed canonical · local memory/control-plane · historical audit deliberately not pushed.**
4. **F9 SOURCE-OF-TRUTH INVESTIGATION** (P7, after the lifecycle work). ⛔ **Do NOT create a second sector-mapping mechanism.** FIRST establish: **A** every reader of sector/instruments data · **B** every writer/update/import path · **C** whether `config/instruments.csv` is authoritative, generated, stale, test-only or unrelated · **D** how production obtains `data_store/instruments.csv` · **E** whether a fresh deployment expects an external/bootstrap data load · **F** what *"config-driven placeholder"* meant in the original design — a versioned mapping that **SUPPLEMENTS** the instrument source, or a mechanism that **SELECTS/CONTROLS** the existing one. ⭐ Only then ask Rama for a design choice, ⛔ and only if one is still genuinely required. ⛔ **No guessing.**
   🔴 `sector_cap_mode` **STAYS `observe`.** ⚠️ With no data every symbol lands in ONE `UNKNOWN` bucket and exposure accumulates across the whole book against the 0.40 cap — ⭐ harmless under `observe` (which only logs), ⛔ **but it would change decisions the instant anyone set `enforce`.**
   ⭐ **M8 instance #1 is ANSWERED: the empty-data path is a SILENT PASS** (`instrument_cache.py:267` · `risk_engine.py:352` RE9 · `:491`) — ⛔ not a block, ⛔ not an exception.
5. Then **P2 F6 lifecycle** → **P3 F6-leg** → **P4 F4 observability** → P5 F11 → P6 S6 → P7 F9.

## §6 · STATE TABLE — CARRY THIS FORWARD
| item | state |
|---|---|
| rollback TREE | **`75e637c`** (last proven boot) |
| `origin/main` == VM bare HEAD | **`bc9a9f5`** · tracked drift **0** |
| `75e637c` boot | **PROVEN** — `STARTUP` 3794 @ 08:15:29.559, after `ExecMainStart` 08:15:18; previous `STARTUP` 3791 was 25-Aug ⇒ **L-1 satisfied** |
| `bc9a9f5` boot | **PENDING** — tomorrow 08:15 |
| 17:35 EOD gate | **PROVEN — PASSED TRIVIALLY** (flat book) |
| pipeline-aware MIS-vs-CNC EOD | **UNPROVEN** — never exercised |
| EOD resolver feature | **UNPROVEN** — ⛔ boot ≠ feature |
| T-6 shadow recorder | **PROVEN** — rc 0, `wrote=5257`, non-vacuous |
| F9 / UNIT B | **BLOCKED PRE-BUILD** — source-of-truth |
| A3 `N20-14` | **CANNOT COMPUTE** — row absent |
| DEFECT B | **PARKED — NON-CORE** |
| A-1 | **CLOSED** |
| carry design | **NOT EXERCISED**, preserved intact |
| 🔴 **F2** | **ALREADY BUILT — 48 commits — UNDEPLOYED** |
| ERRORS | **THIRTEEN owned**, unsoftened |

⭐ **STANDING:** absence of a log line ≠ path not executed · flat book ≠ resolver correctness · boot success ≠ feature correctness · a join is a fan-out until proven otherwise · measure or search before judging · ⛔ non-core reporting must not consume a core-fix window.
⭐ **OVERNIGHT:** service stopped, book flat, cron only. ⛔ **No hourly status noise. ⛔ Do not manufacture work because a loop exists.**

## WHAT I DID NOT MEASURE
⛔ **F-a…F-f — QUEUED, ⛔ NOT STARTED.** No commit list, no merge base, no collision map, no criterion-by-criterion diff reading.
⛔ Whether the branch's F2 work is CORRECT — only that it EXISTS and what its commit subjects and diffstat say.
⛔ The revert trigger's actual code path — ⭐ **the collision is recorded from wording and anchors only; the trigger was ⛔ NOT traced end-to-end and ⛔ NOT touched.**
⛔ Whether main's 77 commits reverted or superseded any branch work (F-e) — **unknown.**
⛔ The 62 uncommitted audit files — **not classified.**
