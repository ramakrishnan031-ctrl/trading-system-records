---
name: Paper-to-live transition - LIVE since 11-May-2026
description: Paper trial complete; system LIVE on VM since 11-May; Rs 25K micro capital; double-release fixed Day 1
type: project
originSessionId: 3240cc27-d911-4827-864b-d5427aec0c5f
---
3-week paper→live path completed. **SYSTEM IS LIVE since Mon 11-May-2026.**

## Timeline completed
| Week | Dates | Label | Status |
|------|-------|-------|--------|
| 1 | 20–24 Apr | Full Diet Paper | DONE |
| 2 | 27 Apr–08 May | Chaos Diet + extended paper | DONE (multiple prod bugs fixed) |
| 3 | Code Freeze | Skipped — went live after stabilization | — |

## Live status
- **Live Day 1:** Mon 11-May-2026
- Capital: Rs 25,000 micro capital
- Execution host: VM (161.118.187.249), systemd active
- Day 1 incident: HARD_KILL from double-release bug → root cause fixed commit 4ef614e
- Day 2 (12-May): Monitoring for clean run

## Production bugs fixed during paper (non-exhaustive)
- vwap None check, PENDING_FILL cleanup, orphaned orders
- entry window hardcode, log quoting
- capital invariant paper mode, paper order status
- paper P&L stubs, single instance enforcement
- quote cache, pool sizing, shadow_tracker null guard
- symbol aliases, exit tracking timeout, log rotation
- double capital release (root cause: paper positions)

## Key constraint (still active)
- NEVER push code changes during market hours (09:15–15:30 IST)
