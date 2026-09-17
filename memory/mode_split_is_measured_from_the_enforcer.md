---
name: mode-split-is-measured-from-the-enforcer
description: "Which parameters are intraday/delivery-specific is decided by tracing the ENFORCER, never by a key-name pattern — a prefix search missed two live delivery caps and put a false claim on an approved screen."
metadata: 
  node_type: memory
  type: project
  originSessionId: d18f7831-33b0-47e0-9e35-d1354f8c5db5
  modified: 2026-09-02T08:41:06.102Z
---

🔬 **MEASURED 02-Sep-2026 at the deployed SHA `39292d3`. NINE parameters are
configured and enforced separately per book — ⛔ not three.**

| enforcer | resolves per book |
|---|---|
| `capital/position_sizer.py:375-384` | `risk_per_trade_pct` · `max_concentration_pct` · `max_position_value_pct` |
| `capital/risk_engine.py:326-343` | `daily_loss_limit_pct` · `max_sector_exposure_pct` · both COUNT caps |
| `capital/risk_engine.py:557-560` · `:655-660` | ⭐ OPEN_POSITIONS + DAILY_TRADES **BRANCH on `bucket == "positional"`** |

⇒ ⭐ **A DELIVERY ENTRY NEVER CONSULTS `max_open_positions` OR `max_daily_trades`.**
Plus `capital.intraday_bucket_pct`/`positional_bucket_pct` and
`capital.leverage_map.INTRADAY`/`.DELIVERY` ⇒ **nine**.
🔬 Today: **5 vs 3** open positions, **10 vs 5** daily trades — ⚠️ a LIVE difference.
⛔ An unset delivery key **RAISES at boot** (exit 5); ⛔ it never inherits.

## ⛔ THESE FOUR ARE GLOBAL — never give them a Delivery column

`max_consecutive_losses` (📄 *"the streak breaker is a portfolio-wide circuit"*,
`risk_engine.py:642-644`) · `min_pass_score` (a signal is scored **before** its
product is chosen) · `max_single_order_qty` (a **shares**-per-order cap, ⛔ not
lots) · `price_drift_threshold`.
⛔ **A duplicated value under two headings is a FABRICATED DISTINCTION.**

## 🔴 THE METHOD ERROR THIS RECORDS

⛔ **A KEY-NAME PATTERN IS NOT A MEASUREMENT.** S17 searched for a `delivery_`
**PREFIX** and concluded *"the config has no delivery variant"* for the two count
caps. 🔬 They exist under an **INFIX**: `max_open_delivery_positions`,
`max_daily_delivery_trades`. ⇒ ⚠️ an **APPROVED** screen carries a false
operational claim over a live cap.
⛔ Likewise S17 sources *Minimum Eligible Score* from `v3_chain.min_pass_score` —
📄 a value the config file itself labels a **non-gating SEED**. The live gate is
`config/scoring_weights.yaml min_pass_score`. ⭐ Same number (60), ⛔ wrong source.
⏸ Both **REPORTED and UNTOUCHED** (the S16 card forbade modifying S17) — 👤 Rama's
call.

## ⭐ HOW TO CHECK IT NEXT TIME

🔬 The deployed YAML holds **EXACTLY SEVEN** `delivery`-scoped keys. ⭐ Sweep the
config for them and assert each reaches the UI, so a NEW key added upstream cannot
silently go unshown — ⛔ never trust a hand-written list.
⚠️ ⭐ `gui09` forked **14-Aug**, BEFORE these keys landed on **22-Aug** — so a GUI
review must render against the DEPLOYED config (`git show 39292d3:config/…`),
⛔ not the branch's own.

Related: [[a-floor-is-not-a-non-vacuity-check]] · [[capital_vocabulary]] ·
[[provenance_labels_23aug]] · [[feedback_status_label_rule_27jul]]
