---
name: ct-day3-prereqs
description: "Three fixes required before Day 3 crash test — eod-pre-alert crash, order-monitor PENDING→OPEN, CLOSED_MANUAL PnL variance"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

Fix before Day 3 starts:

1. **eod-pre-alert thread crash** — `is_trading_day` AttributeError in MarketWindows. Fixed in FIX-155c: changed to `is_trading_holiday(now)` with inverted logic.
2. **order-monitor InvalidTransitionError** on PENDING→OPEN orphan orders. Fixed in FIX-155c: auto-step through SUBMITTED + poll_cycle try/except resilience.
3. **CLOSED_MANUAL trades not included in trades PnL sum** — Rs 140.45 variance. FM ledger has 4 orphan cleanup releases (EMSLIMITED +226.50, NRBBEARING +63.60, NRBBEARING +65.35, SBIN -215.00) that sum to exactly the variance. These trades are CLOSED_MANUAL, not CLOSED, so `SUM(net_pnl) WHERE status='CLOSED'` misses them.

**Why:** Items 1+2 were P0 crash-test findings from Day 1+2. Item 3 is a PnL trustability gap discovered during Day 3 investigation.

**How to apply:** Fix all 3, run full test suite, then start Day 3 CT067. Items 1+2 are already fixed (commit 1d3f516). Item 3 needs a decision: either include CLOSED_MANUAL in PnL queries or ensure orphan cleanup writes the correct status.

Related: [[ct-day1-day2-complete]] [[ct-restart-findings]]
