---
name: config_sheet_build_01jul
description: "CONFIG sheet (sheet 4 of daily_trade_review.py) BUILT 01-Jul — first consumer of W0 config_snapshots; DB-pure sectioned key/value; value spot-check PASS; STAGED not-pushed"
metadata:
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**01-Jul-2026 — CONFIG sheet (sheet 4) built** — the FIRST consumer of [[w0_config_snapshots_01jul]].
Part of the daily-report redesign; sits in `reports/daily_trade_review.py` alongside
[[orders_sheet_forensic_master_01jul]] (sheets 1–3). STAGED in the working tree, NOT pushed
(Rama pushes off-market). NO schema / NO cron / NO trading-code.

**What it is:** a sectioned two-column key/value view of the day's resolved `AppConfig`, read ONLY
from `config_snapshots.config_json` (the day's latest row by `snapshot_ts`) — never the YAML. Nested
values render as indented SUB-ROWS. Header = `Config snapshot for <date>` + Snapshot ID · Captured-at
· Mode · Account · trade_type · hash. **NO-snapshot case** (pre-W0 dates) → the whole sheet is an
honest `— pending W0 (no config snapshot for this date)` placeholder, never blank.

**Section → config_json path map (VERIFIED against a real `core.config_loader.load_all()` dump):**
- SYSTEM: `$.system.{trade_type,force_intraday_only,delivery_enabled}` + `.trading_hours.*` +
  `.capital.leverage_map.*` (INTRADAY/COVER_ORDER/BRACKET_ORDER/DELIVERY). **max_capital is NOT in
  config** → honest `— not in config (runtime account balance)` (never a fake number).
- RISK: `$.system.risk.*` + `$.system.position_sizing.{max_position_value_pct,max_concentration_pct,risk_per_trade_pct}`.
- SCORING: `$.scoring.{min_pass_score,high/medium_score_threshold}` + `$.scoring.steps.*` (weights, Σ=100, sub-rows).
- SLIPPAGE: `$.slippage.{default_tier,tiers.*.slippage_bps}` (liquid/mid/small) + `$.system.entry_gate.{max_entry_slippage_pct,slippage_buffer}`.
  NOTE the real slippage shape is **tier-based bps**, NOT the "price-slab → allowed" the runbook imagined — rendered to the truth.
- BROKER COSTS: `$.broker_costs.zerodha.*` (equity rates; futures/options sub-dicts present, not expanded).
- STRATEGY: `— pending W0.1` — per-strategy config is NOT in config_snapshots (top-level keys are
  broker_costs/broker_limits/chartink_scanners/file_hashes/nse_holidays/scan_webhook_map/scoring/slippage/system —
  no `strategies`); strategies load via StrategyLoader, a separate domain.

**Code:** `build_config_data(store, date)` → (sections, meta); `render_config_sheet(wb, sections, meta)`;
helpers `_cfg_get` (dotted-path nav) / `_cfg_val` (faithful: bool→'True'/'False', None→'', numbers/str as-is).
Wired into `generate()` as the 4th `render_*` call; log line notes config=yes/pending-W0.

**BUILD-GATE PASSED** (the runbook's required spot-check): fresh v41 StateStore + real `load_all()`
snapshot (`snapshot_config`) → 8/8 value spot-checks PASS incl. the 4 required (min_pass_score=60,
daily_loss_limit_pct=0.03, leverage INTRADAY=5.0, entry_end=15:00) — each renders from config_json
unchanged; NO-snapshot placeholder proven; all 4 sheets present `['1_Orders','2_Signals','3_Reconciliation','4_Config']`.
Tests: `tests/unit/test_daily_trade_review.py` now 41 (+3 Config: no-snapshot→pending-W0, sections+spot-values,
capital-wording); full file 41 pass + `test_config_snapshotter.py` 10 pass.

**HOUSEKEEPING done this pass** (code NB in `build_reconciliation` + `docs/report_data_contract.md` +
PATHS.md): the CAPITAL block no longer calls `RESET_PNL` "pollution" — it is a BY-DESIGN daily EOD reset.
The real reason `get_daily_realized_net_pnl` is avoided = **W10** (it double-subtracts costs). See
[[get_daily_realized_pnl_double_cost_01jul]].

**Docs updated:** `docs/report_data_contract.md` (new "Sheet: Config" section + CAPITAL note fix + footer),
`docs/SYSTEM_MAP.md` (header prepend + reports line sheet-4), `PATHS.md` (generator/reconciliation/backlog/test rows).

**★ BACKLOG recorded (NOT built — future tasks):**
- **W0.1** — strategy-config snapshot writer: a `config_strategy_snapshots` table + a writer AFTER
  StrategyLoader (main.py ~2292) → fills the Config STRATEGY section for future dates. Own task.
- **W10** — `get_daily_realized_net_pnl` double-cost fix (write/read contract): committed permanent fix,
  NON-URGENT (safe direction, biased conservative), its OWN careful task; parity automatic. See [[get_daily_realized_pnl_double_cost_01jul]].
- **W11** — NULL-exit CLOSED_MANUAL trades lack `net_pnl` → excluded from `Σ trades.net_pnl` → can FAIL
  the Reconciliation CAPITAL block HONESTLY on such days. Data-quality; track.

**Build-gate = the value spot-check (PASSED) + Rama approval before the Strategies sheet begins.**
