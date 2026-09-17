---
name: offmarket_deploy_plan_03jul
description: "Off-market push/verify/shadow/cutover runbook for the A-2+C-1+B-1+P1 batch (02-Jul, planning only, committed on C-1 branch, unpushed)"
metadata: 
  node_type: memory
  type: project
  originSessionId: a8d15a29-6620-40b2-a610-0858dd394705
---

Deploy runbook for the four-fix batch. Planning doc only — NO build, NO push in this pass.
Doc `docs/ops/offmarket_deploy_plan_03jul2026.md`, committed on `fix-c1-completion-02jul`
@ **5f965d3** (unpushed; C-1 is the docs-carrier so it rides in first). SYSTEM_MAP.md +
PATHS.md pointers added in the same commit.

**Baseline:** `main == origin/main == 9becf8c`, **schema v41**.

**Branches:** A-2 `fix-a2-timeout-no-retry-02jul`@fd09a38 (contained inside C-1 — do NOT merge
separately) · C-1 `fix-c1-completion-02jul`@5f965d3 (fd09a38→aa02f9f→3 docs→deploy-plan) ·
B-1 `fix-b1-daily-loss-mtm-02jul`@f5fd4d9 · P1 `fix-p1-eod-broker-reconcile-02jul`@4817032 ·
PARKED `fix-t2-import-02jul`@b826ae0 (not in batch).

**Push:** GATE = 03-Jul(Fri) 08:15 boot of 9becf8c clean (SOFT_KILL auto-clear, no orphan/CHECK9
misfire) → then **after-17:05/weekend** window (never 15:30–17:05). One push: `merge --ff-only C-1`
→ `merge --no-ff B-1` → `merge --no-ff P1` → `git push origin main` (post-receive installs `@15:58`
crontab). **Back up BOTH DB files first** (v28 split). Merges verified CLEAN incl. sequential
P1-onto-B1 (B-1/P1 edit disjoint hunks in `config/system_config.yaml` + `core/config_loader.py`).

**Schema:** v41→**v42** (P1 ONLY; pure-add `eod_broker_reconciliation`; `EXPECTED_SCHEMA_VERSION=42`).
A-2/C-1/B-1 no schema.

**Shadow flags default OFF:** `risk.daily_loss_include_unrealized=false` (B-1) ·
`eod_reconcile.authoritative=false` (P1). Zero behaviour change on deploy.

**Activation (after-17:05/weekend push):** A-2 + B-1 at **Mon 06-Jul 08:15 boot** (in-process code);
P1 first shadow EOD **Mon 06-Jul 15:58**. Same-day activation needs a manual trader restart (deploy-
before-resume lesson).

**Shadow watch:** B-1 = `_mtm_refresh_success/failure`, `risk_engine.daily_loss.would_reject_with_
unrealized` log, MTM-vs-broker spot-check incl. SHORT sign. P1 = `eod_broker_reconciliation.mismatch=1`
rows (= eod_verify false-VERIFYs caught), UNVERIFIED proven on a real broker-unreachable weekend dry-run,
day-P&L ties to daily_trade_review. DEEPEN the local-only ledger dimension BEFORE authoritative.

**Cutover (earliest):** B-1 enforce flip ≈ **Mon 13-Jul** (after 06–10-Jul week). P1 authoritative +
retire eod_verify + subsume reconcile_pnl ≈ **Mon 20-Jul** (≥2 clean shadow weeks + ledger deepening +
demonstrated UNVERIFIED). P1 stays DETECT+ALERT only even when authoritative (auto-fix = P3).

**No HIGH/CRIT open outside the batch:** A-1 CLOSED on 9becf8c; C-2 Phase-2 (secret+rate-limit) already
on main (d922007 ancestor). Only residual = C-2 network Phase-3 (deferred infra).

**Deferred (NOT in batch):** C-1 history-purge · optional api_key rotate · C-2 network Phase-3 ·
P1 ledger-deepening · T2 full-repair · credentials.xlsx delete · W10 double-cost · one-symbol-vs-whole
SOFT_KILL question.

Related: [[p1_eod_broker_reconcile_impl_02jul]] [[b1_daily_loss_unrealized_mtm_impl_02jul]]
[[a2_timeout_retry_impl_02jul]] [[c1_secret_remediation_02jul]] [[audit_remediation_status_02jul]]
