---
name: push1_runtime_validation_09jul
description: PUSH-1 (infra C-3/C-4/F-1/E-4 + A-3) FIRST full in-window runtime VALIDATED = PASS on 09-Jul-2026; PUSH-2 (P1 SHADOW) CLEARED
metadata: 
  node_type: memory
  type: project
  originSessionId: 079a8694-5552-4907-ae65-c573d090d444
---

**PUSH-1 runtime validation — VERDICT = PASS (Thu 09-Jul-2026 ~10:12 IST, live/market-open, READ-ONLY).**
First full in-window runtime of PUSH-1 (infra C-3/C-4/F-1/E-4 + A-3); prior it had only an off-market import-clean restart. Ran the operator runbook CHECK 1–4 on the VM.

**Context correction:** runbook said "deployed as working-tree 005c007", but VM bare-repo HEAD is actually **`9815786`** (the 08-Jul login merge) — that merge CARRIES PUSH-1 (infra+A-3) + the schema fail-fast + the GUI login. PUSH-1's code is live inside `9815786`, validated against that.

**Evidence:**
- CHECK 1 — `trading-system.service` active/running, `Result=success`, `ExecMainStatus=0`, **NRestarts=0**, fresh boot **08:15:11 IST** (past the market guard, ran clean through 09:15 open). Boot init clean; the one startup CRITICAL = documented-benign auto-clear (yesterday's 15:15 circuit-breaker SOFT_KILL → "new day starts clean"). No import/init/DB/SchemaVersionMismatch, no halt.
- CHECK 2 — schema_version = **41** (P1/v42 NOT deployed, as designed); `PRAGMA integrity_check = ok`.
- CHECK 3 C-3 — health listener bound **`127.0.0.1:8080`** (loopback, not 0.0.0.0). (webhook :5000 still 0.0.0.0 = known separate C-2 item, firewall-REJECTed externally.)
- CHECK 3 E-4 — `/health` → HTTP **200 "healthy"**, daemon liveness wired + gating (`order_monitor/order_reconciler/eod_scheduler/tgt_retry` ok; `live_feed` connected, non-gating); **`account_id` dropped** (payload = `account_present`+`expires_at` only). trades_today=7, uptime ~6996s.
- CHECK 3 F-1 — running `main.py:1761` reads `app_config.system.logging.min_free_disk_gb`; resolved value = **2.0** (not the old 1.0 fallback).
- CHECK 3 C-4 — token file `-rw-------` (**600**), dir **700**, **mtime 08:15:01 today** → proves the C-4 writer (`os.open(...,0o600)`+`chmod 0o600`) applied 0600 on this morning's refresh (not just a one-time chmod). C-4's "owed one-time chmod" is now moot.
- CHECK 4 A-3 — presubmit re-check present in running `order_placer.py:1214/1231` (`kill_switch_active_last_mile_presubmit`); **0 firings** (no SOFT_KILL mid-session → no over-block); **5 OPEN trades** placed+filled on the clean path (entries flow normally); 2 FAILED = benign broker MIS-block rejections (UNICHEMLAB "MIS orders blocked" + GAUDIUMIVF screener quote-unavailable), correctly NOT counted toward auto-trip (breaker is connectivity-only). No A-3/order_placer regression.

**⇒ PUSH-2 (P1 SHADOW) is CLEARED** for a later off-market window today (Thu evening onward). Rama runs the `push2_p1_shadow_deploy_runbook`; P1 branch is `wave4-p1-v3` @`a62ece5` (still UNMERGED/undeployed). Then STOP.

SYSTEM_MAP.md changelog entry HELD for the off-market doc-sync (market open, no mid-market push) — bundle with the next doc-sync. Fixed nothing (validation only). [[push1_pc_vm_sync_08jul]] [[infra_lowsev_c3c4f1e4_08jul]] [[a3_kill_recheck_investigation_08jul]] [[schema_version_failfast_08jul]] [[p1_reintegrated_failfast_main_08jul]] [[gui_redesign_screen01_login_08jul]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 313 B (budget 300 B). The index now carries a hook and this link.

- ✅🛡️🟢 **PUSH-1 runtime VALIDATED = PASS (09-Jul ~10:12 IST, live)** — infra C-3/C-4/F-1/E-4 + A-3 first in-window runtime all clean (service active/NRestarts=0 · schema 41+ok · E-4 /health daemon-gating · C-4 token 0600 · A-3 0-firings, 5 OPEN placed normally). [[push1_runtime_validation_09jul]]
