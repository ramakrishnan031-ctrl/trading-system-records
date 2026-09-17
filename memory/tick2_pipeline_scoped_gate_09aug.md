---
name: tick2-pipeline-scoped-gate-09aug
description: TICK 2 built and committed on fix/tick2-pipeline-scoped-daily-gate (0337378). No schema change needed - pipeline derives from orders.product via leg=ENTRY, fail-closed. Ruling 2 / gate 3 unchanged.
metadata:
  node_type: memory
  type: project
---

# 🚪 TICK 2 — `<BUILT · TESTED · COMMITTED `0337378` · NOT PUSHED · NOT DEPLOYED>`

**Branch `fix/tick2-pipeline-scoped-daily-gate` off `main` (`f963438`), third worktree `D:\Projects\trading-system-tick2`.** ⭐ **Its own branch on purpose: the two files DIFFER between `main` and the sizing branch — but the TWO FUNCTIONS changed are BYTE-IDENTICAL on both refs, so it transplants either way.**

## 🔑 IT IS NOT NEW POLICY — it completes Ruling 2's own second clause
📜 **Ruling 2 (Rama, 07-Aug):** *"ONE simultaneous OPEN position per symbol, account-wide — **and the symbol becomes eligible again the INSTANT it is flat**."* ⛔ **The second half had never been true**: gate 1 is product-blind and DAY-scoped, so a CLOSED delivery trade kept blocking intraday on that symbol+direction all day. ⭐ **The authority dates from 07-Aug; this is implementation, not a new decision.**

| rule | scope | after |
|---|---|---|
| **Ruling 2 / gate 3** — one simultaneous OPEN position per symbol | ACCOUNT-WIDE | ⛔ **UNCHANGED** — a delivery holding still blocks intraday **while open** |
| **Gate 1** — one completed trade per symbol+direction per day | was account-wide | ⭐ **PER-PIPELINE**; neither book blocks the other |

## 🔑 §2 ANSWERED BEFORE ANY CODE: **NO SCHEMA CHANGE**
**(P)** `trades` has **no** product/pipeline/intent column on `main` **or** on the sizing branch — **v46's eight new columns are ALL sizing-audit** *(`qty_by_allocation`, `planning_basis_rs`, …)*. ⭐ **The pipeline derives from `orders.product` (`TEXT NOT NULL`, MIS/CNC/CO) via `LEFT JOIN … AND o.leg='ENTRY'` — the join FIVE other `state_store` queries already use.** ⇒ **hours, not days; ⛔ not the sizing build's "own evening, alone" class.**

## ⛔⛔ FAIL-CLOSED IS THE WHOLE SAFETY ARGUMENT
A trade whose product cannot be resolved (no ENTRY row) counts for **BOTH** pipelines ⇒ **byte-identical to today** ⇒ ⭐ **the change is a strict RELAXATION only where the product is KNOWN, and there is no blind morning.** ⛔ A join letting NULL fall out of both buckets would make a protective gate **fail OPEN**. **An unresolvable INTENT likewise → `pipeline=None` → account-wide → the older, stricter behaviour. Fail-closed at both ends.**
⭐ **Delivery is the CLOSED set `{CNC}`; intraday is its COMPLEMENT (`<> 'CNC'`), ⛔ not an `IN ('MIS','CO')` allow-list** — a product code added later would escape an allow-list and be blocked by nothing.
⚠️ **`COUNT(DISTINCT t.trade_id)`** — SCALE mode writes several ENTRY legs per trade and `COUNT(*)` would multiply one trade into three.
🏷️ **`HISTORICAL PIPELINE RESOLVABILITY = UNMEASURED` — ⛔ NOT "proven", and ⛔ it must be CHECKED BEFORE THIS EVER DEPLOYS:** the local DB snapshot (03-Aug) holds **zero** trades, and measuring the VM's DB was not done. ⭐ **The fail-closed design makes it non-blocking** — an unresolved row can never cause a wrong ALLOW.

## 🔴 I SHIPPED THE SAME DEFECT TWICE IN ONE DAY, AND THE OLD TESTS CAUGHT IT BOTH TIMES
I resolved the pipeline via **`self._pipeline_for_intent(...)`** — an INSTANCE lookup — inside a **live entry path**. The existing gate tests call it on a minimal stub, so it raised `AttributeError`: **18 failures in `test_one_trade_per_symbol_direction.py`.** ⭐⭐ **The identical shape to Phase 0's alert-formatter defect a few hours earlier, and my own new tests were blind to it AGAIN because they use a real object.** ✅ **Fixed at the cause (class-qualified), ⛔ never by editing those tests, and a regression guard now pins it.** ⚠️ **And my "adjacent suites" choice was wrong — I ran `test_signal_processor`/`test_state_store`/`test_risk_engine` and omitted the gate's OWN dedicated file.** 📌 **RULE: the adjacent set must include the test file NAMED AFTER THE THING BEING CHANGED.**

## 📏 THE GATE — ⛔ never the word "clean"
**`NO NEW FAILURES — 8 known failures remain; 1 prior baseline failure (`test_instance_lock::test_p2_restart_after_crash_is_not_blocked`) did not reproduce; raw `PYTEST_RC=1` retained.`** ⛔ **"set-identical" would have been the WRONG WORD.** ⭐⭐ **CONFIRMED FLAPPING: the NEXT run on this branch (`43f73b1`) came back 9F/5,599P with that test FAILING again.** ⚠️ **1 baseline failure did NOT reproduce** — `test_instance_lock::test_p2_restart_after_crash_is_not_blocked`, the **documented pre-existing full-suite ORDERING artifact** (unreaped `Popen` orphan). ⭐ **RECORDED, ⛔ NOT CHASED (`G3`)** — and unrelated to an entry gate. ⭐⭐ **The arithmetic corroborates it EXACTLY: `5,582` (main baseline, derived as `5,596 − 14` from the Phase-0 run on the same base) `+ 16` new tests `+ 1` flipped artifact `= 5,599`, and `9 − 1 = 8`.** 🕛 14:54 IST — ⛔ no midnight crossing.

## ✅ PARITY — and this one is the good case
⭐ **PAPER CAN EXERCISE IT: a DB-PREDICATE gate, ⛔ not a broker path.** Both modes tested, resolving identically. ⛔ **Nothing here is a simulation** — unlike Phases 0/1, and the distinction is deliberate.

See also [[rulings-1-2-taken-07aug]] · [[entry-throttle-measures-entry-to-entry-07aug]] · [[alert-remediation-branch-phase1-09aug]]
