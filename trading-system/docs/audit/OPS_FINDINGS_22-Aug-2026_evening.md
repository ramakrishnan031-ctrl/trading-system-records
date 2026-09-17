# DEPLOY DOES NOT INSTALL UNIT FILES · security-watcher ANSWERED · THE ALERT GUARD RE-SCOPED

**22-Aug-2026 (Saturday) evening, IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

🏷️ **STATUS: `RECORDED · ⛔ NOTHING APPLIED · ⛔ NO CODE · ⛔ NO VM WRITE · ⛔ NO PUSH · ⛔ NO DEPLOY`.**
Every VM interaction was read-only (`cat`, `ls`, `sed -n`, `grep`, `md5sum`,
`systemctl cat`, `systemctl show`, `journalctl`). ⛔ No `sudo`. ⛔ No process was
started, stopped or restarted. ⛔ OPS ② was **not** applied.

---

## §0 — WC-PATTERN #9, RECORDED

> ⛔ **Web Claude attributed a pre-existing defect to the change that made it easier to reach.**

The card wrote *"this pass increased exposure to a known, unfixed defect"* and framed the
coupling as something F1 created. `main.py:1862` at `4568385` wraps `load_all` in
`try/except Exception` → `return 5`, which has always caught **any** config failure; there
are **four** `exit 5` sites (`:1862`, `:1753`, `:1559`, `:1562`). The crash-loop has been
live and unfixed for as long as they have existed.

⭐ The accurate statement: F1 + NI-4 widen the **aperture** — from *a malformed config
file* to *a missing or null value in any of seven delivery keys*, i.e. from a rare event to
**a routine human error**. ⇒ O-3 is **overdue**, ⛔ not newly created, and none of this
argues against fail-closed.

---

## §1 — 🔴 STANDING OPERATIONAL HAZARD: **DEPLOY DOES NOT INSTALL UNIT FILES**

### The hazard

Deploy is a `post-receive` git checkout from `/home/ubuntu/trading-system.git/` into
`/home/ubuntu/systems/trading-system/`. **It never touches `/etc/systemd/system/`.**

- ⛔ **Every service-file change is a MANUAL act on the VM, forever.**
- ⛔ **The repo copy `deploy/systemd/*.service` is DOCUMENTATION — it is NOT the source of
  truth for runtime behaviour.**
- 🔴 **A future reader who edits the repo copy and pushes will believe they changed the
  restart policy. They will be wrong, and nothing will tell them.**
- ⚠️ **The drift is currently harmless and MUST be re-measured, ⛔ never assumed, any time a
  directive changes.**

### Measured today

| | md5 | note |
|---|---|---|
| installed `/etc/systemd/system/trading-system.service` | `136a4e88774fb5d2f392688a2ce40d3e` | 1411 B, **18-Jun 16:35** |
| repo `deploy/systemd/trading-system.service` @ `4568385` | `e24b88493bc5cdd7ff7753479a73a8dc` | the deployed tree's copy |

The diff is **two COMMENT lines** (the exit-4 note, added in git and never re-installed).
Every **directive** is identical — ⭐ **that is luck, ⛔ not a mechanism.** Nothing in the
system compares them.

### 🔴 A SECOND GAP, FOUND WHILE LOOKING FOR THE FIRST — **DROP-INS ARE NOT INTEGRITY-WATCHED**

`scripts/security_monitor.py:213-224` already hashes the installed unit every ~61 s at
**CRITICAL** severity:

```python
{"path": "/etc/systemd/system/trading-system.service",  "severity": "CRITICAL", "label": "unit_trading"},
{"path": "/etc/systemd/system/security-watcher.service","severity": "CRITICAL", "label": "unit_security"},
```

⚠️ **The watch list is 8 explicit FILE paths — no directories, no globs.** So
`/etc/systemd/system/trading-system.service.d/` is **not watched at all**:

- the **existing** `watchman.conf` drop-in is unwatched;
- **any new drop-in — including the OPS ② one I recommended — would change the restart
  policy of the live trading service without tripping the CRITICAL integrity check.**

🔴 **This slightly revises the OPS ② recommendation.** The drop-in is still the right shape
(rollback is `rm` + `daemon-reload`, and it leaves the 18-Jun unit untouched), **but it
lands in an unmonitored location.** The in-place edit is the opposite trade: it *is*
watched, so applying it would fire a CRITICAL file-integrity alert — correct behaviour,
but the baseline then has to be re-blessed.

⇒ ⭐ **Recommendation, unchanged in shape and extended: take the drop-in, AND add
`/etc/systemd/system/trading-system.service.d/` to `_default_watched_files()`.**
⛔ **PREPARED, NOT DONE** — that is a code change and this card forbids code.

### Where a DRIFT check would belong, and what it would cost

⚠️ First, a distinction that matters, because the two are easy to conflate:

| | check | exists? |
|---|---|---|
| **(A) INTEGRITY** — did the installed file change from its own stored baseline? | `security_monitor.py` file-integrity, CRITICAL, ~61 s | ✅ **exists** (gap: drop-ins, above) |
| **(B) DRIFT** — does the installed file still match the REPO copy? | — | ⛔ **does not exist. This is the §1 finding.** |

**Best home for (B): `scripts/preflight/checks/services.py`.** It is already in the 08:30
Phase-A preflight check-set, already renders into the 09:20 email + Telegram, already runs
on the VM, and is already about services. A second, arguably better trigger point is
`scripts/deploy_assert.py` — it fires at exactly the moment someone would wrongly believe a
pushed unit file took effect; its own design puts observability defects at WARNING, which
is the right class (⛔ this must never block a deploy).

**Cost — and ⛔ I am not going to call it a one-liner:**

1. ⛔ **A byte-compare is the wrong check and would be RED TODAY on comments alone.** It
   would report drift that does not matter, be ignored within a week, and become the
   NI-14 pattern below. ⭐ Do not build that version.
2. ✅ The version worth having compares **effective directives**: parse both files, drop
   comments and blank lines, normalise whitespace, and compare the `[Unit]` / `[Service]` /
   `[Install]` key→value sets. That is what would have been *green* today and *red* on a
   real change.
3. ⚠️ It must also account for **drop-ins**, or it will report "identical" while a drop-in
   silently changes behaviour. The robust form reads `systemctl show -p <property>` — the
   genuinely effective value after merge — and compares that against what the repo copy
   declares. That needs an explicit property list (`Restart`, `RestartSec`,
   `RestartPreventExitStatus`, `ExecStart`, `KillSignal`, `TimeoutStopSec`, …).
4. Tests: a fixture pair that is directive-identical but comment-different (must be GREEN —
   today's real state) and a pair differing in one directive (must be RED).

⇒ **Realistic size: a small unit — a directive comparator, one check row, and its tests.
⛔ Not a one-liner, and ⛔ not worth doing as a byte-compare.**

---

## §2 — ✅ ANSWERED: `security-watcher` IS THE DELIBERATE HEARTBEAT. IT IS **NOT** FAILING.

The card was right to make me establish this rather than repeat my own memory note.
**Established by measurement, ⛔ not by assumption:**

### 1 · The unit file says so itself — and anticipates exactly this confusion

```
# VM Security Manager Phase 1 — periodic watcher (model: alert-watcher.service).
# Type=simple + Restart=always + RestartSec=60: ExecStart runs one monitoring
# pass and exits 0, systemd restarts it ~60s later → ~60s cadence. Rising
# NRestarts is NORMAL (it's a heartbeat, not a crash-loop). NB: systemd REFUSES
# Restart=always with Type=oneshot — must be Type=simple.
```

### 2 · The passes exit **0** and log real work

```
ExecMainStatus=0        Result=success
ExecMainStartTimestamp = Sat 2026-08-22 21:23:39 IST
ExecMainExitTimestamp  = Sat 2026-08-22 21:23:40 IST      ⇒ a 1-second pass
```

Journal, six consecutive cycles:

```
21:18:36 Started …   21:18:37 INFO security_monitor: pass complete (1 finding(s), 0 new alert(s))   Deactivated successfully.
21:19:37 Started …   21:19:38 INFO security_monitor: pass complete (1 finding(s), 0 new alert(s))   Deactivated successfully.
21:20:38 …           21:21:38 …           21:22:39 …           21:23:39 …
```

**Cadence: 61 s, exactly as designed** (`RestartSec=60` + a ~1 s pass). It runs
`scripts/security_monitor.py --watch` — auth.log + file integrity + alerts.

### 3 · The count is consistent with the design, and the counter's origin is measured

`NRestarts` was **71,433** at 20:58 and **71,449** at 21:23. At 61 s that is ≈50.4 days.
The counter did not start in June — it started at a **VM reboot**:

```
-- Boot 3b636066be3a4b4098a1797015751d45 --
2026-07-03T22:22:05 security-watcher.service: Scheduled restart job, restart counter is at 1.
2026-07-03T22:23:08 … counter is at 2.
2026-07-03T22:24:08 … counter is at 3.
```

**3-Jul 22:22 → 22-Aug 21:23 = 50.0 days.** ✅ The arithmetic closes.

⇒ 🏷️ **VERDICT: deliberate heartbeat, healthy, working as documented. ⛔ Not a silently
failing service. ⛔ Nothing was fixed, restarted or stopped.** My memory note was correct —
and it is now *established* rather than asserted.

### 🔴 §2b — BUT THE "1 finding(s)" IS WORTH THE TEN MINUTES · **NI-14**

Every pass reports `1 finding(s)`. It is **not** a stuck finding — the key rotates hourly:

```json
{"checks_run": 10, "clean": false, "findings_count": 1, "max_severity": "INFO",
 "persistent": ["rootspike:2026082221"], "persistent_count": 1}
```

```python
def check_root_probe_spike(cfg, scan, now):
    if scan["root_probes"] > cfg.root_probe_spike_threshold:      # config/security.yaml: 400/hr
        return [Finding("INFO", f"rootspike:{now:%Y%m%d%H}", "Root login-probe spike",
                        f"… root login probes in the last hour … Blocked by key-only auth.")]
```

Benign by design: INFO severity, internet background noise, and `PermitRootLogin no` is
confirmed on this box (30-Jul SSH audit). **But two consequences are real:**

1. ⚠️ **The threshold no longer discriminates.** Its own comment says *"constant noise;
   alert only on anomaly"*, yet **>400 probes/hour is exceeded every hour**, so the finding
   fires every hour. A threshold that always fires measures nothing.
2. 🔴 **It pins the Control Tower's security panel to `warn`, permanently.**
   `ops/control_tower/aggregator.py:80` does `if not data.get("clean", True):` → appends a
   finding; then
   `status = "critical" if any CRITICAL else "warn" if findings else "ok"` — **any** finding,
   **including INFO**, forces `warn`. `SECURITY_MAP` maps `INFO → INFO`, so severity never
   rises, but the *status* is stuck.

⇒ **The security source can never read `ok`.** A panel that is always amber is a panel
nobody reads — the same alarm-fatigue class this campaign keeps finding. 🏷️ `MEASURED ·
⛔ NOT FIXED`. Options (⛔ none chosen, ⛔ none built): raise the threshold so it means
something; or have the Tower ignore INFO-only findings when computing `status`; or exclude
by-design-noisy keys from `clean`.

---

## §3 — THE ALERT-GUARD DEFECT, RE-SCOPED · ⛔ O-3 DOES NOT FIX IT

**Old framing (wrong):** *"exit 5 crash-loops, and the once-per-day alert guard is defeated
by the loop."*

**Correct scope:** `deploy/token_watcher.sh` calls `clear_alert_flags()` on
`ActiveState = active` **OR** `activating`. Any exit code **not** in
`RestartPreventExitStatus` is auto-restarted by systemd and therefore reports
`activating (auto-restart)` — proven live on this box by `security-watcher`. Such a unit
**never reaches `failed`**, so the watcher permanently takes the *"running — nothing to
do"* branch: **no alert is ever fired, and the once-per-day flags are deleted every 30 s
poll.**

⇒ 🔴 **THE DEFECT WAS NEVER EXIT-5-SPECIFIC.**

| exit code | in `RestartPreventExitStatus=3 4`? | in the trap? | after OPS ② |
|---|---|---|---|
| 0 | n/a — clean exit | no | unchanged |
| **1** | ⛔ no | 🔴 **YES — today, and always has been** | 🔴 **STILL YES** |
| **2** | ⛔ no | 🔴 **YES — today, and always has been** | 🔴 **STILL YES** |
| 3 | ✅ yes | no — reaches `failed`, alerts | unchanged |
| 4 | ✅ yes | no — reaches `failed`, alerts | unchanged |
| **5** | ⛔ no | 🔴 **YES** | ✅ **removed from the trap** |

⭐ Empirical contrast already on the record: the three real non-zero exits in the journal
(`16-Jul status=4`, `21-Jul status=4`, `10-Aug status=3`) each printed
`Failed with result 'exit-code'` **immediately**, precisely *because* 3 and 4 are in the
list.

⛔ **The tracker row must not read as "fixed by OPS ②".** OPS ② removes **one** exit code
from a trap that still holds **two**. An immediate, repeatable startup crash exiting 1 or 2
— a bad `.env`, an import error — lands in it exactly as before. 🏷️ `LATENT · ⛔ NOT FIXED`.

---

## §4 — HOLDS, CONFIRMED

| item | state |
|---|---|
| **OPS ②** | 🏷️ **PREPARED · ⛔ NOT APPLIED.** VM verified untouched: unit md5 still `136a4e88…`, drop-ins still `watchman.conf` only, `RestartPreventExitStatus=3 4`, service `inactive/dead`, `NRestarts=0`. Only Rama runs it, on the VM, with `sudo` |
| **NI-5** | 🏷️ **STOPPED · ⛔ NOT COMMITTED · ⛔ NOT DEPLOYED.** Patch `docs/audit/NI5_STOPPED_22-Aug-2026.patch` md5 `e1bce4ac3583e2ff0f1f8c37c794fc7f`, 19,032 B — **intact**. The three defaults still at `position_sizer.py:136/:137/:147`. ⛔ Not resumed, ⛔ neither option chosen |
| **repo-copy reconciliation** of the unit file | 🏷️ **PREPARED · ⛔ NOT DONE** — its own commit when authorised |
| **drop-in integrity watch** (§1) | 🏷️ **PREPARED · ⛔ NOT DONE** — code, forbidden by this card |
| **installed-vs-repo drift check** (§1) | 🏷️ **SCOPED · ⛔ NOT BUILT** — home and cost stated above |

**Still open, ⛔ none of it touched:** OPS ① `OnFailure=` (⭐ the only catch-all for an
unenumerated failure) · the boot-path alert wiring (⚠️ without it the operator gets
*"crashing (exit 5)"* with ⛔ **no key name**) · giving exit 5 exit-3's branch in
`token_watcher.sh` (⭐ a config rejection is a config failure, ⛔ not a crash) · the
alert-guard defect per §3 · **NI-14** (§2b, new) · **NI-15** (drop-ins unwatched, §1, new) ·
NI-9 · NI-11 · NI-12 · NI-13 · `sl_gap_buffer_pct` · F2 / F2a · MIS 3.5× (⛔ **HELD**) ·
the ~15:3x provenance questions ①②③ · the §5 parity list — ✅ **that one WAS produced**, in
`docs/audit/JOB1_AND_NI_ITEMS_22-Aug-2026.md` **§10**.

---

# ADDENDUM — 22-Aug, late evening. ⛔ RECORD ONLY. ⛔ Nothing applied, nothing built.

## §A — OPS ②: BOTH OPTIONS ON THE RECORD · ⛔ NEITHER CHOSEN

⭐ **The reframing is right on its central point, and it changes the balance.**
`/etc/systemd/system/trading-system.service.d/` is unwatched **today**, and `watchman.conf`
already sits in it unwatched. ⇒ **a second drop-in does not WIDEN NI-15** — it adds one
more file to a directory that was already blind. Meanwhile what OPS ② prevents — an
unbounded crash-loop from 08:15 with **no alert reaching the operator** — is a live safety
gap. ⇒ **Holding a safety fix behind an unrelated monitoring gap is the wrong way round.**

⭐ **And the in-place edit's "downside" is substantially its advantage.** A CRITICAL that
fires *because you changed something* is the integrity watch **working**. Re-blessing a
baseline after a deliberate, documented, verified change is normal operations, ⛔ not a
cost. On that reading the in-place edit gives a **monitored** result today with **no
dependency on NI-15 at all**.

| | option | for | against |
|---|---|---|---|
| **(i)** | **DROP-IN** `trading-system.service.d/exit5-no-restart.conf` | ⭐ safest EDIT — creates a new file, never touches the 18-Jun unit; rollback is `rm` + `daemon-reload` | ⛔ lands **unmonitored** (NI-15); arguably wants NI-15 resolved first |
| **(ii)** | **IN-PLACE** anchored `sed` on the installed unit | ⭐ **monitored** — fires a CRITICAL that **confirms the change landed and the watch works**; ⛔ no NI-15 dependency; unblocks today | ⚠️ the riskier EDIT (a `sed` on a live unit file); needs the integrity baseline re-blessed |

⚠️ **The honest counter, not hidden:** (ii) edits a live unit file in place. Mitigated by —
the `.bak` taken first, **the service being DOWN so a bad edit cannot break a session**, and
`systemctl show -p RestartPreventExitStatus` proving the result immediately. Rollback is
`cp` back + `daemon-reload`, already written in the O-3 section above.

⛔ **I have not chosen.** ⛔ OPS ② stays **PREPARED and NOT APPLIED** until Rama picks (i)
or (ii). Both command sets are written out in `OPS2_EXIT5_PREPARED_22-Aug-2026.md`.

## §B — NI-14, SHARPENED — **and one clause of the sharpening is WRONG**

The card's sharper claim: *"a genuine WARNING-severity finding would not change the panel's
status either ⇒ one whole severity band cannot be seen."*

**Half of that is confirmed. Half of it overstates, and I am not going to let the
flattering half stand unchecked.**

### ✅ CONFIRMED — the per-source `status` field has lost its discriminating power

`ops/control_tower/aggregator.py`:

```python
if not data.get("clean", True):
    sev = map_severity(SECURITY_MAP, str(data.get("max_severity", "INFO")))  # WARNING->MEDIUM
    findings.append(Finding("security", sev, ...))
status = ("critical" if any(f.severity == "CRITICAL" for f in findings)
          else "warn" if findings else "ok")
```

The hourly INFO `rootspike` guarantees `findings` is never empty ⇒

- 🔴 **`ok` is permanently UNREACHABLE** for the security source;
- 🔴 **INFO and WARNING(→MEDIUM) are INDISTINGUISHABLE in that field** — both yield `warn`.
  **Only a CRITICAL moves it.** Three defined states, one permanently occupied, one
  reachable only at the top of the scale.

⭐ **A second field is pinned the same way, and nobody has said this either:**
`write_run(... "status": "OK_WITH_FINDINGS" if detected else "OK")` — `detected` always
contains the INFO finding, so **the run row's status is permanently `OK_WITH_FINDINGS` and
can never be `OK`.**

### ⛔ OVERSTATED — the WARNING band is NOT invisible system-wide

Measured, and it matters because it changes how bad this is:

| path | INFO `rootspike` | a WARNING security finding |
|---|---|---|
| `SourceResult.status` | `warn` | `warn` — 🔴 **indistinguishable** |
| `counts` / `medium_count` on the run row | ⛔ **not counted at all** — `counts` is built over `("CRITICAL","HIGH","MEDIUM","LOW")` only | ✅ **counted as MEDIUM** |
| `upsert_finding` → `open_severities` → `health.score_and_band` | present as INFO (RANK 0) | ✅ present as MEDIUM (RANK 2) — **moves the health score** |
| `reporter.select_push` → Telegram | eligible by the push rules | ✅ eligible |

⇒ **The accurate statement: the defect is in the STATUS signal, not in the security
pipeline.** A real WARNING still increments `medium_count`, still moves the health score,
and is still push-eligible. What is lost is the *per-source status field* as a signal, plus
the run-level `OK` state.

⚠️ **That is still worth fixing** — a field that can only ever show one of three values is
dead weight on a dashboard, and `OK_WITH_FINDINGS` forever is the same shape. But it is
⛔ **not** "one whole severity band cannot be seen".

⛔ **Not fixed. ⛔ The 400/hr threshold NOT touched** — and the right prerequisite is
recorded: a **historical distribution first** (median, high percentile, max root-probes/hr
over the available journal) **plus the documented reason it was set at 400**, before anyone
moves it.

## §C — 🔴 F11 · SYSTEMATIC INERT-CONTROL SWEEP — **OPENED, ⛔ NOT STARTED, ⛔ NOT DESIGNED**

One Saturday produced four more instances of a single defect class:

| instance | the shape |
|---|---|
| **NI-14** | a threshold whose own comment says *"alert only on anomaly"* that fires **every hour** ⇒ discriminates nothing |
| **NI-15** | an integrity watch list of 8 explicit files that **misses the directory** where restart policy can be changed |
| **the alert guard** | defeated by **exactly the condition it exists to catch** (a restart loop reads `activating`) |
| **config_auditor group F** | NI-5 proved it would silently skip its row and turn its PASS into a **vacuous check** |

…on top of what the register already holds: `CHECK 2` at DEBUG on a DEBUG-off runtime ·
the sector cap on 10/10 UNKNOWN · `max_position_value` unreachable **by algebra** ·
`sl_atr_multiplier` with zero production readers · `dynamic_by_winrate` logging and gating
nothing · `min_multiplier`/`max_multiplier` with no production reader (measured this pass).

⭐ **Every one is the same shape: A CONTROL THAT EXISTS, RUNS, REPORTS HEALTHY, AND
CONSTRAINS NOTHING.** That is `N20-48`'s recorded dominant structural risk — *"configured,
built, started, yet INERT"*. **The instance count is now high enough that finding them one
at a time, by accident, while looking for something else, is no longer the efficient
method.**

**F11 — a deliberate hunt for controls that cannot fire.** Candidate axes, recorded only:
thresholds never crossed · branches never reached · guards algebraically dominated by a
tighter one · log lines below the runtime level · watch lists that miss their target ·
config keys with no production reader.

⛔ **NOT started. ⛔ NOT designed. ⛔ No axis chosen, no tooling written.** Recorded so Rama
sees it framed as **one problem, not nine**. ⚠️ A system whose safety depends on controls
that silently do nothing is a system whose safety is **unmeasured**.

## §D — NI-15: THE CONTRACT MUST BE VERIFIED BEFORE ANY CODE

⭐ Correctly flagged, and recorded as a hard prerequisite. Before adding the `.d/` directory
to `_default_watched_files()`, establish by measurement:

- does the watcher accept a **directory** at all, or only regular files?
- does it **recurse** into `*.d/*.conf`?
- does it hash **contents** or metadata?
- would **add** / **modify** / **remove** each trigger the CRITICAL? (a *new* drop-in
  appearing is the case that matters most, and a watch list keyed on known paths would miss
  exactly that)

🔴 **If it only supports regular files, adding the directory path would give FALSE
PROTECTION — worse than the gap it was meant to close.** ⛔ PREPARED, ⛔ not built.

---

# §E — THE DEPLOY SHAPE, MEASURED · ⛔ MEASURED, NOT DEPLOYED

**22-Aug-2026, late evening.** ⛔ Nothing pushed, nothing applied. The only remote contact
was `git ls-remote` and one `git push --dry-run`, which negotiates and updates **no ref** —
`origin/main` was re-measured **after** it and is unchanged.

## D-1 · THE CHAIN IS A CLEAN LINEAR FAST-FORWARD ✅

| measurement | result |
|---|---|
| `4568385` is an ancestor of `742d9da` | ✅ **YES** |
| `d00e574` is an ancestor of `742d9da` | ✅ **YES** |
| merge commits in `4568385..742d9da` | **0** |
| commits in `4568385..742d9da` | **8** |
| commits `742d9da` is BEHIND `origin/main` | **0** |
| `git push --dry-run origin 742d9da:refs/heads/main` | `4568385..742d9da → main`, **rc=0** — no `+` (forced) and no `!` (rejected) marker |
| `origin/main` re-measured after the dry-run | `45683859…` — **unchanged** |

⇒ ⭐ **Shipping is ONE explicit-refspec push. ⛔ No rebase, ⛔ no refit, ⛔ no merge exercise.**
The chain, oldest first: `d00e574` → `940a572` → `4928941` → `c146eb7` → `5a7dbf6` →
`6ad328e` → `4c495d0` → `742d9da`.

## D-2 · 🔴 WHAT WE HAVE IS **TWO CHAINED GATES**, ⛔ NOT ONE END-TO-END GATE

**Say which is true: two chained differentials.**

| gate | base | unit | measured |
|---|---|---|---|
| F1 | `4568385` — `rc 1 · 7F / 5,665P / 4S` | `d00e574` — `rc 1 · 7F / 5,715P / 4S` | 22-Aug morning, F1's session |
| this pass | `d00e574` — `rc 1 · 7F / 5,715P / 4S` | `742d9da` — `rc 1 · 7F / 5,751P / 4S` | 22-Aug 19:59–20:30, this session |

⭐ **The join is corroborated, not assumed.** F1's UNIT measurement of `d00e574`
(`7F / 5,715P / 4S`) and this session's independent BASE measurement of `d00e574`
(`7F / 5,715P / 4S`) are **the same numbers** — different session, different worktree,
hours apart. That is real evidence the two differentials meet at the same point.

⛔ **But it is still not the same claim.** Nobody has run a single differential
`4568385 → 742d9da`. The record must not say otherwise.

**Cost of a direct end-to-end gate:** one more BASE run at `4568385` — this session's base
run took **946.90 s** and the unit run **897.94 s**, so **≈16 minutes** reusing tonight's
`742d9da` unit run, or **≈31 minutes** for both sides fresh in one session (the stricter
form). ⛔ No code. **Predicted result, stated in advance so it is falsifiable:**
`7F / 5,665P / 4S` → `7F / 5,751P / 4S`, **0 NEW / 0 DISAPPEARED** at id level, and
`+86 = F1's +50 + this pass's +36`.

## D-3 · THE ATTRIBUTION SET — ✅ CONFIRMED, WITH TWO ADDITIONS

⭐ **A new, stronger measurement was taken for this: the sizing surface compared
`4568385` → `742d9da` DIRECTLY** — the whole 8-commit stack, not the two halves.

```
252-point grid (4 intents × 3 tiers × 7 prices × 3 stop distances), incl. the reason strings
  4568385 -> 80,831 B      742d9da -> 80,831 B      diff -> IDENTICAL
```

⭐ **Control: planting `delivery_risk_per_trade_pct 0.01 → 0.02` makes it go RED — 186
differing lines.** Config restored md5-identical, tree clean.

**The card's two families are CONFIRMED. Two further surfaces exist and are reporting-only:**

| # | surface | class | differs today? |
|---|---|---|---|
| **1** | a **missing or null** config key now REFUSES at boot instead of defaulting — F1's five + NI-4's two = **seven keys** | 🔴 **DECISION** | only on a malformed config |
| **2** | the SL-direction guard now **WARNS** instead of raising `KeyError` (NI-1) | 🔴 **DECISION** | only on an inverted SL |
| **3** | `config_auditor` C2 can now emit a WARN it previously could not (NI-2) | ⚪ **REPORTING** | ⛔ **no** — measured: verdict PASS, 0 C-group findings on the shipped config. And C2 is `Severity.WARN`; the startup path `raise_if_blocked()` fails fast **only on BLOCK** ⇒ ⛔ **it cannot stop a boot** |
| **4** | the position-value-cap CRITICAL field + rejection reason now report the **enforced** pct (F1, `position_sizer.py:660/:674`) | ⚪ **REPORTING** | ⛔ **no** — `delivery_max_position_value_pct == max_position_value_pct == 0.40`, so the emitted text is identical (the 252-point grid compares `reason` strings and found none) |

⚠️ **Scope of the direct measurement, stated rather than glossed:** the 252-point grid
covers the **sizer**. The **gate** side (`risk_engine` checks 7/8 and the delivery count
caps) is not in it — no value changed there, and it is covered by the two chained
differentials plus F1's own T-2/T-6. ⛔ That is a weaker form of evidence than the grid and
is labelled as such.

⇒ ⭐ **"Which of the eight commits broke Tuesday" has only two possible answers, and both
require an abnormal input to express** (a malformed config, or an inverted SL). **That is
the case FOR shipping them as one unit.** ⛔ It is Rama's ruling, ⛔ not mine.

## D-4 · THE QUEUE

| | |
|---|---|
| `origin/main` | **`45683859a0a05f466189ac5bc98f9a9f089f98d3`**, committed **2026-08-20 20:14:10 IST — Thursday**. ⚠️ **Unmoved for 2 days; Monday's 08:15 boot runs Thursday's code** |
| this branch `fix/delivery-fill-and-ni-22aug` | **8 commits** ahead, **0 behind**, clean, on **no remote** |
| `fix/delivery-config-independence-22aug` (F1 alone) | 1 ahead — an ancestor of the above, preserved untouched |
| local `main` (`3dff752`) | **90 ahead / 53 behind** — ⛔ a divergent lineage, **LOCAL BY DESIGN** (the register). ⛔ Not a deploy candidate |
| other branches ahead of `origin/main` | ~20, incl. `feat/screen10-slippage-analytics` 75 · `feat/delivery-config-split` 48 · `feat/tier-multipliers-61-62` 44 · `fix/alert-phase2-watcher` 32 · `fix/tick2-pipeline-scoped-daily-gate` 31 |

## D-5 · OPS ② ORDERING — MEASURED, AND THERE IS **NO CODE DEPENDENCY**

| measurement | result |
|---|---|
| `deploy/` files touched by `4568385..742d9da` | **0** |
| `main.py` exit-code sites, `4568385` vs `742d9da` | **26 vs 26**, and the exit-5 sites are at the **same lines** (`:1559`, `:1562`, `:1862`) on both |
| what `main.py` actually changed in the stack | **+9 / −1** — wiring five delivery kwargs, plus comments |

⇒ ⭐ **OPS ② is independent of the code.** It edits a systemd unit the stack never touches,
and the stack introduces no new exit code and moves none. It can be applied on its own, with
the service down, at any time.

⇒ 🔴 **But the SAFETY ordering is not symmetric.** The seven fail-closed keys become
reachable **only once the code is deployed**. So:

- **OPS ② BEFORE the push** — ✅ the aperture is covered from the moment it widens, **and**
  the pre-existing exit-5 paths (a malformed YAML, a missing file) gain the same protection
  immediately. Strictly better, no downside found.
- **OPS ② WITH the push** — ✅ equivalent in effect.
- **OPS ② AFTER the push** — 🔴 leaves a window in which a config typo crash-loops silently
  from 08:15 with no alert reaching the operator.

⇒ **PRECEDE or ACCOMPANY. ⛔ Never follow.** And because it is independent, "precede" costs
nothing and blocks nothing. ⛔ Still PREPARED and NOT APPLIED; ⛔ still Rama's choice of (i)
or (ii), and his `sudo`.

---

# §F — TWO TERMINOLOGY CORRECTIONS, AND V-1 SETTLED FROM THE DOCUMENT

**22-Aug-2026, late evening.** ⛔ No code, no VM write, no `sudo`, no push, no deploy.

## §F.1 — 🔴 "ONE SCRIPT PER DAY" IS A TRADING RULE. IT HAS NOTHING TO DO WITH DEPLOYING.

The review merged two unrelated rules into one phrase — *"the old 'one script per day' /
one-unit change policy"*.

| phrase | what it actually is |
|---|---|
| **one trade per `(symbol, DIRECTION, BOOK)` per trading day** | a **TRADING** rule. `docs/DAILY_ENTRY_POLICY.md`, settled 22-Aug. `PENDING_FILL` consumes the slot. ⛔ Nothing to do with deploys |
| **one fix per commit** / one unit per evening | a **DEPLOYMENT** discipline |

🔴 **This is a THIRD instance of the class `N20-56` was created to prevent — hours after it
was created.** `N20-56` retired the bare phrase *"one scrip per day"* precisely because it
cost a night of ambiguity; `N22-10` did the same for a bare `F1`/`F6`. The phrase has now
escaped into **deployment governance**, where it means something else entirely.
⭐ **The rule was right and the phrase escaped anyway** — which is the finding, not the slip.

## §F.2 — ⛔ THE RATIONALE WAS ALSO WRONG, AND IT CHANGES WHAT IS BEING DECIDED

The review gave the reason as *"the additional effort and review overhead … was becoming
disproportionate and 'not worth the effort'."*

- ⛔ Rama's *"not worth efforts"* was about the **GTT + MIS two-entry exception**, ⛔ not
  about deployment bundling.
- ⛔ **One-fix-per-commit exists for ATTRIBUTION** — so that when something breaks you can
  name the change — ⛔ **not to save effort.**

⭐ **That distinction decides whether D-3 is relevant at all.** If the rule is about
attribution, **D-3 speaks directly to it**: the attribution set is **two decision surfaces,
not eight commits**. If the rule were about effort, D-3 would be beside the point. **It is
about attribution.**

⛔ **This is NOT an authorisation to bundle, and the corrected rationale must not be read as
one.** Only Rama overrides the policy, in his own words. What is offered here is that he
decides against the **real** reason rather than a misremembered one.

## §F.3 — ✅ V-1 SETTLED: A WHOLE-STACK GATE IS **NOT** FORMALLY REQUIRED

**The exact line, quoted from `docs/PRE_BUILD_REVIEW_GATE.md` @ `23ea03d`, under
"WHAT STILL APPLIES UNCHANGED":**

> - One fix per commit
> - **Full differential gate before any deploy; gate results do not survive a SHA
>   change**

⇒ ⭐ **It says "full differential gate". It does NOT specify a SPAN** — no "whole stack",
no "end-to-end", no requirement that the base be the currently deployed SHA. A sweep of
`docs/campaign_practices.md` for a gate-span rule returns **nothing** either.

**And the second clause does not bite here.** *"Gate results do not survive a SHA change"* —
**no SHA under either gate result has changed**: `d00e574` and `742d9da` are both exactly
as gated, and `d00e574` sits **inside** the stack as an ancestor, ⛔ not a superseded
lineage. Neither result is invalidated.

⇒ 🏷️ **The chained evidence stands on the document's own terms. ⛔ Do not spend another
16–31 minutes for a nicer label.**

⚠️ **The one honest caveat, stated rather than glossed:** if the SINGLE combined push is
chosen, the head that lands (`742d9da`) was gated against `d00e574`, not against the
then-deployed `4568385`. The document does not require otherwise — but the tightest fit is
noted in §F.4.

## §F.4 — ⭐ D1 AND D2 BEAR ON THE DECISION, AND NOBODY HAS CITED THEM

**`docs/campaign_practices.md` D1 · ⛔ THERE IS NO PARTIAL DEPLOY**

> `main` is linear and deploy is **push → `checkout -f`**. **Anything committed before a
> push rides that push.**

⇒ ⭐ **One-unit-per-evening is still achievable here, and the mechanism is concrete:** push
the explicit SHA `d00e574:refs/heads/main` first, then `742d9da:refs/heads/main` at a later
slot. D1 constrains what rides *a* push; it does not prevent pushing an earlier ancestor.

⭐ **And the two chained gates map EXACTLY onto that staging** — each push would be covered
by a gate whose base is the then-deployed state (`4568385 → d00e574`, then
`d00e574 → 742d9da`). ⇒ **If Rama holds one-unit-per-evening, the existing evidence is
precisely the right shape and no further gate is needed. If he chooses one combined push,
the chained pair is what covers it — and V-1 says that is sufficient.** Either way, ⛔ no
extra run.

**D2 · THE BEHAVIOURAL SURFACE INVENTORY runs before EVERY deploy window** — its stated
intent: *"WHICH COMMITS CHANGE BEHAVIOUR, and is each of those named?"*

⭐ **D-3 IS that inventory for this stack.** Answered at commit granularity:

| commit | touches |
|---|---|
| `d00e574` | 🔴 **behaviour** — the 7-key family (with `6ad328e`) + the reporting change |
| `4928941` | 🔴 **behaviour** — NI-1, warns instead of raising |
| `6ad328e` | 🔴 **behaviour** — the last two of the 7 keys |
| `c146eb7` | ⚪ **reporting only** — C2; 0 findings on the shipped config, `Severity.WARN`, cannot block a boot |
| `940a572` · `5a7dbf6` · `4c495d0` · `742d9da` | ⚪ **nothing executable** — tests, comments (AST-identical), a docstring, an R100 rename |

⇒ **3 of 8 commits change behaviour; all three are named. D2 is satisfied.**

## §F.5 — ⚠️ "ONE UNIT PER EVENING" IS NOT A WRITTEN RULE

Measured: `grep -rn -i "one unit per evening|one script per day|one scrip per day"` over
`docs/` and the root `*.md` returns **ZERO hits**. The written rules are **"One fix per
commit"** (the gate document) and **D1** (no partial deploy). One-unit-per-evening is an
**operating preference** — which is exactly why only Rama can hold or override it, and why
it cannot be settled by citing a document.
