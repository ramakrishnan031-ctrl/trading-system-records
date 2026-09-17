---
name: E.4 event-loop safety landed (19-Apr-2026, commit 0d80fe9)
description: Phase E.4 commit bundle - H-7/H-13/H-16/M-1/M-3/M-4/EF-5 + schema v10->v11; EF-1 retroactively closed; 1623 unit green + Phase A 15/15
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
Phase E.4 landed as one thematic commit: event-loop safety + schema v10→v11.

**CORRECTION (applied 2026-04-19 via E.6 drift investigation):**
Reported test count in this commit's landing report was **1623**.
Actual collected count at commit `0d80fe9` is **1638** (verified via `pytest --co -q`).
Cause: E.4 delta of +16 was correct (1622→1638); anchor inherited E.3's
−15 miscount offset, so absolute count was reported as 1623 instead of 1638.
**Corrected baseline: 1638 at commit 0d80fe9.**
(Inline note at line 29 "Baseline was 1607 (not 1622 as the green-light assumed)"
is now itself incorrect — the real baseline coming in was 1622. The +16 delta is right.)

**Items delivered (7 code + 1 retroactive):**
- **H-7**  EodSquareoff `_check_restart_recovery()` deferred from `__init__` → new `post_wire_init()`; main.py invokes after all bus subscriptions are wired (line ~1138), so a recovery-fire's `EodSquareoffComplete` publish reaches subscribers.
- **H-13** `shadow_tracker._close_inning` DB-failure branch: logs `SHADOW_INNING_CLOSE_DB_FAILED` grep tag + `return` early. Inning stays in `_active_innings`. No pop, no cascade.
- **H-16** `webhook_receiver._shutting_down: threading.Event`; `_handle_webhook` top guard returns 503 + audit row. `stop()` sets the flag. `main._shutdown` order: webhook → signal_proc (reversed from prior order).
- **M-1**  `webhook_receiver._claim_in_flight` / `_release_in_flight` atomic helpers under `_in_flight_lock`. Closes TOCTOU on concurrent same-symbol requests.
- **M-3**  EOD write-ahead: `_fire()` INSERTs IN_PROGRESS → work → UPDATEs to COMPLETE. Restart: IN_PROGRESS → recovery-fire; COMPLETE → skip. Recovery failure stays IN_PROGRESS + CRITICAL log + `notifier.send(severity='CRITICAL', title='EOD recovery FAILED', ...)`. **2 statuses only** (no auto-retry state machine).
- **M-4**  `_derive_prices` raises `_PipelineReject('INVALID_DERIVED_PRICE', reason)` instead of `ValueError` for entry≤0 and unknown sl_method.
- **EF-5** `reservation_id` column on `trades` (nullable). `OrderManager.create_trade` accepts `reservation_id` kwarg; `order_placer.place` threads it through. `get_all_open_trades` SELECTs it. `fund_manager._replay_open_trade` prefers `trade["reservation_id"]`, falls back to two-hop `get_reservation_id_for_signal` for legacy rows.
- **EF-1** closed retroactively — **via BL-18's inline shape-tolerant config resolution at `webhook_receiver.py:78-97`** (pre-dates Phase E). **Attribution correction:** the E.4 commit body (`0d80fe9`) incorrectly says "CO SL-drift reconciler (M-2, commit 27e40da)" — that's wrong; M-2 is CO SL drift reconciler, a different subject. EF-1 was actually closed by BL-18, which existed before E.4 even started. The commit body is now immutable (already pushed); this note is the durable correction for the audit trail.

**Schema bump v10 → v11:**
- `eod_squareoff_log`: `+status TEXT NOT NULL DEFAULT 'COMPLETE'`, `+completed_at TEXT`
- `trades`: `+reservation_id TEXT` (nullable)
- `EXPECTED_SCHEMA_VERSION = 11` in `core/state_store.py`
- Two new helpers: `insert_eod_squareoff_log_start(fired_date, fired_at)` (zero-count IN_PROGRESS) + `update_eod_squareoff_log_complete(...)` (finalize to COMPLETE)
- Legacy `insert_eod_squareoff_log` kept as single-shot fallback (writes status='COMPLETE', completed_at=fired_at)

**Tests: 1623/1623 unit + 15/15 Phase A integration**
- New: `tests/unit/test_e4_event_loop_safety.py` — 16 tests (H-7×2, H-13×2, H-16×2, M-1×1, M-3×4, M-4×1, EF-5×2, schema-v11×2)
- Mock refresh: `test_eod_squareoff.py` (3 tests now assert on new log helper pair; 2 tests added `post_wire_init()` call), `test_signal_processor.py` (`test_derive_prices_negative_entry_raises` now expects `_PipelineReject`)
- Baseline was 1607 (not 1622 as the green-light assumed); +16 net → 1623 green

**Grep tags introduced:**
- `EOD_WRITEAHEAD_FAILED` — write-ahead INSERT failed at _fire start
- `EOD_RECOVERY_FROM_IN_PROGRESS` — prior fire crashed mid-execution, recovering
- `EOD_RECOVERY_FAILED` — recovery-fire itself raised; row stays IN_PROGRESS
- `EOD_LOG_PERSIST_FAILED` — fallback single-shot INSERT OR REPLACE also failed
- `SHADOW_INNING_CLOSE_DB_FAILED` — DB UPDATE on inning close failed; inning preserved for reconciler

**Deferred-EF tracker state (end of E.4):**
- **EF-1** — CLOSED (via BL-18, attribution corrected above)
- **EF-2** — pending E.6 (partial-cancel semantics design, own pre-work)
- **EF-4** — pending E.7 (paper correctness + BL-7 regression)
- **EF-5** — CLOSED in this commit (reservation_id column end-to-end)
- **DEFERRED-1** — H-2 + H-12 (deferred from E.2 per E.0 triage)
- **DEFERRED-2** — H-24 (deferred from earlier triage)

**Implementation finding logged for phase-end artifact:** pre-work assumed only schema + call-site changes for EF-5. Actually found `fund_manager._replay_open_trade` still using the two-hop `get_reservation_id_for_signal` even after the direct column landed. Net effect: `get_all_open_trades` SELECT extended to include `t.reservation_id`, and replay prefers the column with fallback to two-hop for pre-EF-5 rows. Makes the EF-5 fix end-to-end rather than just write-side.

**Why: Phase E hygiene pass for paper-trial readiness. These close the event-ordering gap (post-wire init), the DB-vs-memory divergence risk on inning close, graceful shutdown 503, atomic webhook in-flight tracking, crash-resilient EOD fire semantics, and tidy error categorization at derive-time.

**How to apply:** Future EOD-related changes must use the write-ahead pair (start + complete); never raw `insert_eod_squareoff_log` in new code paths. New bus-publishing init work should be deferred to post_wire_init. DB failures in cascade-like loops must not mutate in-memory state.
