---
name: fix_183_gtt_adoption_26jun
description: "FIX-183 orphan-GTT adoption — reconstruct a live broker GTT with no gtt_state row + correlate to its open delivery trade, as a prepass before CHECK1; closes C2.1; no schema; DEPLOYED to main af4b784 26-Jun"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b445dff-c546-4ec1-b292-3ec665699a63
---

**FIX-183 (26-Jun-2026): orphan-GTT ADOPTION / reconstruction.** Completes the locked
SLICE2.5-P2 principle "broker GTT = authority, `gtt_state` = self-healing mirror". A LIVE
broker GTT (status `active`) with NO `gtt_state` row is now ADOPTED instead of orphaned.

**The gap it closes (C2.1):** a carried CNC delivery holding lives in `holdings()`, NOT
`positions()`, so the reconciler's `bp is None` → without an ACTIVE `gtt_state` row to exclude
it, CHECK1 would mis-mark the trade `CLOSED_MANUAL` (and G5b/CHECK9 place a spurious SL). A
row-less GTT (persist-failure at placement, or one predating the table) had no self-healing path.

**Build:**
- `orders/cnc_gtt_monitor.py` `adopt_orphan_gtts()` — skip unless `status=='active'`; skip if a
  row exists for the `gtt_id` (`get_gtt_state_by_id`); else RECONSTRUCT all columns except
  `trade_id` from the broker GTT (`_reconstruct_from_broker_gtt`: **SL/TGT split by trigger
  MAGNITUDE, not array index** → robust to leg reordering; unparseable → WARN, leave alone) and
  CORRELATE `trade_id` product-aware (`_delivery_open_trades_by_symbol` via `get_all_open_trades`,
  which carries the ENTRY-leg product through its LEFT JOIN — the bare
  `get_trades_by_status_and_symbol` lacks product). Outcomes: **1** open CNC trade w/ no ACTIVE
  row → ADOPT (`insert_gtt_state`, reusing the durable write path); **0** → can't adopt (FK
  forbids) leave-alone + WARN; **>1** (only via manual entry; `DUPLICATE_SYMBOL` blocks otherwise)
  → WARN no-adopt; **1 but already ACTIVE row** → WARN no-adopt (2nd ACTIVE row would trip M2).
- **NEVER deletes a live GTT** — adoption only INSERTs or WARNs. Unadoptable WARNs de-duped
  **once per gtt_id per process** (`_adopt_warned`, like FIX-182) so the every-cycle prepass can't
  spam (esp. benign human GTTs = the 0-trades case). Alerts `source_module="cnc_gtt_adoption"`.
- **Placement (timing fix):** narrow prepass `order_reconciler._run_gtt_adoption_prepass()` at the
  **top of `_reconcile()`**, BEFORE the delivery-exclusion build + CHECK1. Because CHECK1 is inside
  `reconcile_once`, this guarantees adopt-before-CHECK1 in BOTH startup (`start()` → reconcile_once)
  AND the 15-min poll (reconcile_once runs before the monitor's own reconcile()) — WITHOUT
  reordering `_maybe_run_cnc_monitor` or any MIS check (minimal regression). Fail-safe: no-op when
  no monitor wired; never raises. Cost: `get_gtts()` once per ~15s cycle (LIVE) — "margins" bucket
  (burst 8, 8/s) makes it trivial.

**Parity:** paper `get_gtts()` has the identical dict shape → adoption runs end-to-end in paper.
**No DB schema** (`gtt_state` exists from P2 → no `.backup` step). delivery_enabled stays **false**.

**Tests:** `tests/unit/test_cnc_gtt_adoption_fix183.py` (12, paper injected-state) incl. **the C2.1
regression** (row-less carried GTT → reconcile_once → trade stays OPEN + gains ACTIVE row, NOT
CLOSED_MANUAL; + a no-monitor contrast that DOES go CLOSED_MANUAL = the gap) and **the MIS
regression** (intraday trade → CHECK1 unchanged, no gtt_state row). Full PC unit suite **3837 pass /
12 skip / 0 regressions**; touched suites 113 pass; integration smoke 11 pass.

**DEPLOYED to main `af4b784` 26-Jun ~11:11 IST** (one-time authorized push+restart; standing
Rama-owns rule RESTORED after — not a precedent). ff-merged `fix-183-gtt-adoption-26jun` onto main
(also carried the pending P2 docs-log `75d4eca`); push → post-receive deployed clean + crontab
auto-installed (no hook errors). The 11:11 restart **self-exited 0/SUCCESS at the HOLIDAY guard**
(26-Jun = Muharram, NSE closed → "market closed, connect Monday" banner in 786ms, before StateStore)
— so like the P1/P2 after-hours boots the service didn't fully start; **real boot = Mon 29-Jun 08:15**.
Verified independently (broker-session-free, 5/5 PASS): FIX-183 symbols present (`adopt_orphan_gtts`/
`_reconstruct_from_broker_gtt`/`_run_gtt_adoption_prepass`), `load_all()` clean (Config Auditor 0
BLOCK), `delivery_enabled=False`, **live schema_version=36 + gtt_state (14 cols)** (P2 migration
already applied). One of the go-live gates before delivery_enabled=true, alongside T2 (+ Phase 3/4 next).
See [[slice25_p2_gtt_durability_25jun]], [[slice25_p1_cnc_gtt_25jun]], [[feedback_system_map_first]].
