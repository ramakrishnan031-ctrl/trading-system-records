---
name: migration-on-open-rule-14jul
description: "ARCHITECTURAL RULE — schema migrations run on DB-OPEN (StateStore.__init__), not at boot. Any process opening the live DB with newer code migrates it, incl. during market hours. Rule+inventory recorded; a migration GUARD is PROPOSED not implemented (Rama decision)."
metadata: 
  node_type: memory
  type: project
  originSessionId: af2049f8-fa39-4730-86ad-2bdf2b3c024d
  modified: 2026-07-24T10:18:47.311Z
---

**SCHEMA MIGRATIONS RUN ON DB-OPEN, NOT "AT BOOT" (verified 14-Jul against source).** `core/state_store.py::StateStore.__init__` (line 180) → `_initialize_schema()`: reads on-disk `schema_version`; if `old_version < EXPECTED_SCHEMA_VERSION` runs `migrations.run_migrations()` (**rebuilds** affected tables) + `relocate_analytics` then `executescript(schema.sql)`. **This fires whenever ANY process constructs a `StateStore` against the live DB with newer code** — whichever opens FIRST after a schema-changing push. The 08:15 `main.py` boot is only the first opener on a normal day, NOT the mechanism.

**Empirical proof (13-Jul):** v42→v43 migrated **19:30** (`cron_watchdog`); v43→v44 **23:41** (`forward_shadow_record` V4 run). **Neither at boot.** Both additive+off-market → harmless by timing luck, not design. **Corrects our standing belief** "deploy schema off-market → migrates at next 08:15 boot" — WRONG; it migrates on the first open.

**RISK:** a schema pushed such that a **during-market** StateStore-opener runs first → live-table REBUILD runs 09:00-15:30 with `main.py` running on the DB. Realistic trigger = **`cron_officer` (09:20 + hourly)**. The off-market-push convention is the ONLY thing preventing this today (unenforced).

**Migration TRIGGERS = the 24 StateStore-constructing processes** (main.py + 23 scripts). **NOT triggers (by mechanism):** GUI `ops_dashboard` (`?mode=ro`, a ro conn can't `executescript`) · `capture_metrics_baseline` (`*/5 09-15`, raw `db_connect`, no StateStore) · `db_backup` (`sqlite3 .backup` CLI). The frequent during-market openers are safe by mechanism, not intent; the unsafe one is `cron_officer`.

**COROLLARY:** a "read-only verification" of the LIVE DB with newer code is NOT read-only — opening a StateStore migrates it. Always `--db <copy>` (V1-V4 did). The 23:41 run was a REAL run (captured 3467 records) so its live open was legitimate — and is exactly why v43→v44 happened then.

**Recorded:** SYSTEM_MAP.md §Deploy (prominent, not a footnote) + PATHS.md top + full doc `docs/audit/migration_on_open_rule_14jul2026.md` (rule + inventory + proposal). Committed `d634f1c` (docs-only).

**✅ GUARD BUILT `ed1c4b9` (14-Jul, Rama ratified AC1-AC5 — corrected my Opt-1: a blanket time-refusal would block main.py from starting after a mid-session crash = lost session; RIGHT boundary = "only the boot path migrates"):** `StateStore.__init__(..., *, allow_migrate=False, market_open=False)` + `MigrationNotPermitted` + `_refuse_migration` (drops CRITICAL sentinel via function-local `alerts.critical` import, then raises). `_initialize_schema`: migrate iff `allow_migrate AND NOT market_open`, else refuse.
- **AC1** only `main.py:1566` passes `allow_migrate=True`; 23 other openers default False → refuse. **AC2** main.py passes `market_open`=(weekday ∧ 09:15-15:30 from config) → boot refuses in-market. **AC3** blocked → CRITICAL sentinel naming vN→vN+1 + raise, never silent. **AC4** off-market restart recovers; no manual surgery. **AC5** newer-than-code fail-fast preserved.
- **PROVEN** `tests/unit/test_migration_guard.py` (6): non-boot refuses+DB-untouched · boot migrates off-market · boot refuses in-market · **FORCED block fires the CRITICAL sentinel naming v43→v44** (alert path proven like V2) · current/fresh DBs still open for every opener. Migration tests (test_migrations/test_schema_version_failfast) opt into boot path (`allow_migrate=True`). **Zero-new:** state_store+migrations 126 pass; test_main stash-diff 26==26. Accepted consequence: a schema deployed before the next boot → forward-shadow cron fails loud + skips a day (right trade).

**§1 also recorded (same commit):** the 13-Jul 23:31 CRITICAL email (`20260713_233122_2506c85a`) = the deliberate forward-shadow forced-failure, **RECEIVED IN RAMA'S INBOX** → crash→sentinel→alert_watcher→Telegram+email→Rama chain PROVEN END-TO-END by the recipient (strongest verification of the P4/M-A1 + P5 alert work). See [[q5-wave7-backlog-14jul]] · [[unpushed-pending-deploy-ledger]].

**⚠️ SCHEMA-VERSION SOURCE — ROLLBACK TRAP (24-Jul, verified live):** the on-disk version read at `_initialize_schema` lives in **`schema_meta`** — a `(key, value)` table: `SELECT value FROM schema_meta WHERE key='schema_version'` → **`44`**. It is **NOT `PRAGMA user_version`**, which is **`0`** and will mislead a rollback operator (the natural reflex) into "unversioned / version zero". Read `schema_meta`, never the pragma. Recorded in `docs/SYSTEM_MAP.md` at the schema-migration rule heading (where a rollback operator reads it), per the "record it where the reader is" rule.
