---
name: BL-2 / B.4 CapitalDriftDetected handler landed green
description: Phase B.4 complete; CapitalDriftHandler with source-module filter + tiered escalation; 1535 tests
type: project
originSessionId: 223ab02f-171e-45a3-b037-e6b1df4a6516
---
# BL-2 landed (commit 59fc5fa, 19-Apr-2026)

**Fact:** CapitalDriftDetected now has a real subscriber with tiered kill
escalation. `capital/drift_handler.py::CapitalDriftHandler` replaces the
WARNING-level `_log_capital_drift_event` stub that previously subscribed.

**Why:** Pre-B.4 the event fired into a log-only stub; a genuine broker-
vs-local capital drift would appear as a WARNING line and the system
would keep trading. FM9's sync_from_broker publishes this event whenever
broker balance diverges from local by >Rs1, so a drift indicating an
accounting bug could accumulate silently across reconciliation cycles.

**How to apply:** When adding NEW publishers of CapitalDriftDetected or
modifying EXISTING ones:
- The handler filters by `event.source_module`. The frozenset
  `_ESCALATING_SOURCES = {"fund_manager"}` in capital/drift_handler.py
  controls which sources escalate to kill_switch. If a new publisher
  needs kill escalation, add it there. One-line change.
- CHECK5 POSITION_GREW emits delta as INTEGER SHARE QUANTITY, not
  rupees. CHECK2 ORPHAN_ADOPTION emits delta as notional rupees with
  expected=0. G3 CAPITAL_DRIFT and FM9 emit absolute rupees. Do NOT
  assume uniform semantics -- three different meanings across four
  publishers. Source-module filtering sidesteps the ambiguity.
- Thresholds are ABSOLUTE rupees (250 / 1000 / 2500). YAML comment
  flags that percentage-based thresholds become preferable at
  live-scale capital (>Rs5M); revisit then.
- Consecutive-cycle escalation is fund_manager-SCOPED. A reconciler
  event arriving mid-sequence MUST NOT reset or increment the
  counter (tested explicitly).
- `on_drift` swallows its own exceptions (DH6 / EV4 load-bearing).
  EventBus raises EventDispatchError on propagated errors; crash
  would reach fund_manager.sync_from_broker. DO NOT remove the
  try/except without first confirming EV4 policy changed.

**Pattern precedent:** α-direct Optional[KillSwitch] from BL-9 was
reused here. Symmetry: both FundManager and CapitalDriftHandler
inject KillSwitch as an optional constructor dependency, log
CRITICAL "escalation not possible" if None.

**Pre-work surprises:**
- CapitalDriftDetected has only 3 fields (expected, actual, delta).
  The spec assumed 5+ fields (drift_pct, drift_amount, local_used,
  broker_used); none of those exist. Handler computes severity from
  abs(delta) alone.
- 4 publishers, 3 delta semantics (rupees/qty/notional). Source-module
  filter was the safest design (Option X). Would have hard_killed on a
  3-share reconciler discrepancy without it.
- Legacy _log_capital_drift_event stub at main.py was already
  subscribed. B.4 removes it in the same commit (no double-log window).
- test_main.py had one test exercising the stub
  (test_log_capital_drift_event_no_exception); removed alongside stub.

**Test count:** 1524 -> 1535 (+12 new BL-2 tests, -1 stub test).

**Next:** B.5 (BL-3 CAPITAL_ACCOUNTING_DRIFT reconciler check). Small.
