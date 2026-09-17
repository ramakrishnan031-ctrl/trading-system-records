---
name: crash-test-open-to-open-finding
description: order_monitor OPEN→OPEN InvalidTransitionError flood — low priority fix needed
metadata: 
  node_type: memory
  type: project
  originSessionId: b1f5f4b4-3390-48a3-8b95-770fe53c2346
---

order_monitor polls every 2s and tries SUBMITTED→OPEN on orders already in OPEN state. Causes `InvalidTransitionError` noise with many stale paper orders (31 trades today = dozens of SL/TGT orders). The error is caught and logged but creates log spam.

**Fix:** Skip transition if order is already in target state (`_safe_transition` should no-op on same-state). Low priority — not P0.

**Why:** Observed during Day 4 crash testing (09-Jun-2026). The flood made log monitoring difficult — had to filter out `Traceback` from EOD monitors. Functional impact is zero (errors are caught), but operational impact is noisy logs.
**How to apply:** When touching `order_monitor.py` or `order_state_machine.py`, consider adding a same-state guard. Related to [[ct-day4-results]].
