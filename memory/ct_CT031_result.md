---
name: ct-ct031-result
description: "CT031 Signal After Force_Close — PASS; rejected 'Outside entry window' at 15:17"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT031: Signal After Force_Close / During EOD Squareoff** — PASS

Injected signal at 15:17 IST (exact squareoff time) via webhook (scanner: open_low_breakout_long, symbol: INFY).
HTTP response: `{"error":"Outside entry window"}`

Signal correctly rejected. Entry window already closed (entry_end=15:15). No signal row created in DB.

**Related:** [[ct-CT030-result]], [[ct-day1-progress]]
