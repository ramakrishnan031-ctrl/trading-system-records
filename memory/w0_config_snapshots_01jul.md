---
name: w0_config_snapshots_01jul
description: W0 report-redesign foundation — config_snapshots table (schema v41) + startup writer; STAGED not pushed
metadata: 
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**W0 — config_snapshots writer** (01-Jul-2026). First build of the approved daily-report
redesign. Gives the report's Config sheet + historical re-runs a DB-pure source for "what
config was live on date X". Builds on the Phase-0 audit ([[daily_report_redesign_phase0_audit_30jun]],
Sheet-2 Config_data, which recommended exactly this — option A).

**Investigation stop-gate = CLEAN** (all 3 hard conditions green):
- Config IS centralized as ONE Pydantic `AppConfig` via `core/config_loader.load_all()`
  (`main.py:1485`) — not a raw dict, but `.model_dump(mode="json")` gives the full JSON dict.
- Resolved ONCE per startup; no hot-reload (CL5/CL6). Restart re-reads YAML.
- NO full-config snapshotting existed. There IS per-FILE hash change-detection
  (`utils/startup_checks.check_config_hash` + `session.last_config_hash` = `json.dumps(app_config.file_hashes)`)
  — a DISTINCT mechanism (file hashes, not the full config JSON). W0's `config_hash` is sha256 of the whole config.

**BUILD (files):**
- `core/schema.sql` TABLE 46 `config_snapshots` (snapshot_id PK / snapshot_date / snapshot_ts /
  account_id / mode / trade_type / config_hash / config_json) + `idx_config_snapshots_date`.
  Schema **v40→v41 PURE ADDITION** (no MIGRATION_TABLES entry; same path as v37/v39/v40).
- `core/state_store.py` `EXPECTED_SCHEMA_VERSION = 41`. `core/migrations.py` v36→v41 pure-addition note.
- `core/config_snapshotter.py` — NEW. `snapshot_config(store, app_config, *, snapshot_date, snapshot_ts,
  account_id, mode, trade_type)` serializes `model_dump(mode="json")` → stable sorted JSON → sha256.
  **IDEMPOTENT per (snapshot_date, config_hash)**: identical → skip (returns None); same-day config
  change → new row. Uses `store.fetch_one`/`store.transaction` (NO new StateStore DAO — minimal blast radius).
- `main.py` (~L1824, after `is_paper` finalized post interactive-flip, after `--status`/`--dry-run` return):
  one `snapshot_config(...)` call, `try/except` non-fatal. Fires in BOTH paper+live (mode is a column → parity).
- `docs/report_data_contract.md` — NEW permanent SYSTEM-writer↔REPORT contract; Config rows seeded.
- Test pins: `test_control_tower_phase1a` de-brittled (`>=40` + `==EXPECTED_SCHEMA_VERSION`);
  `test_sr_detector_observer` + `test_sr_v2_monitor` bumped `==41`. NEW `tests/unit/test_config_snapshotter.py` (13).

**Key decisions (non-obvious):**
- **Strategies NOT snapshotted** — `strategies/*.yaml` load via a SEPARATE `StrategyLoader` (late,
  `main.py:2292`), NOT part of the `load_all()` AppConfig. Per-strategy params = `NEEDS_CAPTURE`
  follow-up in the contract (own table or a `_strategies` key). W0 captures the COMPLETE AppConfig
  (8 sub-configs + file_hashes) unfiltered — that covers trading_hours/capital/risk/position_sizing/
  leverage_map/scoring/broker_costs/slippage/excluded_symbols (closes audit Gap #7), just not strategies.
- **Secret-safe by CL5** — the resolved config expands NO env vars, so config_json holds env-var NAMES
  only (never values); the one plaintext `alerts.smtp.password` is EMPTY in prod. Writer logs only row-id + hash-prefix.
- **"heartbeat" in the work order = logging discipline**, not a cron heartbeat (this is a startup step, not a cron job).

**Verified on REAL repo config**: 1 row, config_hash `ad3ff375…`, 12,378-byte VALID JSON, all 8 sub-configs +
file_hashes present; re-run returned None (idempotent), count stayed 1. **4126 pass / 13 skip / 0 fail** full unit suite.

**STATUS: STAGED — NOT pushed** (Rama pushes off-market). NO cron / NO flags / NO trading-code. Schema v41
applies at the next boot after deploy (like every prior pure-addition). NOT on a branch yet — working tree only.
See [[feedback_foundation_rules]] (derive-don't-duplicate, DB-only report rule) + [[feedback_paper_live_parity]].
Docs updated: SYSTEM_MAP header + DB section, PATHS Main-DB line + W0 section, report_data_contract.md (new).
