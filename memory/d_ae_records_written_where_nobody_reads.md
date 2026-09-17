---
name: d_ae_records_written_where_nobody_reads
description: "D-AE — four separate times a record was written to a branch or root the next reader never looks at; documentation's twin of \"declared, built, started, yet inert\""
metadata: 
  node_type: memory
  type: project
  originSessionId: 31334cdb-96e4-4a09-bdf4-def39d5ad8ab
  modified: 2026-08-30T15:23:06.497Z
---

🔴 **D-AE — THE PROJECT'S DOCUMENTATION IS REPEATEDLY WRITTEN TO A BRANCH OR
ROOT THAT IS ⛔ NOT THE LINE THAT GETS READ.**

⚠️ ⭐ **FIVE INSTANCES. ⛔ THIS IS NOT FIVE ACCIDENTS — IT IS ONE DEFECT.**
⭐ **THREE of the five name a PATH THAT DOES NOT EXIST** (#2, #4, #5) — ⭐ that is the
dominant shape, ⛔ not misplacement.

1. 🔬 **Ledger Entry 22** existed ONLY on `587b306` (the held F2-CORE branch) —
   `grep 'Entry 22'` returned **0** on the push line. ⇒ ⭐ a session reading the
   ledger from pushed `main` would ⛔ never see the 7 held commits. *(Caught and
   fixed: the held-unit facts are duplicated onto the BOARD.)*
2. 🔬 **`~/doc/SYSTEM_MAP.md`** — ⛔ a path that **does not exist**. The real file
   is `docs/SYSTEM_MAP.md`. ⇒ ⚠️ **every card naming it was naming nothing.**
3. 🟢 **CLOSED 02-Sep-2026.** 🔬 **The S11–S13 `SYSTEM_MAP.md` / `PATHS.md`
   blocks** had landed on the **`gui09` branch only**, ⛔ never on the main lineage.
   ⭐ The 02-Sep merge (`686df1c`) put them on `main`; 🔬 `origin/main` = VM bare =
   VM deployed = `7d4970a`. ⛔ No longer owed.
4. 🔬 **`docs/MASTER_REGISTER.md`** — ⛔ absent from **every branch in the project
   graph**. A file of that name exists under
   `D:/Projects/trading-system-main/docs/`, **outside that tree**, in a clone
   **85 commits behind `effff24`**, pending refit. ⛔ **No assumption that the
   two are interchangeable.** ⚠️ Its 231 items were compiled in that stale tree
   ⇒ ⭐ the **contents** may be stale, ⛔ not merely misplaced.

5. 🔬 **`run_gate.sh`** — ⛔ a path that **exists nowhere in the repo**, on any
   branch. It was named as *"the project's own launcher"* in two consecutive
   instruction files, ⭐ sourced from the register's own **N20-19** entry.
   ⚠️ 🔴 **Following it naively had a live failure mode:** the only
   gate-shaped runner that DOES exist is **`run_tests.py`**, ⛔ the one the practices
   forbid — it collects the 44 never-gated `tests/crash_test/` tests that
   `load_dotenv()` the **real `.env`**. ⭐ The documented gate is the bare
   `pytest tests/unit tests/integration -q`. *(Caught 02-Sep by measuring before
   obeying: `git ls-files | grep gate` returned no such file.)*

⭐ **Instance 1 is now HALF-CLOSED too:** 🔬 F2-CORE's held-unit facts and its
`587b306` SHA were written into the **repo** `UNPUSHED_LEDGER.md` on 02-Sep
(`7d4970a`), where they previously existed **only in session memory**. ⚠️ The
branch's own *Entry 22* still lives only on `587b306`.

⇒ ⭐ **This is the documentation-layer twin of the campaign's central structural
risk:** things **declared, built and started — yet INERT.**

⭐ **NEXT-SESSION TASK — bounded, concrete, MEASURE-ONLY:**
Take **every path named in the standing memory directive** —
`mempalace` · `docs/SYSTEM_MAP.md` · `PATHS.md` ·
`UNPUSHED_PENDING_DEPLOY_LEDGER` / `MEMORY_BOARD.md` ·
`docs/MASTER_REGISTER.md` — and **verify each one exists on the working line.**
⛔ **Do not fix them in the same pass.** ⭐ Measure first, ⭐ then decide.

⚠️ ⭐ **A memory directive that names a non-existent path has been silently
unexecutable for an unknown number of sessions.** ⭐ That is the finding.

⭐ Related: [[a_count_without_its_environment_is_not_a_baseline]] ·
[[gui_review_needs_filled_data]] (the S11–S13 blocks) ·
[[s4_trigger_payload_is_discarded]] (the same night's other structural finding).
