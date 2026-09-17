---
name: integration-merge-blocked-15jul
description: "15-Jul combined-deploy (Branch A + Branch B) — was BLOCKED on an F2 stale mock, now CLEARED (autospec fix + prevention, all gates green, tag deploy-15jul-combined). UNPUSHED, awaiting Rama's push."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5e0da463-297c-4dc3-bb3f-4db09f2c57a7
---

**15-Jul COMBINED-DEPLOY INTEGRATION — 🟢 CLEARED (ready for Rama's push).**
Was BLOCKED (regression red on 2 Branch-B/F2 stale-mock tests); resolved test-only after an
approved compatibility audit, all deploy-integrity gates green, annotated rollback tag created.
**NOTHING PUSHED.**

**Git state (all LOCAL, UNPUSHED):**
- Merged `main` HEAD = **`c9fb298`** (docs tail: PATHS pending-note `c9fb298` · report CLEARED
  `cb567cb` · prevention docs `32389c0` · guard `1645bd6` · autospec `397f3f6` · STOP report
  `714b733` · Q4 test `894db27` · merge `b749882`).
- **Tag `deploy-15jul-combined` → `1645bd6`** (annotated; single-tag rollback point = the
  fully-gated code HEAD; docs commits ride on top).
- Merge parents `1c891b6` (Branch B) + `0c7a6dd` (Branch A). **Schema v44** unchanged.
- **VM == bare == `2dc69d5`** (22 commits behind; nothing pushed).

**The blocker + resolution (test-only; production was already correct):**
Branch-B/F2 (`795a417`) added optional `functional_status` to `record_heartbeat` (before
`db_path`); `HeartbeatTimer.__exit__` forwards it; the pre-existing `_capture` mock in
`test_fix135_fno_ban.py` froze the old param list → `TypeError`. **Compatibility audit found NO
production incompatibility** — one canonical def; all ~30 callers + wrappers pass `db_path` by
keyword (so the insertion misbinds nothing); reader (`cron_officer.parse_functional_status`)
compatible; no partial/decorator/adapter freezes the signature. Only 2 test mocks affected.

**Fixes + prevention (commits `397f3f6`, `1645bd6`, `32389c0`):** both mocks →
`create_autospec(record_heartbeat)` (assertions preserved via `call_args`); **signature-lock
contract test + discovery-guard test** (`tests/unit/test_cron_heartbeat_contract.py`) — guard
proven to flag the old stub and pass the autospec/permissive forms; **Interface Change Checklist**
engineering pattern in `docs/monitoring_prevention_checklist.md` (callers·wrappers·mocks·autospec·
contract·discovery-guard on any signature change), referenced from `docs/SYSTEM_MAP.md`, with an
explicit **scope lock** (guard stays record_heartbeat-only, no AST/repo-wide scanner this cycle).

**Gates — all GREEN:** combined regression **5052 pass / 12 fail** (14→12; the 12 = the known
PC-env set ONLY, identical to baseline `0a77c92`, zero new); Q4 overlap integration test 1 passed;
**EOD dry-run clean on a DB COPY** (all 7 steps OK incl. Branch-A FK-safe eod_cleanup prune +
fm_ledger `ledger_id` fix; `foreign_key_check` clean + `integrity_check` ok; copy deleted; live
side-effects neutralized); **deploy_assert rc=0** (blockers clear; the Windows-console ✅-emoji
`UnicodeEncodeError`→exit1 is cosmetic/cp1252, UTF-8/VM exits 0); live `integrity_check` ok +
`foreign_key_check` empty; schema v44.

**Rama's runbook (docs/audit/integration_deploy_15jul2026.md §8):** F0 restore
`ALERT_SMTP_PASSWORD` → backup → push main+tag → verify deploy (bare HEAD==`32389c0`, v44, canary
08:20) → **ONLY THEN** Phase-B supervised prune (`eod_cleanup --signal-retention-days 7|30`;
default 90d prunes 0 now) → next-EOD verify. Rollback L1 per-branch revert / L2 reset to the tag.

See [[unpushed-pending-deploy-ledger]], [[monitoring-hardening-15jul]], [[fixes-15jul]],
[[migration-on-open-rule-14jul]], [[pc-test-env-hygiene]].
