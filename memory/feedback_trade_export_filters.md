---
name: trade-export-filters
description: Daily report candles sheet must exclude CANCELLED trades; strategy field validated
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9aefa85b-0188-4017-b867-0390152cb3f2
---

## Trade export filtering rules (2026-05-18)

**Fix applied**: Sheet 4 (Candles) in daily_report.py now filters to only CLOSED trades.

```python
closed_trades = [t for t in data.trades if t.get("status") == "CLOSED"]
```

**Why**: CANCELLED trades have None/0 for execution prices (entry_actual_price, exit_price), creating NaN values in analysis that confuse P&L review. These trades never executed, so they don't belong in candle analysis.

**Strategy column**: Schema has `strategy TEXT NOT NULL` (schema.sql:86). Code correctly reads `trade.get("strategy", "")`. If showing NaN:
- Check if older trades in DB have empty string "" instead of strategy name
- Excel may render "" as blank, but NOT as NaN
- If truly NaN: investigate data quality at trade creation time

**How to apply**: 
- ALL candle/price-based analysis sheets should filter `status = 'CLOSED'`
- Summary/P&L sheets already do this correctly (dashboard, strategy analysis)
- Capital sheet shows ALL trades (including CANCELLED) for fund tracking—that's intentional
