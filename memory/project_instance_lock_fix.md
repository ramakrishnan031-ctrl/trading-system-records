---
name: Single instance enforcement (commit ab2c6d2)
description: PID lock + port check prevents stale process port conflicts; Restart=on-failure prevents holiday alert loops; deployed 2026-05-05
type: project
originSessionId: 39f954e1-db94-431b-a77f-bdc2fccd375d
---
## Bug (2026-05-05): No webhooks received all day

Manual `python main.py --resume` from May 4 held port 5000. Systemd-managed process (PID 21371) started fresh today but couldn't bind port 5000 → zero Chartink webhooks received.

## Fixes (2 commits)

### Commit 398dbae: systemd restart loop + path alignment
- `Restart=always` → `Restart=on-failure` + `RestartPreventExitStatus=3`
- All deploy/ paths updated to `/home/ubuntu/systems/trading-system/`
- Prevents infinite holiday/weekend alert spam

### Commit ab2c6d2: single instance enforcement
- **GUARD 1**: `check_port_available()` before webhook thread — exits 1 if port occupied
- **GUARD 2**: PID lock file `/tmp/trading-system.lock` — prevents duplicate instances
- Lock released via try/finally wrapping `_main_locked()`
- `main.py` split: `main()` = lock wrapper, `_main_locked()` = full body

## Key rule
**NEVER run `python main.py --resume` without `sudo systemctl stop trading-system` first.**
Stale processes from manual runs will hold port 5000 and silently eat all webhooks.

**Why:** Single instance enforcement is the only reliable way to prevent "system looks healthy but gets no signals" failures.

**How to apply:** If health check shows `kill_switch_active: true` or webhook test works locally but Chartink signals don't arrive — check `ps aux | grep main.py` for stale processes.
