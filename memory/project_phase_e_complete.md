---
name: PHASE E COMPLETE (19-Apr-2026, 7-commit hygiene chain E.1–E.7)
description: Phase E hygiene chain closed; 1649 green; 4 retroactive closures; 4 deferred; schema v10→v11; 2 process locks; next=Phase F or paper trial
type: project
originSessionId: daf7a7d0-49f5-49f6-8f12-9791b8824592
---
**Phase E — pre-paper hygiene sweep.** Seven commits landed 2026-04-19 to
close all HIGH/MED latent gaps surfaced by the three audits + extra-findings
tracker before Monday's paper cut (2026-04-20).

## Commit chain

| Commit  | Subject                                                              | Actual count (pytest --co) |
|---------|----------------------------------------------------------------------|---------------------------:|
| 1a6c49c | E.1 / H-17 — time_authority sweep (datetime.now → now_ist, 5 files) | 1603                       |
| 0752a25 | E.2 | capital — H-1/H-3/H-4/H-5; per-bucket INV6; BEGIN IMMEDIATE  | 1613                       |
| 27e40da | E.3 | orders — H-6/H-21+M-5/H-15/M-2 (reported "-6"; actual +9)   | 1622                       |
| 0d80fe9 | E.4 | orders+signals — H-7/H-13/H-16/M-1/M-3/M-4/EF-5; schema v11| 1638                       |
| 006464c | E.5 | cleanup — H-25 bind_trade; H-10 delete; H-14 helper         | 1642                       |
| 1ad3d5c | E.6 | orders — EF-2 track-failure cleanup symmetric to BL-8       | 1645                       |
| (next)  | E.7 | EF-4 consolidation + H-22 audit-trail + EF-7 auto-resolved | 1649                       |

**E.3 reporting correction:** E.3's commit body stated "1607 green (net −6
obsolete H-6 tests removed)." Neither half was true — no tests were removed;
9 new H-6/H-15/H-21/M-2 tests were added. The absolute was miscomputed by
−15. E.4 and E.5 inherited the wrong baseline via delta arithmetic. E.6
broke the chain by running `pytest --co -q` and reporting the actual
collected number (1645, not the predicted 1630). Correction blocks landed
in project_e3/e4/e5 memory files; no test or code change.

## Architectural locks established (23 items)

### From E.1 (time_authority)
1. **TA1** — All datetime.now() calls inside trading-system modules route
   through `core.time_authority.now_ist()`. Two documented exemptions:
   `core/logger.py` (record creation pre-IST-bootstrap) and
   `scripts/preflight_scanner_check.py` (startup pre-adapter).

### From E.2 (capital)
2. **CAP1 / H-1** — `FundManager.sync_from_broker()` enforces the Σ-invariant
   (reservations + used ≤ total_capital + ε). Violations raise
   `CapitalStateInconsistent` and trigger `hard_kill("capital_invariant_
   broken_after_sync")`.
3. **CAP2 / H-3** — Margin math is leverage-map-aware via
   `MarginPolicy.for_instrument()` (per-symbol leverage from instruments.csv);
   no more global 1/5 shortcut.
4. **CAP3 / H-4** — `FundManager.__init__` guards against double-init with
   an `_initialized` flag; second call raises `RuntimeError`.
5. **CAP4 / H-5** — Every fm_ledger write uses `BEGIN IMMEDIATE` transaction
   mode to avoid SQLite's "upgrade from BEGIN to EXCLUSIVE on WAL" race.
6. **CAP5 / INV6** — Invariant splits into per-bucket checks
   (reservations + used ≤ cap); escalating alert `fund_manager_bucket_
   overflow` routes through critical.

### From E.3 (order-lifecycle hygiene)
7. **OL1 / H-6** — `_bind_trade_internal_id` uses memory-first read
   (`_fill_map[iid].trade_id`) with DB fallback; preserves the O(1)
   mainline path while remaining crash-safe.
8. **OL2 / H-21 + M-5** — `link_signal_to_trade()` hard-fails on duplicate
   signal_id (UNIQUE constraint violation → raise). No silent retry.
9. **OL3 / H-15** — `_check6_orphaned_entry_fills` does a second-source
   check before logging an orphan (belts-and-braces against trade-row
   write delay).
10. **OL4 / M-2** — `_check8_cover_order_sl_drift` reconciles CO SL trigger
    prices against smart_tgt_state; non-matching pairs emit
    `cover_order_sl_drift` warning.

### From E.4 (event-loop safety + schema v11)
11. **EL1 / H-7** — EventBus subscribe/publish happen only on the main
    thread; background threads use `asyncio.run_coroutine_threadsafe`
    into the main loop.
12. **EL2 / H-13** — `SignalQueue` drops (with log tag
    `SIGNAL_QUEUE_DROP`) rather than blocking when full.
13. **EL3 / H-16** — Subscribers that raise are logged with grep tag
    `EVENT_HANDLER_RAISED` and unsubscribed; other subscribers continue.
14. **EL4 / M-1 TOCTOU** — `OrderMonitor.track()` holds the fill_map lock
    across the duplicate-check and insert (no window between read and
    write for a second concurrent publisher to pass the check).
15. **EL5 / M-3 + EF-5** — Schema v10→v11: `trades.reservation_id` column
    added; `_replay_open_trade` reads it directly (single-hop) instead
    of the old two-hop `trade.signal_id → fm_ledger` query.
16. **EL6 / M-4** — Error shape unified: all BrokerError subclasses carry
    `retry_after_sec: float | None` and `escalation: "none" | "warn" |
    "critical" | "hard_kill"`.
17. **EL7 / EF-1** — Retroactively closed by E.2's BL-18 shape-tolerant
    config resolution (no separate E.4 work needed).

### From E.5 (cleanup)
18. **CL1 / H-25** — 5 reconciler sites now call `bind_trade()` helper
    instead of inline trade_id binding (DRY + single audit point).
19. **CL2 / H-10** — `is_active_for_dispatch()` deleted (dead code since
    MAIN14's dispatch refactor).
20. **CL3 / H-14** — `count_signals_today()` helper extracted from 4
    duplicate call-sites in signal_processor.py.

### From E.6 (EF-2)
21. **OP-EF2a** — OrderPlacer.place() wraps the 3-leg (ENTRY/SL/TGT)
    track() + _fill_map write in a single try/except. On exception:
    5-step cleanup (pop _fill_map, untrack, critical log, BL-8
    _handle_placement_failure, re-raise).
22. **OP-EF2b** — NO hard_kill on EF-2 path (protocol-only failure class;
    capital and broker state recoverable via BL-8 path).

### From E.7 (EF-4 consolidation)
23. **EF-4 setter pattern** — `ZerodhaAdapter.set_paper_capital(value)`
    method with value>0 validation and live-mode no-op. main.py constructs
    the adapter with provisional `paper_capital=0.0` and late-binds via
    the setter AFTER account selection completes. `is_paper` re-evaluated
    after `_interactive_confirm_live` because args.mode may have flipped.
    Single source of truth = AccountRow.paper_capital (accounts.csv,
    AR11-validated).

## Retroactive closures (4)

- **EF-1** — closed by E.2's BL-18 shape-tolerant config resolution (not
  by a separate E.4 fix as originally scoped).
- **EF-3** — closed by Phase A commit containing BL-7d+BL-10a (direction-
  aware release_used).
- **H-22** — retroactively closed by Phase A commit 4a08d73 (A.3.g exit
  gate): `test_long_happy_path_full_lifecycle_capital_accounting` +
  SHORT mirror at `test_end_to_end_smoke.py:690,742`. Uses parametrize +
  `bus.publish(OrderFilled(...))` with `paper_auto_fill_delay_sec=60.0`
  instead of sim_kite helper. E.7 records the closure; no new code.
- **EF-7** — auto-resolved by E.7's EF-4 setter consolidation. Before
  E.7, G3 reconciler read `adapter.get_margins()` which in paper mode
  returned the stale 500k getattr default while FundManager operated on
  5M AccountRow value. After E.7, both derive from
  AccountRow.paper_capital; divergence eliminated. No separate commit.

## Deferred items (4)

- **EF-5** — CLOSED in E.4 (schema v11).
- **EF-6** — LOW: orders-row status on FAILED-trade path stays stale
  (cosmetic; capital+broker+trade all correct). Revisit at next orders-
  table schema pass.
- **EF-6a** — LOW: paper-mode synth-fill race vs cancel (paper-only;
  silent drop via unknown-iid branch, no capital impact). Will not
  survive into live mode.
- **DEFERRED-1** — (pending — see extra_findings.md)
- **DEFERRED-2** — (pending — see extra_findings.md)

## Schema evolution

- **v10 (E.4, M-3)** — fm_ledger got `trade_id` column populated at
  OrderPlacer binding time.
- **v11 (E.4, EF-5)** — trades table got `reservation_id` column; backfill
  query SELECTs latest RESERVE per signal_id.

## Process locks (2)

1. **Test-count reporting discipline** — every landing report MUST include
   actual collected count from `venv/Scripts/python -m pytest --co -q
   2>&1 | tail -1`. No delta arithmetic against prior reports. See
   `process_lock_test_count.md` for the rule. Triggered by E.6's +15
   drift investigation, codified permanently.

2. **Spec-vs-architecture pre-work discipline** — every phase's greenlight
   spec runs through a 6-step pre-work before implementation. E.7's pre-
   work is the 5th such instance this project that reshaped a spec before
   coding (EF-4's "add PaperConfig.capital" was caught as would-create-
   3rd-source-of-truth; reframed to setter-based consolidation).

## Next phase

- **Phase F** — open for post-paper-trial follow-ups if Monday surfaces
  gaps. Dir is `docs/web_claude/03_audit_responses/` for new findings.
- **Monday 2026-04-20** — paper trial start. Gates A/B/C/D at
  `docs/web_claude/06_live_operations/monday_paper_playbook.docx`.
  Enable systemd only after gates pass.

## Why (Phase E as a whole)

Close every HIGH and MEDIUM latent gap flagged by the three audits plus
everything surfaced by pre-work before the paper cut. Latent gaps left
unclosed tend to manifest under paper-day traffic volumes that unit
tests don't reproduce. Phase E bought the paper trial a clean
architectural baseline.

## How to apply

- Any new finding post-Phase-E should be filed to `extra_findings.md`
  with severity + discovery context; do not silently bundle into the
  next unrelated commit.
- All 23 architectural locks above are module docstring-documented at
  their enforcing site; new code in those paths must honor the lock
  or explicitly deprecate it (with a migration note).
