---
name: e4-w10-outcome-impact-19jul
description: "19-Jul READ-ONLY: the E4/W10 cost double-count would have changed the daily-loss outcome on N=0 of 23 book days. Established the REAL production threshold first (3% × ~Rs10k ≈ Rs300, single-source, no absolute) — the decision file had fixture values (5%/25k/10k). Closest approach Rs 243; not robust to a ~5× sizing rise."
metadata: 
  node_type: memory
  type: project
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-07-19T08:10:13.509Z
---

**E4/W10 OUTCOME-IMPACT (19-Jul-2026, READ-ONLY, docs-only).** Report
`docs/audit/e4_w10_outcome_impact_19jul2026.md`. Live DB provably untouched (`6df0c09a…`). Snapshot
queries only, never `scripts/*.py --db`.

## ⭐ THE PRODUCTION DAILY-LOSS THRESHOLD, STATED ONCE AND CORRECTLY (stop the fixture leak)
**ONE limit: `daily_loss_limit_pct = 0.03`** (`config/system_config.yaml:193`, "SOLE authority, PERMANENT").
The absolute `capital.daily_loss_limit` (was ₹300) was **DELETED 24-Jun** (`config:131-133`). **No absolute
mechanism, no second key.** Both enforcement points read the same field (`main.py:2231` FundManager, `:2369`
RiskEngine) and apply **3% × current capital**, realized-only (`daily_loss_include_unrealized:false`):
pre-trade gate `risk_engine.py:569`, post-close breach `fund_manager.py:1280`.
**Capital base = broker margin ≈ Rs 10,000** (`fund_manager.py:440` `_total=broker_balance`; ledger INIT rows
Rs 9,995–10,040; the Rs 1,000,000 12-Jun INIT is the pre-sync fixture seed). ⇒ **threshold ≈ Rs 300/day**
(moving <Rs 2/day). **NOT Rs 25,000 / Rs 10,000** — those were fixture constructor literals that leaked via the
stale [[dual-daily-loss-mechanism]] memory into decision file 01. Both now corrected. **Batch 2's single-source
conclusion CONFIRMED.**

## ⭐ N = 0 OF 23 DAYS — the double-count never changed a daily-loss outcome
Deployed reader = **Option B** (Σpnl_delta − Σcosts), proven: every `RESET_PNL` row = −net_B on all 22 reset
days. Per-day, both readings, worst intraday running-cumulative, vs the −Rs 300 threshold ⇒ **N=0.**
**Closest approach: 07-07, worst cum_B −56.47 = Rs 243.5 of margin** (worst day = 19% of the limit). For a
double-count-only flip a day's true-net loss must land in (−300, −294.4]; the worst the book reached is −56.47.
**§B4 scaling:** N=0 is structural (~5.3× headroom) but **NOT robust to D1** — ~4× sizing → margin ~Rs 74; ~5.3×
→ the day breaches under BOTH readings (double-count moot). Capital top-up raises the threshold ⇒ more robust.
36 pre-fix `costs=0` gross rows make Option B *less* divergent ⇒ cannot manufacture a straddle; N=0 stands.
**Posture call (adopt Option A vs keep B) stays Rama's — now against a number, not a feeling.**

## ⭐ §C TRIAGE — which of the 10 decisions are cheaply settleable
**COMPUTABLE NOW** (existing data/harness, no deploy): **D3** (out-of-sample 1-min band-inversion stability),
**D4** (out-of-sample exit backtest), **PerformanceAllocator** (reachability algebra vs the 100%-binding conc cap).
**NEEDS SYSTEM RUNNING:** D1 (positive-edge re-soak), Regime (~2.2 months). **NEEDS RAMA:** E4/W10 (posture,
now computed), Freeze-min_pass (priority), Prune-retention (intent). **BLOCKED:** D2 + Regime (Q10 Kite token),
Throttle (#10, on D3). Caveat: D3/D4 "out-of-sample" needs fresh 1-min data (only ~2 months / single regime exists).

## ⭐ LESSON (§C2): establish a threshold from CODE before computing against it
E4/W10's own "what would settle it" silently assumed the thresholds — they were wrong by ~50×. **A settlement
that computes against a config value must read that value from code first**, not from a decision file or memory.
D1 (concentration cap) and D3 (`min_pass_score`) carry the same shape — read the live value before acting.

Related: [[dual-daily-loss-mechanism]] [[e4-w10-done-17jul]] [[capital-operational-note]]
[[decision-packages-19jul]] [[feedback-verify-the-finding-premise]] [[capital-chain-binding-constraint-analysis-13jul]]
