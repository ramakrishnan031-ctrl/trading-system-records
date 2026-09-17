---
name: project-fix127-stale-killswitch
description: "FIX-127 auto-clear stale kill switch + restart loop root cause (2026-05-30, commit 79ea97d)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1bd6d797-10ec-4774-b045-1283ba6bd864
---

FIX-127 landed (commit 79ea97d, pushed to VM).

**Root cause of 10,652-restart loop (May 21-23):**
1. May 21 07:42 IST: order_reconciler detected naked MANKIND position (missing SL order) → SOFT_KILL persisted in DB
2. Every restart: KillSwitch._load_state_from_store() loaded SOFT_KILL → main.py line 1611 `is_active("any")` → exit 1
3. systemd `Restart=on-failure` restarted on exit 1 → infinite loop
4. Loop ran ~10,652 times until midnight Saturday when weekend guard broke it (exit 0)

**Fix:** `KillSwitch.clear_stale_state(today)` — if kill switch was triggered on a previous calendar day, auto-clear to INACTIVE. Called in main.py right after construction, before startup checks. If the trigger was legitimate, startup reconciliation will re-trigger within seconds.

**Additional VM fixes applied:**
- Manually cleared stale SOFT_KILL state in DB
- Fixed daily_report cron: removed stale `--candle-dir` flag (removed in FIX-124)
- Enabled token-watcher for auto-start on boot: `systemctl enable token-watcher`

**Why:** Kill switch persistence (KS3/Audit #18) is correct for same-day restart recovery, but cross-day persistence creates restart loops since operator resume() is never called automatically.

**How to apply:** New-day startup = clean slate. Never let previous-day operational state block next-day startup without re-validation.

**Related:** [[project-double-release-fix]], [[project-capital-invariant-paper-bug]]
