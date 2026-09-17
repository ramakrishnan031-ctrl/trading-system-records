---
name: p1_reintegrated_failfast_main_08jul
description: "P1 (EOD broker-reconcile, v42) RE-INTEGRATED onto the fail-fast main — branch wave4-p1-v3 @a62ece5 (LOCAL/UNPUSHED, undeployed, SHADOW); v42+trigger+fail-fast coexist; 0 regression; v42-migration×fail-fast validated; PUSH-2 pending"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e32bad3-6610-4e3c-a772-6502eeb354b4
---

**P1 RE-INTEGRATED onto the fail-fast main — branch `wave4-p1-v3` (`a62ece5` P1 + `e12e52e` SYSTEM_MAP doc, LOCAL/UNPUSHED, NOT merged/deployed, cron NOT installed, SHADOW default `eod_reconcile.authoritative:false`). Supersedes [[p1_reintegrated_271d24f_08jul]]** (wave4-p1-v2/`3ef7c35` was on the stale pre-PUSH-1 base `271d24f`).

**Re-cherry-pick:** P1 (orig `3ef7c35`) onto current main `7338e08` (= PUSH-1 infra+A-3 `9bcc1eb` + fail-fast `0b816dc` + docs). Cherry-pick CLEAN; `core/state_store.py` AUTO-MERGED — the fail-fast guard (`_initialize_schema` ~:335) and P1's changes (EXPECTED bump @:101, reconcile methods @:2817/:2834) are disjoint hunks. Confirmed the auto-merge did NOT disturb the fail-fast guard.

**Coexistence (verified):** `schema.sql` — BOTH `trg_trades_terminal_status_guard` (:278) AND `eod_broker_reconciliation` (:1487) present, `schema_version='42'` (:1509). `state_store.py` — fail-fast guard INTACT + `EXPECTED_SCHEMA_VERSION=42` → the guard now keys off 42: v41<42 migrates up, v42==42 boots, v43+ raises. config additive (`eod_reconcile:` + `EodReconcileConfig`); cron additive; `main.py` (M-C1 seed) untouched by P1; P1's state_store call signatures (`get_all_open_trades`/`get_pending_intraday_orders`/`get_today_closed_pnl` + its own `upsert/get_eod_broker_reconciliation`) re-verified vs current main.

**Validation (wave4-p1-v3, Py3.11.9):**
- Full suite **11 fail / 4373 pass / 15 skip** — the 11 = the IDENTICAL pre-existing PC-env set (fix061×4 / fix181 inflight-orphan / test_main×4 / interactive_startup holiday-guard / phase17 flask-max-content); +18 pass vs the `9bcc1eb` baseline (4355) = P1's 15 tests + the 3 fail-fast tests → **0 regression**.
- **v42 migration × fail-fast (throwaway COPY DBs, live DB untouched):** (2a FORWARD) a genuine v41 DB (built v42 → dropped table → stamped 41) opened by v42 code → migrates to v42 (table CREATED, trigger coexists, `integrity_check`=ok, idempotent re-open), fail-fast does NOT fire. (2b ROLLBACK) a real checkpointed v42 DB opened by the v41-EXPECTED main code (via a detached `git worktree` of `7338e08`) → RAISES `SchemaVersionMismatch` + version untouched at 42 → confirms **config-flag-only rollback** (`authoritative:false`), NOT code-revert.
- Assertion sweep: no hardcoded `==41` version asserts remain (P1 updated its 3 test files; the fail-fast tests are version-relative).
- ⚠️ **Test-scaffolding gotcha (NOT a bug):** MSYS `/c/...` paths handed to native Windows Python mis-resolve to a bogus drive root (create/read empty DBs); + a WAL isn't cross-process-visible until a TRUNCATE checkpoint. Both bit the bash-orchestrated cross-process 2b until fixed with `cygpath`/Windows paths + explicit `PRAGMA wal_checkpoint(TRUNCATE)`. For any cross-process DB test use `tmp_path`/`tempfile` (real Windows paths) + checkpoint.

**Parity:** `eod_broker_reconcile` paper SELF_CONSISTENCY intact (P1 tests green; mode-aware, never broker-authoritative in paper).

**⚠️ UPDATE (08-Jul, same evening):** main has since advanced PAST `7338e08` — the schema-version fail-fast was deployed early (merged+pushed as part of the GUI login deploy, `9815786`; see `schema_version_failfast_08jul`). The fail-fast guard is now LIVE in production ahead of P1. `wave4-p1-v3` (based on `7338e08`) still contains ONLY the fail-fast + P1's own commit — P1 itself remains UNMERGED/undeployed. **PUSH-2 must now merge `wave4-p1-v3` onto the NEW main tip (`9815786`+)**, not `7338e08` — re-check for conflicts against the login-redesign files (unlikely, disjoint paths: `ops_dashboard/` vs P1's `core/schema.sql`+`core/state_store.py`+`scripts/eod_broker_reconcile.py`) before the coordinated deploy.

**NEXT:** Web Claude issues the coordinated **PUSH-2** (merge `wave4-p1-v3` → current main + push + SHADOW deploy; the SYSTEM_MAP P1 entry rides along on the branch). [[schema_version_failfast_08jul]] · [[push1_pc_vm_sync_08jul]] · [[fresh_audit_postremediation_08jul]]
