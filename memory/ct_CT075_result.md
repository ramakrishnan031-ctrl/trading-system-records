---
name: ct-ct075-result
description: CT075 EOD Pre-Alert — FAIL; eod-pre-alert thread crashed on startup (is_trading_day AttributeError)
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

**CT075: EOD Pre-Alert** — FAIL

No pre-alert fired at 14:45 or any time after restart at 14:22.

**Root cause**: eod-pre-alert thread crashed on startup:
```
AttributeError: 'MarketWindows' object has no attribute 'is_trading_day'. Did you mean: 'is_trading_holiday'?
```
Location: `main.py:734` — thread function calls `market_windows.is_trading_day(today)` but correct method is `is_trading_holiday`.

**Impact**: No 15-minute EOD warning to Telegram. Squareoff itself (separate scheduler) is unaffected.

**Fix needed**: Change `is_trading_day` to correct method name in main.py. Logic inversion may also be needed (is_trading_holiday returns True for holidays, not trading days).

**Related:** [[ct-restart-findings]], [[ct-day1-progress]]
