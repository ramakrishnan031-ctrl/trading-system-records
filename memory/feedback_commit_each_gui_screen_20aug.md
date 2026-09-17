---
name: feedback-commit-each-gui-screen-20aug
description: "Rama, 20-Aug: every GUI screen gets its own LOCAL commit the moment it is done — plus the approval record and a ledger entry. Never batch screens into one commit, never push."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37a05d72-7ed6-4125-9a9c-d51a349642a6
  modified: 2026-08-20T17:33:29.305Z
---

**Rama, 20-Aug-2026: *"Always remember for local commits once one screen is done."***

⭐ **Each approved GUI screen ends with its OWN local commit — ⛔ never a batched one
covering several screens, and ⛔ never a push.** The full closing sequence per screen is:

1. **correction commit** (local) — the screen's code/CSS/test changes only
2. **approval record commit** (local) — the entry appended to
   `docs/audit/VISUAL_APPROVAL_LEDGER_19-Aug-2026.md`, carrying Rama's words verbatim
3. **UNPUSHED_PENDING_DEPLOY_LEDGER updated** immediately after, naming the commit SHA
4. **`PUSH = NO`, `DEPLOY = NO`** — the GUI branch stays local

**Why:** the screens are approved ONE AT A TIME, so the record has to be reviewable one
at a time too. A batched commit makes it impossible to see what a given approval
actually covered, and the approval ledger is the artefact Rama reads back.

**How to apply:**
- Commit as soon as a screen is verified — ⛔ do not carry uncommitted screen work into
  the next screen's session; a lost session then costs the whole screen (it already did
  once: the first S04 pass was lost and had to be redone from scratch).
- Keep the two commits SEPARATE — corrections and the approval record are different
  facts with different authority (mine vs Rama's).
- ⛔ No amend / rebase / merge of unrelated work to tidy the history.
- The open questions a screen raises are recorded as **approved WITH, ⛔ not resolved
  by** the approval — see [[unpushed-pending-deploy-ledger]].

⚠️ Related: [[feedback-status-label-rule-27jul]] — an approval is `APPROVED`, which is
⛔ not `DEPLOYED` and ⛔ not `VERIFIED LIVE`. The GUI branch is still unpushed.
