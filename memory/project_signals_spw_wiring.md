---
name: Signal processor wiring update (SPW1-SPW10)
description: Module 30 — signal_processor.py wired with strategies, screener, scorer; price derivation added
type: project
originSessionId: fc58fdb1-62db-42d0-abf8-209c7761d163
---
Files modified (NOT new module — update to existing):
- signals/signal_processor.py  (updated)
- tests/unit/test_signal_processor.py  (updated: 29 -> 48 tests)
- orders/order_placer.py  (extended: tgt_price=None kwarg added to place())
- tests/unit/test_order_placer.py  (updated: 36 -> 38 tests)

Locked decisions: SPW1-SPW10

Key changes:
- Constructor: replaced scanner_configs dict with strategies (dict[str, StrategyConfig]) +
  scan_webhook_map (dict: {scanner_name: {"strategy": name}}); secondary_screener and
  quality_scorer are now required (not None); order_placer still optional
- Step 2: scan_webhook_map[scanner_name] -> strategy_name -> strategies[name] = strategy_obj
  Rejects REJECTED_UNKNOWN_STRATEGY (replaces old REJECTED_UNKNOWN_SCANNER)
- Step 3: secondary_screener.screen() called; SKIPPED_* paths return early without
  writing status (screener already wrote per P18); screener REJECTED paths same
- _derive_prices(trigger_price, strategy): entry offset for LIMIT, SL FIXED_PCT/ATR,
  sl_min_pct / sl_max_pct bounds enforcement with WARNING
- _derive_target(entry, sl, strategy): FIXED_PCT, RISK_REWARD, ATR-fallback
- order_placer.place() now receives tgt_price kwarg; if None, OP3 internal computation used
- stats() extended: signals_screened_passed, signals_screened_rejected (dict),
  signals_screened_skipped (dict), avg_screening_ms
- _MockScreener in tests: accepts state_store, mirrors P18 by writing status to store

Cross-module consumption:
- strategies/loader.load_all_strategies() -> strategies dict consumed by processor
- scan_webhook_map.yaml scanners subdict -> scan_webhook_map consumed by processor
- screening/secondary_screener.SecondaryScreener.screen() -> called at step 3
- screening/quality_scorer.QualityScorer -> injected, kept for logging/metrics (not directly called)

Deviations: None. Test count after: 901 + 1 pre-existing failure in test_secondary_screener.py
(test_signal_age_over_90s_rejected_signal_age — timing bug in that test, unrelated to Module 30)

**Why:** Wiring the real screener and strategy loader into the processor pipeline; completing
the signal flow from webhook to order placement stub.
**How to apply:** When referencing signal_processor constructor, use new param names. Use
scan_webhook_map for scanner->strategy mapping, not scanner_configs. P18: screener writes
PASSED/REJECTED status; processor only writes PROCESSING, RESERVED, PROCESSED, PLACEMENT_FAILED.
