---
name: ct-ct076-result
description: "CT076 3 Circuit Breaker Failures → Hard Kill — CANNOT_TEST; paper adapter doesn't produce real API errors"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT076: 3 Consecutive Circuit Breaker Failures → Hard Kill** — CANNOT_TEST

The circuit breaker counter (max_api_failures) in order_monitor only increments on real broker API errors. Paper adapter always succeeds. Blocking Zerodha REST has no effect on paper adapter operations.

**To test:** Need live mode or inject BrokerError into adapter during order operations.
