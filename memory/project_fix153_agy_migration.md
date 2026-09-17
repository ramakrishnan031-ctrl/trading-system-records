---
name: project_fix153_agy_migration
description: "FIX-153 — gemini→agy migration, AGENTS.md, live flow trace; all 6 scripts updated"
metadata: 
  node_type: memory
  type: project
  originSessionId: b8fba364-d7b1-465d-aaaf-0503ef8286a7
---

FIX-153: Antigravity CLI migration + AGENTS.md + live flow trace (2026-06-04)

**Changes:**
- All 6 gemini_*.py scripts: `_GEMINI_BIN` default `"gemini"` → `"agy"`, flag `"-p"` → `"--print"`
- `deploy/systemd/trading-watchman.service`: `/home/ubuntu/tools/antigravity` added to front of PATH
- `scripts/gemini_watchman.py` rewritten (FIX-153):
  - `_tail_new_lines` now returns `(warning_lines, flow_lines, new_pos)` — single file read, two streams
  - `_FLOW_RE` matches: SIGNAL, SCREEN, ORDER, FILL, PROTECTION, CLOSE, CAPITAL, SL_TRAIL
  - `_append_to_flow_trace(flow_trace_dir, date_iso, lines)` — writes raw events to `reports/flow_trace/trace_YYYY-MM-DD.md` with no API call
  - `_eod_flow_summary(...)` — single agy call at EOD, appends 10-line summary to trace file
  - `run_watchman` accepts new `flow_trace_dir: Path` parameter
  - `--flow-trace-dir` CLI arg added
- `AGENTS.md` created at project root AND `docs/AGENTS.md` — identical content
  - 9 roles: CEO, Operations Manager, Auditor, Documentation Writer, Watchman, Co-pilot, Security Manager, Coach, **Live System Flow Observer (new)**
  - Hard boundaries: read-all, write only to reports/docs/tmp, never edit code/DB/git

**Why:** Antigravity CLI (agy) replaces Gemini CLI on VM; AGENTS.md is the cross-tool standard that agy reads automatically alongside GEMINI.md; flow trace = "flight recorder" with zero API cost during market hours.

**How to apply:** agy is now the default; set GEMINI_BIN env var to override. Flow traces land in `reports/flow_trace/`. EOD summary = 1 API call per day.
