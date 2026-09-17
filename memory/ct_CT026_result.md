---
name: ct-ct026-result
description: "CT026 Sustained Load 10min: PASS — 120 signals at 5s intervals, all terminal, queue stable, no memory growth"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT026 | Sustained Load — 1/5s for 10 min (120 signals) | PASS | 08-Jun-2026

**Test:** 120 signals at 5s intervals over 10 minutes (09:54:45 → 10:04:41). Mix of 15 real symbols + synthetic STOCK051-STOCK120.

**Results:** 120/120 HTTP 200. 50 ACCEPTED (new), 70 DUPLICATE (reused from CT025 flood). All reached terminal status. Queue depth stayed at 0/300 throughout — no accumulation. Latency: 2.9-40ms. System remained healthy with 7 open trades processing simultaneously.
