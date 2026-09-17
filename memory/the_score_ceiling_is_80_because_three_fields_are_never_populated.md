---
name: the_score_ceiling_is_80_because_three_fields_are_never_populated
description: atr/rsi/sector are hardcoded None in the only market-data builder, so the 100-point score can never exceed 80 and HIGH tier has never once occurred.
metadata:
  type: project
---

> ⚠️ **CORRECTED 11-Sep-2026: the ceiling is 65, not 80.** The code's own comment (`screening/quality_scorer.py:17-19 @970aabf`): 25/100 points dead-at-0 plus 20 pinned-at-half make >65 algebraically impossible (`_G2_CEILING_TRIPWIRE = 65`); `avg_volume_20d` is also hardcoded `None`, beside `atr` / `rsi` / `sector`. Measured 11-Sep by two independent read-only passes: 173,756 scored rows, max 65, 4,301 (2.48 %) at >= 60 -- the pass mark 60 admits only the 60-65 band. The body below is kept as written; its 80 was the earlier estimate.


**MEASURED 09-Sep-2026 at `3b15bbf`, on production data.**

`screening/secondary_screener.py:378 _build_market_data` is the only builder of
the market-data dict. At **`:410-414`** it hardcodes
`"atr": None, "rsi": None, "sector": None, "prev_close": None,
"avg_volume_20d": None` -- comment: *"Still not in Kite quote API; would need
instruments cache"*. ⛔ Nothing re-populates them downstream.

⇒ `screening/step_executor.py:271 _step_3_atr_filter` reads `md.get("atr")`,
sees None, and returns **0.0 always**. ⛔ It calls **no ATR helper and passes no
timeframe/interval** -- there is no ATR computation on this path to have a
timeframe. Same shape: `_step_4_rsi_range`→**0.5**, `_step_6_sector_strength`→**0.5**.

🔬 Weights (`config/scoring_weights.yaml:11-20`, sum **100**) put 10 on
atr_filter, 10 on rsi_range, 10 on sector_strength ⇒ **20 points structurally
unreachable, ceiling 80.**

🔬 Confirmed on production: 09-Sep `atr_filter=0.0` on **3441/3441** scored rows;
`market_data_snapshot.atr` null on **4384/4384**. All-time across **188,391**
rows: **max score 65**, **0 rows above 80**, tiers **LOW 188,376 / MEDIUM 15 /
HIGH 0**. 09-Sep was **LOW ×4384 — 100%**.
⭐ Non-vacuous: `price_action` in the same rows varies (1.0/0.96/0.81/0.64…) and
`ltp` is populated, so the extraction works.

⇒ `high_score_threshold: 80` (`:28`) is **unreachable by construction**;
`medium_score_threshold: 65` (`:29`) equals the all-time max; `min_pass_score: 60`
(`:22`) passed **111 of 4384** on 09-Sep.
⚠️ The raw ATR is **persisted but null** -- `market_data_snapshot` (written
`secondary_screener.py:196`) keeps the field, so there is nothing to recover.
