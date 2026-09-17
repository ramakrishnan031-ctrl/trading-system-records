---
name: mc5-mc6-testmain-16jul
description: "16-Jul-2026 — M-C5 CAS harden + M-C6 zero/negative multiplier skip + the test_main logger-leak fix (branch, UNPUSHED). With these the M-C capital-safety cluster is COMPLETE."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**Branch `mc5-mc6-testmain-16jul` (off `main`@`16437ae`), UNPUSHED. 3 INDEPENDENT commits + docs.**
`f87e587` test_main · `0847134` M-C5 · `6ca1bbe` M-C6. No schema change. Report
`docs/audit/mc5_mc6_testmain_16jul2026.md`.

**🏁 THE M-C CAPITAL-SAFETY CLUSTER IS NOW COMPLETE (all 4 fixed, all 4 UNPUSHED):**
M-C4 `6c77525` ([[mc4-killswitch-lock-16jul]]) · M-C8 `8f9ce0d` ([[mc8-async-hardkill-16jul]]) ·
M-C5 + M-C6 (this branch). **⏰ NEXT = consolidate all three branches → FRESH COMBINED regression →
SANDBOX hard_kill DRILL (M-C8 is the emergency path) → off-market cluster deploy. Do NOT disturb the
deployed `11abebb`.**

**M-C5 (`0847134`) — `commit_adopted_entry` is now safe ON ITS OWN.** The guard (`_commit_exists`) runs
INSIDE `self._lock`, the commit OUTSIDE (it must — `commit_to_used` takes the lock itself + defers BL-4
hard_kill to after release). Two NON-GATING callers both pass the guard → both commit. **The harm is NOT
capital: `_apply_commit:1999` pops the reservation, so the loser's `commit_to_used` raises ValueError →
BL-4 fires a SPURIOUS hard_kill.** Not reachable today (both prod callers gate atomically —
`order_reconciler:3603` `adopt_recovery_trade_to_open`, `:3660` `mark_recovery_trade_exiting`). **Fix =
3 gates:** (1) caller's atomic transition (primary, unchanged) · (2) `fm_ledger` COMMIT row = DURABLE,
covers a later cycle after restart · (3) **NEW in-memory CAS claim `_commit_claims` = CONCURRENT, covers
the window (2) structurally cannot see.** The claim is a test-and-set under the **lock already held**
(guard+claim = one atomic step), released in a `finally`; **NO lock across the commit I/O** (the M-4/M-C4
anti-pattern). Released on success (durable guard takes over) AND on failure (else retries are locked out
forever). NOT part of the 3-balance invariant. **RED-on-old shows BOTH halves:** `assert CommitResult(...)
is None` + `CRITICAL commit_to_used_failed_hard_kill`. Race made deterministic by parking only the FIRST
caller inside `commit_to_used` — blocking both would DEADLOCK the old code instead of failing it. Capital
suites 238 pass.

**M-C6 (`6ca1bbe`) — a zero/negative multiplier SKIPS instead of flooring to 1 lot.**
`max(1, floor(raw_qty * 0))` = 1 lot ⇒ real capital on a signal the model sized to nothing. Now
`effective_mult <= 0` → `SizingResult(success=False, qty=0, constraint="ZERO_MULTIPLIER")` + WARNING;
**FIX-133's floor is PRESERVED for every positive multiplier** (its real job: stop a small-but-positive
mult rounding to 0 and killing a wanted trade). **`<= 0` needs NO tolerance** — `perf_weight` is clamped
`>=0` one line up so the product can't be a tiny FP negative; a negative means a genuinely negative
`tier_mult` (**`PositionSizingTierConfig` types HIGH/MEDIUM/LOW as bare floats with NO `ge=0` bound** ⇒ a
config typo reaches sizing); `-1.0 * 0.0 == -0.0` which `<=0` catches but `<0` would not (pinned by a test).
**BEHAVIOUR-NEUTRAL in prod, verified:** `performance_allocator` clamps `min_weight=0.5` (PA3/PA8) +
`signal_processor:893/1827` defaults unknown strategies to `1.0` ⇒ `effective_mult >= 0.25`. **Hard
PREREQUISITE for ever lowering `min_weight`.** Sizing suites 59 pass.

**⚠️ M-C6 INVERTS A DOCUMENTED FIX-133 DECISION — needs ratification:**
`test_fix133_dynamic_sizing.py::test_perf_weight_zero_floor_at_one` asserted `tiered_qty >= 1` for
perf_weight=0 and the module docstring recorded "perf_weight=0 -> floor at 1" as INTENDED. **That test
ENCODED THE DEFECT.** Renamed → `test_perf_weight_zero_skips_the_trade`, docstring corrected; every sibling
FIX-133 assertion (2x cap, scaling, breakdown) untouched and passing. The approved instruction directs this
split, but it IS a capital-path behaviour change.

**test_main leak (`f87e587`) — FIXED (test-only).** `main._main_locked` declares `global _log`
(`main.py:1538`) and rebinds it (`:1626`); `test_main` patches `main.get_logger`→MagicMock and the patch
restores `get_logger` but **NOT `_log`** ⇒ after test_main runs, `main._log` is a MagicMock for the whole
session and **any later test asserting on main's logging is SILENTLY VACUOUS** (it passes while testing
nothing — that is how M-C8's test_d3 was found). Fix = an **autouse module fixture** saving/restoring
`main._log` (autouse because there are **4** separate `patch.multiple("main", ...)` sites — fixing them
one-by-one would let the next reintroduce it). Guard `test_zz_main_log_is_not_left_as_a_mock` is
**deliberately LAST in the file** (pytest runs in definition order — last is the only position where the
entry-invariant assertion has meaning); RED with the fixture disabled.

See [[mc-cluster-investigation-16jul]] [[mc4-killswitch-lock-16jul]] [[mc8-async-hardkill-16jul]]
[[unpushed-pending-deploy-ledger]] [[verify-check-the-rc-not-the-output]]
</content>

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 452 B (budget 300 B). The index now carries a hook and this link.

- 🏁✅ **[16-Jul M-C5 CAS + M-C6 zero-mult skip + the test_main logger leak](mc5_mc6_testmain_16jul.md)** — M-C5 = a spurious hard_kill from a double commit, fixed with a CAS claim (no lock across the I/O). M-C6 = zero/negative multiplier skips instead of flooring to 1 lot (**inverts a documented FIX-133 decision — ratified**). The test_main leak made any later test asserting on main's logging **silently vacuous**. [[mc5-mc6-testmain-16jul]]
