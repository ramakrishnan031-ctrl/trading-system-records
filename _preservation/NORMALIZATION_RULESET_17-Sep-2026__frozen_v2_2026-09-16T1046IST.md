# NORMALIZATION RULESET **v2** — FROZEN — 17-Sep-2026 boot comparison

**Written 2026-09-16 10:46 IST, BEFORE the first VM write.** Supersedes v1 (`…T1025IST.md`, md5 `f56fe84ff11ba3c07a41989f243a915b`), **KEPT**.
**Executable form, frozen with it:** `normalize_bootlog__frozen_2026-09-16T1046IST.py`.

> ⛔🔴 **Normalize ONLY what is mechanically established from the log format or the code.** ⭐ **A field is not dynamic because it differed; it is dynamic because THE CODE MAKES IT SO.**
> ⭐ **Raw logs remain the evidence of record** — normalization is for **comparison only**, and a normalized "same event" **must still resolve to an auditable raw line**.

## 🔴 WHY v2 — v1 WAS NEVER RUN AGAINST REAL DATA
🔬 Calibrated 16-Sep ~10:50 on **15-Sep vs 16-Sep boot windows** (no code change between them ⇒ they *should* normalize identical). **v1 left 13 differing event-instances.** Five message families were legitimately dynamic and v1 **missed all five**. Added as R3.4–R3.8 ⇒ **residual 3**, which are **real variance** and are ⛔ deliberately NOT normalized.

## R1 — `logs/system_YYYY-MM-DD.log` (JSON lines)
- **R1.1** key = **(`level`, `logger`, normalized `msg`)**. **R1.2** drop **`ts` only**. **R1.3** no other field dropped. **R1.4** ⛔ `level`/`logger` **never** normalized — they are under test.
- **R1.5** ⛔ **match the FULL `msg`, never a substring** — 🔬 three sites emit `"ENABLED and started"` and `sr_detector`'s is already in the baseline.

## R2 — journal
- **R2.1** strip the syslog prefix (host + **PID**). **R2.2** strip systemd lifecycle timestamps, ⛔ **keep status/exit codes**. **R2.3** nothing else.
- ⚠️ The journal holds **WARNING+ only** ⇒ ⛔ absence of an INFO row there is **NOT** a finding.

## R3 — message-body rules. **CLOSED at EIGHT.** Each justified by code.
| # | Normalized | 🔬 Justification |
|---|---|---|
| R3.1 | `db=` path prefix → `<PATH>`; filename kept | `runner.py:152` logs `self._store.path`, runtime-resolved |
| R3.2 | `counters=`/`history=` → `<JSON>` | `runner.py:158` `json.dumps(self.counters)` — session-dependent |
| R3.3 | capture-failure `<SYMBOL>` | `signal_processor.py:649` interpolates the symbol |
| R3.4 | `check_disk_space: OK free=<GB>` | `utils/startup_checks.py:1242` logs `shutil.disk_usage` free — a live measurement |
| R3.5 | `config_snapshotter: resolved config for <DATE>` | `core/config_snapshotter.py:184` arg `snapshot_date` |
| R3.6 | `wrote config snapshot id=<ID> for <DATE>` | `core/config_snapshotter.py:214` — `new_id` is DB-assigned |
| R3.7 | `startup_scenario=COLD: new day (prev=<DATE>, today=<DATE>)` | `utils/startup_checks.py:296` |
| R3.8 | kill-switch `from <DATE>` and `-- new day <DATE>`; ⛔ `reason=`/`by=` KEPT as evidence | `capital/kill_switch.py:360` |

- ⭐ **Why TARGETED date rules rather than a blanket date wildcard:** the calibration compared two different days, so **every date-bearing boot message necessarily differed and was therefore enumerated**. ⇒ the targeted set is **complete for the boot window**, and ⛔ does not mask an unknown date field.
- ⛔🔴 **THE COMPOSITION COUNTS ARE NEVER NORMALIZED — THEY ARE THE MEASUREMENT.** ⛔ **Multiplicity is never normalized away — duplicates are the signal.** ⛔ **Adding an R3.9 tomorrow is the escape hatch this file exists to close.**

## R4 — procedure
1. Verify md5s of both baselines, prediction **v3**, **this file**, and the frozen normalizer. ⛔ Mismatch ⇒ **STOP**.
2. Normalize with **R1–R3 only**. 3. **Multiset** compare. 4. Order asserted **only where the SOURCE proves it**. 5. **Boot and EOD windows separately.** 6. **CRITICAL as a set-difference.**
7. **KNOWN-VARIANCE families (measured, ⛔ not normalized):** `check_ntp_sync` (INFO↔WARNING — ⚠️ changes journal visibility) and `telegram_notifier/email_fallback.sent`. **Measured noise floor: 3 event-instances.**
