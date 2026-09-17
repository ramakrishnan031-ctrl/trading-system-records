---
name: ct-day5-ct137
description: "CT137 Kill Switch + Active Positions + EOD — PASS. SOFT_KILL HALTs system, preserves positions, blocks entries."
metadata: 
  node_type: memory
  type: project
  originSessionId: 46ec89b8-48f0-47c1-920a-8d920c9f5480
---

**CT137: Kill Switch + Active Positions + EOD Squareoff — PASS**
Date: 2026-06-10, 09:33-09:39 IST

**Steps executed:**
1. Started with 2 OPEN trades from CT136 + injected signals → 3 OPEN positions (HERANBA, WINDMACHIN, PATELRMART)
2. Set SOFT_KILL in DB (reason: ct137_loss_limit_breach)
3. Restarted system → observed HALT scenario
4. Verified positions preserved in DB
5. Cleared kill switch, restored system

**Assertions:**
- Kill switch prevents new entries: ✓ (HALT scenario — system refuses to start entirely)
- Existing positions preserved: ✓ (3 OPEN trades intact in DB)
- Shutdown graceful: ✓ (cancelled 4 pending ENTRY orders, WAL checkpoint complete)
- EOD squareoff with kill switch: CANNOT_TEST (09:38 IST, EOD runs at 15:17)

**Key finding:**
SOFT_KILL with emergency reason → startup_scenario=HALT. System does NOT continue running with blocked entries — it halts completely. Operator must use `--resume` to clear. This is MORE restrictive than expected:
- SOFT_KILL blocks entries (intent=entry) but allows exits (intent=exit)
- However, HALT scenario prevents any processing at all
- Positions remain at broker, must be managed manually or after --resume

**EOD interaction:** Since system halts, EOD timer never fires. Operator must resume first, then EOD can fire. This is a deliberate safety design — forces human operator to assess before auto-recovery.

Related: [[ct-day5-ct136]]
