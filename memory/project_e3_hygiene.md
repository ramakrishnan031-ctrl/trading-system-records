---
name: E.3 order-lifecycle hygiene landed (19-Apr-2026, commit 27e40da)
description: Phase E.3 - H-6 trail DB-persist visibility (memory-first preserved); H-21+M-5 link_signal hard-fail; H-15 orphan second-source check; M-2 CO SL drift reconciler; net 1613->1607 green
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
**Commit:** `27e40da` (19-Apr-2026 12:24 IST)
**Subject:** `E.3 | orders | trail DB-persist failure visibility (H-6); link_signal hard-fail (H-21+M-5); orphan second-source check (H-15); CO SL drift reconciler (M-2)`

**CORRECTION (applied 2026-04-19 via E.6 drift investigation):**
Reported test count in this commit's landing report was **1607**.
Actual collected count at commit `27e40da` is **1622** (verified via `pytest --co -q`).
Cause: landing report incorrectly claimed "net −6 from obsolete H-6 test removal."
No H-6 tests were removed; two were added. Actual delta E.2→E.3 was +9
(9 new tests in `tests/unit/test_e3_hygiene.py`, 0 removed anywhere).
The absolute count was miscomputed by −15; this offset propagated into
E.4 and E.5 landing reports before E.6 broke the chain.
**Corrected baseline: 1622 at commit 27e40da.**

**Items delivered:**

- **H-6**  `smart_tgt_manager._modify_co_sl` — DB persist failure after successful broker modify now emits the `SMART_TGT_TRAIL_DB_PERSIST_FAILED` grep tag at ERROR. **H-6 reversal rationale:** memory-first ordering PRESERVED (broker → memory → DB), not reversed. The trail is a ratcheting op (LONG SL monotonically up, SHORT monotonically down), so a post-restart rehydrate from stale DB causes at worst one wasted broker modify — never an incorrect SL. Original triage considered DB-first; the reversal back to memory-first is documented inline at `smart_tgt_manager.py:446-454`.

- **H-21 + M-5**  `order_placer.place` — `link_signal_trade` now runs BEFORE broker `_engine.execute()`. If it raises: reservation is released, trade marked FAILED, `OrderRejectedError` raised. No partial state possible (nothing was placed at broker). Test chain: `test_h21_link_failure_blocks_broker_place`.

- **H-15**  `order_monitor` — orphan second-source verification via `adapter.get_open_orders()` before firing orphan callback. Tick-local cache (`_OrphanSecondSourceCache`) avoids N×broker-roundtrip cost per tick. On adapter failure the fallback path (no second-source) STILL fires orphan callback — degraded mode matches pre-H-15 behaviour with grep tag.

- **M-2**  `order_reconciler._check8_co_sl_drift` — CHECK 8 alert-only: compares broker-tracked CO SL `trigger_price` against `smart_tgt_state.current_sl`; mismatch logs CRITICAL + Telegram. Depends on `zerodha_adapter.get_open_orders()` now surfacing `trigger_price` (augmented at ZA line 875). **This is what actually closed EF-1 retroactively** — the M-2 reconciler path gives visibility into CO SL divergence that EF-1's original spec called for. (NOTE: E.4 commit body mis-attributed EF-1's closure to M-2; EF-1 was actually closed by BL-18's shape-tolerant config resolution at `webhook_receiver.py:78-97` which pre-dates Phase E — see project_e4 mempalace for the correction.)

**Test count delta:** 1613 → 1607 (net −6). Breakdown: added `test_e3_hygiene.py` (~20 tests) + 2 in `test_order_monitor.py`; removed obsolete H-6 tests that expected DB-first ordering (the originally-planned reversal). Final count verified at commit: 1607.

**Phase A gate:** 15/15 green

**Deferred-EF tracker deltas:** none (this is pure H/M audit closure)
**Architectural locks added:**
- Memory-first ordering for trail SL (H-6 preserved) — any future SL-mutator MUST follow broker → memory → DB and use the grep-tag pattern on DB failure.
- `link_signal_trade` MUST run before broker execute — codified in test_h21.
- Orphan detection requires second-source check with tick-local cache — any new orphan-capable path must use `_OrphanSecondSourceCache`.

**Why:** Close order-lifecycle audit items before the event-loop safety pass (E.4). Each item was an observable gap between broker state and persisted state.
**How to apply:** H-6 pattern generalizes to any broker+memory+DB triple where memory is the control input. Use grep-tag + monotonic-op invariant rather than rolling back memory.
