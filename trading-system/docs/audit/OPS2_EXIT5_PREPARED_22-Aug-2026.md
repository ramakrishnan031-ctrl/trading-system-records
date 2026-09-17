# OPS ② — `RestartPreventExitStatus` += `5` · **PREPARED, ⛔ NOT APPLIED**

**22-Aug-2026 (Saturday) evening, IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).

🏷️ **STATUS: `PREPARED · ⛔ NOT APPLIED · ⛔ NO VM WRITE · ⛔ NO sudo RUN`.**
Every VM interaction below was **read-only**: `cat`, `ls`, `md5sum`, `systemctl show`,
`systemctl cat`, `journalctl`, `sed -n`, `grep`. ⛔ No write, ⛔ no `sudo`, ⛔ no service
state change. The service was **down** throughout (`inactive/dead`, last exit **0** at
`Fri 2026-08-21 17:35:04 IST`, `NRestarts=0`).

---

## O-1 — THE ACTUALLY INSTALLED UNIT (⛔ not the repo copy)

| measured | value |
|---|---|
| systemd's own answer | `FragmentPath=/etc/systemd/system/trading-system.service` |
| file | `-rw-r--r-- root root **1411** B, **Jun 18 16:35**` |
| md5 (installed) | **`136a4e88774fb5d2f392688a2ce40d3e`** |
| ⚠️ **drop-in ALREADY present** | `DropInPaths=/etc/systemd/system/trading-system.service.d/watchman.conf` (38 B, `f1ea771c1e42155175c71c96a5849925`) |
| drop-in content | `[Unit]` / `Wants=trading-watchman.service` — ⭐ **no `[Service]` section, so it does not touch restart policy** |
| unit file state | `UnitFileState=enabled`, `UnitFilePreset=enabled` |
| systemd | **255 (255.4-1ubuntu8.17)** |
| deployed tree | `git --git-dir=/home/ubuntu/trading-system.git rev-parse HEAD` → **`45683859a0a05f466189ac5bc98f9a9f089f98d3`** = `origin/main` ✅ |

### 🔴 The installed unit is **NOT** the repo copy

| | md5 |
|---|---|
| installed `/etc/systemd/system/trading-system.service` | `136a4e88774fb5d2f392688a2ce40d3e` |
| repo `deploy/systemd/trading-system.service` **at the deployed SHA `4568385`** | `e24b88493bc5cdd7ff7753479a73a8dc` |

```diff
--- repo copy @ 4568385
+++ installed on the VM
@@ -27,8 +27,6 @@
 # Exit 3 = startup check failure (would loop on same failure) -- no restart.
-# Exit 4 = HALT: kill switch active, manual --resume required -- no restart
-#          (otherwise systemd hammer-restarts on the same SOFT_KILL; 18-Jun crash-loop).
 # Exit 1/2 = runtime error/crash -- restart so system can recover mid-day.
 Restart=on-failure
```

⭐ **Every DIRECTIVE is identical — the difference is two COMMENT lines.** The installed
file is an **older revision** (18-Jun) whose comment block was later expanded in git and
never re-installed. Confirmed independently by `systemctl show`, which reports the same
effective values either way.

🔴 **THE HAZARD THIS EXPOSES, AND IT IS THE REASON O-1 EXISTS:** deploy is a git checkout
into `/home/ubuntu/systems/trading-system/` (bare repo → post-receive). It does **NOT**
install unit files. ⇒ **Editing `deploy/systemd/trading-system.service` and pushing
changes NOTHING about the running restart policy.** The install is a separate manual act,
and the two have already drifted once. Any fix must touch `/etc/systemd/system/`.

---

## O-2 — 🔴 THE RATE LIMITER · MEASURED · **IT DOES NOT SAVE US**

This was the open question: *if systemd's rate limiter already halts the loop, the picture
changes.* **It does not change. Measured on the VM:**

```
DefaultStartLimitIntervalUSec=10s      DefaultStartLimitBurst=5
StartLimitIntervalUSec=10s             StartLimitBurst=5        StartLimitAction=none
Restart=on-failure                     RestartUSec=10s
RestartPreventExitStatus=3 4
```

### The arithmetic — it is not "probably won't fire", it is **cannot**

To trip the limiter you need **≥5 starts inside a 10 s window** ⇒ a mean gap of **≤2.5 s**.
`RestartSec=10` forces a gap of **≥10 s** plus the process runtime. Five starts therefore
span **≥40 s** — four times the window.

⇒ **The limiter can never engage for this unit, for any exit code, at any runtime.**
`RestartSec` (10 s) ≥ `StartLimitIntervalSec` (10 s) makes it structurally unreachable.

### ⭐ And it is confirmed empirically, on this same box, by a unit already doing it

`security-watcher.service` runs a deliberate `Restart=always` / `RestartSec=60` heartbeat.
Sampled three times, three seconds apart:

```
Restart=always  RestartUSec=1min  NRestarts=71433  ActiveState=activating  SubState=auto-restart
Restart=always  RestartUSec=1min  NRestarts=71433  ActiveState=activating  SubState=auto-restart
Restart=always  RestartUSec=1min  NRestarts=71433  ActiveState=activating  SubState=auto-restart
```

**71,433 restarts and the limiter has never stopped it.** That is direct, live proof of
both halves of the mechanism:

1. **A slow restart loop is never rate-limited on this machine.**
2. 🔴 **A unit being auto-restarted reports `ActiveState=activating`** — which is the exact
   string `token_watcher.sh` treats as *"running — nothing to do"*.

### Has exit 5 ever actually happened? **No — and the search is proven able to find it**

| search | result |
|---|---|
| `journalctl -u trading-system -g "status=5\|Scheduled restart\|start-limit\|repeated too quickly"`, 45-day window | **No entries** |
| **CONTROL** — same window, same `-g` machinery, looking for known non-zero exits | ✅ **found 3**: `2026-07-16 10:55:22 status=4` · `2026-07-21 11:37:53 status=4` · `2026-08-10 08:15:25 status=3` |
| journal span available | `2026-06-10 05:24` → `2026-08-21 17:35` (~73 days) |

⇒ **The exit-5 crash-loop is `LATENT`, ⛔ not `LIVE`. It has never fired in ~73 days of
journal.** ⚠️ **But see the correction at the foot of this document: exit 5 was already
reachable before F1** (any `load_all` exception routes to it). F1 + NI-4 widen the
aperture from "a malformed config file" to "a missing or null value in any of seven
delivery keys" — they do not create the exposure.

⭐ Note what the control also shows: every one of those three exits printed
`Failed with result 'exit-code'` **immediately**, because 3 and 4 **are** in
`RestartPreventExitStatus`. That is the empirical contrast — the same event with exit 5
would instead enter `activating (auto-restart)` and cycle.

---

## O-3 — THE EXACT CHANGE · ⛔ NOT APPLIED

### The one-token change

```
RestartPreventExitStatus=3 4      →      RestartPreventExitStatus=3 4 5
```

⛔ **Nothing else.** `Restart=on-failure`, `RestartSec=10`, `StartLimit*`, `KillSignal`,
`TimeoutStopSec` and every other directive are untouched. Exits **0, 1, 2** keep their
current behaviour exactly.

### 🔴 Recommended shape: a DROP-IN, not an edit of the installed unit

**Why a drop-in:** rollback is `rm` + `daemon-reload` — no backup file to restore and no
chance of a bad in-place edit. The pattern is already established on this box
(`watchman.conf`), and `systemctl cat` shows drop-ins plainly. It also leaves the 18-Jun
installed unit exactly as it is, so the O-1 comment drift is not silently widened.

⭐ **The two-line form is deliberate.** `RestartPreventExitStatus` is a list-type setting;
assigning the empty string first **resets** it, then the second line **sets** it outright.
This makes the result `3 4 5` **without depending on whether a drop-in appends or
replaces** — ⛔ I did not want the outcome to rest on a semantics assumption I could not
test without writing to the VM.

### Commands for Rama — run **in a shell ON the VM**

⚠️ Run these in a VM shell, ⛔ not nested inside `ssh '...'` — a heredoc through nested SSH
quoting is how this campaign has mangled content before.

```bash
# ── 0 · PRE-CHECK: the service must be down, and record the BEFORE state ──────
systemctl show trading-system.service -p ActiveState -p SubState -p ExecMainStatus
systemctl show trading-system.service -p RestartPreventExitStatus
#   expect:  ActiveState=inactive  SubState=dead
#   expect:  RestartPreventExitStatus=3 4          <-- the rollback anchor

# ── 1 · APPLY ────────────────────────────────────────────────────────────────
sudo mkdir -p /etc/systemd/system/trading-system.service.d
sudo tee /etc/systemd/system/trading-system.service.d/exit5-no-restart.conf >/dev/null <<'EOF'
# 22-Aug-2026 — exit 5 = config REJECTED at load (main.py returns 5 via
# _config_error_detail). Fix item 1 + NI-4 make SEVEN delivery keys able to
# produce it. Without 5 here, systemd restarts every RestartSec=10s forever,
# the unit never reaches `failed`, and token_watcher therefore never fires its
# crash alert (it treats ActiveState=activating as "running — nothing to do").
# Reset-then-set so the result does not depend on list-append semantics.
[Service]
RestartPreventExitStatus=
RestartPreventExitStatus=3 4 5
EOF

sudo systemctl daemon-reload

# ── 2 · VERIFY — this is the acceptance test ─────────────────────────────────
systemctl show trading-system.service -p RestartPreventExitStatus
#   MUST print exactly:  RestartPreventExitStatus=3 4 5
systemctl cat trading-system.service | tail -20
#   the drop-in must appear, and the base unit must be unchanged
```

**`daemon-reload` does NOT start or restart anything.** The unit is inactive; the new
policy applies at the next exit. ⛔ No restart is needed and none should be done.

### Rollback — one command

```bash
sudo rm -f /etc/systemd/system/trading-system.service.d/exit5-no-restart.conf
sudo systemctl daemon-reload
systemctl show trading-system.service -p RestartPreventExitStatus
#   MUST print:  RestartPreventExitStatus=3 4
```

### Alternative (⛔ not recommended): edit the installed unit in place

```bash
sudo cp -p /etc/systemd/system/trading-system.service \
           /etc/systemd/system/trading-system.service.bak-22aug2026
sudo sed -i 's/^RestartPreventExitStatus=3 4$/RestartPreventExitStatus=3 4 5/' \
           /etc/systemd/system/trading-system.service
sudo systemctl daemon-reload
systemctl show trading-system.service -p RestartPreventExitStatus
# rollback:
sudo cp -p /etc/systemd/system/trading-system.service.bak-22aug2026 \
           /etc/systemd/system/trading-system.service && sudo systemctl daemon-reload
```

⚠️ The anchored `sed` matches the installed file's line exactly as measured today
(`RestartPreventExitStatus=3 4`, no trailing space). It is still the riskier option.

### 📌 Repo reconciliation — PREPARED, ⛔ NOT DONE

`deploy/systemd/trading-system.service` in the repo still reads `RestartPreventExitStatus=3 4`.
Whichever option is taken, the repo copy should be brought in line **in its own commit**,
with a comment recording that installing it is a manual act. ⛔ Not done here: the card
scopes this to prepare-only and forbids code beyond §2.

---

## O-4 — 🔴 WHAT O-3 DOES **NOT** FIX

Measured from `deploy/token_watcher.sh` on the deployed tree
(`SLEEP_SEC=30`, `LONG_SLEEP=300`, `MAX_CRASH_PER_HOUR=3`).

### 1 · The operator still does not get the key name

After O-3, exit 5 lands in `failed`, and token_watcher's `case` falls to its **`1|2|*)`
default** branch. The message is:

> `trading-system crashing (exit 5); restart backoff limit reached. Manual check needed.`

⛔ **Generic. It does not say which config key was rejected.** The key name exists only in
the CRITICAL line the boot writes to `logs/system_<date>.log`. Naming it in the alert is
the **boot-path alert wiring** — ⭐ still queued, ⛔ not done.

### 2 · It is not a clean stop — it is 3 futile boots per hour

Exit **3** gets special treatment: *"failed today ⇒ NOT restarting"*, alert immediately.
**Exit 5 has no such branch.** It goes to the crash path, which will `start_service` up to
`MAX_CRASH_PER_HOUR=3` times per hour, each a fresh boot that fails again in about a
second, before it alerts.

⭐ **Derived from the constants (⛔ not measured — exit 5 has never occurred):** at a 30 s
poll, three attempts plus the alerting poll is roughly **2 minutes** from the 08:15
failure to the first Telegram — against **no alert at all** today. That is the real gain.
⚠️ It also revises the earlier "roughly half an hour" estimate downward.

⇒ **The natural follow-up is to give exit 5 exit-3's branch** (a config rejection is a
config failure, not a crash). That is a change to `token_watcher.sh` — ⛔ beyond a
one-token unit edit, and ⛔ not done.

### 3 · The alert-guard defect is NOT fixed — it is only made unreachable *via exit 5*

`clear_alert_flags()` fires on `active` **or** `activating`, deleting the once-per-day
flags. After O-3, exit 5 sits in `failed`, so that path stops being reachable **for exit 5**
and the once-per-day guard works again for it.

🔴 **But exits 1 and 2 are still auto-restarted by systemd, still report
`ActiveState=activating` — proven above by `security-watcher` — and still hit
`clear_alert_flags` every 30 s poll.** An immediate, repeatable startup crash exiting 1 or
2 therefore lands in exactly the trap this item describes, and always has. `LATENT`,
⛔ not fixed, ⛔ not in scope here. ⭐ **This is wider than the exit-5 framing: the defect
was never exit-5-specific.**

### 4 · OPS ① is still the only thing that catches the unknown

A systemd `OnFailure=` unit catches **every** failure mode, including ones nobody has
enumerated. O-3 fixes one exit code. ⭐ Still queued, ⛔ not done.

---

## THE COUPLING — AND A CORRECTION TO HOW IT HAS BEEN FRAMED

### Exit 5 is verified end-to-end, on the DEPLOYED tree

`main.py:3833 sys.exit(main())` → `main()` `:1849 return _main_locked(...)` →
`_main_locked` Phase 0b:

```python
    try:
        app_config = load_all(config_dir)
    except Exception as exc:
        _log.critical("Config load failed: %s%s", exc, _config_error_detail(exc))
        return 5                                    # main.py:1862 @ 4568385
```

⇒ a `ConfigSchemaError` really does become **process exit code 5**. Measured at `4568385`,
⛔ not recalled.

### 🔴 THE CORRECTION: exit 5 is **not new**, and the hazard **pre-dates F1**

That `except Exception` catches **anything** `load_all` raises. So exit 5 has ALWAYS been
reachable from a malformed YAML, a missing config file, or a schema violation on **any**
key. `main.py` at `4568385` has **four** `exit 5` sites in total: `:1862` (config load),
`:1753` (argparse failure), and `:1559`/`:1562` (missing `api_key`/`api_secret` env vars on
the login path — ⚠️ that path uses `input_fn`, so its reachability from the headless service
is **unverified** and I am not claiming it).

⇒ **I should not say F1 "created" this exposure. The crash-loop has been live and unfixed
for as long as exit 5 has existed.** What F1 + NI-4 change is the **aperture**: seven
delivery keys now route a *missing or null value* into `:1862`, turning a rare
malformed-file event into a routine human error — an omitted line in a config edit.

⭐ **This makes O-3 more urgent, not less.** It is not a new coupling introduced by this
pass; it is a pre-existing, never-triggered defect that this pass makes materially easier
to hit. ⛔ Nothing here argues for reverting fail-closed — fail-closed is right. It argues
for the order: **the one-token fix should ship with the seven keys, not after them.**

---

## THREE KINDS OF EVIDENCE — ⛔ NONE SUBSTITUTES FOR ANOTHER (permanent, in this record)

⚠️ **I conflated the first with the second in the previous pass and it is corrected here.**
Saying *"the CRITICAL fired"* proves the **watcher** works. It proves **nothing** about
whether `RestartPreventExitStatus=3 4 5` actually took hold.

| evidence | what it proves | how it is obtained |
|---|---|---|
| **DETECTION** — the integrity CRITICAL fires | the watch **saw the file change** | the security_monitor alert, ~61 s after the edit (⚠️ **only for the in-place option** — a drop-in lands in an unwatched directory, NI-15) |
| **ENFORCEMENT** — the intended policy actually loaded | systemd is **using** `3 4 5` | `systemctl show trading-system.service -p RestartPreventExitStatus` → must print exactly `RestartPreventExitStatus=3 4 5`. ⛔ Reading the FILE is not enough — a drop-in, a syntax error or a missed `daemon-reload` all leave the file right and the policy wrong |
| **GOVERNANCE** — no undocumented repo-vs-VM divergence | the change is **recorded where the next reader will look** | the repo copy reconciled in its own commit, and the integrity baseline deliberately re-blessed |

⇒ **If OPS ② is ever authorised, all three must be collected — and the ENFORCEMENT one is
the only one that answers "did the fix work".**

⭐ Note the asymmetry this exposes between the two options: **(i) the drop-in yields
ENFORCEMENT but no DETECTION** (unwatched directory); **(ii) the in-place edit yields both**.
That is a second, independent argument in (ii)'s favour, and it is ⛔ still not a choice —
Rama's.
