---
name: ct-ct139-result
description: "CT139: Invariant violation + open positions — PASS. HARD_KILL fired, 5 trades preserved, --resume required."
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f6347b4-0a9c-4253-b5d1-150bacb5b32b
---

## CT139 | Invariant Violation + Open Positions | PASS

**Date:** 2026-06-10 11:07 IST

**Setup:** 5 OPEN trades (INOXINDIA, AEGISVOPAK, AEGISLOG, CAPLIPOINT, NLCINDIA), kill switch INACTIVE.

**Method:** Corrupted fm_ledger COMMIT row (ledger_id=6137, INOXINDIA) by adding 999999 to balance_after. Restarted system. Rehydration replayed corrupted chain → excess inflated → invariant check detected lhs=1996589.05 vs rhs=996590.05 (delta=999999).

**Results:**
- [PASS] `CapitalInvariantViolation` raised during rehydrate: `lhs=1996589.0500 rhs=996590.0500 delta=999999.0000`
- [PASS] HARD_KILL fired (not SOFT_KILL): `triggered_by=fund_manager._check_invariant`
- [PASS] All 5 open trades preserved as OPEN in DB (not squaredoff)
- [PASS] `CapitalStateInconsistent` raised → main.py exits with code 1
- [PASS] Subsequent restarts detect HARD_KILL → `HALT -- kill switch active; use --resume to clear`
- [PASS] System cannot auto-clear HARD_KILL: `Manual --resume required`

**Cleanup:** Restored fm_ledger balance_after, cleared kill_switch_state → INACTIVE, restarted. System healthy.

**Note:** Paper mode has no capital_snapshot table, so the existing `test_capital_invariant_violation.py` script (which corrupts capital_snapshot) would SKIP. This test corrupted fm_ledger directly to trigger the invariant violation during rehydration replay — a more realistic corruption scenario.
