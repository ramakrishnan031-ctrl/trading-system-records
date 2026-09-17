---
name: ct-ct045-result
description: "CT045 5 Concurrent Allocations: PASS — all 5 reserved in 16ms, unique rids, invariant A holds"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT045 | 5 Concurrent Allocations | PASS | 08-Jun-2026

**Test:** 5 threads reserve simultaneously (RELIANCE, INFY, TCS, HDFCBANK, SBIN at 1000/share).
**Results:** 4/4 checks pass. All 5 reserved in 16ms. 5 unique reservation_ids. Available decreased 70K→59.5K (5×2100 margin). Total unchanged. Invariant A holds. No lock contention.
