---
name: Screening module built and locked (QS1-QS10, SE1-SE10)
description: screening/quality_scorer.py + screening/step_executor.py built and tested; QS1-QS10 + SE1-SE10 locked
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
screening/quality_scorer.py + screening/step_executor.py built and locked. 17+43=60 tests green. Total: 859 (799 prior + 60 new).

**Why:** Quality scorer and step executor are leaf-node modules that unblock secondary_screener (Module 29). Both are stateless and have no circular dependencies.

**How to apply:** Import from `screening` package: `from screening import QualityScorer, StepExecutor`. QualityScorer requires ScoringConfig (from AppConfig). StepExecutor is stateless (logger only). Call `executor.run_all(signal, market_data, thresholds)` then `scorer.score(result.step_results)`.

## Files created
- `screening/__init__.py` — exports QualityScorer, ScoreResult, StepExecutor, StepExecutorResult
- `screening/quality_scorer.py` — QualityScorer + ScoreResult frozen dataclass
- `screening/step_executor.py` — StepExecutor + StepExecutorResult frozen dataclass
- `tests/unit/test_quality_scorer.py` — 17 tests
- `tests/unit/test_step_executor.py` — 43 tests

## Key design decisions (QS1-SE10)
- QS3: Missing step -> 0.0 + WARNING + appears in missing_steps
- QS4: weighted_score = raw * weight; total capped at 100
- QS5: tier from thresholds in scoring_weights.yaml (high=80, medium=65)
- QS7: Scorer returns tier string only; position_sizer applies size multiplier (PS5)
- SE4: 10 steps with audit fixes: step_2 direction-aware vwap; step_1 avg_volume=0->0.0
- SE5: Each step try/except; errors recorded, run_all() never raises
- SE6: latencies_ms populated per step via time.monotonic()
- SE7: ALL 10 steps always run (no short-circuit; scorer needs all scores)
- SE8: Missing market_data keys use per-step defaults (0.5 neutral or 0.0 reject)
- SE10: now_ist() is only non-deterministic dep; mockable for tests

## ScoringConfig (from config_loader)
- Class name: ScoringConfig (NOT ScoringWeightsConfig — that was spec shorthand)
- Located in core/config_loader.py
- Fields: steps (ScoringStepsConfig), min_pass_score, tier_multipliers, high_score_threshold, medium_score_threshold

## Schema version
Unchanged (v6).

## Deviations
- None.

## locked_decisions.yaml
- total_decisions updated: 146 -> 166
- screening_module: section with QS1-QS10 + SE1-SE10 appended
