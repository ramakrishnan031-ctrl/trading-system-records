---
name: slippage_calibration_data_20jun
description: "TGT/SL/R:R config + real slippage data to calibrate the tiered slippage bands (20-Jun, READ-ONLY). CRITICAL: SL fixed from SIGNAL, TGT recalc from FILL (FIX-013) -> slippage directly inflates risk + erodes edge. Real slippage usually ~0 (median 0%, max 1.15%)."
metadata: 
  node_type: memory
  type: project
  originSessionId: e7a6af13-236a-41d8-aca5-213b591647fd
---

**SLIPPAGE CALIBRATION DATA (20-Jun-2026, READ-ONLY investigation for tiered-slippage band design;
[[tiered_slippage_abort]]).**

## TGT / SL / R:R (config/strategies/*.yaml)
- **SL** `sl_pct`: **0.8%–2.0%** (vwap 0.8%, gap_fade/range/breakout 1.0%, gap_go 1.2%, first_pullback 1.5%,
  positional 2.0%). Formula (price_math.calc_sl_price): `SL = entry × (1 ∓ sl_pct)`.
- **R:R** `tgt_risk_reward`: **1.5–2.5** (gap_fade 1.5; gap_go 2.5; everything else 2.0).
- **TGT% = sl_pct × R:R = 1.5%–4.0%** (TIGHTEST: gap_fade 1.5%, vwap 1.6%; widest: positional 4.0%).
  Formula (calc_tgt_price): `risk=|entry−SL|; TGT = entry ± risk×rr` ⇒ `TGT = entry × (1 ± sl_pct×rr)`.

## CRITICAL: SL from SIGNAL, TGT recalc from FILL (FIX-013, order_placer.py:2437)
"Recalculate TGT from actual fill price to preserve R:R. SL stays anchored to original strategy level."
So on a LONG that slips up by S (fill = signal+S): **SL fixed** at signal-based level ⇒ **actual risk
grows by S** (fill−SL = signal·sl_pct + S); **TGT recalc'd from fill** keeps R:R relative to the bigger
risk ⇒ absolute TGT moves further away. Net: **entry slippage directly inflates risk (+S) AND erodes
edge (~S against the reward / needs a bigger move)** — the TGT recalc does NOT save the edge, it moves
the goalpost. Confirms Rama's insight; slippage tolerance should be SMALL vs the SL/TGT distance.

## Guard comprehensiveness (order_placer.place())
- Runs for ALL entries (both protocols go through `place()`); entries are **never MARKET** — LIMIT_TRIPLE
  = LIMIT entry; CO = `order_type="SL"` (stop bracket). So price-controlled by order type.
- **Bypass/skip conditions:** the guard `if signal_trigger_price>0` and `if _slip_ltp is not None` — so
  it SKIPS when (a) the signal has no trigger price, or (b) LTP can't be fetched (best-effort). On skip,
  only the order type + the FLAT `entry_gate.slippage_buffer` (₹2.0, the entry-LIMIT offset:
  `limit = min(signal+buffer, LTP)` LONG) bound the fill.
- NB **THELEELA filled signal+₹3.10 > the ₹2.0 buffer** (positional_sector_rotation, during the 19-Jun
  FIX-190 incident) — positional/CO entries or the incident path can exceed the LIMIT buffer; worth a look.

## Real slippage (last 24 filled entries, trades table entry_target vs entry_actual)
**median 0.000%, mean 0.080%, max 1.154%, min −0.144%.** Only **3/24 unfavorable**: THELEELA 0.64%/₹3.10,
CHEMPLASTS 1.15%/₹2.55 (221→223.6), LLOYDSENGG 0.52%/₹0.43 (83→83.44). Most LIMIT entries fill EXACT or
better. Tiers (₹2.00 in 200-500 band) would abort THELEELA + CHEMPLASTS, allow the rest.

## Spread data? YES
- `config/slippage_model.yaml`: per-liquidity-tier slippage bps (liquid 5 / mid 15 / small 30) — PAPER
  fill sim + cost calc. - Live liquidity gate: `entry_gate.max_spread_pct=0.5%`, `min_depth_qty=500`
  (real bid-ask spread + depth pre-entry). No historical "avg intraday move per band" stored (external).

## Calibration implication (for Rama's "slippage ≤ 20-25% of edge")
Edge (TGT%, SL%) is a PERCENTAGE; a flat-₹-per-band tolerance is a larger % at LOWER prices in a band, so
it does NOT consistently stay ≤25% of edge — worst for the TIGHTEST-TGT strategies (gap_fade 1.5%, vwap
1.6%). E.g. 200-500 band ₹2.00 tol vs a 1.5% gap_fade TGT: at ₹200 → 67% of TGT; at ₹500 → 27%. vs SL
distance (₹2.00 / sl_pct·price): positional(2%) 21%, gap_fade(1%) 42%, vwap(0.8%) 52% at ₹481.
⇒ Options to discuss (NOT built): (1) tolerance as a **% of SL/TGT distance** (auto-scales with price +
strategy); (2) tighter low-price bands; (3) per-strategy tolerance keyed to the tightest TGT. Current
flat-₹ bands are simple + fine for the observed (tiny) slippage, but loosest exactly where edge is
thinnest. Related: [[tiered_slippage_abort]], [[fix_190_incident]].
