---
name: fix-158-antigravity-audit
description: "FIX-158 — 3 issues from antigravity audit (DB corruption, OPEN→OPEN log bloat, cron .env + Telegram factories)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 46ec89b8-48f0-47c1-920a-8d920c9f5480
---

FIX-158 addresses 3 issues found by antigravity audit on 10-Jun-2026:

1. **DB Corruption (P0)**: Malformed b-tree pages in trading_system.db. Restore from daily backup at `data_store/backups/`. Integrity check: `PRAGMA integrity_check`.

2. **OPEN→OPEN Log Bloat (P0)**: order_monitor `_safe_transition` re-raised `InvalidTransitionError` for OPEN→OPEN (same-state) transitions, causing ~10GB/day log spam. Fixed by adding same-state check (`from_state == to_state → return False`) before the re-raise path. 3 new tests.

3. **Cron .env + Telegram factories (P1)**:
   - Added `from_env()`, `from_config()` classmethods to TelegramNotifier
   - Added `send_alert()`, `send_critical()`, `send_info()` convenience methods
   - Fixed 8 scripts using broken constructors (no chat_ids) → use `from_env()`
   - Fixed `disk_monitor.py` wrong `send()` signature
   - Updated `deploy/cron/trading-system.cron` — all Python entries now source `.env`
   - 7 new tests

**Why:** Crash test Day 4 residue + live production issues.
**How to apply:** Deploy code + install updated crontab on VM. DB restore is separate VM operation.

**Deployment notes (10-Jun-2026):**
- June 10th 01:00 backup was ALSO corrupted (b-tree damage)
- Restored from June 9th backup + REINDEX → integrity ok
- First start after restore crashed (sqlite WAL race); systemd auto-restart succeeded
- System stable since 09:19:50 IST, health=ok, no errors
- Data loss: 09-Jun 01:00 to 10-Jun (no market-hour trades lost)

Related: [[ct_day4_results]], [[ct_open_to_open_finding]]
