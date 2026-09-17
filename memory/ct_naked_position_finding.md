---
name: ct-naked-position-finding
description: "P0 DESIGN_GAP: paper-mode CHECK9 false positive — SL fill timing race triggers SOFT_KILL + emergency exit cascade"
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

## Finding: Paper-Mode Naked Position False Positive (08-Jun-2026, 10:43 IST)

**Classification:** DESIGN_GAP (paper-mode timing race)

**Symptoms:** SOFT_KILL fired during normal trading. CHECK9 MISSING_EXITS detected for NRBBEARING — SL order not in broker open orders. Emergency MARKET exits placed. Multiple cascading emergency orders (11+ on first trade, 9+ on second).

**Root Cause:**
1. NRBBEARING SL order (PAPER_6E10F2FFFB08) filled via LTP-gated paper synth — LTP crossed SL
2. Filled SL transitions from SUBMITTED→COMPLETE in `_paper_fills`
3. `get_open_orders()` no longer returns it (status=COMPLETE)
4. Before order_monitor processes the OrderFilled event and closes the trade in DB...
5. Reconciler CHECK9 runs → sees OPEN trade + no SL in open orders → "naked position"
6. Emergency MARKET EXIT placed → SOFT_KILL activated

**Cascade bug:** After first emergency exit fills, paper_positions reduces qty. Next reconciler cycle sees trade STILL OPEN (order_monitor hasn't caught up) with smaller qty → places ANOTHER emergency exit. Repeats until qty=5 remains.

**Why this doesn't affect live mode:** In live mode, Kite API returns order status from broker backend — SL fill, trade update, and order cancellation happen atomically from the broker side. No timing window for CHECK9 false positive.

**Fix options (post-crash-test):**
1. **Skip CHECK9 in paper mode** — simplest, but loses paper/live parity for a safety check
2. **Add grace period** — if SL/TGT order recently completed (within last 30s), suppress CHECK9 alert for that trade
3. **Atomic paper fill** — make `_synthesise_fill` update DB trade status synchronously before reconciler next cycle
4. **Emergency exit dedup** — CHECK9 should not place a second emergency exit if one is already in-flight for the same trade

**Recommended:** Option 4 (emergency exit dedup) + Option 2 (grace period) — defense in depth. Both fix the cascade AND the false positive.

**Impact on crash test Day 1:** System in SOFT_KILL. Signal injection blocked. Isolated FM tests still work. Need --resume before afternoon time-gated tests.

**Related:** [[ct_capital_drift_finding]] (also paper-mode adapter gap)
