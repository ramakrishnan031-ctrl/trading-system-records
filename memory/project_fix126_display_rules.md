---
name: project-fix126-display-rules
description: "FIX-126 daily_report 8 display bugs — dash-vs-zero rules, cost visibility, processed count (2026-05-30, commit 3cfa547)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1bd6d797-10ec-4774-b045-1283ba6bd864
---

FIX-126 landed (commits 2f4bf71 + 3cfa547, pushed to VM).

**8 bugs fixed in daily_report.py:**
- BUG 1: Sheet 1 trade_id fallback via trades.signal_id reverse join
- BUG 2: Cost cols (31-36) show "—" for non-CLOSED trades; only show values for CLOSED + charges present
- BUG 3: Exit Price (col 43) shows "—" when exit_price is None/0
- BUG 4: Time in Trade (col 12) shows "—" when no exit_time; 0 only for instant-exit trades
- BUG 5: Candle OHLC (cols 8-11) shows "—" when candle not found (was 0)
- BUG 6: SL Risk / Target Profit in Sheet 3 computed for ALL trades with sys_sl/sys_tgt using abs(); no longer gated by exit_reason
- BUG 7: Telegram Sent At (col 2) falls back to created_at when entry_time is None
- BUG 8: Processed count in Sheet 6 uses signal statuses {PROCESSED, TRADED, FILLED, CLOSED, PLACED, SIZED, APPROVED, RESERVED}; fixes both strategy-wise and time-of-day tables

**Display rules established:**
- "—" = genuinely not applicable (open trade, no data)
- 0 = valid zero value (e.g. CLOSED trade with charges=0)
- Never show 0 as placeholder for missing data

61 tests green (54 existing + 7 new for FIX-126); 2085 unit total passing.

**Why:** Report showed misleading zeros for open/failed trades, making it hard to distinguish "not happened yet" from "happened with zero value."

**How to apply:** When adding new report columns, follow the dash-vs-zero rule: "—" for N/A, 0 for genuine zero.

**Related:** [[project-fix125-report-gaps]], [[project-daily-report-generator]]
