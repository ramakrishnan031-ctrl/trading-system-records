---
name: in_flight is in-memory only
description: Symbol in_flight locks are Python dict, cleared on restart; no database table
type: feedback
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
The in_flight symbol set (`webhook_receiver._in_flight`) is an in-memory Python dict, NOT a database table.

**Why:** Prevents duplicate processing of same symbol while signal is in pipeline.

**How to clear:**
- Restart service: `sudo systemctl restart trading-system`
- Or wait 5 minutes for sweeper to auto-evict (runs every 60s, evicts entries >300s old)

**No need to:** Run SQL DELETE - there is no `in_flight_symbols` table.
