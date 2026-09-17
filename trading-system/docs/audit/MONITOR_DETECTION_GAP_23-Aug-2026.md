# 🔴 ONE FINDING, FOUR MEASURED LEGS — `security_monitor.py` WOULD NOT DETECT WHAT AN INTRUDER WOULD ACTUALLY DO

**23-Aug-2026, 18:08–18:40 IST.** Governed by `docs/PRE_BUILD_REVIEW_GATE.md` (`23ea03d`).
🏷️ **MEASUREMENT + CONSOLIDATION ONLY.** ⛔ No code · ⛔ no permission change · ⛔ no VM write ·
⛔ no push · ⛔ nothing fixed.
📄 Measurement detail: `docs/audit/SUDO_AND_SUDOERS_WATCH_23-Aug-2026.md`.
**Watcher pinned:** deployed `security_monitor.py` sha256 `35e5e8fc…` = repo blob @ `742d9da`,
byte-identical ⇒ ⭐ every line number holds on the live box (`M3`).

**Provenance:** 🔬 measured · 📄 from evidence · 💭 inference · 👤 Rama's.

---

## §0 — THE CONCLUSION, IN ONE SENTENCE

> 🔴 **The two checks that would catch someone already on the box — file integrity and sudo —
> are blind to the actions that matter; the four legs below are one conclusion, not four rows.**

### ⭐ AND THE SEVERITY, FRAMED HONESTLY — THIS IS **DETECTION**, ⛔ NOT **PREVENTION**

🔬 `ubuntu` already holds `(ALL) NOPASSWD: ALL`. ⇒ 💭 **anyone on the box as `ubuntu` already
has everything.** ⛔ None of the four legs below changes what an attacker *can do*. ⭐ They change
**only whether Rama would ever find out.**
⇒ ⭐ **A camera pointed at a wall, ⛔ not an open door.**

### ⚠️ AND WHICH CAMERAS *DO* POINT AT SOMETHING — 🔬 MEASURED, ⛔ NOT ASSUMED

Every alert the monitor has raised in the retained window, one pass, **2026-06-10 → 2026-08-23**
(**972 alerts**):

| alert | count | severity |
|---|---|---|
| Root login-probe spike | **389** | INFO |
| New successful SSH login IP | **260** | WARNING |
| Non-whitelisted sudo command | **96** | INFO |
| Active SSH sessions over limit | **91** | WARNING |
| UNEXPECTED SSH KEY present | **70** | CRITICAL |
| Sensitive file changed: `system_config` | **38** | WARNING |
| NEW SSH KEY DETECTED | **13** | CRITICAL |
| SSH key COUNT exceeds baseline | **7** | CRITICAL |
| Sensitive file changed: `dotenv` | **5** | CRITICAL |
| Failed-login spike | **2** | WARNING |
| Sensitive file changed: `unit_trading` | **1** | CRITICAL |
| 🔴 **`sudoers`** | 🔴 **0** | — |

⇒ ⭐ **THE PERIMETER IS WELL WATCHED.** 4 SSH-facing checks account for **440** alerts; the key
checks alone fired **90** times at CRITICAL. ⛔ The monitor is **not** decorative as a whole, and
saying so would be inaccurate.
⇒ 🔴 **IT IS THE INTERIOR THAT IS BLIND.** Getting *onto* the box is watched. What is done
*once on it* — reading credentials, replacing a watched file, changing the root grant — is not.
⭐ **That is the frame for D-2, and it is more actionable than "the monitor is broken".**

---

## §1 — THE FOUR LEGS

### LEG 1 · 🔴 `/etc/sudoers` has NEVER been watched — not once, on any pass

🔬 `/etc/sudoers` = `440 root:root`. `security-watcher.service` runs **`User=ubuntu`**.
⇒ `sha256_file()` → `None` every pass ⇒ `if cur is None: continue` (`:733-734`).
🔬 **Production artifact** — live `data_store/security_state.json`, 18:08 today: seven real
hashes and **`"/etc/sudoers": None`**.
🔬 Journal, **65 days, all boots**, control firing in the same stream (`13:18:32 unit_trading`
CRITICAL): **0 sudoers lines.** ⛔ **That zero is the instrument being disconnected, ⛔ not silence
that means anything.**

### LEG 2 · 🔴 `/etc/sudoers.d` grants the root access — and is unwatchable as designed

🔬 `sudo -n -l` → **`(ALL) NOPASSWD: ALL`**. ⛔ Not from `/etc/sudoers` (mtime **2024-01-29**,
stock file, never edited) ⇒ 💭 a `/etc/sudoers.d/` drop-in, `mtime=ctime 2026-05-03 12:29:12`
(cloud-init provisioning).
🔬 The directory is in **no** watch list · adding the path is **false protection**
(`sha256_file(<dir>)` → `None`) · 🔴 **and enumeration also fails: `/etc/sudoers.d` is
`750 root:root`, so `ubuntu` cannot even `ls` it.**

### LEG 3 · 🔴 Delete-and-replace is a COMPLETE silent bypass, for every watched file

🔬 `742d9da:scripts/security_monitor.py:730-735` — the statement **order**:

```python
730:        cur = sha256_file(path)
731:        prev = hashes.get(path)
732:        hashes[path] = cur        # <-- baseline overwritten FIRST …
733:        if cur is None:
734:            continue              # <-- … and only THEN is the None skipped
735:        if prev is not None and cur != prev:
```

⇒ a delete sets the stored baseline to `None`; the file may then be **re-created with different
content** and `prev is None` ⇒ **no alert.** ⛔ Applies to all eight paths — `.env`,
`sshd_config`, both units, `system_config.yaml`, `accounts.csv` — ⛔ **regardless of what is in
the list.**

### LEG 4 · 🔴 The sudo check whitelists exactly the commands that read secrets

🔬 `check_sudo_events(cfg, scan_window)` (15-min window, `:1292`); `_SUDO_RE` (`:89`) captures the
`COMMAND=` binary; the whitelist is a **`startswith` on that path** (`:710`).
🔬 `sudo_whitelist_prefixes` contains **`/usr/bin/cat`, `/usr/bin/grep`, `/usr/bin/tail`,
`/usr/bin/systemctl`**, and a *non*-whitelisted sudo is only **INFO**.
⇒ 🔴 **`sudo cat <anything>` raises nothing.** See §2 — this leg is the money path.

---

## §2 — 🔴 ITS OWN ROW: READING THE BROKER CREDENTIALS IS INVISIBLE

### 🔬 What `.env` actually contains — **key names only, ⛔ no values read into any record**

**24 keys**, of which:

| | |
|---|---|
| `ZERODHA_API_KEY_*` | **5** — `D351962` · `DR6114` · `LFL836` · `ZA004` · `ZA005` |
| `ZERODHA_API_SECRET_*` | **5** — same five accounts |
| 🔴 `ZERODHA_TOTP_*` | **5** — the **2FA seeds**, same five accounts |
| `ZERODHA_PASSWORD` · `ZERODHA_USER_ID` | the account login itself |
| `WEBHOOK_SECRET` | the signal-path HMAC secret |
| `TELEGRAM_BOT_TOKEN` + 3 chat/channel ids · `ALERT_SMTP_PASSWORD` | the entire alert channel |

⇒ 🔴 **This is not "the API key and secret". It is complete, unattended access to FIVE live
brokerage accounts — key, secret, password, and the TOTP seed that defeats 2FA — plus the
webhook secret that lets an attacker inject signals, plus the credentials to the alert channel
that would otherwise report it.**

### 🔬 AND READING IT RAISES NOTHING — PROVED BY A **SAME-PASS** CONTROL

⭐ The strongest form of this evidence: two sudo commands seconds apart, **one pass, one window.**

| time | command run as root | monitor's response |
|---|---|---|
| **15:01:03** | `/usr/bin/cat /var/log/auth.log /var/log/auth.log.1` | 🔴 **NOTHING** |
| **15:01:0x** | `/usr/bin/true` — *does nothing at all* | ✅ `15:01:05 ALERT [INFO] Non-whitelisted sudo command — sudo by ubuntu: /usr/bin/true` |

⇒ 🔴 **THE PASS RAN, THE CHECK FIRED, AND IT PICKED THE NO-OP OVER THE FILE READ.** The
discriminator is proven to be the whitelist, ⛔ not a broken check: 🔬 **96** `Non-whitelisted
sudo command` alerts in the window (`cut`, `stat`, `crontab`, `sshd`, `test`, `true`, `cp`,
`sed`). ⭐ **A check with 96 firings and a same-pass negative is ⛔ not a vacuous control.**

### ⚠️ The same whitelist covers more than `cat`

- 🔬 `grep` and `tail` are whitelisted on the same `startswith` rule ⇒ `sudo grep API_SECRET …/.env`
  is equally silent.
- 🔬 **`/etc/shadow` = `640 root:shadow`**; `ubuntu` cannot read it directly, **`sudo cat` can**,
  and 🔬 it appears **0 times** in the live `config/security.yaml` ⇒ ⛔ not watched, ⛔ not
  reported, on either path.
- 🔬 `sudo -n -l` writes **no `COMMAND=` line** to `auth.log` ⇒ 💭 enumerating one's own root
  privileges is invisible to this check **by construction**.

⛔ **NOT FIXED. ⛔ The whitelist was not touched.** ⭐ It feeds **D-2 (c)**.

---

## §3 — `WC-PATTERN #10` · AN ACCURATE OBSERVATION CARRIED A WRONG INFERENCE, AND THE INFERENCE WAS RECORDED AS THE FACT

📄 **05-Aug, recorded:** *"every read-only `ssh` ran UNPROMPTED … while the one `sudo`
state-change … was DENIED, twice (bundled, then bare)"* ⇒ *"the gate held exactly where this
entry says it would not."*

- ✅ **THE OBSERVATION WAS ACCURATE.** A denial did occur, twice, exactly as described.
- 🔴 **THE INFERENCE WAS ABOUT THE WRONG GATE.** 🔬 `Bash(*systemctl stop *)` is in the LOCAL
  **deny** list and outranks `Bash(ssh *)` ⇒ **the request never left the PC.** ⛔ It said
  nothing about the VM, and it was denied whether or not `sudo` appeared in the string.
- ⚠️ **AND IT STOOD FOR 18 DAYS** as a property of a live production VM, because ⛔ nobody
  re-measured a permission that looked settled.

⭐ **Family resemblance:** same shape as *"`N9-10` is recorded against `65b7196`"* and *"the
register describes a system that does not exist"* — a true datum, a wrong reading, and the
reading filed as the datum. ⚠️ **What is new in #10 is the 18-day survival**: the earlier
instances were caught inside a session.

### ⭐ THE OPERATIONAL LESSON, WHICH IS THE DURABLE PART

> ⛔ **A denial observed at the PC is NOT evidence about the VM. Two gates sit in that path, and
> only one of them is the machine.**

---

## §4 — 👤 D-2 RE-PUT. ⛔ THE ORIGINAL QUESTION IS NO LONGER THE QUESTION.

⚠️ The measurement overtook the decision. ⛔ It must be re-put, ⛔ not answered as framed:

- ⛔ **"Add the directory"** — 🔬 **FALSE PROTECTION.** Measured.
- ⛔ **"Enumerate the directory"** — 🔬 **UNBUILDABLE from `User=ubuntu`.** Measured.
- ⛔ **And LEG 3 defeats the control for every watched file anyway**, whatever the list contains.

### ⇒ 👤 THE QUESTION IT NOW IS

> **The integrity monitor cannot see the things that matter. Is it worth repairing — and at what
> privilege?**

| | option | measured cost / effect |
|---|---|---|
| **(a)** | **Fix the ordering at `:732-734`** | ⭐ smallest real improvement; closes delete-and-replace for **all eight** watched paths. ⛔ Does **not** help sudoers. 💭 Pure code, no privilege change |
| **(b)** | **Give the watcher a root-side helper** for the unreadable paths | ⭐ makes `/etc/sudoers` **and** `sudoers.d` visible — the only thing that can. ⚠️ **A privilege change on a live box** |
| **(c)** | **Narrow `sudo_whitelist_prefixes`** so `cat`/`grep`/`tail` on sensitive paths report | ⭐ closes §2 — the credential read. ⚠️ Noisy at first (🔬 the whitelist exists because these are the watcher's *own* helpers) |
| **(d)** | **Accept it, explicitly** | ⭐ record that the interior checks are decorative and **stop treating their silence as evidence.** ⚠️ Legitimate — ⛔ **but it must be a stated ruling, ⛔ never a default** |

### ⚠️ AND ONE QUESTION UNDERNEATH ALL FOUR

> 👤 **Should `ubuntu` hold `NOPASSWD: ALL` at all?**

🔬 It is a **cloud-init provisioning default from 03-May-2026**, ⛔ not a decision anyone made.
💭 Tightening it is a **bigger lever than any monitor fix** — it moves the finding from
*detection* back to *prevention*. ⚠️ ⛔ It is a change to **the box**, ⛔ not to code, and ⛔ it
would break every `sudo` path the operator currently relies on (including this campaign's own
read-only measurements). 👤 **His call, and it is the largest one on this page.**

---

## §5 — ⚠️ TWO SMALLER THINGS, ⛔ RECORDED, ⛔ NOT CHASED

- 🔬 **25 allow entries name `sudo systemctl restart trading-system` and are all DEAD LETTERS**,
  overridden by `deny: *systemctl restart*`. ⭐ Fails **safe** — ⚠️ but the allowlist reads as
  authorising something it cannot perform. ⛔ Debt-ledger line only.
- 🔬 **`NRestarts=72687`** on `security-watcher`, **+1,254** since the 71,433 reading. ⛔ Confirmed
  as the designed 61 s heartbeat, ⛔ not a fault — ⚠️ ⭐ but worth one line that **the box's
  most-restarted unit is the one that watches nothing it most needs to.**

### ⭐ AND ONE LIVE CORROBORATION FOR **D-1**, CAUGHT IN PASSING

🔬 Today at **15:18:11** the root-probe spike fired at **401 probes against a threshold of 400** —
one over. ⭐ That is D-1's *"set inside the noise band"* finding happening in production while the
measurement was being written, ⛔ and it is the single most economical illustration of it.

---

## 🏷️ STATUS

🏷️ **MEASURED · CONSOLIDATED · ⛔ NOTHING FIXED · ⛔ NOT PUSHED.** ⛔ No VM write; the only
privileged call in this pass was `sudo -n -l`, which executes nothing. ⛔ No `.env` value was read
into any record — key names only.
⇒ 👤 **D-2 as re-put above, plus the `NOPASSWD` question, are Rama's. D-1, D-3 and D-4 stand
unanswered from the earlier block.**
