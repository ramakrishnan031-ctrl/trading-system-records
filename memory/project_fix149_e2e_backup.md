---
name: fix149-e2e-backup
description: FIX-149 end-to-end integration test (7 tests) + backup restore drill script with monthly cron
metadata: 
  node_type: memory
  type: project
  originSessionId: 8481a692-05c3-4b15-ba44-00f7b0a40666
---

FIX-149 landed (2026-06-03, commit ea2e3fa, pushed+deployed).

**Task 1: End-to-end integration test** (`tests/integration/test_full_signal_flow.py`)
- 7 tests covering full signal lifecycle with mocked broker
- Happy path: webhook -> screen -> size -> reserve -> place -> fill -> TGT hit -> close
  - Assertions: strategy, P&L, capital accounting, no orphans, no naked positions, report gen
- Sad path 1: risk rejection (max_open_positions saturated) -> no trade, capital unchanged
- Sad path 2: broker rejection (OrderRejectedError) -> FAILED trade, capital released
- Sad path 3: SL hit -> negative P&L, exit_reason=SL_HIT, costs deducted
- Uses `paper_auto_fill_delay_sec=60.0` to suppress synth threads (deterministic fill control)

**Task 2: Backup restore drill** (`scripts/backup_restore_drill.py`)
- Picks latest backup from data_store/backups/
- Restores to temp DB, validates: schema version, integrity_check, 27 tables, FK consistency, WAL checkpoint, sample queries
- Outputs drill report to docs/backup_drill_YYYY-MM-DD.md
- Monthly cron: 1st of month, 03:00 IST

**Test count:** 2725 passed, 12 skipped (baseline 2718 + 7 new)

**Why:** System needs proven end-to-end flow verification and validated backup restoration.
**How to apply:** Monthly drill runs automatically; integration tests run with every pytest invocation.
