---
name: ct-ct043-result
description: "CT043 Bad OHLC (High < Low) — PASS; no ZeroDivisionError, rejected cleanly"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT043: Bad OHLC Data (High < Low)** — PASS (3/3)

Isolated test on VM. Quote returns inverted OHLC (high=90, low=120). No ZeroDivisionError, no crash. Screener produces valid status and non-negative score.

**Related:** [[ct-day1-progress]]
