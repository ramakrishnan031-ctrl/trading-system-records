---
name: ct-ct094-result
description: "CT094 SIGINT with active trades — PASS_WITH_RISK; graceful 4s shutdown, trades preserved, paper adapter SOFT_KILL on restart"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT094: SIGINT with Active Trades** — PASS_WITH_RISK

- 2 OPEN trades (JNKINDIA) at time of SIGINT
- Graceful shutdown completed in ~4 seconds
- `entry_cancelled_zero_fill` for PENDING orders — correct behavior
- DB integrity maintained (WAL mode + FULL synchronous)
- On restart: CHECK1 CLOSED_MANUAL'd both trades (paper adapter lost in-memory state)
- CHECK9 MISSING_EXITS → SOFT_KILL (protective; live mode would retain broker positions)
- **Risk:** Paper mode can't preserve positions across restart; requires manual kill switch clear
- **RTO:** 4s shutdown + 10s systemd restart + operator clear ≈ 15-20s
- **Tested:** 2026-06-09 ~09:57 IST
