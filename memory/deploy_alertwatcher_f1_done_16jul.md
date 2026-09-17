---
name: deploy-alertwatcher-f1-done-16jul
description: "16-Jul-2026 off-market deploy DONE — alert-watcher --loop + F1 trades.sector/gate-8-observe live at 11abebb; alert-watcher respawn loop killed (104,567 -> 0); two soaks owed."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
---

**16-Jul-2026 ~18:42–18:50 IST — the CONSOLIDATED alert-watcher + F1 deploy is LIVE. VM==bare==`11abebb`.**
Executed by VS Code Claude on Rama's handed instruction (v2), off-market (past 17:05). Report
`docs/audit/deploy_done_16jul2026.md`. Push: `c9fb298..11abebb` + tag `deploy-16jul-alertwatcher-f1`→`1d5337d`.

**The SHA deviation (Rama-approved, worth remembering as a pattern):** the instruction pinned `main` at
`f68d15d` and made any mismatch a §9 STOP. Actual was `11abebb` — 2 docs-only commits (M-C8 report
`63dbb38` + SYSTEM_MAP `11abebb`) had landed after the instruction was drafted. Resolved by proving the
delta inert rather than by trusting the SHA: `git diff --name-only 1d5337d..11abebb` = 5 files, all `.md`,
+366 lines; **non-markdown delta = EMPTY ⇒ deployed CODE == the regression-green tag**. Asked Rama; he
approved. **The tag, not the branch SHA, is the code identity — verify against the tag.**

**Deployed behaviour change: NONE.** F1 = `sector_cap_mode: observe` (log-only, `config/system_config.yaml:187`);
alert-watcher = monitoring. Schema **v44 unchanged, no migration** (v44 == EXPECTED_SCHEMA_VERSION).
Backup `data_store/backups/pre_deploy_16jul.db` (357MB, integrity ok, 361 trades).

**alert-watcher FIXED:** `activating`/auto-restart **NRestarts=104,567 → `active`/`running` NRestarts=0**,
running `--loop` (PID 1318632 @ 18:47:03). Canary ALL GREEN incl. the new 5th `respawn` probe.

**⏰ TWO SOAKS OWED:**
1. **alert-watcher 24h** — re-sample ≈17-Jul 19:00 vs baseline (16-Jul 18:47:50, PID 1318632):
   **RSS 37,548kb · VSZ 50,264kb · threads 1 · fd 4 · db_fds 0**. ANY sustained growth → ROLLBACK
   (revert unit to `--once`+`Restart=always`; the crash cause is already fixed, so revert is loop-only).
2. **F1 observe ≥1 session** — **first data = Fri 17-Jul** (engine paused tonight, see below). Collect
   UNKNOWN-sector % · WOULD_REJECT count · sector distribution · DQ count · concentration → evidence
   report → **Rama's explicit approval** → `observe→enforce` as a SEPARATE off-market step.

**M-C4 (`6c77525`, branch `mc4-killswitch-lock-16jul`) deliberately NOT in this deploy — still UNPUSHED,
its own later increment.** PC `main`==`16437ae` = `11abebb` + 1 docs commit, **left UNPUSHED on purpose**
(pushing it would move bare HEAD off the verified `11abebb`).

See [[consolidation-16jul]] [[f1-trades-sector-16jul]] [[alertwatcher-loop-fix-16jul]]
[[unpushed-pending-deploy-ledger]] [[killswitch-autoclear-prior-day]] [[verify-check-the-rc-not-the-output]]
</content>

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 482 B (budget 300 B). The index now carries a hook and this link.

- ✅🚀 **[16-Jul DEPLOY DONE — alert-watcher `--loop` + F1 observe LIVE; VM==bare==`11abebb`](deploy_alertwatcher_f1_done_16jul.md)** — off-market 18:42–18:50, v44 no-migration, behaviour change NONE. **alert-watcher respawn loop KILLED (NRestarts 104,567→0).** The TAG is the code identity, not the branch SHA. ⏰ 2 soaks were owed → Rama-gated F1 enforce flip (alert-watcher 24h; F1 observe ≥1 session, first data Fri 17-Jul). [[deploy-alertwatcher-f1-done-16jul]]
