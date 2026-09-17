---
name: loss-governor-scope-08aug
description: "The two-pipeline split separated the loss COUNTERS but not the loss ACTION — a daily-loss breach still fires a system-wide SOFT_KILL, so an intraday loss stops delivery and vice versa. Measured 08-Aug, not fixed."
metadata: 
  node_type: memory
  type: project
  originSessionId: 35a1c3dd-75a3-42ce-bdc5-d5e981dad58a
  modified: 2026-08-08T11:36:31.455Z
---

# 🛑 THE PIPELINE LOSS GOVERNOR — measured 08-Aug, then **`<BUILT 08-Aug>`**

> ## ✅ **BUILT (branch `feat/delivery-config-split`, ⛔ NOT DEPLOYED). THE FIX: IT IS NO LONGER EXPRESSED AS A KILL.**
> ⭐⭐ **The `risk_engine`'s own `DAILY_LOSS` gate already blocks the breached book, so
> the governor needs NO NEW STATE:** it **survives a restart BY CONSTRUCTION**
> (recomputed from `fm_ledger`, the `FIX-051`/`FIX-183` shape) and **clears at the DAY
> boundary** (the query is date-scoped). ⛔ **It does NOT inherit `SOFT_KILL`'s
> BOOT-BOUND clearing** — losing that (a same-day restart hitting HALT/exit-4) is a
> simplification, not a regression.
> ⛔⛔ **`kill_switch` STAYS PRODUCT-BLIND** — 35 `is_active(` callers, and an
> emergency stop some book can ignore is not one. A test asserts `is_active` never
> learns the words product/pipeline/CNC/MIS.
> ⚖️ **ASYMMETRIC ON PURPOSE: intraday breach → `fire_now()` (already MIS/CO-only,
> ⛔ untouched) · DELIVERY breach → CLOSES NOTHING** (a holding survives `HARD_KILL`
> per Q4; force-closing would realise the very loss the limit caps). ⛔ **The old
> `soft_kill` fallback on a FAILED close is gone — a broker failure closing intraday
> can no longer take delivery down with it.**
> ✅ **The base disagreement is fixed in the same build: one limit, two enforcement
> points, ONE source, ⛔ no second loss calculation.**
> 🧪 **14 tests. RED-first: reverting only the behavioural half = 6F/8P, and the
> sharpest red is *"the governor never arms the kill switch"* FAILING on old code.**
> ✅ **GATE (D1 + governor together, `e0c83da`): `RC=1`, 9F/5634P/4S in 885 s — the
> failing set IS THE BASELINE NINE, LINE FOR LINE, zero new and zero missing.**
> ⭐ **Pass count reconciles with no remainder: `5616 + 4 + 14 = 5634`.**
> 🏷️ **REGRESSION ACCEPTED — zero NEW failures; 9 known baseline; RC=1 by convention.**
> ⚠️ **The FIRST post-§1 run was CONTAMINATED (I edited §2 while it ran) and was
> DISCARDED, ⛔ not reported as a result** — it showed 12F, 3 of them the C5 auditor
> tests since fixed. ⭐ **A gate run whose tree moved under it is not evidence.**

---

## 📜 THE MEASUREMENT THAT LED TO IT (08-Aug, before the build)

Record: `docs/audit/pipeline_loss_governor_scope_08aug2026.md`.

> **VERDICT: an INTRADAY loss breach STOPS DELIVERY, and a DELIVERY loss breach STOPS
> INTRADAY.** ⛔ **The split separated the COUNTERS and the pre-trade GATE; it did NOT
> separate the ACTION.** ⭐ **Two independent counters still lead to ONE shared stop —
> and the loss governor is the control most likely to actually fire.**

## 🔑 THE SEQUENCE IS **TWO ACTIONS WITH TWO DIFFERENT SCOPES** — only one is wrong

**(S)** `main.py:771-812`, fired from `fund_manager.release_used:1326-1341`:
- ② **`eod.fire_now()` — ✅ ALREADY INTRADAY-ONLY.** EOD6/FIX-015: *"DELIVERY (CNC)
  positions NOT touched"*; filter `EMERGENCY_FLATTEN_PRODUCTS = {"MIS","CO"}`.
- ③ **`kill_switch.soft_kill()` — 🔴 PRODUCT-BLIND.** `is_active(intent)` takes
  `intent ∈ {entry,exit,any}` — ⛔ **an ACTION KIND, NOT a product.** Blocks every new
  entry in BOTH books.
⇒ **an intraday loss does NOT close delivery positions (good) but DOES stop delivery
taking new entries (wrong).**
⛔⛔ **A blanket *"the action is global, scope it"* would ALSO have scoped the close —
which is already right, and scoping it would be a REGRESSION.**

## ✅ THE STREAK BREAKER IS ALREADY CORRECT

**(P)** width = every non-test ref to `max_consecutive_losses` across
`capital/ core/ main.py signals/ orders/`: its ONLY consumers are the `risk_engine` gate
and `pipeline_policy`. **No callback, no kill, no close.** ⛔ The only
"consecutive-…-kill" in the tree is `max_api_failures`, a different circuit breaker.

## 🔴 A DEFECT THE SPLIT INTRODUCED — the dual mechanism's two halves DISAGREE

⭐ **I rebased the PRE-TRADE gate onto the per-pipeline purse and did NOT touch the
POST-CLOSE breach** (`fund_manager` still reads the GLOBAL realised P&L against
`daily_loss_limit_pct × TOTAL`). 🏷️ The standing rule on this exact mechanism says
*"read the threshold from code AND its base — both move."* **One base moved.**
**As fractions of TOTAL: intraday gate 2.10% · delivery gate 0.90% · post-close breach
3.00%.** ⭐ **The ORDERING is the safe one — both gates trip BEFORE the breach, so
nothing is loosened** — ⛔ but the breach's SCOPE is global and its BASE now disagrees
with the gate it backstops.

## ⛔ THE SMALLEST FIX IS **NOT** A PRODUCT-AWARE KILL SWITCH

**(P) 35 non-test `is_active(` call sites.** Threading a product through them makes the
**GLOBAL EMERGENCY CONTROL** product-aware — ⛔ exactly what must not happen, on the
highest-consequence surface in the system. ⚠️ `HARD_KILL` already flattens only MIS/CO
(Q4) — **that is a decision about WHAT IT CLOSES, ⛔ not licence to narrow WHO IT STOPS.**
🔑 **Instead: STOP EXPRESSING THE GOVERNOR AS A KILL.** Give it a per-pipeline block flag
the `risk_engine` gate already reads ⇒ the kill switch stays the global emergency
control and the governor gets a scoped mechanism. **Call sites: `fund_manager.py:1326`
(bucket-scoped reader ⭐ ALREADY BUILT), `:1327` (⭐ `bucket` is already in local scope),
`:1341`, `main.py:771-812`.**
🏷️ **ITS OWN BUILD, ITS OWN CARD, ITS OWN TESTS — ⛔ not a rider on anything.**

## ⚠️ PARITY — a STRUCTURAL claim, ⛔ not an observation

Every site traced is **mode-blind shared code** ⇒ paper and live resolve identically.
⛔ **(P)** the VM DB holds 561 trades, **all `mode=LIVE`, ZERO paper rows** ⇒ **no paper
observation exists to check it against.** ⭐ **An absent instrument is not a passing
control** — this parity claim rests on the code being shared and on nothing else.

Related: [[two-pipeline-split-08aug]] · [[dual-daily-loss-mechanism]] ·
[[q4-hard-kill-delivery-30jul]] · [[kill-ladder-never-fired-28jul]]
