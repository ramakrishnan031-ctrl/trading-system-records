---
name: expected-gap-is-still-a-claim-15aug
description: "A gap you EXPECT to find still needs proving — a grep that finds nothing proves only that one shape is absent, not that the system cannot evidence the fact."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f7680a01-c58d-40df-8d4b-65bca6443142
  modified: 2026-08-15T11:39:25.824Z
---

⛔ **A GAP I *EXPECT* IS STILL A CLAIM. Verify it as hard as a number.**

**The incident (15-Aug-2026, Screen 13 Audit).** The approved design's centrepiece
was an old → new value pair (`Max Orders 100 → 150`). A repo-wide grep for
`old_value` / `new_value` / `previous_value` / `changed_from` across every `.py`
and `.sql` returned **ZERO**, so I was about to report it as unbuildable without
fabrication.

It was buildable. `config_snapshots` stores the **full resolved AppConfig as
JSON**, one row per change, deduped by hash. Diffing consecutive rows yields
genuine field-level pairs — real recorded values, nothing invented:

    system.risk.max_daily_trades   10 → 8      [Risk / Risk Engine]

**Why the grep misled:** it searched for a *change-shaped* record. The system
never stores changes — it stores **states**, and the change is the difference
between two of them. The evidence existed in a completely different shape from
the one I searched for.

🔑 **THE GENERAL FORM:**
A negative grep proves **one shape is absent**, ⛔ not that the fact is
unrecoverable. Before declaring a gap, ask the second question:

> "Is there a table that stores the **state** this thing changes,
>  more than once?"

State + a second sample = a derivable change. The same trick applies to any
"we don't record X" conclusion: rates from cumulative counters, durations from
two instants, diffs from two snapshots.

**How to apply:**
1. Grep for the change-shaped record. If it is absent, ⛔ do not stop.
2. Grep for the **state** it would have changed, and check whether more than one
   sample is retained.
3. If a derivation exists, say plainly what it can and cannot support — here, the
   snapshot is written at STARTUP, so its stamp is when the system **observed**
   the configuration, ⛔ not when someone edited the file. Derive the value; ⛔
   never derive the timestamp semantics you wish you had.
4. If genuinely nothing exists, then state the gap **with the search width** —
   [[feedback_absence_needs_wide_check]].

⚠️ Note the symmetry with [[feedback_verify_the_finding_premise]]: that entry
says an audit *finding* is a hypothesis. This one says the same of an audit
*absence*. Both directions need evidence; a convenient "it cannot be done" is
just as unverified as a convenient "it is broken".
