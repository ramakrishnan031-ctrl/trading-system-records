---
name: fix-166-complete
description: FIX-166 — all 5 P1 audit items fixed (F22/F06/F08/F13/F17); 2937 tests green; deployed
metadata: 
  node_type: memory
  type: project
  originSessionId: be792b36-df53-4386-8656-e1f951dc1c29
---

FIX-166 completed 13 Jun 2026. Fixed all 5 remaining P1 items from the deep system audit.

## Fixes

- **F22 (DESIGN_GAP):** KillSwitch hard_kill was toothless — adapter not wired. Added `set_adapter()` method to KillSwitch, wired `broker_adapter` in main.py after notifier. Hard_kill can now exit positions via `_exit_all_trades_indestructible`.
- **F06 (DESIGN_GAP):** Gate path (`continue_from_gate`) missing strategy governor check. Added `strategy_governor.check()` mirroring `_process_one`. Gate-released entries now respect cooldowns and circuit breakers.
- **F08 (RISK):** `_check_liquidity` bypassed adapter rate limiting by calling `_kite.quote()` directly. Added `get_quote_raw()` to ZerodhaAdapter (rate-limited, returns raw dict with depth). Changed `_check_liquidity` to use it.
- **F13 (CONFIG_GAP):** `email_fallback_config` existed in config and notifier constructor but was never wired in main.py. Added `email_fallback_config=alert_cfg.email_fallback` to TelegramNotifier.
- **F17 (DUPLICATION):** `_PRODUCT_TO_INTENT` dict was copy-pasted in 3 files. Created `core/constants.py` with canonical `PRODUCT_TO_INTENT`, updated imports in fund_manager, order_placer, order_reconciler, shadow_tracker.

## Files changed (10)
`core/constants.py` (new), `main.py`, `capital/kill_switch.py`, `signals/signal_processor.py`, `orders/order_placer.py`, `broker/zerodha_adapter.py`, `capital/fund_manager.py`, `orders/order_reconciler.py`, `orders/shadow_tracker.py`, `tests/unit/test_fix134_liquidity_check.py`

## Result
Test suite: 2937 passed, 0 failed, 12 skipped. Commits `9255b3b` + `9dbc345` deployed to VM.

**Why:** Weekend audit cleanup — all P0 and P1 items now fixed. Only P2 items remain.
**How to apply:** Audit is fully closed for P0/P1. See [[fix-165-deep-audit]] for the original audit findings.
