# NORMALIZATION RULESET **v3** — FROZEN — 17-Sep-2026 boot comparison

**Written 2026-09-16 11:21 IST, BEFORE the first VM write.** Supersedes v2 (`64c29e4e…`) and v1 (`f56fe84f…`), **both KEPT**.
**Executable form:** `normalize_bootlog__frozen_v2_2026-09-16T1121IST.py`.

## ⛔🔴 R0 — SINK AUTHORITY IS BY **ORIGIN**, NEVER BY LEVEL (Amendment 15 §2)
| Origin | Authoritative sink |
|---|---|
| **application-emitted** (via `get_logger`) | ⭐ **`logs/system_<DATE>.log`, ALWAYS** — it carries INFO+, so a level flip never changes what it holds |
| **systemd / unit lifecycle** | ⭐ **the journal** — the app log cannot carry these at all |

- ⛔ **The journal's copy of an application event is a level-dependent stdout DUPLICATE and is NEVER used for comparison.**
- 🔬 **Why this rule exists:** `check_ntp_sync` is INFO when it succeeds and WARNING when it fails ⇒ journal-to-journal it would **appear from nowhere and vanish again** without the event ever moving. ⭐ **Any family whose level varies with outcome does this.** R0 eliminates the class instead of adjudicating instances.
- ✅ **Mechanically enforced:** the normalizer **refuses (rc 2)** non-JSON input, so it cannot be pointed at the journal.

## R1 — application log (JSON lines)
**R1.1** key = **(`level`, `logger`, normalized `msg`)** · **R1.2** drop **`ts` only** · **R1.3** nothing else dropped · **R1.4** ⛔ `level`/`logger` never normalized — under test · **R1.5** ⛔ **match the FULL `msg`, never a fragment** (🔬 three sites emit `"ENABLED and started"`; sr_detector's is already in the baseline). ⭐ *The prediction names events by what a human would grep for; the comparison must match what the CODE EMITS.*

## R2 — journal — **systemd lifecycle events ONLY**
**R2.1** strip the syslog prefix (host + **PID**) · **R2.2** strip lifecycle timestamps, ⛔ **keep status/exit codes** · **R2.3** nothing else · **R2.4** ⛔ **application events are NOT compared here** (R0).

## R3 — message-body rules. **CLOSED at EIGHT.** Each justified by code.
| # | Normalized | 🔬 Justification |
|---|---|---|
| R3.1 | `db=` path prefix → `<PATH>` | `runner.py:152` logs runtime-resolved `self._store.path` |
| R3.2 | `counters=`/`history=` → `<JSON>` | `runner.py:158` session-dependent |
| R3.3 | capture-failure `<SYMBOL>` | `signal_processor.py:649` |
| R3.4 | `check_disk_space: OK free=<GB>` | `utils/startup_checks.py:1242` — live `shutil.disk_usage` |
| R3.5 | `resolved config for <DATE>` | `core/config_snapshotter.py:184` `snapshot_date` |
| R3.6 | `snapshot id=<ID> for <DATE>` | `:214` — `new_id` DB-assigned |
| R3.7 | `startup_scenario=COLD: new day (prev=<DATE>, today=<DATE>)` | `utils/startup_checks.py:296` |
| R3.8 | kill-switch `from <DATE>`, `-- new day <DATE>`; ⛔ `reason=`/`by=` KEPT | `capital/kill_switch.py:360` |

- ⭐ **Date rules are TARGETED, not a wildcard:** the calibration compared two different days, so every date-bearing boot message necessarily differed and was **enumerated** ⇒ the set is complete for the boot window and masks nothing unknown.
- ⛔🔴 **Composition counts are NEVER normalized — they ARE the measurement.** ⛔ **Multiplicity is never collapsed — duplicates are the signal.** ⛔ **An R3.9 added tomorrow is the escape hatch this file exists to close.**

## R4 — KNOWN-VARIANCE FAMILIES — ⛔ recognised by IDENTITY, never by count
| Family | Behaviour |
|---|---|
| `check_ntp_sync` | outcome varies; flips INFO↔WARNING (harmless under R0) |
| `email_fallback.sent` | fires on some days, not others |

- ⛔ **These are real events and are NEVER normalized away to make tomorrow green.**
- ⭐ **Ten instances of a known family is ORDINARY. ONE instance of a NEW family is NOT.** ✅ The normalizer exits **rc 1** on any unrecognised family, irrespective of known-family counts.
- ⛔ **No numeric noise allowance exists.** The observed residual (3 instances, one comparison) is a **sample**, ⛔ **not a rate and not a budget**.

## R5 — procedure
Verify all md5s → normalize (R1–R3 only) → multiset compare **per authoritative sink** → boot and EOD **separately** → CRITICAL as **set-difference** → classify → ⛔ **no fix-forward: classify, preserve, then adjudicate.**
