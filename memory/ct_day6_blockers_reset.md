---
name: ct-day6-blockers-reset
description: "Day 6 crash test TEMP config: all risk limits maxed for CT159 (11-Jun-2026)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b860701-6391-4408-be2a-86ea2bdeaf60
---

All risk limits set to max for Day 6 crash test (11-Jun-2026, 08:45 IST):
- max_daily_trades: 9999
- max_consecutive_losses: 9999
- daily_loss_limit: 9999999
- daily_loss_limit_pct: 1.0 (100% — schema enforces ≤1.0)
- min_pass_score: 30

System restarted, healthy, kill switch INACTIVE, 0 open trades/orders.

**Why:** Days 1-5 hit daily trade/loss limits that interrupted test execution. Maxing limits prevents premature test termination.

**How to apply:** Revert ALL to production values after CT159: max_daily_trades=20, max_consecutive_losses=4, daily_loss_limit=10000, daily_loss_limit_pct=0.05, min_pass_score=60.

Related: [[ct-day5-complete]]
