---
name: softkill_investigation_20jun
description: "SOFT_KILL headless fix DONE 20-Jun (commit a60868f): ALL prior-day kills auto-clear at next-day startup (Rama's choice) + KILL_AUTO_CLEARED system_events audit (Task B bridge). Was already true via FIX-127 clear_stale_state; solidified + audited. Monday 22-Jun auto-clears, NO resume.sh"
metadata: 
  node_type: memory
  type: project
  originSessionId: e7a6af13-236a-41d8-aca5-213b591647fd
---

**SOFT_KILL scheduled-vs-emergency investigation — 20-Jun-2026 (READ-ONLY, no fix applied).**
The premise ("no distinction; 15:15 scheduled kill needs manual resume every morning") is **OUTDATED** —
the distinction already exists and is wired. The real issue is the inverse.

## What already exists (verified in git + on the VM)
- `capital/kill_switch.py`: `SCHEDULED_KILL_REASONS = {"circuit_breaker_force_close_15:15","EOD_SQUAREOFF"}`
  + `_is_scheduled_reason()` + `auto_clear_scheduled_kill()` (same-day, scheduled-only, flat-only,
  NEVER HARD_KILL) — **FIX-154**. And `clear_stale_state(today)` — **FIX-127** — clears ANY prior-day
  kill (incl HARD_KILL/emergency).
- `main.py` startup runs BOTH: `clear_stale_state` (1439) then `auto_clear_scheduled_kill` (1444). VM
  deploy confirmed has both (HEAD a24ae24).
- Persistence: `kill_switch_state` single row (id=1) cols **state/reason/triggered_at/triggered_by** —
  NO kill_type column; type is INFERRED from the reason string.
- Startup: after the clears, `detect_startup_scenario`→ if kill still active → `StartupScenario.HALT`
  → `main()` returns **4**; token_watcher: same-day exit4 = no restart + manual `--resume`; prior-day
  exit4 = one clean start. Resume = `deploy/resume.sh` → `scripts/clear_kill_switch.py` (refuses
  HARD_KILL without `--force`).

## So scheduled kills DO auto-clear
A `circuit_breaker_force_close_15:15` SOFT_KILL: next-day → cleared by clear_stale_state (prior-day,
no position check); same-day+flat → cleared by auto_clear_scheduled_kill. Neither needs manual resume.
**Current VM state proves it:** `kill_switch_state = SOFT_KILL / circuit_breaker_force_close_15:15 /
2026-06-19T15:15 / order_monitor` — a scheduled kill from Fri that WILL auto-clear Monday 08:30.

## The REAL gaps (inverse of the premise)
1. **clear_stale_state is too aggressive** — auto-clears prior-day **EMERGENCY + HARD_KILL** too (test
   `test_clear_stale_state_hard_kill_also_cleared` confirms), on the assumption "reconciliation
   re-triggers." For **review-required** kills it does NOT re-trigger → they vanish. **This DEFEATS the
   System Manager's "SOFT_KILL for tomorrow"** (set 18:45 today → prior-day at Mon 08:30 →
   clear_stale_state clears it BEFORE the operator reviews). HARD_KILL aftermath likewise auto-clears
   next day. ← biggest finding.
2. **Idempotent-masking**: `soft_kill` is a no-op if already SOFT_KILL → if the 15:15 scheduled kill
   fires FIRST, a later emergency SOFT_KILL keeps the *scheduled* reason → same-day auto_clear would
   wrongly clear it. (Minor; HARD emergencies aren't masked.)
3. Same-day restart with open positions → scheduled kill NOT auto-cleared (minor; intraday flat).
4. EOD self-exit (16:00) leaves the scheduled kill in the DB overnight → `/health` 503 overnight
   (FIX-188) for a routine kill. Cosmetic.

## Why Rama still resumes manually (hypotheses — NOT the 15:15 kill)
Most likely EMERGENCY same-day re-triggers: **Kite IP-403 BrokerAuthError** on the morning's first
order → emergency kill → HALT exit 4 (see `kite_ip_allowlist_dependency`); or pre-FIX-154 muscle memory;
or a deploy-gap day. The pure 15:15 scheduled kill auto-clears.

## Triggers (reason → classification)
SCHEDULED: `circuit_breaker_force_close_15:15` (main.py:535), `EOD_SQUAREOFF` (eod_squareoff.py:324).
EMERGENCY (all others): clock_skew_critical, `{source}:{reason}` critical-failure (incl BrokerAuthError),
circuit_breaker_api_failure (HARD), daily_loss_limit_breached, orphan_order:*, token-expiry,
Auto-trip N API failures, LIVEFEED_*, reconciler/fund_manager-invariant/drift_handler/order_placer
hard/soft, `System Manager EOD <day>: <reasons>`.

## DECISION + FIX APPLIED (20-Jun, commit a60868f)
The investigation had proposed making clear_stale_state reason-aware (KEEP prior-day emergencies). **Rama
chose the OPPOSITE: TRUE HEADLESS — ALL prior-day kills auto-clear** (scheduled, emergency, HARD_KILL,
loss-limit, System Manager EOD). The system NEVER blocks startup; the safety net shifts to EOD report
analysis ("Task B", separate/later). Since `clear_stale_state` already cleared all prior-day kinds, the
fix **solidified** it (explicit headless docstring) and added the **audit bridge** for Task B:
`KillSwitch._record_cleared_kill()` writes a `system_events` row (`event_type=KILL_AUTO_CLEARED`; details
JSON = previous_state / reason / triggered_by / triggered_at / classification `scheduled|emergency` /
`cleared_via` `clear_stale_state|auto_clear_scheduled`) on EVERY auto-clear. Same-day kills still persist
(the `triggered_date >= today` guard is unchanged → loss-limit/HARD_KILL stay active intraday).
**Why/How to apply:** Task B's EOD report should query `system_events WHERE event_type='KILL_AUTO_CLEARED'`
to surface what the headless start cleared overnight (esp. an `emergency`/HARD_KILL that no longer
blocks). System Manager kill is dated `now_ist` (run-time, never post-dated) → always clears as prior-day.
**Monday 22-Jun: live kill (`circuit_breaker_force_close_15:15`, Fri) auto-clears at 08:30, NO resume.sh**
(proven on a DB copy → INACTIVE + audit row). The morning manual-resume Rama actually hits is a SAME-DAY
emergency re-trigger (Kite IP-403 BrokerAuthError → HALT exit 4), a separate token/IP issue, NOT this.
Parity-safe (kill switch is mode-agnostic). +4 tests; 42 kill_switch tests pass.
Related: [[task_5_system_manager]], [[fix_190_incident]], [[kite_ip_allowlist_dependency]],
[[fix_188_headless_autostart]].
