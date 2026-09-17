---
name: smtp-alert-watcher-config
description: "alert-watcher email/SMTP config (Gmail) + crisp [LFL836] subject; WORKING (verified 18-Jun)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

alert-watcher (scripts/alert_watcher.py) email delivery — configured 18-Jun-2026 (commit 6ee105b;
doc-correct 7e235b4). It emails CRITICAL sentinel `.flag` files, then renames them `.delivered`.

CONFIG (config/system_config.yaml → alerts.smtp): host smtp.gmail.com, port 587, use_tls true,
username/from_address/to_addresses = `ramakrishnan031@gmail.com` (send+receive), password via
`password_env: ALERT_SMTP_PASSWORD` (in VM .env, not committed). Schema = SmtpConfig (extra=forbid):
real fields are `from_address` + `to_addresses` (LIST), NOT `from`/`to`.

EMAIL FORMAT (alert_watcher.py, `_ACCOUNT_TAG="LFL836"`): single → subject `[LFL836] <SEVERITY> —
<title>`, body = alert summary + 1 metadata line + compact context (no hostname/PID walls). Digest
(>3 pending) → subject `[LFL836] CRITICAL — DIGEST: <N> alerts`, numbered one-line-per-alert list.
Tests updated: test_alert_watcher.py (29 pass).

✅ WORKING (verified 18-Jun-2026). A valid 16-char Gmail App Password was set in .env; on restart the
watcher logged `Digest delivered: 16 alerts → .delivered` (.flag=0, .failed=0) and emailed the digest
to ramakrishnan031@gmail.com (subject `[LFL836] CRITICAL — DIGEST: 16 alerts`). No auth errors after
the valid password. (Earlier failure was `535 BadCredentials` from an invalid/20-char value — Gmail
needs the 16-char App Password, 2FA on, no spaces.)

SERVICE PATTERN (don't mistake for a crash-loop): alert-watcher.service is `Restart=always` +
`RestartSec=10`, and alert_watcher.py runs ONE pass then exits 0 → periodic-oneshot. `auto-restart` /
climbing NRestarts is NORMAL (a sentinel check ~every 10s). Contrast trading-system.service whose
loop was a real crash (exit 4). See [[eod_18jun_cleanup_restart]]; watcher is EMAIL (not Telegram).
