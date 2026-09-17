---
name: no-two-pipeline-split-deployed-20aug
description: "At origin/main 08b462b there is NO two-pipeline split: delivery and intraday share ONE tier_multipliers dict and ONE threshold pair, so any tier change moves BOTH books."
metadata: 
  node_type: memory
  type: project
  originSessionId: 3bdb2912-ae06-4bd6-bc2f-4df54526afca
  modified: 2026-08-20T03:23:24.752Z
---

**Measured 20-Aug-2026 at `origin/main` = `08b462ba175d904e8723ed34a13c956f0dd33679`:**

- `config/scoring_weights.yaml` contains **zero** delivery keys (`grep delivery` → empty).
- `config/system_config.yaml` has **no `delivery_tier_multipliers` block** at all.
- `capital/position_sizer.py` holds **exactly one** multiplier dict —
  `self._tier_multipliers` (`:155`, `:445`, `:467`) — with **no delivery branch**.

⇒ 🔑 **Delivery and intraday share one threshold pair and one multiplier dict.
Any change to `position_sizing.tier_multipliers` or to
`high_score_threshold`/`medium_score_threshold` moves the DELIVERY book too.**
Delivery is live: `delivery_enabled: true`, `force_intraday_only: false`,
`delivery_active: true`, three positional strategies in `will_trade`.

**Why it matters — a commit message asserts the opposite and is wrong on this base.**
`3cf3729` ("tier thresholds 61/62 and multipliers 0.75/0.85/1.00") says *"INTRADAY
position sizes will rise"* and marks its `delivery_tier_multipliers` line **"INERT BY
CONSTRUCTION"**. ⭐ **True on `65b7196`'s tree, which introduces the two-pipeline split.
⛔ FALSE on the deployed tree, which does not have it.** The two-pipeline split arrives
only with `65b7196` — ⛔ **not deployed**.

**How to apply:** ⛔ **Never carry a commit's own inertness claim across a base change —
re-measure it at the base you are actually shipping onto.** An "inert" tag is a claim
about a *tree*, not about a *change*. The same trap in reverse is
[[rulings_1_2_taken_07aug]] (`force_intraday_only`=false ⇒ "INERT" tags are FALSE) and
[[stated_vs_configured_limits_09aug]].

📌 **Sizing arithmetic that follows from this** (`position_sizer.py:216-220`):
`raw_qty = min(qty_by_risk, qty_by_capital, qty_by_concentration)` then
`tiered_qty = floor(raw_qty * tier_multiplier)` — the tier multiplier is applied
**AFTER** the concentration cap, so raising it moves size **up toward** the
10 %-of-total cap and **never past it**. That is why `M-C2`'s reach *shrinks* rather
than grows when the multipliers rise. See [[value_cap_card_stopped_10aug]].
