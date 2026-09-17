---
name: decision-packages-19jul
description: "19-Jul docs-only batch: assembled docs/decisions/ (one file per open decision, corrected evidence, NO recommendations), verified the MEMORY.md compaction was lossless, and added the throttle finding as a decision carrying its counter-case. The free-text-classification pattern is now a named class of four."
metadata: 
  node_type: memory
  type: project
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-07-21T08:28:49.494Z
---

**DECISION PACKAGES + COMPACTION VERIFICATION (19-Jul-2026, DOCS-ONLY).** Report
`docs/audit/decision_packages_19jul2026.md`. Live DB provably untouched (`6df0c09a…` before/after).
This is the **single entry point to Rama's open choices**: `docs/decisions/00_INDEX.md`.

## ⭐ THE DECISIONS BOARD — `docs/decisions/` (10 files + index + actions)
One file per open decision, each = **CHOICE (as options) · WHAT IS KNOWN (corrected evidence + citations) ·
WHAT IS UNKNOWN (knowable-from-data / only-by-running / not-knowable) · EXPOSURE EACH WAY (₹ where the
record supports) · WHAT WOULD SETTLE IT (+cost)**. **NO recommendation, no ordering by preference.**
01 E4/W10 · 02 D1 concentration · 03 D2 strategy-mix · 04 D3 min_pass · 05 D4 exits · 06 PerformanceAllocator ·
07 Regime · 08 Freeze min_pass · 09 Prune-retention (new) · 10 Entry-throttle admission (new). Actions (not
decisions): Q10 Part B (token) + security → `ACTIONS_not_decisions.md`.
**Corrected values carried into the files, superseded noted:** D1 = Rs990 direction LONG 10.00% vs SHORT 10.72%
by rate (was "LONGs 4.5× harder"); D2 = 91% LONG (was "58% short").
**Key couplings (stated, not ranked):** D1↔D3 (cap is a lever on a book of unknown sign) · D3↔#08 (change resets
the regime clock; freeze forbids the change) · D3↔#10 (ranked admission only helps if the score ranks) · D2/#07↔Q10
(token-blocked) · #06↔D1 (multiplier ~~masked by~~ **[⚠️ CORRECTED 19/21-Jul: perf_weight is a POST-cap multiplier, NOT masked — it moves final qty on 233/298; see `masking_premise_sweep_19jul2026.md`]** the 100%-binding concentration cap).

## ⭐ §A — THE MEMORY COMPACTION WAS LOSSLESS (verified item-by-item)
The 8-pass compaction of MEMORY.md (19.9→17.1KB) dropped **NOTHING category-(iii)** (existed only there).
Every removal was (i) duplicative of a still-linked topic file or (ii) a completed item. The two scary
candidates both survive elsewhere: **"alert-watcher soak"** (`ct_guard_invariant_18jul.md:85` + deploy reports),
**"live-test cert"** (`batch_classification_16jul2026.md:175`). Both trimmed `[[links]]` still resolve.
**Every open board item confirmed present** (E4/W10, D1-D4, PerformanceAllocator, Regime, FREEZE, Q10 Part B,
security). Nothing restored because nothing needed it. **Lesson: a compaction CAN silently drop a board item —
this one didn't, but it was checked, not asserted.**

## ⭐ THROTTLE DECISION (#10) — the finding and its counter-case NEVER travel separately
Finding: global 20s `min_gap`, FCFS after approval; 77/217 approved in the 10:00-10:02 burst, 14.3% clear;
132/139 = that one gate; 100% market-open; not best-first (score 60.09 vs 59.878, no gradient).
**COUNTER-CASE (equal weight): ranked admission only helps if the ranking has predictive power, and it doesn't** —
M-S4 rho **+0.003** (OUTCOME C, no ranking power); band inversion: the **60-65 band the throttle sees is the WORST**
(31% win, −0.27R, 4-5σ). If the scorer can't rank, FCFS discards no edge; ranking by the current score ranks noise
and could prefer the worst (already-moved) signals. **Stands regardless of ranking:** ~23 approved/day discarded,
87% of orders in hour 1, gate category **free-text only ⇒ invisible in reports.**

## ⭐ FREE-TEXT CLASSIFICATION IS NOW A CLASS OF FOUR (not an incident)
"A decision recorded in prose where a structured column should carry it" — the shape that produced the 3,098
misclassification:
1. **Sizing concentration-vs-capital** (ORIGIN, FIXED 18-Jul) — `daily_report.py:464` `"CAPITAL" in reason` where
   `status=REJECTED_SIZING_CONCENTRATION` existed → 3,098 mislabelled; `:549` → 190 lines. [[daily-report-classification-fix-18jul]]
2. **`REJECTED_KILL_SWITCH` stage** — identical status from pre-gate (`signal_processor.py:685`) + risk check 1
   (`risk_engine.py:405`); no column carries the stage. Census; latent.
3. **`is_sizing_rejection()`/`REJECTED_SIZING_VALID`** — status-prefix classifier would call a risk-engine check a
   sizing rejection. Census; latent.
4. **Throttle gate category** — min_gap/burst/per_symbol only in free-text `rejection_reason`. This weekend.
Related but distinct: **W9** — 134,342 webhook drops, reason never persisted at all (not free text, no column).
All reported, not repaired. [[feedback-never-classify-by-free-text]]

## QUEUE AFTER THIS (unchanged, restated)
Extract the live-seed expression from `main()` (boot-path, careful loop, AFTER Monday) · live-path quote
observability (no partial-response detection while paper names missing symbols `main.py:546-549`) · 403 signal-count
instrumentation (~338k) · 3 deferred `event_type` sites · `Rejected (Sizing/Capital)` label · `build_taxonomy_map()`
`--config-dir` · wave-7 backlog · the degenerate Rs 0.29 SL distance in the slippage-guard rejections.
**⚠️ MONDAY 20-Jul 08:15 = FIRST REAL BOOT after the S4 fix; entries open 10:00 (pre-10:00 POSTs 403'd by design);
registry officer's first live run 16:22; rehydrate is a no-op on a flat book.**

Related: [[throttle-selection-record-correction-19jul]] [[signal-mortality-census-19jul]]
[[consecutive-losses-gate-wired-19jul]] [[q9-batch4-sizing-reachability-18jul]] [[e4-w10-done-17jul]]
[[regime-thesis-validation-18jul]] [[regime-minscore-control-18jul]] [[feedback-never-classify-by-free-text]]
