---
name: browser_qa_measurement_traps
description: "Two browser-QA measurements that silently lie — a maximised \"1920\" window is NOT a 1920 CSS viewport (dpr 0.75), and an overlap/clipping detector that returns 0 may be incapable of returning anything else. Read before claiming any @1920/@1440 result."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bec7a3ec-e183-4b2b-ba82-32af4e73fcb2
  modified: 2026-09-01T14:27:06.225Z
---

**🔬 Measured 01-Sep-2026 during the S22 Holdings visual QA. Both produced a GREEN that was
worth nothing, and both were caught only by deliberately trying to make them red.**

## 1. ⛔ A MAXIMISED 1920 WINDOW IS NOT A 1920 CSS VIEWPORT

🔬 This machine's Chrome reports **`devicePixelRatio = 0.75`** (75% zoom / display scaling).
⇒ a maximised window on a 1920 physical display gives **`window.innerWidth === 2549`**.

⚠️ So *"I verified at 1920×1080"* measured a **2549px viewport** — a third wider than the
requirement. Columns that truncate at 1920 rendered fine, and the first overflow/clipping pass
**did not count**.

⛔ **`resize_window` does NOT fix it** — a maximised window ignores the request and the tool
still reports *"Successfully resized"*. 🔬 `outerWidth` stayed 1920 across two attempts.

⭐ **THE FIX — measure inside a same-origin iframe of exact CSS dimensions.** Media queries
inside an iframe evaluate against the **iframe's own** viewport, so this is a true emulation:

```js
const f = document.createElement('iframe');
f.style.cssText = 'position:fixed;left:0;top:0;width:1920px;height:1080px;border:0;z-index:99999';
f.src = '/the-page'; document.body.appendChild(f);
await new Promise(r => f.onload = r); await new Promise(r => setTimeout(r, 3000));
const d = f.contentDocument, win = f.contentWindow;   // win.innerWidth === 1920, exactly
```

⭐ **ALWAYS print `window.innerWidth` from inside the frame and quote it in the report.**
⛔ Never quote the window size you asked for.

## 2. ⛔ A DETECTOR THAT RETURNS 0 MAY BE UNABLE TO RETURN ANYTHING ELSE

🔬 A panel-overlap check reported `0 overlaps` across 19 panels. ⚠️ Nudging a panel by **70, 150,
400 and even 900px still reported 0** — because the nudge moved it *up and out of the viewport*,
where it overlaps nothing. The detector was fine; **the calibration was meaningless.**

⭐ Only a **60px SIDEWAYS** nudge (into a neighbour, whose gap was 12px) produced a detected
`48×96` overlap. ⛔ Only then was the baseline zero worth reporting.

⭐ **RULE: before reporting any "0 problems found", mutate the page so the detector MUST fire,
and show it firing.** Applies equally to blank-cell audits, clipping scans and console checks —
🔬 an empty console is meaningless until a `console.error` canary proves capture works.

⚠️ Same session, same class: a clipping scan using `scrollWidth > clientWidth` can measure only
OVERFLOW; ⛔ `scrollWidth` never reports **less** than `clientWidth`, so it cannot detect *slack*
in a column. ⭐ Do not compute "spare space" from it.

## 3. ⚠️ LOAD CORRUPTS A LONG SUITE — SAY SO RATHER THAN GUESS A CAUSE

🔬 The same GUI regression ran **554s / 8074s / 553s** across three runs. The middle run — with 3
dashboards and Chrome iframes competing — produced **one extra failure that never reproduced**.
⭐ Kill the review servers before a full regression. ⛔ If an anomaly appears only in the slow run,
report *"did not reproduce, mechanism not proven"* rather than asserting a cause; 🔬 three
plausible hypotheses were each disproved by measurement.

See also [[feedback_gui_redesign_workflow]] · [[feedback_verify_rc_not_output]] · [[pc_test_env_hygiene]]
