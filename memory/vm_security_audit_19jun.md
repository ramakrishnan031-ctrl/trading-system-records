---
name: vm_security_audit_19jun
description: "Pre-build read-only audit for a VM Security Manager — current SSH/access, monitoring, integration points, copy-protection & approval feasibility on the Oracle Cloud VM"
metadata: 
  node_type: memory
  type: project
  originSessionId: 34eb8dba-9799-4234-a8dc-bb8ca1411fa8
---

**VM SECURITY MANAGER PRE-BUILD AUDIT (19-Jun-2026, read-only).** Oracle Cloud VM
(host 161.118.187.249, internal 10.0.0.114, user ubuntu). What EXISTS vs NEEDS BUILDING.

## A — SSH / access (current)
- sshd (effective `sshd -T`): **passwordauthentication no** (KEY-ONLY ✅), pubkey yes,
  kbdinteractive no, permitemptypasswords no, **permitrootlogin without-password** (key-only
  root; no root keys present so effectively off — could tighten to `no`), **maxsessions 10**,
  maxstartups 10:30:100, **forcecommand none**, **x11forwarding yes** + **allowtcpforwarding yes**
  (tunneling on — minor hardening), clientaliveinterval 0 (no idle timeout), no AllowUsers/Groups.
  Subsystem sftp = `/usr/lib/openssh/sftp-server` (sftp/scp enabled).
- authorized_keys: **exactly 1 key** — ED25519 `SHA256:DrHT9VviCBFmeg+RBwO3wZhw+EwzhjRD/G2ceKntEqM`
  comment `rama@DESKTOP-029USHU`. BOTH PC PowerShell and VS Code Claude use this SAME key
  (`trading_vm_secure`). **No unknown keys.** ✅
- sudo: **`(ALL) NOPASSWD: ALL`** for ubuntu → any SSH access = instant root (high blast radius).
  sudoers.d = Oracle Cloud defaults (oca-vss, oracle-cloud-agent, cloud-init).
- sessions: `who` empty (audit uses non-PTY exec); `last` shows Rama's dynamic IPs; 3 established
  :22 conns during audit (Rama + Claude).

## B — monitoring / logging (mostly ABSENT)
- **auth.log EXISTS**: `/var/log/auth.log` (syslog:adm 640, weekly rotate, ~12 MB). Readable w/ sudo,
  fully parseable. Logs all sshd accept/disconnect + sudo COMMANDs. ✅ monitorable.
- **🚩 20,457 "Invalid user" + heavy brute-force** (Jun 14 00:00 → Jun 19 22:43, ~3.5k/day) from
  **499 distinct IPs** (distributed botnet). Top: 103.204.167.14 (1496), 218.148.106.182 (1091),
  59.30.138.58 (1039), 49.254.0.82 (970), 107.174.212.19 (929) — mostly KR/CN ranges. Top tried
  usernames: admin(1232), admin1(1078), user(774), debian, + name-dictionary (veena/seema/renu...).
  Only 1 "Failed password"; 648 "Accepted publickey" (legit, all from Rama IP 157.51.57.3). Root
  probes from foreign IPs (45.148.10.141, 188.241.61.189) hit preauth. Key-only auth blocks all of
  it, but UNMITIGATED noise/attack surface → fail2ban = biggest quick win.
- **NO security tooling**: fail2ban inactive/not-installed, auditd inactive/not-installed, ufw inactive,
  iptables default policy ACCEPT (only Oracle InstanceServices + dormant ufw chains). **No file-integrity**:
  inotifywait / auditctl / aide / ausearch ALL MISSING.

## C — integration points (ALL EXIST — strong reuse)
- **System Manager** (`scripts/system_manager.py`): `run()` calls a list of 8 isolated check lambdas →
  add a 9th `security_check()` returning a `CheckResult` + append to specs/titles. `_send()` already does
  Telegram (`TelegramNotifier.from_env(config_dir=...)`) + CRITICAL→sentinel→email. record_heartbeat,
  trigger_soft_kill present. [[task_5_system_manager]]
- **Cron Officer** (`config/cron_registry.yaml` source of truth): add a `security_*` cron job + heartbeat.
  [[task_3_cron_officer]]
- **Alerts**: `TelegramNotifier.from_env` (proven standalone — [[cron_env_export_fix]] probe = NOTIFIER OK)
  + `alerts/critical.write_critical_sentinel()` → `data_store/critical_alert_*.flag` → alert-watcher email
  `[LFL836] <SEV> — <title>`. Reusable as-is by a standalone security script.
- **Watcher pattern**: `alert-watcher.service` (periodic-oneshot: run→exit0→systemd restart) and
  `token-watcher.service` (bash loop). A `security-watcher.service` models on either.

## D — copy protection (feasible, needs building)
- SCP today: code deploy = **git push → bare-repo post-receive hook** (no scp). Direct scp DOES exist:
  `scripts/copy_token_to_vm.bat` (token PC→VM) + ad-hoc Claude scp (docx/probes). ubuntu shell `/bin/bash`.
- Intercept: **ForceCommand none**, no scponly/rssh (deprecated). Options: `Match`+ForceCommand wrapper
  (careful — would also hit git-over-ssh / Claude scp), or sftp logging. **sftp logging OFF** (no `-l`)
  → enable `Subsystem sftp internal-sftp -l INFO -f AUTHPRIV` to log INBOUND file ops (PC pulling FROM VM).
- VM→PC copy detection: VM is the *client* for outbound scp → sshd can't see it; needs **auditd execve**
  of scp/sftp, shell-history, or **egress firewall** (currently NONE — OUTPUT policy ACCEPT, ufw inactive).
- Time windows: **pam_time available but NOT enabled for sshd** (only commented in pam.d/login,su).
  Feasible via `/etc/security/time.conf` + pam.d/sshd, or a watcher that kills out-of-window sessions.

## E — Telegram/email for security
- Send path ✅ (from_env + sentinel, proven). **NO inbound Telegram anywhere** (grep: no getUpdates /
  callback_query / long-poll / InlineKeyboard / setWebhook) — notifier is **send-only**. An interactive
  Telegram approval (button/reply) is NET-NEW (build a getUpdates long-poll consumer). **Recommend for
  Phase 1: time-limited token-file approval** (operator drops an authorizing flag/token with TTL) — far
  simpler, no inbound bot.

## Recommended Phase-1 build (monitoring + alerts)
EXISTS to reuse: auth.log parse, TelegramNotifier.from_env, write_critical_sentinel, System-Manager
9th-check slot, cron registry, watcher-service pattern. BUILD/INSTALL: (1) `fail2ban` (brute-force —
biggest quick win vs the 20k attempts); (2) `auditd` OR `inotify-tools` to watch
`.env`/`config/`/`~/.ssh/authorized_keys` changes; (3) a `security_check()` (new authorized_keys,
sudo events, failed-login spikes, sessions from new IPs, sensitive-file mtimes) wired into System
Manager + a `security-watcher.service`. OS constraints: NOPASSWD sudo (watcher can self-install, but
is also the risk); auth.log needs sudo/`adm` group; OCI cloud Security Lists are the real ingress
control (host iptables open); ForceCommand/scp-restriction must be Match-scoped or it breaks
git-over-ssh + Claude scp. Related: [[project_vm_architecture_locked]], [[feedback_ssh_automation]].
