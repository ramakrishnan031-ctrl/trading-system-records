---
name: a_count_without_its_environment_is_not_a_baseline
description: "A test count is not a baseline unless its interpreter, PYTHONPATH, cwd and invocation are recorded with it - a recorded GUI baseline was invalidated by an inherited PYTHONPATH"
metadata:
  type: project
---

🔴 **A COUNT WITHOUT ITS ENVIRONMENT IS ⛔ NOT A BASELINE -- IT IS A NUMBER.**

🔬 **The measured instance, 02-Sep-2026.** The GUI suite on the merged tree
returned **5F / 2167P** against a recorded baseline of **1F / 2171P** -- four new
`ImportError`s resolving `ops_dashboard.*` against `D:/Projects/trading-system`,
⛔ **a different worktree**, parked on `feat/delivery-config-split`, which has no
S17 `controls.py`.

⭐ **Cause:** the session inherited **`PYTHONPATH=D:/Projects/trading-system`**,
and the GUI suite runs with cwd `.../ops_dashboard`, which contains ⛔ **no**
`ops_dashboard` package -- so every `from ops_dashboard... import` fell through to
that env var.

⭐ **Proven three ways on the BASELINE COMMIT ITSELF (`0bbe127`), ⛔ not on the
merge:** inherited -> **4F** · cleared -> **4F** ·
`PYTHONPATH=<root of the tree under test>` -> **36 passed, RC 0**.
⇒ ⭐ the failures existed at the baseline; ⛔ **the merge caused none of them.**

🔴 ⇒ **A RECORDED BASELINE WAS RETROACTIVELY INVALIDATED.** B (1F/2171P) had
been measured in a **different environment** than C. ⭐ It was re-measured under the
corrected environment and reproduced **exactly** -- ⭐ and that, ⛔ not the
original record, is what makes the Δ0 claim trustworthy.

⭐ **THE RULE:** ⭐ **every comparison pair must share an environment, and the
environment must be recorded beside the number** -- ⭐ interpreter · `PYTHONPATH`
· cwd · the exact invocation. ⭐ This extends §V2's *"the interpreter is
part of the baseline"* to the whole environment.

⭐ **OPERATIONAL:** ⭐ the GUI suite must run with **`PYTHONPATH` = the root of the
tree under test**. ⭐ The trading gate is immune (`python -m` puts cwd first) and its
`.env` is unreachable (`find_dotenv` walks *up* from cwd).

⚠️ ⭐ **Same family as G7.1, which fired the same evening:** both test wrappers
reported **exit 0** while pytest's own RC was **1**. ⇒ ⭐ twice in one night an
instrument reported clean while the thing it measured was not.

⭐ Related: [[feedback_no_fixed_test_baseline]] · [[feedback_verify_rc_not_output]]
· [[stale_local_main_is_a_push_trap_02sep]].
