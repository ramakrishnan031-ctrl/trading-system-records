---
name: VM Directory Structure (LOCKED)
description: CRITICAL - final VM architecture; IP now 161.118.187.249 (was 161.118.188.171); use SSH alias `trading-vm`; multi-system layout; shared venv; ubuntu user; reference before ANY VM setup/deployment
type: project
originSessionId: 00972e13-adf4-462d-8fa4-5507eac59da8
---
# VM Architecture — LOCKED

## VM Details
- **IP**: 161.118.187.249 (CHANGED as of 18-Jun-2026; old IP 161.118.188.171 no longer reachable)
- **OS**: Ubuntu 24.04 (full, not minimal)
- **Specs**: 2 OCPU, 12GB RAM, 100GB disk
- **Timezone**: Asia/Kolkata (IST) — PERMANENT
- **User**: ubuntu (in trading group for file access)
- **SSH**: `ssh trading-vm` (alias in ~/.ssh/config → HostName 161.118.187.249, key trading_vm_secure). Always prefer the alias; the hardcoded IP drifts.
- **Active account**: LFL836 (api keys are account-scoped in .env: `ZERODHA_API_KEY_LFL836` etc.; token json at data_store/session/zerodha_token.json carries its own api_key + date + expires_at)

## Directory Structure

```
/home/ubuntu/
├── .bashrc                      # Auto-activates venv on login
├── systems/
│   ├── venv/                    # SHARED venv for ALL systems
│   ├── trading-system/          # Trading system v2
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── .env                 # Real credentials (not in git)
│   │   ├── alerts/ broker/ capital/ config/ core/ data/
│   │   ├── data_store/
│   │   │   ├── trading_system.db
│   │   │   └── session/zerodha_token.json
│   │   ├── deploy/ logs/ orders/ reports/ screening/
│   │   ├── scripts/ signals/ strategies/ utils/
│   │   └── .gitignore
│   └── [future-systems]/        # Room for expansion
```

**Git Bare Repo**: `/home/ubuntu/trading-system.git` → auto-deploys to `systems/trading-system/`

## Systemd Service
- `WorkingDirectory=/home/ubuntu/systems/trading-system`
- `ExecStart=/home/ubuntu/systems/venv/bin/python main.py`
- `Restart=on-failure` + `RestartPreventExitStatus=3`
  - Exit 0 (holiday guard / normal EOD): NO restart
  - Exit 3 (startup check failure): NO restart
  - Exit 1/2 (crash): restarts for mid-day recovery
  - NEVER use `Restart=always` — causes infinite holiday alert loop on weekends

## Cron Jobs (ubuntu user, IST times, see deploy/cron/trading-system.cron)
- `00 00 * * *` — daily log cleanup (>30 days)
- `00 01 * * *` — nightly SQLite backup → data_store/backups/
- `00 02 * * *` — 7-day rolling backup cleanup
- `00 05 * * *` — rm stale zerodha_token.json (daily)
- `00 16 * * 1-5` — daily EOD review report (xlsx + md) → reports/daily/YYYY-MM-DD/
- `01 16 * * 1-5` — screened stocks CSV → reports/daily_review/
- `00 18 * * 0` — weekly instrument master refresh (Sunday)
Last synced: 2026-05-09 (7 jobs, VM = canonical file)

## Files EXCLUDED from VM (PC-only)
venv/, tests/, .pytest_cache/, __pycache__/, .claude/, web_claude/, docs/, .env

## Files INCLUDED on VM
.gitignore, requirements.txt, requirements-dev.txt, DEPLOYMENT.md

## Venv Strategy
- Single shared venv at `/home/ubuntu/systems/venv/`
- Auto-activates on SSH login via .bashrc
- All future systems use same venv

**Why:** Multi-system ready architecture. Shared venv avoids duplication. ubuntu user simplifies sudo operations.

**How to apply:** ANY VM reset, restore, or new deployment MUST follow this exact structure. Reference this memory FIRST before any VM work.
