---
name: ct-ct014-result
description: "CT014 Outside Market Hours — PASS; rejected 'Outside entry window' at 15:18 (post-squareoff)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT014: Signal Outside Market Hours** — PASS

Injected signal at 15:18 IST (after EOD squareoff at 15:17) via webhook (scanner: open_low_breakout_long, symbol: TCS).
HTTP response: `{"error":"Outside entry window"}`

Signal correctly rejected at webhook layer. Entry window closed (entry_end=15:15 in config). No signal row created, no capital reserved.

Previously deferred from Day 0 — now confirmed PASS.

**Related:** [[ct-day1-progress]]
