---
name: telegram_token_shadow_investigation_03jul
description: "CONFIRMED bug — systemd drop-in telegram.conf shadows .env with a REVOKED (401) bot token; main trading-system process runs the dead token, cron uses valid .env token; read-only, not fixed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fe7c775-fb70-4094-bcaf-e66df45399c5
---

**Read-only investigation, 03-Jul-2026 ~23:20 IST (off-market). NOT fixed — Web Claude designs the parity-correct fix next.** No token value stored anywhere. Full findings: `docs/audit/telegram_token_shadow_investigation_03jul2026.md`.

**Confirmed bug (was flagged during the webhook rotation).** systemd drop-in `/etc/systemd/system/trading-system.service.d/telegram.conf` (mtime 2026-05-18) hard-codes `TELEGRAM_BOT_TOKEN` as `Environment=`, which **overrides** the unit's `EnvironmentFile=.env`. Value-blind sha256 compare: `.env` vs drop-in `TELEGRAM_BOT_TOKEN` are **DIFFERENT**; `TELEGRAM_CHANNEL_PRIMARY`/`SECONDARY` are IDENTICAL (harmless; secondary is the `FILL_CHANNEL_ID_2` placeholder in both); `TELEGRAM_PERSONAL_CHAT_ID` only in `.env` (not shadowed).

**Which token is live (value-blind getMe on each — both same bot id 8648177777 / @Trade_sysbot, public):**
- `.env` token (02-Jul rotated) = **VALID**.
- drop-in `telegram.conf` token = **HTTP 401 DEAD** (revoked by the 02-Jul rotation).

**Live source verdict:** main `trading-system` process → **drop-in token = DEAD**; cron jobs (officer/EOD/healthcheck/control-tower/reconcile) run OUTSIDE the unit → source `.env` = **VALID**. So the 02-Jul rotation is NOT live for the main process. Rama still gets alerts because they are cron-originated (valid `.env` token); CRITICAL alerts also have an email backup (sentinel → alert_watcher), masking the gap.

**Runtime impact (precise, not overstated):** G8 tier routing (`telegram_notifier.py:308-311`) — INFO/WARN failures are **dropped SILENTLY**, ERROR/CRITICAL write `failed_alerts.log` (which has **no entries since 02-Jul 18:50**, the rotation time). So main-process INFO/WARN telegram alerts with the dead token fail **invisibly**. No positively-logged main-process failure found for 03-Jul; an earlier ~174-hit grep was a **false positive** (unrelated signal_processor score-rejection lines) and is retracted — mechanism confirmed, a runtime failure line is NOT asserted.

**Parity:** same unit + drop-in governs paper & live identically (mode is a runtime arg, not a separate unit) → shadow affects both the same. **Blast radius:** only `TELEGRAM_BOT_TOKEN` is the live defect; channels harmless. Same EnvironmentFile-shadow pattern as the webhook finding, but here the drop-in value diverged (revoked) → latent redundancy became a live bug.

**Fix direction (NOT applied):** remove `TELEGRAM_BOT_TOKEN` (+ redundant `TELEGRAM_CHANNEL_*`) from `telegram.conf` so `.env` is the single source, then `daemon-reload` + off-market restart. See [[webhook_token_rotated_03jul]] (where this was first flagged), [[post_rotation_creds_02jul]] (the 02-Jul rotation that revoked the old token), [[project_vm_architecture_locked]].
