---
name: mo5-deployed-22jul
description: M-O5 deployed — fire_now resets the EOD fired-flag on failure so the 15:17 backstop can retry; RESET_PNL must be SUM-verified.
metadata: 
  node_type: memory
  type: project
  originSessionId: f27493f3-bd21-4f8c-b3f6-2b541fbdd7df
  modified: 2026-07-22T11:21:15.805Z
---

M-O5 DEPLOYED 22-Jul-2026 off-market — commit `4585bd2`, tag `deploy-22jul-mo5`, PC==origin==VM tree; schema v44, no migration.

**Bug:** `orders/eod_squareoff.py::fire_now` set `_fired_for_date[today]=True` before `_fire` with **no reset on failure**; `check_and_fire` (the 15:17 scheduled backstop) reads the SAME flag and skips if set ⇒ a `fire_now` (the AUTOMATIC daily-loss-breach callback `main.py:780`, its ONLY caller — no operator trigger) whose `_fire` **raised, or returned with positions/cancels un-squared**, silently disabled the scheduled squareoff. `check_and_fire` already reset-on-exception; `fire_now` was the lone asymmetry.

**Fix:** mirror `check_and_fire:223-229` (reset flag on exception + re-raise) + **Rider 1** (also reset when `positions_failed>0 or cancels_failed>0`); flag **STAYS set on full success** (so 15:17 doesn't re-square what fire_now already squared). Safe: the E.5 broker-position filter re-queries broker truth so a retry cannot double-square; `check_and_fire` has run this exact pattern in production.

**Verification:** RED-first tests (raise · partial-fail · reset_daily_pnl-twice · a `check_and_fire` reset pin); full `test_eod_squareoff.py` 68✓; regression `comm-23` **EMPTY both ways** (same-env, 11==11 pre-existing). ⚠️ a `git worktree` BASE was **env-confounded** (missing untracked files + Microsoft-Store `python` alias); redone same-tree (revert 2 files via verified patch, never stash) → clean. Backup `pre_deploy_mo5_20260722.db` (v44, quick_check ok). Service NOT restarted (inactive by the 16:00 self-exit; loads at next 08:15 boot).

**Why:** M-O5 was the sole Tier-A live careful-loop item ⇒ deploying it empties Tier A; the careful-loop backlog is now clear.

**How to apply:** ⚠️ **B1 — verify RESET_PNL by `SUM(pnl_delta)` over the RESET_PNL rows, NEVER a single-row read.** A Rider-1 retry runs `reset_daily_pnl` (`fund_manager.py:1617`, `entry_type='RESET_PNL'`, `pnl_delta=-old_pnl`) **twice in one day**; the 2nd row carries `-(net at 15:17)`, non-zero. **B2/B3 — no natural production-verification day** (0 daily-loss breaches in 30 d + a raise-resistant `_fire`): the RED-first tests are the entire evidence base; an 08:15 boot does NOT exercise an EOD-path change. Recorded at the highest-propagation surface (`docs/SYSTEM_MAP.md` top banner). Reports `docs/audit/mo5_investigation_22jul2026.md` + `docs/audit/mo5_deploy_22jul2026.md`. Sibling of the [[e4-w10-done-17jul]] `pnl_delta`-is-NET contract; the daily-loss trigger that fires fire_now is [[persisted-kill-is-halt-21jul]]-adjacent.
