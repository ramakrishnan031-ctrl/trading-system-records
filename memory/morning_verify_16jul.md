---
name: morning-verify-16jul
description: 16-Jul first live boot on c9fb298 verified clean; planned-pause SOFT_KILL applied → system HALTED (exit-4); book flat at broker
metadata: 
  node_type: memory
  type: project
  originSessionId: ae4c0f99-744c-4ada-b426-6f05252962a4
---

**16-Jul-2026 morning verify + planned-pause soft-kill (operator-directed; read-only verify + one operational kill; NO code changes).** Report `docs/audit/morning_verify_16jul2026.md`.

**FIRST LIVE BOOT on the 15-Jul combined deploy = CLEAN.** VM/bare HEAD `c9fb298`, tag `deploy-15jul-combined` present; schema **v44** (`schema_meta`; the `PRAGMA user_version=0` is a red herring — app tracks version in its own table); 08:15 boot no-migration/no-abort (`ExecMainStatus=0`, `NRestarts=0`); token auto-refreshed 08:15; **monitoring fixes WORKING** — canary 08:20 ALL GREEN incl **`✅ email: SMTP login OK`** (F0 restore holds), telegram valid, sentinel 0, dashboard active. Boot auto-cleared yesterday's stale `SOFT_KILL(circuit_breaker_force_close_15:15, by order_monitor)`.

**⚠️ PRE-MARKET WINDOW MISSED** (task picked up 09:56; SSH latency + wrong-path discovery ate the ~4-min runway). System ran a live session from 10:00 and took **3 trades — all closed cleanly by the engine**: ACI (stopped out SL 10:17), **HUHTAMAKI (hit TGT, win, 10:48)**, PRAVEG (closed 10:48); MRPL rejected ×2 by the slippage guard. **Book verified FLAT at the BROKER** (`positions()` net nonzero=0; buys=sells per symbol → no manual Kite short; holdings 0).

**SOFT_KILL applied 10:54:28** (mechanism: stop→set via `KillSwitch.soft_kill()`→start; reason **"planned pause for pending fix/review work — no trading issue"**, triggered_by=`operator`). Result: boot detected the active same-day kill → `startup_scenario=HALT` → **exit-4** (designed halt-on-active-kill, Audit Issue #18). `RestartPreventExitStatus=3 4` → systemd does NOT restart on 4 → service settled `failed`, **stable, no flap**.

**Why (current system state for the NEXT session):** trading-system.service is **HALTED / down (exit-4)** with **SOFT_KILL active** — this is the intended planned pause, NOT a crash. Independent monitoring/EOD crons (canary, cron_officer 09:20, eod_cleanup 15:50, eod_verify 15:55, backups) run regardless → EOD emails + visibility continue.

**How to apply / KEY operational facts:**
- **No live halt/flatten API.** KillSwitch loads state at `__init__` only (in-memory `is_active()`); ports 8080=health-GET, 5001=instance-lock, GUI-control WIP. So a soft-kill requires a **restart**, and **an active kill at boot HALTS the service (exit-4)** — there is NO "running-but-soft-killed" state at startup.
- **Resume:** `deploy/resume.sh` (stop→clear→start) or `scripts/clear_kill_switch.py`+start; OR it **auto-clears tomorrow 08:15** (`clear_stale_state` wipes prior-day kills → clean start). Same-day operator kills survive boot; `auto_clear_scheduled_kill` only clears force_close/EOD_squareoff reasons.
- **DB status can LAG broker truth** — ACI showed `OPEN` for minutes after its SL had filled; a naive DB-driven flatten would have opened a naked short. Flatten against broker truth with the exit-manager stopped (LIMIT_TRIPLE OCO is software-enforced; Zerodha regular orders have no broker OCO).
- **Live working tree = `/home/ubuntu/systems/trading-system`** (venv `/home/ubuntu/systems/venv`); bare `~/trading-system.git`.

**Findings (NOT fixed — follow-up):** 🔴 **alert-watcher respawn loop** (pre-existing, non-trading) — `alert-watcher.service` `Restart=always` + script exits 0 every ~10s → ~101,570+ restarts; F1 fixed the crash (exit 2→0) but the unit-level loop persists benignly (canary paths still green). Recommend oneshot+timer / RemainAfterExit fix.

⏰ **Rama:** system is intentionally paused today; resume when ready (or it self-heals at 08:15 tomorrow). Confirm 16-Jul EOD emails arrive (cron-driven, unaffected by the halt). See [[unpushed-pending-deploy-ledger]] · [[deploy-done-16jul]] · [[monitoring-hardening-15jul]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 1402 B (budget 450 B). The index now carries a hook and this link.

- ⏸️🟢🔝 **[16-Jul MORNING VERIFY + PLANNED-PAUSE SOFT_KILL — system HALTED; deploy verified clean on first live boot](morning_verify_16jul.md)** — First live boot on `c9fb298` **CLEAN** (schema v44, no-migration, token 08:15, **canary 08:20 ALL GREEN incl `✅ email` — F0 SMTP restore holds**). **⚠️ Pre-market kill window MISSED** (task@09:56) → ran a **live session from 10:00**, took **3 trades all closed cleanly by the engine** (ACI SL-out · **HUHTAMAKI TGT-win** · PRAVEG; MRPL rejected×2 slippage); **book verified FLAT at the BROKER** (buys=sells per symbol → no manual Kite short). **SOFT_KILL applied 10:54:28** (operator, "planned pause… no trading issue") → boot `startup_scenario=HALT` → **exit-4** (designed halt-on-active-kill, Audit #18; `RestartPreventExitStatus=3 4` → stable, no flap). **KEY:** no live halt/flatten API (KillSwitch in-memory, loaded at boot) → soft-kill needs a restart, and **an active kill at boot HALTS the service (down), NOT running-but-halted.** Resume = `deploy/resume.sh`, or auto-clears 08:15 (`clear_stale_state`). **Findings:** alert-watcher respawn loop (→ now fixed); live tree = `/home/ubuntu/systems/trading-system`; **DB status LAGS broker truth** (ACI naked-short trap avoided → the 8-step broker-truth runbook). Report `docs/audit/morning_verify_16jul2026.md`. [[morning-verify-16jul]] [[deploy-done-16jul]]
