---
name: crash-test-temp-max-trades-500
description: "TEMP: max_daily_trades set to 500 for Day 5 crash test. Revert to 20 before paper trading."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

max_daily_trades set to 500 TEMP for Day 5 completion (2026-06-10). Revert to 20 before paper trading begins.

**Why:** Daily limit of 20 was hit by 11:00 IST on Day 5, blocking CT140, CT143, CT159.
**How to apply:** After all Day 5 tests complete (or at latest before paper trading):
```
ssh trading-vm "sed -i 's/max_daily_trades: 500.*$/max_daily_trades: 20        # hard cap on new trades per day (>= 1)/' ~/systems/trading-system/config/system_config.yaml"
```
Also revert local config/system_config.yaml.
