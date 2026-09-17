---
name: signal-mortality-census-19jul
description: "The 19-Jul read-only census of where signals die — 19.00% of admitted signals reach the risk engine, silent drops = 0, and all three inherited claims were wrong in part (incl. the ~249/day KeyError, which was never silent and was fixed 14-Jul)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e968c54-eca0-4d3d-b502-cb87d73a6049
  modified: 2026-07-19T06:32:40.916Z
---

**THE SIGNAL MORTALITY CENSUS (19-Jul-2026, READ-ONLY).** Report
`docs/audit/signal_mortality_census_19jul2026.md`; commit `9eb7d71`, docs-only, PC == origin ==
VM bare. Live DB **provably untouched** (sha256 `e69fd1b4…` + mtime `09:20:01` identical before
and after; every query ran on a `mode=ro` snapshot, since removed).

## ⭐ THE HEADLINE
**REACHED THE RISK ENGINE = 5,845 of 30,769 admitted = 19.00%** (6 complete days).
**Verified twice from independent sources** — DB statuses and `risk_engine.approve` log lines
agree at **5,845 exactly**. ≈975 approve() calls/day ⇒ **Q9's gates are NOT a dead code path.**
The "3.54% of arrivals" figure is real but **misleading — do not quote it**: 81% of arrivals are
intentional dedup (≈1 POST/min/scanner vs a 300s TTL ⇒ 80% expected, 81.5% observed).

## ⭐ SILENT DROPS = 0
Every `signals` row maps to a known stage: **0 unmapped statuses, 0 NULL, 0 stuck non-terminal.**
**97.60% of deaths are deliberate DECISIONS**, 2.40% data failures (725 quote-unavailable + 13
placement).
The **134,342 webhook-layer drops** have no row and **no log line** (proven: grep of ~500MB of
logs returns 0 for `IN_PROCESS`/`QUEUE_FULL`/`STORE_ERROR`/`INVALID_SYMBOL`/`INVALID_PRICE`/
`EXCLUDED_SYMBOL`; the 294 `DUPLICATE` hits are the **risk engine's** check, not webhook dedup)
— **BUT the count IS reported daily**, tagged `[W9] PENDING_CAPTURE`
(`daily_trade_review.py:699-710` documents the mechanism; `:897/:910/:1008/:2307` render it).
⇒ **A tracked capture gap, NOT a blind spot.** Retryable failures bounded near-zero via the 503
count (18 POSTs all-window, **0** in the complete era).

## 🔴 THE MEASUREMENT BOUNDARY (affects every future signals-table analysis)
`scripts/eod_cleanup.py:234` prunes **status-selectively**:
`(status IN ('EXPIRED','DUPLICATE') OR status GLOB 'REJECTED*') AND fingerprint_date < ? AND NOT
EXISTS(trades)`.
⇒ **Only 2026-07-09 → 16-Jul is COMPLETE** (accepted == rows *exactly*). Before it just ~1.5% of
rows survive — the residue is **86.89% `SKIPPED_QUOTE_UNAVAILABLE` + qualified, ZERO
`REJECTED_*`**. **Any share computed over all 32,928 rows is meaningless.**
✅ **Corollary: `SKIPPED_*` counts ARE complete for the whole 24-day window** (the prune never
touches them) — which is what makes the claim-1 refutation airtight.

## ⭐ ALL THREE INHERITED CLAIMS WERE WRONG IN PART
1. **07-08 "63 signals after 10:22:23, the system stopped pricing"** — count **VERIFIED**,
   interpretation **INVERTED**. Acceptance *accelerated* after 10:22 (hourly accepted 464 → 676 →
   1,179 → 1,431 → **1,462**, the day's busiest hour). The 63 are **1.21% of that day's 5,212
   accepted — the 6th-LOWEST rate of 21 days** (mean 1.78%; the bad days were 07-13 3.57%, 06-30
   3.46%, 07-15 3.01%, none ever flagged). **The cliff is survivorship bias**: 07-08 is in the
   pruned era, so only skips + qualified survive. Last surviving non-skip = **10:20:20**, first
   surviving skip = **12:36:12** ⇒ a **2h16m hole with no row of any kind**, exactly where the
   deleted rejections lived.
2. **"~249/day silently-dropped `KeyError` at `secondary_screener.py:167`"** — **INVERTED, and
   already fixed.** It was **never silent**: `raise KeyError` was caught by the `except Exception`
   **two lines below it in the same function** and logged **ERROR + full traceback** — the
   noisiest thing in the log. **It is also NOT a separate killer** — both paths end in
   `_make_skipped("SKIPPED_QUOTE_UNAVAILABLE")` + `_persist`, so **adding claims 1 and 2
   double-counts the same deaths.** Fixed **14-Jul in `c22a25c`** (logging only; mortality
   unchanged). The ~249 was a **log-line** count, not a signal count — measured mortality is
   ~124/day.
3. **"~Rs 990 / 23.3% / LONGs 4.5x harder"** — threshold **VERIFIED and exact**, share
   **VERIFIED**, direction **INVERTED**. Below 990: **0.00%** concentration rejections in all
   three bands; above: **42.25%** (990-2000) / **41.01%** (>2000). Share >990 = **24.02%** (vs
   23.3% claimed). Direction: **LONG 10.00% vs SHORT 10.72%** — shorts marginally *harder*. The
   "4.5x" is rate/count confusion: LONGs take 90.5% of rejections, but that is the **10.2x volume
   skew** (28,027 vs 2,742), not differential treatment.

## ⭐ B1 — BATCH 4's REACHABILITY TABLE **IS** BIASED (price-structured)
Share >Rs990 by stage: **admitted 24.02% → sizer 34.73% (1.45x enrichment) → risk engine 0.14%**;
mean price Rs 732 → 875 → **441**. Screening *enriches* for expensive names; the concentration cap
then deletes the whole band **before the risk engine sees it**.
⇒ Batch 4's verdicts (incl. "only 4 of 15 sizing guards can bind") **hold for the population that
reaches the sizer** — the arithmetic was never in doubt — but **must NOT be read as statements
about signals in general**. A guard needing high notional/share is unreachable *because of an
upstream cap*, not its own threshold. **Bounds the domain; does not invalidate.**

## OTHER FINDINGS (reported, NOT fixed — this was a census)
- 🔵 **The one genuine blind spot: the 403 population.** 25,960 POSTs refused before parse ⇒
  `signals_accepted`/`signals_rejected` both **0**, signals inside **never counted anywhere**.
  Correctly refused (outside entry window) but **unmeasured**. **Estimable: 39.32 bytes/signal ×
  512.7 avg bytes ⇒ ~13/POST ≈ 338,000 signals** — comparable to the entire counted population.
- ⚪ **`REJECTED_KILL_SWITCH` cannot identify its stage** — emitted by both the pre-gate
  (`signal_processor.py:685`) and risk-engine check 1 (`risk_engine.py:405`). **Latent** (0 rows).
- ⚪ **`signal_status.is_sizing_rejection()` would claim `REJECTED_SIZING_VALID`**, which is a
  **risk-engine** check (check 2), not a sizer outcome. **Latent** (0 rows).
- **A7 paper-vs-live:** all 361 trades are `mode=LIVE` ⇒ no paper population to compare. But the
  quote path **does** differ structurally: paper short-circuits (`zerodha_adapter.py:1579`) to an
  injected provider which **also fetches real Kite quotes** yet applies **its own alias map + 0.35s
  rate limit**. ⭐ **Paper is BETTER instrumented than live** — it logs a WARNING *naming* missing
  symbols (`main.py:546-549`); **live has no partial-response detection at all**.
- **B2 (D2 data, no recommendation):** score gate is the largest killer (10,949 = 35.58%);
  **91.1% of admitted signals are LONG** (28,027 vs 2,742) — the skew starts at the **scanner**,
  matching BK-1's 91%-long closed book; 3,098 (10.07%) die at a **price ceiling, not a judgement**
  ⇒ a universe/config mismatch, structurally distinct from "the scoring has no edge".

## RISK-ENGINE CHECK ORDER (re-confirmed from source, `risk_engine.py` `checks_run.append`)
`KILL_SWITCH → SIZING_VALID → CAPITAL → OPEN_POSITIONS → DAILY_TRADES → CONSECUTIVE_LOSSES →
DAILY_LOSS → SECTOR_EXPOSURE → CONTRARY_POSITION → DUPLICATE_SYMBOL`.
Independently confirms Q9's §0.1 correction: **CONSECUTIVE_LOSSES is 6, DAILY_LOSS is 7** ⇒ the
latter **cannot** mask the former. Pipeline order: pre-gates → screener → **sizing → risk engine**
(sizing runs FIRST; `signal_processor.py:901` then `:1075`).

## WHAT CANNOT BE MEASURED FROM THE RECORD
Composition of the webhook drop (**W9**) · signal count inside 403 POSTs (**cheaply fixable** —
size already stored) · **all `REJECTED_*` history before 09-Jul is destroyed** (⚠️ **CORRECTED
19-Jul: this is NOT a sliding window** — retention is **90d**, earliest data **12-Jun** ⇒ the daily
prune deletes **0 rows** until **~10-Sep**; the 09-Jul boundary was the **one-off 16-Jul manual
Phase-B prune**, not the clock; the real risk is another manual short-window prune) ⇒ *any future
rejection-composition analysis must run on an unpruned window or the **preserved snapshot** now at
`/home/ubuntu/preserved/signal_census_19jul2026/`* · per-check attribution inside `approve()`
(records only the FIRST failing check) · whether paper/live quote mortality actually differs.

Related: [[q9-batch4-sizing-reachability-18jul]] [[daily-report-classification-fix-18jul]]
[[consecutive-losses-gate-wired-19jul]] [[feedback-verify-the-finding-premise]]
[[feedback-never-classify-by-free-text]] [[bk1-long-short-scanner-17jul]]
