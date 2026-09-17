---
name: task_8_config_guide
description: docs/CONFIG_GUIDE.md — Rama-facing plain-language reference for every config setting; read before touching any config
metadata: 
  node_type: memory
  type: project
  originSessionId: 34eb8dba-9799-4234-a8dc-bb8ca1411fa8
---

**TASK #8 DONE (2026-06-19):** Created `docs/CONFIG_GUIDE.md` — comprehensive
Rama-facing config reference so config can be tweaked daily without breaking things.

- 12 sections (Capital&Risk, Live Test Mode, Hours, Orders, Signals, Reconciliation/Safety,
  Alerts, Cron, DB/Storage, Health, Strategy/Signals, Override Precedence).
- **"Currently Effective Values" quick table at top** (mode, caps, loss limits, throttle, etc.).
- **Override Precedence** (the critical section): `live_test_mode` (4/6) > base risk caps (5/20);
  dual daily-loss = pct pre-trade+unrealised vs absolute ₹300 post-close+realised
  ([[dual_daily_loss_mechanism]]); smallest sizing cap wins (concentration 10%/₹1k BINDS on ₹10k);
  `force_intraday_only` forces MIS; entry window = narrowest of global/per-strategy/cutoff.
- Common Scenarios (with edit+restart commands), Dangerous-Changes warnings, Quick Commands.

**Two non-obvious truths documented up front:** (1) `mode` paper/live is the `--mode` CLI flag
in the systemd `ExecStart`, **NOT a YAML key** (no `mode:` exists in system_config.yaml);
(2) every config edit needs a **restart** to take effect (deploy ≠ restart, see [[deploy_requires_restart]]).

Cross-referenced from `docs/SYSTEM_MAP.md` (Related Docs + Changelog). Docs-only.
Commit **3fa0b4d**; pushed→deployed→verified on VM (34 KB).
Read this before recommending any config change. Related: [[live_test_mode_permanent]],
[[capital_sizing_audit_18jun]], [[task_10_telegram_master_switch]].
