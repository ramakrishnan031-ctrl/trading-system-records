---
name: q4-capital-safety-hardenings-14jul
description: "Q4 — three capital-safety hardenings (gate-8 sector TOCTOU, kill_switch boot fail-fast, structure_exit∩trailing_sl guard) BUILT on branch q4-hardenings-13jul, UNPUSHED, awaiting Rama review + deliberate off-market deploy."
metadata: 
  node_type: memory
  type: project
  originSessionId: c886f77e-4d0e-4e3b-9fa7-0304326d7022
---

**Q4 (Rama's 18:23 continuous-queue) — 3 capital-safety hardenings BUILT + LOCALLY COMMITTED, UNPUSHED.** Branch **`q4-hardenings-13jul`** off `main` (`bb9b1e7`, the deployed VM HEAD). 5 commits `330fa38`→`c1eea66`. Built incrementally + committed after each provable unit (Rama warned of a power outage). **NOT deployed — always-on capital-path hardenings need Rama's explicit go + a deliberate off-market window (NOT pre-market on a trading day).** Full suite: **zero new test failures** (every failure — test_fix156 in state_store, 4 in test_main — proven IDENTICAL against clean `main` = known PC-env pre-existing).

## Q4(a) — gate-8 SECTOR_EXPOSURE TOCTOU (FIX-185-class). Commits 330fa38 + 9050ba9 + 7c76408.
The SECTOR_EXPOSURE gate summed only `StateStore.sector_exposure` (TRADE ROWS PENDING_FILL/OPEN/PARTIAL). A **reserved-not-placed** reservation (`fund_manager.reserve()` done, PENDING_FILL row written LATER outside `portfolio_lock`) is invisible → two concurrent same-sector signals both read stale exposure and TOGETHER breach `max_sector_exposure_pct`.
- **`core/state_store.py::sector_exposure`** gains `*, statuses=("PENDING_FILL","OPEN","PARTIAL")` (byte-identical default; parameterizes the `status IN (...)`).
- **`capital/risk_engine.py`** new `_effective_sector_margin(sector, existing)` = `max(existing_DB_truth, sector_exposure(("OPEN","PARTIAL")) + Σ live-reservation margin in sector)`. Partition counts each PENDING_FILL ONCE (OPEN/PARTIAL excludes it; the reservation includes it). `max()`-floored → **can ONLY harden, never loosen**. getattr-guard on `fm.get_live_reservations`; degrades to DB truth but **LOGS loudly** (`sector_toctou_degraded`). Computed in `approve()` (inside portfolio_lock, same seam FIX-185 reads reservations), passed into `_run_checks`; **snapshot `sector_exposure_pct` stays DB truth** (reporting byte-identical).
- Tests: `tests/unit/test_gate8_sector_toctou.py` (NEW, real StateStore+FundManager+RiskEngine, sibling of test_h7) + 4 in test_risk_engine.py; `_MockFundManager` gained `get_live_reservations()`/`add_reservation()`. **5-item merge checklist all satisfied**, incl. the TOCTOU RED/GREEN proven by `git checkout main -- <2 files>` (old approve() returns approved=True; new REJECTS). RAMCOIND 6/6, parity green.

## Q4(b) — kill_switch=None → BOOT-TIME fail-fast in LIVE. Commit 8ea1a4e.
RiskEngine accepts kill_switch=None and at RUNTIME only WARNs + SKIPS the KILL_SWITCH gate (defense-in-depth; hot path must not crash). A wiring regression would run LIVE unprotected while whispering. New **`utils/startup_checks.py::check_kill_switch_present(kill_switch, is_paper, logger)`** → LIVE+None raises `StartupCheckFailed` (main returns 3); PAPER+None WARNs (non-fatal). Wired in `main.py` immediately before RiskEngine construction, mirroring the `check_paper_capital_consistency` fail-fast precedent. **Runtime gate NOT flipped.** 4 truth-table tests + standalone registration. `check_kill_switch_present` is the answer to the Step-5 "kill_switch fail-open" review flag.

## Q4(c) — structure_exit ∩ strategy trailing_sl (two SL owners). Commit c1eea66.
`structure_exit_enabled` (system) makes StructureExitManager the SINGLE SL owner; a strategy with `trailing_sl_enabled=true` (per-strategy, `strategies/schema.py:105`, read `order_placer.py:2072`) would ALSO move that leg → two owners racing. Enforced before only by comments. New **config-auditor rule A4** (`core/config_auditor.py` group A / BLOCK, single source): structure_exit on AND ≥1 ENABLED strategy trailing → CONTRADICTORY CONFIG. **`main.py` construction guard** re-runs group A WITH the loaded strategies (config_loader ran it without them) before any structure-exit/zone infra, fail-fast return 3. Answers the Step-8 "breakeven∩structure convention-not-construction" review flag.
- **KEY GOTCHA (fixed):** first cut used `if _struct_exit_on:` + `raise_if_blocked()` → broke 16 test_main tests, because those tests use a **MagicMock app_config** so `_struct_exit_on` was a truthy MagicMock and the auditor's A2 (`trade_type` not a valid string on a MagicMock) BLOCKED → return 3. Fix: gate on **`_struct_exit_on is True`** (a MagicMock is never `is True`; production real bool works; byte-identical when off) AND act ONLY on the **A4 finding** (not raise_if_blocked, so an unrelated group-A block can't mis-fire). A4 rule also uses `... is True` internally. **Lesson: a construction guard that runs the config auditor must guard against truthy-proxy (MagicMock) configs in unit tests.**

## ⚠️ VM footgun learned (this session)
`git checkout HEAD -- <file>` on a file with UNCOMMITTED changes WIPES them (HEAD = last commit, not working tree). It silently deleted the A4 rule mid-build (had to re-apply). **For clean-vs-dirty stash-diff, COMMIT first, then `git checkout main -- <file>` (a different ref) and restore with `git checkout HEAD -- <file>`.** Also: backticks in a `git commit -m "..."` string via the Bash tool trigger command substitution — mangles the body; use a heredoc or avoid backticks.

## NEXT
Q5 (Wave-7 audit backlog) → Q6 pipeline split → Q7 scenarios → Q8 VM security → Q9 GUI. Q4 waits for Rama's review + deploy-window go. See [[unpushed-pending-deploy-ledger]].
