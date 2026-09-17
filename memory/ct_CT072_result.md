---
name: ct-ct072-result
description: CT072 Orphan Order → Soft Kill — CANNOT_TEST; paper adapter maintains in-memory order state
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT072: Orphan Order → Soft Kill** — CANNOT_TEST

In paper mode, deleting SL order from DB doesn't trigger orphan detection because reconciler compares against paper adapter's in-memory state (which still has the SL). The SL_MISSING check requires broker API to report different orders than what's in DB.

**To test:** Need live mode where broker's order book is the truth source.
