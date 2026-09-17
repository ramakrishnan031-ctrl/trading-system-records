---
name: fix-186-orphan-leak
description: "FIX-186 — 3 fixes for the 17-Jun IRFC orphan-order DB leak (local-DB finalize, stale sweep, G5b race guard)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d2f14dc-74af-404c-b5f4-7a58aa389121
---

FIX-186 (18-Jun-2026): root-cause fix for the orphan-order DB leak (17-Jun IRFC incident — see
[[order_reconciliation_audit_18jun]]). LIVE-mode bug. 3 separate commits, all pushed + deployed to VM.

ROOT CAUSE: order_reconciler `_cancel_orphaned_orders_for_trade` cancelled SL/TGT at the BROKER but
never wrote local orders.status; it relied on order_monitor to observe the cancel on a later poll.
When the cancel landed at EOD shutdown, no poll followed → the stale non-terminal row leaked to the
next day, where no check could match it (broker resets order history daily). The doomed order was a
G5b recovery SL placed one cycle and CHECK1-cancelled the next (manual-close race).

FIX 1 (commit 488eb21) — _cancel_orphaned_orders_for_trade now finalizes the LOCAL DB:
  success / "order not found" (already gone) → mark CANCELLED; "being processed" (may fill) → leave
  for order_monitor; other error → leave for retry. New helper `_mark_order_cancelled_local` has a
  terminal-status WHERE guard so a filled (COMPLETE) order is never clobbered. Classifiers:
  `_cancel_reason_already_gone` / `_cancel_reason_being_processed`.

FIX 2 (commit 8421c68) — new public `OrderReconciler.sweep_stale_orders()`: marks any non-terminal
  order whose parent trade is terminal (CLOSED/CLOSED_MANUAL/CANCELLED/FAILED) as CANCELLED + WARNING
  Telegram alert if count>0. Wired at startup (main.py, after reconcile_once) and at EOD
  (EodSquareoff.set_stale_order_sweep(), invoked after the two-pass squareoff). Best-effort; never
  aborts startup/EOD. Defense-in-depth backstop independent of order_monitor timing.

FIX 3 (commit 67db189) — `_g5b_crash_recovery_sl(trade, broker_positions=...)`: skips placing a
  recovery SL when the broker snapshot positively shows no live position for the symbol (absent or
  qty==0) — prevents the doomed-SL race. Fail-safe: snapshot None (broker timeout/auth) → still place
  (protect the position). Reuses the same broker_pos snapshot CHECK1 uses that cycle (no extra call;
  hoisted in `_reconcile`).

PARITY: all 3 mode-agnostic (reconciler path doesn't branch on paper/live; paper adapter cancel
returns success). TESTS: 19 new in test_order_reconciler.py (6+3+ G5b set). Full suite 3087 passed;
the only 4 failures are PRE-EXISTING/ENVIRONMENTAL — `ntp_clock_skew` (utils/startup_checks.py:506
check_ntp_sync makes a real UDP pool.ntp.org:123 query; the dev box has no NTP path; unrelated module,
not touched by FIX-186; passes on the VM). VM verified: code deployed, AST-parses, 94 relevant tests
pass on Python 3.12.

ACTIVATION: deploy != restart ([[deploy_requires_restart]]) — code is in the VM working tree; the
running process picks it up on the next restart.
