---
name: Two notification bugs fixed (2026-05-06)
description: Holiday alert loop (sentinel anti-loop) + exit alert timeout (LTP-gating 60s→21600s)
type: project
originSessionId: 3511025d-0169-48ad-b569-b2bef776df3d
---
## BUG 1: Holiday Telegram alert loop
**Root cause:** token_watcher restarts service on holidays; holiday guard sends Telegram + exits 0; cycle repeats every 30s flooding channel.
**Fix:** Sentinel file `logs/.holiday_notified_<date>` — only sends Telegram once per day.
**Note:** "06-May as holiday" likely means VM has stale code or stale message from May 1 (Maharashtra Day). Current code correctly identifies May 6 as trading day.

## BUG 2: No SL/TGT exit alerts in paper mode
**Root cause:** `paper.ltp_gating_max_wait_sec: 60` — exit orders only had 60 seconds for LTP to cross price. SL/TGT takes minutes-hours. After timeout, order stays SUBMITTED; position closes via EOD (which intentionally skips alerts).
**Fix:** max_wait raised to 21600s (6h, covers full trading day), poll_sec raised to 5.0s (keeps 30 exit threads at ~6 LTP fetches/sec). Validator cap raised from 3600 to 25200.

**Why:** Both bugs made paper trial monitoring blind — can't tell if system is alive (holiday spam) or trading correctly (no exit signals).

**How to apply:** After deploy to VM, verify: (1) no holiday spam on next non-trading day, (2) exit alerts appear within 5s of LTP crossing SL/TGT level.

## DEPLOYED to VM (2026-05-06 17:48 IST)
- Commit a3e2ce5, pushed via `git push vm main`
- Service restarted, active (running), 17 threads healthy
- Config verified: ltp_gating_max_wait_sec=21600, 6 sentinel refs in main.py
- Paper/Live parity: UNIFIED (both modes use same execution path)
