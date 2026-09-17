---
name: monday_validation_06jul
description: "Mon 06-Jul trading-day validation (read-only): clean-base gate PASS (no naked/oversell/CHECK9/HARD_KILL; orphan-recovery + config-55 worked; EOD clean, 0 open) with 2 non-blocking notes (capital-drift ×2 transient; B-1 shadow unconfirmable from journal). + off-market pending inventory."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Mon 06-Jul session validation (read-only, ~23:00 IST).** Two sessions ran: 08:15→11:20 (natural boot) + 11:20→16:00 (config-55 WARM restart); clean EOD exit 16:00. Deployed HEAD `9709a46` (Wave-3+sync; eod_verify `eb75731` + P1 `wave4-p1` are LOCAL/unpushed), schema **v41** (P1 not deployed ✓), GUI `gui-dashboard` **active**.

**CLEAN-BASE GATE = PASS** (safety-critical): 08:15 boot clean, prior-day SOFT_KILL auto-cleared (new-day headless), preflight OK, **0 naked / 0 oversell / 0 CHECK9 / 0 HARD_KILL / 0 EMERGENCY**, A-1/E-1 **inflight-orphan recovery worked** (WHIRLPOOL/IFGLEXPOR CHECK2 orphan→adopted, no double-entry), A-2/order-monitor handled fill-timeouts + a transient kt-oms network error cleanly, protective rejects fired (slippage-abort ×2, MIS-block LIBERTSHOE, circuit-proximity), **EOD clean** (15:15 circuit-breaker SOFT_KILL→square-off→CHECK1 manual-close ×5→16:00 exit), **0 OPEN now**. **config-55 WORKED** (trades flowed: 3 CLOSED + 5 CLOSED_MANUAL; 16 FAILED = benign slippage/MIS/zero-fill; 2 REJECTED). 155 Tracebacks = benign quote_fn KeyErrors (GAUDIUMIVF/LAXMIINDIA illiquid, SKIPPED_QUOTE_UNAVAILABLE). 9 CRITICAL = all benign (startup kill-clear + EOD circuit-breaker + CHECK1 manual-close).

**2 NON-BLOCKING NOTES (investigate, not safety regressions):**
1. **G3 CAPITAL_DRIFT ×2** (10:28, 10:58; `expected=0 actual=10000 delta=10000 tol=50`) — **no position open at the time** → almost certainly a transient broker-margin-read glitch (returned 0/stale vs the ₹10k local total); self-resolved (no recurrence post-11:00), **did NOT halt**. Look into margin-reliability / capital-reconcile (M-C1 adjacent).
2. **B-1 shadow not confirmable from the journal** — config CORRECT (`daily_loss_include_unrealized: false` = SHADOW, non-enforcing); but 0 `mtm_refresh`/`would_reject` lines (logs at DEBUG and/or no daily-loss threshold approached today). Can't positively confirm the 15s MTM loop ran → verify via DEBUG log or the DB.
3. NOTE: today's `eod_verification=VERIFIED / pnl_variance=0.0` is the **pre-honest-fix FACADE** (deployed 9709a46 lacks `eb75731`); positions/orders clearing is genuine, but P&L wasn't actually checked. Honest-fix flips it to PENDING once pushed.

**BASE CLARIFICATION:** today validated the **Fri-batch + config-55** base — NOT Wave-3. Wave-3 (+config-55 commit) deployed tonight `9709a46`, **import-verified only**; its runtime validation is **tomorrow's 08:15**. So the confirmed-clean base for next-week = (Fri-batch+config-55, today-validated) + (Wave-3 on-disk, runtime-pending 08:15); eod_verify honest-fix + P1 sit local/unpushed on top.

## Off-market pending inventory (sequenced)
- **P1 SHADOW deploy** — integrated+validated (`wave4-p1` `c54f688`, v42, [[p1_wave4_integration_validated_07jul]]). **BLOCKED until after the 08:15 Wave-3 confirm** (then push+deploy SHADOW, authoritative:false). HIGH value (closes 2 audit HIGHs).
- **Low-sev batch (buildable NOW on the clean base; one off-market deploy)** [[audit_lowsev_verify_03jul]]: **C-4** token-file chmod 0600 (world-readable 0664) · **C-3** healthcheck :8080→127.0.0.1 + scrub /health,/metrics leaks · **F-1** `min_free_disk_gb` reads wrong config path (always 1.0) · **E-4** /health missing order_monitor/reconciler/eod/live_feed liveness (Commit A = pure infra) · **A-3** last-mile kill re-check before execute (Commit B, trading-path, LOW/bounded). E-2 ACCEPT (locked 20-Jun) · B-2 docs-note only.
- **W10** [[get_daily_realized_pnl_double_cost_01jul]] — `get_daily_realized_net_pnl` double-subtracts costs (`Σgross − 2·Σcosts`); LOW, **SAFE direction** (early halt, never missed); fix decision pending Rama; bundle w/ B-2. Buildable now.
- **D-1** [[d1_close_trade_race_design_03jul]] — close_trade atomic-close race; design done, MED; buildable now.
- **B-1b** — B-1 follow-up (shadow→enforce validation / SHORT-sign MTM). Verify B-1 shadow metrics first (note #2), then sequence. (Uncertain exact scope — confirm from [[b1_unrealized_mtm_design_03jul]].)
- **daily_report retirement** — verify today's new Phase-C report generated at EOD before retiring old `daily_report.py`. Needs a reports-dir check (not done here).
- **T2 (delivery Slice-2.5)** — Mon window PASSED → **Tue mid-session**, NOT tonight. Note only.

Also standing: [[wave3_config55_runtime_closure_07jul]] (08:15 Wave-3 confirm + anchor removal — DONE 07-Jul) · unpushed `eb75731`+`wave4-p1` (Rama pushes off-market).
