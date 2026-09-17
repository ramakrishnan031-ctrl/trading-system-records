---
name: ct-ct039-result
description: "CT039 Zero/Stale Price: PASS — price=0 rejected at edge; fake symbol SKIPPED_QUOTE; zero price=0 orders in DB"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT039 | Zero/Stale Price Handling | PASS | 08-Jun-2026

**Test 1:** trigger_price=0.0 for RELIANCE → HTTP 200, INVALID_PRICE at webhook edge (never enters pipeline).
**Test 2:** FAKEMICROCAP999 with price=5.50 → ACCEPTED → SKIPPED_QUOTE_UNAVAILABLE (no LTP available, no crash).
**Verified:** Zero orders with price=0.0 (non-cancelled) in entire orders table. No division-by-zero.
