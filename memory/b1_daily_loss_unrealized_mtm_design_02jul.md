---
name: b1_daily_loss_unrealized_mtm_design_02jul
description: B-1 investigate+design (02-Jul) — wire live unrealized MTM into the daily-loss gate via reconciler 15s refresh + get_quote; shadow→enforce; do BEFORE P1. NO code
metadata: 
  node_type: memory
  type: project
  originSessionId: 567e201a-8ff2-4882-b687-0f55318fab0f
---

Audit B-1 (HIGH) — the pre-trade daily-loss gate advertises realized+unrealized but is realized-only. INVESTIGATE+DESIGN done 02-Jul (no code). Full doc: `docs/design/b1_daily_loss_unrealized_mtm_design_02jul2026.md` (SYSTEM_MAP + PATHS point to it).

**Confirmed:** `risk_engine.py:497-512` sums `get_total_unrealized_mtm()` into the 3% gate, but writers `update_unrealized_mtm`/`remove_unrealized_mtm` (`fund_manager.py:1404/1416`) have ZERO production callers (only `test_fund_manager.py`) → `_unrealized_mtm` dict always empty → gate realized-only. Quantified: 3 open positions each −1.2% = −3.6% aggregate open drawdown, none closed → gate sees total_pnl=0 → keeps approving new entries. Bounded by per-position SLs + 15:17 squareoff + realized arm → degraded not absent. Gate is **reject-only** (`ApprovalResult(approved=False)`; no kill/force-close) so wiring only stops NEW entries earlier — bounded, safe.

**Design (permanent):**
- **Source** = `broker_adapter.get_quote([syms]).last_price` — the ONE parity-clean LTP (paper uses `_make_paper_quote_provider` = REAL Kite quotes via token file, `main.py:1669/377-482`). Compute `unrealized=(ltp−avg_fill)×qty_filled×sign`. NOT broker `pnl` (Position model drops it `zerodha_adapter.py:1105-1112`; paper lacks it → not parity-clean).
- **Hook** = the `order_reconciler` **15s** cycle (already fetches get_positions + iterates open trades + holds quote_fn). Add `_refresh_unrealized_mtm()`: batch get_quote, compute per open trade, update_unrealized_mtm, **prune non-open**. No new thread. 15s fresh enough (gate is pre-trade/per-signal, not per-tick).
- **Removal = SET-BASED** (rebuild from the open-trade set each cycle) → closed-by-ANY-path drops out automatically; no per-close-path hooks; no stale-MTM mis-trip. (Optional: also remove on PositionClosed for faster prune.)
- **Interactions:** `_unrealized_mtm` is a SEPARATE dict (`fund_manager.py:368`), NOT in the 3-balance invariant/buckets → zero capital-accounting change; advisory read-only for the gate. Post-close absolute daily-loss control unchanged (realized-only, separate).
- **Failure modes:** stale LTP→last-known + staleness stamp (>2 cycles=STALE); get_quote outage→**degrade to realized-only + ALERT** (never block-all, never fabricate); restart→dict cleared, recovery prepass re-adopts open positions, first refresh (~15s) repopulates (bounded gap); adopted orphan→enters open set→MTM next cycle. Gate reads a freshness flag: STALE/UNAVAILABLE→realized-only+WARN (never silent like today).
- **Rollout = SHADOW first:** flag `daily_loss_include_unrealized=false` → populate MTM + LOG `would_reject_with_unrealized` but enforce realized-only → observe MTM correctness (vs broker pnl) + block frequency a few sessions → flip flag to enforce. Reversible.
- **Tests:** populate on open / set-prune on every close path / gate sums+rejects at 3% realized-only would miss / outage→realized-only+WARN / restart repopulate / paper parity / shadow flag decouples log-vs-enforce / invariant untouched.

**Sequencing: build B-1 STANDALONE BEFORE P1** — smaller, independent (risk-gate vs EOD-reconcile), closes a dead HIGH control, additive to the reconciler P1 later extends. Open HIGH/CRIT = only {A-2 unpushed, C-1 residual+purge, B-1, C-2 network}; A-1 CLOSED. Related: [[audit_remediation_status_02jul]], [[dual_daily_loss_mechanism]], [[get_daily_realized_pnl_double_cost_01jul]], [[p1_eod_broker_sync_assessment_02jul]], [[capital_operational_note]].
