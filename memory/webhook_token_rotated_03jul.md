---
name: webhook_token_rotated_03jul
description: "WEBHOOK_SECRET rotated 03-Jul (VM-side, value never displayed) after the old token was exposed in chat twice; old rejected / new accepted verified; single shared token for all 15 Chartink scanners"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fe7c775-fb70-4094-bcaf-e66df45399c5
---

**WEBHOOK_SECRET rotated 03-Jul-2026 ~23:xx IST (off-market).** Reason: the old token value was exposed in chat **twice**. Permanent rotation — old token fully invalidated, no dual-accept window, no fallback path. **rotated: yes.** The token value is stored in NO memory/doc/report/log (this file included) — it exists only in the VM `.env` (0600).

**Mechanism (single source, confirmed STEP 1):** `WEBHOOK_SECRET` env var, sole source = `EnvironmentFile=/home/ubuntu/systems/trading-system/.env`. Consumed at `main.py:2479` (`os.environ.get`) → `WebhookReceiver(secret_token=...)`; validated at `signals/webhook_receiver.py:429` `hmac.compare_digest(token_param, self._secret)` (active `?token=` path because `require_hmac: false`). **No unit/drop-in `Environment=` override for WEBHOOK_SECRET** (verified count 0), no hardcoded value in code, defined once in `.env`. **One shared token for all scanners** (scanner_name is a separate URL path checked against `scan_webhook_map`; the secret is shared) → **all 15 scanner URLs use the same `?token=`**. Paper & live use the identical mechanism (`required_startup_secrets()` mandates it in both modes).

**Rotation done: VM only.** Generated + written + verified entirely on the VM, value-blind (only booleans returned). STEP 3 (value-blind): OLD token REJECTED, NEW token ACCEPTED, new = 64-hex, perms 0600, all other `.env` keys intact. PC `.env` was **not** touched — it now holds the dead old value (harmless: Chartink only hits the VM; PC copy is dev-only and off the live path). If Rama wants PC parity he pastes the new value (which he reads for Chartink anyway) into the PC `.env` `WEBHOOK_SECRET` line himself — value never via chat.

**Load timing:** trading-system unit is INACTIVE off-market; the new value loads at **Mon 06-Jul 08:15 headless boot** (systemd re-reads EnvironmentFile at start). No `daemon-reload` needed (unit unchanged). No signals over the weekend, so Monday-boot load is sufficient — no restart forced tonight.

**Rama's pending manual steps (handed over):**
1. Read the new value into HIS OWN SSH terminal (never chat): `grep '^WEBHOOK_SECRET=' /home/ubuntu/systems/trading-system/.env | cut -d= -f2-`
2. Update the `?token=` query param in **all 15** Chartink scanner webhook URLs (Chartink → Alerts): open_low_breakout_long, first_pullback_long, vwap_bounce_long, gap_go_long, gap_fade_long, range_breakout_long, open_high_breakdown_short, first_pullback_short, vwap_rejection_short, gap_go_short, gap_fade_short, range_breakout_short, positional_momentum_long, positional_sector_rotation, positional_swing_long. (URL base: `http://<VM_IP>:5000/webhook/<scanner>?token=<NEW>`.)

**⚠️ MONDAY-OPEN CHECKLIST LINE:** *confirm the first real Chartink signal is ACCEPTED with the rotated token* (full end-to-end only provable at market open; if Chartink URLs weren't updated, signals will 401 and no trades fire — watch for that).

**Incidental finding (out of scope, NOT fixed):** the systemd drop-in `/etc/systemd/system/trading-system.service.d/telegram.conf` **hardcodes** `TELEGRAM_BOT_TOKEN`/`CHANNEL` as `Environment=` overrides that shadow `.env` — so the 02-Jul telegram rotation in `.env` may not be in effect on the running process (drop-in value wins). Separate parity hazard worth a dedicated look. See [[post_rotation_creds_02jul]], [[c2_webhook_lockdown_02jul]], [[project_vm_architecture_locked]].
