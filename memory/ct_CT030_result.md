---
name: ct-ct030-result
description: "CT030 Signal Before Force_Close — PASS; rejected 'Outside entry window' at 15:14 (entry_end=15:15)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT030: Signal Before Force_Close** — PASS

Injected signal at 15:14 IST via webhook (scanner: open_low_breakout_long, symbol: RELIANCE).
HTTP response: `{"error":"Outside entry window"}`

Signal rejected at webhook layer before DB insertion. Entry window ends at 15:15 (config `entry_end`), so 15:14 is within the final minute — system correctly refuses new entries this close to force_close.

No signal row created in DB (verified: latest RELIANCE signals are from earlier in the day with different statuses).

**Related:** [[ct-day1-progress]]
