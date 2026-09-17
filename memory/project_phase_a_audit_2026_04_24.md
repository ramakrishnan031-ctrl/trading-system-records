---
name: Phase A audit fixes complete (2026-04-24, commit 9b7bcda)
description: All 7 P0 pre-live blockers from deep_system_audit_2026-04-24 landed in one commit; 1679 green; Phase B next
type: project
originSessionId: a95ff8b2-8972-47f7-b6e5-51fb612e7504
---
**Commit:** `9b7bcda` (single Phase A block per user direction "option (b)")
**Tests:** 1679 green (+22 vs 1657 baseline). `pytest --co -q` confirmed.
**Source:** `docs/web_claude/03_audit_responses/deep_system_audit_2026-04-24.md` + `_closure.md`

**Why:** Audit closure doc identified 24 findings + 14 priority queue items; 7 of these are P0 pre-live blockers. User green-lit Phase A in prior session and confirmed "all 7" + commit-as-one in this session.

**How to apply:** When the user references "Phase A audit", "the 7 fixes", "naked-short", "OP-NS1..NS5", "OPL7", "OP-AR1/AR2", "INV7", or "LTP gating", this is the single commit to point at. The closure doc lists Phase B (6 items, P1) and Phase C (3 items, P2) still pending.

**The 7 items landed:**
- 1.1 OP-AR1/AR2 -- order_placer inserts _fill_map BEFORE order_monitor.track() per leg; cleanup pops successfully_inserted
- 1.2 Portfolio Lock -- FundManager.portfolio_lock property exposes RLock; signal_processor wraps approve+reserve in both _process_one and continue_from_gate
- 2.1 OP-NS1..NS5 / OPL1..OPL7 -- LIMIT_TRIPLE two-phase: execute() places ENTRY only; place_exits() places SL+TGT at filled qty
- 2.2 INV7 -- invariant.assert_capital_invariant rounds lhs+rhs to paise before tolerance check; _guard_non_negative rounds value too
- 3.1 EOD CO square-off -- branch on order_protocol/variety; CO uses cancel_order(variety="co"); state_store.get_open_intraday_positions joins orders for entry_broker_order_id+variety
- 3.4 OPL7 -- DELIVERY uses order_type="SL" with explicit price; INTRADAY keeps SL-M
- 6.2 -- PaperConfig.ltp_gating_enabled/max_wait_sec/poll_sec; ZerodhaAdapter._synth_fill polls quote_provider and only fills when LTP crosses; default OFF in tests, ON in system_config.yaml

**Skipped as already fixed (per audit closure):** 1.3, 2.3, 2.4, 3.2, 4.1, 4.3, 6.1 (findings) + #4, #7, #9, #10 (priority queue overlapping set)

**Phase B pending (6 P1 items, target 08-May):**
- 3.3+5.2 EOD LIMIT protocol + broker-authoritative qty
- 4.4 Entry Gate rehydration on startup
- 6.5 Waitress WSGI swap
- 5.4 modify_order ThreadPoolExecutor with coalesce
- 5.1 Shadow-tracker re-entry guard in signal_processor
- 12  LiveFeedManager tick-age watchdog

**Phase C pending (3 P2 items, post-live):** 4.2 WAL cron, 6.3 5-min dedup bucket, 5.3 smart-target intra-minute (evaluate paper Week 2 first)

**Phase D INFO only:** 6.4 NTP slew-mode doc note, 4.3 connection-leak misdiagnosis (no action)

**Live D-Day:** Mon 11-May-2026 (paper trial Week 1 currently Day 4/5).
