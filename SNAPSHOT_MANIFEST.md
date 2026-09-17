# SNAPSHOT_MANIFEST -- trading-system-records

> **THIS REPOSITORY IS A READ-ONLY SNAPSHOT OF PROJECT RECORDS. IT IS NEVER A DEPLOY TARGET.**
> It holds the records that describe BOTH machines (production and testing) and the project itself. They are kept here, not inside either machine's snapshot, so they never look like one machine's and never diverge into two copies.
> **Cloning on Windows needs `core.longpaths=true`** -- see `README.md`.

## 1. Source and time
- **Taken from the PC** (the operator's Windows workstation) by Claude Code (model `claude-opus-5[1m]`), 17-Sep-2026 (Thursday) IST, in two passes:
  - **~20:10-20:25 IST (commit 1):** `trading-system/docs/SYSTEM_MAP.md` <- `D:/Projects/trading-system/docs/SYSTEM_MAP.md` · `trading-system/PATHS.md` <- `D:/Projects/trading-system/PATHS.md` · `trading-system/docs/audit/` <- `D:/Projects/trading-system/docs/audit/` · `memory/MEMORY_RULES.md` and `memory/UNPUSHED_PENDING_DEPLOY_LEDGER.md` <- the Claude Code project memory directory · `_preservation/` <- `D:/Projects/_preservation/` (every preserved manifest).
  - **~20:45-20:55 IST (commit 2):** the REST of the project memory directory (786 files added: `MEMORY.md`, `MEMORY_HAZARDS.md`, `MEMORY_BOARD.md`, `MEMORY_REFERENCE.md`, the individual notes, `fallback_instructions/`, `memory_snapshots/`) · the exclusions of section 6 applied · `README.md`.
  - ⚠️ The files taken in commit 1 were NOT refreshed in commit 2 (e.g. the ledger and `SYSTEM_MAP.md` have moved on since ~20:20 on the PC).
- **Contents:** 1340 files including this manifest (incl. `README.md`); 29,153,495 bytes before this manifest.

## 2. REDACTIONS -- the only bytes that differ from the PC originals
> ⚠️ **THE REDACTION IS COSMETIC.** It keeps the value out of THIS repository only. **The value still exists on the machines** (in the PC originals, the machines' configuration and elsewhere) -- dealing with that exposure is a separate task for the owner, ⛔ not something this snapshot does.

The testing VM's Telegram channel ID (one value, used for all three Telegram keys on that VM) is replaced by `<TELEGRAM_CHANNEL_ID_REDACTED>` in the copies below. The replacement ran in memory ON THE TESTING VM, so the value never reached the PC; a byte comparison then proved that only the marked spans differ and that each replaced span was a `-` + 13-digit channel ID. **The PC originals are unchanged.**

| File | Replacements | Committed copy md5 |
|---|---:|---|
| `memory/MEMORY_BOARD.md` | 1 | `5eacfa15ae2afac2205004b0bb29cfe7` |
| `memory/UNPUSHED_PENDING_DEPLOY_LEDGER.md` | 1 | `2ae8327fc477959268e3f2de61ac0f2e` |
| `trading-system/PATHS.md` | 2 | `73021dacbceb308c4691541b7f68662a` |
| `trading-system/docs/SYSTEM_MAP.md` | 2 | `1a5931d48dc3bbc0d4f3ed262238f276` |

## 3. Deliberately NOT included
- `docs/` outside `docs/audit/` and `SYSTEM_MAP.md` (e.g. `docs/decisions/`, the live `MASTER_PENDING` register -- preserved copies of the register ARE in `_preservation/`).

## 4. Credential scan -- values never printed
- **PC-side:** 12 distinct secret values from the PC's `.env`; shape rules G1-G5; `.docx`/zip members decompressed; set equality and sha256 of every staged file against its source.
- **VM-side (in memory on the testing VM, via a tar stream):** 25 distinct secret values from the VM's `.env`, two pre-rotation `.env` backups, the Zerodha session file, the GUI secret key, and values harvested from `/home/ubuntu/.gemini`.
- **Value-independent rules:** G7 unquoted key/value secrets and G8 bare token shapes -- every candidate reviewed by value SHAPE (code expressions, environment-variable names, placeholders, an Oracle Cloud CLI profile identifier); a content-based log detector for text files.
- **Positive controls -- all fired** (each source detects its own values; synthetic PEM / Telegram / GitHub strings; a zip member; a real value mid-text; G7/G8 synthetic positives and an md5 negative; the log detector scores real logs 1.00 and non-logs 0.00).
- **Kept, adjudicated:** files matching only PLACEHOLDER values (a 15-character uppercase placeholder configured for accounts D351962 / ZA004 / ZA005; a placeholder secondary Telegram channel); the alert e-mail address (an identifier, not a secret).
- **Limits:** the PRODUCTION VM's `.env` was not read (production access not approved) -- a credential existing ONLY there is covered by the shape rules alone. `.bundle` files were not unpacked and are excluded.

## 5. ⏸ LEFT OUT PENDING RAMA -- these document a CONTRACT rather than carry rows
They were part of the raw query/analysis outputs excluded as DATA; each looks like it documents a contract, so the decision to add any back is Rama's:
- `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/field_scan_970aabf.txt` -- a code scan: every source line naming each StrategyConfig field @970aabf
- `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/harness_s12_output.txt` -- harness output re-feeding recorded production values (not rows; not clearly a contract either)
- `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/schema_cov_screener.txt` -- the DB schema (CREATE TABLE DDL) as read from production
- `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/yaml_table_970aabf.txt` -- a table of every strategy YAML's keys @970aabf
- `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a2c_out.txt` -- the score formula's combination table (which step combinations can reach 60)
- `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a3_out.txt` -- table column lists (schema) mixed with webhook request counts
- `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/agentD_yaml_dump.txt` -- a raw key/value dump of every strategy YAML @970aabf
- ⚠️ `memory/MEMORY_ARCHIVE_2026H1.md` -- a core memory file, excluded because it carries the PC's REAL Telegram channel ID; the approved redaction method runs where the value lives on the VM and cannot apply to a PC-held value. Add back only with a decision on how to redact it.

## 6. EVERY exclusion, by name
**96 files, 49,151,431 bytes, not in this repository.**

| Class | Files | Bytes |
|---|---:|---:|
| log file / log capture | 13 | 35,222,093 |
| SQLite database copy (shadow DB main/WAL/SHM) | 3 | 7,459,976 |
| git bundle -- compressed repository history; content cannot be credential-scanned without unpacking | 4 | 3,741,393 |
| raw query / analysis output -- DATA (rows or statistics), not design (instruction D2) | 22 | 913,577 |
| CONTAINS A CREDENTIAL VALUE (the testing VM's Telegram channel ID, in raw alert rows) -- found by the VM-side value scan | 2 | 447,114 |
| alert copies (sentinel files and their listing) -- alert text, account tags | 15 | 326,323 |
| systemd journal capture (log) | 3 | 250,191 |
| raw query / analysis output that appears to document a CONTRACT -- left out PENDING RAMA (section 5) | 7 | 229,723 |
| data file (CSV/JSON/JSONL/HTML) -- log extracts, candles or would-be signals | 12 | 190,627 |
| session transcript excerpt -- raw tool output incl. DB reads (instruction D2) | 4 | 177,872 |
| CONTAINS A CREDENTIAL VALUE (the PC's real Telegram channel ID) -- memory file excluded | 6 | 152,277 |
| CONTAINS A CREDENTIAL VALUE (a real Telegram channel ID from the PC .env) -- found by the PC-side value scan | 3 | 30,128 |
| log content (at least half the lines are log lines) -- detected file by file | 2 | 10,137 |

### log file / log capture

| Path | Bytes |
|---|---:|
| `_preservation/2026-09-07_cleanup_archive/trading-system-evidence/2026-08-31/system_2026-08-31.log` | 7,323,615 |
| `_preservation/2026-09-07_cleanup_archive/trading-system-evidence/2026-08-31/window_15-00_to_15-25.log` | 95,653 |
| `_preservation/BASELINE_system_16-Sep-2026.log` | 16,798,379 |
| `_preservation/CRON_DRIFT_1800_APPENDED_BLOCK_17-Sep-2026__after_byte_12347__captured_2026-09-17T1800IST.log` | 921 |
| `_preservation/CRON_DRIFT_CHECK_LOG_trading-sbx__post-1800_17-Sep-2026__captured_2026-09-17T1800IST.log` | 13,268 |
| `_preservation/CRON_DRIFT_CHECK_LOG_trading-sbx__pre-1800_17-Sep-2026__captured_2026-09-17T1000IST.log` | 12,347 |
| `_preservation/CRON_OFFICER_LOG_trading-sbx__pre-1850_17-Sep-2026__captured_2026-09-17T1810IST.log` | 9,069 |
| `_preservation/EVALUATOR_CRONLOG_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1751IST.log` | 1,854 |
| `_preservation/FULLDAY_system_17-Sep-2026__captured_2026-09-17T1752IST.log` | 10,945,945 |
| `_preservation/GATE78_system_17-Sep-2026__captured_2026-09-17T0816IST.log` | 16,585 |
| `trading-system/docs/audit/gate_20aug2026/gate_runner.log` | 2,420 |
| `trading-system/docs/audit/gate_20aug2026/gate_runner_tiers.log` | 1,193 |
| `trading-system/docs/audit/gate_20aug2026/gate_runner_tiersR.log` | 844 |

### SQLite database copy (shadow DB main/WAL/SHM)

| Path | Bytes |
|---|---:|
| `_preservation/SR_SHADOW_DB_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1758IST__FILE_sr_shadow.db-shm.copy` | 32,768 |
| `_preservation/SR_SHADOW_DB_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1758IST__FILE_sr_shadow.db-wal.copy` | 4,412,552 |
| `_preservation/SR_SHADOW_DB_trading-sbx__post-1605_17-Sep-2026__captured_2026-09-17T1758IST__FILE_sr_shadow.db.copy` | 3,014,656 |

### git bundle -- compressed repository history; content cannot be credential-scanned without unpacking

| Path | Bytes |
|---|---:|
| `_preservation/2026-09-07_cleanup_archive/bundles/controlplane.bundle` | 32,917 |
| `_preservation/2026-09-07_cleanup_archive/bundles/main.bundle` | 2,677,025 |
| `_preservation/2026-09-07_cleanup_archive/bundles/n907.bundle` | 5,625 |
| `_preservation/2026-09-07_cleanup_archive/bundles/tiers.bundle` | 1,025,826 |

### raw query / analysis output -- DATA (rows or statistics), not design (instruction D2)

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/gtt_startup_v3.txt` | 1,599 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/orders_gtt_analytics.txt` | 2,264 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/screener_INDOCO_0902_1350_1420.txt` | 3,228 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/signals_rows.txt` | 66,001 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/sr_rows_full_INDOCO.txt` | 16,815 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/sr_rows_summary.txt` | 1,331 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/trades_rows.txt` | 1,507 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm_queries_out.txt` | 751,373 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a1_out.txt` | 2,641 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a2_out.txt` | 3,612 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a2b_out.txt` | 75 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a2d_out.txt` | 1,857 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a3b_out.txt` | 12,216 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a4_out.txt` | 8,736 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a5_out.txt` | 2,580 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a6_out.txt` | 1,797 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a7_out.txt` | 2,496 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/inv1_out.txt` | 6,052 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/twin_ev1_out.txt` | 18,692 |
| `trading-system/docs/audit/capture_10aug2026/A_db_capture.txt` | 5,343 |
| `trading-system/docs/audit/capture_10aug2026/B_orders_pnl.txt` | 2,548 |
| `trading-system/docs/audit/capture_10aug2026/C_orders_logs.txt` | 814 |

### CONTAINS A CREDENTIAL VALUE (the testing VM's Telegram channel ID, in raw alert rows) -- found by the VM-side value scan

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/session_outputs.txt` | 376,404 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/twin_ev2_out.txt` | 70,710 |

### alert copies (sentinel files and their listing) -- alert text, account tags

| Path | Bytes |
|---|---:|
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/_VM_LISTING_BEFORE.txt` | 1,391 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_083002_810f5739.delivered` | 56,911 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_091947_08fc0342.delivered` | 11,189 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_092002_6076b91a.delivered` | 32,665 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_150307_b9df7eac.delivered` | 469 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_150308_9f9e7263.delivered` | 304 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_180001_fc593422.delivered` | 865 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_184511_6b9c496f.delivered` | 7,130 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260916_185003_b8e215e4.delivered` | 53,139 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260917_083003_b47fb938.delivered` | 56,911 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260917_091947_a32d9097.delivered` | 11,189 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260917_092001_496452e4.delivered` | 32,662 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260917_180001_de4ecbfe.delivered` | 1,164 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260917_184511_12465676.delivered` | 7,198 |
| `_preservation/CRITICAL_ALERT_SENTINELS_trading-sbx_16-17-Sep-2026__captured_2026-09-17T1852IST/critical_alert_20260917_185002_30f2b30c.delivered` | 53,136 |

### systemd journal capture (log)

| Path | Bytes |
|---|---:|
| `_preservation/BASELINE_journal_trading-system_16-Sep-2026.txt` | 91,403 |
| `_preservation/FULLDAY_journal_trading-system_17-Sep-2026__captured_2026-09-17T1752IST.txt` | 157,324 |
| `_preservation/GATE78_journal_trading-system_17-Sep-2026__captured_2026-09-17T0816IST.txt` | 1,464 |

### raw query / analysis output that appears to document a CONTRACT -- left out PENDING RAMA (section 5)

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/field_scan_970aabf.txt` | 99,071 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/harness_s12_output.txt` | 1,041 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/schema_cov_screener.txt` | 70,096 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/yaml_table_970aabf.txt` | 3,667 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a2c_out.txt` | 2,244 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a3_out.txt` | 4,505 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/agentD_yaml_dump.txt` | 49,099 |

### data file (CSV/JSON/JSONL/HTML) -- log extracts, candles or would-be signals

| Path | Bytes |
|---|---:|
| `_preservation/CALIBRATION_bootwindow_2026-09-15.jsonl` | 13,828 |
| `_preservation/CALIBRATION_bootwindow_2026-09-16.jsonl` | 13,617 |
| `_preservation/CALIBRATION_eodwindow_2026-09-15.jsonl` | 9,599 |
| `_preservation/CRON_DRIFT_PREDICTION_content_drift_offline_result_17-Sep-2026T1000IST.json` | 2,126 |
| `_preservation/GATE78_bootwindow_17-Sep-2026__from_capture_0816IST.jsonl` | 14,380 |
| `_preservation/GATE78_posctl_sim_success_reordered_2026-09-17.jsonl` | 13,955 |
| `_preservation/NORMALIZER_TEST_INPUT_anchored_family_2026-09-16.jsonl` | 13,743 |
| `_preservation/NORMALIZER_TEST_INPUT_corrupt_lines_2026-09-16.jsonl` | 13,650 |
| `_preservation/NORMALIZER_TEST_INPUT_sim_failed_2026-09-16.jsonl` | 13,617 |
| `_preservation/NORMALIZER_TEST_INPUT_sim_success_2026-09-16.jsonl` | 13,955 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/INDOCO_1m_candlestore.csv` | 66,371 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/v3_would_be_INDOCO_0902.jsonl` | 1,786 |

### session transcript excerpt -- raw tool output incl. DB reads (instruction D2)

| Path | Bytes |
|---|---:|
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__text_after_1955IST.txt` | 78,022 |
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__tools_SLAB_2237-2240IST.txt` | 14,222 |
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__tools_SLIPPAGE_ANCHOR_2121-2124IST.txt` | 17,607 |
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__tools_SLIPPAGE_DEEP_2036-2043IST.txt` | 68,021 |

### CONTAINS A CREDENTIAL VALUE (the PC's real Telegram channel ID) -- memory file excluded

| Path | Bytes |
|---|---:|
| `memory/MEMORY_ARCHIVE_2026H1.md` | 48,520 |
| `memory/memory_snapshots/MEMORY_2026-07-23_pre_compaction.md` | 20,733 |
| `memory/memory_snapshots/memory_snapshot_2026-07-24_194144_precompaction/MEMORY.md` | 20,890 |
| `memory/memory_snapshots/memory_snapshot_2026-07-25_presplit/MEMORY_ARCHIVE_2026H1.md` | 57,392 |
| `memory/project_20260518_deployment_verification.md` | 3,738 |
| `memory/project_telegram_recreate_20260428.md` | 1,004 |

### CONTAINS A CREDENTIAL VALUE (a real Telegram channel ID from the PC .env) -- found by the PC-side value scan

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/attribution_gloss_sweep_21jul2026.md` | 15,662 |
| `trading-system/docs/audit/backup_retention_and_telegram_delivery_22jul2026.md` | 6,609 |
| `trading-system/docs/audit/gemini_watchman_alerts_21jul2026.md` | 7,857 |

### log content (at least half the lines are log lines) -- detected file by file

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/twin_ev3_out.txt` | 5,202 |
| `trading-system/docs/audit/capture_10aug2026/D_boot_logs.txt` | 4,935 |

