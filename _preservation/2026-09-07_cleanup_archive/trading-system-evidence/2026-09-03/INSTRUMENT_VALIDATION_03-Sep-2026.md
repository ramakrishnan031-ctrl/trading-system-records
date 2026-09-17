# INSTRUMENT VALIDATION — GUI deployed-instance sweep
**03-Sep-2026 · PC · ⛔ BEFORE any production run · ⛔ the VM was not touched**

The instrument is `gui_sweep_snippet.js` — ⭐ see `SHA256SUMS.txt` for the hash of
the **shipped** revision. ⚠️ Revised after 👤 FILE 114 and **re-validated**; the
post-FILE-114 tests are in *"Round 2"* below.

## 🔴 NAMESPACE WARNING — ⛔ do not confuse these two
| label | what it is | numbers |
|---|---|---|
| **SYNTHETIC-S02** | a throwaway `index.html` on a local test server, used ONLY to validate this instrument | h=**1080** @1920×1080 · h=**916** @1440×900 |
| **DEPLOYED-S02** | the real Dashboard screen, the production precondition | h=**1212** · ovf=**no** · <13px=**0** (19-Aug record) |
⛔ **A later reader must never take 1080/916 as an expected production value.**
⭐ Every "S02" in the validation runs below is **SYNTHETIC-S02**.

⭐ **Why this file exists:** 👤 FILE 112 §4 — the instrument is recorded beside the
numbers. ⭐ And 👤 FILE 111/112: an instrument never given a wrong answer is ⛔ not
a validated one. ⭐ Two probes had already died on the auth layer before this.

## Environment of the validation run (⛔ NOT the production run)
| | |
|---|---|
| harness | `python -m http.server 8777 --bind 127.0.0.1`, synthetic same-origin pages |
| browser | Chrome **152.0.0.0** |
| host `devicePixelRatio` | **0.6667** |
| viewports exercised | **1920×1080** and **1440×900**, set on the iframe |
| invocation | `window.__GUI_SWEEP_CFG = {…}` (test hook, inert in production) then `eval(fetch('/gui_sweep_snippet.js'))` in the page console |

## What was proven

### 1. SELFTEST — every detector can fire, and can go quiet
🔬 On a crafted document: `sub13` **1**, `clipped` **1**, `ovf` **true**.
🔬 On a clean document: `sub13` **0**, `clipped` **0**, `ovf` **false**.
⇒ ⭐ `SELFTEST: PASS`. ⛔ The run aborts if this fails — a zero from an untested
detector is worthless → [[a_floor_is_not_a_non_vacuity_check]]

### 2. The S02 precondition gate fires in BOTH directions
| expectation given | result |
|---|---|
| `h=99999` (deliberately wrong) | `Δ h=-98919` · **VERDICT: 🔴 environment DEVIATES** · **HALTED at C1**, sweep not run |
| `h=1080` (observed truth) | **VERDICT: ✅ environment COMPARABLE** · full sweep proceeded |
⇒ 🔴 ⭐ **A gate that can only pass is not a gate.** ⭐ This one was made to fail
first.

### 3. The detectors fire on real page content, ⛔ not only in the self-test
```
S02  /index.html    1920x1080  h=1080 ovf=false (sw=1920/cw=1920) sub13=0 clipped=0 auth=true
S02  /index.html    1440x900   h=916  ovf=false (sw=1417/cw=1417) sub13=0 clipped=0 auth=true
SX1  /clipped.html  1920x1080  h=1080 ovf=false (sw=1920/cw=1920) sub13=1 clipped=1 auth=true
SX1  /clipped.html  1440x900   h=900  ovf=false (sw=1440/cw=1440) sub13=1 clipped=1 auth=true
SX2  /wide.html     1920x1080  h=1057 ovf=true  (sw=4000/cw=1920) sub13=0 clipped=0 auth=true
SX2  /wide.html     1440x900   h=877  ovf=true  (sw=4000/cw=1440) sub13=0 clipped=0 auth=true
SX3  /login.html    1920x1080  h=1080 ovf=false (sw=1920/cw=1920) sub13=0 clipped=0 auth=false ⛔LOGINPAGE
SX3  /login.html    1440x900   h=900  ovf=false (sw=1440/cw=1440) sub13=0 clipped=0 auth=false ⛔LOGINPAGE
INTEGRITY: ⛔ 2 row(s) suspect: SX3@1920, SX3@1440
```

### 4. 🔴 THE AUTH HOLE IS CLOSED
🔬 `/login.html` was detected as **`auth=false ⛔LOGINPAGE`** at both viewports
and flagged by `INTEGRITY`. ⇒ ⭐ **29 routes of login-page metrics can no longer
masquerade as a complete sweep** — ⭐ the exact hole 👤 FILE 112 §5 named, ⭐ and
the one that killed the `/static` md5 probe (302 body) and the route probe (401).

### 5. 🔴 THE DPR TRAP IS DEFEATED IN PRACTICE, ⛔ NOT IN THEORY
🔬 The host ran at `devicePixelRatio` **0.6667**, ⭐ yet **every** row reports
`cw=1920` / `cw=1440`. ⇒ ⭐ The iframe's CSS box is the measurement surface, ⭐ so
the host window's scaling cannot reach it. ⚠️ ⭐ The snippet **asserts**
`innerWidth === requested` and voids the number otherwise — ⛔ it does not assume
it → [[browser_qa_measurement_traps]]

### 6. Raw numbers are exposed, ⛔ not just booleans
⭐ `S02@1440` shows `sw=1417/cw=1417` — 🔬 a vertical scrollbar narrowing the
client box below 1440. ⭐ Correctly reported `ovf=false`. ⇒ ⭐ Had only the boolean
been printed, that 23px would have been invisible.

## ⚠️ Operational findings from the validation
- 🔬 Each route/viewport took ~**4.0 s**, ⛔ not the ~1.2 s the settle loop implies:
  ⭐ Chrome throttles `setTimeout` to ~1 s in a **non-focused** tab.
  ⇒ ⭐ **Keep the tab visible and focused** — throttling also suspends rendering,
  which would make measurements unreliable. ⭐ Budget ~3 min for 21×2.
- ⭐ Two bugs were found and fixed by this exercise, ⛔ before shipping:
  1. ⭐ `loadInto('about:blank')` — ⭐ the load event may never fire for a document
     the frame already has ⇒ ⭐ the run would have **hung** for 30 s and died.
  2. ⭐ `String(el.className)` on an SVG element yields
     `"[object SVGAnimatedString]"` ⇒ ⭐ garbage keys in the sub-13px breakdown.

---

# ROUND 2 — after 👤 FILE 114 (three holes closed, each re-validated)

## §1 The scrollbar confound — the C1 verdict is now TWO-PART and diagnosable
⭐ **The problem:** DEPLOYED-S02's recorded height **1212 > 1080 viewport** ⇒ there
**WILL** be a vertical scrollbar ⇒ `cw < 1920` ⇒ the narrower box **reflows** the
page ⇒ `h` is partly a function of the browser's **scrollbar width**.
🔴 ⭐ And the 19-Aug instrument **never recorded `cw`** ⇒ ⛔ a scrollbar-explained
deviation can be **hypothesised, ⛔ never proven**.

⭐ `cw` and `sbar` (= requested − cw) are now printed on **every** row, and C1
classifies rather than just failing:

| test | viewport | scrollbar | classification | halted? | diagnostic |
|---|---|---|---|---|---|
| **T3** | 1920×1080 | **0 px** | 🔴 `UNEXPLAINED` | HALTED | — |
| **T4** | 1440×900 | **23 px** | ⚠️ `SCROLLBAR-PLAUSIBLE` | HALTED | *"NOT RESOLVABLE against the historical record"* printed |

🔬 Both given the same wrong expectation (`h=99999`); 🔬 Δh −98919 and −99083.
⇒ ⭐ The classifier splits on **exactly the right variable** — the presence of a
scrollbar — ⛔ not on the size of the miss. ⭐ Both still halt: 👤 **Rama decides**.
⇒ ⭐ That converts an ambiguous halt into a **diagnosable** one.

## §2 Focus loss — now DETECTED, ⛔ not merely warned about
⭐ `document.hasFocus()` + `document.visibilityState` are sampled **before and
after every measurement**; a row that lost either is marked **`⛔UNFOCUSED`** and
listed by `INTEGRITY` — ⭐ the same shape that made `⛔LOGINPAGE` work.

| test | condition | result |
|---|---|---|
| **T5** | 🔬 genuinely backgrounded tab (`hasFocus=false`, `visibilityState=hidden`) | **3 rows `⛔UNFOCUSED`**, INTEGRITY listed them, S02 verdict still `COMPARABLE` (orthogonal, correct) |
| **T6** | focus/visibility stubbed true | **0 rows flagged**, INTEGRITY: *"tab stayed focused"* |

⇒ ⭐ Fires on a **real** unfocused tab (⛔ not a stub) and goes quiet when focused.
🔴 ⭐ **This retroactively explains the ~4.0 s/route in Round 1 — those runs were
themselves measured in an unfocused tab.** ⭐ Harmless on trivial static pages,
⭐ and precisely the risk on real ones. ⛔ *"Keep the tab focused"* is an
instruction to a human mid-run; ⭐ **this is the control.**

## §3 The run header spans two sources
⭐ `GUI_PID` / `GUI_START_TIME` are **VM-side**; ⭐ browser version, DPR, viewport,
`AUTHENTICATED` are **browser-side**. ⇒ ⭐ Bound into ONE file,
`RUN_HEADER_03-Sep-2026.md`, ⛔ never two.
⚠️ 🔴 ⭐ **The binding is manual and it is the weak link** — ⛔ nothing in the
snippet can verify which process served it. ⭐ The only protection is
**SEQUENCE**: confirm the new PID → **then** hand over the snippet.
⛔ Never the reverse: ⭐ a pre-restart run would look perfect and be void, ⭐ and
⛔ no later inspection could tell.

---

# ROUND 3 — after 👤 FILE 115

## §1 🔴 A BRANCH THAT COULD NEVER FIRE — γ, in my own gate
⭐ Round 2 classified on *"is a scrollbar present?"*. ⚠️ 🔴 **DEPLOYED-S02's
recorded `h=1212` EXCEEDS the 1080 viewport ⇒ a vertical scrollbar is CERTAIN ⇒
`sbar > 0` ALWAYS ⇒ every possible deviation would classify the same way.**
⇒ ⭐ `UNEXPLAINED` was **algebraically unreachable for the one screen the gate was
built for.** ⭐ T3 only reached it because the synthetic page **fit** its viewport
— ⚠️ a condition the real screen cannot reproduce.
⭐ Safety was never lost (both branches halted), ⛔ but the diagnostic was worth
less than it looked. ⭐ Same γ class this project has been hunting in the trading
code → [[a_floor_is_not_a_non_vacuity_check]]

⭐ **THE FIX — ⛔ no threshold, ⛔ no pass band.** ⭐ The scrollbar is no longer a
verdict. ⭐ The verdict splits on **what moved** (⭐ height only vs more than the
height — ⭐ reachable regardless of scrollbars), and the **magnitudes are printed
side by side** so the reader judges:
`MAGNITUDES:  Δh = 804px  ·  scrollbar = 23px  ·  ratio 35.0×`
⭐ plus the standing fact that a scrollbar is ~15–25px, ⭐ and an explicit line
saying a scrollbar being **present** proves nothing here.

| test | page @1920 | scrollbar | verdict | halted |
|---|---|---|---|---|
| **G1** | tall (fits width) | **23px** | ⚠️ `HEIGHT ONLY` · Δh 804 vs 23 · **35.0×** | HALTED |
| **G2** | tall **and** wide | **23px** | 🔴 `MORE THAN THE HEIGHT MOVED` | HALTED |

⇒ 🔴 ⭐ **G2 is the fix proven: the strong verdict now fires WITH a scrollbar
present** — ⭐ the exact condition DEPLOYED-S02 is permanently in. ⛔ The branch is
no longer unreachable.

## §2 ⛔ ROUND 1's NUMBERS ARE NOT LOAD-BEARING
⭐ Round 1's **conclusions** are binary (⭐ can a detector fire? ⭐ go quiet? ⭐ does
the gate halt?) ⇒ ⭐ throttling cannot change a yes/no ⇒ ⭐ they stand.
⚠️ ⭐ Round 1's **numbers** (`h=1080`, `h=916`, `sw=1417/cw=1417`) were taken with
rendering suspended. ⭐ Probably fine on trivial static pages; ⛔ **not proven
fine.**
⇒ 🔴 ⭐ **The 23px must NEVER become an assumed production scrollbar width** —
⭐ it was measured under precisely the condition the new focus control exists to
reject. ⭐ Every number the production run relies on comes from the production
run, focused, ⭐ and flagged if not.

## §3 SCOPE — a stop-early result is a COMPLETE result
⭐ `STOP_AFTER_C2` added. ⭐ C0–C2 (SELFTEST · AUTHENTICATED · DEPLOYED-S02 · S17)
fully answers *"is the deployed GUI serving the refitted build?"* in well under
a minute. ⭐ Everything after is **baseline-building**, ⛔ not verification.

| test | flag | marker printed | stop line | S17 measured | later route measured |
|---|---|---|---|---|---|
| **G3** | `true` | ✅ | ✅ | ✅ | ⛔ **no** — stopped |
| **G4** | `false` | ✅ | — | ✅ | ✅ — continued |

⭐ The full run **contains** the short answer, demarcated by
`══════ COMPLETE ANSWER REACHED (C2) ══════`, ⭐ so the answer is on screen early
even if the rest is abandoned.
⚠️ ⭐ If stopped early the record must read *"deployment verified at C2; Tiers 2
and 3 not measured"* — ⛔ **never** *"sweep complete."* ⭐ The script prints that
reminder itself.

## Bounds — ⛔ what this validation does NOT establish
⛔ It does **not** show the snippet measures the same way the **19-Aug**
instrument did. ⭐ That instrument is not in the repository and cannot be run
→ [[the_gui_delta_has_no_comparand_03sep]].
⇒ ⭐ Therefore Tier 1 is reported as **CORROBORATION (new instrument)** —
⭐ presence and order of magnitude — ⛔ never as a Δ.
⭐ The correct wording for the gap, 👤 FILE 113 §4: *"the historical campaign
validation is **not independently reproducible** from the repository today."*
⛔ **NOT** *"the campaign was invalid"*, ⛔ **NOT** *"the measurements were false."*
⭐ There is no evidence for either.
