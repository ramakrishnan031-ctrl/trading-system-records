---
name: mc4_killswitch_lock_16jul
description: "M-C4 FIXED (lock scope only) — record_api_failure no longer holds the kill-switch lock across soft_kill's publish+send; branch UNPUSHED"
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — M-C4 FIXED (lock scope ONLY, no behaviour change). BUILT + TESTED LOCAL, UNPUSHED.**
Branch **`mc4-killswitch-lock-16jul`** (off `main`@`f68d15d`; 2 commits: fix **`6c77525`** + report
`1b0e5e5`). Report `docs/audit/mc4_killswitch_lock_16jul2026.md`.

**Root cause:** `kill_switch.record_api_failure` (`:649-663`) held `self._lock` (RLock) and called
`soft_kill()` INSIDE the `with` — soft_kill releases only its OWN reentrant acquisition, never the
caller's, so the outer lock stayed held across soft_kill's `bus.publish` (`:483`) AND its Telegram send
(`:495`). `is_active()`/`current_state()` — the last-mile order gate on EVERY entry/exit, every thread —
blocked for that whole I/O, exactly during a broker wobble. **Measured pre-fix: 20.02s blocked.**

**Fix:** count + DECIDE in-lock (`should_trip` + `trip_reason`, reason built in-lock ⇒ byte-identical
message), release, then `soft_kill(...)` OUTSIDE. Covers publish AND send. Public interfaces unchanged;
no second locking mechanism; RLock retained (stale class-docstring claim about the removed reentrancy
corrected); parity = one shared path, no mode-branch; no schema change.

**Verified BEFORE implementing (the two STOP-gates — both clear, NO guard added):**
- **2a soft_kill IS idempotent** (`:456-468`): already-SOFT_KILL → DEBUG + `return` **inside the lock**
  (no republish/renotify/re-mutate); HARD_KILL → return (no downgrade). ⇒ the release-then-call
  double-trip window collapses to ONE publish+send by soft_kill itself.
- **2b state-before-send + no-rollback**: state mutates `:477-480` BEFORE publish/send; `_publish_event`
  (`:783-806`) and the send (`:493-505`) are try/except log-only ⇒ **activation never depends on notify
  success** and cannot roll back.

**Tests:** new `test_mc4_autotrip_does_not_hold_the_lock_across_publish_and_send` — blocks the trip
thread FIRST in `bus.publish`, THEN in `notifier.send`; at BOTH points concurrent `is_active` /
`current_state` / a 2nd `record_api_failure` must return <2s with the kill already active. **RED-on-old
(20.02s blocked) / GREEN-on-new.** kill_switch **48 pass**; callers **318 pass** (signal_processor ×17
sites, order_reconciler, eod_squareoff, cnc_gtt_monitor, p0_live_day1, h4_retry); **full suite 4700 pass,
ZERO new**.

**⚠️ NEW ENV FINDING (see [[pc-test-env-hygiene]]):** the full suite showed an **11th** failure —
`test_interactive_startup::test_holiday_guard_missing_yaml_proceeds` — which is **PRE-EXISTING and
TIME-GATED**, not from M-C4: it fails identically on the pre-fix base ("Outside service window
[08:00-16:00 IST]; current IST 16:19 … assert 0 == 5" = the **FIX-189 startup guard**) and PASSES with
`TS_IGNORE_MARKET_WINDOW=1`. **⇒ the known-PC-env failure count is TIME-OF-DAY dependent: 10 in-window,
11 outside 08:00–16:00 IST.** Always compare a regression to a base run at the SAME time of day.

**⏰ Deploy (off-market, separate):** its OWN branch — EITHER fold into the pending F1+alert-watcher deploy
(**re-consolidate + re-run the combined regression**) OR land as its own increment AFTER that lands. **Do
NOT disturb the validated F1+alert-watcher consolidation (tag `deploy-16jul-alertwatcher-f1`→`1d5337d`)
just to add this.** Rollback = revert `6c77525` (restores the stall; no schema/data/interface change).

**Still open from the cluster:** **M-C8** (sync→async hard_kill retry — NEXT), M-C5 (mitigated), M-C6
(latent). [[mc-cluster-investigation-16jul]] [[unpushed-pending-deploy-ledger]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 430 B (budget 300 B). The index now carries a hook and this link.

- 🔒🛠️ **[16-Jul M-C4 FIXED — kill-switch lock released before the auto-trip publish+send](mc4_killswitch_lock_16jul.md)** — the RLock was held across `soft_kill`'s publish+Telegram send, blocking the last-mile order gate **20.02s** (measured). RED-on-old proven. **env finding: the known-PC-env failure count is TIME-GATED — 10 in-window, 11 after 16:00 IST** ([[pc-test-env-hygiene]]). [[mc4-killswitch-lock-16jul]]
