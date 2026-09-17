---
name: decision-readiness-triage-19jul
description: "19-Jul triage of Rama's 10 open decisions into DECIDABLE-NOW (3) vs GATED (7), each gate named; one-screen briefs for the decidable 3; and the PREPARED-BUT-NOT-EXECUTED E4/W10 deploy runbook. Docs pushed 051e672. No recommendation; nothing deployed/merged/booted."
metadata:
  node_type: memory
  type: project
  originSessionId: 1294e59d-898e-4c0a-a00c-adb95bcf5dcb
  modified: 2026-07-21T08:28:51.046Z
---

**DECISION-READINESS TRIAGE + E4/W10 DEPLOY PREP (19-Jul, DOCS-ONLY; NO rec; nothing deployed/merged/started/booted).**
Report `docs/audit/decision_readiness_triage_19jul2026.md`. PC == origin == VM bare == `051e672` (docs-only; delta vs `d271525` markdown-only; AUTO-INSTALLED reinstall invariant). 3 artifacts byte-identical (DB `6df0c09a…` · analytics `bb229f44…` · JSONL 7,827@16-Jul).

## ⭐ THE TRIAGE — 3 decidable now, 7 gated (verified against the decision files, not inherited)
- **DECIDABLE NOW (only Rama's judgement missing):** **01 E4/W10** (evidence complete, N=0; posture call + manual-flatten precondition) · **08 Freeze min_pass** (priority/hygiene judgement — **already frozen by inaction**, NOT a deadline) · **09 Prune retention** (his intent: is rejection-composition a recurring need? — 0 rows pruned until ~10-Sep, 6-day snapshot holds current data).
- **GATED ON ANOTHER DECISION:** **02 D1** → D3 (+ leverage) · **06 PerfAllocator** → D1/sizing-leverage (perf_weight pinned 1.0, ~~masked by~~ **[⚠️ CORRECTED 19/21-Jul: POST-cap multiplier, not masked — moves qty 233/298]** the 100%-binding cap) · **10 Throttle** → D3 (ranked admission worthless if the score can't rank).
- **GATED ON EVIDENCE:** **03 D2** → Q10 token+months · **04 D3** → forward-shadow OOS days (first 3 point *away*) · **05 D4** → ~17-34 trading days of winners · **07 Regime** → Q10 ~2.2 months + token.
- **⭐ The 7 gated collapse to 3 ROOTS: D3/scorer** (gates 02,04,08,10) · **Q10/the Kite token** (03,07) · **power/running-days** (04,05). Answer D3 + refresh the token ⇒ most of the board unlocks in sequence.
- **Cost of waiting: only #03 (D2) has any** — a genuinely-broken strategy keeps draining (e.g. `vwap_bounce_long` −12.1R over the window), but broken-vs-regime is unmeasurable today ⇒ even that cost is unquantifiable. The other 6 gated cost nothing to leave open.

## ⭐ BRIEFS (decidable-now, one screen each; compression test passed — arguable both ways)
`docs/decisions/BRIEF_01_e4_w10_pnl_contract.md` · `BRIEF_08_freeze_min_pass.md` · `BRIEF_09_prune_retention.md`. Marked as summaries; do NOT supersede the full files. 01's evidence question is CLOSED (N=0/23, Rs 243 margin, ~Rs 300 threshold) ⇒ residual is posture + deploy precondition, not analysis.

## ⭐ E4/W10 RUNBOOK — PREPARED, **NOT EXECUTED** (`docs/decisions/RUNBOOK_e4_w10_deploy.md`)
⛔ Gated on **decision-01 "adopt" + a manual flatten + observing Monday**; timing constraint at the TOP (capital-path change ⇒ after Monday, unhurried, careful loop, never a trading morning). **The branch was NOT touched** (read-only `log`/`merge-base`/`diff` only; `e4-w10-pnl-contract` HEAD still `ad34ee4`).
- Branch `e4-w10-pnl-contract`@`ad34ee4` (2 commits off base `4c148fb`), schema v44, never pushed. **81 commits behind main** ⇒ NOT a fast-forward — **but the 5 capital-path files are conflict-free** (`fund_manager.py`/`state_store.py`/`order_reconciler.py`/`cnc_gtt_monitor.py`/new `cost_calculator.py` = 0 commits on main since base); only `main.py` (1 commit, different region) + `PATHS.md` + `SYSTEM_MAP.md` are 3-way.
- **Post-deploy signature:** `RESET_PNL` must stop equalling `−(Σpnl_delta − Σcosts)` and start equalling `−Σpnl_delta` (differ by Σcosts on a losing day); reader returns −100 not −140 for NET −100/costs 40. **Rollback:** revert (merge `-m 1`, or the 2-commit range), schema-free, minutes. 36 pre-fix `costs=0` rows NOT backfilled (fabrication); deploy after an EOD reset is clean.

## ⭐ POST-MONDAY QUEUE (ordered; most are decision-independent)
1 **live-seed extraction** (`main.py:2255-2258`, boot-path) + 2 ~~**check_scanner:703** (add 401 like :808)~~ **❌ CLOSED 20-Jul, REFUSED WITH EVIDENCE** — external Chartink, not local `/health`; real sibling = `scripts/preflight/checks/signals.py:28` [[preflight-401-third-sibling-20jul]] — **group: same boot-path careful-loop class** · 3 **candle retention** (verify `db_retention` won't drop OOS 1-min candles before D4's ~17-34d — VERIFY, gates D4) · 4 **PerfAllocator reachability algebra** (treat "COMPUTABLE NOW" as UNVERIFIED) · 5 live-path quote observability · 6 403 signal-count (~338k) · 7 deferred `event_type`/`Rejected (Sizing/Capital)` label/`build_taxonomy_map()` · 8 wave-7 backlog · 9 degenerate Rs 0.29 SL.

## ⭐ NAMED SEPARATELY — NOT on the queue
- **Leverage (5× MIS) = an open DESIGN AREA, not a task.** System sizes against UNLEVERED capital; every limit (daily-loss %, cap, tiers) was calibrated when margin==notional. **The recalibration is the work, not the multiplier.** Sits under D1 + #06. No design done (batch scope).
- **MEMORY.md compaction OWED (§D4): SNAPSHOT FIRST.** The last interrupted trim couldn't be byte-diffed because the palace is NOT git-tracked and no backup existed — a snapshot before the next compaction makes it diffable. After Monday, deliberately, not under a hook's pressure. [[monday-preboot-readiness-19jul]]

Related: [[decision-packages-19jul]] [[e4-w10-done-17jul]] [[e4-w10-outcome-impact-19jul]] [[d3-band-inversion-robustness-19jul]] [[forward-shadow-capacity-d4-feasibility-19jul]] [[throttle-selection-record-correction-19jul]] [[monday-preboot-readiness-19jul]] [[unpushed-pending-deploy-ledger]]
