---
name: feedback-absence-needs-wide-check
description: "AN ABSENCE IS ONLY ESTABLISHED BY A CHECK WIDE ENOUGH TO HAVE FOUND THE THING. State the search width BEFORE reporting 'there is no X'. Three instances in one day, 28-Jul-2026."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c4bb72b3-0d74-4f27-bc40-b99f67899e79
  modified: 2026-07-28T09:38:59.805Z
---

# 🔍🚫 AN ABSENCE IS ONLY ESTABLISHED BY A CHECK WIDE ENOUGH TO HAVE FOUND THE THING

**Before reporting "there is no X", state the SEARCH WIDTH** — what was searched, over what range,
how many rows / lines / refs / files that covered — **and ask whether the check could have found X
at all.** A zero from a narrow search is not evidence of absence; it is evidence of a narrow search.

## The FOUR instances, one day (28-Jul-2026). Each was MY confident report, and each was wrong.

1. **`git reflog show main` was empty → "the bare repo has NO reflog at all, nothing records
   deployment."** The record was on **HEAD**: `~/trading-system.git/logs/HEAD`, **801 entries back
   to 3-May**. Bare repos create no *per-ref* log, so the one ref I checked was the one guaranteed
   to be empty. [[deploy-record-exists-28jul]]
2. **`.gitignore:45` was `__pycache__/` → "there is no bare `*.pyc` rule, so a Type B shows in
   `git status`."** **Line 46** is `*.py[cod]`. I read one line and reported the absence of a rule I
   had not looked one line further to find. The instruction built on it (C6) had to be retired as VOID.
3. **grep `"capital drift detected"` returned 0 → "no drift events."** The JSON key is **`msg`**,
   not `message`, and the real events carried a different message entirely — **two HARD-tier events
   at ₹10,000 were sitting there.** [[kill-ladder-never-fired-28jul]]

4. **A RED test → "a production defect on the hard-kill path."** Mid-repair of FIX-061 my own
   fixture returned an SL row, which sends execution down `order_placer.py:3524`'s *"an SL already
   exists, place the TGT only"* branch and **returns** before `place_deferred_exits`. Three tests
   failed on `hard_kill not called` — and I was one step from reporting a **production defect on
   the kill path that was entirely my own doing.** Tracing the branch, instead of believing the
   assertion, is what caught it. ⭐ **A RED test is evidence of *something*, not evidence of *the
   thing you expected*** — the same shape as 1–3: a conclusion drawn from a check too narrow to
   distinguish two causes. [[pc-test-env-hygiene]]

⭐ **The tell in #3 is worth memorising: two of my own greps disagreed** — `"capital drift detected"`
= 0 while `"tier":"HARD"` = 2. **When two searches over the same corpus disagree, the narrow one is
lying, and that contradiction is the cheapest possible signal.** Look for it deliberately.

**Why:** all four were caught only because I re-derived from measurement instead of re-reading my
own earlier note. **Proving the width AFTER the fact still worked — but proving it FIRST is
cheaper**, and in two of the four the wrong claim had already been carried into a live instruction
before anyone re-checked. A false absence is worse than a false presence: it closes an
investigation, and it manufactures invariants that do not exist.

**How to apply:**
- Report absences in the shape *"searched N files / M lines / range R for <pattern>; zero hits"*,
  never a bare "there is none". The width belongs in the SAME sentence as the zero.
- Before believing a zero, ask **"could this check have found it?"** — try a second, differently-
  shaped query (a neighbouring key, a broader glob, a different ref, one line either side). If the
  two disagree, the narrow one is wrong.
- Prefer searching for the **container** (`logger`, table, directory) over the **exact string** you
  expect — you control the container name, you are guessing the string.
- ⛔ Never let an absence become an *instruction* ("preserve this gap", "nothing records X, so build
  one") without a width statement attached. That is how #1 and #2 both escaped into live documents.

Sibling rules: [[feedback-verify-the-finding-premise]] (a finding is a hypothesis — verify its
premise) and [[feedback-verify-rc-not-output]] (a green check is evidence only if it could have been
red). ⭐ This one is their mirror image: **a zero is evidence only if it could have been non-zero.**
