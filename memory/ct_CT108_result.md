---
name: ct-ct108-result
description: "CT108 Network Drop 5min — PASS_WITH_RISK, system survived but network_controller blocked SSH (tool bug fixed)"
metadata: 
  node_type: memory
  type: project
  originSessionId: b1f5f4b4-3390-48a3-8b95-770fe53c2346
---

**CT108: Network Drop 5min** — PASS_WITH_RISK | 09-Jun-2026

System survived the 5-minute total network outage (block_all_outbound).
Kill switch activated correctly, recovery detected after unblock.

**Risk finding:** network_controller.py `block_all_outbound` preset only had `--dport 22` ACCEPT rule, which protects SSH client connections FROM the VM but not SSH server RESPONSE packets (which have `--sport 22`). This blocked all SSH sessions to the VM, requiring a reboot to recover.

**Fix applied:** Added `--sport 22` ACCEPT rule before the DROP, so SSH server responses are always allowed. This is a test tool bug, not a trading system bug.

**Why:** Safety-critical — test tools must never lock operators out of the VM.
**How to apply:** Any future network presets that use broad DROP rules must preserve SSH (sport 22 + dport 22).
