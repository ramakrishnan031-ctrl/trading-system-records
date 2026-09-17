# MONDAY 10-Aug-2026 — THE WRITTEN EXPECTATION, RECORDED BEFORE THE BOOT

**Written 07-Aug-2026 (Friday) 18:4x IST · clock via PowerShell `Get-Date` = `2026-08-07 18:42:27 +05:30`.**
**⛔ READ-ONLY. NO CODE. NO CONFIG. NO GTT CANCELLED. NOTHING AUTHORISED TO CHANGE.**

> ## 📄 WHY THIS IS A STANDALONE CARD AND NOT §9 OF THE VERIFICATION REPORT
> The anti-duplication rule binds against a **parallel document on the same subject**. This is not
> that: the verification report is a *retrospective* that is finished, and this is a *forward*
> artifact with a lifecycle — **write, then score**. It has to be findable at 08:00 on Monday and
> re-opened that same morning; as §9 of a ~50 KB report it would be neither.
> **Precedent:** `MONDAY_POST_SESSION_CHECKLIST.md` · `THURSDAY_CONTINGENCY_06-Aug-2026.md` ·
> `FRIDAY_MORNING_07-Aug-2026.md` — the campaign already keeps dated day-cards standalone.
> ⛔ **§2's seven adoptions do NOT go here** — each goes to its existing home (§7 below).

> ## 🧪 PARITY, STATED RATHER THAN ASSUMED
> **Everything below is a LIVE-ONLY path.** Delivery/CNC, broker GTTs, `holdings()`/`positions()`
> settlement behaviour and the `cnc_gtt_monitor` ladder have **no paper analogue that could produce
> these observations**: paper nets by *symbol* where live Kite nets per *(symbol, product)*, and the
> paper adapter has no T+1 settlement model at all. ⛔ **No paper claim is made, and a paper drill of
> any of this would be vacuously green.** *(All 24 retained daily logs read `mode=live`.)*

---

# §0 · THE STATE THIS PREDICTS FROM — every operand quoted

| fact | value | source |
|---|---|---|
| GTT under prediction | **`330944932`** · DIFFNKG · `active` · SELL/SELL · CNC/CNC · triggers **`[437.2, 459.45]`** · created `2026-08-07 15:20:35` | `kite.get_gtts()` |
| DIFFNKG holdings | **`quantity=0`, `t1_quantity=0`, `realised=0`** | `kite.holdings()` |
| DIFFNKG positions | **CNC `net=-1`, `buy=0`, `sell=1`** | `kite.positions()` |
| the actual sale | order `260807170745584` SELL CNC LIMIT, **`filled=1`, `COMPLETE`, `2026-08-07 14:50:52`, `average_price = 437`** | `kite.orders()` / `kite.trades()` |
| Friday last traded price | **`441`** *(Friday OHLC open `453.9` · high `453.9` · low `432.8`)* | `kite.quote(["NSE:DIFFNKG"])` |
| the DB row | `trd_010f8e21…` **`OPEN`**, `exit_time` NULL, created `2026-08-06 10:02:16` | `trades`, `mode=ro` |
| the respawn chain | `330658430` TRIGGERED *(→ the 14:50:52 fill)* → `330940420` created `15:05:26`, TRIGGERED `15:08:11` → `330944932` created `15:20:35`, **ACTIVE** | `gtt_state` + broker |

**THE MECHANISM, quoted from source** — `orders/cnc_gtt_monitor.py:457-464`:

```python
        for p in positions:
            product = ... ;  if str(product).upper() != "CNC": continue
            ...
                held[sym] = held.get(sym, 0) + abs(int(qty))     # ← :464 — F6
```

⇒ **today** `held["DIFFNKG"] = 0 (holdings) + abs(-1) (positions) = 1`, which equals `row_qty = 1`, so
`_handle_row` lands on **branch 2** (`present_active and held == row_qty`) and returns `healthy`.
**That is why it is sitting there rather than being cleaned up.**

---

# §1 · THE PREDICTIONS · ⛔ each with its falsifier

**Buckets:** **(a)** CONFIRMED DEFECT · **(b)** CONFIRMED DESIGN · **(c)** ASSUMPTION DISPROVED ·
**(d)** CANNOT DETERMINE. **Evidence:** **(P)** it happened · **(S)** the code says so · **(I)** inferred.
🏷️ **Evidence-STRENGTH tags use the prefix `X` — `X1/X2/X3+`** for one / two / three-plus independent
sources. *(⛔ Deliberately not `E1–E3`: this card already uses `E1–E6` for the predictions themselves.
The collision is named in §2.6 and this is the resolution.)*

---

## E1 — DOES THE FRIDAY STOP HAPPEN?

### 🏁 **NOT A PREDICTION — ALREADY RESOLVED. THE STOP RAN.** **(P)** · **X3+**

⭐ **The card that commissioned this was written before the stop; it has since been executed by Rama
at `18:36:44 → 18:36:48` on 07-Aug and verified.** Recording it as measured rather than writing a
prediction for a settled fact.

| evidence | reading |
|---|---|
| unit state | `ActiveState=inactive · SubState=dead · Result=success · ExecMainStatus=0 · NRestarts=0` |
| journal | `Stopping 18:36:44` → `Deactivated successfully 18:36:48` → `Stopped 18:36:48` |
| app log | `Shutdown complete 18:36:48.353`; WAL `checkpointed=362 busy=0` |
| (d) at 86 s | still `inactive`; `token_watcher.log` last line still `[2026-08-07 08:15:27]` ⇒ **no start attempt** |
| census | **55 lines**, `BEGIN day=2026-08-07 mode=live entries=70` … `MISMATCH: NONE` … `END mismatches=0` |

> ### ⇒ **THE `STOPPED` BRANCH IS LIVE. Monday's 08:15 boot WILL run, and E2–E5 are therefore reachable.**
> ⛔ **The `NOT STOPPED` branch is recorded as dead, not deleted:** had the stop not run, there would be
> no boot, the routine `15:15 SOFT_KILL` would persist, **Monday would take no entries**, and **none of
> E2–E5 would occur** — the GTT would simply rest, unexamined, into Monday's market hours.
> ⭐ **That branch is exactly the one that made the stop doubly load-bearing**, and it is now closed.

---

## E2 — 🔑 AT MONDAY'S 08:15 BOOT, WHAT DOES `held` COMPUTE TO FOR DIFFNKG?

### 🎯 **PREDICTION: `held = 0`.** **(P)** grounded in the ATULAUTO precedent · **X2**

**Reasoning, and the two things it rests on:**
1. **(S)** `held` is built from `holdings()` + CNC rows of `positions()` (`:451-464`). DIFFNKG's holding
   is already `quantity=0, t1_quantity=0` and contributes **0** whether or not the row persists.
2. **(P)** the `-1` CNC row lives in the **day** position book, and that book is empty pre-market.

> ### ⭐ **THE PRECEDENT IS DIRECT, AND IT IS THE STRONGEST EVIDENCE HERE — `positions()` RETURNED `0 positions` AT THE ATULAUTO BOOT**
> **(P)** at `2026-08-07T08:15:41.516` and again at `…41.655`:
> `get_positions call_end … result_summary:"0 positions"` — **twice, pre-market, on the T+1 morning
> after ATULAUTO's sale.** ⭐ **And it returned zero for the WHOLE BOOK, not just ATULAUTO** — so this
> is a property of the day-book rollover, not a symbol-specific accident. `held` therefore reached 0,
> branch 4 fired, and the GTT was deleted.

### ⚠️ **THE CARD ASKED WHETHER THE PRECEDENT MATCHES. IT MATCHES ON THE DIMENSION THAT GOVERNS AND DIFFERS ON ONE THAT DOES NOT — BOTH STATED**

| | ATULAUTO | DIFFNKG |
|---|---|---|
| sale | 06-Aug **09:31:56** | 07-Aug **14:50:52** |
| next boot | 07-Aug **08:15:41** | 10-Aug **~08:15** |
| **wall-clock interval** | **22 h 43 m 45 s** | **≈ 65 h 24 m** — **2.88× longer** |
| nights crossed | 1 | 3 (a weekend) |
| **structural relation** | **boot occurs PRE-MARKET on the T+1 settlement day, after ≥1 day-book rollover** | **IDENTICAL** |

> ⇒ **The intervals are NOT the same and the card was right to insist on the check.** But the governing
> variable is *"has the day book rolled over before the boot reads it"*, and on that the two cases are
> the same, with DIFFNKG having **more** rollovers, not fewer. **The difference is in the direction that
> adds margin.** ⛔ It is still a **one-instance** precedent (`X2` only because source + precedent agree),
> and a weekend settlement is not something this system has been observed through before.

**⛔ FALSIFIER — any one of these refutes E2:**
- `get_positions` at Monday's boot returns a DIFFNKG CNC row (any sign) ⇒ **E2 FAILED**, `held ≥ 1`.
- `holdings()` returns DIFFNKG with `quantity > 0` or `t1_quantity > 0` ⇒ **E2 FAILED**.
- The boot log shows `cnc_gtt_monitor` returning `healthy:DIFFNKG` instead of `gtt_exit` ⇒ **E2 FAILED**.

---

## E3 — IF `held` REACHES 0: THE SEQUENCE, AND THE PRICE

### 🎯 **PREDICTION: the ATULAUTO sequence repeats line for line.** **(S)** + **(P)** · **X2**

Predicted, in the ATULAUTO form so it can be compared directly *(`:501-508` → `:526-595`)*:

```
cnc_gtt_monitor.forensic   … "GTT active but holding flat (external close)"   [orphan_active_gtt_flat]
delete_gtt call_end        … gtt_id:"330944932", mode:"LIVE"
cnc_gtt_monitor.gtt_exit   … trade_id:"trd_010f8e21…", exit_price:<X>, pnl:<Y>, reason:"GTT_EXIT"
⇒ trades.trd_010f8e21… → CLOSED, exit_reason='GTT_EXIT', gtt_state 330944932 → CLEANED
```

### 🔴 **THE EXIT PRICE — PREDICTED SOURCE, AND IT IS RUNG 2**

**(S)** `_resolve_exit_price` is a three-rung ladder: **broker `get_trades()` matching the exit side →
`get_quote()` LTP → `entry_price` proxy.**

> **🔑 RUNG 1 WILL MISS.** `get_trades()` is the broker's **DAY** trade book. The DIFFNKG sale is a
> **Friday** trade; on Monday it is not in Monday's tradebook. **(P)** it is in *today's*:
> `TRADE: 2026-08-07 14:50:52 SELL 437 1`. On Monday that list will not contain it.
> ⇒ **the exit price will be resolved from RUNG 2, the LTP.**

**⇒ PREDICTION: the P&L written on Monday will be WRONG, and OVERSTATED (too favourable).**

**The mechanism, and the sign, with the operands quoted and no figure invented:**
- the **real** sale price is **`437`** *(measured)*;
- Friday's **last traded price is `441`** *(measured)*, and at 08:15 Monday — before pre-open — that is
  what a quote returns;
- `441 > 437` ⇒ the booked exit exceeds the true exit on a **LONG** ⇒ **P&L overstated / the loss understated.**

> ### ⭐⭐ **AND THE SIGN IS SYSTEMATIC, NOT LUCK — IT IS SET BY *WHICH LEG* FIRED**
> A **stop** leg fires at the local low of an adverse move; a **target** leg fires at a local high. Any
> later proxy price is therefore biased **above** a stop fill and **below** a target fill. ⇒
> **stop-triggered delivery exits systematically OVERSTATE P&L; target-triggered ones systematically
> UNDERSTATE it.** DIFFNKG's `437.2` is the **stop** leg.
>
> **(P) THE ATULAUTO PRECEDENT CONFIRMS BOTH THE MECHANISM AND THE SIGN:** its triggers were
> **`[575.65, 605.0]`** — the **stop** leg fired; every post-sale LTP that day read **577.45 → 582.0 →
> 582.05**, all **above** the stop; and the price booked at the next boot was **`579.55`**, ~**3.9 above
> the stop trigger.** ⭐ **Same leg, same sign, and a near-identical gap to DIFFNKG's `441` vs `437`.**
> ⚠️ **Stated honestly: ATULAUTO's exact fill price is not in the retained record** — only its trigger
> and the surrounding LTPs — so the ~3.9 is measured against the **trigger**, not against a fill.

**⛔ FALSIFIER:**
- booked `exit_price` == `437` ⇒ **E3's price limb FAILED** (rung 1 somehow resolved, or Kite's day
  tradebook is not day-scoped as assumed).
- booked `exit_price` < `437` ⇒ **the SIGN is FAILED** (P&L understated, not overstated).
- The sequence emits `_reprotect` / `qty_mismatch` instead of `forensic → delete_gtt → gtt_exit` ⇒
  **E3's sequence limb FAILED.**

---

## E4 — IF `held` DOES *NOT* REACH 0: DOES A FOURTH DIFFNKG GTT APPEAR?

### 🎯 **PREDICTION: NO — no fourth GTT at the boot.** **(S)** · **X1**

### 🔴 **AND THIS CORRECTS THE CARD'S PREMISE, WHICH IS THE MOST USEFUL THING IN E4**

The card states *"branches 1–4 fail and `:513` fires `_recreate`."* **That is the ladder for a GTT that
is MISSING. `330944932` is PRESENT and `active`,** so the walk is different — traced at `:485-521`:

| branch | condition | with `held=1`, `row_qty=1`, GTT present+active |
|---|---|---|
| 1 | `triggered` | ⛔ no — status is `active`, not `triggered` |
| **2** | `present_active and held == row_qty` | ✅ **TRUE — returns `healthy:DIFFNKG`, and the walk STOPS HERE** |
| 3 | `held > 0 and held != row_qty` | never reached |
| 4 | `held == 0` | never reached |
| 5 | `held == row_qty` → `_recreate` @ `:513` | **never reached** |

> ⇒ **If E2 fails, the monitor does NOTHING — it books the phantom as `healthy` and touches
> `touch_gtt_state_verified`. No fourth GTT.** ⭐ **A fourth GTT requires branch 1: `330944932` must
> TRIGGER while `held` still reads > 0** — which is precisely how GTTs three and two were born
> (`_reprotect`, `why="F6: GTT triggered but holding still > 0"`, at `15:05:26` and `15:20:35`).
> ⚠️ **That is arguably worse than a fourth GTT**: a silent `healthy` on a position that does not exist
> is the defect reporting itself as correct.

**⛔ FALSIFIER:** a `cnc_gtt_monitor.recreated` line for DIFFNKG at the boot, or a 4th `gtt_state` row,
with `held ≠ 0` ⇒ **E4 FAILED.**

---

## E5 — 🔴 IF `330944932` TRIGGERS, DOES A REAL SELL ORDER REACH THE MARKET?

### 🏷️ **(d) CANNOT DETERMINE — and I am not going to reason it into an answer.** **X1**

**⭐ FIRST, THE STRUCTURAL POINT THAT MOST REDUCES THE RISK, AND IT FOLLOWS FROM E1+E2:**

> **If E2 holds, `330944932` is DELETED at ≈08:15 — a full hour before the 09:15 open.** The GTT
> therefore never gets the chance to trigger on Monday at all, and **E5 is never tested.**
> ⇒ 🔑 **E5 becomes live ONLY if E2 FAILS.** The risk chain is
> **`E2 holds → deleted pre-open → no exposure`** versus **`E2 fails → healthy (E4) → the GTT rests into
> market hours → E5 is live`.** ⭐ **This is also exactly why the Friday stop mattered: no stop ⇒ no boot
> ⇒ no 08:15 monitor cycle ⇒ no deletion. That branch is now closed (E1).**

**WHAT IS ESTABLISHED (P):**
- `330940420` **TRIGGERED at the broker at `15:08:11`** on 07-Aug, when the holding was already flat.
- **NO corresponding order exists in the broker's order book.** *(Width: the complete `kite.orders()`
  list for the day — **21 orders** — filtered to DIFFNKG yields **exactly one**, the `14:50:52` COMPLETE sell.)*
- **Our system logged NOTHING at `15:08:11`** — the trigger was purely broker-side; the next action was
  `_reprotect` at `15:20:35`.
- A GTT trigger on the **same symbol 18 minutes earlier**, when the holding **did** exist
  (`330658430` → `14:50:52`), **did** produce a visible order. ⇒ GTT-triggered orders *do* surface in
  `orders()` when they succeed *(and untagged — every tagged order in the book carries a `trd_…` tag from
  our own placer; the DIFFNKG sell carries none)*.

**WHY THAT STILL DOES NOT SETTLE IT — the discriminator was run and came back empty:**

> **(P)** today's order book is `{CANCELLED: 11, COMPLETE: 10}` — **ZERO `REJECTED` orders, of any
> symbol.** ⇒ **there is no instance in the record of Kite surfacing a rejection**, so I cannot show
> that a rejected GTT-triggered order *would* have appeared. The absence at `15:08:11` is therefore
> consistent with **both**:
> - **(i)** the broker rejected at trigger-time validation and created no order record; **and**
> - **(ii)** an order object exists that `orders()` does not surface.
>
> ⛔ **I cannot distinguish (i) from (ii) from the retained record.** ⚠️ **And the distinction is the
> whole risk: (i) is a stale object; (ii) is a live sell order for shares the account does not own.**
> ⭐ **It would be settled by exactly one observation — the next time a triggered GTT meets a zero
> holding — which is what Monday may supply.**

**⛔ FALSIFIER / WHAT TO CAPTURE IF IT HAPPENS:** if `330944932` triggers on Monday, capture
`kite.orders()` **immediately** and record whether a DIFFNKG SELL appears **in any status** — that single
observation converts this (d) into a determination, in whichever direction.

---

## E6 — WHERE IS DIFFNKG RELATIVE TO `437.2` AND `459.45`?

### 🏷️ **(P) MEASURED — the stop leg is well within reach; the target leg is not.** **X1**

Quoted from `kite.quote(["NSE:DIFFNKG"])`, Friday close of business:

| | value | gap from LTP `441` | arithmetic |
|---|---|---|---|
| **last traded price** | **441** | — | — |
| **stop trigger (lower)** | **437.2** | 🔴 **−3.80 = −0.862 %** | `441 − 437.2 = 3.80`; `3.80 / 441 = 0.862 %` |
| **target trigger (upper)** | **459.45** | **+18.45 = +4.184 %** | `459.45 − 441 = 18.45`; `18.45 / 441 = 4.184 %` |
| Friday low | **432.8** | — | 🔴 **BELOW `437.2` — the stop level was TRADED THROUGH on Friday** |
| Friday open / high | **453.9 / 453.9** | — | below the `459.45` target |

> ### 🔴 **⇒ THIS IS A REACHABLE TRIGGER, NOT A THEORETICAL ONE.** A **0.86 %** move down hits the stop,
> and Friday's own low already went **below** it. The target at **+4.18 %** is comparatively remote and
> Friday never traded above `453.9`. ⇒ **the leg that matters on Monday is the STOP leg**, which is also
> the leg whose exit-price error is **overstating** (E3).

---

# §2 · SCORING INSTRUCTIONS — ⛔ READ BEFORE TOUCHING ANYTHING ON MONDAY

1. ⛔ **Score E2–E6 BEFORE any fix, any cancellation, and before any explanation is offered.**
2. ⛔ **Do NOT amend a prediction after the fact.** A failed prediction is the valuable outcome —
   **P3 failed on 07-Aug and it reversed the F6/Ruling-2 sequencing for the better.** A clean sweep
   teaches nothing about the predictor.
3. Capture first, interpret second: the boot's `get_positions` / `get_holdings` result summaries, every
   `cnc_gtt_monitor.*` line, the `gtt_exit` `exit_price`, and `kite.get_gtts()` — **to a file, then filter.**
4. ⭐ **E5 is the one that can only be scored if it happens.** If `330944932` is deleted at 08:15 as E2
   predicts, record E5 as **NOT TESTED** — ⛔ not as passed.

## §2.1 — THE SCORING TABLE · ⛔ **ONE ARTIFACT, NOT TWO**

*(Review points 2.8 and 3.7 asked for the same thing in different words — a post-Monday score sheet and
a prediction/observation table. **They are built ONCE, here.** ⛔ Do not also produce a separate
"post-Monday report".)*

> ### ⭐⭐ **CONFIDENCE AND EVIDENCE WIDTH ARE FROZEN TOO — filled in BEFORE Monday.**
> ⛔ **Without this a correct LOW-confidence prediction and a correct HIGH-confidence one score
> identically, which destroys the one thing the exercise measures.** 🏷️ **This is an ADDITION to the
> scoring frame, ⛔ not an amendment to any prediction — §2.2's freeze permits it and must not be used
> to block it.** *(Confidence recorded 07-Aug night; ⛔ it may not be revised after observation begins.)*

> ### 🆕 **OUTCOME — THREE STATES, ⛔ NEVER TWO. Added 08-Aug-2026.**
> **Every row scores exactly one of: `PASS` · `FAIL` · `NOT TESTED / NOT APPLICABLE`.**
> ⛔ **NEVER force a non-test into a `FAIL`.** ⭐⭐ **The distinction is between *"we looked and it did
> not happen"* and *"we did not look."* The first is EVIDENCE; the second is a GAP** — and collapsing
> them is how a gap acquires the authority of a measurement.
> 🔑 **Two live examples already exist, and BOTH would read as failures under a two-state rule:**
> **① E5 unfired is `NOT TESTED`, ⛔ never `PASSED` and ⛔ never `FAILED`** — if the GTT is deleted at
> the 08:15 boot before any trigger path is reached, that IS its correct outcome.
> **② the ABSENCE of a shutdown census at the boot is NOT a failed census** — **the census is a
> *SHUTDOWN* stage, not a boot stage** (§3.1b), so its absence is `NOT APPLICABLE`.
> ⚠️ **② is the dangerous one: on the morning of a deploy it would look like a broken boot.**
> 🔑 **A `NOT TESTED` with its reason recorded SATISFIES gate line 2 of `GO_NOGO_f6_deploy.md`. ⛔ A
> BLANK does not.** ⭐ That is the whole reason this block exists: at 18:30 Monday, *"is E1–E7
> scored?"* must be answerable without improvising a judgement on a live deploy.
> 🏷️ **An ADDITION to the scoring frame. ⛔ No prediction's wording, confidence, width or offset is
> touched — §2.2's freeze permits this and must not be used to block it.**

> ### 🆕 **PROVENANCE — fill this for EVERY finding, ⛔ including unexpected ones. ⚠️ EXTENDED 08-Aug-2026: FOUR PHASES, NOT THREE.**
> ~~`BEFORE` · `WEEKEND` · `BOOT`~~ **stopped at Monday morning** — ⛔ **the deployment and Tuesday were
> not in it.** **Every finding is exactly one of:**
> **`PRE-EXISTING`** *(existed before the weekend)* · **`MONDAY-BOOT`** *(introduced by the 10-Aug
> boot)* · **`DEPLOYMENT-TRANSITION`** *(introduced by the Monday-evening stop/push/verify window)* ·
> **`F6-FIRST-LIVE`** *(introduced by the Tue 11-Aug 08:15 boot, the first on the new code)* ·
> **`UNKNOWN`**.
> *(Weekend-intervention findings map to `PRE-EXISTING` unless an intervention is identified — and
> under the weekend policy there should be none.)*
> ## ⭐⭐ **THE REASON IS SPECIFIC: AFTER TUESDAY, EVERYTHING ANOMALOUS WILL LOOK LIKE F6 — BECAUSE F6 IS WHAT CHANGED.**
> 🔑 **A label applied BEFORE the deploy is the only thing that can later say *"this was already
> there."*** ⭐ The Friday-night baseline + state fingerprint (`857258db…`) and the frozen
> before-snapshot exist precisely to make this answerable.
> ⛔ **`UNKNOWN` MUST STAY AVAILABLE — forcing a label is how a LATENT defect gets attributed to the
> change that merely REVEALED it.** ⛔ Without the split every finding defaults to whichever phase
> everyone is watching.

| Prediction | 🔒 CONFIDENCE | 🔒 EVIDENCE WIDTH | 🔗 **DEPENDS ON** | Observed | 🆕 **OUTCOME** *(PASS · FAIL · NOT TESTED/NA)* | 🆕 **PROVENANCE** | Root cause | Architecture impact | Action |
|---|---|---|---|---|---|---|---|---|---|
| **E1** stop ran ⇒ boot runs | **CERTAIN** *(not a prediction — measured)* | **X3+** — unit state · journal · app log · census | — *(already resolved)* | | | | | | |
| **E2** `held = 0` | **HIGH** | **X2** — source (`:451-464`) + **one** precedent, ⛔ never across a weekend | 🔑 **`SD-1`** + boot stages 1-12 | | | | | | |
| **E3a** sequence `forensic → delete_gtt → gtt_exit → CLOSED` | **HIGH** | **X2** — source ladder + the ATULAUTO trace | 🔑 **`SD-1`** *(via E2)* + stages 13-15 | | | | | | |
| **E3b** exit price from **LTP**, P&L **OVERSTATED** | **MEDIUM-HIGH** *(the mechanism is HIGH; the SIGN depends on Monday's open)* | **X2** — `_resolve_exit_price` + ATULAUTO's `579.55` vs stop `575.65` | **E3a firing at all** *(no exit ⇒ no price)* | | | | | | |
| **E4** **no** fourth GTT (branch 2 `healthy`) | **HIGH** | **X1** — source trace only; ⛔ **never observed**, this branch has no precedent | 🔑 **`SD-1` INVERTED** — E4 is the `held = 1` branch | | | | | | |
| **E5** order on trigger — **CANNOT DETERMINE** | **N/A — a declared non-prediction** | **X1** — one ambiguous event (`15:08:11`) | **E2 FAILING** *(if E2 holds the GTT is deleted pre-open and E5 is NOT TESTED)* | | | | | | |
| **E6** stop leg reachable (−0.862 %) | **CERTAIN** *(arithmetic on a quoted quote)* | **X1** — one quote read | — *(market data only)* | | | | | | |
| 🆕 **E7** MANINFRA untouched *(NEGATIVE CONTROL — §3.8)* | **HIGH** | **X2** — source (branch 2) + **(P)** its state is correct at the broker | **INDEPENDENT of `SD-1`** ⭐ — its `+4` is a genuine long, so no settlement residue is involved | | | | | | |

> ### 🔑 **READ THE DEPENDS-ON COLUMN BEFORE SCORING THREE ROWS RED.**
> **E2, E3a and §11.6's candidate 6 all hang on `SD-1`** *(whether a Friday CNC SELL's `-1` day-book row
> is gone by Monday's pre-market `positions()` read — see report §12)*. ⛔ **They do not fail
> independently; they fail TOGETHER, from ONE root cause.** ⭐ A scorer seeing three reds must record
> **one** finding, not three — and the DEPENDS-ON column is what makes that visible from the table
> itself rather than from a paragraph elsewhere.
> ⭐⭐ **And note the two rows that are structurally different: E4 depends on `SD-1` being WRONG** (it is
> the `held = 1` branch), **and E7 does not depend on `SD-1` at all.** ⇒ **E7 is the only row that
> stays interpretable whichever way `SD-1` resolves** — which is precisely what makes it a control.

⭐ **Read the confidence column against the outcome, not instead of it.** A **HIGH** that fails is worth
more than a **MEDIUM** that fails; an **X1** that holds is weaker evidence than an **X3+** that holds.
🔴 **E4 is the one to watch: HIGH confidence on X1 width** — that combination is exactly where this
campaign has been wrong before *(P3 was confident and narrow)*.

⛔ **This is GOVERNANCE EVIDENCE, not incident history.** The last two columns are the point: a row whose
*Architecture impact* and *Action* are blank has not been scored, it has merely been narrated.
⭐ **Add a row for any UNEXPECTED observation** — something true on Monday that no prediction covered is
worth more than a confirmed prediction, and it is the only way the set can be shown to be incomplete.

---

# 🔒 §2.2 — **THE PREDICTIONS ARE FROZEN**

> ## **FROZEN AT COMMIT `4cf6217` (07-Aug-2026), amended once at `c10e700` to ADD §3 and this freeze — ⛔ NO PREDICTION WORDING WAS TOUCHED.**
> ⛔ **From this point NO wording in E1–E6 may be edited, softened, or "clarified" once observation
> begins.** A prediction that evolves after reality is not a prediction. **If a prediction turns out to
> be ambiguous, SCORE IT AGAINST THE WORDING AS WRITTEN and record the ambiguity as a finding about the
> prediction, ⛔ never as a licence to restate it.**
> ⭐ **Anything learned that the predictions did not cover goes in a NEW row of §2.1, never into an old one.**

---

# §3 · THE MONDAY CONTROLLED OBSERVATION — **THE CAPTURE LIST**

> ⭐ **This costs nothing under EITHER of Rama's branches.** If he cancels, E2/E3/E4 still score. If he
> leaves it, **E5 becomes capturable for the first time.** ⇒ the plan is written before the open either way.
> 🧪 **PARITY: every artifact below is LIVE-ONLY** — CNC, broker GTTs, T+1 settlement. **Paper has no
> analogue** (nets by *symbol*, no settlement model) and a paper rehearsal would be **vacuously green**.
> ⛔ **Do not treat any of this as paper-validated.**

## §3.1 — CAPTURE FIRST, INTERPRET SECOND · ⛔ **to a FILE, then filter**

**⛔ Never `grep` straight from a live source and keep only the match** — the discard is unrecoverable.
Write the raw artifact to `~/preserved/monday_10aug2026/`, then filter the copy.

| # | instant | artifact | why this instant |
|---|---|---|---|
| ~~**A**~~ | ~~**BEFORE the 08:15 boot**~~ | 🔴 **IMPOSSIBLE — SUPERSEDED BY `A′`. DO NOT record it as a missed step; it CANNOT be executed.** | see `A′` below |
| ✅ **A′** | 🔑 **FRIDAY NIGHT — ALREADY TAKEN, `2026-08-07 21:07:28 +0530`** | `get_gtts()` · `holdings()` · `positions()` · `orders()` · `trades()` + the `gtt_state` / `trades` / `kill_switch` rows for **both** DIFFNKG and MANINFRA | 🔑 **THE BASELINE. It brackets the weekend from the NEAR side** — paired with Monday's boot log it isolates **what settlement did**, which is E2's entire content |
| **B** | **AT the 08:15 boot** *(the boot writes it itself)* | `logs/system_2026-08-10.log` — every `get_positions` / `get_holdings` `result_summary`, every `cnc_gtt_monitor.*` line | **E2's decisive evidence**: whether `positions()` returns `0 positions` as it did on 07-Aug |
| **C** | **~08:20, after the boot settles** | `kite.get_gtts()` again · `gtt_state` rows · the `trades` row for `trd_010f8e21…` | **E3/E4**: did `330944932` get deleted, did the trade close, what `exit_price` was booked |
| **D** | **09:14 — one minute BEFORE the open** | `kite.get_gtts()` | 🔑 **The last clean read before market risk begins.** If a GTT is still resting here, E5 is live today |
| **E** | **09:16–09:20 and again ~09:30** | `kite.get_gtts()` · **`kite.orders()`** · `positions()` | **E4's in-hours rebuild window** (`_drain_preopen` fires on the first in-hours cycle) **and E5's trigger window** |
| **F** | 🔴 **IMMEDIATELY on any trigger** *(if `330944932` status flips to `triggered`)* | **`kite.orders()` FIRST**, then `positions()`, `holdings()`, `get_gtts()` | 🔑 **THE ONE OBSERVATION THAT SETTLES E5.** ⛔ Capture the ORDER BOOK before anything else — it is the artifact that distinguishes a stale object from a live sell order |

⭐ **`orders()` at instant F is the whole point of the exercise.** Everything else can be reconstructed
later; **an order book that was never read cannot be.**

### 🔴 **WHY INSTANT A WAS IMPOSSIBLE — measured, and it is why `A′` was taken on Friday night**

> **A broker read needs a valid token, and the 08:15 cron is what MAKES Monday's token.** Verified:
>
> | fact | value | source |
> |---|---|---|
> | current token `expires_at` | **`2026-08-08T05:00:00+05:30`** *(Saturday 05:00)* | `zerodha_token.json` |
> | `token_cleanup` schedule | **`0 5 * * *` — DAILY, weekends included** — `rm -f …/zerodha_token.json` | crontab |
> | `auto_refresh_token` schedule | `15 8 * * 1-5` — **Mon-Fri only** | crontab |
>
> ⇒ **From `05:00 Saturday` until `08:15 Monday` there is NO token file at all**, and Friday's token is
> expired from 05:00 Saturday regardless. 🔑 **There is NO window in which a Monday pre-boot broker read
> is possible.**
> ⛔ **Instant A as originally written cannot be executed — and an instruction that cannot be executed
> is worse than no instruction, because it gets recorded as a MISSED step rather than an IMPOSSIBLE
> one.** ⭐ **`A′` (Friday night) replaces it and was taken with ~8 hours of token life remaining.**

### ✅ **`A′` — PRESERVED AND HASHED** *(`~/preserved/monday_10aug2026/`, `chmod 444`, 0 bytes stderr)*

```
b5895a8effd7ae6eef85bcd02207ac7fa770b2fe1779a958f71899e56987b890  FRIDAY-NIGHT_broker.json   (41,626 B)
6a652e5e3be9cdaa88cecd8b059509775eaae5d0ecc7b3546882369ec4be6336  FRIDAY-NIGHT_db.json       ( 7,585 B)
captured_at 2026-08-07T21:07:28+0530
```

⭐ **This is the cheaper reading and it was available; the Monday pre-boot one was better and is not.**
⛔ **`A′` does NOT replace instants B–F** — those all happen after the boot, when a fresh token exists.

### 🔒 **HASH AND ARCHIVE *BEFORE* INTERPRETING — ⛔ this is NOT the same as capture-then-filter**

> **After EACH instant: (1) write the raw artifact to `~/preserved/monday_10aug2026/<instant>_<name>.json`,
> (2) `sha256sum` it into `MANIFEST.txt` in the same directory, (3) interpret ONLY from the preserved copy.**
> ⛔⛔ **NEVER re-read a live source to check a reading.** State has moved between the two reads, and the
> second read **silently replaces** the first — you end up reasoning about a different moment while
> believing you verified the original one.
> ⭐ **The hash is what makes the archive an artifact rather than a copy:** without it, a later
> re-capture cannot be distinguished from the original, and the whole chain becomes unfalsifiable.
> 🏷️ **This campaign already has the precedent — the 05-Aug evidence was copied off-box and `chmod 444`'d
> precisely so it could not be re-derived after the fact.**

## §3.2 — 🔑 **WHAT ARCHITECTURAL CONCLUSION CHANGES IF EACH PREDICTION FAILS**

*(The card had falsifiers but no consequences. Without this column Monday is narrative, not evidence.)*

| # | if it FAILS, what changes |
|---|---|
| **E2** | 🔴 **The largest single consequence in the set.** It would mean **the CNC day-position residue SURVIVES a weekend**, so the ATULAUTO precedent does **not** generalise across settlement gaps. ⇒ F6's blast radius is **wider than measured**: every Friday delivery exit strands until the residue clears, not just until the next boot. ⭐ It would also make **candidate 6 of §11.6 conditional rather than reliable**, which removes the only durable removal path the system has |
| **E3a** | The `forensic → delete_gtt → gtt_exit` sequence is **not** the general resolution path — it was ATULAUTO-specific. Every claim resting on that precedent (including E2's grounding) weakens |
| **E3b** | If the exit price is **not** LTP-derived: `_resolve_exit_price`'s rung ordering is misunderstood, and **F6 cost 5 ("a fabricated exit price") needs re-measuring.** If the sign is **understated** rather than overstated, the *"stop leg fires at a local low ⇒ proxy biased above"* generalisation is **refuted** and the leg-determines-sign rule must be withdrawn |
| **E4** | If a **4th GTT appears anyway**, `_handle_row`'s branch order is not what §11.2 traced ⇒ **§11's entire decision matrix is void**, and the advice given to Rama about cancelling was wrong in a second, independent way |
| **E5** | 🔴 **If a live order appears: the risk was REAL, not theoretical.** A resting GTT on a flat holding is then a **latent short-delivery exposure**, F6 gains an **eighth cost**, and the priority of fixing it rises immediately. **If a rejection appears instead**, the exposure is bounded and the hypothesis in §3.4 is confirmed |
| **E6** | Only a market-data claim; failure changes nothing architectural. ⛔ **Recorded as the low-value row it is** — not every prediction carries equal weight, and pretending otherwise inflates the scoreboard |

## §3.1b — 🔒 **THE FROZEN BOOT-STAGE REFERENCE TRACE** · ⛔ *"boot executed" ≠ "boot succeeded"*

> ## ⭐⭐ **WHY THIS EXISTS: if the boot RUNS but the monitor cycle never COMPLETES, E2 is UNTESTABLE — and it would score as FAILED.**
> A set of independent checks all reading red tells you nothing about **where** it broke. **A stage
> sequence does: the FIRST DIVERGENCE localises the failure.** ⭐ **And a linear chain IS the dependency
> graph here — ⛔ no second artifact is drawn.**

**Every timestamp below is quoted from `logs/system_2026-08-07.log`, `token_watcher.log`,
`cron_marks/token_cleanup.done` and `journalctl`. ⛔ No time is invented.** Offsets are arithmetic
against **08:15:00**.

| 🆔 | stage | 07-Aug ACTUAL | offset | Δ from prev | source |
|---|---|---|---|---|---|
| **B0** | `token_cleanup` deletes the old token | `05:00:01` | −3 h 15 m | — | `cron_marks/token_cleanup.done` |
| **B1** | **token written** (`saved_at`) | `08:15:02.166` | **+2.166 s** | — | `zerodha_token.json` |
| **B2** | watcher detects + issues start | `08:15:27` | **+27 s** | **+24.8 s** | `token_watcher.log` |
| **B3** | systemd `Started trading-system.service` | `08:15:27` | **+27 s** | ~0 s | `journalctl` |
| **B4** | app banner `Trading System v2.0.0 starting (mode=live)` | `08:15:28.353` | **+28.353 s** | +1.35 s | app log |
| **B5** | `service window: may START in [08:00, 18:15)` | `08:15:28.412` | +28.412 s | +0.06 s | app log |
| **B6** | `KILL SWITCH ACTIVE AT STARTUP: state=SOFT_KILL` | `08:15:28.423` | +28.423 s | +0.01 s | app log |
| **B7** | 🔑 **`Kill switch auto-cleared`** | `08:15:28.427` | **+28.427 s** | +0.004 s | app log |
| **B8** | `startup_scenario` resolved | `08:15:28.427`→`.442` | +28.4 s | ~0 s | app log |
| **B9** | `run_all_startup_checks: OK` | `08:15:41.335` | **+41.335 s** | 🔑 **+12.89 s** *(the long stage)* | app log |
| **B10** | `fund_manager.session_start` · `cnc_gtt.hydrated` | `08:15:41.340` / `.410` | +41.3–41.4 s | +0.005 s | app log |
| **B11** | 🔑 **first `get_positions call_end`** | `08:15:41.516` | **+41.516 s** | +0.11 s | app log |
| **B12** | `get_holdings call_end` | `08:15:41.687` | **+41.687 s** | +0.17 s | app log |
| **B13** | 🔑 **`cnc_gtt_monitor.forensic`** | `08:15:41.704` | **+41.704 s** | +0.017 s | app log |
| **B14** | `delete_gtt call_end` | `08:15:41.722` | +41.722 s | +0.018 s | app log |
| **B15** | 🔑 **`cnc_gtt_monitor.gtt_exit`** — resolution complete | `08:15:41.795` | **+41.795 s** | +0.073 s | app log |

⭐ **`B0…B15` are stable IDs — cite them.** Monday's report should read **"B11 passed, B12 failed"**,
⛔ never *"the boot looked wrong."* ⚠️ **`B9` is the only slow stage at +12.89 s** (`run_all_startup_checks`);
everything from `B10` to `B15` completes in **0.46 s**, so a Monday gap anywhere in `B10-B15` is itself
a signal. *(The Δ column is review point 7 — elapsed time between milestones — taken here as a
by-product of the offsets rather than as a separate artifact.)*

**Arithmetic:** service start `08:15:27` → resolution `08:15:41.795` = **14.795 s**. The whole
delivery-exit resolution completes **inside 15 seconds of the service starting**, and **~42 seconds
after 08:15:00**.

> ### ⛔ **TWO CORRECTIONS TO THE STAGE LIST AS IT WAS GIVEN TO ME — both matter for scoring**
> **① THE CENSUS IS NOT A BOOT STAGE.** It is emitted at **SHUTDOWN** (`effect_census | BEGIN … END`,
> observed 07-Aug at the 18:36:48 stop). ⛔ **Looking for a census at Monday's boot and not finding one
> is NOT a divergence** — it would be the correct behaviour. The boot chain ends at stage 15.
>
> ### ② 🔑 **STAGE 8 IS *EXPECTED* TO DIFFER ON MONDAY, AND THAT DIFFERENCE IS NOT A FAILURE.**
> **(P)** 07-Aug logged **`startup_scenario=COLD: new day (prev=2026-08-06, today=2026-08-07)`** and
> then **`startup_scenario=CRASH: same day, no SHUTDOWN event found`**, with
> `run_all_startup_checks: OK scenario=CRASH`. ⭐ **It resolved to CRASH because 06-Aug never shut down
> cleanly — the delivery carry deferred `eod_self_exit`, so no SHUTDOWN event existed.**
> **Friday 07-Aug DID shut down cleanly at `18:36:48` with `Shutdown complete` and a full census.**
> ⇒ **MONDAY SHOULD RESOLVE TO `COLD`, NOT `CRASH`.**
> ⛔ **Do not score a `COLD` scenario as a divergence from this reference — it is the reference being
> read correctly.** ⭐⭐ **This is exactly what building the trace was for: it surfaced, in advance, the
> one stage where Monday is *supposed* to look different — which would otherwise have been the most
> convincing false alarm available.**

**HOW TO USE IT:** walk stages 1→15 in order and stop at the first that is missing or out of sequence.
⭐ **The stage that is missing names the failure**: no stage 1 ⇒ TOTP failed · no stage 3 ⇒ the watcher
did not act · stage 9 absent ⇒ startup checks blocked · **stages 11-12 present but 13-15 absent ⇒ the
monitor ran and chose NOT to act, which is E2 failing rather than the boot failing** — and those are
two entirely different conclusions that a flat set of red checks would have merged.

🧪 **PARITY: ⛔ LIVE-ONLY.** Stages 11-15 read broker `positions()`/`holdings()` and act on a T+1
residue; paper has no settlement model, so a paper rehearsal would skip straight past stage 13.

## §3.2b — 🪞 **THE MIRROR: WHAT BECOMES *STRONGER* IF EACH SUCCEEDS**

*(Evidence must both remove uncertainty AND raise confidence in what survives. ⛔ Without this column a
clean sweep teaches nothing — the failure §8.7 already named.)*

| # | if it HOLDS, what is strengthened |
|---|---|
| **E2** | 🔑 **The day-book rollover becomes a property, not an anecdote** — established across a *weekend* and not merely overnight. ⇒ **§11.6 candidate 6 (the system's own boot) is promoted from "observed once" to a RELIABLE removal path**, which is the single fact Rama's "do nothing" rests on. It also raises confidence that F6's blast radius is bounded **by the next boot** rather than open-ended |
| **E3a** | The ATULAUTO resolution **generalises** ⇒ `forensic → delete_gtt → gtt_exit` is *the* delivery-exit resolution path, and any future F6 reasoning may cite it as such |
| **E3b** | ⭐ **The leg-determines-sign rule is promoted from a two-instance pattern to a MECHANISM** — stop leg ⇒ overstated, target leg ⇒ understated. That is reusable well beyond F6, and it makes **F6 cost 5 quantifiable in DIRECTION** for the first time |
| **E4** | **`_handle_row`'s branch ORDER is confirmed empirically**, not only by reading ⇒ **§11's entire decision matrix gains its missing empirical leg**, and the advice given to Rama about cancelling is validated rather than merely reasoned |
| **E5** | Any of A/B/C/D resolving turns *"what the venue does with a triggered GTT on a zero holding"* into a **standing invariant** future architecture can rely on. ⭐ Even **C** (the bad branch) strengthens something: it converts a suspected exposure into a **measured** one and gives F6 an eighth, quantified cost |
| **E6** | Nothing architectural — ⛔ **and saying so is the point.** A prediction that strengthens nothing on success is a *check*, not evidence |
| **E7** | 🔑 **The boot's SELECTIVITY is demonstrated** — that it acts on the phantom and leaves a legitimate carry alone. ⇒ E2–E4 stop being *"the boot did something"* and become *"the boot did the RIGHT thing"* |

## §3.3 — FREEZE

**Done — see §2.2 above.** Frozen at `4cf6217`; this section and §2.1/§2.2 were **added**, and ⛔ **no
E1–E6 wording was altered.**

## §3.4 — ⚠️ **THE E5 HYPOTHESIS — NAMED, ⛔ NOT ASSUMED**

**ChatGPT asserted an answer to E5: that a CNC sell without holdings is expected to be REJECTED
broker-side rather than becoming a naked short.**

> ### 🏷️ **RECORDED AS HYPOTHESIS `H-E5`, ⛔ NOT AS A PREMISE.**
> **It is plausible, and it is exactly what E5 says CANNOT BE DETERMINED from the record.** §8.9
> already established why: today's order book is `{CANCELLED: 11, COMPLETE: 10}` — **zero `REJECTED`
> of any symbol** — so there is **no instance of Kite surfacing a rejection** against which to test it.
> ⛔⛔ **IT MUST NOT BE USED TO LOWER THE ASSESSED RISK.** An unverified reassurance adopted as a
> premise is precisely the failure mode `V5` names: a check with no failing input manufactures confidence.
> ⭐ **Its VALUE is that it is now FALSIFIABLE, and Monday can settle it.**

### 🔴 **E5 HAS *FOUR* OUTCOMES, NOT THREE — AND MY EARLIER WORDING COLLAPSED TWO OF THEM**

**My §3.4 first read *"no order appears at all ⇒ still cannot determine."* ⛔ That silently merges two
architecturally different venues:** one that **validates** and one that **swallows**. Split:

| | outcome | what it means | **distinguishing observation** |
|---|---|---|---|
| **A** | broker **REJECTS BEFORE ORDER CREATION** | the venue **validates** at trigger time: no order object is ever born | 🔑 **GTT status flips to `triggered` AND the order book stays empty AND a rejection is visible SOMEWHERE** — a GTT-level `rejection_reason`/`meta` field on the GTT object itself, or an order-book entry that exists only transiently. **Check `k.get_gtt(330944932)` — the SINGULAR fetch — which returns fuller detail than the list** |
| **B** | broker **CREATES A REJECTED ORDER** | an order object exists with `status='REJECTED'` and a `status_message` | **`orders()` shows a DIFFNKG SELL with `REJECTED`.** Unambiguous |
| **C** | 🔴 broker **CREATES A LIVE ORDER** | a real sell reaches the market for stock we do not own | **`orders()` shows OPEN/COMPLETE.** ⇒ **short delivery + auction settlement.** The risk was real |
| **D** | broker **SILENTLY SUPPRESSES** | the GTT flips `triggered` and **nothing at all** is recorded anywhere | **`get_gtt()` singular shows `triggered` with NO rejection detail AND `orders()` is empty AND no GTT-level reason exists** |

> ### ⭐⭐ **THE POINT OF THE ENUMERATION: EXACTLY ONE SURVIVES MONDAY, SO E5 YIELDS A STANDING BROKER INVARIANT IN *EVERY* BRANCH — INCLUDING THE ONE WHERE NOTHING APPEARS.**
> ⇒ **E5 is never wasted, only untested.** If the GTT never triggers, E5 is **NOT TESTED**; if it
> triggers, **one of A/B/C/D is established as a fact about the venue** and becomes referenceable
> architecture (§3.5).
> 🔑 **A vs D is the split that was missing, and it matters: A means the venue enforces the holding
> constraint (a safety property we could rely on); D means it does not record what it did (a blind
> spot we must never rely on).** ⛔ **Treating "nothing appeared" as reassurance would be assuming A
> when D is equally consistent** — which is precisely the `15:08:11` ambiguity, unresolved.
> ⚠️ **Practical note for instant F: fetch `get_gtt(330944932)` SINGULARLY, not just the list.** The
> list view is what produced the original ambiguity; the singular fetch is the untried source and may
> be what separates A from D.

## §3.5 — IF E5 RESOLVES, IT EARNS ITS OWN PERMANENT ENTRY

⛔ **Not buried inside F6's incident history.** A broker-observed invariant — *"what the broker does with
a triggered CNC sell GTT when the holding is zero"* — is a **standing fact about the venue**, not about
one trade. It outlives F6 and any future architecture may need to reference it.
➡️ **Home: a new dated entry under `docs/audit/`, cross-linked from the F6 design and from
`SYSTEM_MAP.md`.** ⭐ **Write it whichever way it resolves** — a confirmed rejection is as much a
standing invariant as a confirmed live order.

## §3.6 — ORDER OF OPERATIONS ON MONDAY

1. ⛔ **SCORE E1–E7 BEFORE any fix, any cancellation, and before any explanation is offered.**
2. **E5 unfired = `NOT TESTED`. ⛔ NEVER `PASSED`.**
3. ⛔ **No push during market hours** — the post-receive `checkout -f` lands on the live VM.
4. 🆕 **THE INTERPRETATION RULE — apply it before reaching for a cause:**
   > ## **If Monday behaves unexpectedly, ask FIRST: *"did the preserved weekend state EXPOSE a latent defect?"* — ⛔ NOT *"did the boot CREATE one?"***
   ⭐ **A weekend carry with a settled T+1 sell is a state this system has NEVER been in.** Novel states
   **expose**; they rarely **create**. ⛔ **Getting that backwards sends the whole post-mortem after the
   wrong component** — and the boot is the tempting suspect precisely because it is the thing being
   watched. 🔗 Pair it with the **PROVENANCE** column: a `BEFORE` finding that surfaces on Monday is
   the *expected* shape of this, not an anomaly.
5. Only then: interpretation, and only then: any proposal.
6. 🆕 **AFTER scoring, during the trading day: the `margins()` capture — §3.6b.**
   ⛔ **Not before step 1. It is a read-only GET and cannot disturb E1–E7, but the
   ordering rule is not negotiable, and the reason to hold it is that it will be
   tempting not to.**

## 🆕 §3.6b — **THE `margins()` MEASUREMENT** · ⛔ AN OPERATIONAL STEP, **NOT AN E-PREDICTION**

**Added 08-Aug-2026.** 🏷️ **This is an ADDITION to §3's capture list. ⛔ It is NOT a
prediction, it is NOT scored, and it does NOT touch §1 or §2.2's freeze.** ⭐ It carries
no expectation on purpose — writing one down would be the thing it exists to avoid.

> ### 🔑 **THE QUESTION: DO SL / TGT LEGS CONSUME ADDITIONAL CAPITAL AT ZERODHA?**
> ⛔ **The ONLY part of the sizing question that cannot be answered from our own
> records**, and the shape of any future sizing build turns on it.

**(P) OUR SIDE IS ALREADY ANSWERED and needs no repeating:** 454 protective legs placed
(193 filled), every margin-moving `fm_ledger` entry type is ENTRY-keyed, and a join to
SL/TGT legs carrying margin returns **0**. **What is missing is the BROKER's side.**

**CAPTURE — four readings, SAME symbol and SAME quantity throughout:**

| # | when | what |
|---|---|---|
| 1 | **before entry** | `margins()` |
| 2 | **after the entry fills** | `margins()` |
| 3 | **after the SL leg exists** | `margins()` |
| 4 | **after the TGT leg exists** | `margins()` |

⭐ **Preserve raw and hash into the manifest, exactly like every other capture** —
capture first, interpret second, and ⛔ never re-read a live source to check a reading.

> ### ⛔⛔ **IF NO NATURAL DELIVERY ENTRY OCCURS ON MONDAY, THIS SIMPLY DOES NOT HAPPEN.**
> ⛔ **DO NOT MANUFACTURE A TRADE TO OBTAIN IT.** ⛔ **Do not substitute an intraday leg
> for a delivery leg without labelling the difference** *(MIS is levered 5×, CNC is 1× —
> the margin arithmetic is not the same question)*.
> ⭐⭐ **`NOT MEASURED` IS A VALID OUTCOME. A measurement taken under the wrong
> conditions is not** — it is worse than the gap, because it looks like an answer.

> ### 🏷️ **EVIDENCE GRADE — hold the line that is easy to let slip**
> Record `(P)` for **exactly what the four readings show, and nothing further.**
> ⛔ **The general principle — *"a position-reducing order needs no fresh margin"* —
> stays `(I)` until those numbers exist.** ⭐ It is plausible, widely believed, and
> precisely the kind of "everyone knows" claim this campaign has repeatedly refuted.
> **It must not quietly become fact between now and Monday.**

⚠️ **PARITY: THIS STEP IS LIVE-ONLY.** ⛔ Paper cannot answer it at all — it synthesises
fills and never calls `margins()`. **(P)** the VM DB holds 561 trades, **all
`mode=LIVE`, zero paper rows.** ⭐ **An absent instrument is not a passing control.**

## §3.7 — ⛔ **THE FOUR LAYERS MUST BE REPORTED SEPARATELY AND NEVER MERGED**

| # | layer | status |
|---|---|---|
| 1 | **EXPECTED broker behaviour** | 🏷️ **HYPOTHESIS** — this is `H-E5` and anything like it |
| 2 | 🔑 **OBSERVED broker behaviour** | ⭐ **THE ONLY EMPIRICAL LAYER. Quote the artifact.** |
| 3 | **SYSTEM reaction** | what `cnc_gtt_monitor` did about layer 2 — a *consequence*, not evidence about the broker |
| 4 | **BUSINESS decision** | Rama's. ⛔ Never derivable from layers 1–3 alone |

> ⭐ **Only layer 2 is evidence.** The failure mode this prevents is writing *"the broker rejects a CNC
> sell with no holding, so the system re-protected and we can leave it"* — one sentence containing a
> **hypothesis**, an **observation**, a **reaction** and a **decision**, in which the unverified first
> clause silently licenses the last. ⛔ **Report them as four rows, never as one narrative.**

---

# 🆕 §3.8 · **E7 — THE NEGATIVE CONTROL** *(a NEW prediction; ⛔ no existing wording amended)*

> ## ⭐⭐ **THE SET HAD NO CONTROL, AND WITHOUT ONE, E2–E4 CONFIRMING WOULD PROVE THE BOOT DID *SOMETHING* — NOT THAT IT DID THE *RIGHT* THING.**

**MANINFRA is a REAL carry** — **(P)** `positions()` CNC `net=+4, buy=4, sell=0`, a genuine open
delivery position, protected by **one matching `active` GTT `330856765`** (`trigger_values
[112.92, 118.69]`, `trade_id trd_9e709c50…` matched exactly). **It is correct in every respect and it
must come through Monday's boot UNTOUCHED.**

### 🎯 **PREDICTION: `cnc_gtt_monitor` takes NO action on MANINFRA beyond `healthy`.**
**CONFIDENCE: HIGH · WIDTH: X2** · **(S)** + **(P)**

**(S)** the trace: `held` = holdings + `abs()` of the CNC row. MANINFRA's `+4` is a **genuine long**,
so `abs()` is a no-op on it *(⭐ the F6 defect needs a NEGATIVE quantity to bite, and MANINFRA has
none)* ⇒ `held = 4 = row_qty` with the GTT `active` ⇒ **branch 2 (`:492`) → `healthy:MANINFRA`.**

**⛔ FALSIFIER — ANY of these refutes E7:**
- any `delete_gtt` on `330856765`
- any `cnc_gtt_monitor.recreated` for MANINFRA, or a 2nd MANINFRA GTT appearing
- any `forensic` / `qty_mismatch` / `_reprotect` line naming MANINFRA
- `trd_9e709c50…` leaving `OPEN`, or its `gtt_state` row leaving `ACTIVE`
- its `trigger_values` changing from `[112.92, 118.69]`

> ### 🔴 **IF E7 FAILS IT IS THE MOST SERIOUS RESULT OF THE DAY — AND NOBODY HAS PREDICTED IT.**
> A boot that disturbs a **legitimate** carry is a defect in the opposite direction from F6: not
> *"fails to close a phantom"* but *"acts on a real position it should have left alone."* ⛔ **Without
> E7 on the board, such an event would be read as normal boot activity and pass unremarked**, because
> every other prediction is about the boot *acting*. ⭐ **The control is what makes E2–E4 mean
> anything.**
> 🧪 **PARITY: ⛔ LIVE-ONLY.** MANINFRA's `+4` CNC position and its T+1 state have no paper analogue —
> paper nets by symbol with no settlement model — so a paper drill could not distinguish E7 from E2.

---

# 📋 §3.8b · **THE ASSUMPTION REGISTER — PROVEN · ASSUMED · WAITING FOR MONDAY**

> ⭐ **ONE artifact, not two** *(review points 1 and 6 asked for the same thing in different words)*.
> 🔑 **Its purpose is the THIRD column: a thing that is UNRESOLVED must be recorded as unresolved, not
> rounded to "safe" or "unsafe". ⛔ Binary framing of an open question is how an assumption becomes
> architecture.**

| ✅ **PROVEN** *(measured, with a source)* | ⚠️ **ASSUMED** *(reasoned, not observed)* | ⏳ **WAITING FOR MONDAY** *(⛔ do not resolve early)* |
|---|---|---|
| The Friday stop ran — `inactive/dead/success`, census 55 lines | **`SD-1`** — that the `-1` CNC day-book row clears over a **weekend** *(observed once, overnight only)* | 🔴 **`330944932`'s behaviour if it triggers — E5.** ⛔ **NOT "safe". NOT "unsafe". UNRESOLVED** |
| 10-Aug is a trading day (2 sources) | That Monday's boot follows the **same 15-stage path** as Friday's | Whether `held` reaches **0** (E2) |
| The token chain is headless TOTP; no manual step | That `_resolve_exit_price` falls to **rung 2** on Monday (E3b) | Whether the exit price is LTP-derived and **overstates** (E3b) |
| Friday's kill reason is in `SCHEDULED_KILL_REASONS` (exact literal) | That branch 2 returns `healthy` for a present+active GTT with `held=1` (E4) | Whether a **4th** GTT appears (E4) |
| `cnc_gtt_monitor.py` is byte-identical to `0197923` | That MANINFRA's `+4` makes `abs()` a no-op (E7) | Whether the boot is **SELECTIVE** — MANINFRA untouched (E7) |
| Cancelling rebuilds via `:513`; rebuild is trigger-equivalent | That `startup_scenario` resolves **COLD**, not CRASH | Which of **A/B/C/D** the venue does (`H-E5`) |
| The Friday-night baseline + its state fingerprint | — | — |

> ⛔ **THE ONE LINE THAT MATTERS: `330944932` STAYS IN COLUMN 3 UNTIL EVIDENCE EXISTS.** Nothing in this
> campaign has established what the venue does with a triggered CNC sell GTT on a zero holding — §8.9
> measured the day's order book as `{CANCELLED: 11, COMPLETE: 10}` with **zero `REJECTED` of any
> symbol**, so even the discriminator is untested. ⭐ **Any sentence that moves it to column 1 or 2
> before Monday is an assumption wearing a finding's clothes.**

---

# 🔑 §3.9a-0 · **THE FRIDAY-NIGHT STATE FINGERPRINT — for MECHANICAL drift detection**

**Hashing the FILES proves they were not edited. Hashing the STATE proves the world did not move.**
Canonical state (sorted, separator-normalised JSON over GTTs · holdings · non-zero net positions ·
non-terminal trades · ACTIVE `gtt_state` · kill switch), captured `2026-08-07 21:07:28 +0530`:

```
STATE FINGERPRINT  sha256 = 857258db28446847469b928b73ab1edde2670053aa8b5e4dfb5094d714f54270
  gtts             330658430 DIFFNKG triggered · 330856765 MANINFRA active · 330940420 DIFFNKG triggered · 330944932 DIFFNKG active
  holdings         DIFFNKG qty=0 t1=0
  positions_net    DIFFNKG CNC -1 (buy 0 / sell 1) · MANINFRA CNC +4 (buy 4 / sell 0) · 4 flat MIS rows
  open_trades      trd_010f8e21… DIFFNKG OPEN · trd_9e709c50… MANINFRA OPEN
  gtt_state ACTIVE 330944932→DIFFNKG · 330856765→MANINFRA  (both trade_id-matched)
  kill             SOFT_KILL / circuit_breaker_force_close_15:15
```

⭐ **ON MONDAY: recompute the same canonical structure and DIFF IT.** A changed fingerprint with no
predicted cause **is the finding** — ⛔ and it is the check that would catch a weekend change *no
prediction covers*, which is precisely the class the whole card is weakest against.
*(Preserved `chmod 444` as `STATE_FINGERPRINT.json`, sha256 `36f256bb…` in `MANIFEST.txt`.)*

---

# 🔒 §3.9 · **THE PRECONDITIONS THE WHOLE ANALYSIS RESTS ON — MEASURED, AND THEY ALL HOLD**

> ⚠️ **§11.6 candidate 6 — the only durable removal path — is *"the system's own 08:15 boot."* Every
> "doing nothing dominates" cell assumes that boot happens, and NOTHING in the record established that
> it would.** ⭐ **Checked now. Both preconditions HOLD, and nothing is owed by Rama.**

## §3.9a — **IS 10-Aug-2026 A TRADING DAY?** ✅ **YES — TWO INDEPENDENT SOURCES AGREE** · **X2**

| source | reading |
|---|---|
| **the system's own calendar** — `config/nse_holidays_2026.yaml` | **(P)** `2026-08-10` appears **0** times; **there are NO August entries at all** *(width: grep for `2026-08` over the whole file)*. The file's header separately notes **15-Aug-2026 Independence Day falls on a SATURDAY** and is therefore not listed |
| **external** — NSE/BSE 2026 holiday calendars | **no weekday holiday closures in August 2026**; 15-Aug is a Saturday |
| **weekday** | 07-Aug is Friday ⇒ **10-Aug is a MONDAY** |

⇒ ✅ **10-Aug-2026 IS A TRADING DAY. The boot fires, the market opens, and E2–E7 are all scoreable.**

> ### ⭐ **AND THE EXTERNAL CHECK CAUGHT SOMETHING THE SYSTEM'S CALENDAR CANNOT KNOW — FILED FORWARD**
> **26-Aug-2026 (Wednesday) is a *SETTLEMENT* holiday, not a trading holiday**: trading runs normally,
> but **fund and security pay-in/pay-out shift to the next working day.**
> 🔑 **That is precisely the mechanism E2 depends on** — the T+1 rollover that clears the CNC day-book.
> ⛔ **`nse_holidays_2026.yaml` lists TRADING holidays only and has no concept of a settlement holiday**,
> so nothing in the system can currently distinguish the two. ⚠️ **A delivery exit around 25–27 Aug may
> therefore behave differently from the model in this card.** 🏷️ **Recorded, not chased (G3)** — it is
> 19 days out and outside this card's scope, but it belongs on the record now rather than being
> rediscovered as a surprise.

## §3.9b — **WHAT DOES MONDAY'S 08:15 BOOT REQUIRE?** ✅ **EVERY LINK IS AUTOMATIC** · **X2/X3+**

| # | precondition | **AUTOMATIC or RAMA'S?** | evidence |
|---|---|---|---|
| 1 | the 08:15 token refresh | ✅ **AUTOMATIC** | **(P)** crontab: `15 8 * * 1-5 … scripts/auto_refresh_token.py`. **(S)** its own header, line 5: *"Fully headless Zerodha token refresh via **TOTP (no browser, no manual OTP)**"*, line 7: *"eliminating the daily manual OTP step"* |
| 2 | the token file actually appearing | ✅ **AUTOMATIC — and observed 6 consecutive trading days** | **(P)** `token_watcher.log`: `Fresh token detected` on **31-Jul, 03, 04, 05, 06 and 07-Aug**; token file mtime `Aug 7 08:15` |
| 3 | the watcher starting the service | ✅ **AUTOMATIC** | **(P)** each of those lines is followed by `trading-system.service start command issued`; unit `Restart=always`, `RestartSec=10`, polling ~30 s |
| 4 | Friday's `SOFT_KILL` clearing | ✅ **AUTOMATIC** | 🔑 **(P)+(S) EXACT MATCH:** the persisted reason is **`circuit_breaker_force_close_15:15`**, which is **literally the first literal in `SCHEDULED_KILL_REASONS`** (`capital/kill_switch.py:121-124`) ⇒ `clear_stale_state` clears it at boot, and it **ignores open positions** |
| 5 | no blocking schema migration | ✅ **N/A — none pending** | **(P)** `schema_meta` = `('schema_version','45')`; code `core/state_store.py:102` `SCHEDULED… SCHEMA_VERSION = 45`. **Equal.** *(The `MIGRATION_REFUSED v44→v45` line in `cron-auto-token.log` is dated **28-Jul** — the file's mtime is `Jul 28 08:15` — and has been superseded by six clean boots since)* |

> ## ✅ **CONCLUSION: NOTHING IS OWED BY RAMA FOR MONDAY'S BOOT. THE FEARED INVERSION DOES NOT APPLY.**
> The card's concern was that *"the dominant strategy is not 'do nothing', it is 'do the token step'."*
> **Measured: there is no token step. It is headless TOTP and has run unattended for six consecutive
> trading days.** ⇒ **"Do nothing" remains genuinely available.**
>
> ### ⚠️ **THE ONE RESIDUAL, STATED RATHER THAN BURIED — and it is a SILENT failure mode**
> **A failed 08:15 token refresh produces NO alarm.** If TOTP fails on Monday, there is **no boot, no
> monitor cycle, no `clear_stale_state`** ⇒ **the GTT rests into market hours with E5 live, and it
> presents as "a quiet market."**
> ⭐ **NOT REQUIRED, BUT IT IS THE CHEAP INSURANCE:** a ~30-second check any time after 08:20 Monday —
> **is `data_store/session/zerodha_token.json` stamped today, and is the service `active`?** ⛔ That is
> a *compensating control*, not a precondition; the boot needs nothing from him, but this is the one
> failure the system cannot tell him about.

---

# §3 · WHAT THIS CARD DOES NOT ESTABLISH

- ⛔ **Nothing about paper.** Every path here is live-only; no paper analogue exists (see the parity note).
- ⛔ **No authorisation to cancel `330944932`**, fix F6, or touch `MANINFRA` (`net=+4` with matching GTT
  `330856765` — **CORRECT, do not sweep it with DIFFNKG**).
- ⛔ **E5's mechanism is undetermined**, and no amount of the retained record closes it.
- ⛔ **E2 rests on a ONE-INSTANCE precedent** across a weekend the system has not been observed through.
- ⛔ **No figure is predicted for Monday's P&L** — only the mechanism and the sign.
