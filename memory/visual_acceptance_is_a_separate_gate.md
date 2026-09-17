---
name: visual_acceptance_is_a_separate_gate
description: "Rama's 01-Sep-2026 ruling on S17 — no-overflow, no-overlap and green tests are NOT evidence a screen matches its artwork. Visual match is a separate acceptance gate, and it must be MEASURED against the PNG, not asserted."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bec7a3ec-e183-4b2b-ba82-32af4e73fcb2
  modified: 2026-09-01T16:37:32.809Z
---

👤 **RAMA, 01-Sep-2026, rejecting the first S17 Controls render:**

> *"The previous review incorrectly treated functional correctness, panel
> non-overlap, and regression results as evidence that the screen was visually
> matched. That is not sufficient."*
> *"A layout can have zero overlap and still be badly designed."*
> *"Do not report PASS merely because: there is no overflow · there is no overlap
> · tests pass · the browser loads · the data is truthful."*

⛔⛔ **HE WAS RIGHT.** I had reported exactly that list as acceptance.

## ⭐ THE RULE

**Functional correctness and visual match are TWO gates. Passing the first says
NOTHING about the second.** ⛔ Never present overflow/overlap/test metrics as
evidence of design fidelity — they are necessary, ⛔ never sufficient.

## 🔬 HOW TO ACTUALLY MEASURE VISUAL FIT

⭐ **Measure the ARTWORK, then measure the RENDER, then diff the numbers.**
⛔ Do not eyeball, and ⛔ do not trust a screenshot that has been scaled.

```python
# panel boundaries from the PNG — a dark theme defeats a brightness threshold,
# so use EDGE DETECTION on the gradient instead
gx = np.abs(np.diff(np.asarray(im.convert("L")).astype(int), axis=1))
vscore = (gx > 12).mean(0)      # columns with many strong edges = panel borders
```

Then in the browser, at a TRUE viewport (see [[browser_qa_measurement_traps]]):
`document.documentElement.scrollHeight / innerHeight` · the set of distinct
panel `top` values · each row's widths and heights.

🔬 **What that found on S17, which no functional metric had:**
· page **2366px = 2.19× the viewport**, against artwork whose own 1536×1024
  proportions imply **~1280px** at 1920 wide;
· **NINE scattered row-tops** against the artwork's **FOUR clean bands**;
· row-2 widths 360/495/495 against the artwork's measured **11 : 34 : 24**.
⭐ The HORIZONTAL composition was already correct (rail at 1584 vs the PNG's
1582) — ⭐ **the entire failure was vertical**, and only the numbers showed it.

## ⭐ THE USUAL CAUSE: ONE UNBOUNDED PANEL

🔬 Three panels with no height bound (`12. HISTORY` 814px, a rail history 525px,
a limits panel 564px) dragged their whole rows down and destroyed the rhythm.
⭐ **The fix is to bound the long list and let it scroll INSIDE its footprint** —
⛔ never to delete panels or hide data, and ⛔ never to shrink everything else.
⚠️ Scope the bound to the screen (`.ctl-page .ctl-histpanel .tbl-scroll`);
⛔ never touch a shared class like `.tbl-scroll`.

## ⚠️ AND ZOOM IN — SOME DEFECTS HAVE NO METRIC

🔬 `table-layout: fixed` gave four EQUAL ~55px columns, so every label wrapped to
three lines and the header collided into **"PARAMETERINTRADAY"**. ⛔ No geometry
check caught it; ⭐ it was found by **zooming into the render**. Use `auto` when a
label column and numeric columns share a table.

See also [[browser_qa_measurement_traps]] · [[feedback_gui_redesign_workflow]] ·
[[gui_review_needs_filled_data]] · [[feedback_status_label_rule_27jul]]
