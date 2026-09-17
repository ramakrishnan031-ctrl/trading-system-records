---
name: reconcile-positions-blind-t1-30jul
description: "30-Jul-2026: reconcile_positions reads kite.positions() ONLY and never holdings(), so a delivery holding is invisible to it from T+1 for its whole life -- a held delivery trade would emit a daily FALSE MISSING_AT_BROKER CRITICAL, and a 15:45 SUCCESS on a delivery day is a green check that cannot go red. Also: the 15:15/15:17 CNC force-close premise is REFUTED, but HARD_KILL does flatten CNC on the buy day and cannot from T+1."
metadata: 
  node_type: memory
  type: project
  originSessionId: 91948a89-4eda-4cd0-ac78-c3b773765042
  modified: 2026-07-30T06:22:39.179Z
---

# Reconciliation redesign — investigation 30-Jul-2026. Design doc, nothing built.
`docs/audit/reconciliation_redesign_design_30jul2026.txt` (for ChatGPT red-team).

## ⛔⛔ `reconcile_positions` IS POSITIONS-ONLY ⇒ BLIND TO DELIVERY FROM T+1
`scripts/reconcile_positions.py:158-168` reads `kite.positions()` `net` bucket,
non-zero qty. **It NEVER calls `holdings()`.** A CNC equity position is in
`positions()` on its BUY DAY ONLY; overnight it settles into `holdings()`.
**MEASURED 30-Jul 10:45 (read-only):** `positions()` day+net = 1 row (SYNGENE MIS
qty=0) ⇒ adapter-equivalent **0 positions**, while `holdings()` = all five T2
symbols qty 3 CNC. ⇒ empty ∪ empty ⇒ `all_symbols` empty ⇒ **exit 0 SUCCESS, 0
rows, no alert** (`:256-274`).
⛔ **A 15:45 SUCCESS IS NOT EVIDENCE THE BOOK IS FLAT.** Wednesday's exit 2 fired
only because Wednesday was the buy day — the one day it could see the position.
⛔ **I told Rama the opposite this morning in the Friday close card ("free second
witness"). Corrected in the card §A2(2)/(3).** [[feedback-verify-rc-not-output]]

## ⚠️⚠️ THE WORST GAP: a HELD delivery trade emits a DAILY FALSE `MISSING_AT_BROKER`
From T+1: broker side `{}` (invisible), system side `{SYM: qty}` (trade correctly
still OPEN) ⇒ `broker_qty==0 and system_qty!=0` ⇒ **`MISSING_AT_BROKER`** (`:267`)
⇒ `log.critical` + ERROR Telegram + exit 2, **every day the position is held.**
⭐ The asking card predicted a false ORPHAN; the real failure is the **mirror**, and
"MISSING_AT_BROKER" reads as *our stock is gone*. **Alert fatigue on the capital
path from day one of delivery.** ⇒ fix BEFORE/WITH the 4-Aug flip (small, no schema:
scope the job to intraday).

## ✅ 15:15 / 15:17 DO **NOT** FORCE-CLOSE CNC — THE REGISTER'S CLAIM IS REFUTED
Three sites: the 15:15 breaker is a **SOFT_KILL** (`kill_switch.py:115`,`:331`) and
`is_blocked(intent="exit")` is True only for HARD_KILL (`:476-484`) ⇒ it closes
nothing · the 15:17 squareoff excludes delivery by design (**EOD6**,
`eod_squareoff.py:23-24`,`:34`) enforced by `p.product in ("MIS","CO")`
(`:1064-1072`, FIX-015) · the FIX-182 residual flatten filters the same way
(`:1439`). ⇒ **NOT a 4-Aug flip blocker.** [[feedback-verify-the-finding-premise]]

## ⚠️ BUT HARD_KILL **DOES** FLATTEN CNC — and from T+1 it CANNOT
The flatten's trade SELECT has **no product filter**; `product` is fetched only to
exit under the same product (`kill_switch.py:1463-1479`,`:1510`). The FIX-181
LAYER A sweep (`:1567-1611`) flattens **any** non-zero `get_positions()` row and
maps CNC→DELIVERY intent on purpose (H-5, `:1582-1590`).
⇒ **BUY DAY: a HARD_KILL sells a delivery position.** ⇒ **T+1 ON: the sweep cannot
see it, so HARD_KILL's stated "must leave NO live broker position" invariant is
FALSE for delivery.**
⛔ **SUPERSEDED 30-Jul — Rama DECIDED Q4: delivery must SURVIVE a HARD_KILL.** So
the buy-day behaviour is now a **DEFECT** needing a product filter, and the T+1
blindness is now right **by accident** — which creates a hard ordering constraint.
**Read [[q4-hard-kill-delivery-30jul]] before touching either.**
⛔ **T2 survived Wednesday's 15:15 because NO HARD_KILL FIRED — not because of DB
isolation.** The shared-cash note's wording was imprecise. [[t2-shared-cash-seam-29jul]]

## ⭐⭐ ANTI-DUPLICATION: TWO PIECES ALREADY EXIST — DO NOT REBUILD
- **`eod_broker_reconcile.py` (cron 15:58)** — broker-authoritative, own creds,
  per-dimension + ONE overall **VERIFIED/ISSUES/UNVERIFIED** verdict, never a false
  VERIFIED, shadow-gated by `eod_reconcile.authoritative`. ⇒ **Rama's "one
  consolidated alert" is ALREADY BUILT as a framework.** ⛔ It has **no** holdings /
  CNC / delivery dimension — delivery-blind, not delivery-wrong.
- **`CncGttMonitor._gather()` (`orders/cnc_gtt_monitor.py:422-455`)** — merges
  `get_holdings()` (settled + t1) **PLUS** `get_positions()` filtered to
  `product=="CNC"` (`:447-454`). ⇒ **a correct symbol→held-qty read that SPANS the
  T/T+1 boundary already runs in production.** Y4: broker failure DEFERS, never
  reads no-data as no-positions. ⛔ **Do not write a third definition of "held".**
⇒ **The right shape is ONE new `delivery` dimension in the 15:58 job, fed by that
reader — NOT a second reconciler.**

## 🏷️ ARTEFACT vs GAP (the distinction that sized the scope)
**ARTEFACT** (vanishes when delivery writes to the LIVE DB): the 5
ORPHAN_AT_BROKER rows · the 5 boot Orphan-GTT WARNINGs (a real delivery trade has
an adoption candidate ⇒ adopted silently) · **CHECK2 HUMAN_ORDER + the Rs 5,000
tolerance — keys on "no local trade" (`order_reconciler.py:1815-1822`), so a real
delivery trade NEVER gets it ⇒ FIX-182 is OUT of the redesign's scope.**
**GENUINE:** the two above · nothing persists a closing inventory ⇒ no morning
comparison is possible at all · `eod_broker_reconcile` delivery-blind ·
daily-loss reads `fm_ledger.pnl_delta` ⇒ **blind to unrealized overnight
drawdown** (may be deliberate — open Q for Rama) · `delivery_symbols` orphan-sweep
exclusion (`order_reconciler.py:847`,`:904`) has **never executed**.
