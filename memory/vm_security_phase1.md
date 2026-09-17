---
name: vm_security_phase1
description: "VM Security Manager Phase 1 (monitoring + alerts) — built + deployed 19-Jun; security_monitor.py + fail2ban + auditd + security-watcher.service; alert-only, never blocks"
metadata: 
  node_type: memory
  type: project
  originSessionId: 34eb8dba-9799-4234-a8dc-bb8ca1411fa8
---

**VM SECURITY MANAGER PHASE 1 — DEPLOYED 19-Jun-2026** (commits a701b0d→fcfa9a8).
Alert-ONLY (never blocks access — key-only SSH is the gate). Built from [[vm_security_audit_19jun]].

## Artifacts (in git)
- `scripts/security_monitor.py` — standalone watcher, 7 isolated checks: (1) new/changed
  `authorized_keys` CRITICAL, (2) non-whitelisted sudo INFO, (3) failed-login spike WARNING
  (>500/hr), (4) NEW successful-login IP WARNING ("was this you?" — Rama's IPs are dynamic),
  (5) sensitive-file CONTENT-HASH change (CRITICAL/WARNING; hash not mtime so no-op deploys don't
  false-fire), (6) active SSH session count > max (WARNING, alert-not-block), (7) root-probe spike.
  Reads `/var/log/auth.log` directly (ubuntu ∈ group `adm`). State `data_store/security_state.json`
  (key hash, 38 seeded login IPs, file hashes, alert-dedup ledger w/ 6h cooldown). Modes:
  `--watch` (service) / `--report` / `--baseline`. Alerts: `TelegramNotifier.from_env` + CRITICAL
  `write_critical_sentinel` → alert-watcher email. Never crashes (every check try/except; always exit 0).
- `config/security.yaml` — **standalone** (NOT system_config.yaml — that loader is `extra="forbid"`,
  a security key there would break main.py). Holds baseline `expected_key_fingerprint:
  SHA256:DrHT9VviCBFmeg+RBwO3wZhw+EwzhjRD/G2ceKntEqM`, thresholds, sudo whitelist (exact VM paths).
- `deploy/systemd/security-watcher.service` — `Type=simple`+`Restart=always`+`RestartSec=60` (~60s
  periodic; systemd REFUSES `Restart=always` on `Type=oneshot` — must be simple). Model = alert-watcher.
- `deploy/security/jail.local` (fail2ban) + `trading-security.rules` (auditd). 15 unit tests (all green).

## Live VM state (OS-level, NOT git)
- **fail2ban** installed+enabled+active; `/etc/fail2ban/jail.local` (sshd jail, bantime 3600, maxretry
  5, `ignoreself`, reads auth.log, NO static IP allow-list). Pre-tested with `fail2ban-regex`: 20,507
  attacker lines match, **0 management IPs (157.51.*/106.192.*) in the bannable set** → no self-lockout.
  Bans are RARE (botnet is low-per-IP across 499 IPs → seldom 5-in-10min) — that's fine, it's noise
  reduction; key-auth is the real gate. (Transient rollout `addignoreip 157.51.57.3` set at runtime;
  clears on next fail2ban restart.)
- **auditd** installed+enabled+active; 10 file-watches loaded (env_change/config_change/systemd_change/
  ssh_keys_change/sshd_config_change/sudoers). Query: `sudo ausearch -k <key>`.
- **security-watcher.service** enabled+active (cycling ~60s). First live pass proved Telegram alerting
  works (sent 5 INFO sudo alerts for the rollout's own apt-get/cp/etc.; deduped after).
- **SSH access verified intact at every step** (fresh key login OK throughout).

## SSH hardening
- **#2 APPLIED (19-Jun, commit c040722): `PermitRootLogin no`** via drop-in
  `/etc/ssh/sshd_config.d/99-trading-security.conf` (source `deploy/security/sshd_config.d/`). Was
  sshd's built-in default `without-password`; nothing set it explicitly, so the drop-in wins
  (first-match). Validated `sshd -t` → `systemctl reload ssh`; effective `permitrootlogin no`; **ubuntu
  fresh login verified intact** (zero root keys exist, ubuntu is the only login user). The drop-in is
  itself integrity-watched (watched_files CRITICAL + auditd `-w /etc/ssh/sshd_config.d/`).
- **#1 HELD (Rama): NO idle timeout** (`ClientAliveInterval`) — operator runs long `tail -f` sessions.
  `MaxSessions` left at 10 (VS Code Claude multiplexes).

## NOT done (deferred)
- Phase 2 = copy protection; Phase 3 = System Manager EOD integration (add a 9th `security_check()`).

NB Rama got 5 INFO Telegram alerts during rollout (the monitor flagging my own sudo) — expected, deduped.
Related: [[vm_security_audit_19jun]], [[task_5_system_manager]], [[cron_env_export_fix]].
