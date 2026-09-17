# PRE-REGISTERED EXPECTED-DIFF **v3** — 17-Sep-2026 BOOT vs THE 16-Sep BASELINE

**Written 2026-09-16 10:46 IST — ⭐ BEFORE the first VM write.** Supersedes **v2** (`…v2_…T1025IST.md`, md5 `fab48fadb84912131fdee356dc521b13`) and **v1** (`…T1007IST.md`, md5 `b5f7019c30095c1e536578f695a38710`). **Both KEPT.**
Per **AMENDMENTS 12 §1, 13 §§1–4, 14 §§2–4**.

## Why v3 exists
1. **§2 — the E-4 negative assertions needed their OBSERVABILITY STATED**, not implied. Done below, with levels and e7bf477 line numbers.
2. **§3 — the normalizer was CALIBRATED against a known-answer diff** (15-Sep vs 16-Sep boot, no code change between them). 🔴 **It found 13 differing event-instances.** Five message families were legitimately dynamic and the ruleset had **missed all five** — added now, pre-deployment. **Residual measured noise floor: 3.**
3. 🔴 **The baseline composition counts are now MEASURED, so the prediction is LITERAL:** `62 registered, 62 expected` → **`63 registered, 63 expected`**.
4. ⚠️ **A substring-match trap was found** (below) that would have produced a false multiplicity anomaly.

---

## 🔴 THE MEASURED NOISE FLOOR — what "ordinary" looks like

🔬 **Calibration:** `CALIBRATION_bootwindow_2026-09-15.jsonl` (83 events) vs `CALIBRATION_bootwindow_2026-09-16.jsonl` (82 events), boot window = the `Trading System v… starting` line through `composition OK` inclusive. ⛔ **No code changed between these two boots**, so after normalization they *should* be identical.

| Stage | Differing event-instances |
|---|---|
| raw (ts dropped only) | **13** |
| after R3.4–R3.8 were added | **3** |

**The residual 3 are REAL day-to-day variance — ⛔ NOT normalized away.** ⭐ *"A field is not dynamic because it differed; it is dynamic because the code makes it so."* These are genuine differing events, so they stay visible:

| Known-variance family | 15-Sep | 16-Sep |
|---|---|---|
| **`check_ntp_sync`** — ⚠️ **changes LEVEL, so it changes JOURNAL visibility** | `check_ntp_sync: drift 0.001s OK (host=pool.ntp.org)` **INFO** | `check_ntp_sync: failed to query pool.ntp.org: timed out` **WARNING** |
| **`telegram_notifier` / `email_fallback.sent`** (INFO) | present | absent |

> ⭐🔝 **HOW TO READ TOMORROW'S DIFF:** up to **~3 unpredicted event-instances from these two families is ORDINARY**. ⛔ **Anything else is not.** Without this number, the first UNPREDICTED line has no context and nobody can tell whether five unpredicted events is alarming or routine. **A test whose noise floor is unknown cannot be read, only argued about.**
>
> ⚠️ **Note for Gate 2's session-health read:** the 16-Sep NTP timeout is a **WARNING already present in TODAY'S baseline** ⇒ tomorrow it is ⛔ **not new**. It is ⛔ not caused by the deployment and is ⛔ not a reason to stop; it is recorded so it is not mistaken for one.

---

## ⛔🔴 E-4 OBSERVABILITY — stated, not implied (Amendment 14 §2)

> ⭐ **THE DEFECT THIS CLOSES IS A7.** A must-absent row checked against a sink that **cannot carry the event** passes **by construction**, whether or not the event fired. ⛔ **A green check that could not have been red is worse than no check.** Same defect as `STOP_NOT_DEFENDED`, moved from the product into the deployment test.

| # | Event | Level | 🔬 Source @ `e7bf477` | Reaches journal? (WARNING+) | Reaches `system_*.log`? (INFO+) | Observable? |
|---|---|---|---|---|---|---|
| 6 | `sr_shadow wiring failed …` | **ERROR** | `main.py:3539` `_log.error` | ✅ yes | ✅ yes | ✅ **NOT vacuous** |
| 7 | `effect_telemetry composition assertion FAILED…` | **CRITICAL** | `core/effect_telemetry.py:209` `logger.critical` (msg `:197`) | ✅ yes | ✅ yes | ✅ **NOT vacuous** |
| 8 | `sr_shadow: drain error=…` | **ERROR** | `sr_shadow/runner.py:166` `_safe_log("error"…)` | ✅ yes | ✅ yes | ✅ **NOT vacuous** |
| 9 | `sr_shadow.stop_invariant_violated …` | **ERROR** | `sr_shadow/runner.py:216` `_safe_log("error"…)` | ✅ yes | ✅ yes | ✅ **NOT vacuous** |
| 10 | any **new** CRITICAL (set-difference vs baseline) | CRITICAL | — | ✅ yes | ✅ yes | ✅ **NOT vacuous** |

✅ **CONCLUSION, STATED FOR THE RECORD: every E-4 row is ERROR or CRITICAL, both ≥ WARNING ⇒ BOTH sinks carry all of them ⇒ ⛔ NO E-4 row is vacuous.** ⭐ The authoritative sink for E-4 is **either**; check `system_*.log` (it is the superset).

---

## SINK MAP (unchanged from v2) — ⛔ absence in the WRONG sink is NOT a finding
🔬 The journal carries **WARNING+ only** (`core/logger.py:420` stdout `setLevel(WARNING)`; unit routes stdout+stderr → journal). `system_*.log` carries **INFO+, all logger names** (`_SystemFilter`, a pure level catch-all), as **JSON** (`ts`·`level`·`logger`·`msg`).

| Event | Level | system_*.log | journal |
|---|---|---|---|
| E1.1 `sr_shadow: worker started …` | INFO | ✅ | ⛔ **NO** |
| E1.2 `sr_shadow: ENABLED and started …` | INFO | ✅ | ⛔ **NO** |
| E2.3 `composition OK …` | INFO | ✅ | ⛔ **NO** |
| E3.5 `sr_shadow: worker stopped …` | INFO | ✅ | ⛔ **NO** |
| E4.6–10, E5.11, E5.12, runtime rows | ERROR/CRITICAL/WARNING | ✅ | ✅ |

---

## E-1 — NEW AT BOOT, each **exactly once**, in `logs/system_2026-09-17.log`

| # | `logger` | `level` | `msg` | 🔬 Source @ `e7bf477` |
|---|---|---|---|---|
| 1 | **`sr_shadow`** | INFO | `sr_shadow: worker started (contract=v1.3 schema=1 db=<PATH>/sr_shadow.db)` | `sr_shadow/runner.py:151` |
| 2 | **`main`** | INFO | `sr_shadow: ENABLED and started (mode=LIVE, log-only)` | `main.py:3537` |

- ⚠️🔴 **SUBSTRING TRAP — MATCH THE FULL `msg`, ⛔ NEVER A SUBSTRING.** 🔬 `e7bf477:main.py` has **THREE** sites emitting `"ENABLED and started"`: `:3517` `sr_detector`, `:3537` `sr_shadow`, `:3569` `market_regime`. ⭐ On the twin **`sr_detector.enabled: true`** ⇒ **its line is ALREADY in the baseline**; `regime.enabled: false` ⇒ absent. ⇒ ⛔ **a substring count of `"ENABLED and started"` reads 1 today and 2 tomorrow, and would flag a FALSE multiplicity anomaly.** Match `(level, logger, full msg)`.
- **MULTIPLICITY:** each **exactly 1**. **0 ⇒ FINDING** (manager did not come up) · **2 ⇒ ANOMALY** (double construction). ⛔ Never normalized away — duplicates are the signal.
- **ORDER:** 🔬 `start()` is called before the `_log.info` in the same block ⇒ **E1.1 precedes E1.2**. ⛔ **The ONLY order this list asserts.** Incidental baseline order is ⛔ never promoted to a contract.

## E-2 — CHANGED

| # | Event | Predicted change |
|---|---|---|
| 3 | `effect_telemetry: composition OK (%d registered, %d expected)` · `core/effect_telemetry.py:190` · logger `main` · INFO | 🔬 **MEASURED baseline = `62 registered, 62 expected`** (identical on 15-Sep and 16-Sep) ⇒ ⭐ **PREDICTED: `63 registered, 63 expected`**. **Three DISTINCT deltas:** **63/63 ⇒ PASS** · **63 expected / 62 registered ⇒ ⛔ STOP, the manager did not register** · **any other ⇒ ⛔ STOP**. ⛔ **The asymmetric case is NEVER downgraded to a warning.** ⛔ **Counts are NEVER normalized — they ARE the measurement.** |
| 4 | config hash | ⛔ **"changed" is NOT proof of correct deployment.** Record **baseline + expected + observed**. 🔬 YAML `351bd82e…` → `4eab1ae5…`. ⚠️ Note the *snapshot* hash in `config_snapshotter` (`hash=1ad58cb445db`, len 16509B on both calibration days) is a **different artifact** from the YAML md5 — ⛔ do not conflate them. |

## E-3 — NEW AT EOD SHUTDOWN (17-Sep ~17:35) — ⭐ a SEPARATE window from boot
| 5 | `sr_shadow` | INFO | `sr_shadow: worker stopped counters=<JSON> history=<JSON>` · `runner.py:158` |
|---|---|---|---|

⛔ E-3's absence at **boot** is expected and is ⛔ not a finding.

## E-4 — MUST REMAIN ABSENT — observability table above; presence ⇒ ⛔ STOP → ordered rollback

## E-5 — PREDICTED UNCHANGED
| 11 | `sr_detector/retest enabled but no market-data kite handle…` (WARNING, `main.py:3496`) | 🔬 Cannot newly appear: the twin already has `sr_detector.enabled: true`, `v3_chain_mode: "shadow"`, `watchlist.enabled: true` ⇒ the `_md_kite` branch was **already taken**. Presence/absence must match the baseline **in both sinks**. |
|---|---|---|
| 12 | **RUNTIME-ONLY events — ⛔ no BOOT-time appearance expected** | `sr_shadow capture failed for <SYMBOL>: …` (ERROR, `signals/signal_processor.py:649`) · `sr_shadow.capture_failed signal_id=…` (ERROR, `runner.py:142`) · `sr_shadow.capture_duplicate signal_id=…` (INFO, `runner.py:137`) · `sr_shadow.process_failed …` (`runner.py:210`). ⭐ **A capture failure during the session is a RUNTIME FINDING adjudicated on its own — ⛔ NOT a boot-diff anomaly.** |
| 13 | anything from `core/config_loader.py` | 🔬 75-line diff is **pydantic schema only — 0 logging statements**. |
| 14 | everything else | 🔬 `signal_processor.py` adds a ctor kwarg + a runtime path; `expected_managers.yaml` is data consumed by row 3. |

---

## 📋 THE PER-EVENT GATE 7/8 RECORD (Amendment 14 §4) — ⛔ prose is NOT auditable
Fill one row per predicted event. ⭐ *"The manager appeared"* is ⛔ not a result.

| Event | Expected sink | Expected multiplicity | Observed multiplicity | Observed sink | Order requirement | Raw line ref | Result |
|---|---|---|---|---|---|---|---|
| E1.1 | `system_2026-09-17.log` | 1 | | | before E1.2 | | |
| E1.2 | `system_2026-09-17.log` | 1 | | | after E1.1 | | |
| E2.3 | `system_2026-09-17.log` | 1, counts **63/63** | | | — | | |
| E2.4 | — | baseline/expected/observed all recorded | | | — | | |
| E4.6–10 | either (use `system_*.log`) | **0** | | | — | | |
| E5.11 | both | **= baseline** | | | — | | |

- ⛔ **Raw logs stay the evidence of record.** Normalization is **for comparison only**, and every normalized "same event" **must still resolve to an auditable RAW line** — record its reference.
- ⛔ **"Absent" means absent from the event's AUTHORITATIVE sink**, ⛔ never from whichever sink is easiest to query.

## How Gate 7/8 runs
1. Verify filename + size + md5 of: both baselines · **this file (v3)** · **ruleset v2** · **the frozen normalizer**. ⛔ Mismatch ⇒ **STOP**.
2. Normalize with the frozen normalizer **only**. ⛔ Never widen the ruleset.
3. Multiset-compare **normalized semantic events**, each row **in its correct sink**; boot and EOD windows **separately**; CRITICAL as a **set-difference**.
4. Classify every difference into E-1…E-5, **KNOWN-VARIANCE** (the two families above), or **UNPREDICTED**.
5. ⛔ **THE PREDICTION IS CLOSED FROM THE FIRST VM WRITE.** A legitimate missed event is a **MISS IN THE PREDICTION**.
