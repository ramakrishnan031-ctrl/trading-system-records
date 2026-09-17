---
name: deploy_requires_restart
description: git push deploys to the VM working tree but does NOT restart the long-running service; code in git != code running until restart
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 705e3934-5847-4a81-9394-fec010dffb93
---

`git push origin main` triggers the bare-repo post-receive hook which `git checkout`s into ~/systems/trading-system (working tree). It does NOT restart the systemd `trading-system` service. The service is a long-running process (`main.py --mode live`) that imported its code at start time — files changed on disk do NOT affect the running process.

**Why:** On 16-Jun-2026 (Live Day 1), FIX-180/181 were pushed/synced to the VM working tree at 16:46 but the service kept running the 09:04 process with PRE-FIX-180/181 code all day. Every failure that day was already fixed in code that simply wasn't running. See [[fix_182_complete]].

**How to apply:**
1. After `git push`, ALWAYS `sudo systemctl restart trading-system` to activate new code, and verify with `curl localhost:5000/health` AND by confirming the running process picked up the change (e.g. check a new log marker, or `systemctl show -p ActiveEnterTimestamp`).
2. No cron/systemd-timer restarts the service — the daily morning restart is MANUAL (Rama's routine). Startup runs `kill_switch.clear_stale_state(today)` (main.py:1253) which auto-clears a PRIOR-day HARD_KILL/SOFT_KILL, and re-auths with the fresh 08:00 token cron.
3. `clear_stale_state` is startup-only (not runtime). After 15:15 the order_monitor force-close circuit breaker sets SOFT_KILL (`circuit_breaker_force_close_15:15`); it persists overnight and only clears on the next morning restart. So a same-day restart will NOT clear today's kill — use `KillSwitch.resume()` explicitly if needed.
4. After a restart, if the persisted kill_switch_state is HARD_KILL (same-day), startup HALTs (exit non-zero) and `Restart=on-failure` crash-loops until the kill is cleared (resume) — exactly the 08:51 / 21:46 loops on 16-Jun.

Related: [[weekend_cron_protection]].
