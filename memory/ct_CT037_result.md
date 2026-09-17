---
name: ct-ct037-result
description: "CT037 Screening Happy Path: PASS — SBIN scored 59, threshold 60, clean reject"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT037 | Screening Happy Path | PASS | 08-Jun-2026

**Test:** Injected SBIN to open_low_breakout_long via webhook port 5000 (Chartink time format).

**Results:** HTTP 200, signal ACCEPTED. Screener ran full pipeline: score=59, tier=LOW, eligible_score=60. Status=REJECTED_SCORE_59 (strict `<` comparison: score < threshold rejects). screener_results row correctly persisted. No crash, clean pipeline.

**Boundary note (CT041):** Code at secondary_screener.py:186 uses `total_score < effective_min` — so score >= threshold passes. Confirmed by data: 59 rejected, 64 passed.
