---
name: stale_local_main_is_a_push_trap_02sep
description: "The worktree named `main` holds a branch 90 ahead / 94 behind origin/main - a plain `git push origin main` from it would overwrite the deployed SHA"
metadata:
  type: project
---

🔴 **`D:/Projects/trading-system-main` IS A PUSH TRAP.**

🔬 Measured 02-Sep-2026, at the moment of the GUI merge push:
- that worktree holds the local branch **`main`** at **`3dff752`** (22-Aug)
- **90 ahead / 94 behind** `origin/main`, diverging at **`645728d`** (07-Aug)
- its 90 unique commits are **docs-only**, and its tip's subject
  (`docs(register): provenance gate closes as (C)`) appears ⛔ **nowhere** on
  `origin/main`

⇒ 🔴 **`git push origin main` from that directory pushes `3dff752` OVER the
deployed SHA.** ⚠️ That is the **default form** of the command, in a directory
**named `main`**. ⭐ Only the use of an explicit refspec --
`git push origin <sha>:refs/heads/main` -- avoided it on 02-Sep.

⭐ **THE FIX, and it is one command:** ⭐ **RENAME the branch** so the default
command has nothing to resolve. ⛔ **Do not delete the worktree** -- those 90
commits are unexamined and may hold work that was never landed.

⚠️ **Sibling trap, same evening, same `D:/Projects/` root:** the PRIMARY tree
`D:/Projects/trading-system` is parked on `feat/delivery-config-split` with
uncommitted changes and an untracked `alerts/delivery.py` -- ⭐ and it is what this
session's inherited `PYTHONPATH` pointed at, which produced 4 phantom test failures.
⇒ ⭐ **Two of the directories under `D:/Projects/` are proven traps.**

⭐ Related: [[a_count_without_its_environment_is_not_a_baseline]] ·
[[install_collision_map_10aug]] -- the branch whose NAME matches the work is twice
now the wrong one to push.
