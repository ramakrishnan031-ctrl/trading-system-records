---
name: eod-18jun-cleanup-restart
description: "18-Jun-2026 EOD — repo cleanup done + VM restarted; service crash-loops on persisted SOFT_KILL (Kite-IP), not code"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

18-Jun-2026 EOD ops (post-market). Two items, both actioned.

CLEANUP (commit 9f3937c, deployed + verified on VM):
 - Deleted dead 0-byte `trading.db` at repo root (VM-direct; was untracked).
 - Deleted 56 stale `critical_alert_*.flag` (older than today); 16 today's kept.
 - Archived dated notes `CRON_FIX_2026_05_18.md` + `FIXES_DAILY_REPORT_2026_05_18.md` → `docs/archive/` (git mv).
 - Removed `deploy_audit_fixes.ps1` (superseded by git-push deploy).
 - Removed duplicate PC git remote `vm` (only `origin` remains).
 - Local scratch `CLAUDE_md_and_explanations.txt` → `docs/archive/` (stays gitignored, NOT committed).
 - Updated docs/SYSTEM_MAP.md (PENDING CLEANUP cleared; changelog).

RESTART (to activate tasks #9 score 55→60, #10 telegram switch, #11 drift 30min, #12/FIX-186 orphan
leak, #4 SYSTEM_MAP): `sudo systemctl restart trading-system.service` (passwordless sudo OK).

OUTCOME — service CRASH-LOOPS (activating/auto-restart, exit code 4, NRestarts ~240+). ROOT CAUSE is
NOT my code: app loads all 8 config files cleanly, then HALTs because the kill switch is in persisted
**SOFT_KILL** (auto-tripped 2026-06-18T12:37 by "3 consecutive API failures" = the Kite-IP 403 issue,
see [[kite_ip_allowlist_dependency]] / FIX-185). main.py startup scenario=HALT → exit 4; systemd
restarts because exit 4 is not in the unit's RestartPreventExitStatus=3 → loop. My deployed fixes are
verified to import/load fine; they will run once the service actually starts.

TO RECOVER (Rama's call — I did NOT do these; clearing the kill switch re-arms live trading):
 1. Fix the Kite dev-console IP allowlist for the VM IP (so place_order stops 403-ing and re-tripping).
 2. Clear the kill switch: run main.py with `--resume` (or the documented resume path).
 3. Then restart; the service should stay up and all of today's fixes are active.

NEW open issue found during this op: `alert-watcher.service` is INACTIVE (why flags accumulated) —
start/enable it. Also consider adding exit-code 4 (HALT) to the systemd unit's RestartPreventExitStatus
so a manual-resume-required HALT doesn't pointlessly hammer-restart. Both noted in SYSTEM_MAP issues.

FOLLOW-UP — 3 infra fixes (commit ebfe780, deployed):
 A) `alert-watcher.service` enabled + started (was UnitFileState=disabled, never enabled; not a crash).
    Now active+running, survives reboot. BUT delivery still fails: `alerts.smtp` is placeholder
    (`alerts@example.com` username/from, `operator@example.com` to, `password_env: ALERT_SMTP_PASSWORD`
    UNSET) → digest send throws, 16 flags stay `.flag` (not `.delivered`). The watcher is email-based
    (NOT Telegram). REMAINING ACTION (Rama): set real SMTP user/from/to + ALERT_SMTP_PASSWORD (Gmail
    app-password). Until then CRITICAL sentinels are written but not emailed.
 B) systemd `RestartPreventExitStatus=3 4` — applied to live unit (sed + daemon-reload) AND canonical
    `deploy/systemd/trading-system.service`. VERIFIED: the exit-4 HALT crash-loop STOPPED — NRestarts
    froze at 325, service now settles to `failed` (down) instead of hammer-restarting. Correct state:
    it SHOULD stay down until the Kite-IP allowlist is fixed and the kill switch is `--resume`d.
 C) deleted 0-byte dead PC `trading.db` (untracked; VM copy removed earlier).
Service `trading-system.service` is now cleanly `failed`/stopped (not looping). Recovery still requires
Kite-IP allowlist fix + `--resume` (unchanged; I did NOT clear the kill switch).
