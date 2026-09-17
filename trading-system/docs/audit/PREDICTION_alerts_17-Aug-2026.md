# PREDICTION — THE ALERTS UNIT (INSTALL ⑤)

**Written:** 2026-08-17, frozen at **19:05 IST**, ⛔ **BEFORE the push.**
**Unit:** `f62db55d3bb60eabf674ba1867c4f9c3fc8fab86`, branch `fix/alert-phases-0-1-2`.
**Deploys onto:** `origin/main` = `6fa8a1c8019268e2cc54ae8045af29b72f1f1446`, resolved
**at gate time by two independent measures** — VM bare-repo
`git --git-dir=/home/ubuntu/trading-system.git rev-parse refs/heads/main` and PC
`git ls-remote origin main` over the network. ⛔ Not taken from any SHA written earlier
in a card.

## §A — WHAT IS BEING INSTALLED

Three commits, one unit: `58035bf` (Phase 0, the alert delivery contract applied to the
two highest-consequence swallows) → `37336bc` (Phase 1, the contract applied to
feed-death / SOFT_KILL / EOD-deferred) → `f62db55` (Phase 2, the propagation defect in
the watcher's Telegram fallback).

**Nine files, and the diff is byte-identical to the extraction record:** `git diff
6fa8a1c f62db55` = **53,290 B**, md5 **`cc12e920f725308c2ddc8c73b1af40eb`** — the same
bytes as `git diff f963438 071169b`, the original union. ⇒ the rebase onto `6fa8a1c`
preserved the unit exactly; it is ⛔ not a re-authoring.

```
A  alerts/delivery.py          M  capital/kill_switch.py    M  data/live_feed.py
M  main.py                     M  orders/order_placer.py    M  scripts/alert_watcher.py
A  tests/unit/test_alert_delivery_contract.py
A  tests/unit/test_alert_delivery_phase1.py
A  tests/unit/test_alert_delivery_phase2.py
```

**Exactly ONE new production module** (`alerts/delivery.py`); the other three additions
are tests. ⛔ Stating "one new file" would be false — there are four.

**Import risk ELIMINATED, ⛔ not assumed:** `alerts/` is an EXISTING package at
`6fa8a1c` — `alerts/__init__.py`, `critical.py`, `cron_alerts.py`,
`telegram_notifier.py` are all present. `delivery.py` is a new module in an existing
package, ⛔ not a new namespace package.

## §B — THE PRESENCE SIGNATURE, AND ITS CONTROL

🔑 **Signature: the log event string `alert_send_caller`.** It is `_EVENT` in
`alerts/delivery.py:50`, emitted by `_emit()` and reached through
`send_alert_recorded()`.

**The control was measured BEFORE the push and could have come back the other way:**

| where | occurrences of `alert_send_caller` |
|---|---|
| the `6fa8a1c` tree (what is deployed now) | **0** |
| the `f62db55` tree | **1 file** — `alerts/delivery.py`, and nothing else |
| VM deployed source, `grep -rl --include=*.py` | **0** |
| VM `logs/system_2026-08-17.log` | **0** |
| VM `logs/` — every file | **0** |

⇒ **The current build cannot produce this string.** Its appearance is therefore
attributable to this install and to nothing else.

## §C — ⛔ THE CEILING, STATED HONESTLY AND BEFORE THE PUSH

🔴 **NO RUNTIME SIGNATURE CAN FIRE TONIGHT. This is a real limit, ⛔ not a hedge.**

- The trading service is **down** (`eod_self_exit` 17:35:00.002) and ⛔ must not be
  started. Its four call sites (`main.py`, `capital/kill_switch.py`, `data/live_feed.py`,
  `orders/order_placer.py`) therefore cannot execute before the **18-Aug 08:15 boot**.
- 🔴 **`alert-watcher` is `active`/`running`, MainPID `2562355`, started
  `Sat 2026-08-01 06:17:50 IST` — 16 days.** The post-receive `checkout -f` replaces
  `scripts/alert_watcher.py` on disk, but that process has already loaded the old module
  and ⛔ **keeps running the OLD code.**
  ⇒ **PHASE 2's FIX IS NOT LIVE AFTER THIS PUSH**, and ⛔ it will NOT become live at
  tomorrow's 08:15 boot either — the trading service's boot does not restart
  `alert-watcher`. It requires its own restart, which is ⛔ NOT authorised tonight.
  ⭐ **Therefore this install delivers Phases 0+1 into the trading process at the next
  boot, and Phase 2 into a file that nothing is executing.** That is the honest scope.

⇒ **Tonight's evidence ceiling is DEPLOY-TIME ONLY:** file presence, md5 identity
PC==VM, and deployed-tree == HEAD. **`VERIFIED LIVE` is NOT available tonight** and will
⛔ not be claimed. `NOT TESTED` and `CANNOT DETERMINE` are available verdicts.

## §D — FALSIFIERS

| # | FIRES IF | source |
|---|---|---|
| **G1** | after the push, `origin/main` ≠ `f62db55` by either independent measure | VM `rev-parse` + PC `ls-remote` |
| **G2** | `alerts/delivery.py` is ABSENT from the VM deployed tree `/home/ubuntu/systems/trading-system` | `ls` / `md5sum` on the VM |
| **G3** | any of the 9 files differs PC vs VM by md5 | `md5sum` both sides |
| **G4** | the VM deployed tree shows tracked drift vs the new HEAD | `git --git-dir=… --work-tree=… status --porcelain` |
| **G5** | the 18-Aug 08:15 boot fails to reach `active`, or exits non-zero | `systemctl show` |
| **G6** | the 18-Aug boot logs `ImportError`/`ModuleNotFoundError` naming `alerts.delivery` | `logs/system_2026-08-18.log` |
| **G7** | the 18-Aug 18:45 `system_manager` names any of the 9 files as deployed-tree drift | `logs/system-manager.log` |
| **G8** | `alert_send_caller` appears in a VM log **tonight**, before the 08:15 boot | ⭐ would REFUTE §C's ceiling — a welcome falsifier, ⛔ not expected |

**G1–G4 are scoreable tonight. G5–G7 are `NOT TESTED` until 18-Aug. G8 is expected NOT
to fire, and if it does, §C was wrong.**

⛔ **WHAT THIS PREDICTION DOES NOT CLAIM.** It does not claim the alert contract works —
only that the code is installed. It makes no claim about Phase 2's behaviour, which
nothing will execute. It makes no claim about any file outside the nine. It does not
claim the unit is reversible in effect: the code is revertible to `6fa8a1c`, but any
alert already suppressed or delivered differently is a produced effect, ⛔ not undone by
a revert.

<!-- FROZEN-BOUNDARY — everything ABOVE this line is FROZEN. ⛔ No edit above it, especially if a call turns out wrong. Addenda go BELOW, appended only, each with its own timestamp. -->

## ADDENDA (append-only, below the boundary)

### ADDENDUM 1 — 2026-08-17, PUSH EXECUTED 19:06 IST, SCORED 19:07:24 IST

**PUSHED.** `git push origin f62db55:refs/heads/main` → `6fa8a1c..f62db55  f62db55 -> main`,
rc=0. ⛔ Explicit refspec, ⛔ never `git push origin main`, ⛔ no `--force`. post-receive
reported *"Deploying main to /home/ubuntu/systems/trading-system… Already on 'main'…
crontab AUTO-INSTALLED from canonical… Deployment complete."*
**Rollback point = `6fa8a1c`**, the value measured at gate C by two independent means.

| # | verdict | evidence |
|---|---|---|
| **G1** | ✅ **DID NOT FIRE** | `origin/main` = `f62db55d3bb60eabf674ba1867c4f9c3fc8fab86` by **both** measures — VM bare `rev-parse` and PC `ls-remote` |
| **G2** | ✅ **DID NOT FIRE** | `/home/ubuntu/systems/trading-system/alerts/delivery.py` present, **5,960 B**, mtime `Aug 17 19:06` — matches the blob's byte count exactly |
| **G3** | ✅ **DID NOT FIRE** | **9/9 md5 MATCH**, PC == VM. PC side read from the **ref's blobs** (`git show f62db55:<f>`), ⛔ never worktree files — the root worktree is on another branch and dirty |
| **G4** | ✅ **DID NOT FIRE** | deployed HEAD = `f62db55…`; `status --porcelain --untracked-files=no` = **EMPTY** ⇒ zero tracked drift |
| **G5** | ⏳ **NOT TESTED** | needs the 18-Aug 08:15 boot |
| **G6** | ⏳ **NOT TESTED** | needs the 18-Aug 08:15 boot |
| **G7** | ⏳ **NOT TESTED** | needs the 18-Aug 18:45 `system_manager` |
| **G8** | ✅ **DID NOT FIRE** | `alert_send_caller` = **0** across every file in `logs/` ⇒ ⭐ **§C's ceiling is CONFIRMED BY MEASUREMENT, ⛔ not merely asserted** |

**THE 9 md5 VALUES, PC == VM:** `alerts/delivery.py` `7282e50f30ab…` ·
`capital/kill_switch.py` `3fa519a1309b…` · `data/live_feed.py` `af3aeece4baf…` ·
`main.py` `f8aec8df915b…` · `orders/order_placer.py` `c337d5c3bb5a…` ·
`scripts/alert_watcher.py` `13efd70786bd…` · `test_alert_delivery_contract.py`
`f106fd2de538…` · `…phase1.py` `0205e09da168…` · `…phase2.py` `40da1b19c051…`.

**SERVICE NOT STARTED, as required.** `ActiveState=inactive` · `SubState=dead` ·
`MainPID=0` · `NRestarts=0` · `ExecMainExitTimestamp` still `Mon 2026-08-17 17:35:04
IST` — unchanged across the push. ⛔ Nothing was started, restarted or resumed.

🔴 **§C's PHASE-2 GAP IS NOW MEASURED, ⛔ NOT PREDICTED.** After the push,
`alert-watcher` reports **`MainPID=2562355`, `ExecMainStartTimestamp Sat 2026-08-01
06:17:50 IST`** — byte-for-byte the same process as before the push. The new
`scripts/alert_watcher.py` (md5 `13efd70786bd…`) is on disk and **nothing is executing
it.** ⇒ **Phases 0+1 will enter the trading process at the 18-Aug 08:15 boot; Phase 2
enters nothing until `alert-watcher` is restarted, which is ⛔ not authorised tonight and
⛔ does not happen at the trading service's boot.**

**STATUS: `DEPLOYED`. ⛔ NOT `VERIFIED LIVE`** — no production artefact of this code
executing exists, and by §C none can exist before the 18-Aug 08:15 boot.

### ADDENDUM 2 — 2026-08-17, RAMA'S RULING ON ACTIVATION + THE CLASS MEASUREMENT

**RULING, QUOTED:** *"Accept Phase 2 as dormant tonight — no restart. But record the
plan, not just the state: alert-watcher gets restarted TOMORROW MORNING right after the
08:15 boot, so Phases 0+1 (which enter the trading process at that boot) and Phase 2 all
become live on the same day. ⭐ Splitting activation across two days would make
tomorrow's G5/G6/G7 scoring un-attributable — some falsifiers live, others dormant, one
unit."*

**THE PLAN, OWED TOMORROW (18-Aug), IN ORDER:** ① let the 08:15 boot run — it activates
Phases 0+1 inside the trading process ② **immediately after the boot is confirmed
healthy, restart `alert-watcher`** — this activates Phase 2 ③ then score G5/G6/G7 against
a build in which **all three phases are live**. ⛔ Do NOT score G5/G6/G7 with Phase 2
still dormant: one unit half-active makes every verdict un-attributable. ⛔ No restart
tonight; the service stays down and the watcher keeps its 01-Aug process.

**`alert-watcher` UNIT POLICY, MEASURED:** `Id=alert-watcher.service` ·
**`UnitFileState=enabled`** (`UnitFilePreset=enabled`) ⇒ it starts at VM boot and
persists across trading days, which is why one process has spanned 16 of them ·
**`Restart=on-failure`**, `RestartPreventExitStatus=` empty, `NRestarts=0` ⇒ ⭐ a CLEAN
exit is NOT auto-restarted, so `systemctl restart alert-watcher` is the deliberate
gesture and it will come back · `ExecStart=/home/ubuntu/systems/venv/bin/python
/home/ubuntu/systems/trading-system/scripts/alert_watcher.py --loop` ·
`WorkingDirectory=/home/ubuntu/systems/trading-system`. ⛔ `RestartSec` was not returned
by the query and is therefore **NOT MEASURED**, ⛔ not assumed.

## 🔑 THE CLASS MEASUREMENT — THE HYPOTHESIS'S PREMISE IS **REFUTED**

**QUESTION PUT:** how many deploys since 01-Aug 06:17:50 touched
`scripts/alert_watcher.py`? *"If the answer is more than zero, that is a
DEPLOYMENT-LEVEL configured-not-covered defect."*

**ANSWER: ZERO. Proven three independent ways.** ① `git log --since='2026-08-01 06:17:50
+0530' 6fa8a1c -- scripts/alert_watcher.py` = **0 commits** ② **0** distinct blob
versions across that span ③ **blob identity** — the file at the commit deployed when the
watcher started (`fa7c45c`) is `da21f00ce00e9cd563f8ab53f1f38719221f1f0f`, and the blob
at `6fa8a1c` is **the same SHA**; it changes only at `f62db55`
(`d8e39f359656696c26e06e0049157fe13a187d5e`).

**PROBE VERIFIED — it could have come back non-zero.** Unbounded, the same query returns
`f62db55`, `5311fe6` and `c405c30` for this file. ⇒ the zero is a measurement, ⛔ not a
broken filter.

⇒ ⛔ **THE DEPLOYMENT-LEVEL DEFECT IS NOT DEMONSTRATED. Tonight is INSTANCE #1, ⛔ not the
latest of many.** ⭐ The honest statement: **the structural gap is real and has simply
never been activated before**, because nothing had changed the file since the process
started.

🔴 **BUT THE CLASS IS WIDER THAN THE ONE SERVICE — THREE long-lived units run code out of
the deployed tree, and none is restarted by the `post-receive` hook or by the trading
service's boot** *(width: every `running` service on the VM, `ExecStart` filtered for
`systems/trading-system` or `systems/venv`)*:

| unit | runs | started | deploys touching its files since |
|---|---|---|---|
| `alert-watcher.service` | `scripts/alert_watcher.py --loop` | 01-Aug 06:17:50 | **0** |
| `gui-dashboard.service` | `ops_dashboard/…` under its OWN venv | 14-Aug 20:50:57 | **0** |
| `token-watcher.service` | `deploy/token_watcher.sh` (bash) | 28-Jul 06:02:38 | **0** |

**All three ZERO ⇒ the class has never been exercised either.** ⭐ Two things follow that
matter more than tonight: **(a) `gui-dashboard` is the one to watch** — every pending
Screen unit (`d031ed6` and the 20/21/22 work) lands in `ops_dashboard/`, so a GUI deploy
without a `gui-dashboard` restart ships screens that do not appear. ⚠️ Its 14-Aug 20:50
start is AFTER that night's 19:33 push, so it *has* been restarted post-deploy at least
once — ⛔ whether that is a standing practice or a coincidence is **NOT MEASURED**.
**(b) `token-watcher` is a BASH script, and its failure mode would be different and
worse** — bash re-reads a script by byte offset, so replacing it mid-run can execute
garbage rather than merely stale code. ⛔ Mechanism INFERRED, ⛔ never exercised here
(0 deploys), ⛔ recorded as a caution, not a finding.

⛔ **MEASURED, ⛔ NOT FIXED. No restart performed. No hook changed.**

### ADDENDUM 3 — 2026-08-18, THE 08:15 BOOT + THE `alert-watcher` RESTART, SCORED 09:15 IST

**ADDENDUM 2's PLAN WAS EXECUTED IN ORDER, AND ONLY THEN WAS ANYTHING SCORED.** ① the
08:15 boot ran unaided ② it was confirmed healthy and REPORTED before anything else was
touched ③ `alert-watcher` was restarted **ONCE, by Rama**, at `09:11:21` ④ G5/G6/G7
scored against a build in which all three phases are **LOADED**. ⛔ No falsifier was
scored with Phase 2 still dormant.

**🔑 §C's PHASE-2 CLAIM IS NOW CONFIRMED POST-BOOT, ⛔ NOT MERELY PREDICTED.** §C said the
fix "will ⛔ NOT become live at tomorrow's 08:15 boot either — the trading service's boot
does not restart `alert-watcher`." **Measured 09:03:21, 48 minutes AFTER the 08:15:31
boot: `alert-watcher` was still `MainPID=2562355`, `ExecMainStartTimestamp Sat 2026-08-01
06:17:50 IST`** — the boot passed straight over it. ⭐ The call was right, and it was
right for the stated reason.

**THE BOOT.** `trading-system.service` `ExecMainStartTimestamp = Tue 2026-08-18 08:15:31
IST` · `MainPID 3933620` · `ActiveState=active` / `SubState=running` · `NRestarts=0` ·
`Result=success` · `ExecMainStatus=0` · `ExecMainExitTimestamp` **empty**. Re-read
09:13:45 — same PID, still transacting (`get_margins` `net=10611.0` at 09:02:04). Nine
preflight checks all `OK`. Prior-day `SOFT_KILL` auto-cleared `08:15:32.337`;
`kill_switch_state` now `INACTIVE`, `triggered_by=main.auto_clear_stale` (read `mode=ro`).

**THE RESTART — OLD PID → NEW PID, AND IT IS MANUAL.**

| | before (09:03:21) | after (09:11:49) |
|---|---|---|
| `MainPID` | **2562355** | **3938122** |
| `ExecMainStartTimestamp` | `Sat 2026-08-01 06:17:50 IST` | **`Tue 2026-08-18 09:11:21 IST`** |
| `/proc/<pid>` | — | old **gone**; new `cwd -> /home/ubuntu/systems/trading-system`, `PPID 1` |
| state | active / `NRestarts=0` | **active·running** / `NRestarts=0` / `Result=success` |

⛔ `active` alone was NOT relied on — a process that never died is also `active`. The old
PID's `/proc` entry is **gone**, the PID differs, and the start timestamp moved 17 days.
⭐ The restart is **manual and deliberate**: no `post-receive` hook and no trading boot
performs it. Confirmed structurally — `/home/ubuntu/systems/trading-system` has **no
`.git`**; it is a bare-repo checkout target, so the hook writes files and stops there.

## G5 · G6 · G7 — SCORED SEPARATELY, EACH BY ITS OWN SIGNATURE

| # | verdict | signature | evidence |
|---|---|---|---|
| **G5** | ✅ **DID NOT FIRE** | the 18-Aug 08:15 boot fails to reach `active`, or exits non-zero | reached `active`/`running` `08:15:31`; `ExecMainStatus=0`; `Result=success`; `NRestarts=0`; `ExecMainExitTimestamp` empty; same `MainPID 3933620` at 09:15 |
| **G6** | ✅ **DID NOT FIRE** | the 18-Aug boot logs `ImportError`/`ModuleNotFoundError` naming `alerts.delivery` | 0 across **two** search widths, plus a POSITIVE import proof — below |
| **G7** | ⏳ **NOT TESTED** | the 18-Aug 18:45 `system_manager` names any of the 9 files as deployed-tree drift | **its window had not arrived at 09:15** — below. ⛔ NOT a pass |

**G5 — FALSIFIABILITY PROVEN, ⛔ not asserted.** This exact unit produced G5's red
condition **eight days ago**: `Aug 10 08:15:25 trading-system.service: Main process
exited, code=exited, status=3/NOTIMPLEMENTED` → `Failed with result 'exit-code'`. ⇒ the
same `systemctl show` that reads green today read red on 10-Aug. ⭐ **A green check is
evidence only if it could have been red; this one could.**

**G6 — THE SIGNATURE'S OWN WIDTH IS TOO NARROW, AND THAT IS RECORDED RATHER THAN
GLOSSED.**

- ① the file the signature names: `grep -cE "ImportError|ModuleNotFoundError"
  logs/system_2026-08-18.log` = **0**; `alerts[._]delivery` in that file = **0**.
- ② 🔴 **a `ModuleNotFoundError` at import time crashes BEFORE the JSON logger exists**,
  so it would land on **stderr in `journalctl`**, ⛔ never in that file — the signature as
  written could have missed its own target. Width widened:
  `journalctl -u trading-system.service --since "2026-08-18 08:00"` grepped for
  `ImportError|ModuleNotFoundError|Traceback` = **0**.
- ③ ⭐ **POSITIVE, not merely absent.** All four Phase-0/1 call sites import the module at
  **column 0, module-level, unguarded** — `main.py:41`, `capital/kill_switch.py:110`,
  `data/live_feed.py:22`, `orders/order_placer.py:235`. A failed import could not have
  been survived; the process reached `active` and ran nine preflight checks. And
  `alerts/__pycache__/delivery.cpython-312.pyc` was **created at `08:15:31.659`** — inside
  the boot second — from a source (`alerts/delivery.py`, mtime `17-Aug 19:06:02`) that did
  not exist when any earlier process started. ⇒ **the trading process compiled and
  imported `alerts.delivery`.** That is rung ② for Phases 0+1, from a second direction.

**G7 — NOT TESTED, AND THAT IS A MEASUREMENT.** `logs/system-manager.log`'s last entry is
`2026-08-17 18:45:07.721`, reading *"deployed tree == HEAD (6fa8a1c) — no tracked drift"*
— the **pre-push** run. There was no 18-Aug entry at 09:15. ⛔ A falsifier whose window
has not arrived is `NOT TESTED`, ⛔ never a pass.

⚠️ **LEADING INDICATOR ONLY, labelled as such:** at 09:15:03 the deployed tree reads HEAD
`f62db55d3bb60eabf674ba1867c4f9c3fc8fab86`, `status --porcelain --untracked-files=no` is
**EMPTY**, and each of the nine unit files individually reports clean. ⛔ **Different
tool, different clock, different question — it does NOT substitute for the 18:45 run, and
G7 stays open until that run exists.**

## 🔴 THE CEILING MOVED ONE RUNG, ⛔ NOT TWO

**The §B presence signature has NOT fired.** `alert_send_caller` = **0** across **every
file under `logs/`** at 09:15 — and that is the right width: `alerts/delivery.py:_emit`
writes it via `log.<level>(_EVENT, extra=fields)`, i.e. through the module logger, which
lands in `logs/`. ⇒ **no alert has traversed the contract today, in either process.**

⭐ **THE HONEST STATUS, and the words are chosen: Phases 0+1 are LOADED into the trading
process; Phase 2 is LOADED into `alert-watcher`. ⛔ NOT `VERIFIED LIVE`** — no production
artefact of this code *executing* exists. ⛔ **"alerts live" is NOT written.** Rung ③ was
⛔ **NOT manufactured**: reaching it needs a real SMTP failure with pending sentinels, and
⛔ none was induced.

**RUNG ② FOR PHASE 2 — THE METHOD, NAMED.** ① `scripts/alert_watcher.py` md5
`13efd70786bd7ed112c3801545ad5e99` (35,950 B) and `alerts/delivery.py` md5
`7282e50f30abc6ccada939c65d11b1b5` (5,960 B) **identical before and after** the restart
⇒ the bytes hashed are the bytes on the path at exec ② `__main__` has **no bytecode
cache**, so CPython compiles the entry script from disk every exec — there is no
stale-pyc path for it ③ `alert_watcher.py:61` is `from alerts.delivery import
send_alert_recorded` at **column 0, unguarded**; the 01-Aug file had no such line
④ 🔑 **the observation that closes it — the new process wrote its own log AFTER that
import ran:** `logs/alert_watcher_2026-08-18.log`, created `09:11:21.596`, containing
`--loop mode (interval=60s, heartbeat=off)` and `No pending sentinels found.` Logging is
configured inside `main()`, which runs after every module-level import; a process that
died at line 61 could not have written those lines ⑤ PEP-552 header of
`delivery.cpython-312.pyc`: magic `cb0d0d0a` == interpreter magic, `flags=0` (timestamp
invalidation), header source-mtime `1786973762` == on-disk `1786973762`, header
source-size `5960` == on-disk `5960` ⇒ the bytecode is provably derived from the deployed
source bytes.

## NEW FINDING — LATENT, ⛔ MEASURED NOT FIXED: the date-embedded watcher log is defeated by `--loop`

The dying process's **last write, `09:11:21.238`, went to
`logs/alert_watcher_2026-08-01.log`** — a file named for the day it *started*, **17 days
stale, 1.4 MB**. The new process opened `logs/alert_watcher_2026-08-18.log`. The
date-embedded filename (`5311fe6`, F4/hygiene) is computed **once at process start**;
`--loop` (`34c2993`, q5/P5) then makes the process outlive its own filename. ⭐ **Same
shape one file earlier:** `alert_watcher_2026-07-28.log` stops at `2026-08-01 06:17:50`,
the instant the 01-Aug process replaced the 28-Jul one. ⇒ **the two fixes defeat each
other whenever the watcher is long-lived**, which per ADDENDUM 2 is 16-17 days at a time.
⛔ Observability plane, no capital path ⇒ **LATENT: documented and continued, ⛔ not
repaired today.** ⚠️ It also means *"grep today's watcher log"* is an unreliable probe on
any day the watcher was not restarted — a **method** hazard, not merely a cosmetic one.

## CORRECTION TO A PRIOR RECORD — the 02-Aug allowlist entry is STALE

The 02-Aug allowlist finding records the one `sudo` attempt as **DENIED x2**. **Measured
18-Aug 09:03 on `trading-vm`: `sudo -n true` returns rc `0`** — passwordless sudo is
available to the agent account for at least that command. ⛔ **NOT probed further** and
⛔ **not used**; the restart remained Rama's, executed by Rama. ⭐ Recorded because a
stale permission record means an earlier session concluded something about this system
that is **no longer true** — the conclusion, not just the value, has expired.

⛔ **G1-G4 and G8 are untouched — already scored in ADDENDUM 1 and ⛔ not re-litigated
here.** ⛔ Nothing above the FROZEN-BOUNDARY line was edited; this addendum is appended
only.
