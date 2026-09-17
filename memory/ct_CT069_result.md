---
name: ct-ct069-result
description: "CT069 3 Consecutive API Failures — CANNOT_TEST; paper adapter doesn't make real Zerodha API calls"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT069: SOFT_KILL 3 Consecutive API Failures** — CANNOT_TEST

Paper adapter handles all order operations internally without making real Zerodha REST API calls. Blocking Zerodha REST has no effect on order_monitor's API failure counter. The counter only increments on real broker API errors (BrokerError, not BrokerAuthError) in `order_monitor._poll_cycle()`.

Code verified: `broker/order_monitor.py:667-684` — consecutive_api_fails increments on generic API error during poll, not on paper adapter responses.

**To test:** Need live mode with real broker connectivity, or inject BrokerError into paper adapter.

Related: [[ct-CT073-result]]
