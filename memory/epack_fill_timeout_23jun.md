---
name: epack-fill-timeout-23jun
description: "EPACK \"10-min timeout didn't work\" = MISREAD; the 60s ENTRY fill-timeout fired+cancelled an unfilled SHORT entry correctly (trade FAILED, no position, no orphan)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e1a15ec3-5140-4531-93b5-a58f94e7260a
---

**"The 10-minute timeout didn't work for EPACK" (Rama, 23-Jun) is a MISREAD — reconstructed read-only from logs + DB.**

EPACK was a **SHORT ENTRY**, not an exit. Timeline (`system_2026-06-23.log`):
- 14:18:20 secondary_screener PASSED (score 62) + risk_engine approved (after ~2h of REJECTED_SCORE_52/57 since 12:27).
- 14:18:21 `trade_created` `trd_7a1ee35163c6454fbbf7bb26fcc17ea9` direction=SHORT strategy=**vwap_rejection_short**.
- 14:18:23 LIMIT **SELL entry** placed: 236.43, SL 238.32, TGT 232.65, qty 2, broker `260623171580838`. LTP was ~236.2 → a SELL LIMIT at 236.43 sits ABOVE market, needs price to rise to fill.
- 14:18:25→14:19:25 `order_monitor` polled `get_order_history` every ~2s for **62s**.
- **14:19:25.430 `order_monitor.fill_timeout`** → 14:19:25.431 `cancel_order` → broker shows **0/2 CANCELLED at 14:19:25**.
- DB trade: qty_filled **0**, entry_time/exit_time empty, status **FAILED** (terminal). **Position never opened → no orphan, no exit needed.**

**Verdict = (b): the timeout WORKED.** Mechanism = the **60s ENTRY fill-timeout** (`broker/order_monitor.py` OM7/OM14; `config/system_config.yaml: order_monitor.fill_timeout_sec: 60`; exit legs ENTRY/SL/TGT/EOD skip it). **There is NO "10-minute" timeout** (config has only 60s fill + `partial_fill_timeout_minutes: 5`). The broker "CANCELLED 0/2" is exactly the fill-timeout correctly cancelling a LIMIT entry that never reached its price within 60s. **No bug; no fix to timeout logic.**

The trade-coach (16:42) flag — "positional_sector_rotation entry 3 min before close, above ~Rs205 day-range ceiling, needs a time-of-day entry guard" — is about a **DIFFERENT trade**: EPACK is `vwap_rejection_short` @ 14:18 @ 236.43, not positional_sector_rotation, not near close, not ~205. EPACK's entry window is 09:25–15:00 (15:05+ EPACK signals were rejected OUTSIDE_ENTRY_WINDOW), so 14:18 was in-window. Any late-entry-guard work is a separate strategy-design item, unrelated to EPACK and to the timeout. See [[order_lifecycle_operational_note]], [[fix_186_orphan_leak]].
