# ORDER SIZING — THE ALLOCATION MODEL

**Date:** 08-Aug-2026 (Saturday, off-market). Branch `feat/delivery-config-split`.
**Closes:** ChatGPT's §23 A–F, via the ORDER SIZING build card.

## 🔑 COMMITTED LOCALLY — `65b7196` — WITH ITS PRE-COMMIT SCOPE EVIDENCE

📜 **RAMA, 09-Aug-2026, VERBATIM:** *"Approve local commit only, no push/deploy.
Order-sizing discussion should now be frozen."*

⛔⛔ **A LOCAL COMMIT IS A SOURCE-CONTROL CHECKPOINT, ⛔ NOT PERMISSION TO DEPLOY** — and
the *existence* of the commit must never become an assumption that it rides with F6.
**It does not: it carries the v45→v46 migration.**

⭐ **THE SCOPE EVIDENCE IS RECORDED HERE, ATTACHED TO THE COMMIT, BECAUSE A CLEAN WORKING
TREE PROVES NOTHING ABOUT WHETHER THE RIGHT FILES WENT IN.** Checked *before* staging:

| check | result |
|---|---|
| `git diff --check` · `git diff --cached --check` | clean — no whitespace damage, no conflict markers |
| files in the commit | **30** (27 modified + 3 new), all order-sizing / freeze work |
| governor · F6 · GTT · `main.py` | **ABSENT** — `git diff --name-only` matched none of `kill_switch│eod_squareoff│fund_manager│gtt│cnc_gtt│main.py│f6` |
| branch | `feat/delivery-config-split` |

🚦 **`310b8ee` IS A DEPLOYMENT-SAFETY GATE, ⛔ NOT NEW SIZING WORK** — it adds GO/NO-GO
line 9 and touches no sizing logic. ⭐ **The freeze therefore reads as intact: sizing
logic is FROZEN; deployment control may still be strengthened.** It was kept a *separate*
commit so `65b7196` is exactly what was reported.

---

## 🔒 STATUS — PRECISE, ⛔ NOT FLATTERING

> **ARCHITECTURE closed · IMPLEMENTATION complete · REGRESSION clean vs baseline ·
> BROKER VERIFICATION not done · DEPLOYMENT not authorised · PUSHED no ·
> SERVICE untouched.**
>
> ⛔ **BUILT ≠ DEPLOYED ≠ BROKER-VERIFIED ≠ LIVE-ACCEPTED.**

**Test status: `REGRESSION-CLEAN AGAINST BASELINE — NOT ABSOLUTE-GREEN`.**
⛔ *"9 failed / 5,666 passed, failure set byte-identical to baseline"* means **ZERO NEW
FAILURES**. ⭐ It does **NOT** mean the repository is green: **the nine remain known
unresolved failures**, and ⛔ **"PC-env" is a LABEL, not a diagnosis.**

⛔ Nothing in this record has run against a broker. **F6 deploys ALONE on Monday evening;
this build rides with nothing**, and its deployment is a separate decision on a separate day
— now **impossible** to combine rather than merely unwise, because of the schema migration
in §4b.

---

## 0. THE TWO RULINGS THIS BUILD RESTED ON

Both were Rama's, both taken 08-Aug-2026, and the build waited on them.

**① §0.A — THE SIZING MODEL: `Pick 1 (Allocation model)`.**
Under it **the stop % does NOT change the share count — it changes the RUPEE RISKED.**
Same allocation ⇒ same shares; a 2.0 % stop simply risks more money than a 1.5 % stop.
`₹5,833 × 1.5 % = ₹87.50` · `× 2.0 % = ₹116.67`.

**② THE EXPOSURE CEILINGS: rebase onto each segment's own basis, at 20 % / 25 %.** Quoted:

> *"right now intraday's ₹5,833 allocation is being checked against caps measured on
> unlevered total capital, which is comparing two different things … concentration is 10 %,
> while your allocation is 1/6 = 16.7 % of the basis. Those contradict each other by
> construction — the cap will always win and your 58 becomes 10 … Also tell VS Code Claude:
> the position-value cap currently rejects the trade instead of trimming it — it should trim."*

⭐ **The second ruling was not on the card.** It came out of a finding raised before any code
was written: **at the shipped 10 % / 40 % the entire build would have been inert.** See §2.

---

## 1. THE FORMULA AS BUILT

`capital/position_sizer.py`, modified **IN PLACE**. ⛔ No second sizing path, ⛔ no second
leverage term — `leverage_map` is read once, at one site.

```
basis           = segment_bucket × planning_leverage      # 5× MIS, 1× delivery
base_allocation = basis ÷ max_daily_trades                # ⛔ NOT max_open_positions
allocation      = base_allocation × effective_mult        # ⛔ clamped ≤ 1.0
stop_pct        = sl_rupees ÷ entry
risk_budget     = allocation × stop_pct
raw_qty         = risk_budget ÷ sl_rupees                 # ⛔ the RISK FORM, §1.1
final_qty       = floor_to_lot( MIN(candidates) )
final_qty ≤ 0   → REJECT                                  # ⛔ never forced to 1
```

**Coded as the risk form, never `allocation ÷ entry`,** though the two are algebraically
equal. The long form keeps units explicit, works unchanged for a point/ATR stop, and
**prints the rupee risk in the audit line** — which the shortcut silently hides.

### The candidates (§1.2), each naming itself in `limiting_reason`

| candidate | source | on breach |
|---|---|---|
| `ALLOCATION` | the formula above | REJECT at zero |
| `BROKER_MARGIN` | `avail ÷ (entry ÷ broker-reported leverage)` | trim |
| `SEGMENT_CAPITAL` | `avail ÷ (entry ÷ configured leverage)` | trim |
| `MAX_POSITION_VALUE` | `basis × 25 % ÷ entry` | **trim** (was REJECT) |
| `CONCENTRATION` | `basis × 20 % ÷ entry` | trim |
| `MAX_QTY` | a share count; **null = no cap** | trim |
| `FLAT` | flat-mode `flat_value_rs ÷ entry` | trim |

⭐ `BROKER_MARGIN` and `SEGMENT_CAPITAL` are **deliberately not collapsed** (§0.F):
configured leverage is what we PLAN against, the broker's figure is what ADMITS the order.
Told 2× where we planned 5×, the size comes down. ⛔ The levered quantity is never forced.

**Not implemented as qty candidates, and why:** the card lists *strategy
`max_concurrent_positions`* and *pending/contingent reservations* among the step-9
candidates. Both are **category errors in a share-count MIN**:
- `max_concurrent_positions` is a **position COUNT** gate. It is enforced atomically under
  the portfolio lock at `signals/signal_processor.py:645` and binds independently. A count
  cannot cap a share count.
- Pending reservations are **already** in `avail`: `_fm.reserve()`
  (`signal_processor.py:1212/2051/2358`) decrements the bucket, so they reach sizing through
  `SEGMENT_CAPITAL`. See §5 for why §0.C needs nothing further.

---

## 2. THE FINDING THAT CHANGED THE CARD

**At the shipped ceilings the build would have produced nothing.** Both were fractions of
**total capital** while the intraday allocation is a fraction of **buying power**:

| | shipped | at ₹10k | vs a ₹5,833 order |
|---|---|---|---|
| `max_concentration_pct` | 10 % of total | ₹1,000 | caps at **10 shares**, not 58 |
| `max_position_value_pct` | 40 % of total | ₹4,000 | **REJECTS** the order outright |

Delivery was unaffected — its caps already resolved against the ₹3,000 delivery bucket and
its ₹500 allocation cleared both. The asymmetry is exactly that **intraday's basis carries
5× leverage while its ceilings were measured against unlevered capital.**

**After the ruling**, at ₹10,000 total:

| | intraday | delivery |
|---|---|---|
| basis | ₹7,000 × 5 = **₹35,000** | ₹3,000 × 1 = **₹3,000** |
| allocation (÷6) | **₹5,833** | **₹500** |
| concentration 20 % | ₹7,000 | ₹600 |
| position value 25 % | ₹8,750 | ₹750 |

Both ceilings sit **above** the 1/6 = 16.7 % allocation, so **the formula sizes and the caps
only catch an anomaly** — which is what their own config comment always claimed they did,
and did not. `test_shipped_ceilings_never_bind_at_full_size` pins it.

⭐ The auditor's **C2 ladder survives**: 25 % > 20 %, so the catastrophic-loss backstop is
still the looser, outer rail.

---

## 3. §0.D — READ FROM THE CODE PATH, AND ITS PREMISE FAILED

The card asked what the MIS `CO_PLUS_TGT` target leg actually is. **`CO_PLUS_TGT` is not the
live protocol.**

- `orders/order_placer.py:960` discards the per-strategy value: `order_protocol =
  self._default_protocol`.
- `_default_protocol` is hardcoded **`"LIMIT_TRIPLE"`** (`:554`, `:571`). **No
  `default_order_protocol` key exists in `system_config.yaml`** — config cannot reach it.
- Corroborated in-code at `orders/order_protocol_co.py:86-87`: *"CO never used: 805/805
  regular, X6."* `CO_PLUS_TGT` is declared by 12 of 15 strategy YAMLs and inert.

**What the live legs are** (`orders/order_protocol_limit.py:211/382/466`): ENTRY plain LIMIT;
**SL a separate `order_type="SL"` stop-limit on the opposite side**; **TGT a separate plain
LIMIT on the opposite side**. Same product, no `parent_order_id`, no bracket, no OCO —
**three unlinked regular orders, two of them position-reducing.**

⇒ **The answer to "what is the target leg" is: an independent opposite-side order.** Under
the live protocol the SL is independent too. Had `CO_PLUS_TGT` been live the SL would have
been broker-linked inside the CO and **there would be no separate SL order to observe** —
so Monday's four `margins()` readings are coherent only against `LIMIT_TRIPLE`, which is
what actually runs.

🏷️ **`entry_only` remains a LOGGED ASSUMPTION, and its basis is now precise:** there is no
broker-bracket linkage to lean on, so it rests entirely on *"a position-reducing order in
the same product needs no fresh margin."* ⛔ That claim stays **(I)** until Monday's numbers
exist. Monday changes a **constant**, ⛔ not this design.

---

## 4. WHAT THIS BUILD NARROWED — STATED, NOT BURIED

Three deployed behaviours changed as a consequence. None was requested in so many words;
all three follow from §5's prohibitions, and all three are reversible in one line.

1. **`PerformanceAllocator`'s UPSIDE IS CAPPED AT ONE FULL ALLOCATION.** §5 forbids a
   multiplier above 1.0, and the model's core property is that 6 × allocation == the basis
   **exactly**. So `effective_mult = min(1.0, tier × perf_weight)`.

   ⚠️ **CORRECTED — an earlier draft of this record said "the upside is INERT". That
   overstated it.** The clamp is on the **COMBINED** multiplier, not on `perf_weight` alone:
   - **HIGH tier (1.0)** — no headroom, so `max_multiplier: 2.0` really is fully clipped.
   - **MEDIUM (0.7)** — a perf weight up to ~1.43 still raises the size; beyond that, clipped.
   - **LOW (0.5)** — the full `max_multiplier: 2.0` remains usable.

   ⇒ A winning strategy **can still be lifted back up to a full allocation**; what it can
   never do is spend **past** one. `min_multiplier: 0.5` applies in full. Both figures are
   logged (`effective_mult_unclamped` keeps the raw value auditable), and
   `test_the_multiplier_is_clamped_to_one_and_scaling_is_monotonic` pins both arms.

   🟢 **LOCKED 08-Aug-2026 — THE POLICY, IN THESE WORDS:**
   > *"Performance and tier may move a trade's allocation up or down WITHIN the
   > single-allocation ceiling — ⛔ they may never spend a second trade's allocation."*

   ⭐ **This is not a judgement call; it follows from the model.** `6 × allocation = the
   basis, exactly`, so letting one trade exceed one allocation **silently spends a LATER
   trade's slot**, and the phrase *"allocation per trade"* would stop being true. ⛔ No
   longer an open question — the earlier OWED entry is CLOSED.
2. **`risk_per_trade_pct` / `delivery_risk_per_trade_pct` are no longer sizing inputs.** The
   rupee risk is a *consequence* now. **The keys are RETAINED** — the config auditor's C3/C4/C5
   still read them and retiring them is the **owed 06-Aug twin-retirement ruling**, ⛔ not this
   build's to take. They are marked `⛔ INERT for sizing` in the YAML so they cannot be read as
   live.
3. **FIX-133's `max(1, min(tiered, raw*2))` is DELETED.** ⛔ Both halves are forbidden by §5:
   the floor manufactured a 1-lot position out of an allocation that could not afford one
   share, and the 2× cap would let one order spend another's allocation. **`POSITION_VALUE_CAP`
   as a rejection is likewise unreachable** — it trims now.

---

## 4b. 🔴 THIS BUILD NOW CARRIES A SCHEMA MIGRATION (v45 → v46)

**⚠️ NOT IN THE CARD, AND IT CHANGES THE DEPLOY PROFILE. Flagging it loudly.**

**How it was found:** `trades` has REAL columns `qty_by_risk` / `qty_by_capital` /
`qty_by_concentration`, written from the sizing breakdown at `orders/order_manager.py:257`.
Renaming the breakdown keys would have left **three audit columns silently NULL on every
new trade** — a data loss with no error and no alert.

**The choice taken, and the one refused:**
- ⛔ **REFUSED: reuse `qty_by_risk` for `qty_by_allocation`.** A column that survives with a
  CHANGED MEANING makes every historical row uninterpretable — a reader could not tell
  whether a given row's `qty_by_risk` was the old risk budget or the new allocation. That is
  strictly worse than a column that disappears, which fails loudly.
- ✅ **TAKEN: v46 adds 8 new columns and RETIRES the two dead ones in place** (left in the
  table, written NULL from v46). Pre-v46 rows keep their true values.

### THE EXACT COLUMN MAPPING — ⛔ no row may become semantically ambiguous

⚠️ **An earlier draft said "retires the two dead ones" while naming THREE old sizing
columns. That was ambiguous and is corrected here.** Verified against the code, ⛔ not
inferred: the sizer's breakdown keys were enumerated and matched against every `bd.get(...)`
in `orders/order_manager.py`.

**OLD columns — status from v46 onward:**

| column | v46 status | why |
|---|---|---|
| `qty_by_risk` | 🔴 **RETIRED — NULL from v46** | the risk budget is no longer a sizing candidate; the key is gone from the breakdown |
| `qty_by_capital` | 🔴 **RETIRED — NULL from v46** | split into `qty_by_segment_capital` + `qty_by_broker_margin`, which §0.F requires be kept apart |
| `qty_by_concentration` | ✅ **RETAINED — still populated** | ⭐ concentration is **still a live candidate** (the 20 % cap). Same name, **same meaning**, same units. Nothing else carries it. |
| `qty_by_flat` | ✅ **RETAINED — still populated** | flat mode is still a candidate |
| `binding_constraint` | ✅ **RETAINED — populated with the NEW vocabulary** | ⚠️ values change (`allocation`/`segment_capital`/… replace `risk`/`capital`); the column comment records both eras |
| `actual_position_value_rs` | ✅ **RETAINED — unchanged** | still `final_qty × entry_price` |

⇒ **RETIRED = 2** (`qty_by_risk`, `qty_by_capital`). ⭐ **`qty_by_concentration` is NOT one
of them** — the "two dead ones" phrasing was correct in count and misleading in isolation.

**NEW columns — exact meaning of each:**

| column | meaning |
|---|---|
| `planning_basis_rs` | `segment_bucket × planning_leverage` — the rupee buying power the book plans against (₹35,000 intraday / ₹3,000 delivery at ₹10k) |
| `capital_per_trade_allocation` | `planning_basis_rs ÷ the daily-trade cap × effective multiplier` — **the rupee figure that sized this position** |
| `risk_budget_per_trade` | `allocation × stop_pct` — the rupees at risk. ⭐ A **consequence**, ⛔ not a budget that set the size |
| `qty_by_allocation` | candidate qty from the allocation — normally the binding one |
| `qty_by_segment_capital` | candidate qty from the bucket's remaining capital at **CONFIGURED** leverage |
| `qty_by_broker_margin` | candidate qty at the **BROKER's** reported margin. ⚠️ **Equals `qty_by_segment_capital` whenever no adapter answered** — that tie is by construction, not a coincidence |
| `qty_by_max_position_value` | candidate qty from the 25 %-of-basis value cap (**TRIMS**, never rejects) |
| `qty_by_max_qty` | candidate qty from the per-order share cap. **NULL = no cap configured**, ⛔ not a zero-height ceiling |

🔑 **A reader of any row can therefore date it unambiguously:** `qty_by_risk` non-NULL ⇒
pre-v46, risk-budget model. `qty_by_allocation` non-NULL ⇒ v46+, allocation model. **The two
are never both populated**, and `qty_by_concentration` means the same thing in both eras.

🔴 **THE DEPLOY CONSEQUENCE, STATED SEPARATELY FROM THE CODE (`G11`):** this is a `trades`
REBUILD — the same shape as v45's, which dry-ran at 134 ms on a production copy. But the
standing hazard applies in full: **an evening schema push buys a night of CRITICALs**, since
every heartbeat-writing cron trips `_refuse_migration` until the next 08:15 boot migrates.
⇒ **This build must not be pushed in an evening unless that is the deliberate plan.** It is
one more reason it cannot ride with F6.

---

## 5. §0.C — NO NEW MACHINERY NEEDED, AND THE EVIDENCE FOR THAT

The card required that *"the allocator must not hand the same delivery cash to a second entry
merely because the first shows no margin block."* **It already cannot**, for a reason worth
recording: **we never read the broker's margin block for admission.** `_fm.reserve()`
decrements `positional_avail` in our **own** ledger the moment an entry is sized, and the
sizer's `SEGMENT_CAPITAL` candidate reads that same figure.

**(P)** `grep gtt capital/fund_manager.py` → **zero hits**, and that is correct rather than a
gap: a GTT on a held delivery position is a protective SELL against holdings we already own
and whose cash is already in `positional_used`.

---

## 6. C5 RE-RUN — REPORTED, ⛔ NOT SILENCED

Run against the new numbers via `core.config_auditor._group_c_capital_relative`. **C2, C3 and
C4 are silent. C5 and C5b both WARN.** ⛔ Neither the numbers nor the auditor were touched.

| | the auditor's stale formula | recomputed under the allocation model | threshold |
|---|---|---|---|
| **C5** intraday | 6 × 1 % = **6.0 %** of total | ₹87.50 × 6 = ₹525 = **5.25 %** | 4.2 % |
| **C5b** delivery | 6 × 2 % × 30 % = **3.6 %** of total | ₹10 × 6 = ₹60 = **0.6 %** | 1.8 % |

- ✅ **C5 (intraday) — REAL. Classify as `TRUE FINDING`.** ₹87.50 × 6 = **5.25 %** against a
  **4.2 %** threshold. It fired at 5 slots before this build; 6 makes it modestly worse.
  ⭐ **The stale formula does not make the finding false.** ⛔ DO NOT SILENCE IT.
  `5` / `1 %` / `2.10 %` untouched.
- 🔴 **C5b (delivery) — classify explicitly as `KNOWN FALSE — STALE AUDITOR PREMISE`.**
  Real figure **0.6 %**, threshold **1.8 %**; the auditor reports 3.6 %. Its premise — that
  `delivery_risk_per_trade_pct` sizes anything — **was invalidated by this very build**, and
  it will WARN **every morning at boot** about a breach that is not there.
  ⚠️ **This is the *wrongly certain* failure mode, ⛔ NOT the merely missing one — it is
  worse, and it fires daily.** ⭐ Recorded so nobody reads it as a capital breach.
  **OWED: rebase C5/C5b onto `allocation × stop_pct`, or retire them with the
  twin-retirement ruling.** ⛔ Not tuned here — the card forbids it and the classification
  is Rama's.

---

## 7. CONFIG DIFF (§2)

```
position_sizing:
  risk_per_trade_pct              0.01   → 0.01   (unchanged VALUE, now ⛔ INERT for sizing)
  max_concentration_pct           0.10   → 0.20   + base changed: total capital → BASIS
  max_position_value_pct          0.40   → 0.25   + base changed, + REJECT → TRIM
  max_qty                          —     → (new, null = no cap)
  delivery_risk_per_trade_pct     0.02   → 0.02   (unchanged VALUE, now ⛔ INERT for sizing)
  delivery_max_concentration_pct  0.30   → 0.20   + base changed: bucket → BASIS
  delivery_max_position_value_pct 0.40   → 0.25   + base changed, + REJECT → TRIM
  delivery_max_qty                 —     → (new, null = no cap)
risk:
  intraday_max_open_positions        5   → 6
  intraday_max_daily_trades         10   → 6      ⛔ ALSO THE SIZING DIVISOR
  max_open_delivery_positions        3   → 6
  max_daily_delivery_trades          5   → 6      ⛔ ALSO THE SIZING DIVISOR
  max_consecutive_losses             4   → 5   ⛔ NOT the card's 6 — see below
  delivery_max_consecutive_losses    3   → 5   ⛔ NOT the card's 6 — see below
  daily_loss_limit_pct            0.03   → 0.03   (already correct)
  delivery_daily_loss_limit_pct   0.03   → 0.03   (already correct)
```

⚠️ **`max_daily_trades` is no longer a limit that can be tuned in isolation** — it is the
sizing divisor, so moving it moves every position size. Flagged in the YAML at both keys.

### 🔴 THE CARD'S §2 SAID 6/6/6 — AND 6 FOR THE STREAK BREAKER WAS A DEFECT

**Caught by a PRE-EXISTING test**, `test_q9_consecutive_losses_wired.py::
test_production_config_leaves_the_gate_reachable`, which pins
`intraday_max_daily_trades > max_consecutive_losses`.

**The mechanism (P):** the loss streak is **DAY-SCOPED** — `recent_trade_pnls_for_pipeline(
…, today=today)` at `capital/risk_engine.py:386-390`, deliberately, because FIX-183 found a
cross-day streak was a deadlock. So reaching 6 same-day losses needs 6 CLOSED trades, and the
7th entry the breaker would refuse **is already refused by DAILY_TRADES (also 6)**. ⇒ At 6/6
the streak breaker is **dead code on both books**.

**Rama ruled `5`** (asked with the alternatives; the other options were keeping 6/6 and
retiring the gate, or raising daily trades to 7 — which would have silently re-sized every
order, since that number is now the divisor). ⭐ `max_consecutive_losses` is **not** the
divisor, so this costs nothing in sizing. ⛔ **It must stay strictly below the daily-trade
cap**, and both YAML keys now say so.

🔴 **EXPOSURE RISE, STATED PLAINLY.** `max_open_delivery_positions` 3 → 6 **doubles** the
delivery slot count, on top of the ×1.5–1.8 delivery size rise the split already carried.
`delivery_max_consecutive_losses` **3 → 5** *(⛔ corrected: an earlier draft of this record
said 3 → 6 in this paragraph while §7's table said 3 → 5. **Rama ruled 5**; the table was
right and this sentence was wrong.)* — **still a real loosening of a deliberate asymmetry**
(the old comment: *"3, tighter than intraday's 4: a delivery loss takes days to discover"*),
⭐ just a smaller one than the withdrawn text claimed. Both are recorded as increases,
⛔ not as housekeeping.

🔑 **WHY BOTH BOOKS SIT AT 5, AND WHY 6 WAS NOT AVAILABLE:** the streak gate is
**DAY-SCOPED** (`today=today`, `capital/risk_engine.py:386-390`, deliberate since FIX-183 —
a cross-day streak was a deadlock). So ⛔ **any value ≥ the daily-trade cap of 6 makes the
gate UNREACHABLE**: reaching N same-day losses needs N closed trades, and the (N+1)th entry
the breaker would refuse is already refused by DAILY_TRADES. 5 is the largest value that
keeps the breaker alive on both books.

---

## 8. PARITY

⛔ **PAPER CANNOT EXERCISE the part that matters most.** The sizer itself is **pure** — paper
and live resolve every candidate identically, and every test in
`tests/unit/test_order_sizing_allocation.py` is paper-safe. What paper cannot do:

- **prove the broker admits the quantity.** `test_broker_margin_above_the_planning_assumption_reduces`
  proves we obey a margin figure; it proves nothing about what Zerodha charges. That is
  Monday's `margins()` capture — a **measurement**, not a test.
- **exercise a CNC round trip or T+1 settlement.** ⭐ And *paper nets by SYMBOL while live Kite
  nets per (SYMBOL, PRODUCT)*, so a paper drill of any product-semantics change is vacuously
  green.

---

## 8b. THE GATE — MEASURED, SET-COMPARED, ⛔ NOT COUNT-COMPARED

Run from **Git Bash** (⛔ never PowerShell's `bash` — the WSL alias adds ~20 phantom
failures) as `pytest tests/unit tests/integration`, ⛔ never `run_tests.py`.

| run | result |
|---|---|
| **BASELINE** (clean tree, before any edit) | **9 failed · 5,634 passed · 4 skipped** |
| after the code change, before test rework | 75 failed (= the same 9 + **66 new**) |
| **FINAL** (clean single-day run, 09-Aug) | **9 failed · 5,666 passed · 4 skipped** |
| ⚠️ discarded — crossed midnight | 18 failed — ⛔ NOT evidence, see the note below |

⭐ **SET-compared, not counted.** The final failure set is **exactly** the baseline set —
`comm` reports zero new and zero disappeared. The 9 are the known PC-env family
(`test_instance_lock` ×2, `test_main` ×4, `test_fix181`, `test_closure_source_contract`,
`test_phase17_batch2`) and ⛔ **none of them is env** — that label is a description, not a
diagnosis; they were failing identically before this build touched anything.

⚠️ **A FOURTH GATE RUN CROSSED MIDNIGHT AND WAS DISCARDED, ⛔ NOT REASONED FROM.** A
verification run begun late on 08-Aug finished on 09-Aug and reported **18 failed** — 9 more
than baseline. ⛔ **It was not treated as a regression**, because the standing rule says a
regression run must not cross midnight: `_TODAY` is captured at COLLECTION and rows are
dated at EXECUTION, so the boundary corrupts attribution silently. **(P) Re-running those 9
inside a single day: 114 passed, 0 failed.** ⭐ The rule predicted the exact failure and the
exact family — every one of the 9 was date-keyed (`test_pipeline_loss_governor`,
`test_two_pipeline_split`, `test_risk_engine`, the delivery-cap test). A clean single-day run
supersedes it. 🏷️ Recorded because *"18 failed"* sitting in a transcript with no explanation
is exactly how a phantom regression enters the record.

**All 66 were reworked, none silenced.** ⛔ No number was edited without first checking
whether it encoded a property. What the rework consisted of:
- **~30 asserted the OLD MODEL's numbers or keys** (`qty_by_risk`, `raw_qty`, `tiered_qty`,
  constraint `RISK`/`CAPITAL`). Rewritten to the new vocabulary; the dead keys are asserted
  ABSENT so they cannot return with a changed meaning.
- **~12 asserted behaviour §5 ORDERED REMOVED** — FIX-133's floor-at-1 and 2× ceiling, and
  `POSITION_VALUE_CAP` rejecting. **INVERTED and RENAMED**, each carrying why. ⭐ The old §C
  finding (a quantity reaching 2× the tightest arm while the audit column still claimed
  `concentration`) is now pinned as **CLOSED BY CONSTRUCTION**.
- **~14 hard-coded a cap or count** (5/10, 3/5, 0.10/0.40). Where the number was scenario
  SETUP it now derives from the policy (`provider("CNC").max_open_positions`), so a future
  authorised change cannot silently under-seed a test into passing vacuously. Where the
  number IS the thing guarded — the caps drift check — it stays a literal ON PURPOSE.
- **4 were fixture/helper defects** the rewrite exposed: `_assert_bound_by` crashed on a
  `None` candidate (null `max_qty` = "no cap", ⛔ not a zero-height ceiling) and demanded a
  strict unique minimum between `SEGMENT_CAPITAL`/`BROKER_MARGIN`, which are EQUAL by
  construction when no broker answered.

🔑 **THE INTEGRATION FIXTURE WAS ALSO WRONG, AND THAT WAS A FINDING.** `tests/integration/
conftest.py` sized at 10 %/40 %, so every integration signal was CONCENTRATION-bound while
production is ALLOCATION-bound — **the suite was exercising a configuration that exists
nowhere.** Moved to the shipped 20 %/25 %.

⚠️ **Two defects of mine were caught by EXISTING guards, not by me:**
1. **Preflight `F_stale_defaults`** — `PositionSizer.__init__` still defaulted
   `max_position_value_pct=0.40` after config moved to 0.25. Aligned (0.20/0.25).
2. **Preflight `CapsConfigDriftCheck`** went CRITICAL on 6 vs the expected 5. ⭐ It did
   exactly its job: it forced the cap change to be an explicit, authorised edit.

---

## 9. OWED — ⛔ RECORDED, NOT RESOLVED

1. 🔴 **The `PerformanceAllocator` upside** (§4.1) — acceptable, or does the model need a
   separate over-allocation allowance?
2. 🔴 **C5b is now a false alarm** (§6) — rebase or retire, with the twin-retirement ruling.
3. 🔴 **`risk_per_trade_pct` retirement** — the 06-Aug twin-retirement item, now materially
   larger: the key is inert for sizing but still drives three auditor checks.
4. ⚠️ **`REJECTED_SIZING_REJECT_ZERO_QTY_AFTER_ALLOCATION`** is a clumsy derived status
   (`signal_processor` prefixes `SIZING_`, doubling the word "REJECT"). The card names the
   constraint verbatim, so it was kept verbatim rather than silently renamed.
5. ⚠️ **`PipelinePolicy.sizing_base` is now dead to the sizer** but retained, and
   `log_fields()` still prints `effective_risk_pct` — **decorative** since this build. The
   sizer's own audit line is authoritative.

---

## 10. ▶️ RESUME HERE — HANDOFF, 08-Aug-2026 (paused mid-test-rework)

**⛔ NOTHING COMMITTED. ⛔ NOTHING PUSHED. ⛔ SERVICE NOT TOUCHED.**
`HEAD fe94fc3`, branch `feat/delivery-config-split`. **8 files uncommitted:**

```
 M capital/pipeline_policy.py              M core/config_loader.py
 M capital/position_sizer.py               M tests/crash_test/state_machine_validator.py
 M config/system_config.yaml               M tests/unit/test_position_sizer.py
 ?? docs/audit/order_sizing_allocation_build_08aug2026.md   (this file)
 ?? tests/unit/test_order_sizing_allocation.py              (20 tests, ALL GREEN)
```

### DONE — the build itself is COMPLETE and proven
- The allocation model is implemented and `tests/unit/test_order_sizing_allocation.py`
  went **17 RED → 20 GREEN**. Rama's examples reproduce exactly (intraday **58**,
  delivery **5**, ₹501 delivery **REJECTS not 1**).
- `tests/unit/test_position_sizer.py` **fully reworked → 43 passed**.
- Config §2 applied; C5 re-run and reported (§6).

### RAMA'S RULINGS TAKEN TODAY — ⛔ do not re-litigate
1. **§0.A = the ALLOCATION model.** Stop % moves the RUPEE RISK, not the share count.
2. **Ceilings rebase onto each segment's basis at 20 % / 25 %, and the position-value
   cap TRIMS instead of rejecting.**
3. **`max_consecutive_losses` 6 → 5 on BOTH books** (the card said 6). At 6 the gate was
   UNREACHABLE — see the YAML comment; ⛔ keep it below `max_daily_trades`.

### ⏭️ NEXT ACTION — finish the test rework, then re-run the gate
**Gate baseline (measured, Git Bash): 9 failed / 5634 passed — the known PC-env set,
saved at `scratchpad/baseline_failures.txt`. After the change: 75. 66 new = 63
test-maintenance + 2 helper/trigger + 1 real (the 6/6 defect, now RULED).**

⛔ **RUN THE GATE FROM GIT BASH ONLY** (PowerShell's `bash` is the WSL alias ⇒ +20
phantom failures) and **SET-compare**, ⛔ never compare counts.
⛔ **CAPTURE FULL OUTPUT — do NOT pipe through `tail`.** That truncation already
invalidated one comparison this session (75 failures, 59 captured).

**Remaining files to rework (~43 tests), with the failure shape already clustered:**

| file | n | shape |
|---|---|---|
| `tests/integration/test_q9_sizing_floors_caps_wired.py` | 16 | 4 assert REMOVED behaviour (2× ceiling, position-value REJECT); its `_assert_bound_by` helper (`:249`) crashes on the `None` value of `qty_by_max_qty`/`qty_by_flat` — **None is the honest "no cap"; fix the helper to skip it** |
| `tests/unit/test_two_pipeline_split.py` | 6 | old 5/10 and 3/5 limits; one asserts `sizing_base` |
| `tests/unit/test_mc6_zero_multiplier_skip.py` | 4 | `KeyError: tiered_qty` — key GONE, not renamed |
| `tests/unit/test_fix066_entry_offset_margin.py` | 4 | old numbers (`assert 500 == 70`) |
| `tests/unit/test_diary4_tier_multiplier.py` | 4 | flat mode now a CANDIDATE (`'FLAT' == 'BELOW_MIN'`) |
| `tests/unit/test_config_auditor.py` | 4 | assert the old 10 % / 40 % |
| `tests/unit/test_position_sizer_delivery_scaffold.py` | 3 | scaffold semantics |
| `tests/unit/test_intraday_cap_rename.py` | 2 | assert 5 / 10 |
| `tests/unit/test_preflight.py` · `test_fix133_dynamic_sizing.py` | 2 | fix133 asserts the DELETED 2× ceiling |
| `tests/integration/test_q9_consecutive_losses_wired.py` | 1 | ⭐ **should now PASS** — the 6→5 ruling fixed it |

**Method that worked, reuse it:** rewrite each test to assert the NEW behaviour with
its rationale in the docstring; where a test back-solved a quantity out of the dead
risk formula, pin it with **`max_qty`** instead. ⛔ **VERIFY THE PROPERTY BEFORE
EDITING ANY NUMBER** — several of these numbers encode a property, not a value.

### 🔴 STILL OWED RAMA (all recorded in §9, none resolved)
1. **PerformanceAllocator's upside is now inert** (`max_multiplier: 2.0` clipped to 1.0).
2. **C5b is now a FALSE alarm** — its premise died in this build.
3. `risk_per_trade_pct` retirement (the 06-Aug twin-retirement item).

### ⛔ UNCHANGED BY THIS WORK
**F6 still deploys ALONE Monday evening ⇒ first live Tue 11-Aug 08:15.** This build
rides with NOTHING. The nightly manual stop still stands.
