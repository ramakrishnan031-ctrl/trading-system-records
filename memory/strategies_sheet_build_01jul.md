---
name: strategies_sheet_build_01jul
description: "STRATEGIES sheet (sheet 5 of daily_trade_review.py) BUILT 01-Jul — first analytics sheet; 5 tables from the trades truth layer + trailing confidence-weighted composite ranking; build-gate PASS; STAGED not-pushed"
metadata:
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**01-Jul-2026 — STRATEGIES sheet (sheet 5) built** — the first ANALYTICS sheet of
`reports/daily_trade_review.py`. Follows [[config_sheet_build_01jul]] / [[orders_sheet_forensic_master_01jul]].
STAGED in the working tree, NOT pushed (Rama pushes off-market). NO schema / NO cron / NO trading-code.
Read-only, mode-agnostic (PAPER/LIVE identical).

**Source decision:** aggregate DIRECTLY from the `trades` truth layer (the same Orders `records` +
Signals `srecords` the earlier sheets proved) — **`strategy_metrics` INTENTIONALLY NOT used** (it is a
thin, derived, CLOSED-only EOD rollup: only sharpe/win_rate/avg_pnl/total_trades; drops CLOSED_MANUAL and
lacks signals/gross/ROI/direction/time-bucket/RR). win=`net_pnl>0`, loss=`net_pnl<0` (the system's own
`compute_strategy_metrics` definition). T1–T4 reuse the day's already-built Orders/Signals records
(no re-query); T5 is one trailing query.

**5 spaced BASIS-labelled tables:**
- **T1 PERFORMANCE** (per strategy, this day): signals(reached-storage)·trades·wins·losses·win%·loss%·
  gross·net·ROI%(=Σnet/Σcapital)·capital_used·max_win·max_loss. Signal-only strategies (0 trades) shown.
- **T2 TIME-BUCKET** (30-min, this day): trades bucketed by ENTRY time, signals by VM-receipt time; empty
  buckets omitted. `_bucket_for` (edges 09:15-09:30 & 15:00-15:15 are 15-min).
- **T3 LONG vs SHORT** (per direction, this day). T3 LONG net = ₹3.24 over 18 trades == the Orders TOTALS.
- **T4 RR** (per strategy, this day): planned SL%/TGT% = abs(entry−sys_sl)/entry & abs(sys_tgt−entry)/entry;
  actual = from filled SL/TGT legs; avg RR = `trade_slippage_log.actual_rr`.
- **T5 RANKING** (TRAILING N sessions, default 20, by entry date — NOT that-day-only). `_build_t5_ranking`.

**T5 COMPOSITE (transparent — every component shown on-sheet, not a black box):**
`composite = (0.40·win%_norm + 0.40·netROI%_norm + 0.20·avgRR_norm) × confidence`, where
`confidence = min(trades_n/20, 1)` and each `_norm` = min-max across strategies (**0.5 for all when equal**
— never fabricated spread; `_minmax_norm`). Rank by composite desc. **The design goal (proven):** a
low-sample strategy CANNOT top a high-sample one — a 1-trade/100%-win strategy scores raw ~1.0 but ×0.05
confidence → composite ~0.05 → rank #7–9, while an 8-trade/50% strategy tops #1. The window shrinks to the
actual distinct trade-sessions (11 on the 30-Jun DB), stated on-sheet; confidence still divides by 20, so
nothing hits full confidence on a short window (appropriately cautious).

**BUILD-GATE PASSED (both parts, on the real 30-Jun VM backup `scratchpad/vm_trades.db`):**
(a) **aggregate** — T1 recomputed independently for EVERY strategy (fresh loop) + a raw-SQL cross-check on
the 2 highest-trade strategies (`DATE(created_at)=30-Jun`, COUNT/wins/Σnet/Σmargin) — all match the sheet;
(b) **composite sanity** — the three 1-trade/100% strategies down-weighted to composite ~0.05 (rank #7–9)
while the 8-trade/50% `first_pullback_long` tops (#1); components shown for top+bottom. `generate()` writes
all 5 sheets. Tests: `tests/unit/test_daily_trade_review.py` now **45** (+4 Strategies: T1/T2/T3, T4 RR,
T5 confidence-flip [raw LOW>HIGH but composite HIGH>LOW], pure helpers `_minmax_norm`/`_bucket_for`).

**Docs updated:** `docs/report_data_contract.md` (new "Sheet: Strategies" section + composite explainer +
removed from pending list + footer), `docs/SYSTEM_MAP.md` (header prepend + reports line sheet-5),
`PATHS.md` (generator/Strategies-row/test rows).

**Build-gate = aggregate + composite validation (PASSED) + Rama approval before the Slippage sheet begins.**
Remaining report sheets: **Dashboard**, **Slippage** (per the Phase-0 audit matrix).
