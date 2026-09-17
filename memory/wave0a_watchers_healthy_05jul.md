---
name: wave0a-watchers-healthy-05jul
description: "Wave 0a read-only diagnosis — alert-watcher + security-watcher are HEALTHY periodic-oneshots, NOT dead; the 05-Jul audit \"stuck in activating\" flag is a monitoring FALSE POSITIVE. Read before touching either unit."
metadata: 
  node_type: memory
  type: project
  originSessionId: 195d7581-8ffa-4581-941a-90abdcae8bb2
---

Wave 0a (05-Jul-2026, read-only) resolved the 04/05-Jul audit's flag that
`alert-watcher.service` and `security-watcher.service` were "stuck in
`activating`" (two DEAD safety units). **They are NOT dead.** Both are healthy
periodic-oneshots working exactly as designed. The audit's Phase 9 (Agent-I)
was cut off before finishing this; the flag is a monitoring FALSE POSITIVE.

**Root cause (SAME for both):** `Type=simple` + `Restart=always` + `RestartSec=N`
where the launched script runs ONE pass and exits 0 (alert_watcher.py main→run_once;
security_monitor.py --watch → one run_pass → `return 0`, "exit 0 always" at :1020).
Lifecycle = run ~0.1–1s → exit 0 → systemd waits RestartSec (alert 10s / security 60s)
→ restart. During the wait, SubState=`activating (auto-restart)`. Because the wait
dwarfs the sub-second pass, ANY snapshot lands in `activating` ~98–99% of the time
even when perfectly healthy. Catching both in `activating` is EXPECTED, not a stall.
The security-watcher unit-file header comment (lines 2-6) literally predicts this:
"Rising NRestarts is NORMAL (it's a heartbeat, not a crash-loop)."

**Decisive evidence (05-Jul 12:28–12:40 IST):**
- systemctl show BOTH: ExecMainStatus=0, code=exited, Result=success, SubState=auto-restart,
  Type=simple, NotifyAccess=none, WatchdogUSec=0.
- NB: `ExecMainCode=1` is si_code CLD_EXITED (=exited normally), NOT exit code 1.
- NRestarts alert=13075 / security=2277 — exactly consistent with uninterrupted
  10s/60s cadence since boot (03-Jul ~22:22, ~1d14h uptime).
- security `data_store/security/last_run.json` fresh (13s old): checks_run=9,
  findings_count=0, clean=true → all 9 checks ran to completion.
- alert `logs/alert_watcher.log`: metronomic ~10.5s "No pending sentinels found."; lock
  absent between passes (clean acquire/release).
- Journals `--since 4 days`: clean `Deactivated successfully` / `pass complete` every
  cycle; **0** failure-keyword hits. The only non-heartbeat lines are the watcher DOING
  ITS JOB (03-Jul 23:03 CRITICAL `.env` change = token-shadow fix; SSH-over-limit;
  new-login-IP for Rama's rotating mobile IPs).
- Parity: running code md5 == git HEAD blob (LF) for both scripts AND both installed
  units (/etc/systemd/system) — zero drift. Running code == what was analyzed.

**Candidates ruled OUT:** (a) notify/sd_notify — N/A, Type=simple; (b) hung ExecStartPre —
none defined; (c) crash-loop — ExecMainStatus=0; (d) dep wait — only network-online (up);
(e) drop-in Environment= shadow (the 24-Jun class) — NO `.service.d/` dirs exist. This is
NOT the 24-Jun Telegram drop-in class.

**Blast radius:** none currently — both safety functions are running (alert delivers
within ~10s; security runs 9 checks/60s and is alerting on real events). Real risk is only
that a naive `systemctl is-active` health check keeps false-flagging or desensitizes on-call.

**Recommended fix path (NOT implemented; awaiting next instruction):**
(a) RECOMMENDED (S, zero risk): fix the health check — health = ExecMainStatus==0 &&
Result==success PLUS last_run.json/alert log freshness, NOT is-active==active; document in
SYSTEM_MAP so it isn't re-flagged. (b) Optional (M, off-market): convert to a systemd
`.timer` + Type=oneshot so the timer shows `active (waiting)` and the service `inactive
(dead)` between runs (legible to naive checks) — but that rebuilds WORKING safety units, so
only for legibility, not correctness.

**Post-receive hook (Part B, verified 05-Jul):** LIVE `/home/ubuntu/trading-system.git/hooks/post-receive`
(md5 bd950b7b, mtime 23-Jun 19:27) is BYTE-IDENTICAL to tracked `deploy/hooks/post-receive` (HEAD blob, last
touched 428f923 23-Jun — no drift) and checks out to `--work-tree=/home/ubuntu/systems/trading-system` →
TARGET CORRECT (the /systems/ path). Push remote = `origin trading-vm:~/trading-system.git` = bare
`/home/ubuntu/trading-system.git`.
⚠️ A SECOND tracked copy `deploy/post-receive` (md5 604d2b37, 3629B, STILL at HEAD) is a STALE BOOBY-TRAP:
`CHECKOUT=/home/ubuntu/trading-system` + `VENV=/home/ubuntu/trading-system/venv` are pre-/systems/ paths that
DO NOT EXIST on the VM (verified `ls` → No such file). Its own header says "Arm by: cp deploy/post-receive
~/trading-system.git/hooks/...". If ever armed, `checkout -f` would CREATE `/home/ubuntu/trading-system` and
phantom-deploy there = silent no-op "successful" deploy (running system keeps old code). This = known audit
finding **M-DP1** (full_system_audit_04july2026.md:165), now live-confirmed. FIX (later): delete/reconcile
`deploy/post-receive` so only `deploy/hooks/post-receive` is authoritative.
Docs OK: PATHS.md:385 + SYSTEM_MAP.md:216 correctly cite deploy/hooks/post-receive & /systems/ → PATHS NOT
proven wrong, no correction due. Stale path lingers only in historical docs (DEPLOYMENT.md, docs/web_claude/*).
DEPLOY-CONTEXT for the upcoming watcher fix: live hook does checkout + crontab-auto-install ONLY — NO systemctl
restart, NO daemon-reload, NO pip/venv sync, and (regression vs old deploy/post-receive) NO FIX-065 market-hours
push guard. So a fix push lands CODE but does NOT restart units (manual `systemctl restart` needed); a UNIT-FILE
change (e.g. .timer) also needs manual `cp → /etc/systemd/system/` + `daemon-reload`. Old checkout-only hook
preserved as `post-receive.pre-cron-framework.bak` (md5 77898068). No pre-receive installed.

**No modifications were made** (VM non-mutating; repo docs SYSTEM_MAP.md/PATHS.md intentionally
NOT edited per Rama's "no changes" directive — staged for go-ahead).

Related: [[smtp_alert_watcher_config]] · [[vm_security_phase1]] · [[cron_framework_armed_23jun]] · [[full_repo_audit_04jul_pending]] · [[telegram_token_shadow_FIXED_03jul]]
