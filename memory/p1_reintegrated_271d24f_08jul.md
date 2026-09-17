---
name: p1_reintegrated_271d24f_08jul
description: P1 eod_broker_reconcile RE-INTEGRATED onto current main 271d24f — branch wave4-p1-v2 @3ef7c35 (LOCAL/UNPUSHED/undeployed); schema v42 + terminal-guard trigger coexist; validated; SHADOW-default; supersedes wave4-p1 branch
metadata: 
  node_type: memory
  type: project
  originSessionId: a1ce6ed3-8992-41fa-9570-f5c148c8d6b8
---

**P1 (broker-authoritative EOD reconcile) RE-INTEGRATED onto 271d24f — branch `wave4-p1-v2` @ `3ef7c35` (08-Jul, LOCAL/UNPUSHED, UNDEPLOYED, cron NOT installed, main untouched at 271d24f).** Reason: the old `wave4-p1` (`c54f688`) was based on `eb75731`; main advanced to `271d24f` (= eb75731 + Wave-5 H-7 `2023948` + FIX-067 `3f4587f` + terminal-guard `24127a1` + M-C1 `0fba665` + docs). Cherry-picked P1's delta (orig `4817032`) onto a fresh branch off 271d24f. **Supersedes [[p1_wave4_integration_validated_07jul]] (branch wave4-p1, discard).**

**Overlap analysis — runbook's premise was PARTLY WRONG (verified at source):** the ONLY file both P1 and Wave-5 touch is `core/schema.sql`. Wave-5 did NOT touch `core/state_store.py` (the terminal-guard D-1 CAS lives in `orders/order_manager.py:493 close_trade`; the M-C1 helper lives in `capital/fund_manager.py:1664`). So state_store had ZERO signature drift → P1's 3 reconcile methods apply clean.

**Schema-version reconciliation OUTCOME (the crux):**
- `core/schema.sql` auto-merged CLEANLY (the two hunks are ~1200 lines apart): terminal-guard trigger `trg_trades_terminal_status_guard` (from 271d24f, ~line 278, behaviour-only, was v41) + P1's `eod_broker_reconciliation` table (~line 1487) **coexist**; single `schema_version` marker = **42** (P1's bump now stacks on the trigger). Both idempotent `CREATE … IF NOT EXISTS`.
- `EXPECTED_SCHEMA_VERSION` 41→42 (`state_store.py:101`). The **4 hardcoded `==41` test assertions are all in the 3 files P1 already updates** (test_config_snapshotter/sr_detector_observer/sr_v2_monitor — Wave-5 never touched them, so P1's 41→42 applies clean). **Wave-5's 4 new test files have ZERO schema-version assertions.** Every other assertion is dynamic (`==EXPECTED_SCHEMA_VERSION`) → auto-follows to 42. No orphan 41-assertions.
- M-C1's fund_manager change is additive-only (no P1-facing signature drift); P1 does NOT touch main.py (M-C1 seed intact).

**Validation (all local, real collaborators):**
- Integration set **330 passed / 0 failed** (P1's 15 + all 4 Wave-5 suites: H-7 TOCTOU / FIX-067 / terminal-guard illegal-transition matrix / M-C1 + every schema-version test + Wave-5-modified suites) at v42.
- Full `tests/unit/` **4305 passed / 10 failed / 13 skipped**; the SAME 10 fail IDENTICALLY on a clean `271d24f` worktree (order_placer_fix061 ×4, test_main webhook/gate ×4, fix181 ×1, flask max-content ×1) = pre-existing PC-env (green on VM). **Zero new failures from the re-integration.**
- Fresh build lands at v42 with trigger + table + integrity ok.
- **Migration v41(+trigger)→v42 on a throwaway COPY**: adds table, bumps to 42, trigger coexists, data preserved (seeded trade+signal survived), integrity ok, new table functional, idempotent re-open. Live DB untouched.
- **Parity**: `scripts/eod_broker_reconcile.py` byte-identical to `c54f688` (empty diff) → P1 paper SELF_CONSISTENCY path UNCHANGED.
- Pre-commit hook regenerated `deploy/cron/trading-system.cron` (generate==committed; `eod_broker_reconcile` @15:58 Mon-Fri present). Working tree clean.

**SHADOW default** (`eod_reconcile.authoritative=false` = log-only, zero behaviour change). **NOT pushed/deployed/cron-installed.** Web Claude writes the P1 SHADOW deploy runbook (off-market) from THIS re-integrated state. **PATHS.md: no change.** SYSTEM_MAP.md P1-reintegration changelog entry PENDING the next off-market doc-sync on main (deferred to honour the runbook's "keep main untouched" — batched with the Wave-5 runtime-validation entry [[wave5_runtime_validated_08jul]]). [[p1_eod_broker_reconcile_wave4_investigation_06jul]] · [[eod_verify_honest_fix_07jul]]
