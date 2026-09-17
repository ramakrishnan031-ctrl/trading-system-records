---
name: slippage_sheet_build_01jul
description: "SLIPPAGE sheet (sheet 6 of daily_trade_review.py) BUILT 01-Jul — last analytics sheet; 6 blocks from trade_slippage_log; 3-leg decomposition sums-to-total; tiers NOT persisted (W12); build-gate PASS; STAGED not-pushed. All data/analytics sheets done — only Dashboard remains"
metadata:
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**01-Jul-2026 — SLIPPAGE sheet (sheet 6) built** — the LAST analytics sheet of
`reports/daily_trade_review.py` (absorbs the parked "Slippage Phase-2 reports"). Follows
[[strategies_sheet_build_01jul]] / [[config_sheet_build_01jul]] / [[orders_sheet_forensic_master_01jul]].
STAGED, NOT pushed. NO schema / NO cron / NO trading-code. Read-only, mode-agnostic.

**Source:** `trade_slippage_log` (the per-trade roll-up `orders/slippage_recorder.py` writes) + the Orders
`records` (gross P&L + entry tolerance `slip_delta`). DB-pure.

**★ DECOMPOSITION = 3 legs, not 4** (verified against the system's own `calc_rr_damage_pct`):
`total slip cost/trade = (entry_slippage_rs + sl_slippage_rs − tgt_slippage_rs) × qty` — ENTRY adverse(+),
SL-exit adverse(+), **TGT-exit favourable(−, subtracts)**. The 3 components SUM to the total by construction.
There is NO 4th leg — SL/TGT ARE the two exit paths (mutually exclusive per trade). EOD/manual-exit slippage
is NOT captured by the roll-up (it only sets sl_fill on SL_HIT / tgt_fill on TGT_HIT) — flagged as a follow-up.

**★ TIER FINDING (the key PHASE-1 discovery):** `slippage.tiers` (liquid=5/mid=15/small=30 bps) is resolved
at RUNTIME by `broker/slippage_engine.tier_for(symbol)` via **InstrumentCache** (F&O→liquid, non-F&O→mid,
unknown→default) — a PAPER-fill simulation model — and is **NOT persisted per trade** (trade_slippage_log has
`price_band`, not a tier). So there is NO DB-pure per-trade tier. Per the runbook's fallback, **Block 2
buckets by the recorded `price_band`**; the configured tier bps (from W0 `config_snapshots`) are shown as a
REFERENCE only (gracefully omitted when no snapshot exists for the date, e.g. 30-Jun). **W12** = persist the
resolved slippage tier per trade → enables true per-tier actual-vs-expected.

**6 blocks:** (1) SUMMARY+DECOMPOSITION (total slip cost · ENTRY/SL/TGT component totals · slippage as % of
gross P&L), (2) BAND ANALYSIS (per price_band: trades·avg/max/min entry bps·cost + tier-bps reference),
(3) STRATEGY-WISE, (4) STOCK-WISE, (5) WORST-20 (by slip cost: symbol·strategy·entry slip ₹/sh·total cost·
excess-over-tolerance), (6) 10-DAY TREND (trailing 10 sessions). `build_slippage_data`/`render_slippage_sheet`
(reuses `_render_strat_table` for the tabular blocks); `_slip_tiers_for_date`.

**Rounding discipline:** aggregates at FULL precision, rounds ONCE for display — so the decomposition sums to
the total EXACTLY (no rounding leakage; the first cut rounded per-trade then summed → 2-paisa drift, fixed).

**BUILD-GATE PASSED (all 3, real 30-Jun VM backup):** (a) total slip cost ₹19.65 == Σ per-trade recomputed
independently from the log; (b) decomposition ENTRY(−0.13)+SL(0.20)+TGT(19.59)=19.65 == total (no leakage),
each component == the independent sum; (c) band '200-300' stats recomputed independently match. Honest signal
surfaced: slippage cost = **249% of the day's ₹7.89 gross** — dominated by CGCL's adverse TGT_HIT-at-loss exit
(the same CGCL the Orders sheet renders faithfully). Tests: `tests/unit/test_daily_trade_review.py` now **47**
(+2 Slippage: decomposition-sums-to-total [entry+sl−tgt identity + %-of-gross + worst sort + band agg], and
empty-graceful [no rows → total 0, pct None, empty blocks]).

**Docs updated:** `docs/report_data_contract.md` (new "Sheet: Slippage" section; Slippage removed from pending),
`docs/SYSTEM_MAP.md` (header prepend + reports line sheet-6), `PATHS.md` (generator/Slippage-row/backlog/test).

**★ STATUS: ALL data + analytics sheets DONE** — Orders, Signals, Reconciliation, Config, Strategies, Slippage.
**Only the DASHBOARD remains** (the final sheet, built on all six: capital via `fm_ledger`, the Reconciliation
OVERALL banner, roll-ups of the six). Build-gate = the totals/decomposition validation (PASSED) + Rama approval
before the Dashboard begins.

**Backlog carried:** W12 (persist slippage tier per trade + EOD/manual-exit slippage capture). Prior open items
unchanged: W0.1, W2, W5–W11.
