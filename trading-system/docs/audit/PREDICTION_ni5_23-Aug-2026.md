# FROZEN PREDICTION — NI-5, option (a)

**Written:** 23-Aug-2026, BEFORE any build action.
**Base:** `742d9da` (`fix/delivery-fill-and-ni-22aug`), worktree `j2-work`, clean.
**Ruling being executed:** option **(a)** — extend NI-5 into `core/config_auditor.py`
and its test. Authorising quote, Rama, 23-Aug: *"act on these 2 files simultaneously,
dont skip anything"*.
**Governed by:** `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

> ⛔ Nothing below may be edited after the build starts. A wrong prediction is
> recorded as wrong; it is not corrected retroactively.

---

## PRE-BUILD MEASUREMENT (done first, at `742d9da`)

| # | question the gate requires | measured answer |
|---|---|---|
| 1 | Does this already exist? | No. The three params carry defaults at `capital/position_sizer.py:136-153`. |
| 2 | Who owns the value today? | `config/system_config.yaml` → `ps_cfg`, passed at `main.py:2501-2524`. The constructor default is a **second, silent owner** — that is the defect. |
| 3 | Is there a second place it lives? | Yes — the constructor defaults themselves, plus `core/config_auditor.py:176-177`, which asserts default==config for `max_position_value_pct` only. |
| 4 | Old → new expression | `risk_per_trade_pct: float = 0.01` / `max_concentration_pct: float = 0.10` / `max_position_value_pct: float = 0.40` → all three **required**, `max_position_value_pct` moved above the defaulted block. |
| 5 | Every call site (swept, not taken on trust) | **21** real `PositionSizer(` sites (`_MockPositionSizer` is a different class and is excluded). **1 production:** `main.py:2501` — already passes all three explicitly ⇒ **no production edit**. **20 in tests**, 0 positional ⇒ re-ordering is safe. |

---

## THE PREDICTIONS

### P-1 — scope
The diff touches **`capital/position_sizer.py` + `core/config_auditor.py` + test files
only**. No third production file.
**FALSIFIER:** any production file besides those two appears in the diff ⇒ the tripwire
has fired again ⇒ STOP and report, do not commit.

### P-2 — production is already safe
`main.py` needs **no edit**; the sole production construction site already passes all
three keys from config.
**FALSIFIER:** the suite fails anywhere that constructs the sizer from `main.py`'s path,
or `main.py` appears in the diff.

### P-3 — 🔴 THE AUDITOR-BLINDNESS CASE (the explicit falsifier the card demands)
This is the prediction the whole option-(a) ruling rests on. It will be **measured in an
intermediate state**, with the defaults removed and `config_auditor.py` deliberately
**not yet fixed** — so the check can come back red.

With defaults removed and the auditor unchanged, I predict **all three** of:

- **(i)** group F reaches `core/config_auditor.py:581` `if default is
  inspect.Parameter.empty: continue` and **silently drops** the `PositionSizer`
  row — no finding of any severity is emitted for it;
- **(ii)** `_group_f_stale_default` still returns the `F_ok` **PASS** at `:592-595`,
  whose text reads *"component defaults match config intent (position-value cap +
  daily-loss pct)"* — naming a cap it did **not** check. This is the `V5`
  tautological-check class;
- **(iii)** `tests/unit/test_config_auditor.py::TestGroupFStaleDefault::test_diverging_position_cap_default_warns`
  **FAILS**.

**FALSIFIER:** if that test PASSES, or if group F emits any finding for the
`PositionSizer` row, or if the PASS message does not appear — then §5's diagnosis in
`docs/audit/JOB1_AND_NI_ITEMS_22-Aug-2026.md` was **wrong**, option (a) has no
justification, and I must STOP and report that the stop-reason itself did not reproduce.

⭐ A green suite at this intermediate step would **disprove** the reason for the ruling.
The step exists so the fix is proven necessary before it is written.

### P-4 — after the auditor fix
Group F performs exactly **one** real default-vs-config comparison
(`FundManager.daily_loss_limit_pct`), the `PositionSizer` row is reported **explicitly**
as required-therefore-not-compared rather than skipped, and the summary line names
**only** what it actually compared.
**FALSIFIER:** the summary still claims the position-value cap was checked; or the
skipped row produces no output at all.

### P-5 — severity is not escalated
No existing finding changes severity. The `except Exception: continue` branch at
`core/config_auditor.py:579` is made **visible** but is **not** promoted to WARN —
alerting severity is major-impact under the gate and is not mine to change.
**FALSIFIER:** any new WARN/CRITICAL appears in a group-F run against the live config.

### P-6 — the gate
Full differential run, `pytest tests/unit tests/integration`, base `742d9da` vs the NI-5
commit. Base and head are **both green**; head's total rises by exactly the NI-5 tests
added; **no test that passed at base fails at head**.
**FALSIFIER:** any base-green test goes red at head.

---

## WHAT THIS BUILD MUST NOT DO

⛔ Not touch `max_multiplier` (stays 2.0) · ⛔ not touch the `raw_qty * 2` ceiling ·
⛔ not touch NI-16 · ⛔ not delete any legitimate programming default · ⛔ not push ·
⛔ not deploy · ⛔ not edit `main.py`.

---

## SCORING

To be completed **after** the gate, in `docs/audit/`. Each prediction gets
CORRECT / WRONG / PARTIAL with the measurement that decided it.

---

# SCORED — 23-Aug-2026, after the gate

**Commit:** `a4a5cef` on `fix/ni5-policy-defaults-23aug` (base `742d9da`), 12 files,
+328 / −20. ⛔ NOT PUSHED. ⛔ NOT DEPLOYED.

| # | verdict | the measurement that decided it |
|---|---|---|
| **P-1** scope | ✅ **CORRECT** | production side is exactly `capital/position_sizer.py` + `core/config_auditor.py`; the other 10 files are tests. `git diff --name-only \| grep -v '^tests/'` returns those two and nothing else |
| **P-2** production safe | ✅ **CORRECT** | `main.py` is not in the diff. Its sole site `main.py:2501` already passed all three from `ps_cfg` |
| **P-3** auditor blindness | ✅ **CORRECT — all three arms** | **(i)** probe printed `PositionSizer row emitted? -> False` — no finding of any severity. **(ii)** `VERDICT: PASS`, `code='F_ok'`, message *"component defaults match config intent (position-value cap + daily-loss pct)"* — naming a cap it had not checked. **(iii)** `test_diverging_position_cap_default_warns` **FAILED** (`assert False`), having **PASSED at base** minutes earlier |
| **P-4** after the fix | ✅ **CORRECT** | the row is now `F_PositionSizer_max_position_value_pct_required` with `outcome='required'`; summary reads *"component defaults match config intent (FundManager.daily_loss_limit_pct)"* — names only what it compared |
| **P-5** no severity escalation | ✅ **CORRECT** | group F against the live config: verdict `PASS`, zero WARN, zero BLOCK. The `except` branch is now visible but stayed at PASS |
| **P-6** the gate | ⚠️ **PARTIAL — the operative half CORRECT, the wording WRONG** | see below |

## 🔴 P-6, stated honestly

**What I got wrong:** I wrote *"base and head are both green"*. They are **not green** —
**10 failures on each side**. I wrote that before establishing the campaign's recorded
baseline, which is a **standing set of 7 failures**. ⛔ The word "green" was never
achievable and should not have been in a frozen prediction.

**What held — and it is the falsifier that mattered:** *"no test that passed at base
fails at head."* ✅

| | base `742d9da` | head `a4a5cef` |
|---|---|---|
| result | **10 failed · 5,748 passed · 4 skipped** (944.89 s) | **10 failed · 5,772 passed · 4 skipped** (976.55 s) |
| collected | 5,762 | 5,786 |

- **Failure sets are IDENTICAL** — `diff` of the two sorted `FAILED` lists is **empty**.
  ⭐ **SET-compared, ⛔ not count-compared.**
- **+24 passes decomposes exactly:** 22 (the new `test_ni5_…` file) + 2 (group F, 3 → 5).
  Collection rose by the same 24. ⛔ Nothing unexplained.
- **Skips unchanged** at 4.

## ⚠️ DISCLOSED — my harness does NOT reproduce the recorded baseline, and why

The recorded gate for `742d9da` is **`7F / 5,751P / 4S`**. Mine reads **`10F / 5,748P /
4S`**. The gap is **exactly 3**, and it is **environmental, ⛔ not a defect in `742d9da`
and ⛔ not caused by NI-5**:

- the 7 recorded standing failures are all present and unchanged —
  `test_closure_source_contract` ×1 · `test_fix181` ×1 · `test_main` ×4 ·
  `test_phase17_batch2` ×1;
- the extra 3 are all in `tests/unit/test_t4_deploy_preflight.py`
  (`test_ist_now_emits_valid_ist`, `test_check_tz_fails_on_broken_utc_form`,
  `test_check_tz_passes_on_agreement`);
- **cause, measured:** `D:/Projects/trading-system/venv/` is **EMPTY** and no sibling
  worktree has one, so `scripts/ist_now.sh`'s `pick_python()` falls past
  `$REPO_ROOT/venv/Scripts/python.exe` all the way to `command -v python3` — the
  **WindowsApps stub** (*"Python was not found… App execution aliases"*, rc 49/2);
- **control, both directions, both trees** (the test file and `ist_now.sh` are
  **byte-identical** across them — md5 `1e4eaad9…` and `4f8e1d4a…`):
  **without** `PYTHON` → `3 failed / 6 passed`; **with** `PYTHON=/c/python311/python` →
  **`9 passed`**, on the base tree *and* the head tree.
- ⚠️ A PATH shim for `python3` is **NOT** sufficient — measured, still failed.
  `pick_python()` honours `$PYTHON` first; that is the working lever.

⇒ with `PYTHON` set the base would read **`7F / 5,751P / 4S`** — the recorded baseline
exactly. ⭐ The harness is sound once this one deviation is named; ⛔ but a raw run on
this PC today reads **10F**, and calling that "the baseline" without this paragraph would
be wrong.
