---
name: order-reconciliation-audit-18jun
description: "How order polling, OCO, orphan handling, EOD, startup, broker APIs and order/trade state machines work (read-only audit 18-Jun-2026)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

ORDER RECONCILIATION & ORPHAN AUDIT (18-Jun-2026, investigation only). Context: Rama sometimes
closes system positions on Kite manually. Two monitor threads run concurrently:

## Q1 Polling — TWO independent daemon threads
- broker/order_monitor.py OrderMonitor: per-ORDER fill poller. _poll_loop:594 → _poll_cycle:602 →
  _process_order:632 calls adapter.get_order_history(broker_order_id):639 for EACH tracked order.
  Interval = order_monitor.poll_interval_sec = 2s (system_config.yaml:71). Drives OSM, emits
  OrderFilled on COMPLETE (_handle_complete:981), handles fill-timeout/partial/orphan.
- orders/order_reconciler.py OrderReconciler: account-level poller. _poll_loop:356 (wait
  poll_interval_sec:359) → reconcile_once:334 → _reconcile:471. Interval = order_reconciler.
  poll_interval_sec = 15s (yaml:193). Calls adapter.get_positions():485 + get_open_orders() (CHECK6/9).
  Runs 9 checks each cycle. So: event-ish (2s per-order fills) + periodic (15s account reconcile).

## Q2 Lifecycle linkage (schema.sql)
- orders.trade_id → trades.trade_id (FK schema.sql:274). leg ∈ ENTRY/SL/TGT/EOD/CO/CANCEL (:228-230).
  NO oco_group / parent_order_id column. SL trail replacement chain via orders.superseded_by:272.
  trades.order_protocol ∈ CO_PLUS_TGT | LIMIT_TRIPLE (:165). One trade → many orders.

## Q3 OCO + orphan handling (SOFTWARE OCO, not broker-native)
- One exit leg fills → OrderFilled → order_placer._on_order_filled:1330 → _handle_exit_fill:1805:
  exit_reason SL_HIT/TGT_HIT (_LEG_TO_EXIT_REASON:232), close_trade, THEN _cancel_oco_siblings:1968
  (impl :3265) cancels the sibling. For CO_PLUS_TGT cancels the CO entry (variety=co) to collapse the
  broker-managed inner SL (:3318). order_monitor._handle_complete only emits the event; it does NOT
  cancel siblings itself. See [[co_bracket_operational_note]] [[order_lifecycle_operational_note]].
- Position closed externally (human flattens): reconciler CHECK1 _check1_manual_close:682 →
  mark_trade_manually_closed + _cancel_orphaned_orders_for_trade:893 (cancels open SL/TGT) +
  _resolve_exit_price:847 (broker trades()→LTP→entry proxy) + release_used + CRITICAL alert.
- Human cancels ONLY the SL (naked position): CHECK9 _check9_missing_exits:1356 (local SL row's
  broker_order_id not in get_open_orders) → CRITICAL + soft_kill; G5b:1589 re-places SL next cycle.
  G5b also handles missing LOCAL SL record. Orphan ORDER (broker order, no live local pos): CHECK6:1241.

## Q4 EOD (orders/eod_squareoff.py)
- Times: eod_squareoff_time 15:17 (yaml:20); RMS auto-square 15:20; market_close 15:30 (recovery-fire
  window). _fire:262 → soft_kill → PASS1 cancel pending entries (_cancel_pending_entries:668) + cancel
  live SL/TGT legs (_cancel_pending_exit_legs:751, Audit #6, prevents naked overnight) → sleep 2s
  (FIX-063 phantom-fill settle) → PASS2 _exit_open_positions:831 which FETCHES adapter.get_positions()
  and uses BROKER qty as authoritative (:858-862); CO via cancel(variety=co); LIMIT_THEN_MARKET protocol.
  So EOD IS broker-driven (verifies flat against broker). Separate cron eod_verify.py 15:55 = post-hoc.

## Q5 Startup/preflight (main.py)
- kill_switch.clear_stale_state:1273 (FIX-127). reconciler.start() runs _check_cnc_overnight_positions
  (:201/398). Phase 0f reconcile_once:2049 runs ALL 9 checks → catches yesterday's orphans/naked/human;
  ABORTS if kill switch active after (:2054). Paper: store.cancel_stale_paper_orders:2101.
  order_monitor.rehydrate_from_store:2104 + order_placer.rehydrate_fill_map:2107 (restore exit-fill watch).
  Cron preflight: premarket_healthcheck.py 08:30; token cleanup 05:00; token refresh 08:00; eod_cleanup 15:50.

## Q6 Broker APIs (broker/zerodha_adapter.py)
- place_order:429 cancel_order:563 modify_order:626 get_order_history:682 get_positions:746
  get_margins:955 get_trades:1298 get_open_orders:1334 get_quote. Periodic: get_order_history every 2s
  per tracked order; get_positions+get_open_orders+get_margins every 15s.
- Rate limits (broker_limits.yaml, client-side token bucket broker/rate_limiter.py): order burst8/8ps,
  quote 3/3, historical 2/2, margins burst8/8ps. Category map zerodha_adapter.py:220 — get_order_history→
  "order" bucket (shares with place/cancel/modify!); get_positions/get_margins/get_trades→"margins".
  429 → penalize + backoff [1,5,30]s → soft_kill; BL-6 exp backoff. CONCERN: many tracked orders polled
  at 2s pressure the SAME "order" bucket used to place/cancel orders.

## Q7 Human-placed NEW orders
- CHECK2 _check2_orphan_adoption:947 — broker position with NO local trade (any status) = human order.
  System does NOT adopt/protect/flatten. Logged once/day (FIX-182), added to _human_order_symbols.
  fund_manager has ZERO visibility (no reservation, no PnL tracking). Only effect: widens G3 capital-drift
  tolerance by human_order_margin_tolerance (5000, yaml:194) in _g3_capital_drift:1766 to avoid alert spam.
  Discriminator = a local trade exists for that symbol today. See [[human_order_policy]].

## Q8 State machines
- ORDER (broker/order_state_machine.py:64): PENDING, SUBMITTED, OPEN, PARTIAL, COMPLETE, CANCELLED,
  FAILED, EXPIRED, UNKNOWN_IN_FLIGHT. Terminal: COMPLETE/CANCELLED/FAILED/EXPIRED. Transition table:100.
- TRADE (schema.sql:157): PENDING, PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL, CANCELLED,
  FAILED, UNKNOWN_IN_FLIGHT, REJECTED*. CLOSED_MANUAL = the "externally closed" marker (set by CHECK1);
  EXITING = hard_kill MARKET exit in flight (FIX-179).

## GAPS (don't exist yet)
1. No broker-native OCO — software-only; relies on 2s poll + cancel. Race handled by close_trade
   double-guard + OCO-runs-after-close ordering (order_placer comment :1961).
2. No order-level CANCELLED_BY_HUMAN / EXTERNALLY_CLOSED state — a human cancel looks identical to a
   system CANCELLED at the order row; only reconciliation_log + trade.CLOSED_MANUAL distinguish intent.
3. Human modifying an SL/TGT price so it fills → recorded as SL_HIT/TGT_HIT with the actual fill price
   (exit_reason may mislabel a human-driven exit; cosmetic).
4. Human NEW orders: no capital/PnL accounting at all; daily-loss controls (fm_ledger) can't see them.
5. CHECK2/6/9 skipped for a cycle on broker timeout/auth error (RC11) — orphan detection pauses.

═══════════════════════════════════════════════════════════════════════════════
17-JUN ORPHAN INCIDENT — ROOT CAUSE (investigated 18-Jun-2026, LIVE mode)
═══════════════════════════════════════════════════════════════════════════════
Mode: LIVE (system_2026-06-18.log "starting (mode=live)"; real Kite order IDs). NOT paper —
the ShadowTracker/paper hypothesis is moot for this incident.

THE ORPHAN: IRFC SL order_id 260617171317470 (trade trd_3b83c7c82d884fbe87d7f50faae0265d).
Sequence (cross-cycle race + EOD timing):
- 13:40 IRFC entry filled at broker; local trade still PENDING_FILL (CHECK2 INFLIGHT_ORPHAN).
  Original SL 260617171027280 + TGT placed.
- 15:17:04 reconcile cycle A: G5b CRASH_RECOVERY_SL placed a NEW SL 260617171317470 (the trade
  looked SL-less for the inflight row). reconciliation_log: "CRASH_RECOVERY_SL ... Placed SL SELL".
- 15:17:20 cycle B (next 15s poll): Rama had manually closed IRFC between cycles → broker shows no
  position → CHECK1 MANUAL_CLOSE → _cancel_orphaned_orders_for_trade cancelled 260617171317470 at
  broker (debug log: DELETE /orders/regular/260617171317470 → 200). Trade → CLOSED_MANUAL.
- BUT local orders.status for ...470 was left NON-TERMINAL. After 15:17:20 there is NO further
  mention of ...470 in 17-Jun logs → order_monitor never observed the broker CANCELLED before the
  daily EOD shutdown.
- 18-Jun: broker no longer lists a 17-Jun order_id (daily reset) → CHECK6 (matches local↔broker
  open orders) cannot resolve it; order_monitor rehydrate can't either. Orphan persisted.
- 18-Jun 08:10:32: manually set to CANCELLED (recon=RECONCILED) by VS Code Claude. (18-Jun logs
  show NO automated handling of the order_id → system did not self-heal.)

ROOT CAUSE: orders/order_reconciler.py `_cancel_orphaned_orders_for_trade` (~:893-936) cancels the
orphaned SL/TGT at the BROKER via adapter.cancel_order but NEVER writes the local orders.status. It
relies on order_monitor to later poll the broker and transition the row to CANCELLED. When the cancel
happens at/near EOD (15:17) there is no subsequent order_monitor poll before daily shutdown, so the
local row stays non-terminal and survives the daily rollover, after which no check can match it
(broker has dropped the order). Contributing trigger: G5b placed a recovery SL for a position that
was simultaneously being manually closed (cross-cycle race) — the SL was born orphaned.

IS A FIX NEEDED? YES — systemic gap, not a one-off. Recurs whenever an orphaned exit leg is
broker-cancelled near EOD (or whenever order_monitor misses a post-cancel poll). Recommended (NO code
changed in this investigation):
 1. PRIMARY: _cancel_orphaned_orders_for_trade should UPDATE local orders.status='CANCELLED'
    (+updated_at) right after a successful broker cancel, and also treat "order not found / cannot be
    cancelled (already gone)" as terminal. Closes the loop independent of order_monitor timing.
 2. DEFENSE-IN-DEPTH: startup/EOD sweep marking any non-terminal local order whose parent trade is
    terminal (CLOSED/CLOSED_MANUAL/CANCELLED/FAILED) as CANCELLED.
 3. OPTIONAL: G5b guard — skip recovery-SL placement when broker reports no live position for the
    symbol (prevents creating a doomed SL during a manual-close race).
Other observations from the logs (not the cause): Zerodha 503 on get_open_orders at 18-Jun 06:27
(pre-market maintenance, hit CHECK6); BEPL SL cancel "being processed" then filled (no orphan); 18-Jun
10:58–10:59 restart crash-loop (the Kite-IP/403 issue, see [[kite_ip_allowlist_dependency]]);
INDOFARM in-flight orphan spam on 18-Jun is a separate same-day PENDING_FILL trade.
