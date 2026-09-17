---
name: project_trade_review_workflow
description: Daily/weekly trade analysis generation from VM database; Step 1 of 3-step workflow (generate data → fetch candles → Web Claude analyzes)
metadata: 
  node_type: memory
  type: project
  originSessionId: a2263a2c-78e2-431a-939e-8b5b47fa2103
---

# Trade Review Workflow (Repeatable Task)

**Why:** User needs regular post-trade analysis to evaluate system performance, identify pattern failures, and refine strategies. This is Step 1 (data extraction) of a 3-step collaborative workflow.

**How to apply:** When user says trigger phrases like "Generate trade review for [date]", "Trade analysis for May 18", "Review trades for this week", or "Follow TRADE_REVIEW_SOP", execute the sequence below without asking for clarification.

## Key Paths
- VM Database: `/home/ubuntu/systems/trading-system/data_store/trading_system.db`
- PC Output: `C:\Users\rama\Downloads\trade_review\`
- Reference: `TRADE_REVIEW_SOP.txt` (user's workflow document)

## Date Parsing
- Single: "May 18" → `['2026-05-18']`
- Range: "May 8-15" → all weekdays in range
- Week: "this week" → Mon-Fri of current week
- Auto-skip weekends

## Execution Sequence

### 1. Create analysis script on VM
SSH and create `/tmp/generate_trade_analysis.py` with:
- Query `trades` table for closed trades in date range
- 17 columns: trading_date, signal_time, symbol, strategy_name, direction, quantity, system_entry/sl/tgt, actual_entry/exit, exit_reason, net_pnl, trade_id, entry_time, exit_time, status
- Generate Excel with formatting (header blue, exit_reason color-coded: TGT_HIT=green, SL_HIT=orange, EOD=yellow)
- Generate `stocks_YYYY-MM-DD.txt` files (one per date, newline-separated symbols)

### 2. Execute on VM
```bash
ssh trading-vm "cd /tmp && python3 generate_trade_analysis.py"
```

### 3. SCP to PC
```bash
scp trading-vm:/tmp/trade_analysis_*.xlsx C:/Users/rama/Downloads/trade_review/
scp trading-vm:/tmp/stocks_*.txt C:/Users/rama/Downloads/trade_review/
```

### 4. Confirm to user
Format:
```
✅ Trade analysis ready for [dates]:

Files created in C:\Users\rama\Downloads\trade_review\:
- trade_analysis_[range].xlsx ([N] trades)
- stocks_YYYY-MM-DD.txt ([M] files, [X] unique symbols)

Next steps:
1. Run candle_fetcher.py for each date:
   cd C:\Users\rama\Downloads\trade_review
   python candle_fetcher.py YYYY-MM-DD
2. Upload to Web Claude for analysis:
   - trade_analysis_*.xlsx
   - candle_data_*.csv (after fetching)

See TRADE_REVIEW_SOP.txt for full workflow.
```

## Error Handling
- Zero trades → "No closed trades found for [dates]. Check if trades were actually executed."
- SSH/SCP fails → check VM connectivity, provide manual instructions
- Missing pandas/openpyxl → `ssh trading-vm "pip install pandas openpyxl"`

## Model Recommendation
Sonnet 4.5 (straightforward SQL + file operations, no need for Opus)

## Related Memories
- [[project_vm_architecture_locked]] — VM paths and SSH setup
- [[project_reports_module]] — daily_review.py (different: automated EOD report; this is on-demand analysis)
- Reference: `TRADE_REVIEW_SOP.txt` (user's 3-step workflow doc)

## Time Estimate
~2-3 minutes for entire process (SSH + query + SCP + confirm)
