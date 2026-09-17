---
name: ct-ct122-result
description: CT122 CPU Stress 90%+ — PASS; system healthy at 100% CPU for 60s
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT122: CPU Stress 90%+** — PASS

stress-ng --cpu $(nproc) --timeout 60 drove CPU to 100%. System remained healthy throughout. Health endpoint responded normally. No crash, no timeout, no kill switch activation.

Related: [[ct-CT123-result]]
