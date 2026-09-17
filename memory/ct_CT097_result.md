---
name: ct-ct097-result
description: "CT097 SIGKILL with active trades (CRITICAL) — PASS_WITH_RISK; DB survives, WAL recovery works, no data loss"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT097: SIGKILL with Active Trades (CRITICAL)** — PASS_WITH_RISK

- 2 OPEN trades (THOMASCOOK, PANACEABIO) at time of SIGKILL
- `PRAGMA integrity_check` = ok immediately after kill
- WAL file recovered (2.2MB → 2.3MB, no corruption)
- THOMASCOOK trade preserved as OPEN in DB
- PANACEABIO CLOSED_MANUAL by reconciler during startup
- System enters HALT loop: CHECK9 MISSING_EXITS → SOFT_KILL → exit code 4 → systemd restart → repeat
- **No data loss or corruption** — SQLite WAL + FULL synchronous works as designed
- **Risk:** Paper mode limitation causes restart loop requiring operator intervention (--resume)
- In live mode: broker retains positions, CHECK9 wouldn't flag missing exits
- **RTO:** Depends on operator response time (automated restart alone loops)
- **Tested:** 2026-06-09 ~09:59 IST
