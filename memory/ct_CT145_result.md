---
name: ct-ct145-result
description: "CT145: Rapid Crash Cycle 3x — PASS. Two SIGKILL+restart cycles, no corruption, 0 duplicate signals, DB ok."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

## CT145 | Rapid Crash Cycle 3x | PASS

**Date:** 2026-06-10 ~11:20 IST

**Method:** 3 cycles:
1. Inject 2 signals → wait 10s → SIGKILL → restart
2. Inject 2 signals → wait 10s → SIGKILL → restart
3. Inject 1 signal → process normally (10s)

**Results:**
- [PASS] All signals accepted (HTTP 200) across all cycles
- [PASS] No state corruption: DB `PRAGMA quick_check` = ok
- [PASS] No phantom signals: 0 duplicate signal_ids (51 new signals from test + natural Chartink)
- [PASS] No duplicate fm_ledger entries (2 new entries — INIT on each restart)
- [PASS] System healthy after all 3 cycles (status=ok, kill switch INACTIVE)
- [PASS] 8 startups in last 10 min (includes systemd auto-restarts)

**Note:** Injected symbols (CYC1SIG1 etc.) were rejected by screening (expected — synthetic symbols). The test validates crash recovery integrity, not signal processing. Natural Chartink signals continued arriving and processing correctly between crashes.
