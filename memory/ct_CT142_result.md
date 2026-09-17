---
name: ct-ct142-result
description: "CT142: DB Busy + Signal Burst — PASS. 20s DB lock, 10 signals queued and processed after unlock, no deadlock or crash."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

## CT142 | DB Busy + Signal Burst | PASS

**Date:** 2026-06-10 ~11:12 IST

**Method:** Acquired BEGIN IMMEDIATE lock on trading_system.db for 20s via separate thread. Injected 10 signals (RELIANCE through KOTAKBANK) to webhook while lock was held.

**Results:**
- [PASS] All 10 signals accepted (HTTP 200) — webhook queue absorbed signals during DB lock
- [PASS] All 10 signals processed to terminal status after DB unlock (REJECTED_SCORE_* or REJECTED_DAILY_TRADES)
- [PASS] No deadlock detected — all operations completed
- [PASS] No crash — system health ok, kill switch INACTIVE
- [PASS] DB integrity: `PRAGMA quick_check` = ok

**Note:** The queue-based architecture means signals are accepted to an in-memory queue immediately. The signal processor then writes to DB when available. The 30s busy_timeout on the main connection would handle the 20s lock comfortably. Real market signals from Chartink continued arriving during the test and were also processed normally (vwap_rejection_short batch visible in recent signals).
