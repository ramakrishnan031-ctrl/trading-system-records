---
name: fix150-complete
description: FIX-150 system metrics + Gemini premarket brief + data integrity check (schema v24, 3 scripts, 76 tests)
metadata: 
  node_type: memory
  type: project
  originSessionId: auto
---

FIX-150 landed (2026-06-03, commit 65ef57d, pushed+deployed).

**Schema v24:** 2 new tables
- `system_metrics`: timestamp, cpu_pct, memory_mb, db_size_mb, log_size_mb, open_fds, thread_count, disk_used_pct
- `system_metrics_daily`: daily summary with snapshot_count, avg/max/p95 for CPU/mem/disk

**3 new scripts:**
1. **capture_metrics_baseline.py**
   - Captures health snapshot every 5 min during market hours (9:00-15:59)
   - `--summarize` at 16:16: computes daily avg/max/p95, writes to system_metrics_daily
   - Drift detection: alerts via Telegram if any metric > 80% of historical max
   - Cron: `*/5 9-15 * * 1-5` (snapshot) + `16 16 * * 1-5` (summary)

2. **gemini_premarket_brief.py**
   - Pre-market operational briefing at 08:55 IST (10 min before market open)
   - Loads yesterday's EOD review + open positions + strategy metrics + kill switch state
   - Pipes to Gemini CLI for 100-word briefing
   - Saves to reports/briefing/ + sends to Telegram
   - Cron: `55 8 * * 1-5`

3. **gemini_data_integrity_check.py**
   - Daily candle data integrity check at 17:00 IST (after all data settled)
   - Samples 5 traded symbols (random), fetches Zerodha historical 1-min candles
   - Compares system DB candles vs Zerodha (OHLC 0.05% threshold, volume 5% threshold)
   - Gemini CLI reviews findings: CLEAN (exit 0) or DIVERGENCE_DETECTED (exit 2 + Telegram)
   - Saves to reports/integrity/
   - Cron: `0 17 * * 1-5`

**Cron additions** (4 entries in trading-system.cron):
- 08:55: premarket brief
- */5 9-15: metrics snapshot
- 16:16: metrics daily summary
- 17:00: data integrity check

**Tests:** +76 (24 metrics + 26 premarket + 26 integrity); 2801 passed, 12 skipped

**Also includes:** `docs/first_day_live_runbook.md`
- Pre-day checklist (7 TEMP config reverts, healthcheck, disk space)
- Day 1 morning timeline (08:00 token → 09:14 mental checklist)
- During-market monitoring (first 30 min full attention, then 15-min checks)
- 7 abort conditions (slippage, naked position, capital mismatch, token expiry, API failures, kill switch, wrong fills)
- EOD reconciliation (P&L must match within Rs 5)
- 7 success criteria for continuing Day 2

**Why:** Operational readiness for micro-live: health monitoring, premarket context, candle quality assurance.

**How to apply:** Cron jobs run automatically; Telegram alerts on drift/divergence; first-day checklist is authoritative for Day 1 live.
