---
name: ssh-alert-full-details-03jul
description: "Root-caused and fixed the \"?, since ?\" gaps in the SSH over-limit alert (03-Jul)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b1fa8b6-3ab8-4f25-a39a-0a6806490486
---

**Root cause #1 (geo "?"):** transient — those alerts fired before the GeoIP
enrichment ([[ssh_alert_geoip_03jul]]) was deployed. No bug once that landed;
not a rate-limit issue in practice at this alert volume.

**Root cause #2 ("since ?" / user "?"):** `session_ip_breakdown` only matched
established peers against `auth.log` "Accepted publickey" events. Some flagged
IPs (`103.238.128.18`, `45.198.224.120`, both bot hosts) are **unauthenticated
scan/probe connections** — root/admin-login attempts that sshd rejects within
~1-2s, always `[preauth]`, never producing an Accepted line — but `ss`'s
one-shot snapshot can still catch the TCP connection ESTABLISHED for that
instant. There's no login to report because there was no successful login;
the old code just had no fallback for that case.

**Fix (`scripts/security_monitor.py`, commit `e3cb834` + config fix `800d0c1`):**
- `established_ssh_connections()` (replaces `established_ssh_peers()` as the
  primary path; that name kept as a thin back-compat wrapper) now runs `ss`
  via `sudo -n ss -tnHp ...` instead of a plain `ss` — plain `ss` as `ubuntu`
  cannot see the pid of the root-owned `sshd [priv]` parent, so the process
  column was always empty before. `ubuntu` already has passwordless
  `NOPASSWD:ALL` sudo on this VM ([[project_vm_architecture_locked]]).
- New `process_start_and_user(pid)`: `sudo -n ps -o lstart=,args= -p PID` →
  (start_time, attempted_user). Best-effort — `(None, None)` if the pid has
  already exited (common; these connections live ~1-2s).
- `session_ip_breakdown` fallback chain per IP with no Accepted match: (1) the
  connection's sshd PID's own process-start time + attempted user, else (2)
  the current monitor-pass time (`now`) — a true lower bound, since the
  connection WAS just observed via `ss` — with user `"unauthenticated"`. **No
  session can show "?" anymore**, confirmed live on the VM (real dev sessions
  + a synthetic bot-IP-with-expired-pid both produced full detail lines).
- Gotcha caught during deploy: `config/security.yaml` carries its own
  `sudo_whitelist_prefixes:` list that OVERRIDES the `SecConfig` dataclass
  default entirely (not merged) — the first deploy (`e3cb834`, code-only)
  left the monitor's own new `sudo ss`/`sudo ps` calls self-alerting as
  non-whitelisted sudo (INFO spam). Second commit (`800d0c1`) added
  `/usr/bin/ss` + `/usr/bin/ps` to the YAML list too. **Any future
  sudo_whitelist_prefixes edit must touch both the code default AND
  config/security.yaml, or the YAML silently wins.**

**GeoIP source:** unchanged from [[ssh_alert_geoip_03jul]] — `ip-api.com`
fallback (no local MaxMind DB on the VM; still flagging that a MaxMind
license key is Rama's call if he wants offline/rate-limit-proof geo later).

**Live sample (multi-IP, real VM data, 03-Jul ~18:45 IST):**
```
9 active SSH sessions (limit 2). 103.238.128.18 x1 (unauthenticated, since 18:45:14, Mumbai, IN — Srmak Technological System Private Limited) | 223.237.179.17 x8 (ubuntu, since 17:16:57, Chennai, IN — Bharti Tele Ventures Ltd). (Alert only — not blocked.)
```

**Deployed:** main `cf6ecb8 → e3cb834 → 800d0c1`, pushed to the VM bare repo,
restarted `security-watcher.service` only both times (trader untouched). 42
existing unit tests in `tests/unit/test_security_monitor.py` pass (no
dedicated tests existed for the touched functions before this work).

**How to apply:** if a future security_monitor change adds a new whitelisted
sudo command, update BOTH `SecConfig.sudo_whitelist_prefixes` default AND
`config/security.yaml`'s `sudo_whitelist_prefixes:` list.
