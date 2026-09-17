---
name: ct-ct088-result
description: "CT088 Partial Fill Timeout — CANNOT_TEST; paper adapter doesn't simulate partial fills"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT088: Partial Fill Timeout (5 min)** — CANNOT_TEST

Paper adapter fills orders completely (full qty) on simulated fill. No partial fill simulation available. The 5-minute partial fill timeout code path exists but cannot be triggered in paper mode.

**To test:** Need live mode or paper adapter enhancement to simulate partial fills.
