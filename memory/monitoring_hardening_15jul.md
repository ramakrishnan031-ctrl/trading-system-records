---
name: monitoring-hardening-15jul
description: "15-Jul-2026 monitoring-hardening build (F1-F4 + canary + deploy-gate + prevention checklist) — closes the two silent-failure classes from the health audit. Branch, UNPUSHED."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5e0da463-297c-4dc3-bb3f-4db09f2c57a7
---

**15-Jul-2026 MONITORING HARDENING — BUILT + tested; closes the two silent-failure CLASSES from the health audit ([[system-health-audit-15jul]]).** Branch **`monitoring-hardening-15jul`** off `main`@`0a77c92` (8 commits, tip **`1c891b6`**), **UNPUSHED, schema-free, test-first, paper==live.** Report `docs/audit/monitoring_hardening_15jul2026.md`. ChatGPT+WebClaude-approved. **PC main `0a77c92` unchanged; VM==bare `2dc69d5`.** (Second unpushed code branch alongside [[fixes-15jul]] `fixes-eodcleanup-…`@`0c7a6dd`.)

**PHASE-0 (read-only, STOP-GATE=PROCEED):** paradox resolved — the "535 since 18-Jun" was TWO clusters (64 on 18-Jun brief/recovered + 4,745 on 15-Jul loop), NOTHING 19-Jun→14-Jul; `.delivered` writes only on real `sendmail` success (`alert_watcher.py:422/471`) so 19-Jun–14-Jul deliveries were genuine; credential died overnight (first 535 15-Jul 03:20). Watcher is EMAIL-ONLY (no secondary channel). `cron_heartbeat` is schema-versioned (table 28) with a free-form `message` col → F2 functional status fits there with NO schema change (a column was not an option). No design fork.

**F1 `c405c30` alert_watcher (Architecture+Monitoring):** ROOT CAUSE = on SMTP auth failure `run_once` `return 2` → systemd Restart=always/10s crash-loop; email-only → sentinels unrecoverable (CLASS 2). FIX: never exit non-zero on a delivery fault; **TELEGRAM FALLBACK** (`TelegramNotifier.from_env` + `.send(write_sentinel=False)` → `mark_delivered`); time-based backoff (60s×2ⁿ cap 1800s) skips dead SMTP; **`data_store/alert_watcher_degraded.json`** degraded marker (written on failure, cleared on recovery). Tests `TestF1SmtpRobustness` (3) + updated `test_smtp_auth_error_no_longer_crashes`; 38 pass.

**F2 `795a417` EXECUTION vs FUNCTIONAL (Architecture/systemic):** ROOT CAUSE (CLASS 1) = one heartbeat SUCCESS regardless of real function/delivery. FIX: EXECUTION in `status` col (unchanged); FUNCTIONAL encoded in the `message` col as `[func=<STATUS>]` (NO schema change). `record_heartbeat`/`HeartbeatTimer` +`functional_status`; `parse_functional_status` reader. Applied to `generate_screened_csv` (`_cron_main` → CSV-artifact check OK/EMPTY_NO_DATA/FAILED). **Cron Officer `build_eod_summary` surfaces (a) per-job functional issues + (b) the F1 email-degraded marker** → a dead SMTP is VISIBLE even when execution is green. Tests `test_f2_functional_status` (4); officer 39. Heartbeat_db-job tail enumerated in the report (incremental fast-follow, one line each).

**F3 `d960760` check_cron_drift (Monitoring):** ROOT CAUSE = PASS 1 checked heartbeats for EVERY monitored job, but exit_code_file jobs (preflight_phase_a/b/c, sr_detector_backfill) write MARKERS → standing daily FALSE 'no heartbeat in 24h'. FIX: dispatch by `effective_detection_method`, reusing the Officer's `_read_marker` (markers for exit_code_file). Tests `test_f3_cron_drift_markers` (2).

**F4 `5311fe6`+`e57fdac` hygiene (Operational):** purge stale `officer.telegram_ban_until:'2026-06-23'`→null; date-embed `alert_watcher_<date>.log` (Foundation Rule 1.7, NOT RotatingFileHandler; cleaned by log_cleanup). Tests `test_f4_hygiene` + updated `test_log_file_created` + `test_officer_config_eod_time_and_ban`.

**CANARY `11520b4` (Architecture/P-3):** `scripts/monitoring_canary.py` daily 08:20 — probes EMAIL(SMTP login)/TELEGRAM(getMe)/SENTINEL(F1 marker+backlog)/DASHBOARD(systemctl); QUIET healthy, LOUD broken (Telegram WARNING → CRITICAL sentinel fallback riding F1); records execution+F2 functional. **Email probe FAILS until F0 — that IS the canary working.** Satisfies all 7 checklist items. Registered in cron_registry (regenerated crontab). Tests `test_monitoring_canary` (7).

**DEPLOY-GATE `66cb182` + CHECKLIST:** `scripts/deploy_assert.py` blocks a deploy ONLY on BLOCKER class (DB `quick_check`/`foreign_key_check`/schema parity; read-only mode=ro); monitoring=WARN, never blocks. `docs/monitoring_prevention_checklist.md` = the 7 items every new cron/service needs (functional criterion·health-check·alert path·fallback·regression test·owner·monitoring class), referenced from SYSTEM_MAP. Tests `test_deploy_assert` (3).

**Full touched-suite green; 5,068-test collect clean. Nothing pushed/restarted.** **⏰ F0 (Rama, urgent ops — NOT this task): restore `ALERT_SMTP_PASSWORD`** (fresh Gmail app-password) → stops the loop + resumes email/sentinel delivery. Then deploy both code branches off-market. See [[system-health-audit-15jul]] · [[fixes-15jul]] · [[unpushed-pending-deploy-ledger]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 1010 B (budget 300 B). The index now carries a hook and this link.

- 🛡️🔧 **[15-Jul MONITORING HARDENING BUILT (branch, UNPUSHED)](monitoring_hardening_15jul.md)** — closes the two silent-failure classes from the audit. Branch `monitoring-hardening-15jul`@`1c891b6` (off main `0a77c92`; 8 commits; schema-free, test-first). **F1** `c405c30` alert_watcher no-crash-loop + **TELEGRAM FALLBACK** + degraded marker (CLASS 2) · **F2** `795a417` EXECUTION vs FUNCTIONAL status (in the `message` col, NO schema; Cron Officer surfaces it + the email-degraded line — CLASS 1) · **F3** `d960760` cron-drift marker-aware · **F4** `5311fe6`/`e57fdac` purge stale ban + date-embed alert_watcher.log · **CANARY** `11520b4` daily 4-path self-test · **DEPLOY-GATE** `66cb182` (BLOCKER-only) · **CHECKLIST** 7-items `docs/monitoring_prevention_checklist.md`. Full touched-suite green; 5,068-collect clean. **PC main `0a77c92` unchanged; VM==bare `2dc69d5`.** ⏰ **F0 (Rama, urgent): restore `ALERT_SMTP_PASSWORD`.** [[monitoring-hardening-15jul]] [[system-health-audit-15jul]]
