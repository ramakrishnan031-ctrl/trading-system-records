---
name: ct-ct027-result
description: "CT027 Idempotency Under Load: PASS — 20 signals sent twice, all 20 duplicates correctly detected"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT027 | Idempotency Under Load | PASS | 08-Jun-2026

**Test:** Sent 20 unique real symbols (AXISBANK through INDUSINDBK) to gap_fade_long. Waited 30s for all to reach terminal status. Re-sent identical 20.

**Result:** All 20 re-sends returned DUPLICATE. 20/20 exact duplicate detection. Fingerprint dedup (symbol+scanner+date) is 100% effective under load.
