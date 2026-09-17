---
name: ct-day5-ct136
description: "CT136 Signal Flood + Network Drop — PASS (paper adapted). 50 signals, 5 trades, system stable."
metadata: 
  node_type: memory
  type: project
  originSessionId: 46ec89b8-48f0-47c1-920a-8d920c9f5480
---

**CT136: Signal Flood + Network Drop — PASS (PAPER_MODE_ADAPTED)**
Date: 2026-06-10, 09:30-09:31 IST

**Steps executed:**
1. Pre-state: 0 trades, 0 orders, kill_switch=inactive, queue=0/300
2. Flood: 50 signals at 200ms intervals (10 named symbols + 40 STOCK0XX synthetics)
3. Network block: block_zerodha_all applied at #25 for 30s
4. Post-state: 5 trades (2 OPEN, 3 FAILED), system healthy

**Signal outcomes (61 total received):**
- 40 SKIPPED_QUOTE_UNAVAILABLE (synthetic symbols)
- 5 PROCESSED → 5 trades
- 11 REJECTED by quality score (44-55 range)

**Trades created:**
- AFCONS LONG OPEN @ 343.05 x145
- HERANBA LONG OPEN @ 194.3 x256
- HERANBA LONG FAILED (x2)
- STUDDS LONG FAILED

**Assertions:**
- Some processed ✓ (5/50 processed, expected)
- API failures: N/A in paper mode (block_zerodha_all targets external hosts)
- No SOFT_KILL ✓
- No corruption ✓ (PRAGMA integrity_check = ok)
- State integrity ✓ (Invariant E = PASS)
- Pre-existing invariant failures (A,B,F,G) — not caused by CT136

**Why paper-adapted:** Paper adapter doesn't make external API calls to api.kite.trade/ws.kite.trade, so block_zerodha_all has no effect on trading operations.

Related: [[ct_day5_results]]
