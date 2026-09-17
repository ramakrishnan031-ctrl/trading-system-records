# S&R SHADOW v1.3 — TESTING-VM DEPLOY MANIFEST (STANDALONE COPY, OUTSIDE GIT)

**Preserved:** 2026-09-16T1820 IST, per the 16-Sep "DEPLOYMENT CARD AMENDMENT 4" §1.
- **Save it with the cards.**
- **Tracked twin:** `D:/Projects/trading-system/docs/SYSTEM_MAP.md`, sections `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` (~01:12, amended ~01:25, ~01:40 and ~02:09) and the 16-Sep amendment entries.
- ⚠️ That twin is tracked but UNCOMMITTED: `git checkout -- .` or `reset --hard` destroys it. This file is the copy that survives.
- ⛔ **If the two ever differ, the later timestamp wins, and the difference is reported.**
- ✅🔝 **THIS VERSION RECORDS THE GATE 1 RESULT: V2RETAIL RAN 16-Sep **08:26 IST** AND **PASSED** (full entry at the end).** ⛔ **A resuming session must NOT re-run it** — it is specified as ONE read-only run and the broker calls (`instruments=1 historical_data=1`) are already spent. Gates 2–9 have NOT run; ⭐ the VM is still UNCHANGED.
- ⛔🔴 **AMENDMENT 9 IS IN THIS VERSION.** Two things a reader must not miss: ① **GATE 3 IS NOT TO BE WIDENED** — its strictness is the barrier; after a partial transition, **STOP and adjudicate the actual VM state**. ② **IF THE SERVICE HAS NOT SELF-EXITED, DO NOT STOP IT** — record `is-active`/uptime/last logs and abandon the window. Plus the operator **STOP table**, and the Gate 1 **near-miss** now recorded beside the defect note.
- ⏰⛔🔴 **AMENDMENT 10 IS IN THIS VERSION. ONE ACTION IS OWED TONIGHT AT GATE 2, BEFORE ANY WRITE: PRESERVE TODAY'S BOOT LOG** (journal **and** `logs/system_2026-09-16.log`) **as the Gate 7/8 baseline, then md5-freeze both.** ⭐ Tomorrow's comparison is against a **file, not a memory**. Also: self-exit is adjudicated **from evidence, never the clock** (three cases; ⚠️ after 16:00 the watcher cannot fire in any of them, so case 3 is ⛔ **not** a safety stop), and the stop reason in case 3 is **ATTRIBUTABILITY, ⛔ not safety**.
- ⛔⚠️ **AMENDMENT 11 CORRECTS A CLAIM MADE IN THE 0946 VERSION.** The `KillSignal=SIGINT` mechanism does ⛔ **NOT** block tomorrow's start after a 17:42 stop — 🔬 both a 17:35 self-exit and a 17:42 manual stop date the clean exit **16-Sep**, and on 17-Sep both read as *"a prior day"*. ⭐ **It bites the DAYTIME ROLLBACK (08:15–16:00) instead**, where it silently keeps the twin down for the rest of the session. ⭐ **Tonight's real hazard is EVIDENCE: a still-ACTIVE service is a FINDING to preserve, ⛔ not resolve** — a manual stop would make the anomaly look normal.
- ✅⭐ **AMENDMENT 12: THE EXPECTED DIFF FOR TOMORROW'S BOOT IS ALREADY PRE-REGISTERED AND FROZEN** — `EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_2026-09-16T1007IST.md` (5,321 B, md5 `b5f7019c30095c1e536578f695a38710`), written **10:07 IST, ~7.5 h before the window, from committed code, ⛔ with no VM contact**. ⛔ **Gate 2 only re-verifies its md5; it does ⛔ not create it, and it is ⛔ NEVER amended after seeing tomorrow's log.** Gate 2 is also now **conjunctive** (INACTIVE **and** clean exit **and** healthy session) and **capture-first**.
- 🔴⚠️ **AMENDMENT 13 CORRECTED THE PREDICTION BEFORE IT COULD DO HARM.** 🔬 **The journal carries `WARNING`+ ONLY** (`core/logger.py:420`; the unit sends stdout → journal) ⇒ the three sr_shadow **INFO** "must appear" rows live **ONLY** in `logs/system_<DATE>.log`. ⛔ **Looking for them in the journal would have declared "the manager did not come up" and stopped a CORRECT deployment.** ✅ **Prediction v2** now carries a **SINK MAP**, and the **normalization ruleset** is its own frozen file. ⭐ **Correction is allowed BEFORE the first VM write, ⛔ never after** — v1 is kept.
- 🔴⭐ **AMENDMENT 14: THE NORMALIZER WAS CALIBRATED ON A KNOWN-ANSWER DIFF AND IT WAS WRONG.** 🔬 15-Sep vs 16-Sep boots (no code change) left **13** differing events under ruleset v1 — **five dynamic families were missed** and are now R3.4–R3.8. ⭐ **Measured noise floor = 3**, from two REAL variance families (`check_ntp_sync` INFO↔WARNING, `email_fallback.sent`) — ⛔ not normalized. ⭐ **Composition prediction is now LITERAL: 62/62 → 63/63.** ⚠️ **Substring trap:** three sites emit *"ENABLED and started"* and sr_detector's is already in the baseline ⇒ **match the FULL msg**. ✅ **Every E-4 row now states its observability (A7) — all ERROR/CRITICAL ⇒ none vacuous.**
- ⛔🔴 **AMENDMENT 15: SINK AUTHORITY IS BY *ORIGIN*, NEVER BY LEVEL.** Application events ⇒ the **application log** always; systemd lifecycle ⇒ the **journal**. 🔬 `check_ntp_sync` flips INFO↔WARNING, so journal-to-journal it would **appear from nowhere and vanish again** — ⭐ the event never moved, its **visibility** did. This **eliminates the level-flip artefact class**. ⛔ **E-4 rows are checked in the application log.** ⛔ **"3" is NOT a budget** — recognition is by **FAMILY IDENTITY**, never by count. ⭐ **Composition: 62/62 → 63/63.**
- ⛔🔴 **AMENDMENT 16: THE NORMALIZER'S EXIT CODE INVERTS TOMORROW AND CARRIES NO VERDICT.** 🔬 Simulated: a **CORRECT** deploy ⇒ rc **1**; a **FAILED** one ⇒ rc **0**. ⛔ And it **cannot detect a MISSING event at all** — absence yields no difference. ✅ Closed by giving the Gate 7/8 record **no field for its verdict**, only a residual list. ✅ The family classifier is now **anchored** (fragment matching gave a **silent FALSE GREEN**), and **any unparseable line is a FINDING**.
- ✅⛔ **AMENDMENT 17: THE WINDOW.** ✅ Both delimiters are **semantic**, so the window **grows with the boot** — a positional one would have **manufactured phantom MISSING events out of the deployment itself**. 🔴 **But a boot-window-only E-4 check would have been VACUOUS BY WINDOW:** `drain error` comes from a **background thread** and can fire long after the end marker. ✅ Each row now has its own window. ✅ **Gate 4-PRE** re-checks artifact identity immediately before the first write. ⚠️ Evidence boundary stated; **raw test outputs kept**.
- ⛔🔴 **AMENDMENT 18: THE IDENTITY GATE WOULD HAVE CERTIFIED THE WRONG SET.** 🔬 v6's own identity step named the **superseded** artifacts — and every superseded file is **kept on disk**, so verifying them **matches** ⇒ ⭐ **the gate would have reported GREEN against the wrong identity.** ✅ **Structural fix: the PREDICTION is DATA, the MANIFEST is PROCEDURE, never both** — the prediction now points at the manifest **by section name, never by version**. ✅ A **missing end marker** is now itself a finding.
- ⛔🔴 **AMENDMENT 19: THE MARKER GUARD WAS `>= 1` AND PASSED THE TWO-BOOT CASE** — now **`== 1`** on both markers and both windows, **mechanically enforced by a frozen validator** (7 non-vacuous cases). 🔴 **AND THE EOD WINDOW HAD NEVER BEEN SPECIFIED**, though E3.5/E4.9 are assigned to it: **`Shutdown initiated` → `Shutdown complete`**, both semantic, with the end marker **after `sr_shadow.stop()`**. ⛔ **`WINDOW_INVALID` precedes every residual.**
- ⛔🔴 **AMENDMENT 20: THE EOD EVALUATOR HAD NO PREDICTED OBSERVABLE.** Gate 6 installs a cron job; Gate 7/8 never looked for it. ✅ **It CANNOT reach the application log** — it calls `get_logger` but **never `setup_logging`**, so in that separate process root has no handlers and only WARNING+ reaches stderr. ⇒ its only sinks are the **cron log** and the **shadow DB**, and ✅ **E4.10 is unaffected**. Class **E-6** added. ⚠️ **The exit status is NOT observable post-hoc** — named, not closed.
- ✅⛔ **AMENDMENT 21: E-6 CLOSED.** The process rc is **not captured and not to be added** — redundant against the cron log's three states, and **the evaluator is inside the FROZEN SET** (one of the 17 copy files, md5 `edebd2d8…`). ✅ **Verified by code read: EVERY non-crash exit path emits the summary line, including the REFUSED path** ⇒ the feared false-red does not exist. ⛔ **Never call `setup_logging()` in the evaluator** — the process separation is what protects E4.10.
- ⛔🔴 **AMENDMENT 22: AN ABSENCE-INFERENCE OF MY OWN, CORRECTED.** *"No content ⇒ the cron never fired"* is **wrong**: summary absent + no traceback ⇒ **EXECUTION NOT PROVEN**, equally consistent with a kill before output, a shell/process-boundary failure, an environment fault, or the cron daemon. ✅ **No E-6 completion evidence ⇒ NOT PROVEN; the CAUSE is classified separately.** ⚠️ Also recorded for LATER: from run 2 a crashed run's traceback lands in the **next** run's block, and a traceback carries **neither timestamp nor target_date**.
- **Supersedes** `…T1314IST.md`, which superseded 1302, 1231, 1212, 1156, 1140, 1125, 1049, 1027, 1009, 0958, 0946, 0903, 0829, 0735, 0210, 0156, 0145 and 0128. **This version adds AMENDMENT 8**, applied ~07:21–~07:35 IST: (a) every guarded write is now **IDEMPOTENT** — the precondition has THREE outcomes (`ALREADY_DONE` / proceed / `REFUSED_DRIFT`), so a re-run is no longer indistinguishable from drift; (b) **every command is labelled `RUNNABLE — LITERAL COMMAND` or `TEMPLATE — DO NOT RUN`**, and the ones that mattered are now literal — **20 runnable commands, 0 placeholder tokens, all 20 parse under `bash -n`**; (c) 🔴 a recorded **FINDING**: Amendment 8 §2's claim that the whole sequence becomes re-runnable from the top is true at file level but ⛔ **NOT at sequence level — Gate 3 still STOPs on a second pass**; recorded, ⛔ not fixed. The 0210 version added Amendment 7: every boot-path write (Gates 4c–4f, Gate 5, every rollback restore) becomes a guarded write-then-rename with the md5 checked BETWEEN `cat` and `mv`; Gate 3 gains rename preconditions; and the PRE and POST YAML copies are preserved outside git.
- **Companion files in this folder:** `TWIN_system_config_PRE-SR-SHADOW_md5-351bd82e__preserved_2026-09-16T0208IST.yaml` and `TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml`. Keep them with this manifest; Gate 5 and the rollback read them.
- ⭐ **NEW COMPANION (Amendment 8):** `SR_SHADOW_GATE1_capture_wrapper_md5-dc9476f3__preserved_2026-09-16T0731IST.py` — 3,438 bytes, md5 `dc9476f3e43bbe64b161ed151e973a56`. ⚠️ **The approved Gate 1 wrapper was NOT a file anywhere** — it existed only as the fenced listing inside the manifest. 🔬 Extracted ~07:30, verified to reproduce the approved md5 exactly, and it compiles. Gate 1 step 3 now reads it by that literal path.
- ⚠️ **Time-label correction:** the 0128 version's section labels ran AHEAD of the system clock (e.g. "~01:30", "amended ~01:50"). Measured clock readings put the writes at: manifest ~01:12 · Amendment 3 ~01:15 · `tar -t` check ~01:20 · Amendment 4 ~01:25 · Amendment 5 ~01:40. The tracked SYSTEM_MAP copy is corrected, as is this file. The section IDs (`MANIFEST-…`, `RESULT-…-AMENDMENTn-…`) are the stable references.
- **Precedence inside this file,** where the verbatim notes below differ: the manifest's **Gate 4** (ordered copy) and **Gate 7/8 rollback** (block first, then the four files in reverse copy order, ⛔ no deletion of `sr_shadow/`), amended ~01:25, ~01:40 and ~02:09, supersede the ~01:05 ordered note, which in turn supersedes the order in the ~01:00 atomic note. The content of all three agrees; only the ordering was refined.

**Code:** commit `e7bf477` on `feat/sr-shadow-v1.3-15sep` (worktree `D:/Projects/wt-sr-shadow-15sep`, parent `970aabf`). ⛔ Unamended, ⛔ unpushed, ⛔ never `main`.

**Scope:** COMMIT 27 files · VM DEPLOYMENT 17 files · VM-LOCAL CONFIG = the `sr_shadow:` block, copied back as a validated file. TESTING VM `130.210.13.114` (`trading-sbx`) ONLY; ⛔ production untouched.

**Cards this manifest implements:** "S&R SHADOW v1.3 — DEPLOYMENT AND FIRST SESSION" and Amendments 1–7 (all 16-Sep).

---
## 16-Sep-2026 (Wed) ~01:12 IST — `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` — ⭐ THE TRACKED DEPLOY MANIFEST (Amendment 3 §3) · TESTING VM ONLY

**Why here:** the build report is UNTRACKED and the schedule exists only as in-session timers. This file is tracked. ⚠️ It is also uncommitted in the main tree, so it survives `git clean` but ⛔ not `git checkout -- .` or `reset --hard`. A second copy of the essentials is in the memory ledger.

### ⛔ RESUME RULE
- **Nothing runs by itself.** ⚠️🔴 **CORRECTED 16-Sep ~14:10 (Amendment 26 §1): the timer list previously written here (08:27 · 17:42 · 17-Sep 08:27 · 17:47) was STALE and named timers that do not exist.** ✅ **EXACTLY ONE in-session timer is armed: 17:30 IST on 16-Sep, armed 09:00.** It dies with the Claude session; ⛔ it is not VM cron and ⛔ not evidence.
- ⛔🔴🔝 **ACTIVE *BEFORE* THE EXPECTED SELF-EXIT IS NORMAL — ⛔ IT IS NOT A FINDING. ACTIVE *AFTER* THE EXPECTED SELF-EXIT IS A FINDING (Amendment 28 §3).** ⭐ **The clock decides WHEN TO LOOK; ⛔ it NEVER decides WHAT THE STATE MEANS.** ✅ **At 17:30 do only the parts that do ⛔ NOT depend on service state** — open the manifest · starter inventory · artifact identity by role. ✅ **THEN WAIT FOR EVIDENCE OF THE SELF-EXIT.** ✅ **Only then run the three-case adjudication.** ⚠️ Adjudicating at 17:30 reads ACTIVE because the service **has not exited yet**, and would ⛔ **FALSE-STOP a healthy deployment for being five minutes early.**
- ⛔🔴🔝 **WHETHER AN IN-SESSION TIMER SURVIVES AUTO-COMPACTION IS *NOT ESTABLISHED*.** ⭐ **Assume it does NOT fire.** ⚠️ **The 17:30 reminder must live somewhere OUTSIDE the Claude session** — a timer nobody has tested is ⛔ **not a control**. ✅ **This file is the resume path and needs no session history.**
- ⛔⭐🔝 **AN ALARM IS A REMINDER, ⛔ NOT THE PROCEDURE** (Amendment 11 §4). **THIS MANIFEST AND THE LEDGER ARE THE AUTHORITY**, and both are current. ⚠️ The 17:30 timer armed 16-Sep 09:00 carries **STALE TEXT** — it describes the pre-Amendment-10 sequence and **omits the Gate 2 baseline capture**. A re-arm was **denied**, so it stands. ⭐ **That is a documentation mismatch, ⛔ not a deployment risk — provided nobody reads an alarm's text as the instruction.** ⛔ **Do not retire a timer that fires on time in order to fix its wording**: losing a working timer to correct text nobody should treat as authoritative is a bad trade. ⭐ If a replacement is ever armed, **arm it BEFORE retiring the old one.**
- If the session closes, a **fresh session resumes from THIS MANIFEST**, starting at the first gate below **without a recorded result**. ⚠️ **CORRECTED: the cards are now the deploy card plus Amendments 1–26, ⛔ not "1–3"** — but ⭐ **this file is self-sufficient for the four resume questions and the cards are context, ⛔ not a prerequisite.**
- **Authority:** 👤 Rama's 16-Sep ~00:20 answer (all four; order 4 → 1 → 2–3 only if 1 passes), recorded as a delegated answer. ✅ Item 4 is done: `e7bf477`.
- ⛔🔴🔝 **THE FIRST VM WRITE IS A *STATE TRANSITION*, ⛔ NOT A TIMESTAMP (Amendment 26 §4) — AND ITS CURRENT STATE IS DECLARED HERE:**
  - **HAS IT OCCURRED?** ⛔ **NO. AS AT 16-Sep 14:10 IST THE FIRST VM WRITE HAS NOT OCCURRED.**
  - **WHICH ARTIFACT SET WAS WRITTEN?** — **NONE.** No artifact set has been written to the VM.
  - **WHAT VERIFICATION WAS PERFORMED?** — **NONE on the VM.** The only VM contact all day was Gate 1's single read-only run (08:26) plus read-only log fetches; ⭐ **nothing was written.**
  - ⭐ **A cold reader must not confuse "expected" with "already happened".** Until this block says otherwise, **Gate 4-PRE and the guarded writes have NOT been performed** and **the artifact set is NOT frozen** — see the two-interval rule.
  - ⚠️🔴🔝 **THIS DECLARATION IS DATED EVIDENCE, ⛔ NOT A CURRENT STATE (Amendment 27 §2).** At 17:30 a cold reader is looking at a line **three hours old**: it establishes what was true at 14:10, ⛔ **it cannot establish what is true when they read it.**
  - ✅⭐🔴 **AND IT DOES NOT NEED TO — THE PROCEDURE RE-PROVES IT:** ✅ **the state declaration is a HINT that orients a cold reader** · ✅🔝 **GATE 3'S ABSENCE CHECK IS THE PROOF** (`sr_shadow/` and `scripts/sr_shadow_evaluate.py` must both read **ABSENT**, and the `sr_shadow_evaluate` crontab count must be **0**) · ⛔🔴 **IF THE TWO EVER DISAGREE, THE VM WINS AND THE DEPLOYMENT STOPS.**
  - ⭐ **So the resume path does ⛔ NOT depend on a trusted timestamp.** ⭐ This converts the last remaining *"trust a recorded value"* into *"verify at the gate"* — the pattern everything else in this manifest already follows.
- ✅🔝 **THE CURRENT ARTIFACT SET, so a cold reader is not misled by superseded copies kept on disk:** the identity command in Gate 2 ⑥ and Gate 4-PRE is **the only authority**. Superseded predictions, rulesets and normalizers **remain on disk deliberately and WILL verify clean against their own hashes** — ⛔ **that is not evidence they are current.**
- **Result so far:** ✅ **GATE 1 RAN 16-Sep 08:26 IST and PASSED** (entry below). ⛔ Gates 2–9 have NOT run. ⭐ **The VM is still UNCHANGED** — Gate 1 is read-only and wrote nothing on it; `0` bytes of stderr.

### ⛔🔝 THE ONE UNSAFE CELL, AND THE STARTER RULE (applies to deploy AND rollback; added ~01:55 per Amendment 6 §2)

**The cell (Amendment 6 §2, verified row by row ~01:55):** among states made of COMPLETE files, both ordered procedures visit exactly one unsafe configuration, the same cell from either side:

> **NEW `config/expected_managers.yaml` PRESENT + `sr_shadow:` BLOCK ABSENT**

- The deploy enters it at Gate 4f, before Gate 5; the rollback enters it after removing the block, before restoring the registry (R0).
- No ordering removes it: going the other way lands on the unexpected-manager cell (block present + old registry ⇒ `unknown`, `effect_telemetry.py:182`).
- **The card's rule, verbatim:** *"from the moment `expected_managers.yaml` changes until the YAML block matches it, the service must not start."*

**⛔ The operative starter rule is WIDER.** The card's rule covers only complete-file states, and a transfer can leave a PARTIAL file:
- 🔬 PC demo, GNU tar 1.35 (~01:55): an existing `970aabf` `main.py` (208,758 bytes, md5 `85219d22`) was overwritten by `git archive e7bf477 main.py | head -c 150000 | tar -x` (tar rc=2, "Unexpected EOF").
  - It was left as a **147,968-byte file** (md5 `4041aad9`) that still **COMPILES** but has **no `if __name__ == "__main__":`** (`main.py:4319` of the full file).
  - ⇒ The old file does NOT survive an interrupted copy.
  - 💭 Started, it would define its functions and **exit 0 having done nothing**: `Restart=on-failure` ignores exit 0, and the watcher skips a same-day clean exit (📄 memory, 05-Aug) ⇒ a **silent** no-trade day.
- Partial states exist BEFORE the registry changes (Gates 4c–4e) and during every rollback restore. The checksum gate DETECTS them; only a stopped service PROTECTS until they are repaired.

> **OPERATIVE RULE:** from the first write to any boot-path file (`core/config_loader.py`, `signals/signal_processor.py`, `main.py`, `config/expected_managers.yaml`, `config/system_config.yaml`) until every written file verifies at its target md5 AND `load_all` passes on the VM, **the service must not start**. Deploy and rollback alike.

It contains the card's cell as a special case.

**Both wordings stand** (Amendment 7 §2): ONE unsafe COMPLETE-FILE cell, plus TRANSFER-INTEGRITY hazards. The latter are not a second cell, because their content depends on where the interruption fell.
- Since ~02:09 every boot-path file (Gates 4c–4f, Gate 5 and every rollback restore) is written by a **guarded write-then-rename**: bytes go to `<path>.tmp`, the md5 is checked, the mode is copied, then an atomic `mv`.
  - ⇒ A boot-path file is always either fully old or fully verified-new; the transfer-integrity hazard is removed for those files.
- The operative rule is still kept, as defence in depth: a killed transfer can leave `.tmp` residue, the rename instant exists, and an operator may deviate.

### ⛔🔝 COMMAND LABELLING · THE IDEMPOTENT GUARDED WRITE (Amendment 8, applied ~07:29–~07:33 IST 16-Sep)

⚠️ **Time-label correction (same class as the 0128 one, caught the same way):** this pass's first draft labelled its own work `~07:35 / ~07:40 / ~07:45 / ~07:55 / 0800`, **ahead of the system clock.** 🔬 Corrected against artifact mtimes: guard contract demo **07:21** · round-trip rehearsal **07:27** · wrapper extracted **07:30**, preserved **07:31** · manifest amended **07:29–07:33** · standalone copy **07:35**. ⭐ The section IDs are the stable references, ⛔ not the time labels.

**§3 — EVERY command in this manifest now carries one of two labels, and the label is part of the command.**

| Label | Meaning |
|---|---|
| **`RUNNABLE — LITERAL COMMAND`** | literal paths, literal digests, no placeholders. Safe to paste as-is. |
| **`TEMPLATE — DO NOT RUN`** | contains `<...>` or `…`. It explains a SHAPE. ⛔ Pasting it is an incident. |

- 🔬 **Why:** the **02:08 incident** was a command containing `<path>` / `<validated file>`, written to explain a fix and then typed as if runnable. ⭐ **Nothing was written — the shell was still waiting on the unmatched quote.** ⛔ Not a Gate 5 event · ⛔ no VM state change · ⛔ no rollback. 👤 Authorship of the defective command was accepted by the card's author, 16-Sep.
- ⛔ **Mechanical criterion for a RUNNABLE command** (so the label can be checked, not judged): `grep -oE '<[A-Za-z_][A-Za-z0-9_ .-]*>'` over the command must return **NOTHING**, and it must contain no `…`. A genuine shell redirect (`< path`, `> /dev/null`) is not a placeholder and is allowed.

**§2 — every guarded write is now IDEMPOTENT: the precondition has THREE outcomes, not two.**

⛔ **THE TRAP THIS REMOVES.** An inline current-md5 precondition (ChatGPT §6 — adopted, and right) FAILS on a second run: the file is at the TARGET md5, not the EXPECTED-CURRENT one, so the guard prints `REFUSED` and exits 1 — **output identical to genuine drift.** ⇒ An operator re-running a rollback at 08:10 because they are unsure how far it got sees `REFUSED` and ⛔ **cannot tell "already done" from "something is wrong."** ⭐ That is the worst possible moment for an ambiguous error.

**THE CONTRACT — FOUR terminal states. ⭐ The target is NEVER left partial in any of them.**

*(`EXPECTED-CURRENT` and `TARGET` are used instead of old/new because the two directions swap them: deploying, EXPECTED-CURRENT is the `970aabf` md5 and TARGET the `e7bf477` md5; rolling back, they are exchanged.)*

| `md5(P)` on entry | Stream | Prints | rc | Effect on `P` |
|---|---|---|---|---|
| **EXPECTED-CURRENT** | complete | `WROTE <p>` | **0** | replaced, verified at TARGET |
| **EXPECTED-CURRENT** | short / empty | `REFUSED_WRITE <p>` | **1** | ⭐ **untouched, still EXPECTED-CURRENT**; `.tmp` removed |
| **TARGET** | (drained) | `ALREADY_DONE <p>` | **0** | untouched — already correct |
| anything else, **incl. absent** | (drained) | `REFUSED_DRIFT <p> have=… want=…` | **1** | untouched |

- ⭐ `ALREADY_DONE` and `REFUSED_DRIFT` are now **DISTINGUISHABLE**. `REFUSED_WRITE` is Amendment 7's behaviour, deliberately KEPT — a bad stream must still refuse.

**⛔🔝 THE OPERATOR STOP TABLE (Amendment 9 §3, ADOPTED) — so that ⛔ no non-zero result is ever read as *"probably already done"*:**

| rc | output | action |
|---|---|---|
| `0` | `WROTE` | continue, **after the independent post-check** |
| `0` | `ALREADY_DONE` | continue, **after the independent post-check** |
| `1` | `REFUSED_WRITE` | ⛔ **STOP** |
| `1` | `REFUSED_DRIFT` | ⛔ **STOP** |
| `*` | **anything else** | ⛔ **STOP** |

- **On ANY stop, record:** gate · command · rc · stdout · stderr · **the observed md5 state of EVERY file touched in that gate.** ⛔ **Do not proceed on inference.**
- ⚠️ **`bash -n` proves SYNTAX, ⛔ not that the host, path, permissions or digests are right.** ⭐ Those are Gates 2–5, on the VM. A command that parses can still be pointed at the wrong machine.
- ⭐ Both early-exit paths run `cat > /dev/null` to **DRAIN the inbound stream**, so the local `git show` is not killed by SIGPIPE and the ssh exit status is the guard's own.

**THE SHAPE — `TEMPLATE — DO NOT RUN`** (every literal instance is in Gate 4, Gate 5 and the rollback below):
```
cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < <PATH>; } 2>/dev/null | cut -c1-32); if [ "$cur" = "<TARGET>" ]; then cat > /dev/null; echo "ALREADY_DONE <PATH>"; exit 0; fi; if [ "$cur" != "<EXPECTED-CURRENT>" ]; then cat > /dev/null; echo "REFUSED_DRIFT <PATH> have=${cur:-NONE} want=<EXPECTED-CURRENT>"; exit 1; fi; cat > <PATH>.tmp && [ "$(md5sum < <PATH>.tmp | cut -c1-32)" = "<TARGET>" ] && chmod --reference=<PATH> <PATH>.tmp && mv -- <PATH>.tmp <PATH> && echo "WROTE <PATH>" || { rm -f -- <PATH>.tmp; echo "REFUSED_WRITE <PATH>"; exit 1; }
```

🔬 **DEMONSTRATED ON THE PC (~07:21 IST, this exact shape, ⛔ not a paraphrase)** — fixtures EXPECTED-CURRENT `2534db9f…`, TARGET `bdf16cfe…` (6,715 B); six cases, each rc and each post-state read back:

| Case | Result | rc | Target after |
|---|---|---|---|
| EXPECTED-CURRENT + full stream | `WROTE` | 0 | TARGET, no `.tmp` |
| ⭐ **immediate RE-RUN** *(the Amendment 8 case)* | `ALREADY_DONE` | 0 | TARGET, unchanged |
| drifted target | `REFUSED_DRIFT have=168c5903… want=2534db9f…` | 1 | unchanged |
| EXPECTED-CURRENT + 3,000-of-6,715-byte stream | `REFUSED_WRITE` | 1 | ⭐ **still EXPECTED-CURRENT**, no `.tmp` |
| EXPECTED-CURRENT + empty stream | `REFUSED_WRITE` | 1 | still EXPECTED-CURRENT |
| target **ABSENT** | `REFUSED_DRIFT have=NONE` | 1 | — · ⭐ **0 bytes of stderr** |

- ⭐ The absent-file case is why the precondition read is wrapped `{ md5sum < P; } 2>/dev/null`: the bare form leaked a shell redirect error to stderr. It **reports**, it does not leak, and it is ⛔ never silent.
- ⚠️🔬 ⛔ **MODE PRESERVATION IS *NOT* PROVEN BY THIS DEMO — THAT CHECK WAS VACUOUS.** Windows did not honour `chmod 600` on the fixture (`stat -c %a` read **644 before AND after**) ⇒ `chmod --reference` **could not have been observed failing**. ⭐ The real protection is the **VM-side `stat -c %a` check after every write**, ⛔ not this demo. Limit inherited unchanged from Amendment 7.

**⭐ WHAT THIS BUYS — AND ITS EXACT LIMIT, WHICH IS NOT WHAT THE AMENDMENT CLAIMS.**

- ✅ **At the FILE level the claim holds:** a fresh session resuming from this manifest does **not** need to know which files landed. It re-runs the writes in order; each either proceeds or reports `ALREADY_DONE`, and only real drift stops it.
- 🔴⛔ **At the SEQUENCE level it does NOT hold yet, and GATE 3 IS WHY.** Gate 3's preconditions are *absence* and *pre-state* checks that a partially-completed run has **already falsified**. On a second pass they STOP — ⭐ **the very two-outcome trap Amendment 8 removed from the writes, surviving one gate earlier:**

  | Gate 3 precondition | After a partial first run | Re-entry verdict |
  |---|---|---|
  | `sr_shadow/` and `scripts/sr_shadow_evaluate.py` must NOT exist | 4a/4b landed them | ⛔ STOP |
  | the 4 wiring md5s must equal `970aabf` | any of 4c–4f landed | ⛔ STOP |
  | `config/system_config.yaml` = `351bd82e…` | Gate 5 landed | ⛔ STOP |
  | crontab must not contain `sr_shadow_evaluate` | Gate 6 landed | ⛔ STOP |

- 🏷️ **STATUS — the two claims are labelled separately, ⛔ never merged:** the write-level fix is **BUILT + 🔬 DEMONSTRATED (PC)**; *"the whole transfer sequence is re-runnable from the top"* is **⛔ NOT YET TRUE**.
- ✅🔝 **SETTLED BY AMENDMENT 9 §1 — ⛔ THIS IS NO LONGER AN OPEN QUESTION, AND ⛔ GATE 3 IS NOT TO BE WIDENED.** 👤 The card's author withdrew the over-strong §2 claim and replaced it with the wording below, which supersedes it in this manifest:
  > *Each guarded existing-file write is idempotently re-runnable. The deployment SEQUENCE remains protected by Gate 3's strict pre-state barrier; after a partial transition, STOP and adjudicate the actual VM state rather than assuming a clean restart.*
  - ⛔🔴 **DO NOT WIDEN GATE 3.** ⭐ **Its strictness IS the barrier, ⛔ not a bug in it.** Making it permissive in advance would trade a **stall** for a **guess** — and a stall is exactly what you want when the VM state is unknown. If a real interruption happens: **stop and inspect the actual state.**
  - ⭐ **The per-file work still earns its place:** it is what makes a **STOPPED** sequence safe to continue **by hand, one file at a time**, once the state has been adjudicated. ⛔ It was never a licence to restart blind.

### GATE 1 — SPOT-CHECK (after the 08:15 token; decisive for everything below)
0. ⭐ **PREREQUISITE — the approved wrapper is NOT a file in the repo; it exists only as the fenced listing below.** It is now ALSO preserved outside git: `D:/Projects/_preservation/SR_SHADOW_GATE1_capture_wrapper_md5-dc9476f3__preserved_2026-09-16T0731IST.py` — **3,438 bytes, md5 `dc9476f3e43bbe64b161ed151e973a56`**. 🔬 Extracted from that listing at ~07:30 and verified to reproduce the approved md5 **exactly**, and it compiles (`py_compile` rc 0). ⛔ If the file is missing, re-extract the listing below and ⛔ run nothing until it hashes to `dc9476f3…`.
1. **Script identity on the twin.** **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum scripts/sr_corp_action_spotcheck.py'
```
   Must print **`d954c1781e55ebf68d44c9c815ef353e`**. Else ⛔ STOP.
2. **Token freshness — metadata only, ⛔ never the content.** **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && stat -c "%n mtime=%y size=%s" data_store/session/zerodha_token.json'
```
   The mtime date must be **today**. Else ⛔ STOP — a stale token makes the run meaningless.
3. **THE ONE READ-ONLY RUN.** The wrapper goes over ssh stdin; stdout and stderr are captured **separately on the PC**; ⛔ nothing is written on the VM. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && PYTHONIOENCODING=utf-8 /home/ubuntu/systems/venv/bin/python -B - scripts/sr_corp_action_spotcheck.py' < D:/Projects/_preservation/SR_SHADOW_GATE1_capture_wrapper_md5-dc9476f3__preserved_2026-09-16T0731IST.py > D:/Projects/_preservation/GATE1_V2RETAIL_16-Sep-2026.stdout.txt 2> D:/Projects/_preservation/GATE1_V2RETAIL_16-Sep-2026.stderr.txt
```
   ⛔ **ONCE.** The wrapper hard-codes the card's exact argv (`--symbol V2RETAIL --around 2026-03-25 --window 20`) and wraps the broker methods so the single `instruments()` and single `historical_data()` are **recorded, not repeated**.
4. **Adjudicate from the returned rows** (⛔ never from the script's headline, which has a known false-pass defect, see ~01:05):
   - **PASS** = sessions demonstrably BEFORE and ON/AFTER 2026-03-25, with no ~10:1 discontinuity;
   - **STOP** = a ~90% discontinuity at the ex-date;
   - **INCONCLUSIVE** = anything else, including a clean post-split-only series. ⛔ No row count is a criterion.
5. **Record:** exact command · stdout · stderr · first and last session · counts before and on/after · instrument token · ISIN if present.

<details><summary>Capture wrapper — md5 <code>dc9476f3e43bbe64b161ed151e973a56</code> (approved, Amendment 2 §4)</summary>

*⭐ This fence is a **PYTHON SOURCE LISTING**, ⛔ not a command — the TEMPLATE/RUNNABLE labels do not apply to it. It is the authoritative copy of the wrapper; the preserved `.py` in Gate 1 step 0 was extracted from it and hashes to the same `dc9476f3…`.*

```python
"""Evidence capture around the UNMODIFIED scripts/sr_corp_action_spotcheck.py.

Runs the script's own main() with the card's exact argv. Wraps the two broker
methods on the kite object the script builds, so the one instruments() call and
the one historical_data() call are recorded, not repeated. Writes nothing.
Deployment-card amendment §5 fields: first/last session date, sessions before
and on/after the ex-date, instrument token, and every field of the matching
instrument record.
"""
import importlib.util
import sys
import traceback
from datetime import date, datetime

SCRIPT = sys.argv[1] if len(sys.argv) > 1 else "scripts/sr_corp_action_spotcheck.py"
ARGV = ["--symbol", "V2RETAIL", "--around", "2026-03-25", "--window", "20"]
SYMBOL = "V2RETAIL"
EX_DATE = date(2026, 3, 25)

spec = importlib.util.spec_from_file_location("sr_corp_action_spotcheck", SCRIPT)
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

cap = {"instruments_calls": 0, "historical_calls": 0, "matches": None, "hist_kwargs": None, "rows": None}
_orig_build = sc._build_kite


def _build():
    k = _orig_build()
    if k is None:
        return None
    inst, hist = k.instruments, k.historical_data

    def instruments(*a, **kw):
        cap["instruments_calls"] += 1
        rows = inst(*a, **kw)
        cap["matches"] = [dict(r) for r in rows if r.get("tradingsymbol") == SYMBOL]
        return rows

    def historical_data(*a, **kw):
        cap["historical_calls"] += 1
        cap["hist_kwargs"] = {"args": [str(x) for x in a], **{key: str(v) for key, v in kw.items()}}
        rows = hist(*a, **kw)
        cap["rows"] = rows
        return rows

    k.instruments, k.historical_data = instruments, historical_data
    return k


sc._build_kite = _build

print("=== SCRIPT OUTPUT: sr_corp_action_spotcheck.main(%r) ===" % (ARGV,), flush=True)
rc = None
try:
    rc = sc.main(ARGV)
except BaseException:  # the evidence below must print even if the script dies after the call
    print("SCRIPT RAISED:", flush=True)
    traceback.print_exc(file=sys.stdout)
print("=== SCRIPT rc=%r ===" % (rc,), flush=True)

print("=== CAPTURED EVIDENCE ===")
print("broker calls: instruments=%d historical_data=%d" % (cap["instruments_calls"], cap["historical_calls"]))
print("instrument records with tradingsymbol=%s: %s" % (SYMBOL, "NONE CAPTURED" if cap["matches"] is None else len(cap["matches"])))
for m in cap["matches"] or []:
    print("  record:", {key: (str(v) if isinstance(v, (date, datetime)) else v) for key, v in sorted(m.items())})
print("historical_data request:", cap["hist_kwargs"])
rows = cap["rows"]
if rows is None:
    print("rows: NONE CAPTURED")
else:
    def _d(r):
        v = r["date"]
        return v.date() if isinstance(v, datetime) else v
    dates = [_d(r) for r in rows]
    print("rows returned: %d" % len(rows))
    if rows:
        print("first session: %s" % min(dates))
        print("last session : %s" % max(dates))
    print("sessions BEFORE %s: %d" % (EX_DATE, sum(1 for d in dates if d < EX_DATE)))
    print("sessions ON/AFTER %s: %d" % (EX_DATE, sum(1 for d in dates if d >= EX_DATE)))
    print("duplicate dates: %d" % (len(dates) - len(set(dates))))
    print("date        open      high      low       close     volume")
    for r in rows:
        print("%s  %-9s %-9s %-9s %-9s %s" % (_d(r), r.get("open"), r.get("high"), r.get("low"), r.get("close"), r.get("volume")))
print("=== END ===")
```
</details>

### GATE 2 — STARTER INVENTORY (Amendment 3 §2; before ANY transition, deploy or rollback)
Establish **on the twin** and record every mechanism that can start `trading-system.service`. 📄 Memory from 05-Aug (production, ⛔ re-verify here):
- `token-watcher.service` (`deploy/token_watcher.sh`, 30 s poll): starts the service only if the token date is today AND the hour is ≥ 8 and < 16 IST AND the last clean exit was a PRIOR day;
- the unit's `WantedBy=multi-user.target` (a VM reboot starts it);
- `Restart=on-failure` + `RestartPreventExitStatus`, and any drop-in (`trading-system.service.d/`, e.g. `watchman.conf`);
- any timer, any cron line, any healthcheck/watchdog that calls `systemctl start|restart`;
- plus `zerodha_morning.ps1` on the PC (manual).

**Suppression rule** (amended ~01:25 per Amendment 4 §3, the refinement from ChatGPT's review):
1. Identify the exact starter.
2. Determine whether it can fire in the window.
3. **Only if it can:** use the least invasive supported suppression.
4. Record what was suppressed, restore it exactly, and verify the restoration.

⛔ Never blind-mask an infrastructure service.

**Exposure:**
- ⭐ The token-watcher facts (no start at or after 16:00; none after a same-day clean exit) make the **17:42 window safe from it**. Re-check at 17:42.
- ⚠️ **A rollback between 08:15 and 16:00 IS exposed** to the watcher, which is the case the rollback ordering exists for.


### ⛔🔴🔝 GATE 2 (cont.) — SELF-EXIT IS ADJUDICATED FROM **EVIDENCE**, ⛔ NEVER FROM THE CLOCK (Amendment 10 §§1–2)

⚠️ **A clock reading 17:35 is not evidence that the service exited.** Record `is-active`, uptime, the **main PID**, the last service log lines, and the observed **start and exit timestamps**.

- ⛔🔴🔝 **CAPTURE FIRST, BEFORE ANY ACTION THAT COULD ALTER STATE** (Amendment 12 §2). ⭐ **The first operation after seeing ACTIVE is EVIDENCE CAPTURE** — ⛔ not a decision, ⛔ not a tidy-up, ⛔ not a stop.
- ⛔🔝 **GATE 2 IS CONJUNCTIVE: `INACTIVE` **AND** an expected clean exit **AND** a healthy session. ⭐ INACTIVE ALONE IS ⛔ NOT A PASS.** Anything less than all three ⇒ ⛔ STOP with **`BASELINE_NOT_ESTABLISHED`**.
- **Preserve without modifying the source logs**, and **record the preservation BEFORE any write**. ⭐ **Two log sources, each frozen INDEPENDENTLY.**
- ⛔ **DO NOT OVER-COLLECT** — those two sources, ⛔ not every log on the machine.

⛔🔴🔝 **ACTIVE *BEFORE* THE EXPECTED SELF-EXIT IS NORMAL — ⛔ IT IS NOT A FINDING. ACTIVE *AFTER* THE EXPECTED SELF-EXIT IS A FINDING (Amendment 28 §3).** ⭐ **The clock decides WHEN TO LOOK; ⛔ it NEVER decides WHAT THE STATE MEANS.** ✅ **At 17:30 do only the parts that do ⛔ NOT depend on service state** — open the manifest · starter inventory · artifact identity by role. ✅ **THEN WAIT FOR EVIDENCE OF THE SELF-EXIT.** ✅ **Only then run the three-case adjudication.** ⚠️ Adjudicating at 17:30 reads ACTIVE because the service **has not exited yet**, and would ⛔ **FALSE-STOP a healthy deployment for being five minutes early.**

⛔🔴🔝 **ONE ADJUDICATION CHECKPOINT: 17:42 (Amendment 29 §2). ⛔ THERE IS NO 17:36 CHECKPOINT** — ⚠️ the file previously carried **both**, and a service exiting at 17:38 (a slow DB flush; nothing wrong) would read as a **FINDING ⇒ STOP** under 17:36 and as **still waiting ⇒ proceed** under 17:42. ⭐ **The asymmetry decides it: a false stop costs a DAY, waiting six extra minutes costs SIX MINUTES.**

✅⭐🔝 **AND THE CHECKPOINT DOES ⛔ NOT CARRY THE JUDGEMENT ALONE — READ THE TWO FROZEN SHUTDOWN MARKERS, ⛔ NOT THE CLOCK.** 🔬 Both are already frozen as the EOD delimiters (Amendment 19) and already on the Gate 2 capture list: **`Shutdown initiated`** (`main.py:1631`) and **`Shutdown complete`** (`main.py:1839`). ⭐ **"Is it late?" becomes "did the shutdown START?" — which the markers answer and a clock never could.**

⛔🔴🔝 **READ THE MARKERS IN THE APPLICATION LOG — `logs/system_<DATE>.log` — ⛔ NOT IN THE JOURNAL.** 🔬 **Both markers are `_log.info(...)`, i.e. INFO from logger `main`**, and the stdout handler is `setLevel(WARNING)` (`core/logger.py:420`) ⇒ ⛔ **neither marker can ever appear in the journal.** ⚠️ **Adjudicating from `journalctl` would find NEITHER marker, read `initiated ABSENT`, and declare a FALSE CASE B ⇒ a FALSE STOP of a perfectly clean shutdown.** ⭐ **This is the E-1 defect class reappearing inside the adjudication itself — origin-based sink authority applies here too.**

- ✅ **`initiated` PRESENT + `complete` PRESENT + `is-active` inactive ⇒ CASE A · PROCEED.**
- ⚠️ **`initiated` PRESENT + `complete` ABSENT ⇒ THE SHUTDOWN IS IN PROGRESS · WAIT AND RE-CHECK.** ⛔ **This is NOT a finding, and ⛔ NEVER a reason to stop the service.** ⛔🔴 **THE WAIT HAS THREE EVIDENTIAL EXITS AND IS ⛔ NOT OPEN-ENDED (Amendment 30 §2) — ⭐ "wait and re-check" without a terminal condition is ⛔ not a rule:**
    - ✅ **`Shutdown complete` OBSERVED ⇒ the shutdown COMPLETED · proceed to the **conjunctive** check (inactive **AND** clean exit **AND** healthy session).** ⛔🔴 **`complete` ALONE IS NOT A PASS — the conjunctive check still governs.** ⭐ No clock involved.
    - ⛔🔴 **INACTIVE and `Shutdown complete` NOT OBSERVED ⇒ the process is GONE and completion was NEVER OBSERVED · STOP.** ⛔🔴 **THE CAUSE IS ⛔ NOT ESTABLISHED (Amendment 31 §2).** ⚠️ *"Died mid-shutdown"* is the **likely operational reading** — 💭 **record it as an INFERENCE and LABEL it**, ⛔ **never as the finding**: the process could equally have finished its work and been killed before the log write, or lost its buffer. ⭐ No clock involved.
    - ⛔🔴 **NEITHER, PAST THE CUTOFF ⇒ completion NOT OBSERVED WITHIN THE POLICY WINDOW · STOP.** ⛔🔴 **WHETHER IT IS HUNG IS ⛔ NOT ESTABLISHED (Amendment 31 §2)** — ⭐ absence within a bound is ⛔ **not evidence of a cause** (same rule as Amendment 22 §2: *summary absent + no traceback ⇒ EXECUTION NOT PROVEN*, ⛔ never *"the cron never fired"*).
    - ⛔🔴🔝 **THE CUTOFF IS A *DEPLOYMENT-POLICY* NUMBER — ⛔ IT IS NOT AN INFERENCE THAT THE SHUTDOWN IS HUNG, AND ⛔ IT CANNOT BECOME ONE BY BEING GENEROUS (Amendment 31 §1).** ⭐ It is **how long we are willing to hold the window open**, nothing more. ✅ **TEN MINUTES measured as a DURATION FROM `Shutdown initiated`, ⛔ NEVER a clock time like "17:52"** — a clock time would re-create the second checkpoint Amendment 29 removed.
    - ⚠️🔴 **⛔ THE EARLIER JUSTIFICATION WAS CIRCULAR AND IS WITHDRAWN.** ⛔ I wrote *"both outcomes past the bound are STOP, so a generous bound can cost the window but never correctness"* — ⭐ **that is true ONLY because the bound was defined as the point at which we stop; it assumes what it sets out to prove.** 🔴 **A healthy shutdown taking TWELVE minutes completes cleanly and is stopped at TEN — that is a FALSE STOP produced by the cutoff, and it is a CORRECTNESS cost, ⛔ not a window cost.** ✅ **Correct statement: ten minutes is ⛔ not "proof of hung"; it is the policy hold, chosen at ~158× the SINGLE measured shutdown of 3.78 s.**
    - ✅⭐🔝 **BECAUSE THE CUTOFF CAN BE WRONG, IT MUST RECORD ITS OWN COUNTER-EVIDENCE (Amendment 31 §3). WHEN THE CUTOFF FIRES:**
        - ✅ **RECORD**: service state · **main PID** · the last application-log lines · **elapsed time since `Shutdown initiated`**.
        - ✅⭐ **THEN KEEP WATCHING** — record **whether `Shutdown complete` arrives afterwards, and at what elapsed time.** ⛔ Stopping the deployment does ⛔ not mean stopping the observation.
        - ⭐ **`Shutdown complete` OBSERVED LATE (e.g. at 12 min) ⇒ establishes that ten minutes was too short *FOR THAT OCCURRENCE*.** ⛔ **It does ⛔ NOT set a new threshold.** ✅ **Revisit the policy only when enough measured durations exist.**
        - ⛔🔴 **`Shutdown complete` NEVER OBSERVED ⇒ record that COMPLETION REMAINED UNOBSERVED.** ⛔ **Do ⛔ NOT infer from that alone whether the shutdown was hung, ⛔ nor whether the ten-minute cutoff was correct.** ⚠️⭐ **"The cutoff was right" would infer a FACT FROM AN ABSENCE** — and a reviewer in week two seeing no late completions would read the cutoff as **validated** and ⛔ **stop collecting the very evidence that could show it is not.**
        - ⭐🔴 **A judgement that records its own counter-evidence becomes MEASURABLE RATHER THAN ASSUMED, and can be revisited DELIBERATELY as evidence accumulates.** ⚠️⭐ **Two observations are EVIDENCE; they are ⛔ NOT a distribution.** ✅ **This is the one place in the deployment still running on a SINGLE measurement.**
- ⛔🔴 **`initiated` ABSENT at the checkpoint ⇒ THE EOD PATH NEVER BEGAN — ⭐ *THAT* is the CASE B FINDING.**

✅🔬 **EMPIRICAL BOUND, MEASURED — ⛔ not assumed:** on **15-Sep the whole shutdown took 3.78 s** (`Shutdown initiated` 17:35:00.712 → `Shutdown complete` 17:35:04.493, exactly **1** of each). ⭐ So a **generous** wait for `complete` costs nothing, and ⭐ **a shutdown still incomplete minutes after `initiated` is itself worth stopping for.**

**THE THREE CASES AT THE 17:42 CHECKPOINT — work them explicitly:**

| Observed | Token-watcher risk | Verdict |
|---|---|---|
| **inactive**, clean 17:35 exit in the logs | **none** — the hour is 17, and the watcher requires **hour < 16** | ✅ **proceed to Gate 3** |
| **ACTIVE** | n/a | ⛔ **DO NOT STOP IT.** Record, and **STOP the deployment** (Amendment 9 §2) |
| **inactive**, but **no clean exit today** (crashed, or never started) | **also none** — the hour blocks it | ⛔ **STOP** — for the §2 reason below, ⛔ **not** for safety |

#### ⛔🔴🔝 CASE B (STILL ACTIVE) — **THE SERVICE BEING ACTIVE AT THE CHECKPOINT IS ITSELF A FINDING, TO BE *PRESERVED*, ⛔ NOT *RESOLVED*** (Amendment 11 §2)

If it is still ACTIVE at 17:42, **something is not normal**: the EOD path did not complete, or the process is stuck, or the session ran long for a reason nobody has seen yet.

> ⛔ **A manual stop would produce a log that looks EXACTLY like a clean 17:35 self-exit** — same SHUTDOWN event, same DB flush, same log lines (`KillSignal=SIGINT`). ⭐ **The evidence of WHY it was still running would be gone — overwritten by a tidy shutdown that the OPERATOR caused.**

- ⇒ ⭐ **The reason not to stop it is the same as Amendment 10 §2: ⛔ not safety — ATTRIBUTION.** A manual stop **destroys the one piece of evidence that would explain the anomaly, and it does so by making the anomaly look NORMAL.**
- ⚠️ **That is strictly worse than the watcher concern, because it is SILENT and it is PERMANENT.**
- ⇒ **Record and preserve; ⛔ do not tidy.** Capture `is-active`, uptime, main PID, the running state and the logs **as they are**, then **STOP the deployment.**

- ⭐⚠️ **NOTE THE MIDDLE COLUMN.** After 16:00 the token watcher **cannot fire in any of these cases** (its recorded condition: token date today **AND hour ≥ 8 and < 16** **AND** last clean exit a PRIOR day). ⇒ **The third case is ⛔ NOT a safety problem. Stopping there *for safety reasons* would be superstition.**

#### ⛔🔴 THE REAL REASON TO STOP IN CASE 3: WITHOUT A HEALTHY SESSION TODAY, **TOMORROW'S BOOT CHECK MEASURES NOTHING**

Gate 7/8 says to *"compare against the previous boot's log for anything else changed."* ⭐ **That comparison needs a previous boot to compare against.**

> If the twin never started today, or started and failed, there is **no healthy baseline**. Every anomaly in tomorrow's boot log then has **two candidate causes** — the deployment, or whatever was already wrong — and the gate **cannot separate them**.

- ⇒ The deployment would proceed **safely** and produce an **UNATTRIBUTABLE result.** ⭐ **That** is the failure mode worth stopping for, and it is ⛔ not about the watcher or the file state at all.
- ⛔ **If a normal session cannot be established, STOP — and say in the report that the reason is ATTRIBUTABILITY, ⛔ not safety.** Getting the reason right in the record matters as much as the stop.

#### What Gate 2 must RECORD to establish the baseline
1. the **start timestamp**, and whether it was the expected **08:15 watcher start**;
2. the **clean-exit line at 17:35, QUOTED**;
3. whether a **normal trading session** occurred — read from **the system's EXISTING routine log markers**;
   - ⛔🔴 **DO NOT INVENT A NUMERIC THRESHOLD** (Amendment 11 §3). ⭐ A signal count or a runtime minimum would be **an unvalidated parameter smuggled in through a deployment gate** — exactly what this project refuses elsewhere. Use the vocabulary the logs already have.
   - ⛔ If the routine markers cannot establish it, report **`BASELINE_NOT_ESTABLISHED`** and **STOP** — ⭐ an explicit token, ⛔ never a judgement call dressed as a number.
4. **any CRITICAL, any restart, any composition warning** during the day;
5. ⭐🔝 **the FULL boot log of today's start, PRESERVED as THE BASELINE for the Gate 7/8 comparison.**
6. ⭐🔴🔝 **THE PRE-REGISTERED EXPECTED-DIFF LIST** — every difference the deployment *should* produce in tomorrow's boot log, enumerated from the four wiring diffs and the `sr_shadow` config, **written down and frozen alongside the baseline with its own filename, size and md5** (Amendment 12 §1).
   - ✅ **WRITTEN AND FROZEN BEFORE ANY VM WRITE**, from committed code only, ⛔ with no VM contact. **THREE frozen artifacts, each verified at Gate 2 and again at Gate 7/8:**
     | Artifact | Size | md5 |
     |---|---|---|
     | ⭐ **`EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_v12_2026-09-16T1338IST.md`** — **THE CURRENT PREDICTION (v6)** | 43,540 B | `41e2cdec41411651ea29bdcac7c87d2a` |
     | ⭐ **`NORMALIZATION_RULESET_17-Sep-2026__frozen_v4_2026-09-16T1138IST.md`** — the frozen ruleset (v4) | 6,067 B | `0fab34f53387c54a8d536292e77d22b5` |
     | ⭐ **`normalize_bootlog__frozen_v3_2026-09-16T1138IST.py`** — the frozen NORMALIZER (v3) | 8,797 B | `0cbcf225048e079c4ac83f06e044745a` |
     | ⭐ **`validate_window__frozen_2026-09-16T1225IST.py`** — **the frozen WINDOW VALIDATOR (precondition gate)** | 4,218 B | `8c354fd7322d104b15e6bc9246b864c9` |
     | 📄 `WINDOW_VALIDATOR_TEST_EVIDENCE_2026-09-16T1225IST.txt` — RAW, 7 cases + Check B | 5,745 B | `8cbcbce293ea4c67e71827484408413f` |
     | 📄 `CALIBRATION_eodwindow_2026-09-15.jsonl` — real EOD window, validates the EOD spec | 9,599 B | `89bf3d3eddd511a94d3df062086a5454` |
     | 📄 **`NORMALIZER_TEST_EVIDENCE_2026-09-16T1150IST.txt`** — **RAW** output + rc of all six tests | 19,657 B | `3c340707ccaf2b64339332faf13c1460` |
     | 📄 `NORMALIZER_TEST_INPUT_*.jsonl` (4) · `CALIBRATION_bootwindow_2026-09-1[56].jsonl` (2) | — | originals **UNCHANGED** `f5809812…` `ee034ee1…` |
     | ⛔ predictions v11–v1 · rulesets v3–v1 · normalizers v2–v1 — SUPERSEDED, KEPT | — | — |
   - ⛔🔴🔝 **THE WINDOW SPECIFICATION (Amendment 17 §1) — recorded HERE, with the hashes.** ⚠️ **The deployment makes the boot LONGER**, so a window delimited by **POSITION or DURATION** would push later lines OUT of tomorrow's window, where they would read as **MISSING EVENTS** — ⛔ **the very signature E-1 treats most seriously.**
     - ⛔🔴 **BOTH BOOT DELIMITERS ARE *INFO* ⇒ READ THEM IN `logs/system_<DATE>.log`, ⛔ NEVER the journal (Amendment 30 §1).** ⚠️ `composition assertion FAILED` is **CRITICAL** and so appears in **both** — ⭐ **the START and the OK-END are journal-invisible; only the FAILED-END is not.**
- ✅ **BOTH DELIMITERS ARE SEMANTIC**, ⛔ neither positional nor time-bounded: **START** = the `Trading System v… starting` line · **END** = `effect_telemetry: composition OK (…)` or `composition assertion FAILED`. ⭐ **The window GROWS WITH THE BOOT.**
     - ✅ **The end marker sits AFTER ALL MANAGER CONSTRUCTION**, ⛔ not between managers: 🔬 `assert_composition` at **`main.py:4277`** vs the sr_shadow block at **`main.py:3536–3539`**.
     - ✅ **MARKER UNIQUENESS VERIFIED WHOLE-DAY, BOTH DAYS** (read-only): `starting=1 · composition OK=1 · FAILED=0` on 15-Sep and 16-Sep ⇒ unambiguous, and **no mid-day restart**. ⚠️ If Gate 2 records **`NRestarts` ≠ 0** or a second `starting` line, ⛔ **re-examine the window before comparing.**
     - ⛔🔴 **AND THE FINDING: a BOOT-WINDOW-ONLY E-4 CHECK WOULD BE *VACUOUS BY WINDOW*.** 🔬 `start()` spawns a **background daemon thread** (`runner.py:149`) and `sr_shadow: drain error=` is emitted from inside its loop (`runner.py:166`) ⇒ **it can fire long AFTER the end marker.** ⭐ **A must-absent row checked over a window that cannot contain the event passes BY CONSTRUCTION — the same A7 defect in a THIRD dimension: sink → level → WINDOW.**
     - ⛔🔴🔝 **IF NEITHER END MARKER APPEARS, THAT IS ITSELF THE FINDING (Amendment 18 §3).** The terminator is `composition OK` **OR** `composition assertion FAILED`; ⚠️ **if the boot dies before reaching composition (`main.py:4277`) neither fires**, the awk flag stays set and it **prints to end of file** ⇒ the "boot window" **silently becomes the whole day** and the comparison produces enormous residuals. ⭐ Loud — ⚠️ **but it would look like a NORMALIZER or WINDOW fault rather than what it is: THE BOOT NEVER REACHED COMPOSITION.** ⛔🔴🔝 **THE GUARD IS `== 1`, ⛔ NOT `>= 1` (Amendment 19 §1).** `>= 1` closes the zero case but ⚠️ **PASSES TWO markers**: **0 ⇒ STOP** · **1 ⇒ valid** · **2+ ⇒ STOP** (⚠️ *`>= 1` would have passed this*). ⚠️ **Two markers is fatal whatever caused it:** E1.1/E1.2 are each predicted **exactly once**, so across two boots the whole-day log holds **two of each**, and **`drain error` + any new CRITICAL — both WHOLE-DAY rows — would span TWO PROCESS LIFETIMES attributed to ONE deployment**; ⭐ **and the awk exits at the FIRST terminator**, so the boot window would silently be **boot #1** while the whole-day checks covered **both**. ✅ **The guard, on BOTH windows: start `== 1` · end `== 1` · end AFTER start** ⇒ else **`WINDOW_INVALID` → STOP**. ⭐ Hand-verified uniqueness and Gate 2's `NRestarts` are **an observation and a separate gate, ⛔ not this guard.**
     - ⛔🔴🔝 **THE *EOD* WINDOW, SPECIFIED (Amendment 19 §2) — it never had been, although the table assigns E3.5 and E4.9 to it.** **START `Shutdown initiated`** (`main.py:1631`) → **END `Shutdown complete`** (`main.py:1839`), **both SEMANTIC**. ✅ **The end marker sits AFTER `sr_shadow.stop()` (`main.py:1705`)** ⇒ **E3.5 and E4.9 are emitted INSIDE the window.** ⛔ **NOT a clock slice** — a 17:30–17:40 box would be positional, and the same reasoning that made a positional boot window unsafe makes that unsafe. ✅ **Same missing-end-marker case** (a shutdown that dies partway never emits `Shutdown complete` ⇒ *"the shutdown never completed"* is ITSELF the finding) **and the same `== 1` guard.** 🔬 **Validated on real data:** the 15-Sep EOD extract (`init=1 complete=1`) ⇒ **WINDOW_OK**; the same spec on a **boot** file ⇒ **WINDOW_INVALID** (non-vacuous cross-check). ⚠️ At midday 16-Sep read `init=0 complete=0` — ⭐ correct, the session had not yet self-exited; **the EOD baseline exists only after 17:35**, which is why Gate 2 captures after the self-exit.
       - ⭐🔝 **Same pattern as Amendment 18 §1:** there a procedure lived in **two places** and only one was updated; here **a window rule was established for one window and the second was never brought under it.** ⛔ **Both are gaps between "the rule exists" and "the rule covers everything it names."**
     - ⛔🔴🔝 **`WINDOW_INVALID` PRECEDES EVERY RESIDUAL (Amendment 19 §3).** ⛔ **When the window is invalid the FIRST finding is `WINDOW_INVALID`, ⛔ NEVER `NORMALIZER_RESIDUAL`.** ⭐ An unterminated window runs to EOF and yields enormous residuals that **look like a normalizer or window fault rather than what they are.** ✅ **The validator runs FIRST, as a PRECONDITION; on failure the comparison is ⛔ not run at all.**
     - ✅ **WINDOW PER EVENT CLASS:** **E1.1/E1.2/E2.3/E4.6/E4.7/E5.11 ⇒ BOOT WINDOW** · **E4.8 `drain error`, E4.10 new CRITICAL, E5.12 runtime ⇒ the WHOLE-DAY application log** · **E4.9 + E3.5 ⇒ the EOD window** · **systemd lifecycle ⇒ the journal, whole day**. ⚠️🔝 **THE JOURNAL'S `--since today` IS TIME-BOUNDED, AND THE REASON IT IS TOLERABLE STAYS ATTACHED TO IT (Amendment 18 §4):** it is acceptable **ONLY** because it is a **whole-day bound on SYSTEMD events** — nothing the deployment adds can be pushed out of a full day. ⛔ **It must NEVER become a positional or time-bounded delimiter for an APPLICATION-event window** — that was the Amendment 17 §1 hazard, and ⭐ **the distinction is easy to lose later once only the command survives.**
   - ⛔🔴🔝 **THE PREDICTION IS *DATA*; THE MANIFEST IS *PROCEDURE* — ⛔ NEVER BOTH (Amendment 18 §2).** 🔴 **Why this rule exists, measured:** v6 carried its own copy of *"How Gate 7/8 runs"*, and its **step 1 — the artifact-identity check itself — named the SUPERSEDED set** (`v4` · `ruleset v3` · `normalizer v2`). ⚠️ **Every one of those files is still on disk, deliberately kept** ⇒ an operator following it verbatim would have md5-verified them, **got a clean MATCH, and proceeded with the wrong set.** ⭐ **The gate would not merely have failed to catch the mismatch — it would have CERTIFIED it and reported GREEN.** 🔬 Confirmed on disk: `b330ca13…` · `5c212e3f…` · `b011440e…` all verify clean.
     - ⭐ **Same shape as everything this chain has surfaced:** `STOP_NOT_DEFENDED` that could never be red · E-4 rows checked against a sink that could not carry them · boot-window checks for events emitted by a background thread · and now **an identity gate that passes against the wrong identity.**
     - ✅ **FIXED STRUCTURALLY, ⛔ not by editing the line:** the prediction's procedure section is now **a POINTER to `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` → Gate 4-PRE and Gate 7/8**, and the prediction carries **DATA ONLY**. ⛔ **A prediction that also INSTRUCTS must be re-verified every time the procedure moves; one that only PREDICTS does not.** ⛔ **The reference is BY SECTION NAME, never by version** — *"v7 refers to the current set"* is the same failure with one more indirection. 🔬 The manifest itself was checked: **all 15 artifact references are the current set, 0 stale.**
   - ⛔🔴🔝 **THE EVALUATOR IS PART OF THE DEPLOYMENT AND HAD NO PREDICTED OBSERVABLE (Amendment 20 §1).** Gate 6 installs a **cron job** at **16:05 Mon-Fri**; Gate 7/8 never looked for it. Its first run is **17-Sep 16:05, BETWEEN the boot and EOD comparisons.** ⭐ **Every other failure in this chain was a green that could not have been red — this was a component with NO TEST AT ALL.** ✅ Now class **E-6** in the prediction.
     - ✅🔴 **THE SINK QUESTION, ANSWERED FROM CODE, no VM contact:** 🔬 the evaluator calls `get_logger("sr_shadow_evaluate")` (`scripts/sr_shadow_evaluate.py:180`) **but NEVER calls `setup_logging`** (0 occurrences), and **nothing in its import chain attaches a handler at import time** (`core/logger.py`'s two `addHandler`/`basicConfig` occurrences are **inside** `setup_logging`). ⇒ ⛔ **In that separate cron process the root logger has NO handlers**, so Python's **`lastResort`** applies: **WARNING+ to STDERR, INFO/DEBUG DISCARDED.**
     - ⇒ ⛔🔴 **THE EVALUATOR WRITES NOTHING TO `logs/system_<DATE>.log`.** Its only sinks are the **cron log** (`>> logs/cron-sr-shadow-evaluate.log 2>&1`) and the **shadow DB**. ⭐ **This is the answer §1 explicitly permits — now STATED rather than unstated.**
     - ✅🔴 **THEREFORE E4.10 IS UNAFFECTED, which is the consequence that mattered:** a failing evaluator **cannot inject a CRITICAL into the application log**, so it **cannot be misclassified as a service-deployment violation.** ⛔ It emits **no `log.critical` at all** — its only two log calls are `log.error` (`:118` market data unavailable, `:138` fetch failed).
     - **E-6 MUST APPEAR:** the **JSON summary line** (`print(json.dumps(summary…))`, `:186`) — ⭐ the evidence the cron **fired at all**; a **completed-run row** via `store.record_run(…)` (`:169`, only when **not** `dry_run` and **not** refused); per-row `store.write_evaluation` (`:154`). **E-6 MUST BE ABSENT:** the two `log.error` texts, any CRITICAL, any traceback — ✅ all **ERROR or above**, so `lastResort` carries them to stderr and the cron log **can** observe them (⛔ not a must-absent row against a sink that cannot carry it).
     - ⚠️ **A GAP NAMED, ⛔ NOT CLOSED: THE EXIT STATUS IS NOT OBSERVABLE POST-HOC.** 🔬 The cron line redirects **stdout and stderr only** — an exit code is **not written to the log**. Codes are **0** clean · **2** `rows_left_unevaluated > 0` · **3** refused, session not over (`:88`, `:170`). ⭐ rc is **DERIVABLE from the JSON summary's own fields** but ⛔ **not directly recorded.** ⛔ Whether to record it is a **decision, not made here.**
   - ✅⛔🔝 **E-6 IS CLOSED (Amendment 21 §1). THE PROCESS EXIT STATUS IS *NOT* CAPTURED, AND IS NOT TO BE ADDED.** ⭐ **Reason 1 — the cron log already separates three states without it:** **summary present ⇒ the evaluator COMPLETED** (its fields carry the outcome) · **summary absent + traceback ⇒ started, failed before completing** · **summary absent + no traceback ⇒ ⛔ EXECUTION NOT PROVEN**. ⛔ An rc adds a fourth way to say what those three already say. ⚠️🔴 **CORRECTED BY AMENDMENT 22 §2: an earlier draft read "no content ⇒ the cron never fired" — an ABSENCE-INFERENCE.** ⭐ That third state is equally consistent with a process killed before output, a shell/process-boundary failure, an environment fault before logging, or the cron daemon itself. ✅ **THE RULE: no E-6 completion evidence ⇒ E-6 NOT PROVEN / INCOMPLETE; the CAUSE is classified separately and only on supporting evidence.** ⭐ **Reason 2 — the evaluator is INSIDE THE FROZEN SET:** `scripts/sr_shadow_evaluate.py` is committed in `e7bf477`, is **one of the 17 copy files**, and carries frozen md5 **`edebd2d8…`** in the file table ⇒ ⛔ **changing it now would invalidate the commit, the file table, the Gate 4 copy manifest, the four-artifact identity check and the 27-vs-17 accounting** — hours before the window, to record a derivable value.
     - ✅🔴 **THE REQUIRED VERIFICATION IS DONE — A CODE READ, ⛔ NOT A CODE CHANGE.** 🔬 Exhaustively at `e7bf477`: `run()` has **exactly two returns** — `:88` (refused) and `:170` — **both carrying a summary dict**; `main()` has **exactly one return** (`:187`), preceded **unconditionally** by `print(json.dumps(summary…))` at **`:186`**; the only `sys.exit` is `:191`, **after** `main()` returns. ⇒ ✅ **EVERY non-crash exit path emits the summary line, INCLUDING THE REFUSED PATH** ⇒ ⛔ **the false-red §1 feared — a refused run indistinguishable from "cron never fired" — DOES NOT EXIST.**
     - **THE CONTRACT, stated not inferred:** the **JSON summary line at `:186` IS the completion marker** · its fields **ARE** the result — `refused` key ⇒ **rc 3** · `rows_left_unevaluated > 0` ⇒ **rc 2** · else ⇒ **rc 0** · the process rc is **NOT** captured **and the record says why** · ✅ a **second discriminator** exists: `record_run` (`:169`) is guarded by `if not dry_run:` (`:168`) and is **unreachable on the refused path**, so **summary + run row = completed** · **summary with `refused` + no run row = refused** · `"dry_run": true` (`:160`) is **self-declaring**. ✅ **EVERY PATH LEAVES EVIDENCE** — the only way to omit the summary is an uncaught exception before `:186`, which writes a **traceback to stderr** into the cron log. ⛔ **There is no silent path.**
     - **E-6 is RUN-LEVEL:** ⭐ **a run with ZERO eligible rows is a COMPLETED run, not an absent one.** ⛔ "cron fired" and "evaluator completed" stay **distinct**. ⚠️ **The script emits NO START MARKER** — the summary line is the **sole semantic terminator**, so E-6 is delimited by the run's appended block and ⛔ **never by a 16:05–16:10 clock slice**, for the same reason a positional boot window was rejected.
   - ⛔🔴🔝 **§2 — DO NOT SOLVE E-6 BY CALLING `setup_logging()` IN THE EVALUATOR.** ⭐ **The process separation is the reason E4.10 cannot be contaminated by a failing evaluator — a PROPERTY WORTH KEEPING, ⛔ not a limitation worth fixing.** ⚠️ Attaching the application handlers there would create **precisely the contamination Amendment 20 went looking for, in the name of closing the ticket Amendment 20 opened.** **Recorded as intentional: evaluator → cron log + shadow DB; service → application log + journal. Two processes, two evidence chains, NO OVERLAP.**
   - ⛔🔴🔝 **IDENTITY LIVES HERE, AND NOWHERE ELSE (Amendment 23 §1).** ⭐ **Cards, reports and reviews name artifacts by ROLE ONLY** — *the prediction* · *the ruleset* · *the normalizer* · *the window validator* — ⛔ **never by version, never by hash.** ⭐ **"Current" means whatever THIS MANIFEST'S identity command returns at the moment it is run**, ⛔ never a number written in a card hours earlier.
     - 🔬 **The mechanism, observed THREE times in one day:** a card names the current version → the card is applied → applying it **produces a new version** → **the card that caused the increment now names the superseded one.** ⭐ **The card is stale BY THE ACT OF BEING USED.** ⚠️ Same lesson as Amendment 18 §2 in a third location: **identity lived in two places and the copy went stale** — while the cards warning about it were themselves the copy.
     - ✅ **The prediction already had the right shape and keeps it:** it **names no artifact filename at all**, referencing the validator by ROLE, so **it cannot go stale.**
   - ⚠️🔴 **A RESIDUAL IN *THIS* IDENTITY CHECK, RECORDED AND ⛔ NOT FIXED.** 🔬 The identity command compares a **NAMED file** against a **STATED hash** ⇒ ⛔ **it cannot see a newer artifact it does not name.** ⚠️ If a future pass produces a new prediction and **forgets to update this manifest**, the command still names the superseded file — which **is kept on disk and verifies CLEAN** ⇒ ⭐ **the gate would certify the superseded set and report GREEN.** 🔬 **Exactly the Amendment 18 §1 defect, surviving in the one place identity is allowed to live.** 🔬 Confirmed: **0** checks in this manifest assert *"no newer artifact exists"*.
     - ✅⏸ **DISPOSITION (Amendment 24 §1): RECORDED AS *DORMANT*, ⛔ NOT CLOSED. Noticed 16-Sep-2026.**
       - ⛔🔴🔝 **CORRECTED BY AMENDMENT 25 §1 — THE "SHUT BY THE FREEZE" ARGUMENT WAS WRONG FOR THE INTERVAL THAT COUNTS.** ⚠️ **THE SET IS NOT FROZEN NOW.** The standing rule is that the prediction, ruleset and normalizer **CLOSE AT THE FIRST VM WRITE**, which **has not happened** — and 🔬 **the prediction has in fact moved twelve times today, most recently v11 → v12 at 13:38.**
       - ⭐ **TWO INTERVALS, AND THEY ARE NOT THE SAME:**
         - **NOW → FIRST VM WRITE:** artifacts **can still change** · ⚠️ **the residual is LIVE** · the mitigation is **PROCEDURAL** — *the pass that creates an artifact updates the manifest in the same action*. ⭐ **Every pass today has done it, which is EVIDENCE, ⛔ not a guarantee.**
         - **AFTER THE FIRST VM WRITE:** artifacts **closed** · the trigger condition **cannot arise** · the defect is **structurally DORMANT.**
       - ⇒ ⛔ **The structural argument only ever applied to the SECOND interval — the one where nothing changes anyway.** ⭐ **For the hours that actually matter it is PROCEDURE holding the line, exactly as the earlier wording claimed it was not.**
       - ✅🔴🔝 **THE FREEZE-BROKEN PROTOCOL — adopted so the mitigation is TESTABLE instead of REMEMBERED:**
         - **After the artifact freeze:** ⛔ no creation · ⛔ no replacement · ⛔ no version increment · ⛔ no identity-changing mutation.
         - **If an authorised correction produces a new artifact, THE FREEZE IS BROKEN** — ⭐ **say so in those words**, update the manifest, **re-run the identity and digest gate**, and record that **the deployment set is NOT the previously frozen set**.
         - ⛔🔴 **NEVER describe that state as "still frozen".**
       - 🏷️ **Classification unchanged: REAL · DORMANT AFTER THE WRITE · ⛔ NOT CLOSED.** Only the *reason* for the pre-write interval is corrected — it is **procedure, not structure**.
       - The procedural mitigation covers the **only** remaining case — a correction between now and 17:30: **the pass that creates an artifact updates this manifest in the same action.** Every pass today has done it.
       - ⛔🔴 **DO NOT ADD A "HIGHEST VERSION WINS" ASSERTION.** ⭐ **Version numbering is a NAMING CONVENTION, ⛔ not the identity contract**; making version arithmetic part of deployment acceptance would create a **new class of failure — an artifact correctly named but REJECTED FOR ITS NUMBER.**
       - ⚠️🔴 **IT BECOMES LIVE AGAIN ON THE NEXT DEPLOYMENT CYCLE**, the moment artifacts start moving and the freeze is not there to protect it. ⭐ **A defect disposed of by CIRCUMSTANCE rather than by FIX is the kind that returns unannounced.**
   - ✅🔝 **ROLE-ONLY DOES NOT MEAN HASH-FREE (Amendment 24 §2)** — stated so Amendment 23 §1 is not over-read. **Three functions, kept separate:**
     - **CARD** names the **ROLE** — the prediction · the ruleset · the normalizer · the window validator. ⛔ Never a version, never a hash.
     - **MANIFEST** resolves the role to a **concrete artifact**. ⭐ The single identity authority.
     - **HASH** verifies the **integrity** of the artifact the manifest resolved.
     - ⇒ ⭐ **Removing versions from cards removes STALE IDENTITY from procedural documents. It does ⛔ NOT remove integrity verification** — the first-write boundary still verifies every resolved artifact by **filename, size and digest**.
   - ✅🔝 **THE LABEL CHECK, ANSWERED ONCE SO IT IS NOT RE-ASKED (Amendment 24 §4).** ✅🔴 **THE INVARIANT, which is the thing that matters: ZERO RUNNABLE LABELS LACK A COMMAND BLOCK.** 🔬 Verified by checking, for every occurrence of the label string, whether a fence opens within two lines: **28 command-bearing labels, 0 orphans.**
       - ⚠️🔴 **⛔ DO NOT USE A RAW `grep -c` OF THE LABEL STRING AS THE CHECK — IT IS SELF-INVALIDATING.** 🔬 A naive count also matches **the labelling RULE table row** (which defines the label and carries no command by design) **and every PROSE MENTION of the string — including this one.** ⭐ **Recording the count literally CHANGED the count**, from 29 to 30, in the act of writing it down.
       - ⭐ **So the stable check is the INVARIANT (label ⇒ a fence within two lines), ⛔ never the bare occurrence total.** ⚠️🔴 **THIRD INSTANCE, AND IT CAUGHT THE REVIEWER TOO (Amendment 27 §4):** 🔬 `"ENABLED and started"` · `"RUNNABLE"` · and a **section-heading pattern that did not match the real heading format**, which returned *"4 present, 22 missing"* — ⭐ **a clean, confident, entirely wrong answer that looked exactly like a catastrophic finding.** ⭐ **Three substring-count failures in one day across TWO independent reviewers** ⇒ ⛔ **the rule binds the people CHECKING the work, not just the work.** ⚠️ **A number always looks like evidence.** ⭐ **Same mechanism as Amendment 23 §1: a document that records a number about itself is stale the moment it records it.**
   - ✅ **§25 CONFIRMED — THE VALIDATOR KEYS ON MARKER *TEXT*, ⛔ NOT SOURCE LINE NUMBERS.** 🔬 It matches with `msg.startswith(start_key)` / `msg.startswith(k)`; the `main.py` line references appear **only** in the printed `prov` provenance string — **0 uses inside any comparison.** ⭐ **A line number moves on the next edit; the marker text does not.** The line numbers stay in the record as **evidence**.
   - ✅ **§24 THREE-LAYER SEMANTIC CONSISTENCY — CHECKED, NO DIVERGENCE.** Manifest · frozen artifacts (prediction + ruleset) · validator, against **six** propositions: **start == 1** · **end == 1** · **end after start** · **missing end ⇒ STOP** · **multiple ends ⇒ STOP** · **no comparison after an invalid window**. ⭐ **All three layers carry all six.** ⚠️ One apparent divergence (*end after start* absent from the manifest) was a **false positive from a case-sensitive pattern** — re-checked case-insensitively, the manifest states it: *"The guard, on BOTH windows: start `== 1` · end `== 1` · end AFTER start"*. ⭐ **Reported as a self-corrected check, ⛔ not as a finding.**
   - ⭐🔝 **WHAT THE SEVEN VALIDATOR CASES DO AND DO NOT ESTABLISH, kept verbatim because the distinction is lost under time pressure:** seven validator cases pass → **the validator recognises those cases** · 28 RUNNABLE, 0 placeholders → **structural readiness** · four identity hashes match → **identity** · **none of the above → that tomorrow's deployment will pass.** ⭐ **Case E (two end markers, rc 3) is the most valuable of the seven, because it is the case `>= 1` ACCEPTED this morning — a test that fails against the PREVIOUS implementation is worth more than six that pass against both.**
   - ⚠️⚖️ **EVIDENCE BOUNDARY (Amendment 17 §4), stated honestly:** the normalizer fixes are **verified according to THIS SESSION'S report**, with named non-vacuous tests — ⛔ **NOT an independent code audit.** ✅ So the **RAW outputs are kept**: six runs with full output and rc (**T1 rc 0 · T2 rc 1 · T3 rc 0 · T4 rc 1 · T5 rc 1 · T6 rc 2**), their four input files, and the **ORIGINAL calibration extracts UNCHANGED** — ⭐ **the pair is what shows the correction did not change what the calibration means.**
   - ⛔🔴🔝 **THE NORMALIZER'S EXIT CODE CARRIES *NO VERDICT* (Amendment 16 §1).** 🔬 **DEMONSTRATED by simulating both 17-Sep outcomes against the real 16-Sep boot window:** a **CORRECT** deployment (sr_shadow up, 63/63) ⇒ `UNRECOGNISED FAMILIES: 4` ⇒ **rc 1**; a **FAILED** deployment (manager never started) ⇒ `UNRECOGNISED FAMILIES: 0` ⇒ **rc 0**. ⇒ ⛔ **rc 1 IS EXPECTED AND rc 0 IS ALARMING — the reverse of what the no-change calibration established. A correct deployment reads as failure; a failed one reads as clean.**
     - ⛔🔴 **DEEPER: the normalizer CANNOT DETECT A MISSING EXPECTED EVENT AT ALL.** It reports **differences**; an event absent from **both** sides produces **no difference**. ⭐ **Absence is exactly the E-1 failure mode the prediction exists to catch, and the tool is STRUCTURALLY BLIND to it.**
     - ✅ **CLOSED by removing the place to record the wrong answer:** the per-event Gate 7/8 record has **NO FIELD for normalizer pass/fail — only a field for its RESIDUAL LIST**, plus an **UNPARSEABLE LINES** row. ⭐ *The enforcement is that there is nowhere to write the wrong answer down.* The tool also **prints the warning itself**, before and after its output.
   - ⛔🔴 **THE FAMILY CLASSIFIER IS NOW ANCHORED (Amendment 16 §2).** It used **fragment matching** — the very trap **R1.5** exists to close — and here the damage points the wrong way: for event identity a bad match gives a **FALSE ANOMALY (LOUD)**; for family recognition it gives a **FALSE GREEN (SILENT)**. ✅ Now `logger` must **match** AND `msg` must **START WITH** the key. 🔬 Verified non-vacuous: a new `ERROR` from `main` reading *"startup_checks: check_ntp_sync wrapper crashed"* is now **UNRECOGNISED** — the old code **absorbed** it.
   - ⛔🔴 **ANY UNPARSEABLE LINE IS NOW A FINDING (Amendment 16 §3).** The ≥50% rule only caught *"you pointed this at the journal"*; below it, bad lines were **silently dropped and the run could exit 0** — in a comparison whose entire purpose is to notice **missing** events. 🔬 Verified: **2 bad lines in 84 ⇒ rc 1 + a FINDING** (previously rc 0). ⭐ The app log is machine-written JSON; an unparseable line **is itself an anomaly to adjudicate**.
   - ⛔🔴🔝 **SINK AUTHORITY IS BY *ORIGIN*, NEVER BY LEVEL (Amendment 15 §2).** **APPLICATION-EMITTED events ⇒ `logs/system_<DATE>.log` is authoritative ALWAYS** (🔬 it carries INFO+, so a level flip never changes what it holds); the journal's copy is a **level-dependent stdout DUPLICATE** and is ⛔ **NEVER used for comparison**. **SYSTEMD/UNIT LIFECYCLE events ⇒ the JOURNAL is authoritative** (the app log cannot carry them at all).
     - 🔬 **Why:** `check_ntp_sync` is **INFO** when it succeeds and **WARNING** when it fails ⇒ journal-to-journal it would **appear from nowhere on 16-Sep and vanish again if NTP recovers on 17-Sep.** ⭐ **The event never moved — its VISIBILITY did.** ⚠️ **Any family whose level varies with OUTCOME does this.** ⇒ R0 **eliminates the whole class** instead of adjudicating instances tomorrow.
     - ⛔ **This TIGHTENS Amendment 14 §2: the E-4 must-absent rows are checked against the APPLICATION LOG**, because that is where the application emits them — ⛔ not against the journal merely because ERROR and CRITICAL happen to reach it.
     - ✅ **Mechanically enforced:** the frozen normalizer **REFUSES (rc 2)** non-JSON input, so it cannot be pointed at the journal. 🔬 Verified: journal-format input ⇒ REFUSED rc 2; JSON ⇒ rc 0.
   - ⛔🔴🔝 **THE NUMBER "3" MUST NOT TRAVEL — RECOGNITION IS BY *FAMILY IDENTITY*, NEVER BY COUNT (Amendment 15 §1).** ✅ **Ten instances of `check_ntp_sync` is ORDINARY.** ⛔ **ONE instance of a THIRD family is NOT.** ⛔ **There is no numeric noise allowance.**
     - **Correct framing:** *pre-deployment calibration observed **3 residual event-instances across the ONE available no-change comparison**. These are the currently observed normalisation and variance cases — ⛔ **NOT a statistically estimated false-positive rate.** There is no denominator and no distribution over repeated no-deployment boots.*
     - ✅ **Enforced mechanically:** the normalizer reports **by family** and exits **rc 1 if ANY unrecognised family appears**, whatever the known-family counts. 🔬 Verified non-vacuous: known-only (x2 + x1) ⇒ rc 0; one injected new family ⇒ `UNRECOGNISED FAMILIES: 1`, rc 1.
     - **KNOWN-VARIANCE FAMILIES**, ⛔ never normalized away to make tomorrow green: **`check_ntp_sync`** (flips INFO↔WARNING — harmless once the app log is authoritative) and **`email_fallback.sent`**.
   - 🔴 **The composition row is the STRONGEST:** 🔬 measured baseline **`62 registered, 62 expected`** ⇒ predicted **`63 registered, 63 expected`** — ⭐ **two specific integers that either appear or do not; falsifiable in a way a delta is not.** ⛔ Carry the **measured baseline pair** into the Gate 7/8 record beside the observed pair. **63 expected / 62 registered ⇒ STOP**, ⛔ never a warning.
   - ⚠️🔴 **SUBSTRING TRAP — match the FULL `msg`.** 🔬 Three `main.py` sites emit `"ENABLED and started"` (`:3517` sr_detector · `:3537` sr_shadow · `:3569` market_regime) and **sr_detector is ENABLED on the twin ⇒ already in the baseline** ⇒ a fragment count reads 1 today / 2 tomorrow = a **FALSE multiplicity anomaly on the first thing Gate 7/8 looks at**. ⭐🔝 **Why it was nearly missed: the prediction named the event by the text A HUMAN WOULD GREP FOR; the comparison must match WHAT THE CODE EMITS — a different thing.** ✅ The fix is **general**, ⛔ not a patch for one string.
   - ⛔🔴🔝 **THE AMENDMENT WINDOW (Amendment 13 §2) — BOTH HALVES, OR §1 HAS NOWHERE TO GO:** ⭐ **the prediction MAY be corrected at ANY time BEFORE the first VM write; it may NEVER be corrected after.** A pre-deployment correction is **timestamped, md5'd, and SUPERSEDES — with the superseded version KEPT and the reason recorded.** ⭐ **The anti-rationalisation property comes from the prediction preceding the OBSERVATION, ⛔ not from the file being untouchable from the moment it was typed. Freezing an error you have already found would be discipline theatre.** ⛔ **After the first write tonight the prediction is CLOSED** — from then on a legitimate missed event is a **MISS IN THE PREDICTION**.
   - ⚠️🔴 **WHY v2 EXISTS — v1 WOULD HAVE FAILED A CORRECT DEPLOYMENT.** 🔬 `core/logger.py`: the stdout handler is **`setLevel(WARNING)`** and the unit sends stdout+stderr to the **journal** ⇒ ⛔ **EVERY `INFO` LINE IS ABSENT FROM THE JOURNAL.** ⭐ All three *must-appear* rows are **INFO** ⇒ they exist **ONLY** in `logs/system_2026-09-17.log`. ⚠️ **Had Gate 7/8 looked for them in the journal it would have declared "the manager did not come up" and stopped a correct deploy.** ⭐ v2 carries a **SINK MAP** so each row is checked in the right file.
   - ✅ **Amendment 13 §1 answered, 🔬 from code, no VM contact:** handlers attach to the **ROOT** logger (`core/logger.py:375,452`), ⛔ **not per logger name**; `get_logger` only calls `logging.getLogger` (`:266-273`); **no `propagate = False` anywhere**; and `system_*.log`'s `_SystemFilter` is a **pure level catch-all** (`levelno >= INFO`), ⛔ **no name restriction**. ⇒ ⭐ **`sr_shadow` DOES reach the system log.** ⚠️ `_safe_log` **swallows silently** (`runner.py:218-221`) — a residual note, ⛔ not an expected event.
   - ⛔🔴 **IF THE EXPECTED LIST IS WRITTEN TOMORROW, WHILE LOOKING AT THE DIFF, IT IS ⛔ NOT A TEST — IT IS A RATIONALISATION.** ⭐ An operator at 08:15 with a diff in front of them will adjudicate each line as it appears, and **every difference will find a reason.** Predicting what *should* change, **before changing anything**, is the only version of that check **that can FAIL**.
   - Tomorrow: anything in the diff **NOT on the list** is an **anomaly to adjudicate**, ⛔ not a line to explain away; anything **on the list that is ABSENT** is **equally a finding** — a predicted startup line that never appeared means **the manager did not come up**.
   - ⛔ **DO NOT AMEND THE LIST AFTER SEEING TOMORROW'S LOG.** A legitimate omission is recorded as **a MISS IN THE PREDICTION**, ⛔ never as a late addition.

> ⛔⭐ **Item 5 matters most. Preserve it TONIGHT, BEFORE the deployment.** Tomorrow's comparison is **against a file, not a memory**, and the comparison is **worthless if nobody captured the "before"**.

**① Service state, timestamps, and the INSTALLED unit.** **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'echo "== is-active =="; systemctl is-active trading-system; echo "== properties =="; systemctl show trading-system -p ActiveState -p SubState -p MainPID -p ExecMainStartTimestamp -p ExecMainExitTimestamp -p ExecMainStatus -p ExecMainCode -p NRestarts -p Result; echo "== INSTALLED unit + drop-ins =="; systemctl cat trading-system'
```
- ⚠️ **`systemctl cat` is in there deliberately.** 📄 Memory: **deploy does NOT install unit files** — `deploy/systemd/*.service` in the repo is intent, ⛔ not what runs; and **drop-ins are ⛔ not integrity-watched**. ⭐ Read the INSTALLED unit, ⛔ never assume the repo's.
- A clean self-exit should read `ExecMainStatus=0` / `Result=success`. 📄 The repo unit's policy: **exit 0 = holiday guard or normal EOD ⇒ no restart**; `Restart=on-failure`; `RestartPreventExitStatus=3 4`.

**② PRESERVE TODAY'S JOURNAL — THE Gate 7/8 BASELINE.** 📄 The unit logs to the journal (`StandardOutput=journal`, `SyslogIdentifier=trading-system`). **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'journalctl -u trading-system --since today --no-pager' > D:/Projects/_preservation/BASELINE_journal_trading-system_16-Sep-2026.txt
```

**③ PRESERVE TODAY'S APPLICATION LOG** (the app also writes its own dated log). **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cat logs/system_2026-09-16.log' > D:/Projects/_preservation/BASELINE_system_16-Sep-2026.log
```

**④ SESSION-HEALTH SCAN — read it, ⛔ do not just store it.** **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'journalctl -u trading-system --since today --no-pager | grep -nE "CRITICAL|Traceback|composition|SHUTDOWN|Started |Stopped |Main process exited|kill.switch|SOFT_KILL" | tail -80'
```

**⑤ FREEZE THE BASELINE — record FILENAME + SIZE + md5 for both captures** (Amendment 11 §3: artifact integrity, **immutable for the deployment record**), so tomorrow's comparison is against a fixed artifact. **`RUNNABLE — LITERAL COMMAND`**
```
md5sum D:/Projects/_preservation/BASELINE_journal_trading-system_16-Sep-2026.txt D:/Projects/_preservation/BASELINE_system_16-Sep-2026.log && wc -c D:/Projects/_preservation/BASELINE_journal_trading-system_16-Sep-2026.txt D:/Projects/_preservation/BASELINE_system_16-Sep-2026.log
```
**⑥ CONFIRM THE THREE *CURRENT* FROZEN PREDICTION ARTIFACTS ARE UNCHANGED** (Amendments 12 §1 + 13 §§2–3). **`RUNNABLE — LITERAL COMMAND`**
```
md5sum D:/Projects/_preservation/EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_v12_2026-09-16T1338IST.md D:/Projects/_preservation/NORMALIZATION_RULESET_17-Sep-2026__frozen_v4_2026-09-16T1138IST.md D:/Projects/_preservation/normalize_bootlog__frozen_v3_2026-09-16T1138IST.py D:/Projects/_preservation/validate_window__frozen_2026-09-16T1225IST.py && wc -c D:/Projects/_preservation/EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_v12_2026-09-16T1338IST.md D:/Projects/_preservation/NORMALIZATION_RULESET_17-Sep-2026__frozen_v4_2026-09-16T1138IST.md D:/Projects/_preservation/normalize_bootlog__frozen_v3_2026-09-16T1138IST.py D:/Projects/_preservation/validate_window__frozen_2026-09-16T1225IST.py
```
  Must read **`41e2cdec41411651ea29bdcac7c87d2a`** (43,540 B) · **`0fab34f53387c54a8d536292e77d22b5`** (6,067 B) · **`0cbcf225048e079c4ac83f06e044745a`** (8,797 B) · **`8c354fd7322d104b15e6bc9246b864c9`** (4,218 B, the window validator). ⛔ Any mismatch ⇒ **STOP**; the test is void.





- ⛔⭐ **SNAPSHOT IMMUTABILITY — ⛔ NEVER re-take these after the deployment.** 📄 Standing rule: a re-taken baseline destroys the before/after pair **and leaves no trace** — the file still exists, still parses, still looks like a baseline, and now silently **AGREES** with the after-state.
- ⚠️ If either capture is **empty or missing**, that is itself the case-3 finding: ⛔ **STOP**, and report it as an **attributability** stop.

#### 🔴⚠️ THE `KillSignal=SIGINT` MECHANISM — ⛔ **AIMED AT THE DAYTIME ROLLBACK, NOT AT TONIGHT** (corrected by Amendment 11 §1)

📄 The repo unit carries **`KillSignal=SIGINT`**: *"Send SIGINT on stop so main.py's Ctrl+C handler runs (clean shutdown, SHUTDOWN event, DB flush)"*. ⇒ 💭 a manual `systemctl stop` runs the **same clean-shutdown path as a genuine self-exit**.

⛔ **THE EARLIER AIM WAS WRONG AND IS WITHDRAWN.** It claimed a manual stop tonight could manufacture a fake *"clean exit today"* and change tomorrow's start. ⭐ **Work the arithmetic — it does not:**

| event | last clean exit | read on 17-Sep 08:15 |
|---|---|---|
| self-exit **17:35** on 16-Sep | 16-Sep | **a PRIOR day** ⇒ watcher starts |
| manual stop **17:42** on 16-Sep | 16-Sep | **a PRIOR day** ⇒ watcher starts |

- ⇒ ⭐ **At 17:42 the SIGINT mechanism does NOT block tomorrow's start.** Both paths date the clean exit **16-Sep**, and on 17-Sep both satisfy *"a prior day"*.

⛔🔴🔝 **WHERE IT DOES BITE — THE DAYTIME ROLLBACK (08:15–16:00), the window Amendment 3 §2 already flags as exposed:**

> A manual stop **between 08:15 and 16:00** writes a clean exit for **THAT day**. The watcher's *"last clean exit was a PRIOR day"* then reads **FALSE for the rest of the day** ⇒ ⛔ **the watcher will not restart the service until tomorrow.**

- ⇒ ⭐ **A daytime rollback that includes a manual stop takes the twin down for the remainder of the session — SILENTLY**, because the suppression is **the watcher DECLINING**, ⛔ not anything failing. Nothing errors; nothing alerts.
- ⚠️ 💭 **INFERENCE**, read from the **repo** unit, which 📄 deploy never installs ⇒ it may differ from the twin's (hence `systemctl cat` above).
- 🏷️ **Scope (Amendment 11 §3):** *"do not manually stop"* is a rule **for THIS procedure**, ⛔ **not** a universal claim about `systemctl`.

### GATE 3 — PRE-COPY (the service must be stopped: after the 17:35 self-exit)
- **Service:** `systemctl is-active trading-system` must not be `active` or `activating`. Record the `ExecStart` `--mode` (📄 expected `live`; ⛔ confirm).
- ⛔🔴🔝 **IF THE SERVICE HAS NOT SELF-EXITED, DO NOT STOP IT.** (Amendment 9 §2 — the procedure previously had **no branch at all** for this, and the obvious move, `systemctl stop`, is exactly the shape of the 02:08 incident: a reasonable-looking action taken because the document did not say not to.)
  - **Record** `is-active`, the **uptime**, and the **last log lines** — then **STOP THE DEPLOYMENT.**
  - ⭐ **The window is MISSED; the next one is after the following clean exit.** ⚠️ Missing an evening costs a **day**. Forcing a stop on a service whose exit path feeds **tomorrow's start logic** costs something **unknown**, which is worse.
  - ⛔ **A manual stop is a VM state change that was never authorised**, and its interaction with the token watcher's *"last clean exit was a PRIOR day"* condition is ⛔ **not established**.
- **md5 at the VM, which must equal `970aabf`:**

  | File | md5 at `970aabf` |
  |---|---|
  | `main.py` | `85219d2285a0b07bc363ebd9e31bac6e` |
  | `signals/signal_processor.py` | `da8c6f983e92f8644656dbe0a081e51d` |
  | `core/config_loader.py` | `a034fc0816582717267bcb1ef70ba5f8` |
  | `config/expected_managers.yaml` | `1dad38c53d556db8c8652389f2838d5f` |

- **Absence:** `sr_shadow/` and `scripts/sr_shadow_evaluate.py` must NOT exist. If either exists ⛔ STOP.
- **YAML:** `config/system_config.yaml` must be `351bd82e73bb0301d850341191c7b72b`. Any mismatch ⛔ STOP.
- **Cron:** the crontab must not already contain `sr_shadow_evaluate`. A duplicate ⛔ STOP.
- **Rename preconditions** (added ~02:09 per Amendment 7): the guarded writes replace the directory entry, so they would silently break a symlink or hard link, and could change mode or owner.
  - Run: `cd /home/ubuntu/systems/trading-system && stat -c '%n|%F|%a|%U:%G|links=%h' core/config_loader.py signals/signal_processor.py main.py config/expected_managers.yaml config/system_config.yaml`
  - Each must be a **`regular file`**, **`links=1`**, owner **`ubuntu`**; **record each mode**. Any symlink, hard link or other owner ⛔ STOP.
  - **Absence:** none of `core/config_loader.py.tmp`, `signals/signal_processor.py.tmp`, `main.py.tmp`, `config/expected_managers.yaml.tmp`, `config/system_config.yaml.tmp` may exist. If any exists ⛔ STOP.

- ⭐ **ALL GATE 3 CHECKS IN ONE READ-ONLY SWEEP** (added ~07:33, Amendment 8 §3 — previously these were six separate prose checks an operator had to assemble). Nothing below writes. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && echo "== service (must NOT be active/activating) ==" && systemctl is-active trading-system; echo "== md5 (all five must equal 970aabf / 351bd82e) ==" && md5sum main.py signals/signal_processor.py core/config_loader.py config/expected_managers.yaml config/system_config.yaml; echo "== absence (both must say ABSENT) =="; { [ -e sr_shadow ] && echo "sr_shadow PRESENT" || echo "sr_shadow ABSENT"; }; { [ -e scripts/sr_shadow_evaluate.py ] && echo "evaluator PRESENT" || echo "evaluator ABSENT"; }; echo "== rename preconditions (regular file, links=1, owner ubuntu; RECORD each mode) ==" && stat -c "%n|%F|%a|%U:%G|links=%h" core/config_loader.py signals/signal_processor.py main.py config/expected_managers.yaml config/system_config.yaml; echo "== stray .tmp (nothing listed = clean) =="; ls -l core/config_loader.py.tmp signals/signal_processor.py.tmp main.py.tmp config/expected_managers.yaml.tmp config/system_config.yaml.tmp 2>/dev/null; echo "== cron (count MUST be 0) =="; crontab -l 2>/dev/null | grep -c sr_shadow_evaluate'
```
  ⛔ Any single failure above is a **STOP**. ⚠️ The `crontab -l` count is a `grep -c`, so `0` is the pass value and the command exits non-zero on 0 matches — ⭐ read the printed number, ⛔ not the exit status.

### GATE 4 — COPY 17 FILES (VM DEPLOYMENT SCOPE 17 · COMMIT SCOPE 27 · ⛔ tests and harness never copied)
- **Source:** the committed bytes of `e7bf477`, ⛔ never the PC working copies (three have CRLF).
- **Transfer — ORDERED, one group at a time** (amended ~01:25 per Amendment 4 §2). The md5 of each group is checked at the destination **before the next group is sent**; the first mismatch ⇒ ⛔ STOP → rollback.

  | Order | Group | Why here |
  |---|---|---|
  | 4a | `sr_shadow` (12 files) | the code must exist before anything references it |
  | 4b | `scripts/sr_shadow_evaluate.py` | not on the boot path |
  | 4c | `core/config_loader.py` | the new loader accepts the old YAML, `enabled: False` |
  | 4d | `signals/signal_processor.py` | its new `sr_shadow=None` kwarg is harmless under the old `main.py` |
  | 4e | `main.py` | ⛔ must follow 4d: `970aabf`'s `SignalProcessor.__init__` has **no `sr_shadow` param and no `**kwargs`**, and the new `main.py` passes `sr_shadow=sr_shadow` unconditionally (`main.py:3640`) ⇒ a TypeError at boot in ANY mode |
  | 4f | `config/expected_managers.yaml` | **LAST**: the registry only ever expects a manager whose code and wiring are already in place |

  **⛔🔴🔝 4-PRE — THE PRE-WRITE IDENTITY CHECK, IMMEDIATELY BEFORE THE FIRST VM WRITE (Amendment 17 §2).** The frozen artifacts were corrected **hours** before this window; confirm the manifest points at the **CURRENT set and nothing else**. ⛔ **If the manifest and the files disagree, STOP — never copy using one version and compare using another.** ⭐ Routine frozen-artifact hygiene after a late correction, ⛔ not a new gate. **`RUNNABLE — LITERAL COMMAND`**
```
md5sum D:/Projects/_preservation/EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_v12_2026-09-16T1338IST.md D:/Projects/_preservation/NORMALIZATION_RULESET_17-Sep-2026__frozen_v4_2026-09-16T1138IST.md D:/Projects/_preservation/normalize_bootlog__frozen_v3_2026-09-16T1138IST.py D:/Projects/_preservation/validate_window__frozen_2026-09-16T1225IST.py
```
  Must read **`41e2cdec41411651ea29bdcac7c87d2a`** · **`0fab34f53387c54a8d536292e77d22b5`** · **`0cbcf225048e079c4ac83f06e044745a`** — prediction **v6**, ruleset **v4**, normalizer **v3**. ⛔ Superseded versions and the original calibration extracts stay **KEPT**; ⛔ **do not overwrite the first calibration with the post-fix run** — both are evidence.

  **4a and 4b (new, inert files) — tar, unchanged** (Amendment 8 §2 keeps these on tar: a truncated NEW file destroys nothing, nothing imports them before 4e, and the per-group checksum catches it first). ⚠️ They are ⛔ **NOT** idempotent-reporting — a re-run silently re-extracts. That is safe here and ⛔ nowhere else.

  **4a** — the 12 `sr_shadow/` files. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep archive --format=tar e7bf477 sr_shadow/__init__.py sr_shadow/bars.py sr_shadow/calendar.py sr_shadow/decision.py sr_shadow/evaluator.py sr_shadow/params.py sr_shadow/pipeline.py sr_shadow/pricing.py sr_shadow/runner.py sr_shadow/schema.py sr_shadow/store.py sr_shadow/zones.py | ssh -o BatchMode=yes trading-sbx 'tar -x --no-overwrite-dir -C /home/ubuntu/systems/trading-system'
```
  Verify 4a. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum sr_shadow/__init__.py sr_shadow/bars.py sr_shadow/calendar.py sr_shadow/decision.py sr_shadow/evaluator.py sr_shadow/params.py sr_shadow/pipeline.py sr_shadow/pricing.py sr_shadow/runner.py sr_shadow/schema.py sr_shadow/store.py sr_shadow/zones.py'
```

  **4b** — the evaluator. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep archive --format=tar e7bf477 scripts/sr_shadow_evaluate.py | ssh -o BatchMode=yes trading-sbx 'tar -x --no-overwrite-dir -C /home/ubuntu/systems/trading-system'
```
  Verify 4b. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum scripts/sr_shadow_evaluate.py'
```

  **4c–4f (EXISTING boot-path files): one IDEMPOTENT GUARDED WRITE-THEN-RENAME per file** (Amendment 7 §1 shape; the inline precondition and the three outcomes added by Amendment 8 §2, contract above). The old file stays intact until verified new bytes replace it in one `rename(2)`. ⭐ Each prints exactly one of `WROTE` · `ALREADY_DONE` · `REFUSED_DRIFT` · `REFUSED_WRITE`.

  ⛔ **Run them in this order.** `4e` before `4d` is a TypeError at boot; `4f` is always LAST.

  **4c** — `core/config_loader.py`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:core/config_loader.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < core/config_loader.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "5b27302483de514ec3117442267609f3" ]; then cat > /dev/null; echo "ALREADY_DONE core/config_loader.py"; exit 0; fi; if [ "$cur" != "a034fc0816582717267bcb1ef70ba5f8" ]; then cat > /dev/null; echo "REFUSED_DRIFT core/config_loader.py have=${cur:-NONE} want=a034fc0816582717267bcb1ef70ba5f8"; exit 1; fi; cat > core/config_loader.py.tmp && [ "$(md5sum < core/config_loader.py.tmp | cut -c1-32)" = "5b27302483de514ec3117442267609f3" ] && chmod --reference=core/config_loader.py core/config_loader.py.tmp && mv -- core/config_loader.py.tmp core/config_loader.py && echo "WROTE core/config_loader.py" || { rm -f -- core/config_loader.py.tmp; echo "REFUSED_WRITE core/config_loader.py"; exit 1; }'
```
  **4d** — `signals/signal_processor.py`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:signals/signal_processor.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < signals/signal_processor.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "d45cc437815dba5eb876602724fbb52f" ]; then cat > /dev/null; echo "ALREADY_DONE signals/signal_processor.py"; exit 0; fi; if [ "$cur" != "da8c6f983e92f8644656dbe0a081e51d" ]; then cat > /dev/null; echo "REFUSED_DRIFT signals/signal_processor.py have=${cur:-NONE} want=da8c6f983e92f8644656dbe0a081e51d"; exit 1; fi; cat > signals/signal_processor.py.tmp && [ "$(md5sum < signals/signal_processor.py.tmp | cut -c1-32)" = "d45cc437815dba5eb876602724fbb52f" ] && chmod --reference=signals/signal_processor.py signals/signal_processor.py.tmp && mv -- signals/signal_processor.py.tmp signals/signal_processor.py && echo "WROTE signals/signal_processor.py" || { rm -f -- signals/signal_processor.py.tmp; echo "REFUSED_WRITE signals/signal_processor.py"; exit 1; }'
```
  **4e** — `main.py`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:main.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < main.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "5aacc1b8028682405834b7dd6238ab5a" ]; then cat > /dev/null; echo "ALREADY_DONE main.py"; exit 0; fi; if [ "$cur" != "85219d2285a0b07bc363ebd9e31bac6e" ]; then cat > /dev/null; echo "REFUSED_DRIFT main.py have=${cur:-NONE} want=85219d2285a0b07bc363ebd9e31bac6e"; exit 1; fi; cat > main.py.tmp && [ "$(md5sum < main.py.tmp | cut -c1-32)" = "5aacc1b8028682405834b7dd6238ab5a" ] && chmod --reference=main.py main.py.tmp && mv -- main.py.tmp main.py && echo "WROTE main.py" || { rm -f -- main.py.tmp; echo "REFUSED_WRITE main.py"; exit 1; }'
```
  **4f** — `config/expected_managers.yaml`. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show e7bf477:config/expected_managers.yaml | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/expected_managers.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "8625c4b724c34a41f09f06297e3cd797" ]; then cat > /dev/null; echo "ALREADY_DONE config/expected_managers.yaml"; exit 0; fi; if [ "$cur" != "1dad38c53d556db8c8652389f2838d5f" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/expected_managers.yaml have=${cur:-NONE} want=1dad38c53d556db8c8652389f2838d5f"; exit 1; fi; cat > config/expected_managers.yaml.tmp && [ "$(md5sum < config/expected_managers.yaml.tmp | cut -c1-32)" = "8625c4b724c34a41f09f06297e3cd797" ] && chmod --reference=config/expected_managers.yaml config/expected_managers.yaml.tmp && mv -- config/expected_managers.yaml.tmp config/expected_managers.yaml && echo "WROTE config/expected_managers.yaml" || { rm -f -- config/expected_managers.yaml.tmp; echo "REFUSED_WRITE config/expected_managers.yaml"; exit 1; }'
```
  - **After each command** — **`RUNNABLE — LITERAL COMMAND`** *(one file shown; the same three checks for each of `core/config_loader.py`, `signals/signal_processor.py`, `main.py`, `config/expected_managers.yaml`)*:
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && md5sum main.py && stat -c %a main.py && ls -l main.py.tmp 2>/dev/null; echo TMP_ABSENT_IF_NOTHING_ABOVE'
```
    md5 = the committed md5 in the table below · `stat -c %a` = the mode Gate 3 recorded · the `.tmp` absent. Else ⛔ STOP → rollback.
  - ⛔ **Why the md5 sits BETWEEN `cat` and `mv`:** 🔬 PC demo (~02:05) shows a stream cut short with a clean EOF makes `cat` exit **0**. `cat > tmp && mv tmp path` alone would therefore rename a PARTIAL file into place. Only the checksum can tell a short stream from a complete one.
  - 🔬 **REHEARSED END-TO-END ON THE PC (~07:27, real blobs, real digests, network removed):** a sandbox seeded with the real `970aabf` bytes ran these four commands ⇒ all four `WROTE`, landing on exactly the four `e7bf477` digests in the table below; an immediate re-run ⇒ all four `ALREADY_DONE` rc 0; no stray `.tmp`. ⭐ **NON-VACUOUS** — the same `4e` command REFUSED twice minutes later: a 90,000-byte truncated `main.py` ⇒ `REFUSED_WRITE`, and the wrong blob ⇒ `REFUSED_WRITE`, with `main.py` left at `85219d22…` both times.
- ⛔ **Never one archive of all 17.** 🔬 `git archive` emits paths SORTED ⇒ `config/expected_managers.yaml` is extracted FIRST and `sr_shadow/` LAST, the exact unsafe order (verified with `tar -t`, ~01:20).
- **Check:** every one of the 17 must equal its committed md5.

| # | Path | Committed md5 (`e7bf477`) | Destination md5 | Result |
|---|---|---|---|---|
| 1 | `config/expected_managers.yaml` | `8625c4b724c34a41f09f06297e3cd797` | ⏸ pending | ⏸ |
| 2 | `core/config_loader.py` | `5b27302483de514ec3117442267609f3` | ⏸ pending | ⏸ |
| 3 | `main.py` | `5aacc1b8028682405834b7dd6238ab5a` | ⏸ pending | ⏸ |
| 4 | `scripts/sr_shadow_evaluate.py` | `edebd2d8251084584cad8eca2ef3002c` | ⏸ pending | ⏸ |
| 5 | `signals/signal_processor.py` | `d45cc437815dba5eb876602724fbb52f` | ⏸ pending | ⏸ |
| 6 | `sr_shadow/__init__.py` | `a8eaba39c80dc9f45fe2fb18ab9d26fb` | ⏸ pending | ⏸ |
| 7 | `sr_shadow/bars.py` | `c28e35c1be186824f5112c982d09ed93` | ⏸ pending | ⏸ |
| 8 | `sr_shadow/calendar.py` | `06fe4b44155b2ef9455abdf152b0a44a` | ⏸ pending | ⏸ |
| 9 | `sr_shadow/decision.py` | `bc5a62dfaf1e0faec8c48d1e24e54b1a` | ⏸ pending | ⏸ |
| 10 | `sr_shadow/evaluator.py` | `b7ad4a264a8158db26add8a6f23c5d16` | ⏸ pending | ⏸ |
| 11 | `sr_shadow/params.py` | `25f6e350257a2e85e13a85a670ab5bdd` | ⏸ pending | ⏸ |
| 12 | `sr_shadow/pipeline.py` | `a2bd0dbb2a7a583e56614b0c4814f2f2` | ⏸ pending | ⏸ |
| 13 | `sr_shadow/pricing.py` | `da30bf651c4e4caa2135a4ac7f92d098` | ⏸ pending | ⏸ |
| 14 | `sr_shadow/runner.py` | `d8216592c3d49b60ca16ae5a72044883` | ⏸ pending | ⏸ |
| 15 | `sr_shadow/schema.py` | `2e5b2a833b09c90d30747a1ed2c6c566` | ⏸ pending | ⏸ |
| 16 | `sr_shadow/store.py` | `90c087593218ca9aee30127cb57f204c` | ⏸ pending | ⏸ |
| 17 | `sr_shadow/zones.py` | `e055bb399ab7901b209155313ec52560` | ⏸ pending | ⏸ |

### GATE 5 — VM-LOCAL `config/system_config.yaml` (⛔ copy-back, never hand-edit)
- **Pre-change md5:** `351bd82e73bb0301d850341191c7b72b` (the 15-Sep fetch; re-checked in Gate 3).
- **Post-change md5:** `4eab1ae5a9716059431b55a210e917c9` = that fetch + the `e7bf477` `sr_shadow:` block.
  - The block is 25 lines, md5 `2ac7322e489fc07e32857c58ab2afa12`, = `git show e7bf477:config/system_config.yaml | sed -n '/^sr_shadow:/,/^regime:/p' | sed '$d'`.
  - Regenerate deterministically if the scratch copy is lost; the result must hash to `4eab1ae5…`.
- **Loader validation, done 🔬 locally** (Python 3.11.9, pydantic 2.13.0, PyYAML 6.0.3):
  - `e7bf477` + block ⇒ VALID `enabled: True`;
  - `e7bf477` without block ⇒ VALID `enabled: False`;
  - `970aabf` + block ⇒ INVALID `extra_forbidden`;
  - `970aabf` without block ⇒ VALID.
- **Source files, preserved outside git** (~02:08) so recovery never depends on the session scratchpad:
  - PRE `D:/Projects/_preservation/TWIN_system_config_PRE-SR-SHADOW_md5-351bd82e__preserved_2026-09-16T0208IST.yaml` (55,554 bytes);
  - POST `D:/Projects/_preservation/TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml` (56,846 bytes).
  - Both were scanned: env-var NAMES only, no secret values; one sandbox alert address.
- **Transfer — IDEMPOTENT GUARDED WRITE-THEN-RENAME** (Amendment 7 §1 replaced the original `cat > config/system_config.yaml`, which 🔬 **truncated the only VM copy BEFORE the first byte arrived** — 0 bytes one second in; Amendment 8 §2 made the precondition three-outcome). The drift precondition is inside the command, so a re-run reports `ALREADY_DONE` instead of an ambiguous `REFUSED`. **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/system_config.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "4eab1ae5a9716059431b55a210e917c9" ]; then cat > /dev/null; echo "ALREADY_DONE config/system_config.yaml"; exit 0; fi; if [ "$cur" != "351bd82e73bb0301d850341191c7b72b" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/system_config.yaml have=${cur:-NONE} want=351bd82e73bb0301d850341191c7b72b"; exit 1; fi; cat > config/system_config.yaml.tmp && [ "$(md5sum < config/system_config.yaml.tmp | cut -c1-32)" = "4eab1ae5a9716059431b55a210e917c9" ] && chmod --reference=config/system_config.yaml config/system_config.yaml.tmp && mv -- config/system_config.yaml.tmp config/system_config.yaml && echo "WROTE config/system_config.yaml" || { rm -f -- config/system_config.yaml.tmp; echo "REFUSED_WRITE config/system_config.yaml"; exit 1; }' < D:/Projects/_preservation/TWIN_system_config_POST-SR-SHADOW_md5-4eab1ae5__preserved_2026-09-16T0208IST.yaml
```
  - Then the md5 at the destination must be `4eab1ae5…`, the mode must equal Gate 3's, and the `.tmp` must be absent.
  - 🔬 PC demo of this exact shape (~02:05): short stream ⇒ REFUSED, target still `351bd82e`, no `.tmp`; empty stream ⇒ REFUSED, intact; full stream ⇒ `4eab1ae5`, no `.tmp`.
  - 🔬 **RE-REHEARSED ~07:27 with the three-outcome guard, against the real preserved YAML:** `351bd82e…` ⇒ `WROTE` ⇒ `4eab1ae5…`; immediate re-run ⇒ `ALREADY_DONE` rc 0; a deliberately drifted target ⇒ `REFUSED_DRIFT config/system_config.yaml have=b9292e45… want=351bd82e…` rc 1, ⭐ proving the branch is reachable and distinct.
  - 📄 `mv` within one directory is `rename(2)`, atomic on one filesystem (POSIX). The PC demo proves the shell logic, ⛔ not the twin's ext4.
  - The config goes from valid-without-block to valid-with-block in one instant, so Gate 5 never adds an invalid-config moment on top of the Gate 4f cell.
  - ⚠️ If the remote shell is KILLED mid-transfer, the `||` cleanup cannot run: check `config/system_config.yaml.tmp` is absent afterwards; if present, remove it by that literal path and record it (no scratch residue on the VM).
- **Validate ON THE VM** with the deployed loader (read-only; `load_all` and its imports write nothing). ⭐ The payload goes over stdin so there is **no nested quoting** to get wrong. **`RUNNABLE — LITERAL COMMAND`**
```
echo 'from pathlib import Path; from core.config_loader import load_all; c = load_all(Path("config")); print("LOAD_ALL OK sr_shadow.enabled=", c.system.sr_shadow.enabled)' | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && /home/ubuntu/systems/venv/bin/python -B -'
```
  It must print `LOAD_ALL OK sr_shadow.enabled= True`. Then print the block back.

### GATE 6 — CRON (hand-added, testing VM only; ⛔ never the canonical crontab or `cron_registry.yaml`)
Exactly these two lines, appended to the user crontab. Record the installed crontab diff (+2 lines only) and the timestamp. ⚠️ The fence below is the **crontab CONTENT** to add by hand, ⛔ not a shell command — the TEMPLATE/RUNNABLE labels do not apply to it. ⛔ **Never** pipe it to `crontab -` blind: that replaces the WHOLE crontab.
```
# sr_shadow_evaluate  [16:05 Mon-Fri]  S&R SHADOW v1.3 EOD evaluator — HAND-ADDED, TESTING VM ONLY
5 16 * * 1-5 cd /home/ubuntu/systems/trading-system && set -a && . ./.env && set +a && PYTHONPATH=. /home/ubuntu/systems/venv/bin/python scripts/sr_shadow_evaluate.py >> logs/cron-sr-shadow-evaluate.log 2>&1
```

### GATE 7/8 — BOOT (17-Sep 08:15, normal; ⛔ never forced; never restart over a manual stop)

> ⛔🔴🔝 **FOR THE 17-Sep RUN, THE NORMALIZER'S EXIT CODE CARRIES NO VERDICT.** 🔬 On a change pair it **inverts** (correct deploy ⇒ rc 1; manager never started ⇒ rc 0) and it is **blind to a missing event**. ⭐ **Under stress an exit code is read as a verdict — that is exactly when this would bite.** Record its **residual list**; the verdict comes from the **per-event table**.
⛔🔴🔝 **NAME THE SINK WHEREVER A MARKER IS READ — ⛔ THIS IS A MARKER-READING RULE, ⛔ NOT A BOOT-WINDOW RULE (Amendment 30 §1).** ⚠️ **"Verify in the boot log" was AMBIGUOUS: the Gate 2 baseline names TWO logs** — `BASELINE_journal_…txt` **and** `BASELINE_system_…log` — ⭐ **and the five checks below do ⛔ NOT all live in the same one.**

⛔🔴 **THE SINK IS PER-MARKER, BECAUSE THE LEVEL IS PER-MARKER** (🔬 verified at `e7bf477`; stdout handler is `setLevel(WARNING)`, `core/logger.py:420`):

| Marker | Level | Sink |
|---|---|---|
| `sr_shadow: ENABLED and started` | **INFO** (`main.py:3537`) | ⛔ **`logs/system_<DATE>.log` ONLY — NEVER the journal** |
| `effect_telemetry: composition OK` | **INFO** (`core/effect_telemetry.py:190`) | ⛔ **`logs/system_<DATE>.log` ONLY — NEVER the journal** |
| `composition assertion FAILED` | **CRITICAL** (`:209`) | ✅ both |
| `sr_shadow wiring failed` | **ERROR** (`main.py:3539`) | ✅ both |

⚠️🔴 **AN OPERATOR WHO READS THE JOURNAL FOR THE TWO *INFO* ROWS FINDS NEITHER, CONCLUDES "THE MANAGER DID NOT COME UP", AND STOPS A CORRECT DEPLOY.** ⭐ **That is E-1 exactly, still live in Gate 7/8 until now — found by applying §1's general form rather than patching the two markers Amendment 29 named.**

Verify in the boot log — **`logs/system_<DATE>.log` unless the table above says otherwise**:
- `sr_shadow: ENABLED and started (mode=…, log-only)`;
- `effect_telemetry: composition OK`;
- ⛔ **grep explicitly for `composition assertion FAILED` and for any CRITICAL**, since in live a construction failure is a CRITICAL and the service continues;
- `sr_shadow wiring failed` must be absent;
- the config loads; compare against the previous boot's log for anything else changed (a config-hash change is expected).
- ⛔🔴🔝 **THE COMPARISON USES THE *FROZEN* ARTIFACTS AND THE *PRE-REGISTERED* LIST** (Amendment 12). ⛔ **NEVER a fresh reconstruction of 16-Sep**, and ⛔ **never a retrospectively manufactured baseline.**
  - Baseline: `BASELINE_journal_trading-system_16-Sep-2026.txt` + `BASELINE_system_16-Sep-2026.log`, at the filename/size/md5 recorded at Gate 2.
  - ⛔🔴 **STEP 0 — VALIDATE BOTH WINDOWS FIRST. ⛔ If either is invalid, STOP; the comparison is not run.** **`RUNNABLE — LITERAL COMMAND`**
```
python D:/Projects/_preservation/validate_window__frozen_2026-09-16T1225IST.py boot D:/Projects/_preservation/BASELINE_system_16-Sep-2026.log && python D:/Projects/_preservation/validate_window__frozen_2026-09-16T1225IST.py eod D:/Projects/_preservation/BASELINE_system_16-Sep-2026.log
```
    rc **0** = `WINDOW_OK` · rc **3** = `WINDOW_INVALID` · rc **2** = input unusable. ⭐ This rc **is** a precondition verdict — ⛔ unlike the normalizer's, which never is. Repeat for the 17-Sep log before comparing.
  - Prediction: `D:/Projects/_preservation/EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_v12_2026-09-16T1338IST.md` (md5 `41e2cdec41411651ea29bdcac7c87d2a`) — ⭐ **v6**; v1–v5 superseded, KEPT. ⭐ **It carries the WINDOW SPECIFICATION — ⛔ adjudicate every row in its own window.**
  - Normalization: `D:/Projects/_preservation/NORMALIZATION_RULESET_17-Sep-2026__frozen_v4_2026-09-16T1138IST.md` (md5 `0fab34f53387c54a8d536292e77d22b5`) + executable `D:/Projects/_preservation/normalize_bootlog__frozen_v3_2026-09-16T1138IST.py` (md5 `0cbcf225048e079c4ac83f06e044745a`). ⛔ Verify BOTH; ⛔ **NEVER widen R3** — CLOSED at eight.
  - ⛔🔴 **COMPARE PER AUTHORITATIVE SINK, BY ORIGIN:** application events **in the application log ONLY**; systemd lifecycle **in the journal ONLY**. ⛔ **Never compare an application event journal-to-journal** — a level flip would fake an appearance/disappearance.
  - ⛔🔴 **RECOGNITION IS BY FAMILY IDENTITY, NEVER BY COUNT.** Known families (`check_ntp_sync`, `email_fallback.sent`) are ordinary **at any count**; **one** instance of a new family is not. ⛔ **No numeric noise allowance.** The observed residual (3 instances, ONE comparison) is a **sample**, ⛔ not a rate and ⛔ not a budget.
  - **Fill the PER-EVENT RECORD TABLE in v3** — expected event · expected sink · expected multiplicity · observed multiplicity · observed sink · order requirement · **raw line ref** · result. ⛔ **Prose such as "the manager appeared" is NOT auditable.**
  - ⛔🔴 **CHECK EACH ROW IN ITS CORRECT SINK.** 🔬 The journal holds **WARNING+ ONLY** (stdout handler is `setLevel(WARNING)`) ⇒ ⛔ **the three INFO must-appear rows are in `logs/system_2026-09-17.log`, NOT the journal. Their absence from the journal is NOT a finding.**
  - **Multiplicity is part of the test:** E-1 rows **exactly 1** each — **0 ⇒ a finding** (dead manager), **2 ⇒ an anomaly** (double construction). **Order asserted ONLY where the source proves it** (E1.1 before E1.2); ⛔ incidental baseline order is **never** promoted to a contract. **Boot and EOD windows compared SEPARATELY.** **CRITICAL compared as SET-DIFFERENCE** — ⛔ one already in the baseline is not new. ⛔ **"Hash changed" is NOT proof of correct deployment** — record baseline, expected AND observed.
  - **Classify EVERY differing line** into **E-1** (new at boot) · **E-2** (changed — composition counts **both exactly +1**, config hash) · **E-3** (new at shutdown) · **E-4** (must be absent) · **E-5** (must be unchanged) · or **UNPREDICTED**.
  - **UNPREDICTED ⇒ adjudicate as an anomaly** · **E-1/E-2 absent ⇒ a finding** · **E-4 present ⇒ ⛔ STOP → ordered rollback.**
  - ⭐ Record the outcome **including any MISSES in the prediction**, ⛔ without editing the frozen list.

A failure ⇒ **ORDERED ROLLBACK** (standing note ~01:05, amended ~01:25):
1. Starters first (Gate 2).
2. Remove the block.
3. Restore the 4 wiring files from `970aabf` **in the reverse of the copy order**: `config/expected_managers.yaml` → `main.py` → `signals/signal_processor.py` → `core/config_loader.py`.
   - The registry goes first so it never expects an unbuilt manager.
   - `main.py` goes before `signal_processor.py` because new `main.py` + old `signal_processor.py` = TypeError.
4. Remove the cron line.
5. Run `load_all` under the restored loader.
6. Confirm `expected_managers.yaml` = `1dad38c5…`.
7. A normal boot.

- **Rollback mechanism** (~02:09, same guarded write-then-rename as Gates 4c–5, ⛔ never `cat >` straight onto a boot-path file; made IDEMPOTENT ~07:33 per Amendment 8 §2). ⭐ **Run these five in the order given.** Each prints one of `WROTE` · `ALREADY_DONE` · `REFUSED_DRIFT` · `REFUSED_WRITE`; ⭐ an operator re-running because they are unsure how far the rollback got now gets `ALREADY_DONE`, ⛔ not an ambiguous `REFUSED`.
  - **Step 2 — remove the block** (copy back the preserved PRE YAML). **`RUNNABLE — LITERAL COMMAND`**
```
ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/system_config.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "351bd82e73bb0301d850341191c7b72b" ]; then cat > /dev/null; echo "ALREADY_DONE config/system_config.yaml"; exit 0; fi; if [ "$cur" != "4eab1ae5a9716059431b55a210e917c9" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/system_config.yaml have=${cur:-NONE} want=4eab1ae5a9716059431b55a210e917c9"; exit 1; fi; cat > config/system_config.yaml.tmp && [ "$(md5sum < config/system_config.yaml.tmp | cut -c1-32)" = "351bd82e73bb0301d850341191c7b72b" ] && chmod --reference=config/system_config.yaml config/system_config.yaml.tmp && mv -- config/system_config.yaml.tmp config/system_config.yaml && echo "WROTE config/system_config.yaml" || { rm -f -- config/system_config.yaml.tmp; echo "REFUSED_WRITE config/system_config.yaml"; exit 1; }' < D:/Projects/_preservation/TWIN_system_config_PRE-SR-SHADOW_md5-351bd82e__preserved_2026-09-16T0208IST.yaml
```
  - **Step 3.1 — `config/expected_managers.yaml`** — the registry goes FIRST so it never expects an unbuilt manager. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:config/expected_managers.yaml | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < config/expected_managers.yaml; } 2>/dev/null | cut -c1-32); if [ "$cur" = "1dad38c53d556db8c8652389f2838d5f" ]; then cat > /dev/null; echo "ALREADY_DONE config/expected_managers.yaml"; exit 0; fi; if [ "$cur" != "8625c4b724c34a41f09f06297e3cd797" ]; then cat > /dev/null; echo "REFUSED_DRIFT config/expected_managers.yaml have=${cur:-NONE} want=8625c4b724c34a41f09f06297e3cd797"; exit 1; fi; cat > config/expected_managers.yaml.tmp && [ "$(md5sum < config/expected_managers.yaml.tmp | cut -c1-32)" = "1dad38c53d556db8c8652389f2838d5f" ] && chmod --reference=config/expected_managers.yaml config/expected_managers.yaml.tmp && mv -- config/expected_managers.yaml.tmp config/expected_managers.yaml && echo "WROTE config/expected_managers.yaml" || { rm -f -- config/expected_managers.yaml.tmp; echo "REFUSED_WRITE config/expected_managers.yaml"; exit 1; }'
```
  - **Step 3.2 — `main.py`** — before `signal_processor.py`: new `main.py` + old `signal_processor.py` = TypeError. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:main.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < main.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "85219d2285a0b07bc363ebd9e31bac6e" ]; then cat > /dev/null; echo "ALREADY_DONE main.py"; exit 0; fi; if [ "$cur" != "5aacc1b8028682405834b7dd6238ab5a" ]; then cat > /dev/null; echo "REFUSED_DRIFT main.py have=${cur:-NONE} want=5aacc1b8028682405834b7dd6238ab5a"; exit 1; fi; cat > main.py.tmp && [ "$(md5sum < main.py.tmp | cut -c1-32)" = "85219d2285a0b07bc363ebd9e31bac6e" ] && chmod --reference=main.py main.py.tmp && mv -- main.py.tmp main.py && echo "WROTE main.py" || { rm -f -- main.py.tmp; echo "REFUSED_WRITE main.py"; exit 1; }'
```
  - **Step 3.3 — `signals/signal_processor.py`** — safe here because old `main.py:3575` passes all 36 args BY KEYWORD (R2). **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:signals/signal_processor.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < signals/signal_processor.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "da8c6f983e92f8644656dbe0a081e51d" ]; then cat > /dev/null; echo "ALREADY_DONE signals/signal_processor.py"; exit 0; fi; if [ "$cur" != "d45cc437815dba5eb876602724fbb52f" ]; then cat > /dev/null; echo "REFUSED_DRIFT signals/signal_processor.py have=${cur:-NONE} want=d45cc437815dba5eb876602724fbb52f"; exit 1; fi; cat > signals/signal_processor.py.tmp && [ "$(md5sum < signals/signal_processor.py.tmp | cut -c1-32)" = "da8c6f983e92f8644656dbe0a081e51d" ] && chmod --reference=signals/signal_processor.py signals/signal_processor.py.tmp && mv -- signals/signal_processor.py.tmp signals/signal_processor.py && echo "WROTE signals/signal_processor.py" || { rm -f -- signals/signal_processor.py.tmp; echo "REFUSED_WRITE signals/signal_processor.py"; exit 1; }'
```
  - **Step 3.4 — `core/config_loader.py`** — last; the loader accepts the old YAML. **`RUNNABLE — LITERAL COMMAND`**
```
git -C D:/Projects/wt-sr-shadow-15sep show 970aabf:core/config_loader.py | ssh -o BatchMode=yes trading-sbx 'cd /home/ubuntu/systems/trading-system && cur=$({ md5sum < core/config_loader.py; } 2>/dev/null | cut -c1-32); if [ "$cur" = "a034fc0816582717267bcb1ef70ba5f8" ]; then cat > /dev/null; echo "ALREADY_DONE core/config_loader.py"; exit 0; fi; if [ "$cur" != "5b27302483de514ec3117442267609f3" ]; then cat > /dev/null; echo "REFUSED_DRIFT core/config_loader.py have=${cur:-NONE} want=5b27302483de514ec3117442267609f3"; exit 1; fi; cat > core/config_loader.py.tmp && [ "$(md5sum < core/config_loader.py.tmp | cut -c1-32)" = "a034fc0816582717267bcb1ef70ba5f8" ] && chmod --reference=core/config_loader.py core/config_loader.py.tmp && mv -- core/config_loader.py.tmp core/config_loader.py && echo "WROTE core/config_loader.py" || { rm -f -- core/config_loader.py.tmp; echo "REFUSED_WRITE core/config_loader.py"; exit 1; }'
```
  - After each: md5, mode and `.tmp` absence, exactly as in the deploy.
  - 🔬 **REHEARSED ~07:27 on the PC sandbox, full round trip:** after the deploy rehearsal left all five files at `e7bf477`/`4eab1ae5`, these five commands in this order restored **all five to exactly the `970aabf` / `351bd82e…` digests**; an immediate re-run ⇒ `ALREADY_DONE` rc 0; no stray `.tmp`.
- ⛔ **Do NOT delete `sr_shadow/` or `scripts/sr_shadow_evaluate.py` in a rollback.** The `970aabf` wiring never references them, so they are inert, and deleting is extra work that can fail (Amendment 4 §2).
- The same reverse order applies to a **partial** Gate 4 failure: restore only the wiring files that landed, in that order.
- **Intermediate states verified** (Amendment 5, ~01:40):
  - **R0** (new all four, block removed) is the ONE unavoidable composition-incomplete state; the stopped service covers it.
  - **R1, R3 and R4** are safe.
  - **R2** (old `main.py` + new `signal_processor.py`) is safe **only because** old `main.py:3575` passes all 36 arguments **by keyword** (0 positional; `sr_shadow` is NOT the last parameter).
  - ⛔ **Never restore `signal_processor.py` before `main.py`:** new `main.py` + old `signal_processor.py` ⇒ `TypeError: unexpected keyword argument 'sr_shadow'`.

### GATE 9 — FIRST SESSION (17-Sep, measurement only)
Per the deploy card §4 and Amendment §6: TIME_CLOSE is a diagnostic only; print both P counts (R-C); ⛔ no tuning.

---

## ROLLBACK — THE STANDING NOTES, VERBATIM FROM SYSTEM_MAP

### ⛔🔝 STANDING NOTE — S&R SHADOW ROLLBACK IS ATOMIC (testing VM)

**ROLLBACK = all of the following in ONE stopped-service action, or none. There is no valid partial rollback:**
1. Restore **ALL FOUR** wiring files from `970aabf`: `main.py`, `signals/signal_processor.py`, `core/config_loader.py`, `config/expected_managers.yaml`.
2. In the same action, **REMOVE** the VM-local `sr_shadow:` block from `config/system_config.yaml`. ⛔ It is **not optional**.
3. Remove the hand-added cron line.
4. `sr_shadow/`, `scripts/sr_shadow_evaluate.py` and `data_store/sr_shadow/` may be left in place: nothing imports them once the wiring is reverted.

**Hazards:**
- ⛔ **`sr_shadow.enabled: false` ALONE IS NOT A ROLLBACK.** The registry still says `expected-active`, so `assert_composition` (`main.py:4277` @ `e7bf477`) either RAISES (paper, a failed boot) or sends a CRITICAL and continues (live). A quick disable must take the registry entry out in the same action.
- ⛔ **A LEFTOVER `sr_shadow:` BLOCK UNDER THE `970aabf` LOADER KILLS THE BOOT IN ANY MODE.** 🔬 At `970aabf`, `SystemConfig` has `model_config = ConfigDict(extra="forbid")` (`core/config_loader.py:1988`) and system_config.yaml is checked with `schema_cls.model_validate(data)` (`:2507`). Config load precedes the mode, so this hits live too.
  - The amendment's step 3 ("the block may be left or removed; inert either way") is **WRONG**.
  - 🔬 **Proven locally** on the twin's own `system_config.yaml`, as fetched on 15-Sep (md5 `351bd82e…`):

    | Loader | YAML | Result |
    |---|---|---|
    | `970aabf` | + block | **INVALID `sr_shadow: extra_forbidden`** |
    | `970aabf` | as-is | VALID (control) |
    | `e7bf477` | + block | VALID, `enabled: True` (post-append md5 `4eab1ae5…`) |
    | `e7bf477` | as-is | VALID, `enabled: False` (the gap between steps 5 and 6 is safe) |

- ⚠️ **The same pairing applies going forward:** the four wiring files and the VM-local block are one unit, deployed together in one stopped-service window.


### ⛔🔝 STANDING NOTE — S&R SHADOW ROLLBACK ORDER (supersedes the order in the ~01:00 note; the content is unchanged)

Config validity by loader and block (🔬 proven locally on the twin's own YAML, ~01:00):

| Loader | Block present | Config load |
|---|---|---|
| `970aabf` | yes | ⛔ **INVALID** (`extra_forbidden`), the ONLY invalid cell |
| `970aabf` | no | valid |
| `e7bf477` | yes | valid, `enabled: True` |
| `e7bf477` | no | valid, `enabled: False` |

- **DEPLOY order:** files first, then the block.
- **ROLLBACK order is NOT the mirror image:**
  1. Confirm the service is stopped.
  2. **REMOVE the VM-local `sr_shadow:` block** (state: new loader, no block ⇒ valid).
  3. **Restore all four wiring files from `970aabf`** (state: old loader, no block ⇒ valid).
  4. Remove the hand-added cron line (independent of the other steps).
  5. Validate that the config loads under the restored loader.
  6. Confirm `config/expected_managers.yaml` is back at its `970aabf` md5 `1dad38c5…`.
  7. Only then allow a normal boot.
- ⛔ Restoring the files first passes THROUGH the invalid cell, and is safe only if nothing boots meanwhile.
- ⚠️ **One refinement, recorded and not contested:** every state in this order is **config-valid**, but the states between step 2 and the end of step 3 are **composition-inconsistent**. The registry still lists `sr_shadow` as `expected-active` while nothing constructs it, so a boot there ⇒ paper RAISES / live CRITICAL. The same is true forward, between steps 5 and 6. The **stopped service** stays the guard for that dimension, so both windows must be one uninterrupted stopped-service action.


---

## VM-LOCAL YAML — COPY-BACK RULE, VERBATIM

### STEP 6 — COPY BACK THE VALIDATED FILE; ⛔ NEVER HAND-EDIT ON THE VM
1. The VM's current `config/system_config.yaml` must be md5 **`351bd82e73bb0301d850341191c7b72b`**, the file fetched 15-Sep. ⛔ Any other value ⇒ **STOP**: the VM has drifted and the validated append no longer applies.
2. Copy back the locally built file: that fetch + the `e7bf477` `sr_shadow:` block (25 lines, md5 `2ac7322e…`). It is validated under the `e7bf477` loader (`enabled: True`), md5 **`4eab1ae5a9716059431b55a210e917c9`**.
3. Re-verify **`4eab1ae5…`** at the destination.


---

## KNOWN DEFECT IN THE SPOT-CHECK SCRIPT, VERBATIM

### ⛔🔝 KNOWN DEFECT — `scripts/sr_corp_action_spotcheck.py` CAN PRINT A FALSE PASS
- **What:** `main()` never checks that the returned candles span the ex-date. Any series with ≥ 2 rows and every overnight close ratio within 15% of 1.0 prints **"VERDICT: ADJUSTED (continuous) — historical_data returns split/bonus-adjusted candles. ✅"**. That includes a series that is **entirely after** the event.
- **Script hash:** md5 `d954c1781e55ebf68d44c9c815ef353e`, identical at `970aabf` and `e7bf477`. It ships with SNR-DETECTOR-V1 (`dea336a`) and is on the testing VM.
- **Plausible cause** (💭 inference, not verified): an instrument-token change at an ISIN change, as with V2RETAIL on 25-Mar-2026, can return only post-event bars.
- 🔬 **Reproduction** (PC, 16-Sep ~00:55; FAKE broker, fabricated data):
  - a stub `kiteconnect` module whose `historical_data` returns only weekday sessions **≥ 2026-03-25** at a flat 205.0;
  - `main(["--symbol","V2RETAIL","--around","2026-03-25","--window","20"])` prints `V2RETAIL around 2026-03-25: 11 daily candles` · `largest overnight close ratio = 1.000 at None` · **`VERDICT: ADJUSTED (continuous) … ✅`**, rc 0;
  - the capture wrapper, from the same rows, shows `sessions BEFORE 2026-03-25: 0`.
- **Also known:** it prints neither the first nor last date, nor the per-side counts, so a reader cannot see the gap.
- ⛔ **Do not trust its headline.** Adjudicate from the returned rows.
- ✅⚠️🔝 **THE LIVE NEAR-MISS, 16-Sep 08:26 — keep this beside the reproduction (Amendment 9 §4).** The real V2RETAIL window returned **exactly 11 post-ex-date rows — the SAME COUNT as the fabricated post-only reproduction above** (*"11 daily candles"*). ⭐ **It passed on real grounds ONLY because 14 pre-ex-date rows were there too.** ⚠️ **A narrower `--window` could have returned the post-only shape, and the script would have printed `ADJUSTED ✅` with nothing behind it.** ⇒ ⭐ **This is the argument for row-level adjudication, in one concrete case:** the headline was identical in both; only the per-side counts told them apart. ⛔⭐ **A reader comparing the two outputs AT HEADLINE LEVEL would have seen IDENTICAL evidence for a false pass and a real one** — same verdict string, same candle count. **14 before / 11 on-after** is the only thing that separated them.
- **Not fixed; not this deployment's job.**

## AMENDMENT 3 NOTES, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 3" (16-Sep). Nothing needed from Rama; ⛔ the VM is still untouched.

1. **Why the rollback order stays even with the service stopped.** If something DOES start the service mid-transition, the two intermediate states are not equally bad:
   - composition incomplete ⇒ **live: a CRITICAL and the service stays up** (paper: a failed boot);
   - config invalid ⇒ **a failed boot in ANY mode**, before the mode is read.

   On this live VM, the order turns a guaranteed boot failure into a CRITICAL alert. It costs nothing.
2. **⛔ "Keep the service stopped" is a rule, not an enforceable condition.** A clock-driven starter exists (the token watcher, polling every 30 s from 08:00). Before ANY deploy or rollback transition:
   - establish and record every starter;
   - confirm none can fire in the window;
   - mask or stop any that could, FIRST, and restore it LAST, recording both.

   ⛔ A rollback near 08:15 deals with the starter before touching a single file. Procedure: manifest Gate 2 (~01:12).
3. **The deploy manifest is now in this tracked file** (`MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026`, ~01:12): 17 paths with committed md5, the YAML pre/post md5 and validation, the exact cron line, the starter inventory, the wrapper source and the resume rule. **If the Claude session closes, nothing runs; a fresh session resumes from that manifest plus the cards.**


---

## AMENDMENT 4 NOTES, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 4" (16-Sep). ⛔ No docs commit, ⛔ no amend. Nothing needed from Rama beyond receiving the file. The VM is still untouched.

1. **Standalone manifest, outside every git repository** (§1):
   - **`D:/Projects/_preservation/SR_SHADOW_V1_3_DEPLOY_MANIFEST_16-Sep-2026__preserved_2026-09-16T0128IST.md`**, 348 lines, md5 `87fbc44b59d9efb415b5b7879e649a89`.
   - It is assembled from this file's manifest (as amended ~01:25) plus the verbatim rollback, copy-back and defect notes, with a precedence line.
   - 🔬 `_preservation/` is not a git repo. It follows the folder's existing `__preserved_<stamp>` convention; Rama saves it with the cards.
   - 📄 **Correction to the card's table:** the memory ledger is also outside git (`~/.claude/projects/…/memory/`, 🔬 not a repo), so `reset --hard` cannot touch it. It holds only the essentials, though, so the standalone file remains the complete copy.
2. **Ordered copy inside Gate 4** (§2), now in the manifest: `sr_shadow/` → evaluator → `config_loader.py` → `signal_processor.py` → `main.py` → `expected_managers.yaml` LAST, with md5 per group before the next.
   - 🔬 **Two facts behind the order:**
     - `git archive` emits SORTED paths, so the planned single archive would have extracted the registry FIRST;
     - `970aabf`'s `SignalProcessor.__init__` has no `sr_shadow` param and no `**kwargs`, while the new `main.py:3640` passes `sr_shadow=` unconditionally ⇒ new `main.py` before new `signal_processor.py` = a TypeError at boot in ANY mode. The card listed the three wiring files as one step; the order within it matters.
   - **Rollback:** restore the files in the exact reverse order (registry → `main.py` → `signal_processor.py` → `config_loader.py`), after removing the block. ⛔ Never delete `sr_shadow/` or the evaluator.
3. **Starter suppression narrowed** (§3, ChatGPT's refinement): identify → can it fire in the window → only then the least invasive supported suppression → record → restore exactly → verify. ⛔ Never blind-mask infrastructure.
   - The watcher cannot start at or after 16:00, nor after a same-day clean exit ⇒ the 17:42 window is safe from it (re-check at 17:42).
   - ⚠️ A rollback between 08:15 and 16:00 IS exposed.
4. **VM-side `load_all` placement accepted** (§4): after the copy-back, before cron and any boot.


---

## AMENDMENT 5 — ROLLBACK STATES VERIFIED, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 5" (16-Sep). Verification only: no code, no commit, and the VM is still untouched.

**⛔ Correction to my own Amendment 4 reply:** "no intermediate state has a config, composition or TypeError failure" was **wrong about R0**. R0 (all four files new, block removed) is composition-incomplete, as I had stated myself when answering Amendment 3.

### The rollback states, verified (block already removed; restore order registry → `main.py` → `signal_processor.py` → `config_loader.py`)

| # | VM state | Verdict | Evidence (🔬 local, `e7bf477` vs `970aabf`) |
|---|---|---|---|
| R0 | new all four · no block | ⚠️ **UNSAFE, unavoidable**: the registry expects `sr_shadow`, nothing builds it ⇒ live CRITICAL + continue / paper raise | (a) + (b) below |
| R1 | new main/sp/loader · OLD registry · no block | SAFE | `enabled` defaults False ⇒ not built and not registered; the old registry does not list it; config valid (matrix row 4) |
| R2 | OLD main · new sp/loader · old registry | **SAFE, by keyword binding** (§3 below) | old call: 0 positional, 36 keywords, binds by NAME |
| R3 | OLD main/sp · new loader · old registry | SAFE | no caller passes `sr_shadow`; config valid (matrix row 4) |
| R4 | all OLD · no block | SAFE | matrix row 2 |

**(a) With no block, `enabled` defaults to False.**
- `SrShadowConfig.enabled: bool = False` (`core/config_loader.py` @ `e7bf477`, class at :1266).
- 🔬 Runtime proof: matrix row 4 printed `VALID enabled: False` on the twin's own YAML.

**(b) With `enabled` False, the manager is neither constructed nor registered.** 🔬 `git grep` over the `e7bf477` tree, excluding tests:
- The only `_effect_handle("sr_shadow")` is `sr_shadow/runner.py:120`, inside `SrShadowService.__init__`.
- The only `SrShadowService(` is `runner.py:252`, inside `build_sr_shadow`.
- The only `build_sr_shadow(` is `main.py:3529`, inside `if _sr_shadow_on:` (`:3526`), where `_sr_shadow_on = bool(cfg is not None and cfg.enabled)` (`:3489`).
- No `register_constructed("sr_shadow")` exists anywhere; the infra tuple (`main.py:4262–4273`) does not name it.

**Why no order removes R0** (the card's argument, confirmed from code): restoring the registry BEFORE removing the block gives new loader + block + old registry ⇒ `enabled: True` ⇒ built and registered but absent from the registry ⇒ `unknown` in `effect_telemetry.assert_composition` (`core/effect_telemetry.py:182`) ⇒ a composition failure. Every order has exactly one unsafe window; this one lands on the CRITICAL-and-continue path on the live VM, not on a config-load failure. The stopped service covers it.

### §3 — the silent positional-binding hazard, checked
1. **Is `sr_shadow` the LAST parameter? ⛔ NO.** In `e7bf477`, `SignalProcessor.__init__` has 43 params including `self`; `sr_shadow` sits at **index 31 of 42**, inserted after `sr_detector` and before `zone_warmer`. The last is `evidence`. No `*args` and no `**kwargs`.
2. **Does old `main.py` bind by keyword? ✅ YES, completely.** 🔬 An AST pass over every non-test `SignalProcessor(` call:
   - `970aabf` `main.py:3575` (the only site) = **positional 0 · `*` expansions 0 · `**` expansions 0 · 36 keywords · 0 duplicates**.
   - `inspect.Signature.bind` of those 36 keywords against the NEW signature ⇒ **OK**: every keyword binds by name, none unexpected, and `sr_shadow` is not supplied (→ default `None`).
   - (`e7bf477` `main.py:3607`: positional 0, 37 keywords.)
   - Non-vacuity control: the same counter on `SignalProcessor(q, store, bus, *extra, mode=1, **kw)` reports positional 4 · `*` 1 · `**` 1.
- ⇒ **R2 is SAFE.** Keyword binding is position-independent, so the inserted parameter cannot shift any argument. The safety condition is (1) **OR** (2); the card's "if either is not true, R2 is unsafe" was stricter than needed, and (2) holds.
- ⛔ **The card's fallback ("swap `main.py` and `signal_processor.py` — safe in the other direction") would NOT have been safe.** Restoring `signal_processor.py` first creates **new `main.py` + old `signal_processor.py`**. 🔬 Binding `e7bf477` `main.py:3607`'s 37 keywords against the `970aabf` signature ⇒ **`TypeError: got an unexpected keyword argument 'sr_shadow'`**, a boot crash in ANY mode (the Amendment 4 finding). That state is not R3.
- ⇒ The restore order **registry → `main.py` → `signal_processor.py` → `config_loader.py` stays**. ⚠️ If a future edit makes old `main.py` pass anything positionally, re-run this check before any rollback.
- Scripts (scratchpad, session-only): `sp_call_binding_check.py` and `sp_call_binding_check_reversed.py`.

### Copies (§4)
Three copies, three failure modes:
- the preserved file in `_preservation/`, outside git;
- SYSTEM_MAP: discoverable, dies to `reset --hard`;
- the ledger: outside git, essentials only.

No docs commit; `e7bf477` stays unamended.


---

## AMENDMENT 6 — ONE UNSAFE CELL + PARTIAL WRITES, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 6" (16-Sep). It corrects its own §3 connective and fallback (both already recorded ~01:40). The VM is still untouched; `e7bf477` is unchanged.

### §2 — the forward walk, verified against the evidence already gathered
| After | State | Verdict | Evidence |
|---|---|---|---|
| 4a+4b `sr_shadow/`, evaluator | old wiring + inert new files | SAFE | nothing at `970aabf` imports them |
| 4c `config_loader.py` | new loader · blockless YAML · old main/sp/registry | SAFE | matrix row 4 (`enabled: False`); loader diff is +75/−0, additive only |
| 4d `signal_processor.py` | old main × new sp | SAFE | the R2 proof: 0 positional, 36 keywords bind by name, `sr_shadow` → `None` |
| 4e `main.py` | new main/sp/loader · old registry · no block | SAFE (= R1) | `enabled: False` ⇒ `build_sr_shadow` not reached ⇒ nothing built or registered ⇒ the old registry expects nothing |
| 4f `expected_managers.yaml` | new all four · no block | ⚠️ **UNSAFE (= R0)** | registry expects `sr_shadow`, nothing builds it |
| Gate 5 block | new all four + block | SAFE if construction succeeds | built, registered, expected; a construction failure = live CRITICAL (Gate 7/8 grep) |

⇒ **Confirmed: one cell, entered from below by the deploy and from above by the rollback:** NEW registry PRESENT + block ABSENT. No ordering removes it (the alternative lands on `unknown`, `effect_telemetry.py:182`).

### ⛔ But that is not the whole starter requirement: partial files
- 🔬 **Demo** (PC, GNU tar 1.35, ~01:50–01:55): an interrupted stream over an existing `970aabf` `main.py` ⇒ tar rc=2 "Unexpected EOF". The file was replaced by a **147,968-byte `main.py` that compiles but has no `__main__` guard**. The old file does not survive.
  - 💭 As a service it would exit 0 having done nothing ⇒ no restart (`Restart=on-failure`), no watcher retry on a same-day clean exit (📄 05-Aug) ⇒ a **silent** no-trade day.
  - ⚠️ The twin's tar version and behaviour are **not measured**; the demo is the PC's GNU tar.
- **Where partial states occur:** Gates 4c–4e happen BEFORE the registry changes, and every rollback restore writes files, so the card's rule ("from the registry change until the block matches") leaves them uncovered.
- **The operative rule, now in the manifest above both ordered procedures:** from the first write to any boot-path file until every written file verifies at its target md5 AND `load_all` passes on the VM, the service must not start. Deploy and rollback alike. The card's cell is a special case of it.
- For the 17:42 deploy this changes nothing in practice: the window is already after 16:00 and after the same-day clean exit, so no starter can fire (re-checked at Gate 2). It matters for a daytime rollback.

### Optional hardening — PROPOSED, ⛔ NOT ADOPTED without a word
For the four boot-path wiring files and the YAML: write each file only after it has **fully arrived and its md5 verifies**. For example: `git show e7bf477:<path> | ssh trading-sbx "<read all stdin in memory, compare md5 to the manifest value, write the target only on a match>"`.
- It removes the network-truncation class entirely, with no scratch file.
- It does not remove a crash during the local disk write (milliseconds).
- It is not required: the stopped service plus the per-group checksum gate already cover the risk.
- **Standalone manifest, current version (~01:57):** `D:/Projects/_preservation/SR_SHADOW_V1_3_DEPLOY_MANIFEST_16-Sep-2026__preserved_2026-09-16T0156IST.md`, 485 lines, md5 `4102d6cf1cbafd786d0ce9c99747b822`. It supersedes 0145 (kept).


---

## AMENDMENT 7 — GUARDED WRITE-THEN-RENAME, VERBATIM


**Card:** "DEPLOYMENT CARD AMENDMENT 7" (16-Sep). The VM is still untouched; `e7bf477` is unchanged.

1. **Confirmed: `cat > config/system_config.yaml` destroys the file first.** 🔬 PC demo (~02:05): with a producer sleeping 2 s, the target was **0 bytes one second in**; the shell's `O_TRUNC` fires before any data.
2. **⛔ Refinement: `cat > <path>.tmp && mv <path>.tmp <path>` alone is NOT enough.** 🔬 PC demo (~02:05): a stream cut to 5,000 bytes and ending in a **clean EOF** makes `cat` exit **0**, so the `&& mv` branch runs and a PARTIAL file is renamed into place.
   - `cat` cannot tell a short stream from a complete one. A remote EOF can arrive before a SIGHUP, for example when the client side ends early.
   - ⇒ **The md5 must gate the rename.**
   - The adopted form, per file: `[pre-md5 check &&] cat > P.tmp && [ md5(P.tmp) = expected ] && chmod --reference=P P.tmp && mv -- P.tmp P || { rm -f -- P.tmp; echo REFUSED; exit 1; }`
   - 🔬 Demo of that exact shape: short ⇒ REFUSED, target intact `351bd82e`, no `.tmp` · empty ⇒ REFUSED, intact · full ⇒ `4eab1ae5`, no `.tmp`.
3. **Two side effects of rename, now gated in Gate 3:**
   - `mv` replaces the directory entry, so it would silently turn a symlink or hard link into a regular file, and the new inode takes the `.tmp`'s mode.
   - ⇒ Gate 3 requires `regular file`, `links=1`, owner `ubuntu`, and records the mode; `chmod --reference` preserves it; the post-check compares it.
   - Gate 3 also requires every `<path>.tmp` to be absent beforehand.
4. **Adopted for Gate 4c–4f as well** (the card's "recommended, take it or leave it"): taken in the lighter per-file form, same directory with no staging directory, for the four EXISTING boot-path files only.
   - `sr_shadow/` and the evaluator stay on `git archive | tar -x` with per-group md5: they are new and inert, since nothing imports them until `main.py` lands after their md5 passes.
   - The rollback restores (the PRE YAML, then the four `970aabf` files) use the same guard.
5. **Durability:** the PRE (`351bd82e…`) and POST (`4eab1ae5…`) YAML copies are now preserved outside git in `D:/Projects/_preservation/…T0208IST.yaml`. Neither recovery nor the Gate 5 source depends on the session scratchpad any more.
6. **"No scratch files on the VM":** each `.tmp` is renamed into the deployed file on success and removed by literal path on refusal. A KILLED remote shell cannot run the cleanup, so the post-check requires the `.tmp` absent; residue is removed by literal path and recorded.
7. **§2 confirmations noted:** the cron line first fires on 17-Sep, not today. A V2RETAIL PASS approves beginning Gate 2 only; it is ⛔ not permission to skip Gates 2–8.

---

## AMENDMENT 8 — IDEMPOTENT GUARDED WRITES + TEMPLATE/RUNNABLE LABELLING, VERBATIM

**Card:** "DEPLOYMENT CARD AMENDMENT 8" (16-Sep), handed over **07:15 IST**, ahead of its own 08:14 slot; applied ~07:21–~07:35 IST. ⛔ The VM is still untouched; `e7bf477` is unchanged, unamended and unpushed.

⚠️ **Time-label correction:** this pass's first draft labelled its own work `~07:35 / ~07:40 / ~07:45 / ~07:55 / 0800`, **ahead of the system clock** — the same class of defect as the 0128 version's. 🔬 Corrected against artifact mtimes: contract demo **07:21** · rehearsal **07:27** · wrapper extracted **07:30**, preserved **07:31** · manifest amended **07:29–07:33** · this copy **07:35**.

1. **§1 closed.** Amendment 7's form is the rule: the md5 must sit BETWEEN `cat` and `mv`, because `cat` cannot tell a short stream from a complete one. Both rename side effects (mode from the `.tmp`; a symlink or hard link silently replaced) stay covered by the Gate 3 preconditions.
2. **§2 ADOPTED — the inline current-md5 precondition goes in EVERY guarded write, and it is IDEMPOTENT.**
   - ⛔ **The trap:** with an inline precondition, a write that has ALREADY SUCCEEDED fails its precondition on a second run — the file is at the TARGET md5, not the EXPECTED-CURRENT one ⇒ `REFUSED`, rc 1, **output identical to genuine drift.** An operator re-running a rollback at 08:10 cannot tell *"already done"* from *"something is wrong."*
   - **The fix — three precondition outcomes, four terminal states:** `md5(P)` = EXPECTED-CURRENT ⇒ proceed (`WROTE`, or `REFUSED_WRITE` rc 1 if the stream is short/empty, target untouched) · = TARGET ⇒ `ALREADY_DONE` rc 0 · anything else, including absent ⇒ `REFUSED_DRIFT` rc 1.
   - **Applied to all four boot-path files in BOTH directions** (Gates 4c–4f and the four rollback restores) **and to Gate 5** (POST copy and PRE copy-back).
   - ⛔ `sr_shadow/` and the evaluator stay on tar, as the card directs. ⚠️ Recorded: they are **NOT** idempotent-reporting — a re-run silently re-extracts.
3. **§3 ADOPTED — TEMPLATE versus RUNNABLE.** Every command carries `RUNNABLE — LITERAL COMMAND` or `TEMPLATE — DO NOT RUN`, with a **mechanical** criterion so the label is checkable: `grep -oE '<[A-Za-z_][A-Za-z0-9_ .-]*>'` over a RUNNABLE command returns nothing.
   - ⭐ **The templates that mattered are now literal.** Gate 4 previously gave ONE example and said *"4d, 4e and 4f are identical in shape"* — i.e. the operator had to CONSTRUCT three boot-path commands by hand at 17:45, the exact shape of the 02:08 incident. All four are now literal, as are 4a (12 paths spelled out), 4b, Gate 5, all five rollback restores, Gate 1's three steps and a new one-paste Gate 3 sweep.
   - Two fences are neither: the Gate 1 wrapper (a **Python source listing**) and the Gate 6 block (**crontab content**). Both are marked as such.

### 🔬 Evidence
- ⭐ **No digest was transcribed by hand**: the runnable commands are emitted by a generator from one verified table, and the markdown is assembled from that generator's output.
- **All 21 digests reproduce** from the refs' blobs (`git show <sha>:<path> | md5sum`): the 17 `e7bf477` files, the 4 `970aabf` wiring files, plus both preserved YAMLs. ⚠️ Confirmed `git show` emits **raw blob bytes despite `core.autocrlf=true`**.
- **Guard contract demo (~07:21, six cases)** and a **full round-trip rehearsal (~07:27)** in a PC sandbox seeded with the real `970aabf`/`351bd82e…` bytes: deploy ⇒ all five at the committed `e7bf477`/`4eab1ae5…` digests; re-run ⇒ all `ALREADY_DONE` rc 0; rollback in the mandated order ⇒ all five back to `970aabf`/`351bd82e…`; re-run ⇒ `ALREADY_DONE`. No stray `.tmp` at any point.
- ⭐ **NON-VACUOUS** — the same commands went RED three times: truncated `main.py` ⇒ `REFUSED_WRITE`; wrong blob ⇒ `REFUSED_WRITE` (left at `85219d22…` both times); drifted YAML ⇒ `REFUSED_DRIFT have=b9292e45…`.
- **All 20 RUNNABLE commands parse under `bash -n`** (parse only, nothing executed), and the Gate 3 sweep was run against the sandbox and produced every expected field.
- ⚠️🔬 ⛔ **ONE CHECK WAS VACUOUS AND IS REPORTED AS SUCH: mode preservation.** Windows did not honour `chmod 600` on the fixture (`stat -c %a` read 644 before and after) ⇒ `chmod --reference` could not have been observed failing. ⭐ The protection is the **VM-side `stat -c %a` after every write**. Limit inherited from Amendment 7.

### 🔴 FINDING — §2's larger claim does not hold as written
> §2: *"It makes the whole transfer sequence re-runnable from the top … That is exactly the gap in the resume rule … This closes it."*

- ✅ **True at FILE level** (demonstrated, both directions).
- 🔴 ⛔ **NOT true at SEQUENCE level.** Gate 3's preconditions are *absence* and *pre-state* checks that a partial run has already falsified, so a second pass STOPS at Gate 3 and never reaches the idempotent writes: `sr_shadow/` must not exist (4a/4b landed it) · the 4 wiring md5s must equal `970aabf` (4c–4f landed) · the YAML must be `351bd82e…` (Gate 5 landed) · the crontab must not contain `sr_shadow_evaluate` (Gate 6 landed). ⭐ **It is the same two-outcome trap, surviving one gate earlier.**
- ⏸ **OWED — ⛔ NOT FIXED, deliberately.** Widening Gate 3 changes the deploy procedure's STOP conditions, which Amendment 8 does not authorise (*"No rebuild. No redesign."*). Until a decision: **a resumed run that trips Gate 3 STOPS and reports** — the safe direction, already what the gate does ⇒ the limit costs a **stall**, ⛔ never a bad write.

---

## 16-Sep-2026 (Wed) 08:26 IST — `RESULT-SR-SHADOW-V13-GATE1-V2RETAIL-16SEP2026` — ✅ **GATE 1 PASS** · ADJUDICATED FROM THE ROWS, ⛔ NOT THE HEADLINE · THE VM IS STILL UNCHANGED

**Authority:** 👤 Rama's 16-Sep ~00:20 delegated answer, §6 item 1. **Timing:** the in-session 08:25 timer fired; preconditions 08:25–08:26; the single run at **08:26:08–08:26:10 IST**, after the **08:15:01** token.

### Preconditions — both PASS
| Check | Required | 🔬 Measured | |
|---|---|---|---|
| `md5sum scripts/sr_corp_action_spotcheck.py` | `d954c1781e55ebf68d44c9c815ef353e` | `d954c1781e55ebf68d44c9c815ef353e` | ✅ exact |
| `data_store/session/zerodha_token.json` mtime | today | `2026-09-16 08:15:01.388324184 +0530` (257 B) | ✅ fresh, metadata only |
| wrapper identity (PC side) | `dc9476f3e43bbe64b161ed151e973a56` | same, checked before the run | ✅ |

### The run
- **ONE** read-only run, exactly the manifest's Gate 1 step 3 literal command. ⭐ **rc 0, stdout 2,711 B, stderr 0 B, and nothing was written on the VM.**
- **Broker calls, as counted by the wrapper: `instruments=1 historical_data=1`** — ⭐ recorded, ⛔ not repeated.
- **Evidence preserved outside git:** `D:/Projects/_preservation/GATE1_V2RETAIL_16-Sep-2026.stdout.txt` and `….stderr.txt` (0 B).
- **Instrument:** token **`3780097`**, exchange_token `14766`, `NSE`/`EQ`, name `V2 RETAIL`, lot 1, tick 0.01. ⚠️ **No ISIN field** — the Zerodha instruments dump does not carry one, so the manifest's *"ISIN if present"* resolves to **absent**, ⛔ not missed.
- **Request:** `from_date 2026-03-05` → `to_date 2026-04-14`, `interval day`. **Rows 25 · first session `2026-03-05` · last `2026-04-13` · duplicates 0.**
- **Counts: 14 sessions BEFORE 2026-03-25 · 11 ON/AFTER.**

### ✅ ADJUDICATION = **PASS**, on three independent grounds
1. **Both sides of the ex-date are present** — 14 before, 11 on/after. ⛔ This is **not** a post-split-only series.
2. **No ~10:1 discontinuity.** Last pre `2026-03-24` close **192.70** → first post `2026-03-25` open **195.00**, close **196.30**: close→close ratio **1.0187**. An UNADJUSTED 10:1 series would read **~0.10** here. 🔬 Across the **whole** 25-session window the extreme overnight close ratios are **max 1.0542 / min 0.9561** — nothing anywhere approaches a split break.
3. ⭐ **An independent arithmetic fingerprint, computed from the rows and owing nothing to the script:** **14/14** pre-ex-date rows have all four prices landing on whole rupees when multiplied by 10, and **14/14** have volume divisible by 10; post-ex-date only **3/11** and **1/11**. ⇒ the pre-history is (original prices ÷ 10) and (original volume × 10) — **the 10:1 split has ALREADY been applied to it.**

⚠️🔝 **SCOPE OF GROUND 3 — stated so it is not over-read (Amendment 9 §4).** It is **a third independent consistency check ON THIS ONE CASE**, and good supporting evidence here. ⛔ It is **NOT** a general corporate-action detection rule and ⛔ **must not become one without separate validation** — the ÷10/×10 signature depends on the original tick and volume granularity and would not generalise to other ratios or instruments untested. ⭐ The PASS rests on grounds 1 and 2; ground 3 corroborates.

### ⛔ The known defect was checked, not assumed away
📄 The script's `VERDICT: ADJUSTED (continuous) — ✅` headline **can be false**: its failure mode is a window of **post-only candles**, where continuity is trivial (SYSTEM_MAP ~01:05). ⚠️ This window returned **exactly 11 post-ex-date rows**, the same count as in that defect note — but it **also** returned **14 pre-ex-date rows**, so the window spans the ex-date and the continuity is real. ⭐ **The headline was not used; grounds 1–3 above stand without it.**

### What this authorises — and what it does not
- ✅ **A PASS authorises BEGINNING Gate 2** (starter inventory, **~17:42 — the single adjudication checkpoint**, after the 17:35 self-exit; ⛔ **not 17:36**, Amendment 29 §2).
- ⛔ **It does NOT skip Gates 2–8**, and it is ⛔ **not** authority to copy anything. The VM remains untouched; `e7bf477` remains unpushed.

## 16-Sep-2026 (Wed) ~09:00 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT9-16SEP2026` — §2 CLAIM WITHDRAWN AND CORRECTED · ⛔ GATE 3 NOT TO BE WIDENED · ⛔ **NEVER MANUALLY STOP A SERVICE THAT DID NOT SELF-EXIT** · STOP TABLE ADOPTED

**Card:** "DEPLOYMENT CARD AMENDMENT 9" (16-Sep), for the evening window. ⭐ **It contains no commands — nothing in it is RUNNABLE.** ⛔ The VM is unchanged since Gate 1 (read-only); `e7bf477` unamended and unpushed; production untouched.

### §1 — the over-strong claim is WITHDRAWN, and the limit is now SETTLED, ⛔ not owed
- 👤 The card's author withdrew *"the whole transfer sequence is re-runnable from the top"* and replaced it with, verbatim: *"Each guarded existing-file write is idempotently re-runnable. The deployment SEQUENCE remains protected by Gate 3's strict pre-state barrier; after a partial transition, STOP and adjudicate the actual VM state rather than assuming a clean restart."*
- ⛔🔴 **DO NOT WIDEN GATE 3** — ⭐ its strictness **IS** the barrier. Making it permissive in advance trades a **stall** for a **guess**, and a stall is what you want when the VM state is unknown.
- 🏷️ The morning's entry is re-labelled: this moved from **⏸ OWED / undecided** to **✅ SETTLED**. ⭐ The finding itself was accepted as correct; only my proposed *remedy* was wrong.
- ⭐ **The per-file idempotency still earns its place** — it is what makes a **STOPPED** sequence safe to continue **by hand, one file at a time**, once the state has been adjudicated.

### §2 — 🔴 A MISSING BRANCH, NOW CLOSED: *"the service did not self-exit"*
- ⚠️ Gate 3 required a stopped service and checked `is-active`, but said **nothing about what to do if it is still up at 17:42.** ⭐ The obvious move — `systemctl stop` — is **exactly the shape of the 02:08 incident: a reasonable-looking action taken because the document did not forbid it.**
- **Now explicit in Gate 3:** ⛔ **DO NOT STOP IT.** Record `is-active`, uptime and the last log lines, then **STOP THE DEPLOYMENT**. The window is missed; the next is after the following clean exit.
- ⭐ **The asymmetry that decides it:** missing an evening costs a **day**; forcing a stop on a service whose exit path feeds **tomorrow's start logic** costs something **unknown** — worse. ⛔ The interaction with the token watcher's *"last clean exit was a PRIOR day"* condition is **not established**.

### §3 — the operator STOP table, ADOPTED
- Added beside the four terminal states: rc 0 `WROTE` / `ALREADY_DONE` ⇒ continue **after the independent post-check**; rc 1 `REFUSED_WRITE` / `REFUSED_DRIFT` ⇒ ⛔ STOP; **anything else** ⇒ ⛔ STOP.
- **On any stop:** gate · command · rc · stdout · stderr · **the observed md5 of every file touched in that gate**. ⛔ **No proceeding on inference.**
- ⚠️ Recorded with it: **`bash -n` proves SYNTAX only** — ⛔ not host, path, permissions or digests. Those are Gates 2–5, on the VM.

### §4 — Gate 1 ACCEPTED; the near-miss promoted into the preserved record
- ✅ **PASS stands** on row-level adjudication. ⛔ **The broker call is NOT to be repeated** — the evidence is preserved.
- ⭐ **The near-miss now sits beside the defect note itself**, where a future reader meets it: the live window returned **exactly 11 post-ex-date rows — the same count as the fabricated post-only reproduction** (*"11 daily candles"*). It passed on real grounds **only because 14 pre-ex-date rows were also present**. ⚠️ A narrower `--window` could have produced the post-only shape and the script would have printed `ADJUSTED ✅` with nothing behind it. ⇒ **the argument for row-level adjudication, in one concrete case.**
- ⚠️ **Ground 3 (the ÷10/×10 fingerprint) is scoped in place:** a third independent consistency check **on this one case**, ⛔ **not** a general corporate-action detection rule, and ⛔ not to become one without separate validation. ⭐ The PASS rests on grounds 1–2; ground 3 corroborates.

### §5 — carried forward, unchanged
Gates 2 → 3 → 4 → 5 → 6 exactly as defined, ⛔ never compressed into one command or one archive · the six-group order · guarded idempotent writes for 4c–4f and Gate 5 · service stopped throughout · starters identified and suppressed **only if they can fire** · **mode preservation verified VM-side, ⛔ never claimed from the PC rehearsal** · the rollback order and its verified states · ⛔ `sr_shadow/` and the evaluator never deleted · the script defect recorded and unfixed · no cleanup, no scope additions · `e7bf477` unamended and unpushed · production untouched.

⛔ **A Gate 1 PASS authorises beginning Gate 2. Nothing more.**

## 16-Sep-2026 (Wed) ~09:25 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT10-16SEP2026` — SELF-EXIT ADJUDICATED FROM EVIDENCE · 🔴 **THE STOP REASON IS ATTRIBUTABILITY, ⛔ NOT SAFETY** · TODAY'S BOOT LOG MUST BE PRESERVED TONIGHT

**Card:** "DEPLOYMENT CARD AMENDMENT 10" (16-Sep), before Gate 2. ⭐ **No commands in the card.** ⛔ The VM is unchanged since Gate 1 (read-only); `e7bf477` unamended and unpushed; production untouched.

### §1 — evidence, not the clock
- Gate 2 now carries the **three-case table** with the **token-watcher-risk column**, and the point that column makes: ⭐ **after 16:00 the watcher cannot fire in ANY of the three cases** (its condition needs **hour < 16**). ⇒ ⛔ **Case 3 is NOT a safety problem, and stopping there *for safety* would be superstition.**
- Required evidence **at the 17:42 checkpoint** (⛔ **not 17:36**, Amendment 29 §2) — ✅ **including BOTH shutdown markers read from `logs/system_<DATE>.log`**: `is-active` · uptime · **main PID** · last service log lines · observed **start and exit timestamps**.

### §2 — 🔴 the real reason, now the recorded one
- **Gate 7/8's comparison needs a previous boot to compare against.** With no healthy session today, every anomaly in tomorrow's boot log has **two candidate causes** — the deployment, or whatever was already wrong — and the gate **cannot separate them**.
- ⇒ the deploy would proceed **safely** and produce an **UNATTRIBUTABLE result**. ⛔ **If a normal session cannot be established: STOP, and say in the report that the reason is ATTRIBUTABILITY, not safety.**
- **Five recorded items** added to Gate 2, of which item 5 is the load-bearing one: ⭐🔝 **preserve TODAY'S FULL BOOT LOG TONIGHT, BEFORE the deployment** — *"tomorrow's comparison is against a file, not a memory, and it is worthless if nobody captured the before."*
- 📄 **Both log sources are covered**, established from the repo without touching the VM: the unit logs to the **journal** (`StandardOutput=journal`, `SyslogIdentifier=trading-system`) **and** the app writes **`logs/system_2026-09-16.log`** (the form used by the 11-Sep boot proofs). Five literal **RUNNABLE** commands added — state+`systemctl cat`, journal capture, app-log capture, health scan, and an md5 freeze of both artifacts.
- ⛔ **Snapshot immutability restated in place:** ⛔ never re-take these after the deployment — a re-taken baseline destroys the before/after pair **and leaves no trace**.

### 🔴 A mechanism found for Amendment 9 §2, while establishing the log paths
- 📄 The repo unit carries **`KillSignal=SIGINT`**: *"Send SIGINT on stop so main.py's Ctrl+C handler runs (clean shutdown, SHUTDOWN event, DB flush)."*
- ⇒ 💭 **a manual `systemctl stop` would run the SAME clean-shutdown path as a genuine self-exit**, plausibly manufacturing a **fake "clean exit today"** — which is precisely the token watcher's condition for tomorrow.
- ⚠️ Labelled as 💭 **INFERENCE**, read from the **repo** unit, which 📄 **deploy never installs** ⇒ it may differ from the twin's. ⭐ Hence `systemctl cat` is now part of Gate 2's capture. ⛔ The rule needed no mechanism; it now has a candidate one.

### §3 — near-miss sharpened, ground 3 unchanged
- Added: ⛔⭐ **a reader comparing the two outputs AT HEADLINE LEVEL would have seen IDENTICAL evidence for a false pass and a real one** — same verdict string, same candle count; **14 before / 11 on-after** was the only separator. It stays beside the defect note.
- Ground 3 (the ÷10/×10 fingerprint) remains scoped to this one case. **The PASS rests on grounds 1–2; ground 3 corroborates.**

### §4 — carried forward, unchanged
Gate 3 strict, ⛔ never widened · per-file idempotence with ⛔ no whole-sequence restartability claimed · the STOP table with an independent post-check **even on rc 0** · ⛔ no manual stop if the service is still active · six-group copy order · guarded writes on 4c–4f and Gate 5 · **mode verified VM-side only** · rollback order and its verified states · ⛔ `sr_shadow/` never deleted · the script defect recorded and unfixed · TEMPLATE/RUNNABLE labelling · no cleanup, no scope additions · `e7bf477` unamended and unpushed · production untouched · ⛔ **no repeat of the V2RETAIL call**.

⛔ **A Gate 1 PASS authorises beginning Gate 2. Nothing more.**

## 16-Sep-2026 (Wed) ~10:05 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT11-16SEP2026` — ⛔ **MY SIGINT INFERENCE WAS MISAIMED AND IS CORRECTED** · CASE B IS AN EVIDENCE PROBLEM · ⛔ NO NUMERIC SESSION THRESHOLD

**Card:** "DEPLOYMENT CARD AMENDMENT 11" (16-Sep), before the 17:30 alarm. ⭐ **No commands in the card.** ⛔ The VM is unchanged since Gate 1; `e7bf477` unamended and unpushed; production untouched.

### §1 — ⛔ the mechanism was aimed at the wrong window; **corrected in place**
- ⛔ **WITHDRAWN:** my claim that a manual stop **tonight** could manufacture a fake *"clean exit today"* and change tomorrow's start. ⭐ **The arithmetic refutes it:** a 17:35 self-exit and a 17:42 manual stop **both** date the clean exit **16-Sep**, and on **17-Sep 08:15 both read as "a PRIOR day"** ⇒ the watcher starts the service **either way**.
- ✅ **RE-AIMED, and it is a real hazard there:** a manual stop **during a DAYTIME rollback (08:15–16:00)** writes a clean exit for **THAT day** ⇒ *"last clean exit was a PRIOR day"* reads **FALSE for the rest of the day** ⇒ ⛔ **the watcher will not restart the service until tomorrow.** ⭐ **The twin goes down for the remainder of the session SILENTLY — the suppression is the watcher DECLINING, ⛔ not anything failing.** Nothing errors; nothing alerts.
- ⭐ This lands on exactly the window **Amendment 3 §2 already flagged as exposed**, and now says *why* in mechanism terms.
- 🏷️ The find itself stands (and `systemctl cat` stays in Gate 2 — the **installed** unit is what matters). ⭐ **Only its aim was wrong.**

### §2 — 🔴 Case B restated: the hazard tonight is **EVIDENCE**, not the watcher
- **The service being ACTIVE at the checkpoint is ITSELF A FINDING, to be PRESERVED, ⛔ not RESOLVED.**
- ⛔ A manual stop would produce a log **that looks EXACTLY like a clean 17:35 self-exit** — same SHUTDOWN event, same DB flush, same lines. ⭐ **The evidence of WHY it was still running would be gone, overwritten by a tidy shutdown the OPERATOR caused.**
- ⇒ same reason as Amendment 10 §2: **ATTRIBUTION, ⛔ not safety.** ⚠️ **Strictly worse than the watcher concern, because it is SILENT and PERMANENT.**

### §3 — adopted
- **Baseline artifact integrity:** **filename + size + md5**, immutable for the deployment record (the ⑤ command already emits all three).
- ⛔🔴 **NO NUMERIC "NORMAL SESSION" THRESHOLD.** Use the system's **existing routine log markers**; if they cannot establish a session, report **`BASELINE_NOT_ESTABLISHED`** and STOP. ⭐ A signal count or runtime minimum would be **an unvalidated parameter smuggled in through a deployment gate**.
- 🏷️ **Scope:** *"do not manually stop"* is a rule **for THIS procedure**, ⛔ not a universal claim about `systemctl`.
- Already in place and reconfirmed: `bash -n` proves **syntax only**; **exactly one CURRENT manifest pointer**.
- ✅ **The two-log-source find is confirmed as load-bearing** — neither review had it: the **journal** and **`logs/system_2026-09-16.log`** are **different artifacts**, and the baseline needs **both**, each captured and frozen.

### §4 — the stale alarm, recorded plainly
⭐ **AN ALARM IS A REMINDER, ⛔ NOT THE PROCEDURE.** The manifest and ledger are the authority and both are current; at 17:30 the work is driven from those. ⚠️ The timer's text lags (pre-Amendment-10, no baseline capture) and its re-arm was **denied** — ⭐ **a documentation mismatch, ⛔ not a deployment risk.** ⛔ **Do not retire a timer that fires on time to fix wording**; if ever replaced, **arm the replacement BEFORE retiring the old one.**

### §5 — tonight, in order
**17:30** alarm → **read the manifest, ⛔ not the alarm text**. **Gate 2 capture BEFORE any write:** installed unit via `systemctl cat` incl. drop-ins · `is-active` · uptime · main PID · start evidence and whether it was the **08:15 watcher start** · routine session markers **from existing log vocabulary** · CRITICAL · restarts · composition warnings · **the exit line, QUOTED, with its timestamp** · **both log sources preserved and md5-frozen as THE BASELINE**. ⛔🔴 **THEN WAIT FOR EVIDENCE OF THE SELF-EXIT — ⛔ DO NOT ADJUDICATE AT 17:30 (Amendment 28 §3): ACTIVE *before* the expected exit is NORMAL, ⛔ not a finding, and stopping on it FALSE-STOPS a healthy deployment.** **Only then adjudicate:** ACTIVE **after the expected self-exit** ⇒ ⛔ do not stop · record · STOP ·· inactive + healthy session ⇒ Gate 3 ·· inactive + baseline unprovable ⇒ ⛔ STOP for **attribution** (`BASELINE_NOT_ESTABLISHED`). **Gates 3 → 4 → 5 → 6 only on a clean Gate 2, ⛔ never compressed.**

## 16-Sep-2026 (Wed) ~10:10 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT12-16SEP2026` — ⭐ **THE EXPECTED DIFF IS PRE-REGISTERED AND FROZEN, ~7.5 h BEFORE THE WINDOW** · CAPTURE-FIRST · GATE 2 IS CONJUNCTIVE

**Card:** "DEPLOYMENT CARD AMENDMENT 12" (16-Sep), before the 17:30 alarm. ⭐ **No commands in the card.** ⛔ The VM is unchanged since Gate 1; `e7bf477` unamended and unpushed; production untouched.

### §1 — ✅ the pre-registered expected-diff list is **WRITTEN AND FROZEN ALREADY**
- ⭐ **Done at 10:07 IST, ⛔ not deferred to 17:36** — earlier is strictly better, because the prediction is then furthest from the diff it must be able to fail against. 🔬 Derived from `git diff 970aabf..e7bf477` over the four wiring files + the `e7bf477` `sr_shadow:` block + the twin's **live pre-deploy** YAML. ⛔ **No VM contact.**
- **`D:/Projects/_preservation/EXPECTED_DIFF_17-Sep-2026_boot__pre-registered_2026-09-16T1007IST.md` — 5,321 bytes, md5 `b5f7019c30095c1e536578f695a38710`.** Gate 2 now re-verifies that md5 before proceeding; a mismatch voids the test ⇒ STOP.
- **Five classes, 14 enumerated rows:**
  - **E-1 NEW AT BOOT (must appear):** `sr_shadow: worker started (contract=v1.3 schema=1 db=…/sr_shadow.db)` — 🔬 `CONTRACT_VERSION="v1.3"`, `SCHEMA_VERSION=1` — then `sr_shadow: ENABLED and started (mode=LIVE, log-only)` — 🔬 `mode_label` is **upper-cased**, and the unit runs `--mode live`. ⭐ **The ORDER is predicted too** (`start()` precedes the info line).
  - **E-2 CHANGED:** `effect_telemetry: composition OK (%d registered, %d expected)` — ⭐ **BOTH counts exactly +1**; ⛔ **+1 expected without +1 registered = the manager did not register ⇒ STOP.** Plus the config hash (`351bd82e…` → `4eab1ae5…`).
  - **E-3 NEW AT SHUTDOWN (17-Sep ~17:35):** `sr_shadow: worker stopped counters=… history=…`.
  - **E-4 MUST BE ABSENT:** `sr_shadow wiring failed…` · `effect_telemetry composition assertion FAILED…` · `sr_shadow: drain error=…` · `sr_shadow.stop_invariant_violated…` · any new CRITICAL.
  - **E-5 MUST BE UNCHANGED** — ⭐ **the sharpest prediction of the set:** the `main.py` diff adds `_sr_shadow_on` to the `_md_kite` build condition, so a naive reading expects a possible new *"no market-data kite handle"* warning. 🔬 **It cannot appear**: the twin's live config already has `sr_detector.enabled: true`, `v3_chain_mode: "shadow"` and `watchlist.enabled: true` ⇒ **that branch was ALREADY taken**. ⇒ the warning's presence/absence **must match the baseline exactly**. Also unchanged: `config_loader.py`'s 75-line diff is 🔬 **pydantic schema only — 0 logging statements** ⇒ no boot output at all.
- ⚠️ **One correction made while building it:** a first pass concluded `sr_shadow/` was **silent**. 🔬 It is not — `runner.py` logs through a `_safe_log` wrapper, which a narrow `_log.info(` grep missed. **E-1 row 1 exists because that was caught.**

### §2 — adopted into Gate 2
- ⛔ **CAPTURE FIRST, before any action that could alter state** — ⭐ the first operation after seeing ACTIVE is **evidence capture**.
- ⛔ **Gate 2 is CONJUNCTIVE: `INACTIVE` AND an expected clean exit AND a healthy session.** ⭐ **Inactive alone is ⛔ NOT a pass.**
- **Preserve without modifying the source logs; record the preservation BEFORE any write; two sources frozen independently; ⛔ do not over-collect** — those two, ⛔ not every log on the machine.
- **Gate 7/8 now says explicitly: use the FROZEN artifacts and the PRE-REGISTERED list**, ⛔ never a fresh reconstruction, ⛔ never a retrospectively manufactured baseline.

### §3 — tonight, in order
**17:30** alarm → **read the manifest, ⛔ not the alarm text**. **Gate 2, capture FIRST:** `systemctl cat` incl. drop-ins · `is-active` · uptime · main PID · timestamps · routine session markers from **existing log vocabulary** · CRITICAL · restarts · composition warnings · **the exit line, QUOTED** · **both log sources preserved + frozen (filename + size + md5)** · ⭐ **re-verify the frozen expected-diff md5**. ⛔🔴 **THEN WAIT FOR EVIDENCE OF THE SELF-EXIT — ⛔ DO NOT ADJUDICATE AT 17:30 (Amendment 28 §3).** **Only then adjudicate conjunctively:** ACTIVE **after the expected self-exit** ⇒ ⛔ do not stop · record · STOP ·· INACTIVE + clean exit + healthy ⇒ Gate 3 ·· anything less ⇒ ⛔ STOP, **`BASELINE_NOT_ESTABLISHED`**. **Gates 3 → 4 → 5 → 6 only on a clean Gate 2, ⛔ never compressed.**

## 16-Sep-2026 (Wed) ~10:25 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT13-16SEP2026` — 🔴 **v1 OF THE PREDICTION WOULD HAVE FAILED A CORRECT DEPLOYMENT** · SINK MAP ADDED · NORMALIZATION RULESET FROZEN

**Card:** "DEPLOYMENT CARD AMENDMENT 13" (16-Sep), before the 17:30 alarm. ⭐ **No commands in the card.** ⛔ The VM is unchanged since Gate 1; `e7bf477` unamended and unpushed; production untouched.

### §1 — the question was right; 🔴 **the answer found a WORSE problem one layer over**
- ✅ **The literal question resolves in the prediction's favour**, 🔬 from code, ⛔ no VM contact: handlers attach to the **ROOT** logger (`core/logger.py:375,452`), ⛔ **not per logger name**; `get_logger` merely calls `logging.getLogger` (`:266-273`); **`propagate = False` appears nowhere**; and `system_*.log`'s `_SystemFilter` is a **pure LEVEL catch-all** (`levelno >= INFO`) with ⛔ **no name restriction**. ⇒ **a brand-new `sr_shadow` logger DOES reach the system log.**
- 🔴⚠️ **BUT v1 NEVER SAID WHICH SINK EACH ROW LANDS IN — AND THE TWO SINKS HAVE DIFFERENT CUT-OFFS.** 🔬 The stdout handler is **`setLevel(WARNING)`** (`core/logger.py:420`) and the unit routes **stdout+stderr → journal** ⇒ ⛔ **EVERY `INFO` LINE IS ABSENT FROM THE JOURNAL.**
- ⭐ **All three "must appear" rows are INFO** — `sr_shadow: worker started`, `sr_shadow: ENABLED and started`, and `effect_telemetry: composition OK` ⇒ they exist **ONLY** in `logs/system_2026-09-17.log`.
- ⇒ 🔴 **Had Gate 7/8 looked for them in the journal, it would have found them absent, applied the rule "absent means the manager did not come up", and STOPPED A CORRECT DEPLOYMENT.** ⭐ **Exactly the failure §1 predicted — arriving through level routing rather than per-name handlers.**
- ✅ **v2 carries a SINK MAP** (10 rows × level × which file) so every row is checked in the right place, and matches on the JSON tuple **(`level`, `logger`, `msg`)** — 🔬 `system_*.log` is **JSON**, fields `ts`·`level`·`logger`·`msg` (`_JsonFormatter`). 🔬 E1.2's logger is **`main`** (`main.py:113,2187`).
- ⚠️ Recorded as a residual: `_safe_log` **swallows silently** (`runner.py:218-221`) ⇒ a logging failure inside the worker would be invisible. The routing is verified, so this is ⛔ not an expected event.

### §2 — the amendment window, both halves
⭐ **The prediction MAY be corrected at any time BEFORE the first VM write; it may NEVER be corrected after.** A pre-deployment correction is **timestamped, md5'd and supersedes, with the superseded version KEPT and the reason recorded** — ✅ done: **v1 (`b5f7019c30095c1e536578f695a38710`, 5,321 B) is intact on disk**, v2 supersedes it, and the reason is in both files. ⭐ *"The anti-rationalisation property comes from the prediction preceding the OBSERVATION, not from the file being untouchable from the moment it was typed."* ⛔ **From the first write tonight, the prediction is CLOSED.**

### §3 — the normalization ruleset is now its own frozen artifact
- **`NORMALIZATION_RULESET_17-Sep-2026__frozen_2026-09-16T1025IST.md` — 3,326 B, md5 `f56fe84ff11ba3c07a41989f243a915b`.** ⭐ *"Do not add exclusions after tomorrow's log" is a rule with no enforcement if the ruleset is a note someone can edit — frozen, widening it is ⛔ not a temptation resisted, it is a MISMATCH THAT SHOWS."*
- **R1** JSON key = (`level`, `logger`, normalized `msg`); **drop `ts` only**; ⛔ `level`/`logger` never normalized — they are under test. **R2** journal: strip the syslog prefix (host + **PID**) and systemd lifecycle timestamps, ⛔ **keep status/exit codes**. **R3** — ⛔ **CLOSED AT EXACTLY THREE** body rules, each justified by code: the runtime-resolved `db=` path, the session-dependent `counters=`/`history=` JSON, and the interpolated `<symbol>`.
- ⛔🔴 **The composition COUNTS are NEVER normalized — they ARE the measurement.** ⭐ Adding an R3.4 tomorrow is the escape hatch this file exists to close.

### §4 — adopted into v2 and the ruleset
**Normalized semantic events, ⛔ not raw lines** · **multiplicity** (E-1 exactly 1; **0 ⇒ finding**, **2 ⇒ anomaly**) · **order only where the SOURCE proves it**, ⛔ incidental baseline order never promoted to a contract · **boot and EOD windows observed separately** · **CRITICAL compared as a SET** — one already in the baseline is not new · **the three composition deltas stay distinct and the asymmetric case (+1 expected / +0 registered) is ⛔ NEVER downgraded to a warning** · **baseline and prediction stay separate artifacts** · ⛔ **"hash changed" is not proof of correct deployment** — record baseline, expected and observed · **row 12 means "no BOOT-TIME appearance expected"** — a runtime capture failure is a **runtime finding**, ⛔ not a boot-diff anomaly.

### §5 — Gate 1 independently confirmed by the card's author
✅ The fingerprint was re-read from the returned rows and matches: **all 14 pre-ex-date volumes end in zero; of the 11 on-or-after, only `1,026,230` does**; the 1-decimal price pattern runs through 03-25, 03-27 and 03-30 — **the 3 of 11**. Close continuity **192.70 → 196.30** against **~0.10** for an unadjusted 10:1 series. **Grounds 1–2 carry it; ground 3 corroborates and stays scoped to this case. 🔒 CLOSED — ⛔ do not repeat the call.**

## 16-Sep-2026 (Wed) ~10:50 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT14-16SEP2026` — 🔴 **THE NORMALIZER WAS WRONG AND THE CALIBRATION CAUGHT IT** · NOISE FLOOR MEASURED = 3 · E-4 OBSERVABILITY STATED (A7)

**Card:** "DEPLOYMENT CARD AMENDMENT 14" (16-Sep). ⭐ **No commands in the card.** ⛔ Nothing was written on the VM — the only VM contact was a **read-only** fetch of two boot-window extracts. `e7bf477` unamended and unpushed; production untouched.

### §2 — E-4 observability, stated rather than implied — ⭐ **this is A7**
- ⭐ *A must-absent row evaluated against a sink that cannot carry the event passes **by construction**.* ⛔ **A green check that could not have been red is worse than no check** — the same defect as `STOP_NOT_DEFENDED`, moved from the product into the deployment test.
- ✅ **Established from `e7bf477` source, with line numbers:** row 6 `main.py:3539` **ERROR** · row 7 `core/effect_telemetry.py:209` **CRITICAL** · row 8 `sr_shadow/runner.py:166` **ERROR** · row 9 `runner.py:216` **ERROR** · row 10 CRITICAL. **All ≥ WARNING ⇒ BOTH sinks carry them ⇒ ⛔ NO E-4 row is vacuous.** Now an explicit table in the prediction, ⛔ not an implication.

### §3 — 🔴 the calibration found a broken normalizer, exactly as predicted
- 🔬 **15-Sep vs 16-Sep boot windows**, `Trading System v… starting` → `composition OK` inclusive, **83 vs 82 events**. ⛔ **No code changed between them** ⇒ after normalization they must be identical.
- 🔴 **Ruleset v1 left 13 differing event-instances.** **Five message families were legitimately dynamic and v1 missed ALL FIVE:** `check_disk_space free=` (a live `shutil.disk_usage` reading, `utils/startup_checks.py:1242`) · `config_snapshotter: resolved config for <DATE>` (`core/config_snapshotter.py:184`) · `wrote config snapshot id=<ID> for <DATE>` (`:214`, `new_id` DB-assigned) · `startup_scenario=COLD: new day (prev=,today=)` (`utils/startup_checks.py:296`) · kill-switch `from <DATE> … new day <DATE>` (`capital/kill_switch.py:360`).
- ✅ Added as **R3.4–R3.8** — a **pre-deployment correction**, which Amendment 13 §2 permits and which costs nothing. ⛔ **Adding them tomorrow would have been the escape hatch everyone has been guarding against.**
- ⭐ **Why TARGETED date rules and not a blanket wildcard:** the calibration compared **two different days**, so **every date-bearing boot message necessarily differed and was therefore enumerated** ⇒ the targeted set is **complete for the boot window** and ⛔ masks no unknown field.
- 🔴 **OBSERVED RESIDUAL SAMPLE = 3 event-instances across the ONE available no-change comparison** *(⚠️ corrected by Amendment 15 §1: ⛔ NOT a "noise floor" and ⛔ not a false-positive rate — no denominator, no distribution)*, and they are **real day-to-day variance — ⛔ deliberately NOT normalized** (§3's more valuable finding):
  - **`check_ntp_sync`** — `drift 0.001s OK` **INFO** on 15-Sep vs `failed to query pool.ntp.org: timed out` **WARNING** on 16-Sep. ⚠️ **It flips LEVEL, so it flips JOURNAL VISIBILITY.**
  - **`telegram_notifier` / `email_fallback.sent`** (INFO) — present 15-Sep, absent 16-Sep.
- ⭐ **⇒ tomorrow's diff now has context — by FAMILY IDENTITY, ⛔ never by count** *(Amendment 15 §1)*: a **known family is ordinary at ANY count**; **ONE** instance of a **new** family is not.
- ⚠️ **For Gate 2's session-health read:** the 16-Sep **NTP timeout is a WARNING already in TODAY'S baseline** ⇒ tomorrow it is ⛔ **not new**, is ⛔ not deployment-caused, and is ⛔ not a reason to stop. Recorded so it is not mistaken for one.

### 🔴 Two further findings from the same pass
- **The composition prediction is now LITERAL:** 🔬 measured baseline **`62 registered, 62 expected`** on **both** calibration days ⇒ **PREDICTED `63 registered, 63 expected`**. ⛔ The asymmetric case (**63 expected / 62 registered**) remains a **STOP**, ⛔ never a warning.
- ⚠️ **SUBSTRING TRAP:** 🔬 **three** `e7bf477:main.py` sites emit `"ENABLED and started"` (`:3517` sr_detector · `:3537` sr_shadow · `:3569` market_regime); **sr_detector is ENABLED on the twin, so its line is already in the baseline** ⇒ ⛔ a substring count reads **1 today / 2 tomorrow** and would flag a **FALSE multiplicity anomaly**. ⭐ Ruleset **R1.5** now requires matching the **FULL `msg`**.

### §4 — adopted
**Raw logs remain the evidence of record**; normalization is comparison-only and every normalized event **must resolve to an auditable raw line** (the per-event table has a **Raw line ref** column) · **a PER-EVENT Gate 7/8 record** — ⛔ prose is not auditable · **"absent" means absent from the AUTHORITATIVE sink** · **composition counts never normalized** · **multiplicity never normalized away — duplicates are the signal** · **exact source references preserved** (`e7bf477` line numbers, ⛔ not verbal conclusions).

### Artifact set now frozen (all verified at Gate 2 and again at Gate 7/8)
**CURRENT:** prediction **v3** `419289c2c7805b84772b2995e8e06717` · ruleset **v2** `64c29e4e859c958a4eb5cbc8ea342dc7` · **normalizer** `e00e13267308267156e2413dec6c2fe5`.
**KEPT, SUPERSEDED:** prediction v2 `fab48fad…` · v1 `b5f7019c…` · ruleset v1 `f56fe84f…`.
**RAW CALIBRATION EVIDENCE:** `CALIBRATION_bootwindow_2026-09-15.jsonl` `f5809812…` · `…2026-09-16.jsonl` `ee034ee1…`.

## 16-Sep-2026 (Wed) ~11:20 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT15-16SEP2026` — ⛔ **SINK AUTHORITY BY ORIGIN DISSOLVES THE LEVEL-FLIP ARTEFACT CLASS** · ⛔ "3" IS NOT A BUDGET · OBSERVABILITY = SOURCE + LOGGER + LEVEL + SINK ROUTING

**Card:** "DEPLOYMENT CARD AMENDMENT 15" (16-Sep). ⭐ **No commands in the card.** ⛔ Nothing written on the VM; `e7bf477` unamended and unpushed; production untouched.

### §1 — my framing was overstated, and the number must not travel
- ⛔ **"False-positive rate" is WITHDRAWN.** One no-change pair is an **observed residual sample** — ⛔ there is no denominator and no distribution over repeated no-deployment boots.
- ⛔🔴 **AND "3" MUST NOT TRAVEL.** ⭐ My phrasing scoped it to the families correctly, but **a number in the same sentence reads as a BUDGET to whoever picks this up cold.**
- ⭐ **RECOGNITION IS BY FAMILY IDENTITY, NEVER BY COUNT: ten instances of `check_ntp_sync` is ORDINARY; ONE instance of a third family is NOT.**
- ✅ **Enforced in code, ⛔ not by instruction:** the normalizer reports **by family** and exits **rc 1 on ANY unrecognised family**, whatever the known counts. 🔬 Non-vacuous: known-only (x2 + x1) ⇒ rc 0; one injected new family ⇒ rc 1.

### §2 — 🔴 the consequence nobody had drawn, and the rule that dissolves it
- **Followed through:** the journal takes stdout, stdout is **WARNING+** ⇒ `check_ntp_sync` lands in the app log on both days but in the **journal only on the day it FAILS**. ⇒ ⛔ **journal-to-journal it would appear from nowhere on 16-Sep and vanish again if NTP recovers on 17-Sep. ⭐ The event never moved — its VISIBILITY did.**
- ⚠️ **Any message family whose level varies with OUTCOME generates phantom UNPREDICTED events in a journal-based comparison** — and one such family was found on the **only two days examined**.
- ✅ **THE RULE, now R0 of the ruleset — split sinks by ORIGIN, not by level:** **application-emitted ⇒ the APPLICATION LOG is authoritative ALWAYS** (it carries INFO+, so a level flip never changes what it holds; the journal's copy is a **stdout duplicate** and is ⛔ **never** used for comparison); **systemd/unit lifecycle ⇒ the JOURNAL is authoritative** (the app log cannot carry them at all).
- ⇒ ⭐ **No event's authoritative sink ever depends on its level, and the entire class of level-flip artefacts DISAPPEARS rather than being adjudicated case by case tomorrow.**
- ⛔ **Tightens Amendment 14 §2:** the **E-4 must-absent rows are checked in the APPLICATION LOG** — ⛔ not the journal merely because ERROR/CRITICAL reach it. ✅ They remain non-vacuous: the app log carries **INFO+**, so it holds all five regardless of level.
- ✅ **Mechanically enforced:** the normalizer **REFUSES (rc 2)** non-JSON input ⇒ it **cannot** be pointed at the journal. 🔬 Verified both ways.

### §3 — the substring trap, and why it was nearly missed
⭐ **Recorded, because the reason generalises: the prediction named the event by the text A HUMAN WOULD GREP FOR; the comparison must match WHAT THE CODE EMITS — a different thing.** Requiring the **full `msg`** is general, ⛔ not a patch for one string: `worker started` and every other predicted row get the same protection without enumeration.

### §4 — the composition row is now the strongest
🔬 **62 / 62 measured → 63 / 63 predicted** — ⭐ **two specific integers that either appear or do not.** ⛔ A prediction of **exact values is falsifiable in a way a delta is not.** The **measured baseline pair is carried into the Gate 7/8 record beside the observed pair**. **63 expected / 62 registered ⇒ ⛔ STOP** (the manager did not register); **62/63 or anything else ⇒ anomaly**.

### ⭐🔝 §5 — THE GENERAL RULE THIS WORK PRODUCED, worth keeping past this deployment
> **OBSERVABILITY IS `SOURCE + LOGGER + LEVEL + SINK ROUTING` — ⛔ NOT "the event exists in the code."**

⭐ **Both failures came from that one gap:** the **E-1 near-miss** (three INFO rows hunted in a WARNING+ journal ⇒ would have read as *"the manager did not come up"* and stopped a correct deploy) and the **E-4 vacuity problem** (must-absent rows checked against a sink that cannot carry them ⇒ green **by construction**). Recorded in `MEMORY_RULES.md`.

### §5 adopted
Raw logs remain the evidence of record, every normalized event traceable to a raw line · ⛔ **no numeric noise allowance** · the residuals stay **unnormalised as known variance**, ⛔ never normalised away to make tomorrow green · dates normalised **only where the code makes the date a session parameter** · composition counts never normalised · multiplicity never collapsed · source-proven order only · boot and EOD windows separate · ⛔ **no fix-forward inside Gate 7/8 — classify, preserve, then adjudicate** · the per-event record carries **event identity · logger · level · AUTHORITATIVE SINK · expected and observed multiplicity · order rule · result · raw-evidence reference**.

## 16-Sep-2026 (Wed) ~11:40 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT16-16SEP2026` — 🔴 **THE NORMALIZER'S rc INVERTS TOMORROW, AND IT IS BLIND TO ABSENCE** · CLASSIFIER ANCHORED · ANY UNPARSEABLE LINE IS A FINDING

**Card:** "DEPLOYMENT CARD AMENDMENT 16" (16-Sep) — three findings in **the one piece nothing had reviewed independently**. ⭐ **No commands in the card.** ⛔ Nothing written on the VM; `e7bf477` unamended and unpushed; production untouched.

### §1 — 🔴 the exit code inverts. **Confirmed by simulation, ⛔ not accepted on argument.**
🔬 Both 17-Sep outcomes were simulated against the **real 16-Sep boot window**:

| Simulated outcome | Normalizer | rc |
|---|---|---|
| ✅ **CORRECT deployment** (sr_shadow up, composition 63/63) | `UNRECOGNISED FAMILIES: 4` | **rc 1** |
| ⛔ **FAILED deployment** (manager never started) | `UNRECOGNISED FAMILIES: 0` | **rc 0** |

- ⇒ ⛔🔴 **rc 1 IS THE EXPECTED OUTCOME AND rc 0 IS THE ALARMING ONE** — the reverse of what the no-change calibration established and of what any operator or future session will assume. **A correct deployment reads as failure; a failed one reads as clean.**
- ⛔🔴 **AND THE DEEPER PROPERTY: the normalizer CANNOT DETECT A MISSING EXPECTED EVENT AT ALL.** It reports **differences**; an event absent from **both** sides produces **no difference**. ⭐ **Absence is precisely the E-1 failure mode the prediction exists to catch — and the tool is STRUCTURALLY BLIND to it.** 🔬 The failed-deployment simulation returned **0 residuals**.
- ✅ **Closed by option (b) — leave the tool alone and REMOVE THE PLACE TO RECORD ITS VERDICT.** ⛔ The per-event Gate 7/8 record has **NO FIELD for normalizer pass/fail**; it has a **RESIDUAL LIST** row and an **UNPARSEABLE LINES** row. ⭐ *The enforcement is that there is nowhere to write the wrong answer down.* ⛔ **Option (a) — teaching it the predicted events — was NOT taken:** it would re-architect and re-calibrate a tested tool hours before the window and change what the recorded calibration means.
- ✅ **Stated in ONE LINE at the TOP of the Gate 7/8 procedure**, because *under stress an exit code is read as a verdict — exactly when this would bite*. The tool also **prints the warning itself, before and after its output**.

### §2 — the classifier was doing the very thing R1.5 forbids
- `family_of()` used **`if key in msg`** — **fragment matching**, the trap the `"ENABLED and started"` finding proved. ⭐ **And here the asymmetry is worse:** for **event identity** a bad match gives a **FALSE ANOMALY, which is LOUD**; for **family recognition** it gives a **FALSE GREEN, which is SILENT.** ⛔ **The looser rule sat on the side where the damage is quieter.**
- ✅ **Anchored:** `logger` must **match** AND `msg` must **START WITH** the key. 🔬 Non-vacuous: a new `ERROR` from `main` reading *"startup_checks: check_ntp_sync wrapper crashed"* is now **UNRECOGNISED (rc 1)** — the previous code **silently absorbed it** into a known-variance family.

### §3 — a partially corrupt file could still exit 0
- The ≥50% guard caught *"you pointed this at the journal"*, but below it bad lines were **counted, printed, and then ignored by the exit logic**. ⭐ **Five events silently dropped from a comparison whose entire purpose is to notice missing events** — under a line an operator skims past.
- ✅ **ANY unparseable line now forces a non-zero result and a FINDING row.** 🔬 Verified: **2 bad lines in 84 ⇒ rc 1** (previously rc 0). The ≥50% ⇒ **rc 2 REFUSED** rule stays for the journal-misuse case. ⭐ The app log is **machine-written JSON** — an unparseable line **is itself an anomaly to adjudicate**, ⛔ not a rounding error.

### Artifacts now frozen
**CURRENT:** prediction **v5** `a5a72f6f8e8be241a5d1acedba853bab` (13,370 B) · ruleset **v4** `0fab34f53387c54a8d536292e77d22b5` (6,067 B) · normalizer **v3** `0cbcf225048e079c4ac83f06e044745a` (8,797 B).
**KEPT, SUPERSEDED:** predictions v4–v1 · rulesets v3–v1 · normalizers v2–v1. **RAW EVIDENCE:** both calibration extracts.
✅ **Re-calibrated after the changes:** the 15-Sep vs 16-Sep comparison still recognises **both** known families and returns **rc 0**, so the recorded calibration result still means what it said.

## 16-Sep-2026 (Wed) ~11:55 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT17-16SEP2026` — ✅ **BOTH WINDOW DELIMITERS ARE SEMANTIC** · 🔴 **BUT A BOOT-WINDOW-ONLY E-4 CHECK WOULD BE VACUOUS BY WINDOW** · PERMANENT WORDINGS · EVIDENCE BOUNDARY

**Card:** "DEPLOYMENT CARD AMENDMENT 17" (16-Sep) — the extraction step in front of everything already hardened. ⭐ **No commands in the card.** ⛔ Nothing written on the VM; `e7bf477` unamended and unpushed; production untouched.

### §1 — the window, stated for both sinks
- ✅ **BOTH DELIMITERS ARE SEMANTIC MARKERS**, ⛔ neither a line count nor a time bound: **START** = `Trading System v… starting`, **END** = `effect_telemetry: composition OK (…)` / `composition assertion FAILED`. ⭐ **The window grows with the boot**, so the extra sr_shadow lines cannot push anything out — ⛔ the phantom-missing-event failure mode does **not** apply.
- ✅ **The end marker sits after ALL manager construction:** 🔬 `assert_composition` at **`main.py:4277`** vs the sr_shadow block at **`main.py:3536–3539`**.
- ✅ **Marker uniqueness verified whole-day, both days** (read-only): `starting=1 · composition OK=1 · FAILED=0` ⇒ unambiguous, **no mid-day restart**. ⚠️ **`NRestarts` ≠ 0 or a second `starting` line ⇒ re-examine the window before comparing.**
- ✅ **Identical delimiters for baseline and tomorrow, now recorded in the manifest beside the artifact hashes.**

### 🔴 THE FINDING — the question surfaced a third A7 dimension
- 🔬 `start()` spawns a **background daemon thread** (`runner.py:149`); **`sr_shadow: drain error=` is emitted from inside that thread's loop** (`runner.py:166`) ⇒ ⛔ **it can fire at any point in the session, long AFTER the end marker.** The same is true of **E4.10 (any new CRITICAL)** and the **E5.12 runtime** events; **E4.9** fires at shutdown.
- ⇒ ⛔🔴 **Checking those rows over the BOOT WINDOW would pass BY CONSTRUCTION** — ⭐ **a must-absent row adjudicated over a window that cannot contain the event is the A7 defect in a THIRD dimension: sink → level → WINDOW.**
- ✅ **Closed by assigning a window PER EVENT CLASS:** boot window for **E1.1/E1.2/E2.3/E4.6/E4.7/E5.11**; the **WHOLE-DAY application log** for **E4.8 / E4.10 / E5.12**; the **EOD window** for **E4.9 / E3.5**; the **journal, whole day** for systemd lifecycle. ⚠️ The journal's `--since today` is time-bounded, acceptable **only** as a **whole-day** bound for **lifecycle** events — ⛔ never as a positional boot delimiter.

### §2 — the pre-write identity check, at the actual first-write boundary
✅ Added as **Gate 4-PRE**, immediately before 4a: `md5sum` the three current artifacts and confirm **v6 / v4 / v3**. ⛔ **If the manifest and the files disagree, STOP — never copy using one version and compare using another.** ⛔ Superseded versions and the original calibration extracts stay **KEPT**, and ⛔ **the first calibration is never overwritten by the post-fix run.**

### §3 — the six permanent wordings, with the rc's real meaning
Recorded in v6: **NORMALIZER** (residual extractor + input-quality checker only) · **EXPECTED EVENTS** (each adjudicated independently — ⭐ **including when the normalizer reports no residual**) · **FAMILY** (configured logger **AND** configured prefix) · **CORRUPTION** (any unparseable line is a finding; ≥50% a refusal) · **EVIDENCE** (every finding resolves to a raw line) · **FREEZE** (all three close at the first VM write).
⭐ **And the rc keeps a real meaning as a TOOL-HEALTH signal** — **0** no residual and no input problem · **1** residual or malformed finding · **2** input misuse — ⛔ **none of which is "the deployment succeeded."** ⭐ **Writing that distinction down is what stops a future maintainer deleting the per-event table and restoring the original defect without noticing.**

### §4 — the evidence boundary, and the raw outputs
⚠️ The fixes are **verified according to this session's report** — ⛔ **not an independent code audit.** ✅ **`NORMALIZER_TEST_EVIDENCE_2026-09-16T1150IST.txt`** (19,657 B, md5 `3c340707ccaf2b64339332faf13c1460`) holds **all six runs with full output and exit codes**: T1 post-fix calibration **rc 0** · T2 simulated CORRECT deploy **rc 1** · T3 simulated FAILED deploy **rc 0** · T4 anchored-family **rc 1** · T5 corrupt-lines **rc 1** · T6 misuse guard **rc 2**. The four test inputs are kept beside it, and ✅ **the original calibration extracts are UNCHANGED (`f5809812…`, `ee034ee1…`)** — ⭐ **the pair is what shows the correction did not change what the calibration means.**

## 16-Sep-2026 (Wed) ~12:10 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT18-16SEP2026` — 🔴 **THE IDENTITY GATE WOULD HAVE CERTIFIED THE WRONG SET AND REPORTED GREEN** · PREDICTION IS DATA, MANIFEST IS PROCEDURE · MISSING END MARKER

**Card:** "DEPLOYMENT CARD AMENDMENT 18" (16-Sep). ⭐ **No commands in the card.** ⛔ No VM write, no cron, no commit, no push as part of this correction. `e7bf477` unamended and unpushed; production untouched.

### §1 — 🔴 confirmed, and it sat in the step whose whole purpose was to prevent it
- 🔬 **v6 line 227, step 1 of its own "How Gate 7/8 runs":** *"Verify filename + size + md5 of: both baselines · **v4** · **ruleset v3** · **the frozen normalizer v2**."* — **every version named was superseded.**
- ⚠️🔴 **AND EVERY SUPERSEDED FILE IS STILL ON DISK, DELIBERATELY KEPT.** 🔬 Verified: `b330ca13…` · `5c212e3f…` · `b011440e…` **all match**. ⇒ ⭐ **An operator following step 1 verbatim would have verified the WRONG THREE FILES, got a clean match, and proceeded — the gate would have CERTIFIED the mismatch and reported GREEN.**
- ⭐ **The same shape as every other finding in this chain:** `STOP_NOT_DEFENDED` that could never be red · E-4 rows checked against a sink that could not carry them · boot-window checks for background-thread events · **and now an identity gate passing against the wrong identity.** ⭐ All four found by asking **whether a green could ever have been red.**
- ✅ Corrected **before the first VM write** — v7's own freeze rule closes the artifact at that boundary, so the window was open and this is precisely what it is open for.

### §2 — ⭐ the structural cause, fixed structurally
- **The prediction was carrying PROCEDURE.** The manifest and the prediction both described *"how Gate 7/8 runs"*; **the manifest was updated six times today and the prediction's copy was not.** ⭐ **Two documents, same procedure, both reading as authoritative to whoever opens only one.**
- ✅ **Roles separated:** **THE PREDICTION IS DATA** (events, loggers, levels, sinks, multiplicities, orders, windows). **THE MANIFEST IS PROCEDURE** (identity verification, how to compare, what to record, when to stop). The prediction's procedure section is now **one pointer** to `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` → **Gate 4-PRE and Gate 7/8**.
- ⛔ **The pointer is BY SECTION NAME, never by version** — *"v7 refers to the current set"* would be the same failure with one more indirection. ⭐ **One authoritative location, named once.**
- ✅ **The manifest was itself checked for the same defect: all 15 artifact references are the CURRENT set, 0 stale.** The divergence existed only where the procedure was duplicated.

### §3 — the missing-end-marker case
⚠️ The awk terminator is `composition OK` **OR** `composition assertion FAILED`. **If the boot dies before composition (`main.py:4277`), neither fires**, the flag stays set, and awk **prints to end of file** ⇒ the boot window **silently becomes the whole day**. ⭐ Loud, but **it would read as a normalizer or window fault rather than what it is — THE BOOT NEVER REACHED COMPOSITION.** ✅ **Marker counts are now checked BEFORE the comparison** (`composition OK` + `FAILED` ≥ 1); **zero ⇒ STOP and report "boot did not reach composition"**, ⛔ never run the comparison and interpret the residuals.

### §4 — the journal's time bound keeps its reason attached
✅ Recorded in place: `--since today` is tolerable **ONLY** as a **whole-day bound on SYSTEMD events**, and ⛔ **must never become a positional or time-bounded delimiter for an application-event window.** ⭐ **The distinction is easy to lose later once only the command survives.**

### Scope held (Amendment 18 §5)
✅ Corrected the stale identity line · decided prediction-vs-procedure and applied it · added the missing-end-marker case · re-froze with new size and md5 · recorded why v7 exists.
⛔ **NOT done:** no re-working of prediction content · no renumbering or restructuring of the E-classes · no change to the window assignments · **no superseded artifact or calibration extract overwritten** · **the VM untouched.** 🔬 Verified: E-class headings and the window-assignment section are **byte-identical** between v6 and v7.

**CURRENT SET:** prediction **v7** `41e2cdec41411651ea29bdcac7c87d2a` (43,540 B) · ruleset **v4** `0fab34f5…` · normalizer **v3** `0cbcf225…`.

## 16-Sep-2026 (Wed) ~12:30 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT19-16SEP2026` — 🔴 **THE MARKER GUARD WAS `>= 1` AND PASSED THE TWO-BOOT CASE** · **THE EOD WINDOW HAD NEVER BEEN SPECIFIED** · WINDOW_INVALID PRECEDES EVERY RESIDUAL

**Card:** "DEPLOYMENT CARD AMENDMENT 19" (16-Sep). ⭐ **No commands in the card.** ⛔ No VM write; the only VM contact was a **read-only** fetch of the 15-Sep EOD window and marker counts. `e7bf477` unamended and unpushed; production untouched.

### §1 — 🔴 `>= 1` closed the zero case and **passed the two-marker case**
| markers | meaning | under `>= 1` | now |
|---|---|---|---|
| **0** | window never reached its terminator | STOP ✅ | STOP |
| **1** | one unambiguous window | valid ✅ | valid |
| **2+** | two boots / shutdowns in one day | ⚠️ **PASSED** | ⛔ **STOP** |

- ⚠️ **Two markers is fatal whatever caused it:** **E1.1 and E1.2 are each predicted EXACTLY ONCE**; across two boots the whole-day log holds **two of each**, and **`drain error` + any new CRITICAL — both WHOLE-DAY rows — would span TWO PROCESS LIFETIMES attributed to ONE deployment.** ⭐ **And the awk exits at the FIRST terminator**, so the boot window would silently be **boot #1** while the whole-day checks covered **both** — **two windows with two different meanings of "today's boot".**
- ✅ **The guard is now `== 1` on BOTH markers, on BOTH windows, plus end-after-start** — and it is **mechanically enforced by a frozen validator**, ⛔ not prose. ⭐ Hand-verified uniqueness and Gate 2's `NRestarts` remain **an observation and a separate gate** — ⛔ **the guard now matches what was already verified.**
- 🔬 **Non-vacuous, 7 cases, raw output kept:** valid boot **rc 0** · start-no-end **rc 3** · **TWO end markers rc 3** *(the case `>= 1` passed)* · two starts **rc 3** · end-before-start **rc 3** · **real 15-Sep EOD rc 0** · EOD spec on a boot file **rc 3**.

### §2 — 🔴 the EOD window had never been specified
- The window table assigned **E3.5** and **E4.9** to an EOD window whose **delimiters did not exist anywhere**. ⭐ **Every hazard established for the boot window applied to it unchanged — and none had been checked.**
- ✅ **Now specified to the same standard:** **START `Shutdown initiated`** (`main.py:1631`) → **END `Shutdown complete`** (`main.py:1839`), **both semantic**, ⛔ **not a clock slice**. ✅ **The end marker sits AFTER `sr_shadow.stop()` (`main.py:1705`)** ⇒ both events land inside. ✅ Same missing-end-marker case, same `== 1` guard.
- 🔬 **Validated against real data**, ⛔ not asserted: the 15-Sep EOD extract returns **WINDOW_OK**; the same spec on a boot file returns **WINDOW_INVALID**.
- ⚠️ **16-Sep read `init=0 complete=0` at midday** — ⭐ **correct**: the session had not yet self-exited. **The EOD baseline exists only after 17:35**, which is exactly why Gate 2 captures **after** the self-exit.
- ⭐🔝 **Same pattern as Amendment 18 §1:** a procedure in two places with one updated; a window rule covering one window and not the other. ⛔ **Both are the gap between "the rule exists" and "the rule covers everything it names."**

### §3 — adopted, and evidenced
- ✅ **Check B — the prediction carries no independently maintained procedure**, proven mechanically: pointer to the manifest **section by name = 1** · independent identity step = **0** · numbered procedure steps = **0** · ⭐ **artifact filenames named = 0**, so **the prediction cannot go stale** (the validator is referenced by **role**; the manifest holds its filename, size and md5).
- ✅ **Check C — the missing-end-marker condition is mechanically enforced as `WINDOW_INVALID` / STOP**, with **Case E (two end markers) added**, which ⚠️ **would have failed under `>= 1`** and is the proof of §1.
- ⛔🔴 **`WINDOW_INVALID` is the FIRST finding, never `NORMALIZER_RESIDUAL`.** ⭐ A huge residual list from a malformed window must not be read as the primary failure; **the validator runs first as a precondition and on failure the comparison is not run at all.**

**CURRENT SET:** prediction **v8** `41e2cdec41411651ea29bdcac7c87d2a` (43,540 B) · ruleset **v4** `0fab34f53387c54a8d536292e77d22b5` · normalizer **v3** `0cbcf225048e079c4ac83f06e044745a` · **window validator** `8c354fd7322d104b15e6bc9246b864c9` (4,218 B).

## 16-Sep-2026 (Wed) ~13:00 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT20-16SEP2026` — 🔴 **THE EVALUATOR HAD NO PREDICTED OBSERVABLE** · IT CANNOT REACH THE APPLICATION LOG · §24/§25 CHECKED CLEAN

**Card:** "DEPLOYMENT CARD AMENDMENT 20" (16-Sep). ⭐ **No commands in the card.** ⛔ No VM contact of any kind for this pass — everything below is from code at `e7bf477`. `e7bf477` unamended and unpushed; production untouched.

### §1 — the last named-but-uncovered path
- **The deployment installs TWO things** and only one was predicted: the 17-file service change, and **a cron job** that Gate 6 installs at 16:05 Mon-Fri. ⭐ **Its first run is 17-Sep 16:05, between the boot and EOD comparisons, and nothing predicted anything about it.**
- ✅ **SINK ESTABLISHED FROM CODE:** the evaluator calls `get_logger("sr_shadow_evaluate")` (`:180`) **but never calls `setup_logging`** (**0** occurrences), and **no module in its import chain attaches a handler at import time** — `core/logger.py`'s two `addHandler`/`basicConfig` occurrences are **inside** `setup_logging`, which this process never runs.
- ⇒ ⛔🔴 **In that separate cron process root has NO handlers** ⇒ `logging.lastResort` ⇒ **WARNING+ to stderr, INFO/DEBUG discarded** ⇒ **THE EVALUATOR WRITES NOTHING TO `logs/system_<DATE>.log`.**
- ✅🔴 **CONSEQUENCE THAT MATTERED: E4.10 IS UNAFFECTED.** A failing evaluator **cannot** inject a CRITICAL into the application log and so **cannot be misclassified as a service-deployment violation**. It emits **no `log.critical`** at all; its only two log calls are `log.error`.
- ⭐ **This is exactly the outcome §1 called a legitimate answer — the evaluator writes nowhere the comparison can see, and its only evidence is the CRON LOG and the SHADOW DB ROWS. It is now recorded rather than assumed.**
- ✅ **Class E-6 added while the prediction is still open:** MUST APPEAR — the JSON summary line (the evidence the cron fired at all), a `record_run` row, per-row `write_evaluation`. MUST BE ABSENT — the two `log.error` texts, any CRITICAL, any traceback. ✅ **All must-absent rows are ERROR or above and therefore observable in the cron log** — ⛔ not vacuous by sink.
- ⚠️ **GAP NAMED, ⛔ NOT CLOSED:** §1 asked for a completion marker **with its exit status**. 🔬 The cron line redirects **stdout and stderr only**; **rc is never written to the log**. Codes: **0** clean · **2** rows left unevaluated · **3** refused (session not over, before 15:30 IST). ⭐ rc is **derivable from the summary's own fields**, ⛔ **not directly recorded**. **Whether to record it is a decision, and it is not made here.**

### §2 — both pre-write checks, run
- ✅ **§25 — the validator keys on marker TEXT.** 🔬 `msg.startswith(...)` for both start and end; the `main.py` line numbers appear **only** in the printed `prov` string, with **0** uses in any comparison. ⭐ **A line number moves on the next edit; the marker text does not.** Line numbers stay as provenance.
- ✅ **§24 — three-layer semantic consistency: NO DIVERGENCE.** Manifest · frozen artifacts · validator, all six propositions present in all three layers.
- ⚠️ **One apparent divergence was my own false positive** — *end after start* appeared absent from the manifest under a **case-sensitive** pattern; re-checked case-insensitively the manifest states it verbatim. ⭐ **Recorded as a self-corrected check rather than a finding** — the risk §24 targets (procedure says X, implementation does Y) did **not** materialise on the third look.

### §3 — what the evidence does and does not establish, kept verbatim
seven validator cases pass → **the validator recognises those cases** · 28 RUNNABLE, 0 placeholders → **structural readiness** · four identity hashes match → **identity** · **none of the above → that tomorrow's deployment will pass.**
⭐ **Case E — two end markers, rc 3 — is the most valuable of the seven, because it is the case `>= 1` accepted this morning. A test that fails against the PREVIOUS implementation is worth more than six that pass against both.**

### The principle, now stated by both reviewers
⭐🔝 **A RULE IS NOT CLOSED BECAUSE IT EXISTS. It is closed when every sink, window, artifact and execution path it names is covered and mechanically tested.** ⭐ The evaluator was the last named-but-uncovered path; it is now covered.

**CURRENT SET:** prediction **v9** `41e2cdec41411651ea29bdcac7c87d2a` (43,540 B) · ruleset **v4** `0fab34f5…` · normalizer **v3** `0cbcf225…` · window validator `8c354fd7…`.

## 16-Sep-2026 (Wed) ~13:15 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT21-16SEP2026` — ✅ **E-6 CLOSED: THE rc IS REDUNDANT AND THE EVALUATOR IS FROZEN** · EVERY EXIT PATH EMITS THE SUMMARY · THE PROCESS SEPARATION IS INTENTIONAL

**Card:** "DEPLOYMENT CARD AMENDMENT 21" (16-Sep). ⭐ **No commands in the card.** ⛔ No VM contact for this pass — a **code read only**, at `e7bf477`. `e7bf477` unamended and unpushed; production untouched.

### §1 — the decision, and the verification it required
- ✅ **DECISION TAKEN BY THE CARD: the process exit status is NOT captured and is NOT to be added.**
- **Reason 1 — redundancy.** The cron log already separates **no content ⇒ never fired** · **content + traceback, no summary ⇒ crashed before completing** · **summary present ⇒ completed**. ⭐ *"The question worth answering is not what was the rc, but did it run and did it finish — and the log content answers both."*
- **Reason 2 — ⚠️ the evaluator is INSIDE THE FROZEN SET.** Committed in `e7bf477`, **one of the 17 copy files**, frozen md5 **`edebd2d8…`** in the file table. ⛔ **Changing it would invalidate the commit, the file table, the Gate 4 copy manifest, the four-artifact identity check and the 27-vs-17 accounting** — to record a value already derivable. ⭐ **The wrong trade, and exactly the late change this chain has refused all day.**
- ✅🔴 **THE VERIFICATION — DONE AS A CODE READ, ⛔ NOT A CHANGE.** 🔬 `run()` has **exactly two returns**, `:88` (refused) and `:170`, **both carrying a summary dict**. `main()` has **exactly one return** (`:187`), preceded **unconditionally** by the print at **`:186`**. The only `sys.exit` is `:191`, which runs **after** `main()` returns. ⇒ ✅ **EVERY non-crash exit path emits the summary line — INCLUDING THE REFUSED PATH.**
- ⇒ ⛔ **THE FALSE-RED §1 FEARED DOES NOT EXIST.** A refused run is **positively identified** by the `refused` key; it is **not** indistinguishable from "cron never fired".
- ✅ **E-6 CONTRACT, STATED:** summary line = completion marker · `refused` ⇒ rc 3, `rows_left_unevaluated > 0` ⇒ rc 2, else rc 0 · rc not captured, **and the record says why** · second discriminator: `record_run` (`:169`) guarded by `if not dry_run:` (`:168`) and **unreachable on the refused path** · `"dry_run": true` (`:160`) is self-declaring · ✅ **every path leaves evidence** — the only way to omit the summary is an uncaught exception before `:186`, which leaves a **traceback** in the same log. ⛔ **No silent path exists.**

### §2 — the separation is a property, not a limitation
⛔ **DO NOT SOLVE E-6 BY CALLING `setup_logging()` IN THE EVALUATOR.** ⭐ **That separation is the reason E4.10 cannot be contaminated by a failing evaluator.** ⚠️ Attaching the application handlers there would create **precisely the contamination Amendment 20 went looking for, in the name of closing the ticket Amendment 20 opened.** ✅ **Recorded as intentional: evaluator → cron log + shadow DB; service → application log + journal. Two processes, two evidence chains, NO OVERLAP.**

### §3 — the self-corrected false positive, and why it is named
⭐ The *"end after start missing from the manifest"* result was **my own case-sensitive pattern artefact**, re-checked and recorded as a **self-corrected check rather than a finding**. ⭐🔝 **Worth naming because the pressure runs the other way: twenty amendments of real defects makes the twenty-first look like one too, and a reviewer who has been right repeatedly is exactly the one most likely to report a pattern artefact as a finding. Recording the correction rather than quietly deleting it is what keeps the record honest.**

### §4 — the distinction that survives tonight
seven validator cases passing → **the validator recognises those cases** · four hashes matching → **identity** · 28 runnable blocks with no placeholders → **structural readiness** · ⛔ **none of them → that tomorrow's deployment will pass.**

⭐ **17:30 is a gate, not a deadline.**

**CURRENT SET:** prediction **v10** `41e2cdec41411651ea29bdcac7c87d2a` (43,540 B) · ruleset **v4** `0fab34f5…` · normalizer **v3** `0cbcf225…` · window validator `8c354fd7…`.

## 16-Sep-2026 (Wed) ~13:40 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT23-16SEP2026` — ⛔ **IDENTITY BY ROLE, NOT BY VERSION** · A TRACEBACK GETS NO DATE FROM ITS POSITION · 🔴 A RESIDUAL IN THE IDENTITY CHECK ITSELF

**Card:** "DEPLOYMENT CARD AMENDMENT 23" (16-Sep). ⭐ **No commands, and deliberately no version numbers.** ⛔ No VM contact for this pass. The build commit is unamended and unpushed; production untouched.

### §1 — one mechanism, three occurrences, and the fix already existed on the other side
- 🔬 **The mechanism:** a card names the current version → the card is applied → **applying it produces a new version** → **the card that caused the increment now names the superseded one.** ⭐ **The card is stale by the act of being used**, so **there is no version number a card can carry that survives its own application.**
- ✅ **ADOPTED:** cards, reports and reviews name artifacts **by ROLE ONLY** — the prediction, the ruleset, the normalizer, the window validator. **Identity lives in this manifest and nowhere else.** ⭐ **"Current" = whatever the identity command returns when it is run.**
- ⭐ **Same lesson as Amendment 18 §2, third location:** a thing lived in two places and the copy went stale — here **while the cards warning about staleness were themselves the copy.**
- ✅ The prediction already had the right shape from the moment it stopped naming filenames, and **keeps it**.

### 🔴 A RESIDUAL IN THE IDENTITY CHECK ITSELF — found by applying §1 to this manifest
- 🔬 The identity command compares a **NAMED file** to a **STATED hash**. ⛔ **It cannot see a newer artifact it does not name.**
- ⚠️ **If a future pass produces a new prediction and forgets to update this manifest, the command names the superseded file — which is deliberately KEPT on disk and verifies CLEAN** ⇒ ⭐ **the gate certifies the superseded set and reports GREEN.**
- ⭐ **That is precisely the Amendment 18 §1 defect, surviving in the one place identity is allowed to live.** 🔬 Confirmed by search: **0** checks assert *"no newer artifact exists"*.
- ⏸ **DECISION NAMED, ⛔ NOT MADE:** whether the identity step should also assert that no higher-versioned artifact exists. ⛔ That changes the gate's STOP conditions and is not authorised here. **Mitigation until then is procedural** — the pass that creates an artifact updates the manifest in the same action, which every pass today has done.

### §2 — the premise correction, and the rule it yields
- ✅ **Confirmed and already recorded:** the summary carries `target_date` and **no wall-clock timestamp** (**0** timestamp-like keys); `now_fn()` goes to the **shadow DB**, not the log. So the asymmetry is **not** "timestamped versus not" — it is **"attributable to a trading day" versus "attributable to nothing."**
- ✅ **NEW, now stated as a rule: A TRACEBACK GETS NO DATE FROM ITS POSITION.** ⭐ **Sitting between two summary lines is NOT evidence of belonging to either run.** A traceback appearing during the measurement period is **UNDATED** until something **outside the cron log** dates it. ⚠️ **Position in an append-only file is an ORDERING fact, ⛔ not an ATTRIBUTION fact** — the same class of error as inferring a cause from an absence.
- ✅ **Mitigation recorded:** the shadow DB `record_run` row **is** timestamped. **The database is the timestamped record; the cron log is not.**

## 16-Sep-2026 (Wed) ~13:45 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT24-16SEP2026` — THE IDENTITY RESIDUAL IS **DORMANT, NOT CLOSED** · ROLE-ONLY ≠ HASH-FREE · THE 29-vs-28 COUNT RESOLVED

**Card:** "DEPLOYMENT CARD AMENDMENT 24" (16-Sep). ⭐ **No commands; artifacts named by role only.** ⛔ No VM contact. ✅ **The four frozen artifacts are UNCHANGED by this pass and the prediction was deliberately NOT incremented** — §1's reasoning depends on no further artifacts being created, and §§1/2/4 are **procedure**, not prediction data.

### §4 — the label check, verified rather than assumed
✅🔴 **THE INVARIANT: ZERO RUNNABLE LABELS LACK A COMMAND BLOCK.** 🔬 **28 command-bearing labels, 0 orphans**, verified by testing whether a fence opens within two lines of each label. ✅ **No operator will look for a command that is not there.**
⚠️🔴 **⛔ A RAW `grep -c` OF THE LABEL STRING IS NOT THE CHECK — IT IS SELF-INVALIDATING.** 🔬 It also matches the labelling **RULE row** and **every prose mention**; ⭐ **recording the number changed it from 29 to 30 in the act of writing it down.** ⭐ **Same mechanism as Amendment 23 §1 — a document that records a number about itself is stale the moment it records it.** ⛔ Use the invariant, ⛔ never the bare total.

### §1 — the manifest identity residual: DORMANT, ⛔ not closed
- ⛔🔴 **CORRECTED BY AMENDMENT 25 §1.** The earlier claim — that the window is shut *structurally* by the freeze — **was wrong for the interval that counts.** ⚠️ **THE SET IS NOT FROZEN NOW**; the artifacts close at the **first VM write**, which has not happened, and 🔬 **the prediction moved twelve times today, most recently at 13:38.** ⭐ **NOW → FIRST WRITE: the residual is LIVE and the mitigation is PROCEDURAL** (every pass today has done it — **evidence, ⛔ not a guarantee**). ⭐ **AFTER THE FIRST WRITE: structurally dormant.** ⇒ the structural argument only ever covered the interval **where nothing changes anyway**.
- The procedural mitigation covers the only remaining case — a correction before 17:30: **the creating pass updates the manifest in the same action.**
- ⛔🔴 **NO "HIGHEST VERSION WINS" ASSERTION.** ⭐ **Version numbering is a naming convention, ⛔ not the identity contract.** Making version arithmetic part of deployment acceptance would create a **new class of failure: an artifact correctly named but rejected for its number.**
- ✅🔴🔝 **THE FREEZE-BROKEN PROTOCOL, ADOPTED (Amendment 25 §1)** — so the mitigation is **testable instead of remembered**: after the freeze, ⛔ **no creation, no replacement, no version increment, no identity-changing mutation**; and **if an authorised correction produces a new artifact, THE FREEZE IS BROKEN** — ⭐ **say so in those words**, update the manifest, **re-run the identity and digest gate**, and record that **the deployment set is NOT the previously frozen set**. ⛔🔴 **NEVER call that state "still frozen".**
- ⚠️🔴 **RECORDED AS DORMANT WITH THE DATE NOTICED (16-Sep-2026). It becomes LIVE again on the next deployment cycle**, when artifacts move and the freeze no longer protects it. ⭐ **A defect disposed of by circumstance rather than by fix is the kind that returns unannounced.**

### §2 — role-only does not mean hash-free
**CARD** names the ROLE · **MANIFEST** resolves the role to a concrete artifact · **HASH** verifies that artifact's integrity. ⭐ **Removing versions from cards removes STALE IDENTITY from procedural documents; it does ⛔ not remove integrity verification.** The first-write boundary still verifies **filename, size and digest** for every resolved artifact.

### §3 — position is ordering, not attribution (general form)
⭐ **Physical position in an append-only log is ORDERING evidence. It is ⛔ NOT ATTRIBUTION evidence.** A traceback between two summary lines is not proof it belongs to either run. **Attribution comes from an independently dated source** — for the evaluator, the shadow DB `record_run` row, which is timestamped while the cron log is not. ⭐ **The same class of error as inferring a cause from an absence.**

## 16-Sep-2026 (Wed) ~14:10 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT25-16SEP2026` — ⛔ **"SHUT BY THE FREEZE" WAS WRONG FOR THE PRE-WRITE INTERVAL** · THE FREEZE-BROKEN PROTOCOL ADOPTED

**Card:** "DEPLOYMENT CARD AMENDMENT 25" (16-Sep). ⭐ **No commands; artifacts by role only.** ⛔ No VM contact. ✅ **No prediction increment** — this is procedure, not prediction data, and §3 confirms that was the right call last pass too. The build commit is unamended and unpushed; production untouched.

### §1 — the correction, and it goes against the earlier record
- ⛔ **THE SET IS NOT FROZEN NOW.** The standing rule is that the prediction, ruleset and normalizer **close at the FIRST VM WRITE** — which has not happened. 🔬 **Verified: the prediction has moved TWELVE times today, most recently v11 → v12 at 13:38**, and the four artifacts carry mtimes 11:38, 11:38, 12:27 and 13:38.
- ⭐ **"Frozen" described an INTENTION, ⛔ not a STATE** — and the intention was already contradicted twelve times over by the time it was written down.
- **TWO INTERVALS:** **NOW → FIRST WRITE** — artifacts can still change, the residual is **LIVE**, and the mitigation is **PROCEDURAL**; every pass today has done it, which is ⭐ **EVIDENCE, ⛔ not a guarantee**. **AFTER THE FIRST WRITE** — artifacts closed, trigger cannot arise, **structurally dormant**.
- ⇒ ⛔ **The structural argument only ever applied to the second interval — the one where nothing changes anyway.** ⭐ **For the hours that actually matter it is procedure holding the line, exactly as the earlier wording claimed it was not.**
- 🏷️ **Classification UNCHANGED: REAL · DORMANT AFTER THE WRITE · ⛔ NOT CLOSED.** Only the reason for the pre-write interval is corrected.

### ✅ THE FREEZE-BROKEN PROTOCOL — adopted, because it makes the mitigation testable
- **After the artifact freeze:** ⛔ no creation · no replacement · no version increment · no identity-changing mutation.
- **If an authorised correction produces a new artifact: THE FREEZE IS BROKEN.** ⭐ **Say so in those words** · update the manifest · **re-run the identity and digest gate** · record that **the deployment set is NOT the previously frozen set**.
- ⛔🔴 **NEVER describe that state as "still frozen".**

### §2 — the invariant is the permanent form
✅ Already applied: **zero RUNNABLE labels lack a command block**, verified structurally by a fence opening within two lines of each label; ⛔ **a raw grep of the label string is not the check** — it matches the rule row and every prose mention.
⭐ **The generalisation kept: a document that records a number about itself is stale the moment it records it. Record the INVARIANT, ⛔ not the value.** ⚠️ **Two different substring traps in one day** — `"ENABLED and started"` and this one — **both found by checking rather than counting.**

### §3 — why not incrementing was right, and what it illustrates
✅ The prior pass created no artifact because its content was **procedure, not prediction data** — and **creating an artifact to record "no further artifacts will be created" would have contradicted the argument in the act of making it.**
⭐🔝 **And that is the cleanest illustration of §1: the only thing that kept the artifact set stable through that pass was A JUDGEMENT MADE IN THE MOMENT. ⛔ Not a freeze.**

---

## 16-Sep-2026 (Wed) ~14:17 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT26-16SEP2026` — 🔴 **THE RESUME PATH WAS TESTED AND IT HAD THREE HOLES** · THE FIRST VM WRITE IS NOW A DECLARED STATE · ⛔ THE HELD ITEM STAYS HELD

**Card:** DEPLOYMENT CARD AMENDMENT 26. **§1** test the cold-resume path now, because auto-compaction may end this session before 17:30. **§2** the held item needs Rama's own word, and **a stated identity that does not match the computed one is a STOP**. **§4** declare the first VM write as a state transition.

### §1 — the cold read was run, and it FAILED three of its own questions

⭐🔴 **THE TEST WAS NOT A REREAD OF WHAT I REMEMBERED — it was run against the standalone file alone, answering the four resume questions from its bytes.** ✅ **Q1/Q2 (which gates ran, what happened) PASSED** · ✅ **Q3 (what runs next) PASSED** · ⚠️ **Q4 (where are the artifacts) was PARTIAL.** 🔴 **Three defects were found, and every one of them would have misled a cold reader, ⛔ not merely inconvenienced them:**

- 🔴⛔ **THE RESUME RULE NAMED FOUR TIMERS THAT DO NOT EXIST** — `08:27 · 17:42 · 17-Sep 08:27 · 17:47`. 🔬 **Exactly ONE timer is armed: 17:30, armed 09:00.** ⭐ A cold reader would have believed a 17:42 timer was going to fire and would have **waited for it**. ✅ Corrected in place, with the correction left visible.
- 🔴⛔ **THERE WAS NO STATE DECLARATION FOR THE FIRST VM WRITE** — 🔬 **12 mentions of "first VM write", all of them RULES *about* it, none saying whether it had HAPPENED.** ⭐ **A rule is not a state.** A cold reader could not tell whether the VM had been written to. ✅ Closed by §4 below.
- 🔴⛔ **THE PRESERVED COPY CARRIED AMENDMENT 24 TWICE, AND THE TWO COPIES DISAGREED** — one held the **pre-correction** 29-count, the other the corrected **invariant**. ⭐ **This is the A7 class inside the resume artifact itself: a cold reader had a 50% chance of reading the superseded half and re-introducing a number I had already proven self-invalidating.** 🔎 **Cause found: the copy was being built by APPENDING the newest section each pass**, so a section amended twice landed twice. ✅ **Fixed at the cause — the copy is now rebuilt DETERMINISTICALLY** (header + live manifest section + the static VERBATIM run + every live section from Gate 1 onward), with an assertion that each amendment appears exactly once. 🔬 Verified: **no section lost, none gained** (set-diff against the old copy is empty both ways).

✅🔬 **RE-TESTED after the fix, with a CONTROL** — a string that is **not** in the file returns **0**, so the passing checks could have failed. **1,453 lines, md5 `482c8ce7…`.**

### §2 — the alarm, stated plainly

⛔🔴🔝 **THE 17:30 TIMER MAY NOT FIRE, AND I CANNOT PROVE IT WILL.** ⚠️ **Whether an in-session timer survives auto-compaction is NOT ESTABLISHED** — I have no evidence either way, and ⭐ **I am not going to report an untested mechanism as a control.** It also carries **stale text** (Amendment 11 §4). ⭐ **Two independent reasons not to lean on it.** ✅ **The 17:30 reminder has to live OUTSIDE this session.**

### §4 — the first VM write, declared as a STATE

⛔🔴 **AS AT 16-Sep 14:17 IST THE FIRST VM WRITE HAS NOT OCCURRED.** — **artifact set written: NONE** · **verification performed on the VM: NONE.** 🔬 The only VM contact all day is Gate 1's single **read-only** run at 08:26 plus read-only log fetches; **`0` bytes of stderr; nothing written.** ⭐ **Consequences a cold reader must draw:** Gate 4-PRE and the guarded writes have **NOT** been performed, and ⛔ **the artifact set is therefore NOT frozen** (Amendment 25's two-interval rule still governs).

✅ **The four artifacts re-verified at 14:17, byte-identical to record** — `41e2cdec…` (13:38) · `0fab34f5…` (11:38) · `0cbcf225…` (11:38) · `8c354fd7…` (12:27). ⭐ **THE FREEZE IS NOT BROKEN.**

### ⛔ The held item is still held

⛔ **`ENTRY-EXEC-DG5-DOCS-MATERIALISATION-1` remains HELD and is ⛔ NOT part of tonight's gate.** ⭐ It needs **Rama's own words naming the filename** — ⛔ **no console-generated continuation prompt is authorisation.** Two substantive blockers also stand: 🔴 **a stated hash that does not match the computed one** (`…127198551…` stated vs `…127190551…` computed — they differ at **one position only**, `8` vs `0`, which ⛔ **cannot** be produced by a content difference) — ⭐ **and a stated identity that does not match the computed one is a STOP, not a rounding error**; and 🔎 **Task A's source is not in `_inbox`** — only the *instruction* that commissioned the corrected propagation record is there, ⛔ not the record itself.

---

## 16-Sep-2026 (Wed) ~14:30 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT27-16SEP2026` — ✅ **THE RESUME PATH IS CONFIRMED BY A SECOND, INDEPENDENT READ** · 🔴 **THE STATE DECLARATION IS A HINT; GATE 3 IS THE PROOF** · THE COUNTING TRAP CAUGHT THE REVIEWER TOO

**Card:** DEPLOYMENT CARD AMENDMENT 27. No commands. Artifacts by role only.

### §1 — the cold read now has two independent witnesses

✅⭐ **The reviewer read the same standalone file from outside, with no session history — which is the check my own test could NOT be.** All four resume questions answered, plus the timer correction, the first-write state, **Amendment 22's content surviving despite its heading never being written**, and **each amendment section appearing exactly once by heading**. ⭐ **A self-test plus an independent read is a different quality of evidence than a self-test alone.**

### §2 — 🔴 the state declaration is DATED EVIDENCE, not a current state — ADOPTED

⚠️🔴 **The reviewer is right, and this was the last "trust a recorded value" left in the procedure.** `AS AT 16-Sep 14:10 … HAS NOT OCCURRED` is **three hours old** by 17:30: it establishes what was true at 14:10, ⛔ **it cannot establish what is true when a cold reader reads it.**

✅⭐ **And it does not need to — the procedure already re-proves it, which I verified in the manifest rather than accepting from the card:** 🔬 **Gate 3 carries the absence check verbatim** — `sr_shadow/` and `scripts/sr_shadow_evaluate.py` must **both** read `ABSENT`, and the `sr_shadow_evaluate` crontab count must be **`0`**. ✅ **Recorded in the manifest in the three-line form:** the declaration is a **HINT** that orients a cold reader · **GATE 3'S ABSENCE CHECK IS THE PROOF** · ⛔🔴 **if the two ever disagree, THE VM WINS AND THE DEPLOYMENT STOPS.**

⭐ **The resume path therefore depends on ⛔ no trusted timestamp at all** — *"trust a recorded value"* becomes *"verify at the gate"*, the pattern everything else here already follows.

### §3 — why the duplicate mattered

✅ **Recorded as the reviewer framed it:** deleting the duplicate would have fixed **today**; rebuilding deterministically from the map fixes **every future regeneration**. ⭐ **Fix the generator, ⛔ not the output.**

### §4 — ⚠️ the counting trap caught the REVIEWER too — third instance

🔬 **Three substring-count failures in one day, across TWO independent reviewers:** `"ENABLED and started"` · `"RUNNABLE"` · and the reviewer's own section-heading pattern, which did not match the real heading format and returned **"4 sections present, 22 missing"** — ⭐ **a clean, confident, entirely wrong answer that looked exactly like a catastrophic finding.**

⭐🔴 **The lesson binds the people CHECKING the work as much as the work: verify structurally, ⛔ never by grep count.** ⚠️ **A number always looks like evidence.** ✅ Written to `MEMORY_RULES.md` as a standing rule (393 B; both memory guards re-checked clean).

### §5 — state going into the gate

✅ **The reviewer's state list matches mine; nothing in it is contradicted by anything I hold.** ⛔ **`ENTRY-EXEC-DG5-DOCS-MATERIALISATION-1` remains held, separate, and ⛔ not in tonight's gate.** ⭐ **17:30 is a gate, ⛔ not a deadline — if the evidence is not there, stopping is correct and costs a day.** ⭐ **BEFORE ACCEPTING ANY GREEN, PROVE THE CHECK COULD HAVE BEEN RED.**

---

## 16-Sep-2026 (Wed) ~14:45 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT28-16SEP2026` — 🔴 **A FALSE-STOP PATH IN THE MOST-READ POSITION** · ACTIVE IS A FINDING ONLY *AFTER* THE EXPECTED SELF-EXIT · THE CLOCK NEVER DECIDES WHAT A STATE MEANS

**Card:** DEPLOYMENT CARD AMENDMENT 28. No commands. Artifacts by role only.

### §1 — 🔴 the loose wording led to a FALSE STOP, not merely an early start

⭐ **The reviewer worked my flag through to its consequence and it is worse than I stated.** A cold reader arriving at 17:30 and running the three-case adjudication reads `is-active` → **ACTIVE** — **because the service has not exited yet** — applies *"ACTIVE ⇒ do not stop · record · STOP"*, and **the window is missed.** ⛔🔴 **That is a FALSE STOP of a healthy deployment for being five minutes early**, produced by a clock misreading, **inside the very check whose purpose is to detect an abnormal service.** ⭐ **Exactly the class this chain spent the day eliminating, arriving through a summary sentence.**

### §2 — ✅ I swept for the CLASS, ⛔ not the two named lines

🔬 **Structural sweep, ⛔ not a grep count** (Amendment 27 §4): every line mentioning **17:30** *and* adjudication/ACTIVE, partitioned by whether it also carries the precondition. ✅ **It returned exactly the two the reviewer named and no others** — the authoritative three-case table, the Gate 3 anchor and the Gate 1 authorisation line were all **correctly anchored after the expected exit**. ⭐ **The two defective lines sit in the "next action" position** — what someone reads to learn *what to do*, ⛔ not *why*.

⭐ **Same shape as Amendment 18 §2 and Amendment 23 §1:** a sequence living in an authoritative section **and** in two summaries, where the summaries dropped a precondition. ⛔ **Duplication drifting, again, in the most-read location.**

### §3 — the rule, placed at FIVE sites

✅ **Adopted verbatim in force:** ⛔🔴 **ACTIVE *before* the expected self-exit is NORMAL — it is NOT a finding. ACTIVE *after* the expected self-exit IS a finding.** ⭐ **The clock decides WHEN TO LOOK; it NEVER decides WHAT THE STATE MEANS.** ✅ At 17:30 do only the state-independent parts — **open the manifest · starter inventory · artifact identity by role** — **then WAIT for evidence of the self-exit**, and only then adjudicate.

✅ **Written to the three-case table (positively, up front), to BOTH summaries, and to the RESUME RULE** — so a cold reader meets it before reaching any adjudication. 🔬 **Re-swept: 5 sites carry the precondition, 0 gaps, and a synthetic gap line is still detected** ⇒ ⭐ **the check could have been red.** ✅ **No contradiction with line 5202** — *"a clock reading 17:35 is not evidence that the service exited"* — which still holds exactly.

### ⚠️ A self-corrected check, recorded rather than deleted

⚠️ **My first sweep reported 2 GAPS — and both were the RULE I HAD JUST INSERTED.** 🔎 Cause: my predicate tested lowercase `self-exit` while the inserted rule is uppercase. ✅ Re-run case-insensitively: **0 gaps**. ⭐ **Third case-sensitivity false positive in this chain** — and it arrived **one section after** writing the rule that a count over a document about itself is not a check. ⭐ **Recorded, ⛔ not deleted: the detector is part of the evidence.**

### §5 — state

✅ The reviewer's state list matches mine. ⛔ **`ENTRY-EXEC-DG5-DOCS-MATERIALISATION-1` held and outside tonight's gate.** ⭐ **The 17:30 reminder is a reminder. THE SELF-EXIT IS THE PRECONDITION. The manifest is the procedure.** ⭐ **Prove a green could have been red — and prove a RED could have been GREEN.**

---

---

## 16-Sep-2026 (Wed) ~15:25 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT29-16SEP2026` — 🔴 **TWO CHECKPOINTS, SIX MINUTES OF GRACE THAT EITHER EXISTED OR DID NOT** · ✅ **THE MARKERS ADJUDICATE, ⛔ NOT THE CLOCK** · 🔴 **AND THE NEW ADJUDICATION HAD AN E-1 TRAP IN IT**

**Card:** DEPLOYMENT CARD AMENDMENT 29. No commands. Artifacts by role only. ⭐ **Found by ChatGPT; neither the reviewer nor I had caught it.**

### §1 — the gap was real, and it survived INSIDE the rule that closed the last one

🔬 **Structural sweep confirmed exactly the five lines named and no others.** ⚠️ A service exiting at **17:38** — a slow DB flush, a long final report, **nothing wrong** — reads as **ACTIVE after the expected exit ⇒ FINDING ⇒ STOP** under the 17:36 table, and as **still waiting ⇒ proceed** under the 17:42 line. ⭐ **Amendment 28 said ACTIVE after the EXPECTED self-exit is a finding — and the file gave two different answers to when that was.** ⛔ **Same false-stop class, nested one level deeper.**

### §2 — ✅ ONE checkpoint, and the markers carry the judgement

✅ **Normalised to 17:42 at every adjudication site** (⛔ no 17:36 checkpoint remains). ⭐ **The asymmetry decides it: a false stop costs a DAY; waiting six extra minutes costs SIX MINUTES.** 🔬 Re-swept: **0 gaps, 6 compliant lines, and a synthetic 17:36 line is still flagged** ⇒ ⭐ **the check could have been red.**

✅⭐ **The reviewer's second point is the better half, and it is adopted:** the checkpoint decides **WHEN TO READ**, and the **two frozen shutdown markers decide WHAT HAPPENED** — `Shutdown initiated` (`main.py:1631`) and `Shutdown complete` (`main.py:1839`), both **verified present at the build commit** and both already on the Gate 2 capture list. ⭐ **"Is it late?" becomes "did the shutdown START?"** ⛔ **No new mechanism and no new number.**

### 🔴 §2 defect I found in the adopted mechanism — it would have FALSE-STOPPED a clean shutdown

⛔🔴 **BOTH MARKERS ARE `_log.info(...)` — INFO, from logger `main`** — and the stdout handler is `setLevel(WARNING)` (`core/logger.py:420`) ⇒ ⛔ **NEITHER MARKER CAN EVER APPEAR IN THE JOURNAL.** ⚠️ **Adjudicating from `journalctl` would find neither, read `initiated ABSENT`, and declare a FALSE CASE B — "the EOD path never began" — stopping a perfectly clean shutdown.** ⭐ **This is the E-1 defect class reappearing INSIDE the very adjudication that was added to prevent a false stop.** ✅ **Closed by naming the sink in the rule: read the markers in `logs/system_<DATE>.log`, ⛔ never the journal.** ⭐ **Origin-based sink authority is not a boot-window rule; it binds every marker read, everywhere.**

### ✅ The empirical bound, MEASURED rather than assumed

🔬 **15-Sep: the whole shutdown took 3.78 s** — `Shutdown initiated` **17:35:00.712** → `Shutdown complete` **17:35:04.493**, exactly **1** of each. ⭐ So a **generous** wait for `complete` costs nothing, and ⭐ **a shutdown still incomplete minutes after `initiated` is itself worth stopping for** — the bound is a judgement, but a cheap one in the safe direction.

### §3 — accepted

✅ **Fourth counting failure today, and the disposal stands:** the structural sweep, the control line and the case-insensitive re-run held even when the instance did not. ⭐ **The rule did not protect the person who had just written it — which is exactly why the METHOD, ⛔ not the vigilance, is the control.**

### ⚠️ One item in the card's §4 state list is now STALE

⚠️ **`ENTRY-EXEC-DG5-DOCS-MATERIALISATION-1` is ⛔ no longer "held".** 👤 **Rama authorised it by name**, it was **executed**, and 👤 **Rama then ruled the task belongs to the `mcx_data_storage` project** ⇒ ✅ **all four artefacts were MOVED to `D:\Projects\mcx_data_storage\doc\design\`** and ⛔ **this project holds none of them.** ✅ **It is still correctly OUTSIDE tonight's gate** — that half of the card's line holds.

---

## 16-Sep-2026 (Wed) ~15:45 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT30-16SEP2026` — 🔴 **THE GENERAL FORM FOUND AN UNFIXED E-1 IN GATE 7/8** · THE WAIT NOW HAS THREE EVIDENTIAL EXITS AND A LABELLED BOUND · ⭐ **THE REVIEWER RETIRED HIS OWN STATE BLOCK**

**Card:** DEPLOYMENT CARD AMENDMENT 30. No commands. Artifacts by role only.

### §1 — 🔴 generalising the sink rule found a LIVE instance, ⛔ not just a tidy-up

✅ **Adopted in the general form: THE SINK IS NAMED WHEREVER A MARKER IS READ — ⛔ a MARKER-READING rule, ⛔ not a boot-window rule.** ⭐ **And applying it as a sweep rather than as a patch immediately found an unfixed defect in Gate 7/8.**

⛔🔴 **`Verify in the boot log:` WAS AMBIGUOUS, AND THE FIVE CHECKS UNDER IT DO ⛔ NOT SHARE A SINK.** 🔬 The Gate 2 baseline names **two** logs — `BASELINE_journal_…txt` **and** `BASELINE_system_…log` — and, verified at `e7bf477`: **`sr_shadow: ENABLED and started` is INFO** (`main.py:3537`) · **`effect_telemetry: composition OK` is INFO** (`core/effect_telemetry.py:190`) · `composition assertion FAILED` is **CRITICAL** (`:209`) · `sr_shadow wiring failed` is **ERROR** (`main.py:3539`). ⚠️🔴 **The two INFO rows are journal-INVISIBLE** (stdout handler `setLevel(WARNING)`, `core/logger.py:420`) ⇒ **an operator verifying them in the journal finds NEITHER, concludes "the manager did not come up", and STOPS A CORRECT DEPLOY.** ✅ **Closed with a per-marker sink table.** ✅ **The boot-window delimiters got the same treatment** — START and the OK-END are INFO and journal-invisible; ⛔ only the FAILED-END is not.

### §2 — ✅ the wait is now bounded, and two of its three exits need no clock

✅ **Adopted.** ⭐ **"Wait and re-check" without a terminal condition is ⛔ not a rule**, and ChatGPT was right to say so. ⚠️🔴 **AS FIRST WRITTEN THIS ENTRY OVERSTATED TWO OF THE THREE EXITS; CORRECTED BY AMENDMENT 31 §1–§2 and superseded by the manifest text:** ⛔ *"the process DIED MID-SHUTDOWN · FINDING"* and ⛔ *"purely evidential"* were **wrong** — 💭 **INACTIVE with `complete` unobserved does ⛔ NOT prove a mid-shutdown death** (it could have finished and been killed before the log write, or lost its buffer). ⛔ *"HUNG · FINDING"* was likewise wrong: ⭐ **absence within a bound is ⛔ not evidence of a cause.** ✅ **Both now STOP with the CAUSE explicitly NOT ESTABLISHED.**

⚠️🔴🔝 **AND MY "NEVER CORRECTNESS" JUSTIFICATION WAS CIRCULAR — WITHDRAWN (Amendment 31 §1).** ⛔ *"Both outcomes past the bound are STOP, so a generous bound can cost the window but never correctness"* holds **only because the bound was DEFINED as the point at which we stop** — ⭐ **it assumes what it sets out to prove.** 🔴 **A healthy shutdown taking TWELVE minutes completes cleanly and is stopped at TEN: a FALSE STOP produced by the cutoff, and a CORRECTNESS cost.** ⭐ **The cutoff is a DEPLOYMENT-POLICY hold, ⛔ not an inference of hung-ness, and ⛔ it cannot become one by being generous.** ⚠️ **Same error as Amendment 22 §2, made nine cards later — in the card asserting that a correction is where the next defect hides.**
✅⭐🔝 **THE BOUND IS A DURATION FROM THE OBSERVED MARKER — TEN MINUTES FROM `Shutdown initiated`, ⛔ NEVER "at 17:52".** ⭐ **A clock time would re-introduce precisely the second checkpoint Amendment 29 removed.** ⚠️⭐ **It is LABELLED A JUDGEMENT:** ⛔ not measured, ⛔ not derived — 🔬 **3.78 s does NOT imply 600 s.** ✅ **What IS measured is that ten minutes is ~158× the observed duration.** ⭐ **The asymmetry closes it: both outcomes past the bound are STOP, so a generous bound can cost the WINDOW but ⛔ never CORRECTNESS.**

### §3 — ⭐ the reviewer retired his own state block, and the diagnosis is exact

✅ **The stale "held" line on the DG5 task was the v9→v10→v11 mechanism again:** a thirty-line **STATE GOING INTO THE GATE** block copied forward and **re-verified against nothing**. ⭐ **He removed version numbers from his cards for exactly this reason and left a state list doing the same thing.** ✅ **Retired from Amendment 30 onward; the manifest holds state, and a card that restates it is a second surface that can only go stale.** ⭐ **This is Amendment 18 §2 and Amendment 23 §1 landing on the reviewer's own artifact — the rule binds whoever writes, ⛔ not whoever is being checked.**

### ⚠️ My detector failed THREE ways on one question — recorded, ⛔ not hidden

⚠️ **The sink sweep needed three corrections before it was trustworthy:** 🔬 a bare `"starting"` matched ordinary English · a **±6-line window** was too narrow once I inserted text into the block · and a **contiguous-non-blank "block"** split on the blank lines inside one logical section, reporting **5 gaps that were all covered by a rule 2–9 lines away.** ⭐ **I stopped tuning and READ the region**, which settled it in one pass: ✅ **no genuine gap.** ⛔🔴 **A detector re-tuned until it agrees with you is ⛔ not evidence.** ⭐ **Fifth counting/detector failure today — and the disposal is unchanged: the method is the control, ⛔ never the vigilance.**

✅ **One improvement came out of reading it:** the sink rule sat **after** the three cases, so a top-down operator met the cases first. ✅ **Moved ABOVE them** — ⭐ **for a rule whose whole purpose is to stop a journal read, reading ORDER is part of the control.**

### §4 — what this leaves for the gate

✅ **The checkpoint decides WHEN TO READ · the markers decide WHAT HAPPENED · the markers are read in `logs/system_<DATE>.log`, ⛔ never the journal · the wait has three evidential exits and a labelled ten-minute bound from `Shutdown initiated`.** ⭐ **Everything else is in the manifest, which is the only place it lives.**

⭐🔴🔝 **CARRY INTO TOMORROW: A CORRECTION IS WHERE THE NEXT DEFECT IS MOST LIKELY TO BE — it is the newest thing in the file and the least looked at.** 🔬 **Both false stops found today arrived INSIDE a fix for the previous one**, and §1's E-1 was inside the fix for the second. ⭐ **Prove a green could have been red — and prove a RED could have been GREEN.**

---

## 16-Sep-2026 (Wed) ~16:00 IST — `RESULT-SR-SHADOW-V13-DEPLOY-AMENDMENT31-16SEP2026` — 🔴 **THE CUTOFF IS A POLICY HOLD, ⛔ NOT AN INFERENCE** · ALL THREE EXITS NOW NAME ⛔ NO CAUSE · ✅ **AND THE CUTOFF NOW RECORDS ITS OWN COUNTER-EVIDENCE**

**Card:** DEPLOYMENT CARD AMENDMENT 31. No commands. Artifacts by role only. No state block.

### §1 — ⛔ the reviewer's "never correctness" claim was circular, and I had recorded it verbatim

⚠️🔴 **WITHDRAWN.** ⛔ *"Both outcomes past the bound are STOP, so a generous bound can cost the window but never correctness"* is true **only because the bound was DEFINED as the point at which we stop** — ⭐ **it assumes what it sets out to prove.** 🔴 **A healthy shutdown taking TWELVE minutes completes cleanly and is stopped at TEN. That is a FALSE STOP produced by the cutoff, and it is a CORRECTNESS cost, ⛔ not a window cost.**

✅ **Correct statement, now in the manifest:** ⭐ **the cutoff is a DEPLOYMENT-POLICY HOLD** — how long we are willing to hold the window open — ⛔ **it is NOT an inference that the shutdown is hung, and ⛔ it cannot become one by being generous.** ⚠️⭐ **The reviewer names it exactly: this is Amendment 22 §2's error** (*"no content ⇒ the cron never fired"*) **made nine cards later, inside the card asserting that a correction is where the next defect hides.** ⭐ **I had propagated it to the manifest, the A30 record and the ledger; all three are corrected.**

### §2 — the three exits, with every inferred cause removed

✅⭐ **ChatGPT is right on the second exit too, and my wording was the overstatement:** ⛔ **INACTIVE with `complete` unobserved does ⛔ NOT prove a mid-shutdown death** — 💭 the process could have finished its work and been **killed before the log write**, or **lost its buffer**. ⛔ **My *"purely evidential"* label was wrong:** what is evidential is that **the process is gone and completion was never observed**; the *cause* is ⛔ not.

- ✅ **`Shutdown complete` OBSERVED ⇒ proceed to the CONJUNCTIVE check** (inactive **AND** clean exit **AND** healthy). ⛔🔴 **`complete` ALONE IS NOT A PASS.**
- ⛔ **INACTIVE, `complete` NOT OBSERVED ⇒ STOP · CAUSE NOT ESTABLISHED.** 💭 *"Died mid-shutdown"* is recorded as a **labelled INFERENCE**, ⛔ never as the finding.
- ⛔ **NEITHER, PAST THE CUTOFF ⇒ STOP · WHETHER IT IS HUNG IS NOT ESTABLISHED.** ⭐ **Absence within a bound is ⛔ not evidence of a cause.**

✅ **The cutoff stays at TEN MINUTES as a DURATION from `Shutdown initiated`** — ⛔ never a clock time — ⭐ **with its justification restated honestly: ⛔ not "ten minutes proves hung", but "ten minutes is how long we hold the window, chosen at ~158× the SINGLE measured shutdown of 3.78 s." A policy number, labelled as one.**

### §3 — ⭐ the cutoff now records its own counter-evidence — neither review drew this

✅⭐🔝 **THE REVIEWER'S BEST POINT TODAY, AND IT FOLLOWS ONLY ONCE §1 IS ADMITTED: if the cutoff can produce a false stop, then the one thing that MUST survive the stop is the evidence that would show it was too tight.** ✅ **WHEN THE CUTOFF FIRES:** record **service state · main PID · last application-log lines · elapsed since `Shutdown initiated`** — ✅⭐ **THEN KEEP WATCHING**, and record **whether `Shutdown complete` arrives afterwards and at what elapsed time.** ⭐ **Stopping the deployment does ⛔ NOT mean stopping the observation.**

⭐ **`complete` OBSERVED LATE (e.g. 12 min) ⇒ establishes that ten minutes was too short *for that occurrence* — ⛔ it does NOT set a new threshold; revisit the policy only when enough measured durations exist.** ⛔🔴 **`complete` NEVER OBSERVED ⇒ record that completion remained UNOBSERVED, and ⛔ infer NOTHING from that alone** — ⛔ neither that the shutdown was hung, ⛔ nor that the cutoff was correct. ⭐🔴 **A judgement that records its own counter-evidence becomes MEASURABLE RATHER THAN ASSUMED, and can be revisited DELIBERATELY as evidence accumulates** — ⚠️⭐ **two observations are EVIDENCE, ⛔ not a distribution.** ✅ The cutoff was the last place still running on a single measurement.

### §4 — accepted, no action

✅ The Gate 7/8 mixed-sink find is recorded as **the third E-1 instance today and the one that would have bitten hardest** — ⭐ **at the LAST gate, on a correct deploy.** ✅ Both detector lessons stand: ⛔ **a detector re-tuned until it agrees with you is not evidence**, and ⭐ **a rule's POSITION in the document is part of the control** when its purpose is to stop someone reading the wrong log.

---

## 16-Sep-2026 (Wed) 18:05 IST — `RESULT-SR-SHADOW-V13-GATE2-16SEP2026` — ✅ **GATE 2 PASS · CASE A** · 🔴 **THE SINK RULE PREVENTED A REAL FALSE STOP TONIGHT** · ⛔ **STOPPED AT GATE 2 ON 👤 RAMA'S INSTRUCTION**

👤 **Authorisation:** Rama, 17:30+ — *"Run Gate 2 — the manifest-defined read-only capture and adjudication. Nothing beyond it without my word."* ✅ **Gate 2 only. ⛔ Gate 3 NOT run.**

### ✅ THE CONJUNCTIVE VERDICT — all three legs, ⛔ inactive alone is not a pass

| Leg | Evidence | |
|---|---|---|
| **INACTIVE** | `is-active=inactive` · `SubState=dead` · `MainPID=0` | ✅ |
| **Expected clean exit** | `ExecMainExitTimestamp=17:35:05` · `ExecMainStatus=0` · `Result=success` · `NRestarts=0` | ✅ |
| **Healthy session** | routine markers, ⛔ no numeric threshold invented | ✅ |

✅ **Markers (app log):** `Shutdown initiated` **17:35:01.823** → `Shutdown complete` **17:35:05.546**, **exactly 1 each** ⇒ **CASE A · PROCEED.** 🔬 **Shutdown took 3.723 s** — ⭐ a **SECOND** measured duration (15-Sep = 3.78 s). ⚠️ **Two observations are EVIDENCE, ⛔ not a distribution** — the 10-minute cutoff remains a labelled policy number.

✅ **Session established from the system's EXISTING vocabulary:** `Trading System v… starting`×1 · `composition OK`×1 · `composition assertion FAILED`×0 · `effect_census BEGIN day=2026-09-16 mode=live entries=70`×1 · `effect_census END`×1 · restarts **0**.

### 🔴🔝 THE SINK RULE WAS NOT THEORETICAL — IT FIRED TONIGHT

🔬 **Both shutdown markers: 1 each in `logs/system_2026-09-16.log`, and ⛔ ZERO each in the journal.** ⚠️🔴 **An operator adjudicating from `journalctl` would have read `initiated ABSENT` ⇒ declared "THE EOD PATH NEVER BEGAN" ⇒ CASE B FINDING ⇒ STOP — on a perfectly clean shutdown.** ⭐ **Amendment 30 §1 prevented a real false stop on the night it mattered.** ⭐ **Origin-based sink authority is now validated by observation, ⛔ not argument.**

### ⚠️ RECORDED PER GATE 2 ITEM 4 — 6 CRITICALs, and 🔴 TWO ARE NOT THE ROUTINE LADDER

✅ **Four are routine, matched on `reason` ⛔ not on date** (the standing rule): ① 08:15:24 startup notice (`SOFT_KILL reason=circuit_breaker_force_close_15:15`, **auto-cleared same second** as prior-day) · ④⑤⑥ 15:15:00 the EOD kill ladder (`force_close_triggered` → `INACTIVE → SOFT_KILL` → `SOFT_KILL ACTIVATED … triggered_by=order_monitor`).

⚠️🔴 **TWO ARE NOT, AND ARE 👤 RAMA'S TO ADJUDICATE:**
- **15:03:03.985 `mis_autosquareoff` — `MIS_REMAINS: PASS_1: 1 MIS position(s) still open: ['GROWW']`**
- **15:03:08.170 `order_reconciler` — `CHECK1 MANUAL_CLOSE: trade_id=trd_002d28edfcaa4678b7d1039ea1309588 symbol=GROWW local=OPEN/PARTIAL broker=no_position closure_source=EXTERNAL_UNATTRIBUTED rung=none`**

⚠️🔴 **MY FIRST READING — *"closed at the broker by something OUTSIDE the system"* — WAS WRONG AND IS WITHDRAWN.** 🔬 **The contradicting line was in my own capture, 4.2 s earlier:** `15:03:03.922 zerodha_adapter place_order call_start GROWW INTRADAY MARKET qty=2 BUY` → **`15:03:03.959 mis_autosquareoff MIS_AUTO_SQUAREOFF_EXIT_SUBMITTED GROWW broker_order_id=2100155999477342208 market_protection_percent=1.5`**. ⭐ **THE SYSTEM SUBMITTED A MARKET SQUARE-OFF FOR EXACTLY THIS POSITION FOUR SECONDS BEFORE THE BROKER REPORTED `no_position`** — and 🔬 **GROWW not recurring at PASS_2/PASS_3 fits that too: it was gone by the next pass.**
- ⭐🔴 **`rung=none` IS THE TELL.** The reconciler attributes closures to its known rungs (the SL/TGT/EOD ladder); ⛔ **a MIS auto-squareoff order is NOT one of them**, so a closure caused by the system's own square-off has **no rung to match** and falls through to `EXTERNAL_UNATTRIBUTED` **by construction**.
- ⛔🔴 **STILL NOT ESTABLISHED, AND ⛔ NOT CLAIMED:** whether order **`2100155999477342208`** actually FILLED, and whether **189.81** is its fill price. ✅ **ONE read-only query settles it** — that order's status, filled qty, average price and timestamp: **filled/qty 2/~189.81/~15:03:04 ⇒ the system closed its OWN position and failed to recognise its OWN order** ⇒ the CRITICAL is a **MISLABEL** and the real defect is a **reconciler ATTRIBUTION BLIND SPOT**; **not filled or a different price ⇒ "external" stands.**
- ⚠️⭐ **IF IT IS THE ATTRIBUTION GAP, THE SCOPE IS WIDER THAN ONE TRADE: *every* MIS auto-squareoff closure would log a CRITICAL and an unattributed manual close** ⇒ ⭐ **count how often this has already happened BEFORE treating any of them as external events.** ⛔ **SEPARATE TICKET — ⛔ not tonight's work.** ⭐ **It is INTRADAY (15:03) and therefore does ⛔ not contaminate the BOOT baseline Gate 7/8 compares.**

✅ Also recorded: **8 ERROR rows**, **2 Tracebacks** (10:01:12, 10:13:10 — `OrderRejectedError`, which the breaker **explicitly does not count**: *"not a transient connectivity error; breaker is connectivity-only"*).

### ✅ STARTER INVENTORY — re-verified ON THE TWIN, ⛔ not taken from the 05-Aug memory

| Mechanism | Can it start the service in this window? |
|---|---|
| `token-watcher.service` (enabled, **active**) | ⛔ **NO — TWO independent blocks, read at source.** `token_watcher.sh:50` requires `h -ge 8 && h -lt 16` (it is hour **17**); and `:138` sets `exited_today=true` when the exit date is today (it is) ⇒ restart suppressed. |
| `trading-watchman.service` (**drop-in `watchman.conf` found via `systemctl cat`**) | ⛔ **NO** — the dependency runs **trading-system → watchman** (`Wants=`, and *"BindsTo will stop it when trading-system stops"*); 🔬 no `systemctl start` of the service anywhere in it. |
| `cron-watchdog.timer` — **fires 19:30 tonight** | ⛔ **NO** — 🔬 `cron_watchdog.py` contains **no** `systemctl start/restart` and **no** reference to the service; its only `trading-system` hit is the unit **Description**. It asserts cron ran. |
| `Restart=on-failure` | ⛔ **NO** — exit status **0** ⇒ no restart; `NRestarts=0` confirms. |
| **cron (full crontab read)** | ⛔ **NO line starts the service** — all entries are retention, backups, token refresh, preflight, monitoring. |
| **other timers** | ⛔ **NO** — all OS housekeeping (fwupd, sysstat, logrotate, man-db, dpkg, motd, update-notifier, tmpfiles, monitoring-agent). |
| `WantedBy=multi-user.target` | ⚠️ **only via a VM REBOOT.** |
| `resume.sh` · `zerodha_morning.ps1` | ⚠️ **MANUAL only.** |

✅⚠️ **CORRECTED WORDING (adopted): ⛔ NOT "nothing can start the service" but — ⭐ **NO CHECKED AUTOMATED START PATH CAN START IT; A VM REBOOT OR A MANUAL ACTION REMAINS POSSIBLE.** ⭐ **Both exceptions are listed in the table above and the summary must carry them.** ✅ **Nothing suppressed — nothing needed suppressing** (suppression rule step 3: *only if it can fire*). ⛔ **No infrastructure service was masked.**

### ✅ BASELINE FROZEN — two sources, independently

- `BASELINE_journal_trading-system_16-Sep-2026.txt` — **91,403 B** · md5 **`b934aeb832de9021f34c9b5cf8495935`**
- `BASELINE_system_16-Sep-2026.log` — **16,798,379 B** · md5 **`525f00a94baf85a4c644c8b538b70fc8`**
- ✅ **Four frozen prediction artifacts re-verified UNCHANGED** — `41e2cdec…` · `0fab34f5…` · `0cbcf225…` · `8c354fd7…`. ⭐ **THE FREEZE IS NOT BROKEN.**

### ⛔🔴 THE FIRST VM WRITE HAS **STILL NOT OCCURRED**

✅ **Gate 2 was entirely READ-ONLY** — captures and `systemctl show`/`cat` only. ⛔ **Nothing was written to the twin.** ⛔ **Gate 3 NOT run**, and its absence check will re-prove this state independently of this record. ⭐ **If the two ever disagree, the VM wins and the deployment STOPS.**

---

## 16-Sep-2026 (Wed) 18:20 IST — `RESULT-SR-SHADOW-V13-GATE3-16SEP2026` — ✅ **GATE 3 PASS · ALL SIX CONDITIONS** · ✅ **THE ABSENCE CHECK AGREES WITH THE STATE DECLARATION** · ⛔ **STOPPED — GATE 4 IS NOT AUTHORISED**

👤 **Authorisation:** Rama — *"GATE 3 ONLY. Stop there and report."* ⛔ **Gates 4, 5 and 6 are NOT authorised by it.** ⭐ **Gate 4 is the FIRST VM WRITE of the project and is authorised separately, after this result.**

| # | Condition | Observed | |
|---|---|---|---|
| 1 | service NOT active/activating | `inactive` | ✅ |
| 2 | five md5s at `970aabf` / `351bd82e` | all five match the manifest's recorded values | ✅ |
| 3 | absence of both artefacts | `sr_shadow ABSENT` · `evaluator ABSENT` | ✅ |
| 4 | rename preconditions | all 5: **regular file · links=1 · `ubuntu:ubuntu` · mode `664`** | ✅ |
| 5 | no stray `.tmp` | nothing listed | ✅ |
| 6 | cron count | **`0`** | ✅ |

✅ **md5s verified against the manifest's own recorded values, ⛔ not eyeballed:** `main.py` **`85219d22…`** · `signals/signal_processor.py` **`da8c6f98…`** · `core/config_loader.py` **`a034fc08…`** · `config/expected_managers.yaml` **`1dad38c5…`** · `config/system_config.yaml` **`351bd82e73bb0301d850341191c7b72b`** (exact, the 15-Sep fetched file). ⛔ **No drift.**

### ⚠️ THE COMMAND EXITED **rc 1**, AND THAT IS THE *CORRECT* RESULT — PROVEN, ⛔ NOT ASSUMED

⚠️🔴 **An unexplained non-zero rc on a deployment gate must never be waved through.** 🔬 **Cause isolated:** the chain's last command is `crontab -l | grep -c sr_shadow_evaluate`, and **`grep -c` exits 1 when the count is ZERO** — which is exactly the condition Gate 3 requires. ✅ **CONTROL RUN:** the same shape with a pattern that **does** match (`disk_monitor`, count **2**) returns **rc 0** ⇒ ⭐ **the rc tracks the match, ⛔ not a failure.** ⭐ **This is the inverse of the usual trap: here the rc is misleading in the SAFE direction, and it still had to be explained before the gate could be called green.**

### ✅🔝 THE AMENDMENT 27 §2 MECHANISM WORKED — THE TWO SOURCES AGREE

✅ **The state declaration said the first VM write had NOT occurred. Gate 3's absence check — the PROOF, independent of any recorded value — returns `sr_shadow ABSENT` · `evaluator ABSENT` · cron `0`.** ⭐ **They agree, so no disagreement clause is triggered.** ⛔🔴 **THE FIRST VM WRITE HAS STILL NOT OCCURRED.** ⭐ **Gates 2 and 3 were both entirely read-only; the twin is UNCHANGED since 08:15.**

### ✅ Mode recorded for the guarded writes

🔬 **All five target files are mode `664`, owner `ubuntu:ubuntu`, `links=1`, regular files.** ⭐ **This is the value `chmod --reference` must reproduce**, and it is the VM-side `stat -c %a` that protects it — ⚠️ **the PC-side mode test was proven VACUOUS earlier today (Windows ignored `chmod`), so this recorded value is the authority.**

## 16-Sep-2026 (Wed) ~15:10 IST — `RESULT-ENTRY-EXEC-DG5-DOCS-MATERIALISATION-1` — ⚠️ **EXECUTED HERE, THEN RELOCATED TO `mcx_data_storage` BY 👤 RAMA'S DIRECTION** · ⛔ **TRADING-SYSTEM NOW HOLDS NONE OF THESE ARTEFACTS**

⛔🔴🔝 **THIS TASK'S ARTEFACTS DO ⛔ NOT LIVE IN THIS PROJECT. ⭐ THEY ARE AT `D:\Projects\mcx_data_storage\doc\design\`.** ⛔ **Do not look for them under `docs/design/secondary_filteration/` — they were created there on 16-Sep and MOVED OUT the same hour.**

### What happened, in order

✅ `ENTRY-EXEC-DG5-DOCS-MATERIALISATION-1` + ADDENDUM A was authorised by 👤 **Rama's own words naming the task**, and executed in this session: four files created under `docs/design/secondary_filteration/`. ⚠️🔴 **👤 Rama then stated the task belongs to the `mcx_data_storage` project and directed that the files be MOVED to `D:\Projects\mcx_data_storage\doc\design`.** ✅ **Moved 16-Sep ~15:10, copy-verify-then-delete, every SHA-256 re-checked at the destination before any source was removed.**

| File (now at `mcx_data_storage/doc/design/`) | Bytes | SHA-256 |
|---|---|---|
| `DG5_PROPAGATION_2_RECORD_16-Sep-2026.txt` | 14,850 | `65936bd3…` |
| `DG5_PROPAGATION_2_RECORD_16-Sep-2026.txt.provenance.txt` | 1,300 | `b44f65c6…` |
| `WEB_CLAUDE_VALUE_ADDED_DG5_PROPAGATION_2_FINAL_REVIEW_16-Sep-2026.txt` | 8,726 | `cc9925c6…` |
| `WEB_CLAUDE_VALUE_ADDED_DG5_PROPAGATION_2_FINAL_REVIEW_16-Sep-2026.txt.provenance.txt` | 1,863 | `0e601bbe…` |

✅ **This project is back to its pre-task state:** `reviews/` **12 entries / 11 review documents**, `entry-execution/` **4 entries** — exactly as before.

### ⚠️🔴 THE INDEX-STALENESS NOTE IS **CANCELLED**, ⛔ NOT PENDING

⛔ **The "PENDING CONTROLLED SPECIFICATION EDIT" recorded earlier for `00_READ_THIS_FIRST.txt` line 70 IS WITHDRAWN.** 🔬 The file that made the count stale **has left this project**, so `reviews/` again holds **11 review documents** and ✅ **line 70 is CORRECT AS WRITTEN.** ⛔ **No edit to `00_READ_THIS_FIRST.txt` is owed.** ⭐ **A staleness caused by a write is undone by the write's removal — re-measure, ⛔ never carry a pending edit forward on memory alone.**

### 🔴 The one finding worth keeping here — it passed through THIS project's `_inbox`

🔬 **The `_inbox` original and the instruction's APPENDIX B fallback diverge at EXACTLY ONE LINE (209), and it is the known corrupted path.** ⭐ The `_inbox` file carries `D:\Projects` + **`0x09` (a real TAB)** + `rading-system` — the first-order corruption where the backslash-t was consumed. ⚠️ **APPENDIX B had degraded that TAB further into four literal SPACES** — a **SECOND-order corruption acquired in transcript transport.** ✅ **Taking the on-disk original rather than the transcript fallback kept the second-order damage out of the record.** ⭐🔴 **A fallback that reads as equivalent is ⛔ not equivalent — only the BYTE comparison proved it.**

### ✅ What legitimately stays in THIS project

⛔ **`docs/_inbox/` is TRANSPORT, ⛔ NOT A STORE** — nothing in it acquires governing standing; ⛔ never cite it as a source of truth; ⛔ do not clean, delete from or reorganise it. ⚠️ **FILENAME IS NOT IDENTITY** — the same filename carries two distinct artefacts across this bridge, so ✅ **open line 1 before using any `_inbox` file as a source.** ⛔🔴 **NEVER take a Windows path from a chat message as literal** — re-derive it from `PATHS.md` or a listing you ran yourself; ✅ where a corrupted rendering sits inside a verbatim quotation, **copy it as received and flag it**, ⛔ never silently repair quoted governance text. ⭐ **The §A7 cross-project boundary** is recorded in `MEMORY.md` / `MEMORY_HAZARDS.md` and governs this session.

### ⚠️ My error, recorded

⚠️ **§7.1 of the instruction said `~/doc/SYSTEM_MAP.md` — `doc/` SINGULAR, which is `mcx_data_storage`'s convention, ⛔ not this project's `docs/`.** 🔬 mcx has **both** `doc/SYSTEM_MAP.md` and `doc/PATHS.md`, matching §7.1/§7.2 exactly. ⛔ **I mapped them onto this project's files without flagging the discrepancy.** ⭐ **That one-character difference was the signal that the task's memory targets were another project's, and it was the moment to stop and ask.** ✅ **Rule: a path that does not match this project's own convention is a ROUTING QUESTION, ⛔ never a typo to normalise.**

⛔ **Standing position unchanged:** SPEC-2 remains **`NOT LOCATED BY THE DECLARED SEARCH`** · Class-B remains **`ZERO OCCURRENCES LOCATED WITHIN THE DECLARED SEARCH SCOPE`** · **the U1 wording remains IDENTIFIED AND UNAPPLIED.** ⛔ **No code, no config, no commit, no push, no VM access, no production access, no new search.**
