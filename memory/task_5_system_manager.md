---
name: task_5_system_manager
description: TASK
metadata: 
  node_type: memory
  type: project
  originSessionId: 6c3b6780-736c-4396-9a65-be6d83862a10
---

**TASK #5 COMPLETE (19-Jun-2026): System Manager EOD** — `scripts/system_manager.py`, runs **18:45 Mon-Fri** (after the [[task_3_cron_officer]] EOD at 18:30). A deep cross-check that goes beyond the Cron Officer (job execution only). Commits 8d37f4f→29e477e; deployed; crontab installed (registry==crontab, no divergence); first REAL run Mon 22-Jun 18:45.

**8 isolated checks** (one failing check never crashes the report): 1 config-vs-actual (effective caps honour `live_test_mode`, so cap=1/6 not 5/20; daily_loss_limit is absolute ₹), 2 order quality (entry/exit slippage, partials, orphans), 3 report integrity (REAL paths: `reports/output/daily_report_<date>.xlsx` + `.md` reports incl `reports/watchman/watchman_<date>.md`; missing = WARNING not kill), 4 system health (cron_heartbeat, PRAGMA integrity_check, disk, token, STARTUP-count, sentinels, kill switch), 5 strategy health (per-strategy win-rate + LONG/SHORT split + strategy_metrics demotions), 6 risk events (**HARD_KILL detected via LOG `HARD_KILL ACTIVATED`** — NOT queryable in any table; + drift/manual-close/orphan counts from reconciliation_log), 7 vs-yesterday (>2x deviation flags), 8 tomorrow readiness (next trading day, DB-clean stuck signals/trades/orphans, kill-switch resume).

**Output:** `generate_full_report` → Telegram via `TelegramNotifier.from_env` (cron_officer `_send` pattern); **CRITICAL severity writes a sentinel FIRST → alert-watcher email** (so violations reach Rama even with Telegram banned till 22-Jun); saved to `reports/system_manager/<date>.txt`. Exit codes 0 clean / 2 warnings / 3 violation.

**SOFT_KILL for tomorrow** (standalone `KillSwitch(store, EventBus(), log).soft_kill(reason, triggered_by="system_manager_eod")`) ONLY on a real safety violation: config cap breach (position/trade/loss/position-value), DB-integrity failure, or HARD_KILL fired today. Suppress with `--no-soft-kill`; `--dry-run` = print+save only. Missing reports / strategy concerns are warnings, never kills.

**Validated against real 19-Jun VM data:** correctly flagged the incident-day position-cap breach (3 concurrent > live_test cap 1) + 1 HARD_KILL (cleared) → would SOFT_KILL Monday; accurate slippage/strategy/risk/tomorrow sections. 10 unit tests. **Cleanup done (19-Jun):** the "6 stuck PENDING trades from 18-Jun" (POWERICA/BEPL/INDOFARM/GLOBUSSPR/BAJAJHCARE/NYKAA, qty_filled=0, ENTRY orders already CANCELLED) → marked **CANCELLED, exit_reason='pre-FIX-189 cleanup'** (DB clean now). **OPEN FOLLOW-UP:** their ~₹587 fm_ledger reservations are still live — NOT released, because touching fm_ledger while the FM is running would make in-memory _reservations disagree with the ledger and trip a false CHECK7/CAPITAL_DRIFT. Release them via FundManager.release at the next DOWNTIME (today's 16:00 EOD self-exit or Monday pre-open). Harmless meanwhile (₹587 of ₹10k, masked by Bug I tolerance). Also note: the stuck-signal check (check 8) only flags PROCESSING signals >15 min old (commit c75e9b9) so it's safe to run during market hours. See [[fix_190_incident]] context. Schema reference: trades/orders/fm_ledger/signals/cron_heartbeat/strategy_metrics/kill_switch_state/system_events/capital_snapshot/reconciliation_log (columns mapped during build).
