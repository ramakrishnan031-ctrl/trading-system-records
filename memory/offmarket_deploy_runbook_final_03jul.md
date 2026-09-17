---
name: offmarket_deploy_runbook_final_03jul
description: Final commands-only production runbook for the A-2/C-1/B-1/P1 off-market batch (03-Jul); distilled + git-state re-verified
metadata: 
  node_type: memory
  type: project
  originSessionId: 157eab85-5916-43a3-9c57-323a11cc5b69
---

FINAL commands-only runbook distilled from [[offmarket_deploy_plan_03jul]] (committed doc
`docs/ops/offmarket_deploy_plan_03jul2026.md` @ `5f965d3` on `fix-c1-completion-02jul`; NOT in the
`fix-p1` checkout — that's why Rama couldn't find it). Output in full to Rama in the 03-Jul session;
no build, no push.

**Git topology RE-CONFIRMED this session (shifted since plan authored):**
- `main == origin/main == 9becf8c` (schema v41).
- C-1 `fix-c1-completion-02jul` @ **`678c592`** (03-Jul path-fix commit on top of `5f965d3`) — carries A-2
  `fd09a38` as ancestor + docs commits (aa02f9f C-1 scripts, 3d34357/a0c8605/b5660f6 docs, 5f965d3
  deploy-plan, 678c592 data_store/ path fix). **A-2 rides inside C-1 — do NOT merge fix-a2 separately**
  (its branch no longer exists standalone; `fd09a38` is a C-1 ancestor).
- B-1 `fix-b1-daily-loss-mtm-02jul` @ `f5fd4d9` (single commit, SHADOW).
- P1 `fix-p1-eod-broker-reconcile-02jul` @ `4817032` (single commit, SHADOW, schema v42).
- `9becf8c` is a strict ancestor of `678c592` → **C-1 lands as a deterministic fast-forward → main==678c592.**
- Full sequential merge chain **C-1→B-1→P1 = CLEAN** (re-verified via `git merge-tree` write-tree chain
  against the new `678c592` tip on 03-Jul).

**Verified real keys/metrics for the verify step** (grepped in branch code, not guessed):
- B-1: `orders/order_reconciler.py::_refresh_unrealized_mtm` (L2811) + counters `_mtm_refresh_success`/
  `_mtm_refresh_failure`; shadow log `risk_engine.daily_loss.would_reject_with_unrealized`
  (`risk_engine.py:533`); flag `daily_loss_include_unrealized: false` (system_config L176).
- P1: table `eod_broker_reconciliation` (schema.sql L1455) with cols `overall_status,self_consistency,
  authoritative,eod_verify_status,mismatch`; `EXPECTED_SCHEMA_VERSION = 42` (state_store L101); flag
  `eod_reconcile.authoritative: false` (system_config L278); cron `58 15 * * 1-5 ... eod_broker_reconcile.py`.
- A-2: `except BrokerTimeoutError` in **3** placement paths (signal_processor L1009/1663/1936).

**Runbook shape (8 sections):** STEP0 gate (03-Jul 08:15 boot clean) · STEP1 window (after-17:05-Fri or
weekend, never 15:30–17:05) · STEP2 back up BOTH DB files (`/home/ubuntu/systems/trading-system/data/{trading_system,analytics}.db.pre-v42-<date>`)
· STEP3 merge C-1(ff→5f965d3)→B-1(--no-ff)→P1(--no-ff) · STEP4 single `git push origin main` · STEP5
verify (HEAD parity, crontab==canonical @15:58, schema 42, both flags OFF, A-2 x3, MTM counters, P1 row,
drift clean) · STEP6 rollback (flag-flip preferred; `git revert -m 1 <merge-sha>` P1-then-B-1; schema
pure-add) · STEP7 **recommend WEEKEND** (zero overlap with live v41 trader/15:58 job) · STEP8 dates
(B-1 enforce ≥Mon 13-Jul · P1 authoritative + eod_verify/reconcile_pnl retire ≥Mon 20-Jul, after ≥2
clean shadow weeks + ledger deepening + real-unreachable UNVERIFIED demo).

PATHS.md L393 + SYSTEM_MAP.md already reference the committed plan **on C-1** — they land at merge; no
working-tree edit made on `fix-p1` (kept clean for the merge). NO push this pass.

**STEP-0 GATE RESULT (03-Jul ~09:30 IST, read-only check): PASS — weekend push CLEARED.**
VM running 9becf8c (bare main, tree≡main), trading-system active since 08:15:28, prior-day SOFT_KILL
(circuit_breaker 02-Jul) auto-cleared at boot → INACTIVE, pre-flight A/B/C all rc=0 (markers 08:30:03/
09:14:02/09:19:48; token minted today 08:15:01), dirty-grep clean (only the 2 expected kill-switch
startup lines + benign BL-2 subscribe), schema v41 / P1 script+cron ABSENT / 0 B-1 markers.

**✅ STEP2 BACKUP PATH BUG — FIXED in the doc (03-Jul, commit `678c592` on C-1, doc-only, unpushed).**
Was: `data/{trading_system,analytics}.db` (stale relic — `data/trading_system.db` = 0 bytes since 18-May);
real DBs = `data_store/` (PATHS.md L24-25, verified live: 230MB + 6MB). Fixed ALL sections, not just STEP-2:
§2.3 backup (both cp), §4.1 + read-only sqlite3 schema check, §5.2 + ready verdict query on
`eod_broker_reconciliation`, §10 + explicit `data_store/` restore command; stale `b5660f6 "current HEAD"`
tip-annotations ×3 generalized to "C-1 tip". Grep-gate: 0 `data/` DB refs remain. Merge chain re-proven
CLEAN vs `678c592`; sqlite3 CLI confirmed on VM (`/usr/bin/sqlite3`).
Hygiene (F-backlog): trading-watchman exits 0 at 08:15 boot & nothing restarts it at 09:15 (dead ALL
market hours; identical 02-Jul → pre-existing, not a 9becf8c regression); `preflight_runs` v33 table has
NO prod writer (always empty — dashboard readers see nothing); something legacy still writes `data/state.db`
(mtime 02-Jul 16:01).
