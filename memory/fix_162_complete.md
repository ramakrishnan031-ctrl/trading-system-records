---
name: fix-162-complete
description: "FIX-162: AGY automation fully working — dotenv in cron scripts, watchman auto-start, arg order fixed. Deployed 11-Jun-2026."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b860701-6391-4408-be2a-86ea2bdeaf60
---

**FIX-162: AGY automation fixes** — commit `f018131`, 2026-06-11

## Issues fixed
1. **Arg order**: `--dangerously-skip-permissions` now at index 1 (was 2 — split `--model` from value, causing CLI hang). Test assertion added for position.
2. **dotenv loading**: Added `from dotenv import load_dotenv; load_dotenv(_ROOT / ".env")` to all 8 cron/AGY scripts. Previously cron env had no .env → Telegram=None → NoneType crash. Verified "Telegram alert sent" post-fix.
3. **Watchman auto-start**: systemd drop-in at `/etc/systemd/system/trading-system.service.d/watchman.conf` adds `Wants=trading-watchman.service`. Watchman starts with trading-system, exits outside market hours (by design).

## Verification
- `check_cron_drift.py` → "Telegram alert sent" (no crash)
- 26/26 tests pass
- git push deployed to VM

Related: [[agy-automation-status]] [[fix-160-agy-cascade]]
