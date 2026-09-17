---
name: a-floor-is-not-a-non-vacuity-check
description: "A \">= N\" guard cannot prove a scan is complete — it survives the scan silently halving. Assert an EXACT identity derived from the source instead."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d18f7831-33b0-47e0-9e35-d1354f8c5db5
  modified: 2026-09-02T08:40:45.754Z
---

🔬 **02-Sep-2026, S16.** A CSS-rule extractor I wrote scanned Screen 16's block
with `re.findall(r"(?:^|[{}])\s*([^{}@\s][^{}]*?)\s*\{([^{}]*)\}", block)`.

⛔ **THE ANCHOR CONSUMES THE BRACE, AND `re.findall` DOES NOT OVERLAP.** Each
rule's closing `}` was eaten by its own match, so it was no longer available to
anchor the NEXT rule. ⇒ 🔬 the scan returned **54 of 108 rules — every OTHER
one** — and the page-scope guard built on it was checking half the stylesheet.

⚠️ **WHAT LET IT SURVIVE: my own non-vacuity check was a FLOOR.**
`assert len(selectors) >= 30`, later `>= 55`. 🔬 A halved count still cleared
both. ⭐ **A floor cannot detect a halving. That is the whole lesson.**

## ⭐ THE RULE

**A non-vacuity check must be an IDENTITY derived from the source, ⛔ not a
threshold I guessed.** If a scan claims to find every X, express the count of X
independently and assert equality.

🔬 The fix here — and it DOES go red when the regex is reverted:

```python
block = _css_rules()                       # comments already stripped
expected = block.count("{") - block.count("@media")   # every { opens a rule or a media block
assert len(rules) == expected, (len(rules), expected)
```

⭐ Fixed the scan itself with a **LOOKBEHIND**, which asserts the brace without
consuming it, so consecutive rules are all found:
`r"(?:(?<=\})|(?<=\{)|\A)\s*([^{}@\s][^{}]*?)\s*\{([^{}]*)\}"`

## ⚠️ THE SECOND HALF — A FIXTURE CAN MAKE A SWEEP VACUOUS TOO

🔬 Same session: a test asserting *"no delivery-scoped key is left off the
panel"* **passed a mutation that should have killed it** — the shared `conftest`
fixture carries only **2 of the 7** delivery keys, so the sweep only ever saw
two. ⭐ Fixed by sweeping the DEPLOYED configuration as well as the fixture.

⇒ ⭐ **A sweep is only as strong as the set it sweeps. State what the set
contains, and sweep production's set too, ⛔ never only the fixture's.**

Related: [[feedback-no-fixed-test-baseline]] · [[feedback_verify_rc_not_output]] ·
[[visual_acceptance_is_a_separate_gate]] · [[browser_qa_measurement_traps]]
