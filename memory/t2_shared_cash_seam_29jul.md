---
name: t2-shared-cash-seam-29jul
description: "29-Jul-2026 evening. AN ISOLATED DATABASE IS NOT AN ISOLATED ACCOUNT — T2's DB isolation is real and row-level verified, but CASH is shared. The T2 arm blocked Rs643.98 of broker cash the live system never learned about. The drift ladder did NOT fire and STRUCTURALLY CANNOT on this test — mechanism proven from source, four independent confirmations. Two premises in the asking card refuted. Also: reconcile_positions' first non-vacuous run in its whole history; PB-01 CLOSED at n=3."
metadata:
  node_type: memory
  type: project
  originSessionId: 464acc11-0f7d-4eac-9992-704ebb1cc075
  modified: 2026-07-30T05:36:59.567Z
---

# ⭐⭐ THE SEAM: AN ISOLATED DATABASE IS NOT AN ISOLATED ACCOUNT

T2's DB isolation is **real and verified at ROW LEVEL** (29-Jul: zero T2 symbols in
`fm_ledger` or `trades`, ever; zero live `gtt_state` rows). **CASH IS NOT ISOLATED**
and nobody had written that down. The arm blocked **₹643.98** of real broker margin
at 11:37–11:43 against a shared ₹9,997.40 account. **The same seam returns every time
delivery is exercised.** [[t2-arm-result-29jul]] [[slice25-execution-plan-27jul]]

## ✅ THE DRIFT LADDER DID NOT FIRE — AND STRUCTURALLY CANNOT ON THIS TEST
**SEARCH WIDTH:** case-insensitive `drift` across **every file in `logs/` (~98 files,
all names/dates)** *plus* the **entire systemd journal** for 29-Jul. Result: **3 lines,
all 08:15 boot INFO** (NTP drift · "capital drift handler subscribed (BL-2)" ·
ConfigValidator) — **byte-identical in class to the 28-Jul control**. Zero in
`reconciler_2026-07-29.log`. Zero in the journal.

**THREE INDEPENDENT REASONS, in the order they bind:**
1. ⭐ **The escalating publisher runs ONCE A DAY, at 09:15 — two hours before the arm.**
   `fund_manager.sync_from_broker` (FM9, `source_module="fund_manager"`) has exactly
   **ONE** production caller: `main.py:995`, a one-shot thread (`_run` waits for 09:15,
   syncs, returns — no loop). MEASURED today 09:15:00.055 `old=9997.4 new=9997.4
   delta=0.0` — below the `abs(delta)>1.0` publish gate, so it emitted **nothing even
   then**. ⇒ after 09:15 **nothing re-reads broker cash into the FundManager all day.**
2. ⭐ **The only check that DOES see broker cash is NON-ESCALATING by design.**
   G3 `_g3_capital_drift` compares `adapter.get_margins().net` vs `fm.get_snapshot()
   .total` every 15s — but publishes `source_module="order_reconciler"`, which is **NOT**
   in `_ESCALATING_SOURCES` (`{fund_manager, fund_manager_self_check,
   fund_manager_bucket_overflow}`). Per DH1 the handler logs INFO and returns **before
   touching the counter** ⇒ **G3 can never reach SOFT_ESCALATED. No rung. Ever.**
3. **G3 never reached its own alert threshold** — see the ₹5,000 allowance below.

## ⛔⛔ TWO PREMISES IN THE ASKING CARD WERE WRONG — BOTH REFUTED FROM SOURCE
- **"CHECK7 = `fund_manager_self_check` sees the ₹644."** ❌ CHECK7 compares the FM's
  in-memory `_reservations[rid].margin` against `sum_fm_ledger_margin_delta(rid)` —
  **internal bookkeeping vs internal ledger, per live reservation. It NEVER reads the
  broker.** T2 created no live reservation ⇒ CHECK7 had **literally nothing to iterate**.
  The 15s cadence was right; the **input** was wrong.
- **"3 consecutive LOG_ONLY cycles ≈ 45s ⇒ SOFT_ESCALATED."** ❌ The DH4 counter is only
  reachable from escalating sources, and the sole broker-cash escalating source **runs
  once per day**. ⭐ FM9 also **overwrites `_total` with the value it just read**, so a
  one-time step is one event and the next sample is NOISE (counter resets). **A step
  change can never produce three consecutive cycles.**

## ⚠️⚠️ THE REAL FINDING — FIX-182 WIDENS THE TOLERANCE BY Rs5,000 ON A Rs9,997 BOOK
CHECK2 classified all five T2 symbols **`HUMAN_ORDER`** at the exact arm timestamps
(MEASURED: IOB 11:37:47 · TRIDENT 11:42:07 · SOUTHBANK 11:42:38 · MSUMI 11:42:55 ·
SJVN 11:43:11) ⇒ `effective_tolerance += human_order_margin_tolerance = **₹5,000**`.
Today's G3 tolerance ladder against `expected=₹9,997.40` (frozen at 09:15):
  · 09:15→11:37 `max(50, 9997.40×0.10)` = **₹999.74**
  · 11:37→15:45 (+human) = **₹5,999.74**
  · 15:45→17:35 (`broker_margin_reliable` False, pct drops) = **₹5,050**
⇒ **while any human/untracked order exists, G3 would not notice a discrepancy up to
~50% of the account.** Deliberate (the alternative is CRITICAL spam) and correct here —
but **T2 GUARANTEES it happens, for the whole day, every time.** Register, do not tune.
⭐ Without the allowance the arm alone (₹643.98) had only **₹355.76** of headroom.

## ✅ FOUR INDEPENDENT CONFIRMATIONS (not one grep four times)
(a) log+journal absence, width above · (b) **`fm_ledger` `SYNC` = 1 today** — the sync
ran exactly once, from the DB not the log · (c) EOD report **"✅ Capital drift events:
0"**, computed by the system itself · (d) source-level reachability, above.

## ⏭️ TOMORROW (30-Jul) — NO, THE REVERSE SWING CANNOT TRIP THE LADDER
**The 08:15 boot RE-BASELINES.** FM seeds from `broker.net` (MEASURED precedent today:
`fund_manager.initialize total=9997.4`, = broker net) ⇒ tomorrow it seeds ≈ **₹9,353.42**
(cash already net of the ₹644) and the 09:15 sync sees delta ≈ 0. **The arm's ₹644 is
absorbed into tomorrow's baseline; only the RELEASE shows as drift.**
· delta after the ~09:20 closes ≈ **+₹644** vs in-session tolerance `max(50,
  9353.42×0.10)` = **₹935.34** ⇒ **silent, headroom ~₹291** [ESTIMATED].
· ⭐ MIS deployment from 10:00 moves delta **toward zero**, not away — they offset.
  Empirical bound: today 09:15–11:37 ran at a ₹999.74 tolerance with no alert ⇒ peak
  MIS margin < ₹999.74 [MEASURED by absence].
· **Even if it exceeded: ONE throttled CRITICAL Telegram. No kill. Entries unaffected.**
· ⚠️ The 5 GTTs get **WARN only, no `gtt_state` row** (`adopt_no_trade`, candidates==0)
  ⇒ `delivery_symbols` stays empty tomorrow too.
⇒ Briefing line, **not a fix**. Written into `Downloads/THU_30-JUL_T2_CLOSE_COMMANDS.txt` §A2.

## 🆕 A REAL NEW FINDING: `reconcile_positions` HAD ITS FIRST NON-VACUOUS RUN EVER
15:45 cron **FAILED exit 2** — prior 11 runs (14→28-Jul) **all SUCCESS**. MEASURED:
`position_reconciliation` holds **5 rows across 1 date — the whole table, all time.**
All five = `ORPHAN_AT_BROKER broker_qty=3 system_qty=0` (the T2 basket).
⭐⭐ **Every prior SUCCESS was an empty-book run — a green check that COULD NOT have
been red.** The FAILED is the job **working**, not breaking. One CRITICAL sentinel
written 15:45:02, **delivered 15:46:02** (Rama already has it).
⛔⛔ **RETRACTED 30-Jul — this file said "tomorrow 15:45 is a free second witness on
the closes (SUCCESS = sold)". FALSE.** The job reads `positions()` only, never
`holdings()`, so from T+1 it cannot see the basket either way and returns SUCCESS
regardless. **Wednesday's exit 2 fired only because Wednesday was the BUY day.**
⇒ it is **no witness at all.** [[reconcile-positions-blind-t1-30jul]]

## ✅ PB-01 25→12 — CLOSED, and the register was MISLABELLED
**WIDTH FIRST:** `pb01_capture` has run **exactly 3 times ever** (27/28/29-Jul, all
11:30:0x SUCCESS); table = **52 rows / 3 dates**. Not pruned — that is the feature's
whole life. Series by CAPTURE date: **25 → 12 → 15**. ⇒ **not a trend; it recovered
next day. n=3 cannot support "anomalous".**
⭐ **12 is what was CAPTURED, not what survived** — the 30-Jul cohort is 15 rows all
`PENDING`; survival is tracked separately in `status` (28-Jul: 15/25 `SKIPPED_GAP`;
29-Jul: 6/12). ⇒ fewer qualifying setups at capture = **market/input side**, NOT more
rejections, NOT capture truncation. ⛔ **Two label corrections:** `trading_date` is
**FORWARD-dated** (rows written 11:30 the PRIOR day), and there is **no 17:00 pb01
heartbeat in the entire history** — the 28-Jul handoff's "`pb01_capture SUCCESS
17:00:04` / 12 rows dated 28-Jul" named the wrong job and the wrong date (28-Jul had
**25**; the 12 was 29-Jul's). [[silent-failure-gaps-25jul]]

## ✅ §B/§C — THE MISSED EVENING CHECKS, RUN AS POST-MORTEM (expected state stated first)
- **B1 17:35 self-exit PASSED:** `inactive(dead)` · `Result=success` · `ExecMainStatus=0`
  · exit **17:35:04** · `NRestarts=0` · start 08:15:15 unbroken.
- **B2 census — 7 lines, ALL SEVEN CLASSIFIED, zero unexplained.** Comparables
  22/23/24/27/28/**29**-Jul = 6/11/12/13/9/**7** (2nd-lowest). 1 CRITICAL 08:15 prior-day
  kill notice · 3 CRITICAL 15:15 routine circuit-breaker triple (reason appears 4× daily
  by design) · 2 ERROR = **one** `slippage_exceeded` (TFCILTD) × 2 loggers = the guard
  refusing an entry · 1 ERROR `order_placer` orphan-TGT cancel refused mid-fill
  (= the known CHECK1 mid-fill class, `check1_mid_fill_defer_sec=0.0` OFF).
- **B3 capital PASSED:** **RESERVE 39 = RELEASE 30 + COMMIT 9**; COMMIT 9 = RELEASE_USED
  9 = 9 trades; **ZERO orphaned reservations**; **ZERO T2 contamination**; `RESET_PNL`
  present (the routine 15:15 kill did not forfeit it).
- **B4 book:** live DB **flat, 0 open** (⚠️ the first query ERRORED on a bad column and
  read as a blank pass — re-run properly; *a green check is evidence only if it could
  have been red*). 7 CLOSED + 2 CLOSED_MANUAL, net **₹7.36** live; +T2 unrealized
  ≈ Rama's screen **₹13.28** [ESTIMATED]. Broker holds 5 CNC — **the test, not a finding**.
- **C — the stray-`.pyc` detector's FIRST production run: PREDICTION HELD.** Predicted 0
  stray *before* reading (walk root excludes only `venv`/`sats`, so the five new
  `t2_proof_*` dirs **are** in scope but hold SQLite, not bytecode). Got
  **`✅ no .pyc outside __pycache__`**, **0 violations**, 11 warnings, report 4,807 B
  (28-Jul: 4,242 B). 🏷️ **"ran once in production" — an OCCASION, NOT a property.**

## ⚠️ K1 IS LIVE IN TONIGHT'S EOD REPORT AND IT LANDS ON THE CLOSE MORNING
`reports/system_manager/2026-07-29.txt` says *"Kill switch: SOFT_KILL — needs
`deploy/resume.sh` before market open"*. **FALSE** — a scheduled reason auto-clears at
08:15. **Today proved it** (same line last night, cleared this morning, 9 trades ran).
⛔ Flagged in the close card §A2(1) so it is not acted on tomorrow.
[[killswitch-autoclear-prior-day]] [[feedback-verify-rc-not-output]]
[[feedback-absence-needs-wide-check]] [[feedback-verify-the-finding-premise]]
