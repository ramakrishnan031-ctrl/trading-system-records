# PREDICTION — N9-07, FORWARD-SHADOW ENCODING (extraction, HELD)

**Frozen 18-Aug-2026 (evening, IST), BEFORE any push.** Unit:
`d8969687306ad9fe37a7e99b606e9a3902d88c72` on `fix/n907-extract-18aug`, parent
`08b462ba175d904e8723ed34a13c956f0dd33679` (== `origin/main` at freeze time),
worktree `D:\Projects\trading-system-n907`.

> ## 🔑 **THIS UNIT HAS NO PRESENCE SIGNATURE, AND THAT IS A MEASURED CONCLUSION — ⛔ NOT AN OVERSIGHT.**
> It is **LATENT HARDENING**. Its outcome tomorrow is **`NOT TESTED` BY CONSTRUCTION**,
> ⛔ not by accident, ⛔ and not by a window that failed to arrive.

---

## §A — WHAT IS BEING INSTALLED, AND WHAT IT IS NOT

**Two characters of behaviour.** `scripts/forward_shadow_record.py`, two calls:
`read_text()` → `read_text(encoding="utf-8")` — the weights read (`_weights`) and
the token read (`_build_kite`). Plus a new 145-line test file. **+154 / −2, two files.**

⛔ **IT IS NOT** a fix to what the job writes · not a schema, config or capital change ·
not a service change (the job is **cron**, 18:15 Mon–Fri, and does not need the
trading service) · ⛔ **not the branch it came from** (see §F).

## §B — 🔑 THE PRESENCE SIGNATURE: THERE ISN'T ONE, AND HERE IS THE PROOF

A presence signature must be an artifact that **could not exist before the change**.
This unit can produce none, because **the code path it protects already succeeds**.

**MEASURED ON THE VM, 18-Aug evening, read-only:**

| Fact | Measurement |
|---|---|
| The job's history | **26 runs, 26 SUCCESS**, `2026-07-13` → `2026-08-18` (whole `cron_heartbeat`) — including tonight `18:16`, `wrote=5917 sim=5546` |
| The premise's file | `config/scoring_weights.yaml` carries **exactly 51 non-ASCII bytes** — ⭐ the commit's claim is **correct** |
| Locale vars | ⛔ **none** in the crontab, ⛔ none in `.env` |
| The unpatched read, in the real cron env (`env -i`) | **SUCCEEDS** |

⇒ ⛔ **Any behavioural signature would be VACUOUS.** "The job succeeds" was true
**26/26 times before this change**. That is the `V5` tautological-check class:
⛔ a check with no failing input manufactures confidence.

⭐ **THE HONEST SIGNATURE IS FILE IDENTITY ONLY** — md5 of the deployed
`scripts/forward_shadow_record.py` == the ref's blob (Gate E1). ⛔ **That is a
DEPLOYMENT fact, ⛔ NOT a presence fact**, and it is not written as one.

## §C — 🔑 WHY IT NEVER FIRED: THE COMMIT'S STATED MECHANISM IS WRONG ON THIS VM

The commit says *"a cron environment with LANG unset resolves the platform default
to ASCII"*. ⛔ **That is false here, and the real reason is better.**

⭐ **PEP 540: CPython enables UTF-8 Mode BY DEFAULT when `LC_CTYPE` is `C` or
`POSIX`.** Cron sets no `LANG`, so the locale **is** C ⇒ UTF-8 Mode is on and the
locale never governs. ⛔ **Not** an env var — the probe ran under `env -i`, with **no
variables at all**, and still measured `sys.flags.utf8_mode = 1`. ⛔ Not `pyvenv.cfg`
(plain venv, `home=/usr/bin`, no directives) · ⛔ not a build flag · ⛔ not a wrapper
(`bin/python` is a symlink) · Python **3.12.3** (⛔ PEP 686's default-on lands only in
3.15+).

⭐ **AND THERE IS A SECOND, INDEPENDENT PROTECTION:** PEP 538 C-locale coercion
(C → C.UTF-8), available because `C.utf8` **is installed**.

**THE REACHABILITY BOUNDARY, MEASURED — both must be deliberately disabled:**

| environment | `utf8_mode` | encoding | read |
|---|---|---|---|
| `LANG=C` | 1 | utf-8 | OK |
| `PYTHONUTF8=0 LANG=C` | 0 | UTF-8 | OK |
| `PYTHONCOERCECLOCALE=0 LANG=C` | 1 | utf-8 | OK |
| **`PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LANG=C`** | 0 | **ANSI_X3.4-1968** | 🔴 **UnicodeDecodeError** |

⭐ `locale -a` = **C · C.utf8 · POSIX · en_US.utf8** — ⛔ **no non-UTF-8 locale is
installed**, so no locale choice alone can reach the bug.

🔑 **CONSEQUENCE, AND IT INVERTS THE WORRY:** the protection is **interpreter
behaviour**, ⛔ not a config line — a venv rebuild REPRODUCES it, and a service-file
edit cannot drop it. It disappears only under a **deliberate double-override**.
⭐ **The code is right for a reason its author did not name.** ⛔ The commit is NOT
rewritten; the correction is recorded in the register.

## §D — FALSIFIERS

| id | fires if | measured by |
|---|---|---|
| **P1** | after any push, `origin/main` ≠ `d8969687…` on either independent measure | VM bare `rev-parse` + PC `ls-remote` |
| **P2** | either changed file differs PC vs VM by md5 | PC side from the **ref's blobs** |
| **P3** | the VM deployed tree shows tracked drift vs the new HEAD | `GIT_INDEX_FILE` temp-index method |
| **P4** | 🔑 the **first 18:15 run after install** does not write a `cron_heartbeat` row, or writes `status != SUCCESS` | `cron_heartbeat`, `job_name LIKE '%forward_shadow%'` |
| **P5** | 🔴 that run's `wrote=` / `sim=` counts move in a way market data cannot explain | the `message` column, against the 26-run history |
| **P6** | ⛔ any behavioural artifact is claimed as proof this code is LOADED | ⇒ **§B was violated** |

⛔ **P4 and P5 are the ONLY post-deploy falsifiers, and BOTH are checks that nothing
CHANGED.** ⭐ There is no falsifier that can CONFIRM the code is running, and §B says
why.

## §E — THE CEILING, STATED IN ADVANCE

⭐ The highest status this unit can reach on the day after any install is
**`DEPLOYED`** — file identity plus an unchanged job. ⛔ **`VERIFIED LIVE` IS
UNREACHABLE FOR IT**, and ⛔ must not be written: reaching it needs the encoding path
to be **exercised in anger**, which requires the double-override of §C that no one
should perform on a live box.

⛔ **A day the 18:15 job does not run scores `NOT TESTED`.** ⭐ So does a day it runs
and succeeds — because it also succeeded 26 times before.

## §F — WHAT THIS UNIT IS **NOT**: THE BRANCH IT CAME FROM

🔴 `fix/n907-forward-shadow-encoding` (`7649cd8`) sat **30 commits** ahead of
`origin/main` and was **CONTAMINATED**:

- 🔴 **`c39e799` — the REFUSED F6**, +1,864 lines across `capital/fund_manager.py`,
  `core/state_store.py`, `orders/cnc_gtt_monitor.py`, `orders/order_reconciler.py`.
  **F6 is NO-GO.**
- 🔴 **`4f91784`** — named `docs(risk):`, **edits `capital/risk_engine.py`** (+10).
  The **seventh** name-vs-content instance; the **third** branch carrying F6.
- ⚠️ `9fdfe41` — named `fix(tests)`, also edits `tests/conftest.py` (+59).

⭐ **ONLY `7649cd8` WAS EXTRACTED**, onto `08b462b`. ⛔ **The branch was NOT rebased** —
that would have dragged F6 across. **VERIFIED ON THE EXTRACTION:** `c39e799` is ⛔ **not
an ancestor**, and `fund_manager.py` · `state_store.py` · `cnc_gtt_monitor.py` ·
`order_reconciler.py` · `risk_engine.py` · `conftest.py` are all **unchanged vs
`origin/main`**. The contaminated branch ref is preserved untouched.

## §G — THE GATE

**Full regression, SAME worktree, SAME command, BOTH SIDES.**

| | failures | passed | skipped | rc |
|---|---|---|---|---|
| base `08b462b` | **10** | 5,643 | 4 | **1** |
| unit `d896968` | **10** | **5,651** | 4 | **1** |

⭐ **THE FAILURE SETS ARE IDENTICAL — compared as SETS with `comm`, ⛔ not by eye:
`comm -23` (new failures) is EMPTY.** ⇒ **ZERO NEW FAILURES.**
⭐ **NON-VACUITY: 5,643 → 5,651 = +8 = EXACTLY the 8 tests in
`tests/unit/test_n907_forward_shadow_encoding.py`.**

⚠️ **The 10 are PRE-EXISTING at the base and are named, ⛔ not waved past:**
`test_closure_source_contract` (1) · `test_fix181` (1) · `test_main` (4) ·
`test_phase17_batch2` (1) · `test_t4_deploy_preflight` (3, all TZ). ⚠️ This worktree
lacks the gitignored `instruments.csv`, a known phantom-fail source — ⛔ which is
**exactly why the baseline was run**, and why "they look unrelated" was not accepted
as attribution.

## §H — 🔴 WHY IT IS HELD, AND THE REASON IS NOT ATTRIBUTION

🔑 **`scripts/forward_shadow_record.py` IS GATE A1's OWN INSTRUMENT** — the row-count
check that gates every future deploy, **including tiers**.

⛔ **YOU DO NOT CHANGE THE MEASURING INSTRUMENT ON THE NIGHT BEFORE YOU RUN AN
EXPERIMENT WITH IT.** Tomorrow's A1 reading has to be trustworthy on **unchanged**
code, and tiers still needs A1 to gate it. ⭐ **That holds the push on its own,
independently of §B's missing signature.**

⭐ **PREDICTED EFFECT ON A1's BASELINE WHEN IT DOES SHIP: NONE.** The change alters
only *how two files are read*, ⛔ not what is written — no row, column or count is
touched, and both reads already succeed (§C). Tonight's unpatched run wrote
**5,917 / sim 5,546**; the first run after install should be governed by market data
alone. **That is P5's whole content.**

## §I — WHAT THIS PREDICTION DOES NOT CLAIM

⛔ It does not claim the change is unnecessary — the file really does carry 51
non-ASCII bytes, and explicit encoding is correct. ⛔ It does not claim the bug can
never occur — §C names the exact double-override that reaches it. ⛔ It does not claim
anything about the 29 commits left behind. ⛔ It makes no claim about tiers
(`7d1fd4e`), which is separately gated and did not go tonight.

<!-- FROZEN-BOUNDARY — everything ABOVE this line is FROZEN. ⛔ No edit above it, especially if a call turns out wrong. Addenda go BELOW, appended only, each with its own timestamp. -->

## ADDENDA (append-only, below the boundary)
