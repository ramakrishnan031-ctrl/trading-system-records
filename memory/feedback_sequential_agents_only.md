---
name: feedback-sequential-agents-only
description: "Rama's rule (04-Jul-2026): NEVER run multiple audit/subagents in parallel — one agent at a time, collect its report, then start the next"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f39c9932-1562-4657-8d80-d3327d287983
---

# Sequential agents only — no parallel fan-out

**Why:** On 04-Jul-2026 an 11-agent parallel audit fan-out burned the entire API session limit twice; all agents were terminated mid-work with zero reports returned ("API burned and all were wasted" — Rama).

**How to apply:** For any multi-agent work (audits, sweeps, migrations): launch ONE agent, wait for its completed report, then launch/resume the next. Never batch-launch. Interrupted agents can be resumed via SendMessage with their agentId (context preserved) — prefer resuming over relaunching. Related: [[full-repo-audit-04jul-pending]]
