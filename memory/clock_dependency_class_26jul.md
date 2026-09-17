---
name: clock-dependency-class-26jul
description: "Clock-dependent code is a CLASS with three axes — hour-of-day (25-Jul), day-of-week (26-Jul), and YEAR; the year one is not a test bug, it is a MEASURED boot-blocker on the first boot of 2027 (nse_holidays_2027.yaml absent ⇒ ConfigMissingError)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1c52b905-f204-4abe-966d-ae9b3bbd045e
  modified: 2026-07-26T16:31:05.816Z
---

⏰ **THREE AXES, FOUND ONE PER DAY. Two were test bugs; the third stops the service.**

| axis | instance | status |
|---|---|---|
| **hour-of-day** | `test_interactive_startup::test_holiday_guard_missing_yaml_proceeds` — `main()` returns 0 at the 18:15 window check instead of reaching the config load it asserts on | fixed 25-Jul |
| **day-of-week** | `test_daily_trade_review::test_main_defaults_date_to_today_and_records_heartbeat` — no `--date` ⇒ today IST ⇒ the non-trading-day guard correctly skips ⇒ the xlsx it demands is never written | fixed 26-Jul, branch `hold-check1-w8-26jul` |
| **YEAR** 🔴 | `core/config_loader.py` `_CONFIG_FILES` resolves `f"nse_holidays_{date.today().year}.yaml"` **at module import**; only `nse_holidays_2026.yaml` exists | ⚠️ **OPEN — pinned, not fixed** |

🚨 **THE YEAR ONE, MEASURED (not reasoned): patching `date.today` to 2027 before importing
`config_loader` gives `ConfigMissingError: Required config file not found:
nse_holidays_2027.yaml`. `load_all()` is on the boot path (`main.py:1743`) ⇒ THE FIRST 08:15
BOOT OF 2027 DOES NOT START.**
⚠️ And the suite hides it: every existing config test writes stubs named
`nse_holidays_2026.yaml`, so **they would all break the same morning** for a reason that is
not a bug in the code under test.
✅ **PINNED, BOTH HORIZONS.** `test_every_registered_config_file_exists_for_the_CURRENT_year`
(green 2026, **proven RED under a 2027 clock**) **plus** `test_next_years_holiday_file_lands_
before_the_current_one_runs_out`, which fires **from 1-Dec** — 30 days, deliberately not 60:
long enough to act in, short enough that NSE has actually published, because **a red test
nobody CAN fix is noise**. Both messages say *add the file, do not edit the test*.

⛔⛔ **AND THE TRAP IN THE OBVIOUS FIX: NEVER INVENT OR INFER THE HOLIDAY DATES.** A guessed
calendar is far worse than a missing one — the system would trade on a market holiday, or skip
a real trading day, **and believe it was right**. NSE publishes the next year's list ~Nov–Dec;
until then there is nothing to copy. **The fix is to commit NSE's PUBLISHED
`config/nse_holidays_2027.yaml` before 31-Dec-2026 — Rama's action. The tests are only alarms.**

📧✅ **26-Jul EVENING — THE WARNING NOW REACHES A HUMAN, not just a test runner
([[holiday-reminder-reaches-rama-26jul]], `cbcad2c`).** The suite tripwire is KEPT, but a
reminder that needs somebody to run the tests is not a reminder: `security_monitor.
check_nse_holiday_calendar` emails from 15-Dec, generalised to `{next_year}`, and stops when the
file exists. ⛔ **The boot-blocker itself is STILL NOT FIXED and cannot be — only NSE's published
list fixes it.**

⭐⭐ **WHY NO EARLY WARNING EXISTED, AND IT IS A SHAPE WORTH REMEMBERING:** the check built to
catch exactly this **cannot reach it**. `check_config_files_present()` explicitly requires
`nse_holidays_{current_year}.yaml` and records `missing_config_files` as BLOCKING — but it runs
inside `run_all_startup_checks()` at **`main.py:2069`, 253 lines AFTER the `load_all()` at
`:1816`** that already killed the boot. **A downstream check cannot catch an upstream death.**
⭐ **AND THE FIX FOR THAT SHAPE IS A DIFFERENT PROCESS, not an earlier line:** the reminder lives
in the always-on watcher precisely because on 1-Jan the trading service is the thing that is dead.
⚠️ Also: the SAME DATA read two ways in ONE boot has **two opposite failure policies** — the SU6
guard reads the YAML directly and *swallows* the missing file (`main.py:1769`, "proceed with
startup"), while `load_all`'s blanket "all 8 must exist" turns the same absence into a dead
boot. **The file is a HARD boot requirement serving a SOFT purpose.**
⛔ Nothing was changed on the boot path: v45 must stay Tuesday's single variable, so the warning
lives in the SUITE (which runs constantly here) and costs no production code.

**Why it matters beyond the three:** ⭐ **a suite that answers differently on a Saturday than
on a Tuesday makes a WEEKEND baseline non-comparable to a WEEKDAY one — and BASE-vs-MERGE
comparability IS the gate.** A clock-dependent test is not a nuisance; it corrupts the only
regression instrument this project has. [[feedback-no-fixed-test-baseline]]

**How to apply:**
- ⭐ **CONTROL THE INPUT, DO NOT DISABLE THE CHECK.** Pin the clock so the real assertion still
  runs; make the pin **self-verifying** (assert the pinned date is still a trading day) rather
  than trusting a date literal.
- ⚠️ **`core.time_authority` IS NOT THE ONLY CLOCK.** 5 production sites read it directly:
  `config_loader.py:2159`, `holiday_guard.py:78`, `startup_checks.py:863`, `main.py:1718`, and
  the documented exemption `state_store.py:73`. A sweep that patches only `time_authority`
  **misses all five** — that is how the year axis stayed hidden.
- To sweep empirically: run the suite under a simulated calendar (patch `now_ist`/`today_ist`
  in an autouse fixture) at ≥2 weekdays and ≥1 weekend day and **diff the failure SETS**.

Related: [[feedback-no-fixed-test-baseline]] · [[feedback-verify-rc-not-output]] ·
[[service-window-configurable-25jul]] · [[paper-cannot-exercise-class-26jul]]
