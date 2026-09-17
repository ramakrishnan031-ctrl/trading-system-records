---
name: project-fix129-p0-batch2
description: "FIX-129 five P0 Batch 2 fixes — order state validation, NTP check, cold-start safety, rejection handling, graceful shutdown"
metadata: 
  node_type: memory
  type: project
  originSessionId: 66b1f409-4cb9-4036-9b0e-6084605cf8fc
---

FIX-129 committed 2026-05-30 (commit 5a52b74). All 5 Batch 2 items implemented. Schema bumped to v16.

**Why:** Second batch of P0 critical fixes for live trading safety.

## Item 26: Order State Machine Validation
- Schema v16: `orders.reconciliation_status` column (NULL/OK/SL_MISSING/MISMATCH/ORPHAN)
- `state_store.update_order_reconciliation_status(order_id, status)` helper
- `order_reconciler._check9_missing_exits`: stamps "SL_MISSING" on naked position detection + "OK" when SL verified at broker
- 5 tests in `test_fix129_order_state_validation.py`

## Item 27: NTP Clock Sync
- `startup_checks.check_ntp_sync()`: UDP query to pool.ntp.org via stdlib socket (no external deps)
- `NtpCheckResult` dataclass; injectable `ntp_fetcher_fn` for tests
- drift < 2s: OK; 2-5s: warning; >= 5s: blocking failure; fetch failure: skipped (best-effort)
- Added as check #10 in `run_all_startup_checks()`; `StartupReport.ntp` field added
- 7 tests in `test_fix129_ntp_check.py`

## Item 34: Cold-Start Safety
- **ALREADY FULLY IMPLEMENTED** — no new code needed
- Existing: `_check1_manual_close`, `_check2_orphan_adoption`, `_check9_missing_exits`
- Existing: `fund_manager.rehydrate_from_open_trades`, `order_monitor.rehydrate_from_store`
- 8 verification tests in `test_fix129_cold_start_safety.py` document the existing coverage

## Item 43: Order Rejection Handling
- `_handle_placement_failure()`: Telegram WARNING alert on every rejection
- `suppress_alert=True` from slippage guard (avoids duplicate; slippage already sends its own alert)
- `symbol` kwarg added to key call sites (broker rejections, 429 exhausted, BrokerError, EOD cutoff, kill-switch)
- `_on_order_status_changed`: Telegram alert on broker-side FAILED/REJECTED zero-fill
- 5 tests in `test_fix129_rejection_handling.py`

## Item 45: Graceful Shutdown
- `order_monitor.cancel_all_entry_orders()`: cancels tracked ENTRY legs; preserves SL/TGT/EOD
- `_shutdown()` calls `cancel_all_entry_orders()` before `stop()` (logs cancelled count)
- Existing shutdown already had: signal handlers, thread drain, WebSocket close, WAL checkpoint
- 6 tests in `test_fix129_graceful_shutdown.py`

## VM Deployment Notes
- Schema v16: new `orders.reconciliation_status` column (ALTER TABLE or recreate)
- NTP check requires outbound UDP to pool.ntp.org:123 on VM (usually open; check firewall if blocked)
- NTP fetch failure → skipped (best-effort); does not block startup
