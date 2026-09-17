---
name: feedback-carry-the-countermeasure-09aug
description: The same instance-lookup defect shipped twice in six hours. Phase 0 produced the countermeasure (a bare-stub test) and it was not carried to Tick 2. A practice recorded but not carried is not adopted.
metadata:
  node_type: memory
  type: feedback
---

# 🔁🔴 **A PRACTICE THAT IS RECORDED BUT NOT CARRIED IS NOT ADOPTED**

**09-Aug-2026, twice in six hours, in two different subsystems:**
| | the call | where it broke |
|---|---|---|
| **Phase 0** | `self._alert_prefix(...)` | `_emit_signal_alert` on a 3-attribute stub → `AttributeError` **swallowed** ⇒ the alert vanished SILENTLY |
| **Tick 2** | `self._pipeline_for_intent(...)` | `_enforce_one_trade_per_symbol_direction` on a minimal stub → `AttributeError` **on a live ENTRY path** |

⭐ **Both were instance lookups on a live path where the EXISTING tests pass a minimal stub. Both were caught by the OLD tests. Both were INVISIBLE to the new tests — because the new tests use a real object.**

## **Why:**
🔑 **Phase 0 ALREADY PRODUCED THE COUNTERMEASURE** — a test asserting the method still works on a **BARE STUB** — **and it was not carried to Tick 2.** ⛔ Recording the lesson was the smaller half; the larger half is carrying the *artefact* into the next suite. ⭐ Six hours is short enough that no memory decay explains it: the gap is procedural, not cognitive.

## **How to apply:**
1. 📌 **Every new test suite that touches a CLASS METHOD on a live path includes ONE bare-stub case.** Construct the class with `__new__` or a 3-attribute stand-in, call the method, assert it does its job.
2. ⭐ **Make it BEHAVIOURAL, ⛔ not a source grep.** Tick 2's first guard grepped for `self._pipeline_for_intent`; a rename or a differently shaped lookup slips past that. The stub test cannot be fooled.
3. ⛔ **Helpers reached from a live path are `@staticmethod` and are called CLASS-QUALIFIED** (`Cls.helper(...)`), never `self.helper(...)`.
4. ⚠️ **THE ADJACENT-SUITE RULE, learned the same day: the adjacent set MUST include the test file NAMED AFTER THE THING BEING CHANGED.** Tick 2's regression was missed because I ran `test_signal_processor` / `test_state_store` / `test_risk_engine` and omitted `test_one_trade_per_symbol_direction.py`.
5. ⭐ **When a countermeasure is produced, write it into the NEXT card's checklist, not only into the record.** A rule in a memory file is not in the loop; a test in the suite is.

⭐ **Carried on 09-Aug to Tick 2 (`43f73b1`), Phase 2 and N9-07. From here it travels with every suite.**

See also [[alert-delivery-contract-phase0-09aug]] · [[tick2-pipeline-scoped-gate-09aug]] · [[feedback-tense-drift-09aug]]
