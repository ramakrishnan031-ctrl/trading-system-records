---
name: operator-backup-ssh-27jul
description: "Offsite backup RUN for the first time 27-Jul (and its runbook had omitted the one unregeneratable file). SSH->Tailscale REFUSED for now: the phone has been off the tailnet 23 days, so closing port 22 would void the documented emergency path."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1651e524-a1a0-427f-84ae-b0f0b833e483
  modified: 2026-07-27T14:21:24.289Z
---

# The two long-standing operator items, 27-Jul-2026

## D1 — OFFSITE BACKUP: DONE, and the runbook had the worst possible gap

✅ **First offsite copy ever taken:** `D:\backups\vm\2026-07-27\` — `trading_system.db`
(integrity ok, trades 430 = the VM's own count), `analytics.db` (ok, candles 310,168),
**`forward_shadow_fs-v1.jsonl` 21,149 lines**, `would_be.jsonl`. ~199 MB.

⭐⭐ **THE GAP: the runbook backed up both DBs and NOT `data_store/v3/forward_shadow_fs-v1.jsonl`
— the one artifact that genuinely cannot be regenerated.** The DBs are substantially
reconstructible from broker records; the forward-shadow record is not, and its producer must
never be re-run by hand. It was in **no backup anywhere**. Now included.

Two more inaccuracies fixed: the verify step called **`sqlite3`, which is NOT on the PC's PATH**
(so "the step people skip" was unrunnable), and it compared against a hardcoded **`trades 423`**
(now 430) — replaced by comparing to the VM's own live count so it cannot go stale.
⛔ **Never a bare `cp`/`scp` of a live WAL DB** — use `sqlite3 SRC ".backup DEST"`.
Command + full reasoning: `Downloads/OPERATOR_backup_and_ssh_27-JUL.txt`.

## D2 — SSH → TAILSCALE-ONLY: ⛔ REFUSED FOR NOW, one named blocker

⛔🔑 **`tailscale status` shows `moto-g96-5g` OFFLINE, LAST SEEN 23 DAYS AGO.** The phone
fallback in `TONIGHT_IF_PC_IS_DOWN_27-JUL.txt` works **only because port 22 is open to the
world** — so closing it now would **silently void the emergency runbook Rama was told to rely
on**, at the moment he'd need it. ⭐ 27-Jul is the proof it is not hypothetical: the PC did go down.

Measured scope of the change:
- ✅ **Cron: nothing breaks** — ZERO crontab lines use `ssh`/`scp`/`rsync`.
- ⚠️ **Deploy path breaks, trivially fixable** — `~/.ssh/config` resolves `trading-vm` to the
  PUBLIC `161.118.187.249`, not Tailscale `100.74.84.44`. One line. PC is already on the tailnet.
- ⛔ **Phone fallback breaks** — the blocker above.
- Tailscale IS installed/running on the VM; no `ufw`, rules are raw **iptables**
  (`ACCEPT tcp dpt:22 from 0.0.0.0/0`). ⭐ The webhook port is already restricted to a single
  source IP, so the pattern is understood and in use.

**Order:** phone back on tailnet and PROVEN (mobile data, WiFi OFF) → repoint the PC's HostName
and prove a push still deploys → only then restrict :22 → and confirm a cloud-console recovery
path FIRST. ⏰ **Not this week** (Wed T2 arm / Thu close); natural slot is with the 2FA seed move
already deferred to **Fri 7 / Sat 8-Aug** — both are access work.
