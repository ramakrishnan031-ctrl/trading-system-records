---
name: feedback_gui_redesign_workflow
description: THE review-first workflow for every GUI redesign screen (S08+S09 approved 24-Aug; S07 owes a RE-approval, S06 a re-render sighting). Established across Screen-02/03; Rama reaffirmed it. Follow verbatim before touching any screen.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fdc2ec50-6d89-4677-aad8-58c61d58972c
  modified: 2026-08-24T08:51:23.074Z
---

**GUI redesign — the review-first workflow Rama LOCKED after Screen-02/03. Follow verbatim for
every remaining screen, in `gui/NN. Name.{png,txt}` order. ⭐ Current position is in `## Status`
at the foot of this file — ⛔ read it there, ⛔ never assume the next screen from this line.**

**Why:** Rama wants each screen pixel-close to its approved mockup on the FIRST review, minimal
correction rounds, and every screen looking like one app.

## The process (do this order, every screen)
1. **Read BOTH** `D:\Projects\trading-system\gui\<Screen>.png` AND `.txt` first. Don't code yet.
2. **Pixel-study the mockup**: layout, section order, alignment, spacing, card sizes, font
   sizes/weights, paddings, margins, colors, borders, icons, table column widths, responsiveness.
3. **Reuse the shared design language** (do NOT redesign components independently):
   - Root the page content in `class="dash-page <screen>-page"` so Screen-02's system applies:
     full-bleed left-aligned layout (`main.content:has(>.dash-page){width:100%;margin:0;…}`),
     `.kc` KPI cards (icon chip + colored top-rail + value + sub), `.mc-panel`/`.mc-head`/
     `.mc-title`, tint tokens (`--t-blue/green/red/orange/gray`, `--card`, `--card-bd`), `.info-banner`.
   - **Header = Screen-02 standard, ALWAYS**: LEFT Trader/Mode/Kill/Phase + Broker ID + Client Name;
     RIGHT Trading Date + Current Time + Log out. **NEVER** put Date/Time on the left even if the
     mockup does (Rama's global rule). Broker ID/Client Name come from `summary` (roster-resolved,
     [[gui_dashboard_screen02_deploy_10jul]]).
   - Tables: shared `data_table`/`tableMixin` (now FIXED — see components.js note below) OR a
     `.st-tbl`-style table matching Screen-03; sort arrows, status pills, `.uf-*` usage bars,
     integer ₹ for capital / 2-dp for P&L, `white-space:nowrap` + tight padding so it fits at 1600
     with NO horizontal scroll. Buttons: `.btn-primary`(blue)/`.btn-ghost`; prominent `.btn-export`.
   - Typography floor 13px; section titles 14-16px; critical values larger. Inter/Segoe/IBM Plex.
3b. 🔴 **SCANNER IS NOT A SEPARATE DIMENSION — DROP IT, KEEP STRATEGY (👤 Rama, 24-Aug-2026).**
   👤 His words: *"wherever Scanner & Strategy or Strategies labels/columns appears … remove
   'Scanner' and retain Strategy label/column only, Since scanner=strategy same data only … Not
   only for this screen for entire remaining screens too."*
   ⇒ ⛔ **Wherever a design file shows BOTH, delete the Scanner one:** columns · filters · ranking
   panels · attribution options · Best/Worst rows · export headers.
   ⚠️ **THE OLD DESIGN FILES STILL SHOW SCANNER** — `09. PnL_Analytics.{png,txt}` has a whole
   "SCANNER P&L RANKING" panel and a Scanner column. ⭐ **This ruling OVERRIDES the artwork on that
   one point**; everything else in the artwork still governs.
   ⭐ **Applies to EVERY REMAINING SCREEN**, ⛔ not just S09.
   ⛔ Do NOT invent a replacement dimension in the freed space — close the gap naturally.

4. **Backend limits → preserve the UI**: use existing data / honest placeholders (`—`); add ONLY
   additive read-only fields (precedent: `client_name`, `trade_type` from YAML `intent`). NO
   route/API/logic/DB changes. **Ask ONLY if a limit affects FUNCTIONALITY** (e.g. Screen-03 capital
   Allocated/Remaining — no per-strategy cap; asked, Rama decided). Otherwise proceed + flag in report.
5. **Before EVERY commit**: re-compare against PNG+TXT, pixel-review, FIX visual diffs first, THEN
   ask Rama to review. Don't ship approximations that trigger rounds.
6. **Consistency**: every screen must look like the same application.

## How to verify (PC test DB is EMPTY → mock it)
Scratchpad `serve_verify.py` (port 8599): `_bypass` before_request auths everything; add a
`/__demoN` route that `render_template("<screen>.html")` + injects a `window.fetch` override
returning canned mock JSON for the screen's `/api/*` (MUST be `{ok:true,status:200,json:…}` — base
`getJson`/`pageBase` check `r.ok`). Headless Edge screenshot (`--headless=new --hide-scrollbars
--window-size=W,H --screenshot`) at 1600 AND 1920; for exact px use `--dump-dom --virtual-time-budget`
+ a script that writes rects to `document.title`. Check console errors with `--enable-logging=stderr
--v=1 … 2>log; grep -i "Alpine Expression Error|SyntaxError|is not defined"`.

## Deploy (off-market, established)
`git add/commit` (Co-Authored-By trailer) → `git push origin main` (bare repo post-receive checks out
to VM working tree) → `ssh trading-vm "sudo systemctl restart gui-dashboard"` → verify `is-active` +
`NRestarts=0` + `GET /<page> -> 302`. Update the UNPUSHED ledger + MEMORY.md each time. Full suite:
`ops_dashboard/.venv/Scripts/python.exe -m pytest tests/ -q` → expect **ALL GREEN** — **2,080 passed**
as of 24-Aug (the old "354" was stale by ~1,700). ⛔ Treat any failure as yours until proven
otherwise: the suite pins approved per-screen contracts, not just wiring. Use the GUI `.venv`
(system python shows 1 false "kiteconnect" isolation failure).

## Gotchas already solved (don't rediscover)
- **components.js was broken** (comment `*/` typo) → tableMixin/filterMixin undefined → ALL
  data_table screens blank. FIXED in `ab14650`. If a table screen renders blank, check components.js
  parses first. [[gui_screen03_strategies_and_componentsjs_fix_10jul]]
- **no-store cache headers now on** (`065d32e`) → deploys are instant; if Rama says "still showing
  old", it's his pre-fix browser cache → one hard-refresh (Ctrl+Shift+R).
- PC `gui_config.local.yaml` points `config_dir`/DBs at the VM path → roster/DB unreadable on PC
  (header shows `--` locally; real values only on VM). Verify data-bound things on the VM.
- Jinja caches compiled templates per-process → the demo server needs a RESTART to pick up
  template edits (CSS/static are served fresh from disk).

## Status — 🔄 CURRENT AS OF 01-Sep-2026

🟢 **01-Sep-2026: S22 (`4b08372`) and S17 (`c8e1238`) APPROVED ⇒ 19 of 22 GREEN, ⛔ NOT PUSHED.** ⏸ **S16 Configuration is the ONLY screen left.** 🔴 S17 taught the rule in [[visual_acceptance_is_a_separate_gate]]: 👤 Rama REJECTED a render that had 0 overlaps and a green suite. 🔴 Its control plane is ⛔ DESIGNED-BUT-NEVER-BUILT — ⛔ do not 'fix' a control by creating a write path. ⏸ S06 owes a re-render sighting, S07 a RE-approval. ⏸ The **global table rule** (freeze header / body-only scroll / draggable headings) is 👤 DEFERRED until all 22 are built. ⏸ **S22 open decision: the Symbol column stays 78px and truncates 10-char symbols at a TRUE 1920.**

⭐ **THE AUTHORITY IS `docs/audit/VISUAL_APPROVAL_LEDGER_19-Aug-2026.md`** (on the GUI branch),
⛔ not this block. This is a pointer, kept current so nobody resumes on the wrong screen.

🔴 **THE LIVE GUI BRANCH IS `feat/screen10-slippage-analytics`** — it carries **S01–S07** work from
19–21 Aug. ⛔ **CHECK CONTENT, NEVER THE NAME:** `feat/screen04-signals`, `feat/screen05-orders`,
`feat/screen06-positions` and `feat/screen09-pnl-analytics` are **STALE TIPS from 12–15 Aug** and
are ⛔ **NOT** the active branch. Worktree: `D:\Projects\trading-system-gui09`.

- **S01–S05** ✅ **VISUALLY APPROVED** (19–20 Aug). ⚠️ `Q1`·`Q2` (S04) and `Q3`·`Q4` (S05) were
  approved **WITH**, ⛔ not resolved by, those approvals — ⛔ do not reopen or reinterpret them
  unless Rama asks.
- **S06 Positions** — correction committed (`5142dfd`, `b47e148`) + approval record committed
  (`3742f91`). 🔬 Corrected re-render captured 24-Aug at both viewports and **MEASURED GOOD**
  (5 separators on group row / sub-heading row / each of 7 data rows; `var(--card-bd)`; overflow-x
  0; 0 clipped). 🔴 **⛔ STILL NOT VISUALLY CONFIRMED — Rama's "Screen approved" was given on the
  PRE-correction render.** ⛔ A measurement is not a sign-off.
- **S08 Capital & Risk** ✅ **REBUILT + APPROVED 24-Aug** — `c479b40` (rebuild) + `a5545d0`
  (approval record). 👤 Rama took it OFF HOLD with an explicit ruling: **clean full reproduction,
  ⛔ NOT a patch.** The stale uncommitted 21-Aug pass was superseded by the rebuild.
  🔴 **⚠️ TWO post-approval changes he has ⛔ NOT seen re-rendered:** gauge geometry (→ the tested
  `cap-gauge` contract) and the gated **Export Limits** button. Both forced by TEST contracts.
- **S09 P&L Analytics** ✅ **APPROVED 24-Aug** — `7dba039` (corrections) + `725ede9` (approval).
  ⚖️ Judged **CORRECT, ⛔ not rebuild** — the skeleton already was the approved composition.
  ⭐ Added Recent Risk Events + the bottom export bar; both were required and missing.
- **S07 Trade Explorer** — ⏳ **RE-APPROVAL OWED.** 🔴 ⛔ **Do NOT call it "never approved":**
  👤 Rama approved it **14-Aug** (`cd9043c`, real VM data). His own **19-Aug 13px-floor** decision
  says it *"RE-OPENS EVERY EXISTING SCREEN APPROVAL"* for all 22, and `66fc82e` (21-Aug) landed
  after the sign-off. ⏳ S06's corrected re-render still awaits Rama's sight.

### 🔴 THREE OPEN QUESTIONS RAISED AT S09 — 👤 RAMA'S CALL
1. **Screen 21 "Scanner Attribution" is an entire screen premised on scanner as a dimension.**
   ⚠️ If scanner ≡ strategy (his 24-Aug ruling), is S21 redundant or does it become something else?
   ⭐ Raised at S09 deliberately, ⛔ rather than discovered at S21.
2. S09's rail carries a **"Trade Type & Direction"** panel that is ⛔ **not in the artwork** — it
   appears to be what filled the space when Scanner was first removed. Keep or drop?
3. The **equity-curve Day/Week/Month/Custom toggle** was ⛔ **withheld**: the page-level period pills
   already own the range, and a second control could disagree with the first.

### 🔴 A REGRESSION SHAPE WORTH REMEMBERING (S09, 24-Aug)
⚠️ **A density fix can BREAK the artwork it was meant to serve.** Closing a dead band with
`height:100%` on the heat cells turned the approved **compact near-square** day/time cards into tall
rectangles — 👤 Rama caught it. ⇒ ⭐ **When a panel's content is SHORTER than its row, ask whether the
artwork wants the CONTENT to grow or the ROW to shrink.** ⛔ Growing the content is the wrong answer
whenever the artwork draws a fixed, compact card. ⭐ Exclusions of this kind must carry a comment
saying why, or the next density pass silently re-applies them.

### ⭐⭐ THE LESSON S08 PAID FOR — RUN THE SUITE BEFORE CLAIMING A SCREEN IS DONE
🔴 A from-scratch rebuild raised **11 failures**: the repo already guarded the exact
Alpine-template-inside-SVG bug I had just hit, and the closure tests pin an **approved gauge/bar
contract** (ONE classifier · ⛔ **no arc when utilisation is unknown** · arc constant must match the
path · ticks clear 13px **after** SVG user-unit scaling · bars relative to the LARGEST consumer
while the % column keeps the TRUE total · the **gated export macro** screens 04/08/09 must render).
⇒ ⭐ **A "clean rebuild" silently discards contracts the tests hold. Re-run
`ops_dashboard/.venv/Scripts/python.exe -m pytest tests/ -q` (expect ALL green, ~2080) BEFORE the
correction commit — ⛔ never after.**

### 🔴 `pageBase.money()` RENDERS A MISSING VALUE AS `₹0.00`
🔬 `Number(v || 0)` ⇒ an ABSENT value is indistinguishable from a real zero. On a capital screen
that is a **fabricated fact**. ⛔ Overridden in **S08 only**; ⛔ **not** changed in `base.html` —
that reaches all 22 screens. 🏷️ **OPEN for 👤 Rama.** ⚠️ Every remaining screen inherits the defect.

See [[gui_dashboard_screen02_deploy_10jul]] and [[gui_screen03_strategies_and_componentsjs_fix_10jul]].


### 🔴⭐ 01-Sep (S15) — ALPINE RENDERS ONLY THE **FIRST ROOT** OF AN `x-if`, AND THE REST VANISH SILENTLY
🔬 Alpine 3.14.1 builds an `x-if` branch with `content.cloneNode(true).firstElementChild`. ⛔ A
`<template x-if>` holding **two sibling elements** therefore renders **only the first**; the second is
**never created** — ⛔ no error, ⛔ no console warning, ⛔ no failing test. On S15 the discarded span was
the `NOT INSTRUMENTED` one, and the survivor carried `x-show="r.status"` ⇒ hidden **exactly when the
value was missing** ⇒ 🔬 **20 of 20 cells rendered BLANK** while the markup read correctly to a
reviewer. ⭐ **PUT BOTH BRANCHES ON ONE ELEMENT** (the S13 ternary shape:
`:class="v ? 'pill' : 'slg-ni'" x-text="v || 'NOT INSTRUMENTED'"`).
⭐⭐ **THE GENERALISABLE PART: a defect can live in the RENDER while the SOURCE looks right.** ⛔ Reading
the template is not verification — ⭐ count the rendered cells in the browser. And ⭐ **sweep the CLASS,
⛔ not the instance**: one regex over all 33 templates found exactly two occurrences, both on S15, which
is what proved no other screen was affected. Pinned by
`test_no_x_if_branch_has_two_root_elements`.

### ⚙️⚠️ THE REVIEW HARNESS CACHES TEMPLATES — CSS HOT-RELOADS, JINJA DOES **NOT**
🔬 `backend.app` runs without debug, so **Jinja caches `*.html` at first render**. ⛔ Editing a template
and reloading the page shows the OLD markup, while `style.css` (a static file) picks up instantly.
⚠️ **THIS CONTAMINATES AN A/B MEASUREMENT** — on S15 a `git checkout` of both files gave a nonsense
hybrid (my cached template + reverted CSS) that matched neither build. ⭐ **To compare two builds, run
TWO SERVERS on different ports from separate worktrees** (`bind_port` is overridable in the
git-ignored `gui_config.local.yaml`), ⛔ never revert-in-place. ⭐ A screen can be rendered on real VM
evidence by pointing that same file's `paths.main_db` / `logs_dir` at a READ-ONLY extract — ⛔ the
428 MB live DB is never copied; dump only the tables the screen reads.
