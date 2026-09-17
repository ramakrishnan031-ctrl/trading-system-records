---
name: ct-ct018-result
description: "CT018 IN_PROCESS Symbol: PASS — two ONGC signals to different scanners; both processed sequentially, no deadlock"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT018 | IN_PROCESS Symbol | PASS | 08-Jun-2026

**Test:** Injected ONGC to gap_fade_short, then ~9s later to gap_fade_long. Both accepted, both reached terminal status (REJECTED_SCORE_50 and REJECTED_SCORE_40). IN_PROCESS lock serialized processing.

**Note:** 9s gap (not 100ms) due to SSH command sequencing. CT033 (3 same-symbol in 100ms) will test tighter timing.
