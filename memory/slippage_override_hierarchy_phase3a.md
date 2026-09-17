---
name: slippage_override_hierarchy_phase3a
description: Phase 3a manual slippage-tolerance override hierarchy (Symbol>Strategy>Band>Global) + schema v32 tolerance_source persistence
metadata: 
  node_type: memory
  type: project
  originSessionId: 0084080d-8dce-4adb-88eb-2c4b5a0e4693
---

Slippage tolerance override hierarchy — **Phase 3a (MANUAL), schema v32, 20-Jun-2026.**
Builds on [[slippage_intelligence_phase1]] (v31 raw layer) and [[tiered_slippage_abort]]
(the `entry_gate.slippage_control` sl_fraction model, global 0.22).

**What:** Rama can now set per-symbol / per-strategy / per-price-band entry-slippage
tolerance fractions NOW (from trading knowledge), without waiting for Phase 3b's
auto-recommender. New config `entry_gate.slippage_control.overrides`:
`enabled` + `by_price_band` / `by_strategy` / `by_symbol` maps — **all ship FULLY
EMPTY** (commit 8fd54a8, Rama's call): every entry resolves to the global **0.22**
baseline everywhere for clean data collection first; add overrides later from
real evidence. (The initial commit 2ce54ab had one example band `0-100: 0.18`;
8fd54a8 cleared it too.)

**Resolution (the rule):** effective `sl_fraction` = MOST-SPECIFIC-WINS
**Symbol > Strategy > Price Band > Global** (first match). Pure
`resolve_slippage_fraction(cfg, symbol, strategy, price_band) -> (fraction, source)`
in `orders/order_placer.py`; threaded into `_slippage_decision`/`_compute_slippage_tolerance`
via a new keyword `fraction_override`. Resolved once in `place()` (BEFORE create_trade;
band from `signal_trigger_price` or `entry_price` via `get_price_band`) so it both drives
the pre-order abort guard AND is recorded. **Only `sl_fraction` mode uses overrides**
(flat_tiers/pct carry their own per-band Rs; they record NULL source).

**Persistence (schema v32, closes the Phase-3b loop):** `tolerance_fraction_used` (REAL)
+ `tolerance_source` (TEXT, e.g. `symbol:IDEA` / `strategy:gap_fade` / `band:0-100` /
`global`) added to **trades** (written by `OrderManager.create_trade`, 2 new optional
kwargs) AND **order_execution_log** (the async `slippage_recorder._enrich_order` reads them
from the parent trade and copies onto the execution row; `_OEL_COLS` extended).
`MIGRATION_TABLES[32] = [trades, order_execution_log]` rebuilds both (new cols → NULL);
`EXPECTED_SCHEMA_VERSION` 31→32. Phase 3b query: `SELECT t.tolerance_source,
AVG(s.rr_damage_pct) FROM trades t JOIN trade_slippage_log s USING(trade_id) GROUP BY 1`.

**Transparency:** logged per entry (`entry_slippage_observed` + `slippage_guard_exceeded`
+ Telegram abort body show `tolerance_source`/`tolerance_fraction`).

**Validation:** config HARD-REJECTS fractions outside `(0,1]` (pydantic `SlippageOverridesConfig`).
`validate_slippage_overrides()` (pure, in order_placer.py) WARNS at startup (main.py, after
strategies load) on extreme values (<0.05 / >0.50) and on `by_symbol`/`by_strategy` keys that
match no known instrument/strategy (typo → silently ignored). Never rejects/blocks startup.

**System Manager EOD: 10th check `SLIPPAGE OVERRIDES`** (`slippage_overrides_check`) —
**VISIBILITY ONLY, never a violation / never SOFT_KILL**: active override counts + per-
`tolerance_source` placed/rejected usage today. (REJECTED counts any reason, so the "review"
marker is a hint, not a signal.)

**Parity:** mode-agnostic, paper + live. **Migration verified** on a built DB
(DROP-COLUMN-simulated v31 → migrate → cols added, rows preserved, round-trips) — local PC,
NOT the real VM DB (VM migration runs on next restart). Activates next restart.

**Tests:** +27 (test_slippage_control 20 incl. the 5 spec examples + validate; test_slippage_recorder
+1 enrichment; test_migrations +1 v31→v32). Fixed brittle version-pins: test_slippage_recorder
==31→>=31/==EXPECTED; test_p0_live_day1_fixes ==30→>=30 (was already red at v31).

**Phase 3b (auto-recommendation from accumulated rr_damage) = PENDING.** Commit 2ce54ab.
