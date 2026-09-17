---
name: regime-computable-today-20jul
description: "Runtime-proven 20-Jul — the regime engine DOES compute today (271 daily NIFTY bars from live Kite); April's \"insufficient\" was a missing-handle run, and the candle-backfill hypothesis is closed."
metadata: 
  node_type: memory
  type: project
  originSessionId: d010c6e6-1e94-4ed6-9e89-609c3f52dda7
  modified: 2026-07-20T14:13:47.000Z
---

**REGIME (#07) is COMPUTABLE TODAY.** Proven by observation on the VM at 19:35 IST 20-Jul-2026,
read-only, with `regime.enabled` left **false** (the engine was constructed locally and
`compute()` called directly — the shadow *runner*, which is the only thing that persists
`regime_state.json`, was never built).

**What the engine actually issued** (recorded by wrapping the production fetch closure, lifted
out of `main.py` by AST so no import side effects could occur):
- `instrument_token=256265`, `interval="day"`, span **400 days** → **271 bars**, 2025-06-16 → 2026-07-20.
- `instrument_token=256265`, `interval="5minute"`, span 1 day → 75 bars, 09:15 → 15:25 today.
- Requirement is `max(ema_slow+1, 2*adx_period+1)` = **201**. 271 ≥ 201 ⇒ **status OK**, not UNKNOWN.
- Output: direction **BULL/LOW** (`preference_multiplier` 0.2), volatility NORMAL/MEDIUM,
  day_type UNDETERMINED/MEDIUM, `extreme_flag` false.

**The candle-backfill hypothesis is CLOSED.** A `sqlite3.connect` tracer installed before any
project import recorded **0 connections and 0 SQL statements** across the whole compute path —
in the success case *and* in a forced-failure case. `OhlcFetcher` holds no DB handle at all; its
only source is the injected `fetch_fn`. **No amount of `analytics.candles` backfill can affect
regime at any range.** This supersedes the "not computable / backfill MOOT" framing.

**⭐ The April state file was a MISSING-HANDLE run, not a data shortage.** `_make_sr_fetch_fn`
(`main.py:424-425`) returns **`[]` rather than raising** when the kite handle is None, so a
no-token run yields 0 bars → the exact note `insufficient_index_daily_candles`. A control run
with `market_kite=None` reproduced the April file's note byte-for-byte. Corroborating: the file
exists **only on the PC** (the VM has no `data_store/regime/` directory at all), and the PC's
token is stale (21-Jun). ⚠️ **The persisted note cannot distinguish "Kite served <201 bars" from
"there was no Kite handle" — only the log line carries the count (`0 < 201`).** That
observability gap is queued, not fixed. See [[feedback-verify-the-finding-premise]].

**Also settled:** the standing "the NIFTY index token must be VM-verified" item — `config/system_config.yaml`
says *"VERIFY live historical access on the VM before flipping enabled"*. **Now verified on the VM.**

**What this does NOT unblock.** #07 still needs ~2.2 months of FORWARD within-cell data, and the
live consumer is unbuilt (regime is emitted in the V3 **shadow** chain and gates nothing). The #10
coupling stands: admission is first-come-first-served, so a score preference the throttle ignores
is decorative. The gate moved from **"cannot compute"** to **"needs forward data"** — a different
and much smaller problem. No recommendation is made here.

Report: `docs/audit/regime_computability_verification_20jul2026.md`.
Related: [[regime-thesis-validation-18jul]] [[regime-phase1-investigation-18jul]] [[regime-minscore-control-18jul]]
