---
name: feedback-no-rm-rf-from-variables
description: "Rama interrupted a QA script for building `rm -rf` out of shell variables; use explicit literal paths and shapes that refuse"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8d2a242-be98-4728-bf5d-fb772e95b3fa
  modified: 2026-08-17T17:44:09.304Z
---

⛔ **NEVER build `rm -rf` (or any recursive/forced delete) from shell variables.**
Rama INTERRUPTED a Screen-17 browser-QA command on 17-Aug-2026 that ran
`rm -rf "$S/$prof"` to reset temp Edge profile dirs. If either variable were
empty or unset it expands to a catastrophic path.

**Why:** this is the same hazard as [[MEMORY]]'s standing rule that four live
`venv` symlinks under `D:/Projects/` point into the shared object store — a
wrong path or a followed link takes every branch in the campaign. A QA
convenience script is not exempt from it.

**How to apply:**
- Temp/profile paths must be **explicit, literal, created with `mkdir -p`, and
  never deleted by a variable-built command**. Prefer using a fresh directory
  over deleting an old one; leaving a temp dir in the session scratchpad costs
  nothing.
- When a delete is genuinely required, use a shape that REFUSES: `rmdir` for a
  directory, plain `rm` (no `-r`, no `-f`) for a symlink, `rm -f <literal path>`
  for one known file.
- ⛔ Do not bypass a safety prompt to finish generating screenshots. Rama listed
  this explicitly as a QA-script requirement.

⭐ Also from the same session: python `print()` of `⛔`/`—` crashes on this PC's
cp1252 stdout and can abort a script MID-RUN after earlier steps already wrote
files. Use `sys.stdout.reconfigure(encoding='utf-8')` first, or don't print
non-ASCII.
