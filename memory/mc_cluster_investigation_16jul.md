---
name: mc_cluster_investigation_16jul
description: "Capital-safety cluster M-C4/C5/C6/C8 read-only investigation (16-Jul) — verdicts+locations for the fix cycle; C4/C8 reachable, C5/C6 not"
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — capital-safety cluster M-C4/C5/C6/C8 READ-ONLY investigation (verified at HEAD
`a658ba7`; fixed nothing).** Report `docs/audit/mc_cluster_investigation_16jul2026.md`, docs-only commit
`2c9a590` on `main` (UNPUSHED). **Runtime beat the register: only 2 of 4 are reachable now.**

- **M-C4 — ✅ FIXED 16-Jul** ([[mc4-killswitch-lock-16jul]]; branch `mc4-killswitch-lock-16jul`, fix
  `6c77525`, UNPUSHED — lock scope only, RED-on-old 20.02s / GREEN-on-new, full suite zero-new).
  *(was OPEN + REACHABLE, MED)* — `kill_switch.py:649-663` — `record_api_failure` held `self._lock`
  (RLock) and calls `soft_kill` at `:657` INSIDE the lock; soft_kill's `_publish_event`+`_notifier.send`
  (`:495`) then run while the OUTER RLock is still held. The DIRECT soft_kill/hard_kill paths send OUTSIDE
  the lock (fine) — only the AUTO-TRIP path stalls `is_active()`/`current_state()` (the last-mile order
  gate) during the bus-publish + Telegram send. **Fix:** compute the trip inside the lock, call soft_kill
  AFTER releasing it.
- **M-C8 — OPEN + REACHABLE (MED-HIGH). 🔎 DEEPER INVESTIGATION DONE 16-Jul → [[mc8-investigation-16jul]]
  (`63dbb38`): the async design CAN fire-and-return (no caller uses the report); seam = dispatch only the
  adapter path; **#1 hazard = `count_active_positions()` is EXITING-blind ⇒ the eod-self-exit can kill the
  process mid-flatten (latent today)**; no single-flight state exists. Design next.** `kill_switch.py:550` → `_run_cancel` → `_exit_all_trades_
  indestructible` retry loop `:1204-1290` (`time.sleep` 5/15/45s, bounded 2h `_HARD_KILL_MAX_RETRY_HOURS`)
  runs SYNCHRONOUSLY on the caller thread. Callers on the fill/commit path (`order_placer.py:1499/3750`,
  `fund_manager.py:974/2259`) → that thread frozen up to 2h during an emergency, starving the fill/event
  pipeline. **Fix:** trip the kill STATE synchronously (cheap) but run the exit-retry loop on a DEDICATED
  worker thread (CancellationReport becomes async — the non-trivial part).
- **M-C5 — PARTIAL / MITIGATED, race NOT reachable (LOW).** `fund_manager.py:1029-1053` — the
  `_commit_exists` guard is inside `self._lock` but `commit_to_used` (writes the COMMIT row + BL-4
  hard_kill) runs OUTSIDE the lock, so the method is not self-contained atomic. BUT both prod callers
  (`order_reconciler.py:3603 adopt_recovery_trade_to_open`, `:3660 mark_recovery_trade_exiting`) gate on an
  ATOMIC trade-state transition → only one call per trade → the spurious-hard_kill race can't fire. **Fix
  (low urgency):** make the guard+commit atomic, or lock the caller-gate dependency with a test.
- **M-C6 — OPEN / LATENT, not reachable (LOW).** `position_sizer.py:446` `max(1, min(tiered_qty, raw_qty*2))`
  floors a ZERO `effective_mult` to 1 lot (only in the tier-ON path; OFF_FLAT `:455` correctly skips). Only
  zero source = `perf_weight=0`, but `performance_allocator.py` clamps every weight ≥ `min_weight=0.5`
  (`:46/102/114`) → effective_mult never 0. **Reachable IF** min_weight is lowered or a perf_weight=0 path is
  added. **Fix:** `if effective_mult<=0: tiered_qty=0` (→ BELOW_MIN skip) else keep the floor-at-1.

**§3 flags:** M-C4 also spans `bus.publish` (slow subscriber stalls the lock too — same fix); a re-entrant
2nd `hard_kill()` re-runs the sync retry loop (same M-C8 fix must cover it). No new critical issue beyond
the four.

**Why:** these are the most safety-critical paths (kill-switch + capital-commit); precise reachability
changes the fix priority. **How to apply:** Web Claude designs fixes for the REACHABLE ones first
(**M-C8** then **M-C4**), each design → ChatGPT red-team → implement (parity paper+live, one fix per commit,
off-market deploy). C5/C6 are hardening/latent — lower priority, but C6 is a HARD PREREQUISITE before ever
lowering the allocator min_weight. [[pending-register-16jul]] [[capital-operational-note]]
