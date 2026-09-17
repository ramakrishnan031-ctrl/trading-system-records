---
name: Phase G medium severity fixes (MED #1-#14)
description: 14 medium issues triaged; 7 confirmed fixes applied; 1351 tests green
type: project
originSessionId: dfc8e70f-0cb7-40da-9959-f2a5d00f4101
---
Phase G complete. 1344 → 1351 tests (7 new).

**Triage results:**
- ALREADY_FIXED: MED #1 (log rotation), MED #3 (openpyxl lazy), MED #6 (_derive_prices negative), MED #7 (order_placer product_resolver)
- NOT_APPLICABLE: MED #5 (no README in project), MED #9 (risk_engine snapshot already built before all checks at RE11), MED #11 (fill_map all accesses guarded)
- DEFERRED: none (MED #5 effectively skipped)
- CONFIRMED+FIXED: MED #2, #4, #8, #10, #12, #13, #14

**Fixes applied:**
- MED #2: `_NEXT_DAY_LOOKAHEAD_CAP` 10→30 in `core/market_windows.py`
- MED #4: thaw logging in `broker/rate_limiter.py` — `_was_frozen` flag + `pop_thaw_notice()` + INFO log on first acquire after freeze
- MED #8: `capital/position_sizer.py` — sl_price==entry_price now returns `SizingResult(success=False, constraint="SL_DISTANCE_ZERO")` instead of raising ValueError
- MED #10: `main.py` — `_write_session()` called EARLY (after Phase 0c, before Phase 0d); still called again at Phase 0h to update
- MED #12: `core/config_loader.py` — `SignalProcessorConfig.atr_fallback_mode: Literal["WARN","HALT"] = "WARN"`; `signal_processor.py` raises `_PipelineReject("REJECTED_NO_ATR_DATA", ...)` in HALT mode
- MED #13: `orders/order_protocol_co.py` OPC4 reversed — TGT failure now returns `success=False` (contract honesty); CO broker_order_id preserved in entry_broker_order_id for reconciliation
- MED #14: `data/candle_store.py` `MAX_HISTORY` 390→500 with comment

**Why (MED #13 deviation note):** OPC4 was locked as success=True on TGT fail. Audit fix changes it to success=False. Consequence: order_placer will call _handle_placement_failure(), releasing reservation and marking trade FAILED while CO is live. Reconciler handles orphaned CO on next startup.

**Next:** Phase H (chaos tests) awaiting Rama confirmation.
