# §E — IS THE LOSS GOVERNOR'S **ACTION** SCOPED? · MEASURED 08-Aug-2026

**Read-only trace. ⛔ No code, no config.** ChatGPT's §E, and it is a real gap.

> **"When the maximum REALISED loss limit is reached, ONLY THE AFFECTED PIPELINE IS CUT
> OFF … A pipeline loss governor is NOT a global emergency control."**

> ## 🔴🔴 **VERDICT (2.4), IN ONE LINE: YES — AN INTRADAY LOSS BREACH STOPS DELIVERY, AND A DELIVERY LOSS BREACH STOPS INTRADAY.**
> ⛔ **The split separated the COUNTERS and the pre-trade GATE. It did NOT separate the
> ACTION.** ⭐ **Two independent counters still lead to one shared stop — and the loss
> governor is the control most likely to actually fire.**

---

## 2.1 · WHAT AN INTRADAY `daily_loss_limit_pct` BREACH DOES — **(P)+(S)** · **X2**

**TWO enforcement points (the "dual daily-loss mechanism"), and they now DISAGREE:**

| # | where | reads | limit base | scope of action |
|---|---|---|---|---|
| **A · pre-trade gate** | `risk_engine` `DAILY_LOSS` | **per-pipeline** realised P&L *(as built)* | **per-pipeline purse** *(as built)* | ✅ **rejects that pipeline's entry only** |
| **B · post-close breach** | `fund_manager.release_used:1326-1341` | 🔴 **`get_daily_realized_net_pnl(today)` — GLOBAL, no bucket filter** | 🔴 **`daily_loss_limit_pct × self._total` — 3 % of TOTAL** | 🔴 **system-wide, see below** |

**(S)** the breach sequence is `main.py:771-812`:
1. `CRITICAL` log + a `CRITICAL` Telegram *"Closing all positions and halting new trades"*;
2. **`eod_instance.fire_now(reason="daily_loss_limit_breached")`**;
3. **`kill_switch.soft_kill(reason="daily_loss_limit_breached")`**.

### ⭐ THE SEQUENCE DECOMPOSES INTO TWO **DIFFERENT** SCOPES — and only one is wrong

| step | scope TODAY | verdict |
|---|---|---|
| ② `eod.fire_now()` — close positions | ✅ **ALREADY INTRADAY-ONLY.** **(S)** `eod_squareoff` EOD6 / FIX-015: *"DELIVERY (CNC) positions NOT touched. Only INTRADAY (MIS) and COVER_ORDER (CO) products exited"*; the filter is `EMERGENCY_FLATTEN_PRODUCTS = {"MIS","CO"}` | ⭐ **correctly scoped, by an older decision** |
| ③ `kill_switch.soft_kill()` — halt entries | 🔴 **PRODUCT-BLIND.** **(S)** `kill_switch.is_active(intent)` takes `intent ∈ {entry, exit, any}` — ⛔ **that is an ACTION kind, NOT a product.** A `SOFT_KILL` blocks **every** new entry in **both** books | 🔴 **THE GAP** |

⇒ **An intraday loss does NOT close delivery positions (good), but it DOES stop delivery
from taking new entries (wrong).**

## 2.2 · `max_consecutive_losses` — ✅ **ALREADY CORRECTLY SCOPED** · **(P)** · **X2**

**Width: every non-test reference to `_max_consec` / `max_consecutive_losses` across
`capital/ core/ main.py signals/ orders/`.** Its ONLY consumers are the `risk_engine`
`CONSECUTIVE_LOSSES` gate and the new `pipeline_policy`. **There is no callback, no kill,
no close.** ⛔ **The only "consecutive-…-kill" in the tree is `max_api_failures`, a
different circuit breaker on broker API errors.**

⇒ ✅ **the streak breaker rejects entries in the affected pipeline and does nothing else
— exactly what §E asks for, and the split already delivers it.**

## 2.3 · THE NEW DELIVERY LIMITS, AS BUILT — **(S)**

`delivery_daily_loss_limit_pct` and `delivery_max_consecutive_losses` are wired **into the
`risk_engine` GATE ONLY.** ⛔ **Neither is wired to any action**, and neither reaches
`fund_manager`'s breach check — which still reads the global figure against 3 % of total.

## 🔴 AND A DEFECT **THIS BUILD INTRODUCED**, NAMED RATHER THAN LEFT IMPLICIT

⭐ **The two halves of the dual mechanism no longer share a base.** The pre-trade gate was
rebased onto the per-pipeline purse; **the post-close breach was not touched.**
🏷️ Memory's own rule on this mechanism reads: *"ONE limit, TWO enforcement points … read
the threshold from code AND its base — both move."* **I moved one base and not the other.**

**Where they now sit, as fractions of TOTAL capital:**

| control | trips at |
|---|---|
| intraday pre-trade gate | **2.10 %** *(3 % × the 70 % bucket)* |
| delivery pre-trade gate | **0.90 %** *(3 % × the 30 % bucket)* |
| **post-close breach (both)** | **3.00 %** *(3 % × TOTAL)* |

⭐ **The ORDERING is the safe one — both gates trip BEFORE the breach, so the breach is a
strictly later backstop and nothing is loosened.** ⛔ **But the breach's SCOPE is still
global, and its BASE now disagrees with the gate it is supposed to backstop.**

## 2.5 · THE DISTINCTION, EXPLICITLY

| | must be | is |
|---|---|---|
| **PIPELINE LOSS GOVERNOR** — daily-loss + streak | **SCOPED** to its book | streak ✅ · daily-loss **half-scoped** (gate ✅, action ❌) |
| **GLOBAL EMERGENCY `HARD_KILL`** | **GLOBAL** | ✅ global — ⛔ **leave it** |

> ### ⛔⛔ **DO NOT SCOPE THE EMERGENCY CONTROL WHILE FIXING THE GOVERNOR.**
> ⚠️ `HARD_KILL` already flattens **only MIS/CO** and delivery survives it (Q4, Rama
> 30-Jul). **That is a decision already taken about WHAT IT CLOSES, ⛔ not licence to
> narrow WHO IT STOPS.** An emergency control that some book can ignore is not one.

## 2.6 · IF IT IS SHARED — **THE CALL SITES, AND THE SMALLEST CHANGE.** ⛔ NOT FIXED HERE

| # | site | what it needs |
|---|---|---|
| 1 | `fund_manager.py:1326` `get_daily_realized_net_pnl(today)` | the **bucket-scoped** variant — ⭐ **already built and tested** (`get_daily_realized_net_pnl_for_bucket`) |
| 2 | `fund_manager.py:1327` `self._daily_loss_limit_pct * self._total` | the pipeline's pct × **its own bucket**. ⭐ **`bucket` is already in local scope at that line** (it is on the `ReleaseResult` two lines below) |
| 3 | `fund_manager.py:1341` `self._on_loss_breach()` | pass the **pipeline** |
| 4 | `main.py:771-812` the callback | ② `fire_now` is already intraday-only; ③ the `soft_kill` is the only part needing a scope |

> ### ⭐⭐ **THE SMALLEST CORRECT CHANGE IS *NOT* A PRODUCT-AWARE KILL SWITCH.**
> **(P) 35 non-test `is_active(` call sites.** Threading a product through all of them
> makes the **global emergency control** product-aware — ⛔ **precisely what 2.5
> forbids**, and on the highest-consequence surface in the system.
> 🔑 **Instead: stop expressing the GOVERNOR as a kill at all.** Give it a per-pipeline
> block flag that the `risk_engine` gate already reads, so the kill switch stays the
> global emergency control and the governor gets a scoped mechanism of its own.
> ⚠️ **That is a design decision, not a patch** — and it changes a live-safety surface.

🏷️ **⇒ ITS OWN BUILD, ITS OWN CARD, ITS OWN TESTS. ⛔ Not a rider on anything.**

---

## 🎯 THE PRE-REGISTERED EXPECTATION, SCORED

**"I expect the action IS system-wide."** ✅ **RIGHT — for the `soft_kill`.**
⚠️ **But incomplete in an important way, and the incompleteness is the useful part: the
CLOSE half was ALREADY correctly scoped** (EOD6/FIX-015, MIS/CO only). ⭐ **The sequence
is not one action with one scope — it is two actions with two different scopes, and only
one of them is wrong.** ⛔ A blanket *"the action is global, scope it"* would have gone on
to scope the close as well, which is already right and would have been a regression.

## ⚠️ PARITY

**(S)** every site traced — `risk_engine`, `fund_manager.release_used`, the `main.py`
callback, `eod_squareoff`'s product filter, `kill_switch.is_active` — is **mode-blind
shared code**, so **paper and live resolve this IDENTICALLY**. ⛔ **And that is a
STRUCTURAL claim from the source, not an observation:** **(P)** the VM DB holds 561
trades, **all `mode=LIVE`, zero paper rows** ⇒ **there is no paper observation to check
it against.** ⭐ **An absent instrument is not a passing control** — the parity claim here
rests on the code being shared, and on nothing else.
