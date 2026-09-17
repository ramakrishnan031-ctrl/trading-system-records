---
name: ct-ct009-result
description: "CT009 Single Valid Signal: PASS — full chain verified: signal→trade→orders→fm_ledger for SBIN LONG 50@984.5"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT009 | Single Valid Signal — Happy Path | PASS | 08-Jun-2026

**Test:** Injected SBIN to first_pullback_long at price 985 (real LTP). Signal processed through full pipeline.

**Chain verified:**
- Signal: sig_b2ad07... → PROCESSED (10s latency)
- Trade: trd_ce2a7b... → OPEN, SBIN LONG 50 @ 984.5
- Orders: ENTRY + SL (969.25) + TGT (1013.5) all placed
- fm_ledger: RESERVE (10332.16) → COMMIT (9845.0, excess returned)
- Telegram: alert sent (verified in exactly-once)

**Full end-to-end happy path working.** Real Chartink signals also generating trades simultaneously (7+ open trades from market open).
