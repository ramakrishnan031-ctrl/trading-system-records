---
name: f6-deploy-authorised-08aug
description: "Rama AUTHORISED the F6 deploy on 08-Aug-2026 — YES, Monday evening, leave the DIFFNKG GTT. The three verbatim lines, the resolved first-live date, and why authorisation is not readiness."
metadata: 
  node_type: memory
  type: project
  originSessionId: 35a1c3dd-75a3-42ce-bdc5-d5e981dad58a
  modified: 2026-08-08T06:59:55.480Z
---

# 🟢 F6 DEPLOY — AUTHORISED 08-Aug-2026. ⛔ AUTHORISED ≠ READY.

**RECORD ON DISK (⛔ not a chat window), Rama asked for this explicitly:**
`docs/decisions/AUTHORISATION_f6_deploy_08aug2026.md` — the record ·
`docs/decisions/GO_NOGO_f6_deploy.md` — the eight-line gate ·
`docs/decisions/RUNBOOK_f6_first_live_acceptance.md` §0.2 — the Monday timeline.

## THE ANSWER — ⛔ quoted, never paraphrased

> **RAMA, 08-Aug-2026:**
> **1. Deploy F6: YES**
> **2. Window: MONDAY evening**
> **3. DIFFNKG GTT 330944932: LEAVE IT**

Card = `DECISION_CARD_02` **rev 2**. ⚠️ An answer to rev 1 would not have been an answer to
rev 2 — the changed sentence is the reversibility one. ⛔ **No clock time was given; none was
invented.** Record written `2026-08-08 11:58:37 +05:30` (PowerShell `Get-Date`).

## 🗓️ THE DATE, RESOLVED ONCE

**MONDAY evening = 10-Aug-2026** ⇒ 🔑 **F6's FIRST LIVE EXECUTION = the 08:15 boot of
TUESDAY 11-Aug-2026.** ⛔ Written as a DATE — *"Tuesday"* alone is what lets a wrong Tuesday be
followed a week later. **(P)** `Get-Date`: 08-Aug Sat · 10-Aug Mon · 11-Aug Tue.
**(P)** `nse_holidays_2026.yaml` whole file, ISO dates ⇒ grep `2026-08` would have found one:
**ZERO** August entries. ⚠️ The one August string is a **COMMENT** (`15-Aug (Sat)`), not data.
⛔ The runbook's §1.0 table STAYS parameterised — only this instance is resolved.

## 🔑 THE RULE THIS EARNED — `G12`, parent `G10`

⛔ **"He said YES" is not a precondition met; it is permission to ATTEMPT the preconditions.**
`G10` named the conflation in the direction of DELAY (design-complete read as authorised).
⭐⭐ **This is the mirror, and it is the dangerous one: it points at a live machine, not at a
delay — because an authorisation in hand FEELS like a precondition already met.**
⇒ record and gate are **SEPARATE FILES**; the gate is ONE SCREEN, run immediately before the
push, and carries *"authorisation does not override this line"* on its face.
⛔ **ANY single NO defers, with the failed line named in one plain sentence.**

## 📏 SCORING RULES — added 08-Aug, ⛔ THREE STATES AND FOUR PHASES

🔑 **GATE LINE 2 WAS AMBIGUOUS AND WOULD HAVE BITTEN AT 18:30 MONDAY:** E5 is a declared
CANNOT-DETERMINE, so if the GTT resolves at the boot E5 is `NOT TESTED` — its CORRECT outcome —
and nothing said whether *"E1-E7 SCORED"* was then satisfied. ⇒ somebody improvises on a live
deploy, or defers one that should have gone. ✅ **FIXED, one sentence: SCORED = each of E1-E7
carries a RECORDED OUTCOME; `NOT TESTED` IS one and SATISFIES the line; ⛔ a BLANK does not.**
⭐⭐ **The distinction is *"we looked and it did not happen"* vs *"we did not look."* The first is
EVIDENCE, the second a GAP.**

⛔ **THREE OUTCOMES EVERYWHERE Mon+Tue are scored: `PASS` · `FAIL` · `NOT TESTED / NA`. NEVER
force a non-test into a FAIL.** Two live cases: **E5 unfired = NOT TESTED, ⛔ never PASSED**, and
**the absence of a shutdown census at boot is NOT a failed census** — the census is a *SHUTDOWN*
stage. ⚠️ The second would look like a broken boot on the morning of a deploy.

🏷️ **FOUR PHASES, not three — `PRE-EXISTING` · `MONDAY-BOOT` · `DEPLOYMENT-TRANSITION` ·
`F6-FIRST-LIVE` · `UNKNOWN`.** The old `BEFORE/WEEKEND/BOOT` stopped at Monday morning.
⭐⭐ **After Tuesday EVERYTHING anomalous will look like F6, because F6 is what changed — a label
applied BEFORE the deploy is the only thing that can later say "this was already there."**
⛔ **`UNKNOWN` MUST stay available: forcing a label is how a LATENT defect gets attributed to the
change that merely REVEALED it.**

⛔ **AN OPEN ITEM IS NOT AUTOMATICALLY A BLOCKER (runbook §1.3, recorded ONCE) — one question,
PER ITEM: *does it invalidate an F6 ASSUMPTION or a DEPLOYMENT PRECONDITION?* NO ⇒ stays open,
deploy path unchanged. YES ⇒ gate line 3 = NO ⇒ defer.** ⭐ ⛔ Neither an informal gate because
it sounds important, nor a wave-through because it sits outside Card 02.

## 🎯 THE GTT — ruled, ⛔ and the ruling did not rewrite the analysis

**LEAVE IT** — Rama's conscious choice, told what it costs. **It binds in BOTH directions:**
⛔ **it is NOT now "safe", and it must NOT be cancelled later as a precaution** — that would
contradict an explicit decision, and "cancel to be safe" is the shape a future reader reaches
for. Unchanged: cancelling does **not** achieve its original objective (`:513` rebuilds it in
market hours, same triggers); leaving it carries an **unquantified tail**; §11.5's matrix is
**one-dimensional** — mechanical dominance only, the tail is in none of its cells.
⚠️ If the GTT is deleted at Monday 08:15, score **E5 = NOT TESTED**, ⛔ never "passed".

## ⛔ WHAT IS STILL OWED

**RAMA, MONDAY EVENING: the manual stop is LOAD-BEARING FOR THE DEPLOY** — precondition 5
needs the service DOWN, the tool layer is denied `sudo`, and `eod_self_exit` **defers** on an
open carry. ⛔ **Do NOT `restart` to achieve it** — `active` at 08:15 ⇒ *"nothing to do"* ⇒
**Tuesday's boot never happens.**
⛔⛔ **The nightly stop stays compulsory Monday, Tuesday and every night after, until §2 passes
on an OBSERVED LIVE EVENING.** ⭐ Deploying does not retire it. F6 §15.2's five criteria: all
unmet. ⚠️ **Paper cannot rehearse ANY of this — no T+1 settlement ⇒ a green paper run is not
pre-validation.**

## 🆔 BUILD IDENTITY — FROZEN

`HEAD 5b2d6499bc58…` · tree `892a9d4d0d63…` · `ahead 26` **(re-measured; the ledger's 21 is
SUPERSEDED)** ⛔ **the ahead-count is NOT the identity.** Executable subject `c39e799` +
`4f91784` *(comment-only, verified from the diff)* + `c315908`. md5 manifest of all 9 non-doc
files in the record §4.2. ⛔ Nothing about F6 changes before the deploy — a further review gets
**FILED**, ⛔ not folded in.

Related: [[f6-delivery-exit-abs-defect-06aug]] · [[reversibility-two-claims-08aug]] ·
[[delivery-carry-blocks-shutdown-05aug]] · [[feedback-status-label-rule-27jul]]
