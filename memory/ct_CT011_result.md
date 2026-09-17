---
name: ct-ct011-result
description: "CT011 Same Symbol Different Strategies: PASS — COALINDIA to 2 scanners 1s apart; sequential processing, no race"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT011 | Same Symbol, Different Strategies | PASS | 08-Jun-2026

**Test:** Injected COALINDIA to gap_fade_short (price 380), 1s later to gap_fade_long. Both ACCEPTED at webhook.

**Result:** gap_fade_short → REJECTED_SCORE_50, gap_fade_long → PROCESSED (trade created). IN_PROCESS serialization worked — second signal queued while first was processing same symbol. No race condition, no deadlock.
