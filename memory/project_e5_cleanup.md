---
name: E.5 cleanup landed (19-Apr-2026, commit 006464c)
description: Phase E.5 - H-25 bind_trade at 5 reconciler sites; H-10 delete is_active_for_dispatch; H-14 count_signals_today; 1623->1627 green (+5 new, -1 removed)
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
**Commit:** `006464c` (19-Apr-2026)
**Subject:** `E.5 | cleanup | H-25 bind_trade adoption; H-10 delete is_active_for_dispatch; H-14 count_signals_today helper`

**CORRECTION (applied 2026-04-19 via E.6 drift investigation):**
Reported test count in this commit's landing report was **1627**.
Actual collected count at commit `006464c` is **1642** (verified via `pytest --co -q`).
Cause: E.5 delta of +4 was correct (1638→1642); anchor inherited the −15
offset from E.3 via E.4, so absolute count was reported as 1627 instead of 1642.
**Corrected baseline: 1642 at commit 006464c.**
(Line 18 claim "1623 + 5 − 1 = 1627 within tolerance" is arithmetically self-consistent
but the 1623 baseline was itself wrong — real baseline was 1638, real landing 1642.)

**Items delivered:**

- **H-25**  `orders/order_reconciler.py` — `from core.logger import bind_trade, log_exception`. Applied `log = bind_trade(self._log, trade_id=trade_id)` at the entry of 4 trade-scoped methods (`_check1_manual_close`, `_check4_partial_close`, `_check5_position_grew`, `_g5b_crash_recovery_sl`) and per-iteration inside `_check8_co_sl_drift`'s `for row in tracked_states` loop (trade_id only exists per iteration). All `self._log.*` calls inside those 5 methods replaced with the bound local `log`. `log_exception(self._log, exc)` in `_check1` rebinds to `log_exception(log, exc)` — bound context flows into the exception record. **L3 routing (trade-id → trades.log) now applies automatically** for every record these 5 methods emit. The 6 excluded methods (`_reconcile`, `_g3_capital_drift`, `_check7_capital_accounting_drift`, `_poll_loop`, `_note_auth_error`, `_finalise_auth_counter`) are **untouched** by design — they operate at cycle/global scope where trade_id is not a single value.

- **H-10**  `capital/kill_switch.py:172` — `is_active_for_dispatch()` deleted. Zero production callers (verified via full-repo grep; only ref was test + KS6 docstring + module_18 doc + audit report). KS6 docstring updated (line 24). `module_18_kill_switch.txt` lines 59+171 trimmed (trivial deletions, not deferred). `tests/unit/test_kill_switch.py`: `test_is_active_for_dispatch` (lines 247-259 pre-edit) removed + runner entry + module docstring bullet. **Regression guard:** `test_h10_is_active_for_dispatch_removed_from_class` asserts `not hasattr(KillSwitch, 'is_active_for_dispatch')`.

- **H-14**  `core/state_store.py` — `count_signals_today(self, date_iso: str) -> int` added adjacent to `count_trades_today`. Mirrors the `SUBSTR(col, 1, 10) = ?` pattern on `signals.received_at` (ISO-8601 IST string, same shape as `trades.created_at`). `count_trades_today` docstring clarified (counts trade rows, one per trade; signal-scoped counterpart is count_signals_today). **No new index required** — existing `idx_signals_received_at` is already on `signals.received_at`, and SUBSTR prefix-match still benefits from the index scan for date-ordered rows. **No production call-site changes**; the helper is available for future use (e.g., daily review report, signal-volume dashboards).

**Test count delta:** 1623 → 1627 (+4 net; +5 new in `test_e5_cleanup.py`, −1 from `test_is_active_for_dispatch` removal). **Target was 1628 ±3**; 1627 lands at the expected arithmetic (1623 + 5 − 1 = 1627), within tolerance.
**New test file:** `tests/unit/test_e5_cleanup.py` — 5 tests (H-25 ×2, H-10 ×1, H-14 ×2).
**Phase A gate:** 15/15 green

**Mock-parity scan** (`grep -rn "MockReconciler\|_mock_reconciler\|reconciler ="` over tests/): 3 hits, all benign:
- `tests/integration/test_end_to_end_smoke.py:487, 507` — uses real OrderReconciler; asserts on DB state + actions, not log output; unaffected.
- `tests/unit/test_time_authority_sweep.py:76` — uses `OrderReconciler.__new__` to exercise `_now_ist` in isolation; unaffected.
No MockReconciler class exists.

**Deferred-EF tracker deltas:** none (E.5 is pure audit closure; no EF changes).

**Architectural locks added:**
- Any new trade-scoped reconciler method MUST bind_trade(trade_id=...) at entry and use the bound log for all records inside the method. Global/cycle-scope methods must NOT bind_trade (no single trade_id to attach).
- Last-mile kill-switch gating is owned by `is_active("entry")` / `is_active("exit")` only; no separate dispatch helper.
- `count_trades_today` and `count_signals_today` live next to each other; both use the SUBSTR-on-ISO-date pattern. Future date-scoped counters should follow the same shape.

**Why:** Final cleanup pass before paper-trial entry. H-25 makes trade-scoped reconciler records grep-friendly by trade_id in trades.log without touching call sites. H-10 removes a vestigial helper whose existence signalled a maintenance obligation that didn't exist. H-14 provides a symmetric companion to count_trades_today for future signal-volume observability.

**How to apply:**
- Future order_reconciler additions: if a method accepts `trade` (row) as its first arg, use `bind_trade` at entry; otherwise don't. Per-iteration binding inside a trade-loop is the pattern for cycle-level methods that happen to iterate over trades (like `_check8`).
- Future date-scoped COUNT helpers: `SELECT COUNT(*) AS n FROM <table> WHERE SUBSTR(<iso_col>, 1, 10) = ?` is the canonical shape. Don't introduce a new column or index unless profiling surfaces an issue.
