---
name: orders_sheet_forensic_master_01jul
description: ORDERS sheet (forensic trade master) — sheet 1 of the NEW DB-pure report generator; STAGED not pushed
metadata: 
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**ORDERS sheet — forensic trade master** (01-Jul-2026). Sheet 1 of a NEW consolidated,
DB-PURE report generator, built on the W0 foundation ([[w0_config_snapshots_01jul]]) and the
Phase-0 audit ([[daily_report_redesign_phase0_audit_30jun]]).

**Module:** `reports/daily_trade_review.py` — `main(--db,--date,--output-dir)` → xlsx
`reports/output/daily_trade_review_report_<date>.xlsx`, sheet `1_Orders`. ONE row per trade
placed; 69 columns in 9 colour-banded groups A–I; 3-row header, freeze `F4` (through Symbol),
Excel OUTLINE groups B–I (collapsible), TOTALS row, SL→red/TGT→green row tint + Net/slip-over/
mismatch conditional fmt. **DB-ONLY** (StateStore date getters + direct `fetch_all`; reuses
`reports/style_constants.py` palette; the 4 cell helpers mirrored locally to stay decoupled from
`daily_report.py`). **PARALLEL** — does NOT edit/retire/re-cron `daily_report.py`/`daily_review.py`.

**3 flags (investigated vs real schema/code, then resolved):**
- **FLAG 1 (exit-trigger timestamp) = DEFINITIVELY ABSENT.** No column records when an SL/TGT
  trigger FIRED distinct from the fill (`orders.filled_at`≈`trades.exit_time`; a resting SL/TGT's
  `placed_at` is at entry). → "Exit Trigger" + "Exit Delay s" render `— pending W5`. **Entry Delay
  IS confirmable** (`trades.order_to_fill_ms` = ENTRY placed→filled).
- **FLAG 2 (closure type) = RESOLVED HONESTLY via a `reconciliation_log` join** (refined same-day
  after a semantics review — a forensic label must be TRUE, not convenient). `classify_closure(trade,
  recon_rows)` keeps the precedence ORDER but NARROWS the RECON_CLOSE trigger. **Key truth (verified
  code + real data):** the daily-EOD squareoff writes NO positive per-trade marker — it lets the
  reconciler record the flat position as `check_name='MANUAL_CLOSE'` + `exit_reason='MANUAL'`, the SAME
  signature as operator-manual, RMS, and kill-flatten. So **`MANUAL_CLOSE` = the reconciler DETECTING an
  external close, NOT a repair → it must NOT be RECON_CLOSE** (over-claim). Only `STUCK_EXITING`
  (reconciler-INITIATED finalize) = **RECON_CLOSE** (rare). `%ORPHAN%`/`SYSTEM_OVERSELL` = ORPHAN_RECOVERY.
  A POSITIVE EOD marker (`exit_reason='EOD_SQUAREOFF'` or legacy `*EOD*`) = EOD_SQUAREOFF (a co-occurring
  `MANUAL_CLOSE` = bookkeeping, ignored). The daily-EOD/operator/RMS collapse → honest **SYSTEM_CLOSE**
  ("external close via manual/system path; trigger not separately recorded"), NO time heuristic.
  `RECON_EOD_CLOSE` only if BOTH a reconciler-initiated marker AND a positive EOD marker. Values:
  SL/TGT/EOD_SQUAREOFF/SYSTEM_CLOSE/RECON_CLOSE/RECON_EOD_CLOSE/ORPHAN_RECOVERY/UNKNOWN/—. Normal SL/TGT
  carry NO recon row → fall through. **Permanent fix = W8** (per-trade `closure_source` written at close
  time; e.g. daily-EOD job sets `exit_reason='EOD_SQUAREOFF'`) to split SYSTEM_CLOSE into EOD vs manual/RMS.
  (`eod_squareoff_log` is per-DAY, no trade key — cannot join. Reconciler check_names writing closes:
  MANUAL_CLOSE @order_reconciler:968/1087, STUCK_EXITING @1194, ORPHAN_* @1386/1892/…, SYSTEM_OVERSELL @1547.)
- **FLAG 3 (freshness) = partial.** S&R 2-state derivable (`sr_detector_results.actual_result` NULL=detect
  /NOT=backfill). MFE/MAE per-trade provenance ABSENT (no source tag on `trade_excursions`;
  `excursion_reconstruction_runs` = aggregate counts only, no trade_id). → honest composite +
  RECON-vs-BACKFILL split logged `— pending W6`.
- Also `— pending W2` (broker-margin, audit W2) and `— pending W7` (no `orders.exchange_order_id` col).

**BUILD-GATE PASSED.** Rendered a REAL date off the 1-Jul VM nightly backup (pulled read-only via
SSH `trading-vm` → scratchpad; the local PC dev DB is empty). 30-Jun = 18 trades, mode LIVE, TOTALS
net ₹3.24. **10-trade forensic validation ALL PASS** (twice — pre + post the FLAG-2 honesty refinement,
independent hand-written oracle) — every field re-derived from source tables: entry/exit px+times,
gross/charges/Σcosts==charges/net, slippage(rs+rr_damage), ROI, broker-oid, closure. **Refinement
before→after:** NRBBEARING (exit 10:33, external) + ARVIND (exit 15:17, the daily-EOD squareoff) both
`RECON_CLOSE → SYSTEM_CLOSE` (honest — ARVIND NOT over-claimed as RECON_CLOSE nor time-guessed as EOD);
ALL SL/TGT unaffected; nothing is RECON_CLOSE on 30-Jun (no STUCK_EXITING). CGCL `TGT_HIT`@−₹6.07
rendered faithfully (forensic master reflects stored DB truth, does not correct it). 22 unit tests
`tests/unit/test_daily_trade_review.py` (incl. MANUAL_CLOSE→SYSTEM_CLOSE, STUCK_EXITING→RECON_CLOSE,
EOD-marker-beats-bookkeeping, RECON_EOD_CLOSE only-if-both).

**SIGNALS sheet (sheet 2, 01-Jul) — HONEST storage-basis denominator.** `2_Signals`, one row per signal
that REACHED STORAGE (21 cols, freeze `A18`). **Stop-gate finding (the crux):** webhook duplicates are
DROPPED at the TTLCache/fingerprint dedup BEFORE any INSERT (`signals/webhook_receiver.py` returns
`status='DUPLICATE'` with no row); score/secondary/capital REJECTS ARE stored (a `QUEUED` row updated to
`REJECTED_*`). So the design identity `Received = Qualified + Rejected + Duplicate` CANNOT hold per-signal.
30-Jun proof: **46,337 received (webhook_audit aggregate SUM(accepted+rejected)) → only 8,477 (18%) reach
storage; 37,860 (82%) dropped pre-storage** (dupes + invalid/out-of-window/backpressure, no per-signal
detail). A per-signal sheet is FORCED onto stored signals (the only per-signal data) → basis = "signals
that reached storage" (the task pre-named it). Totals block = TWO levels: (1) webhook aggregate CONTEXT
(received/accepted/dropped from `webhook_audit`), (2) storage partition `Received(stored)=Qualified+Rejected
+Skipped/Other` **Δ=0** (verified; no fake Δ=0, no fabricated dup rows). `Stage Reached` derived
(RECEIVED→SCORED→SECONDARY_FILTER→CAPITAL_CHECK→ORDERABLE→ORDER_CREATED) from `signals.status`+screener-row
+trade_id. Score←`screener_results.score` (N/A for pre-score rejects e.g. SHADOW_INNING=611 w/ no screener
row); direction/trade_type only for traded signals (`—` else — signals row stores neither). Conditional:
rejected→amber/dup→grey/qualified→green. **BUILD-GATE PASSED:** 30-Jun render 8,477 rows; totals-validation
ALL PASS (46337/8477/Qual 18/Rej 8166/Skip 293, Δ=0) vs independent DB; cross-sheet integrity = the 18
Qualified (ORDER_CREATED) signals == the 18 Orders trades. **W9 = permanent fix** (persist per-signal drops
/ raw receiver log so the all-signals denominator is per-signal complete). 13 Signals tests (35 total).

**RECONCILIATION sheet (sheet 3, 01-Jul) — the integrity backbone.** `3_Reconciliation`, 5 blocks
(`Identity | LHS | RHS | STATUS | Verified-At | Detail`) + an OVERALL VERDICT the Dashboard banner reads.
Blocks: (1) SIGNAL-STORAGE `stored=qual+rej+skip+other` Δ=0 [+funnel context; **unmapped status→FAIL**],
(2) ORDER `qualified=order_placed_ok+placement_failed` (placed_ok=trade has entry order; 30-Jun 18=16+2),
(3) TRADE `placed=filled+cancelled+rej/failed+pending` [unmapped→FAIL; 30-Jun filled 10 + rej/fail 8],
(4) CAPITAL `opening+realized=closing` via a REAL cross-source check **`Σ fm_ledger.RELEASE_USED.pnl_delta`
== `Σ trades.net_pnl`** ≤ ₹1 tolerance, (5) BROKER **PENDING_CAPTURE** (broker P&L/positions/margin not
persisted → W2/W3, never FAIL). OVERALL = FAIL if any FAIL / else "PASS — N pending capture" / else PASS.
**CAPITAL realized gotcha (important):** do NOT use `get_daily_realized_net_pnl` — a `RESET_PNL` housekeeping
fm_ledger row pollutes it (30-Jun returns 0.0 while trades = ₹3.24); `RELEASE_USED.pnl_delta` (=₹3.24 = trades)
is the clean trade-close realized. RMS-close `costs=0.0` can drift the two → FAILs honestly (flagged, not hidden).
Partition blocks (1,3) use EXPLICIT status buckets (no silent catch-all) so a new/unmapped status → Δ≠0 → FAIL.
Also **re-labelled the Signals totals block FUNNEL-FIRST** (Received webhook 46,337 → storage 8,477/18.3% →
Qualified 18 → Traded 18). **BUILD-GATE PASSED (both parts):** (a) 30-Jun render — all 4 computable blocks
match independent DB, OVERALL "PASS — 1 pending capture"; (b) **FAIL-INJECTION** — +₹100 to a closed trade's
net_pnl on a COPY DB flipped CAPITAL PASS→FAIL (ledger 3.24 vs trades 103.24) AND OVERALL→FAIL, then removed
(live untouched) — proves the FAIL path fires. 3 reconciliation unit tests (38 total).

**STATUS: STAGED — NOT pushed.** NO schema / NO cron / NO flags / NO trading-code. Working-tree only
(also brings the W0 changes — all un-pushed). Each sheet's build-gate is Rama-approved before the next.
Docs: SYSTEM_MAP header + reports row, PATHS section, `docs/report_data_contract.md` (Orders + Signals +
Reconciliation rows). Sheets DONE: Orders (1), Signals (2), Reconciliation (3). Next (NOT started): Config
(uses W0 config_snapshots), Strategies, Slippage, Dashboard(last, reads the Reconciliation OVERALL banner).
Follow-ups W2/W5/W6/W7/W8 (Orders) + W9 (Signals). See [[feedback_foundation_rules]] (DB-only),
[[feedback_paper_live_parity]].
