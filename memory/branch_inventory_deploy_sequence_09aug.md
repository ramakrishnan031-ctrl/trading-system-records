---
name: branch-inventory-deploy-sequence-09aug
description: FIVE branches verified by diff (not recollection). The alert deployable ref is fix/alert-phase2-watcher, NOT fix/alert-remediation. Schema invariant holds. Deploy sequence 10-14 Aug written for Rama.
metadata:
  node_type: memory
  type: project
---

# 🗂️ BRANCH INVENTORY — VERIFIED BY DIFF, ⛔ NOT BY RECOLLECTION (09-Aug)

| branch | vs `main` | contents | schema | worktree | independent? |
|---|---|---|---|---|---|
| `fix/alert-remediation` | 2 | 🔴 **Phases 0 + 1 ONLY — ⛔ NOT Phase 2** | v45, 0 schema files | clean | yes |
| **`fix/alert-phase2-watcher`** | 3 | ⭐ **Phases 0+1+2 — THE DEPLOYABLE UNIT** | v45, 0 schema files | clean | **contains** `fix/alert-remediation` |
| `fix/tick2-pipeline-scoped-daily-gate` | 2 | Tick 2 + the carried countermeasure | v45; touches `state_store.py` but **(P) 0 DDL lines** ⇒ QUERY-ONLY | clean | yes |
| `fix/n907-forward-shadow-encoding` | 1 | N9-07 | v45 | clean | yes |
| `feat/delivery-config-split` | 19 | sizing + split + governor | 🔴 **v46 — THE ONLY ONE** | dirty *(funds-short + docs, deliberate)* | yes |

⭐ All five share `merge-base = main f963438`. ✅ **SCHEMA INVARIANT HOLDS: only the sizing branch carries v46; every other reads 45** ⇒ **Monday's gate line 9c premise is intact, and Tick 2's `state_store` edit is a QUERY change, ⛔ not a schema change.**

## 🔴 FINDING 1 — THE OBVIOUS BRANCH NAME IS THE WRONG REF TO PUSH
**`fix/alert-remediation` does NOT contain Phase 2.** Phase 2 sits on `fix/alert-phase2-watcher`, which is BASED ON it and therefore contains all three phases. ⛔ **Pushing `fix/alert-remediation` would install Phases 0+1 and SILENTLY OMIT Phase 2 — the availability fix that stops the watcher crashing.** ⭐ **The deployable ref is `fix/alert-phase2-watcher`.** ⚠️ The card's §1 assumed the three phases had landed on one branch named for the first of them; they did not, and the difference is what gets installed on the night.

## 🔴 FINDING 2 — THE ORDER DECIDES WHO REBASES (measured file overlap)
- `alert-phase2` ∩ `sizing` = **`main.py`**
- `tick2` ∩ `sizing` = **`core/state_store.py`, `signals/signal_processor.py`**
- `alert-phase2` ∩ `tick2` = **NONE** ⭐ fully independent of each other
- `n907` ∩ everything = **NONE** ⭐ rides any evening
⇒ **whichever of {alerts, tick2} deploys AFTER sizing must be re-fitted onto the new `main` and re-gated BEFORE its evening, ⛔ not on it.** ⚠️ **If sizing jumps to first — which Rama may well want — BOTH must be re-fitted.**

## ✅ THE ARCHITECTURE EXCEPTION, RECORDED AS ONE
**Phase 2 is based on `fix/alert-remediation`, ⛔ NOT on `main`, and the card that ordered "own branch off `main`" ALSO ordered "use Phase 0's contract, no second mechanism".** ⛔ **Those two cannot both hold: `alerts/delivery.py` exists only on the alert branch, so branching off `main` would have forced a SECOND COPY of the delivery contract — the exact thing the same card forbade.** ⭐ **Consequence, which is the part that matters: the three alert phases are ONE deployable unit, ⛔ not three.** That is correct — they share one contract and splitting them splits the contract — **but the deploy plan was drafted assuming three separate items, so it is written down here.**

## 🗓️ THE SEQUENCE — `Downloads/DEPLOY_SEQUENCE_10-14_AUG.txt`, a RECOMMENDATION
**MON 10 F6 alone · TUE 11 F6's first live day, install NOTHING · TUE 11 eve the ALERT unit** *(changes no trading decision ⇒ safest second, and it re-proves the deploy path)* **· WED 12 eve SIZING ALONE** *(v46; unblocks Tick 4)* **· THU 13 eve TICK 2** *(the only entry-behaviour change ⇒ its own quiet day)* **· FRI 14 eve N9-07** *(smallest, but on OPEN-1's un-regenerable instrument ⇒ last, where a surprise costs least)*.
⭐ **(P) weekdays computed, ⛔ not recalled; and `nse_holidays_2026.yaml` has ZERO August DATA entries — the only August string is a COMMENT, `15-Aug-2026 (Sat)`, which costs no trading day.**
🔴 **THE OPEN QUESTION PUT TO RAMA: should SIZING jump ahead of the alerts?** It is the piece he wants live. **Against:** F6's first live day would be followed immediately by a database change, so a wrong Wednesday morning would have two new causes instead of one — the alert unit sits between them precisely because it CANNOT be the cause of a trading problem.

⛔ **NOTHING built, merged, pushed or deployed by this pass.**

See also [[alert-phase2-n907-09aug]] · [[tick4-blocked-on-sizing-deploy-09aug]] · [[tick2-pipeline-scoped-gate-09aug]]
