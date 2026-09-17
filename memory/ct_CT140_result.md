---
name: ct-ct140-result
description: "CT140: EOD Squareoff Failure — DEFERRED. Daily trade limit hit (21/20), no open positions at 15:14."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

## CT140 | EOD Squareoff Failure — All Positions | DEFERRED

**Date:** 2026-06-10

**Reason:** Daily trade limit hit (21 trades today vs max_daily_trades=20). All positions were closed by 11:09 IST (CLOSED_MANUAL during CT139 cleanup). Cannot create new positions for the 15:14 time window.

**Prerequisite:** Needs 3+ open positions at 15:14 + ability to block Zerodha REST. Requires a fresh trading day with available trade capacity, OR temporary increase of max_daily_trades.

**Note:** The EOD squareoff mechanism was validated in Day 4 (CT089: EOD squareoff PASS at 15:17:02). This scenario specifically tests failure mode when REST is blocked during squareoff.
