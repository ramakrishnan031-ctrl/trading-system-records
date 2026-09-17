---
name: Alerts subsystem built and locked (CR1-CR10, TG1-TG12, AW1-AW11)
description: alerts/critical.py + alerts/telegram_notifier.py + scripts/alert_watcher.py; 89 tests + 4 integration; 678 total; G8 fully implemented
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
Module 24 (three sub-modules) build complete. All 678 cumulative tests green.

**Why:** G8 requires no single point of failure for CRITICAL alerts. Telegram is primary; sentinel+watcher is the guaranteed fallback even if the trading process crashes.

**How to apply:** Any code that must fire a CRITICAL alert should call
`TelegramNotifier.send("CRITICAL", ...)`. The notifier writes the sentinel first
(CR2 atomic write), then attempts Telegram. If both fail, the watcher picks up
the sentinel file on its next scheduled run and emails it.

## Files changed

- `alerts/__init__.py` (NEW): package marker
- `alerts/critical.py` (NEW): pure sentinel writer; CR1-CR10; no imports except stdlib
- `alerts/telegram_notifier.py` (NEW): TelegramNotifier class; TG1-TG12
- `scripts/__init__.py` (NEW): package marker
- `scripts/alert_watcher.py` (NEW): standalone CLI; AW1-AW11
- `tests/unit/test_critical.py` (NEW): 31 tests
- `tests/unit/test_telegram_notifier.py` (NEW): 31 tests
- `tests/unit/test_alert_watcher.py` (NEW): 23 tests
- `tests/integration/test_alerts_pipeline.py` (NEW): 4 integration tests
- `core/config_loader.py`: added SmtpConfig, TelegramConfig, AlertsConfig; SystemConfig.alerts field
- `config/system_config.yaml`: added alerts: section with telegram + smtp sub-sections
- `tests/unit/test_config_loader.py`: added AlertsConfig/TelegramConfig/SmtpConfig imports + test; 26->27 tests
- `docs/locked_decisions.yaml`: added CR1-CR10, TG1-TG12, AW1-AW11; total_decisions 60->93
- `data_store/.gitkeep` (NEW): ensures data_store/ exists in repo

## Test counts (post-Module 24)

| Suite | Count |
|---|---|
| test_critical.py | 31 |
| test_telegram_notifier.py | 31 |
| test_alert_watcher.py | 23 |
| test_config_loader.py | 27 (+1 alerts test) |
| test_alerts_pipeline.py (integration) | 4 |
| Total cumulative | 678 across 27 suites (23 unit + 3 new unit + 1 integration) |

## Key design decisions

- CR2: Atomic sentinel write (.tmp -> .flag via rename). 8 JSON fields. id = YYYYMMDD_HHMMSS_8hex
- CR5: Lifecycle: .flag -> .delivered (watcher success) or .failed (max attempts)
- TG4/TG5: CRITICAL sentinel written FIRST before Telegram attempt. If sentinel fails: log.error, try Telegram anyway.
- TG6: 429 -> sleep Retry-After (max 5s), retry once. 5xx -> exponential backoff. 4xx -> permanent fail.
- TG9: paper_mode skips HTTP but CRITICAL still writes sentinel (watcher integration tests work in paper mode)
- AW3: Lock file with pid. Live pid -> exit 0. Dead pid -> clean stale and proceed.
- AW5: Attempt counter in alert_watcher_attempts.json. Pruned after delivery/failure.
- AW9: Exit 0=ok, 1=config error, 2=SMTP auth failure.

## Deviations from spec

None. All CR/TG/AW decisions implemented as specified.
