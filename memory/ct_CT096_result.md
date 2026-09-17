---
name: ct-ct096-result
description: "CT096 SIGKILL Idle — PASS; systemd auto-restart, rehydration runs, healthy in ~15s"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT096: SIGKILL — Idle** — PASS

SIGKILL sent to main.py while idle (0 positions, 0 orders). Systemd auto-restarted (Restart=on-failure). System detected WARM scenario (recent SHUTDOWN marker from prior graceful stop). Rehydration completed: 0 orders, 0 trades, fm total=1000000.0.

RTO: ~15s (kill to healthy endpoint responding).

Related: [[ct-CT093-result]] [[ct-CT097-result]]
