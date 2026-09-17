---
name: alert-delivery-sweep-09aug
description: "MEASURED 09-Aug — N9-14 is the only DEAD notifier call repo-wide, but 14 production alert sites sit in a silent swallow, 5 rate limiters stamp before the send, and nothing can notice an alert that was never attempted."
metadata: 
  node_type: memory
  type: project
  originSessionId: d9595f8a-8cb4-47fd-9b87-a97e7c891339
  modified: 2026-08-09T06:50:27.484Z
---

# 🔇 THE ALERT-DELIVERY SWEEP — ⛔ READ-ONLY, NOTHING FIXED

**(P) AST sweep, 09-Aug-2026. 92 production `notifier.<send*>(` call sites** *(142 incl. tests)*. ⛔ **Excluded and stated: `sats/semgrep-env` is VENDORED site-packages, and `sev`/`severities`/`reset_mock`/`titles` are TEST-DOUBLE methods** — counting either would have manufactured findings.

## ① METHOD RESOLUTION — ⭐ `N9-14` IS A ONE-OFF
Resolved against the class **actually bound** (`main.py:328` → `TelegramNotifier.from_env`), ⛔ not a duck-typed assumption: `send` ×86 ✅ · `send_alert` ×4 ✅ · `send_info` ×2 ✅ · `send_critical` ×1 ✅ · **`send_warning` ×1 ❌**. ⇒ **exactly ONE dead call site repo-wide.** ⭐ **The better answer, and it makes `N9-14` an instance rather than a family on this axis.**

## ② THE SWALLOW — 🔴 *THIS* IS THE CLASS: 14 SITES
73 log the failure · 4 UNGUARDED · 1 other · **14 in a silent `except Exception: pass`.** ⭐ All 14 name a correct method **today**, so they die only if `send` itself raises — ⛔ **but the swallow is the MECHANISM, and they sit one refactor from `N9-14`.**

| what would go unreported | site |
|---|---|
| 🔴 **HARD_KILL fired and a position could NOT be exited — manual intervention required** | `kill_switch:1444` |
| 🔴 **SL placement failed permanently — an EMERGENCY market exit was placed** | `order_placer:4003` |
| 🔴 **the market-data feed is DEAD; SOFT_KILL triggered** | `live_feed:486` |
| 🔴 **EOD shutdown DEFERRED — positions still open past the window** | `main:1261` |
| the feed dropped / is reconnecting · gave up off-hours (token likely expired) | `live_feed:397` · `:457` |
| the service shut down cleanly for the day | `main:1238` |
| the sector cap is running on bad data | `order_placer:749` |
| an order was blocked — spread too wide / not enough depth | `order_placer:4104` · `:4130` |
| a position was flattened on a structure break ⚠️ *dormant, default-OFF* | `structure_exit_manager:333` |
| the nightly AI log review failed entirely · the instrument refresh failed validation | `gemini_log_review:283` · `refresh_instruments:279` |
| a signal EXPIRED before it could be acted on — ⛔ **already dead** | `signal_processor:1262` (`N9-14`) |

## ③ STAMP-BEFORE-SEND — ⛔ A CLASS OF FIVE, not `N9-14`'s alone
The allowance is consumed **even when delivery fails**: `kill_switch:856` *(1 h — KITE IP NOT ALLOWLISTED)* · `kill_switch:1442` *(5 min — HARD_KILL EXIT FAILED)* · `tgt_retry_manager:195` *(crash-loop re-alert)* · `signal_processor:1260` *(60 s — expired)* · ⚠️⚠️ **`signal_processor:623` — MINE, written today, and the LONGEST window of the five: a WHOLE DAY per symbol.**

## ④ 🔑 IS ANYTHING WATCHING? — half-refuted, half-confirmed
**Three mechanisms DO exist:** `_audit_send` *(27-Jul — one LOG line per send with `outcome` = delivered/failed/suppressed)* · `failed_alerts.log` *(ERROR tier only)* · the CRITICAL sentinel → `alert_watcher` email.
⛔⛔ **ALL THREE LIVE INSIDE `send()`.** They can only record a send that was **ATTEMPTED**. A call that never reaches `send()` — a wrong method name, or a caller-side `except: pass` — **writes nothing, anywhere.**
⛔ **And NOTHING READS the trail**: the only repo references are a note in `expected_managers.yaml` and a path in `system_config.yaml`.
⇒ ⭐ **There is no mechanism that would notice an alert that was never attempted, and no monitor on the trail that does exist.**

## ⑤ PARITY — ⚠️ **SUPERSEDED BY §⑧ BELOW; kept legible per `G4` because it is what the correction is evidence against**
~~**12 of the 14 are paper-reachable.**~~ ⛔ **WITHDRAWN as a loose RATIO — see §⑧ for the per-site split (11 / 1 / 2).** ⭐ `live_feed.connect()` at `main.py:3624` is **UNGUARDED by mode**, so the three feed alerts fire in paper too; the two cron sites are mode-independent; `structure_exit_manager` is dormant in BOTH. ⚠️ **A dead alert on a live-only path would be undetectable in paper by construction** — none of these is on one.

⛔ **NOTHING FIXED.** ⭐ Each dead alert that starts firing is a live behaviour change, and several at once would be a wall of first-ever alerts on a trading day. **Fix order and staging are Rama's** — register `N9-15`.

## 🔒 **`ALERT-DELIVERY INVESTIGATION — COMPLETE. REMEDIATION — NOT AUTHORISED.`** *(09-Aug)*

### 🔑 THE SAFETY QUESTION IS CLOSED — ⛔ no notification failure can abort a trading safety action
⭐ **The 14 swallows are a VISIBILITY problem; the 4 UNGUARDED sites were the opposite shape and had to be traced.** ⚠️ **My own sweep's *"unguarded"* label was FUNCTION-LOCAL — tracing across the call boundary REVERSES two of the four.** Recorded, because the first label would have read as four defects.

| site | verdict |
|---|---|
| `eod_squareoff:682` · `:703` *(EOD DAILY SUMMARY)* | ✅ **`GUARDED AT THE CALLER`** — `:562` wraps it in `try/except` **and logs**, and it runs AFTER every close, cancel, `reset_daily_pnl`, kill-switch resume and the `EodFireResult`. A raise costs the summary message and nothing else |
| `reporter.py:54` *(Control Tower push)* | ✅ **`CONTAINED — not a safety path`** — `run_aggregation` is `try/finally` with ⛔ no handler, so a raise DOES propagate; but `conn.commit()` is at `:273` **before** the push at `:277`, so state is durable. Cost = the pull report + result dict, on an ops cron that kills/exits/cancels nothing |
| 🔴 `alert_watcher.py:399` | **`ACCIDENTAL PROPAGATION — DEFECT`**, and self-evidently so: the file states its own contract two lines below *("a DELIVERY failure is NOT a crash — never return non-zero")*. A raise from `notifier.send` skips **the degraded marker** *(machine-visible, read by the canary/Officer)*, the `EMAIL DELIVERY DEGRADED` log line, and the counter save. ⭐ **Bounded — sentinels persist and the next pass retries; OBSERVABILITY plane, ⛔ not safety** |

⇒ ⭐⭐ **ChatGPT §14's fear — *"notification failure must never become the reason a safety action fails"* — is MEASURED AND NOT REALISED.** ⚠️ Rama pre-registered *"at least one of the four accidental"*: **correct, exactly one.**

### ✅ `kill_switch:1444` SWALLOW SCOPE — CORRECT
The `try` opens immediately before `notifier.send(` and closes immediately after — **it encloses ONLY the alert**. The method is `_alert_exit_failed(failed_trades)`: a pure alerting method RECEIVING already-failed trades; every exit and kill decision is outside it. ⇒ **the swallow protects the action and hides only the notification.**

### ⑧ PARITY, PER SITE — ⛔ the *"12 of 14"* ratio is WITHDRAWN as loose
**11 carry NO mode guard** (`kill_switch:1444` · `live_feed:397`/`:457`/`:486` · `main:1238`/`:1261` · `order_placer:749`/`:4003`/`:4104`/`:4130` · `signal_processor:1262`) — `live_feed.connect()` (`main.py:3624`) is itself mode-unguarded, so the feed alerts do run in paper. ⚠️ **But 2 of the 11 (`kill_switch:1444`, `order_placer:4003`) need a BROKER-SIDE failure, and whether the paper broker can produce one was NOT MEASURED — code-reachable ≠ behaviourally exercisable.** **1 reachable in NEITHER mode: `structure_exit_manager:333`** (default-OFF). **2 CRON-ONLY, mode-independent: `gemini_log_review:283` · `refresh_instruments:279`.** 11+1+2 = 14.

### 🔩 ROOT → MANIFESTATIONS — ⛔ ONE ROOT, NOT SEVERAL ROWS
🔑 **THE ROOT: the alert path has NO DELIVERY CONTRACT** — nothing states what must happen when an alert fails to send, so four dimensions drifted independently: **(a)** the call may not resolve · **(b)** the failure may be swallowed silently · **(c)** the allowance may be consumed before delivery is known · **(d)** observability begins AT `send()`, so anything that never reaches it writes nothing anywhere. ⛔ **`N9-14`/`N9-15` stay as written, the unguarded trace folded INTO `N9-15`, and N STAYS 248** — ⚠️ N went 233 → 248 in two days; a register that opens a row per symptom stops measuring anything.
📋 **REMEDIATION ORDER (risk-driven; ⛔ RECORDED, ⛔ NOT AUTHORISATION):** ① the two EXIT-related swallows (`order_placer:4003`, `kill_switch:1444`) ② kill/feed (`live_feed:486`, `main:1261`) ③ `alert_watcher:399` ④ the routine remainder ⑤ the limiter ordering as ONE change. ⛔⛔ **DO NOT "solve" `N9-14` by defining `send_warning` — the remediation must answer what happens when a VALID method RAISES, not only when a missing one is called.**

See also [[alert-pipeline-tag-funds-short-09aug]] · [[silent-failure-gaps-25jul]] · [[feedback-verify-rc-not-output]]
