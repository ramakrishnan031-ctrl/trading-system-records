---
name: exit5-restart-loop-unbounded-22aug
description: "systemd's start rate limiter cannot stop a restart loop on this VM, and an auto-restarting unit reads as ActiveState=activating so token_watcher never alerts"
metadata: 
  node_type: memory
  type: project
  originSessionId: b3398573-7588-48ce-8ab3-97f2c5107eaf
  modified: 2026-08-22T15:43:26.539Z
---

# EXIT 5 CRASH-LOOPS, THE LIMITER CANNOT STOP IT, AND NOBODY GETS TOLD

**Measured 22-Aug-2026 evening on the VM, read-only.** ⛔ Nothing was applied.
Related: [[unpushed-pending-deploy-ledger]] · [[boot-chain-token-watcher-05aug]] ·
[[ct-guard-invariant-18jul]]. Prepared change:
`docs/audit/OPS2_EXIT5_PREPARED_22-Aug-2026.md`.

## 1 · THE LIMITER IS ARITHMETICALLY UNREACHABLE

Measured on `trading-system.service` (systemd **255**, Ubuntu 255.4-1ubuntu8.17):

```
DefaultStartLimitIntervalUSec=10s      DefaultStartLimitBurst=5
StartLimitIntervalUSec=10s             StartLimitBurst=5      StartLimitAction=none
Restart=on-failure                     RestartUSec=10s
RestartPreventExitStatus=3 4
```

To trip the limiter you need **≥5 starts inside 10 s** ⇒ a mean gap **≤2.5 s**.
`RestartSec=10` forces gaps of **≥10 s**. Five starts therefore span **≥40 s** — four
times the window.

⇒ ⛔ **The limiter can NEVER engage for this unit, for any exit code, at any process
runtime.** This is not "unlikely"; it is arithmetic. `RestartSec` ≥
`StartLimitIntervalSec` makes it structurally unreachable.

⭐ **CONFIRMED EMPIRICALLY BY A UNIT ALREADY DOING IT ON THE SAME BOX.**
`security-watcher.service` (`Restart=always`, `RestartSec=60`) has **`NRestarts=71433`**
and has never been rate-limited.

## 2 · AN AUTO-RESTARTING UNIT READS AS `activating` — AND THAT DEFEATS THE ALERT

Sampled `security-watcher` three times, three seconds apart:

```
ActiveState=activating  SubState=auto-restart      (x3, NRestarts=71433)
```

`deploy/token_watcher.sh` branches on `ActiveState`:

- `active` **or** `activating` → `clear_alert_flags()` + *"running -- nothing to do"*
- `failed` → the `case` on `ExecMainStatus` (4 → HALT alert · 3 → startup alert ·
  `1|2|*)` → crash backoff, `MAX_CRASH_PER_HOUR=3`, then `alert_once_per_day crash`)

⇒ 🔴 **An exit code NOT in `RestartPreventExitStatus` never reaches `failed`**, so the
watcher permanently takes the FIRST branch: **no alert is ever fired, and the
once-per-day flags are deleted every 30 s poll.**

⚠️ **This is WIDER than exit 5.** Exits **1 and 2** are in exactly the same trap today and
always have been. Adding `5` to `RestartPreventExitStatus` removes exit 5 from it and
leaves 1 and 2 in it. `LATENT`, ⛔ not fixed.

## 3 · EXIT 5 PRE-DATES F1 — ⛔ DO NOT SAY F1 CREATED IT

`main.py:1862` (`4568385`): `_main_locked` wraps `load_all` in `try/except Exception` →
`return 5`, and `sys.exit(main())` propagates it. That `except` catches **anything** —
a malformed YAML, a missing file, any schema violation on any key. `main.py` at `4568385`
has **four** `exit 5` sites (`:1862` config · `:1753` argparse · `:1559`/`:1562` missing
api-key/secret on the login path, ⚠️ headless reachability UNVERIFIED).

⇒ F1 + NI-4 do **not create** the exposure. They widen the **aperture**: seven delivery
keys now route a *missing or null value* into `:1862`, turning a rare malformed-file event
into a routine human error. ⭐ That makes the one-token fix overdue, ⛔ not new.

## 4 · IT HAS NEVER FIRED — AND THE SEARCH IS PROVEN

| search | result |
|---|---|
| `journalctl -u trading-system -g "status=5\|Scheduled restart\|start-limit\|repeated too quickly"`, 45-day window | **No entries** |
| **CONTROL**, same window + machinery, known non-zero exits | ✅ found **3**: `2026-07-16 10:55:22 status=4` · `2026-07-21 11:37:53 status=4` · `2026-08-10 08:15:25 status=3` |
| journal span | `2026-06-10 05:24` → `2026-08-21 17:35` (~73 days) |

⭐ Each of those three printed `Failed with result 'exit-code'` **immediately** — because
3 and 4 **are** in `RestartPreventExitStatus`. That is the empirical contrast.

## 5 · THE INSTALLED UNIT IS NOT THE REPO COPY, AND DEPLOY DOES NOT INSTALL IT

| | md5 |
|---|---|
| installed `/etc/systemd/system/trading-system.service` (1411 B, **18-Jun 16:35**) | `136a4e88774fb5d2f392688a2ce40d3e` |
| repo `deploy/systemd/trading-system.service` @ deployed `4568385` | `e24b88493bc5cdd7ff7753479a73a8dc` |

The diff is **two COMMENT lines** (the exit-4 note, added in git and never re-installed).
Every directive is identical. ⚠️ There is also an existing drop-in
`trading-system.service.d/watchman.conf` (`[Unit] Wants=trading-watchman.service`, no
`[Service]` section).

🔴 **Deploy is a git checkout into `/home/ubuntu/systems/trading-system/`. It does NOT
install unit files.** ⇒ ⛔ editing `deploy/systemd/*.service` and pushing changes NOTHING
about the running restart policy. The install is a separate manual act, and the two have
already drifted.

## 6 · 🔴 DROP-INS ARE NOT INTEGRITY-WATCHED

`scripts/security_monitor.py:213-224` already hashes the installed unit every ~61 s at
**CRITICAL**:

```python
{"path": "/etc/systemd/system/trading-system.service",   "severity": "CRITICAL", "label": "unit_trading"},
{"path": "/etc/systemd/system/security-watcher.service", "severity": "CRITICAL", "label": "unit_security"},
```

⚠️ The list is **8 explicit FILE paths — no directories, no globs.** So
`/etc/systemd/system/trading-system.service.d/` is **unwatched**: the existing
`watchman.conf`, and any new drop-in, can change the live trading service's restart policy
**without tripping the CRITICAL integrity check.**

⇒ Trade-off for OPS ②: the **drop-in** is operationally safer (rollback = `rm` +
`daemon-reload`) but lands **unmonitored**; the **in-place edit** *is* watched and would
fire a CRITICAL alert on apply (correct, but the baseline then needs re-blessing).
⭐ **Recommendation: take the drop-in AND add the `.d/` directory to
`_default_watched_files()`.** ⛔ PREPARED, NOT DONE.

⛔ **An installed-vs-REPO drift check does NOT exist** (the integrity check compares the
file to its own stored baseline, a different question). ⭐ Home would be
`scripts/preflight/checks/services.py` (08:30 Phase-A → 09:20 email/Telegram) or
`scripts/deploy_assert.py` (WARNING class — ⛔ must never block). ⛔ **A byte-compare is the
WRONG check — it would be RED today on comments alone and ignored within a week.** It must
compare **effective directives** (comments/whitespace stripped) and account for drop-ins
via `systemctl show -p <property>`.

## 7 · ✅ `security-watcher`'s 71,449 RESTARTS ARE THE DESIGN — ESTABLISHED, NOT ASSUMED

Asked 22-Aug because the number deserved a question. **Answer: deliberate heartbeat,
healthy. ⛔ NOT a silently failing service.**

- The unit's own header documents it: *"Type=simple + Restart=always + RestartSec=60:
  ExecStart runs one monitoring pass and exits 0 … Rising NRestarts is NORMAL (it's a
  heartbeat, not a crash-loop). NB: systemd REFUSES Restart=always with Type=oneshot."*
- `ExecMainStatus=0`, `Result=success`; a pass runs **1 second** (21:23:39 → 21:23:40).
- Journal, six consecutive cycles: **61 s apart**, each logging
  `INFO security_monitor: pass complete (1 finding(s), 0 new alert(s))` → `Deactivated successfully`.
- Counter origin **measured**: `-- Boot 3b636066… --` then
  `2026-07-03T22:22:05 … restart counter is at 1.` ⇒ 3-Jul 22:22 → 22-Aug 21:23 = **50.0
  days**, and 71,449 × 61 s ≈ **50.4 days**. ✅ The arithmetic closes.

### ⚠️ NI-14 — the standing "1 finding" pins the Control Tower to `warn` forever

`data_store/security/last_run.json`: `clean:false`, `findings_count:1`,
`max_severity:"INFO"`, `persistent:["rootspike:2026082221"]` — an **hourly-rotating**
INFO from `check_root_probe_spike` (threshold **400/hr**, `config/security.yaml`), whose
own text says *"Blocked by key-only auth."*

1. ⚠️ The threshold no longer discriminates — its comment says *"alert only on anomaly"*,
   yet it fires **every hour**.
2. 🔴 `ops/control_tower/aggregator.py:80` — `if not data.get("clean", True)` appends a
   finding, and `status = … "warn" if findings else "ok"` treats **any** finding, INFO
   included, as `warn`. ⇒ **the security panel can never read `ok`.** Alarm fatigue.

🏷️ `MEASURED · ⛔ NOT FIXED`. ⛔ No option chosen.

## 8 · NI-14 REFINED — ⛔ AND ONE SHARPENING OF IT IS OVERSTATED

A later card sharpened NI-14 to *"a genuine WARNING finding would not move the panel either
⇒ one whole severity band cannot be seen."* **Half confirmed, half overstated.**

### ✅ CONFIRMED — the per-source `status` field has lost its discriminating power

The hourly INFO `rootspike` guarantees `findings` is never empty, so in
`aggregator.py`'s `status = "critical" if any CRITICAL else "warn" if findings else "ok"`:

- 🔴 **`ok` is permanently UNREACHABLE** for the security source;
- 🔴 **INFO and WARNING(→MEDIUM) both yield `warn`** — indistinguishable in that field.
  **Only a CRITICAL moves it.**
- ⭐ **A SECOND field is pinned the same way:**
  `write_run(... "status": "OK_WITH_FINDINGS" if detected else "OK")` — `detected` always
  holds the INFO finding ⇒ **the run row can never be `OK`.**

### ⛔ OVERSTATED — the WARNING band is NOT invisible system-wide

| path | INFO `rootspike` | a WARNING security finding |
|---|---|---|
| `SourceResult.status` | `warn` | `warn` — 🔴 indistinguishable |
| `counts` / `medium_count` | ⛔ not counted — `counts` covers only CRITICAL/HIGH/MEDIUM/LOW | ✅ counted as MEDIUM |
| `upsert_finding` → `open_severities` → `health.score_and_band` | INFO (RANK 0) | ✅ MEDIUM (RANK 2) — moves the health score |
| `reporter.select_push` → Telegram | eligible | ✅ eligible |

⇒ **The defect is in the STATUS signal, not in the security pipeline.** A real WARNING
still increments `medium_count`, still moves the health score, and is still push-eligible.
What is lost is the per-source `status` field and the run-level `OK` state.

⛔ **Not fixed. ⛔ The 400/hr threshold NOT touched** — prerequisite recorded: a historical
distribution (median / high percentile / max root-probes per hour) **and** the documented
reason it was set at 400, before anyone moves it.

## 9 · OPS ② — BOTH OPTIONS, ⛔ NEITHER CHOSEN

⭐ The gap NI-15 names **already exists**: the `.d/` directory is unwatched today and
`watchman.conf` already sits in it. ⇒ a second drop-in does ⛔ **not widen** NI-15. Holding
a safety fix behind an unrelated monitoring gap is the wrong way round.

| | option | for | against |
|---|---|---|---|
| **(i)** | DROP-IN | safest EDIT; rollback `rm` + `daemon-reload` | ⛔ lands unmonitored |
| **(ii)** | IN-PLACE `sed` | ⭐ **monitored** — the CRITICAL it fires CONFIRMS the change landed and the watch works; no NI-15 dependency | ⚠️ riskier EDIT; baseline must be re-blessed |

⚠️ (ii)'s risk is mitigated by the `.bak`, by **the service being DOWN**, and by
`systemctl show -p RestartPreventExitStatus` proving the result at once.
⛔ **PREPARED · NOT APPLIED · neither chosen.**

## 10 · ⚠️ NI-15's CONTRACT MUST BE MEASURED BEFORE ANY CODE

Before adding the `.d/` directory to `_default_watched_files()`: does the watcher accept a
**directory** at all, or only regular files · does it **recurse** into `*.d/*.conf` · does
it hash **contents** or metadata · would **add / modify / remove** each trigger the
CRITICAL (a *new* drop-in appearing is the case that matters most).
🔴 **If it only supports regular files, adding the directory path gives FALSE PROTECTION —
worse than the gap.** ⛔ PREPARED, ⛔ not built.
