---
name: Phase B audit fixes complete (2026-04-25, commit 13b3d09)
description: All 6 P1 pre-live items from deep_system_audit_2026-04-24 landed in one commit; 1713 green; Phase C deferred post-live
type: project
originSessionId: 3b08fb92-2197-48cd-8a56-29525f182f7d
---
**Commit:** `13b3d09` (single Phase B block per Phase A pattern, user direction "option 1")
**Tests:** 1713 green (+34 vs Phase A baseline 1679). `pytest --co -q` confirmed.
**Source:** `docs/web_claude/03_audit_responses/deep_system_audit_2026-04-24_closure.md`

**Why:** Phase A closed the 7 P0 blockers; Phase B closes the 6 P1 items the closure doc ordered against the 11-May-2026 live D-Day. User explicitly chose option 1 (full Phase B in one commit).

**How to apply:** When the user references "Phase B audit", "the 6 P1 fixes", "EOD LIMIT_THEN_MARKET", "gate rehydrate", "waitress", "modify coalesce", "shadow re-entry guard", or "tick-age watchdog", point at this commit.

**The 6 items landed:**
- B.1 / Audit 3.3 + 5.2 — orders/eod_squareoff.py LIMIT_THEN_MARKET protocol; phase-1 aggressive LIMIT (LTP +/- limit_aggressive_pct), phase-2 MARKET sweep on residual after limit_grace_sec; broker-authoritative qty via get_positions() (DB row may be stale on partial fills); CO branch unchanged. config_loader EodSquareoffConfig adds exit_protocol/limit_aggressive_pct/limit_grace_sec.
- B.2 / Audit 4.4 — schema v12 gate_state table; state_store.insert_gate_state/delete_gate_state/get_all_gate_state; EntryGate.add() persists + update_signal_status(GATE_WAITING); EntryGate._release() deletes; EntryGate.start() rehydrates before poll loop.
- B.3 / Audit 6.5 — requirements.txt waitress==3.0.2; main.py replaces app.run with waitress.serve(threads=8, connection_limit=100).
- B.4 / Audit 5.4 — orders/smart_tgt_manager.py opt-in async_modify=True ThreadPoolExecutor(max_workers=2); _pending_modify dict newest-wins coalesce; _drain_modify worker; _flush_inflight on stop. main.py wires async_modify=True; tests opt out (default sync).
- B.5 / Audit 5.1 — orders/shadow_tracker.py is_tracking(symbol) public method (in-memory O(N) over _active_innings); signal_processor REJECTED_SHADOW_INNING_ACTIVE; fail-closed on is_tracking() exception (REJECTED_SHADOW_TRACKER_ERROR).
- B.6 / Audit 12 — data/live_feed.py _last_tick_at stamped on _on_ticks; _watchdog_loop checks tick_stale_threshold_sec every watchdog_check_interval_sec; on stale during market hours -> CRITICAL + on_critical_failure + ticker.close() forces reconnect. main.py wires market_windows so watchdog gates on entry hours.

**Schema bump:** v11 -> v12 (gate_state table). EXPECTED_SCHEMA_VERSION updated in core/state_store.py. test_e4_event_loop_safety.test_schema_v11_has_status_column updated to assert against EXPECTED_SCHEMA_VERSION rather than literal 11 (test name kept for grep continuity per memory rule).

**Test additions per item:**
- B.1: 14 EOD tests (LIMIT phase-1, MARKET phase-2 sweep, broker-qty override, fallback paths)
- B.2: 3 entry_gate tests (add persists, release deletes, rehydrate restores)
- B.3: requirements pin only, no new tests
- B.4: 5 smart_tgt tests (async eventually calls broker, coalesce primitive, post-shutdown drop, drain empty no-op, stop drains in-flight)
- B.5: 4 signal_processor tests + 2 shadow_tracker is_tracking tests (active rejects, unrelated proceeds, no tracker fail-open, exception fail-closed)
- B.6: 6 live_feed tests (tick_age None pre-tick, updates on tick, paper-mode skip, fires on stale, silent outside hours, alert clears on tick resume)

**Phase C pending (3 P2 post-live):** 4.2 WAL cron, 6.3 5-min dedup bucket, 5.3 smart-target intra-minute (evaluate paper Week 2 first).
**Phase D INFO only:** 6.4 NTP slew-mode doc note, 4.3 connection-leak misdiagnosis.

**Live D-Day:** Mon 11-May-2026 (paper trial Week 1 currently Day 4/5).
