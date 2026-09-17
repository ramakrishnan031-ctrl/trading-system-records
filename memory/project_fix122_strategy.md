---
name: project_fix122_strategy
description: FIX-122 — trades.strategy was empty for all rows; root cause fixed in order_placer + signal_processor; 167 rows backfilled on VM
metadata: 
  node_type: memory
  type: project
  originSessionId: 25222f28-c6d7-4b54-aa0d-afb0f10cc7a5
---

FIX-122 complete — commit 46dc0a9 (2026-05-18).

**What was wrong:** `order_placer.place()` hardcoded `strategy=""` when calling `create_trade()` (line 620, comment "OP10: strategy lookup not yet wired"). Both signal_processor call sites never passed strategy either. Result: all 167 trades across all 10 trading days had empty strategy.

**Fix applied:**
- `orders/order_placer.py`: added `strategy: str = ""` param to `place()`, passed through to `create_trade()`
- `signals/signal_processor.py`: added `strategy=strategy_name` at both `place()` call sites (normal pipeline + gate-release path)
- `tests/unit/test_signal_processor.py`: updated `_MockOrderPlacer.place()` to accept `strategy` kwarg

**DB backfill:** `UPDATE trades SET strategy = (SELECT s.strategy FROM signals s WHERE s.signal_id = trades.signal_id) WHERE strategy IS NULL OR strategy = ''` — fixed all 167 rows on VM; verified 0 nulls remain.

**Report regenerated:** `daily_report_2026-05-18.xlsx` re-run on VM; Sheets 2_Orders/3_Capital/4_Candles/6_Strategy_Analysis all show correct strategy names.

**Pre-existing issue noted:** 71 Windows `PermissionError` failures in `test_order_placer.py` (temp DB cleanup on Windows TempDirectory exit) — unrelated to this fix, pending cleanup.

**Why:** `strategy` was marked as "not yet wired" in the OP10 comment from the initial build; never followed up on.

**How to apply:** Future order_placer changes — check that `strategy` is always passed at `place()` call sites. The `create_trade()` schema column `strategy TEXT NOT NULL` will enforce it at DB level going forward.
