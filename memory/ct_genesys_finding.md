---
name: ct-genesys-finding
description: "GENESYS positional trade: was OPEN at Day 5 EOD, now CLOSED_MANUAL — manually resolved"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b860701-6391-4408-be2a-86ea2bdeaf60
---

GENESYS trade trd_71a8d998 (positional_sector_rotation, DELIVERY, LONG):
- Created: 2026-06-10 12:19 IST
- Was OPEN after Day 5 loss-limit EOD at 13:02 (missed by squareoff)
- As of Day 6 (11-Jun): status=CLOSED_MANUAL, exit_reason=MANUAL

The trade was manually closed between Day 5 and Day 6. No remaining OPEN trades.

**Why:** EOD squareoff on Day 5 squared 18/18 INTRADAY trades but missed this DELIVERY-intent position. This may be by design (positional/CNC trades are not squared off intraday) or a gap in the EOD query filter.

**How to apply:** Document as DESIGN_GAP — EOD squareoff only targets INTRADAY positions. Positional (DELIVERY/CNC) trades survive EOD by design. Verify this matches v2_design_spec.md intent.

Related: [[ct-day5-complete]]
