---
name: ShadowTracker module built and locked (SH1-SH15, Module 39)
description: orders/shadow_tracker.py multi-inning post-trade price simulation; schema v9 (innings table); 48 new tests; 1309 total
type: project
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
ShadowTracker module complete and locked. Module 39.

**Files built/modified:**
- `orders/shadow_tracker.py` (~380 lines): Inning frozen dataclass (15 fields), ShadowTracker class, module-level helpers (_check_hit, _calc_pnl, _derive_sl_tgt_from_strategy, _parse_ts, _make_naive)
- `core/schema.sql`: Added TABLE 16 (innings), schema_version bumped to 9
- `core/state_store.py`: EXPECTED_SCHEMA_VERSION=9; 4 new helpers: insert_inning, update_inning_close, get_innings_for_trade, get_innings_for_date
- `core/config_loader.py`: Added ShadowTrackerConfig (enabled, max_innings 1-5, alert_per_inning); added to SystemConfig
- `config/system_config.yaml`: shadow_tracker section (enabled=true, max_innings=3, alert_per_inning=true)
- `main.py`: ShadowTracker constructed in Phase 0e; _tick_dispatcher replaces lambda (routes to candle_store + shadow_tracker); set_instrument_cache wired
- `tests/unit/test_shadow_tracker.py`: 28 tests (all SH15 categories)
- `tests/unit/test_state_store.py`: +5 innings tests
- `tests/unit/test_config_loader.py`: +4 shadow_tracker config tests (ShadowTrackerConfig import added)
- `tests/unit/test_main.py`: ShadowTracker mock in patches; shadow_tracker config in mock; +1 wiring test

**Deviations from spec:**
- `strategies` optional dict added to constructor (SH2 didn't list it but SH4 requires it for RISK_REWARD support)
- `_active_innings` keyed by `trade_id` only (one active inning per trade at a time)
- Test fix: `test_position_closed_creates_inning_1` uses `max_innings=1` to isolate inning-1 creation (no cascade)

**Key design:**
- Inning 1 = real trade (is_real=True); innings 2+ = simulated (no broker orders)
- Cascade: SL_HIT or TGT_HIT + market_open + not eod_fired + inning_number < max_innings
- EOD: EodSquareoffComplete fires _on_eod_complete; closes all active innings with "EOD"
- _last_price dict maintained in on_tick for EOD fallback price
- _eod_fired bool prevents new innings after EOD
- dataclasses.replace() (dc_replace) used to clone closed Inning for cascade

**Why:** Fixes Concern 4 — "said TGT when SL hit first" visibility bug. Gives full multi-inning view of post-trade price action.

**How to apply:** Module 40 (daily_review multi-inning section) reads innings via get_innings_for_trade and get_innings_for_date helpers.
