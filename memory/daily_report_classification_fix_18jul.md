---
name: daily-report-classification-fix-18jul
description: "18-Jul PRODUCTION FIX (first in six batches) — daily_report classified rejections by substring-matching free-text rejection_reason. Now classifies by structured status via ONE shared module reports/signal_status.py. Breakdown 190 lines -> 9; Silent Dead 139 -> 0. ⚠️ the old count was MISLABELLED not miscounted."
metadata: 
  node_type: memory
  type: project
  originSessionId: 53e59a7c-edb5-400e-9b3e-6d5981ddd5a2
  modified: 2026-07-18T16:39:24.174Z
---

**📊🔧 DAILY-REPORT CLASSIFICATION DEFECT — ROOT-CAUSE FIXED. 18-Jul-2026.**
Report `docs/audit/daily_report_classification_fix_18jul2026.md`. **Tag `deploy-18jul-report-classification`→`b3a960d`; PC == VM == `78e83d4`.**
**⚠️ PRODUCTION CODE CHANGE — the first in six batches.** Reporting layer only; **nothing on the
trading path**. Files: NEW `reports/signal_status.py` · `reports/daily_report.py` ·
`reports/daily_trade_review.py` · NEW `tests/unit/test_signal_status_classification.py`.

## THE DEFECT + THE RULE
`daily_report.py:464` did `"CAPITAL" in rejection_reason.upper()`; the CONCENTRATION reason
embeds **`capital_qty=`** ⇒ the row read **"Rejected (Capital)"** for rejections that were
**100% CONCENTRATION**. `:549` grouped by that same free text (which embeds symbol + 3 arm
values) ⇒ **190 near-unique lines for 7,655 rejections** instead of 9.
**⇒ PERMANENT RULE: [[feedback-never-classify-by-free-text]] — classify off the structured
status; render the text as detail only.**

## ⚠️ THE PREMISE NEEDED CORRECTING (do not repeat the "3,098 → 0" framing)
**The old count was MISLABELLED, not miscounted.** All **3,098** sizing rejections corpus-wide
are `REJECTED_SIZING_CONCENTRATION`; `REJECTED_SIZING_CAPITAL` = **0**; **0** non-sizing reasons
contain "capital" ⇒ the substring picked the RIGHT ROWS for the WRONG REASON. The fix makes it
right **by construction**, fixes the label, and **names the binding constraint** for the first
time. It would have miscounted the moment a 2nd sizing constraint occurred.

## THE SWEEP FOUND 2 MORE OF THE SAME CLASS (both genuinely wrong)
* `:465` counted only `"REJECTED" in status` ⇒ **2,688** signals carrying
  `DROPPED_*`/`SKIPPED_*`/`QUEUE_FULL`/`PLACEMENT_FAILED`/`TIMEOUT` reported as **silently dead**
  (139 on the demo day → **0**). "Silent Dead" now means *no KNOWN disposition* ⇒ a real
  schema-drift alarm.
* `:459` `"DUPLICATE" not in status` conflated the dedup drop with `REJECTED_DUPLICATE_SYMBOL`
  ⇒ `After Dedup/Excluded` 7802 (99.8%) → **7814 (100.0%)**.
**CLEAN (checked, no fix):** the ops dashboard's `_bucket_case_sql()` already buckets on
structured `status` (the precedent this aligns to) · `expand_rejection_reason` maps from STATUS ·
`forward_shadow_record` records verbatim · rendering sites are fine.

## ANTI-DUPLICATION (Rule #4) — promoted, not duplicated
`daily_trade_review._signal_bucket` **already had the right pattern**, so it was **promoted into
`reports/signal_status.py`** and that file now delegates (`_signal_bucket = sig_status.bucket`),
asserted by a test. **Exactly ONE implementation.**

## §A1 — NO PROGRAMMATIC CONSUMER (this is what kept it in scope)
`daily_report` writes **only the xlsx** (`:1761`, no DB writes). Readers: `system_manager.py:403`
(**existence + >2000 bytes only**), the secret scanner, and human download via the dashboard.
`rejected_capital`/`rejection_reasons` are **local render-only variables**. "Auto Tuning Signals"
emits **advisory strings** and never touches `rejection_reason`. ⇒ **presentation-only.**

## ⚠️ A FALSE PASS I CAUGHT IN §C — and a harness artefact
The first before/after diff said **0 differing cells**. NOT clean: with `python -m` the **cwd
precedes PYTHONPATH** on `sys.path`, so the "after" run silently loaded the **OLD** module
(proved via `dr.__file__` / `hasattr(dr,'sig_status')==False`). Redone with the overlay genuinely
first. Then 26 diffs appeared in `6_Strategy_Analysis` — **also my harness**:
`build_taxonomy_map()` (`:1493`) is called with no arg so it resolves `config/` **relative to
cwd** and ignores `--config-dir`. Re-running BOTH sides from an identical cwd removed them.
**⇒ ISOLATED RESULT: 429 diffs, ALL in `0_EOD_Dashboard`; the other 6 sheets byte-identical;
41 labels (P&L, win rate, drawdown, system health) unchanged.**

## BITE PROOF — 4 plants, and the tests bit THEMSELVES twice first
A free-text classification restored (`assert 'CAPITAL' == 'CONCENTRATION'`) · score-collapse
removed · silent-dead reverted (names each status) · **the original `:464` line reintroduced as
CODE ⇒ the source guard names file+line+text**. ⚠️ Two self-catches: `has_explicit_disposition`
initially excluded `QUEUE_FULL`/`TIMEOUT`, and **the guard fired on my own explanatory comment**
(scoped to skip comment lines — documenting the old defect must stay legal).

## ROLLBACK
**`git revert <fix-commit>` — one commit, one step.** No schema/config/flag; this path writes no
state, so nothing to unwind; any past date is regenerable with `--date`.

## RECORDED, NOT FIXED (Rama's call)
`:537` "CRITICAL Count" counts routine `KILL_AUTO_CLEARED`, **double-counted** with `:540` "Kill
Switch Events"; `:536` "ERROR Count" matches **no** event type (structurally 0). Same *pattern*
but **ambiguous intent, not demonstrable misclassification** ⇒ not changed on the eve of a live
boot ([[feedback-live-vs-latent-findings]]). Also `build_taxonomy_map()` ignores `--config-dir`
(pre-existing, harmless under cron).

Related: [[feedback-never-classify-by-free-text]] · [[q9-batch4-sizing-reachability-18jul]] ·
[[feedback-verify-the-finding-premise]] · [[verify-check-the-rc-not-the-output]].
