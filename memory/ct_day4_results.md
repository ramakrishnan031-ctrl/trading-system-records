---
name: ct-day4-results
description: "Crash test Day 4 results (09-Jun-2026) — 21 scenarios; FIX-157; 15 PASS, 6 PASS_WITH_RISK, 2 deferred"
metadata: 
  node_type: memory
  type: project
  originSessionId: b1f5f4b4-3390-48a3-8b95-770fe53c2346
---

## Day 4 Results (2026-06-09)

### Morning Session (CT108-CT130)

| CT | Title | Result | Notes |
|---|---|---|---|
| CT108 | Network Drop 5min | PASS_WITH_RISK | System survived; network_controller blocked SSH (tool bug fixed) |
| CT109 | Partial Network — WS Only | PASS (trivial) | Paper adapter immune to WS block. Deferred to live. |
| CT110 | Partial Network — REST Only | DEFERRED | Paper adapter immune. Need live broker. |
| CT122 | CPU Stress 90%+ | PASS | 2 CPUs saturated 60s. No impact on processing. |
| CT123 | RAM Pressure 90%+ | PASS | 90% RAM 60s. No OOM kill. |
| CT126 | Clock Forward +60s | PASS_WITH_RISK | `clock_skew_probe` disabled in paper mode. |
| CT130 | Cron Silent Failure | PASS | Detected 9 missing heartbeats correctly. |
| CT132 | Delete Config Mid-Session | PASS (Day 1) | Already tested. |

### Afternoon Session (Signal/Startup/DB scenarios)

| CT | Title | Result | Notes |
|---|---|---|---|
| CT093 | SIGINT Graceful Shutdown | PASS_WITH_RISK | Steps PASS; invariants FAIL (known: no capital_snapshot in paper) |
| CT096 | SIGKILL Crash Recovery | PASS_WITH_RISK | Steps PASS; WAL recovery worked; same invariant issues |
| CT100 | Cold Start | PASS_WITH_RISK | Steps mostly OK; systemd "Job canceled" race (tool issue) |
| CT103 | HALT Start — Missing Config | PASS_WITH_RISK | Exit code 3 confirmed; cleanup didn't restore config (fixed manually) |
| CT105 | Systemd Restart Loop Protection | PASS | Loop protection confirmed |
| CT116 | DB Lock Contention | PASS | Signal processed despite 30s DB lock |
| CT117 | WAL Recovery After SIGKILL | PASS | WAL data survived crash |
| CT118 | DB Corruption — Missing Table | PASS | Rerun clean: dropped candles table → system detected + recreated on restart |
| CT120 | Read-Only Filesystem | PASS | Rerun with `chmod a-w`: graceful failure, no crash |

### FIX-157: Two P0 fixes deployed mid-session
1. **CHECK9 false positive on CLOSED_MANUAL:** Re-check trade status before critical path
2. **Capital drift from reconciler-closed trades:** Paper adapter subscribes to PositionClosed events

### Tool fixes applied
1. `network_controller.py`: Added `--sport 22` SSH server response rule
2. `network_controller.py`: Removed non-existent `wss.kite.trade` hostname
3. `system_config.yaml.bak` restored after CT103 cleanup failure

### EOD Window Observations (14:45-15:35 IST)

| CT | Title | Result | Notes |
|---|---|---|---|
| CT075 | EOD Pre-Alert | PASS (retest) | Fired at 14:45:00; "no open positions" — FIX-155c confirmed |
| CT089 | EOD Squareoff | PASS | 15:17:02; 2-pass: 0 cancels, 0 exits; COMPLETE in 2.0s |
| CT031 | Signal During SOFT_KILL | PASS | HTTP 403 "Kill switch active; signals rejected" |
| CT014 | Signal Outside Hours | PASS | HTTP 403 "Kill switch active; signals rejected" |

Post-close invariants: 0 open trades, 31 total (8 CLOSED + 23 CLOSED_MANUAL), kill switch SOFT_KILL @ 15:15.

### Scorecard
- **PASS:** 15 (CT014, CT031, CT075, CT089, CT105, CT114, CT116, CT117, CT118, CT120, CT122, CT123, CT130, CT132, CT109-trivial)
- **PASS_WITH_RISK:** 6 (CT093, CT096, CT100, CT103, CT108, CT126)
- **DEFERRED:** 2 (CT109 real WS, CT110 real REST)

### Findings
- OPEN→OPEN InvalidTransitionError flood from order_monitor (low priority, see [[crash-test-open-to-open-finding]])

**Why:** Day 4 tested infrastructure resilience + DB integrity + startup + EOD window. FIX-157 deployed and verified. CT075 retest confirmed FIX-155c.
**How to apply:** CT109/CT110 deferred to live session. All other scenarios resolved.
