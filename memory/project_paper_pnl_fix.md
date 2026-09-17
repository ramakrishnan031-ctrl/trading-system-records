---
name: Paper mode P&L bugs FIXED (2026-05-05)
description: CRITICAL stub quote fallback (last_price=100.0) caused fake fills at ~99.80, inverted P&L signs, wrong magnitudes; removed stubs + added 50% deviation guard
type: project
originSessionId: 67941a2e-499f-425b-bb60-e2f8872b5fe8
---
## Bug (commit 78aaab7)

`_make_paper_quote_provider()` in main.py returned `_stub_quote(last_price=100.0)` when:
1. `kite_client is None` (token file missing)
2. Kite API threw any exception
3. Symbol not found in Kite response

This caused LTP gating to treat 100.0 as real market price. Effect:
- SL-M SELL orders triggered immediately (100 <= any SL trigger above 100)
- Exit price = 100.0 - slippage = ~99.80 for ALL stocks
- Entry fills at 100.0 + slippage = ~100.20
- P&L computed against fake prices: sign wrong, magnitude wrong

Verified from trades_2026-05-04 log:
- ZENTEC: entry 1492.51, exit 99.80, P&L -16.19 (should be ~-44,566)
- GRWRHITECH: entry 4261.73, exit 99.80
- MEESHO: LONG SL hit showed POSITIVE P&L

## Fix

1. **main.py**: Removed `_stub_quote` entirely. Return `{}` (empty dict) when Kite API fails or `kite_client is None`. All callers (`_fetch_ltp`, EOD `get_quote`, `order_monitor`) already handle missing symbols gracefully (return 0.0 → LTP gating skips → order stays pending → timeout handles it).

2. **broker/zerodha_adapter.py**: Belt-and-braces sanity guard in `_synth_fill`: after LTP-gated fill price is computed, reject if `abs(fill_price - reference) / reference > 0.50`. Reference = trigger_price (for SL-M/SL) or price (for LIMIT). Logs WARNING with full context.

3. **Tests**: 3 new tests covering deviation rejection, normal fill pass-through, and `_calc_pnl` sign correctness.

**Why:** Foundation Rule violation — paper mode must never use fabricated prices. Orders without real LTP data must stay pending (equivalent to real broker leaving order unfilled when condition not met).

**How to apply:** Deployed to VM. After restart, any period where Kite API is down will result in orders staying SUBMITTED (not filling with garbage). Order timeout + EOD square-off are the backstops for cleaning up stale orders.
