# SNAPSHOT_MANIFEST -- trading-system-records

> **THIS REPOSITORY IS A READ-ONLY SNAPSHOT OF PROJECT RECORDS. IT IS NEVER A DEPLOY TARGET.**
> It holds the records that describe BOTH machines (production and testing) and the project itself. They are kept here, not inside either machine's snapshot, so they never look like one machine's and never diverge into two copies.
> **Cloning on Windows needs `core.longpaths=true`** -- see `README.md`.

## 1. Source and time
- **Taken from the PC** (the operator's Windows workstation) by Claude Code (model `claude-opus-5[1m]`), 17-Sep-2026 (Thursday) IST, in three passes:
  - **~20:10-20:25 IST (commit 1):** `trading-system/docs/SYSTEM_MAP.md` <- `D:/Projects/trading-system/docs/SYSTEM_MAP.md` · `trading-system/PATHS.md` <- `D:/Projects/trading-system/PATHS.md` · `trading-system/docs/audit/` <- `D:/Projects/trading-system/docs/audit/` · `memory/MEMORY_RULES.md`, `memory/UNPUSHED_PENDING_DEPLOY_LEDGER.md` <- the Claude Code project memory directory · `_preservation/` <- `D:/Projects/_preservation/` (every preserved manifest).
  - **~20:45-20:50 IST (commit 2):** the rest of the project memory directory (`MEMORY.md`, `MEMORY_HAZARDS.md`, `MEMORY_BOARD.md`, `MEMORY_REFERENCE.md`, the notes, `fallback_instructions/`, `memory_snapshots/`) · raw query/analysis DATA and the transcript excerpts removed · `README.md`.
  - **~21:45-22:00 IST (commit 3):** the structure-versus-rows test applied to the seven contract-like outputs (4 IN, 3 OUT) · 6 memory files and 2 audit documents IN as PC-side-redacted copies (section 2b).
  - **18-Sep-2026 ~00:30-02:30 IST (commit 4):** `trading-system/docs/legacy_system_manual/` <- `D:/Projects/trading-system/docs/legacy_system_manual/` -- the first three chapters of the LEGACY SYSTEM MANUAL (the system is retired; this is a current-state record, not a repair plan), their two appendices, the status index, and the `_working/` evidence datasets those chapters were generated and verified from (section 7).
  - ⚠️ Files taken in an earlier pass were NOT refreshed in a later one (e.g. the ledger and `SYSTEM_MAP.md` have moved on since ~20:20 on the PC).
- **Contents:** 1364 files including this manifest (incl. `README.md`); 33,605,402 bytes before this manifest.

## 2. REDACTIONS -- the only bytes that differ from the PC originals
> ⚠️ **THE REDACTION IS COSMETIC.** It keeps a value out of THIS repository only. **The value still exists on the machines** (in the PC originals, the machines' configuration and elsewhere) -- dealing with that exposure is a separate task for the owner, ⛔ not something this snapshot does.

**The method, one principle for both locations:** redact a STAGING COPY -- never the original, never in place; byte-verify that ONLY the intended spans changed; the PC original stays untouched; every redaction logged here. The replacement runs WHERE THE VALUE LIVES, so it never travels: a value known only to the testing VM is replaced on the VM (2a); the PC's own value is replaced on the PC (2b).

### 2a. The testing VM's Telegram channel ID (one value, used for all three Telegram keys on that VM) -- replaced in memory on the testing VM; each replaced span verified to be a `-` + 13-digit ID

| File | Replacements | Committed copy md5 |
|---|---:|---|
| `memory/MEMORY_BOARD.md` | 1 | `5eacfa15ae2afac2205004b0bb29cfe7` |
| `memory/UNPUSHED_PENDING_DEPLOY_LEDGER.md` | 1 | `2ae8327fc477959268e3f2de61ac0f2e` |
| `trading-system/PATHS.md` | 2 | `73021dacbceb308c4691541b7f68662a` |
| `trading-system/docs/SYSTEM_MAP.md` | 2 | `1a5931d48dc3bbc0d4f3ed262238f276` |

### 2b. The PC's Telegram channel ID (from the PC's `.env`) -- replaced on the PC; each replaced span verified to be exactly that value; PC original md5 unchanged before and after

| File | Replacements | PC original md5 | Committed copy md5 |
|---|---:|---|---|
| `memory/MEMORY_ARCHIVE_2026H1.md` | 1 | `e399edf466e95b824ae7e4e1f40e9275` | `e7bacabd76dc0bb6cde65c9e9aa77261` |
| `memory/memory_snapshots/MEMORY_2026-07-23_pre_compaction.md` | 1 | `c28c68fdd1a81b6fe1c02442170a01d7` | `5cfde460b580f1edc5f23ccc733b6019` |
| `memory/memory_snapshots/memory_snapshot_2026-07-24_194144_precompaction/MEMORY.md` | 1 | `c26b161a9ab73dbd4dbec72801c1c86c` | `86f731777168459676cb02914e4c4f0b` |
| `memory/memory_snapshots/memory_snapshot_2026-07-25_presplit/MEMORY_ARCHIVE_2026H1.md` | 1 | `9ee7cc588f96df77b6512848b4e68f3c` | `e6b2870b6fbc46b46135fd67a271575d` |
| `memory/project_20260518_deployment_verification.md` | 1 | `8a629dc76b2ffe7306c6bcd220c96e4e` | `ddf7671fe5e87d0317fbceb67d3d555e` |
| `memory/project_telegram_recreate_20260428.md` | 1 | `c45189e91d8771197821fba4cdf057d4` | `21c4e0f969a4e99ea22544a57a78749a` |
| `trading-system/docs/audit/attribution_gloss_sweep_21jul2026.md` | 1 | `0c3decf623355fbaaeca3dac1202a265` | `c001e0f599a1949fd6333b40d97eae0f` |
| `trading-system/docs/audit/backup_retention_and_telegram_delivery_22jul2026.md` | 3 | `d66854f9a9e27cca5d3604de595cb6be` | `1e7379ffcdf1ea047bbe227ef47a0512` |

## 3. Deliberately NOT included
- `docs/` outside `docs/audit/`, `docs/legacy_system_manual/` and `SYSTEM_MAP.md` (e.g. `docs/decisions/`, the live `MASTER_PENDING` register -- preserved copies of the register ARE in `_preservation/`). **AMENDED 18-Sep-2026:** `docs/legacy_system_manual/` is now INCLUDED -- it is the manual itself, written as records.

## 4. Credential scan -- values never printed
- **PC-side:** 12 distinct secret values from the PC's `.env`; shape rules G1-G5; `.docx`/zip members decompressed; set equality and sha256 of every staged file against its source.
- **VM-side (in memory on the testing VM, via a tar stream):** 25 distinct secret values from the VM's `.env`, two pre-rotation `.env` backups, the Zerodha session file, the GUI secret key, and values harvested from `/home/ubuntu/.gemini`.
- **Value-independent rules:** G7 unquoted key/value secrets and G8 bare token shapes -- every candidate reviewed by value SHAPE; a content-based log detector for text files.
- **Positive controls -- all fired.** **Kept, adjudicated:** files matching only PLACEHOLDER values (a 15-character uppercase placeholder for accounts D351962 / ZA004 / ZA005; a placeholder secondary Telegram channel); the alert e-mail address (an identifier, not a secret).
- **Limits:** the PRODUCTION VM's `.env` was not read -- a credential existing ONLY there is covered by the shape rules alone. `.bundle` files were not unpacked and are excluded.

## 5. The structure-versus-rows test (commit 3) -- applied to all seven contract-like outputs
**The test:** IN if the file describes STRUCTURE (schemas, field names, config keys, YAML tables, formulas, score definitions); OUT if it contains ROWS keyed to a symbol, date, price, quantity, order id or P&L; OUT if ambiguous or mixed (a rebuild needs the shape, never the sample).

| File | Verdict | Why |
|---|---|---|
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/field_scan_970aabf.txt` | ✅ IN | STRUCTURE -- source-code lines naming each StrategyConfig field -- no data rows (its dated comments, default values and the `lot_size("TCS")` docstring example are code) |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/yaml_table_970aabf.txt` | ✅ IN | STRUCTURE -- a table of every strategy YAML's configuration keys and values |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a2c_out.txt` | ✅ IN | STRUCTURE -- the score formula's combination table (which step values can reach 60) |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/agentD_yaml_dump.txt` | ✅ IN | STRUCTURE -- a key/value dump of every strategy YAML -- no symbol lists or overrides |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/schema_cov_screener.txt` | ⛔ OUT | MIXED -- the DB schema DDL plus ~101 screener rows keyed to signal ids, symbols and timestamps |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/harness_s12_output.txt` | ⛔ OUT | ROWS -- recorded production zone prices and distances for one symbol (INDOCO) |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a3_out.txt` | ⛔ OUT | MIXED -- table column lists plus per-date request counts |

**The three audit documents carrying the PC's channel ID** -- redact-and-include only where the file's value justifies it: `attribution_gloss_sweep_21jul2026.md` (a failure-mode analysis: cause and prevention) ✅ IN, redacted · `backup_retention_and_telegram_delivery_22jul2026.md` (an incident investigation) ✅ IN, redacted · `gemini_watchman_alerts_21jul2026.md` (a point-in-time verification of one day's alerts) ⛔ OUT.

## 6. EVERY exclusion, by name
**84 files, 48,822,802 bytes, not in this repository.**

| Class | Files | Bytes |
|---|---:|---:|
| log file / log capture | 13 | 35,222,093 |
| SQLite database copy (shadow DB main/WAL/SHM) | 3 | 7,459,976 |
| git bundle -- compressed repository history; content cannot be credential-scanned without unpacking | 4 | 3,741,393 |
| raw query / analysis output -- DATA (rows or statistics), not design | 22 | 913,577 |
| CONTAINS A CREDENTIAL VALUE (the testing VM's Telegram channel ID, in raw alert rows) -- found by the VM-side value scan | 2 | 447,114 |
| alert copies (sentinel files and their listing) -- alert text, account tags | 15 | 326,323 |
| systemd journal capture (log) | 3 | 250,191 |
| data file (CSV/JSON/JSONL/HTML) -- log extracts, candles or would-be signals | 12 | 190,627 |
| session transcript excerpt -- raw tool output incl. DB reads | 4 | 177,872 |
| OUT by the structure-versus-rows test (section 5) -- rows or mixed | 3 | 75,642 |
| log content (at least half the lines are log lines) -- detected file by file | 2 | 10,137 |
| CONTAINS A CREDENTIAL VALUE (the PC's real Telegram channel ID) -- a point-in-time audit output whose value does not justify a redacted inclusion | 1 | 7,857 |

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

### raw query / analysis output -- DATA (rows or statistics), not design

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

### session transcript excerpt -- raw tool output incl. DB reads

| Path | Bytes |
|---|---:|
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__text_after_1955IST.txt` | 78,022 |
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__tools_SLAB_2237-2240IST.txt` | 14,222 |
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__tools_SLIPPAGE_ANCHOR_2121-2124IST.txt` | 17,607 |
| `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__tools_SLIPPAGE_DEEP_2036-2043IST.txt` | 68,021 |

### OUT by the structure-versus-rows test (section 5) -- rows or mixed

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/harness_s12_output.txt` | 1,041 |
| `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/vm/schema_cov_screener.txt` | 70,096 |
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/a3_out.txt` | 4,505 |

### log content (at least half the lines are log lines) -- detected file by file

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/twin_ev3_out.txt` | 5,202 |
| `trading-system/docs/audit/capture_10aug2026/D_boot_logs.txt` | 4,935 |

### CONTAINS A CREDENTIAL VALUE (the PC's real Telegram channel ID) -- a point-in-time audit output whose value does not justify a redacted inclusion

| Path | Bytes |
|---|---:|
| `trading-system/docs/audit/gemini_watchman_alerts_21jul2026.md` | 7,857 |


## 7. The legacy system manual (added 18-Sep-2026)

`trading-system/docs/legacy_system_manual/` holds the manual for the retired trading system. Written from the PC worktree
`D:/Projects/wt-sr-shadow-15sep` (commit `e7bf477` plus the uncommitted `force_qty` change set, which is byte-equivalent to the
TESTING VM as delivered 17-Sep-2026 19:31 IST) and from the machine captures in the sbx snapshot. **Production was never read**;
every production statement in the manual is RECORD-DERIVED or NOT ESTABLISHED.

| File | Bytes | What it is |
|---|---:|---|
| `LEGACY_SYSTEM_MANUAL_INDEX.md` | 11,907 | status index for all 25 chapters, the measured scope, the evidence format, the verification accounting and the unresolved list |
| `01_SYSTEM_OVERVIEW.md` | 20,534 | the map: environments, modes, components, external systems, storage, the trading day, the trade path, the control planes, plus **Appendix 01-A** (the measured testing-VM divergences and the file-count reconciliation) |
| `02_REPOSITORY_AND_FILE_MAP.md` | 782,947 | an entry for each of the **200** runtime modules -- purpose, role, importers, imports, key symbols with definition lines, inputs, outputs, side effects, config keys, tables, log counts, unknowns -- plus every other module listed and marked NOT MAPPED |
| `03_STARTUP_RUNTIME_AND_SCHEDULER.md` | 35,778 | the boot sequence, config loading and validation, startup checks, exit codes and the restart policy, the token chain, the scheduler and its standing drift, the deploy hook, EOD square-off and process shutdown |
| `03A_CRON_REGISTRY_TABLE.md` | 12,377 | the 47 declared jobs, the registry -> canonical -> live reconciliation, the unit comparison and the hook, as generated tables |
| `_working/` (6 files) | 3,258,588 | the evidence the chapters were built from: the deterministic module dataset, the 200 verified research entries, the 480 verified sequence steps, the anchoring accounting, and **743 observations parked for chapter 22** |

**Credential scan for these files.** Every one was scanned against the 20 secret values in the PC's `.env` before the commit:
**0 value hits.** Shape rules (PEM blocks, bot-token and channel-id shapes, long opaque tokens, AWS and GitHub token shapes)
flagged 62 distinct tokens, every one adjudicated as a CamelCase Python class name from the class inventory -- code identifiers,
not credentials. Positive controls all fired (a real `.env` value embedded in text, a synthetic PEM, a synthetic bot token, a
synthetic channel id) and the clean control returned 0. The manual quotes environment-variable **names** only; no secret value
appears in it, by construction and by measurement.
