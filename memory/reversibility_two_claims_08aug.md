---
name: reversibility-two-claims-08aug
description: "G11 -- a decision card claimed a live change was undoable; the code reverts, the effects do not. State reversibility separately for code and for effects already produced."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 51de7c9e-6217-4982-91e7-d859d8edbcf0
  modified: 2026-08-08T06:07:53.176Z
---

# 🔴 `G11` — **"LOW-RISK TO INSTALL" AND "REVERSIBLE" ARE TWO DIFFERENT CLAIMS**

**(P) 08-Aug-2026.** `DECISION_CARD_02` **rev 1**, written for Rama to authorise deploying F6
to the live trading VM, said:

> *"Nothing changes about the database, and no settings are touched. If it goes wrong it can be
> undone by reversing the change and sending it again."*

**The first sentence was true but misleading** (no DDL, no schema-version change, no config key
— ⛔ but "nothing changes about the database" reads as *no data changes*, and F6 writes plenty).
🔴 **The second sentence was FALSE, and it was the one he would have decided on.**

## THE MECHANISM

Once F6 is live it **writes `TRIGGERED` markers · stamps `reservation_id` onto `RELEASE_USED` ·
RELEASES CAPITAL · CLOSES A TRADE · DELETES A BROKER-SIDE GTT · emits alerts.**

⛔ **`git revert` cannot un-delete a GTT at Zerodha, cannot un-release capital, cannot restore a
ledger row's prior meaning, and cannot un-ring an alert.**

## THE RULE

⭐⭐ **A change has TWO reversibility properties and they must be stated SEPARATELY:**

| | question | F6's answer |
|---|---|---|
| **① the CODE** | can the change be withdrawn? | ✅ **yes** — `git revert`, minutes |
| **② the EFFECTS ALREADY PRODUCED** | can what it did be undone? | ⛔ **NO** — broker-side deletions, capital movements, closed trades, sent alerts |

⛔ **Conflating them asks for consent to something the reader has not been told about.**
⭐ **And ② is precisely WHY a first-live evening is a GATE rather than a formality** — wording
that implies easy reversal quietly dissolves the reason the gate exists.

## THE CLASS IT BELONGS TO — overclaiming toward *"go ahead"*

Four more defects in the same card, all leaning the same way. ⭐ **The direction is the
finding:** not one of them overstated the risk.

- *"fully tested on my machine"* ⇒ **"regression-tested locally against the known baseline, zero
  new failures — IT HAS NEVER RUN LIVE."** ⭐ The honest version is the STRONGER one: the
  evidence itself says paper cannot exercise T+1 and two of the paper cases are vacuous.
- *"the earliest SAFE window"* ⇒ **"the earliest PLANNED window."** ⛔ **Never assert safety in
  advance of the check that establishes it.**
- *"it will tidy up the mess by itself"* ⇒ too soft; it hid an intentional accounting exception.
  Say plainly: **the P&L will be BLANK, and that row needs manual correction.**
- **a dependent question that was answerable standalone** ⇒ Q2 now reads *"ONLY IF YOU ANSWERED
  YES"*, so a bare "MONDAY" cannot be read as authorisation.

## 🔴 THE SAME BIAS REACHED THE PROCEDURE — found 08-Aug, one edit later

`RUNBOOK_f6_first_live_acceptance.md` §1 precondition 6 was written as *"the deploy COMPLETES
BEFORE **TUESDAY'S** BOOT ⇒ Tuesday's 08:15 boot is F6's first live execution."*
⛔ **That is true only if Rama answers MONDAY.** Card 02 Q2 offers **MONDAY or TUESDAY**, and on
TUESDAY the first live execution is **WEDNESDAY's** boot.

⭐⭐ **A PROCEDURE THAT PRESUMES THE ANSWER TO THE QUESTION IT EXISTS TO SERVE WILL BE FOLLOWED
PAST THE DECISION** — and it will read as correct while doing so, because every other line
around it is right. ✅ **Parameterised: *"before the NEXT SCHEDULED BOOT following the CHOSEN
window"*, with a two-row table, and the chosen window is read off the authorisation record —
⛔ never from the calendar, from momentum, or from which option was discussed most.**

🏷️ **Same direction as the five card defects: it assumed the permissive branch.** ⇒ the bias is
**not a wording habit in cards** — it reaches whatever is written next.

## HOW TO APPLY

**Before issuing any card that authorises a live change, answer both columns of the table
above, in the card, in plain English.** If ② is "no", say so and say what that means — ⛔ do not
soften it into ①. **Version the card and print the correction at the top** so a stale copy
cannot be answered by mistake.

Related: [[f6-delivery-exit-abs-defect-06aug]] · [[feedback-status-label-rule-27jul]] ·
[[feedback-verify-rc-not-output]] · [[decision-card-single-copy-risk-08aug]]
