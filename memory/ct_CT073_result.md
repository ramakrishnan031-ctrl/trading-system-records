---
name: ct-ct073-result
description: "CT073 Token Expiry — CANNOT_TEST; paper adapter doesn't make real Zerodha API calls"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT073: SOFT_KILL Token Expiry** — CANNOT_TEST

Paper mode uses ZerodhaAdapter in paper mode — all order operations go through the paper adapter simulation, not real Zerodha API. Removing the token file during runtime doesn't trigger BrokerAuthError because no real API calls are made for orders.

Token validation happens at startup only (in live mode). Paper mode skips this check.

**To test properly:** Need live mode with real broker credentials, or a mock that intercepts the adapter and injects BrokerAuthError.

Related: [[ct-day3-results]]
