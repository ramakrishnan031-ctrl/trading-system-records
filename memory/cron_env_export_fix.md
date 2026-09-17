---
name: cron_env_export_fix
description: "Cron jobs need `set -a && . ./.env && set +a` to export .env secrets to Python; a plain `. ./.env` silently gives them NO secrets"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 34eb8dba-9799-4234-a8dc-bb8ca1411fa8
---

**CRITICAL CRON FACT (fixed 2026-06-19, commit bff0cad).** `.env` uses bare
`VAR=value` (no `export`). The cron pattern `cd … && . ./.env && python …` sources
the file into the shell but does **NOT** export those vars to the child `python`
process — so **every cron job ran without any `.env` secret**
(`ZERODHA_API_KEY_LFL836`, `TELEGRAM_BOT_TOKEN`/`CHANNEL_PRIMARY`, `GEMINI_API_KEY`).
Proven empirically on the VM: under `. ./.env && python` all vars are MISSING; under
`set -a && . ./.env && set +a` they are SET.

This was the **true root cause** of the 19-Jun 15:45 `reconcile_positions` FAILED
(broker creds "must be set") AND its "Telegram env not set" — same cause. [[fix_189_dash_cron_overnight]]
fixed "jobs die before Python" (dash `. .env`); this is the NEXT layer — jobs RUN but
get no secrets. It only surfaced because FIX-189 first made crons actually execute.

**Fix:** every Python cron line now sources via **`set -a && . ./.env && set +a`**
(allexport). Applied to all 29 lines in `deploy/cron/trading-system.cron`; documented
in `config/cron_registry.yaml` header; enforced by
`tests/unit/test_cron_registry.py::TestCronEnvExport`. Crontab **reinstalled** on VM
(backup in `data_store/crontab_backups/`). **KEEP THE WRAPPER on any cron
regeneration** (like the FIX-189 `SHELL=/bin/bash` + `. ./.env` rule).

NB: `GEMINI_API_KEY` is genuinely absent from `.env` (separate gap — gemini cron auth
still needs it added). The systemd SERVICE is unaffected (it uses `EnvironmentFile=.env`
+ drop-in, which DO export). Related: [[eod_investigation_19jun]], [[deploy_requires_restart]].
