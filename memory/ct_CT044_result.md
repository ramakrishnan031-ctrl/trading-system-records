---
name: ct-ct044-result
description: "CT044 Single Capital Allocation: PASS — reserve succeeded, available decreased, total unchanged, margin matches"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT044 | Single Capital Allocation Happy Path | PASS | 08-Jun-2026

**Test:** Isolated FM (100K broker balance). Reserve RELIANCE 10 shares at 2500.
**Results:** 4/4 checks pass. Reserve succeeded (rid=3a84..., margin=5250). Available decreased 70K→64.75K. Total unchanged at 100K. Margin matches decrease exactly. Invariant A holds.
