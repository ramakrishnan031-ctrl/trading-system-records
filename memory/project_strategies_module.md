---
name: Strategies module built and locked (S1-S15)
description: strategies/schema.py + strategies/loader.py + 15 strategy YAMLs built and tested; S1-S15 locked
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
strategies/schema.py + strategies/loader.py + 15 config/strategies/*.yaml built and locked. 31 tests green. Total: 799 (764 unit + 4 integration + 31 new).

**Why:** Strategies layer (S1-S15) provides StrategyConfig Pydantic model + StrategyLoader for all downstream modules (quality_scorer, secondary_screener, entry_gate, smart_tgt_manager).

**How to apply:** Import from `strategies` package: `from strategies import StrategyConfig, StrategyLoader`. Use `StrategyLoader.load_all_strategies(dir, map_path)` at startup. Use `get_strategy(name)` for per-signal lookup.

## Files created
- `strategies/__init__.py` — exports StrategyConfig, validate_strategy, StrategyLoader
- `strategies/schema.py` — StrategyConfig (Pydantic, extra='forbid'), validate_strategy()
- `strategies/loader.py` — StrategyLoader with load_all_strategies() + scan_webhook_map cross-validation
- `config/strategies/` — 15 YAML files (all fields explicit per S5):
  - Intraday LONG (6): open_low_breakout_long, first_pullback_long, vwap_bounce_long, gap_go_long, gap_fade_long, range_breakout_long
  - Intraday SHORT (6): open_high_breakdown_short, first_pullback_short, vwap_rejection_short, gap_go_short, gap_fade_short, range_breakout_short
  - Positional (3): positional_momentum_long, positional_sector_rotation, positional_swing_long
- `config/scan_webhook_map.yaml` — populated with S14 format (strategy + chartink_url per scanner)
- `config/chartink_scanners.yaml` — populated with 15 scanner URLs
- `tests/unit/test_strategies.py` — 31 tests

## Key decisions locked (S1-S15)
- S1: strategies/ is Layer 2 (below broker/data); imports pydantic, yaml, stdlib, core.exceptions only
- S3: StrategyConfig has 30+ fields (all explicit in every YAML per S5)
- S4: field_validators for enums + model_validator for cross-field (FIXED_PCT requires sl_pct/tgt_pct > 0; sl_min <= sl_pct <= sl_max; time window start < end)
- S5: All fields present in every YAML (authoring convention, not Pydantic enforcement)
- S6: ConfigSchemaError / ConfigMissingError wrap ValidationError in validate_strategy()
- S8: extra='forbid' on StrategyConfig
- S10: StrategyLoader.load_all_strategies() fail-fast on first invalid YAML
- S13: Per-category defaults — gap_go/range_breakout = pullback disabled; first_pullback sl_pct 0.015; vwap sl_pct 0.008; positional = ATR-based, LIMIT_TRIPLE, DELIVERY, no smart_tgt
- S14: scan_webhook_map scanners[name] = {strategy: name, chartink_url: url}
- S16-S20: reserved

## Schema version
Unchanged (v6 from reconciler module).

## Deviations
- S11 mentions loader imports core.config_loader; not imported (paths passed as params, no unused import).
- locked_decisions.yaml updated: total_decisions 131→146, strategies_module section S1-S15 appended.
