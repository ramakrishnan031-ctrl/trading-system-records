---
name: feedback-no-fixed-test-baseline
description: Never attribute a regression against a remembered failure COUNT — take a fresh BASE run in the same session/window as the candidate and comm -23 the two failure SETS; only the differential is meaningful.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d010c6e6-1e94-4ed6-9e89-609c3f52dda7
  modified: 2026-08-02T07:45:14.763Z
---

**There is no fixed-number test baseline. A remembered failure count is a property of one environment
at one moment, not of the code.**

**Why:** on 20-Jul-2026 the E4/W10 deploy was gated on a "**14-failure baseline**" carried in the
instruction and the runbook. The merge run produced **36**. Neither number was wrong — the baseline was
simply not a property of the code:
- the known-failure set is **time-of-day AND calendar dependent** (10 in-window / 11 outside the
  08:00–16:00 window / +1 on weekends and holidays);
- on the PC, `bash` resolves to the **WSL stub** (`...\WindowsApps\bash.exe`), so
  `shutil.which("bash")` **succeeds** and ~20 bash-subprocess tests
  (`test_fix065_market_hours_guard` ×17, `test_t4_deploy_preflight` ×3) **run and fail instead of
  skipping**. A different PATH ordering silently changes the count by 20.

Measured that night: **BASE `80fbe86` = 33 failed / 5001 collected · MERGE = 36 failed / 5021.**
Comparing 36 against a remembered 14 would have been meaningless in both directions — it would have
manufactured a false alarm *and* could equally have hidden a real one.

**How to apply:**
1. Take a **fresh BASE run** on the pre-change commit, in the **same session, same window, same PATH**
   as the candidate run (minutes apart, in the **MAIN TREE** — never a bare worktree, which lacks
   git-ignored runtime files and inflates the baseline).
   ⚠️⚠️ **RE-BROKEN 26-Jul, BY ME, AFTER WRITING IT DOWN.** I ran BASE in a bare
   `git worktree` to parallelise it with the build. Result: **59F/7skip instead of
   33F/5skip — 27 phantom base-only failures**, all `test_main.py`/`test_preflight.py`,
   because a fresh worktree has no git-ignored runtime files (`.env`, `data_store/`,
   local config). ⭐ **The parallelism is exactly the temptation the rule exists to
   resist**, and the inflated baseline would have hidden a real merge-only failure by
   drowning it. Recovered only because a MAIN-TREE BASE on the same commit already
   existed from earlier in the session. **A worktree BASE is not a BASE.**
   ⛔⛔ **AND THE SAME TEMPTATION BROKE IT A SECOND WAY, 26-Jul: NEVER RUN SUITES IN
   PARALLEL ON THIS MACHINE.** I ran three full `tests/unit` runs concurrently to
   compare clocks. `utils/instance_lock` uses a **machine-global** `%TEMP%\trading-
   system.lock`, so the runs corrupted each other: `test_instance_lock` ×2 plus
   `test_interactive_startup::test_holiday_guard_missing_yaml_proceeds` failed with
   *"Another instance is running (PID …)"*. ⭐ **The last one is the 18:15 bomb recorded
   as FIXED — so the corruption looked exactly like a regression in a known-fragile
   test.** Re-run alone at the same simulated 19:00 it **passes**; the 25-Jul fix is
   intact. ⇒ **a corrupted failure set is worse than a slow one, because it reads as a
   finding.** Gate runs go sequential, alone. Parallelism is the temptation this whole
   rule exists to resist — it has now cost twice, by two different mechanisms.
2. `comm -23 <candidate-fails> <base-fails>` — **merge-only must be EMPTY**; also check
   `comm -13` (base-only) so a change that *fixes* something is attributed too.
3. **Neither absolute number is meaningful; the differential is exactly meaningful.**
4. **State the prediction before the run.** On 20-Jul the arithmetic predicted `xfailed 1 → 0` and two
   named failures; observing exactly that is what made the third, unpredicted failure legible as the
   real finding instead of noise.
5. Reconcile the totals (`collected`, `passed`, `failed`, `xfailed`) so the deltas add up — that is what
   revealed the new test file had **20** tests, not the 19 the runbook claimed.

## SIBLING (26-Jul-2026): the same trap outside the test suite — a COUNT over a population under RETENTION

I wrote a handoff whose PASS criterion was "**the SSH-key CRITICAL count is still 37**". On resume it read
**33** — and 33 was the *correct* number. The `sentinel_retention` cron (`02:05` daily,
`find data_store -maxdepth 1 -name 'critical_alert_*.delivered' -mtime +7 -delete`) had run at
**02:05:01, rc=0**, deleting 17-Jul's four 6-hourly sentinels. Cutoff arithmetic exact: oldest survivor
`18-Jul 03:27:09`, just after the 18-Jul 02:05 boundary.

**The criterion was unfalsifiable in the wrong direction:** a *rise* would have meant failure, but a *fall*
meant nothing, and I had named only the rise. A count over an aging, garbage-collected population decays on
its own schedule — so "unchanged" is not a state it can be in.

**How to apply:** when the observable is a file/row COUNT, ask **who else writes or deletes this population**
before naming a number. Prefer a criterion the mechanism cannot move on its own:
- **an extremum** — "newest sentinel of any kind is still `25-Jul 21:46:45`" (what actually settled it), or
- **a predicate at the source** — `findings_count: 0` / `--report` = "No findings".

Both are immune to retention; the count is not.

## ⭐⭐ THE CLASS, NAMED (26-Jul-2026): **A NUMBER PINNED WHERE A PROPERTY IS MEANT**

Three instances in one week. It is a class, not a coincidence — expect a fourth.

| # | the number | the property it stood for | how it broke |
|---|---|---|---|
| 1 | "the SSH-key CRITICAL count is still **37**" | "no NEW alert fired" | the 02:05 retention cron GC'd four sentinels ⇒ read 33, and 33 was *correct* |
| 2 | `get_schema_version() == **44**` ×4 | "config_snapshots / retest_state / sr_detector_results still exist" | every schema bump hand-edits them; the comment trail even records it (*"was 43: pb01_watchlist"*) |
| 3 | `--max-delete **76**` | "the retention cap still refuses an unbounded sweep" | read as a delete *count* rather than a ceiling |

**Why it keeps happening:** a number is easy to assert and reads as precise. The
property is what you actually care about, and the number is only *currently* equal to
it. The moment anything else moves the population, the assertion is wrong in a way
that looks like a real failure — or worse, keeps passing while the property is gone.

**How to apply:**
1. When an assertion contains a literal number, ask: **would this still be the right
   check if the number changed for a legitimate reason?** If yes, assert the property.
2. **Verify the property BEFORE editing the number.** On 26-Jul the three schema
   assertions were bumped 44→45 only after confirming all three tables survive v45 —
   that is what makes the edit behaviour-neutral rather than a test bent to fit code.
3. Prefer an **extremum** ("newest sentinel is still X") or a **source predicate**
   (`findings_count: 0`) — both immune to a population that shrinks on its own.
4. **Sweep for the whole set**, don't fix the ones in front of you.

✅ **ALL THREE CLOSED 26-Jul (§3.1)** — `len(cfg.scanners) == 16` · `len(cfg.holidays) == 15` ·
`len(_COLSPECS) == 69`. Each became the property it stood for:
- scanners → **the file's own stated contract** (every `strategy` has a
  `config/strategies/<name>.yaml`) + a `>= 10` truncation floor. Adding a scanner adds its
  strategy file, so the check is silent on routine edits and loud on a typo/deletion.
- holidays → **no duplicate date** + all-in-year + a `>= 10` floor.
- `_COLSPECS` → **each group is ONE contiguous run** (`_group_spans()` folds only ADJACENT
  same-group columns, so a reappearing group silently yields two spans and
  `column_dimensions.group()` is called twice for one letter) + 5-field well-formedness.

⭐⭐ **THE NEW TRAP, CAUGHT WHILE CONVERTING — A REPLACEMENT THAT CANNOT FAIL IS NOT AN
IMPROVEMENT.** My first instinct was `len(cfg.scanners) == len(raw["scanners"])` ("the loader
dropped nothing"). It reads like a property and is **vacuous**: pydantic **RAISES** on a bad
entry rather than dropping it, so the two lengths can never differ. That would have swapped a
weak assertion for one that can never be red — strictly worse, because it *looks* rigorous.
⇒ **When converting a pinned number, plant the defect and watch the new assertion go RED.**
All three were proven this way (bad strategy name · duplicated date · out-of-order colspec);
sources restored **md5-identical**. [[feedback-verify-rc-not-output]]

Legitimate literals that are NOT this class: `len(digest) == 64` (a sha256 length),
`smtp.port == 587` (the config value under test).

⏰✅ **THE DAY-OF-WEEK INSTANCE — NOW FIXED (26-Jul), and it turned into a class of its own.**
`test_daily_trade_review::test_main_defaults_date_to_today_and_records_heartbeat` failed on
**WEEKENDS** (the report correctly skips a Sunday, so the asserted xlsx is never written).
Clock pinned to a **self-verifying** trading day — the test asserts the pin is still a real NSE
trading day rather than trusting the literal — with the REAL holiday guard still running.
⇒ **CONTROL THE INPUT, DO NOT DISABLE THE CHECK.** Full detail + the third axis (**YEAR — a
MEASURED boot-blocker on the first boot of 2027**) in [[clock-dependency-class-26jul]].
⭐ The reason it mattered is not the test: **a suite that answers differently on a Saturday than
on a Tuesday makes a weekend BASE non-comparable to a weekday MERGE**, which is precisely the
comparison this whole file exists to protect.

⚠️🆕 **26-Jul — A THIRD WAY TO CONTAMINATE A GATE, distinct from parallelism and from the clock:
EDITING A SOURCE FILE WHILE THE SUITE IS IN FLIGHT.** Source-SCANNING tests read the file **from
disk at runtime** (`test_every_live_finding_key_carries_its_identity`; the new `check_*`-wired
predicate) ⇒ a mid-run edit makes them judge a file the rest of the run never imported. ⭐ **The
correct response is to KILL the run and re-take it from a fully committed tree — not to reason
about whether the edit "probably" mattered. A gate you disturbed is not a gate.** Confirm the
kill with `Get-Process python*` → 0 (git-bash `ps` cannot see Windows processes).
⏰ **And the evening baseline has MOVED: an evening run is now 32F, not the remembered 33-34F**,
because the 18:15 time-bomb was fixed 25-Jul. Same lesson, one more time: the count is a property
of one env at one moment — **judge the SET.**

🔎⚠️ **26-Jul — AND WHEN A MERGE-ONLY FAILURE APPEARS, RUN IT DOWN; THE RECORDED EXPLANATION CAN
BE WRONG.** `test_instance_lock::TestSingleInstanceAcrossProcesses` (p1/p2) has long been
written off here as "a machine-global `%TEMP%\trading-system.lock` holding a DEAD PID."
**MEASURED: that is not the mechanism.** Deleting the stale lock did NOT fix it, and the
refusals name **live, DIFFERENT holder PIDs each run** ⇒ it is a **race between the class's own
spawned holder subprocesses**. ⭐ **Two independent proofs it was not the change under test:**
(1) two consecutive isolated runs of the SAME tree gave DIFFERENT failure sets; (2) the test and
its only non-stdlib import are **byte-identical BLOBS** across all three trees (`git rev-parse
<rev>:<path>` — stronger than a re-run, since no code difference can exist). ⇒ **expect 31-33F
and judge the SET; and prefer a blob-identity check over a re-run when asking "could my change
possibly have caused this?"**

## ⭐⭐ 02-AUG-2026 — **THE INVOCATION IS PART OF THE BASELINE. `run_tests.py` IS NOT THE GATE.**

**THE RULE: the campaign regression invocation is `pytest tests/unit tests/integration -q`
(NARROW). ⛔ NOT `run_tests.py`.**

**Why it matters, and why it is a SAFETY rule and not a tidiness one:** `run_tests.py`
runs the **whole tree**, which collects the **44 never-gated `tests/crash_test/` + `tests/core/`
tests** the standing gate deliberately excludes. Several `tests/crash_test/` modules call
**`load_dotenv()` on the REAL `.env`**, and the suite's side-effect guards are **in-process**
— a test spawning a **subprocess is not covered** (the standing hole).
- **In a base WORKTREE this is harmless: a worktree has no `.env`** ⇒ no credentials ⇒ no
  possible real Telegram/broker side effect. Verified 02-Aug (worktree `.env` absent; live
  `data_store/*.db` mtimes unmoved; the harness wrote only into the worktree's own
  `data_store/ct_scratch`).
- ⛔ **In the MAIN TREE it is NOT harmless** — that is where the real `.env` (incl.
  `TELEGRAM_BOT_TOKEN`) and the live DB are. **Never run the full tree there for a gate.**
⇒ I started a wide run on 02-Aug, stopped it, and switched both halves to the narrow
invocation. **Both halves must use the SAME invocation or the sets are not comparable.**

**⚠️ AND THIS NUANCES THIS FILE'S OWN "A WORKTREE BASE IS NOT A BASE" (26-Jul) — read them
together.** That absolute was written after a bare worktree produced **27 phantom base-only
failures**. The campaign now uses a worktree base **deliberately**, and it is sound **only
with the mitigation**: **copy the git-ignored runtime files in, then PROVE and SUBTRACT any
residual artifacts.** Measured 02-Aug (#2c-R):
- ✅ **`cp config/instruments.csv` into the worktree ⇒ the 26 `test_main` phantoms DID NOT
  RECUR** — that is the mechanism's own control, not a hope.
- ⚪ **3 residual worktree-only failures remained** — `test_t4_deploy_preflight` ×3, the
  **subprocess python/bash-not-on-PATH** class (same family this file already names).
- ⇒ base **10F/5,488P** vs new **7F/5,506P**, `comm -23` **EMPTY**, and the **arithmetic
  closed on BOTH axes** (`10−3 = 7`; `5,488+3+15 = 5,506`; collected `+15` = exactly the new
  tests). **The residual-artifact subtraction is only legitimate because the arithmetic
  closes** — if it does not close, the base is not usable.
⛔ **The danger direction is asymmetric and worth stating: a base-only artifact can MASK a
real new failure** (same test failing both sides ⇒ absent from `comm -23`). So minimise
artifacts first; never explain them away.

**🗑️ PARTIAL-LOG DISCIPLINE (applied twice now, both sessions):** a stopped/killed run's
partial output is **DELETED immediately**, never left on disk. A half-written pytest log is
exactly the stale-baseline trap this file exists to prevent — and it reads as authoritative
later. Same instinct as *"a gate you disturbed is not a gate"* above.

Related: [[feedback-regression-must-not-cross-midnight]] (the sibling clock hazard) ·
[[feedback-verify-rc-not-output]] (a green check must have been able to be red) ·
[[e4-w10-deploy-stopped-20jul]] · [[pc-test-env-hygiene]] · [[realert-presence-ledger-26jul]]
