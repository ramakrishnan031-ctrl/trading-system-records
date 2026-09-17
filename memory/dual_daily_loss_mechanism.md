---
name: dual-daily-loss-mechanism
description: ONE daily-loss limit (daily_loss_limit_pct=0.03, 3% of ~Rs10k ≈ Rs300), enforced at TWO points (pre-trade gate + post-close breach). The old absolute capital.daily_loss_limit was DELETED 24-Jun. Corrected 19-Jul.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7cbac53e-3446-42e1-8243-b814aa9e0215
  modified: 2026-07-27T16:32:06.219Z
---

**⚠️ CORRECTED 19-Jul-2026 from config+code (the prior version described a DELETED absolute key and leaked fixture values into decision file 01).** There is **ONE daily-loss limit, enforced at two points** — NOT two limits with different keys, and NOTHING absolute.

**THE SINGLE SOURCE:** `risk.daily_loss_limit_pct = 0.03` (`config/system_config.yaml:193`, *"SOLE daily-loss authority (3% of capital), PERMANENT"*). The old absolute `capital.daily_loss_limit` (was ₹300) was **DELETED 24-Jun** (`config:131-133`). Both enforcement points read the SAME field `app_config.system.risk.daily_loss_limit_pct` (`main.py:2231` FundManager, `:2369` RiskEngine).

**TWO ENFORCEMENT POINTS, both = 3% × current capital (≈ Rs 300; capital = broker margin ≈ Rs 10,000, `fund_manager.py:440`):**
1. **Pre-trade gate** — `risk_engine.py:569` `limit = self._daily_loss_pct * snap.total`; blocks a NEW entry. It *can* include unrealized MTM, but **enforces realized-only** while `daily_loss_include_unrealized: false` (shadow default, `config:200`).
2. **Post-close breach** — `fund_manager.py:1280` `loss_limit = self._daily_loss_limit_pct * self._total`; realized-only; fires `on_daily_loss_breach` → soft_kill after a close. Reads `get_daily_realized_net_pnl` (see [[capital-operational-note]]).

**⭐ The threshold is ≈ Rs 300/day, NOT Rs 25,000 / Rs 10,000** (those were fixture constructor literals). On the live book the cost double-count (E4/W10) would have changed **0** daily-loss outcomes (N=0, closest approach Rs 243). [[e4-w10-outcome-impact-19jul]] [[e4-w10-done-17jul]]

⭐ **The "≈" above is deliberate and must stay.** Re-measured 27-Jul-2026: the base is the day's
`fm_ledger` INIT row and it moves daily — 9,875.60 (19-Jul) → 9,838.00 (22-Jul) → **9,871.80
(27-Jul)**, so the limit was Rs 296.15 today. ⛔ Never quote a rupee threshold to the paisa from a
remembered capital figure; read both the pct (from code) and the base (from the ledger).
[[capital-vocabulary]] [[feedback-no-fixed-test-baseline]]

Related: [[capital-operational-note]] [[e4-w10-outcome-impact-19jul]] [[e4-w10-done-17jul]].
