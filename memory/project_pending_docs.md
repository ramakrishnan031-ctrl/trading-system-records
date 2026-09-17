---
name: project-pending-docs
description: "6 Word documentation docs pending (deferred from pre-live list, Item 60)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6dc0b34-b28a-4065-8bcc-d317b22c1ef2
---

PENDING DOC ITEMS (6 Word docs -- pre-live, before micro-live):

1. **System architecture overview** -- main.py flow, all components, startup phases, event loop
2. **Strategy YAML config guide** -- all fields explained, valid values, scoring weights
3. **Daily operations runbook** -- morning startup, EOD checklist, troubleshooting common issues
4. **DB schema reference** -- all 22 tables, key columns, relationships, indexes
5. **Incident response guide** -- kill switch triggers, capital mismatch, broker API down, recovery procedures
6. **Deployment guide** -- VM setup, cron schedule, token flow, zerodha_morning.bat, systemd services

**Why:** Operational documentation needed before scaling beyond single-operator.
**How to apply:** Write when time permits; not blocking for trading. All operational knowledge currently in mempalace + CLAUDE.md + inline docs.
