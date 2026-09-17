---
name: service-window-configurable-25jul
description: Service shutdown time is now config (17:35) — SERVICE_WINDOW_END had TWO roles and was split; the boot guard cannot read config because it runs before load_all().
metadata: 
  node_type: memory
  type: project
  originSessionId: f2fbf924-aa62-447a-8c75-c058b96e494a
  modified: 2026-07-24T20:19:57.312Z
---

**DEPLOYED 25-Jul-2026 `570b3e8`** (Sat, off-market). `trading_hours.service_window_end`
= **17:35** (was a hardcoded `main.py SERVICE_WINDOW_END = 16:00`). Loads Mon 27-Jul 08:15.
Reason: the PB-01 Chartink EOD scanner fires **17:00**; all ten triggers since 13-Jul hit a
refused connection, so `pb01_watchlist` has 0 rows.

⭐⭐ **THE STRUCTURAL FACT WORTH REMEMBERING — `SERVICE_WINDOW_END` HAD TWO ROLES:**
the FIX-189 **boot-refusal guard** (`_within_service_window`, `main.py:1712`) *and* the
**EOD self-exit**. Moving only the stop time opens a silent trap: a crash-restart between
the two values hits the guard → **exit 0**, which `Restart=on-failure` does **not** retry
→ dead for the evening, and the liveness probe's last run is 15:55 so nothing alarms.

⚠️ **THE BOOT GUARD CANNOT READ CONFIG — it runs at `main.py:1712`, `load_all()` is at
`:1743`.** This constrains any future change to the start window. Moving the config load
earlier was rejected: a broken config on an off-hours start would go from exit 0 to
**exit 5 = an unattended restart loop**. Instead:
- `SERVICE_START_CUTOFF` (latest the service may **START**) = `SERVICE_WINDOW_END_MAX`
- schema: `market_close <= service_window_end < SERVICE_WINDOW_END_MAX (18:15)`
⇒ every legal stop is strictly inside the start window, so the trap is **unrepresentable**,
not merely untested — including after a revert to 16:00. **Accepted cost: the anti-overnight
START window widens 16:00→18:15 (135 min).** A stray start self-exits within one ≤60 s poll.

**18:15 = the `forward_shadow_record` cron**, and the bound is **drift-guarded by a test that
reads `cron_registry.yaml`** — deliberately not a comment. Justified as POSTURE (nothing in
the evening pipeline should have to reason about a live writer), NOT as a concurrency finding:
WAL tolerates it, so the "they would contend" argument is wrong and would rightly be relaxed.

**Revert = one line:** set `service_window_end: "16:00"` (schema default is `"16:00"`, so each
deploy half is independently safe under `extra="forbid"`).

🔍 **Found by measuring, not assuming:** the range validator rejected correctly, but `main()`
logged only `str(exc)` = *"Schema validation failed for system_config.yaml"* — no key, no
value. The reason was already carried in `.context["errors"]` (the channel
`TradingSystemError` documents for structured logging) and discarded. `_config_error_detail()`
now renders it. Beyond the instruction — flagged for Rama.

⚠️ **`_LIVENESS_END` (16:00) is now CONSERVATIVE, not equal to the stop.** The drift guard
changed `==` → `<=` ("never alarm during a period when a clean exit is already legitimate").
⛔ Do **not** restore `==` by raising `_LIVENESS_END` — the probe's cron `*/5 09-15` stops at
15:55 and cannot reach 17:35. **The 16:00–17:35 tail is genuinely UNWATCHED** (triggered
follow-up: extending it needs the cron **and** `_LIVENESS_END` moved together).

**Monday is a PRECONDITION, not a win:** PB-01 is `enabled:false` with no live twin, so a
captured row cannot yet be evaluated. This buys **option value** on an out-of-sample clock
that can only be started, never backfilled (a backfill from Chartink history is a backtest
by construction). [[persisted-kill-is-halt-21jul]] [[s4-boot-outage-17jul]]
[[feedback-no-fixed-test-baseline]]
