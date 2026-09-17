---
name: Memory hygiene rules (MH1-MH6 + WCH1-WCH5)
description: When and what to save in memory; Web Claude context discipline; user bridge responsibilities
type: feedback
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
modified: 2026-07-24T09:21:23.439Z
---
Locked 2026-04-16. Store memory at these trigger points:

**MH1 — End of every module build (after test suite green + locked decisions written):**
One memory entry with: module name + path, total tests passed (cumulative + this module), locked decision IDs added, schema version after this module, cross-module impacts, any deviations from instruction file.

**MH2 — On every locked_decisions.yaml edit:**
Store: which decision IDs added/changed, justification, affected modules.

**MH3 — On every schema_version bump:**
Store: old version → new version, table changes, migration notes. Critical for restart-safety.

**MH4 — On every cross-module bug fix:**
Store: bug description, root cause, files touched, regression test added.

**MH5 — On every deviation from Web Claude's instructions:**
Store: what spec was given, what was built, why deviation was justified (locked_decisions.yaml override, etc.).

**MH6 — Daily memory consolidation (end of each working session):**
Store: modules built this session (list + paths), total test count delta (start → end), open issues/TODOs, next planned module.

**Why:** Context is lost across 20+ modules. Running test count + locked decision IDs must be tracked so Web Claude can stay aligned without reconstructing state from scratch each session.

**How to apply:**
- Never skip MH1 after a green suite — it is the primary recovery mechanism.
- MH3 is critical: schema_version mismatches silently corrupt startup recovery.
- For Web Claude (WCH rules): always request relevant locked_decisions.yaml section before writing a new module instruction. Use locked IDs verbatim (e.g., "per G1, P14, EV6" not invented numbering). Treat locked_decisions.yaml as authoritative over ad-hoc spec; patch gaps, do not rebuild. Track running test count + module count in every reply preamble. At session start with no recent context: ask user to paste current test table + last 3 locked decision IDs.

**MH7 (24-Jul-2026) — the MEMORY.md byte-budget `awk` check is a DE-FACTO INTEGRITY GUARD, not just a length check. Do NOT remove or weaken it when "cleaning up."** It has caught line-BOUNDARY corruption TWICE — the 23-Jul compaction's 3-newline merge, and the 24-Jul leading-newline collapse — both times a guard built to enforce line LENGTH flagged a merged/damaged line an over-budget length revealed. **Companion lesson:** to DELETE a whole index line via the Edit tool, match `[line]\n` (a TRAILING newline) — a LEADING `\n[line]` collapses both newlines around the target and MERGES its neighbours into one over-length line.
