---
name: project-daily-report-generator
description: Daily report generator (7-sheet xlsx) — deployed, fixes FIX-117 through FIX-121
metadata: 
  node_type: memory
  type: project
  originSessionId: bbf48a1f-9792-41fa-b1b6-e04f565291c4
---

# Daily Report Generator Built and Hardened (2026-05-18)

## Module

**`reports/daily_report.py`**  
**`reports/style_constants.py`**  
**Tests:** `tests/unit/test_daily_report.py` (59 tests as of FIX-121)

## Fix History

| Fix | What |
|-----|------|
| FIX-117 | Strategy column populated in Sheets 2/3/4/6 via signal fallback (`or "UNKNOWN"` pattern) |
| FIX-118 | Candle OHLC wired into Sheet 4 via `--candle-dir`; Drawdown % in Sheet 6 (`min(max_loss,0)/capital`) |
| FIX-119 | Sheet 1 col N / Sheet 2 col F show per-strategy effective min_score (gap_fade_long=30 not 60) |
| FIX-120 | Sheet 2_Orders realigned to 43-col design template: 3 header rows, correct sep positions, freeze A4 |
| FIX-121 | Cost breakdown (Brokerage/STT/Exch/Stamp/GST) computed from broker_costs.yaml rates for closed trades |

## Sheet 2_Orders Layout (43 cols, 3 header rows)

- Row 1: Title (DEEAF1 light blue)
- Row 2: Group headers (1F4E79 dark navy, white text, merged)
- Row 3: Sub-headers (2E75B6 medium blue, white text)  
- Row 4+: Data rows
- Separator cols: 8, 13, 20, 23, 29, 37, 40 (4472C4 medium blue, width=2)
- freeze_panes: A4

**Column mapping (key):**
- Col 6: Eligible Score (per-strategy min from YAML, falls back to global 60)
- Col 27: Exit Reason (color-coded)
- Col 30: Gross P&L
- Cols 31-35: Brokerage, STT, Exch Charges, Stamp Duty, GST (computed from broker_costs.yaml)
- Col 36: Total Costs (from DB `charges` field)
- Col 38: Net P&L (green/red color-coded)

## Cost Breakdown Logic (`_compute_cost_breakdown`)

- Uses broker_costs.yaml Zerodha MIS rates
- Intraday round-trip: BUY leg + SELL leg
- STT only on SELL side (MIS/CO product)
- Brokerage = min(₹20, 0.03% × turnover) per leg
- SEBI bundled into Exch Charges column
- Returns `{}` for open trades (no exit_price) → shows "—"
- Verified: VALIANTORG ₹52.25 ≈ DB ₹52.26 ✓

## Candle OHLC Automation

**New script:** `scripts/fetch_daily_candles.py`
- Runs on VM at 15:40 IST (after market close)
- Reads PROCESSED symbols from DB for the day
- Fetches 1-min candles from Kite API (09:00-15:31)
- Saves to `data_store/candles/candle_data_YYYY-MM-DD.csv`

**Cron (updated):**
```
40 15 * * 1-5  scripts/fetch_daily_candles.py   # candles at 15:40 IST
5  16 * * 1-5  reports.daily_report --candle-dir data_store/candles  # report at 16:05
```

## CLI Usage

```bash
python -m reports.daily_report                      # today
python -m reports.daily_report --date 2026-05-18   # specific date
python -m reports.daily_report --candle-dir data_store/candles  # with OHLC
python -m reports.daily_report --date 2026-05-17 --force        # force weekend
```

## Score Investigation (2026-05-18)

All traded signals showing score=60 is NOT a bug — DB confirms all PROCESSED
signals on 2026-05-18 genuinely scored 60 (minimum threshold is 60; only ≥60 pass).
FIX-119 per-strategy override works; gap_fade_long=30 shows when that strategy trades.

## Related Memory

- [[project_reports_module]] — existing daily_review.py (different format)
- [[project_vm_architecture_locked]] — VM deployment paths
