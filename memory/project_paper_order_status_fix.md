---
name: Paper mode order status bug FIXED (2026-05-04)
description: _paper_fills dict tracks order state; SUBMITTED added to _KITE_STATUS_OPEN; commit 56e79a9 pushed to VM
type: project
originSessionId: 20e7cadd-4487-4f2d-87c2-551f76dc9808
---
## Bug
Paper mode `get_order_history()` always returned static `SUBMITTED` stub. `order_monitor` didn't recognize `SUBMITTED` as valid open status → `unknown_status` warnings on every poll cycle. Orders appeared stuck.

## Fix (commit 56e79a9)
1. **`broker/zerodha_adapter.py`**: Added `_paper_fills` dict (thread-safe) to track real order state transitions: SUBMITTED → COMPLETE (on synth fill) or CANCELLED (on cancel). `get_order_history()` reads from this dict instead of returning static stub.
2. **`broker/order_monitor.py`**: Added `"SUBMITTED"` to `_KITE_STATUS_OPEN` set so order_monitor treats it as valid open status.

**Why:** Blocker for all paper trading — every order generated unknown_status warnings and order lifecycle was broken.

**How to apply:** Fix is deployed and verified on VM. Kill switch was also cleared (NEGATIVE_MARGIN_USED from capital invariant paper bug). VM remote URL updated to use `trading-vm` SSH alias.

## Also shipped
- `scripts/test_webhook.py` — standalone webhook connectivity test
- VM remote URL fixed: `trading-vm:~/trading-system.git` (uses SSH alias with correct key)
