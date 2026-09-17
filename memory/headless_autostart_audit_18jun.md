---
name: headless_autostart_audit_18jun
description: "Headless auto-start audit (18-Jun) — daily headless loop is ~90% BUILT; blockers = Kite-IP 403 emergency kill (external) + token-watcher's exit-4 start-loop defect"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7b6e2dc9-1fd2-4420-a210-2ffb31a91a12
---

Investigation 18-Jun-2026 (no code changes). Goal: fully headless 08:00-18:30. **Most of it already EXISTS — it was blocked by token auto-refresh (FIXED today, [[fix_187_headless_totp]]) + the Kite-IP 403 emergency kill ([[kite_ip_allowlist_dependency]]).**

## The designed daily loop (EXISTS, end-to-end)
1. 05:00 token wiped → 08:15 `auto_refresh_token.py` writes fresh token (FIX-187 ✓).
2. **`token-watcher.service`** (root, enabled, active; `deploy/token_watcher.sh`) polls every 30s: if token `date==today` + non-empty access_token AND service not active → `systemctl start trading-system.service`. Runs as root + ubuntu has `NOPASSWD: ALL` → no sudo gap.
3. main.py preflight auto-clears kills: `clear_stale_state(today)` (kill_switch.py:186, clears any **prior-day** kill) + `auto_clear_scheduled_kill()` (kill_switch.py:224, clears **same-day SCHEDULED** kills — `SCHEDULED_KILL_REASONS={circuit_breaker_force_close_15:15, EOD_SQUAREOFF}` kill_switch.py:80 — only if no open positions, never HARD_KILL). Called main.py:1273/1278.
4. Startup reconciliation: `order_reconciler.reconcile_once()` (main.py:2053) + `sweep_stale_orders()` (main.py:2063, FIX-186) ✓.
5. EOD: runtime loop runs until an `end` time then `_shutdown()` → **exit 0** → service stops (systemd `Restart=on-failure`, so exit 0 = no restart). Next morning repeats. Exit contract (`deploy/systemd/trading-system.service:27-35`): 0=EOD/holiday, 3=startup-check-fail, 4=HALT(kill active), 1/2=crash→restart. `KillSignal=SIGINT` = clean stop.
6. The 15:15 `circuit_breaker_force_close` SOFT_KILL (main.py:534) is a SCHEDULED reason → auto-clears next startup. So MIS-only same-day square-off does NOT require manual --resume.

## Health/monitoring (EXISTS)
`scripts/healthcheck_server.py` on **:8080** — `/health` (status/uptime/trades_today), `/metrics` (kill_switch_state, open_positions, daily_pnl, capital_deployed_pct…), `/metrics/prometheus`. Started main.py:2167. Webhook server also serves `/health` on **:5000** (main.py:2160). NB: /health only checks the DB, not broker/token liveness. `deploy/setup_uptimerobot.md` = external uptime config.

## GAPS
- **[EXTERNAL, must fix] Kite IP allowlist** — current SOFT_KILL reason = "Auto-trip: 3 consecutive API failures" (place_order 403 from the un-allowlisted VM IP). EMERGENCY → not auto-cleared → HALT exit 4 → stays down → needs `--resume` AFTER the IP is fixed in the Zerodha dev console. Not a code fix.
- **[CODE DEFECT, needs build] token-watcher ignores exit 4 / HALT.** `token_watcher.sh:64-74` only checks "service not active" → it **re-issues `systemctl start` every 30s** against a service that exited 4 (verified in `logs/token_watcher.log`: starts at :22/:52/:22…, each → HALT exit 4). Defeats the no-restart intent; churns startup (config-sanity logs, session rows, reconciliation) + repeated CRITICAL "HALT" logs. Fix: token-watcher should detect a recent exit-4/`failed`+`ExecMainStatus=4` and back off (and alert once) instead of hammering.
- **[POLICY] same-day EMERGENCY kill never auto-clears** (by design → --resume). Prior-day emergency kills DO auto-clear via `clear_stale_state` (then re-trigger if the condition persists). For headless robustness, a *guarded* same-day auto-clear of specific transient reasons (e.g., API-failure when flat + broker reachable) could be considered — but emergency kills exist to force human review; risky.

## Current manual steps (to eliminate)
(a) Fix Kite dev-console IP allowlist on any VM-IP change (external). (b) One `--resume` to clear the emergency SOFT_KILL after (a). The "daily morning restart" in [[deploy_requires_restart]] is now AUTOMATED by token-watcher once the token auto-refreshes (FIX-187) — it was only manual because token-refresh + the emergency kill were unresolved.
