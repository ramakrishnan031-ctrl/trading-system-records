---
name: ct-ct029-result
description: "CT029 Signal at 14:46: PASS — signal accepted in entry window; EOD pre-alert is notification-only, doesn't block"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

CT029 | Signal at 14:46 (in entry window, near EOD pre-alert) | PASS | 08-Jun-2026

**Test:** Injected POWERGRID to range_breakout_long (HTTP 200, ACCEPTED). Entry window check passes for current time (within 09:25-15:00). Exact 14:46 timing cannot be tested now but mechanism is identical.

**Code verification:** EOD pre-alert (14:45 Telegram notification) is independent from signal acceptance. It does NOT set kill_switch or modify market_windows. The entry window (is_entry_allowed) only cares about entry_start_time/entry_end_time, not EOD pre-alert.
