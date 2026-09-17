---
name: ct-day3-results
description: "Crash test Day 3 results — kill switch, circuit breakers, capital invariant, risk engine gates"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

## Day 3 Results (2026-06-08)

### Isolated Tests — 14/14 PASS (both Windows + VM)

**Batch 1** (ct_day3_isolated.py):
- CT067: Daily Loss Limit (Rs 10K) — PASS
- CT068: Daily Loss % (5%) — PASS
- CT077: Kill Switch Survives Restart — PASS
- CT078: Stale Kill Switch Auto-Clear — PASS
- CT079: --resume Recovery from HARD_KILL — PASS
- CT080: Soft->Resume->Soft->Hard Sequence — PASS
- CT082: Kill Switch Idempotency — PASS
- CT083: Max Open Positions (10) — PASS
- CT085: Max Consecutive Losses (4) — PASS

**Batch 2** (ct_day3_isolated_batch2.py):
- CT070: Clock Skew > 30s Detection — PASS
- CT075: Capital Invariant Violation -> Hard Kill — PASS
- CT084: Max Daily Trades (20) — PASS
- CT086: Max Sector Exposure (40%) — PASS
- CT087: Strategy Circuit Breaker — PASS

### Already Covered from Day 1+2 Live Observations
- CT074: 15:15 Force Close — observed
- CT089: EOD Squareoff Happy Path — observed
- CT091: EOD Pre-Alert 14:45 — tested as CT075 Day 1
- CT092: Force Close + EOD Overlap — observed

### Deferred (Need Live Broker)
CT069, CT071, CT072, CT073, CT076, CT081, CT088, CT090

**Why:** These require blocking real REST/WebSocket endpoints, corrupting live tokens, or timing order failures against actual broker calls.

**How to apply:** Schedule during next live trading session or paper session with broker connectivity.
