---
name: d3-band-inversion-robustness-19jul
description: "19-Jul READ-ONLY: the band-inversion finding (min_pass=60 buys the anti-edge top band) FAILED its first genuine out-of-sample test. Bottom filter (0-34 junk) replicated; the 60-65 inversion did NOT (60-65 best-of-band OOS, sharp contrast reversed, pooled=noise p=0.27). Forward shadow = 3 OOS days, needs more. D3 unresolved; triage COMPUTABLE NOW → NEEDS RUNNING."
metadata: 
  node_type: memory
  type: project
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-07-21T09:10:26.790Z
---

**D3 BAND-INVERSION ROBUSTNESS (19-Jul-2026, READ-ONLY, docs-only).** Report
`docs/audit/d3_band_inversion_robustness_19jul2026.md`. Live DB untouched (`6df0c09a…`). Forward-shadow
JSONL read-only; no scripts run (running the recorder would write the immutable OOS artifact).

## ⭐ THE LIVE GATE (stated once, from code)
`config/scoring_weights.yaml:22 min_pass_score: 60` — the single source (`quality_scorer.py:119` gates).
Tiers `medium=65`/`high=80` (`:28-29`) ⇒ the traded 60-65 band is LOW tier. **All 16 strategies
`min_score: 0`** ⇒ the global governs. ⚠️ `system_config.yaml:423 min_pass_score:60` is a SEPARATE
**V3-chain shadow** seed (non-gating) — do NOT cite it as the live threshold; V3 shadow uses
`v3_min_pass_score:50`/56/75 (`scoring_weights.yaml:42-44`).

## ⭐ THE FORWARD SHADOW = THE CONFIRMATION PATH FOR EVERY SCORING DECISION (inventory it, don't assume)
A JSONL (NOT a DB table): `data_store/v3/forward_shadow_fs-v1.jsonl`, **7,827 records, method fs-v1**; per
signal it stores `old_score`/`old_band`, `ms4_score`, live `decision`, true-path `sim_R`, `realized_pnl`.
Dates: **07-13 (3,467 — IN-WINDOW, the last discovery day), 07-14 (1,644), 07-15 (2,535), 07-16 (181)** ⇒
**genuine out-of-sample = 07-14/15/16 = 3 days, 4,360 signals.** Stopped 16-Jul (system down); grows only
when the system runs. **It IS recording correctly** (not the §B4 empty/broken case).

## ⭐ THE INVERSION FAILED ITS FIRST OUT-OF-SAMPLE TEST — separate the robust half from the actionable one
Discovery (06-19…07-13, ~18d, ONE regime, **stratified 150/band**): 60-65 worst (31% win, −0.27R), 50-54
best (61%); pooled 35-59 vs 60-65 z=+3.95. **OUT-OF-SAMPLE (14-16 Jul, win = sim_R>0):**
- **ROBUST half REPLICATES** — the bottom filter holds: 0-34 win **20.3%** (R −0.47), 35-39 13.3%.
- **ACTIONABLE half does NOT** — 60-65 is the **BEST** mid/high band OOS (win **46.3%**, only positive
  meanR **+0.085**); the sharp contrast **REVERSES** (50-54 vs 60-65 z=**−2.72** OOS vs +5.22 discovery);
  pooled 35-59 vs 60-65 = **noise** (permutation **p=0.27**; negative-control permuted mean ~0 ⇒ pipeline
  sound); roughly **POWERED** (~2-4 OOS days needed, 3 available) ⇒ a real non-replication, not "too small."
- **In-window day 07-13 is day-DOMINATED** (even 0-34 flips to 75% win) — day variance swamps the band.
- **Stratification caveat:** natural dist is **73% in 55-59, ~4% in 60-65**; discovery balanced the bands, so
  its result describes a balanced sample, not the live book (of 162 OOS 60-65 signals only 27 PROCESSED).
**⚠️ CAVEAT BOTH WAYS: 3 OOS days = one regime, as the discovery was one regime. Non-replication does not
refute, just as the discovery did not confirm. D3 is NOT resolvable from existing data.**

**⚠️ NEW CAVEAT (21-Jul — the scanner boundary, distinct from the one-regime caveat above):** the OOS
window (07-14/15/16) is **entirely POST-09-Jul**; the discovery window is **v1-DOMINATED** (mostly pre-09).
Rama reports the Chartink scanners were revised **~09-Jul (v1→v2)**. If so the two samples are NOT the same
population, and "adequately powered ⇒ genuine failure to reproduce" is **UNTESTED** — a scanner-definition
artifact is indistinguishable from a real non-replication. The trade DB neither confirms nor refutes the
magnitude (POST volume stable across 09-Jul; filled-book win% flat 37→40; net/trade ~2.4× worse post-09 on a
small time-selected sample). The **0-34 robust half is generator-agnostic and survives**; the **60-65
inversion is the boundary-sensitive one.** ⇒ downgrade from "settled non-replication" to **boundary-sensitive**.
Same shape hits D4/D2/regime-attribution. See external register `MASTER_PENDING_REVISED_21-Jul-2026.txt` §B.

## ⭐ WHAT D3 RESTS ON + TRIAGE CHANGE
In-window sub-period re-slice is **NOT reproducible read-only** (per-signal sims never persisted;
regenerating = running the recorder, which writes the immutable OOS artifact). ⇒ the actionable premise is
**materially WEAKER than decision file 04 presented it** (it failed its 1st OOS test). **Triage: D3
COMPUTABLE NOW → NEEDS THE SYSTEM RUNNING** (forward-shadow days). D3 gates D1 (sizing lever), #10 (throttle
ranking), #08 (FREEZE) — all inherit "unresolved." Decision file 04 updated neutrally. **📌 Lesson applied
again: read the live value (min_pass, the config path) from code — the gate is `scoring_weights.yaml`, not
`system_config.yaml`.**

Related: [[decision-packages-19jul]] [[regime-minscore-control-18jul]] [[capital-vocabulary]]
[[e4-w10-outcome-impact-19jul]] [[feedback-verify-the-finding-premise]]
