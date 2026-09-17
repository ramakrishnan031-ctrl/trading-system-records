---
name: friday-boot-24jul-resume
description: "Friday 24-Jul: §A boot CLEAN + A3 kill-switch PROVEN by trading + §A-afternoon read-only investigations DONE (A1 F2-gate: is_active reads memory not DB, config boot-only, every June clear a restart; A2 capital_snapshot 0 rows/tests-only/redirect-readers; A3 backup-retention one-time clear not redesign). 2 audit docs UNCOMMITTED. PENDING: §B open the real 16:05 xlsx after 16:10 (first label-batch test), then §C docs-only push IFF §B passes."
metadata: 
  node_type: memory
  type: project
  modified: 2026-07-24T07:11:20.280Z
  originSessionId: 561b005d-d545-4219-8153-9fc5bff40c6b
---

**Handoff mid-task** (instruction file "FRIDAY 24-JUL — BOOT CHECK + 16:05 REPORT VERIFICATION").
Powered down ~09:57 IST; will resume.

**§A boot (~09:41) = CLEAN, correctly ROUTINE** — nothing on the boot path changed since Thu
(label batch is report-layer `reports/*.py` + ops-dashboard; compaction is docs). Standard six all
green: token minted 08:15:01 + `kite.profile()` ok; service active NRestarts=0 ExecMainStatus=0
(boot 08:15:27); `startup_checks OK scenario=CRASH warnings=[]`; **liveness PROVEN RUN** (syslog
dispatched `liveness_probe.py` 09:30/35/40, `cron-liveness.log` 0 bytes = healthy); 09:15
margin_sync delta 0.0; receiver listening (125 live POSTs, all 403 pre-10:00 = designed gate).
A4 capital continuity holds: Thu close 9852.30 +13.03 → Fri seed **9865.30** `replayed_pnl_rows=0`
anomalies 0 (−0.03 = broker settle rounding). E4/W10 holds 3rd day: 23-Jul RESET_PNL −13.03 =
−Σpnl_delta (old code would write −8.95). A5/B2′ clean (Phase C `webhook /health 401 — Flask up`,
0 CRITICAL sentinels). VM bare == PC main == `56e8316`; deployed tree carries the label batch
(checkout 07-23 16:13 ⇒ Thu 16:05 ran OLD code, so Fri 16:05 is first real test).

**A3 DONE (Fri 10:50 IST) — SOFT_KILL cleared PROVEN BY TRADING** (not a flag read): today 439
in-window POSTs ALL 200 (an active SOFT_KILL 403s in-window per the 403 blind-spot finding; the 218
pre-10:00 were 403 = designed gate) ⇒ receiver not blocked. 250 signals received; 15 real broker
orders (7 ENTRY/4 SL/4 TGT, COMPLETE/OPEN/CANCELLED); 8 trades, 4 fills, 2 CLOSED (SURYODAY −3.96,
DBL +8.99), 2 OPEN. So NOT "no signals" and NOT "none approved" — normal trading. Flag corroborates:
INACTIVE, auto-cleared 08:15:28 by `main.auto_clear_stale`. The 55 `REJECTED_STRATEGY_CONTROL`
"delivery dormant" = STANDING `force_intraday_only:true` + `delivery_enabled:false` (stable in
backups since ≥27-Jun = the BK-1 posture), unrelated to yesterday's kill. No kill/halt-attributed
rejections (the 6 "circuit" matches = `REJECTED_CIRCUIT_PROXIMITY`, a per-symbol band guard).

**§A-AFTERNOON (read-only investigations) DONE — Fri ~12:00 IST. Docs written (UNCOMMITTED, for §C):**
`docs/audit/f2_config_reload_investigation_24jul2026.md` + `docs/audit/capital_snapshot_and_backup_retention_24jul2026.md`.
- **A1 (F2 gate):** `is_active()` reads **PROCESS MEMORY** (`kill_switch.py:461`); DB read ONCE at boot
  (`_load_state_from_store`), written on mutation (persist-first). Config is boot-only too (CL1
  `locked_decisions.yaml:730`, NO reload machinery — only SIGINT/SIGTERM shutdown at `main.py:1208`).
  Every June clear was a **RESTART** (`resume.sh`/FIX-188b = stop → clear-DB-while-stopped → start; NO
  resume/activation event type in `system_events`, only STARTUP/SHUTDOWN/CONFIG_DIFF/KILL_AUTO_CLEARED).
  ⇒ a config/DB-flag F2 with MID-SESSION effect needs NEW re-read machinery (EXPENSIVE); a trigger to the
  EXISTING in-process KillSwitch (`ks.soft_kill`/`resume`) needs **NO new state machinery** (CHEAP —
  reuses KS9 persist / KS3 recovery / KS8 event / idempotency). CONFLICT w/ "config-controlled" framing
  (F7): config lever is either not-mid-session or expensive — Rama's fork. History gap (A1.6): single-row
  table + activations not in system_events ⇒ operator F2 inherits it (cheap closure = 1 event row; not built).
- **A2 (capital_snapshot):** CONFIRMED 0 rows (live + 19-Jul backup); writers = **TESTS ONLY**. Anti-dup:
  every field ∈ `fm_ledger`+`trades` (`margin_used`≡Σ`trades.margin_reserved` over open, identical formula;
  `realized_pnl_today`≡today Σ`fm_ledger.pnl_delta`; `cash_floor`=broker-sync). ⇒ fix = **REDIRECT the 3
  readers**, NOT a producer (a producer = 2nd source that drifts from fm_ledger). WARN `engine.py:101`;
  `/metrics.capital_deployed_pct` is permanently **0.0** (`healthcheck_server.py:186-193`, computed only
  `if row:`). = **4th** false-signal-family member. Sizing: ~1 line (WARN) / ~3-site redirect (right).
- **A3 (backup retention):** `--max-delete`=**ABORT** cap (all-or-nothing, `backup_retention.py:111/117/205`),
  default **10**; cron `--apply` no override. Live backlog **62** (pre_ 50 / ts 5 / analytics 7 — NOT the
  inherited 55) ⇒ aborts nightly (cap doing its job). Verdict: **ONE-TIME clear** (`--max-delete 62`),
  steady-state ~2/day < 10 ⇒ NOT a redesign; policy sound. No anchor concept (protection = newest-N mtime;
  real anchors safe only OUT of `data_store/backups`). ⚠️ I created **14 `-wal/-shm` sidecar artifacts** via
  `mode=ro` backup opens (harmless, `.db` intact / `-wal`=0 B; use `?mode=ro&immutable=1` next time).

**⭐⭐ STILL PENDING — §B THE REAL VERIFICATION, after 16:10 (Rama nudges; NO self-wakeup = fails silently):**
Thu's 16:05 ran OLD code (push checked out 16:13) ⇒ the label batch has NEVER executed; Fri's is its
FIRST + single-variable test. PRE-STATE: today IS a real trading day (8 trades, 4 fills, 2 closed:
SURYODAY −3.96 / DBL +8.99) ⇒ `[3_Capital]` carries non-zero numbers, check not vacuous. If today ends
0 trades / 0 P&L → SAY SO (test collapses = a result, not a pass).
  B1. Open the ACTUAL `daily_report_2026-07-24.xlsx` (VM `reports/output/`). Not a test/dry-run/regen.
  B2. `[3_Capital]` = honest CAPITAL SUMMARY (Opening / Closing / Net P&L Realized) — NO broker row,
      NO Reconcile Status. The daily false REVIEW gone BY CONSTRUCTION.
  B3. ALL SEVEN sheets generated (a missing sheet = FAILURE even if `[3_Capital]` is perfect).
  B4. `daily_trade_review` capital block — display string changed; carries the GENUINE reconciliation
      that daily_report's fictional one shadowed. It must still be there.
  B5. ops-dash `risk.html` subtitle — corrected text already confirmed on VM; re-check only if convenient.
  B6. ⚠️ IF THE REPORT FAILED TO GENERATE: revert the merge + re-push immediately. Report BEFORE reverting
      UNLESS nothing generated at all (then revert first, report after).
  B7. IF CLEAN: label batch CLOSES; false-signal trio finished (B2′ 401, C1 CRITICAL count, `[3_Capital]`).
      `capital_snapshot` (A2) = newly-found 4TH member — note in report, don't let it hold the batch open.

**§C — ONLY AFTER §B PASSES — docs-only push (book flat + service self-exits 16:00 = safest window):**
  C1. Commit+push DOCS ONLY: `refused_posts_403_investigation_23jul2026.md` + the 3 §A audit docs (F2
      config-reload, capital_snapshot+backup-retention, `spandana_net_short_24jul2026.md`) +
      ONE line into `docs/SYSTEM_MAP.md` for F1 (`reset_daily_pnl()` reachable only from
      `eod_squareoff._fire()` in-process ⇒ any halted day writes no RESET_PNL row — that line CLOSES F1).
  C2. One fix per commit (do NOT bundle the SYSTEM_MAP line into an audit-doc commit).
  C3. VERIFY: PC == origin == VM bare == VM working tree; post-receive checkout ran; docs-only diff (prove it).
  C4. DO NOT restart the service (next boot Mon 27-Jul 08:15 after token refresh).
  C5. Clear the matching `UNPUSHED_PENDING_DEPLOY_LEDGER` entries as each lands.
  ⛔ DO NOT run §C if §B FAILED — that means §B6 (revert) instead, and nothing else. [[monday-post-session-clean-20jul]]
