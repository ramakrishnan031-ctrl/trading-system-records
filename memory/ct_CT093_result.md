---
name: ct-ct093-result
description: "CT093 SIGINT Idle — PASS; clean 4s shutdown: SHUTDOWN event, WAL checkpoint, exit 0"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT093: SIGINT — Idle** — PASS

Graceful shutdown via `systemctl stop` (SIGINT):
- Signal 2 received → shutdown initiated
- order_monitor shutdown: 0 cancelled
- WAL checkpoint: 66 pages checkpointed
- Shutdown complete in ~4s
- Systemd: "Deactivated successfully"
- RTO: 4s (target: 15s max)

Post-restart: WARM scenario, system healthy.

Related: [[ct-CT096-result]]
