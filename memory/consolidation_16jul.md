---
name: consolidation_16jul
description: 16-Jul COMBINED DEPLOY — alert-watcher + F1 MERGED to main + tagged; ONE off-market push (UNPUSHED). Supersedes the two separate branch pending-pushes.
metadata: 
  node_type: memory
  type: project
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
---

**16-Jul-2026 — COMBINED DEPLOY CONSOLIDATED (integration only, no new code). MERGED to local `main` +
TAGGED, UNPUSHED.** The two approved branches now land together in ONE off-market push.

**State:** VM==bare==`origin/main`==`c9fb298` (15-Jul combined LIVE, schema v44). **Merged `main`@`a658ba7`**
= alert-watcher merge `1d5337d` over F1 merge `e8226db` over `3b9041a` (+ consolidation docs on top).
**Tag `deploy-16jul-alertwatcher-f1`→`1d5337d`** = named ref for the exact deployed code (docs ride on
top, inert). Both merges `--no-ff` → clean per-branch `git revert -m 1` rollback.

**Merge cleanliness:**
- **Config overlap AUTO-MERGED** (no STOP): `config_loader.py` kept BOTH — `AlertsConfig.respawn_restart_delta_threshold`(3)/`respawn_rate_per_hour_threshold`(6.0) [branch 1] + `RiskConfig.sector_cap_mode`(observe)/`sector_unknown_alert_pct`(0.20)+validators [branch 2]; different classes. `system_config.yaml` = F1's sector fields only (branch 1 kept respawn thresholds override-only). Model validates.
- **Only conflict = `PATHS.md`** top banners (trivial doc) — resolved keep-both (HEAD operator-docs + F1 banners + the alert-watcher branch's updated respawn-finding line). SYSTEM_MAP + test_config_loader auto-merged.

**Gates (merged main):**
- **Combined regression: 4700 pass / 10 fail / 15 skip** — the 10 are ALL PRE-EXISTING PC-env, verified
  IDENTICAL on the pre-merge base `3b9041a` (Mock-subscriptable / `int(Mock)` / thread artifacts; green on
  VM). **ZERO new from the merge.**
- **deploy_assert rc=0** (quick_check ok · FK clean · schema live=44==expected=44 · email ok). *(A first
  PC run hit the known cp1252 `✅`-emoji `UnicodeEncodeError`→rc=1 cosmetic; `PYTHONIOENCODING=utf-8`→rc=0.)*
- `PRAGMA integrity_check` ok · `foreign_key_check` CLEAN · schema **v44** (both branches schema-free — no migration).

**Behaviour-neutral on deploy:** gate-8 `sector_cap_mode=observe` (log-only; F1's enforce flip is separate,
Rama-gated); alert-watcher is monitoring-only (isolated from trading).

**⏰ UNIFIED OFF-MARKET RUNBOOK (Rama, tonight; report `docs/audit/consolidation_16jul2026.md`):** ONE
`git push origin main` (+ tag) → verify bare==`1d5337d` → alert-watcher unit reinstall+`daemon-reload`+restart
+ 24h RSS/fd/thread/DB soak → F1 OBSERVE SOAK ≥1 session (archive UNKNOWN% / WOULD_REJECT / distribution /
DQ-alerts) → SHORT evidence report → **ONLY after Rama's EXPLICIT approval** flip `sector_cap_mode
observe→enforce` (activates the live 40% sector cap). Rollback: L1 per-branch `git revert -m 1`; L2 reset
main→`3b9041a`; F1 enforce = instant config de-fang (→observe).

**NOTHING pushed.** Supersedes the two separate branch pending-pushes ([[alertwatcher-loop-fix-16jul]] +
[[f1-trades-sector-16jul]]) → now ONE merged pending push. [[unpushed-pending-deploy-ledger]]
