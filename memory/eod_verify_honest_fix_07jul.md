---
name: eod_verify_honest_fix_07jul
description: "Wave-4 eod_verify HONEST-FIX DONE (07-Jul, commit eb75731 unpushed) — real P&L columns + honest PENDING/N/A verdict (no false VERIFIED) + M-SC1 exit code. Facade closed."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-4 eod_verify HONEST-FIX** (commit `eb75731`, main, UNPUSHED — Rama pushes off-market). Closes Audit-B Phase-8 "eod_verify false-verify" HIGH + M-SC1. One fix = one commit (`scripts/eod_verify.py` + new `tests/unit/test_eod_verify_honest.py` + 2 `test_fix137_batch10.py` facade-tests updated). Related: [[p1_eod_broker_reconcile_wave4_investigation_06jul]] (the eventual real feeder).

**Root cause:** the P&L leg queried NON-EXISTENT columns `ABS(system_net_pnl - broker_net_pnl)` (real `pnl_reconciliation` columns = `broker_pnl`/`system_pnl`/`variance`, schema.sql:780) inside a bare `except Exception: pass` → OperationalError swallowed → `pnl_variance=0.0` → spurious "no variance" → **false VERIFIED**. Compounded: `pnl_reconciliation` has **0 rows** (no broker feeder runs — reconcile_pnl un-cronned, P1 not authoritative) → even a working query defaults 0.0 → the daily "verify" NEVER checked P&L (11/11 historical rows VERIFIED / variance 0.0). And `main()` always `return 0` → cron couldn't catch ISSUES (M-SC1). No mode-awareness.

**STEP-1.3 case = NEEDS-BROKER:** P&L source is a broker feeder that doesn't exist until P1 → honest verdict = **"P&L NOT CHECKED" = PENDING**, never a false VERIFIED, until P1.

**Fix (honest, at the source; NO schema change):** new `_evaluate_pnl()` reads the REAL columns (`variance`,`broker_pnl`); an error/missing-row LOGS + returns `NOT_CHECKED` (never silent 0.0). Honest roll-up in `eod_verification.status` (TEXT, no CHECK → new values OK): **ISSUES_FOUND** (open/pending/P&L DIVERGENCE) | **PENDING** (live, clean, P&L NOT_CHECKED) | **VERIFIED** (live matched OR paper N/A). `pnl_variance` (NOT NULL col) stays 0.0 for N/A/NOT_CHECKED — status disambiguates. **Exit code (M-SC1):** ISSUES_FOUND→**2**, VERIFIED/PENDING→0 (PENDING = known gap until a feeder, not a job failure).

**Parity:** mode-aware, ONE code path (`--mode`/`TRADING_MODE`, default live). **PAPER → P&L N/A** (no broker; positions/orders still verified) — never a false FAIL, never broker-authoritative VERIFIED. No paper-specific duplicate.

**Scope held:** did NOT wire eod_verify↔P1 (later consolidation after P1 soaks); did NOT touch P1/reconcile_positions/reconcile_pnl.

**Tests** (`test_eod_verify_honest.py`, REAL StateStore/schema — no mocks in assertion path): T1 live/no-feeder→PENDING (no false VERIFIED) · T2 real columns detect a **Rs250 divergence**→ISSUES_FOUND (old swallowed→VERIFIED) · T3 paper→N/A · T4 ISSUES→exit 2 (M-SC1) + PENDING→exit 0 · T5 genuine VERIFIED preserved. RED proven against HEAD (clean→VERIFIED, Rs250 divergence→VERIFIED/var=0.0, ISSUES→exit 0). Updated 2 `test_fix137_batch10` facade tests (clean day→now PENDING). **176 green** (eod_verify + fix137 + eod_squareoff + cron_registry + cron_alerts + daily_trade_review; 0 regressions).

**Residual:** the false-VERIFIED facade is CLOSED — eod_verify now honestly reports **P&L NOT CHECKED (PENDING)** every live day until a broker feeder exists. That feeder = P1 `eod_broker_reconcile` (rebase track, undeployed, [[p1_eod_broker_reconcile_wave4_investigation_06jul]]); when P1 is authoritative, the P&L leg gets real data and PENDING flips to VERIFIED/ISSUES (the later eod_verify↔P1 wiring). Telegram stays `send_info` (level not changed — out of scope; the exit code is the monitoring fix). **Wave-4 status: eod_verify honest-fix ✓; P1 on rebase track (undeployed); reconcile_positions/reconcile_pnl = separate items.**
