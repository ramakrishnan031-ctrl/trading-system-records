---
name: ct-ct013-result
description: "CT013 Expired Signal: PASS — 700s-old signal correctly rejected as EXPIRED"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT013 | Expired Signal (triggered_at 700s ago) | PASS | 08-Jun-2026

**Test:** Injected BPCL with triggered_at 700s in the past (signal_expiry_sec=600). Result: EXPIRED.
