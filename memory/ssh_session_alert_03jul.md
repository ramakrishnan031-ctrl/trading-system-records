---
name: ssh-session-alert-03jul
description: "SSH over-limit alert diagnostic (03-Jul) — all sessions were Rama's own IP; alert enhanced to list per-IP breakdown"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b1fa8b6-3ab8-4f25-a39a-0a6806490486
---

**Diagnostic (Part 1, 03-Jul ~18:12 IST):** All 4-5 "over limit" SSH sessions were
`223.237.179.17` (Chennai, Bharti Airtel — Rama's dev PC), single SSH key
(`SHA256:uDRN8BJTmfNGFfCLofbnXkIGtWF6qTtrREQrQJGKduk`), all successfully
authenticated. VS Code Claude SSH tooling opens 3-5 concurrent connections per
session, which is why the count kept climbing (3→4→5) against
`max_active_sessions: 2` in `config/security.yaml`.

`2.57.121.25` (UK, "Unmanaged LTD" hosting — a known bot-scan host) was **never
an active/authenticated session** — only repeated failed `Invalid user admin`
preauth probes on 27-Jun, rejected outright by key-only auth. It has never
appeared in `known_login_ips` or `last_session_peers`, and the over-limit alert
code path (`check_active_sessions`) only ever lists **established** SSH peers —
it cannot have named `2.57.121.25` in an actual alert body. Likely explanation:
Rama saw this IP in an unrelated/older Telegram notice and conflated it with the
same-day over-limit alert.

**Verdict:** no confirmed foreign/unauthorized session. No containment action
taken. Recommended follow-up (Rama's call, not yet decided): raise
`max_active_sessions` above 2, or allowlist the dev IP, since 2 is producing
constant false-positive noise against Rama's own legitimate tooling.

**Part 2 — alert enhancement (deployed 03-Jul ~18:15 IST):** `check_active_sessions`
in `scripts/security_monitor.py` now builds a per-IP breakdown (new helper
`session_ip_breakdown`) — count + user(s) + earliest login time (proxied from
`auth.log` `Accepted publickey` events, 24h lookback) — instead of a bare count
+ partial IP list. Sample fired alert:
`5 active SSH sessions (limit 2). 223.237.179.17 x5 (ubuntu, since 17:16:57). (Alert only — not blocked.)`

Deployed via normal git push to the VM bare repo (main `2e2b2bb→3a27538`) +
`sudo systemctl restart security-watcher.service` (monitor only, trader
untouched — infra change, mode-agnostic). Verified via `--report` immediately
after: 42 existing unit tests in `tests/unit/test_security_monitor.py` still
pass (no dedicated tests existed for `check_active_sessions`/
`established_ssh_peers`, so signature change was low-risk).

**Why:** [[project_vm_architecture_locked]] key-only SSH is the sole
authorization gate; security_monitor is alert-only (never blocks) by design —
see file docstring. This session confirms that design is holding: bot scans
from `2.57.121.25` never got past auth.

**How to apply:** if `max_active_sessions` alerts keep firing on Rama's own
IP, that's expected given multi-connection dev tooling — not a security event
by itself. Only escalate if a *different* IP appears in the per-IP breakdown
with a successful auth.
