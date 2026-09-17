---
name: check9_race_aware_fix_01jul
description: "CHECK9 false-positive naked-position fix (01-Jul) — FACET 1 race-aware broker-truth confirm + FACET 2 oversell guard; branch fix-check9-false-positive-01jul, DEPLOYED to main @ f6de000 same day"
metadata:
  node_type: memory
  type: project
  originSessionId: 757f8225-e410-433e-bd65-0068f0855731
---

**01-Jul-2026 — Fixed the FALSE-POSITIVE naked-position SOFT_KILL (CHECK9) that stuck the system today.**
Direct follow-on to [[t2_halt_investigation_reconciler_tag_bug_01jul]] (the tag fix let the emergency exit
actually PLACE → this fix stops it from oversell­ing on a false flag). Also relates to [[fix_157_check9_closed_manual]].

**Root cause (the 1-Jul BANSALWIRE incident):** CHECK9 flags a naked position when a trade's local SL order is
absent from the broker's OPEN-order list. That absence is AMBIGUOUS — the SL may have just **FILLED** (position
closing normally) rather than vanished. CHECK9's existing FIX-155b guard checks the **LOCAL** orders table for a
COMPLETE exit, but local status LAGS the broker fill (order_monitor's 2-second poll). BANSALWIRE's SL filled at the
broker 11:31:26 but the local row was still TRIGGER_PENDING at that instant → CHECK9 mis-read it as naked → spurious
SOFT_KILL (+ the emergency market exit, which was itself broken by the tag bug that day). The SL then self-resolved 2s
later. So: a benign SL-fill race produced a system halt.

**The fix (`orders/order_reconciler.py`, NO schema, both paper + live):**
- **FACET 1 — race-aware confirm.** New `_confirm_genuinely_naked(broker_sl_id, symbol, log)` called in
  `_check9_missing_exits` AFTER the FIX-155b/FIX-157 local guards, BEFORE the naked block. It checks BROKER TRUTH:
  (1) `get_order_history(broker_sl_id)` — if the last status is COMPLETE, the SL FILLED → **not naked**, skip (no
  soft_kill, no emergency exit); (2) `get_positions()` — if the symbol is FLAT (qty 0/absent) → **not naked**, skip.
  Returns naked=True only if the SL is NOT confirmed-filled AND a position is still held. **Fail-safe:** if BOTH
  broker queries throw (broker-blind), it conservatively returns naked=True (a false CRITICAL is safer than a missed
  naked; FACET 2 still prevents any oversell). A `get_order_history`-less adapter (e.g. angelone) degrades to
  position-only confirmation via the try/except.
- **FACET 2 — oversell guard.** In `_emergency_market_close`, right before placing the sell, re-check the LIVE broker
  qty (`get_positions`): SKIP if flat (`skipped(already_flat)`), SKIP if unconfirmable (`skipped(position_unconfirmed)`
  — never sell blind), and `qty = min(tracked, live_held)` so it never sells more than is held. This matters BECAUSE
  the tag fix now lets this exit actually place — an un-guarded sell of the tracked qty into a just-flattened book
  would oversell into an unintended SHORT. Handles shorts too (`abs()` on signed live qty; side already reversed).

**Parity is exercised, not just satisfied:** ZerodhaAdapter implements both methods for paper too — `get_order_history`
reads `_paper_fills` (returns real COMPLETE when a paper SL fills), `get_positions` reads `_paper_positions`. So the
race-detection genuinely runs in paper, not just live.

**Proof (`tests/unit/test_order_reconciler.py`, 4 new + all 8 existing CHECK9 tests green; 86/86 file):**
`test_check9_race_sl_filled_at_broker_not_naked` (the BANSALWIRE race → NOT flagged), `..._genuine_naked_broker_
confirmed_still_fires` (SL CANCELLED + position open → STILL fires; real protection intact),
`..._facet2_oversell_guard_skips_when_broker_flat`, `..._facet2_oversell_guard_clamps_to_held_qty`. **Fail-on-old
verified:** stashing only the reconciler source, the 3 fix-specific tests FAIL (old code sold qty=50 when only 20
held — the exact oversell), the genuine-naked test passes on both.

**★ STATUS: DEPLOYED. Committed on branch `fix-check9-false-positive-01jul` @ `f6de000` (off 9ed8bbb),
4 files / +236 / −0: `orders/order_reconciler.py` (FACET 1+2) + `tests/unit/test_order_reconciler.py` (4 new
proof tests) + `tests/unit/test_fix148_broker_gaps.py` (×3 naked tests now report a live position) +
`tests/unit/test_emergency_exit_tag_fix.py` (`_RecordingAdapter.get_positions` for FACET 2). The 2 pre-existing
test files needed updating because they encoded the OLD `SL-missing==naked` assumption (no live-position check) —
that's the exact bug being fixed.**
Verified pre-push: full suite 4222 passed / 13 skipped / 0 failed (with report-redesign work present); and the PURE deploy
artifact (report work stashed → tree = f6de000 exactly) 118 reconciler/affected tests green standalone. NO schema.
**PUSHED 01-Jul ~17:4x IST** — `git push origin fix-check9-false-positive-01jul:main`, clean ff `9ed8bbb..f6de000`,
post-receive `checkout -f main` + crontab auto-reinstall (matched canonical, no drift). Verified post-push: bare repo
HEAD == deployed tree HEAD == `f6de000` (deploy uses `--work-tree`/`--git-dir` from the bare repo — no nested `.git`
in `~/systems/trading-system`); no tracked-file drift; local PC `main` fast-forwarded to match `origin/main`.
`kill_switch_state` confirmed UNCHANGED (still `SOFT_KILL`, reason "pre-deploy of fix-emergency-exit-tag 9ed8bbb;
hold trading until GO#2 review") — correctly left alone, not started/resumed. `token-watcher.service` started
(active) for tomorrow's 08:15 boot; `trading-system.service` left inactive/halted by design — tomorrow's 08:15 boot
auto-clears the stuck SOFT_KILL. (The report-redesign uncommitted work — W0 config_snapshotter, daily_trade_review.py,
etc. — was NOT on this commit and was correctly NOT swept in by the push; it remains uncommitted locally on the PC,
still mid-flight per [[w0_config_snapshots_01jul]] and related sheet-build memories.)

**SECONDARY policy question (flagged, NOT built):** should a GENUINE single-symbol naked position SOFT_KILL the
ENTIRE system for the day, or just alert + flatten that one symbol and keep trading the rest? Currently one naked
symbol halts everything. Worth a design decision — deferred.
