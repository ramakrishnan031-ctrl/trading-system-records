---
name: Capital invariant module built and locked (INV1-INV10)
description: capital/invariant.py pure assertion + fund_manager FM11 refactor; 28 tests green; locked decisions INV1-INV10 added
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
Module 23 build complete. All 588 cumulative tests green.

**Why:** G3 Level 1 invariant extracted from fund_manager into a standalone, reusable, testable pure function so any future capital-mutating code can call it without depending on FundManager.

**How to apply:** Use assert_capital_invariant() for any new capital mutation point. Pass cash_floor=settled_capital and realized_pnl_today=today_net_pnl. Fund_manager uses the behavior-preserving degenerate form (pnl=0.0) because it tracks _total as already-settled capital.

## Files changed

- `capital/invariant.py` (NEW): Pure assertion + 3 helpers (compute_lhs, compute_rhs, compute_tradable_balance)
- `capital/fund_manager.py`: FM11 refactor — _check_invariant() now delegates to assert_capital_invariant; cash_floor=self._total, realized_pnl_today=0.0
- `tests/unit/test_invariant.py` (NEW): 28 tests covering INV1-INV10
- `docs/locked_decisions.yaml`: Added INV1-INV10 under capital_module:; total_decisions 50->60

## Test counts (post-Module 23)

| Suite | Count |
|---|---|
| test_invariant.py | 28 |
| test_fund_manager.py | 30 (regression check: unchanged) |
| Total cumulative | 588 across 23 suites |

## Key design decisions

- INV1: Pure stateless function; raises CapitalInvariantViolation, returns None
- INV2: LHS=avail+reserved+used; RHS=cash_floor+min(0,pnl); tolerance=0.01
- INV4: Exactly 12 fields in exception context
- INV6: Negative guards for available/reserved/used/cash_floor; pnl exempt
- INV7: fund_manager passes pnl=0.0 (behavior-preserving degenerate form — _total is already-settled capital, not raw initial+pnl)
- INV8: Layer 3; imports stdlib + core.exceptions only
- INV10: Caller logs; invariant module never logs

## Deviations from spec

None. INV7 degenerate form (pnl=0.0 in fund_manager) is documented in locked_decisions.yaml as the correct behavior-preserving approach — not a deviation.
