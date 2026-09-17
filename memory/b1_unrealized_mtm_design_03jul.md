---
name: b1_unrealized_mtm_design_03jul
description: "B-1 re-investigation 03-Jul — task file SUPERSEDED by built f5fd4d9 (in tonight's batch); fresh evidence + the ONE open gap (4b periodic unrealized soft-kill) designed as B-2 + W10 bundling verdict"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54ecd864-01af-4fbe-b453-740efca8a1e9
---

**03-Jul task file "B-1 INVESTIGATE+DESIGN" arrived describing the 02-Jul AUDIT state — it is
SUPERSEDED for items 1–3 + 4(a):** design done 02-Jul ([[b1_daily_loss_unrealized_mtm_design_02jul]],
doc rides C-1 @3d34357), **implementation BUILT** ([[b1_daily_loss_unrealized_mtm_impl_02jul]],
`f5fd4d9`, +513/−15, 20 tests) and **LOCKED into tonight's ordering-(a) push batch**
([[offmarket_deploy_runbook_final_03jul]]) — shadow default, enforce ≥13-Jul. Did NOT re-design
4(a); did NOT touch the batch. Fresh read-only evidence re-verified on main==9becf8c:

- **Dead term (confirmed):** reader RE7 `capital/risk_engine.py:497-512` (`snap.daily_realized_pnl
  + fm.get_total_unrealized_mtm()`); writers `fund_manager.update_unrealized_mtm:1404` /
  `remove:1416` — prod callers ZERO (tests only) → `_unrealized_mtm` dict permanently empty → both
  controls realized-only. Post-A1E1 line shifts: audit's "fund_manager:1071" is now **FM7 at
  fund_manager.py:1201-1221** (post-close, pct×total, W10-affected SQL read L1210) → breach cb
  `main.py:666-709`: CRITICAL alert → EodSquareoff.fire_now (cancel pending → market-close ALL) →
  SOFT_KILL. RE7 callers = pre-trade signal path ONLY; **NO periodic evaluator anywhere** (orders/
  grep = 0).
- **Price source:** NO tick stream/LiveFeedManager persisted (G0); source = broker-adapter
  `get_quote` REST, batched in the reconciler 15s cycle (B-1 built). **PARITY DISCREPANCY vs task
  file:** task says "paper uses SIMULATED prices for MTM" — built B-1 uses REAL Kite LTP in BOTH
  modes (paper simulates FILLS, quotes are real) = ONE code path. Flagged to Rama, stands unless he
  overrides.
- **W10 root PROVEN:** close path `fund_manager.py:1159` `pnl = gross − costs` → ledger row
  L1182-83 writes `pnl_delta=NET` + `costs` separately; reader `state_store.py:2346-2365`
  `SUM(pnl_delta) − SUM(costs)` = **gross − 2·costs**. Feeds BOTH controls (RE7 via
  get_snapshot:1390; FM7 :1210) + reset_daily_pnl:1447. Trip-EARLY direction (safe), tiny at
  volume. Already worked around in daily_trade_review:1062 + ops_dashboard (D2).

**OPEN GAP (the task's genuinely new item) = 4(b) periodic unrealized-drawdown kill — even with
B-1 enforce ON, unrealized breach only REJECTS new entries; no active kill until closes realize
loss (SLs cap per-position, not portfolio window). DESIGN (B-2, no code yet):** piggyback the SAME
15s `_refresh_unrealized_mtm` cycle (zero extra quote cost) → after refresh, if FRESH and
`realized + unrealized ≤ −(daily_loss_limit_pct × total)` for **2 consecutive cycles** (~30-45s
confirm, no single-spike false-trip) → fire the EXISTING FM7 breach sequence (one shared
`fund_manager.evaluate_combined_daily_loss()` → `_on_loss_breach`; derive-don't-duplicate, no new
kill path) with one-shot daily latch; SKIP when stale (never kill on stale quotes), no-op under
HARD_KILL/SOFT_KILL-already. Rollout: shadow flag `periodic_kill_enabled=false` + shadow log
`would_soft_kill_on_unrealized` → flip after B-1 shadow week proves MTM accuracy (≥13-Jul).

**W10 BUNDLING VERDICT: NOT tonight** (batch frozen/verified; W10 is trip-early-safe) — **bundle
W10 INTO B-2** with 4(b): same files/controls, one coherent loss-control change; canonical
semantics per FIX-056 docstring = pnl_delta stores GROSS (fix writers), reader unchanged; must
also cover reset_daily_pnl round-trip (writes back the W10-affected value). Test matrix (10 rows)
in the 03-Jul session report: open-drawdown trips [was: didn't] · combined arithmetic ·
2-consecutive confirm · stale-skip · parity one-path · HARD_KILL no-op · shadow-only · W10
gross−costs exact trip-point · RESET round-trip · FM7 FIX-128 sequence regression.

**SYSTEM_MAP pointer DEFERRED** (tree = gui-deploy-03jul frozen for tonight's push; a docs edit
now would entangle the GUI merge) — land with the B-2 branch or the post-deploy docs pass.
B-2 build waits until AFTER the batch + GUI deploy + B-1 shadow evidence.
