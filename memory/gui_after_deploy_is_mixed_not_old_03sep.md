---
name: gui_after_deploy_is_mixed_not_old_03sep
description: "An un-restarted gui-dashboard after a deploy serves a MIXED old/new template set, not an old one -- Jinja caches at FIRST RENDER with auto_reload off, so which screens are stale depends on browsing history."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 06b31989-21eb-4564-93cc-440dab44786c
  modified: 2026-09-03T05:53:21.679Z
---

🔬 **MEASURED 03-Sep-2026 ~11:1x**, VM `gui-dashboard` PID **1019239** (started
02-Sep **06:19:53**), deploy checkout **02-Sep 23:39:55**, bare ref `2d08436`.

## 🔴 THE RULE (👤 Rama, FILE 110 §1)
⭐ **Under `auto_reload=False`, a rendered screen evidences the deployed tree
ONLY IF the process started AFTER the deploy.**
⇒ ⛔ *"I looked at the screen and it was correct"* has **never** been valid
acceptance evidence — ⛔ not before a restart, ⛔ not after one, ⭐ on its own.
⭐ A screen first rendered post-deploy shows the new build **whether or not the
restart happened**. ⭐ What makes a post-restart browse valid is that the cache
is **EMPTY** ⇒ every render is a first render off the deployed tree — ⭐ it is
⛔ **not** the looking.
⇒ ⭐ **ORDER, always: restart ⇒ confirm NEW PID + start time ⇒ THEN browse.**
⛔ A browse before the PID is confirmed proves nothing, ⭐ and looks **identical**
to the case where the restart silently failed.
⚠️ ⭐ The GUI's PID is the one that matters (**1019239** / Wed 06:19:53) —
⛔ NOT `trading-system`'s 1101999.

## The claim that was wrong
📄 The BOARD said the un-restarted unit *"⇒ ⛔ serving OLD templates"*.
🔬 **FALSE.** `curl http://127.0.0.1:8500/login` served the **NEW** build:
`.login-hero { … justify-content: flex-end }`, `margin-right: clamp(32px, 8vw,
160px)`, `.login-card-wrap { … flex-start; padding-left: clamp(32px,5vw,100px) }`
— ⭐ all three exist **only** at `2d08436`. ⭐ Positive control (`width: min(64%,
420px)`, present in BOTH builds) also matched, so the probe could have said
otherwise. ⚠️ One apparent old-shape hit was a **different element** (line 104,
`gap: 6px`) — ⛔ not `.login-hero`.

## Why — and why the truth is worse
🔬 Flask **3.1.3**; ⛔ no `TEMPLATES_AUTO_RELOAD`, ⛔ no debug flag, ⛔ empty unit
`Environment` ⇒ `auto_reload = app.debug = False`.
💭 Jinja caches a **compiled** template on **FIRST RENDER** and, with
`auto_reload` off, ⛔ never re-stats the file.
⇒ 🔴 **The GUI is a MIXED state, ⛔ not an old one.** A template first rendered
**before** the deploy is stale in memory; one first rendered **after** it is new.
`/login` is new precisely because an authenticated session ⛔ never renders it.
⇒ ⛔ **Which screens are stale is a function of the operator's browsing history
— ⛔ it is NOT knowable by looking at the screen.**

## The part that is unambiguously stale
🔬 **29 of 29** changed `ops_dashboard/backend/*.py` files have mtime
**02-Sep 23:39:55**, i.e. **after** the process started 02-Sep 06:19:53.
💭 CPython imports a module once per process ⇒ PID 1019239 runs **pre-deploy**
backend code for all 29 (`api/`, `readers/`, `services/`).

🔴 **Two of them are WHOLLY NEW FILES, ⛔ not edits** — 🔬 `cat-file -e` says
`services/controls.py` (19,482 B) and `readers/control_client.py` (3,928 B) are
**ABSENT at `39292d3`**, **EXIST at `2d08436`** (+496 lines, **0** deletions).
⇒ ⭐ The running process has **no such module at all** — ⛔ it is not stale, it
is **missing**. ⭐ That is the concrete backing for *"S17 first after restart"*.
⇒ 🔴 ⭐ **A new template fed by an old view is the real hazard: the page can
LOOK right and be WRONG** — missing a column the new view supplies, or reading
a key the old view never sets. ⭐ Templates can be mixed; ⛔ modules cannot.

## How to apply
⭐ After any `ops_dashboard` deploy, **restart `gui-dashboard`** — ⛔ never reason
that "the templates will pick themselves up". ⭐ State the reason precisely:
⛔ not *"it shows old screens"* but ⭐ *"it shows an unknowable mixture, and all
backend modules are pre-deploy."*
⛔ **Never call a screen `VERIFIED LIVE` from a pre-restart render** — it may be
new by accident and tell you nothing about its neighbours.

## ⚠️ Instrument failure caught in the same pass
🔬 A md5 comparison of served `/static/style.css` + `/static/components.js`
against both commits returned **the identical hash for two different files** —
because `/static/*` is **auth-gated** and both fetches returned the **302
redirect body** (`280c34c2ab9b438cdc708195624414bf`, 199 B, `loc=/login`).
⇒ ⭐ The check was **VACUOUS**: ⛔ it could not have distinguished new from old.
⭐ Discarded, ⛔ not reported as evidence. ⭐ Static-asset confirmation needs an
authenticated browser — 👤 Rama's, after the restart.

⚠️ **AND A SECOND ONE, caught BEFORE it was cited.** ⭐ Since `controls.py` is a
NEW file, a *route probe* looked like a credential-free backend-liveness test:
⭐ hit a `2d08436`-only route; ⭐ 404 ⇒ old backend, ⭐ reachable ⇒ new.
🔬 **Negative control killed it:** `/api/controls-summary` (BOTH builds),
`/api/analytics/slippage` (NEW only) and `/api/definitely-not-a-route-xyz`
(**NEITHER**) **all return `401`** — ⭐ the auth layer answers before routing
resolves, ⛔ so existence is unobservable. ⚠️ Non-API paths 302 to `/login`.
⇒ 🔴 ⭐ **THERE IS NO CREDENTIAL-FREE BACKEND-LIVENESS PROBE.** ⭐ The **PID +
start-time check IS the instrument**, ⭐ and it is sufficient — ⭐ the import
mechanism is deterministic: a process started after the deploy holds the
deployed modules. ⛔ Do not re-derive the route probe; it has been tested.
See [[a_floor_is_not_a_non_vacuity_check]] · [[feedback_verify_rc_not_output]] ·
[[gui_review_needs_filled_data]]
