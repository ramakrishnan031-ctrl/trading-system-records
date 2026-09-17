---
name: feedback-status-label-rule-27jul
description: "STANDING RULE (Rama via ChatGPT, 27-Jul-2026): every item in every report and register section carries one of BUILT / DEPLOYED / VERIFIED LIVE / PENDING DECISION / DEFERRED. The word 'fixed' was carrying five meanings. DEPLOYED is not evidence of anything — only VERIFIED LIVE is."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6e8fb467-3099-47da-9274-455643f9d43e
  modified: 2026-07-27T16:31:13.403Z
---

**⭐ STANDING RULE, 27-Jul-2026. Label every item with exactly one status. Never write "fixed".**

| label | means | what makes it true |
|---|---|---|
| **BUILT** | the code exists and its tests pass | a green gate on a branch |
| **DEPLOYED** | it is on `origin/main` **and** in the VM's working tree | the bare-repo HEAD and the deployed files agree |
| **VERIFIED LIVE** | ⭐ it has **demonstrably executed in production** | a log line, a DB row, an alert — an artifact it produced |
| **PENDING DECISION** | built or designed, waiting on Rama | named in the register as his |
| **DEFERRED** | deliberately not now, with a **reopen trigger** | the trigger is written down |

**Why:** "fixed" was carrying all five meanings at once. On 27-Jul Rama asked twice whether something
was "fixed" and the honest answer differed each time — six things were BUILT but not DEPLOYED, and
two were DEPLOYED but not VERIFIED LIVE.

## ⚠️ THE DISTINCTION THAT CARRIES THE WEIGHT: **DEPLOYED ≠ VERIFIED LIVE**

**This project has found NINE things that were built, looked alive, and had never run.** Deployment
proves a file is on a disk. It proves nothing about whether the code path was ever entered.

⭐ **A thing is VERIFIED LIVE only when it has produced an artifact in production.** Not "the service
started". Not "the tests pass". Something it wrote, in production, that would not exist otherwise.

⛔ **Do not upgrade a label because time passed.** DEPLOYED does not ripen into VERIFIED LIVE by
sitting there. Say what the artifact would be, then go and look for it.

⚠️ **And the sibling trap** — [[silent-failure-gaps-25jul]]'s pattern: *code that RUNS CONSTANTLY and
was never MEASURED*. Ask **both** of anything load-bearing: *has it run?* **and** *has it been
measured?* A thing can be alive, correct, exercised daily, and still unobserved. VERIFIED LIVE is the
first question; it is not the last.

## Worked example — CHECK1/CLASSIFY, 27-Jul

| item | status | why not the next one up |
|---|---|---|
| CLASSIFY (`2f8fd87`) + W8 writer (`77b8b04`) | **DEPLOYED** | on `d3fa5b8`, present in the VM tree — but the reconciler had not run since; **no CHECK1 verdict has been written in production** |
| `trades.closure_source` column | **BUILT, not yet DEPLOYED** | the *code* shipped; production was still on **schema 44** and the column did not exist. v45 adds it at the 28-Jul 08:15 boot |
| §D deferral `check1_mid_fill_defer_sec` | **DEPLOYED, INERT** | default `0.0`; 0 is proven a true no-op, so the path has never executed anywhere |
| the `closure_source` backfill | **PENDING DECISION** | written, guarded, unrun — it rewrites history, so it is Rama's |
| the exits thread | **DEFERRED** | reopen trigger: post-M-S4 re-derivation |

⭐ **The example that makes the rule concrete:** the 27-Jul decision package recommended *building*
CLASSIFY — while CLASSIFY was already DEPLOYED, pushed two hours earlier. One label would have caught
that before the document was written.

**How to apply:**
1. Every report section and every register line gets a label. Retrofit the open ones.
2. When asked "is X fixed?", answer with the label, not the word.
3. ⛔ Never claim VERIFIED LIVE without naming the artifact you saw.
4. A schema change is DEPLOYED only when the **migration has run**, not when the code carrying it has
   — the two are separated by a boot. [[schema-push-overnight-refusal-27jul]]

Related: [[feedback-verify-rc-not-output]] (a green check is evidence only if it could have been red)
· [[feedback-no-fixed-test-baseline]] (a number is a snapshot; say when it was taken)
· [[unpushed-pending-deploy-ledger]] (where DEPLOYED-vs-not is tracked per branch)
