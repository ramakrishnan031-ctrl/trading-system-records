---
name: ct-ct041-result
description: "CT041 Score at Exact Threshold: PASS — uses strict < (score >= threshold passes); confirmed by code + data"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT041 | Score at Exact Threshold Boundary | PASS | 08-Jun-2026

**Code:** secondary_screener.py:186 — `if total_score < effective_min: REJECTED`. Strict less-than, so score == threshold PASSES.
**Data:** 59 → REJECTED_SCORE_59, 64 → PASSED. Threshold = 60 (eligible_score).
**Boundary:** score >= effective_min passes. Documented.
