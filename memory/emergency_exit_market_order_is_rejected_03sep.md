---
name: emergency_exit_market_order_is_rejected_03sep
description: "The MIS squareoff cancels protective orders then refuses to exit on a 15ms confirmation poll, and the emergency fallback places a raw MARKET order Zerodha rejects -- so the system has no working forced exit. Measured 03-Sep-2026 on ANANTRAJ."
metadata: 
  node_type: memory
  type: project
  originSessionId: 06b31989-21eb-4564-93cc-440dab44786c
  modified: 2026-09-03T18:19:18.638Z
---

🔬 **MEASURED 03-Sep-2026** from `logs/system_2026-09-03.log`, `trading_system.db`
(read-only) and the deployed source at `2d08436`.
📄 Full record: `docs/incident/2026-09-03_naked_position_ANANTRAJ.md`

## 🔴 D1 — THE EMERGENCY EXIT CANNOT PLACE AN ORDER AT THIS BROKER
🔬 `order_reconciler.py:_check9_missing_exits` (~2996) places
`order_type="MARKET", price=0.0` with ⛔ no LTP, ⛔ no `market_protection`,
⛔ no limit fallback. 🔬 Zerodha rejects it **every time**: *"Market orders without
market protection are not allowed via API."* — 🔬 **8 rejections in 2 minutes.**
🔴 ⭐ **The fix already exists ~680 lines ABOVE, in the same file** (~2317):
`marketable_limit_price(...)` + `order_type="LIMIT"`.
🔴 ⭐ **AND THE CONSTRAINT WAS KNOWN SINCE 10-JUL** — `scripts/t2_cnc_gtt_realtest.py`
documents *"the 10-Jul canary block"* and claims its marketable LIMIT is
*"identical to the live emergency-exit path"*. 🔬 **That parity claim is FALSE.**
⚠️ 🔬 This same path was already rejected once before — **01-Jul BANSALWIRE**, tag
length — ⇒ ⭐ **twice in production, each time only the symptom was fixed.**
🔬 **COMPOUNDING:** `mis_autosquareoff.py:71` `PASS_2_EXIT_PROTOCOL="MARKET"` and
`:546` use MARKET for **both** passes ⇒ ⭐ even a passing cancel-guard would have
been rejected. ⭐ **Two independent reasons the position could not be auto-exited.**
⇒ ⛔ **Treat EVERY MARKET call site as a path that has never worked in live**
until one is observed to fill. 🔬 40 matches; exit-path ones listed in the record.

## 🔴 D2 — THE CANCEL GUARD DESTROYS PROTECTION, THEN REFUSES TO EXIT
🔬 `mis_autosquareoff.py:565-579` `_verify_cancelled` polls `get_order_history`
**ONCE, ~15 ms after the cancel**, ⛔ no retry, ⛔ no sleep, ⛔ no re-read.
🔬 The cancels **succeeded** (`success=True`); 🔬 the same orders read **terminal
1.1 s later**. ⇒ ⭐ The guard needed to wait one second and waited zero.
🔴 ⭐ **Ordering is what makes it dangerous:** cancels are sent FIRST, verification
runs AFTER ⇒ a verification miss leaves the position with protection **already
destroyed** and no exit submitted.
⚠️ ⛔ **CORRECTION to the standing description:** it does ⛔ NOT "decide on the
cancel call's return value" — ⭐ it DOES re-read the broker. ⭐ The defect is
**TIMING**, ⛔ not source-of-truth. ⭐ That changes the fix.

## 🔴 D4 — THE TRADE ROW MIS-ATTRIBUTES THE RESCUE
🔬 One `trades` row, self-contradictory: `exit_reason=MANUAL` ·
`status=CLOSED_MANUAL` · but `closure_source=**OWN_SL**` · `exits_verified=1` ·
`exits_verify_detail="ok"`.
🔬 **Provably false:** all three protective orders ended `CANCELLED` with
`qty_filled=0` — ⛔ **no SL ever filled.**
⇒ 🔴 ⭐ **A post-trade review reading this row sees a normal SL exit and finds
nothing to investigate.** ⭐ The naked window is invisible in the trade record.

## 🔬 ROUND 2 — THE BROKER BOOK (pulled 03-Sep evening, token expired 04-Sep 05:00)
📄 `docs/incident/2026-09-03_ANANTRAJ_broker_book.json` (sha256 `6b76425e…`)
- ✅ **Naked was REAL.** 🔬 `…7099` CANCELLED **at the exchange 15:10:03**.
  ⇒ ⭐ CHECK9's detector is **CORRECT**, ⛔ not a false positive. ⛔ No 6th defect.
- 🔴 **What flattened it: `260903171167107` — SELL `MARKET`, COMPLETE, 628.05,
  15:12:11, `tag=None`.** ⭐ Every system order is tagged ⇒ 👤 Rama's manual close.
  ⇒ 🔴 ⭐ **A MARKET order FILLED — from the UI.** ⭐ Kite applies protection in the
  UI and **refuses it via API** without `market_protection`. ⭐ Exposure **≈2m20s**
  (11.5 s + 2 m 08 s), ⛔ not 2 m 22 s — ⭐ it ends at the FILL, ⛔ not the observation.
- 🔴 **THE MIS SQUAREOFF EXIT HAS NEVER EXECUTED.** 🔬 All 27 `leg='EOD'` orders
  ever: 26@15:17 + 1@10:00, **all LIMIT**; **ZERO** in 15:07-15:12. ⇒ ⭐ Its MARKET
  defect never surfaced because ⛔ the path has never run. ⭐ 3rd *"built yet inert"*.
- 🔴 **WHY G5b NEVER RE-FIRED — a SOURCE-OF-TRUTH SPLIT, ⛔ not SOFT_KILL.**
  🔬 G5b is gated by `get_sl_order_for_trade()` = the **LOCAL** table; 🔬 that row
  stayed non-terminal until **15:17:04** (7 min after the exchange cancel) ⇒
  `sl_row is not None` ⇒ ⛔ **G5b was never called.** ⇒ ⭐ The system believed the
  position **naked (CHECK9/broker)** and **protected (G5b/local)** at once — ⭐ and
  the remedy that had just worked was the suppressed one.
- **D5:** 🔬 8 identical rejections over 111.4 s. ⛔ No retryable-vs-terminal
  classification. ⭐ A validation error is permanent ⇒ escalate, ⛔ never loop.
- 🔬 **SHAs:** bare main `2d08436`, deployed tree Δ**0** ⇒ running code IS `2d08436`;
  TREE/rollback `39292d3` ⛔ is NOT the running code ⇒ ⭐ the TREE advance is now a
  **prerequisite of the exit-path fix**, ⛔ not a GUI leftover.

## 🔴 A VACUOUS QUERY I ALMOST FILED AS A SYSTEMIC FINDING
🔬 *"`OWN_SL` trades with no SL `qty_filled>0`"* returned **74 of 74** — ⭐ which
reads as *"every exit-attribution analysis is contaminated."*
🔴 ⛔ **It could not have returned anything else:** 🔬 across **all 1315 orders**,
`qty_filled>0` = **0** and `avg_fill_price>0` = **0**. ⭐ Both columns are **dead**.
🔬 Re-run on `status='COMPLETE'` (populated: 623 orders / 159 SL legs) ⇒ **exactly
1** — ANANTRAJ. ⇒ ⭐ **D4 is NARROW, ⛔ not systemic.**
⇒ ⭐ RULE: ⛔ never report a count from a column without first proving the column can
hold the other answer → [[a_floor_is_not_a_non_vacuity_check]]
⚠️ Standing: ⛔ `orders.qty_filled` / `orders.avg_fill_price` are **never populated** —
⛔ any analysis reading them is reading zeros.

## 🔬 ROUND 3 — MEASUREMENT CLOSED. ⭐ THREE OF RAMA'S OWN HYPOTHESES KILLED.
- 🔴 **§4.1 — neither the tag nor `pending_quantity`.** 🔬 `pending_quantity`
  appears in **0 files**; 🔬 the local row carries the **correct `trade_id`** (tag
  never broke association). ⭐ The row went terminal at 15:17:04 via *"Sweep:
  marked 1 stale orders as CANCELLED (parent trade terminal)"*.
  ⇒ ⭐ **Root cause: nothing polls a non-entry order's status between placement and
  a terminal-parent sweep.** ⭐ The reconciler deferred to `order_monitor`; 🔬 that
  produced **1** log line all day.
- 🔴 **§4.2 — "four manual interventions" is FALSE.** 🔬 KIRIINDUS/HIKAL/RBLBANK are
  **`GTT_EXIT`** — ⭐ a broker GTT is placed by Zerodha's engine and carries **no
  tag**. ⇒ ⛔ *"untagged ⇒ manual"* does not hold. ⭐ Only ANANTRAJ is MANUAL ⇒
  ⭐ **D4 stays NARROW.** ⭐ Also explains RBLBANK's MARKET fill: ⭐ GTT engine, ⛔ not
  `place_order`.
- 🔴 **§4.3 — 🔬 `orders WHERE order_type='MARKET'` = 0 rows of 1315.** ⇒ ⭐ The
  system has **never even recorded placing** a MARKET order. ⭐ Both MARKET fills
  today came from the **GTT engine** and 👤 **Rama's UI** — ⛔ neither via the API.
- 🔴 **§4.4 — D6 is a data-hygiene gap, ⛔ NOT a live defect.** 🔬 `trades.qty_filled`
  **335/844 populated** (= the 335 COMPLETE entries); 🔬 only `orders.qty_filled` /
  `orders.avg_fill_price` are dead, and 🔬 **0 of 286 refs read them** (the one
  candidate is an INSERT writing 0). ⇒ ⛔ *"exit sizing computes from zero"* is
  **not supported**.
- **§4.5 — exactly TWO defect sites:** 🔬 `mis_autosquareoff.py` (⛔ does not even
  import `marketable_limit_price`; raw MARKET on **both** passes `:71`/`:546`) and
  🔬 `order_reconciler.py` check9 (~3000, ⛔ no LTP fetch). ⭐ Every other site
  converts. ⚠️ **Residual class:** all converting sites fall back to raw MARKET when
  LTP is missing ⇒ ⭐ **"no quote" means "no exit", silently.**
- 🔴 **DOUBLE-SELL RISK (👤 FILE 127 §2):** 🔬 last emergency attempt **15:12:09**,
  👤 Rama's fill **15:12:11** — **2 s**. ⇒ ⭐ **The only reason there was no double
  sell is that the exit was broken.** ⇒ ⭐ Any fix MUST re-read the broker position
  immediately before submitting. ⭐ The racing party is a **human**; ⛔ no internal
  lock sees him.

## 🔴 ROUND 4 — DESIGN. ⭐ TWO FINDINGS THAT CHANGE THE PICTURE.
📄 `docs/design/2026-09-03_exit_path_design.md`
- 🔴 **THERE IS A WORKING MIS BACKSTOP, and it is not the one anyone was looking
  at.** 🔬 `closure_source='OWN_EOD'` = **27 closures, ALL product MIS**, and their
  `leg='EOD'` orders are **27/27 `LIMIT` + `COMPLETE`.** ⇒ ⭐ The system's **15:17
  `eod_squareoff` works, 27 for 27, because it uses LIMIT.** ⭐ It is the proven
  payload shape any fix should copy.
  ⇒ ⭐ **The real exposure window is 15:07 → 15:17** (MIS squareoff never ran;
  check9 rejected 8×). ⚠️ 🔬 In that window **4 MIS positions closed via
  `EXTERNAL_UNATTRIBUTED`** (COALINDIA 15:09:01 · TATAPOWER 15:12:47 · HDFCSILVER
  15:15:01 · MOSCHIP 15:16:35) — ⛔ **broker cutoff vs manual close is NOT
  determinable**; the label means unattributed, both are untagged, and those
  broker books are gone. ⭐ Flat fact; ⛔ not an argument for any option.
- 🔴 **THE DB TELLS A FALSE STORY.** 🔬 A rejected order returns no `order_id` ⇒
  **no row** ⇒ 🔬 `order_type='MARKET'` is 0 of 1315 **despite 8 attempts**.
  ⇒ ⭐ The DB alone reports ANANTRAJ as *"a clean, verified stop-loss exit"*
  (`OWN_SL`, `exits_verified=1`, ⛔ no failed-exit rows, ⛔ no naked window) — ⭐ every
  part false, ⛔ nothing in the DB contradicting it. ⭐ **Only the log knows.**
  ⇒ ⭐ **RULE: persist attempted-and-rejected orders, or the failure is
  unmeasurable and the fix unprovable.** ⭐ It is now **commit 1**.
- ⭐ **O3 — CONVERT THE INCUMBENT** (👤 Rama's, ⛔ not mine): ⛔ neither
  cancel-then-place (⇒ zero protection) nor place-then-cancel (⇒ 🔬 **three resting
  sells against a qty-1 long**). ⭐ Instead **`modify_order` the resting SL into the
  exit**, cancelling only the far-OTM TGT ⇒ ⭐ ≥1 exit-capable order always rests,
  ⛔ never more than position qty. 🔬 **Kite lists `order_type` as modifiable**
  (*"order_type, quantity, price, trigger_price, disclosed_quantity, validity"*)
  ⇒ ⭐ plausible — ⛔ **but SL→LIMIT conversion, the SELL-SL trigger rule and modify
  rate limits are all UNSTATED** ⇒ ⛔ **not adoptable on doc evidence; needs a live
  drill.**
- ⚠️ **`order_monitor` is the 5th "built yet inert" instance** (🔬 1 log line/day).
  ⭐ The design **routes around** it ⇒ ⛔ every other consumer of local order state
  stays stale. ⏸ Recorded, ⛔ not fixed.

## 🟢 ROUND 5 — BUILT + TESTED 03-Sep NIGHT (T1, T2). ⭐ 4 MORE HYPOTHESES KILLED.
👤 Authorisation: *"We must built>push today, No postponement please"* ⇒ ⭐ build/
test/commit authorised; ⛔ enabling an unproven live path was NOT.
- ✅ **T1 `cc2aeae`** — `MISSING_EXITS` SOFT_KILL now gets its **own** body: states
  *no exit order at the broker*, *NOT managed to SL/TGT*, *manual flattening may
  be required now*. ⭐ A **new branch**, ⛔ not a rewrite — every other reason keeps
  the (true) shared wording, pinned by a test. ⭐ 12 tests pass.
- ✅ **T2 `80091ce`** — `_classify_broker_error` over the adapter's **existing**
  translated taxonomy: TERMINAL (`BrokerAuthError`, or `OrderRejectedError` on a
  **measured** allow-list) · STATE_UNKNOWN (placement timeout — ⛔ may have landed,
  ⛔ no blind retry) · RETRYABLE (**everything else, incl. unrecognised**).
  🔬 Allow-list is **one entry**, pinned by a test so ⛔ nobody widens it from
  reasoning. ⭐ 9 tests pass. ⭐ Net: **fewer orders, louder alerts.**
- 🔴 **WHY FIX-155's GUARD COULD NEVER FIRE (root cause of the 8 retries):** 🔬 it
  queries for an `orders` row `leg='EOD' AND order_type='MARKET' AND status IN
  (PENDING,SUBMITTED,OPEN)` — ⛔ but a **rejected order persists no row**. ⭐ The
  guard had nothing to find. ⭐ Same fact as `order_type='MARKET'` = 0 of 1315.
- 🔴 **§5.1 THE 15:12 vs 15:17 "CONTRADICTION" DISSOLVES — ⛔ there is none.**
  📄 Zerodha (cited): **CAS stocks 3:12 PM · non-CAS 3:25 PM · F&O 3:26 PM**.
  ⇒ ⭐ The config's `mis_squareoff_cutoff 15:12` is the **CAS** (earliest) time and
  is **correct**; ⭐ the 15:17 EOD pass precedes the **non-CAS 15:25** deadline —
  ⭐ which is exactly why 27/27 EOD exits succeeded.
  ⚠️ 🔴 **NEW RESIDUAL RISK:** for a **CAS stock** the broker squares off at
  **15:12**, ⛔ BEFORE the system's 15:17 EOD pass ⇒ ⭐ broker force-close +
  ₹50+GST. ⭐ And 📄 *"you cannot place fresh MIS/CO orders after the auto
  square-off time"* ⇒ ⛔ after the cutoff the emergency exit **cannot place at all**.
- ⛔ **KILLED (FILE 129 §2.1/§2.2):** 🔬 the 27 EOD orders are **21 SELL + 6 BUY**
  ⇒ ⭐ the BUY branch **HAS** run in production; ⛔ not a 6th "built yet inert".
  🔬 `marketable_limit_price` **does** invert (SELL→`mode="down"`, BUY→`mode="up"`).
  🔬 History holds **40 BUY SLs, 38 BUY TGTs, 39 filled SHORT trades** ⇒ ⛔ the
  short side is **not** untested; ⭐ FILE 129 §1's "zero BUY SL" was **today only**.
- ⚠️ 🔬 **A pre-existing RED test already encodes the fix:** `test_fix181.py::
  TestStep4_ReconcilerInflightOrphan::test_inflight_orphan_flattened_when_kill_
  active` asserts `order_type == "LIMIT"` and gets **`MARKET`**. ⭐ It is in the
  baseline 10F. ⇒ ⭐ The codebase has been carrying a red test asserting the very
  thing RC-1 must fix. 🔬 Proven pre-existing by stashing T2 and re-running.

## 🟢 ROUND 6 — PUSHED `80091ce`. ⭐ AND A SECOND OCCURRENCE FOUND.
👤 *"Take Option:1 & close it"* ⇒ ⭐ C0 TREE advance + push authorised.
- ✅ **PUSHED:** `2d08436 → 80091ce` (T1 `cc2aeae` + T2 `80091ce`). 🔬 PC = VM bare
  = deployed tree, **0** differing tracked files; ⭐ both changed sources present on
  the VM; ⭐ hook re-installed the crontab. ⭐ Engine **inactive**; ⛔ MIS NOT enabled.
  ⭐ Regression wording: *"C1+C2 introduced **zero new failures**; the existing 10
  remain unchanged"* — ⛔ never *"the suite is green."*
- 🗿 **ROLLBACK TREE ADVANCED `39292d3` → `2d08436`** 👤 on Rama's Option-1 line.

## 🔴 ROUND 6 CORRECTION — MY *"MIS SQUAREOFF NEVER EXECUTED"* PROOF WAS INVALID
🔴 🔬 `orders/mis_autosquareoff.py` has **NO `insert_order`, NO order-manager
import** — ⭐ it only *reads* the store. ⇒ ⛔ **It never persists its exit order.**
⇒ 🔴 ⭐ So *"0 of 27 `leg='EOD'` orders in the 15:07-15:12 window"* **proved
nothing** — ⭐ exactly like a rejected order, an executed one would leave no row.
👤 FILE 131 §4.1(b) demanded this check and it **overturned my finding.**
⭐ **The conclusion survives on BETTER evidence:** 🔬 across the retained logs
(25-Aug→03-Sep; ⭐ the module only shipped **28-Aug**, so this is nearly its whole
life) the outcome tally is **3 CANCEL_FAILED · 3 MIS_REMAINS · 0 EXIT_SUBMITTED**.
⇒ ⭐ Say *"no exit has been observed in the retained window"*, ⛔ never *"never
executed"* from the EOD-order query.

## 🔴 SECOND OCCURRENCE — 02-Sep COALINDIA. ⭐ IT IS A PATTERN, ⛔ NOT AN INCIDENT.
🔬 02-Sep: `15:07:02.676 CANCEL_FAILED PASS_1 COALINDIA … exit NOT submitted` ·
`15:07:06 MIS_REMAINS` · `15:07:15.147 G5b CRASH_RECOVERY_SL … placing recovery
order` · `15:09:02 CHECK1 MANUAL_CLOSE … EXTERNAL_UNAT…` · `15:10:00 PASS_2 FLAT`.
🔬 **0** CHECK9, **0** emergency failures, **0** market-protection rejections.
⇒ ⭐ **THE ESCALATION STEP IS PASS_2:**
  · ⭐ PASS_1 alone ⇒ cancels protections, no exit ⇒ naked ~12 s ⇒ **G5b recovers**.
    ⭐ Survivable — that is 02-Sep.
  · 🔴 ⭐ PASS_2 ⇒ cancels the **recovery SL too** ⇒ naked again ⇒ ⛔ G5b blocked by
    the stale local row ⇒ CHECK9 ⇒ MARKET rejected ⇒ **2 m+ naked**. ⭐ That is 03-Sep.
⇒ ⭐ **Twice in two trading days.** ⭐ Both times the passes delivered **zero** exits
and **created** the naked window.

## 🔬 §4.1 ANSWERS (👤 FILE 131)
- **(a) ⛔ NO config-only disable exists.** 🔬 Config has only
  `mis_squareoff_{cutoff,first_offset,second_offset,margin_sec}` — ⛔ no `enabled`.
  🔬 `main.py:3325` constructs and `start_polling()`s it **unconditionally**; ⛔ the
  module has no gate; 🔬 `_validate_mis_squareoff_timing` enforces
  `entry_end < CHECK_1 < CHECK_2 < cutoff < eod` ⇒ ⛔ offsets cannot stand it down.
  ⇒ ⭐ **Fork (ii): disabling the passes needs CODE.**
- **(b)** ⭐ answered above — ⭐ the finding stands, ⭐ on log evidence.
- **(c)** ⚠️ Other cancel sites exist (`order_placer:4531/4609` trail-replace ·
  `order_reconciler:1715` CHECK1 orphan · `:3541` duplicate/sweep ·
  `structure_exit_manager:389` · `kill_switch:1634` hard-kill only). 🔬 In **both**
  observed incidents the naked window came **solely** from the MIS passes.
  ⛔ Whether another site could also strand a position is **NOT established**.

## 🔴 ROUND 7 — THE PERSISTENCE GAP IS A LATENT DOUBLE-SELL, AND C6 ARMS IT
🔬 **`mis_autosquareoff` DOES submit** — `self._adapter.place_order(...)` at
**`:541`**, `tag=f"mis_autosq_{which.lower()}"`. 🔬 Its **only** store interaction
is a **READ** (`get_open_mis_exit_orders_for_symbol` `:500`) — ⛔ **no
`insert_order`, no order-manager, no write of any kind.**
⇒ ⭐ `PASS_2_EXIT_PROTOCOL = "MARKET"` (`:71`, used `:546`) is **LIVE config**,
⛔ NOT dead — ⭐ PASS_1 hardcodes `"MARKET"`, PASS_2 reads the constant.
⇒ 🔴 ⭐ **A successfully submitted MIS exit rests at the broker INVISIBLE to the
local order store.** ⭐ CHECK9/G5b decide from local state ⇒ ⭐ they would see *"no
active SL"*, act, and place a **SECOND SELL** against the same position.
⇒ 🔴 ⭐ **C6 (the payload fix) is what ARMS this** — ⭐ the path is dormant only
because 🔬 `EXIT_SUBMITTED` = 0. ⛔ **C5 does NOT cover it:** ⭐ C5 re-reads the
broker **position**, ⭐ which is still open while an unfilled exit rests.
⇒ ⭐ **HARD DEPENDENCY: C6 ships only alongside `mis_autosquareoff` persistence.**
⭐ Sharpest instance yet of the standing root cause — ⭐ *the local order table is
stale and incomplete and safety logic trusts it* — ⭐ because **the fix is the
trigger**.

## 🔴 PASS_2 IS THE FATAL STEP — ⛔ NOT PASS_1 (👤 FILE 132 §1)
🔬 Same start, different ending, two consecutive trading days:
- **02-Sep COALINDIA** — PASS_1 CANCEL_FAILED 15:07:02 ⇒ naked ⇒ ⭐ **G5b recovered
  15:07:15 (13 s)** ⇒ closed externally 15:09:02 ⇒ PASS_2 found **FLAT** ⇒ ⛔ no
  CHECK9, ⛔ no rejections, ⛔ **no incident**.
- **03-Sep ANANTRAJ** — PASS_1 CANCEL_FAILED 15:07:04 ⇒ naked ⇒ ⭐ G5b recovered
  15:07:16 (12 s) ⇒ 🔴 **survived 2 m 59 s to PASS_2 15:10:03**, which cancelled the
  **recovery** SL ⇒ ⛔ G5b blocked by the stale local row ⇒ CHECK9 ⇒ 8 rejections.
⇒ ⭐ **The single variable is whether the position is still open at PASS_2.**
⇒ ⭐ **PASS_1 is survivable** (G5b re-protects in ~12 s, 2 of 2). 🔴 ⭐ **PASS_2 makes
it an incident** — ⭐ it cancels the very order G5b just placed, ⭐ and G5b cannot
re-fire. ⇒ ⭐ **Minimal intervention = disable PASS_2**, ⛔ not both passes.
⚠️ ⛔ But there is **no config-only route** (measured) ⇒ ⭐ the switch is CODE ⇒
⭐ sandbox. ⛔ Not before an open. 📄 That is how 01-Jul and 03-Sep both happened.
⛔ ⭐ Moving `entry_end` earlier would NOT have helped — 🔬 ANANTRAJ entered
**10:01:33** and was still open at 15:07.

## 🔴 THE MIS DECISION IS NO LONGER A RISK — IT IS A NEAR-CERTAINTY
🔬 Module shipped **28-Aug** ⇒ ~5 trading days. 🔬 A position was open at a pass on
**2** of them. 🔬 **Both** failed. ⇒ 🔬 **3 attempts, 3 CANCEL_FAILED, 0 exits.**
⇒ ⭐ Enabling MIS is ⛔ not *"accepting a risk"* — ⭐ it is **scheduling a manual
intervention**. ⭐ 👤 Rama must be at the screen **15:07-15:17**.
⭐ What C1+C2 bought: ⭐ **one clear escalation** instead of 8 misleading CRITICALs,
⭐ and the alert ⛔ no longer claims the position is managed to SL/TGT.

## 🟢 ROUND 8 — STOP A BUILT (`5455ced`). ⭐ SCHEDULE + F2 + F1.
👤 *"Do whatever but try to implement>push now itself"* · 👤 *"2 checks before 1min
of zerodha's closing auto-square off"*.
- ⭐ **SCHEDULE:** cutoff **15:12 → 15:09**, offsets **5m/2m → 6m/3m** ⇒
  🔬 **PASS_1 15:03 · PASS_2 15:06 · cutoff 15:09**. ⭐ Invariant holds
  (`15:00 < 15:03 < 15:06 < 15:09 < 15:17`). ⇒ ⭐ Both passes + the post-pass
  verify finish **before the earliest possible broker action**.
  🔴 ⭐ **RULE (new, standing): ⛔ never design to the LATER of two conflicting
  broker deadlines.** 📄 Zerodha publishes **two** CAS figures — support page
  **15:12**, the 03-Aug-2026 post **15:10**. ⭐ 15:09 is safe under both.
  ⚠️ ⭐ KNOWN COST: 15:09 is universal ⇒ gives up **~16 min** of holding on
  non-CAS names (15:25). ⏸ Per-symbol CAS/non-CAS deadline is the end state.
- ⭐ **F2 — `_verify_cancelled` polls to a bounded 5 s budget** instead of once at
  +27-53 ms. ⛔ The mechanism was never wrong (it reads broker history); ⭐ the
  defect was **timing**. ⭐ A failed read no longer ends the poll. ⚠️ 5 s is a
  **budget from the schedule**, ⛔ NOT derived from the n=1 1.115 s figure.
- 🔴 ⭐ **F1 — `_restore_protection` puts the stop back on EVERY failure path.**
  ⭐ Re-places the SL with **its own** parameters read back from the local orders
  row (⛔ nothing recomputed). ⭐ Idempotent vs a stop already at the broker,
  ⭐ symbol-scoped, ⭐ proceeds when broker state is unknown (⭐ naked is worse than
  a duplicate; the reconciler's one-live-SL invariant catches duplicates).
  ⛔ TGT deliberately NOT restored — ⭐ it is upside, not protection.
- ⚠️ 🔴 **I BROKE MY OWN "NEVER RAISES" CONTRACT AND THE EXISTING SUITE CAUGHT IT.**
  🔬 A resting row without a `leg` key raised `KeyError` **inside an
  already-failing path** ⇒ ⭐ would have masked the original failure and skipped
  its alert. ⭐ Fixed with `_row_get` (dict / `sqlite3.Row` / attribute object) +
  an outer guard; ⭐ both now pinned by tests.
  ⇒ ⭐ RULE: ⭐ a helper that runs inside a failure path must be **proven** unable to
  raise, ⛔ not documented as such.
- ⭐ **Existing tests changed for the right reason:** `placed == []` would now pass
  a version that leaves the position **naked**. ⇒ ⭐ They assert the **two-sided**
  property: ⛔ no EXIT submitted **AND** ⭐ the stop restored.
- ⛔ **NOT shipped: the payload fix (MARKET → marketable LIMIT).** ⭐ It must not
  land before `mis_autosquareoff` **persists** what it places (§ROUND 7).

## 🔴 ROUND 9 — F1's DUPLICATE-SL RISK IS **NOT** CONTAINED. ⭐ NAMED + ACCEPTED.
👤 FILE 135 §2 asked whether the sibling/OCO net covers an F1-placed SL. 🔬 **It
does not**, and the reason is the persistence gap again:
- 🔬 `order_reconciler._check_duplicate_exits` (`:3472`) reads
  **`self._order_mgr.get_orders_for_trade(...)`** — ⭐ the **LOCAL orders table**.
  ⭐ `_dedupe_exit_leg` then cancels the LATER duplicate, keeping the earliest.
- 🔬 But `mis_autosquareoff` **persists nothing** (ROUND 7) ⇒ 🔴 ⭐ **an F1-placed
  restore SL has NO local row ⇒ the duplicate guard cannot see it.**
⇒ ⭐ **REACHABLE PATH:** `cancel_order` **rejected** (SL still resting at the
broker) **AND** `get_open_orders()` **fails** ⇒ F1 proceeds on unknown ⇒ **two
SLs at the same trigger** ⇒ both fill ⇒ ⭐ **naked short** — 📄 exactly the RAMCOIND
25-Jun outcome the dedupe net was built for.
⚠️ ⭐ **ACCEPTED, NAMED trade-off for Fri 04-Sep** (👤 FILE 135 §2): ⭐ a duplicate
stop beats **no** stop at 1-share sizes, ⭐ and it needs a **conjunction** of two
failures. ⛔ F1 is gate-verified and pushed — ⛔ do NOT change it tonight.
⇒ 🔴 ⭐ **F3 (persistence) FIXES THIS TOO** — ⭐ once F1's SL is persisted the dedupe
net sees it. ⇒ ⭐ That raises F3's priority: ⭐ it now unblocks **F4** *and* closes
this. ⛔ There is no broker-side OCO — the system uses software LIMIT_TRIPLE.

## ⭐ RULE CORRECTED (👤 FILE 135 §1) — ⛔ 15:10 AND 15:12 ARE NOT CONCURRENT
🔬 15:10 was the **03-Aug launch** figure; ⭐ Zerodha **revised it to 15:12 on
10-Aug** ⇒ ⭐ 15:12 is CURRENT, ⭐ 15:10 is **superseded**.
⇒ ⛔ **The FILE 134 rule *"use the earlier of two published figures"* is WRONG** —
⭐ it fails the moment a broker moves a deadline **earlier**.
⇒ ⭐ **REPLACEMENT RULE: hold a stated cushion below the broker's CURRENT published
deadline, and RE-VERIFY that deadline on a schedule.**
⭐ 15:09 is unaffected and correct: **3 min** below current 15:12, **1 min** below
the superseded 15:10. ⛔ Config unchanged.
🔴 ⏸ **STANDING OPS ITEM: re-verify Zerodha squareoff timings MONTHLY** against
`zerodha.com/marketintel/bulletin`. 🔬 They changed **twice in a month** (equity
15:20→15:25; CAS 15:10→15:12). ⛔ Nothing in the system re-checks them.

## ⭐ WHAT FRIDAY 04-Sep WILL LOOK LIKE — ⛔ 2-3 CRITICALs IS NOT A NEW EMERGENCY
⭐ If a MIS position is open at **15:03**:
⭐ PASS_1 cancels SL+TGT → ⭐ F2 settle window now **confirms** → ⭐ exit submitted →
🔴 **still MARKET, still rejected** (⛔ F4 not shipped) → ⭐ **F1 restores the stop**
→ ⭐ ONE CRITICAL. ⭐ **15:06** PASS_2 repeats. ⭐ **15:08** verify → restore + CRITICAL.
⇒ ⭐ Then the position rides to `eod_squareoff` **15:17** (non-CAS, 🔬 27/27 LIMIT)
or Zerodha's **15:12** (CAS, ₹50+GST).
⇒ ⭐ **The naked window is now SECONDS, ⛔ not minutes** (today: ~2 m 20 s).
⇒ 👤 **Rama watches 15:03-15:09.** ⛔ He does NOT need to flatten by hand unless an
alert says the **restore itself** failed. ⭐ Expect order churn (cancel + re-place
each cycle) — ⭐ placements/cancels are free; ⛔ only a broker auto-squareoff costs.

## 🔴 ROUND 10 — WHAT FIXED RAMCOIND, ⭐ AND TWO DIVERGENCES IN MY OWN F1
👤 FILE 137 §1: 🔬 duplicate-SL recurrence **IRFC 17-Jun · NIACL 22-Jun · RAMCOIND
25-Jun** — ⭐ three in nine days, ⭐ none since. ⭐ What closed it:
- 🔬 **Layer 1(a)** `_G5B_SETTLING_WINDOW_SEC = 10.0` — ⭐ skip recovery within 10 s
  of the persisted entry fill. ⭐ Its own comment: *"deterministically closes the
  ~40 ms TOCTOU race against the lagging local orders table."*
  ⇒ 🔴 ⭐ **A TIMING fix ⇒ it does NOTHING for F1** — ⭐ F1's missing row is
  **permanent**, ⛔ not a race. 👤 FILE 137 §1.1 confirmed.
- 🔬 **Layer 1(b)** `_already_has_live_sl()` — ⭐ **broker-authoritative**
  (`get_open_orders`, matching **symbol + exit_side + trigger_price > 0**).
  ⇒ ⭐ **This is the shape F1 already copies.** ⭐ Good.
- 🔬 Layer 2 `_check_duplicate_exits` (**local** orders) · 🔬 Layer 3
  `_detect_system_oversell` (**trades** table).

🔴 ⭐ **TWO DIVERGENCES BETWEEN MY F1 AND THE JUNE FIX — ⛔ both mine, ⏸ on the ledger:**
1. ⭐ **No second source on a failed read.** 🔬 `_already_has_live_sl` degrades to
   `order_placer._fill_map` (populated at placement, **ahead of** the local-table
   write) before concluding *"no SL"*. ⭐ F1 just **proceeds**. ⇒ ⭐ A ready-made
   improvement already exists in the codebase. ⏸ F3/F5.
2. ⚠️ ⭐ **Looser match.** 🔬 June matches `symbol + exit_side + trigger>0`; ⭐ F1 matches
   **`symbol + trigger>0` only**. ⇒ ⭐ A trigger-bearing order on the same symbol on
   the **other** side would read as *"protection present"* ⇒ 🔴 ⭐ F1 would **skip a
   genuine restore**. ⭐ Rare, ⛔ but it errs toward leaving the position naked —
   the wrong direction. ⏸ F3/F5.
⛔ Neither changed tonight — ⭐ F1 is gate-verified and pushed.

## 🔬 DOES LAYER 3 ACTUALLY RUN? ⭐ CAREFUL ANSWER: ⛔ NOT PROVEN, ⭐ BUT NOT DEAD
🔬 Retained logs 25-Aug → 03-Sep: **`SYSTEM_OVERSELL` = 0** occurrences.
🔬 But its **containing** check demonstrably runs: **4 × `CHECK2 INFLIGHT_ORPHAN`**
on **4 separate days** (26-Aug CYIENT · 27-Aug BIKAJI · 31-Aug NIACL · 01-Sep
HAPPSTMNDS), ⭐ plus daily `reconcile cycle` lines.
⇒ ⭐ **So `_detect_system_oversell` is UNTRIGGERED, ⛔ not demonstrably dead** —
⭐ materially better than the four *"built yet inert"* components, ⭐ whose containing
paths produced **nothing**. ⛔ But it is **not proven to run**, and 👤 FILE 137 §2 is
right that this project has been wrong on exactly that inference four times.
⇒ ⭐ State it as: *"the containing check is proven live; the oversell branch is
unobserved because no oversell has occurred since June."* ⛔ Never *"Layer 3
works."* ⭐ And it remains **remediation after both fills**, ⛔ not prevention.

## ⭐ FRIDAY RESIDUAL, QUANTIFIED (👤 FILE 137 §3)
⭐ The F1 duplicate needs **two simultaneous failures** (`cancel_order` rejected
**AND** `get_open_orders()` failing). ⭐ If both SLs fill ⇒ −1 ⇒ Layer 3 (⏸ if it
runs) flattens within its **300 s** lookback. 🔬 RAMCOIND's realised cost was
**~₹13.50**; ⭐ at today's sizes a 2 % move on one share is **₹5-13**.
⇒ ⭐ **~₹10-20 per occurrence, requiring two simultaneous broker failures** —
⭐ against the alternative of **no stop at all**, which is what happened on 03-Sep.
⭐ A good trade, ⭐ and now a number rather than a shrug.

## 🟢 ROUND 11 — DIVERGENCE 2 FIXED (`18dd6cc`) · ⏸ DIVERGENCE 1 DEFERRED
👤 FILE 138: ⭐ *"two divergences ≠ two bugs"* — ⭐ they fail in **opposite** directions.
- ✅ **DIVERGENCE 2 — FIXED.** ⭐ F1's idempotency matched `symbol + trigger>0` ⇒ ⭐ an
  **opposite-side** trigger order read as *"protected"* ⇒ 🔴 ⭐ **restore SKIPPED ⇒ no
  stop** — ⭐ the exact ANANTRAJ outcome. ⭐ Now `symbol + transaction_type +
  trigger>0`, ⭐ **the same predicate shape as the June RAMCOIND fix**
  (`_already_has_live_sl`), ⭐ reused ⛔ not reimplemented. ⭐ `exit_side` comes from
  the SL leg itself (SELL⇒LONG, BUY⇒SHORT) ⇒ ⭐ **side-symmetric by construction**.
  ⭐ The SL row is now recovered **before** the check — ⭐ its `transaction_type` is
  what makes the check side-aware.
  ⭐ **Reachable, ⛔ not theoretical:** 📄 product-blind gates + ⛔ no `trades.product`
  ⇒ ⭐ both pipelines can hold the same symbol ⇒ ⭐ a SHORT's BUY stop could suppress
  a LONG's restore.
  ⭐ **Direction:** ⭐ from *"no stop"* (⛔ unbounded tail) → *"possibly duplicate"*
  (⭐ bounded, Layer 3 behind it). ⭐ Strictly the right way round.
  🔬 **RED-proof, ⛔ not assumed:** ⭐ old predicate on the test fixture (LONG, only a
  BUY trigger order) ⇒ `protected=True` ⇒ **skip** ⇒ no stop; ⭐ new ⇒ `False` ⇒
  **restore placed**. ⭐ 21 tests in the file; ⭐ 109 across the three MIS suites.
- ⏸ 🔴 **DIVERGENCE 1 — DEFERRED, ⛔ DELIBERATELY. ⛔ It is a trade-off, ⛔ not a bug.**
  ⭐ June consults `order_placer._fill_map` before concluding *"no SL"*. ⛔ But
  `_fill_map` is **LOCAL state** — ⭐ it proves an **attempt was recorded**, ⛔ not that
  the broker holds the order. ⇒ 🔴 ⭐ **As a decision input it would let a stale entry
  say *"protected"* and RE-OPEN Divergence 2 by another route.**
  ⇒ ⭐ Error weighting: ⭐ a duplicate cost 🔬 ~₹13.50 (RAMCOIND) **and has a backstop**;
  ⭐ a skipped restore costs **the full tail**. ⇒ ⭐ **Proceed-on-unknown stays** — ⭐ it
  is already the safer choice.
  ⭐ **What WAS added: visibility.** ⭐ A failed broker read now logs
  **`PROTECTION_UNKNOWN`**, ⭐ distinct from a clean *"no SL found"* ⇒ ⛔ the record
  never conflates *"we know there is no stop"* with *"we could not find out"*.
  ⏸ ⭐ `_fill_map` may be admitted in **F3** as **corroboration only** — ⭐ a
  broker-acknowledged `order_id`, ⭐ matching symbol **AND** side, ⭐ within a bounded
  recency window. ⛔ Never as a bare presence check.

## ⚠️ TWO WORDINGS CORRECTED (👤 FILE 138 §3)
- ⭐ **Layer 3:** ⭐ *"container proven live, branch unobserved"* stands. ⛔ Never
  *"Layer 3 works."*
- 🔴 ⭐ **The ₹10-20 figure is an ORDER-OF-MAGNITUDE ESTIMATE, ⛔ NOT a bound.** ⭐ It
  comes from **n=1** (RAMCOIND ₹13.50) + an assumed 2 % move, ⭐ and the remediating
  branch **has never fired in production**. ⛔ Do not present it as a guaranteed
  maximum.

## ⭐ HOW TO APPLY
- ⛔ **Never say the system can force-flatten a position.** 🔬 It could not, twice,
  on 03-Sep. 👤 The live safety net is **Rama flattening by hand**.
- ⭐ 🔬 Kite docs (cited): parameter **`market_protection`**, values **>0..100** or
  **`-1`** (auto); *"only applicable for MARKET and SL-M"*; ⭐ and it **converts
  market orders to limit orders anyway** ⇒ ⭐ the repo's own `marketable_limit_price`
  reaches the same place with an explicit cap. ⛔ No fix designed yet.
- ⭐ **Exposure was ~11.5 s + ~2 m 22 s.** ⭐ Loss **₹2.13** only because price never
  reached the 620.08 trigger — ⭐ **luck, ⛔ not design.**
- ⛔ **The 15:07/15:10 passes are CORRECT** — 🔬 config `mis_squareoff_cutoff 15:12`
  −5m/−2m; `entry_end` is **15:00** since T5 (29-Jun). ⇒ ⛔ the *record* saying
  "15:15 cutoff" is STALE; ⭐ 15:17 is EOD, ⛔ not the MIS passes.
- ⭐ `trading-watchman` exited **cleanly** (`Result=success`, status 0) at 08:15:29
  ⇒ ⛔ **NOT causally linked** — it is a Gemini log monitor. ⚠️ But a "market-hours
  monitor" that exits at boot is ⛔ not monitoring: a **separate** fault.
See [[fix2_scored_14aug]] · [[schema_product_is_on_orders_05aug]]
