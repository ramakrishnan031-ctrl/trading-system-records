---
name: mo1-fixed-flatten-quote-key-05jul
description: Wave 1 M-O1 FIXED — _flatten_broker_position quote key now bare-symbol (FIX-181 marketable-limit cap restored; was raw MARKET). Emergency-exit chain H-1/H-2/H-3/M-O1 CLOSED.
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

**Wave 1, M-O1 — FIXED (commit `959badf`, main, UNPUSHED). Emergency-exit chain CLOSED.**

Root cause: `OrderReconciler._flatten_broker_position` (orders/order_reconciler.py) looked up
the LTP with a DOUBLE-prefixed quote key. `_quote_fn` = `adapter.get_quote`, which takes BARE
symbols, internally prepends `NSE:` (zerodha_adapter.py:1567) and returns bare-keyed Quotes
(:1581). The flatten passed `self._quote_fn([f"NSE:{symbol}"])` + `raw.get(f"NSE:{symbol}")` →
get_quote queried `NSE:NSE:SYM` → miss → ltp always None → every kill-switch / inflight-orphan
flatten fell back to a RAW MARKET order → the FIX-181 marketable-limit slippage cap was silently
inoperative in BOTH modes.

Fix (2 tokens): mirror the bare-symbol idiom the other 3 quote sites use (`self._quote_fn([symbol])`
/ `raw.get(symbol)` — reconciler :1329, :2859). No None-guard added (the existing `if q is not None`
legitimately handles a genuine no-quote). `symbol` is bare (passed straight to `place_order(symbol=)`,
which handles NSE: internally) — the double prefix was the only defect.

Parity: `_quote_fn` = adapter.get_quote is mode-agnostic (paper delegates to the injected
quote_provider, same bare-symbol contract; live queries kite). Single shared method, no paper
duplicate. One fix both.

Test: `tests/unit/test_mo1_flatten_quote_key.py` (2, real `_flatten_broker_position` + a quote
provider mirroring get_quote's bare-key contract): long→SELL + short→BUY, RED (order_type MARKET) →
GREEN (order_type LIMIT at the FIX-181 marketable-limit price). order_reconciler 88 pass. No DB
needed (quote-key / order-type test).

**EMERGENCY-EXIT CHAIN CLOSED (H-1✓ H-2✓ H-3✓ M-O1✓):** an emergency flatten now cancels resting
SL/TGT pre-flatten (H-1), goes out as a FIX-181 marketable LIMIT not raw MARKET (M-O1), the fill
completes the full close+release immediately with real costs so capital frees and the loss hits both
daily-loss gates (H-2), and no stale retry fires a duplicate SL / naked reverse (H-3).
Still OPEN (out of scope): twin dead-col `kill_switch.py:977` (HARD_KILL flatten has the same H-1
bug); H-4/H-5 HARD_KILL correctness (Wave 2); H-12 paper get_positions qty-sign (Wave 3) — BLOCKS a
paper drill of the reverse-flatten direction; H-3 TOCTOU (local-table SL check) residual noted.
RECOMMENDED before Wave 2: a single END-TO-END risk-closed integration test (H-1 cancel + M-O1
capped-LIMIT + H-2 close/release + H-3 no-duplicate together on the real schema) — see chain review.

Related: [[h1_fixed_dead_column_05jul]] · [[h2_fixed_exiting_close_05jul]] · [[h3_fixed_exit_retry_guard_05jul]] · [[fix_181_complete]] · [[ramcoind_duplicate_sl_incident_25jun]]
