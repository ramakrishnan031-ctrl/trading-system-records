---
name: ct-ct038-result
description: CT038 Quote Timeout During Screening — PASS; socket.timeout → SKIPPED_QUOTE_UNAVAILABLE
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT038: Zerodha Quote Timeout During Screening** — PASS (3/3)

Isolated test on VM. Mocked quote_fn raises `socket.timeout`. SecondaryScreener catches it cleanly:
- Status = SKIPPED_QUOTE_UNAVAILABLE
- Not passed (no capital reserved)
- Score = 0

No crash, no unhandled exception. Signal rejected gracefully.

**Related:** [[ct-day1-progress]]
