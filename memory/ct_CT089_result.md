---
name: ct-ct089-result
description: CT089 EOD Squareoff — PASS; SOFT_KILL→INACTIVE in 3s; no positions to close
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT089: EOD Squareoff** — PASS

EOD squareoff fired at exactly 15:17:00 IST (matches `eod_squareoff_time` config):
```
15:17:00 CRITICAL: INACTIVE -> SOFT_KILL reason=EOD_SQUAREOFF
15:17:03 CRITICAL: SOFT_KILL -> INACTIVE reason=EOD_SQUAREOFF_COMPLETE
```

Completed in 3 seconds. No open trades to close (all morning trades already resolved before 14:22 restart). Mechanism confirmed working — activates SOFT_KILL, scans positions, deactivates when done.

Post-squareoff state: 0 open trades, 126 orphan open orders (from morning crash, order-monitor thread dead so not cleaned up).

**Related:** [[ct-CT031-result]], [[ct-day1-progress]]
