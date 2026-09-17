---
name: project-fix140-audit-fixes
description: FIX-140/141 — 14-point audit + entry-cancel R:R logic + disk-monitor; 2661 tests; commits 67f21c0/66f9eac
metadata: 
  node_type: memory
  type: project
  originSessionId: e51e9270-0d6d-4042-b121-32464f9034f0
---

FIX-140 landed 2026-06-01 (commit 67f21c0). FIX-141 landed 2026-06-01 (commit 66f9eac).

**14-point audit findings:**
- Points 1-5, 7-10, 14: current architecture CORRECT
- Point 6: entry cancellation gap — FIXED (FIX-141 R:R-based logic)
- Point 11-12: retention/disk gaps — FIXED (disk_monitor.py + cron)
- Point 13: Gemini log review — feasible, deferred

**7 Additional Findings (AF-1 through AF-7):**
- AF-1 CRITICAL: 7 TEMP config values still active (documented, revert before capital increase)
- AF-2 LOW: duplicate cron → FIXED
- AF-3 MEDIUM: logrotate wrong path → FIXED
- AF-4 INFO: no partial profit booking → DEFERRED
- AF-5 INFO: BreakevenManager CO asymmetry → DEFERRED
- AF-6 MEDIUM: no DB archive policy → DEFERRED (disk_monitor covers immediate risk)
- AF-7 MEDIUM: require_hmac=false → CLARIFIED (permanent: Chartink uses ?token= auth; WEBHOOK_SECRET enforced in live mode)

**Entry cancel logic (FIX-141, replaces FIX-140):**
- Config: `entry_gate.min_pending_rr: 1.0` (in entry_gate section, not order_monitor)
- Formula: cancel ENTRY if `remaining_reward / risk_distance < min_pending_rr`
  - LONG: remaining_reward = tgt - ltp; risk_distance = entry - sl
  - SHORT: remaining_reward = ltp - tgt; risk_distance = sl - entry
- Guards: risk_distance ≤ 0 → skip; ltp=0 → skip (fail-open)
- Strategy-adaptive: 2.5 R:R trade absorbs more drift than 1.5 R:R at same threshold

**Other features:**
- `scripts/disk_monitor.py` — hourly cron; >75% WARNING, >86% CRITICAL + auto-cleanup

**How to apply:** TEMP values (AF-1) must be reverted before any capital increase beyond Rs 25K.

**Test count:** 2661 passed, 0 failures (removing price_movement_cancel_pct from OrderMonitorConfig also fixed 3 pre-existing test_fix073/fix075 failures).
