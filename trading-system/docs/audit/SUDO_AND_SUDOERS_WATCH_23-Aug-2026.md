# §1 — `sudo -n` SUCCEEDS · DID A CRITICAL EVER FIRE FOR SUDOERS? · IS `sudoers.d` IN NI-15's BLIND SPOT?

**23-Aug-2026, 18:08–18:20 IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **MEASUREMENT ONLY — READ-ONLY.** ⛔ No permission changed · ⛔ no sudo access added or
removed · ⛔ nothing written on the VM · ⛔ no push.

**Provenance:** 🔬 measured · 📄 from provided evidence · 💭 inference · 👤 Rama's.

**Deployed watcher pinned:** `sha256(/home/ubuntu/systems/trading-system/scripts/security_monitor.py)`
= `35e5e8fcdf71ed…` = **the repo blob at `742d9da`, byte-identical.** ⇒ ⭐ every line number
below holds on the live box (`M3` satisfied).

---

## 🔴 THE HEADLINE — THE ANSWER IS WORSE THAN THE CARD'S HYPOTHESIS

The card asked whether a sudoers change would have been *invisible because `sudoers.d` is a
directory.* 🔬 **The measurement says the blind spot starts one step earlier:**

> 🔴 **`/etc/sudoers` HAS NEVER BEEN WATCHED — NOT ONCE, ON ANY PASS.**
> It is mode `440 root:root`; the watcher runs as `User=ubuntu`. `sha256_file()` returns
> `None` on every pass ⇒ `check_watched_files` hits `if cur is None: continue`
> (`security_monitor.py:733-734` @ `742d9da`) and skips it, silently, forever.

**The production artifact, read from the live state file at 18:08 today**
(`data_store/security_state.json`):

```
/etc/ssh/sshd_config                         -> '64325541513d…'
/etc/ssh/sshd_config.d/99-trading-security…  -> 'c2c97040bbc8…'
/etc/sudoers                                 -> None          🔴
/etc/systemd/system/security-watcher.service -> '78ea95f0eb87…'
/etc/systemd/system/trading-system.service   -> 'faa2cac56bc2…'
…/.env                                       -> 'ac3ad5f82c6b…'
…/config/accounts.csv                        -> 'b012e1ac707b…'
…/config/system_config.yaml                  -> '2d5c4190b987…'
```

⭐ Seven real hashes and **one `None`** — and the `None` is the highest-value file on the box.
⇒ 🔴 This is the `V5` **tautological-check** class, on production: the row exists, it reads as
coverage, and **it has no failing input.** ⛔ It is not "a check that has not fired"; it is a
check that **cannot** fire.

### 🔬 Readability of every watched path, measured AS the watcher's user

| watched path | mode / owner | readable by `ubuntu`? |
|---|---|---|
| `/home/ubuntu/.ssh/authorized_keys` | `600 ubuntu:ubuntu` | ✅ (handled by `check_authorized_keys`) |
| `/etc/ssh/sshd_config` | `644 root:root` | ✅ |
| 🔴 **`/etc/sudoers`** | **`440 root:root`** | 🔴 **NO** — `test -r` false; `PermissionError: [Errno 13]` |
| `/etc/systemd/system/trading-system.service` | `644 root:root` | ✅ |
| `/etc/systemd/system/security-watcher.service` | `644 root:root` | ✅ |
| `…/.env` | `600 ubuntu:ubuntu` | ✅ |
| `…/config/system_config.yaml` | `664 ubuntu:ubuntu` | ✅ |
| `…/config/accounts.csv` | `664 ubuntu:ubuntu` | ✅ |

🔬 `systemctl show security-watcher` → **`User=ubuntu`, `Group=ubuntu`**.

---

## S-1 · 🔬 DID A `Sensitive file changed` EVER FIRE FOR SUDOERS?

**🔬 NO. ZERO — in a window in which the same check fired 44 times for other files.**

**SEARCH WIDTH — stated beside the zero (`feedback_absence_needs_wide_check`):**
`journalctl -u security-watcher --since 2026-06-10 --grep …`, on the VM.
Retained journal: **2026-06-10T05:30 → 2026-08-23T18:11 IST**; the oldest `security-watcher`
line is **2026-06-19T23:19** ⇒ effective width **≈ 65 days, continuous, across all boots**.

| query | result |
|---|---|
| `--grep "Sensitive file changed"` | 🔬 **44 alerts** — `system_config` (WARNING, many), `dotenv` (CRITICAL ×5), `unit_trading` (CRITICAL ×1) |
| `--grep "sudoers"` | 🔴 **0 — `-- No entries --`** |
| **CONTROL (must fire):** `unit_trading` CRITICAL, today | ✅ **PRESENT** — `2026-08-23T13:18:32,089 … ALERT [CRITICAL] Sensitive file changed: unit_trading — /etc/systemd/system/trading-system.service content changed (sha256 7ad85a562ae2→faa2cac56bc2)` |

⭐ The control is in the *same* query stream as the zero ⇒ **the search could have found a
sudoers alert had one been emitted.** The check itself is well exercised: 44 firings, 5 of
them CRITICAL, over 65 days.

⚠️ **⛔ BUT THE ZERO PROVES NOTHING ABOUT SUDOERS.** Given the state file shows `None`, the
correct reading is **"the instrument was disconnected"**, ⛔ not **"nothing happened"**.
🔴 **This watcher cannot tell us whether `/etc/sudoers` ever changed.** Independent evidence
below is what settles that.

---

## S-2 · 🔬 WHAT ACTUALLY GRANTS IT — AND IS `sudoers.d` IN THE BLIND SPOT?

**🔬 `sudo -n -l` on the VM** (read-only: sudo reports its own policy; it executes nothing):

```
User ubuntu may run the following commands on trading-system:
    (ALL : ALL) ALL           <- the %sudo group rule in /etc/sudoers (PASSWORD required)
    (ALL) NOPASSWD: ALL       <- a /etc/sudoers.d/ drop-in — UNRESTRICTED, PASSWORDLESS ROOT
```

🔬 `id` → `uid=1001(ubuntu) … groups=…,27(sudo),…`; `getent group sudo` → `sudo:x:27:ubuntu`.

🔬 **The grant is NOT in `/etc/sudoers`.** That file's **`mtime = 2024-01-29 22:39:56`** — the
stock distro file, **content never edited**; `ctime = 2026-04-14 17:33:19` (base-image
metadata). ⇒ 💭 the `NOPASSWD: ALL` line lives in **`/etc/sudoers.d/`**.

🔬 **`/etc/sudoers.d` = mode `750 root:root`, TYPE=directory, `mtime = ctime = 2026-05-03 12:29:12`** —
the same instant band as `/etc/passwd` (`12:29:07`) and `/etc/group` (`12:29:07`).
⇒ 💭 **cloud-init at instance provisioning, 03-May-2026** — ~3.5 months old, and **6 weeks
before the journal window even opens.**

### ⇒ 🔬 THE PRIVILEGE POSTURE DID NOT CHANGE

| corroborating measurement | result |
|---|---|
| `auth.log` sweep for `visudo\|usermod\|gpasswd\|sudoers`, **5 rotated files, 2026-07-26 → 2026-08-23 (28 days)** | 🔬 **0 hits** |
| `/etc/sudoers` content mtime | 🔬 **2024-01-29** — unchanged |
| `/etc/sudoers.d` mtime | 🔬 **2026-05-03 12:29:12** — provisioning, unchanged since |
| VM uptime | 🔬 50 days (boot ≈ 2026-07-04) |

⭐ ⇒ **`sudo -n` almost certainly succeeded on 05-Aug too.** ⛔ Nothing was silently loosened.
⚠️ **Caveat, stated:** the 28-day `auth.log` window and the 65-day journal window do **not**
reach back to 03-May. 💭 The mtime/ctime evidence does, and it is the stronger source.

### 🔴 AND YES — `sudoers.d` IS SQUARELY IN NI-15's BLIND SPOT, TWICE OVER

1. 🔬 **`/etc/sudoers.d` appears NOWHERE in the live watch list.** `grep -n sudoers
   config/security.yaml` on the VM returns exactly **one** line — `/etc/sudoers` — and no
   directory.
2. 🔬 **Adding the path would be false protection**, exactly as NI-15 measured:
   `sha256_file(<dir>)` → `None` → `continue`.
3. 🔴 **AND THE ENUMERATION FIX ALSO FAILS AS BUILT.** `/etc/sudoers.d` is `750 root:root`:
   `ls` as `ubuntu` → **`Permission denied`**. ⇒ ⛔ **"enumerate the directory" cannot work
   from `User=ubuntu`** — a real fix needs a privilege change or a root-side helper, ⛔ not a
   config line. ⭐ **This is new: NI-15's own proposed remedy is itself unbuildable as the
   watcher stands.**

⇒ 🔴 **The single file that grants unrestricted passwordless root on a live-money box is
invisible to the integrity monitor, has always been invisible, and the fix NI-15 was about to
recommend would not have made it visible.**

---

## S-3 · 🔬 RECONCILING THE TWO EARLIER "DENIED" READINGS — **NEITHER WAS THE VM**

📄 The 05-Aug memory banner records: *"every read-only `ssh` ran UNPROMPTED … while the one
`sudo` state-change — `ssh trading-vm 'sudo systemctl stop trading-system.service'` — was
DENIED, twice (bundled, then bare)"*, and offered two candidate causes: **(a)** the allowlist
was narrowed, or **(b)** `sudo` is the discriminator.

🔬 **Measured tonight in `.claude/settings.local.json` — it is NEITHER. There is a third,
explicit cause, and it is command-shaped, ⛔ not privilege-shaped:**

```
permissions.allow : 533 entries   (includes  Bash(ssh *)  -> read-only ssh runs unprompted ✅)
permissions.ask   :   0 entries
permissions.deny  :  16 entries, including:
        Bash(*systemctl stop *)        PowerShell(*systemctl stop *)
        Bash(*systemctl start *)       PowerShell(*systemctl start *)
        Bash(*systemctl restart*)      PowerShell(*systemctl restart*)
```

⇒ 🔬 `ssh trading-vm 'sudo systemctl stop trading-system.service'` matches
**`Bash(*systemctl stop *)`** — a **deny** rule, which outranks `Bash(ssh *)`. It is denied
**bundled and bare**, which is exactly the doubled denial the banner recorded, and it is
denied **whether or not `sudo` appears in the string**.

| | |
|---|---|
| what was denied | 🔬 **the local Claude Code permission gate**, on the substring `systemctl stop` |
| what was NOT denied | 🔬 **the VM.** The request never left the PC |
| candidate (a) "allowlist narrowed" | 🔬 **refuted** — `Bash(ssh *)` is present and broad |
| candidate (b) "`sudo` is the discriminator" | 🔬 **refuted** — 88 allow entries contain `sudo`; the discriminator is `systemctl stop\|start\|restart` |
| ⇒ did the VM's posture change? | 🔬 **No evidence it did, and mtime evidence that it did not** |

⭐ **The stale-record correction cuts the other way from how it was carried.** Memory framed
this as *"a permission record that expired"*. 🔬 It is both worse and better than that: the
05-Aug **observation** was accurate, but the **inference drawn from it** (*"the gate held
exactly where this entry says it would not"*) was about **the wrong gate entirely**. ⛔ A local
deny rule was read as a property of the live VM, and stood for 18 days.

### ⚠️ FOUND EN ROUTE, ⛔ not chased

- ⚠️ **25 allow entries name `sudo systemctl restart trading-system`** — all of them are dead
  letters, overridden by `deny: *systemctl restart*`. ⭐ Fails **safe**, but the allowlist
  reads as authorising a restart it cannot perform. 💭 Worth a debt-ledger line, ⛔ not a
  change tonight.
- 🔴 **`sudo_whitelist_prefixes` includes `/usr/bin/cat`, `/usr/bin/grep`, `/usr/bin/tail`,
  `/usr/bin/systemctl`** ⇒ 🔬 `sudo cat …/.env` (or `/etc/shadow`) produces **no finding at
  all**, and a *non*-whitelisted sudo is only **INFO**. 🔬 Confirmed live: this session's own
  `sudo cat /var/log/auth.log …` at **15:01:03** is in `auth.log` and raised nothing.
  ⛔ Recorded, ⛔ not fixed.
- ⚠️ 🔬 `NRestarts=72687` on `security-watcher` (memory records **71,433**) — the unbounded
  restart loop is still running, ⛔ unchanged, **+1,254** since it was last counted.

---

## 🔴 A SECOND CODE FINDING, LARGER THAN "DELETE IS SILENT"

🔬 Read at `742d9da:scripts/security_monitor.py:730-735` — the **order** of two statements:

```python
730:        cur = sha256_file(path)
731:        prev = hashes.get(path)
732:        hashes[path] = cur        # <-- the baseline is overwritten FIRST …
733:        if cur is None:
734:            continue              # <-- … and only THEN is the None skipped
735:        if prev is not None and cur != prev:
```

⇒ 🔴 **A delete does not merely fail to alert — it DESTROYS the stored baseline**
(`hashes[path] = None`). On a later pass the file can be **re-created with different content**
and `prev is None` ⇒ `if prev is not None` is **False** ⇒ 🔴 **no alert.**

⇒ 🔴 **`rm` then write = a complete, silent bypass of the integrity watch, for EVERY watched
file** — `.env`, `sshd_config`, both unit files, `system_config.yaml`, `accounts.csv`.
⭐ NI-15 recorded *"deletion is invisible"*. 🔬 The measured behaviour is **delete-and-replace
is invisible**, which is the whole point of the control.
🏷️ **LATENT** (needs an actor with write access), ⛔ not live. ⛔ Recorded, ⛔ not fixed —
`docs/PRE_BUILD_REVIEW_GATE.md` governs and this is a behaviour change.

---

## 🏷️ STATUS

🏷️ **MEASURED · ⛔ NOT FIXED · ⛔ NOT PUSHED.** ⛔ No permission on the VM was modified; the
only privileged call made was `sudo -n -l`, which executes nothing.
⇒ 👤 **All of it feeds D-2, which is Rama's.**
