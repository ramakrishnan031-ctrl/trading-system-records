---
name: mc8-async-hardkill-16jul
description: "16-Jul-2026 M-C8 FIXED (branch, UNPUSHED) — the hard_kill flatten runs on a non-daemon worker instead of the caller's fill thread; the EXITING-blind eod-self-exit race is closed; conditional DB writes."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**M-C8 IMPLEMENTED + TESTED — branch `mc8-async-hardkill-16jul` (off `main`@`16437ae`), UNPUSHED.**
**8 commits, tip `8f9ce0d`:** `5744776` worker (kill_switch.py) · `2d6d005` lifecycle (main.py) · `ed91aa7`
tests · `46ec78a` full-suite repairs · `ae5bf74` thread-start guard · `52cbe92` drain honesty · `61f5977`
docstring correction · `8f9ce0d` docs. No schema change. Report
`docs/audit/mc8_async_hardkill_16jul2026.md` (**read §2.1 + §6 + §6.3 before approving**).
**Deploys OFF-MARKET with the M-C cluster.**

**⏰ 3 DEVIATIONS FROM THE APPROVED INSTRUCTION AWAITING RAMA/ChatGPT RATIFICATION (report §6.3):**
(1) **"all existing tests pass unchanged" is FALSE** — 3 tests needed a 1-line entry-point change (the big
one; see below); (2) single-flight uses a **dedicated lock, not the KS4 RLock** as the instruction said
(reusing it would put a 2h join behind the lock M-C4 just fixed; the instruction's real requirement — kill
STATE tripped before the worker spawns — is preserved); (3) an **inline fallback if the worker thread can't
start** (not in the design; found in self-review — an unflattened book beats a blocked caller).

**The fix:** `hard_kill`'s 2h exit-retry loop ran INLINE on the caller's thread, and all 6 prod callers are
on the fill/commit path ⇒ an emergency could starve the fill pipeline for 2h. Now the **adapter** path
(production — `main.py:1983` always `set_adapter`) dispatches to a **non-daemon worker** and returns
immediately. **The kill STATE is still tripped synchronously** (`is_active` blocks orders instantly — that
did NOT go async).

**🔑 THE LOAD-BEARING SPLIT (do not let anyone "tidy" this):** the **legacy `cancel_fn` path stays
SYNCHRONOUS** and `_exit_all_trades_indestructible` stays a sync internal method — that is what keeps the 86
pre-existing kill-switch tests passing unchanged. `CancellationReport` gained `dispatched=True` so the async
return declares itself instead of masquerading as "attempted=0, nothing to do".

**⚠️ THE DESIGN'S TEST PREMISE WAS FACTUALLY WRONG — and only the FULL suite caught it.** The approved steer
claimed "the only tests that read the report use the LEGACY path ⇒ all existing tests pass unchanged". FALSE:
**`tests/unit/test_p0_live_day1_fixes.py::TestBugC_KillSwitchExit` (3 tests, `:228-270`) calls `hard_kill()`
WITH AN ADAPTER and asserts on the result** — the original seam analysis grepped a SUBSET of the test tree.
**The DESIGN still holds** (it rests on the 6 *production* callers ignoring the report — verified); those 3
tests were about the flatten's Bug-C *logic*, not hard_kill's synchrony, so they now call
`_exit_all_trades_indestructible()` directly like their siblings (`test_h4:109`/`h5:67`/`chain:132`), every
assertion verbatim. **Honest claim = "86 unchanged + 3 needed a 1-line entry-point change", NOT "no test
rewritten".** My 10-suite dev baseline was green the whole time and did NOT contain that suite.

**Design:** state machine `IDLE→RUNNING→DRAINING→COMPLETE` under a **DEDICATED lock, never the KS4 RLock**
(reusing it = M-C4 in a worse place: a 2h join under the lock that gates `is_active`). `COMPLETE` set in a
`finally` — a worker dying at RUNNING would make `is_flatten_in_progress()` answer True forever and hang the
eod gate all night. **Single-flight on the adapter path only** ⇒ **KS6's "re-runs cancellation" is now
PATH-SPECIFIC** (preserved for legacy, single-flight for adapter); it gates only in-flight, so a hard_kill
after COMPLETE still dispatches.

**🔴 THE EXITING-BLIND RACE IS CLOSED** (it was latent TODAY, not introduced by async):
`main._eod_self_exit_due` now gates on `KillSwitch.is_flatten_in_progress` — **never**
`count_active_positions()`, which counts only OPEN/PARTIAL/PENDING_FILL and cannot see a flatten in flight
(the flatten marks EXITING *early*). Fail-safe: gate raises → stay up. `_shutdown` drains the worker
**BEFORE any teardown** (it writes through `store`; `store.close()` is at the bottom). **Shutdown split:**
internal eod-exit waits (bounded by the flatten's own 2h deadline); **external SIGTERM = bounded 15s grace**
because `trading-system.service` has `TimeoutStopSec=30` and systemd SIGKILLs regardless → CRITICAL
"positions may remain open". See [[mc8-investigation-16jul]] for the design inputs.

**📌 TWO SCHEMA FACTS discovered while proving the tests RED-on-old (they corrected the design's premise):**
1. **`schema.sql:278 trg_trades_terminal_status_guard` ALREADY ABORTs** transitions out of
   CLOSED/CLOSED_MANUAL/FAILED/CANCELLED/REJECTED* ⇒ the terminal `trades` case was **never exposed**. The
   conditional write's real gain there is **`UNKNOWN_IN_FLIGHT`** (the A-2 "don't know if it filled" state —
   NOT terminal, NOT guarded), plus turning a trigger-ABORT-caught-and-logged-CRITICAL into a quiet no-op so
   routine concurrency stops imitating a real DB fault.
2. **There is NO trigger on `orders` at all** ⇒ the `CANCELLED`-over-`COMPLETE` clobber (a **FILLED SL
   recorded as cancelled**, leaving the reconciler believing a closed position is still open) was **entirely
   unguarded**. The conditional is the only thing preventing it.

**Tests:** 25 new (`tests/unit/test_mc8_async_hardkill.py`), **8 PROVEN RED-on-old by surgically reverting
each behaviour and re-running** — incl. "hard_kill blocked the caller for 10.03s" and "the process would
have exited mid-flatten". 86 pre-existing kill-switch tests **unchanged**; `test_p0` back to its exact 25;
**136 combined**. FIX-180/181/190/H-4/H-5 preserved by construction.

**⚠️ TWO OF MY OWN TESTS INITIALLY PROVED NOTHING** — caught only by running them against reverted code:
`test_a2` measured `is_active()` *after* `hard_kill` returned (on old code it returns having already finished
the flatten); the first `test_c` asserted the CLOSED case the trigger already protected. See
[[verify-check-the-rc-not-the-output]] — a test that has not been seen to fail is not evidence.

**✅ DEFINITIVE FULL SUITE (on the final tree `61f5977`, no uncommitted .py): `12 failed, 4748 passed, 15
skipped` in 17m34s — ZERO attributable to M-C8.** 11 = the known time-gated PC-env set; the 12th
(`test_end_to_end_smoke::TestScenario1HappyPath`) is a **pre-existing load-sensitive timing flake**, proven
not-mine: it passes in isolation on BOTH trees, passes with the full preceding collection order, passed in
full run #1 (which already had the M-C8 worker), and **never calls `hard_kill`** (only
`soft_kill`/`resume`/`is_active`) ⇒ every line M-C8 changed is unreachable from it. Its waits are hard
`timeout=3.0`/`6.0` wall-clock polls; run #1 took 13m42s and passed, this run 17m34s (~28% more loaded) and
timed out. Worth its own fix (event-driven wait), NOT an M-C8 blocker.

**🧪 EARLIER FULL-RUN ATTRIBUTION (11 known + 4 mine = 15):** proven by
`git checkout main -- capital/kill_switch.py main.py` and re-running each suite — **NOT by `git stash`, which
only stashes UNCOMMITTED work: my first "baseline" still contained the committed M-C8 fixes on BOTH sides,
matched perfectly, and would have let me call a real regression "pre-existing".** Verify a baseline actually
lacks the change (`grep -c _dispatch_flatten_worker` → 0). `test_fix181`/`test_order_placer_fix061` look
kill-switch-related but use a **`Mock()` kill switch** ⇒ pre-existing, not reachable by this change.

**🔬 PRE-EXISTING POLLUTION FOUND (NOT fixed — own cleanup owed):** `main._main_locked` declares
`global _log` (`main.py:1538`) and rebinds it (`_log = get_logger("main")`, `:1626`); `test_main` patches
`main.get_logger` → MagicMock, and the patch restores `get_logger` but **NOT `_log`** ⇒ **after `test_main`
runs, `main._log` is a MagicMock for the rest of the session** → `addHandler` is a no-op, `caplog` is empty,
and **any later test asserting on main's logging is silently VACUOUS**. My `test_d3` now installs its own
probe logger and restores it.

**⏰ Deploy:** off-market, consolidated with the M-C cluster (M-C4 `6c77525` + M-C8, then M-C5/M-C6) OR as its
own increment — decide at deploy time; do NOT disturb the deployed `11abebb`. **Emergency path ⇒ fresh
combined regression + ideally a sandbox hard_kill drill before relying on it.** Rollback = revert `5744776`
+ `2d6d005` (schema-free). M-C5/M-C6 still open (mitigated/latent).

See [[mc8-investigation-16jul]] [[mc4-killswitch-lock-16jul]] [[mc-cluster-investigation-16jul]]
[[unpushed-pending-deploy-ledger]] [[deploy-alertwatcher-f1-done-16jul]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 355 B (budget 300 B). The index now carries a hook and this link.

- 🧨✅ **[16-Jul M-C8 FIXED — hard_kill's flatten runs on a worker, not the caller's fill thread](mc8_async_hardkill_16jul.md)** — closes the EXITING-blind shutdown race too. **⚠️ 3 deviations awaited Rama/ChatGPT ratification (report §6.3) — incl. the design's "all existing tests pass unchanged" being FALSE.** [[mc8-async-hardkill-16jul]]
