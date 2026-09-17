---
name: ct-capital-drift-finding
description: "P0 DESIGN_GAP: paper adapter returned static capital; fixed to track realized PnL per fill; 5 new tests"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

## Finding: Paper Capital Drift (08-Jun-2026, ~10:15 IST)

**Classification:** DESIGN_GAP (not FAIL)

**Symptoms:** Three CapitalDriftDetected alerts after SL/TGT hits: Rs 730 (LOG_ONLY), Rs 831 (LOG_ONLY), Rs 1,633 (SOFT tier). The Rs 1,633 exceeded soft_kill_threshold (Rs 1,000) but no SOFT_KILL fired.

**Root Cause 1 — Static paper capital:**
`broker/zerodha_adapter.py:846-848` — `get_margins()` in paper mode returned `self._paper_capital` set once at startup (1,000,000), never updated after trade PnL. FundManager tracked actual PnL via fm_ledger, so after profitable trades FM total = 1,001,633 while adapter still reported 1,000,000. Delta = 1,633.

**Root Cause 2 — Non-escalating source (correct by design):**
`capital/drift_handler.py:65-69` — `_ESCALATING_SOURCES` contains only fund_manager variants. `order_reconciler` is intentionally non-escalating (DH1 design). In live mode, FM9 sync_from_broker is the primary escalating drift path — the G3 reconciler check is a redundant cross-check. This design is correct; the problem was the data source being wrong.

**Fix applied:**
`broker/zerodha_adapter.py:_synthesise_fill()` — When a paper position reduces or closes, calculate realized PnL = (fill_price - avg_entry_price) * closed_qty (sign-correct for both LONG and SHORT). Add realized PnL to `_paper_capital`. Formula: `(fill_price - old_avg) * (closed_qty if old_qty > 0 else -closed_qty)`.

**Tests:** 5 new tests in `test_zerodha_adapter.py`:
- `test_paper_capital_updates_on_profitable_long_exit` (+500)
- `test_paper_capital_updates_on_losing_long_exit` (-500)
- `test_paper_capital_updates_on_short_exit` (+500)
- `test_paper_capital_unchanged_on_entry` (no change)
- `test_paper_capital_cumulative_across_trades` (+200 net)

**Why this matters for live:** In live mode, `get_margins()` calls the real broker API which naturally reflects PnL. Paper mode now matches this behavior — paper/live parity maintained ([[feedback_paper_live_parity]]).

**Deployment:** Files SCP'd to VM at 10:29 IST. 5/5 tests pass on VM. Restart pending — 7 open trades must close first (SL/TGT or EOD 15:15). Service restart will pick up the fix.

**How to apply:** No action needed — fix is permanent. The G3 reconciler check will no longer see drift in paper mode because adapter and FM now agree.

**Status (08-Jun-2026):** DESIGN_GAP fixed. Paper adapter now tracks realized PnL in _synthesise_fill(). 5 new tests pass. Deployed to VM. Restart pending open trade closure.
