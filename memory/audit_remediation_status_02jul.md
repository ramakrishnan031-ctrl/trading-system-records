---
name: audit_remediation_status_02jul
description: 02-Jul audit (1 CRIT + 4 HIGH) remediation status + P1/P2 dependency map — B-1 is the one OPEN HIGH outside P1/P2 (fix before/with P1); no HIGH is a P1/P2 deliverable
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

Reconciliation of the 02-Jul audit's 1 CRITICAL + 4 HIGH against current state, before the P1 build. Read-only. Full table: `docs/audit/audit_remediation_status_02jul2026.md` (SYSTEM_MAP + PATHS point to it). Deployed baseline `origin/main = 9becf8c` (audit's own baseline was `59f83b5`).

**Status of the 5:**
- **C-1 (CRIT)** — live exposure CLOSED (scrub `7bc3367` deployed in `9becf8c` + all creds rotated 02-Jul); residual PARTIAL (script api_key fix + `.xlsx` scanner + purge runbook `aa02f9f`, unpushed); history-purge = runbook ready, not run. OUTSIDE P1.
- **A-1 (HIGH)** — **CLOSED + deployed** (`9becf8c`, `_recover_in_flight_entries`). OUTSIDE P1.
- **A-2 (HIGH)** — PARTIAL: built, unpushed (`fd09a38`); deploy after 03-Jul 08:15 boot. OUTSIDE P1.
- **B-1 (HIGH)** — **OPEN, untouched**. `risk_engine.py:497-510` sums `get_total_unrealized_mtm()` into the daily-loss gate, but writers `update_unrealized_mtm`/`remove_unrealized_mtm` (`fund_manager.py:1404/1416`) have ZERO production callers (only `test_fund_manager.py`) → gate is realized-only → concurrent open unrealized drawdown can overshoot the 3% limit. **OUTSIDE P1 & P2.**
- **C-2 (HIGH)** — PARTIAL: Phase-2 (WEBHOOK_SECRET both modes + per-IP rate limit) deployed `d922007`/`9becf8c`; network layer still OPEN (`bind_host:"0.0.0.0"` + `require_hmac:false`, plaintext `?token=`, `system_config.yaml:179,187`) = Rama's network call. OUTSIDE P1 & P2.

**Dependency map answers:**
- CLOSED/deployed HIGH: **A-1 only** (A-2 built-unpushed; C-1 live-exposure closed but residual unpushed).
- HIGHs represented by P1/P2: **NONE.** P1 addresses W3 (work-item, not a HIGH) + the eod_verify false-VERIFY; P2 addresses E-4 (LOW-MED /health liveness). No headline HIGH is a P1/P2 deliverable.
- OPEN HIGH outside P1/P2: **B-1** (fully) + **C-2 network** (partial).

**Sequencing:** **B-1 = do BEFORE or WITH P1** (independent subsystem, closes a dead advertised capital control, smaller than P1 — the writer exists, just needs a live per-position MTM source wired + remove-on-close). **C-2 network = AFTER P1** (auth already deployed; network-architecture decision). Nothing higher-risk than P1's target sits un-started except B-1.

**Deploy picture (unpushed):** `fix-a2-timeout-no-retry-02jul@fd09a38` (A-2) · **`fix-c1-completion-02jul@aa02f9f`** = STACKED A-2+C-1 (the practical push; boot-gated) · `fix-t2-import-02jul@b826ae0` = parked/superseded. Uncommitted working-tree docs (P1 assessment, this reconciliation, SYSTEM_MAP/PATHS) doc-only on the c1 branch. Not-yet-started: B-1, P1/P2/P3, C-2 Phase-3, C-1 history purge, optional api_key rotation. Related: [[ref_security_audit_02jul]], [[a1_e1_orphan_fix_impl_02jul]], [[a2_timeout_retry_impl_02jul]], [[c1_secret_remediation_02jul]], [[c2_webhook_lockdown_02jul]], [[p1_eod_broker_sync_assessment_02jul]], [[dual_daily_loss_mechanism]].
