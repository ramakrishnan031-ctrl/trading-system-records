---
name: 07-May production bugs fixed (8 items)
description: Rate limiting + connection pool + shadow_tracker TypeError + orphan spam + ATR configs; quote cache added; 368 tests green
type: project
originSessionId: 8d4b49f4-9836-4656-b34b-38dfd2f0f22d
---
## 07-May Paper Trading Bugs — 8 items triaged, 5 fixed

### FIXED (commit pending)

1. **ShadowTracker TypeError** (shadow_tracker.py lines 288-303, 561-578)
   - `float(trade["sl_initial"])` crashed on NULL DB values
   - Added null guards + early return with error log
   - Also fixed cascade path (same pattern)

2. **Rate Limiting + Connection Pool Exhaustion** (main.py _make_paper_quote_provider + _build_kite_client)
   - Root cause: 30+ LTP-gating threads each calling Kite API individually (6+ calls/sec) with no rate limiting and default urllib3 pool_size=10
   - Fix: Thread-safe LTP cache (3s TTL) + HTTPAdapter(pool_maxsize=50) on both paper and live KiteConnect sessions
   - This also fixes the "no SL/TGT alerts" issue — exit fills weren't happening because quote fetches were failing

3. **Orphan Order Warning Spam** (zerodha_adapter.py get_open_orders)
   - Paper mode returned `[]` from get_open_orders(), causing reconciler CHECK6 to flag every PENDING_FILL trade as orphan every 15 seconds
   - Fix: return paper orders that are still SUBMITTED from _paper_fills dict
   - Also added symbol/side/qty/price/trigger_price to _paper_fills entries

4. **ATR Strategy Config Noise** (3 positional strategy YAMLs)
   - Changed sl_method from "ATR" to "FIXED_PCT" (ATR not implemented)
   - All 3 strategies already had sl_pct: 0.02 as fallback — functionally identical
   - Eliminates "sl_method=ATR not implemented, falling back to FIXED_PCT" warning spam

5. **SL/TGT Alerts Not Firing** — resolved by fix #2 above (quote cache enables LTP gating threads to complete)

### NOT A BUG (misdiagnosed)
- **Secondary Screener KeyError**: Already uses `quotes.get(symbol)` safely (line 90). The "No quote returned" message is a handled error, not a crash.

### DEFERRED
- **134 Unused Config Keys**: audit-only; no functional impact
- **Fill Timeout events**: related to LTP gating; fix #2 should improve this substantially

**Why:** Paper mode's architecture of per-order LTP polling threads was never designed for 30+ concurrent orders. The quote cache is a pragmatic fix; proper solution would be a single shared LTP poller.

**How to apply:** Monitor 08-May paper session for improved quote throughput, reduced orphan warnings, and SL/TGT alert delivery.
