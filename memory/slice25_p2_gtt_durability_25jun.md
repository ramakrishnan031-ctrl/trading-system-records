---
name: slice25_p2_gtt_durability_25jun
description: "SLICE2.5-P2 — durable CNC overnight-GTT (schema v36 gtt_state) + CncGttMonitor reconcile/GTT_EXIT + 15-min monitor; STAGED, delivery_enabled=false"
metadata: 
  node_type: memory
  type: project
  originSessionId: d062a78b-bc2d-4973-9dc4-cd7f1d9913c4
---

SLICE2.5-P2 (25-Jun-2026, Opus 4.8): Phase 2 of the Delivery arc — makes P1's CNC
overnight OCO-GTT **durable + self-healing**. **DEPLOYED to main `bad0aad` 25-Jun
~22:23 IST** (one-time authorized push+restart; the standing Rama-owns-push/restart rule
is RESTORED after — not a precedent). ff-merged the 8 P2 commits onto main; push →
post-receive deployed clean + crontab auto-installed (no hook errors); the 22:23 restart
**exited 0/SUCCESS on the market-window guard** (post-close, by design — NOT a crash;
813ms, before StateStore init). **Schema v36 applies at the Fri 08:15 in-window boot**
(live DB still v35 tonight — the guard exited first; the `.backup` proved v35→v36 safe
18/18 AND the deployed schema.sql/`EXPECTED_SCHEMA_VERSION` verified =36). Broker-session-
free verify **15/15 PASS** (delivery_enabled=false, gtt_sl_off=0.03, Config Auditor 0
BLOCKs — the lone entry_end-vs-squareoff WARN is pre-existing, all P2 modules import
clean). `delivery_enabled=false` throughout (durability + safety only, no activation).
Go-live gates before delivery_enabled=true remain: T2 · FIX-183 · C1-watch.

**Schema v36 (STEP 0)** — TABLE 37 `gtt_state`, a PURE ADDITION (CREATE IF NOT EXISTS,
no MIGRATION_TABLES rebuild, same path as v31/v33): `gtt_id INTEGER PK` (= broker
trigger id), `trade_id` FK→trades, exit_side/qty/sl_trigger/sl_limit/tgt_trigger/
tgt_limit, status CHECK `ACTIVE|TRIGGERED|CANCELLED|EXPIRED|REJECTED|CLEANED`,
`needs_review` (Y2 latch), last_verified_at, 2 indexes. `EXPECTED_SCHEMA_VERSION 35→36`.
**Verified on a `.backup` of the live 161 MB DB** (v35→v36, 0 rebuilt, all rowcounts
intact, FK/integrity/WAL clean) — Rama nodded before the commit. **Y6:** a trade may
accrue MANY rows over its life (each recreate = new gtt_id = new row = history); the M2
one-GTT invariant is on `status='ACTIVE'`.

**gtt_state REPLACES P1's in-memory `_trade_gtts` map** as the source of truth (the map
is now a hot cache hydrated on boot via `CncGttPlacer.hydrate_from_store()`).

Key parts:
- `broker/zerodha_adapter`: +`get_gtt`/`get_gtts`/`delete_gtt`/`get_holdings` (live=Kite,
  paper=in-memory `_paper_gtts`/`_paper_holdings` + `seed_paper_holding`). **Paper gtt
  ids are NUMERIC** (`_PAPER_GTT_ID_BASE`) — a non-numeric `PAPER_GTT_*` string fails
  `datatype mismatch` against the INTEGER PK.
- **R2 guard split (STEP 1.5):** `delivery_enabled` gates ONLY the CNC entry
  (`place_order`); GTT ops (place/modify/delete/get/holdings) are NOT gated — protection
  must survive disablement (with delivery off there are no new entries → a GTT op only
  ever touches a pre-existing holding).
- `orders/cnc_gtt_monitor.CncGttMonitor.reconcile()` — the shared routine. Per ACTIVE
  row: gather get_gtts + holdings + same-day CNC positions → M1/M2 → **K6 ladder**:
  healthy→touch / **GTT_EXIT** (triggered+flat → finalise CLOSED + release delivery-bucket
  capital + publish PositionClosed SYSTEM-OWNED + CLEANED; idempotent via the OPEN→CLOSED
  gate `mark_trade_closed_gtt` so a double-observe never double-releases) / **F6**
  (triggered+still-holding → CRITICAL re-protect remaining) / recreate (missing+qty-match
  in-hours, Y3 fresh LTP; `forget()` then place fresh) / **Y1 pre-open queue** (missing
  pre-open → queued, drained on the first in-hours cycle BEFORE the gather) /
  **qty-mismatch** (CRITICAL ONCE via Y2 needs_review + cancel wrong-qty GTT + NO recreate
  + NO soft-kill + intraday unaffected) / orphan-active-flat (delete+finalise) / **>1
  ACTIVE → SOFT-KILL** / **Y4** broker gather fail → defer+alert (never crash, never treat
  no-data as flat).
- **STEP 4 wiring** (`order_reconciler`): startup [4a] + 15-min in-hours cadence [4b]
  (first in-hours fires immediately for the Y1 drain; reuses the daemon, no new
  scheduler). **Delivery trades (ACTIVE gtt_state) are EXCLUDED from CHECK1/3/4/5 +
  CHECK2 + CHECK9/G5b/duplicate** — a carried CNC holding lives in `holdings()` not
  `positions()`, so without this CHECK1 would wrongly mark it CLOSED_MANUAL and G5b would
  place a spurious SL. main.py wires `market_hours_fn = market_windows.is_market_open`.
- **STEP 5 (8b):** orphan sweep forensic-logs THEN deletes a LEAKED system GTT (still
  ACTIVE at broker, row non-ACTIVE); a human/external GTT (no gtt_state row) is NEVER
  deleted (FIX-182); 50-cap WARNING/CRITICAL; `sweep_stale_orders` touches ONLY the
  `orders` table — a gtt_state GTT is a live protective leg exempt from every cancel-sweep
  (`delete_gtt` is the sole remover).
- **STEP 6 alerting:** `telegram_notifier.send(... source_module="cnc_gtt_monitor")`,
  WARNING (info/50-cap) vs CRITICAL (qty-mismatch/soft-kill/F6/re-protect-fail; CRITICAL
  writes a sentinel → email fallback), Y2 de-dup on needs_review.

**Parity:** the only live/paper difference is the broker I/O boundary; reconcile +
GTT_EXIT + ladder run end-to-end in paper (injected-state tests). Tests:
`test_cnc_gtt_slice25_p2` (5), `test_cnc_gtt_monitor` (13), `test_cnc_gtt_step4_wiring`
(4), P1 asserts updated for numeric gids. **Full PC unit suite 3793 passed / 32
pre-existing env-fails (test_main waitress + TOTP/NTP/interactive — green on VM) / 0
regressions.** T2 (`scripts/t2_cnc_gtt_realtest.py`) real-API/TPIN proof remains the
blocker before `delivery_enabled=true`. See [[slice25_p1_cnc_gtt_25jun]] · [[db_schema_v28_split]].
