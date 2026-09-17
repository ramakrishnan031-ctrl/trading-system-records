---
name: fix-157-check9-closed-manual
description: "FIX-157: CHECK9 skips CLOSED_MANUAL trades; paper_capital updates on reconciler-closed positions"
metadata: 
  node_type: memory
  type: project
  originSessionId: b1f5f4b4-3390-48a3-8b95-770fe53c2346
---

**FIX-157 (09-Jun-2026): Two P0 fixes for CLOSED_MANUAL handling**

### 1. CHECK9 false positive on CLOSED_MANUAL trades
CHECK9 iterates a stale `local_trades` snapshot from `get_all_open_trades()`. When CHECK 1 closes a trade as CLOSED_MANUAL earlier in the same reconciliation cycle, CHECK9 still sees it in the list. FIX-155b's COMPLETE-exit check misses it because CLOSED_MANUAL doesn't complete SL/TGT orders.

**Fix:** Added re-query of trade status in `_check9_missing_exits()` before the critical path. If the trade is no longer OPEN/PARTIAL, skip it.
**File:** `orders/order_reconciler.py`

### 2. Capital drift from reconciler-closed trades
When reconciler closes a trade as CLOSED_MANUAL via `release_used()`, FundManager updates correctly but the paper adapter's `_paper_capital` is never updated. `_synth_fill()` only runs for normal order fills, not CLOSED_MANUAL.

**Fix:** Paper adapter subscribes to `PositionClosed` events. Events from `source_module="order_placer"` are skipped (already handled by `_synth_fill`). Reconciler-sourced events update `_paper_capital`.
**File:** `broker/zerodha_adapter.py`

### Tests
- `test_check9_skips_closed_manual_trade` — verifies CHECK9 doesn't fire for CLOSED_MANUAL
- `test_fix157_paper_capital_updates_on_external_position_closed` — verifies capital updates on reconciler close
- `test_fix157_paper_capital_loss_on_external_close` — verifies negative PnL works

**Why:** Both issues caused cascading failures on restart: CHECK9 false positives triggered SOFT_KILL loops; capital drift accumulated Rs 140.45+ per session from untracked CLOSED_MANUAL PnL.
**How to apply:** Related to [[ct-capital-drift-finding]], [[ct-check9-cascade-fixed]]. Both paper AND live modes benefit (live adapter ignores the subscription).
