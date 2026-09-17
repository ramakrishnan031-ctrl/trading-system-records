---
name: ct-ct012-result
description: "CT012 Duplicate Signal: PASS — second identical signal rejected as DUPLICATE within 5s"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT012 | Duplicate (within 5-min dedup) | PASS | 08-Jun-2026

**Test:** Injected NTPC/gap_fade_short/350 twice, 5s apart. First: ACCEPTED. Second: DUPLICATE.

**Mechanism:** Fingerprint dedup (symbol+scanner+date) catches same-day duplicates at webhook level.
