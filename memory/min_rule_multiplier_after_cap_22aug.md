---
name: min-rule-multiplier-after-cap-22aug
description: "The tier/perf multiplier is applied after min(risk, capital, concentration) and nothing re-caps, so a cap before a x2 multiplier is not a cap"
metadata: 
  node_type: memory
  type: project
  originSessionId: b3398573-7588-48ce-8ab3-97f2c5107eaf
  modified: 2026-08-22T18:08:56.129Z
---

# NI-16 — A CAP APPLIED BEFORE A ×2 MULTIPLIER IS NOT A CAP

**Measured 22-Aug-2026 late evening at `742d9da`** (`M3` — line numbers hold only there).
⚠️ The sizing math is **byte-identical to the deployed `4568385`** (252-point grid), so this
describes what runs today. Full audit: `docs/audit/MIN_RULE_AND_DELIVERY_LIMITS_22-Aug-2026.md`.
Related: [[stated-vs-configured-limits-09aug]] · [[no-two-pipeline-split-deployed-20aug]] ·
[[value-cap-card-stopped-10aug]] · [[unpushed-pending-deploy-ledger]].

## THE ORDER

```
:485  raw_qty    = min(qty_by_risk, qty_by_capital, qty_by_concentration)   <- THE MIN
:584  tiered_qty = floor(raw_qty × effective_mult)                          <- MULTIPLY, AFTER
:587  tiered_qty = max(1, min(tiered_qty, raw_qty × 2))                     <- clamps only to 2× raw
:611  final_qty  = (tiered_qty // lot_size) × lot_size                      <- FLOOR
:650  position_value > eff_max_position_value_pct × total  -> REJECT        <- the ONLY re-cap
```

⛔ **Neither the risk rung nor the concentration rung is ever re-applied.** The single
post-multiplier cap **REJECTS the trade** rather than clamping it.

## MEASURED, ⛔ NOT ARGUED — live config, total ₹10,645.60

| `perf_weight` | conc rung | final | notional | verdict |
|---|---|---|---|---|
| 1.0 | 10 sh | 10 | ₹1,000 | within |
| 1.5 | 10 sh | 15 | ₹1,500 | ⛔ over by 5 |
| **2.0** | 10 sh | **20** | **₹2,000** | 🔴 **2× the rung** |

- **Risk budget breached too:** `0.01 × 10,645.60 = ₹106.46`; at `perf_weight=2.0` the
  delivered `risk_amount = ₹200.00`.
- ⚠️ **The `constraint` field still reports `CONCENTRATION`** while the result is twice that
  rung — an attribution field naming a rung the result exceeds.
- **DELIVERY book behaves identically** (`bucket=positional`, 10 → 20).
- In Rama's own worked example the doubled quantity breaches the position-value cap and the
  outcome is **`qty=0, POSITION_VALUE_CAP`** ⇒ 🔴 **two failure modes: over-size, or the
  signal is DROPPED entirely.** ⛔ Neither is "take the lower — that is the final quantity".

## ⚠️ LATENT, ⛔ NOT LIVE — and it is a CONDITION, ⛔ not a property

`perf_weight` reaches the sizer only via `signal_processor.py:1009/:1948/:2265` as
`self._perf_weights.get(name, 1.0)`, and **`main.py:3141` constructs `SignalProcessor` with
NO `perf_weights` kwarg** ⇒ the dict is empty ⇒ always **1.0**. With `tier_mult ≤ 1.0` the
multiplier can only REDUCE today.

🔴 **It becomes LIVE the moment the PerformanceAllocator is wired — `max_multiplier: 2.0`
is already in config.** (`N20-48`: the 1.0 is a condition, not a property.)

## ⭐ IT IS THE MISSING HALF OF NI-2

NI-2 made `config_auditor` C2 audit the **config** for exactly this hazard
(`conc × max effective multiplier` vs the position-value cap). ⛔ **Nothing re-caps the
RUNTIME result.** The auditor can now warn that the shape is dangerous; the sizer still
produces the over-sized quantity.

## ⛔ WHAT WAS NOT DONE

⛔ No fix built. ⛔ No fix designed. The shape *would* be a re-cap of `tiered_qty` against
the same rungs after `:584` — **a clamp, not a reject** — but that is a money-path change
requiring its own authorisation, its own gate and a frozen prediction. ⛔ **Not started.**

⭐ **What IS compliant:** steps 1–5 of the rule. `min()` at `:485` is real, each pct rung
takes the **selected segment's own key** (`:356-366`, `_require_delivery` has no
else-returning-a-global), and Rama's example reproduces **exactly — 50 shares / ₹5,000**.

## 🔴 23-Aug-2026 — ⛔ NI-16 IS **NOT** FIXABLE BY PORTING THE CLAMP

The authorised read of `65b7196` (build record §4.1) found the clamp: `effective_mult = min(1.0, tier × perf_weight)`, pinned by `test_the_multiplier_is_clamped_to_one_and_scaling_is_monotonic`, enforcing `N9-10`'s LOCKED *"within the single-allocation ceiling"*.

⭐ **The right wording, and it matters:** deployed does not merely LACK the clamp — `4568385:capital/position_sizer.py:530` **carries the exact FIX-133 expression `max(1, min(tiered_qty, raw_qty * 2))` that `65b7196` DELETED as forbidden.** The presence of a thing a later locked decision removed, ⛔ not an absent protection. *"Never ported"* invites someone to port it.

🔴 **AND PORTING WOULD NOT WORK — THERE IS NO ALLOCATION FOR A CEILING TO BE *OF*.** Measured: `capital/pipeline_policy.py` **does not exist** at `4568385` (`git ls-tree`), and `allocation_divisor` has **zero** hits repo-wide there; both live only in `65b7196` (`position_sizer.py:433`, `base_allocation` `:439`). Deployed's per-trade capital arm is `avail = snap.intraday_avail` (`:294`) → `qty_by_capital = floor(avail / margin_per_share)` (`:419`) with `fund_manager.py:478` `_intraday_avail = broker_balance * _intraday_pct` — **the WHOLE bucket**. `65b7196` instead computes `basis = segment_bucket × planning_leverage` → `allocation = basis / max_daily_trades` (`position_sizer.py:13-14`).

⇒ `min(1.0, …)` clamps a multiplier **to one allocation**. Dropped onto deployed it would clamp against a rung that is **10% of TOTAL CAPITAL** — ⛔ a different rule wearing the locked policy's words. ⭐ Recorded as **F12 instance 3**; see `docs/audit/F12_INSTANCE3_AND_GATE_GUARD_23-Aug-2026.md`.
