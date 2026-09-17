---
name: phase_c_cutover_01jul
description: "Phase C report cutover DEPLOYED (01-Jul ~21:37 IST, main 01e07b7) — daily_trade_review live @16:07, daily_review DELETED (git rm), daily_report bake-in; v41 migration applied; manual-run gate PASSED. Runbook docs/phase_c_cutover_runbook.md"
metadata:
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**★ DEPLOYED 01-Jul-2026 ~21:37 IST (off-market) to `main 01e07b7` (ff `f6de000..01e07b7`).** The whole report redesign + Phase C cutover landed in one push (post-receive AUTO-INSTALLED the crontab). Follows [[phase_b_parallel_run_01jul]] (Phase B ×2 + Phase-B.1 = double-confirmed GO). **DELTA from the prepared plan (Rama's directive): daily_review was DELETED, not disabled.**

**Deploy evidence (Rama's steps executed end-to-end):**
1. DB backup: `data_store/backups/pre_report_cutover_20260701_211906.db` (200MB) + `_analytics.db` (5MB); pre-deploy schema = v40.
2. Push: `git push origin fix-check9-false-positive-01jul:main` → clean ff `f6de000..01e07b7`, `post-receive: crontab AUTO-INSTALLED from canonical`. Commit 01e07b7 (25 files, +4618/−2025).
3. Migration ran on the manual gate-run: `migration complete: v40 -> v41`; `schema_meta`=41; `config_snapshots` table EXISTS but **0 rows** (correct tonight — the first row is written by main.py at tomorrow's 08:15 boot, NOT the report; DELTA 3).
4. **Manual-run GATE PASSED** (DELTA 4): `reports/daily_trade_review.py --date 2026-06-30` → wrote `reports/output/daily_trade_review_report_2026-06-30.xlsx` (1.0 MB, **7 sheets** Dashboard·Reconciliation·Orders·Signals·Strategies·Slippage·Config), net=3.24 / 18 trades / reconciliation=PASS-1-pending / config=pending-W0 — ties EXACTLY to Phase B; NO exceptions; `cron_heartbeat("daily_trade_review")=SUCCESS`.
5-7. Deployed HEAD (bare+tree)=01e07b7; `reports/daily_review.py` GONE from the tree; crontab has `daily_trade_review @16:07` + `daily_report` (bake-in), **daily_review GONE**, `crontab == canonical` (no drift), 0 `daily_review:` keys in the deployed registry (Officer won't expect it → no false MISSED); old `reports/daily/` outputs (496K, daily_review.{xlsx,md} only) DELETED.
8. W13 guardrail intact post-run: `shadow_tracker.enabled: true`, `innings`=110 rows.
9. GO for tomorrow's 16:07 automated run. Tonight's monitors (EOD Officer 18:50, CT 17:05, drift 18:00) all ran PRE-deploy → next runs tomorrow, all consistent.

**What DELETE-not-disable changed vs the prepared plan:** `git rm reports/daily_review.py` + `tests/unit/test_daily_review.py` (36 tests); removed the daily_review ENTRY from `cron_registry.yaml` entirely (left a tombstone comment); removed `"reports/daily_review.py"` from `generate_crontab.py::_SPECIAL_NAME`; **REVERTED the `expected_heartbeat_jobs` enabled-skip** (unnecessary once the entry is deleted — the registry no longer has ANY disabled job; verified daily_review was the only `enabled:false`); cleaned daily_review out of `test_time_authority_sweep.py` (import + 1 test) and 2 stale code comments (`state_store.py` innings-caller, `order_manager.py` exit_reason). `test_phase18_batch1.py` + `test_cron_alerts.py` reference the NAME only (inline logic / sample string — no import, left as-is). Rollback for daily_review = `git revert` (restores file + entry from history). Full unit suite **4110 passed / 13 skipped**; the 1 "failure" (`test_interactive_startup::test_holiday_guard_missing_yaml_proceeds`) is a wall-clock market-window test (21:33 IST outside 08:00-16:00) — PASSES with `TS_IGNORE_MARKET_WINDOW=1`, git-clean, NOT a regression.

---

_(original PREPARED note follows — superseded by the DEPLOYED status above)_

**01-Jul-2026 — Phase C cutover (prepared, then deployed same evening). VS Code Claude PREPARED all file changes; deployed on Rama's execute-now directive OFF-MARKET.**

**Deploy = the WHOLE report-redesign lands in one push** (W0 config_snapshots v41 migration + config_snapshotter + all 7 sheets + Phase-B.1 fixes + this cutover). Live prod is pre-W0 (verified: no `config_snapshots` table) → the branch carries the **v40→v41** migration → **DB BACKUP FIRST**, OFF-MARKET only.

**Phase 1 investigation (stop-gate) findings:**
- **Cron is REPO-MANAGED, deploys ON PUSH.** `config/cron_registry.yaml` (single source of truth) → `scripts/generate_crontab.py --generate` → canonical `deploy/cron/trading-system.cron` → the **post-receive hook auto-installs** (regenerates from the deployed registry, `diff -q` byte-equality vs the committed canonical, then `crontab <canonical>`). Confirmed live when CHECK9 pushed earlier ("crontab AUTO-INSTALLED from canonical"). Rama does NOT hand-edit the VM crontab.
- **Old cron entries:** `daily_review.py` @ 16:00 Mon-Fri, `daily_report.py` @ 16:05 Mon-Fri (both default `--date` to today).
- **Slot chosen = 16:07** (after excursion-reconstruction 15:50, eod_verify 15:55, wal_checkpoint 16:00, daily_report 16:05; before trade_journal 16:10).
- **Consumers (the stop-gate item):** `daily_review`'s output (`reports/daily/`) has NO downstream consumer → safe to retire. `daily_report`'s xlsx IS consumed by `scripts/system_manager.py:392` — a **soft WARN-only** EOD deliverable-existence check (not a hard fail). Handled by the bake-in (daily_report kept). The `reports/daily_review/` dir hits were the UNRELATED screened-stocks CSV, not the report. NOT a blocker.
- **daily_report prod health:** runs CLEANLY in prod (produces 1.2 MB xlsx/day, heartbeats SUCCESS 30-Jun/01-Jul) — a REAL safety-net → path C (keep in parallel). Its non-DB config reads only mis-fire on HISTORICAL replays (Phase B), not on the live current date.
- **W13 guardrail confirmed:** `innings` table present (110 rows), `shadow_tracker.enabled: true`, `max_innings: 3`. Phase C must NOT touch these (gates live re-entries + read by daily_report).

**Prepared changes (working tree, NOT committed/pushed):**
1. `config/cron_registry.yaml` — `daily_review` → `enabled:false` (RETIRED, entry KEPT for a 1-flag rollback); NEW `daily_trade_review` job @ `7 16 * * 1-5`, monitored, `env_wrapper: python` (PYTHONPATH), log `logs/cron-daily-trade-review.log`.
2. `deploy/cron/trading-system.cron` — regenerated by the tool (44 command-lines; daily_review line GONE, daily_trade_review IN, daily_report kept). Byte-identical to `generate(registry)`, pure ASCII+LF (post-receive `diff -q` gate holds). `--selftest` 44/44 round-trip.
3. `reports/daily_trade_review.py` `main()` — `--date` now DEFAULTS to today IST (`now_ist().strftime`, like the retired generators → cron needs no date-substitution) + records `cron_heartbeat("daily_trade_review")` SUCCESS (and FAILED-on-exception, re-raise) to the reported DB. (+`import time`.)
4. **`core/cron_registry.py::expected_heartbeat_jobs` now filters `enabled`** — a disabled (retired) job is never "expected", so the Cron Officer raises NO false MISSED for daily_review. THIS is what makes an `enabled:false` retirement clean (found via the stop-gate: `CronRegistry.load` loads ALL jobs regardless of enabled; the roster already filtered enabled but the heartbeat-expectation path did not).
5. `scripts/system_manager.py` — ADDED an EOD deliverable check for `daily_trade_review_report_<day>.xlsx` (daily_report.xlsx check KEPT for the bake-in).
6. Tests: `test_daily_trade_review.py` **57** (+entrypoint default-date+heartbeat), `test_cron_registry.py::test_phase_c_cutover_expectations` (daily_trade_review expected / daily_review NOT / daily_report kept). 147 cron-machinery + 10 system_manager green.

**Cron Officer / drift need NO separate edit** — they derive expectations FROM the registry (`jobs` dict); `content_drift`/`_auto_discover` are live-vs-generate(registry) (set-based, no stored expected-list or hash). The daily_report `_PENDING_REDESIGN_JOBS={"daily_report"}` special-case in `cron_officer.py` is now stale-but-BENIGN (daily_report heartbeats SUCCESS again) — LEFT during bake-in, remove at retirement.

**Multi-Inning (the open regression Q) = DEFER / W13** (settled in Phase B investigation): old `daily_review.py`'s 36-col MULTI_INNING_TRACKING view is not in the new report, but the `innings` data is written LIVE by `shadow_tracker.py` independent of any report → retiring loses NO data, backfillable via `state_store.get_inning_summary_by_date`; the 16-Jun NULL-net signal is caught louder by the Reconciliation CAPITAL drift check.

**Deploy + first-run checklist + rollback = `docs/phase_c_cutover_runbook.md`** (the operational doc). Rollback is low-stakes because the bake-in keeps daily_report producing a report even if the new one fails run 1. Rollback = git revert the cutover (hook reinstalls old cron) OR registry-flip (daily_review enabled:true / daily_trade_review false, regenerate, push). The v41 migration needs NO rollback (pure add; DB backup is the ultimate fallback).

**FOLLOW-UPS after a clean ~3–5-day bake-in:** retire `daily_report` (registry `enabled:false` + regenerate + push), THEN remove `daily_report` from `_PENDING_REDESIGN_JOBS` (cron_officer.py) + remove its `daily_report.xlsx` `_check` in system_manager.py (keep the daily_trade_review one); build the W13 Multi-Inning sheet when convenient.

Docs updated: `docs/SYSTEM_MAP.md` (changelog head), `PATHS.md` (report row + NEW Phase C row + test count 57), `docs/report_data_contract.md` (Phase C bullet → PREPARED), NEW `docs/phase_c_cutover_runbook.md`.