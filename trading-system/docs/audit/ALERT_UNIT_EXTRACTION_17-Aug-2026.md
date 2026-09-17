# ALERT UNIT — EXTRACTION RECORD (17-Aug-2026)

**Status: BUILT. ⛔ NOT DEPLOYED. ⛔ NOT VERIFIED LIVE. ⛔ NOT PUSHED.**
Authority: Rama authorised Option (A) — extract the alert phases onto current
`origin/main`, leaving `071169b` and `bfd6b5f` exactly where they are.

---

## 1. What was built

| | |
|---|---|
| Base | `origin/main` = **`6fa8a1c`**, measured 17-Aug 10:47 IST |
| New branch | `fix/alert-phases-0-1-2` |
| New HEAD | **`f62db55`** |
| Worktree | `D:\Projects\trading-system-alertunit` (throwaway) |

**Old → new map**

| Phase | Original | Cherry-picked to |
|---|---|---|
| PHASE 0 — the alert delivery contract | `a41422b` | **`58035bf`** |
| PHASE 1 — feed-death / SOFT_KILL / EOD-deferred | `bfd6b5f` | **`37336bc`** |
| PHASE 2 — watcher Telegram fallback | `071169b` | **`f62db55`** |

All three applied **rc=0, no conflicts**.

---

## 2. Why `071169b` was NOT deployable as-is

`fix/alert-phase2-watcher` at `071169b` is 32 commits, of which 5 touch code —
and one is **`c39e799`, the F6 delivery rewrite (+1,864 lines)**, recorded as
**AUTHORISED 08-Aug · NO-GO 10-Aug** (gates 3 and 6 failed). Pushing the branch
would have shipped a refused delivery rewrite under an alerts label.

📌 Fifth instance of the name-vs-content trap, and the first where the hidden
payload is something **explicitly refused** rather than merely extra.

---

## 3. Deliberate exclusions

| Commit | What it is | Why excluded |
|---|---|---|
| `c39e799` | F6 delivery rewrite (+1,864) | **NO-GO.** Never to be pushed |
| `4f91784` | `capital/risk_engine.py` | Comment-only — **verified**: 10 added lines, all `#`, inside `RiskEngine`. Introduces no symbol |
| **`9fdfe41`** | WSL-stub gate guard in `tests/conftest.py` | See §4 — excluded, with an inherited risk |

⚠️ **SHA CORRECTION.** The resumption card names this commit **`9fd7e41`**. That
object **does not exist** — `git rev-parse 9fd7e41` returns *"Needed a single
revision"*. The real SHA is **`9fdfe41`**. Any future card must carry `9fdfe41`.

---

## 4. 🔴 THE INHERITED RISK — `9fdfe41` IS LEFT OUT, AND SOMETHING IS LOST WITH IT

`9fdfe41` adds a `pytest_configure` hook to `tests/conftest.py` that **refuses to
run** when `bash` resolves to the WSL app-execution alias under `WindowsApps` — a
stub, not a shell. Measured on 08-Aug: the same command, same tree, same minute
reported **29 failures from PowerShell and 9 from Git Bash**. Two test families
shell out to `bash`; against the stub they assert on WSL's own UTF-16LE error
text. Escape hatch: `TS_ALLOW_UNSUPPORTED_SHELL=1`.

**Leaving it out is safe for THIS unit, for two measured reasons — not one:**

1. The guard supplies **no fixture and no symbol**. It only *refuses*. Nothing in
   the alert unit's 911 added lines references `conftest` (grep count 0). So its
   absence cannot change any alert test's result.
2. In this session `bash` resolves to `/usr/bin/bash` (Git Bash) **first** —
   measured via `which -a bash`; the WindowsApps stub is 4th on PATH. The guard
   would not have fired even if present.

**⛔ WHAT IS INHERITED.** The unit ships a `tests/conftest.py` with **no launcher
guard**. The gate's fail-closed property currently rests on a *standing human
rule* — "run the gate from Git Bash" — and not on anything in the tree.

> ⚠️ **A future session on a different shell inherits an unguarded gate.** The
> dangerous direction is not the one that was hit. On 08-Aug the stub *added* 20
> phantom failures, which is loud. The same mechanism can just as easily
> **swallow a real regression** inside a larger "known failures" set, where a
> count-compare would never show it.

**PENDING:** `9fdfe41`'s conftest guard should be re-landed as its own small
unit, independent of F6. It is not part of this unit and was not gated with it.

---

## 5. Proof the extraction is complete and nothing rode along

**(a) File set — exactly 9, nothing more.**
`git diff --name-only 6fa8a1c f62db55` returns exactly:

```
alerts/delivery.py                          data/live_feed.py
capital/kill_switch.py                      main.py
orders/order_placer.py                      scripts/alert_watcher.py
tests/unit/test_alert_delivery_contract.py  tests/unit/test_alert_delivery_phase1.py
tests/unit/test_alert_delivery_phase2.py
```

`diff` against the independently-derived alert-9 list is **empty**.

**(b) Patch content — byte-identical, not merely same-named.**

| | |
|---|---|
| `git diff f963438 071169b` (original union) | 53,290 B · md5 `cc12e920f725308c2ddc8c73b1af40eb` |
| `git diff 6fa8a1c f62db55` (extracted unit) | 53,290 B · md5 `cc12e920f725308c2ddc8c73b1af40eb` |

⭐ This is the stronger claim and the reason it was measured. A name-only check
cannot detect a dropped hunk or context drift during a cross-history
cherry-pick; byte-identity can. **It was needed:** `6fa8a1c` is **NOT an
ancestor** of `071169b` (merge-base `645728d`), so this was a genuine
cherry-pick across diverged history, not a replay of a contiguous range.

**(c) No collision with what main did meanwhile.** Main changed **40 files**
since the fork at `645728d`. Intersection with the alert 9 = **ZERO**
(`comm -12` empty). This is why all three picks applied without conflict.

---

## 6. 🔴 DEPENDENCY CLOSURE — the check that decides whether this is a unit at all

⭐ Zero *file* intersection does **not** prove zero *semantic* dependency, and
this was answered by reading the code, **not** by "it compiled".

**F6 introduces 13 new symbols** in the modules the alert code imports:

```
core/state_store.py     clean_gtt_states_for_trade · count_observed_gtt_exits
                        get_reconcilable_gtt_states · get_reservation_id_for_trade
                        mark_gtt_state_triggered
capital/fund_manager.py _resolve_release_reservation_id
orders/cnc_gtt_monitor.py  _MAX_OBSERVED_EXITS · _STRANDED_RELEASE_CYCLES
                        _exit_observed_no_recreate · _exit_observed_repeatedly
                        _has_actionable_gtt_row · _release_stranded_delivery_trades
                        _release_stranded_trade
```

Cross-grepped against **all 911 added lines** of the extracted unit:

- **F6 symbol hits: 0** (all 13, individually counted)
- References to `state_store` / `fund_manager` / `cnc_gtt_monitor` /
  `order_reconciler` / `risk_engine` / `conftest`: **0 each**

**The one genuine cross-file dependency, which a file-level check would have
missed entirely:** `tests/unit/test_alert_delivery_phase2.py` imports
`_make_cfg`, `_null_log`, `_write_sentinel` from
**`tests/unit/test_alert_watcher.py`** — a file that is **not among the 9**.

Resolved safely, and by blob identity rather than by presence alone:

| | |
|---|---|
| Present in base `6fa8a1c` | **YES**, all three helpers defined |
| blob at `6fa8a1c` | `48522b301e0a53801f248034c567d22bc1297532` |
| blob at `071169b` | `48522b301e0a53801f248034c567d22bc1297532` |

**Byte-identical ⇒ the helper import is satisfied by the base**, with no
contribution from any excluded commit.

**VERDICT: dependency closure CLEAN. The extraction is VIABLE.**

---

## 7. THE GATE — result

**Run at the FRESHLY MEASURED `origin/main` = `6fa8a1c`.** ⛔ Friday's `1c8c710`
is **not** the comparand; installs ③ and ④ landed since.

| | BASELINE `6fa8a1c` | UNIT `f62db55` |
|---|---|---|
| **RAW_PYTEST_RC** (from pytest itself) | **1** | **1** |
| collected | 5,604 | 5,640 |
| failed | **7** | **7** |
| passed | 5,593 | 5,629 |

📌 **The rc is read from pytest directly** — the command redirects to a FILE, so
`$?` is pytest's own code. ⛔ `| tail -N; echo $?` captures `tail`'s exit code and
produced a false `RAW_PYTEST_RC=0` once already.

**`comm` BOTH directions. ⛔ "set-identical" is not used:**

- **NEW failures (UNIT only): 0** ← the regression question
- **disappeared (BASELINE only): 0**
- **common to both: 7**, and **7/7 with IDENTICAL failure messages**.
  ⭐ This second check matters: **four of the seven are in `test_main.py`, which
  this unit MODIFIES.** Same test ID failing on both sides does not prove the same
  cause; the messages do. All four are pre-existing at `6fa8a1c`, a tree that
  contains no unit code.

**The 7 surviving failures, each named:** `test_closure_source_contract::
test_no_module_restates_the_vocabulary_literals` · `test_fix181::
test_inflight_orphan_flattened_when_kill_active` · `test_main::
test_paper_mode_does_not_require_webhook_secret` · `test_main::TestContinueFromGate`
×3 (`release`, `place`, `stats_placed`) · `test_phase17_batch2::
test_fix077_flask_max_content_length`.

⭐ The documented flapper `test_instance_lock::test_p2_restart_after_crash_is_not_blocked`
did **NOT** appear in either run — nothing needed excusing on those grounds.

**NON-VACUITY, proven ⛔ not asserted:** collected **5,604 → 5,640 = +36**, and the
three files *named after the thing changed* contribute exactly **14 + 11 + 11 = 36**,
**all passing**, **0 collected in baseline**. The delta is explained by the unit's
own tests and the arithmetic closes exactly.

> **VERDICT: full clean-worktree regression completed; RAW_PYTEST_RC=1; NO NEW
> FAILURES — 7 known failures remain; 0 did not reproduce; all failures
> independently attributed; no alerts-unit-specific failure found.**

## 7a. 🔴 TWO ENVIRONMENTAL FAULTS — DIAGNOSED, ⛔ NOT LABELLED "PC-ENV"

**The FIRST run reported 37 failures, not 7.** ⛔ That was not accepted as
"environmental" on assertion. Both causes were proven by experiment, and the
gate was **re-run from scratch** with both repaired. 📌 *"PC-env" is a label, not
a diagnosis.*

**FAULT 1 — `config/instruments.csv` is GITIGNORED (`.gitignore:39`), so a FRESH
WORKTREE NEVER HAS IT.** Its absence trips `main.py:2160`'s BL-20 guard
`assert instrument_cache is not None` (line number measured at `6fa8a1c`).
⭐ **PROVEN by planting it:** `test_main.py` went **30F/51P → 4F/77P**. That is
**26 of the 37**. This is why the 09-Aug alert worktree had this file "staged"
manually — an untracked prerequisite that no `git worktree add` reproduces.

**FAULT 2 — `python3` resolves to the WindowsApps app-execution alias**, and
`C:\python311` ships **no `python3.exe`**. So `scripts/ist_now.sh` and
`check_tz.sh` never run and the tests assert against the stub's *"Python was not
found…"* text. ⭐ **PROVEN with a shim:** the scripts then execute correctly.

> 🔴🔴 **FAULT 2 WIDENS §4's INHERITED RISK, and this is the session's sharpest
> finding about the excluded commit.** `9fdfe41`'s conftest guard refuses to run
> when **`bash`** is a WindowsApps stub. **The identical failure mode exists for
> `python3`, and that guard DOES NOT COVER IT** — this gate hit it today, on a
> machine where `bash` itself resolves correctly to Git Bash and the guard would
> have passed the launcher as fine.
>
> ⇒ **PENDING, and now stronger than when §4 was written:** re-land `9fdfe41` as
> its own unit **WIDENED to `python3`**, ⛔ not merely restored as-is. A launcher
> guard that checks one interpreter and not the other gives the *appearance* of a
> fail-closed gate while the same 20-to-30-failure distortion walks straight past
> it.

⚠️ **Both faults were IDENTICAL on both sides, so they cancelled in the delta —
run 1 also showed 0 new / 0 disappeared.** ⛔ But a delta measured in a knowingly
broken environment is a weaker claim, which is why the gate was re-run rather
than explained away.

## 7b. Gate environment — recorded, because it is not the VM's

⚠️ `D:\Projects\trading-system\venv\` **exists but is completely empty** — the
invisible-damage failure mode. There is no working venv in any worktree.

The gate therefore ran on **system Python 3.11.9** (`C:\python311`), pytest
9.0.3, no plugins, no pytest config ⇒ deterministic collection order.

⭐ **A third hazard, confirmed by the repo's own guard script:** `check_tz.sh`
reports **`TZ='Asia/Kolkata'` is UNRELIABLE in this shell** — MSYS2 carries no
zoneinfo and silently falls back to **UTC**, so `TZ=Asia/Kolkata date` on this PC
reads **5h30m wrong**. The authoritative reading is `now_ist()`, which agrees with
the VM. ⛔ **Never use `TZ='Asia/Kolkata' date` on this PC**; plain `date` (local)
tracks VM IST.

- ⚠️ **The VM runs Python 3.12** (`/home/ubuntu/systems/venv/lib/python3.12`).
  This is a **parity gap**: a local green does not speak for 3.12 behaviour.
- ⭐ The *delta* remains valid regardless: baseline and unit ran in the **same**
  interpreter and the same environment, so environment drift cancels between
  them. What is claimed is the delta, not an absolute pass.
- Safety: the throwaway worktrees contain **no `.env`** and none exists up-tree.
  Every `load_dotenv` site is in `tests/crash_test/`, which is **outside** the
  `tests/unit tests/integration` gate scope. `pytz` is absent from the
  interpreter but imported nowhere in the tree and pinned in no requirements
  file, so its absence is inert.

---

## 8. Prohibitions still standing

- ⛔ Never push `071169b`, `bfd6b5f`, or `c39e799`. **F6 stays NO-GO.**
- ⛔ Nothing pushes before install ③ is scored at the 16:22 window.
- ⛔ `trading-system-p2` was **not mutated** — re-measured clean, HEAD `071169b`.
- ⛔ Local `main` `7290a08` is not the base and is merged into nothing.
