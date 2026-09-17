---
name: task-10-telegram-master-switch
description: Telegram alerts master ON/OFF switch — config key telegram.enabled; gate in TelegramNotifier.send()
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

TASK #10 DONE (18-Jun-2026): Telegram alerts master ON/OFF switch.

Config key: `alerts.telegram.enabled` (true/false) in config/system_config.yaml.
Default: **true** (ON — no behavior change on deploy day).

Gate is a SINGLE check at the top of `TelegramNotifier.send()` (alerts/telegram_notifier.py).
When `enabled=false` the notifier is a FULL silent no-op: no CRITICAL sentinel, no HTTP,
no failed_alerts.log write. Returns `SendResult(success=True, delivered_to=[])`.

Plumbing: `TelegramConfig.enabled` (core/config_loader.py) → `TelegramNotifier(enabled=...)`
constructor arg → wired in main.py Phase 0e (`enabled=tg_cfg.enabled`). Shared config means it
applies to BOTH paper and live equally. NOT per-alert-type toggles (that was deliberately out of scope).

Commit: 1af6124. Deployed to VM (config line 149 shows `enabled: true`). 6 new tests in
test_telegram_notifier.py::TestMasterSwitch; full suite green.

**Item A (commit 40a37b2, 18-Jun-2026):** closed the cron gap. `from_env()` and `from_config()`
now read `alerts.telegram.enabled` from system_config.yaml via module helper
`_read_telegram_enabled(config_dir)` and pass it to the constructor, so the master switch
silences ALL alerts (main app AND cron) — no exceptions. Cron scripts untouched (Option A).
FAIL-OPEN: missing/unreadable/garbage config → enabled=True (better to alert than silently skip).
Cron entries `cd` to project root so the relative `config/` path resolves. 6 new tests
(TestMasterSwitchFromEnv). NOTE: takes effect on next process start (deploy != restart).
