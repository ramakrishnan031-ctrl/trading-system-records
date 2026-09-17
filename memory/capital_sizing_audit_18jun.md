---
name: capital-sizing-audit-18jun
description: "How capital, position sizing, concentration cap, and MIS 5x leverage interact (read-only audit 18-Jun-2026)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

CAPITAL & POSITION SIZING AUDIT (18-Jun-2026, investigation only, no code changed).

## Config values (current)
- accounts.csv: LFL836 paper_capital=10000, capital_share_pct=1 → total_capital=₹10,000 (paper).
  In LIVE total_capital = broker get_margins().net, NOT this file.
- system_config.yaml position_sizing (lines 87-101): risk_per_trade_pct=0.01,
  max_concentration_pct=0.10, min_qty_threshold=1, max_position_value_rs=2500.0,
  max_single_order_qty=10000, min_tick_size=0.05, tier_multipliers HIGH=1.0/MEDIUM=0.70/LOW=0.50,
  dynamic_by_winrate=true, min_multiplier=0.5, max_multiplier=2.0.
- capital (lines 74-85): intraday_bucket_pct=0.70, positional_bucket_pct=0.30, daily_loss_limit=300.0,
  leverage_map INTRADAY=5.0, COVER_ORDER=6.0, DELIVERY=1.0, BRACKET_ORDER=5.0.
- risk (lines 103-109): max_open_positions=5, max_daily_trades=20, daily_loss_limit_pct=0.03.
- Pydantic models: PositionSizingConfig (config_loader.py:210), CapitalConfig:142, LeverageMapConfig:134,
  RiskConfig:367. NOTE: task's "max_position_size"/"max_concentration_size" don't exist by those names;
  real keys are max_position_value_rs (₹ notional cap) and max_concentration_pct (fraction).

## The calculation (capital/position_sizer.py:calculate, lines 149-503)
qty_by_risk          = floor(total_capital * risk_per_trade_pct / sl_distance)         # ₹100/sl_dist
qty_by_capital       = floor(bucket_avail / (entry*(1+offset) / leverage))             # uses MIS 5x here
qty_by_concentration = floor(total_capital * max_concentration_pct / entry_price)      # ₹1000/price, CASH
raw_qty   = min(the three)                                                             # line 365
tiered    = floor(raw_qty * tier_mult * perf_weight), clamped [1, raw*2]               # lines 401-405
final_qty = (tiered // lot_size) * lot_size                                            # line 411
then guards: REJECTED_LOT_SKEW, POSITION_VALUE_CAP (final*entry > 2500 → reject:439), BELOW_MIN.
Call site: signal_processor.py:586 (and watch path :1216). SL derived in _derive_prices (:1001-1036).

## KEY FINDINGS
1. BINDING CAP = max_concentration_pct (0.10), NOT max_position_value_rs (2500).
   Concentration budget = 10% × ₹10,000 = ₹1,000 notional per symbol. At ₹100-170/share that's only
   5-8 shares raw. The ₹2,500 cap NEVER binds at ₹10k capital (concentration caps lower first).
2. Then the ~0.5 tier/perf multiplier halves it. Exact match for today's fills:
   CUPID  floor(1000/168.89)=5 ×0.5 = 2  (2×168.89=₹337.78)
   INDOFARM floor(1000/147.57)=6 ×0.5 = 3 (3×147.57=₹442.71)
   KALAMANDIR floor(1000/111.52)=8 ×0.5 = 4 (4×111.52=₹446.08)
   The 0.5 = tier_mult×perf_weight (most likely LOW tier 0.50 × perf 1.0); exact split is in the
   SizingResult.breakdown JSON, not persisted to DB — re-derivable from the sizing log line / reason.
3. risk_per_trade_pct is NOT the limiter here (₹100 risk / typical 1-3% SL → 20-58 shares >> conc 5-8).

## MIS 5x leverage
- YES the system knows it: capital.leverage_map.INTRADAY=5.0, used at position_sizer.py:255 & 355
  (margin_per_share = entry/leverage) for qty_by_capital and margin_required ONLY.
- Concentration cap and max_position_value_rs are on CASH NOTIONAL (entry_price, NOT /leverage).
- broker_adapter is NOT passed to PositionSizer in main.py:1727-1742 → live-margin path (FIX-072,
  get_live_margin_pct) is INACTIVE; static leverage_map used in BOTH paper and live.
- Consequence: a ₹1,000 notional position reserves only ₹1,000/5 = ₹200 margin. ~5 positions ≈ ₹1,000
  margin used out of ₹10,000 → account heavily under-utilises margin. Task's hypothesis is essentially
  correct (caps are on cash notional; actual margin = notional/5).

## To make positions bigger (priority for Rama)
1. Raise position_sizing.max_concentration_pct 0.10 → ~0.25 (PRIMARY lever; ₹1000→₹2500/symbol).
2. Then max_position_value_rs (2500) becomes the next ceiling — raise together if needed.
3. tier_multipliers / dynamic_by_winrate (perf_weight) — the ~0.5 that halves qty.
4. risk_per_trade_pct (0.01) — only matters if SL is wide.
AUTO-derived from total_capital (scale automatically): risk_rs, concentration budget, bucket avails,
margin_per_share. INDEPENDENT absolute ₹ (must hand-edit): max_position_value_rs, daily_loss_limit.
Cross-field sanity warnings at config_loader.py:869-919 (e.g. max_position_value_rs > daily_loss_limit).
See also [[config_change_needed_concentration]].
