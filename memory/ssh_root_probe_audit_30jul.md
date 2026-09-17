---
name: ssh-root-probe-audit-30jul
description: "30-Jul-2026 SSH audit: ZERO root logins and zero non-publickey/ubuntu logins across both corpora, PermitRootLogin no confirmed via sshd -T on the running daemon. The 400/hr root-probe threshold sits INSIDE the noise band (max ever 516) so it fires ~1.6x/day by design. Auth-log retention ceiling is 50 days. /root/.ssh/authorized_keys is NOT empty, contra the hardening config's own comment."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 91948a89-4eda-4cd0-ac78-c3b773765042
  modified: 2026-07-30T05:58:36.914Z
---

# SSH / root-probe audit — 30-Jul-2026. Read-only, nothing changed.

## ✅ ZERO root logins — and here is the WIDTH that makes the zero mean something
- `/var/log/auth.log*` (5 files): **2026-06-28 -> 2026-07-30**, 32.4 d, 418,332 lines.
- journald `_COMM=sshd` (3.9 GB persistent): **2026-06-10 -> 2026-07-30**, 50 d.

`Accepted * for root` **0** (both corpora) · sshd `session opened for user root`
**0** · `Failed password/publickey for root` **0/0** · `User root from` **0** ·
**any `Accepted` that is not `publickey` for `ubuntu`: 0 of 4,726.** The only
root sessions are **5,559 from `CRON[`** — local, expected. 244 distinct accepted
source IPs = Rama's mobile/CGNAT rotation, not 244 actors.

## ⛔ RETENTION CEILING = 50 DAYS. "EVER" IS UNANSWERABLE.
logrotate is `weekly` + `rotate 4` ⇒ auth.log can never hold >~5 weeks; journald has
vacuumed to 3.9 GB. **The VM predates 10-Jun (root key mtime 3-May; audits from
18-May) ⇒ ~3-May..10-Jun is UNRECOVERABLE.** ⭐ For a future "ever", ship the logs —
retention tuning cannot recover the past. [[feedback-absence-needs-wide-check]]
⚠️ **A grep of auth.log for `Accepted` matches PRIOR AUDITS' OWN sudo COMMAND= lines**
— 14 false hits, self-referential. journald `_COMM=sshd` is the clean corpus.

## ✅ PermitRootLogin no — CONFIRMED, and the RUNNING daemon has it
`sudo sshd -T` (resolves Include + drop-ins + Match) reports **`permitrootlogin no`
· `passwordauthentication no` · `kbdinteractiveauthentication no` ·
`permitemptypasswords no`** · maxauthtries 6 · port 22.
⛔ **`/etc/ssh/sshd_config:42` only has it COMMENTED** — the real setter is
`/etc/ssh/sshd_config.d/99-trading-security.conf:13`. **Grep the main file alone and
you get the wrong answer; `sshd -T` is the only authoritative read.**
⭐ **Disk-vs-running check:** config mtime 19-Jun 23:35 · `ssh.service` active since
**28-Jul 06:02:38** (a package upgrade restarted it, mid-uptime) ⇒ config predates
the start, so it IS loaded. **That upgrade class is exactly what could silently
re-enable root login, and NOTHING watches for it.**

## ⚠️ /root/.ssh/authorized_keys IS NOT EMPTY — the config comment is wrong
99-trading-security.conf says *"No root keys exist … so this is zero-risk."* **False:
1 line, 266 B.** But it is the **cloud-init decoy** —
`no-port-forwarding,…,command="echo 'Please login as the user \"ubuntu\"…';exit 142"`.
⇒ **LATENT, triple-blocked**: PermitRootLogin no · forced command (no shell) · root
password **locked** (`passwd -S root` = `L`). ⛔ Nothing to do; do NOT read the
comment as the justification for the setting. ⚠️ The embedded key is
`rama@DESKTOP-029USHU` (mtime 3-May) while `ubuntu`'s is a *different* key
`trading-vm` ⇒ root holds a **stale copy of a rotated-out key**.

## ⛔ THE 400/hr THRESHOLD IS INSIDE THE NOISE — no number fixes the concept
`config/security.yaml:22 root_probe_spike_threshold: 400`. Matcher is
`_ROOT_PROBE_RE = "authenticating user root"` (`security_monitor.py:88`), which
matches `Connection closed by authenticating user root <ip> [preauth]`.
**Probes/hour over 779 hours: min 3 · p25 29 · p50 57 · p75 185 · p90 361 · p95 413
· p99 467 · MAX 516 · mean 124.** Total 96,764. **400 sits between p90 and p95 ⇒
breached 50/779 h = 6.4% = ~1.6 alerts/day.** Every hour of 32 days has probes —
**a continuous floor, not an event.**
⭐⭐ **Volume cannot indicate compromise here**: 96,764 probes produced 0 successes
and 0 auth failures — with root off + passwords off they never reach an auth
decision. **The metric measures internet weather, not exposure.** Raising 400->600
silences it without making it mean anything.
⚠️ Dedup key is `rootspike:{now:%Y%m%d%H}` (`:697`) — **rotates on the clock hour, so
the 6 h cooldown and the (1.0,4.0,28.0) backoff ladder can NEVER engage.** One
full-severity alert per breaching hour, forever.
⚠️ **fail2ban is active but catches ~none of it** — jail `sshd`, total failed 2,718 /
banned 63 / **currently 0**, against 96,764 probes. Its default filter does not match
the preauth-close line (needs `mode = aggressive`). ⇒ **fail2ban is the lever for
fewer PROBES; the threshold is only a lever for fewer ALERTS.**

## ❓ REGISTERED, UNEXPLAINED — DO NOT RETUNE BEFORE UNDERSTANDING IT
**04:29 and 04:36 on 30-Jul fall in the SAME clock hour**, which the
`rootspike:%Y%m%d%H` key should have collapsed into ONE alert. Either a different
rule produced one of them, or the presence ledger evicted the entry
(`_LEDGER_MAX_ENTRIES = 500`, and the comment says "rootspike:/failspike: keys
rotate hourly" ⇒ they are the churn source). ⛔ **An alert system that
double-fires when its own dedup says it cannot is worth understanding BEFORE the
threshold is retuned** — otherwise a new number gets credited for a fix it did not
make. [[feedback-verify-rc-not-output]]

## 📋 PROPOSED, NOT APPLIED (awaiting Rama) — see the BOARD
Replace volume with **invariants whose measured base rate is 0 over 50 d**: any
`Accepted` not publickey/ubuntu · any `Accepted for root` · **`sshd -T` drift on
permitrootlogin/passwordauthentication/kbdinteractive** (the missing one — it watches
the control that makes the probes harmless). If a volume rule is kept: **single-IP
>250/hr** (measured single-IP max **192**, p99.9 82) and/or **total >1500/hr** (2.9x
the all-time max). ⛔ **NOT 600** — silent today but only 16% over observed max.
