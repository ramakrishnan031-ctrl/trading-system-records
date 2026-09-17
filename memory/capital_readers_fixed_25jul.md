---
name: capital-readers-fixed-25jul
description: "25-Jul: opening_capital SUM->first-INIT (f8a2639) + the 3 capital_snapshot readers sourced live (a70793b). Both display-only. ⭐ THE LESSON: 3 test fixtures in one session asserted numbers their own data did not support, each making a wrong reader look right."
metadata: 
  node_type: memory
  type: project
  originSessionId: 94025df9-7b5d-4673-aa44-14ccbe9d87b3
  modified: 2026-07-26T06:43:42.713Z
---

**TWO capital-reader fixes, DEPLOYED 25-Jul (off-market, service down, NO restart — load Mon 08:15). Both DISPLAY/OBSERVABILITY ONLY, import-graph proven.**

## §A `f8a2639` — `db_reader.opening_capital` SUM → first INIT
`SUM(balance_after) WHERE entry_type='INIT'` doubled on restart days. **INIT is one row per PROCESS START** — H-4's double-init guard is the in-memory `self._initialized` flag (`fund_manager.py:408-448`), which a restart resets. MEASURED: **10 of 30 INIT dates carry >1 row**; 2026-07-21 (forced 11:57 restart) read **19,716.03 vs a true 9,857.30** ⇒ every % against it read HALF.
Now `ORDER BY ts ASC LIMIT 1` — same rule as **`state_store.get_day_opening_capital()`** (⚠️ that is the real name; my 24-Jul note called it `get_opening_capital`, which does not exist).
⭐ **Ordering VERIFIED not assumed:** `fm_ledger.date` is `substr(ts,1,10)` (a string prefix — **no `DATE()`, so no UTC shift**); all 58 prod INIT ts share `+05:30` and length 32; string sort == datetime sort on **every** date (0 diffs). So a mid-day re-seed cannot sort before the 08:15 seed.
⚠️ **One measured behaviour change:** 2026-07-06's 08:15 seed was **0.00** (re-seeded 10,000 at 11:20). The SUM returned 10,000 by coincidence; first-INIT is 0.00, fails the pre-existing `>0` guard ⇒ renders `—`. One historical date, display-only, more honest.

## §B `a70793b` — the 3 `capital_snapshot` readers sourced live
**The table has 0 ROWS in production** and nothing writes it. All three readers were reading nothing and failing *differently and silently*: preflight emitted a **PERMANENT WARN** ("no capital_snapshot row yet") every run forever · `/metrics` never emitted `capital_deployed_pct` at all and shipped the dict's **`0.0` default** as if measured · the GUI rendered an **all-zero** capital block as real numbers.
Sourcing: total ← first INIT · `margin_used` ← `Σ trades.margin_reserved` OPEN/PARTIAL/EXITING · `margin_reserved` ← PENDING_FILL · `realized_pnl_today` ← `Σ pnl_delta` RELEASE_USED (already NET) · `cash_floor` = total − margin_used.
⚠️ **`fm_ledger` does NOT hold those values** (deltas, not levels; `margin_used` comes from `trades`) — the "blind fm_ledger redirect" premise was refuted before building.
🔑 **`FundManagerBalanceCheck` KEEPS ITS MEANING** (free cash sane; CRITICAL; same FAIL conditions) — only the source moved. The deployment % is a **NEW, SEPARATE, WARN-only `CapitalDeploymentCheck`** ⇒ it can never escalate a preflight run to CRITICAL. (B4's "keeps its current reference" contradicted B7+B9 given 0 rows; **Rama ruled: redirect the source**.)
⭐ **`capital_deployed_pct` REDEFINED** (dated at the site): `margin_used / total_capital`, was `/ cash_floor` (a ratio against REMAINING cash — unbounded as the book fills). Safe ONLY because it never emitted ⇒ no series, no consumer.
🐛 **Caught mid-build: SQLite has NO NaN** — a NaN `balance_after` returns NULL, so "no INIT row" and "row with a broken balance" collapse. The first draft WARNed on both, which would have **silently retired the crash-test NaN guard**. Now `has_init` is carried separately: absent → WARN, present-but-unusable → FAIL.
Table **KEPT** (no schema change authorised) with a dated note at its definition.

## ⭐⭐ THE LESSON — a fixture that asserts what its own data cannot support makes a wrong reader look RIGHT
**THREE in one session**, each the reason a defect survived review:
1. GUI `conftest` seeded **two INIT rows split by bucket** (70k intraday + 30k positional) so `SUM==100000` looked correct. Production has **never** written that — all 58 INIT rows are `bucket='both'` with the FULL balance.
2. The same fixture's `capital_snapshot` claimed `margin_used=42000` while its **own trades** carry 4 OPEN × 5,000 = **20,000**.
3. `test_fix133_metrics`' store double branched on `capital_snapshot` and was **the ONLY reason `capital_deployed_pct` ever had a value anywhere** — asserted at 25% in tests while production emitted nothing for months.
**RULE: when a reader looks right only under its fixture, check the fixture against PRODUCTION SHAPE before trusting either.** Correct the fixture FIRST and re-run on the OLD code — if the suite stays green, the fixture change is behaviour-neutral and any later RED belongs to the code.

## ⭐⭐ SIBLING SUB-SHAPE (26-Jul-2026) — the fixture asserted something TRUE and still hid the defect

The three above assert something production never produces. **This one is worse to spot: the fixture is
CORRECT, and it hides the bug by BYPASSING THE FEED.**

`zerodha_adapter.py:2165` hardcoded every PAPER position to `product="MIS"`. Two safety mechanisms read
a position's product — `eod_squareoff.py:1072` (the EOD6/FIX-015 CNC exemption) and `kill_switch.py:1588`
(H-5's HARD_KILL sweep intent; a CNC swept as MIS opens a **naked short**). Both were already covered:

- `test_fix015…` builds `Position(product="CNC")` off a `MagicMock`
- `test_h5…` uses `SimpleNamespace(product="CNC")`

Both assertions are **true and useful** — they prove the CONSUMER is right *given* CNC input. Neither
can prove the paper FEED ever produces it. **It never did.** ⇒ the mechanisms were right, the feed was
wrong, and **no test spanned the two**, so both looked proven while paper could not exercise either.

**RULE: when a test hand-builds the object under test's INPUT, it has proven the consumer, not the
system.** Ask separately: *what real producer creates this input, and has anything asserted that it
does?* A green consumer test plus a silent producer is indistinguishable from a working feature.
⚠️ Cost here: *"paper-proven"* was the stated gate for delivery going live, and paper could not prove
the one thing it had to. Fixed 26-Jul `f7eedd3`. [[handoff-26jul-alert-stream]]

**Method:** RED-first by **planting** (5 plants §A-adjacent, 6 for §B; all RED; source restored md5-identical). P6 restored the old `capital_snapshot` reader and the old WARN string came straight back = B7 anti-vacuity, non-vacuous.
**Regression:** BASE 13/5112 → 12/5122, **MERGE-only EMPTY**; +9 tests reconciled exactly; the one vanished BASE failure is `test_instance_lock`, **proven flaky** (3 runs of the unchanged tree: 2/2/1). ops_dashboard 380.

🔴 **RAMA OWES: `gui-dashboard.service` was ACTIVE during the deploy** (pid 1749999, `127.0.0.1:8500`) ⇒ it still holds the OLD `db_reader` in memory. **Restart it to make §A/§B visible in the GUI.** No live impact meanwhile (no INIT row on a Saturday ⇒ `—`).
🆕 **QUEUED, NOT FIXED:** `reports/daily_report.py:187` takes `init_rows[0]` from `get_fm_ledger_for_date()`, which has **no ORDER BY** — correct today only by query-plan accident, wrong on a restart day. **That is the 16:05 report; it needs its own gate.**

Reports `docs/audit/opening_capital_double_count_25jul2026.md` + `docs/audit/capital_snapshot_redirect_25jul2026.md`. [[capital-snapshot-verify-25jul]]
