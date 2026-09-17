---
name: slice2-strategy-control-24jun
description: Slice 2 — 3-layer strategy control (trade_type + per-strategy enabled) + resolver-driven status table; default ships ALL 15 enabled (true zero-change, the 3 delivery trade as intraday); single resolver drives gate (2 sites) + table; no schema
metadata:
  node_type: memory
  type: project
  originSessionId: 70f5d745-f68b-453a-9155-61b7b08308ff
---

**Slice 2 deployed 24-Jun (branch `slice2-strategy-control-24jun`). Trading-path change (entry gating). No DB schema. Activates next restart (08:15).**

## The 3-layer control
- **LAYER 0 `force_intraday_only`** (EXISTING, unchanged): emergency breaker; rewrites every strategy's intent→INTRADAY at LOAD (`strategies/loader`). Currently `true`.
- **LAYER 1 `system_config.trade_type`** (NEW): INTRADAY | DELIVERY | BOTH (default INTRADAY). SystemConfig field (`config_loader.py:1041`) + validator. Master product gate.
- **LAYER 2 `strategy.intent`** (EXISTING, LIVE): the strategy's product type; sole MIS/CNC driver via `product_resolver.resolve(intent)`.
- **LAYER 3 `strategy.enabled`** (NEW): per-strategy ON/OFF; `StrategyConfig.enabled: bool = True` (opt-in default → zero-change). Added `enabled: true` to all 15 YAMLs.

## Single source of truth
`strategies/control.py` → `strategy_will_trade(strategy, *, trade_type, force_intraday_only) -> Verdict(will_trade, reason, product)`. Pure, no mode branch. THE RULE: `enabled AND (intent permitted by trade_type) AND (breaker doesn't block delivery)`. Defensive `force + raw-DELIVERY → WON'T TRADE` branch never fires in prod (loader pre-rewrites intent→INTRADAY) but locks the breaker semantics for tests.

## Gate (trading-path, BOTH sites)
`signals/signal_processor.py`: gate inserted at `_process_one` (after strategy_obj resolved, before per-strategy window) AND `continue_from_gate` (pullback-wait resumption, symmetric). `if not verdict.will_trade: raise _PipelineReject("STRATEGY_CONTROL", reason)` — BEFORE sizing/reservation. SignalProcessor got `trade_type` + `force_intraday_only` ctor params (wired from `app_config.system` in main.py). **Product wiring UNCHANGED** (the gate only REJECTS; survivors place via the existing intent→product_resolver path) → INVARIANT: default state (trade_type INTRADAY + force on) places MIS for every will-trade strategy, never CNC. Startup one-line `strategy_control.summary` log (WILL/WON'T counts + names).

## DECISION — default ships ALL 15 enabled:true (NOT 3 delivery disabled)
The brief said disable the 3 delivery (`positional_*`) strategies for "zero behaviour change" — but I found they are **trading LIVE as intraday** right now (force_intraday_only rewrites them): `positional_sector_rotation` was 24-Jun's MOST active strategy (5 trades, +₹8.93), `positional_swing_long` traded too, `positional_momentum_long` = signals only. Disabling them would STOP live strategies — NOT zero-change. **Rama chose Option 2: all 15 enabled:true** = TRUE zero behaviour change (the 3 keep trading as intraday). The switch now EXISTS (all on) for Rama to flip any OFF anytime. Conscious enable/disable of the 3 as REAL delivery (CNC) is deferred to when `trade_type` is set BOTH/DELIVERY (Slice 2.5). **Default = 15 WILL TRADE / 0 WON'T TRADE.**

## Status table (resolver-driven; can't disagree with the gate)
`scripts/strategy_status.py`: `build_status_rows(config_dir, trade_type, force_intraday_only)` + `render_html` (full 15-row Gmail-safe table, pills) + `render_plaintext` + `compact_lists`. **Type column shows TRUE declared intent** (DELIVERY for positional_*, sourced from raw `validate_strategy` BEFORE the force-rewrite) while the **Verdict uses the effective (post-rewrite) intent** = exactly what the gate sees (table==gate, test-proven). Footnote flags delivery-as-intraday. Malformed YAML → CONFIG ERROR row (never crashes). Folded into the Cron Officer 09:20 briefing: full HTML table in the email (new `CronReport.strategy_status` + `_section` in `render_briefing_html`), compact in Telegram (names in backtick code-spans so underscores are MarkdownV2-literal — no leak), plain mirror.

## Tests / verification
`tests/unit/test_slice2_strategy_control.py` (28): resolver truth table (8) + schema/config (4) + product/INVARIANT (2) + default-15-regression (1) + status table (7: verdict==gate, true-Type, sort, footnote, malformed, compact, disabled→WON'T) + gate both sites (5) + CNC paper placement (1). Fixed a **Part-C regression** (`test_positional_tgt_not_equal_entry_price` hardcoded R:R 2 → 4% target; now RR-aware from `cfg.tgt_risk_reward` — Part C's full suite was skipped, missed it). Full suite green.

## NOT in this slice (parked)
Delivery LIFECYCLE (squareoff/EOD/stale/overnight/GTT) = Slice 2.5; separate CNC config; intent→Enum tightening (kept validated-str). To enable real delivery later: set trade_type BOTH/DELIVERY + per-strategy enabled + restart, AFTER Slice 2.5.

Related: [[part_c_rr_standardized_1.5_24jun]] · [[cron_officer_email_leak_fix_24jun]] (briefing) · [[live_test_mode_permanent]]
