---
name: deploy-mc-cluster-done-16jul
description: "16-Jul-2026 ~22:1x IST — the M-C capital-safety cluster (M-C4+M-C5+M-C6+M-C8) is DEPLOYED. VM==bare==06a61cb, code == tag 341cc57. Goes LIVE at the 17-Jul 08:15 boot; no restart owed."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**✅🏁🚀 THE M-C CAPITAL-SAFETY CLUSTER IS DEPLOYED — 16-Jul-2026 22:12–22:14 IST, off-market.**
**VM==bare==`06a61cb`** (was `11abebb`); **the deployed CODE == the drilled tag
`deploy-16jul-mc-cluster`→`341cc57`**. Schema **v44 unchanged, NO migration**; integrity/FK clean; services
healthy; **no code changed during the deploy**. Backup `data_store/backups/pre_deploy_mc_cluster.db` (357MB,
integrity ok, 361 trades). Report `docs/audit/deploy_done_mc_cluster_16jul2026.md`. PC `main`==`3af55d4` =
`06a61cb` + 1 docs commit, **deliberately UNPUSHED** (pushing it would move bare off the verified HEAD).

**⏰ GOES LIVE AT THE 17-Jul 08:15 BOOT — NOTHING OWED TONIGHT.** `trading-system.service` is halted on the
planned operator SOFT_KILL; the row is `SOFT_KILL | 2026-07-16 | operator`, which at the 17-Jul boot is a
**PRIOR-DAY** kill ⇒ `main.py:1607 clear_stale_state` auto-clears it (verified present in the deployed tree).
**No restart, no resume, no operator action.** [[killswitch-autoclear-prior-day]]

**🔑 THE CODE-IDENTITY GATE IS WHAT MADE THIS SAFE — and it MATTERED AGAIN.** Local main at run time was
**`06a61cb`, NOT the `341cc57`/`2c7e05d` written in the consolidation report** — docs commits had ridden on
top. Re-derived at run time and proved identity against the **TAG**, before the push AND again on the
deployed bare history: `git diff --name-only deploy-16jul-mc-cluster..HEAD` = **markdown ONLY** ⇒ the code
deployed IS the drilled, regression-green tag. **The TAG is the code identity, not the branch SHA.** (Same
trap fired this morning on the F1 deploy where the instruction pinned `f68d15d`.) [[deploy-alertwatcher-f1-done-16jul]]

**All 4 fixes verified in the CHECKED-OUT tree — M-C4 by AST, not grep** ("is the call inside the lock?" is a
structural property a text search cannot honestly answer): `record_api_failure`'s `with self._lock` block
contains **ZERO** `soft_kill` calls; the call is at line 750, outside. M-C8 worker + dedicated
`_flatten_lock` + FlattenState · main.py gate + `_shutdown` drain + wired · M-C5 `_commit_claims` · M-C6
`ZERO_MULTIPLIER` · test_main fixture — all INTACT. Deployed modules compile; `config_loader.load_all()` OK.

**Boot-readiness verified, not assumed:** deployed `EXPECTED_SCHEMA_VERSION=44` == live `schema_version=44`
⇒ the 08:15 boot **skips migration**; no migration-guard sentinel fired; token auto-refresh cron present.

**⚠️⚠️ THE ONE THING TO WATCH: M-C8 REWROTE THE EMERGENCY-EXIT PATH, AND THE DRILL WAS MOCK-BROKER ONLY —
IT CANNOT PROVE REAL-BROKER LATENCY BEHAVIOUR. THE FIRST LIVE HARD_KILL AFTER THIS DEPLOY IS THE REAL TEST.**
Log lines to watch:
- GOOD: `kill_switch: HARD_KILL flatten dispatched to worker thread` → then
  `kill_switch: flatten worker finished — all N attempted position(s) flat`
- LOUD (each ⇒ **manual broker-truth verification**, never flatten from DB state):
  `flatten worker finished with N UNEXITED trade(s)` · `flatten worker CRASHED` ·
  `SHUTDOWN WITH FLATTEN STILL RUNNING` (external SIGTERM outran the 15s grace — positions may remain open) ·
  `could NOT start the flatten worker … running the flatten INLINE`

**Standing:** M-C6 inverts a documented FIX-133 decision (ratified; inert until `min_weight` is lowered);
**KS6's "re-runs cancellation" is now PATH-SPECIFIC** (legacy re-runs; the adapter path is single-flight).

**Rollback (all schema-free):** L1 revert an individual fix · L2 revert a merge (`c0c9376` M-C4 / `8bc685a`
M-C8 / `341cc57` M-C5+M-C6) · L3 reset main to `16437ae` (= the previously deployed code point `11abebb` +
docs). Any rollback needs an off-market push; no restart owed while the engine is halted.

See [[mc-cluster-consolidation-16jul]] [[mc4-killswitch-lock-16jul]] [[mc8-async-hardkill-16jul]]
[[mc5-mc6-testmain-16jul]] [[unpushed-pending-deploy-ledger]]
</content>

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 551 B (budget 300 B). The index now carries a hook and this link.

- ✅🏁🚀 **[16-Jul M-C CAPITAL-SAFETY CLUSTER DEPLOYED (M-C4+C5+C6+C8)](deploy_mc_cluster_done_16jul.md)** — code == the drilled tag `341cc57`; v44 no-migration; all 4 verified in the checked-out tree (M-C4 by AST). **⚠️ M-C8 rewrote the EMERGENCY path and the drill was MOCK-broker only ⇒ THE FIRST LIVE HARD_KILL IS THE REAL TEST** (watch `flatten dispatched…`+`all N flat` = good; `UNEXITED`/`CRASHED`/`SHUTDOWN WITH FLATTEN STILL RUNNING`/`could NOT start the worker` ⇒ manual broker-truth check). [[deploy-mc-cluster-done-16jul]]
