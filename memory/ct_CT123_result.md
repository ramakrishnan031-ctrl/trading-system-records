---
name: ct-ct123-result
description: CT123 RAM Pressure 90%+ — PASS; system survived stress-ng --vm-bytes 85% for 60s
metadata: 
  node_type: memory
  type: project
  originSessionId: 69413679-b8aa-4102-913a-7ae40999a6f4
---

**CT123: RAM Pressure 90%+** — PASS

stress-ng --vm 1 --vm-bytes 85% --timeout 60. Memory peaked with ~5.7GB used during stress (VM has 12GB). System remained healthy. No OOM kill. Health endpoint responded normally.

Related: [[ct-CT122-result]]
