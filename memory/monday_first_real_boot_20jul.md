---
name: monday-first-real-boot-proven-20jul
description: 20-Jul-2026 first real boot since S4 succeeded clean; S4 fix + liveness probe both proven in prod; all 6 boot-window checks GOOD
metadata: 
  node_type: memory
  type: project
  originSessionId: b14d1d0c-0ba5-4905-a624-c9bdc6af7245
  modified: 2026-07-20T03:40:27.427Z
---

**Monday 20-Jul-2026 was the first real production boot since the S4 outage, and it passed clean.** Boot-window check run once at 09:04 IST (in the 09:00-09:15 window, after boot 08:15-09:00 and the 09:00 liveness sweep, before 09:15 open). READ-ONLY, all six items GOOD:

- **A1 token** — `data_store/session/zerodha_token.json` present, refreshed today 08:15:02 IST (257B). The 05:00-delete → 08:15-TOTP-refresh cycle ran.
- **A2 service** — `active (running)` since 08:15:19 IST, `Result=success`, `ExecMainStatus=0`, `NRestarts=0`, running `main.py --mode live`. The exact inverse of the S4 signature (inactive/exit-0).
- **A3 boot complete** — full sequence ran: 8 config files, `run_all_startup_checks: OK scenario=CRASH warnings=[]`, all subsystems started, `All subsystems started -- entering runtime loop` @ 08:15:36; run loop alive at 09:06 (15s position/margin polls).
- **A4 liveness (most important)** — `cron-liveness.log` 0 bytes @ 09:00 (probe ran, no alert); ZERO LIVENESS/DOWN/CRITICAL across alert logs; alert-watcher heartbeating "No pending sentinels found" every minute. The independent backstop is proven working, and it had nothing to report.
- **A5 broker session** — `get_margins net=9875.6` (== ACTUAL capital Rs 9,875.60), split 6912.92/2962.68 = 70/30 MIS/CNC, `InstrumentCache loaded: 2228 instruments`, `KiteTicker` connected, 0 holdings/0 positions.
- **A6 webhook** — `waitress Serving on http://0.0.0.0:5000`, `ss` confirms `:5000` LISTEN, self-check passed. Zero POSTs by 09:08 = expected pre-open (Chartink fires after 09:15), NOT the BAD unreachable/5xx case.

**Rehydrate was the predicted no-op:** `rehydrate_complete replayed_trades=0 replayed_pnl_rows=0 daily_pnl=0.0 anomaly_count=0` — flat book, M-C1 carryover 0. Nothing unexpected/non-zero.

**Benign, no action (noted so a later grep doesn't alarm):** (1) `check_ntp_sync: failed to query pool.ntp.org: timed out` — non-fatal WARNING, `run_all_startup_checks` still OK/warnings=[]; the independent `clock_skew_probe` (60s) covers clock discipline. (2) `startup_scenario=CRASH: same day, no SHUTDOWN event found` sits next to `Startup scenario: COLD` — the CRASH sub-label just routes through the crash-recovery replay path, which correctly replayed 0 (flat book after the Fri 07-17 run wrote no 07-20 shutdown event). (3) Alert-log filenames are swapped: `alert_watcher.log` (14MB) is FROZEN at 07-16; `alert_watcher_2026-07-16.log` is the ACTIVE one (written today) — pre-existing logging-hygiene oddity, not a boot issue.

**Why:** This closes the "Mon = FIRST REAL BOOT PROOF" open item — the `startup_checks.py:807-808` 2xx-or-401 fix and the independent liveness probe had never both run in prod until today; both are now proven on a live morning.

**How to apply:** Treat the S4 class as proven-fixed in prod (not just verified-present). Still UNPROVEN in prod (do not conflate): Phase-1 replay of a real position, Phase-2 non-zero P&L carryover, M-C1 with non-zero carryover, same-day kill survival, first live HARD_KILL — all no-ops today because the book was flat. The 18:15 post-session checklist (`docs/audit/MONDAY_POST_SESSION_CHECKLIST.md`) is still due; its one urgent condition is forward-shadow contamination (>1 new date in the JSONL).

Related: [[monday-preboot-readiness-19jul]] [[s4-boot-outage-17jul]] [[artifact-baseline-reconciliation-19jul]] [[killswitch-autoclear-prior-day]]
