---
name: E.2 capital tightening landed (19-Apr-2026, commit 0752a25)
description: Phase E.2 - H-1 invariant in sync_from_broker + H-3 leverage-aware margin + H-4 init guard + H-5 BEGIN IMMEDIATE; per-bucket INV6; ESCALATING_SOURCES gets fund_manager_bucket_overflow; 1603->1613 green
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
**Commit:** `0752a25` (19-Apr-2026 11:54 IST)
**Subject:** `E.2 | capital | H-1 invariant enforcement in sync_from_broker; H-3 leverage-map-aware margin; H-4 init guard; H-5 BEGIN IMMEDIATE`

**Items delivered:**

- **H-1**  `sync_from_broker` now calls `_check_invariant` (it was the ONLY mutator skipping it per pre-work). Silent `max(0.0, ...)` clamps at lines 742-747 removed. On bucket overflow: publishes `CapitalDriftDetected(source_module="fund_manager_bucket_overflow")` (NEW escalating source, added to `drift_handler._ESCALATING_SOURCES`), then invariant check fires hard_kill via BL-9 and re-raises. Pre-work found NO existing test exercised the clamp path — the "safety net" had never caught anything in testing. `_check_invariant` extended with per-bucket INV6 guards so bucket overflow surfaces as `NEGATIVE_MARGIN_AVAILABLE` (global sum check alone can hide one-bucket-negative when another offsets).
- **H-3**  `FundManager.required_margin(qty, price, intent)` public method wraps the module-level free function with `self._leverage_map`. `order_placer.py:337` replaces hardcoded `0.20` (coincidentally correct for INTRADAY 5x only; wrong for DELIVERY 1x / COVER_ORDER 6x) with this method. No cross-module private attribute access. `_MockFundManager` in `test_order_placer.py` gained mirror `required_margin` for test isolation.
- **H-4**  `FundManager.initialize()` guards against double-call with WARNING log + no-op. Protects against silent ledger corruption (second call would write a second INIT fm_ledger row with balance_before=0.0 AND silently zero existing reservations/used).
- **H-5**  `state_store.transaction()` uses `BEGIN IMMEDIATE`, serializing writers at SQLite lock level (readers unaffected). Stress test: 8 threads × 50 writes completes in ~0.16s without errors.

**Deferred-EF tracker deltas:**
- H-2 + H-12 deferred per E.0 triage → tracked as **DEFERRED-1**
- H-24 tracked as **DEFERRED-2**

**Architectural lock additions:**
- `fund_manager_bucket_overflow` added to `drift_handler._ESCALATING_SOURCES` — this is a permanent escalating source (regression guard added)
- `_check_invariant` per-bucket INV6 guard — global-sum check no longer sufficient; every bucket checked individually for availability ≥ 0
- `BEGIN IMMEDIATE` as the write-path lock mode — all write paths through `state_store.transaction()` serialize at SQLite level

**Test count delta:** 1603 → 1613 (+10; 9 functional + 1 regression guard for `_ESCALATING_SOURCES`)
**New test file:** `tests/unit/test_e2_capital_tightening.py` (434 lines)
**Phase A gate:** 15/15 green

**Why:** Tighten capital mutators before the order-lifecycle hygiene pass (E.3) so capital invariants hold across all paths including broker-sourced sync.
**How to apply:** Any new capital mutator MUST call `_check_invariant` at exit. Any new drift-source that represents a data-corruption condition (not recoverable drift) MUST be added to `_ESCALATING_SOURCES`.
