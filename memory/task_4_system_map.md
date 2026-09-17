---
name: task-4-system-map
description: TASK
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

TASK #4 DONE (18-Jun-2026): created the authoritative path reference.
Files: `docs/SYSTEM_MAP.md` (full audit) + `PATHS.md` (root quick-ref). Commit **f140339**, pushed
and deployed to VM (verified present; no secrets committed — Telegram token referenced by env-var
name only).

Contents: full VM+PC audit — project root `/home/ubuntu/systems/trading-system`, shared venv
`/home/ubuntu/systems/venv` (py3.12.3), config inventory, per-package module roles (18 pkgs / 419
.py / 305 tests), DB layout (v28: trading_system.db + analytics.db), logs, ~28 cron jobs, 4 systemd
services (trading-system / token-watcher / alert-watcher / trading-watchman), gemini AI-ops tooling,
git-push deploy mechanism (bare repo `~/trading-system.git` post-receive → working tree; NOT scp).

DUPLICATES/ISSUES flagged (listed under "PENDING CLEANUP — awaiting approval", nothing deleted):
 1. root `trading.db` = 0-byte DEAD file (canonical DBs in data_store/).
 2. live crontab DIVERGES from canonical `deploy/cron/trading-system.cron` (refresh_instruments
    timing; live missing analytics.db 01:05 backup + db_retention 02:30 jobs).
 3. ~70 stale `critical_alert_*.flag` sentinels piling up in data_store/ (crash-loop).
 4. duplicate PC git remote (`origin` + `vm` → same bare repo).
 5. trading-system.service crash-loop (Kite IP allowlist, see [[kite_ip_allowlist_dependency]]).

The enforcement rule is [[feedback-system-map-first]] (read before any work, update after path changes).
