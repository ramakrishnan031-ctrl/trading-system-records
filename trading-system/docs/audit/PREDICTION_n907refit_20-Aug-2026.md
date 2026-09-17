# PREDICTION — n907 REFIT onto `7fc5d5a` · `4568385`

**Frozen 20-Aug-2026 (evening, IST), BEFORE any push.**

| | |
|---|---|
| **UNIT** | `45683859a0a05f466189ac5bc98f9a9f089f98d3` |
| **BASE** | `7fc5d5a9d063c9fba3622c5ced2c6ba1c87d65d7` (= `origin/main`, the capital-drift comparator, pushed 19:34:17) |
| **SUPERSEDES** | `docs/audit/PREDICTION_n907_19-Aug-2026.md` (for `d896968`, base `08b462b`) |
| **SCOPE** | `scripts/forward_shadow_record.py` (M) · `tests/unit/test_n907_forward_shadow_encoding.py` (A) — 2 files, +154 / −2 |

⛔ **THE OLD PREDICTION IS NOT EDITED.** It is superseded, not amended: it remains a true
record of `d896968` against `08b462b`, and its frozen md5
`679a4f460d2fa86cea69a1e2df5b50cd` (selector `sed -n '1,168p'`) must stay verifiable.

---

## §A — WHY THIS FILE EXISTS AT ALL

`origin/main` moved from `08b462b` to `7fc5d5a` at 19:34:17. **A gate result does not carry
across a SHA change**, so `d896968`'s gates died with the base. This unit is the same change
replayed onto the new base, and it gets its own prediction because the old one names a base
that is no longer current.

⭐ **THE CHANGE ITSELF IS PROVEN IDENTICAL TO `d896968`'s, five ways** — file list + stat ·
`range-diff` `1: d896968 = 1: 4568385` · index-stripped net-diff md5
`7e3f8f5aa2b180f1238a6a153d67c180` both sides · `patch-id --stable`
`977ab7bb667a486b080a2964636f0fd43de7ef17` both sides · resulting blobs byte-identical
(`a1c3c1434da6…` / `2732149442f9…`). ⭐⭐ The middle two **reproduce exactly the values
`N20-02` banked for the original extraction.**

**Two characters of behaviour**, unchanged from the original: `read_text()` →
`read_text(encoding="utf-8")` at the weights read (`_weights`) and the token read
(`_build_kite`), plus a 145-line test file.

⛔ **IT IS NOT** a fix to what the job writes · not a schema, config or capital change ·
**not a service change** — the job is **cron** (`15 18 * * 1-5`, `critical: false`) and does
**not** need the trading service.

---

## §B — 🔑 THE PRESENCE SIGNATURE: THERE STILL ISN'T ONE

Carried forward from the superseded prediction because it is unchanged by the rebase, and
**re-measured against the new SHA**:

| Fact | Measurement |
|---|---|
| Boot-path references | `main.py` **0** · `capital/kill_switch.py` **0** · `scripts/system_manager.py` **0** |
| Non-script/test mentions | **4, ALL COMMENTS** (`core/config_loader.py:64,76`; `v3_chain/forward_shadow.py:2,12`) |
| Positive control | the same grep **does** fire inside `scripts/forward_shadow_record.py:18` ⇒ the zeros are findings |
| Invocation | cron only — *"records only; no orders, no config change, off the hot path"* |

⇒ ⛔ **Any behavioural signature would be VACUOUS.** The code path it protects **already
succeeds** (see §C). ⭐ **The honest signature is FILE IDENTITY ONLY** — md5 of the deployed
`scripts/forward_shadow_record.py` == the ref's blob. ⛔ **That is a DEPLOYMENT fact, ⛔ NOT
a presence fact**, and it is not written as one.

---

## §C — WHY IT NEVER FIRED (unchanged, and still true)

**PEP 540: CPython enables UTF-8 Mode BY DEFAULT when `LC_CTYPE` is `C` or `POSIX`.** Cron
sets no `LANG`, so UTF-8 Mode is on and the locale never governs. A second, independent
protection is PEP 538 C-locale coercion, available because `C.utf8` is installed.
`locale -a` = C · C.utf8 · POSIX · en_US.utf8 ⇒ ⛔ **no non-UTF-8 locale is installed**, so no
locale choice alone can reach the bug. It disappears only under a **deliberate double
override** (`PYTHONUTF8=0 PYTHONCOERCECLOCALE=0`), which ⛔ **must never be run on a live box.**

---

## §D — FALSIFIERS

| id | fires if | measured by |
|---|---|---|
| **P1** | after any push, `origin/main` ≠ `4568385…` on either independent measure | VM bare `refs/heads/main` + PC `git ls-remote` |
| **P2** | either changed file differs PC vs VM by md5 | PC side from the **ref's blobs**, ⛔ never the working tree |
| **P3** | the VM deployed tree shows tracked drift vs the new HEAD | `GIT_INDEX_FILE` temp-index method **with `update-index --refresh`** between `read-tree` and `diff-files` — ⛔ the uncorrected form reports 1,309 phantom files |
| **P4** | 🔑 the **first 18:15 run after install** writes no `cron_heartbeat` row, or `status != SUCCESS` | `cron_heartbeat`, `job_name = 'forward_shadow_record'` |
| **P5** | 🔴 that run's `wrote=` / `sim=` move in a way market data cannot explain | the `message` column, **compared against the frozen baseline below** |
| **P6** | ⛔ any behavioural artifact is claimed as proof this code is LOADED | ⇒ **§B was violated** |
| **P7** | the post-receive hook restarts `trading-system`, `alert-watcher`, `gui-dashboard` or `token-watcher` | `MainPID` + `NRestarts` vs a before-image captured **before** the push |

⛔ **P4 and P5 are the ONLY post-deploy falsifiers, and BOTH are checks that nothing
CHANGED.** ⭐ There is no falsifier that can CONFIRM the code is running — §B says why.

### 🧊 THE FROZEN BASELINE FOR P5 — banked BEFORE this unit can ship

> **20-Aug-2026 pre-deploy baseline: `wrote=4750`, `sim=4344`**
> (scheduled run OBSERVED at `2026-08-20T18:16:37.769455 | SUCCESS`; ⛔ never invoked by hand)

⭐ **THAT READING IS STILL VALID ACROSS THE BASE MOVE, AND IT WAS MEASURED, ⛔ NOT ASSUMED:**
`scripts/forward_shadow_record.py` is **byte-identical at `08b462b` and `7fc5d5a`**
(`c8354274ab4f8630da8f0affd19fb18b`), the 18:16:37 run preceded the 19:34:17 comparator push,
and **this unit changes that file** (`a1c3c1434da6…`) — so the reading is a genuine pre-image
of exactly the file being changed.

🔴 **Tomorrow's first post-deploy 18:15 run is a BEFORE/AFTER COMPARISON against 4,750 —
⛔ NEVER a new baseline.** Prior comparands: 19-Aug 4,265/3,744 · 18-Aug 5,917/5,546 ·
17-Aug 5,962/5,679 · 14-Aug 5,567/5,294 · **10-Aug `EMPTY_NO_DATA` 0** (the `status=SUCCESS`
trap, with a real instance).

---

## §E — THE CEILING, STATED IN ADVANCE

🏷️ **`DEPLOYED` is the most this unit can reach tonight. ⛔ `VERIFIED LIVE` is UNREACHABLE**
without the deliberate `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0` double-override, which ⛔ must
never be run on a live box. The service is **down** and stays down; **first execution is
tomorrow's 08:15 boot**, and P4/P5 only become scorable at tomorrow's 18:15.

⛔ **Score by SIGNATURE, never narrative.**

---

## §F — THE GATE (full, differential, fresh worktrees, 20-Aug evening)

Both sides run with `pytest tests/unit tests/integration`, raw rc captured **into a variable,
⛔ never through a pipe**; both worktrees provisioned with the gitignored
`config/instruments.csv` (2,229 lines) and a `python3` shim.

| | rc | result | elapsed | tree fingerprint |
|---|---|---|---|---|
| **BASE `7fc5d5a`** | 1 | **7 failed / 5,657 passed / 4 skipped** | 966.27 s | IDENTICAL |
| **CANDIDATE `4568385`** | 1 | **7 failed / 5,665 passed / 4 skipped** | 892.05 s | IDENTICAL |

**DIFFERENTIAL, ID-LEVEL, TWO-WAY `comm`:** `comm -13` = **0 NEW** · `comm -23` = **0
disappeared** · intersection **7**.
⛔ **ID-level only, per `N20-19`:** the `run_gate.sh` message-equality assertion is **vacuous**
(`failmsgs` is `failids` + the 7-char `FAILED ` prefix, and pytest emits no reason suffix for
these), so **no `failmsgs` artefact was produced at all** — nothing later can mistake it for
independent evidence.

⭐ **NON-VACUOUS: 5,657 → 5,665 = +8 = EXACTLY the 8 test functions in
`test_n907_forward_shadow_encoding.py`**, which is **absent at base** (`git cat-file -e` fails)
and whose targeted run is **8 passed**.
⚠️ The 7 are **PRE-EXISTING and NAMED**, and match the recorded baseline name-for-name:
`test_closure_source_contract` 1 · `test_fix181` 1 · `test_main` 4 · `test_phase17_batch2` 1.

🏷️ **WORDING, per the binding rule `N12-16`:**
> *"full clean-worktree regression completed; rc=1; all failures independently attributed;
> no n907-refit-specific failure found."*

⛔ **NEVER *"the gate passed"*. ⛔ NEVER *"set-identical"*.** **DIFFERENTIAL PASS; the FULL
SUITE IS NOT GREEN** — 7 pre-existing failures remain on **both** sides.

---

## §G — WHAT THIS PREDICTION DOES NOT CLAIM

⛔ It does not claim the code will be observed running. ⛔ It does not claim the encoding bug
was ever reachable on this VM — §C says it was not. ⛔ It does not claim tonight's gate
survives another base move: **if `origin/main` moves again, this prediction and its gate die
with it**, exactly as `d896968`'s did.
