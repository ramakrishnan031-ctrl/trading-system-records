---
name: Holiday alert investigation (2026-05-07)
description: 4th report of holiday spam; exhaustive VM check found ZERO evidence of alert on 07-May; likely old message from 01-May Maharashtra Day
type: project
originSessionId: 80c0c78f-481f-491b-832f-8aed476df7de
---
## Investigation Result: FALSE ALARM (2026-05-07)

User reported holiday alert spam for 4th time. Exhaustive check found:
- ZERO "MARKET IS CLOSED" messages in entire journalctl history
- ZERO holiday-related entries in system_2026-05-07.log
- 07-May is NOT in nse_holidays_2026.yaml
- Sentinel code IS deployed and correct
- VM timezone correct (IST), date.today() returns 2026-05-07

**Why:** Most likely explanation: user seeing old Telegram message from 01-May (Maharashtra Day). Journal doesn't go back that far (starts May 4).

**How to apply:** If reported again, ask user to screenshot the Telegram message with timestamp. The sentinel anti-loop code at main.py:774 IS functional. No code change needed.

**Separate issue found:** System ran on 04-May (Sunday) without holiday guard stopping it — possible cron/systemd start bypasses the guard on weekends. Investigate if it matters for paper mode.
