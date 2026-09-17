---
name: fix_181_complete
description: "FIX-181 — 6 post-Live-Day-1 hardening fixes (tick rounding, marketable LIMIT exits, position cap off-by-one, orphan-fill, daily-trade count, holiday API guard); deployed 16-Jun-2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: 768ee318-85d1-4db9-a514-076df3b7c129
---

FIX-181 (16-Jun-2026, post-market). Commit 7f93c2f. 6 fixes, 3010 tests pass, deployed to VM (hashes verified). Test file: tests/unit/test_fix181.py (44 tests). Builds on [[fix_180_complete]] and [[live_day1_zombie_remediation]].

1. **Tick-size rounding** — `orders/price_math.round_to_tick(price, tick, mode)` + tick-aware `calc_sl_limit_price` (SELL→down, BUY→up). Authoritative net: `zerodha_adapter._snap_order_to_tick` snaps EVERY LIMIT/SL price+trigger to a valid tick in `place_order` (both paper+live), wired via `set_instrument_cache` in main.py. `modify_order` has no symbol so can't snap → `breakeven_manager` threads instrument_cache itself; `smart_tgt` already rounded. GICRE incident: limit `round(,2)` produced off-tick prices Zerodha rejects.
2. **Marketable LIMIT emergency exits** — emergency/kill/sl-breach exits use LIMIT at LTP±buffer (`marketable_limit_price`), MARKET fallback if no LTP. Config `capital.emergency_exit_buffer_pct=0.01`. Sites: `order_placer._emergency_market_exit`, `kill_switch` (both place_order calls + `_marketable_exit_params`), `sl_breach_monitor._fire_emergency_exit`. Tags via `truncate_tag_for_broker` (≤16, safely ≤20).
3. **Position cap off-by-one** — `risk_engine` OPEN_POSITIONS `>=`→`>`. The candidate is PRE-incremented into `processor_in_flight_count` (signal_processor bumps `_in_flight_count` before approve), so active_total==max_open means candidate+(max-1) existing = ALLOW. Old `>=` made max=3 only ever hold 2. Tests that call approve() directly must pass `processor_in_flight_count=1` to model the candidate.
4. **Orphan-fill reconciliation** — LAYER A: `kill_switch._exit_all_trades_indestructible` sweeps broker positions (get_positions) and flattens any non-zero position with no local OPEN/PARTIAL/PENDING_FILL trade (removed the empty-open_trades early-return so the sweep always runs). LAYER B: reconciler CHECK2 — a broker position matching a local PENDING_FILL/PENDING trade (`get_trades_by_status_and_symbol`) is flattened on HARD_KILL (`_check2_inflight_orphan`/`_flatten_broker_position`), else left for the normal fill path (no destructive action on transient state). `create_trade` already writes PENDING_FILL (no normalization needed).
5. **Daily-trade count** — `state_store.count_trades_today` now filters `status IN _EXECUTED_TRADE_STATUSES` (PENDING_FILL/OPEN/PARTIAL/EXITING/CLOSED/CLOSED_MANUAL); FAILED/CANCELLED no longer burn the daily quota.
6. **Holiday-aware broker API guard** — `core.market_windows.is_broker_api_available(dt, holidays)` prepones the Fri-17:30 cutoff to Thursday 17:30 when Friday is an NSE holiday (T-1); Friday holiday itself returns False. Cron callers (reconcile_pnl/positions, fetch_daily_candles, premarket_healthcheck) pass `utils.holiday_guard.current_holiday_set(config_dir)` (best-effort, empty on error).
