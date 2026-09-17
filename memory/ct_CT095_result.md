---
name: ct-ct095-result
description: "CT095 SIGINT during signal processing — PASS; signal cleanly marked REJECTED_SHUTDOWN, no half-processed state"
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT095: SIGINT During Signal Processing** — PASS

- Injected MARUTI signal, sent SIGINT 0.3s later
- Signal accepted by webhook (HTTP 200)
- Signal status in DB: `REJECTED_SHUTDOWN: System shutdown before placement`
- No trade created, no half-processed state
- DB integrity: ok
- Graceful shutdown handled in-flight signal correctly
- **Tested:** 2026-06-09 ~10:02 IST
