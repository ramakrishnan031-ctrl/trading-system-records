---
name: F.1 ops readiness landed (19-Apr-2026, commit 316b335)
description: Phase F.1 operational-readiness commit — systemd/logrotate/cron canonicalized, DEPLOYMENT.md runbook, EF-7 paper-capital consistency check, paper_capital 5M→50k (H-26), quote bucket 3/3 (H-24); 1654 green; Phase A 15/15; FUTURE-1 deferred
type: project
originSessionId: daf7a7d0-49f5-49f6-8f12-9791b8824592
---
F.1 / commit 316b335 on main — operational readiness for Monday 2026-04-21 paper trial.

**Why:** Paper trial starts Mon 21-Apr. Needed one bundled ops commit so VM deploy happens from committed artifacts (not ad-hoc copies), and so a paper-capital regression guard exists post-E.7 setter consolidation.

**What landed:**
- `deploy/systemd/trading-system.service` + `alert-watcher.service` — canonicalized from `docs/web_claude/05_deployment/step3_systemd_and_firewall.txt`; repo is source of truth.
- `deploy/logrotate/trading-system` — retention-only (maxage 30), no rotate/compress — Python RotatingFileHandler owns rotation; `copytruncate` avoided (races).
- `deploy/cron/trading-system.cron` — 01:00 IST `sqlite3 .backup`, 02:00 IST 7-day cleanup, 05:00 IST Mon-Fri token wipe, 18:00 IST Sunday `refresh_instruments.py --account LFL836`.
- `scripts/copy_token_to_vm.bat` — `git mv`-ed from repo root.
- `DEPLOYMENT.md` — F.1 runbook: pre-deploy diff commands (MANDATORY), deploy sequence, rollback table, FUTURE-1 note.
- `reports/daily_review.py` — fixed latent bug: `--db` default `data/trading.db` → `data_store/trading_system.db`; new `--unattended` flag (silences stdout); `generate()` exception → stderr + exit 2.
- `utils/startup_checks.py` — new `StartupCheckFailed` exception + `check_paper_capital_consistency(fm, adapter, is_paper, logger, tolerance=0.01)`. Paper-only. Greps on `EF7_STARTUP_CHECK_DIVERGENCE`.
- `main.py` — calls EF-7 check after `fund_manager.initialize`; divergence logs CRITICAL + `return 3`.
- `config/accounts.csv` — `LFL836.paper_capital` 5_000_000 → 50_000 (H-26: match live Day-1 capital for calibration parity).
- `config/broker_limits.yaml` — `quote.burst/rate_per_sec` 1/1 → 3/3 (H-24: relax under burst).
- `docs/web_claude/03_audit_responses/extra_findings.md` — FUTURE-1 filed (auto-start on token arrival deferred; three variants — `.path`, `.timer`, manual).

**How to apply:**
- Don't push systemd files to VM out-of-band; run the pre-deploy diff block in DEPLOYMENT.md §2 first.
- EF-7 divergence in fixtures: test mocks must set both `adapter.get_margins().net` and `fund_manager.total` to the same numeric value. `test_main.py::_make_all_patches` already aligns both to 50_000.0; tests that override `FundManager` must set `fm_mock.total` too.
- `reports/daily_review.py --unattended` is what the Day-1 cron/post-market runs expect; omit to see stdout.
- FUTURE-1 decision (auto-start variant) should wait for Week 1 operational observations.

**Test delta:** 1649 → 1654 (5 new F.1 tests: 3 EF-7 in test_startup_checks.py, 1 accounts.csv value in test_account_registry.py, 1 daily_review generate-exception in test_daily_review.py).

**Baseline:** 1654 collected, 1654 green. Phase A integration gate 15/15.
