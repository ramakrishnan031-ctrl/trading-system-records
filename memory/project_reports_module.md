---
name: reports/daily_review.py built and locked (DR1-DR15, DR-U1-DR-U5)
description: EOD daily review report; 9 sections (xlsx+md); 85 tests total; 8 state_store helpers; DR-U1-U5 multi-inning added in Module 40
type: project
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
Module: reports/daily_review.py (DR1-DR15 original + DR-U1-DR-U5 Module 40 extension)

**DailyReviewGenerator API (DR6):**
- Constructor: `DailyReviewGenerator(state_store, time_authority, logger)`
- Method: `generate(date_iso, output_dir, formats) -> ReportPaths`
- `ReportPaths(xlsx_path, md_path)` dataclass
- Read-only: never mutates state_store (DR7)
- Output: `output_dir/<date_iso>/daily_review.{xlsx,md}`
- openpyxl>=3.1 required

**9 report sections (DR3 + DR-U1):**
1. SUMMARY — totals, P&L, win rate, avg duration + multi-inning sub-block
2. SIGNAL_FUNNEL — 10 stages with count + drop% (P10)
3. SCREENER_ANALYTICS — per-step rejections, per-tier, latency (P18)
4. TRADES — per-trade row
5. ORDERS — per-order row
6. CAPITAL_LEDGER — fm_ledger rows (NOT capital_ledger)
7. SYSTEM_EVENTS — merged system_events + reconciliation_log
8. ALERTS_SENT — placeholder (no Telegram read-back in v2)
9. MULTI_INNING_TRACKING — 36-column per-trade multi-inning sheet (DR-U1)

**MULTI_INNING_TRACKING (DR-U1-U5):**
- 36 columns: 5 id + 9 per inning block * 3 + 4 aggregate
- No is_real column per block (implicit from block position); spec says 9 per block
- Blank strings for missing innings (i2/i3 when trade has fewer innings)
- OPEN inning: exit_reason="OPEN", pnl/duration blank
- Aggregate: total_innings, cumulative_simulated_pnl_pct (i2+i3), best/worst_inning_pnl_pct
- XLSX: freeze_panes="A2", auto-sized columns (min 10, max 25)
- MD: pipe table under "## Multi-Inning Tracking" heading
- Summary sub-block: 6 count lines + cumulative sim P&L + disclaimer note

**State_store additions — 8 helpers:**
DR8 (original 7): get_signals_for_date, get_trades_for_date, get_orders_for_date,
  get_capital_ledger_for_date, get_system_events_for_date,
  get_reconciliation_log_for_date, get_screener_results_for_date
DR-U3 (new): get_inning_summary_by_date(date_iso) — JOIN innings+trades+signals

**Key module-level helpers:**
- `_pivot_innings_to_trade_rows(flat_rows)` — pivots flat list to per-trade dicts
- `_build_multi_inning_summary(trade_rows)` — builds summary sub-block stats
- `_fmt_ts(ts_str)` — normalises timestamps to "YYYY-MM-DD HH:MM:SS"
- `_MULTI_INNING_HEADERS` — 36-element list

**CLI (DR2):**
`python -m reports.daily_review [--date YYYY-MM-DD] [--output-dir DIR] [--format xlsx|md|both] [--db PATH]`

**P&L (DR11):**
Uses trades.net_pnl directly. Win rate = count(net_pnl > 0) / count(CLOSED).

**Tests:** 85 total (50 original + 35 DR-U Module 40). Running total: 1344.

**Why:** Concern 4 reporting visibility closed. Rama's requirement: one row per stock tracked through inning columns.
