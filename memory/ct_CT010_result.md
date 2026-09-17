---
name: ct-ct010-result
description: "CT010 5 Symbols 5 Strategies: PASS — verified in CT008; all 5 processed, capital correct, exactly-once clean"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT010 | 5 Different Symbols, 5 Different Strategies | PASS | 08-Jun-2026

**Test:** (Covered by CT008) Injected WIPRO/gap_fade_long, BAJFINANCE/open_low_breakout_long, SBIN/first_pullback_long, MARUTI/vwap_bounce_long, ICICIBANK/gap_go_long — all with real LTPs.

**Results:** 1 PROCESSED (SBIN→trade), 4 REJECTED_SCORE. All 5 reached terminal status. Exactly-once verifier: 7/7 CLEAN (capital_reserve, capital_commit, order_placement all clean). No double-reserve.

**Invariants:** A=FAIL (pre-existing), B=verified via signal accounting, C/D=PASS.
