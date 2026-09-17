---
name: ct-ct008-result
description: "CT008 Exactly-Once Baseline: PASS — 5 injected signals + real Chartink signals all exactly-once; 7/7 checks clean"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT008 | Exactly-Once Baseline | PASS | 08-Jun-2026

**Test:** Injected 5 unique signals (WIPRO, BAJFINANCE, SBIN, MARUTI, ICICIBANK) with real LTP prices to 5 different scanners. All reached terminal status (1 PROCESSED→trade, 4 REJECTED_SCORE). System also had ~48 real Chartink signals from market open.

**Exactly-once verifier result:** 7/7 CLEAN
- signal_intake: clean
- capital_reserve: clean
- capital_commit: clean
- capital_release: clean
- order_placement: clean
- eod_squareoff: clean
- telegram_alerts: clean

**Total violations: 0.** System is exactly-once compliant.
