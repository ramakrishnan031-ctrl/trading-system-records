---
name: daily-resets-clock-bound-06aug
description: "MEASURED 06-Aug — every daily risk counter is CLOCK-bound (re-read per call, queried by date); what is BOOT-bound is the kill auto-clear, the holiday guard, the capital seed and the day-floor."
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cfdeb7d-39e3-4a02-a0f1-e7eae9351c55
  modified: 2026-08-06T13:45:15.043Z
---

**(S) 06-Aug-2026, source read of every call site.** Settles *"if the service is not stopped, does
it trade the next day on yesterday's risk controls?"* — asked because a running process had never
crossed midnight in this system's life.

## CLOCK-BOUND — these roll correctly inside a live process ✅

| control | site | mechanism |
|---|---|---|
| DAILY_TRADES cap | `capital/risk_engine.py:241` | `today = now_ist().date().isoformat()` **inside `approve()`** — ⭐ the RE16 comment *"read once"* scopes to a **single call**, ⛔ NOT the process |
| CONSECUTIVE_LOSSES | `risk_engine.py:274` | `recent_trade_pnls(…, today=today)`, same per-call value |
| daily-loss limit, **both** halves | `capital/fund_manager.py:1314`, `:1549` | each recomputes `today` immediately before the read |
| its reader | `core/state_store.py:2542-2545` | `SUM(pnl_delta) FROM fm_ledger WHERE date = ?` — **date-scoped** |
| strategy governor | `capital/strategy_governor.py:92-93` | `today_ist()` at call time |
| EOD P&L reset | `orders/eod_squareoff.py:531` → `fund_manager.py:1645` | fired by the **15:17 squareoff EVENT**, re-derives its own `today` |

⭐⭐ **FIX-051 REMOVED the in-memory `_daily_pnl` accumulator entirely** ⇒ **there is no
process-lifetime P&L state that CAN go stale.** Pinned by
`tests/integration/test_q9_post_restart_capital_wired.py:48-49` — *"NOT RESTORED — NOT HELD IN
MEMORY AT ALL."*

## BOOT-BOUND — these simply NEVER RE-RUN ⚠️

1. 🔴 **`main.py:1914` `kill_switch.clear_stale_state(today_ist_date)`** — boot-only ⇒ **a prior-day
   kill has nothing to clear it.** ⭐ Direction is **RESTRICTIVE (entries blocked) = fail-safe**,
   ⛔ not permissive. **Check this BEFORE reading "no trades today" as anything else.**
2. **`main.py:1754` `today = date.today()`** — the SU6 holiday guard, captured once before logging
   exists ⇒ a running process **never re-asks whether the new day is a trading day.** ⚠️ Bites on a
   pre-holiday / Friday→Saturday crossing, not on an ordinary weekday roll.
3. **`main.py:2404` `_start_of_today_iso`** (B5 shared day-floor) and **`initialize()`** (FM13,
   *"once at startup"*) ⇒ no boot ⇒ the **capital seed stays yesterday's**, never re-seeded from
   `broker.net`.

⛔ **DO NOT restate this as "the counters are broken across midnight" — they are not.** The correct
sentence is: **the counters roll; the boot-bound work never re-runs.**
⭐ **Already partly known and re-derived anyway** — `docs/decisions/DESIGN_midnight_day_floor.md` §B4
(21-Jul) recorded the date-scoping, citing `f1_daily_loss_after_halt_21jul2026.md`. An instance of
[[read-the-map-first-05aug]]: read the record before measuring.

Filed as F6 regression **case 9** (spans midnight, continuous AND restart) —
`docs/design/f6_delivery_exit_predicate_design_06aug2026.md` §8. Full working:
`docs/audit/STOP_PROCEDURE_06-Aug-2026.md` §4. Related: [[f6-delivery-exit-abs-defect-06aug]] ·
[[killswitch-autoclear-prior-day]] · [[counts-db-rows-not-broker-06aug]].
