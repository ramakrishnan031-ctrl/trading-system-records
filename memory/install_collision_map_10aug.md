---
name: install-collision-map-10aug
description: "MEASURED 10-Aug — the nine unpushed branches, their true bases, pairwise file overlaps, and which installs force a REFIT. Read before the first install."
metadata: 
  node_type: memory
  type: project
  originSessionId: a9e5145e-3355-41d5-843b-a151f730acea
  modified: 2026-08-12T13:04:32.262Z
---

# 🗺️ THE INSTALL COLLISION MAP — MEASURED 10-Aug-2026. ⛔ NOTHING REBASED, NOTHING PUSHED.

## 🔴🔴 CORRECTION 12-Aug-2026 — **THIS BLOCK GOVERNS.** `refits = installs − 1` IS **WRONG**
⛔ **The formula below (§3 line "The count of refits is FIXED at (installs − 1)" and §6 "`refits = installs − 1`, ALWAYS") is REFUTED. ⛔ Do not quote either.** The text is **RETAINED, ⛔ not deleted** — it records what was believed on 10-Aug.

**(P) WHY IT IS WRONG: it counted only the SIX code installs. The GUI track pushes to the SAME `origin/main` and was NEVER in that count.** ⇒ install ① moved `main` on 11-Aug at 19:07, and **FOUR MORE moves followed on 12-Aug alone** — `cb6769d` `00:17:27` · `994017a` `13:09:30` · `4bc9713` `14:39:57` · `2bfe9e2` `15:52:42` — ⛔ **none of them an install.**

🔑 **THE CORRECTED STATEMENT: `origin/main` MOVES ON GUI DAYS TOO ⇒ EVERY REMAINING UNIT IS POTENTIALLY BEHIND ON ANY DAY, ⛔ not only on an install evening.** ⭐ **Staleness is a PER-GATE MEASUREMENT, ⛔ never a schedule computable in advance** — so §5's *"6 evenings + 5 daytime refits (~2 weeks)"* is ⛔ **NOT a floor** and must not be quoted as one.

⚖️🚦 **AND THE RULE THAT REPLACES THE ARITHMETIC (Rama, 12-Aug, BINDING): every deploy gate resolves `origin/main` BY MEASUREMENT AT GATE TIME, and the fast-forward check is `git push --dry-run origin <sha>:refs/heads/main` against that measured ref — ⛔ NEVER against a SHA written into a card hours earlier.** **(P) 12-Aug: Gate C2's card-written comparand `2e1f109` returned ✅ PASS while `origin/main` was `2bfe9e2`, and the real push was `! [rejected] … (non-fast-forward)`** ⇒ ⛔ **a stale comparand passes and tells you NOTHING.** → detail in `UNPUSHED_PENDING_DEPLOY_LEDGER.md`, rows `N12-27`…`N12-30`.

## 🔢 §0 · THE COUNT IS **TEN**, ⛔ NOT NINE AND ⛔ NOT EIGHT — and the one that was missing is `main`
**(P) `git branch --no-merged origin/main` = 22; TWELVE are pre-campaign (`gui-*`, `wave4-*`, `preflight-check-21jun`, `score-floor-60`, `fix-p1-eod`, `check1-classify`, `fix-a3`, `fix-t2-import`) and are ⛔ NOT installs. THE LIVE SET IS TEN:**

| # | branch | tip | in the install order? |
|---|---|---|---|
| 1 | `fix/capital-carry-rehydrate` | `2e1f109` | ✅ **① Fix 1** |
| 2 | `fix/preflight-capital-coherence` | `4bd8a42` | ✅ **② Fix 2** (code `ee3ff49`) |
| 3 | `fix/registry-seed-state-split` | `cf16554` | ✅ **③ registry** |
| 4 | **`main`** | `f963438` | ✅ **④ F6** |
| 5 | `fix/tick2-pipeline-scoped-daily-gate` | `43f73b1` | ✅ **⑤ Tick 2** |
| 6 | `feat/tier-multipliers-61-62` | `7d1fd4e` | ✅ **⑥ sizing+tiers** (code `3cf3729`) |
| 7 | `feat/delivery-config-split` | `6d24a83` | ⛔ **NO — docs-only, SUPERSEDED for code** |
| 8 | `fix/alert-phase2-watcher` | `071169b` | ⚪ unscheduled |
| 9 | `fix/alert-remediation` | `bfd6b5f` | ⛔ **NO — SUPERSEDED (P: it IS an ancestor of phase2)** |
| 10 | `fix/n907-forward-shadow-encoding` | `7649cd8` | ⚪ unscheduled, ⭐ zero overlap = free slot |

🔑 **WHY IT WAS MISSED, AND IT MATTERS: `main` IS THE ONLY LIVE BRANCH WITH NO WORKTREE** (P: `git worktree list` has no `[main]` row) ⇒ **every worktree-based count omits it — and it is install ④, F6.** ⭐ Rama's "eight" = the eight SIBLING folders; my "nine" = the nine worktrees. ⛔ **Both counted folders, not refs.**

## §1 · THE STACK — ⛔ NOT all branches share a base
```
645728d  (DEPLOYED)
  ├── fix/capital-carry-rehydrate      2e1f109   Fix 1        own 3 files
  ├── fix/preflight-capital-coherence  4bd8a42   Fix 2        own 5   (code ee3ff49)
  ├── fix/registry-seed-state-split    cf16554   registry     own 3
  └── main  f963438  (CONTAINS F6 c39e799)                    own 9
        ├── fix/tick2-pipeline-scoped-daily-gate  43f73b1     own 3
        ├── fix/alert-phase2-watcher              071169b     own 9
        ├── fix/alert-remediation                 bfd6b5f     (P0+P1 only)
        ├── fix/n907-forward-shadow-encoding      7649cd8     own 2
        └── 65b7196 (sizing, schema v46)                      own 70
              ├── feat/delivery-config-split  6d24a83   ⛔ DOCS ONLY beyond 65b7196
              └── feat/tier-multipliers-61-62 7d1fd4e   own 4 (code 3cf3729)
```
🔑 **THREE sit on the DEPLOYED ref** (Fix 1, Fix 2, registry). 🔑 **SIX sit on `main`'s tip `f963438`, which ALREADY CONTAINS F6.**

## 🔴 §2 · TWO FINDINGS THAT CHANGE WHAT GETS DEPLOYED
- 🔴🔴 **THE SECOND NAMING TRAP, AND IT IS THE SAME SHAPE AS THE FIRST: `feat/delivery-config-split` ADDS NO CODE over `65b7196`** — (P) the non-doc diff is **EMPTY**; all six commits are docs. ⇒ ## **INSTALL ⑥ = `7d1fd4e`. ⛔ NOT `feat/delivery-config-split`** — that name reads like the delivery config split and would ship it **WITHOUT THE TIER CHANGE.** ⭐ **Exactly as `fix/alert-remediation` (P0+P1) reads like the alert fix while the deployable unit is `fix/alert-phase2-watcher` (P0+P1+P2, and P: remediation IS an ancestor of it).** 🔑 **TWICE NOW, THE BRANCH WHOSE NAME MATCHES THE WORK IS THE WRONG ONE TO PUSH.**
- ✅ **CORRECTED — ⛔ IT IS *NOT* AN INSTALL PROBLEM, and the earlier *"neither branch alone is complete"* was too strong.** **(P) ZERO code is lost** by not shipping `delivery-config-split`: the full tip-to-tip diff is **six DOC files** — `PATHS.md`, `SYSTEM_MAP.md`, `MASTER_PENDING`, `order_sizing_allocation_build_08aug2026.md`, `GO_NOGO_f6_deploy.md` (+7/−1), `RUNBOOK_f6_first_live_acceptance.md` (+1) — **and all six EXIST on the tier branch, one revision older.** ⇒ **a docs freshness question, ⛔ not a blocker.**
- ⚠️ **WHERE THE GATE DOC NEEDS TO END UP — NAMED, ⛔ NOT MOVED: the FROZEN gate (`6d24a83`, *"9a resolved … the gate freezes"*) is on `feat/delivery-config-split` ONLY — (P) it is an ancestor of NEITHER `main` NOR the tier branch.** It governs install ④, so **it belongs on `main` BEFORE that install**. ⚠️ **And there are further UNCOMMITTED edits to it in the main worktree (`M docs/decisions/GO_NOGO_f6_deploy.md`).** ⭐ **It is READ by the operator, ⛔ not executed — so it does not need deploying to work; it needs the right REVISION in hand on the night.**
- 🗄️ **THE SIZING INSTALL IS A SCHEMA MIGRATION — v45 → v46**, `core/migrations.py:131` (`46: ["trades"]`, 8 sizing-audit columns, table REBUILD). ⇒ **its night is a CRITICAL-noisy night BY CONSTRUCTION** — [[schema-push-overnight-refusal-27jul]].

## §3 · REFITS IN THE AGREED ORDER — cumulative, MEASURED
| # | install | ref | own | overlap with already-landed | refit |
|---|---|---|---|---|---|
| 1 | Fix 1 | `2e1f109` | 3 | — | ✅ **none** (already on the deployed ref) |
| 2 | Fix 2 | `4bd8a42` | 5 | **0** | ⚙️ MECHANICAL |
| 3 | registry | `cf16554` | 3 | **0** | ⚙️ MECHANICAL |
| 4 | F6 (`main`) | `f963438` | 9 | **2** — `capital/fund_manager.py`, `tests/unit/test_fund_manager.py` | 🔴 SUBSTANTIVE |
| 5 | Tick 2 | `43f73b1` | 3 | **1** — `core/state_store.py` | 🔴 SUBSTANTIVE |
| 6 | sizing+tiers | `7d1fd4e` | 70+4 | **4** — `fund_manager.py`, `risk_engine.py`, `state_store.py`, `signal_processor.py` | 🔴🔴 SUBSTANTIVE **+ schema v46** |
| — | alert-phase2 | `071169b` | 9 | **1** — `main.py` | 🔴 SUBSTANTIVE · ⛔ **NOT in the order** |
| — | n907 | `7649cd8` | 2 | **0** | ⚙️ MECHANICAL · ⭐ **ZERO overlap with EVERYTHING — a free slot** |

⛔ **A MECHANICAL refit is still a refit: it needs a NEW EXACT COMMIT and its own FULL GATE.** ~~⭐ **The count of refits is FIXED at (installs − 1) — every install moves `origin/main`, so no branch's fork point survives. What the ORDER changes is only how SUBSTANTIVE each refit is, ⛔ never how many.**~~ 🔴 **REFUTED 12-Aug — see the CORRECTION block at the top of this file. The count is ⛔ NOT fixed: GUI pushes move `origin/main` too.** ✅ What survives: **the ORDER changes only how SUBSTANTIVE each refit is.**

## 🔑 §4 · THE ORDER QUESTION — ANSWERED, ⛔ AND THE CHEAPER ORDER IS UNSAFE
- ⭐⭐ **A MUCH CHEAPER ORDER EXISTS: `main`/F6 FIRST.** Tick 2, alert-phase2, alert-remediation, n907 and the whole sizing stack **all fork from `f963438`** ⇒ if F6 landed first, **those five would need NO rebase at all** — their base would already BE the deployed ref. Only Fix 1/Fix 2/registry would rebase, and all three are **zero-overlap ⇒ mechanical**.
- ⛔⛔ **IT IS REFUSED, AND THE REASON IS ON RECORD: FIX 1 IS F6's PRECONDITION.** F6 was `NO-GO` on 10-Aug because the capital invariant HARD-KILLS the boot **~60 s upstream of `cnc_gtt_monitor`**, so F6's first live execution would sit behind a gate that can prevent it running at all. ⇒ **the safe order costs five refits and that is the price of the ordering Rama already took.** [[fix1-carried-position-accounting-10aug]]
- ⭐ **What CAN move for free:** **n907** (zero overlap with everything) and the **registry split** (zero overlap in both directions) — their positions are arbitrary.

## 📅 §5 · THE HONEST CALENDAR — ⛔ SIX INSTALLS IS NOT SIX EVENINGS
**6 evenings + 5 DAYTIME REFITS between them**, and two more installs (alerts, n907) are not in the order at all.
- ⛔ **A REFIT NEVER HAPPENS ON A DEPLOY EVENING.** It must land in the **daytime** and produce **a NEW EXACT COMMIT that becomes the ONLY deployable target for that evening** — ⛔ otherwise the gate's md5 manifest and ancestor checks run against a PRE-REFIT SHA. ⭐ Same trap as `fix/alert-remediation` (P0+P1 only), one layer along.
- ⏱️ Each refit = read the overlapping hunks + rebase + **a full gate (~15 min run)**. ⛔ **The step-6 refit is 70 files across FOUR prior installs plus a schema migration — it is NOT a one-daytime job.**
- ⚠️ A refit is PC-side and involves no push, so market hours are fine — ⛔ but the **push** stays after 19:00 [[deploy-push-slot-after-1900-09aug]].
- ⇒ 🔑 **~2 working weeks for the six as a PLANNING BASELINE, ⛔ not one — and ⛔ not a commitment.** The refits are not currently in Rama's plan.

## ⛔ §6 · THE FULL N×N MATRIX WAS DECLINED — RECORDED SO IT IS NOT RE-REQUESTED
**A 36-pair all-branch matrix would add ROWS, ⛔ not information.** ⭐ **What decides a refit is NOT *"do these two branches share a file"* but *"does this branch share a file with WHAT HAS ALREADY LANDED"* — which is what §3 measures, cumulatively, in install order.** ~~⭐⭐ **And the structural result makes the rest moot: `refits = installs − 1`, ALWAYS.**~~ 🔴 **REFUTED 12-Aug — see the CORRECTION block at the top.** ⛔ Most pairs never meet.
⚠️ **AND *"MECHANICAL" ≠ ZERO-RISK:** every refit still needs a **new exact commit**, a **full gate**, and the **deploy target repointed**.
