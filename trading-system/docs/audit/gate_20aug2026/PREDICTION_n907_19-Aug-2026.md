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

## ADDENDUM 1 — **20-Aug: THE FREEZE STANDS (BASE UNMOVED) · A SECOND, INDEPENDENTLY-STAGED GATE · AND `P3`'s OWN INSTRUMENT WAS BROKEN.**
Added **2026-08-20 ~09:25 IST**, ⛔ **BEFORE any push.** ⛔ No edit above the boundary.
⛔ Nothing run, restarted or repaired on the VM; every VM read was `mode=ro` / `systemctl show`
/ `grep`. ⛔ `forward_shadow_record.py` was **NOT** invoked by hand.

### A · ⭐ THE BASE-STALENESS CLAUSE DID **NOT** FIRE — ⛔ NO RE-FREEZE IS OWED
`origin/main` re-measured **08:22 IST, two independent ways**: PC `git ls-remote origin
refs/heads/main` (wire protocol) and a raw `cat /home/ubuntu/trading-system.git/refs/heads/main`
on the VM (filesystem, no git binary). **Both = `08b462ba175d904e8723ed34a13c956f0dd33679`** —
identical to the freeze-time base. ⇒ ⭐ **the frozen calls above stand unchanged.**

⚠️ **A CARD PREMISE WAS STALE AND IS CORRECTED HERE, ⛔ not absorbed.** The 20-Aug card's §0
said n907 was *"extracted onto `f62db55`… ⚠️ Base has moved since"*, and instructed a
re-extraction test. **Measured: `d896968`'s parent IS `08b462b`** — the current base — so
`merge-base --is-ancestor 08b462b d896968` = **YES**, **1 ahead / 0 behind**, a clean
fast-forward candidate. ⛔ **No re-extraction was needed or performed.** ⭐ This correction was
already made on 18-Aug (`N18-17`, *"its premise corrected"*); today re-derived it independently.

### B · 🧪 A SECOND FULL GATE, STAGED DIFFERENTLY FROM §G's — ⛔ NOT A REPEAT
§G's gate ran **without** the gitignored `config/instruments.csv` (its own note says so), giving
a 10-failure base. Today's runs planted it **and** a `python3` shim, which is why the baseline is
**7**, not 10. ⭐ **A different harness reaching the same verdict is stronger than a re-run.**

| | rc | failed | passed | skipped | elapsed |
|---|---|---|---|---|---|
| base `08b462b` | **1** | **7** | 5,646 | 4 | 897.92 s |
| unit `d896968` | **1** | **7** | **5,654** | 4 | 917.59 s |

- ✅ **`comm` BOTH directions: 0 NEW · 0 disappeared · 7 common.**
- ⭐ **And the failure MESSAGES are identical, ⛔ not just the ids** — load-bearing, because **4 of
  the 7 are in `test_main.py`; the same id is not the same cause.**
- ⭐ **NON-VACUITY: 5,646 → 5,654 = +8 = EXACTLY the 8 tests** in
  `tests/unit/test_n907_forward_shadow_encoding.py` — **absent at base** (`cat-file -e` fails),
  collects **8**, and all **8 pass** on the unit (targeted run `rc=0`).
- ✅ Tree fingerprint `d41d8cd98f00b204e9800998ecf8427e` **IDENTICAL at start AND end** of both runs.
- 📌 Raw rc taken **from pytest itself** by redirect, ⛔ never through a pipe.
- 🖥️ Staging, recorded: system Python **3.11.9** (`C:\python311\python.exe`), pytest **9.0.3**,
  ⛔ **no venv** (none exists repo-wide — `pyvenv.cfg` count is 0), `config/instruments.csv`
  planted (md5 `a7b07623909e051cb624ad157cee1671`), `python3` shim first on `PATH`, **Git Bash**.
- 🏷️ **MANDATED WORDING:** *no new failures — 7 known remain; 0 did not reproduce; raw rc
  retained.* ⛔ NEVER *"the gate passed"*, ⛔ NEVER *"set-identical"*.

**Content re-proven today, three ways, against the original `7649cd8`:** `range-diff` →
`1: 7649cd8 = 1: d896968` · net-diff md5 identical **RAW** (`d091938839a8179aaffc74df0460a672`)
**and** index-stripped (`7e3f8f5aa2b180f1238a6a153d67c180`) · `patch-id --stable` identical
(`977ab7bb667a486b080a2964636f0fd43de7ef17`).
⭐ **The RAW md5 matching is worth naming** — it usually cannot, because the `index` blob lines
move with the base; here the two touched files are the same blobs on both bases.

### C · 🔴 **`P3`'s INSTRUMENT WAS BROKEN AS WRITTEN, AND WOULD HAVE FIRED FALSELY TONIGHT**
`P3` reads *"the VM deployed tree shows tracked drift vs the new HEAD — measured by the
`GIT_INDEX_FILE` temp-index method"*. Measured today on the VM against a tree **proven identical**:

| method | result |
|---|---|
| `read-tree <sha>` → `diff-files` | 🔴 **1,309 files reported MODIFIED — a FALSE POSITIVE** |
| `read-tree <sha>` → **`update-index --refresh -q`** → `diff-files` | ✅ **0** |
| independent control: `md5sum` of 6 tracked files vs their blobs at `08b462b` | ✅ **6/6 MATCH** |

**Cause:** `read-tree` builds an index with **no stat data**; `diff-files` compares worktree stat
against the index, so with every entry blank it calls every file modified.
⇒ 🔑 **`update-index --refresh` is now part of the method**, and the deployed tree is confirmed to
be `08b462b` by **two** independent means. 📌 *A red check needs its method verified — this one
was red for a reason with nothing to do with the tree.*

### D · 📊 **§3(f) — A1's UNCHANGED BASELINE, BANKED BEFORE THIS UNIT CAN SHIP**
`scripts/forward_shadow_record.py` **is Gate A1's own instrument** (§H), so its own tests passing
is ⛔ **not sufficient**. Two independent arguments that it cannot alter what A1 measures:

**① Mechanism.** Both edits change only the *decoding* of two reads — no logic, no output path, no
row, column or count. **② Environment.** Under a cron-like `env -i` (the crontab sets only
`SHELL`; `.env` carries **no** locale vars), the deployed interpreter reports
**`sys.flags.utf8_mode = 1`** and `getpreferredencoding(False) = utf-8` ⇒ the **unpatched** read
already decodes UTF-8 ⇒ the decoded bytes are identical either way. *(Premise half that IS true:
`config/scoring_weights.yaml` carries exactly **51** non-ASCII bytes, and an ASCII decode of it
really does raise — `0xe2` at position 30.)*

**THE BASELINE, from `cron_heartbeat` (`job_name='forward_shadow_record'`):**

| executed_at | status | wrote | sim |
|---|---|---|---|
| 2026-08-19T18:16:33 | SUCCESS | **4,265** | 3,744 |
| 2026-08-18T18:16:47 | SUCCESS | 5,917 | 5,546 |
| 2026-08-17T18:17:01 | SUCCESS | 5,962 | 5,679 |
| 2026-08-14T18:16:45 | SUCCESS | 5,567 | 5,294 |
| 2026-08-13T18:17:07 | SUCCESS | 5,466 | 5,122 |
| 2026-08-12T18:17:16 | SUCCESS | 5,425 | 5,180 |
| 2026-08-11T18:17:23 | SUCCESS | 6,750 | 6,329 |
| **2026-08-10T18:15:02** | **SUCCESS** | 🔴 **`[func=EMPTY_NO_DATA] … nothing new (0 present)`** | — |
| 2026-08-07T18:17:20 | SUCCESS | 6,198 | 5,875 |
| 2026-08-06T18:18:07 | SUCCESS | 7,947 | 7,898 |
| 2026-08-05T18:18:02 | SUCCESS | 8,675 | 8,596 |

🔴 **THE 10-Aug ROW IS THE PROOF FOR TONIGHT'S A1 READ: `status = SUCCESS` WITH ZERO ROWS.**
⇒ ⛔ **A1 must read the `wrote=` count out of the `message` column; `status`/exit-0 alone is
insufficient and has already been wrong once.** ⭐ **0 rows ⇒ DEFER.**
⚠️ **TODAY'S 18:15 run happens BEFORE the ~19:00 push**, so it is the last unpatched reading and
becomes the *pre*-image; the first **post**-deploy run is **21-Aug 18:15**. ⛔ That run is a
**before/after comparison**, ⛔ never a new baseline.

### E · ⚠️ **A CONSTRAINT THE CARD DID NOT ANTICIPATE — `n907` AND `tiers` CANNOT BOTH FAST-FORWARD**
`d896968` (n907) and `7297be7` (tiers) are **siblings**: both parented on `08b462b`, neither
containing the other, `merge-base` = `08b462b`. `git push --dry-run` with an explicit refspec says
each is a clean FF **on its own** (`08b462b..d896968` rc 0 · `08b462b..7297be7` rc 0) — ⭐ **which
is exactly how this trap passes unnoticed.** The first push moves `origin/main`; the second is
then **1 ahead / 1 behind** ⇒ **non-FF**, and `--force` is prohibited.
✅ **RESOLVED IN ADVANCE, ⛔ not at 19:00:** the card's §8(D) already fixes the order (**n907
first**), so tiers was rebased onto `d896968` as **`b80354c240b79177c62fefacb31d4884bb0464f0`** —
content proven identical to its sibling (`range-diff` `=`, `patch-id` identical
`f3d8297cb494b470f5476619d841f3a7af16dbf1`) — and gated at that exact SHA.
⛔ **This does NOT couple the verdicts:** if n907 is refused, tiers simply keeps its sibling SHA.

### F · ⛔ WHAT THIS ADDENDUM DOES NOT DO
⛔ It does not change any call above the boundary. ⛔ It does not upgrade the ceiling — **`NOT
TESTED` BY CONSTRUCTION still stands**, and today's environment probe is the *reason*, ⛔ not a
counter-example. ⛔ It does not lift §H's hold by itself: §H's condition is that A1's baseline be
read on unchanged code, and **that reading does not exist until tonight's 18:15 run**. ⛔ It makes
no claim about `tiers`, which is separately gated and separately frozen.
