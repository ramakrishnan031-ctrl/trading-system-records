---
name: ct-ct046-result
description: "CT046 Capital Exhaustion: PASS — 8 reserves then clean rejection; no capital leak; invariant A"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT046 | Capital Exhaustion | PASS | 08-Jun-2026

**Test:** Isolated FM (50K broker balance, 35K intraday). Reserve loop until exhaustion.
**Results:** 5/5 checks pass. 8 reserves succeeded (8×4200 = 33.6K used). 9th rejected: "Insufficient intraday capital: need 4200.00, have 1400.00". Extra attempt also rejected. Total unchanged at 50K — no capital leak. Invariant A holds.
