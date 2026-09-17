---
name: ct-day6-complete
description: CT159 Gold Standard Day 6 COMPLETE (11-Jun-2026) — PASS. All time-gated events verified. Paper trading authorized.
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b860701-6391-4408-be2a-86ea2bdeaf60
---

**CT159 Gold Standard: PASS** — 2026-06-11

## Time-Gated Events (all PASS)
- **14:45:00** — EOD pre-alert fired for 18 positions (CT075 PASS)
- **15:15:01** — Force close: 7 entries cancelled, SOFT_KILL activated (circuit_breaker)
- **15:17:04** — EOD squareoff Pass 2: 14/14 LIMIT exits placed
- **15:19:08** — EOD squareoff complete: 14/14 filled in grace window, 0 MARKET promoted, duration=128.56s (CT089/CT140 PASS)
- 3 CNC/DELIVERY positions (AKUMS, INNOVACAP, JINDALPOLY) correctly skipped (overnight hold by design)

## Final Assertions
- State machine validator: **CLEAN** (4691 records, 0 violations)
- Exactly-once verifier: CLEAN except 14 order_placement FALSE POSITIVES (EOD SL replacement pattern)
- Invariant G (orphans): **PASS** after 2 cleanup rounds
- Forensic reconstructor: **PASS** (218 trades, 0 discrepancies)

## Config Reverts (done post-CT159)
- daily_loss_limit: 10000.0
- max_daily_trades: 20
- max_consecutive_losses: 4
- daily_loss_limit_pct: 0.05
- min_pass_score: 60

## Stats
- 4,691 signals processed; 218 trades; 52 closed; daily PnL ₹-4,960.75 (paper)

## Authorization
**Paper trading authorized — full production schedule from 2026-06-12.**

Related: [[ct-day5-complete]] [[ct-day6-retests]] [[ct-day6-blockers-reset]]
