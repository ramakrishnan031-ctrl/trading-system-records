---
name: q8-vm-security-forensics-14jul
description: "Q8 VM security BREACH INVESTIGATION (read-only, 14-Jul off-market) — NO breach. Foreign-SSH-in-time-lock premise refuted; time-lock is a copy-gate not an SSH gate; the \"unexpected key\" was Rama's own rotation."
metadata: 
  node_type: memory
  type: project
  originSessionId: 20882031-c334-404e-8d4c-fe55ea018ce4
---

**Q8 = a breach investigation, not a hardening task. VERDICT: NO BREACH (high confidence). READ-ONLY, changed nothing.** Report: `docs/audit/q8_vm_security_breach_forensics_14jul2026.md`. Recovery pre-check first: main==VM-bare==`2dc69d5`, tree clean (deploy completed pre-disconnect).

**Q1 — broker creds (ZERODHA_* in `.env`) exposed? NO (high confidence).** Not compelled to rotate. Rests on: credential exposure needs an unauthorized `ubuntu`/`root` session, and that would appear in ≥1 of 5 independent+intact+corroborating records — appears in NONE. `.env` `0600 ubuntu:ubuntu`, mtime/ctime Jul 5 22:22 (unchanged), auditd `env_change` 0 events. **Honest caveat:** auditd watches `.env` `-p wa` (**writes/attr only — NOT reads**); atime is relatime (unreliable); the "NO" is by *bounding possible readers to Rama*, not a positive read-audit. Logs intact → "we would have found it" is fair.

**KEY FACTS (all Airtel-India, key-only):** 2,246 successful SSH logins across auth.log (→Jun 21) + wtmp (→May 3), **100% publickey / 100% user=ubuntu / 100% Bharti-Airtel-India dynamic IPs** (157.48-51.x·157.49-50.x·106.192.x·223.237.x·110.224.x·27.60-61.x·171.79.x); **0 password, 0 keyboard-interactive, 0 root.** 8 ED25519 fps ever authenticated, ALL Airtel-sourced = Rama's successive rotations (uDRN8·DrHT9·vsjJ8·BRi6·WcC0=rama@DESKTOP-029USHU·XrYwY·9xTid·wPqEm). sshd: `PermitRootLogin no` + `PasswordAuthentication no`.

**The "foreign IP" = a defeated bot.** Only non-India address ever = `45.198.224.120` (Stockholm, Vpsvault.host) — **1,402 failed root + 482 failed ubuntu + 327 btmp, 0 success.** It sits in the security-watcher `geoip_cache` → likely the spark for the "foreign IP" alarm. fail2ban: 35,319 failed / 450 banned / 0 success (working).

**The "unexpected key" was RAMA.** `authorized_keys` changed Jul 13 09:16 to sole key `BRi6…` "Trading VM"; baseline (`ssh_key_baseline.json` + `security.yaml`) still `uDRN8…` → **un-baselined rotation, NOT intrusion.** Proof: his `bash_history` (intact, 767 lines, ends Jul 13 09:17) shows repeated `nano ~/.ssh/authorized_keys`+`chmod 600`; his wtmp session `157.51.61.99` spans 09:14–09:17 bracketing the edit; BRi6 authenticates only from his Airtel IPs. **security-watcher DETECTED it** (`alerted: authkeys:unexpected:BRi6`, CRITICAL sentinels delivered 09:15:58–09:17:01) → that alert + the copy-gate-as-SSH-lock misconception = the whole "foreign SSH session in the time-lock" premise.

**Q4 — the "time-lock" is a COPY-GATE, not an SSH gate (category error, not a failure).** `scripts/copy_gate.py` gates VM→PC *file copies* (scp/sftp/rsync shims), 18:00–08:00 absolute. SYSTEM_MAP: "git push (ssh) + interactive ssh are NOT wrapped." **There is NO SSH time/network restriction at all** — no Match block, no pam_time; SSH is 24/7 on `0.0.0.0:22`, key-only + fail2ban. ⚠️ **Do NOT add an 18:00–08:00 SSH lock — that's exactly Rama's off-market deploy window (would lock the operator out).**

**Q3 — box clean today:** no persistence — authorized_keys clean (opc/root = Rama's key OCI-`exit 142`-neutered, passwords Locked, opc not sudo); cron = documented jobs only; 0 systemd changes/30d; listeners = 22/**111 rpcbind [hardening item]**/8500(lo GUI)/443(Tailscale); `dpkg --verify` openssh/coreutils/pam/sudo CLEAN; sudoers = OCI+cloud-init only (incl std `ubuntu NOPASSWD:ALL`); only recent SUID = `ssh-keysign` Jul 9 (legit openssh auto-update). **Rootkit scanners ALL ABSENT → formal scan NOT run (proposed, installing=a change).** copy_audit empty since Jun 20; auditd copy_attempt=0. NB the live "non-whitelisted sudo" INFO alerts tonight = MY forensic sudo commands (proves the monitor is live).

**KEY INSIGHT for future work — `ubuntu ≡ root` on this box** (only login user + `NOPASSWD:ALL` sudo). So "make `.env` root-only" buys little (ubuntu can `sudo cat`); the leverage is keeping unauthorized parties off `ubuntu` (Tailscale-only SSH + key passphrase), not file modes.

**Proposed controls (PROPOSE-not-apply; recovery = OCI serial console): C1** re-baseline key (`approve_ssh_keys.py --apply`, do first, resets tripwire) · **C2** SSH→Tailscale-only + close 0.0.0.0:22 (highest value; already has Tailscale) · **C3** key passphrase+agent (real residual risk = key theft from PC; `trading_vm_secure` has none) · **C4** Telegram-per-login · **C5** close rpcbind:111 · **C7** read-only rkhunter/chkrootkit after install. **What Rama does himself:** confirm BRi6 is his → re-baseline; broker-key rotation optional/not-emergency. See [[unpushed-pending-deploy-ledger]] · [[migration-on-open-rule-14jul]] · [[pb01-shadow-deploy-14jul]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 302 B (budget 300 B). The index now carries a hook and this link.

- [Q8 VM SECURITY — NO BREACH (14-Jul, read-only)](q8_vm_security_forensics_14jul.md) — creds not exposed; only foreign IP = a defeated Stockholm bot + Rama's own Jul-13 key rotation (BRi6); "time-lock" = `copy_gate.py` not SSH; never add an 18:00-08:00 SSH lock. [[q8-vm-security-forensics-14jul]]
