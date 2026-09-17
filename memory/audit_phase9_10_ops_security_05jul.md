---
name: audit_phase9_10_ops_security_05jul
description: Audit-B Phases 9 (Operations) + 10 (Security) completed 05-Jul — read-only VM audit; NO IOC; webhook :5000 internet-open is top new item; findings feed go/no-go + Wave 3
metadata: 
  node_type: memory
  type: project
  originSessionId: 46720e02-4098-4c34-87c3-16d4cb5c52fa
---

**Audit-B Phases 9+10 completed 05-Jul-2026** (the 05-Jul audit `docs/audit/audit_05jul2026.md` had ended mid-Phase-9). READ-ONLY VM audit, non-mutating. Feeds production go/no-go + Wave-3 ranking. **NO fixes made.**

## SECURITY VERDICT: NO INDICATOR OF COMPROMISE (no escalation)
Single authorized SSH key = approved baseline `SHA256:uDRN8B…` (oracle-vm-2026); key-only auth (`passwordauthentication no`, `permitrootlogin no`, `permitemptypasswords no`); all Accepted logins from Indian-mobile ISP ranges (Jio 157.50/157.51/106.192, Airtel 223.237 — the documented Rama rotating-IP pattern); all outbound = Tailscale (×3: coord+DERP-blr+lb.fra) / Oracle-email-delivery / OCI metadata 169.254; root+system cron stock-only; no SUID in home; recent /etc changes benign (OCI unified-monitoring-agent, Tailscale apt, expected 04-Jul gui-dashboard deploy); auditd active; copy-guard scp/sftp/rsync wrappers installed.

## SSH-INCIDENT ROOT CAUSE (the "time-lock failed to block 04:18 foreign IP")
Category error. The 18:00–08:00 "time-lock" (`config/security.yaml:82,89-90` copy_protection) is a **VM→PC copy-egress** control (scp/sftp/rsync wrappers + auditd), explicitly **NOT an SSH gate** — `security.yaml:8` "Alert-ONLY. Nothing here blocks access — key-only SSH is the gate." So it structurally cannot block an SSH login. SSH is key-only; a "foreign IP" = a new/rotating mobile IP admitted by the correct gate; >2 sessions / new-IP are ALERT-only (never block). No lock failed; the expectation was wrong. If a nightly SSH block is actually wanted → enforce at nftables (time rule) or go Tailscale-only SSH (drop public :22).

## PHASE 9 — OPERATIONS (new)
- **O-1 [MED]** alert-watcher + security-watcher run as **exit-and-restart poll loops** (Type=simple/Restart=always): NRestarts **15,676 / 2,730**, ~1/10s & /60s, ExecMainStatus=0 (clean, NOT crash-loop). Journal spam + the `is-active`→`activating` false-positive a naive health check misreads. Confirms Wave-0. Fix: Type=oneshot+.timer or in-proc loop+sd_notify; health-check on ExecMainStatus+freshness.
- **O-2 [MED]** post-receive hook = `checkout -f` + crontab-install ONLY. NO `systemctl restart` (deploy≠restart), NO `daemon-reload` (unit changes inert), NO venv/pip sync, NO FIX-065 market-hours push guard (off-market discipline unenforced).
- **O-3 [MED]** Installed-vs-repo **unit drift already present** (consequence of O-2): `trading-watchman.service` installed unit LACKS the `/home/ubuntu/tools/antigravity` PATH the repo added; `trading-system.service` differs comment-only (HALT guard `RestartPreventExitStatus=3 4` IS present in the installed unit — LOW part).
- **O-4 [MED]** Cron observability split across TWO partial mechanisms: `cron_marks/.done` (17 jobs) vs `cron_heartbeat` DB (28 jobs); neither covers all **45** live jobs → root of the 22-vs-30 Officer delta; a job tracked by neither fails silently. All last-runs rc=0 today.
- **O-5 [HIGH — confirms Phase-3]** No off-site backup: 3.4G DB backups on same `/dev/sda1` as primary; no rclone/scp/rsync/s3 cron. Disk 16% used (82G free) — healthy, but single-disk total-loss risk to the trade audit trail.
- **O-6 [LOW]** Log hygiene: no logrotate.d for app logs; single-name append logs grow unbounded (`alert_watcher.log` 8MB via the 10s-restart append); 97 files/834M since Jun-12. A `log_cleanup` cron DOES exist (marker present) — not "never pruned," but accretion + no logrotate.
- **O-7 [LOW]** Recurring UNACTIONED config_sanity warnings every Officer briefing: `max_position_value_rs 2500 > daily_loss_limit 300` (one bad trade can blow the daily cap) + `entry_end 15:15 within 15min of squareoff 15:17` → alert fatigue. Overlaps Phase-2 config.

## PHASE 10 — SECURITY (new)
- **S-1 [MED-HIGH — most urgent new]** Webhook **:5000 open to 0.0.0.0** at nftables (`tcp dport 5000 … accept`, live-confirmed) + Flask bind 0.0.0.0 + `require_hmac:false` + `?token=` query auth. C-2 Option-B (reverse-proxy/HMAC/IP-allowlist to Chartink static IP) **NOT implemented** at the network layer — token leak in any access/referer log ⇒ anyone injects signals from anywhere (downstream caps/screeners limit blast radius; token rotated 03-Jul). Network-confirms Phase-2 [MED].
- **S-2 [MED]** time-lock expectation gap (see root cause above).
- **S-3 [MED]** Public **SSH :22 on 0.0.0.0** (nft-accepted) contradicts "Tailscale-only, no public port" — 22 + 5000 are the two internet-open ports; internet bot probing present (≤684 failed/day, key-auth blocks). Fix: Tailscale-only SSH (drop public 22) — also closes S-2.
- **S-4 [LOW]** `rpcbind:111` binds 0.0.0.0 + enabled BUT nftables REJECTS it externally → not internet-reachable (de-escalated from the baseline flag). Disable for hygiene.
- **S-5 [LOW]** sshd `x11forwarding yes` + `allowtcpforwarding yes` on a key-only single-user box — unnecessary forwarding surface.
- **S-6 [LOW]** security-watcher recurring false-positive INFO "Non-whitelisted sudo … /usr/sbin/sshd" every pass (sshd PAM sudo not in `sudo_whitelist_prefixes`) → noise.
- **S-7 [INFO]** No pip-audit/safety installed (no-install rule) → dep CVE scan is a follow-up (run off-box vs requirements.txt; deps exact-pinned/minimal).
- Carried/known (not new): C-1 git-history secrets (rotated dead, purge pending), M-K5 unredacted config-snapshot pw, token-in-log LOW, fail-open 2FA + ephemeral Flask secret LOWs, M-A1 alert-truncation, Phase-2 email_fallback unfed.

## ROLL-UP
New: **1 MED-HIGH (S-1) + 6 MED (O-1..O-4, S-2, S-3) + 6 LOW + 1 HIGH-confirm (O-5)**. **Most urgent NEW = S-1** (webhook :5000 internet-open, pre-auth, query-token-only). Equal-weight infra risk = O-5 (no off-site backup). No parity issues (webhook ingress mode-agnostic).

Related: [[wave0a_watchers_healthy_05jul]] (O-1 confirms) · [[c2_webhook_lockdown_02jul]] / [[c2_chartink_ip_investigation_03jul]] (S-1) · [[webhook_token_rotated_03jul]] · [[ref_security_audit_02jul]] · [[full_repo_audit_04jul_pending]]. Evidence: 6 read-only SSH batches, `docs/audit/audit_05jul2026.md`.
