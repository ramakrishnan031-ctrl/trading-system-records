---
name: project-crash-test-temp-reverted
description: All 7 TEMP config values reverted to production thresholds for crash test (07-Jun-2026)
metadata: 
  node_type: memory
  type: project
  originSessionId: 6baefba5-fbd6-4be5-a6cf-cb04d7f1755c
---

All 7 TEMP values in config/system_config.yaml reverted to production thresholds (07-Jun-2026, commit 843d9dc):

| Config Key | TEMP Value | Production Value |
|---|---|---|
| capital.daily_loss_limit | 100000.0 | 10000.0 |
| risk.max_consecutive_losses | 20 | 4 |
| risk.daily_loss_limit_pct | 1.00 | 0.05 |
| order_reconciler.capital_drift_tolerance | 100000.0 | 50.0 |
| drift_handler.log_only_threshold_rs | 100000.0 | 250.0 |
| drift_handler.soft_kill_threshold_rs | 200000.0 | 1000.0 |
| drift_handler.hard_kill_threshold_rs | 500000.0 | 2500.0 |

**Why:** Crash test (Jun 8-12) must run with real production thresholds to validate safety nets actually fire under realistic conditions. TEMP values were raised during paper testing to avoid false kill switches.

**How to apply:** These are now the permanent values. Do NOT raise them again for convenience. If drift_handler fires in paper mode, fix the root cause (skip G3 in paper) rather than raising thresholds.
