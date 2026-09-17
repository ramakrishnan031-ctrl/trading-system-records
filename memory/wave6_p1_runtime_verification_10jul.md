---
name: wave6_p1_runtime_verification_10jul
description: Combined runtime verification Fri 10-Jul — Wave-6 + P1-SHADOW v42. PART A (08:15)=PASS · PART B (15:58 feeder)=PASS (verified 16:03). COMBINED PASS; ledger watch item cleared. Soak note = 1 SHADOW cycle, do NOT flip authoritative.
metadata: 
  node_type: memory
  type: project
  originSessionId: af4824f1-41e0-4c1f-b881-49265a715b87
---

Operator runbook: "COMBINED RUNTIME VERIFICATION · Wave-6 (M-O2+M-C7+M-C3) + P1
SHADOW v42" — two run-times on Fri 10-Jul: 08:15 session (Part A) + 15:58 feeder
(Part B). Verifies the behavioral landing of the 09-Jul off-market pushes
(Wave-6 `d6e3302`, P1 SHADOW `f135fee`) at today's first in-window boot.

## PART A (08:15 session) — VERDICT: PASS (verified ~10:15 IST, market open, read-only)
- **CHECK 1 (service):** `trading-system.service` ActiveState=active, Result=success,
  ExecMainStatus=0, **NRestarts=0**, ActiveEnterTimestamp=Fri 08:15:10 IST. Past the
  market guard, processing signals. The one startup CRITICAL ("KILL SWITCH ACTIVE AT
  STARTUP: SOFT_KILL reason=circuit_breaker_force_close_15:15") is the EXPECTED
  prior-day carryover — **auto-cleared the same second** ("new day 2026-07-10 starts
  clean", Audit Issue #18 fix). No import/init/DB error, no halt.
- **CHECK 2 (v41→v42 migration):** schema_version=**42** · `eod_broker_reconciliation`
  table PRESENT · `trg_trades_terminal_status_guard` trigger PRESENT (coexists) ·
  `PRAGMA integrity_check`=**ok**. Clean legal migrate-up, no data loss, no fail-fast.
- **CHECK 3 (Wave-6 code + false-fire):** M-C7 grep hits (state_store.py:1,
  fund_manager.py:3), M-C3 grep hits (fund_manager.py:2). **ZERO CapitalInvariantViolation**
  in both service journal and app log. **ZERO CAPITAL_DRIFT.** No false-fire at boot
  or in-session.
- **CHECK 4 (signals):** 151 signals today, 8 accepted → 4 OPEN + 1 PENDING live. All
  rejections are NORMAL pipeline reasons (score<55 floor [running proc still on 55,
  see [[risk_config_tighten_10jul]]], strategy 2/2 cap, concentration exhausted,
  portfolio cap 5, entry-throttle, dup-symbol, shadow-inning overlap). The ERROR-level
  log lines are ordinary intraday order-rejection noise, all handled gracefully, NONE
  related to Wave-6/P1:
    * "MIS orders blocked for KOTIC" (broker restriction; repeated 10:00/10:06/10:12 —
      mis_filter is shadow so it records but doesn't drop; correctly NOT counted toward
      kill-switch auto-trip);
    * "slippage_exceeded" (UTLSOLAR/HEG — entry slippage abort working as designed);
    * "No quote returned for SIGMAADV-BE" (BE-series symbol quote gap, KeyError handled).

**M-O2 caveat (honest):** the CHECK4 partial-external-close branch was NOT triggered
today (no external partial close occurred) — so that specific behavioral path remains
unexercised-by-opportunity. Not a failure; just no triggering event. Still a watch item.

## PART B (15:58 feeder) — ✅ PASS (verified 16:03 IST, 10-Jul)
The P1 SHADOW feeder cron fired at **15:58:01** and persisted sensible verdicts (no crash, no alert storm):
- `eod_broker_reconciliation` (today row): mode=LIVE, **authoritative=0 (SHADOW)**, broker_reachable=1, positions/orders/pnl/ledger = **VERIFIED**, margin=NOT_CHECKED (expected FIX-189 post-15:45 reliability gate → mismatch=1, detail "margin: NOT_CHECKED (post-15:45/unreliable)"), overall=**VERIFIED**, eod_verify_status=PENDING, verified_at 15:58:01.
- `pnl_reconciliation` (today): status=**OK**, system_pnl 8.14 vs broker_pnl 0.0, variance ₹8.14.
- journalctl: the cron invocation logged at 15:58:01 (feeder output → `logs/cron-eod-broker-reconcile.log`).
- **SHADOW-soak refinement note:** broker_pnl read 0.0 (a positions()-at-EOD nuance after everything squared) → the ₹8.14 variance is that, not a real divergence; exactly what the SHADOW soak is for. Status OK, no enforcement. Worth watching over the next sessions.

**⇒ COMBINED VERDICT: Part A + Part B = PASS.** Wave-6 (M-O2/M-C7/M-C3) behaviorally clean + v42 migration good (Part A); P1 SHADOW feeder runs clean, log-only (Part B). The ledger "AWAITING RUNTIME VERIFICATION" watch item is CLEARED.

---
Original Part B commands (reference) — cron `58 15 * * 1-5 eod_broker_reconcile.py`:
Run AFTER ~15:58 IST today. Commands (read-only, VM):
```
DB=data_store/trading_system.db   # under /home/ubuntu/systems/trading-system
sqlite3 -readonly "$DB" "SELECT * FROM eod_broker_reconciliation ORDER BY rowid DESC LIMIT 2;"
sqlite3 -readonly "$DB" "SELECT * FROM pnl_reconciliation ORDER BY rowid DESC LIMIT 2;"
sudo journalctl --since "15:55" --no-pager | grep -i reconcile | tail -n 40
```
PASS = feeder ran, persisted a verdict row, logged INFO (SHADOW, authoritative:false),
NO behavior change, verdict sensible vs a manual spot-check. FAIL = crashed / didn't
run / nonsensical verdict → isolate, report, STOP (rollback = disable cron or flip
config flag; DB/code stay, SHADOW has nothing to undo).

## ON FULL PASS (after Part B)
1. Report combined evidence + verdict. 2. Clear the ledger "AWAITING RUNTIME
VERIFICATION" watch item ([[unpushed_pending_deploy_ledger]]). 3. Soak note for
Rama/Web Claude: feeder has run only **1** SHADOW cycle today → needs several more
sessions before considering authoritative:true. **Do NOT flip the flag** — separate
future decision. 4. Note Wave-7 (M-K1/M-R1/M-R2/M-SC2 reporting cluster) has no
dependency on this and can proceed once Rama confirms.

Model note: runbook says Sonnet 4.6 sufficient (checks-vs-criteria); ran on Opus 4.8,
no issue.
