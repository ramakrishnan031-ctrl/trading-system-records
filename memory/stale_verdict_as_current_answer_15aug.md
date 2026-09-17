---
name: stale-verdict-as-current-answer-15aug
description: "Rama's 15-Aug ruling — when a panel answers a NOW question, the freshest measurement governs; showing a stale verdict as the current answer IS the unsafe act, and \"I must not invent a verdict\" does not license it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f7680a01-c58d-40df-8d4b-65bca6443142
  modified: 2026-08-15T08:35:05.637Z
---

⛔ **A STALE MEASUREMENT DISPLAYED AS THE *CURRENT* ANSWER IS ITSELF THE UNSAFE ACT.**

**The incident (15-Aug-2026, Screen 12 System Health).** The page rendered
`Overall Status = FAILED` · `Trading Engine = FAILED` · **`Trading Readiness = READY`**.
I had made preflight's `09:14` verdict the headline and merely printed a
contradiction warning underneath it.

**Rama rejected it, quoted:** *"Make the live readiness verdict authoritative …
A stale preflight READY result must never remain the main current READY state
after a required live service has failed."*

**Why:** I had argued *"the GUI is not the authority to declare NOT READY"*.
That is true in the abstract and ⛔ **irrelevant**. The panel's headline question
was *"is trading safe RIGHT NOW?"* — so answering it with a stale yes is not
neutrality, it is a wrong answer to the only question being asked. And applying
the source system's OWN rule (a required component down ⇒ unsafe) to LIVE data
is ⛔ not a new policy: it is the same policy read against a fresher clock.

🔑 **THE GENERAL FORM, and it will recur:**
⛔ ***"I must not invent a verdict"* does NOT license *"so I will show a stale
one"*.** Those are not the only two options. The third — and correct — one is:
**the freshest measurement governs the headline, and the older verdict is
retained beside it, explicitly labelled as history with its own timestamp and
marked superseded.**

**How to apply:**
1. For any panel that answers a *now* question, ask **what clock is the headline
   figure on?** If it is older than a signal that could contradict it, it is
   ⛔ not the headline.
2. Keep the older verdict — ⛔ deleting it loses provenance — but **demote it
   visually** (smaller, tagged `HISTORICAL`, timestamped) so it cannot be read
   as current.
3. When combining two gates, **both must permit**; and an UNMEASURABLE gate
   yields a third state (`NOT CONFIRMED`), ⛔ never a pass and ⛔ never a
   fabricated failure. See [[feedback_absence_needs_wide_check]].
4. Publish **which inputs were allowed to gate the verdict**, so the basis is
   auditable rather than buried in code.

⚠️ Related: [[feedback_status_label_rule_27jul]] (`DEPLOYED` ≠ `VERIFIED LIVE` —
a label never ripens with time) and [[feedback_verify_rc_not_output]] (a green
check is evidence only if it could have been red). This entry is the *display*
counterpart: a green **reading** is evidence only if it is still current.
