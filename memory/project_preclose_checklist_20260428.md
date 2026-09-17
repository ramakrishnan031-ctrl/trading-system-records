---
name: Pre-close verification checklist (2026-04-28)
description: Final verification before market close; EOD scheduler confirmed running
type: project
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
**Pre-close verification (2026-04-28 15:00 IST)**

Checklist sent by user, verified by Claude:

1. **EOD square-off ready?** YES
   - Scheduled for 15:17 (17 mins before check)
   - Thread `eod_squareoff_p` confirmed running via /proc/PID/task/*/comm
   - Config: `eod_squareoff_time: "15:17"`

2. **Entry gate not blocking?** OK
   - Thread `eg-poll` confirmed running
   - Entry window closed at 15:15 - no new entries expected

3. **Smart TGT tracking?** N/A
   - No open positions with active trailing (all closed at SL earlier)
   - Shadow tracker would activate on next inning

4. **Signal processing?** OK
   - `sp-dispatcher` + 5 workers confirmed running
   - Signals being rejected at OUTSIDE_ENTRY_WINDOW (expected after 14:30)
   - No IN_PROCESS locks stuck

**Health check results:**
- Kill switch: INACTIVE
- Open positions: 4 (3 PENDING_FILL never filled, 1 CLOSED_MANUAL)
- Pending orders: 57 (paper SUBMITTED - expected, EOD will clean up)
- All daemon threads running

**Issues noted (non-blocking):**
- Log file rotated during session (startup logs in .log.1)
- step_executor TypeError on BHARATBOND symbols (vwap_position step, None comparison)

**Why:** Final verification before market close ensures EOD fires correctly.

**How to apply:** Run similar health check each day at 15:00 before market close.
