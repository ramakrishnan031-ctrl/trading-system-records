---
name: Post-market cleanup - 3 bugs fixed (2026-04-28)
description: Fixed TypeError in vwap_position, cleaned PENDING_FILL trades and orphaned orders
type: project
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
**Post-market cleanup (2026-04-28 15:12 IST)**

Three bugs fixed for clean runs tomorrow:

## 1. TypeError in vwap_position (FIXED)
- **File:** `screening/step_executor.py` line 160
- **Error:** `TypeError: '>' not supported between instances of 'float' and 'NoneType'`
- **Root cause:** BHARATBOND ETF symbols have `vwap: None` in market data
- **Fix:** Added None check before comparison, return 0.0 (fail gate) for missing VWAP
- **Commit:** 5bbbd67

## 2. PENDING_FILL trades stuck (CLEANED)
- 3 trades: SAIPARENT, JSWDULUX, NIMBSPROJ
- **Root cause:** Entry orders never filled in paper mode
- **Fix:** Added `--cleanup-pending` to check_vm_state.py
- **Action:** Marked as CANCELLED

## 3. 57 PENDING orders stuck (CLEANED)
- 39 LIMIT + 18 SL-M orders
- **Root cause:** Orphaned from trades that were CLOSED/CANCELLED
- **Fix:** Added `--cleanup-orders` to check_vm_state.py
- **Action:** Marked as CANCELLED

## New utility options in check_vm_state.py
- `--health` - Quick system health check
- `--positions` - List open positions
- `--orders` - Order status breakdown
- `--trades` - Recent closed trades
- `--cleanup-pending` - Mark stale PENDING_FILL trades as CANCELLED
- `--cleanup-orders` - Mark orphaned PENDING orders as CANCELLED

**Why:** Clean database state ensures accurate capital tracking and no ghost positions for tomorrow's session.

**How to apply:** Run `python3 scripts/check_vm_state.py --health` at end of each trading day to verify clean state.
