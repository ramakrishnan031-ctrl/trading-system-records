---
name: schema-push-overnight-refusal-27jul
description: "An evening schema push makes EVERY heartbeat-writing cron drop a CRITICAL sentinel until the next 08:15 boot migrates the DB. MEASURED 27-Jul on v44->v45. Expected, not an incident."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1651e524-a1a0-427f-84ae-b0f0b833e483
  modified: 2026-07-27T13:39:17.387Z
---

# A schema push in the evening buys a night of CRITICALs — by design

**MEASURED 27-Jul-2026.** v45 pushed 18:17:37; live DB stayed **v44** until the next 08:15:30 boot.
In that window `StateStore.__init__` sees `old_version(44) < EXPECTED_SCHEMA_VERSION(45)` and, for any
opener without `allow_migrate=True`, calls `_refuse_migration` → **writes a CRITICAL sentinel** →
`alert_watcher` emails it (~30 s).

⛔ **`utils/cron_heartbeat.py:84` does `store = StateStore(db_path)` — default `allow_migrate=False`.**
So *every* cron that records a heartbeat trips it.

⭐ **VOLUME — MEASURED ~4 A NIGHT, and I first said ~25.** The correction matters more than the number:
I counted **cron ENTRIES in the window**; only jobs that write a `cron_heartbeat` ROW actually trip it.
`disk_monitor` runs hourly and writes **no** heartbeat, so it never fires. Measured over Fri 24→Mon 27:
**12 rows across 3 nights.** Observed 27-Jul: `system_manager_eod` 18:45:02 · `cron_officer_eod` 18:50:01
· then `backup_retention` ~02:00 · `auto_refresh_token` ~08:15:03. ⛔ **Count the jobs that WRITE the row,
never the crontab lines.**

⚠️ **SECOND-ORDER: the refusal blocks the heartbeat WRITE**, so those jobs have NO `cron_heartbeat` row
for that date — while their WORK ran fine (`data_store/cron_marks/*.done` still written by the crontab
wrapper). ⇒ **for that window the file marks are truthful and `cron_heartbeat` is not.**
✅ **No knock-on alert:** `cron_watchdog` alerts on a MISSING heartbeat for `_WATCHED = (cron_officer_eod,
check_cron_drift)` — which would have arrived under a DIFFERENT title — but it is **NOT SCHEDULED** (absent
from the crontab, verified). Built, never run.

## What this is NOT

⭐ **Not a defect, and not a v45 problem.** It is the 14-Jul migration guard (`ed1c4b9` AC3,
"never a silent skip") working exactly as specified. It had **never fired before** — 0 occurrences
in all VM logs — because v45 is the first schema bump since the guard was added. See
[[migration-on-open-rule-14jul]].

## What is NOT at risk (each verified separately, not assumed)

- **The next boot.** `auto_refresh_token` does `run_refresh()` FIRST; `_heartbeat()` is called after
  and catches everything (`log.warning("...heartbeat_failed")`, exit 0). **The token still refreshes.**
- **`forward_shadow_record`** — the only irreplaceable output. On 27-Jul it wrote at 18:16:26 and the
  deploy landed 18:17:37: it beat it by **71 seconds**. ⚠️ That was luck, not design.

## The rule for next time

⭐ **Before any evening schema push, expect the night of CRITICALs and say so in advance** — the real
cost is that a GENUINE alert is buried among them for one night.
⭐ **Push on a night when the book is FLAT.** 27-Jul was chosen over deferring precisely because
deferring moved the same flood to the night *after* a real overnight CNC position is armed.
⛔ **A pending migration cannot be applied early past 18:15** — the boot guard refuses to START the
service outside `[08:00, 18:15)`, so there is no "just migrate it now" escape. [[service-window-configurable-25jul]]

Probe that measures it safely (sentinel follows `self._db_path.parent`, so a copy in `/tmp` cannot
reach `alert_watcher`): copy the DB, `StateStore(copy_path)`, catch `MigrationNotPermitted`.

## ✅ 28-Jul-2026 — **THE BLAST RADIUS WAS MEASURED. NOTHING IS OWED. THE WINDOW IS CLOSED.**
⭐ *"The alert was right" is a DIFFERENT QUESTION from "what did the refusal cost"* — every one of
those CRITICALs is **a process that did not do its job**, and nobody had asked the second question.

**Window, from the DEPLOY REFLOG (not from memory): OPEN `d3fa5b8` push+`checkout -f`
*27-Jul 18:17:37* → CLOSE *28-Jul 08:15:16.875* (`migration complete: v44 -> v45`).**

**REGENERABLE-or-GONE for every job inside it** (the distinction is the whole point):
- ⛔🥇 **`forward_shadow_record` — NOT in the window.** It ran **18:16, ~71 s BEFORE the deploy**, and
  wrote **3,695 records for 27-Jul — the HIGHEST of any day**. **Nothing lost.** ⭐ **Safe by LUCK,
  not design:** a 3-minutes-earlier push would have destroyed the only out-of-sample evidence
  producer (D3/D4 both depend on it). ⛔ **NEVER produce a missing day manually** — a loss is a gap,
  a manufactured day is a CORRUPTION.
- `system_manager` 18:45 + `cron_officer` 18:50 — **ABORTED** (tracebacks in `logs/system-manager.log`
  / `logs/cron-officer.log`). ✅ **REGENERABLE** — `--date 2026-07-27`, safely via `--dry-run` /
  `--no-soft-kill`. *(This is why the latest EOD report on disk is `2026-07-24.txt`.)*
- `backup_retention` 02:00 + `db_retention` 02:30 — refused. ✅ **Harmless: both are PRUNES**, i.e.
  deletions that did not happen. ⭐ **The BACKUPS THEMSELVES were taken** (`analytics-2026-07-28.db`
  @ 01:05) — those cron jobs use **raw `sqlite3`, not `state_store`**, so they never hit the guard.
- `auto_refresh_token` 08:15:03 — logged `MIGRATION_REFUSED`, ⭐ **but THE TOKEN STILL REFRESHED**
  (`session/zerodha_token.json` dated 28-Jul 08:15). The refusal hit its **heartbeat write, not its
  work.** This is the one that could have cost the whole trading day, and it did not.

⚠️ **IT IS A PROPERTY, NOT AN INCIDENT — v46 WILL DO IT AGAIN.** Registered as **M1** in
`docs/decisions/ACTIONS_not_decisions.md` with two directions (push immediately before an off-market
boot · let non-boot processes DEGRADE rather than abort whole), neither chosen. **Gate: after 4-Aug.**
⛔ **THE THURSDAY S4 CHANGE DOES NOT COVER THIS** — checked, not assumed: S4 is a *webhook self-check
at BOOT*; this is a *non-boot cron* hitting a *schema* guard. Same shape, different path.

## ⚠️ AND THE OBSERVABILITY GAP THIS EXPOSED (registered as **M2**)
**These CRITICALs are NOT in `logs/system_<date>.log`.** Measured: `grep -icE "refus|migrat|schema"`
= **1** on 27-Jul, and all three 28-Jul matches are unrelated. They live in **`logs/cron-officer.log`
and `logs/system-manager.log`**. ⇒ ***the day's error census is NOT a complete count of CRITICALs —
a whole class reaches email and bypasses it.*** ⛔ **"No new CRITICAL in the census" ≠ "no new
CRITICAL."** (It does not confound the 17:40 gate — these cannot land in that log.)
⛔ The Thursday send-side audit trail (`214a878`) would **not** close it either: it records the send
outcome into the **sending process's own log**, which for a cron job is `cron-*.log`.
