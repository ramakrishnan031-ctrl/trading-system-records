---
name: ct-ct100-result
description: "CT100 Cold Start — PASS; detected as CRASH (same-day entries, no SHUTDOWN); all checks passed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT100: Cold Start** — PASS

Deleted all STARTUP/SHUTDOWN events to simulate cold start. System detected CRASH scenario (same-day entries but no SHUTDOWN event). This is correct behavior — true COLD would require empty DB.

All 14+ startup checks ran. Rehydration completed (0 trades, 0 orders). Capital from fm_ledger replay: 1000000.0. System healthy.

Related: [[ct-CT096-result]] [[ct-CT093-result]]
