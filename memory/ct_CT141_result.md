---
name: ct-ct141-result
description: "CT141: Network Drop + SL Trail + Candle Gap — DEFERRED. Paper mode has no real WebSocket; SmartTgt inoperative."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

## CT141 | Network Drop + SL Trail + Candle Gap | DEFERRED

**Date:** 2026-06-10

**Reason:** Paper mode limitations:
1. No real WebSocket connection to Zerodha — paper adapter is immune to WS blocks
2. SmartTgt requires candle close events from ticker feed — `smart_tgt_state` table has 0 entries
3. Same limitation category as CT109 (WS only) and CT110 (REST only) from Day 4

**Prerequisite for testing:** Live broker session with active SmartTgt trails and real WebSocket feed.
