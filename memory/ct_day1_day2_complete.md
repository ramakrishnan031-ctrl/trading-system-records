---
name: ct-day1-day2-complete
description: "Crash test Day 1+2 COMPLETE 08-Jun-2026: 42 PASS, 3 PASS_WITH_RISK, 1 FAIL, 2 P0 fixed, 3 open findings"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

## Crash Test Day 1+2 Summary (08-Jun-2026)

**47 scenarios executed** across Day 1 (signal lifecycle, load, timing, EOD) and Day 2 (screening, capital, data quality).

### Results: 42 PASS / 3 PASS_WITH_RISK / 1 FAIL / 1 DEFERRED

**The 1 FAIL (CT075)**: EOD pre-alert thread crashed on startup due to `is_trading_day` AttributeError in main.py:734. Fix: change to correct method name (`is_trading_holiday` with inverted logic).

### P0 Findings Fixed During Test
1. **Capital drift**: Paper adapter `_paper_capital` was static — now tracks realized PnL per fill in `_synthesise_fill()`. 5 tests.
2. **CHECK9 cascade**: Reconciler placed 39 emergency exits for 2 trades. Two-layer fix: FIX-155b (skip if exit COMPLETE) + FIX-155 (dedup guard). 4 tests.

### Open Findings (3)
1. **Order-monitor thread crash** (HIGH): Orphan PENDING order from morning crash causes `InvalidTransitionError` on restart → thread dies → no order monitoring. Needs: cleanup orphan orders on startup or handle PENDING→OPEN transition.
2. **EOD pre-alert bug** (MEDIUM): Wrong method name `is_trading_day` → `is_trading_holiday`.
3. **Paper capital snapshot** (LOW): `_paper_capital` resets on restart. Known limitation.

### TEMP Values Reverted
- `max_daily_trades`: 200 → 20 (SCP'd to VM)

### Remaining Crash Test Schedule
- Day 3 (Jun 9): Error recovery scenarios
- Day 4 (Jun 10): Performance + stress
- Day 5 (Jun 11): Edge cases + final certification

**Related:** [[ct-day1-progress]] (detailed per-scenario results), [[ct-check9-cascade-fixed]], [[ct-capital-drift-finding]], [[ct-restart-findings]]
