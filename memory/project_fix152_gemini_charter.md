---
name: project_fix152_gemini_charter
description: "FIX-152 — GEMINI.md charter deployed to VM; Gemini's 8 roles, hard boundaries, and auto-discovery confirmed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 51c5587d-c908-4a66-9462-6843650ddb62
---

FIX-152 COMPLETE (2026-06-03, commit a3f4fa5): GEMINI.md deployed as Gemini CLI's operating charter.

**Why:** Gemini needed explicit role definition, hard boundaries, and daily workflow so it behaves as ops/audit/watchman and not as a developer or code-modifier.

**What was deployed:**
- `docs/GEMINI.md` — canonical copy
- `GEMINI.md` (project root) — auto-discovered by Gemini CLI (convention)
- 8 roles defined: CEO, Ops Manager, Auditor, Doc Writer, Watchman, Co-pilot, Security Manager, Coach
- Hard boundaries: read-all, write only to `reports/` and `docs/`; NEVER touch .py/.yaml/git/systemd
- Daily cron workflow documented (08:55 brief → 16:35 EOD review → 16:40 coach → 17:00 integrity)
- System context: schema v24, SQLite paths, key DB tables

**Verification:**
- `head -20 GEMINI.md` on VM confirmed file present
- Gemini CLI test confirmed correct understanding: "senior operations layer... watching, auditing, briefing... without modifying code or placing trades"
- Note: June 18 2026 — Gemini CLI migrates to "Antigravity CLI"; Gemini instructed to flag this in EOD reviews starting June 12

**How to apply:** Reference this when asking about Gemini's role boundary or when diagnosing unexpected Gemini behavior on VM.
