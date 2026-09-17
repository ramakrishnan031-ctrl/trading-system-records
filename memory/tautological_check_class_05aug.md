---
name: tautological-check-class-05aug
description: A check with no failing input manufactures confidence — expand every proposed verification and name a value that would make it fail. Three instances in one day.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4eb48114-5788-48ac-94d6-e91b992a6fe4
  modified: 2026-08-05T07:56:16.867Z
---

⛔⛔ **BEFORE PROPOSING ANY VERIFICATION, EXPAND IT AND NAME A VALUE THAT WOULD MAKE IT FAIL.
If no such value exists, it is NOT A CHECK — it is an identity wearing a check's clothes.**
Registered as **`campaign_practices.md` §V5**, 05-Aug-2026.

🔑 **THE INCIDENT, AND IT WAS OURS:** the operator was to be handed, as his confirmation that a live
`CRITICAL Capital Drift` was benign:
`delta == (opening − actual) + (expected − opening)`.
⛔ **Expand it: `opening` CANCELS** ⇒ `delta == expected − actual`, which is **the definition of
`delta`** ⇒ **it holds for ANY value of `opening`** — right, wrong, zero, a million. It was offered
with *"the arithmetic closes to the paisa, which is why I am putting it in front of you"*, and **the
closing-to-the-paisa was a property of ALGEBRA, not of the account.**
⭐ **Caught by the implementer, not the author.** The conclusion survived — but on the **structural**
finding (`snapshot.total` vs `margins.net` are different quantities), ⛔ **not on the sum.**
⇒ [[capital-drift-is-operand-mismatch-05aug]]

⭐⭐ **WHY IT IS DANGEROUS AND NOT MERELY USELESS — the asymmetry that earns the rule:**
**A tautological check MANUFACTURES CONFIDENCE.** It presents as *"the arithmetic closes exactly"*,
which is precisely the sentence a tired operator **stops reading after**.
⇒ **A MISSING check leaves you UNCERTAIN. A TAUTOLOGICAL one leaves you WRONGLY CERTAIN.**
The failure mode is not a coverage gap — it is **false assurance delivered in the voice of evidence.**

**THREE INSTANCES IN ONE DAY ⇒ A CLASS, not a slip — all three on artifacts about to reach an operator:**
1. **the `stuck_exiting` grep** — asked *"has this path ever fired?"*, but that path returns
   `check_name="MANUAL_CLOSE"`, **byte-identical to CHECK1's own**, and logs only on failure ⇒ no
   observable difference from its target. **DELETED.**
2. **the identity above** — no failing input exists. **REPLACED** with comparisons against
   *independent* quantities (the broker's own `used margin`; the day's booked P&L).
3. **the `2>/dev/null` grep** — a missing log file gave clean output that read as *"no locks"* ⇒ the
   failure was **suppressed**, not absent. **FIXED.**

**THE TEST, IN PRACTICE:** say out loud what value would turn this RED. **If you cannot name one, you
have not written a check.**

⛔ **DISTINCT FROM ITS NEIGHBOURS — do not fold it in:** **V4** = a test asserting what a **stub was
told** to return (the seam is mocked). **V5** = a check with **no failing input at all** (nothing is
mocked; the arithmetic itself cannot fail). **M8** = not **reading** the record. ⇒ **three different
ways to hold a worthless piece of evidence.** [[read-the-map-first-05aug]]

Related: [[feedback-verify-rc-not-output]] (*a green check is evidence only if it could have been
red* — V5 is that rule turned on a **formula** instead of on a **run**).
