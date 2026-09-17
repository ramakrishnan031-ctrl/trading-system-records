---
name: Next session context - 12-May-2026 onwards
description: System LIVE since 11-May; double-release fixed; audit Phase 1-13 pending; monitor 12-May for clean run
type: project
originSessionId: 3240cc27-d911-4827-864b-d5427aec0c5f
---
**Status: LIVE since 11-May-2026** (Rs 25K micro capital)

## Current state (12-May-2026)
- Commit: 4ef614e (double-release root cause fix)
- Tests: 1795 green
- VM: 161.118.187.249, ubuntu, systemd active
- Path: /home/ubuntu/systems/trading-system/
- SSH: `ssh trading-vm`

## Monitoring 12-May
- No HARD_KILL (the double-release was causing these)
- No double capital release (root cause fixed in zerodha_adapter paper positions)
- Capital releases exactly once per trade close
- EOD fires at 15:17

## Pending work
- Audit files Phase 1-13: systematic fix session needed
- Config drift validator (identified 28-Apr as CRITICAL post-paper priority)
- Phase C deferred items: WAL cron, 5-min dedup, smart-target intra-minute
- Phase H chaos suite (deferred)

## Key commands
- Service status: `ssh trading-vm "systemctl status trading-system"`
- Tail logs: `ssh trading-vm "tail -50 ~/systems/trading-system/logs/system_$(date +%Y-%m-%d).log"`
- DB state: `ssh trading-vm "cd ~/systems/trading-system && python3 scripts/check_vm_state.py --health"`
- Kill switch: `ssh trading-vm "cd ~/systems/trading-system && python3 scripts/check_vm_state.py --cleanup-orders"`

## Temporary configs still active (REVERT WHEN STABLE)
- max_consecutive_losses: 20 (was 4)
- daily_loss_limit_pct: 1.00 (was 0.05)
- _INVARIANT_TOLERANCE: 100.0 (was 0.01)
- capital_drift_tolerance: 100000 (was 50)
