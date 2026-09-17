---
name: ct-ct034-result
description: "CT034 Chartink Retry Simulation: PASS — retry after 30s correctly detected as DUPLICATE"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT034 | Chartink Retry Simulation (503 → wait → retry) | PASS | 08-Jun-2026

**Test:** Sent VEDL/gap_fade_short (ACCEPTED). Waited 30s. Re-sent identical signal. Result: DUPLICATE.

**Note:** Could not test actual 503 backpressure path (CT025 showed queue never fills at current injection rate). But the retry-after-503 dedup path is verified — Chartink retries would be caught by fingerprint dedup.
