---
name: Double-release ROOT CAUSE fix (2026-05-11, commit 4ef614e)
description: Paper get_positions() returning [] caused false CHECK1 MANUAL_CLOSE → double capital release → HARD_KILL; 3-part fix: paper positions tracking + close_trade allowlist guard + ShadowTracker datetime
type: project
originSessionId: dfecdca0-ca25-412a-b703-2ab7e53a04c5
---
HARD_KILL crash on 2026-05-08 (AEROFLEX) and 2026-05-11 (11 trades, ALL exits failed release_used). Total corruption 11-May: -47,169 Rs margin_used.

**3-link bug chain (root cause):**
1. `broker/zerodha_adapter.py` `get_positions()` returned `[]` in paper mode → reconciler CHECK1 false-positive on every OPEN trade
2. `orders/order_manager.py` `close_trade()` guard only checked `status == "CLOSED"`, missed `CLOSED_MANUAL` → double release not blocked
3. `orders/shadow_tracker.py` naive/aware datetime mismatch crashed monitoring (secondary)

**Morning band-aid (commit 4241395):** Only guarded `mark_trade_manually_closed` SQL — failed because root cause (empty positions) was not addressed. 11 false MANUAL_CLOSE events on 11-May.

**Root cause fix (commit 4ef614e) — 3 parts:**
- **Fix 1 (root cause):** `zerodha_adapter.py` — `_paper_positions` dict tracks synthetic fills; `get_positions()` returns real Position objects in paper mode
- **Fix 2 (defense-in-depth):** `order_manager.py` — `close_trade()` guard changed to allowlist (`status not in ("OPEN", "PARTIAL")`) catching CLOSED_MANUAL, CANCELLED, FAILED, PENDING_FILL
- **Fix 3 (datetime crash):** `shadow_tracker.py` — 3 lines: `_parse_ts` returns naive, `_on_position_closed` uses naive fallback, `_close_inning` uses `now_naive` for subtraction

**Why:** Paper adapter had no position state — it was a pure fill simulator. The reconciler's CHECK1 relies on positions to detect manual broker closes; returning `[]` triggered false positives on every paper trade.

**How to apply:** Any new paper-mode feature must maintain position state parity with live mode. The `_paper_positions` dict is authoritative for paper positions, protected by `_paper_fills_lock`.

1795 tests green (3 pre-existing failures unrelated). VM cleanup: kill_switch reset to NORMAL, 5 orphan PENDING_FILL cancelled, 17 stale OPEN orders cancelled.
