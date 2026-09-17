---
name: Telegram channel deleted - recreate before 29-Apr
description: Channel needs recreation; update chat_id in config before market open
type: project
originSessionId: d5bd2391-ce3d-4d13-8c5f-cd1d20f63b64
---
**Telegram channel deleted (2026-04-28 post-market)**

## Recreation steps
1. Rama creates new Telegram channel
2. Add bot to channel as admin
3. Get new chat_id via @RawDataBot (forward a message from channel to bot)
4. Update `config/telegram_config.yaml` with new chat_id
5. Git commit + push to VM
6. Restart service: `ssh trading-vm "sudo systemctl restart trading-system"`

## Config file location
`config/telegram_config.yaml`

## Verification
After restart, trigger a test alert or wait for next signal to confirm alerts flowing.

## Priority
MUST complete before 29-Apr 09:15 IST market open - alerts are critical for monitoring paper trades.

**Status:** COMPLETE (2026-04-28 16:06 IST)
- New channel ID: <TELEGRAM_CHANNEL_ID_REDACTED>
- Local .env updated
- VM .env updated
- Service restarted
