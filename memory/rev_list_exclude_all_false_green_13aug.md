---
name: rev-list-exclude-all-false-green-13aug
description: git rev-list --exclude= never applied to --all; a false green on a destructive op
metadata:
  type: project
---


## Index line relocated from `MEMORY_BOARD.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 869 B (budget 450 B). The index now carries a hook and this link.

- 🧨⚠️🔝 **⛔ NOT A NEW RULE — THE **SECOND** INSTANCE OF *"a green check is evidence ONLY if it could have been red"* (Rama, 13-Aug). ⭐ WHAT IS NEW: THE FIRST APPLICATION TO A **DESTRUCTIVE** OPERATION, WHERE A FALSE GREEN HAS **NO ROLLBACK**.** **(P) `git rev-list --count <b> --not --exclude=refs/heads/<b> --all` returned **0 unique for ALL TEN branches**; the explicit-ref form returns **9** for `main` — `--exclude=` never applied to `--all`.** ⭐ Caught ONLY because `main` is 38 ahead and 0 was implausible; ⛔ had `fix2` (genuinely 0) been measured first the bug would have been CONFIRMED BY ITS FIRST CASE and marked every worktree deletable. ⚖️ **The D2 md5 and the non-vacuity collected-counts are the same rule where being wrong is RECOVERABLE; ⛔ here it is not.** [[feedback-verify-rc-not-output]] [[tautological-check-class-05aug]]
