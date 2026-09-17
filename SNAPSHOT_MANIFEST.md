# SNAPSHOT_MANIFEST -- trading-system-records

> **THIS REPOSITORY IS A READ-ONLY SNAPSHOT OF PROJECT RECORDS. IT IS NEVER A DEPLOY TARGET.**
> It holds the records that describe BOTH machines (production and testing) and the project itself -- the incidents, the amendments, the rules written after something broke. They are kept here, not inside either machine's snapshot, so they never look like one machine's and never diverge into two copies.

## 1. Source and time
- **Taken from the PC** (the operator's Windows workstation) on 17-Sep-2026 (Thursday), ~20:10-20:25 IST, by Claude Code (model `claude-opus-5[1m]`).
- **Layout -> source:**
  - `trading-system/docs/SYSTEM_MAP.md` <- `D:/Projects/trading-system/docs/SYSTEM_MAP.md`
  - `trading-system/PATHS.md` <- `D:/Projects/trading-system/PATHS.md`
  - `trading-system/docs/audit/` <- `D:/Projects/trading-system/docs/audit/`
  - `memory/MEMORY_RULES.md`, `memory/UNPUSHED_PENDING_DEPLOY_LEDGER.md` <- the Claude Code project memory directory for `D:/Projects/trading-system`
  - `_preservation/` <- `D:/Projects/_preservation/` (includes every preserved manifest)
- **Contents:** 587 files including this manifest; 26,708,147 bytes before this manifest. Every file is a byte copy of its source EXCEPT the redactions in section 2.

## 2. REDACTIONS -- the only bytes that differ from the PC originals
The testing VM's Telegram channel ID (one value, used for all three Telegram keys on that VM) appears in three core records. The instruction counts chat IDs as credentials, and dropping these three records would gut this repository, so the value was REPLACED by `<TELEGRAM_CHANNEL_ID_REDACTED>` in these copies only. The replacement ran in memory ON THE TESTING VM, so the value never reached the PC; a byte comparison then proved that only the marked spans differ and that each replaced span was a `-` + 13-digit channel ID. **The PC originals are unchanged.**

| File | Replacements | PC original md5 (at snapshot time) | Committed copy md5 |
|---|---:|---|---|
| `memory/UNPUSHED_PENDING_DEPLOY_LEDGER.md` | 1 | `4511c9f788c91af73ab40cf6c625cca8` | `2ae8327fc477959268e3f2de61ac0f2e` |
| `trading-system/PATHS.md` | 2 | `9ccaab6973d8ae562f8495cf97501323` | `73021dacbceb308c4691541b7f68662a` |
| `trading-system/docs/SYSTEM_MAP.md` | 2 | `5c6edbdea7eed01d1aa071e2469898f0` | `1a5931d48dc3bbc0d4f3ed262238f276` |

## 3. Deliberately NOT included (not requested -- say if they are wanted)
- The other project memory files: `MEMORY.md` (the auto-loaded index), `MEMORY_HAZARDS.md`, `MEMORY_BOARD.md`, `MEMORY_REFERENCE.md`, `MEMORY_ARCHIVE_2026H1.md`, and the individual memory notes.
- `docs/` outside `docs/audit/` and `SYSTEM_MAP.md` (e.g. `docs/decisions/`, the live `MASTER_PENDING` register -- preserved copies of the register ARE in `_preservation/`).

## 4. Credential scan -- values never printed
- **PC-side:** 12 distinct secret values from the PC's `.env`; shape rules G1-G5 (PEM private keys, Telegram bot tokens, GitHub/AWS/Slack tokens); `.docx`/zip members decompressed; set equality and sha256 of every staged file against its source.
- **VM-side (in memory on the testing VM, via a tar stream):** 25 distinct secret values from the VM's `.env`, two pre-rotation `.env` backups, the Zerodha session file, the GUI secret key, and values harvested from `/home/ubuntu/.gemini` (other accounts).
- **Value-independent rules:** G7 unquoted key/value secrets (44 candidate lines -- all code expressions, environment-variable NAMES such as `bot_token_env: TELEGRAM_BOT_TOKEN`, or placeholders); G8 bare token shapes (2 hits -- the same Oracle Cloud CLI profile/tenancy identifier, not a credential).
- **Content-based log detector** (a text file is a log if at least half its lines are log lines): 2 text files excluded as log content. Control: real log captures score 1.00, a test-run output and a scan output score 0.00.
- **Positive controls -- all fired:** each credential source detects its own values; synthetic PEM / Telegram / GitHub / assignment strings; a secret inside a zip member; a real value mid-text; G7 flags an unquoted `password_hash` + `totp_secret` and skips `${API_KEY}`; G8 flags a synthetic seed / secret / key and NOT an md5.
- **Results:** 5 files EXCLUDED for credential content (section 6); 5 redactions (section 2); files matching only PLACEHOLDER values kept (a 15-character uppercase placeholder configured for accounts D351962 / ZA004 / ZA005, and a placeholder secondary Telegram channel): `trading-system/PATHS.md` · `trading-system/docs/audit/audit_05jul2026.md` · `trading-system/docs/audit/c1_credential_exposure_inventory_02jul2026.md` · `trading-system/docs/audit/system_security_audit_02jul2026.md` · `trading-system/docs/audit/telegram_token_shadow_investigation_03jul2026.md`. The alert e-mail address (an identifier, not a secret) appears in `SYSTEM_MAP.md`, the ledger and the three preserved twin `system_config` YAMLs -- kept.
- **Limits:** the PRODUCTION VM's `.env` was not read (production access not yet approved) -- a credential existing ONLY there is covered by the shape rules alone. `.bundle` files were not unpacked and are excluded for that reason.
- **Flagged, included (the instruction's exclusion classes are FILES of databases/logs/data, not text records of queries):** raw query outputs under `trading-system/docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/` and `trading-system/docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/`, `trading-system/docs/audit/capture_10aug2026/A_db_capture.txt` and `B_orders_pnl.txt`, and the session transcript excerpts `_preservation/TRANSCRIPT_b4764d54_16-Sep-2026__*.txt` -- they may contain trade rows. Say if they should come out.

## 5. Kept although they are machine configuration
- `_preservation/TWIN_system_config_*.yaml` (three preserved versions of the testing VM's `config/system_config.yaml`) -- scanned clean apart from the alert e-mail address.

## 6. EVERY exclusion, by name
**57 files, 47,677,982 bytes, not in this repository.**

| Class | Files | Bytes |
|---|---:|---:|
| log file / log capture | 13 | 35,222,093 |
| SQLite database copy (shadow DB main/WAL/SHM) | 3 | 7,459,976 |
| git bundle -- compressed repository history; content cannot be credential-scanned without unpacking | 4 | 3,741,393 |
| CONTAINS A CREDENTIAL VALUE (the testing VM's Telegram channel ID, in raw alert rows) -- found by the VM-side value scan | 2 | 447,114 |
| alert copies (sentinel files and their listing) -- alert text, account tags | 15 | 326,323 |
| systemd journal capture (log) | 3 | 250,191 |
| data file (CSV/JSON/JSONL/HTML) -- log extracts, candles or would-be signals | 12 | 190,627 |
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

