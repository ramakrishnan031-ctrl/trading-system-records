---
name: fix_182_complete
description: "FIX-182 — EOD broker-driven squareoff, human-order silence, daily summary CLOSED_MANUAL, capital-drift tolerance; plus the 16-Jun deploy-gap root cause"
metadata: 
  node_type: memory
  type: project
  originSessionId: 705e3934-5847-4a81-9394-fec010dffb93
---

FIX-182 (16-Jun-2026, commits d7b01c9 / 93396bb / de4dd31). Deployed + service restarted; FIX-180/181/182 now ACTIVE (verified /health ok, broker auth ok, positions flat). 3017 tests pass on VM (12 residual failures are pre-existing env tests — NTP/TOTP/instance-lock/interactive — caused by the live service running; none touch changed code).

**Root cause of 16-Jun Live-Day incident = DEPLOY GAP, not new bugs.** The live process started 09:04 and ran PRE-FIX-180/181 code; FIX-180/181 files were synced to the VM working tree only at 16:46 (post-market) and the service was never restarted. So today's failures (AGARIND tick-size SL rejection → HARD_KILL; 20-char tag emergency-exit failure; GICRE never flattened; AGARIND net_pnl=None) were ALL already fixed in FIX-180/181 but not running. See [[deploy_requires_restart]].

Fixes:
- **FIX 4** (orders/eod_squareoff.py `_sweep_residual_broker_positions` + `_place_marketable_limit_exit`): EOD only acted on local OPEN/PARTIAL trades, so a position live at broker with no local OPEN trade (GICRE: filled at broker while local PENDING) was never flattened ("kept 0/0"). Now after Pass-2 it re-queries broker positions and flattens any non-zero MIS/CO position the system placed (local trade exists for symbol today) via marketable LIMIT. Human/untracked positions (no local trade, e.g. ITC) are logged once and left alone. See [[human_order_policy]].
- **FIX 3** (`_send_daily_summary`): filtered status=='CLOSED' only → "No closed trades" on manual-close days. Now spans CLOSED/CLOSED_MANUAL/EXITING, coerces net_pnl None→0.0, appends human-order note.
- **FIX 2** (orders/order_reconciler.py): `_check2_orphan_adoption` logged ERROR every 15s. Post-FIX-181 it's only reached for true orphans = human orders → now INFO once/symbol/day then silenced (no repeat CapitalDriftDetected). G3 drift tolerance widened by `human_order_margin_tolerance` (OrderReconcilerConfig, default Rs5000) when human orders present.
- **FIX-182c** (main.py): latent FIX-181 bug — `app_config.capital.emergency_exit_buffer_pct` (wrong; it's `app_config.system.capital.emergency_exit_buffer_pct`). Crashed startup at kill_switch construction → crash-loop. Only surfaced now because the 09:04 process ran pre-FIX-181 main.py. Both occurrences fixed (lines 1243, 1865).

FIX 1 (operational): cleaned stale DB — SETL/HARIOMPIPE/AVL (15-Jun) PENDING→CANCELLED; GICRE PENDING→CLOSED_MANUAL + entry order CANCELLED. integrity ok.

Kill switch was persisted HARD_KILL (tick-size); cleared via KillSwitch.resume() before restart (Rama approved re-arm). Now SOFT_KILL (normal post-15:15 entry block).
