---
name: pc-test-env-hygiene
description: "PC (Windows) full pytest suite has ~32 pre-existing env failures; green on VM. Low-priority cleanup so future local testing isn't muddied."
metadata: 
  node_type: memory
  type: project
  originSessionId: 352c7b01-735b-48d3-8902-0d349b1dfe25
  modified: 2026-09-17T05:29:31.607Z
---

**Hygiene queue (LOW priority, do after current work).** The Windows dev PC
cannot run the full pytest suite clean — the VM is the canonical green env.

As of 22-Jun-2026 a full run = **32 failed, 3587 passed, 12 skipped** (~10 min).
Proven **pre-existing / environmental**, NOT from any feature change (stash-
compare: clean `main` shows identical-or-more failures; a change branch produced
one *fewer*). Breakdown:
- `test_main.py` (23) + `test_system_manager.py` (1) — MagicMock/wiring, env-specific.
- `test_fix135_auto_token.py` (6) — TOTP/pyotp + network mocking.
- `test_fix129_ntp_check.py` (2) — NTP drift check.
- 3 collection errors (`test_fix073/074/075`) were `zoneinfo` "No time zone found
  with key Asia/Kolkata" → **fixed 22-Jun by `pip install tzdata` into the venv**
  (Windows ships no IANA tz DB). Consider adding `tzdata` to requirements for Windows.

**🔄 16-Jul-2026 UPDATE (much improved + a NEW time-gate).** A full `tests/unit tests/integration` run is
now **4700 passed / 15 skipped / 10 failed** (~12.5 min) — the 32 shrank to **10**, all still
pre-existing/environmental (stash-compare proven on the pre-change base): `test_main` ×4 ·
`test_order_placer_fix061` ×4 · `test_fix181` ×1 · `test_phase17_batch2` ×1 (Mock-not-subscriptable /
`int(Mock)` / thread-timing mock-harness artifacts).
**⚠️ THE COUNT IS TIME-OF-DAY DEPENDENT — 10 in-window, 11 outside 08:00–16:00 IST.** An 11th,
`test_interactive_startup::test_holiday_guard_missing_yaml_proceeds`, fails ONLY when the suite runs
outside the service window: `main()` takes the **FIX-189 startup guard** (`Outside service window
[08:00-16:00 IST] … clean exit 0`) so the test's `assert result == 5` sees 0. Proven twice: it fails
identically on a pre-change base, and it **PASSES with `TS_IGNORE_MARKET_WINDOW=1`**.
**⇒ RULE: always compare a regression run to a base run taken at the SAME time of day** (or export
`TS_IGNORE_MARKET_WINDOW=1`), else the clock alone changes the "known failures" set and a clean change
looks like a regression. Found during [[mc4-killswitch-lock-16jul]].

**🗓️ 18-Jul-2026 — a CALENDAR-gated failure joins the time-gated set:** `test_daily_trade_review::
test_main_defaults_date_to_today_and_records_heartbeat` FAILS when the suite runs on a **weekend/
holiday** — `daily_trade_review.main()` hits the holiday/weekend skip (`is_holiday_or_weekend`), writes
no report xlsx, so the file-exists assert fails. Not a code bug; same class as
`test_interactive_startup` (time-gated). **⇒ the "known env" count is now CALENDAR- AND time-of-day-
dependent: attribute a regression against a base run taken on the SAME weekday**, or the day-of-week
alone changes the known-failure set (a long session that crosses midnight into Sat/Sun exposes it).

**⛔ 27-Jul-2026 — ONE MEMBER OF THIS SET IS NOT "PC-env" AND MUST BE REMOVED FROM IT.**
`test_instance_lock` ×2 was absorbed into this bucket ("Windows file-lock flake", "PC-only, passes on
the VM"). **Wrong, and the label is what kept it unexamined for nine days.** It is a **120-second
orphan child process the test class spawns and fails to reap** — `_holder_process` does
`time.sleep(120)` in a bare `Popen` with no job object and no `atexit`, so it survives pytest and
holds the machine-global lock into the *next* invocation. Platform-independent; the VM simply never
overlapped two runs. ⭐ **The "different live holder PID each run" is the fingerprint.** Mechanism,
3 sibling test defects, and the corrected entries: [[instance-lock-flake-mechanism-27jul]].
**⇒ When triaging this bucket, do not assume "PC-env" is a diagnosis — for at least one member it was
a label standing in for one.**

**Why it matters:** a PC that can't run the suite clean muddies future local
testing — hard to tell a real regression from background noise (mitigated for now
by per-file stash-comparison). **How to apply:** when convenient, triage the
remaining failures (likely Windows-path / mock / network assumptions), get the PC
suite to match the VM's green, and pin `tzdata` for Windows. Related:
[[feedback_naive_ist_timestamps]], [[feedback_memory_hygiene]].

## ⛔⛔ 28-Jul-2026 — **THE WHOLE BUCKET IS MIS-NAMED. SWEPT, AND NOT ONE OF THE 13 IS "PC-ENV".**
The 27-Jul note below removed **one** member (`test_instance_lock`) and warned that "PC-env" was a
label standing in for a diagnosis. ⭐ **Sweeping the CLASS rather than the instance shows the label
is wrong for EVERY member.** Current regression = **13 failed / 5,362 passed / 4 skipped**, and
***all 13 run in 2.54 seconds*** — no network call, no missing binary, no Windows-path problem.
They fail on mock wiring, a stale fixture, a self-inflicted orphan process, or a REAL contract
violation.

⭐⭐ **THE GENUINELY ENVIRONMENTAL CASES ARE THE *SKIPS*, NOT THE FAILURES** — `test_zerodha_login`
×2 (`skipif` win), `test_backup_retention` (symlinks), `test_gui_secret_key` ("Windows does not
honour POSIX file modes"). Each names its environmental fact and skips cleanly.
⇒ ***The "PC-env failures" label borrows the skips' legitimacy for a population that has none.***
That is exactly how `test_instance_lock` survived 9 days and FIX-061's hard-kill coverage 22.

**Full ranked table + verdicts:** `docs/decisions/ACTIONS_not_decisions.md` § "THE 13-FAILURE SWEEP".
✅ **RANK 1 RESOLVED 28-Jul:** the 4 `test_order_placer_fix061` tests died at `order_placer.py:3513`
(H-3 `a254a82` 05-Jul vs a 15-Jun fixture) **before any assertion**; repaired test-side, **9 pass**,
⇒ the production path was fine and had merely gone unwatched. **No defect.**
⚠️ **RANK 2 OPEN + UNKNOWN:** `test_fix181` inflight-orphan flatten asserts `LIMIT`, production
emits **`MARKET`** under HARD_KILL — stale test or a real kill-path divergence, **not guessed**.
⭐ **RANK 4 IS NOT A FAILURE AT ALL:** the closure-source contract test is WORKING — it reports that
`scripts/backfill_closure_source_w8.py:92` restates `OWN_SL/OWN_TGT/OWN_EOD` instead of importing
`core/closure_source.py`. Unfixed on every branch; that script wrote 35 rows on 28-Jul.

## 🐚⛔ 08-Aug-2026 — **RUN THE GATE FROM GIT BASH. POWERSHELL MANUFACTURES 20 PHANTOM FAILURES.**
**(P) MEASURED, both directions, same command, same tree, same minute:** `pytest tests/unit
tests/integration` launched from **PowerShell** → **29 failed**; from **Git Bash** → **9 failed
/ 5582 passed**, the enumerated §8.12 set exactly. The extra 20 are two whole families that
appear in NO baseline: `test_fix065_market_hours_guard` (17) + `test_t4_deploy_preflight` (3).

⭐⭐ **AND THIS ONE HAS A REAL DIAGNOSIS, unlike the label this file exists to retire.** Both
families **shell out to `bash`**. In PowerShell `bash` resolves to
`C:/Users/rama/AppData/Local/Microsoft/WindowsApps/bash.exe` — the **WSL app-execution alias**,
with no distro installed — so the scripts never run and the tests assert against WSL's own error
text (`'<Distro>' to install`, **UTF-16LE**, which is the `\x00`-interleaving fingerprint). In
Git Bash `bash` is `/usr/bin/bash` and the same 30 tests **all pass**.

🔑 **⇒ THE LAUNCHER IS PART OF THE GATE.** ⛔ A gate whose answer changes with the shell is not a
gate. **Attribution proven by experiment, not prior:** production changes stashed → the two
families returned **20 failed / 10 passed with the FAILED sets IDENTICAL line for line**, so the
change could not have caused them.
⚠️ **THE DANGEROUS DIRECTION IS THE OTHER ONE:** this time the mechanism ADDED noise, but the
same +20 could just as easily have SWALLOWED a real regression inside a bigger "known set" — and
a count-compare would never have shown it. ⇒ always set-compare, and record the launcher.

⚠️ **WIDTH (the standing rule applied to my own sweep):** the 13 come from
`pytest tests/unit tests/integration` = **322 files**. ⛔ **`tests/crash_test/` (8 files) and
`tests/core/` (1) are NOT in that command — 9 test files never run in the gate at all.**
⭐ *A skipped test and a failing test hide the same thing; an **uncollected** test hides more,
because it appears in no count.* [[feedback-absence-needs-wide-check]]

## 🧪🔴 17-Aug-2026 — **TWO MORE PHANTOM-FAILURE SOURCES. THE 08-Aug GUARD COVERS NEITHER.**
Gating the extracted alerts unit, the FIRST run reported **37 failed** where the campaign's
recorded baseline was 9. ⛔ Not accepted as "environmental"; both causes were **proven by
experiment** and the gate **re-run from scratch** ⇒ **37 → 7**.

🔴 **(A) `config/instruments.csv` IS GITIGNORED (`.gitignore:39`) ⇒ A FRESH `git worktree add`
NEVER HAS IT — and its absence manufactures 26 failures.** Without it `main.py:2160`'s BL-20
guard `assert instrument_cache is not None` trips (line measured at `6fa8a1c`). ⭐ **PROVEN by
planting it: `test_main.py` 30F/51P → 4F/77P.** 📌 **RULE: a new worktree is NOT a runnable
tree — the untracked prerequisites (`config/instruments.csv`) must be planted with `cp`
(⛔ never `write_text`, which rewrites every newline). ⛔ Do NOT plant `.env`.**

🔴 **(B) `python3` RESOLVES TO THE WindowsApps STUB, AND `C:/python311` HAS NO `python3.exe`.**
`scripts/ist_now.sh` + `check_tz.sh` then never run and the tests assert against *"Python was
not found; run without arguments to install from the Microsoft Store"* ⇒ `test_t4_deploy_preflight`
×3 + `test_preflight` ×1. ⭐ **PROVEN with a shim** (`cp python.exe → shim/python3.exe`, shim
first on PATH): the scripts execute and all four pass.
🔑🔑 **THIS IS THE SAME DEFECT CLASS AS THE 08-Aug `bash` STUB — AND `9fdfe41`'s conftest guard
DOES NOT COVER IT.** That guard refuses only when **`bash`** is a WindowsApps alias; here `bash`
correctly resolved to `/usr/bin/bash` and the guard would have passed the launcher as fine while
**`python3`** silently distorted the count. ⇒ **when `9fdfe41` is re-landed it must be WIDENED to
`python3`, ⛔ not merely restored** — a launcher guard that checks one interpreter and not the
other gives the APPEARANCE of fail-closed while the same 20-30-failure distortion walks past it.

⏰ **(C) ⛔ NEVER `TZ='Asia/Kolkata' date` ON THIS PC — IT IS 5h30m WRONG.** The repo's own
`scripts/check_tz.sh` says so: *"TZ='Asia/Kolkata' is UNRELIABLE in this shell … MSYS2 has no
zoneinfo → falls back to UTC"*. Measured 17-Aug: `TZ=Asia/Kolkata date` → **05:14** while the VM
and `now_ist()` both read **10:45 IST**. ⭐ **Plain `date` (local) tracks VM IST within ~30 s** —
use that, or `now_ist()`. 📌 A clock check that is itself broken silently mis-times a once-only
window.

📏 **BASELINE AT `origin/main` `6fa8a1c` (17-Aug, repaired env) = 7 failed / 5,593 passed /
4 skipped, RAW_PYTEST_RC=1**: `test_closure_source_contract` ×1 · `test_fix181` ×1 · `test_main`
×4 (`paper_mode_does_not_require_webhook_secret` + `TestContinueFromGate` ×3) ·
`test_phase17_batch2` ×1. ⭐ The `test_instance_lock` flapper did **not** appear.

🐍 **(D) 23-Aug-2026 — ⛔ `D:/Projects/trading-system/venv/` IS NOW **EMPTY** (no `Scripts/`, no `bin/`), and NO sibling worktree has one.** The gate runner is therefore `/c/python311/python` (Python 3.11.9, pytest 9.0.3). 🔴 **CONSEQUENCE: `scripts/ist_now.sh`'s `pick_python()` tries `$PYTHON` → `$REPO_ROOT/venv/Scripts/python.exe` → `venv/bin/python` → `/home/ubuntu/...` → `command -v python3` — with no venv it reaches `python3`, which is the **WindowsApps STUB** (*"Python was not found… App execution aliases"*, rc 49/2) ⇒ **3 SPURIOUS FAILURES** in `tests/unit/test_t4_deploy_preflight.py` (`test_ist_now_emits_valid_ist`, `test_check_tz_fails_on_broken_utc_form`, `test_check_tz_passes_on_agreement`).** ⭐ **FIX: `PYTHON=/c/python311/python pytest …`** — `pick_python()` honours `$PYTHON` FIRST. **PROVEN BOTH WAYS, BOTH TREES** (files byte-identical, md5 `1e4eaad9…` / `4f8e1d4a…`): without it **3 failed / 6 passed**, with it **9 passed**. ⚠️ Adding a PATH shim for `python3` is **NOT** enough — measured, still fails. ⇒ **a raw run reads 10F, not the recorded 7F; the 3 are ENV, ⛔ not a code defect.**

📏🔬 **01-Sep-2026 — NAMED BASELINE AT THE *DEPLOYED* SHA, AND A TRUE Δ0 DIFFERENTIAL.** Gating FILE 104's step 0/2 worktree: **`39292d3` (deployed tree) = 11 failed / 6,006 passed / 5 skipped, `PYTEST_RC=1`** (17m46s, Git Bash, `pytest tests/unit tests/integration`, no venv). ⭐ **DIFFERENTIAL vs the PREVIOUSLY-deployed `52ccb4f` = 11 failed / 5,895 passed, and `comm` proves the FAILED sets are IDENTICAL line-for-line ⇒ Δ0.** 🔑 **The 29–30-Aug code that went live 31-Aug introduced ZERO regressions; the +111 passed are new green tests.** ⚠️ Both runs were taken on the SAME day within ~15 min of each other, honouring this file's own same-weekday/same-time-of-day rule.

🧾 **THE SET, BY NAME (⛔ the docs only ever recorded COUNTS — which is precisely what made 11-vs-7 ambiguous):** 3 ENV (`test_t4_deploy_preflight` ×3, the §D venv/`python3`-stub trio) **+ 8 REAL** — `test_closure_source_contract` ×1 · `test_fix181` ×1 (still `MARKET` vs `LIMIT`, the RANK-2 OPEN item, unchanged since 28-Jul) · `test_main` ×4 (`paper_mode_does_not_require_webhook_secret` + `TestContinueFromGate` ×3) · `test_phase17_batch2` ×1 (`int(Mock)` at `signals/webhook_receiver.py:212`) · **`test_q9_consecutive_losses_wired::TestTheStreakMechanics::test_the_streak_is_scoped_to_today` ×1** (`assert 4 == 0`). ⭐ The first 7 are exactly the 17-Aug `6fa8a1c` set; the **q9 streak test is the 8th**. ⛔ **DO NOT conclude it "joined after 17-Aug"** — its name is literally *scoped_to_today* and this file records two prior CALENDAR/time-gated members, so a cross-day comparison cannot distinguish "new failure" from "date-gated and not fired on 17-Aug". 💭 Unresolved, ⛔ not guessed.

🐍✅ **A SECOND, CLEANER FIX FOR §D's venv HOLE — fill the slot instead of overriding it.** `python -m venv --system-site-packages venv` **inside the worktree** creates `venv/Scripts/python.exe`, which is `pick_python()`'s *second* candidate, so the scripts never reach the stub: `bash scripts/ist_now.sh` → `rc=0`, and `test_t4_deploy_preflight` goes **3F/6P → 9 passed**. ⭐ No downloads (system site-packages), and `venv/` is gitignored (`.gitignore:56`) so the worktree stays porcelain-clean. Use this when the gate must run unattended (nothing to remember to export); keep `PYTHON=/c/python311/python` for a one-off. ⚠️ **PROVEN ACROSS MACHINES, same script/same SHA:** PC without venv → `rc=49` *"Python was not found"*; VM → `rc=0` emitting `2026-09-01T09:26:41.379508+05:30` (`/usr/bin/python3`, 3.12.3).

🔤🕳️ **17-Sep-2026 — IN THIS GIT BASH, A DEFAULT-LOCALE `grep -F` MISSES NON-ASCII LITERALS, AND `grep -P` REFUSES TO RUN.** 🔬 An emoji-bearing literal (the ledger's `⛔🔴🔝 **STANDING ~TWO-WEEK CONDITION …` row) read **0** under the default locale (`locale` reports `en_US.UTF-8`) while `LC_ALL=C grep -F` and a Python substring check both found it (control: a one-character mutation ⇒ no hit); ASCII literals match normally. `grep -P` errors *"supports only unibyte and UTF-8 locales"* — even under `LC_ALL=C`. ⭐ **For any non-ASCII pattern use `LC_ALL=C grep -F` (bytewise) or Python; ⛔ never read a default-locale zero as an absence** — it nearly recorded an unchanged row as changed. ⚠️🔴 **TONIGHT-FACING (17-Sep card §2):** the testing VM's `logs/cron-drift-check.log` headings begin with emoji (🔴 · 🆕 · ⏰ · ⚠️) ⇒ a default-locale grep for a heading can read 0 where there is 1 and score a MISS of the frozen 18:00 prediction that is ⛔ not a miss. ⭐ **For any count on that log or its captures:** `LC_ALL=C` on EVERY grep (⛔ no exceptions, including quick looks) · anchor on the ASCII part (`ENABLED in registry, ABSENT from live crontab (CRITICAL):` · `Live job NOT in registry` · `RAN_UNVERIFIED` · `CRON INTEGRITY`) · prefer Python · ⛔ every zero carries a positive control run with the same flags and locale. ✅ The frozen prediction itself is not affected (0 non-ASCII bytes). ⏸ DEFERRED until after the S&R measurement period: one sweep of previously recorded zeros whose PATTERN contained a non-ASCII character — ⛔ not every zero.
