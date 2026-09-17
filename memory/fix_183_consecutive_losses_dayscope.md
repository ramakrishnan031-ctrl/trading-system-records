---
name: fix_183_consecutive_losses_dayscope
description: FIX-183 — consecutive-loss streak now resets daily; root cause of 18-Jun live signal halt
metadata: 
  node_type: memory
  type: project
  originSessionId: 926bcdec-f5d1-4d8b-ab01-42b2d61dba29
---

FIX-183 (2026-06-18, commit 85c0374). Live signal-processing halt: from market
open, risk_engine rejected EVERY signal at CONSECUTIVE_LOSSES ("2 straight
losses, max=2") despite 0 trades today. Kill switch was INACTIVE (red herring —
operator had cleared it at 08:10).

**Root cause:** `state_store.recent_trade_pnls()` had NO date filter — it read the
last N closed trades by `exit_time DESC` across ALL days. Yesterday's two EOD
losses (RIIL −20.14, IRFC −0.64 squareoff) carried into today and tripped the
gate. This is a deadlock class bug: an entry-blocking cross-day loss streak can
never reset, because breaking it needs a winning trade, which the block prevents.

**Fix:** `recent_trade_pnls(n, today=<IST date>)` scopes the streak to the current
day via `SUBSTR(exit_time,1,10)=?` (mirrors `count_trades_today`); risk_engine
passes `today = now_ist().date().isoformat()`. Within-day 2-loss breaker
unchanged; each new day starts clean. `today=None` keeps legacy cross-day path
(used by some tests). Only consumer is the CONSECUTIVE_LOSSES check (low blast
radius). Parity: identical path paper+live.

Spec note: docs/v2_design_spec.md:679 was contradictory ("consecutive_losses = 0"
under daily reset, but "(carry from yesterday IF positive count)"). Rama chose
daily-reset — the only non-deadlocking interpretation.

Tests: new `test_fix183_recent_trade_pnls_day_scoped`; 3 existing streak tests in
test_risk_engine re-dated to today (added `_TODAY` via now_ist). 205 unit tests
pass locally. Deployed + service restarted (clean: 0 open positions). Verified on
live DB: today-scoped streak=0, legacy streak=2.

Related: [[deploy_requires_restart]], [[dual_daily_loss_mechanism]],
[[human_order_policy]].
