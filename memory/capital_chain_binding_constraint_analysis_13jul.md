---
name: capital_chain_binding_constraint_analysis_13jul
description: "Capital/sizing chain READ-ONLY analysis (13-Jul) — 100% of trades are CONCENTRATION-bound (~Rs 990/position, no leverage); qty_by_risk binds 0/255; system IS margin-aware (reserves value/5, matches broker 87.68 vs 91.74); LOW tier 0.5 DOES halve size in 78% of trades; ~7% of buying power deployed. Fixing M-S4 WOULD change sizes (via tier) for conc>=2 trades. NOT fixed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d1e6c9d-1d21-4715-b704-3b6d175f00db
---

**CAPITAL CHAIN binding-constraint analysis (13-Jul-2026, READ-ONLY, nothing changed). 318 trades in backup `trading_system-2026-07-13.db` + today live. Hand to Web Claude + ChatGPT.**

**T1 sizer arms (`capital/position_sizer.py::calculate`), total_capital = broker net ≈ Rs 9,908:**
- `qty_by_risk = floor(capital*risk_pct/sl_dist)` = floor(~99/sl_dist). `risk_per_trade_pct=0.01`.
- `qty_by_capital = floor(avail/(price/leverage))` = floor(~34,700/price). `leverage_map.INTRADAY=5.0` × `intraday_bucket_pct=0.70` (bucket ≈ Rs 6,935).
- `qty_by_concentration = floor(capital*conc_pct/price)` = **floor(~990/price), NO leverage.** `max_concentration_pct=0.10`.
- `raw_qty=min(3 arms)`; tier: `tiered=max(1, min(floor(raw*tier*perf), raw*2))` applied to the MIN. `tier_multipliers` HIGH1.0/MED0.7/LOW0.5, `position_sizing.enabled=True`.
- POSITION_VALUE_CAP reject if qty*price>40%*capital≈Rs 3,963 (`max_position_value_pct=0.40`; anomaly guard, ~never).
- `fund_manager.reserve()` reserves `required_margin = qty*price/leverage` (FM4, leverage-aware, line 510). risk_engine 10 admission gates (kill-switch, `max_open_positions=5`, max_daily_trades, `max_sector_exposure_pct=0.40`, `max_consecutive_losses=4`, `daily_loss_limit_pct=0.03`, dup-symbol, capital-avail) = reject/allow, NOT size.

**T2 BINDING CONSTRAINT = 100% CONCENTRATION.** `binding_constraint='concentration'` in **255/255** sized trades (63 of 318 unsized=REJECTED/FAILED/pre-schema). Recompute of min(risk,capital,conc): CONCENTRATION sole-min 255/255. **`qty_by_risk` bound 0 times. capital 0. concentration 255.** Rama's hypothesis confirmed exactly: the ~Rs 990/position cap (10% of Rs 9,908, no leverage) dominates; stocks >Rs 990 → conc=0 → un-tradeable (today's REJECTED_SIZING_CONCENTRATION).

**T3 MIS LEVERAGE — system IS margin-aware; leverage-blindness bug REFUTED.** margin/value ratio = **0.200 median (=1/5)** across 255 trades. Reserves Rs 2,000 for a Rs 10,000 MIS position, not Rs 10,000. **Broker cross-check:** today's 1 open (ZAGGLE, val Rs 438) → system margin **Rs 87.68 ≈ broker used Rs 91.74** (both ~20%). A capital/reservation limit blocked a broker-affordable trade: **never** (qty_by_capital 0/255).

**T4 TIER — enabled, 100% LOW (0.5), perf 1.0 (exactly M-S4's ~65-ceiling prediction), and it DOES bind.** The task's premise "tier scales only qty_by_risk → does nothing" is WRONG in code: tier scales `raw_qty` (the concentration min). **`planned<conc` in 200/255 = 78%** (conc 4→2, 3→1, 2→1; conc=1 floored→unaffected, 55 trades). **Web Claude's ORIGINAL "half size" claim is empirically correct for 78% of trades.** Live today matches: CANHLIFE conc6→3, PURVA conc4→2, ZAGGLE conc4→2, KALYAN conc1→1.

**T5 DEPLOYMENT ~7%.** Intraday buying power ≈ Rs 6,935×5 = **Rs 34,700 notional**; peak realized concurrent ≈ Rs 2,500 notional / Rs 500 margin → **~7% used, ~93% idle.** Attribution: concentration cap (Rs 990 × max 5 = Rs 4,950 ceiling) removes ~86%; LOW tier halves conc≥2 → removes ~half the rest; max_open_positions=5 bounds count.

**T6 BOTTLENECK (ordered):** (1) **per-trade concentration cap** (Rs 990/pos, no leverage; 100%) — HIGH blast radius, couple with max_position_value_pct + Rama risk appetite; (2) **LOW-tier 0.5** (halves 78%) — coupled with M-S4; (3) max_open_positions=5; (4) leverage/risk/capital already correct, no action.

**❓ Would fixing M-S4 alone change POSITION SIZES? YES (refutes Web Claude's new "selection-only").** M-S4 ↑score → ↑tier → tier scales concentration-bound raw_qty: **conc≥2 (78%, cheaper stocks) size up to 2× (LOW0.5→HIGH1.0); conc=1 (22%, Rs 450-990) unchanged (floored); the Rs 990 ceiling itself untouched.** So M-S4 = selection PLUS a bounded cheap-stock size increase — must be in the M-S4 impact proof. **M-S4 (selection) and the concentration cap (size) are TWO separate problems; fixing one does not fix the other.** Related: [[m_s4_dead_scorer_steps_investigation_13jul]] · [[capital_operational_note]]. NOTHING changed — analysis only; every sizing change needs its own impact proof + Rama sign-off (live account).
