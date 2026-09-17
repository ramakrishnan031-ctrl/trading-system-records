---
name: throttle-selection-record-correction-19jul
description: "The 19-Jul throttle-selection + record-correction batch (READ-ONLY, docs-only). Headline: the traded book is TIME-selected not QUALITY-selected — a domain qualification on every expectancy number. Plus the census self-correction (data is NOT eroding) and the 3-claim record sweep."
metadata: 
  node_type: memory
  type: project
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-07-19T06:40:51.369Z
---

**THROTTLE SELECTION + RECORD CORRECTION (19-Jul-2026, READ-ONLY, docs-only).** Report
`docs/audit/throttle_selection_and_record_correction_19jul2026.md`. Completes the census's open §B
and sweeps §C. Every query ran on the **preserved `mode=ro` snapshot**; **live DB provably untouched**
(sha256 `6df0c09a…` + mtime `2026-07-19 11:14:29` + size 89,968,640 identical before/after — this is
the post-heartbeat-incident baseline, not the census's `e69fd1b4…`). This closes and replaces the WIP
note `wip-throttle-batch-19jul-resume`.

## ⭐ THE HEADLINE (qualifies EVERY expectancy number on the project)
**The traded book is TIME-selected, not QUALITY-selected — a domain qualification, NOT an
invalidation.** After every gate says yes: **approved 217 → ordered 78 → filled 48.** Two attrition
stages sit below approval, neither is the risk engine re-selecting on quality:
- **Throttle (217→78, −139):** `signals/entry_throttle.py`, wired `signal_processor.py:1170`
  (`_admit_and_place`), **AFTER** `risk_engine.approve()` `:1075`. A **pure in-memory temporal rate
  limiter** (20s global `min_gap` / 3-per-60s `burst` / 300s `per_symbol`; `system_config.yaml:226-229`)
  — **NOT** `max_open_positions` (risk check 4). Docstring asserts **paper==live parity**.
  **132/139 throttles = the global 20s `min_gap`** (7 per_symbol, 0 burst) ⇒ **causally BLIND to
  strategy/score/direction.** Score **60.09 ordered vs 59.878 throttled** (0.21pt, non-monotone: 59→80%,
  60→26.3% n=175, 62/64→100% n=13) · direction LONG 36.2% vs SHORT 33.3% (flat) · **the strategy spread
  21.4%–72.2% is an ARRIVAL-DENSITY CONFOUND, not an effect** · **THE driver = arrival time: ordered%
  12.8% @10:00 → 100% @10:04 → ~100% @10:15+; throttling is 100% market-open** (hour 10: 139 throttled,
  hours 11–14: 0).
- **Fill (78→48, −30): three EXPECTED mechanisms, ZERO defects** ⇒ the "report-and-stop" gate was NOT
  tripped. **17** PROCESSED→FAILED = unfilled LIMIT entries auto-cancelled **uniformly ~60s** later
  (`fill_timeout_sec`; `order_monitor.py:526/560/776`; named event `order_placer.entry_cancelled_zero_fill:1919`)
  · **6** PLACEMENT_FAILED→FAILED = broker RMS "MIS blocked for KOTIC/UNICHEMLAB/BIRLAMONEY" (0 orders)
  · **7** PLACEMENT_FAILED→REJECTED = the system's own `slippage_exceeded` guard (0 orders). 0 partial
  fills anywhere. The only §B5-relevant selection is the **17 unfilled LIMITs** (mechanical selection
  *against* fast-moving/momentum entries; **counterfactual P&L unmeasurable** — they never traded).

**⇒ B5 consequence:** the 38.8% win rate / R-multiples / cost-dominated net all describe **"approved
signals that cleared a 20s opening-minute rate limiter AND filled a resting LIMIT within ~60s"** — the
**same shape as census §B1's batch-4 domain caveat, one layer down.** Bounds the domain; does not
invalidate the sign/magnitude of the edge (quality survives both stages ~unbiased). **D1/D2/D3 are
Rama's; expectancy NOT re-run.** ⚠️ The throttle gate category lives **only** in the free-text
`rejection_reason` (structured status is just `REJECTED_ENTRY_THROTTLED`) — 4th instance of the
[[feedback-never-classify-by-free-text]] shape; recorded, not fixed.

## ⭐ §A — SNAPSHOT PRESERVED + THE CENSUS SELF-CORRECTION
`/home/ubuntu/preserved/signal_census_19jul2026/` (outside all managed paths, `chmod 444`, 0 cron refs):
`trading_system_snapshot_20260719.db` **89,968,640B sha256 `09a22ade4032747c65614b8ceed48e805b471546b89b347a04f4d1daedd140f8`**
+ `signals_20260719.csv.gz` + `webhook_audit_20260719.csv.gz`. Sound: quick_check/integrity/FK ok, v44,
every census figure reproduces (32,928 / 30,769 / 217 / 139 / 78). **6 complete days safe: 09,10,13,14,15,16-Jul.**
**⭐ THE DATA IS NOT ERODING** — `signal_retention_days:90`, earliest data **12-Jun** ⇒ the daily prune
(`eod_cleanup.py:234`) deletes **0 rows** until **~10-Sep** (90d→0/30d→0/14d→0; only ≤10d windows bite).
**The 09-Jul boundary was the one-off 16-Jul manual Phase-B prune, NOT a sliding window — the census's
"keeps sliding" was WRONG** and is corrected everywhere. Real risk = another manual short-window prune,
not the clock. (⚠️ do NOT cite the "real code path deleted 0" dry-run — vacuous, Sunday holiday-skip.)

## ⭐ §C — RECORD SWEPT (dated notes on every occurrence)
- **(a) ">Rs990 hits LONGs 4.5× harder" — DIRECTION INVERTED by rate** (LONG 10.00% vs SHORT 10.72%; the
  4.5×/9.54× are COUNT ratios = the 10.2× long-volume skew, not differential treatment; threshold ~Rs990
  + ~23% share VERIFIED). **In D1's evidence package — flagged.** Fixed: `sizing_interaction_impact_report_13jul2026.md`
  §4/§5, `q9_batch4_sizing_floors_caps_18jul2026.md`, `expectancy_autopsy_13jul2026.md`, memory
  [[q9-batch4-sizing-reachability-18jul]]. (`capital_chain_binding_constraint_analysis_13jul` unchanged —
  its Rs990/pos claims are cap *mechanism*, correct.)
- **(b) "~249/day silent KeyError @secondary_screener:167" — already CLOSED everywhere** (fixed 14-Jul
  `c22a25c`; never silent — ERROR+traceback; same `SKIPPED_QUOTE_UNAVAILABLE` killer; ~249 was a log-line
  count, deaths ~124/day). Sweep found **no open occurrence** (wave-7 triage ✅FIXED table, `q5_wave7_backlog`
  "Retires", census corrected). Refused with evidence — no surgery needed.
- **(c) 07-08 quote-cliff interpretation INVERTED** (survivorship bias from the prune; acceptance
  *accelerated* — peak 1,462/hr; 63 = 1.21%, 6th-lowest/21d). **RE10 verdict + the no-bypass point (1)
  STAND** (entry-vs-exit recomputation, verified separately; census *strengthens* reachable — ~975 approve/day).
  Fixed: `consecutive_losses_gate_wired_19jul2026.md`, `q9_coverage_matrix_final_18jul2026.md`, memory
  [[consecutive-losses-gate-wired-19jul]]. **Keep reason-correction separate from the intact conclusion.**
- **C2 population-bias qualifier** added to batch 4's report + the Q9 coverage matrix: verdicts hold **for
  the sizer population** (enriched **1.45× >Rs990**: 34.73% vs 24.02%; risk engine sees 0.14%); bounds the
  domain, arithmetic unchanged. Do not overstate.
- **C3 standing facts recorded:** retention boundary + status-selectivity (share over 32,928 is meaningless)
  + the NOT-eroding correction · 403 population ≈**338,000** signals never counted (cheaply estimable) ·
  **live has NO partial-response detection** while paper NAMES missing symbols (`main.py:546-549`) · 2 latent
  classifier issues (`REJECTED_KILL_SWITCH` stage-ambiguous; `is_sizing_rejection()` would claim the
  risk-engine's `REJECTED_SIZING_VALID`) · **the `--db`/cron-wrapper rule** below.

## 📌 THE `--db`/CRON-WRAPPER RULE (from the incident)
`python scripts/eod_cleanup.py --db <copy>` **wrote 4 truthful `cron_heartbeat` rows to the LIVE DB** (ids
2417–2420): `eod_cleanup.py:324 _cron_main()` heartbeats **before** `main()` parses `--db`. Only table
changed of 46; schema v44; NOT reverted (deleting truthful audit rows is worse). **RULE: `scripts/*.py
--db <copy>` isolates ONLY the code below the cron entry point** — for a read-only probe call the inner
function/`main()` directly, or query the file `mode=ro`. Sibling of [[migration-on-open-rule-14jul]].

Related: [[signal-mortality-census-19jul]] [[consecutive-losses-gate-wired-19jul]]
[[q9-batch4-sizing-reachability-18jul]] [[feedback-verify-the-finding-premise]]
[[feedback-never-classify-by-free-text]] [[feedback-verify-rc-not-output]]
