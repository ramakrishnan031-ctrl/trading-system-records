---
name: Deployment status (Oracle Cloud VM)
description: VM deployment state — commit parity, systemd posture, pending credential rotation.
type: project
originSessionId: 2462c83a-f3d2-4e65-8d6f-b5fd7ebe539c
---
Deployment state as of **25-Apr-2026**. PC = VM at commit **13b3d09** with **1713/1713 tests green** on PC. systemd units present but DISABLED (will enable only after paper weeks complete).

**Why:** During paper trial, Rama runs the system from the PC (with ngrok tunnel to Chartink) so he can watch live. VM is kept in lock-step via `git push vm main` but not running the service. Switch to VM-headless execution is a post-paper step.

**How to apply:** Do not enable systemd on VM during paper trial. Push code to VM after each commit for parity, but execution stays on PC. After Week 3 code-freeze rehearsal passes, switch execution to VM and enable systemd units.

## VM facts (current)
- IP: **80.225.198.195**, SSH alias: `trading-vm`, user: ubuntu
- Python 3.14.4 venv at ~/trading-system/venv/
- requirements.txt + requirements-dev.txt installed
- Bare repo at /home/ubuntu/trading-system.git with post-receive hook
- Latest checkout update: **17:19 IST 25-Apr-2026** (commit 13b3d09)
- .env present on VM — Zerodha creds NOT rotated yet (only rotate when VM becomes execution host)

## Commit parity protocol
- `git push vm main` via `GIT_SSH="$(which ssh)" git push vm main`
- post-receive hook auto-checkouts main → working tree updates
- Confirm parity with: `ssh trading-vm 'cd trading-system && git rev-parse HEAD'`

## systemd state
- `/etc/systemd/system/trading-system.service` — **DISABLED**
- `/etc/systemd/system/alert-watcher.service` — **DISABLED**
- Enable command (post-paper): `sudo systemctl enable --now trading-system alert-watcher`

## Test counts
- PC: **1713/1713 green** (commit 13b3d09, 25-Apr; +34 vs Phase A 1679)
- VM: not re-run this push; last full run 1413/1413 at 18-Apr deployment
  Re-run before switching execution host.

## Audit closure (pre-live)
- All audit fixes from `deep_system_audit_2026-04-24` complete for pre-live
- Phase A (P0 blockers, 7 items): commit **9b7bcda** 24-Apr
- Phase B (P1 items, 6 items): commit **13b3d09** 25-Apr
- Phase C (P2, 3 items): deferred post-live — WAL cron, 5-min dedup, smart-target intra-minute
- Phase D (INFO, 2 items): doc-only pending — NTP slew note, connection-leak misdiagnosis

## Remaining pre-VM-exec actions (post paper-trial)
1. Rotate Zerodha credentials (API key + secret) in Kite developer console
2. SCP fresh `.env` to VM
3. Add Oracle Cloud security list rule: TCP 5000 ingress
4. `pytest tests/ -q` on VM to re-confirm 1713 green
5. `systemctl enable --now` both units
