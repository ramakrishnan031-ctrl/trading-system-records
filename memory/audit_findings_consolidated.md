---
name: Three Audits Consolidated - 54 Issues
type: project
description: Full list of all issues from 3 external audits, priorities, and fix ownership.
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
# AUDIT SOURCES
- Audit 1: "pre-live audit" (high-level, 10 concerns)
- Audit 2: "second pass" (30 concrete issues with line numbers)
- Audit 3: "final thorough pass" (19 additional + consolidated 54 total)

# TOTAL: 54 issues (15 critical + 15 high + 14 medium + 10 low)
# + 2 MISSING FILES flagged (but both actually built in Module 24)

================================================================
PRIORITY 1 - CRITICAL BLOCKERS (must fix before paper trial)
================================================================

BLOCKER #1 - LiveFeedManager callback signature mismatch
  Source: Audit 2 #25, Audit 3 #1 (confirmed)
  File: main.py line ~380
  Current (broken):
    live_feed.register_callback(
      lambda ticks: [candle_store.on_tick(t) for t in ticks])
  on_tick signature: on_tick(instrument_token, ltp, ts)
  Fix:
    live_feed.register_callback(
      lambda ticks: [candle_store.on_tick(
        t["instrument_token"], t["last_price"],
        t.get("timestamp") or now_ist()
      ) for t in ticks])

BLOCKER #2 - CandleStore.start() never called
  Source: Audit 2 #13, Audit 3 #2
  File: main.py Phase 0g
  Fix: Add candle_store.start() BEFORE live_feed.connect().
       Add candle_store.stop() in shutdown sequence.

BLOCKER #3 - Paper mode quote_provider missing
  Source: Audit 2 #4, Audit 3 #3
  File: zerodha_adapter.py + main.py
  Fix: Inject SimQuoteProvider in paper mode. Return canned
       quotes so get_quote() doesn't raise NotImplementedError.

BLOCKER #4 - continue_from_gate() uses wrong side parameter
  Source: Audit 3 #4 (NEW, most critical)
  File: signal_processor.py
  FIXED: Added side = "BUY" if direction in ("LONG","BUY") else "SELL"
         before sizer.calculate(), risk.approve(), and placer.place().
  TESTED: 2 regression tests (test_continue_from_gate_uses_side_not_direction,
          test_continue_from_gate_short_converts_to_sell)

BLOCKER #5 - EntryGate starts before SignalProcessor
  Source: Audit 3 #4 (second part)
  File: main.py Phase 0g start sequence
  Fix: Swap order. signal_processor.start() BEFORE
       entry_gate.start().

BLOCKER #6 - order_reconciler _check1_manual_close references
             missing 'product' field
  Source: Audit 3 #5
  ALREADY_FIXED during Module 37: state_store.get_all_open_trades
  now includes o.product in SELECT. IT11/IT12 tests green.

BLOCKER #7 - KiteConnect constructor missing timeouts
  Source: Audit 3 #1
  File: main.py line ~353
  Fix:
    kite = KiteConnect(
      api_key=os.environ["ZERODHA_API_KEY"],
      timeout=app_config.broker_limits.timeouts.read_sec,
    )

BLOCKER #8 - OrderMonitor empty get_order_history silently skips
  Source: Audit 3 #2
  File: order_monitor.py line ~214
  Bug: if not history: return (silent skip)
  Fix: Treat as orphan after N consecutive empty responses.
       Add failure counter per order.

BLOCKER #9 - _make_orphan_cb and _make_critical_failure_cb
             call soft_kill without triggered_by
  Source: Audit 2 #7, #8
  File: main.py callback factories
  Fix: kill_switch.soft_kill(reason=..., triggered_by="system_auto")

BLOCKER #10 - broker_orders_fn=None disables CHECK 6 (ORPHAN_ORDER)
  Source: Audit 2 #10, Audit 3 #9
  File: main.py reconciler wiring
  Fix: Add ZerodhaAdapter.get_open_orders() method that calls
       kite.orders() filtered to OPEN/TRIGGER PENDING.
       Pass as broker_orders_fn.

BLOCKER #11 - set_token_map never called in main.py
  Source: Audit 2 #24
  File: main.py
  Fix: After instrument_cache loaded (Module 38):
    token_map = {row.instrument_token: row.symbol
                  for row in instrument_cache.all_rows()}
    candle_store.set_token_map(token_map)

BLOCKER #12 - fund_manager.reset_daily_pnl() never called
  Source: Audit 2 #22
  File: eod_squareoff.py _fire sequence
  Fix: Call fund_manager.reset_daily_pnl() at end of EOD fire.

BLOCKER #13 - EodSquareoff _fired_for_date set BEFORE _fire()
  Source: Audit 2 #16
  File: eod_squareoff.py check_and_fire
  Fix: Set flag AFTER successful _fire() return.

BLOCKER #14 - EodSquareoff post-15:30 restart doesn't fire
  Source: Audit 2 #5 (new critical)
  File: eod_squareoff.py line ~320
  Current: if now.time() > 15:30: log CRITICAL and return
  Bug: If crash at 15:29, restart 15:31 -> positions stay open
       overnight.
  Fix: On post-15:30 startup, if open positions exist,
       fire EOD immediately (even past hard stop). This is
       safety, not a schedule.

BLOCKER #15 - signal_processor _derive_prices can return
              negative entry_price
  Source: Audit 3 #11
  File: signal_processor.py _derive_prices
  Fix: Validate entry_offset_pct < 1.0 at strategy load.
       Also validate entry_price > 0 after derivation;
       reject signal otherwise.

================================================================
PRIORITY 2 - HIGH SEVERITY (fix during/after paper trial)
================================================================

HIGH #1 - OrderMonitor.track() missing for SL/TGT legs
  File: order_placer.py after protocol places orders
  Fix: For each placed order (entry + SL + TGT or entry+TGT):
       order_monitor.track(internal_id, broker_id, symbol,
                            side, qty, price, placed_at)

HIGH #2 - sector_lookup_fn returns "UNKNOWN" for all
  File: main.py
  Fix: Add sector column to instruments.csv (Module 38).
       Wire sector_lookup_fn to instrument_cache lookup.

HIGH #3 - Telegram paper_mode may send real alerts
  File: main.py notifier construction
  Fix: Pass paper_mode=(args.mode == "paper") to notifier.
       TelegramNotifier.send must suppress send_real in
       paper mode.

HIGH #4 - ATR method silently falls back to FIXED_PCT
  File: signal_processor.py _derive_prices +
        step_executor.py step_3
  Fix: Option A - HALT: REJECTED_NO_ATR_DATA if ATR configured
       but not available.
       Option B - WARN: log WARNING every fallback.
       Config flag: strategies.atr_fallback_mode.

HIGH #5 - check_clock_skew hardcoded tolerance 30.0
  Source: Audit 3 #8
  File: startup_checks.py line ~298
  Fix: Read from app_config.system.clock.startup_max_skew_sec

HIGH #6 - webhook_receiver returns 200 on queue.Full
  Source: Audit 3 #10
  File: webhook_receiver.py
  Fix: Return 503 Service Unavailable when queue.Full.
       Client can retry.

HIGH #7 - order_placer persists hardcoded "MIS"/"CNC"
  Source: Audit 3 #12
  File: order_placer.py _persist_entry_orders
  Fix: Use product_resolver.resolve(intent) instead of
       hardcoded map.

HIGH #8 - eod_squareoff _cancel_pending_entries doesn't
           update order row status
  Source: Audit 3 #9
  File: eod_squareoff.py
  Fix: After cancel, update orders row status to CANCELLED.

HIGH #9 - in_flight symbols never timeout on hard crash
  Source: Audit 2 #9, Audit 3 #3
  File: webhook_receiver.py + signal_processor.py
  Fix: Background sweeper thread evicts in_flight entries
       older than 300s. Logs WARNING per eviction.

HIGH #10 - openpyxl imported lazily in daily_review
  File: reports/daily_review.py
  Fix: Import at top of file. Add openpyxl to
       startup_checks importability probe.

HIGH #11 - No log rotation
  File: logger.py
  Fix: Use RotatingFileHandler with maxBytes=50MB, backupCount=5.

HIGH #12 - alerts/critical.py referenced but not provided
  Status: Actually built in Module 24. Verify exists. If missing,
          build per CR1-CR10.

HIGH #13 - telegram_notifier.py referenced but not provided
  Status: Actually built in Module 24. Verify exists. If missing,
          build per TG1-TG15.

================================================================
PRIORITY 3 - MEDIUM (fix before scaling up)
================================================================

MED #1 - position_sizer sl_distance == 0 only warns, should reject
  Fix: Return SizingResult(success=False, reason=SL_TOO_CLOSE)

MED #2 - risk_engine ApprovalResult.snapshot incomplete on early
         rejection
  Fix: Ensure all 9 fields populated even when rejecting early.

MED #3 - rate_limiter freeze doesn't auto-thaw
  Fix: thaw when acquire() succeeds after penalize().

MED #4 - CO protocol returns success=True even when TGT fails
  Fix: Return success=False if any leg fails.

MED #5 - No schema migration logic
  Status: Foundation fresh DB only. v2.1 work.

MED #6-14: see Audit 3 medium list.

================================================================
VERIFICATION PROTOCOL
================================================================

Before fixing ANY issue:
  1. Read the actual source file at current state
  2. Confirm the bug still exists as described
  3. Report: CONFIRMED / NOT_APPLICABLE / ALREADY_FIXED / UNCLEAR
  4. Only fix CONFIRMED issues
  5. Add regression test for each fix

Some issues may be stale (auditor looking at old snapshots).
In particular:
  - Missing telegram_notifier.py - we built this
  - Missing alerts/critical.py - we built this
  - Some "hardcoded" things may have been parameterized already
