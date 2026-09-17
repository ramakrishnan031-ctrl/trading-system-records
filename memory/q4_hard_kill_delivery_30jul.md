---
name: q4-hard-kill-delivery-30jul
description: "Q4 DECIDED by Rama 30-Jul-2026: HARD_KILL flattens ONLY MIS/CO; delivery (CNC) SURVIVES it, protected by its GTT. The invariant narrows to 'leaves no live INTRADAY position'. The buy-day flatten is now a DEFECT needing a product filter; the T+1 blindness is now right BY ACCIDENT, which creates a hard ordering constraint. HARD_KILL has NEVER fired in production."
metadata: 
  node_type: memory
  type: project
  originSessionId: 91948a89-4eda-4cd0-ac78-c3b773765042
  modified: 2026-07-30T06:22:03.351Z
---

# Q4 — HARD_KILL vs DELIVERY. DECIDED 30-Jul. Registered + sized, NOTHING built.
`docs/audit/q4_hard_kill_delivery_decision_30jul2026.txt`

## ✅ THE DECISION (Rama, 30-Jul — REVISES the earlier reading)
**HARD_KILL flattens ONLY MIS/intraday. Delivery (CNC) SURVIVES a HARD_KILL** —
protected by its GTT, designed to be held across sessions. Force-closing delivery
becomes a **separate explicit action** (DELIVERY_HARD_KILL / FORCE_EXIT_ALL).
⭐ **The invariant NARROWS to "leaves no live INTRADAY position."** The documented
one — *"A HARD_KILL must leave NO live broker position"* (`kill_switch.py:1567-71`)
— is wrong **twice at once**: it claims more than intended, AND it is already false
for delivery from T+1. **Fix both in the same edit.**

## ⛔⛔ THE ORDERING CONSTRAINT — THE MOST IMPORTANT LINE HERE
**The T+1 blindness is now the DESIRED behaviour, but BY ACCIDENT: the kill does
not CHOOSE to spare delivery, it CANNOT SEE it** (`get_positions()`; MEASURED
30-Jul: 0 positions vs 5 holdings). ⛔ **DO NOT close it as "already correct."**
⇒ **Reconciliation step 1 · FORCE_EXIT_ALL · the GTT-coverage check ALL make a live
component holdings-aware. The moment ANY of them lands, the accident is gone and
the buy-day product filter is the ONLY thing preventing delivery liquidation.**
🔑 **THE FILTER MUST LAND FIRST.** [[reconcile-positions-blind-t1-30jul]]

## ⚠️ BUY DAY IS NOW A DEFECT (it was correct under the old reading)
Two sites flatten CNC on its buy day: the local-trade SELECT has **no product
filter** (`kill_switch.py:1472-79`, `:1510`), and the FIX-181 sweep filters only on
symbol/qty/handled and **maps CNC→DELIVERY on purpose** (H-5, `:1582-90`) — it is
BUILT to succeed at selling CNC. ⇒ needs a restriction to `("MIS","CO")`.
⭐ **Precedent already in-tree — derive, don't invent:** `eod_squareoff.py` does
exactly this at BOTH its sites (`:1072` FIX-015, `:1439`), per **EOD6** (`:23-24`).
⭐ **Restrict, don't extend:** making an emergency path do LESS cannot add a failure
mode; teaching it to read a new data source can.

## 🎯 BLOCKER ANSWER — the flip and the carry pilot must be SEPARATED
**MEASURED: HARD_KILL has NEVER fired in production** — zero "HARD_KILL ACTIVATED"
in all of `logs/`; `kill_switch_state` holds only INACTIVE + the routine 15:15
SOFT_KILL auto-cleared 08:15. **6 trigger sites / 5 modules:** `main.py:719` ·
`drift_handler.py:231` (HARD tier, ONE sample) · `fund_manager.py:982`,`:2329`
(BL9 / bucket overflow) · `order_placer.py:1534`,`:3792`.
- **The four-flag FLIP: NON-BLOCKER** — no delivery position on the book, nothing
  new to destroy.
- **The CARRY PILOT (same 4-Aug day): BLOCKED** — it deliberately opens a real CNC
  position that sits in `positions()` all buy day ⇒ reachable by both sites.
- ⚠️ **4-Aug is the worst day for the most reachable trigger:**
  `conditional_allocation_enabled` goes TRUE for the first time, and the
  FundManager invariant/bucket sites are the class new capital arithmetic perturbs.
  **[INFERENCE — the BL9 trace is NOT done; it is the only unmeasured link (Q9).]**
- **Cost is the SEQUENCE, not the money** (~Rs 650): the pilot's evidence is an
  UNBROKEN carry ⇒ a liquidation forces a 2+ day restart, pushing to mid-August.
🔴 **AWAITS RAMA (Q7):** (a) ship the filter before 4-Aug ⭐recommended · (b) flip
4-Aug, defer the pilot · (c) accept in writing. ⛔ **Not (c) by default.**

## ⚠️ "PROTECTED BY GTT" IS AN ASSUMPTION MADE AT THE WORST MOMENT
A HARD_KILL fires exactly when the system's picture of reality is broken — nothing
has established the GTT is ACTIVE, unmodified, or was ever placed.
⇒ **DESIGNED (not built): HARD_KILL must not flatten delivery, but MUST VERIFY
every delivery holding has a live protective GTT and raise CRITICAL for any that
does not.** Confirm protected, never assume protected. **NON-BLOCKER** — it is
detect-and-alert only, and on 4-Aug the operator is watching; it earns its keep on
the first UNATTENDED delivery day.
⛔ **AND THE BOUND, WRITTEN DOWN: a GTT stop is a TRIGGER + a LIMIT — a hard gap
through the limit leaves it UNFILLED, and a GTT cannot fire while the market is
closed.** SL limit sits 3% below trigger ⇒ −13.0% of arm price on the T2 band.
⇒ **Delivery surviving HARD_KILL is a DELIBERATE ACCEPTANCE OF GAP RISK** — record
it as a choice, never as a safety property.

## 🔑 ONE ROOT CAUSE, NAMED ONCE — do not fix it four times
**"A live component that cannot see delivery inventory."** Symptoms: the kill's
blindness · `reconcile_positions`' false MISSING_AT_BROKER · FORCE_EXIT_ALL · the
GTT-coverage check. ⇒ **ONE reader serves all four and already runs in production:
`CncGttMonitor._gather()` (`orders/cnc_gtt_monitor.py:422-455`)** — merges
`get_holdings()` with CNC-filtered `get_positions()`, and DEFERS on broker failure
rather than reading no-data as no-positions (Y4). ⛔ **Never write a third
definition of "held."** ⚠️ Lifting it touches a LIVE protection path ⇒ careful loop.

## ❓ OPEN, flagged not decided
**Q6 — the NULL-product fallback changed direction.** `:1510` falls back to
INTRADAY, commented *"safest: MIS exits are always allowed"*. Under the revised
decision that means **an unknown-product trade gets FLATTENED**. Sparing it
protects delivery but could leave a naked MIS live in an emergency. ⛔ Do not
silently pick one. · **Q8** GTT check: verify qty coverage too, or only presence?
(partial coverage is the silent case) · **Q9** trace the flip's effect on BL9.
