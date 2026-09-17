---
name: system-health-audit-15jul
description: "15-Jul-2026 whole-system read-only health audit (16 subsystems, two verdicts). Trading=PASS, Monitoring=FAIL (SMTP email dead → alerts undelivered). Gates the 3-fix branch deploy = PROCEED."
metadata: 
  node_type: memory
  type: project
  originSessionId: 5e0da463-297c-4dc3-bb3f-4db09f2c57a7
---

**15-Jul-2026 WHOLE-SYSTEM HEALTH AUDIT (read-only, 16 subsystems, TWO verdicts) — fixed NOTHING.** Report `docs/audit/system_health_audit_15jul2026.md`, committed **`3b9ccd1`** on `main` (docs-only, UNPUSHED; main now 6 docs commits ahead of VM/bare `2dc69d5`). Gates the 3-fix branch [[fixes-15jul]].

**VERDICT A — TRADING SYSTEM = PASS.** 7 trades within every cap; book flat & reconciled; net P&L ₹0.99; **DB integrity CLEAN** (`quick_check=ok`, `foreign_key_check` empty, WAL=0); token valid; backups produced (340MB); 0 crashes/orphans/partials. The only 2 hard job failures (eod_cleanup, generate_screened_csv) are hygiene/reporting, fixed on the branch.

**VERDICT B — MONITORING TRUTH = FAIL.** The monitor shows green while alerts are silently undelivered:
- 🔴 **SMTP EMAIL DELIVERY DEAD — Gmail `535 5.7.8 BadCredentials` (`ALERT_SMTP_PASSWORD` invalid/expired).** The 15-Jul EOD emails (system_manager_eod 18:45 + cron_officer_eod 18:50) NEVER delivered, and **8/8 critical sentinels today are UNDELIVERED** (0 delivered), yet the jobs' heartbeats say SUCCESS (**Layer-9 masking**: heartbeat ≠ delivery). Delivery worked through **14-Jul 21:20** (11 delivered/0 pending) → broke 15-Jul → credential expired EXTERNALLY (`.env` unchanged, not a deploy effect). *(Earlier 18-Jun 535 was a separate, fixed incident.)*
- 🔴 **`alert_watcher` exit-2 restart-loop** — finds 8 pending → digest EMAIL (>3 threshold) → SMTP 535 → `return 2` → systemd restarts every 10s → permanent loop (log 14MB & growing). **It is EMAIL-ONLY — no Telegram fallback** (`scripts/alert_watcher.py:427` returns 2 on `SMTPAuthenticationError`). So sentinel alerts have NO backup when SMTP dies.
- 🟠 **`check_cron_drift` (18:00) false-alarms** "no heartbeat in 24h" on preflight_phase_a/b/c + sr_detector_backfill — those 4 use `detection_method: exit_code_file` (markers, not heartbeats) and DID run (markers present). Standing daily false-positive.
- 🟡 The 14-Jul `generate_screened_csv` fake-success (heartbeat SUCCESS while empty CSV) — the trigger exemplar — is FIXED by `522da32` (15-Jul it correctly reported FAILED).
- **Telegram (direct-emit) WORKS** — the cron_officer headline fired; only the SMTP/email + sentinel-digest channel is dead.

**EOD-EMAIL ROOT CAUSE = Layer 5/8** (SMTP auth / expired credential). Reports GENERATE fine (artifacts present: system_manager `2026-07-15.txt`, daily_report.xlsx 634KB, daily_trade_review.xlsx 520KB, gemini .md all real); only DELIVERY (email) fails.

**Other subsystems (all Verdict-A PASS):** S4 backups produced · S5 token valid · S7 metrics/control_tower ran · S8 gemini REAL output · S9 forward-shadow fired (2535 rows, idempotent) · S12 integrity clean · S15 disk 81GB free/0 zombies · S16 bare `2dc69d5`, live hook paths correct. S14 security-watcher stuck on Rama's own BRi6 key (Q8, deferred). S13 stale `officer.telegram_ban_until:2026-06-23`.

**CLASSIFICATION: NO BLOCKER** (capital/trading/risk/data/DB all PASS). All defects are monitoring/observability = NON-BLOCKER.

**⏰ DEPLOY RECOMMENDATION = PROCEED with the 3-fix branch** (no BLOCKER; it touches nothing in the alert path + removes 2 daily FAILED heartbeats). **Open a MONITORING-HARDENING cycle:** P0 = **restore the SMTP credential (ALERT_SMTP_PASSWORD)** [Rama — urgent; email/sentinel alerts are down + alert_watcher is looping]; then alert_watcher robustness (no crash-loop / Telegram fallback), close Layer-9 (heartbeat requires delivery), fix check_cron_drift to read markers, purge stale telegram_ban + rotate alert_watcher.log. See [[fixes-15jul]] · [[followup-investigation-15jul]] · [[day-reconstruction-15jul]].

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 947 B (budget 300 B). The index now carries a hook and this link.

- 🩺🔴🟢 **[15-Jul WHOLE-SYSTEM HEALTH AUDIT (read-only, 16 subsystems, TWO verdicts)](system_health_audit_15jul.md)** — **A) TRADING = PASS** (7 trades within caps, book flat, DB integrity clean, backups/token OK, 0 crashes). **B) MONITORING TRUTH = FAIL: SMTP EMAIL DEAD (Gmail 535 BadCredentials / expired `ALERT_SMTP_PASSWORD`)** → 15-Jul EOD emails never delivered + **8/8 critical sentinels UNDELIVERED** while heartbeats say SUCCESS (Layer-9); **alert_watcher exit-2 loop** (email-only, no telegram fallback); check_cron_drift false-alarms 4 marker-jobs. **Telegram (direct) works.** EOD-email root cause = **Layer 5/8 SMTP auth** (broke after 14-Jul 21:20). **NO BLOCKER** (all monitoring/observability) → **DEPLOY REC: PROCEED with the 3-fix branch**; open a monitoring-hardening cycle (**P0 = restore SMTP credential — urgent**). Report `3b9ccd1` on main (docs-only, UNPUSHED). [[system-health-audit-15jul]] [[fixes-15jul]]
