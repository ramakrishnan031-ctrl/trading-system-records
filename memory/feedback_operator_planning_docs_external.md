---
name: feedback_operator_planning_docs_external
description: "Operator CARDS + decision sheets stay external and git-excluded. ⚠️ CHANGED 28-Jul-2026: the REGISTER is now the EXCEPTION — Rama ordered it committed, and it lives TRACKED at docs/MASTER_PENDING_28-Jul-2026.txt. Consolidation of the seven editions is DONE; the sole-copy hazard is discharged."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 20d49820-4aec-41c6-8377-564b6e4855d9
  modified: 2026-07-28T15:00:15.183Z
---

## ⚠️⚠️ 28-JUL-2026 — READ THIS BEFORE THE RULE BELOW. THE REGISTER HALF IS OVERRIDDEN.

> **RAMA, 28-Jul:** *"Write it to Downloads AND **commit it into the repo** so it is versioned and
> survives a lost laptop — check first whether a canonical repo location already exists."*

⇒ ✅ **THE CONSOLIDATED REGISTER IS NOW A TRACKED REPO ARTIFACT:
`docs/MASTER_PENDING_28-Jul-2026.txt`** (commit `d5b9d8c`, local, unpushed until Thu 30-Jul).
A read-copy also sits in `Downloads\`, md5-identical.
⭐ **The location was FOUND, not invented** — `docs/` already tracked `T2_RUNBOOK_29-JUL.txt`,
`DEPLOY_CALENDAR_28-JUL_TO_04-AUG.txt` and `MONDAY_27-JUL_CARD.txt`.

🔑 **THE BLOCK WAS `.git/info/exclude:29`, NOT `.gitignore`** — a grep of `.gitignore` finds
nothing and is the WRONG FILE. Diagnose with `git check-ignore -v <path>`, never a grep.
⭐ **Narrowed by a NEGATION on the canonical path (`!docs/MASTER_PENDING_*.txt`), deliberately
NOT by loosening the glob** — a stray register at the repo root or anywhere else is STILL
excluded, so the 25-Jul rename-gap that rule was broadened to close STAYS closed. Verified both
ways. ⚠️ One-time unblock only: once tracked, git ignores no longer apply to a file.

✅ **CONSOLIDATION DONE — the 7 originals are SAFE TO DELETE and Rama has been told so.**
Reconciliation: **M = 118 carried (exact, enumerated by ID) · K ≈ 91 closed · J = 211 derived**
of ~420 appearances. ⛔ **J is a residual, not a measurement — do not quote it.**
⭐⭐ **THE HARVEST THAT JUSTIFIED THE JOB — it was NOT bookkeeping:** the liveness-probe item that
existed ONLY in the about-to-be-deleted 25-Jul EVENING file turned out to be **LIVE AND BITING**:
`liveness_probe.py:108 _LIVENESS_END = 16:00` vs `service_window_end: "17:35"` ⇒ **95 minutes
unwatched every trading day.** Now register §4 G1. [[feedback-absence-needs-wide-check]]
⚠️ **STILL TRUE, and now the register's §11(6) rule:** a new edition that DROPS a section is
SILENT LOSS with no dangling pointer to notice — **diff the SECTION HEADINGS before calling any
new edition a superset.**

⛔ **UNCHANGED — the CARDS and DECISION SHEETS stay external and excluded**
(`*_CARD.txt`, `TONIGHT_IF_PC_IS_DOWN_*.txt`, `*_DECISION_SHEET_*.txt`). Only the REGISTER moved.

---
*Historical, kept legible — the rule as it stood before the 28-Jul override:*

**Operator PLANNING docs are Rama's OWN external working files — NEVER a repo artifact, never `git add`-ed.**
This covers the master pending register (`MASTER_PENDING_REGISTER_*.txt`) and decision sheets
(`*_DECISION_SHEET_*.txt` / `DEPLOY_DECISION_SHEET_*.txt`). They are excluded via **`.git/info/exclude`**
(local, never pushed — NOT `.gitignore`, so the exclusion needs no push). Rama keeps them outside the
project root so they can't be pushed.

**DISTINCTION (do not confuse):** the tracked ANALYSIS lineage — the census/audit reports under
`docs/audit/` (`pending_reconciliation_*.md`, `fixes_*.md`, `monitoring_hardening_*.md`, etc.) — ARE
legitimate tracked repo docs and STAY tracked. Only the operator's *planning/decision* docs are external.

## ⭐⭐ STANDING RULE, TIGHTENED BY RAMA 27-Jul-2026 — the split is now EXHAUSTIVE

> **`Downloads\` carries the CARDS and the REGISTER. Nothing else.**
> **Every other report is a repo document: `docs/audit/<topic>_<DD>mon<YYYY>.md`.**

The old rule *permitted* reports in `docs/audit/`; this one **requires** it and **forbids** the
alternative. Downloads is reserved for the two artifacts Rama opens **under pressure** — the daily
CARD (`TUESDAY_28-JUL_CARD.txt`, `TONIGHT_IF_PC_IS_DOWN_*.txt`) and the current REGISTER edition.
Anything he reads at leisure — a decision package, an investigation, an operator write-up — belongs
in the repo, where it is versioned, diffable and survives a disk loss.

⚠️ **A decision package is a REPORT, not a planning doc.** It gets committed. Only the *register*
and the *decision sheets* stay external. Applied 27-Jul: `DECISION_check1_external_close_label.txt`
and `OPERATOR_backup_and_ssh_27-JUL.txt` were converted to markdown and committed as
`docs/audit/check1_external_close_decision_27jul2026.md` and `operator_backup_and_ssh_27jul2026.md`.

⭐ **And when a doc is archived into the repo, LIFT ITS LOAD-BEARING LINE INTO THE REGISTER FIRST.**
A fact that can only be reached by opening an archived document is a fact that will not be reached
at 2 a.m. 27-Jul's instance: *closing SSH port 22 would silently void the PC-down runbook, because
the phone has been off the tailnet 23 days* — that lives in §2 of the register now, not only in the
report. **Relocation must not demote a hazard.**

## ⛔⛔ 27-Jul — THE REGISTER LINEAGE HAS ALREADY LOST CONTENT. DO NOT DELETE OLD EDITIONS.

**MEASURED 27-Jul 23:1x:** the **25-Jul editions carry sections A–L**; the **27-Jul editions carry
0–9**. **F, G, H, I, J, K, L were not closed, not merged, not mentioned — they stopped appearing.**
Eight probes against the current edition, **all ZERO hits**: LIVENESS-PROBE/`_LIVENESS_END` · V3
DECISION CONTENT SPEC · `predeploy-*` · secondary_screener/M-S4 · first live HARD_KILL · leverage
gap · PARKED + re-examination trigger · EVIDENCE INFRASTRUCTURE/fs-v1.

⇒ ⛔ **`MASTER_PENDING_REVISED_25-Jul-2026_EVENING.txt` IS THE SOLE COPY of that content.** Memory
holds partial traces (2–4 files each) but none of the register-level gates.
⭐ **This is the DANGLING-POINTER failure one level up — a SILENT DROP, which is worse, because
there is no broken reference to notice.** ⚠️ **A quiet omission is indistinguishable from a
decision.**
🔴 **CONSOLIDATION DEFERRED, needs its own session** (2,678 lines / 5 editions; the bulk is the
1,238-line 25-Jul EVENING). ⭐ **The imminent one hiding in there: the LIVENESS-PROBE extension is
TRIGGERED if the 17:35 window is kept past week one — the window went live 27-Jul, so ~3-Aug — and
`_LIVENESS_END` must move with it. It exists in NO current file.**
Note left for Rama: `Downloads/DO_NOT_DELETE_READ_FIRST_27-Jul-2026.txt`.

✅ **The 25-Jul `.git/info/exclude` gap is CLOSED** — it now carries `MASTER_PENDING_*.txt`
(verified: `git check-ignore` matches the current `MASTER_PENDING_REVISED_27-Jul-2026_EVENING.txt`).
Extended 27-Jul with `*_CARD.txt` + `TONIGHT_IF_PC_IS_DOWN_*.txt`, since the cards are now a named
permanent Downloads artifact and were matched by nothing.

**Why:** these are Rama's living working files; committing them clutters the repo and risks pushing his
private planning to the VM/bare origin. On 16-Jul I mistakenly committed
`MASTER_PENDING_REGISTER_FINAL_16-Jul-2026.txt` to `main` (`55c1a98` + pointer `e7a6d70`); Rama moved it
out of root, and I excised those two UNPUSHED commits via `git reset --mixed daa36cd` (safe, working-tree
preserved) so the register never enters pushed history — a plain `git rm --cached` would have left the add
in `55c1a98` to transit on the next push.

**📍 CURRENT EDITION + LOCATION (25-Jul-2026):** the lineage lives in **`C:\Users\rama\Downloads\`** —
`MASTER_PENDING_REGISTER_FINAL_16-Jul` → `REVISED_19` → `21` → `22` → **`MASTER_PENDING_REVISED_25-Jul-2026.txt`**
(432 lines). None of it is tracked. ⚠️ The 25-Jul refresh instruction's §7.4 said "deliver it as a .txt
IN THE REPO"; that was refused on this rule (source wins) — doing it would have repeated the 16-Jul mistake.

**🔴 GAP FOUND 25-Jul, NOT FIXED (needs Rama — a build instruction said DOCUMENT-ONLY):**
`.git/info/exclude` carries `MASTER_PENDING_REGISTER_*.txt`, `DEPLOY_DECISION_SHEET_*.txt`,
`*_DECISION_SHEET_*.txt` — but **NOT `MASTER_PENDING_REVISED_*.txt`**. The lineage RENAMED itself
(`REGISTER_FINAL` → `REVISED`) on 19-Jul and the pattern was never updated, so
`git check-ignore` does NOT match the current naming ⇒ **a register dropped in the repo today would be
committable, exactly as on 16-Jul.** One-line local fix (never pushed): add `MASTER_PENDING_REVISED_*.txt`
(or broaden to `MASTER_PENDING_*.txt`) to `.git/info/exclude`.

**How to apply:** if asked to produce a pending register / decision sheet, write it where Rama wants
(often external) and DO NOT `git add` it; ensure `.git/info/exclude` carries the pattern. If one is found
tracked, untrack WITHOUT deleting his copy — and if it's baked into an UNPUSHED commit, excise that commit
(reset), don't just `git rm --cached`. Record findings/verdicts in memory (they survive), not by committing
his planning file. SYSTEM_MAP "Related Docs" + PATHS banner state this convention (`3b9041a`).
[[pending-register-16jul]] [[unpushed-pending-deploy-ledger]]
