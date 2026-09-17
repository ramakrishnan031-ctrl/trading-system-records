---
name: tgt-retry-crashloop-postmortem-24jun
description: tgt_retry_manager crash-looped Mon/Tue (is_within_market_hours arg-mismatch, BORN-BROKEN not a regression); NO harm (no trade ever needed a retry); added signature-lock + crash-loop CRITICAL alert + /health liveness; post-mortem 24-Jun
metadata:
  node_type: memory
  type: project
  originSessionId: 70f5d745-f68b-453a-9155-61b7b08308ff
---

**Post-mortem 24-Jun (branch `tgt-retry-postmortem-24jun`). The crash was already auto-fixed; this slice = confirm + add a guard so a dead safety daemon can't sit silent again. No schema change.**

**Symptom:** `tgt_retry_manager` (30s TGT re-place daemon) error-looped every cycle — `TypeError: is_within_market_hours() missing 2 required positional arguments: 'open_t' and 'close_t'` at `tgt_retry_manager.py:161` (`is_within_market_hours(now)`). Counts (from VM `logs/system_*`): **Mon 22-Jun = 840, Tue 23-Jun = 230, Wed 24-Jun = 0.** The `_loop` try/except caught it each time (process never died) → 840 silent ERRORs/day, ZERO alerts. The retry SAFETY NET was dead for two live days.

**Root cause — BORN BROKEN, not a latent regression (corrects the task's hypothesis):** `is_within_market_hours` was *created* by FIX-169 F18 (commit `c303e04`, 13-Jun) WITH the 3-arg signature `(now_t, open_t, close_t)` — it never had a 1-arg form. `tgt_retry_manager` was written SIX DAYS LATER (`6ee5b7e`, 19-Jun 16:45) calling it `is_within_market_hours(now)` (1 arg) — **wrong from its first commit; it never worked.** Invisible until first exercised: deploy ≠ restart + FIX-189 market-window exit meant the new daemon's loop didn't run until Mon 22-Jun 08:15.

**Why no test caught it:** the ONE manager test that turns the guard on (`test_manager_skips_outside_market_hours`) **patched `is_within_market_hours` with a MagicMock** → the wrong arg-count was masked; every other manager test sets `market_hours_guard=False`. No test ever made the real 3-arg call.

**Fix was INCIDENTAL** — it rode along as "P2" inside the unrelated NOCIL circuit-clamp fix (`8812026`, 23-Jun 02:06), deployed + restarted **23-Jun 12:28** (the FIX-191 resume; last cycle_error 12:28:14, fixed code `tgt_retry_manager.started` 12:28:29). Today (24-Jun): `started` once, 0 cycle_errors, 0 `is_within_market_hours` mentions — fix confirmed real.

**HARM Mon/Tue = NONE (decisive evidence):** **no trade has EVER been flagged for retry** — `SELECT … WHERE needs_tgt_retry=1 OR tgt_retry_count>0` is EMPTY all-time; zero Bug-C "SL-only" events in Mon/Tue logs. The retry manager's candidate query would have returned empty every cycle anyway, so the crash (which happened BEFORE that query) cost nothing. Mon = 14 trades (CLOSED/FAILED, none flagged); Tue = 17 (mostly FAILED never-filled silver/ETF + 2 clean CLOSED with `exits_verified=1`). **PACEDIGITK (Tue, `exits_verified=0`) is SEPARATE** (= Issue 2 circuit-cap, deferred to Part C): it FILLED, BOTH `limit_triple.sl_placed` + `limit_triple.tgt_placed` fired (TGT WAS placed), `needs_tgt_retry=0`, closed `SL_HIT`; its `exits_verified=0` came from `exits_verify_mismatch` after a circuit `exit_price_clamped_to_band` — nothing to do with the dead retry net.

**ADDED (the guard — `orders/tgt_retry_manager.py`):**
1. **Signature-lock test** (`test_is_within_market_hours_call_signature_locked`): `inspect.signature` must be exactly `(now_t, open_t, close_t)` + binds the manager's 3-arg call and rejects the old 1-arg call → a future signature change breaks the test, not prod.
2. **Real-call regression tests** (in-hours/off-hours) that run `run_once()` with the REAL (un-mocked) guard — reproduces the Mon/Tue TypeError, now green.
3. **Crash-loop self-detection:** `_loop` tracks consecutive cycle failures; ≥`crash_alert_threshold` (default 3 → ~90s) fires ONE throttled CRITICAL via the notifier (sentinel→email + Telegram), re-alerts ≤1/`crash_realert_interval_sec` (default 1h), and logs+INFO on recovery. Converts "dead 2 days, 840 silent ERRORs" → "1 CRITICAL email in ~90s."
4. **`health_snapshot()` on /health** (`tgt_retry_provider` threaded `main.py`→`healthcheck_server`): `ok=False`/503 when the worker is `dead` (never started / thread gone) or `crash_loop`; `disabled`→ok. Pre-flight **Phase B (`engine.py`) already curls `:8080/health`** → a dead daemon now auto-surfaces as a Phase-B failing check (`failing ['tgt_retry']`), no engine.py change.

**Monitoring status (Part 3.3):** before = NOT health-checked (in-proc thread, not a cron, no liveness probe). After = self-alert (fast, any time of day) + /health 503 + pre-flight Phase B (catches a boot-dead thread at 09:14). Tests +11 (`test_tgt_retry` +7, `test_healthcheck_server` +4).

**Side-finding (separate bug, flagged NOT fixed):** today's 2 unrelated TypeErrors = `strategy_governor.notifier_failed: TelegramNotifier.send() missing 1 required positional argument: 'severity'` — the strategy-circuit-breaker's notify call omits `severity` → a LOST alert (not a trade action). Worth a one-line fix next.

**Root lesson:** a safety-net daemon that isn't health-checked can die silently. Signature-lock cross-module calls; monitor every safety daemon.

Related: [[tgt_retry_mechanism]] · [[fix_190_incident]] · [[fix_191_false_softkill_23jun]] · [[slice1_rr_fix_deployed_22jun]]
