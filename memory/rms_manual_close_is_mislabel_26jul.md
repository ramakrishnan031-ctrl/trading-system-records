---
name: rms-manual-close-is-mislabel-26jul
description: "The RMS/MANUAL CLOSE CRITICAL means \"our own SL/TGT/EOD leg filled\", not an external close — 4/4 alerts false, 35/41 CLOSED_MANUAL trades mislabelled. Money always correct."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4ce1013a-db92-4899-ac6c-796dd439a76e
  modified: 2026-07-28T03:46:14.190Z
---

> ## ✅✅✅ VERIFIED LIVE 28-Jul-2026 — v45 MIGRATED AND THE BACKFILL IS RUN
> **v45 VERIFIED LIVE 28-Jul 08:15:16** (`migration complete: v44 -> v45`, schema 45, trades 430
> unchanged, `integrity_check ok`, service `active` NRestarts=0). **Backfill RUN 09:09:15** —
> `scripts/backfill_closure_source_w8.py` (`90c119d`), run record `docs/audit/w8_backfill_run_28jul2026.md`
> (`52ead46`). **35 written: OWN_EOD 22 · OWN_SL 9 · OWN_TGT 4. SIX left NULL** — SULA · GICRE ·
> AGARIND · EVEREADY · AEROENTER · RCF. ⛔ **SIX, not five — both operator cards said five while
> naming six (they omitted GICRE); verifying against five would have read a correct run as a
> failure.** Undo: `--revert-file data_store/w8_backfill_receipt_20260728_090915.json`.
> ⭐ **24-Jul figures re-run against corrected labels: 8/8 predictions met to two decimals**
> (D.4 arm rate 40.9 %→**43.2 %** n 66→74 · D.3 OOS +2.31→**+2.20 R** n 16→18 · whole-book
> +2.93→**+2.78 R** · **ALL row invariant 139/92/66.2 %**). All four BEFORE figures reproduced the
> 27-Jul report exactly first, which is what makes the AFTER match evidence. **No conclusion moves;
> the exits thread stays CLOSED.** ⚠️ `exit_reason` still says `MANUAL` — that was deliberate
> (option (a), not (b)); **`closure_source` is now the corrected axis, `exit_reason` is not.**
>
> ## ✅✅ FIXED, PUSHED AND DEPLOYED 27-Jul-2026 in v45 — went live at the Tue 28-Jul 08:15 boot
> `bc19aab` §A vocabulary · `77b8b04` §B W8 writer · `10c02ae` classifier · **`2f8fd87` §C CLASSIFY**
> · `81f9372` §D deferral (INERT, `check1_mid_fill_defer_sec=0.0`). All on `main` = `d3fa5b8`.
> **Verified on the VM:** `orders/closure_classifier.py` + `core/closure_source.py` present in the
> deployed tree, `order_reconciler` imports the classifier, bare-repo HEAD `d3fa5b8`, deployed
> `EXPECTED_SCHEMA_VERSION=45`.
> ⚠️ **The live DB is still schema 44** — v45 *rebuilds* `trades` to add the two columns at the
> **28-Jul 08:15 boot**. Until then `trades.closure_source` does not exist. ⛔ **No backfill before
> Tuesday morning**, and anything written before the rebuild would be destroyed by it.
> ⛔ **The 27-Jul `DECISION_check1_external_close_label` package is ANSWERED AND STALE** — it was
> written at 20:0x asking whether to build CLASSIFY, two hours *after* CLASSIFY was pushed at 18:17.
> Archived at `docs/audit/check1_external_close_decision_27jul2026.md` with that box on top.

**⛔ NEVER read `[LIVE] RMS/MANUAL CLOSE — <symbol>` as an external close.** Measured 26-Jul-2026:
**all four ever sent were the system's OWN exit order filling**, and **35 of 41 `CLOSED_MANUAL`
trades have one of their own `SL`/`TGT`/`EOD` legs `COMPLETE`** — ⭐ **EOD 22 · SL 9 · TGT 4,
re-measured against production 27-Jul (this line previously said SL 8 · EOD 23 — wrong).**

| when | symbol | what actually closed it | P&L |
|---|---|---|---|
| 20-Jul 13:52 | HUHTAMAKI | **SL** COMPLETE | −6.04 |
| 23-Jul 13:10 | WAAREERTL | **TGT** COMPLETE (limit 940.0369, filled 940.00) | +16.18 |
| 24-Jul 11:16 | GODIGIT | **SL** COMPLETE | −3.40 |
| 24-Jul 15:17 | BLSE | **EOD square-off** leg COMPLETE | −1.00 |

⭐ **The reconciler logs the disproof itself, ~1.3 s before firing** (3 of 4 carry it verbatim):
`check1: orphan TGT order … is being processed at broker (may fill) … "Order cannot be cancelled
as it is being processed."` — the broker refused the cancel *because the order was mid-fill*, and
CHECK1 then reported "Position closed externally" at CRITICAL. **CHECK1 compares STATE (local
OPEN + broker flat) and reports CAUSE.**

**✅ The MONEY is always right** — WAAREERTL checked end to end: gross 17.20 ✓, net 16.18 ✓,
`RELEASE_USED −191.44` vs `margin_reserved 191.43124` ✓, balance +207.62 exactly ✓,
`trades.net_pnl == fm_ledger.pnl_delta` ✓, `exits_verified=1`, no orphan leg — and it is right
**BY DESIGN**: `mark_trade_manually_closed` returns False if already terminal and `close_trade`
raises on a double-close, so **exactly one** path releases capital.

## ⭐⭐ THE EXITS-STUDY QUESTION IS ANSWERED 27-Jul — NO CONCLUSION MOVES

Report: `docs/audit/check1_manual_mislabel_impact_27jul2026.md` (READ-ONLY, off a `.backup`
snapshot of production).

- **13-Jul exit-policy backtest: structurally immune.** It walks 115 trades on 1-min paths and
  **re-simulates** each exit — `exit_reason` is **not an input to it at all**. ⭐ Say it that way,
  not "the effect was smaller than 8 %": *not read* stays true as the book grows; *too small* has to
  be re-argued every time.
- **24-Jul trailing-stop study: it DOES group by `exit_reason`, and its `MANUAL` bucket was 100 %
  wrong** — all 26 covered rows had an own COMPLETE leg (EOD 14 · SL 8 · TGT 4), **zero** genuine
  external closes. ⚠️ **Exposure is 26/139 = 18.7 % of the STUDIED population, not the 8.1 % of the
  whole book** — the book figure understates it by more than half.
- **Every conclusion survives, three strengthened:** D.1 arm rates all ≥ 50 % after reassignment and
  the ALL row is invariant (relabelling moves no trade in or out) · D.4's SL_HIT arm rate 40.9 % →
  **43.2 %** (n 66→74), so the +46.7R counterfactual grows · D.3's uncapped winner median
  +2.93R → **+2.78R** and **OOS +2.31 → +2.20R** (the 4 added TGT winners are all modest,
  +1.85..+2.51R) — still inside the *"~2.2–2.4R"* band the report itself published.
- 🔴 **BACKFILL — RAMA'S CALL, RECOMMENDED as (a) NOT (b).** (a) **populate `closure_source`** for
  the 35 from the `orders` evidence: new empty column, reversible, W8's whole purpose. (b) **rewrite
  `exit_reason`**: ⛔ **don't** — `status` would still say `CLOSED_MANUAL` while `exit_reason` said
  `TGT_HIT` (a NEW inconsistency), and it destroys the record of what the system believed, which is
  the subject of the investigation. ⭐ Leave the other 6 **NULL, never `EXTERNAL_UNATTRIBUTED`** —
  silence must not manufacture a verdict either. Own commit, after the 28-Jul migration.

## ✅ §C BUILT 26-Jul on `hold-check1-w8-26jul` @ `2f8fd87` — ⭐ NOW MERGED AND SHIPPED (see box)

CHECK1 now **gathers → classifies → acts**. An own-leg close sends **one INFO** naming the leg and
the evidence rung; a genuine external close sends **one CRITICAL**. The CRITICAL *log* follows the
verdict too (a CRITICAL log for a routine exit is the same false claim in another channel, and the
daily report counts CRITICALs). `closure_source` is persisted (W8, COALESCE-guarded).

⭐ **1.4 is what made §C shippable alone:** because CHECK1 wins the race, `order_placer:2374`
swallows the real INFO — so the false CRITICAL *replaced* the good alert. CHECK1 emitting the INFO
itself restores it at bound 0 with capital timing unchanged.
⚠️ **§D (the deferral) is NOT built** — that is the capital-*timing* fix, not a correctness one.
⚠️ **PAPER IS WEAKER THAN LIVE:** `get_trades()` returns `[]` in paper ⇒ rungs 1–2 unreachable and
**the broker-vs-local contradiction rule can never fire there.** Same shape as the `product="MIS"`
hardcode. Bounded for Slice 2.5 only because FIX-183's prepass excludes a carried CNC upstream.

## ⭐⭐ INVESTIGATED 26-Jul — IT IS *NOT* COSMETIC (`docs/audit/check1_external_close_26jul2026.md`)

**CHECK1 RACES OUR OWN EXIT PATH AND WINS.** Measured from the 23-Jul JSONL:
`45.747` SL orphan cancelled · `45.796` **TGT refuses: "being processed"** · `45.835` **CHECK1
resolves the TRUE fill price 940.00 from broker trades** · `46.7` our exit path arrives and finds
the trade already terminal (`exit_fill_already_closed` · `close_trade.cas_no_op`) · `47.144` the
false CRITICAL.

⇒ `order_placer._handle_exit_fill` **returns early at `:2374`**, so **the INFO "🎯 TARGET HIT" alert
is never sent — a false CRITICAL is substituted for it.** ⭐ **The severity is INVERTED, and the
good signal is DELETED, not merely diluted.** (OCO-sibling cancel and capital release are covered
by CHECK1 itself; only the alert + `cost_breakdown` detail are lost.)

**Classification — not a missing check:** `_cancel_reason_being_processed` (`:1449`) EXISTS, fires,
and is correctly commented. Its result is **discarded** because the helper returns an `int` count
and the mid-fill branch doesn't increment it. Plus an **ordering** defect: the label is written at
`:1054`, **30 lines BEFORE** the evidence is gathered at `:1084`. Both must be fixed; reordering
alone is not enough — a filled TGT and an external close are *identical* at the position level, so
the position-poll will routinely beat the fill callback.

⚠️ **"0% true-positive" is about the 4 EMAILS, not the 41-row population.** The **6** rows with no
own COMPLETE leg are the candidate true positives (2 carry real broker exit prices). **A fix must
suppress the CRITICAL only on POSITIVE evidence that one of our legs accounts for the close —
never on absence of evidence.** Broker unreachable / orders unreadable ⇒ still CRITICAL.

⭐ **Slice 2.5 already built a workaround for this** — FIX-183's adoption prepass exists solely so a
carried CNC holding (which lives in `holdings()`, not `positions()`) isn't mis-marked by CHECK1
(`cnc_gtt_monitor.py:136-140`). Fix CHECK1 and that becomes belt-and-braces. [[handoff-26jul-alert-stream]]

**Why:** `reports/daily_trade_review.py:35` already documents `CLOSED_MANUAL`/`MANUAL` as *"a
4-way collision (daily-EOD, operator-manual, RMS, kill-flatten)"* and names **W8** (a per-trade
`closure_source` at close time) as the permanent fix. **The report layer knows the label is
ambiguous; the ALERT layer states it as fact, at CRITICAL.**

**How to apply:** (1) never treat one of these alerts as an external/RMS event without checking
whether an own leg went `COMPLETE` in the same second; (2) **never count `exit_reason='MANUAL'`
as an exit policy or as evidence about exits** — 8 SL_HIT + 4 TGT_HIT + 23 EOD square-offs are
hiding in it, outside the 84 SL_HIT / 57 TGT_HIT census; (3) the fix is **Rama's call** and is
order/capital path — CAREFUL-LOOP, never swept. ⚠️ `charges=0.0` on 35/41 is **NOT** an open
item: E4 (20-Jul `a266432`) closed it; the last zero-cost one is 20-Jul 13:52.

Report: `docs/audit/alert_stream_fixes_26jul2026.md`. [[realert-presence-ledger-26jul]]
[[feedback-verify-the-finding-premise]] [[book-not-long-only-eod-reverse-aware]]
