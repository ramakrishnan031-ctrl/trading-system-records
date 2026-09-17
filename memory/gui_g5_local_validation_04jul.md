---
name: gui_g5_local_validation_04jul
description: "G5 pre-cutover LOCAL validation — clean-env 354/0, route sweep clean, CONDITIONAL GO (Rama browser pass pending)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5504e191-b244-4ae5-8321-b8eac900a8f7
---

Pre-cutover LOCAL validation of the ops_dashboard G5 build (no deploy/merge/push/VM
restart — local branch + commit + run + evidence only). Follows
[[gui_g5e_deploy_plan_04jul]]. Evidence doc:
`ops_dashboard/docs/G5_SIGNOFF_EVIDENCE.md`.

**Local deploy branch:** `gui-g5-deploy` off `origin/main`(`80be23a`), commit
**`91cc207`** — LOCAL ONLY, NOT pushed. Merge-gate CLEAN: committed diff
`origin/main..HEAD` = **45 files, all `ops_dashboard/**`** (0 core/orders/capital/
strategies/broker/signals/main.py/config/schema). The 5 non-G5 dirty paths
(`PATHS.md`, `docs/SYSTEM_MAP.md`, 2×`docs/audit/*`, `gui/`) were left UNSTAGED (ride
a later docs commit).

**Clean-env test result (the go/no-go gate):** fresh throwaway venv `.venv_validate`
(deleted after) with pinned GUI deps only (Flask 3.1.3/Waitress 3.0.2/pyotp 2.9.0/
PyYAML 6.0.3/pytest 8.3.4; **kiteconnect ABSENT = I4 PASS**). **`pytest -q` → 354
passed / 0 failed** (87.74s). ZERO env-only failures in this suite — the ~32 known PC
env failures ([[pc_test_env_hygiene]]) belong to the MAIN repo suite, not the
isolated GUI suite. Gate tests explicitly PASS (28/28): pinned 6/13/8/6/4
(`pinned_contract_counts_unmoved`, `pipeline_still_13_stages`, `pinned_shapes_frozen`
g5c+g5d) · HARD_KILL blink==1 (`hard_kill_blink_still_single`) · two-state honesty
(`two_state_panel_is_honest_never_fabricates`, positions/holdings) · single System
Score (`score_chip_is_system_score_only`) · export OFF · isolation I1–I7
(`test_isolation` a=no-prod-imports/b=readonly-DB/c=no-kiteconnect/**d=no-CDN gate**).

**Route sweep (STEP 6):** (a) LIVE unauthenticated sweep on real Waitress server
`127.0.0.1:8500` — 61 routes: 30 page→302, 30 api→401, /login→200; **0 404, 0 500**
(every route registered, framework clean, auth enforced). (b) authed sweep via test
client — 60 static routes × 2 fixtures = **120 passed** (all 200 authed). Dynamic
routes (`/api/strategies/<name>`, `/api/trade-story/<id>`, gated
`/api/reports/download`) covered by unit tests.

**Browser sign-off (STEP 5): PENDING — Rama's binding human gate.** Cannot be
self-signed: the production overlay stores only a password HASH, so no autonomous
login (TOTP computable from overlay, plaintext password is not). Many STEP-5 items
already have objective backing (auth-401, export-off, two-state honesty, single
System Score, Controls zero-write, 13 stages, pinned counts, no-404/500 all
CONFIRMED); the rest are visual/content confirmations for Rama.

**VERDICT: CONDITIONAL GO** — every machine-verifiable gate GREEN (354/0 · gate tests ·
no 500/404 · merge-gate clean); recommend GO contingent on Rama's browser pass
confirming visual/content items. NO-GO if any STEP-5 item fails (fabricated broker
number, a write control, missing/broken screen, wrong period numbers). Recommendation
only — actual merge/push/VM deploy/soak-resume happens later off-market on Rama's
explicit GO.

**Parity:** confirmed display-only — no screen branches on paper/live; mode is a
displayed data attribute. Cleanup done: `.venv_validate` + temp sweep test deleted;
background server stopped; `.venv` (configured) untouched. `G5_SIGNOFF_EVIDENCE.md`
left as an untracked working-tree artifact (not in the 45-file commit).
