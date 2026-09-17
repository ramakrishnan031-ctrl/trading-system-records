---
name: telegram-token-shadow-fixed-03jul
description: FIXED 03-Jul — removed the telegram.conf systemd drop-in so .env is the SINGLE source for the Telegram bot token (kills the split-brain); no token value stored; activates Mon 08:15 boot
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fe7c775-fb70-4094-bcaf-e66df45399c5
---

**Permanent fix applied 03-Jul-2026 ~23:40 IST (off-market). Single-source established.** No token value in this file. Root cause + evidence: [[telegram_token_shadow_investigation_03jul]].

**What was removed:** the entire systemd drop-in `/etc/systemd/system/trading-system.service.d/telegram.conf` — it contained only `[Service]` + three `Environment=` overrides (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_PRIMARY`, `TELEGRAM_CHANNEL_SECONDARY`). Since removing the three lines emptied it of directives, the whole file was deleted (not left as an empty stub). `watchman.conf` (unrelated, `Wants=trading-watchman.service`) left intact. `.env` was NOT touched — it already holds all four telegram keys (BOT_TOKEN valid; CHANNEL_PRIMARY/SECONDARY byte-identical to what the drop-in had, so zero channel-behaviour change).

**Why delete rather than edit the value:** permanent single-source principle — leaving the channel overrides (even though identical today) would re-create the same shadow hazard on any future channel change. `.env` (EnvironmentFile) is now the sole source for ALL telegram env keys, for both the main process and cron.

**Verification (value-blind):**
- `systemctl daemon-reload` done; `systemctl show trading-system -p Environment` now lists only `PATH` + `PYTHONUNBUFFERED` — **no `TELEGRAM_*` override** (resolves from `.env` EnvironmentFile only). `systemctl cat` references to `telegram.conf` = 0.
- `.env` intact: 4 telegram keys present, perms 600, owner ubuntu. `.env` `TELEGRAM_BOT_TOKEN` re-confirmed VALID post-fix (getMe ok, `@Trade_sysbot`).
- Pre-fix backup (`/home/ubuntu/backups/telegram_conf_pre_fix_03jul.bak`, held the dead token) **shredded** after verify — no stale value left behind.

**Parity:** single unit; `ExecStart=… main.py --mode live` — mode is a runtime arg, not a separate paper/live unit; env resolution is mode-independent → the fix covers both modes by construction.

**Activation timing:** the main `trading-system` process is INACTIVE (off-market) and held the dead token only while running; **no restart tonight**. **Mon 06-Jul 08:15 boot** starts it fresh → reads `.env` → valid token live for the main process. No weekend signals, so Monday-boot activation is sufficient. (An off-market restart tonight would activate immediately but is unnecessary — recommended to wait.)

**MONDAY-OPEN CHECKLIST (both lines, co-located with the webhook one in [[webhook_token_rotated_03jul]]):**
1. *(webhook)* confirm the first real Chartink signal is ACCEPTED with the rotated `WEBHOOK_SECRET`.
2. *(telegram)* confirm a **main-process** Telegram alert delivers post-08:15 boot (e.g. a startup/preflight alert arrives) — proves the drop-in fix is live for the main process, not just cron.

See [[telegram_token_shadow_investigation_03jul]], [[webhook_token_rotated_03jul]], [[post_rotation_creds_02jul]], [[project_vm_architecture_locked]].
