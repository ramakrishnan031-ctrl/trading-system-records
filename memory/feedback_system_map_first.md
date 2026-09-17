---
name: feedback-system-map-first
description: NON-NEGOTIABLE — read docs/SYSTEM_MAP.md before any VM/system work; update it after any path change
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

RULE (NON-NEGOTIABLE, from TASK #4, 18-Jun-2026): Before ANY work on the VM or trading system —
bug fix, development, file creation, path reference, cron/service modification, config change,
script creation/modification, or infrastructure change — FIRST read
`docs/SYSTEM_MAP.md` (full map/audit) and `PATHS.md` (quick reference) in the repo. After ANY
file/path/cron/service change, UPDATE `docs/SYSTEM_MAP.md` (and its Changelog).

**Why:** prevents duplicate paths, editing the wrong/dead file, and wasted work. The audit already
caught real traps: a 0-byte dead `trading.db` at repo root (canonical DBs live in `data_store/`),
the live crontab diverging from the canonical `deploy/cron/trading-system.cron`, accumulating
`critical_alert_*.flag` sentinels, and a duplicate PC git remote.

**How to apply:** open `docs/SYSTEM_MAP.md` first; confirm the canonical file for your target (esp.
DB = `data_store/trading_system.db` + `analytics.db` via `core.db_connect.connect`; deploy =
`git push`, NOT scp, and deploy ≠ restart). When done, if any path/file/cron/service changed, edit
SYSTEM_MAP.md + add a dated Changelog line in the same commit.

**VM coordinates (never guess — grep PATHS.md/SYSTEM_MAP):** project dir = `/home/ubuntu/systems/trading-system/`
(NOT `~/trading-system`), shared venv = `/home/ubuntu/systems/venv/bin/python`, public IP = **161.118.187.249**
(verified via ipify 23-Jun; any `80.225.x` is a STALE artifact from an old audit doc). Working tree has no
`.git` (deployed via bare-repo `~/trading-system.git` checkout) — check the deployed commit with
`git -C ~/trading-system.git log`. Agent CLIs live OUTSIDE the project in `~/tools/` (antigravity/`agy`,
gemini, claude). On 23-Jun I wasted two tries guessing the VM dir before reading PATHS.md — don't repeat it.

Created TASK #4: docs/SYSTEM_MAP.md + PATHS.md (commit f140339). See [[task-4-system-map]].
Related: [[deploy_requires_restart]], [[project_vm_architecture_locked]], [[db_schema_v28_split]].
