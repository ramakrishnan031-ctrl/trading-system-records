---
name: task-11-drift-alert-interval
description: "CAPITAL_DRIFT repeat-alert cadence is now a fixed config interval (30 min), not exponential backoff"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

TASK #11 DONE (18-Jun-2026): capital drift alert repeat interval → fixed 30 min.

Config key: `order_reconciler.capital_drift_alert_interval_sec` = **1800** (30 min).
Placed under `order_reconciler:` (alongside `capital_drift_tolerance`) — that's where the G3
CAPITAL_DRIFT check lives and is wired — NOT under a new `capital:` section as the task text
suggested (cohesion + lowest risk; the task allowed a clear key name). Validator: >= 1.0.

Behavior: G3 CAPITAL_DRIFT (orders/order_reconciler.py) repeat alerts now use a SINGLE
fixed interval via new `_should_alert_capital_drift()`. First detection alerts immediately;
thereafter throttled to at most once per interval (poll-count based: round(interval_sec /
poll_interval_sec) cycles). Throttle resets when drift returns within tolerance
(`_last_capital_drift_alert_poll = None`), so a fresh drift re-alerts immediately.

IMPORTANT CONTEXT — the task premise was slightly off: drift was NEVER a flat "5 min". It used
the FIX-038 generic exponential backoff (immediate → +8 polls/2min → +32 polls/8min → +120
polls/30min cap), shared across all reconciler checks. TASK-11 replaced ONLY the CAPITAL_DRIFT
path with the fixed interval; other checks (POSITION_GREW etc.) keep the FIX-038 backoff
unchanged. The throttle gates both the Telegram alert AND the CapitalDriftDetected publish, but
kill escalation is unaffected because first detection always fires immediately, and escalation
tiers live in [[dual_daily_loss_mechanism]] / drift_handler thresholds, not the alert cadence.

Commit: 7f37bd7. Deployed to VM (config line 196; load check drift_interval=1800.0). Parity:
shared config → paper+live. Test test_fix038_capital_drift_uses_exponential_backoff was renamed/
rewritten to test_task11_capital_drift_fixed_30min_interval (+ resets_after_resolved). 132 tests
pass. Activates on next restart ([[deploy_requires_restart]]).
