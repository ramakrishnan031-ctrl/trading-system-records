---
name: verify-check-the-rc-not-the-output
description: "A green check is only evidence if it could have been red — errored commands, stale baselines, INFLATED baselines (a bare git worktree lacks git-ignored data ⇒ ~30 spurious failures ⇒ the MASKING direction), and never-failed tests all fake a pass. Check the rc; baseline in the MAIN tree via git checkout <base> -- <files>; see every claim-carrying test fail once."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
  modified: 2026-07-30T14:35:51.513Z
---

**⭐⭐ 20-Jul-2026, the sharpest instance yet — I applied this rule to a checklist and then broke it myself,
twice, in the same session.** Having found 5 wrong *prose* expectations in the Monday checklist (0 wrong SQL),
I wrote two prose claims about the memory compaction and shipped them **unmeasured**:
- *"the dropped `[[feedback-verify-rc-not-output]]` was a dangling link — removing it is a repair"* — **FALSE.**
  The verifier reports **0 unresolved slugs** before the compaction. It resolved fine, via the filename-derived
  form; the file also answers to its frontmatter `name:`. Both forms are valid.
- *"the 19-Jul report's `DROPPED = 0` link check had a blind spot"* — **FALSE, and it maligned a correct check.**
  That report had explicitly examined this exact file and classified it, correctly, as not an orphan.

**The lesson is not "be careful with links".** It is that *finding* an unvalidated-expectation defect confers
**no immunity** from committing one. The check I wrote for the byte budget had the same disease in a third
form: `awk 'length($0)>300'` counts **characters, not bytes**, and had no exemption tier — so it was
**permanently red on 23 lines**, and *a check that is always red is exactly as useless as one that can never
be red*. Fixed to `LC_ALL=C awk 'length>(index($0,"🔝")?450:300)'`, then proven able to go red before being
trusted. **Ask of every claim you are about to write down: measured, or assumed?** [[feedback-verify-the-finding-premise]]

---

**🧊 28-Jul-2026 — A COMPILED ARTIFACT PRESENT WHERE ITS SOURCE IS NOT.** Hunting the W8 backfill script on
`main`, `find` returned `scripts/__pycache__/backfill_closure_source_w8.cpython-311.pyc` **but no `.py`** —
the source lived only on `check1-classify-27jul`. ⭐ **A `__pycache__` hit is NOT evidence the module is
there**; `__pycache__` is git-ignored so `git status` stays clean and says nothing. **Confirm the `.py`, and
which ref carries it** (`git log --all -- <path>`).

⭐⭐ **AND THEN MEASURED, because the scary version of this would break an invariant** (report:
`docs/audit/pyc_orphan_sweep_28jul2026.md`): **a `__pycache__` orphan is NOT importable** —
`ModuleNotFoundError`, PEP 3147 keys the cache to a live source file. Only a `.pyc` sitting **where the
`.py` was** (legacy sourceless layout) executes. ⇒ **TWO classes: `__pycache__` orphan = SEARCH hazard,
inert · `.pyc` outside `__pycache__` = IMPORT hazard, executes stale code.** Swept PC + VM: **0 import
hazards** in either, and nothing here can create one (no `compileall`/`-B`/`PYTHONPYCACHEPREFIX`; CPython
writes only into `__pycache__`). ⚠️ **Untracked bytecode DOES survive the deploy** — `checkout -f` never
removes untracked files; `test_daily_review.py` was deleted in `01e07b7` and its 2 `.pyc` have outlived
every deploy since **May**. Residue real, execution impossible. ⛔ **`git clean -xdf` must NEVER be used in
the deployed tree** — `data_store/`, `logs/`, `.env` are all untracked there.

---

**A green result is evidence ONLY if it could have been red.** Three ways a "pass" lies — all three hit on
16-Jul-2026, in one session:

**1. The command errored and printed nothing** (deploy). Assert on the exit code, not on "the output looked
empty/right" — the PowerShell cases below.

**2. The baseline still contained the change** (M-C8). `git stash` only stashes **UNCOMMITTED** work. I
stashed to get a "clean baseline" *after* having committed the fix ⇒ both sides of the comparison contained
the change, every number matched perfectly, and I nearly filed a REAL regression as "pre-existing". **Baseline
against the actual pre-change tree** (`git checkout <base> -- <files>`) and **verify it lacks the change**
(`grep -c <new-symbol>` → 0) before trusting a single number.

**2b. ⭐ The baseline was INFLATED by missing git-ignored data** (18-Jul, Q9 batch 4). The fix for #2 is a
throwaway `git worktree` — but **a bare worktree lacks every git-ignored runtime file**, and that makes the
BASE fail tests it should pass. Here `config/instruments.csv` (75,749 B) is git-ignored ⇒
`main.py:1949` can't build the InstrumentCache ⇒ **`main.py:2014` `assert instrument_cache is not None`**
trips ⇒ **~30 boot-path `test_main.py` + preflight/T4 tests fail spuriously** (base **42F**; with the file
copied in, **15F**). **⚠️ INFLATION IS THE MASKING DIRECTION** — a genuine new failure can coincidentally
match one of those ~30 and be dismissed as pre-existing. Proven causally, not by correlation: the test
**fails in ISOLATION in 0.56 s** in the worktree (⇒ not ordering, not contention), passes in the main tree,
and copying that one file in makes it pass. **⇒ PREFER `git checkout <base> -- <files>` IN THE MAIN TREE**
(it preserves ignored files); if you must use a worktree, **seed it with the git-ignored runtime data first**.
*This also retires the long-standing "~30-test flake band" as an uncharacterised observation — it was never
flake.* And keep base+mine in the **SAME TIME WINDOW** ([[q9-batch3-capital-invariant-18jul]]).
[[q9-batch4-sizing-reachability-18jul]]

**3. The test never could have failed** (M-C8). Two of my own new tests passed against deliberately reverted
code: one measured the victim's state *after* the blocking call had already finished; another asserted a case
a **DB trigger already protected**. Both were vacuous. **Revert the behaviour and SEE each claim-carrying test
go red for the RIGHT reason.** Corollaries: a *scoped* suite can stay green while the only real regression
sits in a suite you never ran (only the FULL 4,758-test run caught M-C8's); and a test asserting on logging
can be silently vacuous if an earlier test left a MagicMock in a module global
([[mc8-async-hardkill-16jul]] §6.1).

**4. ⭐ The VERIFICATION QUERY was self-referential** (20-Jul, Monday checklist A3). `expected_reset =
-(SUM(pnl_delta)-SUM(costs))` summed **over all rows for the date — including the `RESET_PNL` row whose
`pnl_delta` IS the reversal of that sum** ⇒ collapses to `0.0`, compared against `RESET_PNL.amount` which is
`0.0` because a P&L reset moves no capital. **`0.0 == 0.0` for structural reasons.** Its companion
(`ledger_pnl == trades_net`) could *never* hold on a trading day, for the same reason. Correct forms: exclude
the reversal row (`Σ pnl_delta WHERE entry_type != 'RESET_PNL'` == `Σ trades.net_pnl`, held to the paisa at
−18.29), and read the Option-B signature from `RESET_PNL.pnl_delta` (+19.61), **not** `.amount`. **A check
that aggregates over its own output is vacuous — exclude the row the check is about.**
[[monday-post-session-clean-20jul]]

**5. ⭐⭐ THE GATE WAS POISONED BY THE ARTIFACT THE CHANGE EXISTS TO PREVENT** (27-Jul, the `logs/`+`reports/`
write guard). A full BASE-vs-AFTER gate came back clean — **13F → 14F, exactly ONE new failure**, and that one
was the guard correctly catching real pollution. It looked finished. **It was wrong: 4 tests in
`test_interactive_startup.py` were broken and PASSED ANYWAY.** `main.py:1752` reads
`if not sentinel.exists()` before writing `logs/.holiday_notified_<date>` — and that file **already existed,
written at 15:01 by an EARLIER RUN THE SAME DAY.** The branch containing the guarded write never executed, so
the guard was never reached. Deleting the marker and re-running turned 0 failures into **4**.
⛔ **THE SHAPE: a guard's own gate is invalidated by the side effect it was built to stop.** The artifact is a
stale baseline wearing a different hat — and it is DATE-scoped, so it would have surfaced the NEXT morning as
an unexplained 14F→18F "regression" with nothing in the diff to explain it.
⭐ **RULE: before gating an isolation guard, DELETE the artifacts it prevents, then measure.** More generally —
**if a test's outcome depends on a file a previous run created, the run is not repeatable and its green is
not evidence.** Sibling of the time-of-day flip in [[feedback-no-fixed-test-baseline]]; same family as #2.
⭐ The same run settled a design question by measurement: the guard was raising `RuntimeError`, which escaped
production's deliberate `except OSError: pass` around that best-effort write. **Base an isolation guard's
exception on the class production already handles**, or the guard silently overrides a decision production
made on purpose.

**6. ⭐⭐ THE GATE RETURNED THE RIGHT EXIT CODE WITHOUT EVER REACHING THE CODE UNDER TEST** (30-Jul, the T2
close rehearsal). The deploy card mandated: re-run the close on the deployed tree with the confirm flag
OMITTED ⇒ expect `EXIT=2`, and its stated purpose was *"it proves `load_all()` still succeeds against
tonight's `config_auditor.py`"*. **EXIT=2 came back exactly as specified — and proved nothing about
`load_all()`.** Read from source: `t2_cnc_gtt_realtest.py` `main()` does `if not args.confirm: return 2`
**before** calling `_build_live_adapter()`, and `load_all()` lives *inside* that function (`:157`). The
refusal text names WHICH guard fired (the confirm guard, not market-hours), so the short-circuit is
measured, not inferred. ⇒ The fix was a SECOND check: run `load_all()` directly on the deployed tree
⇒ `CONFIG_LOAD_OK`. That, not the exit code, closed the coupling.
⛔ **THE SHAPE: an early-return guard sits between the entry point and the thing you meant to exercise.**
The exit code is real, the refusal is real, and the gate is still vacuous. Distinct from #5 (an artifact
poisons the gate) — here the gate's own control flow never arrives.
⭐ **RULE: for any gate justified as "this proves X still works", trace the call path from entry to X and
confirm X is actually REACHED on the path the gate takes.** A gate is only evidence for the code it
executes. ⚠️ And when a doc's *rationale* overreaches while its *observable claim* is correct, say so
precisely: the operator card here claimed only "ssh, env, PYTHONPATH, venv, script path and argparse
confirmed good" — which was TRUE. It was the deploy file's reasoning that overreached, not the card.

**⚠️ AND THE BROADER ONE: validating QUERIES does not validate EXPECTATIONS.** The same checklist was
schema-validated (16 SQL executed read-only, 1 column fixed) and still shipped **4 wrong prose expectations**
(`eod_self_exit`, this A3 pair, `state=INACTIVE` at close, "403s only before 10:00") — because prose is the
part nobody validated, and a wrong expectation fails silently *in the direction of crying wolf* on a healthy
system. **Ask of every GOOD/BAD clause: is this a measured fact, or something I assumed?** Sibling of
[[feedback-verify-the-finding-premise]].

**Why:** during the 16-Jul deploy, two PowerShell gates silently misfired:
- `git rev-parse deploy-16jul-alertwatcher-f1^{commit}` → PowerShell parses `^{...}` as a **scriptblock**
  → git never ran → the follow-on `if ($?)` printed a **false "TAG NOT IN MAIN => STOP"** (a fabricated
  STOP on a healthy repo).
- `git diff --name-only $tagsha..HEAD` → PowerShell's **`..` range operator** mangled the argument → git
  exited with a usage error → my `if ($code)` read the empty output as "no code changed" and printed a
  **false PASS on the single most important gate of the deploy** (is the deployed code identical to the
  validated tag?).

Both failure modes are silent and point in *opposite* directions — one would have aborted a good deploy,
the other would have waved through a bad one. Neither is caught by reading the output.

**How to apply:**
- Run git ancestry/range/rev-parse checks under the **Bash** tool (`git rev-list -n 1 <tag>`,
  `git merge-base --is-ancestor A B`, `git diff --name-only "A..B"` with the range **quoted**).
- In PowerShell, never leave `^{}`, `..`, `@`, or `~` unquoted in a git argument; test `$LASTEXITCODE`
  explicitly — `$?` reflects PowerShell's own parse/exec, not git's verdict.
- Make the assertion positive and self-evidencing: `grep -v '\.md$' && echo STOP || echo EMPTY` prints
  which branch it took, so an errored command cannot masquerade as a clean result.
- Same family as [[feedback-vm-curl-tests]] (PowerShell escaping breaks JSON) and
  [[feedback-vm-script-transfer-base64]]. Also: multi-line single-quoted `ssh '...'` blocks hit
  "unexpected EOF" — prefer short, separate ssh calls.

See [[deploy-alertwatcher-f1-done-16jul]]
</content>
