---
name: ct-ct033-result
description: "CT033 3 Same-Symbol 100ms: PASS — 1 accepted, 2 DUPLICATE; 2.5ms dedup latency; no deadlock"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT033 | 3 Same-Symbol Signals Within 100ms | PASS | 08-Jun-2026

**Test:** TATASTEEL to gap_fade_short 3 times at 100ms intervals. First: ACCEPTED (36ms). Second: DUPLICATE (2.5ms). Third: DUPLICATE (2.5ms).

**Finding:** Fingerprint dedup is very fast — 2.5ms for duplicate detection. No deadlock, no race condition under tight timing.
