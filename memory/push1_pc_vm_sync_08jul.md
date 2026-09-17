---
name: push1_pc_vm_sync_08jul
description: PUSH-1 PC=VM sync COMPLETE — main 9bcc1eb (infra+A-3) DEPLOYED+RESTARTED+VERIFIED on VM 08-Jul ~19:58 IST; C-4 chmod applied; 4 spot-checks pass; schema still 41; SYSTEM_MAP doc-sync still owed
metadata: 
  node_type: memory
  type: project
  originSessionId: 0e32bad3-6610-4e3c-a772-6502eeb354b4
---

**PUSH-1 (full PC=VM sync) — FULLY DEPLOYED + VERIFIED 08-Jul ~19:58 IST (off-market).** The two 08-Jul builds (infra low-sev C-3/C-4/F-1/E-4 + A-3 entry-kill TOCTOU) consolidated onto `main` and deployed live. Resumed after an unplanned mid-task PC power loss (git state survived; Part B suite re-run clean → GO). Rama authorized VS Code Claude to execute the push + restart directly (his `[Rama]` gates delegated with explicit consent).

**Part B (regression gate):** consolidated suite on `9bcc1eb` = **11F/4355P/15S == baseline's 11 pre-existing PC-env fails, 0 new** (+16P/+2S = the 18 tests the 2 commits added, all green/POSIX-skip). Py3.11.9 real-deps (`C:\python311`). Deploy preflight PASS (PC/VM UTC skew 1s; VM market CLOSED). GO.

**Part C (push + restart) — DONE + VERIFIED:**
- `git push origin main`: `271d24f..9bcc1eb`, exit 0. Post-receive: "Deploying… crontab AUTO-INSTALLED from canonical… Deployment complete" (crontab idempotent no-op — neither commit touched `cron_registry`).
- VM bare repo HEAD → `9bcc1eb` (chain 9bcc1eb→dd4f3f4→271d24f); working tree checked out.
- `sudo systemctl restart trading-system.service` (over SSH, passwordless sudo, rc=0): fresh `ExecMainStartTimestamp 08:15:12→**19:58:57 IST**`; boot `active/running`→`inactive/dead`; `Result=success ExecMainStatus=0 NRestarts=0`. Journal: "Started… **Outside service window [08:00-16:00 IST]; current IST 19:58. Not starting (clean exit 0)**… Deactivated successfully." Early service-window guard exit = clean → validates imports+startup; **full component/schema init runs at tomorrow's in-window 08:15 auto-boot** (system's off-market design — NOT forced past with TS_IGNORE_MARKET_WINDOW). 0 ERROR/CRITICAL in journal + app-log.
- **schema_version STILL 41** (live DB `schema_meta`=41; deployed `schema.sql:1474`='41'). P1 correctly absent.

**Part D (chmod + spot-checks) — DONE:**
- **4 spot-checks CONFIRMED in the DEPLOYED code:** C-3 `scripts/healthcheck_server.py:267` `host="127.0.0.1"` (comment "Was 0.0.0.0") + `:44` `account_present` scrub · E-4 `daemon_liveness_provider` wired into `/health` (`:66`/`:112-119`, 503-on-dead) + `def is_alive()` on `eod_squareoff:280`/`order_reconciler:397`/`order_monitor:519` · F-1 `main.py:1761` `min_free_disk_gb=app_config.system.logging.min_free_disk_gb` (nested, not the 1.0 fallback) · A-3 `orders/order_placer.py:1229` second `is_active("entry")` re-check → `:1231` `"kill_switch_active_last_mile_presubmit"` (OP-LM1 early-out kept @944).
- **C-4 chmod applied:** live token `data_store/session/zerodha_token.json` 0664→**0600**, session dir 0775→**0700** (both rc=0). (Next 08:15 refresh rewrites 0600 anyway.)

**DOC-SYNC DONE (`005c007`, pushed):** `docs/SYSTEM_MAP.md` changelog entry (infra/A-3/Wave-5 + PUSH-1 deploy) committed + pushed → PC=VM 100% (git status clean, 0 ahead of origin). All "pending off-market doc-sync" flags CLEARED. P1 (`wave4-p1-v2`) untouched on its own branch.

Build detail: [[a3_kill_recheck_investigation_08jul]] · [[infra_lowsev_c3c4f1e4_08jul]] · [[full_repo_audit_04jul_pending]]
