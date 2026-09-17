---
name: restore_submitted_is_not_restore_live_04sep
description: "F1's restore reported 'protection RESTORED' on a SUBMITTED order with no status poll, so a broker-side rejection read as success - the third instance of 'accepted != effective', and PlacedOrder has no success field so the type cannot represent failure"
metadata: 
  node_type: memory
  type: project
  originSessionId: 161ed55b-a158-4c12-a83a-53edac5888db
  modified: 2026-09-04T04:28:50.588Z
---

🔴 **`RESTORE SUBMITTED` IS ⛔ NOT `RESTORE LIVE`.** 🔬 Measured at `18dd6cc`,
04-Sep-2026.

## The defect, demonstrated

⭐ `_restore_protection_inner` placed the stop and returned
`"protection RESTORED (order {bid})"` on the strength of a **SUBMITTED** order
(`orders/mis_autosquareoff.py:747`/`:764` at `18dd6cc`). ⛔ **No success check,
⛔ no status poll.** ⭐ Contrast the cancel path forty lines up at `:572` --
`if not getattr(r, "success", False)` -- ⭐ which *does* check.

🔬 **Proven, ⛔ not argued.** ⭐ A test fixture whose broker reports `REJECTED`
for the restored stop returns, at `18dd6cc`, verbatim:

    AssertionError: protection RESTORED (order X1)

🔴 ⇒ ⭐ **That is worse than silence.** ⭐ 📄 The operator rule is
*"RESTORE FAILED ⇒ flatten by hand"*, so a false `RESTORED` tells a human to
**STAND DOWN** next to a position with no stop -- ⭐ the ANANTRAJ outcome reached
through the alert instead of the absence of one.

## The structural cause -- the type cannot represent failure

🔬 **`PlacedOrder` (`broker/zerodha_adapter.py:141-153`) has ⛔ NO `success`
field.** ⭐ It is constructed **only** on the success path with
`status="SUBMITTED"`. ⇒ ⭐ `place_order` RAISES on a *synchronous* refusal
(`:622` → `_translate_broker_exception` → `OrderRejectedError`, `:297`) ⭐ but an
**asynchronous** RMS rejection arriving *after* the id is issued is ⛔ invisible
at every call site.

⚠️ ⭐ **This was already found once.** 🔬 `capital/kill_switch.py:1893-1895`
carries the comment *"Bug C (P0 2026-06-15): place_order returns a PlacedOrder on
success and RAISES on failure; PlacedOrder has no .success attribute. Treat an
empty broker_order_id as the only non-exception failure."* ⇒ ⭐ the mitigation
chosen then catches the **synchronous** case and ⛔ **cannot** catch async
rejection. ⭐ A known root cause with an incomplete fix, ⛔ not a new discovery.

## 🔬 The blast radius -- all 20 production call sites classified

⭐ **ZERO of twenty poll order status after placing.** ⭐ The gradient:
  · **10 have an empty-id guard** -- `kill_switch` ×3, `order_protocol_limit` ×4,
    `order_protocol_co` ×2, `sl_breach_monitor` ×1.
  · **4 hand off to `order_monitor.track`** -- `eod_squareoff` ×3,
    `structure_exit_manager` ×1. ⭐ Deferred, ⛔ but real.
  · **2 persist for downstream reconciliation** -- `order_placer:3929`,
    `order_reconciler:3078`.

🔴 ⭐ **`order_reconciler.py:1949` has the same defect on the LAYER 3 BACKSTOP.**
⭐ The `SYSTEM_OVERSELL` flatten sets `placed_ok = True` immediately after
`place_order` returns and reports `success=placed_ok` with a CRITICAL saying
*"flattened"*. ⇒ ⚠️ ⭐ That is one of the backstops listed *behind* F1.

🔴 ⭐ **`mis_autosquareoff:747` was uniquely exposed** -- ⭐ the only site with
⛔ no guard, ⛔ no handoff and ⛔ no persistence. ⭐ And it ⛔ cannot be covered
indirectly: `:601`'s exit is verified by `_verify_mis_positions_closed`
re-reading broker **positions**, ⭐ but a restored stop **changes no position**,
so that mechanism is blind to it. ⚠️ ⭐ Worse -- 🔬 `mis_autosquareoff` **only
ever READS** from the store (`get_open_mis_exit_orders_for_symbol`,
`get_orders_for_trade`; ⛔ zero writes), ⇒ ⭐ the restored SL's broker id exists
**nowhere locally** and ⛔ no reconciler can match it.

## The fix (F1b) -- reuse F2, ⛔ do not invent

⭐ `_verify_restored(bid)` mirrors `_verify_cancelled`: ⭐ read the **broker's**
order history, ⭐ poll to a bounded 5 s budget, ⭐ and ⛔ never treat *"not yet
terminal"* as failure. ⭐ Verdicts: `RESTORE_CONFIRMED` (`TRIGGER PENDING`/`OPEN`)
· `RESTORE_FAILED` (`REJECTED`/`CANCELLED`) · `RESTORE_FILLED` (`COMPLETE` -- the
stop executed, ⭐ position closed, ⛔ **not** naked) · `PROTECTION_UNKNOWN`
(read failed or never settled -- ⛔ neither success nor failure).

⭐ 📄 **Third instance of one root cause.** ⭐ Naming it matters more than the patch:
    cancel accepted   ≠ cancel effective  → F2 `_verify_cancelled`
    exit submitted    ≠ exit accepted     → the 03-Sep MARKET rejections
    restore submitted ≠ restore live      → **this**

⏸ ⭐ **OWED to F3:** ⭐ the contract fix -- a `place_order` result that *can*
represent failure, ⭐ plus persistence of the restored SL. ⛔ Not an F1 patch.

⭐ See also [[a_count_without_its_environment_is_not_a_baseline]] --
🔬 the `trading-system-gui09` worktree inherited
`PYTHONPATH=D:\Projects\trading-system` (a **different** tree at `6d24a83` with
100 modified files); ⭐ overridden to `PYTHONPATH=.` before any gate was measured.

## 🔴 LAYER 3 IS ⛔ NOT A BACKSTOP -- REMOVED FROM THE WATCH CARD

🔬 `order_reconciler.py:1949` sets `placed_ok = True` **immediately** after
`place_order` returns and reports `success=placed_ok` with a CRITICAL saying
*"flattened"*. ⇒ ⭐ **The same defect as F1's, on the component quoted to 👤 Rama
as sitting BEHIND F1.**

⇒ 🔴 ⭐ Layer 3 is **doubly unproven**: 📄 its `SYSTEM_OVERSELL` branch has fired
**0 times in production** (*container proven live, branch unobserved*), ⭐ **and**
when it does fire it ⛔ cannot tell whether its own flatten worked.
⇒ ⛔ **Never quote Layer 3 to 👤 Rama as cover.** ⭐ The dependable backstops are
  `eod_squareoff` **15:17** (🔬 27/27 LIMIT and COMPLETE -- the one proven path)
  and Zerodha's own cutoff (🔬 15:12 CAS · 15:25 non-CAS).

## 🔴 META-PATTERN (standing): HALF A FIX IS THE EXCEPTION PATH ONLY

⭐ **A fix that handles the exception path and leaves the post-accept path is
HALF A FIX.** 🔬 Shipped three times: ⭐ 15-Jun Bug C (`kill_switch.py:1893-1895`)
· ⭐ 01-Jul tag length · ⭐ 03-Sep market protection.
⇒ ⭐ **F3 must close the CONTRACT, ⛔ not another site.**

## 🔬 INVARIANT ESTABLISHED 04-Sep -- the DELIVERY-intent producers

⭐ Question: ⭐ with the 3 delivery strategies disabled, ⭐ can anything else emit a
CNC/DELIVERY order? ⇒ 🔬 **No.** ⭐ Proven four ways:
  · ⛔ **No** production code hardcodes a DELIVERY order. ⭐ The only DELIVERY
    literals are `fund_manager.py:2085`/`:2275` (⭐ capital accounting from a
    BUCKET, ⛔ not placement) and `main.py:1116` `_PIPELINE_DELIVERY` (⭐ a
    shutdown-classification label).
  · ⭐ Every production exit call site passes `intent=intent` **inherited from an
    existing trade**, or hardcodes `"INTRADAY"`.
  · 📄 `strategies/control.py`: `strategy_will_trade()` is the **SOLE authority**,
    imported by BOTH the entry gate and the status table. ⭐ **LAYER 3
    (`enabled`) is checked FIRST** -- *"a disabled strategy never trades,
    regardless of product gating"* ⇒ `CAUSE_DISABLED`.
  · 🔬 **All three** entry paths in `signals/signal_processor.py` call it and
    reject on `will_trade=False`: `_process_one` (:853), `continue_from_gate`
    (:1894), `continue_from_retest` (:2218). ⭐ Every `rehydrate*` ADOPTS existing
    state; ⛔ none creates a position.
⇒ ⭐ So `cnc_orders_possible=true` is ⭐ **the master lock still being open**,
  ⛔ not a live path. ⭐ One layer, ⛔ not two -- ⭐ but the one layer is the
  authority the entry gate actually consults.

## 🔬 F1b ACTIVATES ITSELF ON MONDAY -- ⛔ NO DEPLOY TASK IS OUTSTANDING

⭐ *"Ships tonight"* was the wrong framing. 🔬 Measured 04-Sep ~12:00:
  · ⭐ bare `refs/heads/main` = **`20061b6`**
  · ⭐ the DEPLOYED TREE already carries F1b (🔬 `_verify_restored` /
    `_RESTORE_SETTLE_DEADLINE_SEC` present) -- ⭐ the post-receive hook checked it out
  · ⭐ tree diff vs main = **only the 3 TEMP config YAMLs**
  · ⭐ the RUNNING process (09:31:38) merely **predates** it
⇒ ⭐ The only missing ingredient is **a process that started after the code**.
⇒ ⭐ Tonight's stop + Monday's **08:15 boot** activates F1b **on its own**, ⭐ and the
  ordering is already right: 🔬 cron **07:41** reverts the YAMLs → ⭐ boot **08:15**
  reads `enabled: true` ⇒ ⭐ **delivery ON + F1b active.**
⇒ ⛔ **Do NOT carry "deploy F1b" as an outstanding task.** ⭐ Today's restart decision
  was only ever about **today's 15:03**.

## 🔴 ORDERING CONSTRAINT -- ENFORCE `hard_deadline` **BEFORE** F4 SHIPS

🔬 `hard_deadline` is passed into `_execute_mis_auto_squareoff` and **NEVER READ**
(⭐ only the signature line matches; ⛔ no deadline check anywhere in the per-symbol
loop). ⇒ ⭐ Pass duration is bounded **only by book size**, ⛔ not by the 15:09 cutoff.

🔴 ⭐ **Why it is not cosmetic:** ⭐ an exit submitted AFTER the broker has already
auto-squared-off opens an **opposite position** (⭐ Zerodha CAS 15:12). ⭐ `hard_deadline`
is exactly the guard that would prevent it.
⇒ ⭐ **Today it is masked by the dead payload:** ⭐ F4 has not shipped, ⭐ the exit is
MARKET and is rejected, ⭐ and a rejected order cannot reverse anything.
⇒ 🔴 ⭐ **So enforcing it is a PRECONDITION OF F4, ⛔ not an F3 nice-to-have.** ⭐ The day
exits start working is the day an unenforced deadline becomes a live reversal path.

## ✅ CONCURRENCY IS IMPOSSIBLE -- ⭐ BUT STARVATION IS THE RESIDUAL

🔬 `start_polling`: *"ONE daemon thread. BOTH passes. Evaluated sequentially...
check_and_fire() runs synchronously in a single loop, so a blocking pass blocks the
loop and **two passes can never be in flight at once**."* ⭐ 📄 25 tests pin it, ⭐ and
the docstring names the avoided outcome: ⭐ *"two exits in flight, position reversed."*
⇒ ⭐ **Not arithmetic -- structural.** ⛔ No lock needed; ⭐ there is only one thread.

⚠️ ⭐ **The residual is STARVATION, ⛔ not collision:** ⭐ *"a blocking pass blocks the
loop"* ⇒ ⭐ a stalled PASS_1 consumes PASS_2's slot, ⭐ and the bound that would stop it
is the `hard_deadline` nobody reads. ⭐ The `PASS_1_RUNNING_AT_PASS_2_DUE` /
`PASS_2_STARTED_LATE` / `PASS_1_ABANDONED_FOR_PASS_2` vocabulary exists to **observe**
this ⇒ ⭐ known and made visible, ⛔ not prevented. ⏸ ⭐ Whether the abandon path is
actually ENFORCED is unverified.

## 🔴 F3 DESIGN ECONOMY -- ONE INSERTION POINT, TWO GUARDS

⭐ The invariant: ⭐ *"after the hard deadline the pass must not submit a **NEW** exit
order"* -- ⭐ **including** the case where a broker call **started before** the
deadline and **returns after** it.
⇒ ⛔ That rules out the naive form (⭐ check the deadline at the top of the loop) ⭐ and
  forces the check **immediately before each submit**.
⇒ 🔴 ⭐ **Which is exactly where the pre-submit broker position/quantity re-read has
  to go too** (⭐ the guard against a human closing in the same seconds -- 🔬 the
  15:12:09 vs 15:12:11 race).
⇒ ⭐ So they are ONE insertion point carrying TWO guards, ⭐ both answering the same
  question -- 🔴 ⭐ **"is this submission still valid RIGHT NOW?"**:
     ⭐ *is the deadline past?* → ⛔ do not submit
     ⭐ *does the broker still show this position, at this quantity?* → ⛔ else do not submit
⇒ ⭐ Build them **together**: ⭐ cheaper, ⭐ and it leaves ⛔ no gap between them for a
  stale submission to slip through. ⭐ Record as a SINGLE F3 item, ⛔ not two.
⇒ ⭐ 📄 Pairs with the 0-of-20 finding as the matching half:
  ⭐ **CHECK BEFORE YOU SUBMIT · VERIFY AFTER YOU SUBMIT.**

## ✅ F1b WENT LIVE 04-Sep 13:47:46 -- MEASURED, ⛔ NOT ASSUMED

🔬 Restart 13:47:46 IST, PID 1214531, `NRestarts=0`, new `boot_id=a30db9512fe1`
(⭐ distinct from 1cafb667d30e @09:31 and c5942000bd16 @08:15).
🔬 **Proof the process imported F1b, ⛔ not an inference:** ⭐ `mis_autosquareoff.py`
written **10:41:15**, ⭐ process started **13:47:46** ⇒ ⭐ file precedes process by
3 h 06 m, ⭐ and CPython imports once per process.
🔬 In-process: ⭐ `CHECK_1=15:03:00 CHECK_2=15:06:00 cutoff=15:09:00 margin=20s`
@13:47:55 · ⭐ `will_trade_count:12` with all 3 positional `WON'T TRADE — switch
disabled` · ⭐ kill switch **INACTIVE** · ⭐ SHA `20061b6` · ⭐ config diff exactly the
3 TEMP YAMLs · ⭐ **Monday cron survived** (⭐ a restart is not a push -- ⭐ confirmed,
⛔ not assumed) · ⭐ F boot self-test `delivered` @13:47:59.

⇒ ⭐ **REGIME FROM 13:47:46: `RESTORE CONFIRMED` is broker-verified.**
⚠️ ⛔ **LIVE ≠ PROVEN.** ⭐ F1b has still never executed in production; ⭐ today is its
first opportunity.

## 🔬 FIRST LIVE PROOF OF THE MANUAL-CLOSE → ORPHAN-CLEANUP PATH

⭐ 👤 Rama closed JASH by hand ~13:34 (⭐ exit 481.15, ⭐ -Rs 2.45) to buy the restart
window. ⭐ The system cleaned up **before** any human could:

    13:34:09.603 CRITICAL CHECK1 MANUAL_CLOSE: symbol=JASH local=OPEN/PARTIAL
    broker=no_position closure_source=EXTERNAL_UNATTRIBUTED rung=none
    exit_price=481.15 exit_source=broker_trades

⇒ ⭐ CHECK1 detected the external close, ⭐ classified it `EXTERNAL_UNATTRIBUTED`
(⭐ correct -- a hand close **is** unattributable), ⭐ and **both SL and TGT went
CANCELLED**. 🔬 Detected 13:34:09 → ⭐ clean by 13:35:17 = **~1 reconciler cycle**.

🔴 ⇒ ⭐ **This DIRECTLY REFUTES the "over an hour" orphan figure** carried all day
from ANANTRAJ (15:12:11 → 15:17:04). ⭐ That hour was the **degraded** path (⭐ naked
position, ⭐ stale local row blocking G5b, ⭐ falling through to CHECK9). ⭐ The healthy
path is ~15-30 s, ⭐ now **measured**, ⛔ not argued.
⇒ ⭐ **Consequence for the procedure:** ⭐ manual sibling-cancelling is ⛔ NOT required
on the healthy path -- ⭐ **verification is.** ⛔ Do not carry *"cancel the siblings
yourself"* forward; ⭐ carry *"verify nothing is resting"*.

## 🔬 THE OCO SWEEP, 3-FOR-3 ON NATURAL FILLS (04-Sep)

⭐ DIFFNKG `SL_HIT` → SL COMPLETE, TGT **CANCELLED** · ⭐ GANECOS `TGT_HIT` → TGT
COMPLETE, SL **CANCELLED** · ⭐ TITAGARH `TGT_HIT` → TGT COMPLETE, SL **CANCELLED**.
🔬 **Zero non-terminal legs** across all closed trades.
⇒ ⭐ A natural TGT/SL fill **IS** a managed bracket-leg fill ⇒ `_cancel_oco_siblings`
fires ⇒ ⭐ the book goes flat CLEAN.
⇒ 🔴 ⭐ **The managed path is demonstrably healthy -- ⭐ which is exactly what makes the
MANUAL path the risky one**, ⛔ not any general distrust of the system.

## 🔴 F3'S CONTRACT ALREADY EXISTS IN THIS CODEBASE -- COPY IT, ⛔ DO NOT INVENT

⭐ Two disciplines live side by side here:
  · ✅ ⭐ **The RISK GATE derives from the store on every read** -- 🔬
    `risk_engine.py:306` `daily_count = self._store.count_trades_today(today)`
    (⭐ likewise `count_settled_trades_today`, `count_daily_delivery_trades`).
    ⇒ ⭐ restart-immune · ⭐ stale-state-immune · ⭐ correct. 🔬 Proven live 04-Sep across
    two mid-session restarts taken after four trades.
  · ⛔ **The ORDER LAYER trusts local rows nothing refreshes** (📄 `order_monitor`:
    one log line a day) ⇒ ⭐ D2 · ⭐ D4 · ⭐ the G5b suppression · ⭐ the latching cancel ·
    ⭐ the 0-of-20 verify gap.

⇒ 🔴 ⭐ **Same codebase, two disciplines -- and the good one is already written.**
⇒ ⭐ So F3 is ⛔ **not a new subsystem**: ⭐ its contract is *"do what `risk_engine`
does"* -- ⭐ derive from the authoritative store on read, ⛔ never from a cached local
belief. ⭐ Record the line reference as the in-house precedent, ⭐ and use it as the
defence against scope creep: ⭐ **an existing pattern applied one layer down.**

## 🔴 04-Sep VERDICT: **NOT EXERCISED** -- F1/F2/F1b STILL HAVE NEVER RUN

🔬 Both passes ran **exactly on schedule** and found an empty book:
    15:03:00.524  MIS_AUTO_SQUAREOFF_SCAN mis_candidates:0 pass:PASS_1
    15:03:00.524  mis_autosquareoff PASS_1: FLAT (0 MIS positions)
    15:06:00.544  ... PASS_2: FLAT (0 MIS positions)
⇒ ⛔ **No cancel, no exit, no restore.** ⭐ The restore path is **still unexecuted in
production**, ⭐ and Monday carries the same uncertainty. ⛔ Do NOT record this day as
a clean run of F1b -- ⭐ it is `NOT EXERCISED`.

⭐ **What WAS proven live 04-Sep:**
  · ⭐ the **new schedule fires correctly** -- 🔬 15:03:00.524 / 15:06:00.544, ⭐ within
    ~0.5 s. ⭐ First live confirmation of 15:07/15:10 → 15:03/15:06.
  · ⭐ **F PRE_PASS self-test `BOTH_ACCEPTED`** @15:01:00 (⭐ telegram 655 ms, ⭐ email
    3315 ms, `boot_id a30db9512fe1`).
  · ⭐ the **FLAT branch** is a clean quiet no-op -- ⛔ no spurious CRITICAL.
  · ⭐ F1b **runtime activation** (⭐ see above) -- ⛔ but activation ≠ execution.
