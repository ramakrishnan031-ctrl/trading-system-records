---
name: project_crash_test_info_04jun2026
description: Crash test info gathering complete (04-Jun-2026); ~107 questions answered; output at docs/crash_test_info_04jun2026.md
metadata: 
  node_type: memory
  type: project
  originSessionId: b8fba364-d7b1-465d-aaaf-0503ef8286a7
---

Completed system info gathering for crash test planning (June 8-12). Output saved to docs/crash_test_info_04jun2026.md.

**Why:** Pre-crash-test survey covering architecture, state machines, kill switches, capital management, DB schema, cron jobs, AGY integration, security, and recovery paths.

**Key findings for crash test design:**
- 7 TEMP config values active (all safety thresholds raised — system won't kill switch on realistic losses)
- Signal queue is in-memory only (lost on crash — Chartink must retry)
- in_flight dict is in-memory (60s sweeper or restart clears stuck symbols)
- HMAC disabled in paper mode (webhook unauthenticated)
- 13 items UNCERTAIN (require live VM: disk stats, actual crontab, Python version, file permissions)
- Full rehydration works: fm_ledger + trades + orders → rebuilds complete state on warm restart

**How to apply:** Use findings to design targeted crash scenarios for June 8-12. Focus on: mid-signal crashes, kill switch persistence, TEMP threshold reversions, and concurrent allocation races.
