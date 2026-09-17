# PRE-REGISTERED EXPECTED-DIFF **v8** — 17-Sep-2026 BOOT vs THE 16-Sep BASELINE

**Written 2026-09-16 11:38 IST — ⭐ BEFORE the first VM write.** Supersedes **v7** (`2faa5aee…`), v6–v1 — **all KEPT**. Per **AMENDMENTS 12–19**.

## Why v8 exists
- ⛔🔴 **§1 — the marker guard was `>= 1`. It must be `== 1`.** `>= 1` closes the zero-marker case but **PASSES TWO markers** — two boots in one day — and **two windows break EVERY multiplicity check.**
- ⛔🔴 **§2 — THE EOD WINDOW HAD NEVER BEEN SPECIFIED**, although the window table assigns **E3.5** and **E4.9** to it. ⭐ **Every hazard established for the boot window applied to it unchanged, and none of them had been checked.** Now specified.

### Why v7 existed
- ⛔🔴 **v6's own identity-verification step named the SUPERSEDED set** (`v4` · `ruleset v3` · `normalizer v2`). ⚠️ **And every one of those files is still on disk, deliberately kept** ⇒ an operator following it verbatim would have md5-verified them, **got a clean MATCH, and proceeded with the wrong set.** ⭐ **The gate would not merely have failed to catch the mismatch — it would have CERTIFIED it and reported GREEN.** 🔬 Confirmed on disk: `b330ca13…` · `5c212e3f…` · `b011440e…` all verify clean.
- ⭐🔝 **STRUCTURAL CAUSE, and the reason a one-line fix is not enough: THE PREDICTION WAS CARRYING PROCEDURE.** The manifest and the prediction both described *"how Gate 7/8 runs"*; the manifest was updated six times today and the prediction's copy was not. ⇒ **§2 fix applied: the prediction is now DATA ONLY** — what the deployment is predicted to change. **The manifest is the sole PROCEDURE.**
- **§3** — the **missing-end-marker** case is now stated.

### Why v6 existed
- **§1** — 🔴 the **WINDOW** was the last unexamined step, in front of everything hardened so far. ✅ Both delimiters are **semantic** (safe), ⛔ **but** a boot-window-only **E-4** check would have been **vacuous by window**: `drain error` comes from a **background thread** and can fire long after the end marker.
- **§3/§4** — the six permanent wordings, the tool-health rc semantics, and the honest evidence boundary with raw outputs kept.

### Why v5 existed
- **§1** — 🔴 **the normalizer's exit code INVERTS on a change pair**, and it is **structurally blind to a missing event**. Closed by removing the place to record its verdict.
- **§2** — the family classifier used **fragment matching**, the very trap R1.5 exists to close — and here it produced a **silent FALSE GREEN**. Now anchored.
- **§3** — a **partially unparseable** file could still exit 0. Any unparseable line is now a finding.

### Why v4 existed
- **§1** — my *"false-positive rate"* framing was **overstated**, and the number **3 must not travel**.
- **§2** — 🔴 **the NTP level-flip has a consequence nobody had drawn**: it dissolves an entire artefact class once sinks are split **by ORIGIN instead of by LEVEL**.
- **§4** — the measured baseline pair is carried into the record beside the observed one.

---

## ⛔🔴🔝 §2 — SINK AUTHORITY IS BY **ORIGIN**, NEVER BY LEVEL

**The problem, followed through from the NTP finding.** The journal receives stdout, and stdout is **WARNING+**. So `check_ntp_sync` lands:

| day | outcome | level | application log | journal |
|---|---|---|---|---|
| 15-Sep | `drift 0.001s OK` | INFO | ✅ | ⛔ **no** |
| 16-Sep | `failed to query … timed out` | WARNING | ✅ | ✅ **yes** |

> ⇒ ⛔ **A JOURNAL-TO-JOURNAL COMPARISON WOULD SHOW THAT EVENT APPEARING FROM NOWHERE ON 16-Sep AND VANISHING AGAIN IF NTP RECOVERS ON 17-Sep.** ⭐ **Neither is a real appearance or disappearance. The event never moved — its VISIBILITY did.**
>
> ⚠️ **Any message family whose level varies with OUTCOME generates phantom UNPREDICTED events in a journal-based comparison** — and one such family was already found on the only two days examined.

**THE RULE THAT DISSOLVES IT — ⛔ not adjudicated case by case tomorrow, ELIMINATED:**

| Event origin | ⭐ AUTHORITATIVE SINK | Why |
|---|---|---|
| **APPLICATION-EMITTED** (anything the app logs via `get_logger`) | ⭐ **`logs/system_<DATE>.log`, ALWAYS** | 🔬 it carries **INFO+**, so a level flip **never** changes what it holds. ⛔ The journal's copy is a **stdout DUPLICATE whose presence depends on level** and **MUST NEVER be used for comparison.** |
| **SYSTEMD / UNIT LIFECYCLE** (`Started`, `Stopped`, `Main process exited`, restarts) | ⭐ **the JOURNAL** | 🔬 the application log **cannot carry them at all** — the application never emitted them. |

- ⇒ ⭐ **No event's authoritative sink ever depends on its level, and the whole class of level-flip artefacts DISAPPEARS.**
- ⛔🔴 **THIS TIGHTENS AMENDMENT 14 §2:** the **E-4 negative assertions are checked against the APPLICATION LOG**, because that is **where the application emits them** — ⛔ **not** against the journal merely because ERROR and CRITICAL happen to reach it.
- ✅ **Enforced mechanically:** the frozen normalizer **REFUSES (rc 2)** a file that is not JSON lines, so pointing it at the journal fails loudly instead of producing a garbage diff. 🔬 Verified: journal-format input ⇒ `REFUSED`, rc 2; JSON input ⇒ rc 0.

---

## ⛔🔴 §1 — WHAT THE CALIBRATION IS, AND WHAT IT IS NOT

> **Pre-deployment calibration observed 3 residual event-instances across the available no-change comparison. These are the currently observed normalisation and variance cases, ⛔ NOT a statistically estimated false-positive rate.**

- ⛔ **There is no denominator and no distribution over repeated no-deployment boots.** One pair is a **sample**, ⛔ not a rate.
- ⛔🔴🔝 **AND THE NUMBER "3" MUST NOT TRAVEL.** ⭐ **RECOGNITION IS BY FAMILY IDENTITY, NEVER BY COUNT.**
  - ✅ **Ten instances of `check_ntp_sync` is ORDINARY.**
  - ⛔ **ONE instance of a THIRD family is NOT.**
- ✅ **Enforced mechanically, ⛔ not by instruction:** the normalizer reports **by family**, and exits **rc 1 if ANY unrecognised family appears**, regardless of how many instances the known families produced. 🔬 Verified non-vacuous: known-only ⇒ rc 0 (with x2 and x1 instances); one injected new family ⇒ `UNRECOGNISED FAMILIES: 1`, rc 1.

**KNOWN-VARIANCE FAMILIES (⛔ deliberately NOT normalized — they are real events):**

| Family | Behaviour |
|---|---|
| **`check_ntp_sync`** | outcome varies; ⚠️ flips **INFO↔WARNING**. ⭐ Harmless now that the application log is authoritative. |
| **`email_fallback.sent`** (`telegram_notifier`) | fires on some days, not others |

---

## E-1 — NEW AT BOOT · authoritative sink: **`logs/system_2026-09-17.log`**

| # | `logger` | `level` | `msg` | 🔬 Source @ `e7bf477` |
|---|---|---|---|---|
| 1 | **`sr_shadow`** | INFO | `sr_shadow: worker started (contract=v1.3 schema=1 db=<PATH>/sr_shadow.db)` | `sr_shadow/runner.py:151` |
| 2 | **`main`** | INFO | `sr_shadow: ENABLED and started (mode=LIVE, log-only)` | `main.py:3537` |

- **MULTIPLICITY:** each **exactly 1**. **0 ⇒ FINDING** · **2 ⇒ ANOMALY**. ⛔ Never collapsed.
- **ORDER:** E1.1 before E1.2 — 🔬 proven by source. ⛔ The only order asserted.
- ⚠️🔴 **MATCH THE FULL `msg`, ⛔ NEVER A FRAGMENT** (§3). 🔬 Three sites emit `"ENABLED and started"` — `main.py:3517` sr_detector · `:3537` sr_shadow · `:3569` market_regime — and **sr_detector is ENABLED on the twin, so its line is ALREADY in the baseline** ⇒ a fragment count reads **1 today / 2 tomorrow** = a **FALSE multiplicity anomaly on the very first thing Gate 7/8 looks at.**
  - ⭐🔝 **WHY IT WAS NEARLY MISSED, worth recording:** **the prediction named the event by the text a HUMAN WOULD GREP FOR. The comparison must match on WHAT THE CODE EMITS — a different thing.**
  - ✅ The fix is **general, ⛔ not a patch for this one string**: requiring the full `msg` protects `worker started` and everything else predicted, without enumerating them.

## E-2 — CHANGED · authoritative sink: **application log**

| # | Event | Predicted |
|---|---|---|
| 3 | `effect_telemetry: composition OK (%d registered, %d expected)` · `core/effect_telemetry.py:190` · logger `main` · INFO | ⭐ **MEASURED BASELINE = `62 registered, 62 expected`** (identical 15-Sep and 16-Sep) ⇒ **PREDICTED `63 registered, 63 expected`**. ⭐ **Two specific integers that either appear or do not — falsifiable in a way a delta is not.** |
| 4 | config hash | ⛔ **"changed" ≠ correct deployment.** Record **baseline + expected + observed**. 🔬 YAML `351bd82e…` → `4eab1ae5…`. ⚠️ The `config_snapshotter` hash (`1ad58cb445db`, len 16509B both days) is a **DIFFERENT artifact** — ⛔ do not conflate. |

**The three composition outcomes, ⛔ never merged:**

| Observed | Verdict |
|---|---|
| **`63 registered, 63 expected`** | ✅ expected |
| **`63 expected / 62 registered`** | ⛔ **STOP — the manager did not register.** ⛔ NEVER downgraded to a warning |
| `62 / 63`, or anything else | ⛔ **ANOMALY → STOP** |

⭐ **Carry the MEASURED BASELINE PAIR (62/62) into the Gate 7/8 record beside the observed pair.**

## E-3 — EOD SHUTDOWN (17-Sep ~17:35) · application log · **a SEPARATE window**
| 5 | `sr_shadow` | INFO | `sr_shadow: worker stopped counters=<JSON> history=<JSON>` · `runner.py:158` |
|---|---|---|---|

## E-4 — MUST REMAIN ABSENT · ⭐ sink: **the APPLICATION LOG** (§2) · ⛔ **window per row (§1): rows 6–7 = BOOT WINDOW; rows 8 and 10 = WHOLE-DAY log; row 9 = EOD**

| # | Event | Level | 🔬 Source @ `e7bf477` | In the app log? | Vacuous? |
|---|---|---|---|---|---|
| 6 | `sr_shadow wiring failed …` | ERROR | `main.py:3539` | ✅ (INFO+) | ✅ **no** |
| 7 | `effect_telemetry composition assertion FAILED…` | CRITICAL | `core/effect_telemetry.py:209` | ✅ | ✅ **no** |
| 8 | `sr_shadow: drain error=…` | ERROR | `sr_shadow/runner.py:166` | ✅ | ✅ **no** |
| 9 | `sr_shadow.stop_invariant_violated …` | ERROR | `sr_shadow/runner.py:216` | ✅ | ✅ **no** |
| 10 | any **new** CRITICAL (set-difference) | CRITICAL | — | ✅ | ✅ **no** |

⭐ **All five are application-emitted, and the application log carries INFO+ ⇒ it holds every one of them regardless of level ⇒ ⛔ NO E-4 ROW IS VACUOUS.** *(A must-absent row checked against a sink that cannot carry the event passes **by construction** — A7.)*

## E-5 — PREDICTED UNCHANGED
| 11 | `sr_detector/retest enabled but no market-data kite handle…` (WARNING, `main.py:3496`) | 🔬 Cannot newly appear — the twin already has `sr_detector.enabled: true`, `v3_chain_mode: "shadow"`, `watchlist.enabled: true` ⇒ the `_md_kite` branch was **already taken**. ⭐ Compared **in the application log**, ⛔ not the journal. |
|---|---|---|
| 12 | **RUNTIME-ONLY** — ⛔ no boot-time appearance expected | `sr_shadow capture failed for <SYMBOL>` (ERROR, `signal_processor.py:649`) · `sr_shadow.capture_failed` (ERROR, `runner.py:142`) · `sr_shadow.capture_duplicate` (INFO, `runner.py:137`) · `sr_shadow.process_failed` (`runner.py:210`). ⭐ A session capture failure is a **RUNTIME FINDING**, ⛔ not a boot-diff anomaly. |
| 13 | `core/config_loader.py` | 🔬 pydantic schema only — **0 logging statements** |
| 14 | everything else | 🔬 ctor kwarg + runtime path; registry is data for row 3 |

---



## ⛔🔴🔝 THE WINDOW SPECIFICATION (Amendment 17 §1) — mirrored in the manifest beside the artifact hashes

⚠️ **THE DEPLOYMENT MAKES THE BOOT LONGER.** sr_shadow adds startup lines, so tomorrow's boot contains **more events** than the baseline's. ⭐ That is the intended change — and it is exactly what breaks a window delimited by **POSITION** or **DURATION**: the added lines would push later lines OUT of tomorrow's window, where they would surface as **ONLY IN A** and read as **MISSING EVENTS** — ⛔ **the one category the per-event table treats most seriously, because "expected present, observed absent" IS the E-1 failure signature.**

### The delimiters actually used — ✅ BOTH SEMANTIC, ⛔ neither positional nor time-bounded
```
awk '/Trading System v.* starting/{f=1} f{print} /composition OK|composition assertion FAILED/{if(f)exit}' logs/system_<DATE>.log
```
| | Delimiter | Kind |
|---|---|---|
| **START** | the `Trading System v… starting (mode=…)` line | ✅ **semantic marker** |
| **END** | the `effect_telemetry: composition OK (…)` line, or `composition assertion FAILED` | ✅ **semantic marker** |

- ⭐ **The window GROWS WITH THE BOOT** ⇒ ⛔ the added sr_shadow lines cannot push anything out.
- ✅ **The end marker sits AFTER ALL MANAGER CONSTRUCTION, ⛔ not between managers.** 🔬 `assert_composition` is called at **`main.py:4277`**; the sr_shadow block is **`main.py:3536–3539`** ⇒ E1.1, E1.2 and E4.6 are all emitted **before** the end marker.
- ✅ **MARKER UNIQUENESS VERIFIED across the WHOLE day, both days** (read-only): `starting=1 · composition OK=1 · composition assertion FAILED=0` on **15-Sep and 16-Sep** ⇒ the window is unambiguous and **no mid-day restart occurred**. ⚠️ If Gate 2 records **`NRestarts` ≠ 0**, or a second `starting` line exists, ⛔ **re-examine the window selection before comparing.**
- ✅ **The IDENTICAL delimiters were used for the baseline and will be used tomorrow.**
- ⛔🔴🔝 **IF NEITHER END MARKER APPEARS, THAT IS ITSELF THE FINDING (Amendment 18 §3).** The terminator is `composition OK` **OR** `composition assertion FAILED`. ⚠️ **If the boot dies before reaching composition at `main.py:4277`, neither fires**, `f` stays set, and awk **prints to end of file** ⇒ the "boot window" **silently becomes the whole day** and the comparison produces enormous residuals.
  - ⭐ That would be **loud**, which is fine — ⚠️ **but it would look like a NORMALIZER or WINDOW fault rather than what it actually is: THE BOOT NEVER REACHED COMPOSITION.**
  - ⛔🔴🔝 **THE GUARD IS `== 1`, ⛔ NOT `>= 1` (Amendment 19 §1).** A `>= 1` guard closes the zero case but ⚠️ **PASSES TWO markers**:

| markers | meaning | verdict |
|---|---|---|
| **0** | the window never reached its terminator | ⛔ **STOP** |
| **1** | a single unambiguous window | ✅ valid |
| **2+** | two boots / shutdowns in one day | ⛔ **STOP** — ⚠️ **`>= 1` would have PASSED this** |

  - ⚠️🔴 **WHY TWO MARKERS IS FATAL, whatever caused it:** **E1.1 and E1.2 are each predicted EXACTLY ONCE.** Across two boots the whole-day log holds **two of each**, and **`drain error` and any new CRITICAL — both assigned to the WHOLE-DAY window — would span TWO PROCESS LIFETIMES attributed to ONE deployment.** ⭐ **And the awk exits at the FIRST terminator**, so the boot window would silently be **boot #1** while the whole-day checks covered **both** ⇒ **two windows, two different meanings of "today's boot".**
  - ✅ **THE GUARD, on BOTH windows:** **start count `== 1`** · **end count `== 1`** · **the end marker occurs AFTER the start marker**. Any violation ⇒ **`WINDOW_INVALID` → STOP.**
  - ⭐ Uniqueness was **observed** by hand on both calibration days, and Gate 2 records `NRestarts` — ⛔ **but those are an observation and a separate gate, not this guard.** ✅ The guard now **matches what was verified**, and is **mechanically enforced by the frozen window validator** (filename, size and md5 in the manifest).
  - ⚠️ **Which direction tomorrow differs from the calibration:** today's was a **normal** boot; tomorrow's **introduces a new manager into the construction path**. A second boot is **not likely** — construction sits inside `try/except` and a live composition failure CRITICALs and continues — ⭐ **but `>= 1` was the one condition under which the comparison would proceed on an ambiguous window and report something.**

### 🔴 BUT A BOOT-WINDOW-ONLY E-4 CHECK WOULD BE **VACUOUS BY WINDOW**
🔬 `start()` spawns a **background daemon thread** (`threading.Thread(target=self._run, name="sr-shadow-worker", daemon=True)`, `runner.py:149`), and **`sr_shadow: drain error=` is emitted from inside that thread's loop** (`runner.py:166`). ⇒ ⛔ **it can be emitted at ANY time during the session — long AFTER `composition OK`.**

> ⛔🔴 **A must-absent row checked over a window that CANNOT CONTAIN the event passes BY CONSTRUCTION** — ⭐ **the same A7 defect as the sink vacuity, in a THIRD dimension: sink → level → now WINDOW.**

### ⭐ WINDOW ASSIGNMENT PER EVENT CLASS — ⛔ no row is adjudicated over a window that cannot hold it

| Events | Window | Source |
|---|---|---|
| **E1.1 · E1.2 · E2.3 · E4.6 · E4.7 · E5.11** | **BOOT WINDOW** `[starting … composition OK/FAILED]` | all emitted on the main thread before `main.py:4277` |
| **E4.8** `drain error` · **E4.10** any new CRITICAL · **E5.12** runtime capture events | ⛔🔴 **WHOLE-DAY application log** — `logs/system_2026-09-17.log` **in full** | background thread / any time |
| **E4.9** `stop_invariant_violated` · **E3.5** `worker stopped` | **EOD WINDOW** (shutdown) | emitted in `stop()` |
| systemd lifecycle (`Started`/`Stopped`/`Main process exited`/restarts) | **journal, whole day** (`--since today`) | systemd, ⛔ never the app |

- ⚠️ The journal capture is **time-bounded by nature** (`--since today`). ⭐ That is acceptable **only** because it is a **whole-day** bound used for **systemd lifecycle events**, ⛔ **not** a positional boot-window delimiter — nothing the deployment adds can be pushed out of a full day.


## ⛔🔴🔝 THE **EOD** WINDOW SPECIFICATION (Amendment 19 §2)

⚠️ **The window table assigns E3.5 (`sr_shadow: worker stopped`) and E4.9 (`sr_shadow.stop_invariant_violated`) to an EOD window — and its delimiters had never been stated.** ⭐ **Every hazard established for the boot window applies to it unchanged**, so it is specified here to the same standard.

| | Delimiter | Kind | 🔬 Source @ `e7bf477` |
|---|---|---|---|
| **START** | `Shutdown initiated` | ✅ **semantic marker** | `main.py:1631` |
| **END** | `Shutdown complete` | ✅ **semantic marker** | `main.py:1839` |

- ✅ **⛔ NOT a clock slice.** A 17:30–17:40 box would be **positional**, and **the same reasoning that made a positional boot window unsafe makes that unsafe** — a shutdown that runs long, or a session that ends early, moves events out of the box.
- ✅ **THE END MARKER SITS AFTER THE `sr_shadow.stop()` CALL, ⛔ not before it:** 🔬 `Shutdown initiated` **`:1631`** → `sr_shadow.stop()` **`:1705`** → `Shutdown complete` **`:1839`**. ⇒ **both E3.5 and E4.9 are emitted INSIDE the window.**
- ✅ **THE MISSING-END-MARKER CASE APPLIES HERE TOO:** a shutdown that **dies partway never emits `Shutdown complete`** ⇒ the window runs to EOF or to nothing. ⛔ **That is ITSELF the finding — "the shutdown never completed"** — ⛔ never a normalizer fault.
- ✅ **THE SAME `== 1` GUARD APPLIES:** `Shutdown initiated == 1` · `Shutdown complete == 1` · end after start.
- 🔬 **Validated against REAL data:** the 15-Sep EOD window extract (`init=1 complete=1`) returns **WINDOW_OK**; the same spec run against a **boot** file returns **WINDOW_INVALID** — ⭐ a non-vacuous cross-check.
- ⚠️ **Note on the 16-Sep baseline:** at midday the 16-Sep log had **`init=0 complete=0`** — ⭐ correct, because **today's session had not yet self-exited.** The EOD baseline only exists **after 17:35**, which is why the Gate 2 capture runs **after** the self-exit.

> ⭐🔝 **THIS IS THE SAME PATTERN AS AMENDMENT 18 §1.** There, a procedure existed in **two places** and only one was updated. Here, a **window rule was established for one window and the second window was never brought under it.** ⛔ **Both are gaps between "the rule exists" and "the rule covers everything it names."**

## ⛔🔴 WINDOW_INVALID TAKES PRECEDENCE OVER EVERY RESIDUAL (Amendment 19 §3)

> ⛔ **When the window is invalid, the FIRST finding is `WINDOW_INVALID` — ⛔ NEVER `NORMALIZER_RESIDUAL`.**

⭐ **A huge residual list produced by a malformed window must not be read as the primary failure.** An unterminated window runs to end of file and yields enormous residuals that **look like a normalizer or window fault** rather than what they are. ✅ **The window validator runs FIRST, as a PRECONDITION**, and on failure the comparison is ⛔ **not run at all.**

## ⛔🔴🔝 THE NORMALIZER'S EXIT CODE CARRIES **NO VERDICT** (Amendment 16 §1)

> ⛔ **FOR THE 17-Sep RUN, THE NORMALIZER'S EXIT CODE CARRIES NO VERDICT.**

🔬 **DEMONSTRATED 16-Sep, by simulating both outcomes against the real 16-Sep boot window:**

| Simulated 17-Sep outcome | Normalizer says | rc |
|---|---|---|
| ✅ **CORRECT deployment** (sr_shadow up, composition 63/63) | `UNRECOGNISED FAMILIES: 4` | **rc 1** |
| ⛔ **FAILED deployment** (manager never started, nothing emitted) | `UNRECOGNISED FAMILIES: 0` | **rc 0** |

- ⇒ ⛔🔴 **rc 1 IS THE EXPECTED OUTCOME AND rc 0 IS THE ALARMING ONE** — the exact reverse of what the no-change calibration established, and the reverse of what any operator or future session will assume. **A correct deployment reads as failure; a failed one reads as clean.**
- ⛔🔴 **AND THE DEEPER PROPERTY: the normalizer CANNOT DETECT A MISSING EXPECTED EVENT AT ALL.** It reports **differences**. An event that never appears on **either** side produces **no difference**. ⭐ **Absence is exactly the E-1 failure mode the whole prediction exists to catch, and the tool is STRUCTURALLY BLIND to it.**

**THE CLOSURE — option (b): leave the tool alone and REMOVE THE PLACE TO RECORD ITS VERDICT.**
- ⭐ The normalizer's output is **INPUT to classification, ⛔ NEVER a verdict.**
- ⛔ **The per-event Gate 7/8 record has NO FIELD for normalizer pass/fail — only a field for its RESIDUAL LIST.** ⭐ *The enforcement is that there is nowhere to write the wrong answer down.*
- ⭐ **The verdict comes SOLELY from the per-event table**, which does test presence, multiplicity and order.
- ✅ The tool now **prints this banner itself**, before and after its output — so the warning cannot be missed by someone reading only the console.

## 📋 PER-EVENT GATE 7/8 RECORD — ⛔ prose is NOT auditable

| Event identity | logger | level | **Authoritative sink** | Expected mult. | Observed mult. | Order rule | Raw evidence ref | Result |
|---|---|---|---|---|---|---|---|---|
| E1.1 `sr_shadow: worker started` | `sr_shadow` | INFO | app log | 1 | | before E1.2 | | |
| E1.2 `sr_shadow: ENABLED and started` | `main` | INFO | app log | 1 | | after E1.1 | | |
| E2.3 `composition OK` | `main` | INFO | app log | 1 · **baseline 62/62 → expect 63/63** | | — | | |
| E2.4 config hash | — | — | — | baseline+expected+observed | | — | | |
| E4.6–10 | various | ERROR/CRITICAL | **app log** | **0** | | — | | |
| E5.11 kite-handle warning | `main` | WARNING | **app log** | **= baseline** | | — | | |
| systemd lifecycle | — | — | **journal** | per baseline | | — | | |
| **NORMALIZER RESIDUAL LIST** (paste verbatim) | — | — | — | — | — | — | — | ⛔ **NOT a verdict — input to classification only** |
| **UNPARSEABLE LINES** (Amendment 16 §3) | — | — | — | **0** | | — | | any ≠ 0 is a **FINDING** |
| ⛔ **WINDOW VALIDITY — boot** (Amendment 19) | — | — | app log, whole day | start `== 1`, end `== 1`, end after start | | — | | **`WINDOW_INVALID` ⇒ STOP, and it PRECEDES every residual** |
| ⛔ **WINDOW VALIDITY — EOD** (Amendment 19) | — | — | app log, whole day | `Shutdown initiated == 1`, `Shutdown complete == 1`, end after start | | — | | **`WINDOW_INVALID` ⇒ STOP** |

⛔🔴 **THERE IS DELIBERATELY NO "normalizer pass/fail" FIELD IN THIS TABLE.** ⭐ Its rc is inverted on a change pair and blind to absence; **the verdict comes from the rows above, ⛔ never from an exit code.**

⛔ **Raw logs remain the evidence of record** — every normalized event must resolve to an auditable **raw line**; record the reference. ⛔ **No fix-forward inside Gate 7/8: CLASSIFY, PRESERVE, THEN ADJUDICATE.**


## 📐 THE SIX PERMANENT WORDINGS (Amendment 17 §3)

| | |
|---|---|
| **NORMALIZER** | residual extractor and input-quality checker **only**; ⛔ its exit code is **not** the deployment verdict |
| **EXPECTED EVENTS** | every pre-registered event adjudicated **independently** for presence, multiplicity and order — ⭐ **including when the normalizer reports no residual** |
| **FAMILY** | known-family recognition requires the **configured logger AND the configured normalized message prefix**; ⛔ never arbitrary substring containment |
| **CORRUPTION** | **any** unparseable application-log line is a **finding**; **≥50% remains a refusal** |
| **EVIDENCE** | every finding resolves to a **raw line** |
| **FREEZE** | prediction, ruleset and normalizer **close at the first VM write** |

⭐🔝 **WHY THE FIRST MATTERS MOST — the rc still has REAL meaning, as a TOOL-HEALTH signal:**

| rc | means |
|---|---|
| **0** | no residual **and** no input problem |
| **1** | a residual **or** a malformed-line finding |
| **2** | input misuse (not a JSON application log) |

⛔ **NONE of those is "the deployment succeeded."** ⭐ **Keeping that distinction written down is what stops a future maintainer deleting the per-event table and restoring the original defect without noticing.**

## ⚖️ THE EVIDENCE BOUNDARY (Amendment 17 §4) — stated honestly

⚠️ The three normalizer fixes are **VERIFIED ACCORDING TO THIS SESSION'S REPORT**, with named non-vacuous tests. ⭐ **That is strong evidence. It is ⛔ NOT an independent code audit** — no external reviewer has read the corrected normalizer.

✅ **So the RAW outputs are kept, ⛔ not the prose summary.** The next reviewer can re-derive every assertion from:
- **`NORMALIZER_TEST_EVIDENCE_2026-09-16T1150IST.txt`** (19,657 B, md5 `3c340707ccaf2b64339332faf13c1460`) — six runs with full output and exit codes: **T1 post-fix calibration rc 0** · **T2 simulated CORRECT deployment rc 1** · **T3 simulated FAILED deployment rc 0** · **T4 anchored-family non-vacuity rc 1** · **T5 two-corrupt-lines non-vacuity rc 1** · **T6 misuse guard rc 2**.
- The four **test INPUT files**, kept beside it (`NORMALIZER_TEST_INPUT_*.jsonl`).
- ✅ **The ORIGINAL calibration extracts are UNCHANGED** (`f5809812…`, `ee034ee1…`) — ⛔ the post-fix run did **not** overwrite them. ⭐ **Both are evidence, and the pair is what shows the correction did not change what the calibration means.**

## ⛔🔴🔝 PROCEDURE LIVES IN THE MANIFEST — ⛔ NOT HERE (Amendment 18 §2)

> ⭐ **THIS FILE IS DATA.** It states **what the deployment is predicted to change**: the events, their loggers, levels, sinks, multiplicities, orders and windows.
>
> ⛔ **THE PROCEDURE — artifact-identity verification, how to run the comparison, what to record, when to stop — IS IN THE MANIFEST, AND ONLY THERE:**
> **`docs/SYSTEM_MAP.md` → section `MANIFEST-SR-SHADOW-V13-DEPLOY-16SEP2026` → Gate 4-PRE and Gate 7/8.**

- ⚠️🔴 **WHY THIS SECTION IS NOW A POINTER AND NOT A COPY.** v6 duplicated the procedure here, and its step 1 went stale while the manifest's did not — naming **v4 / ruleset v3 / normalizer v2**, every one superseded, **every one still on disk and verifying clean**. ⭐ **Two documents describing the same procedure, both reading as authoritative to whoever opens only one.**
- ⛔ **A prediction that also INSTRUCTS must be re-verified every time the procedure moves. A prediction that only PREDICTS does not.**
- ⛔🔴 **The reference above is BY SECTION NAME, deliberately — ⛔ NOT by version.** *"v7 refers to the current set"* would be the same failure with one more level of indirection. ⭐ **One authoritative location, named once.**
