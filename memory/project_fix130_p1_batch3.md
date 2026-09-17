---
name: project_fix130_p1_batch3
description: FIX-130 P1 batch3 complete -- 5 items + 97 pre-existing test fixes; 2303 tests; commit 0cc0009
metadata: 
  node_type: memory
  type: project
  originSessionId: e10470fa-0a49-4239-9cbe-4a0ec4c4c04b
---

FIX-130 P1 batch3 landed (2026-05-30, commit 0cc0009). 2303 tests passing, 12 skipped (bash on Windows), 0 failures.

**Why:** Operational stability + trading safety items from P1 backlog.

**How to apply:** Baseline test count is now 2303. All pre-existing failures resolved.

## Features shipped

### Item 4: SL gap buffer (sl_gap_buffer_pct)
- strategies/schema.py: sl_gap_buffer_pct field (default 0.0)
- signal_processor._derive_prices: applies buffer during 09:15-09:30 if set
- All 4 gap strategy YAMLs: sl_gap_buffer_pct: 0.3

### Item 5: Signal-to-fill latency tracking (schema v17)
- trades table: signal_to_order_ms, order_to_fill_ms, total_latency_ms
- order_manager.record_entry_fill: calls _compute_and_store_latency

### Item 6: Strategy circuit breaker
- capital/strategy_governor.py: StrategyGovernor class
- Pauses strategy when daily loss > 2x avg_daily_loss (last 10 days) before 12:00
- Config: system.strategy_circuit_breaker (enabled, loss_multiplier, cutoff_time, lookback_days)
- Wired into signal_processor._process_one at Step 2 (after strategy lookup)
- Telegram alert on pause; in-memory state, resets on restart

### Item 7: EOD pre-alert at 14:45
- main._fire_eod_pre_alert() + _start_eod_pre_alert_thread()
- Queries open OPEN-status trades, sends Telegram with positions ~30 min before squareoff
- Fires once per day; daemon thread exits after firing

### Item 16: Partial fill handling (Option A)
- order_monitor._handle_partial: ENTRY leg cancelled immediately on first PARTIAL detection
  (not after 5-min timeout); calls _handle_terminal which fires OrderPartiallyTerminated
- order_placer._on_order_partially_terminated: Telegram alert added
  (DB update + SL placement chain was already implemented via OrderPartiallyTerminated)
- Non-ENTRY legs (SL/TGT/EOD) still use timeout path

## 97 pre-existing test fixes
- main.py: check_port_available added to instance_lock import
- order_placer: removed self._leverage_map = fund_manager._leverage_map (H-3 violation); use self._fm.required_margin()
- test_fund_manager: slm_margin_buffer_pct=0.0 in _make_fm helper
- test_logger: QueueListener drain before reading files; _PassthroughQueueHandler in core/logger.py preserves exc_info
- test_fix073, test_logger: ignore_cleanup_errors=True on TemporaryDirectory
- test_startup_checks: scanner_check_delay_sec=0.0 in mock; timing tolerance >= 0.05
- test_alerts_pipeline: alert_digest_threshold=3 in mock config
- test_fix065: skip on Windows (bash not available)
- test_e3_hygiene: _internal_to_composite lookup for _watched key
- test_fix075: slm_margin_buffer_pct=0.0 in FundManager constructors
