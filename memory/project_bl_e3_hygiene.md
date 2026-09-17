---
name: Phase E.3 hygiene batch landed (19-Apr-2026, commit 27e40da)
description: E.3 four-fix batch — H-6 trail DB visibility, H-21+M-5 link hard-fail, H-15 orphan second-source, M-2 CO SL drift reconciler; 1607 unit + 15 integration green
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
Phase E.3 hygiene batch landed on 19-Apr-2026 at commit 27e40da.

**Why:** Four independent audit items in the orders/broker layer that share the "single commit, contained blast radius" profile — grouped to avoid commit thrash.

**How to apply:** When touching any of the four modules below, keep these semantics intact. Do not regress to pre-E.3 swallow/log-only behavior.

**Fixes landed:**

- **H-6 (smart_tgt_manager.py:446-472)** — DB-persist failure in trail success path logs ERROR with grep tag `SMART_TGT_TRAIL_DB_PERSIST_FAILED` but does NOT roll back memory. Reason: broker has already accepted new_sl (modify_order succeeded earlier), and memory must mirror broker to prevent a no-op re-trail on next candle. Trail is ratcheting (LONG SL only up, SHORT only down), so worst case on restart = one wasted broker modify, never an incorrect SL.

- **H-21 + M-5 (order_placer.py, link_signal_trade call site)** — `_om.link_signal_trade` failure now invokes BL-8 `_handle_placement_failure(..., broker_order_ids=())` and re-raises `OrderRejectedError`. Reason: link runs BEFORE `_engine.execute()` so no broker orders exist; empty tuple skips cancel but still marks trade FAILED + releases reservation. Pre-E.3 swallow-and-continue would have left an orphan broker position with no signal linkage.

- **H-15 (broker/order_monitor.py)** — Orphan detection at 3 empty history ticks now makes a second-source call to `adapter.get_open_orders` via `_OrphanTickCache` (tick-scoped, lazy fetch, reused across orphan candidates in the same poll). Three branches: (a) broker returns None → fail-safe fire; (b) order_id in broker-open set → false positive, counter reset; (c) order_id absent → confirmed orphan fire.

- **M-2 (order_reconciler.py `_check8_co_sl_drift`)** — Compares each tracked smart_tgt state's `current_sl` against the CO entry order's broker `trigger_price`. On drift > Rs 0.01, logs `CRITICAL CO_SL_DRIFT_DETECTED` + returns `ReconciliationAction(tier="RECOVERABLE", action_taken="alert_only")`. Critical invariant: MUST NOT call `adapter.modify_order` — alert-only first cut. Auto-repair deferred pending paper trial data.

**Supporting changes:**
- `zerodha_adapter.get_open_orders()` now returns `trigger_price` in each dict (for M-2 comparison + H-15 consumer)
- `tests/unit/test_order_monitor.py` MockAdapter extended with `get_open_orders` for mock parity

**Tests:** +9 in `tests/unit/test_e3_hygiene.py`; 1607 unit green; 15/15 integration green.

**Next:** Phase E.4 (event-loop safety + schema v10 + EF-1 + EF-5 — largest Phase E commit); do NOT start without explicit green light.
