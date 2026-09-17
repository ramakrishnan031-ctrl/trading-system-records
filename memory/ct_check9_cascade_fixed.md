---
name: ct-check9-cascade-fixed
description: "P0 FAIL FIXED: CHECK9 emergency exit cascade; dedup guard added; 2 new tests; FIX-155"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

## FIX-155: CHECK9 Emergency Exit Cascade (08-Jun-2026)

**Classification:** P0 FAIL (upgraded from DESIGN_GAP — infinite cascade is a production-safety failure)

**Symptoms:** 39 emergency exit orders placed for 2 NRBBEARING trades. Each reconciler cycle saw OPEN trade + no SL order → placed another emergency MARKET exit → cascade loop.

**Root Cause:** `_check9_missing_exits` had no dedup guard. When SL order fills in paper mode (removed from open orders) but order_monitor hasn't yet closed the trade in DB, CHECK9 fires repeatedly. Each cycle places a new emergency exit because it never checks if one is already pending.

**Fix (two layers, defense in depth):**

**Layer 1 — FIX-155b (root cause):** Before flagging naked position, check if any exit order (SL/TGT/EOD) already COMPLETE for this trade. If yes: trade is closing via normal path, skip CHECK9 entirely. This prevents the first false-positive trigger.
```sql
SELECT COUNT(*) FROM orders WHERE trade_id=? 
AND leg IN ('SL','TGT','EOD') AND status='COMPLETE'
```

**Layer 2 — FIX-155 (cascade guard):** If Layer 1 didn't catch it and CHECK9 still fires, check for existing pending emergency exit before placing another:
```sql
SELECT COUNT(*) FROM orders WHERE trade_id=? 
AND leg='EOD' AND order_type='MARKET' 
AND status IN ('PENDING','SUBMITTED','OPEN')
```

**Tests:** 4 new in `test_order_reconciler.py` (57 total, all pass):
- `test_check9_skips_when_exit_order_already_complete` — FIX-155b: COMPLETE SL → skip
- `test_check9_still_fires_for_genuine_naked_position` — FIX-155b: no COMPLETE exit → fires correctly
- `test_check9_no_cascade_when_emergency_exit_already_pending` — FIX-155: dedup guard
- `test_check9_places_emergency_exit_when_none_pending` — FIX-155: normal path works

**Paper/Live parity:** Both layers apply to both modes. Live mode rarely hits this (broker updates are atomic) but the guards are defensive.

**Deployment:** Files SCP'd. 57/57 reconciler tests pass (PC + VM). Service masked until 14:30. Kill switch cleared. max_daily_trades=200 TEMP.

**Related:** [[ct_naked_position_finding]] (original finding), [[ct_capital_drift_finding]] (adapter static capital)
