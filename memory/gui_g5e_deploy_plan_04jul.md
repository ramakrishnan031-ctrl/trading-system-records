---
name: gui_g5e_deploy_plan_04jul
description: "G5e ops-dashboard deployment+validation PLAN authored (A–I); merge-gate, rollback tag, cutover human-gate — no execution"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5504e191-b244-4ae5-8321-b8eac900a8f7
---

G5e = the deployment/validation PLAN for the ops_dashboard G5 redesign. Authored
04-Jul-2026 (Sat, off-market) as a **planning artifact only** — ZERO execution
(no deploy/merge/push/restart/production change). Web Claude reviews it; Rama
executes off-market later with a GO ping. Completes the [[gui_g5d_operations_04jul]]
build chain (G5 BUILD is done; G5e is the deploy/soak wrapper).

**Plan doc:** `ops_dashboard/docs/G5e_DEPLOYMENT_PLAN.md` — sections **A–I**:
A deployment checklist · B rollback · C soak-resume (S1–S8 + new-screen) · D smoke ·
E cutover readiness · F risk · G go/no-go · H validation matrix · I report-back format.

**Ground truth (verified read-only 04-Jul):**
- `origin/main == HEAD == 80be23a` — carries the currently-DEPLOYED G2 ops_dashboard.
- **Rollback baseline = `7b1c92d`** (pre-G5 GUI merge; parents `a9d44e0`+`33e9223`).
  Its `ops_dashboard/` tree is functionally IDENTICAL to `80be23a` — the only drift
  7b1c92d→80be23a is `deployment/INSTALL.md` (+40 doc lines). Plan recommends tagging
  `gui-pre-g5-rollback@80be23a` in cutover-prep so rollback is a named target.
- **G5 build lives as UNCOMMITTED working-tree changes** — there is **NO `gui-g5*`
  branch yet** (`git branch -a` verified; the "gui-g5a-04jul" etc. names in earlier
  memories are the intended commit names, not existing branches). Scope = **44
  `ops_dashboard/**` files** (22 modified + 22 untracked).

**Merge-gate (the critical STOP, run FIRST):** create `gui-g5-deploy` off
`origin/main`, `git add ops_dashboard/` only, then
`git diff --name-only origin/main...gui-g5-deploy | grep -vE '^ops_dashboard/'`
must print NOTHING. STOP + report on any `core/ orders/ capital/ strategies/
broker/ signals/ main.py config/ schema` path. **Must EXCLUDE** the non-G5
working-tree noise that is also dirty: `PATHS.md` + `docs/SYSTEM_MAP.md` (both mixed
with telegram/chartink edits), `docs/audit/{c2_chartink,telegram_token_shadow}...md`,
`gui/` (PC source `.txt` specs).

**Deploy = REFRESH, not fresh-install** (venv/systemd/Tailscale already done):
off-market push (never 15:30–17:05 IST; `deploy_preflight.py` market-open gate) →
post-receive checks out `ops_dashboard/` → restart **`gui-dashboard` ONLY** (6 trading
units + DBs + cron untouched) → verify overlay `gui_config.local.yaml` survived
(`chmod 600` + `session_cookie_secure:true`) → Tailscale serve persists (no re-auth,
https://trading-system.tail1cdc6d.ts.net) → curl `127.0.0.1:8500` → 302 /login.

**Rollback = GUI-only blast radius:** `git revert -m 1 <g5-merge-sha>` + push +
`systemctl restart gui-dashboard`. Zero schema to unwind (G5 added none; DBs read-only).

**Smoke:** 21 menu screens (5 groups Dashboard·Trading5·Analytics7·Operations5·
Investigation3) + 9 off-menu direct-URL routes (/risk /capital /exposure /capacity
/pnl /vm /statistics /reports /alerts) + contract checks (13 pipeline stages,
ExportButton OFF, two-state honesty, Controls no-write, ScoreChip single).

**GO iff ALL:** 354 tests green on deploy branch in a **clean env** (PC has 32 known
env-only failures — see [[pc_test_env_hygiene]]) · merge-gate diff clean · smoke pass ·
**Rama's interactive browser sign-off** (the outstanding NOT-RUN human gate — sits
BEFORE production promotion, after smoke) · rollback tag confirmed · off-market window.
**Q3/XLSX stays OFF** at cutover. NO-GO if any fails.

**Soak:** resume the PAUSED S1–S8 contract ([[gui_g2c_deploy_prep_03jul]] +
`SOAK_EVIDENCE_TEMPLATE.md`) against the G5 build + new-screen validation; ≥3 clean
market days = PASS → verdict question "did Rama need Telegram/logs/DB/Excel for
something the dashboard couldn't show?"

Discipline honored: Git HELD (doc written to working tree, no branch/commit/push);
memory + SYSTEM_MAP.md + PATHS.md updated with the G5e planning state.
