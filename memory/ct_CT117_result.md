---
name: ct-ct117-result
description: CT117 WAL Recovery After SIGKILL — PASS; marker survived kill -9 + auto-restart
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT117: WAL Recovery After SIGKILL** — PASS

Inserted CT117_MARKER into system_events, sent SIGKILL to main.py process. Systemd auto-restarted (Restart=on-failure). After restart, CT117_MARKER was present in DB — WAL recovery intact.

SQLite WAL + FULL synchronous mode ensures committed data survives process crashes.

Related: [[ct-CT103-result]]
