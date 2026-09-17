---
name: project-fix154-complete
description: "FIX-154 committed: kill_switch auto_clear_scheduled_kill + FM NaN/Inf guard; 185 tests pass (07-Jun-2026)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6baefba5-fbd6-4be5-a6cf-cb04d7f1755c
---

FIX-154 committed (07-Jun-2026, commit b9b8ca0). Two changes:

1. **kill_switch.auto_clear_scheduled_kill()** — auto-clears SOFT_KILL on startup when reason is scheduled (force_close_15:15, EOD_SQUAREOFF) and no open positions exist. HARD_KILL and emergency reasons still require manual --resume.
2. **fund_manager.reserve_capital() NaN/Inf guard** — rejects NaN, Inf, and non-numeric qty/price before they corrupt capital state.

**Why:** FIX-127's stale kill switch fix only cleared previous-day kills. Same-day restarts (e.g., after 15:15 circuit breaker) stayed blocked. FM NaN guard prevents IntegrityError on fm_ledger writes from garbage upstream data.

**How to apply:** Both are defensive — no config or operational changes needed. auto_clear_scheduled_kill() runs automatically on every startup after clear_stale_state(). 185 tests pass across kill_switch (37), fund_manager (82), main (66).
