---
name: p1_eod_broker_reconcile_wave4_investigation_06jul
description: "Wave-4 P1 investigation (06-Jul, READ-ONLY): eod_broker_reconcile SHADOW feeder is on branch fix-p1-eod-broker-reconcile-02jul (4817032), ABSENT at main. Verdict NEEDS-WORK (design GO; deploy needs rebase + 2 config-merge + cron-sha + schema-assert sweep). Paper handled; schema 41→42 coupled."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-4 P1 `eod_broker_reconcile` INVESTIGATION (06-Jul, read-only; NO fix/deploy).** Verdict = **NEEDS-WORK** (the feeder design is GO-quality + shadow-safe; the DEPLOY MECHANICS need a rebase + merge work). Full report in-session. Related: [[p1_eod_broker_reconcile_impl_02jul]] (build) · design `docs/design/p1_eod_broker_reconcile_build_design_02jul2026.md`.

## AREA 1 — location + what it is
- **Branch `fix-p1-eod-broker-reconcile-02jul`, single commit `4817032` (02-Jul, SHADOW). ABSENT at main HEAD `9709a46`** (confirms audit; the G5 deploy that reached main did NOT carry it — only gui-g2* branches inherited it). No stash, not uncommitted.
- **458-line standalone feeder** `scripts/eod_broker_reconcile.py` @15:58 Mon-Fri, OWN creds (`reconcile_positions._resolve_credentials`) → runs even if trading-system.service was DOWN at 15:17. Queries broker positions/day-realized-P&L/open-orders/margins; compares to local (open trades, pending orders, `get_today_closed_pnl`, fm_ledger invariant, position_reconciliation 15:45). Per-dim verdict: REQUIRED (positions/orders/pnl) unavailable→**UNVERIFIED (never false VERIFIED)**; LEDGER=local invariant; MARGIN=supplemental, reliability-gated [09:00-15:45]→NOT_CHECKED @15:58 (FIX-189). Persists `eod_broker_reconciliation` verdict row + `pnl_reconciliation` (correct columns). **DETECT+VERIFY+ALERT ONLY — never mutates trades/exit/capital.**
- Commit footprint (NOT just a new file): `scripts/eod_broker_reconcile.py`(+458) + `core/schema.sql`(+37) + `core/state_store.py`(+38 writer/reader) + `config/system_config.yaml`+`config_loader.py`(EodReconcileConfig) + `cron_registry.yaml`(+18)+`deploy/cron/trading-system.cron`(+3) + `tests/unit/test_eod_broker_reconcile.py`(**15 tests**, pure verdict matrix) + 3 test files' schema-assert 41→42.

## AREA 2 — deploy-risk
- **ISOLATION: LOW blast radius** — standalone EOD cron, writes only its own outputs, zero trading-path touch.
- **FAILURE MODES: safe** — per-dim broker failure→that field None→UNVERIFIED (no false pass); total creds/query fail→all-None→UNVERIFIED. Margin gated out @15:58 (no post-close false-positive). Broker DAY-realized P&L IS available post-close (kite positions().day). SHADOW default = INFO-only.
- **CREDS: needs Kite token @15:58** (own creds, like reconcile_positions) — token valid through the day; path `data_store/session/zerodha_token.json` (post-S-1B.2 unchanged). OK.
- **PAPER (parity) — CORRECTLY HANDLED (no fix needed):** paper builds broker=mirror-of-local → **SELF_CONSISTENCY** verdict, `mode=PAPER`/self_consistency=1, margin NOT_CHECKED, **never a false FAIL, never counted as broker-authoritative**. Exactly the required nuance.

## AREA 3 — schema (the crux)
- New table **`eod_broker_reconciliation`** (TABLE 47) = **PURE ADD** (`CREATE TABLE IF NOT EXISTS`, no ALTER/rebuild; `detail` col commented "NEVER a secret"). **BUMPS schema_version 41→42** (schema_meta INSERT). **Coupled**: branch `state_store.py EXPECTED_SCHEMA_VERSION = 42` in the same commit → forward-clean.
- state_store guard: on open, executescript (bumps schema_meta) then `if version != EXPECTED_SCHEMA_VERSION: raise SchemaVersionMismatch`. So against the current scrubbed **v41** DB, deploying P1 (v42 schema + EXPECTED=42) auto-migrates 41→42 idempotently, opens clean. **Version-guard relevance (the LOW→HIGH finding): forward-safe; but once the DB is v42, rolling back to pre-P1 code (EXPECTED=41) is REFUSED by the guard** → rollback must be the config flag (`authoritative:false`), NOT a code revert, unless the DB is also handled.

## AREA 4 — cron
- **Cron entry IS in the TRACKED canonical crontab** (`deploy/cron/trading-system.cron`: `58 15 * * 1-5 … scripts/eod_broker_reconcile.py`) + `cron_registry.yaml` (`eod_broker_reconcile`, `58 15 * * 1-5`, critical/market_day_only/monitored/enabled). → a push auto-installs it via post-receive; **no manual cron step**. Timing @15:58 aligns with post-close broker P&L availability (after reconcile_positions @15:45).

## NEEDS-WORK before deploy (none are blockers; standard rebase of a 4-day-old shadow branch)
1. **Rebase/merge onto current main** (branched at `9becf8c`, **46 commits behind** `9709a46`). `git merge-tree` = "changed in both" on **`config/system_config.yaml` + `core/config_loader.py`** (both P1 and main added config since base) → manual 3-way merge (additive). schema.sql / state_store.py / cron_registry / canonical-cron merge CLEAN (main didn't touch them since base).
2. **Re-run full suite post-rebase** + sweep ALL schema-version test assertions 41→42 (P1 updated 3; main may have added more v41-asserting tests since 9becf8c). Verify P1's store-method calls still match current-main signatures.
3. **Regenerate `deploy/cron/trading-system.cron` + its sha** from the merged cron_registry (post-receive checks the sha).
4. Confirm `authoritative:false` (SHADOW) at deploy = log-only, zero behavior change.

**Overall: NEEDS-WORK** (rebase + 2 config-conflict resolution + cron-sha regen + test sweep), then a clean SHADOW deploy. **Schema verdict:** bumps 41→42 (coupled, pure-add, idempotent, forward-clean; version-guard = rollback-via-flag not code-revert). **Paper verdict:** correctly handled (self-consistency, never false-FAIL). STOP — no fix/deploy; Web Claude sequences Wave-4.
