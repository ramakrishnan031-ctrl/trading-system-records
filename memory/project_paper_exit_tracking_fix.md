---
name: Paper exit tracking fix (2026-05-07)
description: order_monitor fill_timeout killed SL/TGT exits after 60s; fix adds leg-awareness; also fixed EOD report schema mismatch
type: project
originSessionId: 80c0c78f-481f-491b-832f-8aed476df7de
---
## Problem
Paper mode exit tracking completely broken — zero SL/TGT fills, zero P&L, all trades CLOSED_MANUAL by EOD.

## Root Cause
`order_monitor._check_fill_timeout()` applied 60s timeout to ALL orders including SL/TGT exits.
In paper mode, `_synth_fill` LTP-gating threads need up to 6 hours to find price crossings.
Race: order_monitor cancels exit orders at 60s → _synth_fill finds "OSM already terminal" at price crossing.

## Fix (commit e550e17)
- Added `leg` field to `_WatchEntry` ("ENTRY" / "SL" / "TGT" / "EOD")
- `_check_fill_timeout` skips exit legs (SL, TGT, EOD)
- All `track()` call sites pass `leg=` (order_placer + eod_squareoff)
- Rehydrate reads `leg` from state_store query (already in SQL)
- 4 new tests proving exit exemption + entry still times out

## Also Fixed
- **daily_review.py line 147**: step_results values are floats (scores), not dicts — was calling `.get("passed")` on a float
- **Cron PYTHONPATH**: Added `PYTHONPATH=.` to daily_review cron job (VM crontab updated)
- **test_daily_review.py**: Updated test fixture to match production schema (floats not dicts)

## Verification
- 1779 unit tests pass (2 pre-existing ATR→FIXED_PCT failures excluded)
- 32 order_monitor tests (28 existing + 4 new)
- Service restarted on VM

**Why:** Exit orders must survive for hours until price crosses; only EOD squareoff or actual fill should close them.
**How to apply:** Safe for live mode — broker handles SL/TGT natively; fill timeout was never needed for exits.
