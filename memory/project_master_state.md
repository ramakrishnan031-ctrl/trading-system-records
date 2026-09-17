---
name: Trading System v2 - Master State
type: project
description: Authoritative project state snapshot — commit, test count, audit status, paper/live stage.
originSessionId: 3240cc27-d911-4827-864b-d5427aec0c5f
---
# PROJECT
- Location: D:\Projects\trading-system\
- User: Rama (non-techie bridge)
- Two-Claude architecture:
  Web Claude = stateless design architect producing .txt
               instructions at /mnt/user-data/outputs/instructions/
  VS Code Claude (me) = stateful executor with this mempalace
  Rama = bridge forwarding between them

# CURRENT STATE (12-May-2026)
- Commit: **5bea607** — Phase 1 audit (10 fixes)
- Tests: **1828 passed**, 2 pre-existing strategy YAML failures (not our problem)
- Branch: main
- Schema: v13

# PHASE 1 AUDIT COMPLETE (12-May-2026, commits 31075d0 → 5bea607)
- FIX-001: _fetch_ltp returns None (paper synth false fills fixed)
- FIX-002: CHECK9 MISSING_EXITS — naked position detection + soft_kill
- FIX-003: EventBus async_dispatch infrastructure; OrderPlacer uses SYNC (no actual deadlock)
- FIX-004: orders/price_math.py — single source of truth for SL/TGT formulas
- FIX-005: _guard_non_negative rounding bug fixed (-0.014 now raises correctly)
- FIX-006: sqlite3.connect timeout=30 + busy_timeout=30000ms
- FIX-007: SignalProcessor rate_limiter pre-check; re-queues on exhaustion
- FIX-008: CNC overnight position bootstrap check in reconciler start()
- FIX-009: get_server_time uses HTTP Date header via response hook
- FIX-010: atomic release_gate_state (delete + signal update in one txn)

# PREVIOUS STATE (11-May-2026)
- Commit: **4ef614e** — capital double-release root cause fix
- Tests: **1795 passed**
- Live Day 1: Mon 11-May-2026, Rs 25K micro capital

# LIVE STATUS
- Live since Mon 11-May-2026, Rs 25K micro capital
- VM: 161.118.187.249, SSH alias: trading-vm, user: ubuntu
- Path: /home/ubuntu/systems/trading-system/
- Shared venv: /home/ubuntu/systems/venv/
- systemd service ACTIVE

# PRE-EXISTING FAILURES (not caused by our work)
- test_strategies.py::test_positional_strategy_fields — YAML has FIXED_PCT; test expects ATR
- test_strategies.py::test_atr_sl_strategy_accepts_zero_sl_pct — same
- These were already failing before Phase 1 audit (commit ea8d90b changed YAML)

# AUDIT STATUS
- Phase 1 (10 fixes): COMPLETE
- Remaining audit phases: 2–13 pending (systematic fix session needed)

# TEMPORARY CONFIGS (REVERT WHEN STABLE)
- max_consecutive_losses: 20 (was 4)
- daily_loss_limit_pct: 1.00 (was 0.05)
- _INVARIANT_TOLERANCE: 100.0 (was 0.01)
- capital_drift_tolerance: 100000 (was 50)

# ARCHITECTURAL DECISIONS (LOCKED HIGHLIGHTS)
- Capital invariant: margin_available + reserved + used
                      == cash_floor + min(0, realized_pnl_today)
- Three-ID lifecycle: signal_id -> trade_id -> order_id (G2a)
- CO_PLUS_TGT protocol default, LIMIT_TRIPLE fallback
- Kill switch: 3-mode INACTIVE/SOFT_KILL/HARD_KILL; HARD requires --resume
- EventBus: sync (default) + optional async_dispatch per subscriber
- orders/price_math.py: single source of truth for calc_sl_price / calc_tgt_price
- Schema version EXPECTED_SCHEMA_VERSION=13
