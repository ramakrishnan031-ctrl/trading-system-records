---
name: ct-ct032-deferred
description: "CT032 blocked by daily_trade_limit; retest Day 2 with max_daily_trades=200, open position, inject same-symbol, revert"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT032 blocked by daily_trade_limit (20/20) from real Chartink signals on Day 1. The position-exposure check was never reached.

**Proper retest Day 2:** Set max_daily_trades=200 in system_config.yaml BEFORE market open, open a position deliberately, inject same-symbol signal to different strategy, verify exposure check fires, then revert config to max_daily_trades=20. Do NOT change config mid-session. Paper + Live parity required.

**Why:** Daily trade limit is an earlier gate in the pipeline than per-symbol exposure. To test the exposure check, the daily limit must not fire first. 200 is safe for Day 2 paper testing.

**How to apply:** Day 2 morning — before starting trading-system, edit config, then revert after CT032 passes.
