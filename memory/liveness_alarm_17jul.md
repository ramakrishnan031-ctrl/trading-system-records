---
name: liveness-alarm-17jul
description: "Liveness alarm BUILT + DEPLOYED 17-Jul: trading-system can no longer die silently. The canary NEVER watched this unit at all (it watches alert-watcher + gui-dashboard) — correcting my own S4 report. Proven on the real box against the real outage."
metadata:
  node_type: memory
  type: project
  originSessionId: 8ce14ca5-df4a-451f-aa35-493d91436ae9
---

**🚨✅ LIVENESS ALARM DEPLOYED 17-Jul** — `6a4c092`, tag **`deploy-17jul-liveness`**;
PC == VM bare == `1a43b5e`. `scripts/liveness_probe.py` + `tests/unit/test_liveness_probe.py`
+ a `cron_registry.yaml` entry. Report `docs/audit/liveness_alarm_17jul2026.md`.
Closes S4 follow-up #3 ([[s4-boot-outage-17jul]]).

## What it does
Cron **`*/5 9-15 * * 1-5`** (`market_day_only: true`, `cadence: intraday`, **`monitored: false`**
— the `capture_metrics` precedent; a 5-min job can't be heartbeat-expected). During
**[09:00, 16:00) on a trading day**, if `trading-system.service` is not active and the operator
did not park it ⇒ **ONE CRITICAL** (Telegram → CRITICAL-sentinel F1 fallback = the canary's exact
delivery contract). Log `logs/cron-liveness.log`.

## ⭐ THE FINDING — it corrected my OWN S4 report
My S4 report said the canary *"watches restart-loops, not liveness, so a cleanly-dead service
scores the good value"* — implying it **looked at** trading-system and misjudged it. **It never
looked at all.** `check_service_respawn`'s unit defaults to **`alert-watcher.service`**
(`monitoring_canary.py:220`), `check_dashboard`'s to **`gui-dashboard`** (`:124`), and
`run_canary` mentions `trading-system` **nowhere** ⇒ the `{"nrestarts": 0}` was **alert-watcher's**
count. **Nothing had EVER watched this unit's liveness.** Corrected in the report; pinned by
`test_old_canary_would_not_have_caught_it`. And restart-counting could never have caught it:
`Restart=on-failure` + a **clean exit 0** ⇒ `NRestarts` stays **0** = the *healthy* value.

## The window — [09:00, 16:00), both bounds reasoned
- **Upper = 16:00 is EXACT**: `main._eod_self_exit_due` returns `(False,-1)` **without querying**
  before `window_end` ⇒ the service **never** self-exits before 16:00 (at 15:59 it must be up).
  == `main.SERVICE_WINDOW_END`, **drift-guarded** by `test_window_end_matches_main`.
- **Lower is deliberately NOT `SERVICE_WINDOW_START` (08:00)**: 08:00 is when it MAY start, not
  when it MUST be up (08:15 token cron → token-watcher → ~08:30 premarket) ⇒ alarming at 08:00
  would be a **guaranteed daily false alarm**. 09:00 clears every start path, 15 min before the
  09:15 open, an hour before the 10:00 entry window.

## The false-alarm matrix (Q3, the crux)
| State | Detected by | Verdict |
|---|---|---|
| holiday/weekend | `utils.holiday_guard.is_trading_day` (S1 authority), **fail-open** | SILENT |
| operator park | `kill_switch_state.state IN ('SOFT_KILL','HARD_KILL')` | SILENT |
| outside window | in code **and** in the cron expression | SILENT |
| unit active | `ActiveState=active` | SILENT |
| **unexpected death** | inactive + trading day + in-window + no marker | **ALARM** |

- **⚠️ A deliberate `systemctl stop` is NOT distinguishable from a silent death** — both leave
  `Result=success`/`ExecMainStatus=0` (today's outage WAS a clean exit 0, via
  `_shutdown_event.set()`). ⇒ **it alarms, honestly** (a missed death costs a session; a false
  alarm costs a message). **Bounded**: the operator already has the documented way to signal
  intent — **park it with a SOFT_KILL** (the 16-Jul "planned pause … no trading issue,
  by=operator" shape), which the probe honours.
- **⭐ SILENCE IS UNBUYABLE**: an unreadable `kill_switch_state` → `UNKNOWN`, deliberately **NOT**
  in the suppression set (a corrupt DB can't mute a real death); an unreadable `systemctl`
  **ALARMS** rather than going quiet.
- **Fail-open direction CHECKED, not inherited**: for the S1 token job fail-open = *run* (never
  starve a trading day); here it = *alarm on a weekday holiday if the calendar is unreadable* —
  same asymmetry, same direction. Uses `is_trading_day` directly, **not**
  `skip_if_non_trading_day` (which writes a SKIPPED heartbeat per call ⇒ ~84 rows/day at this
  cadence).

## Design decisions worth keeping
- **SIBLING probe, not an extended canary**: the canary does an **SMTP login + Telegram getMe
  every run** ⇒ at 5-min cadence that hammers both ~84×/day. Different cadence, different job.
  **Infra IS reused** (delivery contract, cron registry, S1 calendar, and the canary's own
  `_parse_systemctl_show`/`_load_service_state`/`_save_service_state`) — no parallel stack.
- **⭐ It does NOT import `main.py`** — a monitor must not depend on the health of what it
  monitors, or it dies exactly when the system breaks. Window constants duplicated; the **suite**
  owns the drift (`test_window_end_matches_main`), not the runtime.
- **DEDUP = the unit's `InactiveEnterTimestamp`** (a natural incident id, and the "since" the
  operator needs): ~84 probes → **1** alarm; a *distinct* later death alarms **again**; no
  timestamp ⇒ degrades to **≤1/day**, never 1 per probe.
- The alarm names the smoking gun: `Result=success ExecMainStatus=0` ⇒ "**shut itself down
  cleanly, not crashed**" — the detail that points straight at a boot self-check.

## ⭐ The S4 fixture lesson, applied to itself
The matrix tests inject a runner — **the very pattern that hid S4**. So
**`test_default_runner_shells_out_to_systemctl`** pins the PRODUCTION default at the real
boundary (`subprocess.run`): asserts the argv is `systemctl show … trading-system.service …
ActiveState` and that the output is genuinely **parsed** (`props["ActiveState"]=="inactive"`),
not defaulted. Without it a refactor to an assume-healthy stub would leave every other test green
while the probe is blind.
**Mutation-checked** ([[feedback-verify-rc-not-output]]): a probe that can never alarm ⇒ **7 tests
RED**; restored ⇒ **21 pass**.

## ✅ PROVEN ON THE REAL BOX (not a fixture)
The system was still down, so the DEPLOYED probe was pointed at it — **real systemctl, real NSE
calendar, real `kill_switch_state`** — with only `now` moved in-window, calling the *decision*
function (not `main()`) so no alarm was sent:
`09:00 → DOWN` since the **real** `Fri 2026-07-17 08:16:09 IST` · `09:05 → ALREADY_ALARMED` ·
real-now → `OUTSIDE_WINDOW`. **rc=0. It would have caught today at 09:00.**

## Deploy
Regression **11F/4875P/4skip rc=1** (out-of-window known set; **4854+21=4875** reconciles),
**0 attributable PROVEN** (failure set **byte-identical** to the pre-liveness run + none of the
failing suites reference `cron_registry`/the crontab). **⚠️ THIS DEPLOY CHANGED THE CRONTAB**
(48→49 non-comment lines) — **registry == canonical == live all agree on the VM**; `--selftest`
48/48. Schema v44 no-migration. Monitoring-only (reads systemd/calendar/kill-state) — **no
capital/kill/order/signal runtime touched**; parity free (0 mode refs).
**Rollback** = revert `6a4c092` (the cron entry goes with it; the hook reinstalls from canonical).

## Limitations (stated, not hidden)
1. an operator `systemctl stop` **without** a kill marker alarms (indistinguishable — see above);
2. **08:00–09:00 is unwatched** — a death there is caught at 09:00, the price of never
   false-alarming on the boot chain (still an hour before entries);
3. **after 16:00 is unwatched** (a clean exit is legitimate there);
4. it proves the unit is **active**, not that it is trading correctly — a wedged-but-running
   process is the canary's/Officer's territory, not this.

Related: [[s4-boot-outage-17jul]] [[p3s14-done-17jul]] [[feedback-verify-rc-not-output]]
[[feedback-verify-the-finding-premise]] [[killswitch-autoclear-prior-day]] [[pc-test-env-hygiene]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 360 B (budget 300 B). The index now carries a hook and this link.

- 🚨✅🚀 **[LIVENESS ALARM DEPLOYED 17-Jul](liveness_alarm_17jul.md)** — `scripts/liveness_probe.py` cron `*/5 9-15 * * 1-5`: unit inactive in **[09:00,16:00)** on a trading day + not parked ⇒ ONE CRITICAL. ⚠️ a `systemctl stop` == a death (both exit 0) ⇒ park with SOFT_KILL. **⭐ the canary NEVER watched this unit.** [[liveness-alarm-17jul]]
