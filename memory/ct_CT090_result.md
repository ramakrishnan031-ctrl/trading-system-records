---
name: ct-ct090-result
description: CT090 EOD Squareoff Order Fails — CANNOT_TEST; paper adapter always succeeds on MARKET orders
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT090: EOD Squareoff — Order Fails** — CANNOT_TEST

Paper adapter's place_order always succeeds (returns synthetic order, fill daemon processes it). Blocking Zerodha REST doesn't affect paper adapter. Cannot simulate order failure during EOD squareoff in paper mode.

**To test:** Need live mode where MARKET order could genuinely fail at broker.
