---
name: order-lifecycle-operational-note
description: pending_rr_cancel failure logs ERROR but does not escalate to FAILED/orphan
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7cbac53e-3446-42e1-8243-b814aa9e0215
---

`pending_rr_cancel` failure (order_monitor.py:~1200) logs ERROR but does **NOT** transition the order to FAILED or fire the orphan callback (unlike the fill-timeout path, which does).

- Backstops that still catch it: fill-timeout (60s) and reconciler CHECK6.
- No action needed, but **monitor for ERROR logs mentioning `pending_rr_cancel`** during live trading — a recurring one means an ENTRY cancel keeps failing at the broker.

Related: [[co-bracket-operational-note]], [[capital-operational-note]].
