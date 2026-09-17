---
name: New VM deployment 2026-05-01
description: Fresh Oracle Cloud VM at 129.154.253.244 replacing previous VM; full deployment in progress
type: project
originSessionId: c910234e-44b9-477d-a807-36a11a946561
---
New VM deployed at 129.154.253.244 on 2026-05-01.

**Why:** Fresh start for trading system deployment - previous VM replaced.

**How to apply:** All VM operations should target this IP. SSH key: trading_vm_secure (passwordless).

## Deployment checklist (ALL COMPLETE)
- [x] Initial setup (user: trading, dirs: ~/app, ~/logs, ~/data)
- [x] Bare git repo (/home/trading/trading-system.git)
- [x] systemd service (trading-system.service - enabled)
- [x] Code deployment (commit c98a3fd)
- [x] Dependencies (Python 3.12.3 venv with all packages)
- [x] Firewall (UFW: 22/tcp + 5000/tcp)
- [x] Cron jobs (daily report 16:00 UTC, log cleanup midnight)

## Access
- SSH: `ssh -i ~/.ssh/trading_vm_secure trading@129.154.253.244`
- Git push: `$env:GIT_SSH_COMMAND = 'ssh -i C:/Users/rama/.ssh/trading_vm_secure'; git push vm main`

## Notes
- Webhook runs as thread inside main.py (no separate service)
- Service not started yet - needs config files and token

## Setup fixes applied 2026-05-03
- Timezone set to Asia/Kolkata (IST, +0530) via ubuntu user
- venv activation added to trading user ~/.bashrc
- Crontab recreated with correct IST times:
  - 16:00 IST Mon-Fri: daily_review report
  - 05:00 IST daily: rm zerodha_token.json (stale token cleanup)
  - 00:00 IST daily: log cleanup (>30 days)
- cron restarted to pick up new timezone
- sudo for timedatectl requires ubuntu user (trading user has no passwordless sudo)

## Changes deployed 2026-05-01
- 1091dad: friendly holiday notification terminal message
- 9bd9e5d: get_holiday_name() in holiday_guard.py
- 6fea9ee: tests for holiday notification
