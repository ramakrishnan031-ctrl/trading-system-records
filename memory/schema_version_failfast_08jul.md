---
name: schema_version_failfast_08jul
description: "Schema-version fail-fast BUILT (commit 0b816dc + doc 7338e08, main, LOCAL/UNPUSHED) — state_store refuses a NEWER DB instead of silent-downgrade; ships with P1/v42 (PUSH-2); corrects P1 \"refuses v42\" → rollback = config-flag NOT code-revert"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e32bad3-6610-4e3c-a772-6502eeb354b4
---

**Schema-version FAIL-FAST — BUILT + committed 08-Jul (`0b816dc` fix + `7338e08` doc, main, LOCAL/UNPUSHED, off `005c007`). Ships before/with the P1 v42 deploy (PUSH-2). Behaviour-only, `EXPECTED_SCHEMA_VERSION` stays 41.** From fresh-audit §B.1 [[fresh_audit_postremediation_08jul]] (was Audit-A LOW, ELEVATED because P1/v42 is imminent).

**Root cause** (`core/state_store.py::_initialize_schema`, ~:333-376): migrate gate `old_version < EXPECTED` + the following `executescript()` is UNCONDITIONAL (re-creates the terminal-guard trigger + re-stamps `schema_version` every boot). A DB stamped NEWER than the code (a v42 P1 DB opened by v41 code after a code-revert) SKIPPED migration, then executescript **silently stamped the version DOWN to 41** and booted clean — the `:371` `version==EXPECTED` check passed because the stored version had already been rewritten. Silent downgrade, stranded newer tables.

**Fix:** right after `old_version` is read (`:333`) and BEFORE executescript, `if old_version is not None and old_version > EXPECTED_SCHEMA_VERSION: raise SchemaVersionMismatch(...)`. Stored version left INTACT for diagnosis (executescript never runs on the raise). Reuses existing `SchemaVersionMismatch(StateStoreError)` (`:129`). Two legal paths preserved EXACTLY: `< EXPECTED` migrates up, `== EXPECTED` boots; trigger / migrations / version-bump untouched; brand-new DB (`old_version is None`) unaffected. Parity: mode-agnostic single path.

**⚠️ CORRECTS [[p1_reintegrated_271d24f_08jul]]:** its parenthetical "old EXPECTED=41 **refuses** a v42 DB" was WRONG — v41 code did NOT refuse; it silently downgraded. The CONCLUSION stands (and is now actually enforced): **P1/v42 rollback = `eod_reconcile.authoritative:false` config flag, NOT a code-revert** (a code-revert now fails fast against a v42 DB instead of downgrading).

**Tests** `tests/unit/test_schema_version_failfast.py` (3, schema-backed — real StateStore + real schema.sql, no mocks): T1 newer→RAISES + stored version NOT mutated (**RED→GREEN proven**: RED on pre-fix = DID-NOT-RAISE + downgraded to 41); T2 older (EXPECTED-1)→migrates up to EXPECTED; T3 equal/fresh→boots + `trg_trades_terminal_status_guard` present (brick check — the legal paths still executescript). **166 green** (new + `test_migrations` + `test_state_store` + `test_terminal_state_write_guard`), 0 regressions. Py3.11.9.

**NOT pushed** — coordinated with P1 (PUSH-2). NEXT (Web Claude): re-integrate P1 `wave4-p1-v2` onto this fail-fast main, then the coordinated SHADOW deploy. [[push1_pc_vm_sync_08jul]] · [[full_repo_audit_04jul_pending]]
