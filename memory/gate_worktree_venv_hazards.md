---
name: gate-worktree-venv-hazards
description: "The BASE worktree needs venv/ as well as config/instruments.csv, or 3 t4 tests fail as phantoms; and cleaning a junctioned worktree with robocopy /MIR (no /XJ) destroys the REAL venv invisibly to pip."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 984bdc25-3b1a-4022-afb8-d374f2c8be37
  modified: 2026-08-03T15:34:14.167Z
---

**Two hazards in the campaign's BASE-worktree regression gate. Both measured 03-Aug-2026.**

## 1. The base worktree needs `venv/`, not only `config/instruments.csv`

The recipe everyone follows says *copy `config/instruments.csv` into the base worktree* (it is
git-ignored). **`venv/` is a SECOND git-ignored dependency the worktree needs, and it was never
written down.**

Without it, `scripts/ist_now.sh`'s `pick_python()` — which tries `$REPO_ROOT/venv/Scripts/python.exe`
first — falls through to bare `python`, which on this PC is the **Windows Store stub** (exit 49,
*"Python was not found; run without arguments to install from the Microsoft Store"*). Three
`tests/unit/test_t4_deploy_preflight.py` tests then fail:
`test_ist_now_emits_valid_ist` · `test_check_tz_fails_on_broken_utc_form` · `test_check_tz_passes_on_agreement`.

⛔ **They are NOT timezone failures and NOT code failures** — the label would be wrong twice.
⚠️ **Any past worktree-based gate run without `venv/` carried these same 3 phantoms** (a BASE of
12F instead of the true 9F).

**How to apply:** junction it in — `New-Item -ItemType Junction -Path <wt>\venv -Target <repo>\venv`
— then confirm BASE reproduces the recorded campaign baseline (**9F / 5,515P / 4skip** at
`d6c298d`) before trusting any comparison. A BASE that does not reproduce the known baseline is
a broken harness, not a finding.

## 2. ⛔ NEVER `robocopy /MIR` (or `Remove-Item -Recurse`) a tree containing that junction

`robocopy <empty> <worktree> /MIR` **without `/XJ` follows the junction and mirrors the empty
directory into its target** — i.e. it deletes packages out of the REAL venv. Delete the junction
first with `cmd /c rmdir <path>` (removes the reparse point, not the target), or pass `/XJ`.

**Why:** it happened. The repo venv lost `iniconfig`, `cachetools`, `kiteconnect`, `flask`,
`dateutil` and more.

⭐⭐ **The part that fools you afterwards: the damage is INVISIBLE TO PIP.** The package
*directories* are gone but their `*.dist-info` remain, so pip believes everything is installed
and **`pip install -r requirements.txt` is a silent no-op**. `python.exe` and `pip` survive, so
the venv looks healthy until an import fails deep in a test run.

**How to apply:** repair with
`pip install --force-reinstall -r requirements.txt -r requirements-dev.txt`, never a plain `-r`.
⚠️ **Then re-pin the interpreter**: `requirements-dev.txt` says `pytest>=9.0.3` with **no
ceiling**, so the repair silently upgraded pytest to 9.1.1 — replacing the version every campaign
baseline was measured under. This is [[unpushed-pending-deploy-ledger]]'s `R14` (should V2 pin the
interpreter?) with evidence attached. Verify restoration by collection count **and** a full-suite
re-run compared against the pre-damage failure set.

## 3. ⛔ The standing-failure COUNT is 8 *or* 9 — compare SETS, never the number

Settled 03-Aug by 6 consecutive isolated runs of
`tests/unit/test_instance_lock.py::TestSingleInstanceAcrossProcesses`: **`2F/4P` ×5 and
`1F/5P` ×1**. In the same evening `test_p2_restart_after_crash_is_not_blocked` **failed in both
worktree runs, passed in both main-tree runs**.

⛔ **It is FLAKY.** The gate-(c) record calling it *"deterministic (2F/4P on 4 consecutive
isolated runs)"* is **wrong** — corrected here. A ±1 failure on this class is **noise**, so a
whole-suite total of **8F or 9F are both normal**.

**How to apply:** never gate on the failure COUNT. Diff the failure SETS with `comm` both ways,
and treat a lone `test_instance_lock` delta as noise unless something else moves with it. (Its
2F/4P isolated signature is also the cheapest proof that a repaired venv still has the original
launcher-stub behaviour.)

See [[feedback-no-fixed-test-baseline]] [[feedback-verify-rc-not-output]] [[pc-test-env-hygiene]]
