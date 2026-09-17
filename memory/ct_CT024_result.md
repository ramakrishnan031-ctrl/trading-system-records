---
name: ct-ct024-result
description: "CT024 Burst 50 in 5s: PASS — all 50 accepted, queue handled, no crash, latency 3-38ms"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT024 | Burst — 50 Signals in 5s | PASS | 08-Jun-2026

**Test:** 50 signals at 100ms intervals (15 real symbols + 35 synthetic STOCK001-STOCK035).

**Results:** All 50 HTTP 200 ACCEPTED. Queue depth peaked and drained to 0 within seconds. 35 synthetic → SKIPPED_QUOTE_UNAVAILABLE, 15 real → DUPLICATE (already sent today). No queue warning, no backpressure, no memory issues. Latency: 3-38ms per request.
