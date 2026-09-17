---
name: fix_188_headless_autostart
description: FIX-188 headless fixes — token-watcher exit-code awareness (no HALT hammer) + /health token/kill-switch checks; deployed & verified; manual --resume vs systemd lock gap flagged
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b6e2dc9-1fd2-4420-a210-2ffb31a91a12
---

**FIX-188 (18-Jun-2026): two headless gaps fixed (from [[headless_autostart_audit_18jun]]). Deployed + verified.** Commits **7a12cf2** (A+B) + **8cf8685** (B table fix).

## Item A — token-watcher exit-code awareness (`deploy/token_watcher.sh` rewrite)
Was: re-issued `systemctl start` every 30s against an exit-4 HALT (hammer). Now decides on `ExecMainStatus` + `ExecMainExitTimestamp`:
- exit 4 (HALT) / exit 3 (startup-fail) **today** → do NOT restart; ONE Telegram alert/day (date-stamped flag in `/tmp/ts_watcher_state/`); back off to 300s polls. **Prior-day** 4/3 → one clean start attempt (main.py `clear_stale_state` auto-clears prior-day kills → overnight HALTs still auto-recover).
- exit 1/2 (crash) → restart with backoff (max 3/hr).
- exit 0 **today** (clean EOD) → do NOT restart post-EOD; prior-day/none → start. All starts require a fresh token; resume detected (service active) clears alert flags.
- VERIFIED: after restart, watcher issued ZERO starts, correctly deferred; service `active`, `NRestarts=0`.

## Item B — `/health` (:8080) broadened (`scripts/healthcheck_server.py`)
`GET /health` now returns `{status, checks:{db, token, kill_switch}, ...}` and **HTTP 200 healthy / 503 degraded** (uptime monitors detect degraded-but-listening). token via `zerodha_login.is_token_valid`; kill_switch via the **`kill_switch_state` table (id=1, cols state/reason)** — NOT `system_state`. The first live curl caught my initial wrong-table copy (from `/metrics`, which silently mis-defaulted kill_switch_state to INACTIVE forever); fixed both `/health` and `/metrics`. 10 unit tests. VERIFIED live: db ok, token ok, kill_switch correctly reads SOFT_KILL.

## Live hand-off done (this session, after-hours/flat)
Found Rama's manual `main.py --resume` (PID 459526, the recovery step) holding instance-lock **port 5001**; systemd's service loop-failed on the lock (exit 1, NRestarts 113+). With Rama's OK: SIGTERM'd 459526 → `reset-failed` → `systemctl start` → service now runs cleanly under systemd (active, NRestarts=0). The emergency API-failure kill was already cleared by his --resume; the post-EOD `circuit_breaker_force_close_15:15` SOFT_KILL auto-clears next morning.

## Still open
- **[EXTERNAL] Kite IP allowlist** ([[kite_ip_allowlist_dependency]]) — allowlist the VM IP in the Zerodha dev console for order placement tomorrow. Not code.
- **[CLOSED — FIX-188b, commit 9ddcddf] systemd `--resume` path** — `scripts/clear_kill_switch.py` clears the kill in the DB via `KillSwitch.resume()` WITHOUT acquiring the instance lock/loop (`--dry-run`, `--force` for HARD_KILL); `deploy/resume.sh` does stop → clear → reset-failed → start under systemd. **Use these instead of standalone `main.py --resume`** (which competes for instance-lock port 5001). 6 tests; live dry-run verified.
