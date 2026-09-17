---
name: BL-3 / B.5 CAPITAL_ACCOUNTING_DRIFT reconciler check landed green
description: Phase B.5 complete; OrderReconciler._check7 verifies fm._reservations vs fm_ledger; source_module="fund_manager_self_check"; 1545 tests
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# BL-3 landed (commit 10ddf50, 19-Apr-2026)

**Fact:** OrderReconciler now has a `_check7_capital_accounting_drift`
method that verifies FundManager's in-memory `_reservations` dict matches
the signed sum of `fm_ledger.margin_delta` rows per reservation_id.
Drifts publish `CapitalDriftDetected(source_module="fund_manager_self_check")`
which flows through the BL-2 CapitalDriftHandler and escalates (LOG_ONLY
-> SOFT_ESCALATED after N cycles, or SOFT / HARD based on absolute delta).

**Why:** Pre-B.5 the system had no mechanism to detect in-process
accounting drift -- if a bug caused `_reservations[rid].margin` to
diverge from the ledger sum (partial mutation, forgotten ledger write,
silent corruption), the invariant check would still pass (buckets sum
correctly) but the per-reservation accounting would silently rot.
G3 CAPITAL_DRIFT detects broker-vs-local drift; BL-3 detects
local-vs-local-ledger drift.

**How to apply:** When adding NEW publishers of CapitalDriftDetected or
writing/modifying fm_ledger rows:

- `_ESCALATING_SOURCES` now contains BOTH `"fund_manager"` (FM9 sync)
  and `"fund_manager_self_check"` (BL-3). They SHARE the consecutive
  log-only counter -- intentional, since concurrent drift on both
  surfaces is strictly worse than drift on one. A regression test in
  `test_drift_handler.py::test_escalating_sources_frozenset_contents`
  guards the set from accidental removal.

- `StateStore.sum_fm_ledger_margin_delta(rid)` has NO entry_type
  filter. DO NOT add one. Load-bearing docstring explains why:
  RESERVE (+m) and RELEASE/RELEASE_USED (-m) net to 0 for closed
  reservations, which is correct -- the iteration is over
  `fm.get_live_reservations()`, which already drops closed rids.
  A filter would break the invariant `sum == current-reserved-margin`.

- `FundManager.get_live_reservations()` returns **full `_Reservation`
  objects** (not just margins). Future checks can verify symbol/qty
  without a signature change. Always called under the FundManager
  lock; returns a shallow copy so caller iteration is safe.

- Signed delta convention: `delta = fm_margin - ledger_sum` (same as
  FM9). CapitalDriftHandler `abs()`es it before tier computation.

- Per-reservation reporting: one event + one ReconciliationAction per
  drifting rid, not aggregated. Symbol lives in the action's
  description + symbol field for ops grep.

- Tolerance reuses `OrderReconcilerConfig.capital_drift_tolerance`
  (Rs1 default) -- no new config field, symmetry with G3.

- Unidirectional design: fm -> ledger only. Orphan detection
  (rids in ledger but not in fm) deferred to Phase E.

- `CapitalDriftHandler.get_consecutive_cycles()` is a public read-only
  accessor added for integration-test counter assertions. Use it
  instead of `_consecutive_log_only_cycles` in new tests.

**Integration smoke test:**
`test_bl3_integration_check7_to_drift_handler_counter_increments`
wires real FundManager + real OrderReconciler + real CapitalDriftHandler
on a live EventBus; corrupts fm_ledger to create a +500 drift; asserts
`handler.get_consecutive_cycles() == 1` after reconcile_once(). If a
future commit silently drops "fund_manager_self_check" from
`_ESCALATING_SOURCES`, the counter stays at 0 and this test fails
loudly -- preventing degradation to INFO-level logs.

**Pre-work surprises:**
- Grep for `_reservations|def get_snapshot|def get_live` initially
  returned no matches -- grep pattern quirk; `_reservations` dict is
  at fund_manager.py:294 and `get_snapshot` at 691. Confirmed before
  implementation.
- No entry_type filter needed (confirmed in pre-work #4); signed
  `margin_delta` already does the right thing. Simpler SQL + load-
  bearing docstring beats a defensive filter that would have been
  silently wrong for CLOSED reservations.

**Test count:** 1535 -> 1545 (+10 BL-3 tests:
4 reconciler + 2 state_store + 1 fund_manager + 2 drift_handler +
1 integration smoke).

**Next:** B.6 (BL-13 shadow_tracker EOD guard). B.6 is the Phase B
closeout commit; mempalace persistence lands in it. Then Phase C
(error paths -- BL-4, BL-8, BL-11).
