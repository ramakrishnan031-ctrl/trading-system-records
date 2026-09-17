---
name: VM is the production listener as of 2026-04-27 (supersedes earlier "PC + ngrok" plan)
description: trading-system.service is enabled+active on VM; webhook on 0.0.0.0:5000 after commit 2d1e580; the older "systemd disabled, execution stays on PC" memories are stale
type: project
originSessionId: 10cbe4dd-821c-4e9d-a171-0348c2ce6014
---
**Current observed state (2026-04-27, ~09:30 IST):**
- `trading-system.service` on VM: `enabled` + `active` (systemd-managed).
- Webhook listener: `0.0.0.0:5000` (post-restart, PID 219425). Was `127.0.0.1:5000` (PID 218623) before commit `2d1e580`.
- Restart command worked over SSH non-interactively: `sudo -n true` returns OK on the VM (NOPASSWD configured).
- Verification command: `/c/Windows/System32/OpenSSH/ssh.exe trading-vm "ss -tlnp 2>/dev/null | grep ':5000'"` shows `0.0.0.0:5000`.

**Why this matters:**
- The earlier memory entries listed under MEMORY.md as authoritative for paper Week 2 ops (`project_deployment_status.md`, `project_paper_to_live_plan.md`, `project_next_session.md`) said "systemd DISABLED during paper", "execution stays on PC + ngrok through Week 3", "Do NOT enable systemd". Those are STALE — the operator has already moved execution onto the VM. Trust live `systemctl is-active` over the older plan documents.
- Memory hygiene rule (MH3 in `feedback_memory_hygiene.md`): when an observation contradicts a saved memory, trust the observation.

**Operational implications for future sessions:**
- Code pushes to `vm` remote land in production immediately (post-receive hook updates the checkout); a `systemctl restart trading-system` is required for the new code to actually run if the change is in a long-lived module loaded at start.
- Market-hours rule still applies (no code pushes 09:15–15:30 IST) — the 2026-04-27 push at 09:30 was a deliberate operator-authorized override for an ops fix, not a precedent.
- HMAC (`require_hmac=true`) is the only application-level gate on the webhook now that bind is `0.0.0.0`. Cloud security group / host firewall is the network-level gate.

**SSH access pattern (re-verified today):**
- `/c/Windows/System32/OpenSSH/ssh.exe trading-vm "<cmd>"` works non-interactively from Bash tool.
- `sudo -n` works (NOPASSWD).
- For git push: `GIT_SSH="/c/Windows/System32/OpenSSH/ssh.exe" git push vm main`.
