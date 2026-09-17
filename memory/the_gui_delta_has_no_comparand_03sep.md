---
name: the_gui_delta_has_no_comparand_03sep
description: "The per-route two-resolution four-metric GUI baseline that a deployed-vs-local Delta would need does not exist -- the only capture index is 19-Aug and predates the 02-Sep refit, so a \"Delta = 0 everywhere\" claim has no comparand."
metadata: 
  node_type: memory
  type: project
  originSessionId: 06b31989-21eb-4564-93cc-440dab44786c
  modified: 2026-09-03T06:51:08.285Z
---

🔬 **MEASURED 03-Sep-2026 ~11:4x** against `origin/main` `2d08436`, ⛔ before any
step-C run (the PID gate was still closed).

## The ask
👤 FILE 111 §1: run the tunnel check as a **Δ against the same numbers the
local validation produced** — ⭐ same routes, ⭐ same two resolutions
(1920×1080, 1440×900), ⭐ same four metrics (page height · page overflow ·
clipped-cell count · sub-13px count). ⭐ *"Δ = 0 everywhere ⇒ the deployed build
renders as validated."* ⛔ Report Δ per route, ⛔ not *"looks correct."*

## 🔴 THE FINDING — that comparand does not exist
⭐ **What IS in the repo:**
- 📄 `docs/audit/approval_final_19aug/INDEX.md` — 🔬 the **ONLY** capture index
  on **any** branch (`git log --all --diff-filter=A`). **22 screens**, but
  ⛔ **1920 ONLY**, and only **3** metrics: `h` (page height) · `OVF` ·
  `<13px`. ⛔ **NO 1440 column. ⛔ NO clipped-cell column.**
  ⚠️ Authored **`be41d3c`, 19-Aug-2026**.
- 📄 `ops_dashboard/frontend/static/style.css:2017` — 🔬 *"MEASURED 02-Sep
  across all 29 routes"*, ⭐ but that is a **STATIC CSS column-alignment audit**
  (460 header/body pairs; 377 agreed, 83 did not), ⛔ **NOT** a rendered-page
  metric sweep. ⚠️ ⛔ Do not mistake it for one — the route count matches and
  the content does not.
- 📄 `UNPUSHED_LEDGER.md` — 🔬 only **10** lines carry an `@1920`/`@1440`
  measurement, ⭐ all in the last entries (≈32–35 ⇒ S17, S16, S06, S07).
- ⭐ **S14 carried forward explicitly: `+9 @1920, +67 @1440`.**

⭐ **Why the 19-Aug table cannot stand in as the baseline:** 🔬 the global table
rule landed **02-Sep** — `63a3946` and `0bbe127`, **14 days after** `be41d3c` —
and by its own comment it **moves 33 headings** across S02/S03/S07/S17.
⇒ ⭐ That is a **rendering** change post-dating the capture. ⛔ A non-zero Δ vs
19-Aug would therefore be **expected**, ⛔ not a finding.

## 🔴 WORDING, 👤 FILE 113 §4 — the distinction that matters
⭐ Correct: *"the historical campaign validation is **not independently
reproducible** from the repository today."*
⛔ **NOT** *"the campaign was invalid."* ⛔ **NOT** *"the measurements were false."*
⭐ There is ⛔ no evidence for either — ⭐ the difference between a process finding
and an unfounded accusation.

## How to apply
⛔ **Do NOT report a "Δ = 0 everywhere" pass** — there is no complete
*everywhere* to compare against. ⭐ A fresh full sweep would produce **first
measurements**, ⛔ which is precisely the *"fresh opinion"* FILE 111 forbids.
⭐ **Report in three tiers, labelled:**
1. ⭐ **TRUE Δ** (recorded, current, can go red): **S14 `+9`/`+67`** — ⭐ the
   designated negative control, ⭐ its PRESENCE is a PASS — plus the 4 screens
   with current `@1920`/`@1440` lines (S17, S16, S06, S07).
2. ⚠️ **Δ vs a STALE baseline**: the 19-Aug `h`/`OVF`/`<13px` at **1920 only**.
   ⛔ A drift here is ⛔ NOT presumptively a defect — ⭐ the refit changed heights.
3. ⭐ **FIRST MEASUREMENT** (⛔ no baseline exists): **all** clipped-cell counts,
   and **1440×900** for every screen but the four. ⛔ Never call these a Δ.

⭐ **The sweep is worth running anyway — ⭐ it BECOMES the missing baseline.**
⇒ ⭐ Commit it to the repo, ⭐ the same lesson as 👤 FILE 109 §1: ⛔ a procedure
(or a baseline) that lives only in chat transcripts and narrative prose is
⛔ not a procedure. ⭐ This is that finding one layer down — ⛔ not the push
*procedure* this time, ⭐ but the acceptance *numbers*.

## 🔬 THE §3 LOOKUP, DONE — which screens can drift for NON-environmental reasons
⭐ The freeze pane is a **PINNED INVENTORY** in `tests/test_global_table_rule.py`:
🔬 **15 wraps across 7 screens** — `execution`×3 · `live_activity`×3 ·
`config`×3 · `controls`×2 · `scanner_attribution`×2 · `strategy_ranking`×1 ·
`strategy_health`×1. 🔬 `tbl-freeze` count at **`be41d3c` = 0** for all seven
(the shared class is new; the old build froze per-screen).
⇒ ⭐ **HEIGHT DRIFT EXPECTED on 7:** S11 · S16 · S17 · S18 · S19 · S20 · S21.
⭐ Bounding a table body collapses page height — 📄 the ledger records exactly
that (*"2457px → page 2074px"*, *"page 1353 → 1199"*).
⇒ ⭐ **HEIGHT SHOULD HOLD on the other 15** — ⭐ that is the environmental set.

🔴 **THE CLEAN PROBE IS S02 DASHBOARD.** 🔬 `dashboard.html` is **UNCHANGED**
`be41d3c..2d08436` (every other screen's template churned: S08 885+/417-,
S12 211+/60-, S15 151+/103-, S03 149+/67-, S14 112+/25-, S09 97+/19-, down to
S04 17+/31-). ⭐ It gained no freeze wrap, and the only CSS rule reaching it is
**1 heading re-alignment** — ⛔ `text-align` cannot move `h`/`OVF`/`<13px`.
⇒ ⭐ **PREDICTION THAT CAN FAIL: S02 must render `h=1212 · OVF=no · <13px=0`.**
⭐ Any deviation there is **environmental** — ⛔ nothing else can explain it.

## 🔴 BLOCKER — the authenticated sweep is ⛔ NOT autonomous
🔬 `backend/auth.py`: username + password + **TOTP** (`pyotp`, `valid_window=1`),
🔬 **5 failures ⇒ 15-minute lockout**. 🔬 Real values live in the git-ignored VM
overlay `gui_config.local.yaml` (chmod 600) — ⛔ hash only, ⛔ never plaintext.
🔬 The `local_dev.auto_login` bypass is gated by **`OPS_DASHBOARD_LOCAL_DEV=1`**,
an env var that *"cannot travel"* — 🔬 and the VM unit's `Environment=` is
**empty**, by design. ⛔ Do NOT set it on the VM; it is a security control.
⇒ 🔴 ⭐ **Never attempt a login by guessing — 5 tries locks 👤 Rama out of his own
dashboard for 15 minutes, during market hours.**
⇒ ⭐ **Cleanest path: 👤 Rama authenticates once in a browser and hands over the
SESSION COOKIE** — ⭐ it sidesteps both the TOTP window and the lockout counter.
⭐ 👤 His credential decision, ⛔ not an assumption to make.

⚠️ **Measurement traps that apply to the run:** ⭐ use an **iframe** — the host
window is `dpr 0.75`, so a maximised "1920" is **2549 CSS px**
→ [[browser_qa_measurement_traps]]. ⭐ Mutation-test any detector that returns
**0** → [[a_floor_is_not_a_non_vacuity_check]]. ⭐ And it runs as step **C** —
⛔ only after the new PID → [[gui_after_deploy_is_mixed_not_old_03sep]].
