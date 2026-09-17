# 03-A - APPENDIX TO CHAPTER 03: the declared schedule, the units, and the deploy hook

> **Evidence basis.** `config/cron_registry.yaml` and `deploy/cron/trading-system.cron` read from the worktree `D:/Projects/wt-sr-shadow-15sep` (commit `e7bf477` plus the `force_qty` working-tree change). The machine columns are RECORD-DERIVED from the captures preserved in `trading-system-sbx-snapshot/_machine/` (testing VM, 17-Sep-2026 20:06 IST). **Production was never read.** Evidence date: 18-Sep-2026.
> Every count in these tables was produced by parsing the files, not by reading prose. Chapter 03 narrates what they mean.

### T1 - the 47 registry jobs (source of truth: `config/cron_registry.yaml`)

| # | Job id | Registry line | Schedule (declared) | cron expression | Type | Critical | Monitored | Market-day only | Runs | Log target |
|---:|---|---:|---|---|---|---|---|---|---|---|
| 1 | `disk_monitor` | 183 | hourly | `0 * * * *` | python | no | no | no | `scripts/disk_monitor.py` | `logs/cron-disk-monitor.log` |
| 2 | `log_cleanup` | 8 | 00:00 daily | `0 0 * * *` | shell | no | no | no | `find (shell)` | `none` |
| 3 | `db_backup` | 22 | 01:00 daily | `0 1 * * *` | shell | yes | no | no | `sqlite3 (shell)` | `logs/cron-db-backup.log` |
| 4 | `analytics_backup` | 37 | 01:05 daily | `5 1 * * *` | shell | yes | no | no | `sqlite3 (shell)` | `logs/cron-db-backup.log` |
| 5 | `evidence_backup` | 67 | 01:10 daily | `10 1 * * *` | python | no | yes | no | `scripts/backup_evidence.py` | `logs/cron-evidence-backup.log` |
| 6 | `backup_retention` | 52 | 02:00 daily | `0 2 * * *` | python | no | yes | no | `scripts/backup_retention.py` | `logs/cron-backup-retention.log` |
| 7 | `sentinel_retention` | 82 | 02:05 daily | `5 2 * * *` | shell | no | no | no | `find (shell)` | `logs/cron-sentinel-retention.log` |
| 8 | `output_retention` | 97 | 02:10 daily | `10 2 * * *` | python | no | yes | no | `scripts/output_retention.py` | `logs/cron-output-retention.log` |
| 9 | `db_retention` | 125 | 02:30 daily | `30 2 * * 1-6` | python | no | no | no | `scripts/db_retention.py` | `logs/cron-db-retention.log` |
| 10 | `db_retention_vacuum` | 140 | 02:30 daily | `30 2 * * 0` | python | no | no | no | `scripts/db_retention.py` | `logs/cron-db-retention.log` |
| 11 | `backup_restore_drill` | 742 | 03:00 1st-of-month | `0 3 1 * *` | python | no | yes | no | `scripts/backup_restore_drill.py` | `logs/cron-backup-drill.log` |
| 12 | `token_cleanup` | 155 | 05:00 daily | `0 5 * * *` | shell | no | no | no | `rm (shell)` | `none` |
| 13 | `auto_refresh_token` | 198 | 08:15 Mon-Fri | `15 8 * * 1-5` | python | yes | yes | yes | `scripts/auto_refresh_token.py` | `logs/cron-auto-token.log` |
| 14 | `monitoring_canary` | 212 | 08:20 daily | `20 8 * * *` | python | no | yes | no | `scripts/monitoring_canary.py` | `logs/cron-monitoring-canary.log` |
| 15 | `preflight_phase_a` | 230 | 08:30 Mon-Fri | `30 8 * * 1-5` | python | no | yes | yes | `scripts.preflight.orchestrator` | `logs/preflight.log` |
| 16 | `fetch_fno_ban` | 278 | 08:35 Mon-Fri | `35 8 * * 1-5` | python | no | yes | yes | `scripts/fetch_fno_ban.py` | `logs/cron-fno-ban.log` |
| 17 | `gemini_premarket_brief` | 292 | 08:55 Mon-Fri | `55 8 * * 1-5` | python | no | yes | yes | `scripts/gemini_premarket_brief.py` | `logs/cron-premarket-brief.log` |
| 18 | `capture_metrics` | 320 | */5 09-15 Mon-Fri | `*/5 9-15 * * 1-5` | python | no | no | yes | `scripts/capture_metrics_baseline.py` | `logs/cron-metrics.log` |
| 19 | `liveness_probe` | 335 | */5 09-15 Mon-Fri | `*/5 9-15 * * 1-5` | python | no | no | yes | `scripts/liveness_probe.py` | `logs/cron-liveness.log` |
| 20 | `refresh_instruments` | 306 | 09:00 Mon-Fri | `0 9 * * 1-5` | python | yes | yes | yes | `scripts/refresh_instruments.py` | `logs/cron-refresh-instruments.log` |
| 21 | `preflight_phase_b` | 246 | 09:14 Mon-Fri | `14 9 * * 1-5` | python | no | yes | yes | `scripts.preflight.orchestrator` | `logs/preflight.log` |
| 22 | `preflight_phase_c` | 262 | 09:15 Mon-Fri | `15 9 * * 1-5` | python | no | yes | yes | `scripts.preflight.orchestrator` | `logs/preflight.log` |
| 23 | `cron_officer_briefing` | 169 | 09:20 daily | `20 9 * * *` | python | yes | yes | no | `scripts/cron_officer.py` | `logs/cron-officer.log` |
| 24 | `fetch_daily_candles` | 359 | 15:40 Mon-Fri | `40 15 * * 1-5` | python | no | yes | yes | `scripts/fetch_daily_candles.py` | `logs/cron-candle-fetch.log` |
| 25 | `reconcile_positions` | 439 | 15:45 Mon-Fri | `45 15 * * 1-5` | python | yes | yes | yes | `scripts/reconcile_positions.py` | `logs/cron-reconcile-positions.log` |
| 26 | `eod_cleanup` | 453 | 15:50 Mon-Fri | `50 15 * * 1-5` | python | no | yes | yes | `scripts/eod_cleanup.py` | `logs/cron-eod-cleanup.log` |
| 27 | `reconstruct_excursions` | 374 | 15:50 Mon-Fri | `50 15 * * 1-5` | python | no | yes | yes | `scripts/reconstruct_excursions.py` | `logs/cron-excursions.log` |
| 28 | `eod_verify` | 467 | 15:55 Mon-Fri | `55 15 * * 1-5` | python | yes | yes | yes | `scripts/eod_verify.py` | `logs/cron-eod-verify.log` |
| 29 | `eod_broker_reconcile` | 485 | 15:58 Mon-Fri | `58 15 * * 1-5` | python | yes | yes | yes | `scripts/eod_broker_reconcile.py` | `logs/cron-eod-broker-reconcile.log` |
| 30 | `sr_detector_backfill` | 408 | 15:58 Mon-Fri | `58 15 * * 1-5` | python | no | yes | yes | `scripts/sr_detector_backfill.py` | `logs/cron-sr-detector-backfill.log` |
| 31 | `wal_checkpoint` | 502 | 16:00 Mon-Fri | `0 16 * * 1-5` | python | no | yes | yes | `scripts/wal_checkpoint.py` | `logs/wal_checkpoint.log` |
| 32 | `generate_screened_csv` | 516 | 16:01 Mon-Fri | `1 16 * * 1-5` | python | no | yes | yes | `scripts/generate_screened_stocks_csv.py` | `logs/cron-screened-stocks.log` |
| 33 | `daily_report` **(disabled)** | 542 | 16:05 Mon-Fri | `5 16 * * 1-5` | python | no | no | yes | `reports.daily_report` | `logs/daily_report.log` |
| 34 | `daily_trade_review` | 561 | 16:07 Mon-Fri | `7 16 * * 1-5` | python | no | yes | yes | `reports/daily_trade_review.py` | `logs/cron-daily-trade-review.log` |
| 35 | `trade_journal` | 575 | 16:10 Mon-Fri | `10 16 * * 1-5` | python | no | yes | yes | `scripts/trade_journal.py` | `logs/trade_journal.log` |
| 36 | `compute_strategy_metrics` | 589 | 16:15 Mon-Fri | `15 16 * * 1-5` | python | no | yes | yes | `scripts/compute_strategy_metrics.py` | `logs/cron-strategy-metrics.log` |
| 37 | `metrics_summary` | 603 | 16:16 Mon-Fri | `16 16 * * 1-5` | python | no | no | yes | `scripts/capture_metrics_baseline.py` | `logs/cron-metrics.log` |
| 38 | `gemini_log_review` | 641 | 16:20 Mon-Fri | `20 16 * * 1-5` | python | no | yes | yes | `scripts/gemini_log_review.py` | `logs/cron-gemini-review.log` |
| 39 | `strategy_registry_officer` | 626 | 16:22 Mon-Fri | `22 16 * * 1-5` | python | no | yes | yes | `scripts/strategy_registry_officer.py` | `logs/cron-strategy-registry.log` |
| 40 | `gemini_trade_coach` | 655 | 16:40 Mon-Fri | `40 16 * * 1-5` | python | no | yes | yes | `scripts/gemini_trade_coach.py` | `logs/cron-trade-coach.log` |
| 41 | `gemini_data_integrity_check` | 669 | 17:00 Mon-Fri | `0 17 * * 1-5` | python | no | yes | yes | `scripts/gemini_data_integrity_check.py` | `logs/cron-data-integrity.log` |
| 42 | `control_tower` | 424 | 17:05 Mon-Fri | `5 17 * * 1-5` | python | no | yes | yes | `ops/control_tower/runner.py` | `logs/cron-control-tower.log` |
| 43 | `check_cron_drift` | 683 | 18:00 Mon-Fri | `0 18 * * 1-5` | python | no | no | yes | `scripts/check_cron_drift.py` | `logs/cron-drift-check.log` |
| 44 | `gemini_weekly_patterns` | 727 | 18:00 Sunday | `0 18 * * 0` | python | no | yes | no | `scripts/gemini_weekly_patterns.py` | `logs/cron-weekly-patterns.log` |
| 45 | `forward_shadow_record` | 389 | 18:15 Mon-Fri | `15 18 * * 1-5` | python | no | yes | yes | `scripts/forward_shadow_record.py` | `logs/cron-forward-shadow.log` |
| 46 | `system_manager_eod` | 713 | 18:45 Mon-Fri | `45 18 * * 1-5` | python | yes | yes | yes | `scripts/system_manager.py` | `logs/system-manager.log` |
| 47 | `cron_officer_eod` | 699 | 18:50 Mon-Fri | `50 18 * * 1-5` | python | no | yes | yes | `scripts/cron_officer.py` | `logs/cron-officer.log` |

**Totals (measured):** 47 jobs | 46 enabled, 1 disabled (`daily_report`) | 9 critical | 34 monitored | 32 market-day-only | 42 python, 5 shell | 22 carry a `marker_name`.

**Fields every job declares** (47/47 each): `script`, `schedule`, `type`, `critical`, `market_day_only`, `cadence`, `monitored`, `enabled`, `personal_tooling`, `cron_expression`, `command`, `env_wrapper`. `log_target` on 45, `marker_name` on 22, `detection_method` on 5, and one job each carries `excluded_reason`, `weekday`, `day_of_month`.

**The `officer` section** of the same file sets the Cron Officer's day window and thresholds: `day_window_start: 00:00`, `day_window_end: 23:59`, `morning_briefing_time: 09:20`, `eod_floor_time: 18:45`, `eod_gap_minutes: 5`, `miss_grace_minutes: 2`, `telegram_ban_until: None`.

### T2 - registry -> canonical -> live crontab: the arithmetic

| Artifact | What it is | Active entries | Notes |
|---|---|---:|---|
| `config/cron_registry.yaml` | the declared source of truth | 47 jobs | 46 enabled |
| `deploy/cron/trading-system.cron` | the generated canonical crontab, in git | 46 | 0 commented-out entries; the 5 `gemini_*` jobs are ACTIVE here |
| the machine's real `crontab -l` | RECORD-DERIVED capture, testing VM 17-Sep 20:06 IST | 42 | 5 entries commented out by hand (`# DISABLED 09-Sep-2026 (Rama)`), plus 1 hand-added job |

**The reconciliation, exactly:** 47 registry jobs - 1 disabled (`daily_report`) = **46** canonical entries. 46 canonical - 5 hand-commented `gemini_*` + 1 hand-added `sr_shadow_evaluate` = **42** live entries. Both identities hold on the measured counts.

**Therefore the daily drift check has two standing findings, by construction, not by failure:**

| Direction | Jobs | Why |
|---|---|---|
| in canonical, missing from live | `gemini_premarket_brief`, `gemini_log_review`, `gemini_trade_coach`, `gemini_data_integrity_check`, `gemini_weekly_patterns` | all five declare `enabled: true` and `monitored: true` in the registry, and all five are commented out in the live crontab with the note `DISABLED 09-Sep-2026 (Rama): AI tooling off on the testing VM` |
| in live, missing from canonical | `sr_shadow_evaluate` (`5 16 * * 1-5`) | hand-added on the testing VM only; the registry does not declare it, so the generator cannot emit it |

### T3 - systemd units: the repo versus the machine

The repository carries **7** unit files under `deploy/systemd/`. The machine capture shows **8** installed units. Installing a unit file is a manual act on the machine: a push does not do it (see T4).

| Unit | In the repo | Installed on the testing VM | Comparison |
|---|---|---|---|
| `alert-watcher.service` | yes | yes (captured) | identical |
| `cron-watchdog.service` | yes | yes (captured) | identical |
| `cron-watchdog.timer` | yes | yes (captured) | identical |
| `gui-dashboard.service` | **no** | yes (captured) | **installed but absent from the repository** |
| `security-watcher.service` | yes | yes (captured) | identical |
| `token-watcher.service` | yes | yes (captured) | identical |
| `trading-system.service` | yes | yes (captured) | **differs** (2 lines) + drop-in `watchman.conf` on the machine only |
| `trading-watchman.service` | yes | yes (captured) | **differs** (2 lines) |

### T4 - what a push actually does (`deploy/hooks/post-receive`, armed on the VM's bare repo)

| Line | Statement |
|---:|---|
| 28 | `while read -r oldrev newrev ref; do` |
| 29 | `if [ "$ref" = "refs/heads/$BRANCH" ]; then` |
| 30 | `echo "Deploying $BRANCH to $TARGET..."` |
| 31 | `git --work-tree="$TARGET" --git-dir="$GIT_DIR" checkout -f "$BRANCH"` |
| 32 | `cd "$TARGET" \|\| exit 1` |
| 34 | `if "$VENV_PY" scripts/generate_crontab.py --generate \| diff -q - deploy/cron/trading-system.cron >/dev/null 2>&1; then` |
| 35 | `crontab deploy/cron/trading-system.cron && echo "post-receive: crontab AUTO-INSTALLED from canonical."` |
| 36 | `else` |
| 38 | `fi` |
| 39 | `echo "Deployment complete."` |
| 40 | `fi` |

The hook is 41 lines. Its own header records that an earlier version of that header was false about which hook was armed, and that the file and the armed hook must stay byte-identical because that identity is the only proof of which hook is live.
