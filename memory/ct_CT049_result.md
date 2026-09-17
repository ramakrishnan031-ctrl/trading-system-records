---
name: ct-ct049-result
description: "CT049 Reserve Then Cancel: PASS — pipeline abort releases capital fully; invariant A"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT049 | Reserve Then Cancel (Pipeline Abort) | PASS | 08-Jun-2026

**Test:** Isolated FM. Reserve RELIANCE (margin=5250), then release (simulating kill switch before order placement).
**Results:** 5/5 checks pass. Reserve succeeded. Capital decreased (70K→64.75K). Release succeeded. Capital fully restored (64.75K→70K). Total unchanged. Invariant A holds. Simulates pipeline abort at any point between reserve and order placement.
