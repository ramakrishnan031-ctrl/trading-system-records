---
name: ct-restart-findings
description: "Post-restart findings: order-monitor thread crash (orphan PENDING order) + eod-pre-alert AttributeError"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

## Restart at 14:22 IST, 08-Jun-2026

**Kill switch**: Cleared from SOFT_KILL to INACTIVE before restart.
**CHECK9**: No false positives after restart — FIX-155b confirmed working.
**Capital drift**: G3 CAPITAL_DRIFT delta=3499.19 (expected — paper adapter _paper_capital resets to default on restart, losing session PnL).

### Finding 1: order-monitor thread crash
**Severity**: HIGH (thread dead, no order monitoring)
`InvalidTransitionError: Cannot transition 'PAPER_CB77B3CB8DFA' from 'PENDING' to 'OPEN'`
Root cause: Orphan order in PENDING state from morning crash. On restart, order_monitor tried PENDING→OPEN but OSM requires PENDING→SUBMITTED→OPEN.
**Impact**: No order monitoring for rest of session. Acceptable for crash test EOD scenarios.

### Finding 2: eod-pre-alert thread crash
**Severity**: MEDIUM (CT075 won't fire)
`AttributeError: 'MarketWindows' object has no attribute 'is_trading_day'. Did you mean: 'is_trading_holiday'?`
Root cause: Wrong method name in main.py line 734.
**Impact**: EOD pre-alert at 15:00 won't fire. CT075 = FAIL due to bug.
**Fix needed**: Change `is_trading_day` to correct method name.

### Startup otherwise clean
- Webhook port 5000: ok
- Healthcheck port 8080: ok, uptime confirmed
- TEMP marker detected (max_daily_trades=200)
- Scanner connectivity warnings (expected — Chartink doesn't serve status checks)

**Related:** [[ct-day1-progress]], [[ct-check9-cascade-fixed]]
