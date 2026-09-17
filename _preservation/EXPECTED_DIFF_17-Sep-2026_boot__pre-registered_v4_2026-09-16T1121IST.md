# PRE-REGISTERED EXPECTED-DIFF **v4** — 17-Sep-2026 BOOT vs THE 16-Sep BASELINE

**Written 2026-09-16 11:21 IST — ⭐ BEFORE the first VM write.** Supersedes **v3** (`419289c2…`), **v2** (`fab48fad…`), **v1** (`b5f7019c…`) — **all KEPT**. Per **AMENDMENTS 12–15**.

## Why v4 exists
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

## E-4 — MUST REMAIN ABSENT · ⭐ authoritative sink: **the APPLICATION LOG** (§2), ⛔ not the journal

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

⛔ **Raw logs remain the evidence of record** — every normalized event must resolve to an auditable **raw line**; record the reference. ⛔ **No fix-forward inside Gate 7/8: CLASSIFY, PRESERVE, THEN ADJUDICATE.**

## How Gate 7/8 runs
1. Verify filename + size + md5 of: both baselines · **v4** · **ruleset v3** · **the frozen normalizer v2**. ⛔ Mismatch ⇒ **STOP**.
2. Compare **application events in the application log ONLY**; **systemd lifecycle in the journal ONLY**. ⛔ Never compare an application event journal-to-journal.
3. Normalize with the frozen normalizer only. Multiset compare. Boot and EOD windows **separately**.
4. Classify into E-1…E-5, **KNOWN-VARIANCE FAMILY**, or **UNPREDICTED**. ⛔ **Recognition by FAMILY IDENTITY, never by count.**
5. ⛔ **CLOSED FROM THE FIRST VM WRITE.** A legitimate missed event is a **MISS IN THE PREDICTION**.
