---
name: mc-cluster-consolidation-16jul
description: "16-Jul-2026 — the M-C capital-safety cluster MERGED into local main + TAGGED, combined regression green, sandbox hard_kill drill 35/35 PASS. UNPUSHED, awaiting Rama's off-market deploy go."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**🏁 THE M-C CLUSTER IS MERGED, VALIDATED AND DRILLED — UNPUSHED, awaiting Rama's off-market deploy go.**
**Tag `deploy-16jul-mc-cluster` → `341cc57` = the CODE point + rollback anchor.** local `main` = `2c7e05d`
(= tag + 1 inert docs commit). **VM==bare still `11abebb` — untouched.** No schema change.
Report `docs/audit/mc_cluster_consolidation_16jul2026.md`.

**⚠️ AT DEPLOY TIME: re-derive the SHA — do NOT trust one written earlier.** Docs ride on top of the tag, so
main's HEAD will have moved. **The TAG is the code identity, not the branch SHA.** The real gate:
`git diff --name-only deploy-16jul-mc-cluster..HEAD` = **markdown ONLY** ⇒ the code deployed IS the drilled
tag. (This trap already fired once today — the alert-watcher/F1 instruction pinned `f68d15d` and main had
advanced 2 docs commits past it.)

**MERGE (3× `--no-ff`): M-C4 `c0c9376` → M-C8 `8bc685a` → M-C5/M-C6/test_main `341cc57`.**
**🔑 The overlap that mattered: `capital/kill_switch.py` is touched by BOTH M-C4 and M-C8.** Git auto-merged
it — **but "auto-merged" is not "correct" on the emergency path**, so both were verified explicitly after.
**M-C4 verified BY AST, not grep:** `record_api_failure`'s only `with self._lock` block contains **ZERO**
`soft_kill` calls; the call site is OUTSIDE it. **The two locks are COMPLEMENTARY BY DESIGN** — M-C4 shrinks
the KS4 `RLock`'s scope; M-C8 avoids that lock entirely via a dedicated `_flatten_lock` (`:245` vs the RLock
`:221`) and cites M-C4 as the reason in its own comments. Docs conflicts (SYSTEM_MAP ×2, PATHS ×1) = keep-both.

**✅ COMBINED REGRESSION: `11 failed / 4763 passed / 15 skipped` — all 11 = the known time-gated PC-env set
(after 16:00 IST). ZERO new.** Pass count cross-checks the merge: 4735 (mc5/mc6 branch alone) + 27 (M-C8) + 1
(M-C4) ≈ 4763 ⇒ no branch's tests were lost. **NO BEHAVIOUR DIVERGENCE** — each fix's suite matches its
isolated result exactly (M-C8 27/27 · M-C5 5/5 · M-C6 7/7 · M-C4 48/48 · test_main identical); all
cluster-touching suites together **276 pass**.

**✅ SANDBOX hard_kill DRILL: 35/35 PASS — NO capital-path invariant violation.** Mock broker + FRESH scratch
DB from `schema.sql`; **the live store was never opened** (asserted in code AND proven externally: its mtime
was byte-identical before and after). Harness `scratchpad/mc_cluster_drill.py` — deliberately NOT committed
(the task adds no repo code). Proven end-to-end: `hard_kill` returns <0.5s with the kill state ALREADY
blocking · the flatten actually flattens (SELL 10 → net 0) · single-flight (re-entrant + cross-thread) · a
fresh flatten still dispatches after COMPLETE · concurrent fill → **no oversell/naked short** (skip-if-flat)
· `UNKNOWN_IN_FLIGHT` not clobbered · **the eod-self-exit REFUSES to fire mid-flatten while the store reports
0 active** (the EXITING-blind race, demonstrated closed) · SIGTERM bounded grace → CRITICAL · thread-start →
INLINE · **M-C4: `is_active()` took 0.000s during a parked notifier send** · M-C5: loser is a clean no-op, NO
spurious hard_kill · M-C6 zero/negative skip + FIX-133 floor preserved · **3-balance invariant holds at init,
after reserve, after the flatten, and after the M-C5 race**.

**⚠️ THE DRILL'S FIRST RUN WAS 25/35 — AND IT WAS THE HARNESS, NOT THE CODE.** `placed=[]` (the flatten fired
no orders) contradicted the 27 passing M-C8 unit tests ⇒ suspect the harness and DIAGNOSE before touching
anything: **`OrderManager.create_trade` leaves `qty_filled=0`** (status PENDING_FILL — not yet filled) and the
flatten **CORRECTLY** skips `local_qty == 0` (an unfilled trade has NO broker position to flatten). The drill
had seeded positions that didn't exist; all 10 failures cascaded from that one error. Product code untouched;
harness fixed → 35/35. **Never a STOP condition** — the criterion is an invariant violation, and every
invariant passed in BOTH runs. [[verify-check-the-rc-not-the-output]]

**⏰ NEXT = Rama's off-market deploy authorization only.** Runbook in report §6: fresh VM backup → push main +
tag → verify (the `diff..tag` = markdown-only gate, hook path, **schema v44 no-migration**, integrity/FK,
services) → completion checklist → memory only after verified. **`trading-system.service` is HALTED on the
planned operator SOFT_KILL and auto-clears at the next 08:15 boot** ([[killswitch-autoclear-prior-day]]) — the
cluster goes live at that boot; no restart owed. **Rollback:** L1 revert a fix · L2 revert a merge · L3 reset
main to `16437ae`. All schema-free.

**Standing caveats:** M-C8 changes the EMERGENCY path — the drill is mock-broker only, so **the first live
HARD_KILL after deploy is the real test**. M-C6 inverts a documented FIX-133 decision (ratified;
behaviour-neutral until `min_weight` is lowered). KS6's "re-runs cancellation" is now PATH-SPECIFIC (legacy
re-runs; adapter is single-flight).

See [[mc4-killswitch-lock-16jul]] [[mc8-async-hardkill-16jul]] [[mc5-mc6-testmain-16jul]]
[[unpushed-pending-deploy-ledger]] [[deploy-alertwatcher-f1-done-16jul]]
</content>

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 372 B (budget 300 B). The index now carries a hook and this link.

- 🏁🔬 **[16-Jul M-C cluster consolidation — merge + regression + sandbox drill](mc_cluster_consolidation_16jul.md)** — pre-deploy validation: 4763 pass, zero-new, no divergence; drill **35/35**. The drill's first run (25/35) was a **harness** bug (`create_trade` leaves `qty_filled=0` ⇒ nothing to flatten), not a code defect. [[mc-cluster-consolidation-16jul]]
