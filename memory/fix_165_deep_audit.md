---
name: fix-165-deep-audit
description: FIX-165a-h deep system audit (14-Jun-2026) — 6 P0 + 2 P1 bugs fixed; 35 total findings
metadata: 
  node_type: memory
  type: project
  originSessionId: be792b36-df53-4386-8656-e1f951dc1c29
---

Deep system audit completed 13-14 Jun 2026. Full report: `docs/audit/system_audit_14jun2026.md`

## Fixed (8 bugs — FIX-165a through FIX-165h)
- **FIX-165a (P0):** `fund_manager.top_up_reservation` — invariant check race, missing violation handler, slm_buffer dropped
- **FIX-165b (P0):** `kill_switch._exit_all_trades_indestructible` — wrong column names/statuses/directions. Currently unreachable (main.py doesn't pass adapter)
- **FIX-165c (P0):** `signal_processor._in_flight_count` goes negative — both `_process_one` and `continue_from_gate`
- **FIX-165d (P0):** `order_placer._retry_limit_triple_exits` — success path dead code (wrong indentation)
- **FIX-165e (P0):** `signal_processor.continue_from_gate` — missing kill-switch check before placement
- **FIX-165f (P1):** `signal_processor` queue-full abandon — signal status + in_flight leak
- **FIX-165g (P0):** `order_reconciler._check_unknown_in_flight` — FIX-068 silently broken (calls non-existent StateStore methods)
- **FIX-165h (P1):** `order_placer._emergency_market_exit` — `_LEG_SL` → `_LEG_EOD` (corrupted exit_reason)
- **DB fix:** 5 cron scripts used wrong DB filename (`trading.db` → `trading_system.db`)

## P1 items — ALL FIXED (FIX-166)
See [[fix-166-complete]] for details. All 5 P1 items fixed and deployed.

21 P2 items remain documented in report.

**Why:** Weekend safety audit before continued live trading.
**How to apply:** All P0+P1 closed. P2 items are non-urgent. [[feedback_paper_live_parity]]

Test suite: 2937 passed, 0 failed. Deployed to VM commits `7694cb0` + `1bf65ff` + `9255b3b` + `9dbc345`.
