---
name: squareoff_window_protection_band_measured_10sep
description: "Measured adverse price movement and spread in the 15:00-15:20 squareoff window on this book, as evidence for choosing PASS_1/PASS_2 market_protection values -- with the censoring that limits it"
metadata:
  type: reference
---

🔬 **MEASURED 10-Sep-2026.** ⛔ **NO PERCENTAGE IS RECOMMENDED HERE.** 👤 The choice
is Rama's; this card is the evidence he asked for.

## ⭐ 1. ADVERSE EXCURSION IN THE WINDOW — 1-min candles, `analytics.db`
Reference = the **previous minute's close** (the LTP the system would have held);
worst price reachable in the **next 60 s**. 34,336 candles · 1,649 symbol-days ·
57 trading days (19-Jun → 09-Sep) · 0 synthetic. All figures **% of reference**.

| population | n | med | p90 | p95 | p99 | p99.9 | max |
|---|---|---|---|---|---|---|---|
| all traded symbols, 15:00-15:20, SELL | 32,687 | 0.068 | 0.325 | 0.473 | 0.934 | 1.837 | 4.628 |
| all traded symbols, 15:00-15:20, BUY | 32,687 | 0.064 | 0.316 | 0.463 | 0.924 | 1.877 | 8.514 |
| **MIS-held symbol-days only, SELL** | 5,756 | 0.080 | 0.376 | 0.552 | **1.044** | 1.694 | 2.897 |
| **MIS-held symbol-days only, BUY** | 5,756 | 0.075 | 0.364 | 0.543 | 0.993 | 1.843 | 2.558 |
| **15:03 (PASS_1) minute only, SELL** | 1,647 | 0.055 | 0.321 | 0.465 | 0.928 | 2.170 | 2.520 |
| **15:06 (PASS_2) minute only, SELL** | 1,648 | 0.078 | 0.358 | 0.514 | **1.120** | **3.612** | **4.628** |

⭐ **PASS_2's minute is materially worse than PASS_1's in the tail** — p99.9
**3.612 % vs 2.170 %**, max 4.628 % vs 2.520 %. ⭐ That is a *measured* basis for
"two passes with materially different protection", ⛔ not an assumed one.
⚠️ Restricting to volume>0 minutes moves nothing (1.7 % of minutes are untraded).

## ⭐ 2. SPREAD AT THAT TIME OF DAY — `market_execution_context`, 618 captures
| slice | n | med | p90 | p95 | p99 | max |
|---|---|---|---|---|---|---|
| 15:00-15:20 window | 30 | 0.067 | 0.146 | 0.198 | 0.247 | 0.259 |
| all captures, any hour | 618 | 0.067 | 0.133 | 0.185 | 0.349 | 0.760 |
| ₹100-200 band | 94 | 0.080 | 0.204 | 0.259 | 0.712 | 0.712 |
| ₹500-1000 band | 177 | 0.067 | 0.111 | 0.124 | 0.173 | 0.760 |

⭐ **Spread does NOT widen in the squareoff window** (median identical to the
all-day figure; the in-window max 0.259 % is *below* the all-day p99). ⚠️ n=30
in-window — thin, and stated as thin.

## ⭐ 3. REALISED — the 7 aggressive-LIMIT EOD SELL fills in the window
`eod_squareoff.py:1280` prices the EOD exit at `round(ltp*(1-limit_aggressive_pct),2)`
with `limit_aggressive_pct: 0.01`. ⇒ implied LTP = `intended/0.99`, so the fill's
distance from the LTP the system saw is computable:

**n=7 · min −0.005 % · median 0.016 % · mean 0.041 % · max 0.118 %.**
⭐ Every one of the 7 left **≥0.88 of the 1 % budget unused.**

## 🔴🔴 THE CENSORING — ⛔ READ THIS BEFORE USING ANY NUMBER ABOVE
- 🔬 **There has never been a MARKET order in this book: `orders` holds LIMIT and
  SL only, 1,401 rows, all time.** ⇒ §3 measures a **LIMIT** fill, ⛔ not a market fill.
- 🔴 **§3 is survivorship-biased and right-censored at 1 %.** An exit needing more
  than 1 % simply did not fill; it cannot appear in the sample. ⇒ §3 shows the
  band was *sufficient 7 of 7 times*; ⛔ it **cannot bound the tail**.
- ⭐ The censored cases are visible elsewhere: 03-Sep ANANTRAJ, 07-Sep V2RETAIL,
  09-Sep ORCHPHARMA — naked positions whose MARKET rescue was rejected outright.
- ⚠️ §1 is a **60-second** horizon and so is conservative for an order that fills
  in well under a second; ⛔ it is an upper bound on drift, not an estimate of it.
- ⭐ §1 and §2 are the two components a protection band must cover (cross the
  spread, then absorb drift). ⛔ They are **not** additive without judgement.

See [[no_order_path_can_send_market_09sep]] ·
[[emergency_exit_market_order_is_rejected_03sep]].
