---
name: alertwatcher_loop_fix_16jul
description: "alert-watcher --loop daemon fix + canary respawn probe + broker-truth runbook — BUILT+TESTED 16-Jul, UNPUSHED (deploy off-market)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — alert-watcher respawn-loop FIX (Option a): BUILT + TESTED LOCAL, UNPUSHED, deploy OFF-MARKET.**
Written during market hours (trading service HALTED, planned pause — [[morning-verify-16jul]]).

**Root cause:** `alert-watcher.service` ran `--once` (default, no flag) + `Restart=always`+`RestartSec=10`
→ exited every pass → systemd respawned it ~every 10s (**101,570+ restarts**). Benign (F1 keeps alerts
delivering) but wasteful. Yesterday's F1 fixed the CRASH (exit-2→0), not the structural RESPAWN.

**Fix (ChatGPT-approved Option a), after an investigate-first checklist that PASSED (`--loop` is
production-ready):** switch the unit to the EXISTING `--loop` daemon (shipped P5) + `Restart=on-failure`.
- `deploy/systemd/alert-watcher.service`: `ExecStart … --loop`; `Restart=always`→`on-failure`;
  `TimeoutStopSec=10`→**35** (> `_SMTP_TASK_TIMEOUT_SEC=30`, drains an in-flight SMTP batch on stop);
  add `StartLimitIntervalSec=300`+`StartLimitBurst=5` (a real crash-loop trips → `failed`/LOUD).
- Interval = `alerts.watcher_interval_sec` default **60s** (real config field; cadence ~10s→60s is fine —
  email sentinel is the BACKUP; criticals also emit direct-to-Telegram). Single-instance = pidfile lock
  held for the whole loop lifetime. NO second invocation exists (no `.timer`, no cron; installer =
  `deploy/install_vm_services.sh` only). Repo-managed unit → deploy via push + install.

**Regression prevention (the monitor could call a respawning service HEALTHY):** the canary never read
`NRestarts`/`SubState` (zero usages repo-wide) and `check_sentinel_ingestion` stayed green while it churned.
Added a **5th canary path `respawn`** in `scripts/monitoring_canary.py`: pure `_classify_respawn` +
injectable `check_service_respawn` → NOT-healthy on `SubState=auto-restart` OR NRestarts +≥3 at >6/hr
between daily runs (state in `data_store/canary_service_state.json`); systemctl-missing degrades to
healthy-with-note. `scripts/preflight/checks/services.py` comment updated (alert-watcher no longer a
periodic-oneshot; `HEALTHY_STATES` unchanged so preflight still passes).

**#2 (ChatGPT refinement, folded into the branch):** respawn thresholds are now CONFIG-DRIVEN —
`alerts.respawn_restart_delta_threshold` (default 3) + `alerts.respawn_rate_per_hour_threshold`
(default 6.0) in `AlertsConfig` (`extra="forbid"`-safe); `run_canary` passes them to
`check_service_respawn`→`_classify_respawn`. **No YAML override = byte-identical to the old literals.**
YAML untouched (override-only); module constants stay as the direct/test fallback.

**Tests:** 111 pass (canary + alert_watcher + preflight + config_loader: +9 respawn +2 `--loop`
functional +2 threshold-override +2 config-default asserts); all 4 modules compile.

**Findings 2–4 + captures (in the report + SYSTEM_MAP):**
- **F2 paths:** PATHS.md + SYSTEM_MAP.md ALREADY correct (`/home/ubuntu/systems/trading-system`, venv
  `/home/ubuntu/systems/venv`, bare `~/trading-system.git`) — **no change needed there.** Residual stale
  sites: `DEPLOYMENT.md` `.env`/backups still `/home/ubuntu/trading-system/…` (flag → Rama confirm+fix
  off-market); stale `deploy/post-receive` dup (known record-don't-fix footgun).
- **F3:** 8-step **broker-truth verification before every manual intervention** runbook added to SYSTEM_MAP
  (MANDATORY): stop engine→verify stopped→read BROKER positions→compare vs DB→flatten ONLY broker-open→
  verify zero positions→verify zero pending orders→restart only when intended. **NEVER flatten from DB
  alone** (16-Jul: DB read ACI OPEN after SL filled → a DB flatten = naked short; regular orders have no
  broker OCO → manual action races the exit-manager unless engine stopped first).
- **F4:** boot auto-cleared the 15-Jul SOFT_KILL by design — confirm-benign in the 15-Jul EOD review.
- **Captures:** (1) NO live halt/flatten API (KillSwitch boot-only/in-memory → stop→set-kill→start→HALT
  exit-4; future arch decision). (2) pre-market time-sensitive tasks need >~4 min runway (SSH+path
  discovery ate today's kill window).

**Why:** a monitor that reports a churning service "healthy" is the exact blind spot the canary exists to
close; and a DB-driven flatten can open a naked short.
**How to apply:** deploy OFF-MARKET tonight per Section 4 of `docs/audit/alertwatcher_loop_fix_16jul2026.md`
(merge branch→main + push → reinstall unit → daemon-reload → restart alert-watcher → confirm
`active/running`, NRestarts flat → **SOAK several-hrs/24h: RSS + fd + thread + DB-conn all flat + SMTP/
Telegram forced-fail recovery (degraded marker set then cleared)** → then correct DEPLOYMENT.md `.env`/
backups paths ONLY after a VM `ls` confirm → rollback = revert unit). NOTHING pushed/restarted during
market hours.

Report `docs/audit/alertwatcher_loop_fix_16jul2026.md`. On branch **`alertwatcher-loop-fix-16jul`**
(**4 commits**: unit fix · canary respawn probe · docs · configurable thresholds — UNPUSHED); `main`
unchanged; VM==bare==`c9fb298` (still `--once`+always until the off-market deploy — Rama: merge
branch→main + push off-market tonight).
[[morning-verify-16jul]] [[unpushed-pending-deploy-ledger]] [[monitoring-hardening-15jul]] [[deploy-done-16jul]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 1788 B (budget 450 B). The index now carries a hook and this link.

- 🔧🟡🔝 **[16-Jul ALERT-WATCHER --loop FIX — BUILT+TESTED LOCAL, UNPUSHED (deploy OFF-MARKET)](alertwatcher_loop_fix_16jul.md)** — root cause: `alert-watcher.service` = `--once`+`Restart=always`+`RestartSec=10` → systemd respawned it ~every 10s (**101,570+ restarts**; benign, F1 keeps alerts flowing). **Fix (Option a, after an investigate-first checklist that PASSED):** unit → **existing `--loop` daemon** + `Restart=on-failure` + `TimeoutStopSec=35` + `StartLimit 5/300s`; interval=`watcher_interval_sec` 60s; single-instance pidfile lock for the loop lifetime; NO 2nd invocation exists (no timer/cron). **Regression prevention:** the monitor could call a respawning service HEALTHY (canary never read `NRestarts`/`SubState`; 0 usages repo-wide) → added a **5th canary path `respawn`** (`_classify_respawn`+`check_service_respawn`: auto-restart OR +≥3 restarts >6/hr → NOT-healthy; state `data_store/canary_service_state.json`). **#2 (ChatGPT): respawn thresholds now config-driven** (`alerts.respawn_restart_delta_threshold` 3 / `respawn_rate_per_hour_threshold` 6.0; defaults byte-identical). Tests **111 pass**; branch 4 commits. **F2 paths:** PATHS.md+SYSTEM_MAP.md already correct (residual = `DEPLOYMENT.md` `.env`/backups + stale `deploy/post-receive` dup — flag). **F3:** 8-step **broker-truth-before-manual-intervention** runbook → SYSTEM_MAP (NEVER flatten from DB alone — 16-Jul ACI read OPEN after SL filled → a DB flatten = naked short; regular orders have no broker OCO). **F4:** boot auto-cleared 15-Jul SOFT_KILL by design. **Captures:** no live halt/flatten API (KillSwitch boot-only); pre-market tasks need >4-min runway. Report `docs/audit/alertwatcher_loop_fix_16jul2026.md`. [[morning-verify-16jul]] [[unpushed-pending-deploy-ledger]]
