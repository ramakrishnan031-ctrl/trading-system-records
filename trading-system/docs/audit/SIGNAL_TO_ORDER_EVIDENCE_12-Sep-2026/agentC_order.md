# Agent C: order placement trace, `place()` to ENTRY-at-broker, @970aabf

Read-only source trace. All `path:line` citations are **@970aabf** (the `src970` extract), unless marked **LIB**.
LIB = third-party library source read from the local PC install (`C:/Users/rama/AppData/Roaming/Python/Python314/site-packages/`):
kiteconnect **5.1.0** (`__version__.py`) and requests **2.33.1**. Both match the pins in `requirements.txt:8-9 @970aabf`. The VM install was not inspected, so any conclusion that depends on LIB is labelled **INFERENCE**.
Nothing was executed, and no DB, log, VM or broker was consulted. Everything below is static reading. There are no timing measurements; timing values are configured values only.

Provenance labels: **SRC** = read directly at 970aabf · **LIB** = read in library source · **INFERENCE** = derived, not read.

---

## 0. One-paragraph picture

`signal_processor._admit_and_place` calls `OrderPlacer.place(...)` (keyword-only, returns `None`).
`place()` runs these steps in order, and several of them can reject:
- an R:R gate;
- a constant protocol choice (`LIMIT_TRIPLE`);
- trade-row creation (`PENDING_FILL`, then `PENDING`);
- a kill-switch check;
- an EOD-cutoff check;
- a quote-based slippage guard;
- a quote-based price-drift top-up, which can *replace* the entry price with the LTP;
- a dormant liquidity check;
- a second kill-switch check, then `FullEntryEngine.execute`.

`execute` goes to `LimitTripleProtocol.execute`, which places **one ENTRY LIMIT order only**, through `ZerodhaAdapter.place_order`. The adapter then:
- validates the order;
- snaps price to tick (nearest, ROUND_HALF_UP);
- resolves product (INTRADAY→MIS, DELIVERY→CNC);
- acquires an `order` rate-limit token (8/s, burst 8);
- calls `kite.place_order(variety="regular", exchange="NSE", ..., order_type="LIMIT", price=<snapped>, tag=trade_id[:16], market_protection=None)`.

Success means "kite returned an order_id". Broker acceptance is not verified at this point.
`place()` then persists the ENTRY `orders` row (price NULL) and registers the fill-map entry and the order monitor.
SL and TGT are **not** placed in `place()`. They are placed later, on the ENTRY fill event:
- **MIS:** SL stop-limit, then TGT LIMIT, at the filled qty.
- **CNC:** one OCO GTT.

---

## 1. Call site: `signal_processor.py:1446-1460 @970aabf` (SRC)

```python
self._placer.place(
    symbol=symbol, side=side, qty=sizing.qty,
    entry_price=entry_price,  # FIX-067/M-S1: fresh-re-anchored (or stale fallback)
    sl_price=sl_price, intent=strategy_obj.intent, signal_id=signal_id,
    reservation_id=ac.reservation_id, strategy=strategy_name, tgt_price=tgt_price,
    signal_trigger_price=trigger_price,  # FIX-128: for slippage guard
    sizing_breakdown=sizing.breakdown,
    tgt_risk_reward=getattr(strategy_obj, "tgt_risk_reward", None),
)
```

| arg | value / provenance (SRC) |
|---|---|
| `symbol` | webhook signal symbol (`signal_processor.py:879-886`) |
| `side` | `"BUY" if _dir in ("LONG","BUY") else "SELL"` from `strategy_obj.direction` (`:1034-1035`) |
| `qty` | `sizing.qty` from `PositionSizer.calculate` (`:1112-1121`); int (`position_sizer.py:95, :639`) |
| `entry_price` | `_derive_prices` (`:1748-1895`): LIMIT → `trigger*(1-offset)` LONG / `trigger*(1+offset)` SHORT (`:1779-1784`). Offset is 0.001 for all intraday YAMLs and 0.002 for the 3 DELIVERY YAMLs. For `pullback_wait_enabled: false` strategies the base is re-anchored to a live LTP from `broker_adapter.get_quote` (`:1082-1106`); pullback strategies keep the webhook trigger. **Not tick-rounded** anywhere in the processor. |
| `sl_price` | FIXED_PCT `entry*(1∓sl_pct)` (`:1836-1839`), clamped into `[sl_min_pct, sl_max_pct]` (`:1848-1871`), plus the gap buffer only 09:15-09:30 (`:1877-1893`). Unrounded. |
| `intent` | `strategy_obj.intent`: `INTRADAY` (13 YAMLs) / `DELIVERY` (`positional_*`, 3 YAMLs) |
| `signal_id`, `reservation_id` | pipeline signal id; `fm.reserve(...)` id taken inside `portfolio_lock` (`:1328-1340`) |
| `strategy` | strategy name (`:939-942`) |
| `tgt_price` | `_derive_target` (`:1901-1953`): RISK_REWARD `entry ± |entry-sl|*tgt_risk_reward` (`:1930-1936`). All enabled YAMLs: `tgt_method: RISK_REWARD`, `tgt_risk_reward: 1.5`. The BL-16 guard rejects if `|tgt-entry|/entry < tgt_min_pct` (0.003) (`:1945-1951`). |
| `signal_trigger_price` | original webhook `trigger_price` (NOT the re-anchored LTP) |
| `sizing_breakdown` | `sizing.breakdown` (DB audit columns only) |
| `tgt_risk_reward` | `strategy_obj.tgt_risk_reward` = 1.5 in every enabled YAML (schema default 2.0, `strategies/schema.py:95`) |
| not passed | `release_ltp` (default None), `entry_order_type` (default `"LIMIT"`) |

What the processor does with the outcome: `place()` returns `None`, so success means "no exception".
- **On return (success):** `ac.reservation_id=None; ac.placed=True` (`:1461-1463`), then signal status `PROCESSED` (`:1543`).
- **`BrokerTimeoutError`:** signal `TIMEOUT`; the reservation is handed to recovery and not released (`:1464-1484`).
- **`BrokerRateLimitError`:** re-queued up to 3 times (`:1486-1532`).
- **any other exception:** re-raised (`:1533-1538`), then the outer handler marks the signal `PLACEMENT_FAILED` and calls `fm.release(...)` (`:1233-1246`). `release` is idempotent (`fund_manager.py:651-653`).

Two other `place(` call sites exist and are dormant:
- **Gate path** (`:2251-2266`, passes `release_ltp`): nothing calls `EntryGate.add()`. The only hit is the docstring example `screening/entry_gate.py:103`.
- **Retest path** (`:2553-2562`, `entry_order_type="MARKET"`): `sr_detector.wait_for_retest_enabled: false` (`system_config.yaml:529`).

---

## 2. Inside `OrderPlacer.place()`: `orders/order_placer.py:871-1763 @970aabf`, in execution order

Signature (`:871-889`, SRC): keyword-only.
- Parameters: `symbol, side, qty, entry_price, sl_price, intent, signal_id, reservation_id, strategy="", tgt_price=None, release_ltp=None, signal_trigger_price=None, sizing_breakdown=None, tgt_risk_reward=None, entry_order_type="LIMIT"`.
- Returns `None`.

Construction (`main.py:3061-3088`, SRC): the following are **not passed**, so constructor defaults apply:
- `rr_ratio` → 2.0;
- `default_order_protocol` → `"LIMIT_TRIPLE"`;
- `liquidity_check_enabled` → False;
- `liquidity_max_spread_pct` → 0.5;
- `liquidity_min_depth_qty` → 500;
- `price_drift_threshold` → 0.005;
- `breakeven_manager` → None.

### P1. Effect telemetry: `:904`
`self._fx_place.inc()`. It counts dispatch. It cannot reject and does not change price or qty.

### P2. FIX-025 gate-release slippage protection: `:905-926` (DORMANT on this path)
Runs only `if release_ltp is not None`. BUY: `min(entry_price + buffer, release_ltp)`; SELL: `max(entry_price - buffer, release_ltp)`. The buffer is `entry_gate.slippage_buffer` = 2.0.
The processor's main path passes no `release_ltp`, so this never runs there.

### P3. Tick snapping, as a comment only: `:928-931`
"entry/SL/TGT tick-snapping moved to the SINGLE adapter chokepoint (zerodha_adapter._snap_order_to_tick ...)". `place()` does no rounding.

### P4. Target: `:933-935`
`if tgt_price is None: tgt_price = self._compute_tgt(side, entry_price, sl_price)`. `_compute_tgt` uses `self._rr_ratio` (2.0) (`:4387-4389`).
The processor always passes `tgt_price`, so **OP3 `_compute_tgt` is dormant** on this path.

### P5. R:R gate (FIX-136): `:937-958` (LIVE code; see §7)
```python
if self._min_effective_rr > 0 and entry_price != sl_price:
    sl_dist = abs(entry_price - sl_price)
    reward_dist = tgt_price - entry_price  (BUY) | entry_price - tgt_price (SELL)
    effective_rr = reward_dist / sl_dist if sl_dist > 0 else 0.0
    if effective_rr < self._min_effective_rr:
        raise OrderRejectedError(f"RR_GATE_FAILED: effective R:R={effective_rr:.2f} < min={self._min_effective_rr}", trade_id="", ...)
```
- `min_effective_rr` = `entry_gate.min_effective_rr` = **1.0** (`system_config.yaml:659`, wired `main.py:3083`).
- The gate raises **before** any trade row exists. It does not call `_handle_placement_failure`, so the placer does not release the reservation; the processor's outer handler releases it (`signal_processor.py:1239-1243`).

### P6. Protocol selection: `:960-961`
`order_protocol = self._default_protocol`. This is the constructor default `"LIMIT_TRIPLE"` (`:572`; not overridden, `main.py:3061-3087`).
- Nothing per-strategy, per-intent or per-product is consulted.
- The strategy YAML key `order_protocol` is validated at `strategies/schema.py:60, :161-168` and displayed at `ops_dashboard/backend/readers/config_reader.py:79`. No order-path code reads it; grep for `strategy*.order_protocol` finds 0 hits.
- The YAMLs themselves: 13 intraday declare `"CO_PLUS_TGT"`, the 3 DELIVERY declare `"LIMIT_TRIPLE"`. All are ignored.

### P7. Trade fields: `:963-973`
- `direction = "LONG" if side == "BUY" else "SHORT"`.
- `risk_amount = abs(entry_price - sl_price) * qty`.
- `margin_reserved = self._fm.required_margin(qty=qty, price=entry_price, intent=intent)` = `qty*price/leverage` (`fund_manager.py:248-268`). Leverage comes from `capital.leverage_map`: INTRADAY 5.0, DELIVERY 1.0 (`system_config.yaml:208-211`).

This is DB metadata only; the actual reservation was made upstream.

### P8. Slippage-tolerance resolution (Phase 3a): `:975-991`
Runs when `slippage_control.enabled` and `mode == "sl_fraction"`. Both are true (`system_config.yaml:669-670`).
- Band price = `signal_trigger_price`, fed through `get_price_band(..., slippage_bands)`.
- `resolve_slippage_fraction` (`:251-276`): Symbol > Strategy > Band > Global. All override maps are empty (`system_config.yaml:697-706`), so it returns **(0.22, "global")**.
- The result is recorded on the trade row (`tolerance_fraction_used`, `tolerance_source`).

### P9. DB write 1: trade row: `:993-1015`, which calls `order_manager.py:175-270`
`INSERT INTO trades (...)` with these values:

| column | value |
|---|---|
| `trade_id` | `new_trade_id()` = `"trd_"+uuid4.hex` |
| `signal_id, symbol, direction, strategy` | as above |
| `sector` | `_resolve_trade_sector` (instrument_cache, `"UNKNOWN"` on miss, `:710-728`) |
| `qty_planned` | `qty`; `qty_filled`: 0 |
| `entry_target_price` | `entry_price` at this point (pre-drift, pre-snap); `entry_actual_price`: NULL |
| `sl_initial`, `tgt_initial` | `sl_price`, `tgt_price` |
| `margin_reserved`, `risk_amount` | as P7 |
| status | **`'PENDING_FILL'`** |
| `entry_mode` | `'FULL'` |
| `order_protocol` | `'LIMIT_TRIPLE'` |
| `recovered_flag` | 0 |
| `reservation_id, mode` | as passed |
| `tolerance_fraction_used/source` | 0.22 / "global" |
| sizing-audit columns | from `sizing_breakdown` |
| `tgt_risk_reward_applied` | `tgt_risk_reward` (1.5) |

(`order_manager.py:212-261`.) There is **no idempotency or dedup**: every call mints a fresh `trade_id`, and no existing row is checked for the `signal_id`.

### P10. DB write 2: link signal: `:1027-1037`
`UPDATE signals SET trade_id=? WHERE signal_id=?` (`order_manager.py:718-724`).
On exception: `_handle_placement_failure(..., broker_order_ids=())` (trade FAILED + release), then `raise OrderRejectedError("link_signal_trade failed: ...")`.

### P11. Kill switch OP-LM1: `:1049-1058`
`if self._kill_switch.is_active("entry")`: `_handle_placement_failure` (FAILED + release), then `raise OrderRejectedError("kill_switch_active_last_mile")`.

### P12. DB write 3: status PENDING: `:1060-1071`
`self._om.update_trade_status(trade_id, "PENDING")` (FIX-071). A failure here is logged and placement continues.
Nothing in `place()` sets the status back to `PENDING_FILL`. The next writers are the fill handler (`OPEN`, `order_manager.py:410-420`) or a failure path.

### P13. EOD entry cutoff (FIX-073): `:1073-1097`
`if self._market_windows.is_past_eod_entry_cutoff(now_ist())`: `now.time() >= eod_entry_cutoff`, or it is a holiday (`core/market_windows.py:177-190`).
The cutoff is `trading_hours.eod_entry_cutoff` = **15:15** (`system_config.yaml:48`). On breach: `_handle_placement_failure(final_status="REJECTED")`, then `raise OrderRejectedError("order rejected: past EOD entry cutoff 15:15")`.

### P14. Slippage guard (FIX-128): `:1099-1192`
Runs if `signal_trigger_price > 0` (always true on the main path).
- `_slip_ltp = release_ltp`, or else `self._fetch_ltp(symbol)` (`:4036-4064`). `_fetch_ltp` calls `adapter.get_quote_raw(["NSE:SYM"])`, which uses the `quote` bucket (3/s) and kite `quote`. In **PAPER** it returns `{}` (`zerodha_adapter.py:1816-1817`). Any error returns `None`.
- **If LTP is None the guard is skipped** (`if _slip_ltp is not None:`); this is fail-open.
- `_slip_rs = abs(_slip_ltp - signal_trigger_price)` (absolute, so both directions count); `_slip_pct = _slip_rs / trigger * 100`.
- Config has `slippage_control.enabled: true`, so `_slippage_decision` (`:364-390`) applies. With `_compute_slippage_tolerance` (`:325-361`):
  `tol = min(min(|trigger - sl_price| * 0.22, absolute_cap_rs=5.00), hard_max_slippage_rs=10.0)`.
- Abort if `slip_rs > tol`, **or** (since `also_apply_pct_check: true`) if `slip_pct > max_entry_slippage_pct=1.0`.
- On abort: WARNING Telegram, `_handle_placement_failure(final_status="REJECTED", suppress_alert=True)`, then `raise OrderRejectedError("slippage_exceeded: trigger=.. ltp=.. | ...")`.
- An INFO log `order_placer.entry_slippage_observed` is always emitted when the LTP was obtained.

### P15. Price-drift top-up (FIX-075): `:1194-1289`, which can CHANGE THE ENTRY PRICE
Runs `if self._adapter is not None` (always true). It makes a **second** `_fetch_ltp` call.
```python
drift_pct = abs(current_ltp - original_entry_price) / original_entry_price
if drift_pct > drift_threshold:          # self._price_drift_threshold = 0.005 (ctor default)
    additional_margin = required_margin(qty, current_ltp, intent) - required_margin(qty, original_entry_price, intent)
    if additional_margin > 0:            # i.e. current_ltp > entry_price (BUY or SELL)
        top_up_result = self._fm.top_up_reservation(...)
        if not top_up_result.success: ... final_status="REJECTED_PRICE_DRIFT"; raise drift_exc
        entry_price = current_ltp        # raw LTP; snapped later by the adapter
```
- If the LTP is more than 0.5% **above** the computed entry and the top-up succeeds, the ENTRY LIMIT is placed at the LTP. This applies to both BUY and SELL. SL and TGT are not recomputed. `trades.entry_target_price` keeps the pre-drift value.
- If the LTP is below the entry (additional_margin ≤ 0), nothing changes.
- A top-up ledger row `TOP_UP` is written (`fund_manager.py:838-849`). `top_up_reservation` raises `ValueError` if the reservation is unknown; `except Exception` catches that, logs a WARNING, and placement proceeds with the original price.
- Failure of the quote or drift check is fail-open (`:1277-1289`). Only `OrderRejectedError` re-raises (`:1274-1276`).
- INFERENCE: the P14 guard runs first and is measured against the trigger, while P15 is measured against the entry. With intraday offset 0.001 and sl_pct ≥ 0.8%, a BUY LTP that is +0.4% over the trigger usually already exceeds `0.22*SLdist`. For DELIVERY (offset 0.002, sl_pct 0.02), roughly the +0.30% to +0.48% band can pass P14 and trigger P15. This is arithmetic, not measured.

### P16. Liquidity check (FIX-134): `:1291-1305` (DORMANT)
Runs `if self._mode == "LIVE" and self._adapter is not None`, then `_check_liquidity` (`:4066-4151`). `if not self._liquidity_check_enabled: return True, ""` (`:4075-4076`) short-circuits.
`_liquidity_check_enabled` = ctor default **False**, because `main.py:3061-3087` does not pass it. The config `entry_gate.liquidity_check_enabled: true` has no effect.

### P17. Retry loop and pre-submit kill switch: `:1307-1476`
`max_429_retries = self._rl_backoff.max_placer_retries` = **3** (`broker_limits.yaml:38`), so there are up to **4** attempts (`range(max+1)`).
Each iteration first runs **A-3** (`:1335-1343`): `if kill_switch.is_active("entry")`: `_handle_placement_failure` (FAILED + release), then `raise OrderRejectedError("kill_switch_active_last_mile_presubmit")`.
Then `self._engine.execute(symbol, side, qty, entry_price, sl_price, tgt_price, intent, trade_id, order_protocol, entry_order_type)` (`:1345-1356`).
Exception handling (quoted structure):

| caught | action |
|---|---|
| `OrderRejectedError` with `context["kite_status_code"] == 16388`, first time | `adapter.invalidate_margin_cache(...)`, then `continue` (`:1361-1377`) |
| same, second 16388 | `final_status="REJECTED"`, then raise (`:1378-1396`) |
| other `OrderRejectedError` | `_handle_placement_failure` (FAILED + release), then raise (`:1397-1402`) |
| `BrokerRateLimit429Error` | retry (no sleep; the adapter already penalized the bucket); on the last attempt: FAILED + release + raise (`:1403-1432`) |
| `BrokerTimeoutError` | **no** release, `trades.status='UNKNOWN_IN_FLIGHT'`, `_timeout_recovery_queue[trade_id]={signal_id,reservation_id,symbol,added_at}`, then raise (`:1433-1465`) |
| any other `BrokerError` | FAILED + release, then raise (`:1466-1475`) |
| non-`BrokerError` (e.g. `ValueError` from adapter validation, `RateLimitAbortedError`) | **not caught**: it propagates with the trade left `PENDING` and the reservation not released by the placer. The processor outer handler releases it. |

`result is None` guard (`:1492-1501`): produces `BrokerError("...16388 margin retry starved...")` plus FAILED + release. It is reachable only through the 16388 branch.

### P18. FullEntryEngine router: `orders/full_entry_engine.py:72-119`
`protocol = order_protocol or self._default_protocol`. `"LIMIT_TRIPLE"` selects `self._limit`; `"CO_PLUS_TGT"` selects `self._co`; anything else raises `ValueError` (`:93-103`).
It logs `full_entry_engine.execute` and calls `selected.execute(..., tag=tag, entry_order_type=...)`. `tag` is `""` because `place()` passes none.

### P19. `LimitTripleProtocol.execute`: `orders/order_protocol_limit.py:171-248`, which places ENTRY only
```python
order_tag = truncate_tag_for_broker(tag or trade_id)          # trade_id[:16] (core/ids.py:124)
_entry_order_price = 0.0 if entry_order_type == "MARKET" else entry_price
entry_placed = self._adapter.place_order(symbol=symbol, side=side, qty=qty,
    price=_entry_order_price, order_type=entry_order_type, intent=intent, tag=order_tag)
```
- `except BrokerError: raise` (`:220-221`).
- OP-LM3: `if not entry_placed.broker_order_id: raise OrderRejectedError("adapter returned empty broker_order_id for ENTRY order")` (`:223-228`).
- Returns `EntryResult(success=True, entry_broker_order_id, entry_internal_id, sl_*="", tgt_*="", order_protocol="LIMIT_TRIPLE")` (`:239-248`).
- `sl_price` and `tgt_price` are accepted but **not used** (docstring `:192-194`).
- Of the returned `PlacedOrder` it reads only `.broker_order_id` and `.internal_order_id`. The snapped `price`, `product`, `status`, `ts` and so on are discarded.

### P20. `ZerodhaAdapter.place_order`: `broker/zerodha_adapter.py:494-689`, which is the broker call (§4)

### P21. After `execute` returns: `order_placer.py:1503-1731`
- **`result.success` False** (`:1503-1521`): only the CO protocol can return False. The placer cancels the returned ids, marks FAILED, releases, and raises `BrokerError`. **Dormant** for LIMIT_TRIPLE, since `execute` returns success=True or raises.
- **DB write 4, the orders row** (`:1523-1561`, via `_persist_entry_orders` `:4637-4706` and `order_manager.insert_orders_atomic` `:339-391`):
  ```python
  OrderInsertSpec(broker_order_id=result.entry_broker_order_id, leg="ENTRY", transaction_type=side,
                  order_type="SL" if result.order_protocol == "CO_PLUS_TGT" else "LIMIT",
                  product=product,  # self._product_resolver.resolve(intent): MIS / CNC
                  variety="regular", qty_requested=qty)   # price / trigger_price NOT passed -> 0.0
  ```
  The INSERT writes `status='PENDING'`, `qty_filled=0`, and `price`/`trigger_price` → **NULL** (`price if price > 0 else None`, `order_manager.py:387-388`).
  On exception: cancel the entry, mark FAILED, release, and fire `kill_switch.hard_kill(... "persist_entry_orders failed after broker success")` (`:1539-1561`).
  The SL/TGT specs (`:4680-4701`) are never built for LIMIT_TRIPLE because their ids are empty.
- **Fill-map and monitor** (`:1574-1731`): the `_FillEntry(leg="ENTRY", side, sl_price, tgt_price, intent, tgt_risk_reward=(tgt_risk_reward or 0.0), ...)` is inserted **before** `order_monitor.track(internal_order_id, broker_order_id, symbol, side, qty, expected_price=entry_price, placed_at=now, leg="ENTRY", tgt_price, sl_price)`. `placed_at` is set after the broker call returns (`:1575`).
  The SL and TGT track branches (`:1623-1675`) are skipped for LIMIT_TRIPLE because their ids are empty.
  If `track()` raises: pop the entry, untrack, cancel, mark FAILED, release, and raise, with no hard_kill (`:1676-1731`).
- **Log and alert** (`:1733-1763`): `order_placer.place_complete`, then a Telegram "✅ ORDER PLACED" with the body from `_format_order_placed_body` (`:843-869`).
- Returns `None`.

---

## 3. The ENTRY order exactly as sent (LIVE): `zerodha_adapter.py:639-654` (SRC)

```python
kite_order_id = self._kite.place_order(
    variety=variety,                                   # "regular" (param default :504; protocol passes none)
    exchange="NSE",
    tradingsymbol=symbol,
    transaction_type=_KITE_TRANSACTION[side],          # "BUY" | "SELL"
    quantity=qty,
    product=broker_code,                               # ProductResolver: INTRADAY->"MIS", DELIVERY->"CNC"
    order_type=_KITE_ORDER_TYPES[order_type],          # "LIMIT"
    price=price if order_type in ("LIMIT", "SL") else None,   # snapped entry price
    trigger_price=trigger_price if trigger_price > 0 else None,  # 0.0 -> None -> omitted
    tag=tag,                                           # trade_id[:16] (truncated in protocol AND :636-637)
    market_protection=market_protection,               # None -> omitted
)
```

| field | value | source |
|---|---|---|
| order type | `LIMIT` (MARKET only on the dormant retest path) | `order_protocol_limit.py:210-216` |
| price | `_round_nearest_to_tick(entry_price, tick)`: `(Decimal(str(v))/Decimal(str(tick))).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * tick` | `zerodha_adapter.py:1448-1452`, `broker/slippage_engine.py:175-186` |
| rounding direction | **same for BUY and SELL**: nearest, ties away from zero (up). Directional rounding applies only to `order_type=="SL"` (`:1438-1447`). | SRC |
| tick | `instrument_cache.tick_size(symbol)` (from `config/instruments.csv`, `main.py:2441, :2522`); on miss or ≤0 it falls back to `DEFAULT_TICK = 0.05` with a warn-once `snap_to_tick.missing_tick_size` | `zerodha_adapter.py:1383-1407`, `price_math.py:27` |
| price offset inside placer | none on the main path; the only substitution is P15 (entry = raw LTP) | SRC |
| quantity | `sizing.qty`, validated `isinstance(qty,int) and qty > 0` | `:2097-2100` |
| exchange | hardcoded `"NSE"` | `:641` |
| product | `MIS` / `CNC` via `product_map` (`system_config.yaml:157-162`) | `:587` |
| variety | `"regular"` | `:504` |
| validity | **not passed**; kiteconnect strips None (LIB `connect.py:361-366`). INFERENCE: broker default DAY | LIB |
| disclosed_quantity, iceberg, validity_ttl, auction_number | not passed, so omitted | LIB `connect.py:339-356` |
| market_protection | param exists (`:505`), bounds-checked `[0.1, 10.0]` if non-None (`:2116-2137`). The entry path passes nothing, so it is `None` and omitted. The only caller passing it is `orders/mis_autosquareoff.py:877`. | SRC |
| tag | `trd_` + 12 hex chars | `core/ids.py:104-124` |

---

## 4. The broker call: `ZerodhaAdapter.place_order` `:494-689` (SRC unless marked)

Order of operations:
1. **Validate** (`:560-562` → `_validate_place_order` `:2080-2137`). Raises **`ValueError`** for: an empty symbol; a side not BUY/SELL; qty not a positive int; an order_type outside {MARKET, LIMIT, SL, SL-M}; `price <= 0` for LIMIT/SL; `trigger <= 0` for SL/SL-M; a bad market_protection. This happens before the rate limiter or OSM.
2. **Tick snap** (`:567-569`), in both paper and live.
3. **Product coercion** (`:578-584`): only if `force_intraday_only` (config **false**, `system_config.yaml:142`), so it does nothing today.
4. **Resolve product** (`:587`): `ProductResolver.resolve(intent,"zerodha")` (`broker/product_resolver.py:95-138`). Raises `ValueError` for an unknown intent and `ProductNotSupportedError` (a BrokerError) for an empty mapping (BRACKET_ORDER="").
5. **CNC lock** (`:593-602`): `if broker_code == "CNC" and not self._delivery_enabled: raise OrderRejectedError("CNC orders are disabled ...")`. Config `delivery_enabled: true` (`system_config.yaml:155`), so this passes.
6. **OSM** (`:605-606`): `internal_id = new_order_id()`, registered `PENDING`.
7. **PAPER** branch (`:608-619`): `_paper_place_order` gives a fake id `PAPER_<12hex>` plus a synth-fill thread. There is no rate limit and no kite call.
8. **Rate limit** (`:622`): `self._rl.acquire("order")`. This is outside the `try`.
   - Bucket config: `order: burst 8, rate_per_sec 8` (`broker_limits.yaml:9-11`).
   - `acquire` blocks, polling every ≤0.1 s, up to **max_wait_sec = 30.0**. That is the ctor default; `main.py:2348` does not pass it.
   - On timeout it raises `BrokerRateLimitError` (`rate_limiter.py:213-223`); if the shutdown event is set it raises `RateLimitAbortedError` (`:236-244`).
   - Either way the OSM entry stays `PENDING`, because the exception is raised outside the `try`.
9. **Kite call** (`:638-654`, §3). The kiteconnect client was built with `timeout = broker_limits.timeouts.read_sec` = **10 s** (`main.py:381-390`, `broker_limits.yaml:33`). kiteconnect passes it as the single `requests` timeout (LIB `connect.py:210, :923`). `HTTPAdapter(pool_connections=1, pool_maxsize=50)` is mounted with default `max_retries`, which is `Retry(0, read=False)`, so there are **no HTTP retries** (LIB requests `adapters.py:73, :186-187`). The adapter itself has no retry either (ZA11).
10. **On exception** (`:655-661`): OSM goes to `FAILED`, then `raise self._translate_broker_exception(exc, context, "place_order")`.
    - HTTP **429** (`getattr(exc,"code")==429`, `:2006-2008`): `delay = min(0.2*2**n, 5.0) ± 0.05` (`:2010-2028`; `broker_limits.yaml:35-40`), then `rate_limiter.penalize("order", delay)`, then `BrokerRateLimit429Error` (`:2052-2077`).
    - Otherwise `_translate_kite_exception` (`:290-339`):
      - `kex.TokenException` → `BrokerAuthError`;
      - `kex.NetworkException` → **`BrokerTimeoutError`**;
      - `kex.InputException`/`kex.OrderException` → `OrderRejectedError(rejection_reason=str(exc), kite_status_code=exc.code)`;
      - `kex.PermissionException` → `BrokerAuthError`;
      - `TimeoutError`/`socket.timeout` → `BrokerTimeoutError`;
      - `kex.GeneralException` → `BrokerError`;
      - **anything else** → `BrokerError("Unexpected error from Zerodha: ...")`.
11. **On success** (`:663-689`): reset the 429 counter, move OSM to `SUBMITTED`, return the frozen `PlacedOrder`:

    | field | value |
    |---|---|
    | `internal_order_id` | the `internal_id` from step 6 |
    | `broker_order_id` | `str(kite_order_id)` |
    | `symbol, side, qty` | as sent |
    | `price` | the snapped price |
    | `order_type` | as sent |
    | `product` | `broker_code` |
    | `status` | hardcoded `"SUBMITTED"` |
    | `ts` | `now_ist()` |
    | `trigger_price` | as sent |
    | `variety` | as sent |

    **There is no `success` field.** INFO logs: `place_order call_start` (without the price) and `place_order call_end` (duration, broker_order_id).

**Success is assumed, not verified.** A returned order_id counts as placed. The protocol only checks that it is non-empty (`order_protocol_limit.py:224`).
Broker-side acceptance or rejection (for example an RMS REJECTED after acceptance) is learned only when `OrderMonitor` polls `get_order_history` every `poll_interval_sec: 2` (`system_config.yaml:193`). A REJECTED status becomes `FAILED` (`order_monitor.py:782-783`), and then the placer's zero-fill path releases the reservation and marks the trade FAILED (`order_placer.py:1963-2015`).

**What is recorded at placement time:**
- `trades` (P9, P12);
- `signals.trade_id` (P10);
- `orders` ENTRY row (P21), with **price NULL**;
- `fm_ledger` TOP_UP only if P15 fired;
- logs.

**`order_execution_log` is not written at placement.** It is written only on `OrderFilled` (async subscriber, `orders/slippage_recorder.py:113-152`).
The exact wire price is not persisted anywhere: `orders.price` is NULL and `trades.entry_target_price` is pre-drift and pre-snap. It is logged only at DEBUG (`adapter.snap_to_tick`, only when the snap changed the value).

**What the placer returns to the processor:** `None`.

INFERENCE (LIB): kiteconnect re-raises every `requests` exception unchanged (`connect.py:914-927`). requests wraps any `OSError`/socket timeout as `ConnectionError` and read timeouts as `ReadTimeout`; both are `RequestException(IOError)` subclasses, not `TimeoutError` (`adapters.py:659-660, :691`; `exceptions.py:13,72,88`). So a **client-side 10 s HTTP timeout or connection error on `place_order` falls through to the generic `BrokerError`**, and the placer path is FAILED + reservation released + signal `PLACEMENT_FAILED`. It is not the FIX-068 UNKNOWN_IN_FLIGHT path.
The `BrokerTimeoutError` path (`order_placer.py:1433-1465`, `signal_processor.py:1464-1484`) is reachable via `kex.NetworkException`, which kiteconnect raises for a JSON `error_type` "NetworkException", default HTTP 503: "network issue between Kite and the backend OMS" (LIB `exceptions.py:75-80`).
A non-JSON or garbled response (`kex.DataException`) also becomes a generic `BrokerError`.

---

## 5. SL / TGT values: how they are carried, and when and how they are sent

**Carriage (SRC).**
- **Processor values.** `sl_price` and `tgt_price` go into the `trades` row (`sl_initial`, `tgt_initial`) and into the ENTRY `_FillEntry` (`sl_price`, `tgt_price`, `side`, `intent`, `tgt_risk_reward` = 1.5), at `order_placer.py:1590-1607`. They also go into `order_monitor.track(tgt_price, sl_price)`, which is used only for the FIX-141 pending-R:R cancel.
- **ENTRY time.** Nothing protective is placed when the ENTRY is placed (`order_protocol_limit.py:188-194, :242-246`).

**When.** Only after the ENTRY is filled:
1. `OrderMonitor` polls every 2 s. On Kite `COMPLETE` it publishes `OrderFilled` (`order_monitor.py:981-1020`).
2. The placer's synchronous subscriber (`order_placer.py:693`) calls `_handle_entry_fill` (`:2089-2171`).
3. That runs `fm.commit_to_used`, then `record_entry_fill` (trades `OPEN`), then `_place_limit_triple_exits(qty_filled=event.filled_qty, avg_fill_price=event.avg_fill_price)` (`:2156-2163`).

On the first PARTIAL for an ENTRY, the monitor cancels the remainder immediately (`order_monitor.py:910-940`). It then emits `OrderPartiallyTerminated`, and the placer places exits for the filled qty (`order_placer.py:1788-1896`). There is also a fallback at `:2023-2087`.
Exits therefore run on the monitor poll thread, inside the event handler.

**Prices at fill** (`order_placer.py:2870-2908`):
```python
actual_tgt_price = calc_tgt_price(direction=fill_entry.direction, entry_price=avg_fill_price,
    sl_price=fill_entry.sl_price, rr_ratio=self._resolve_fill_rr(fill_entry.tgt_risk_reward, ...))
# price_math.py:100-116:  risk=|entry-sl|;  LONG entry+risk*rr ; SHORT entry-risk*rr
legs = self._engine.place_deferred_exits(order_protocol="LIMIT_TRIPLE", ..., qty=qty_filled,
    sl_price=fill_entry.sl_price, tgt_price=actual_tgt_price, intent=fill_entry.intent, tag=trade_id,
    entry_fill=avg_fill_price)
```
- **SL** stays at the processor's `sl_price`, anchored to the original level.
- **TGT is recomputed from the fill** using the strategy R:R (1.5). `_resolve_fill_rr` falls back to `_rr_ratio` = 2.0, with a WARNING, only if the stored value is falsy (`:4153-4178`).
- The processor's `tgt_price` (`trades.tgt_initial`) is **not** the price sent to the broker. It is used only for logging (`theoretical_tgt`) and, before the fill, by the FIX-141 check.

### 5a. INTRADAY (MIS): the three LIMIT_TRIPLE legs
1. **ENTRY:** LIMIT, as in §3.
2. **SL:** a stop-limit, placed first (`order_protocol_limit.py:369-414`).
   - The circuit band comes from `adapter.get_quote` (`:252-268`). Then `clamp_exit_into_band` (`price_math.py:284-377`) clamps into `[lower*1.02, upper*0.98]` (`DEFAULT_CIRCUIT_MARGIN_PCT = 0.02`, tick default 0.05) and checks placeability against the fill. If the SL is on the wrong side of the fill it raises `SLUnplaceableError` (`:328-345`). If no band data is available it is fail-open.
   - `sl_limit_price = calc_sl_limit_price(exit_side, trigger_price=sl_price, offset_pct=0.005)` (`price_math.py:162-217`): SELL stop → `round_down(trigger*(1-0.005), 0.05)`; BUY stop → `round_up(trigger*(1+0.005), 0.05)`. `capital.sl_limit_offset_pct: 0.005` (`system_config.yaml:204`, wired `main.py:3021`).
   - `adapter.place_order(side=exit_side, qty=qty_filled, price=sl_limit_price, order_type="SL", intent, tag, trigger_price=sl_price)`. The adapter re-snaps the limit with the real tick (SELL down, BUY up) and the trigger to nearest (`zerodha_adapter.py:1438-1447`). The order is MIS, variety regular, with no validity or market_protection.
   - On `BrokerError`: log CRITICAL and re-raise. The caller runs `_emergency_market_exit` and then a hard kill (`order_placer.py:2909-2945`).
3. **TGT:** a LIMIT, placed second (`order_protocol_limit.py:428-525`).
   - It is placed at `actual_tgt_price`, clamped if needed, then snapped to nearest.
   - If the TGT is unplaceable, rejected, or gets an empty id, the protocol returns an **SL-only** result (FIX-190 Bug C). The placer persists and tracks the SL only and the TGT is queued for `TGTRetryManager` (`order_placer.py:2961-2975`).

Both legs persist as `orders` rows with price and trigger (`:2994-3043`), and are tracked by the monitor. SL/TGT legs are exempt from the fill timeout (`order_monitor.py:1085-1086`).

### 5b. DELIVERY (CNC)
- **Entry:** identical to MIS: the same LIMIT via `LimitTripleProtocol.execute` (the protocol is constant). The only differences are `product="CNC"` (`intent="DELIVERY"`), the processor offset of 0.002, and `sl_pct` of 0.02. It passes the CNC lock (`delivery_enabled: true`).
- **Protection:** there are no day SL/TGT legs. `FullEntryEngine.place_deferred_exits` has a gate: `if intent == "DELIVERY" and self._cnc_gtt is not None:` (`full_entry_engine.py:151-177`). The GTT placer is wired at `main.py:3027-3045`. The gate calls `CncGttPlacer.place_for_fill` **after the fill** (`orders/cnc_gtt.py:98-164`):
  ```python
  sl_trigger  = round_to_tick(sl_price,  tick, mode="nearest")          # fill_entry.sl_price
  tgt_trigger = round_to_tick(tgt_price, tick, mode="nearest")          # fill-recalc'd TGT (R:R 1.5)
  sl_limit    = calc_gtt_limit_price(exit_side, sl_trigger,  0.03,  tick)  # SELL: round_down(trig*0.97)
  tgt_limit   = calc_gtt_limit_price(exit_side, tgt_trigger, 0.005, tick)  # SELL: round_down(trig*0.995)
  ```
  - Offsets: `gtt_sl_limit_offset_pct` = 0.03 and `gtt_tgt_limit_offset_pct` = `capital.sl_limit_offset_pct` = 0.005 (`main.py:3029-3030`, `system_config.yaml:204-205`).
  - The tick comes from `broker_adapter._resolve_tick`.
  - A fresh LTP is mandatory (`BrokerError` if missing, `:236-248`).
  - C8 check: `sl_trigger < ltp < tgt_trigger`, and each trigger must be ≥ 0.25% from the LTP; otherwise `BrokerError` (`:250-262`).
  - Then `adapter.place_gtt` (`zerodha_adapter.py:702-754`): `rate_limiter.acquire("order")`, then `kite.place_gtt(trigger_type=GTT_TYPE_OCO, tradingsymbol, exchange="NSE", trigger_values=[sl_trigger, tgt_trigger], last_price, orders=[{SELL,qty,LIMIT,CNC,sl_limit},{SELL,qty,LIMIT,CNC,tgt_limit}])`. The `tag` argument is accepted and unused.
  - It persists `gtt_state` (best-effort), then `_finalize_cnc_gtt` (`order_placer.py:2530-2552`).
  - The circuit-band clamp is **not** applied on this path.
  - A GTT failure is caught by the same handler (`order_placer.py:2909-2945`).

---

## 6. If the ENTRY never fills: `broker/order_monitor.py` (SRC)
- **Fill timeout** (`:1074-1126`): an ENTRY leg is not exempt. After `elapsed > fill_timeout_sec`, the monitor calls `adapter.cancel_order` while the order is Kite `OPEN`/`TRIGGER PENDING`/`SUBMITTED`. The value is **`order_monitor.fill_timeout_sec: 60`** (`system_config.yaml:194`, wired `main.py:3004`), measured from `placed_at`, which is set after the broker call (`order_placer.py:1575`).
  - Cancel succeeds: OSM `CANCELLED`, then `OrderStatusChanged`, then `order_placer._on_order_status_changed` zero-fill path: `fm.release(reservation_id, "entry_cancelled_zero_fill")` and trades status **`FAILED`** (`order_placer.py:1963-2015`).
  - Cancel fails: OSM `FAILED`, untrack, and the orphan callback.
- **Pending-R:R cancel** (FIX-141, `:1128-1207`): **`entry_gate.min_pending_rr: 1.0`** (`system_config.yaml:660`, wired `main.py:3011`). It is checked every poll while the order is OPEN. For BUY, it cancels when `(tgt_price - ltp)/(expected_price - sl_price) < 1.0`. It uses the processor's tgt/sl and a `get_quote` LTP, and is fail-open on missing data. INFERENCE: with TGT at 1.5R, a BUY entry is cancelled once the LTP rises above `entry + 0.5R` before it fills.
- **Partial fill:** the remainder is cancelled immediately and exits go on the filled qty (`:910-940`). **`circuit_breaker.partial_fill_timeout_minutes: 5`** (`system_config.yaml:739`) applies only to non-ENTRY legs (`:942-977`).
- **Force close** (`:794-867`): at **`circuit_breaker.force_close_time: "15:15"`** (`system_config.yaml:740`), all tracked ENTRY orders are cancelled once per day, then the force-close callback runs.

---

## 7. R:R inside the placer (SRC; INFERENCE where marked)
| where | what | can refuse? |
|---|---|---|
| `order_placer.py:937-958` (FIX-136) | `effective_rr = reward/risk` computed from the processor's entry/sl/tgt, compared with `min_effective_rr` = 1.0 | **Yes**: `OrderRejectedError("RR_GATE_FAILED: ...")`, before the trade row exists, giving signal `PLACEMENT_FAILED`. INFERENCE: on the main path the entry price is unchanged before this gate (P2 is dormant; P15 runs later) and every enabled YAML is `RISK_REWARD` with ratio 1.5, so `effective_rr` is 1.5 and the gate cannot fire with the current config. It skips when `entry_price == sl_price`. |
| `:933-935` / `:4387-4389` (OP3) | `_compute_tgt` with `_rr_ratio` = 2.0 | No. It is dormant because `tgt_price` is always supplied. |
| `:1014` | `trades.tgt_risk_reward_applied = tgt_risk_reward` (1.5) | No; it is recorded only. |
| `:1606`, `:2872-2879`, `:4153-4178` | fill-time TGT = fill ± risk × strategy R:R (fallback 2.0) | No; it is a recalculation. |
| outside the placer: `order_monitor.py:1128-1207` (FIX-141) | pending R:R < 1.0 cancels the resting ENTRY | Not a placement refusal; it cancels after placement. |

Plain statement: **one piece of placer code can refuse an order because of R:R**, the FIX-136 gate at `order_placer.py:938-958`. No other placer path refuses on R:R.

---

## 8. Outcome matrix (placement failures; SRC)
| trigger | trade status | reservation (placer) | signal status (processor) | alert |
|---|---|---|---|---|
| R:R gate | no row | not released; the processor releases it | PLACEMENT_FAILED | none |
| link_signal_trade exception | FAILED | released | PLACEMENT_FAILED | ORDER REJECTED |
| kill switch OP-LM1 / A-3 | FAILED | released | PLACEMENT_FAILED | ORDER REJECTED |
| EOD cutoff 15:15 | REJECTED | released | PLACEMENT_FAILED | ORDER REJECTED |
| slippage guard | REJECTED | released | PLACEMENT_FAILED | SLIPPAGE GUARD only |
| drift top-up refused | REJECTED_PRICE_DRIFT | released | PLACEMENT_FAILED | ORDER REJECTED |
| liquidity (dormant) | CANCELLED | released | PLACEMENT_FAILED | — |
| broker `OrderRejectedError` / empty id / CNC lock | FAILED | released | PLACEMENT_FAILED | ORDER REJECTED |
| 429 ×4 | FAILED | released | PLACEMENT_FAILED | ORDER REJECTED |
| `BrokerTimeoutError` (kex.NetworkException) | UNKNOWN_IN_FLIGHT + recovery queue | **kept** | TIMEOUT | none from the placer |
| other `BrokerError` (incl. requests timeout/conn error, INFERENCE) | FAILED | released | PLACEMENT_FAILED | ORDER REJECTED |
| `BrokerRateLimitError` (30 s acquire) | FAILED | released | re-queued ≤3× (idempotent 2nd release) | ORDER REJECTED |
| `ValueError` / `RateLimitAbortedError` (not a BrokerError) | **left `PENDING`** | not released; the processor releases it | PLACEMENT_FAILED | none |
| orders-row persist fails | FAILED + entry cancelled + **hard_kill** | released | PLACEMENT_FAILED | ORDER REJECTED |
| track() fails | FAILED + entry cancelled | released | PLACEMENT_FAILED | ORDER REJECTED |

`kill_switch.record_api_failure` (called by the processor on a `BrokerError`) counts only `BrokerTimeoutError`/`BrokerRateLimitError` toward the auto-trip. Threshold `kill_switch.api_failure_threshold: 3` (`capital/kill_switch.py:842-850`; `system_config.yaml:356`).

---

## 9. Config read on this path (values @970aabf)
| key | value | read at | effect |
|---|---|---|---|
| `broker_limits.order.{burst,rate_per_sec}` | 8 / 8 | `rate_limiter.py:158` | live |
| `broker_limits.quote.{burst,rate_per_sec}` | 3 / 3 | P14/P15/GTT quotes | live (LIVE mode) |
| `broker_limits.timeouts.read_sec` | 10 | `main.py:385` | kite single timeout (LIB) |
| `broker_limits.timeouts.connect_sec` | 5 | parsed only | **no runtime reader** |
| `broker_limits.backoff_sequence_sec` | [1,5,30] | parsed only | **no runtime reader** |
| `broker_limits.rate_limit_backoff.*` | 0.2 / 5.0 / retries 3 / ×2.0 / ±0.05 | adapter 429 + placer loop | live |
| RateLimiter `max_wait_sec` | 30.0 (code default) | `rate_limiter.py:152` | live |
| `system.product_map.zerodha` | INTRADAY MIS / DELIVERY CNC / COVER_ORDER CO / BRACKET_ORDER "" | adapter + persist | live |
| `system.force_intraday_only` | false | adapter `:579` | coercion inactive |
| `system.delivery_enabled` | true | adapter `:593`, GTT placer | CNC allowed |
| `system.trade_type` | BOTH | processor | upstream |
| `trading_hours.eod_entry_cutoff` | "15:15" | P13 | live |
| `entry_gate.min_effective_rr` | 1.0 | P5 | live code, cannot fire with current YAMLs (INFERENCE) |
| `entry_gate.slippage_control` | enabled, sl_fraction, 0.22, cap ₹5.00, hard ₹10.0, also_pct true; overrides enabled, all maps empty | P8/P14 | live |
| `entry_gate.max_entry_slippage_pct` | 1.0 | P14 (pct belt) | live |
| `entry_gate.slippage_buffer` | 2.0 | P2 | dormant path |
| `entry_gate.liquidity_check_enabled / max_spread_pct / min_depth_qty` | true / 0.5 / 500 | parsed (`config_loader.py:1805-1807`), **not wired** | **cannot change behaviour** |
| `risk.price_drift_threshold` | 0.005 | parsed (`config_loader.py:807`), **not wired**; ctor default 0.005 used | **cannot change behaviour** |
| `slippage_bands` | 0-100 … 1000+ | P8 | live (only matters for band overrides, which are empty) |
| `capital.leverage_map` | INTRADAY 5.0, DELIVERY 1.0 | P7/P15 | metadata / top-up size |
| `capital.sl_limit_offset_pct` | 0.005 | SL limit; GTT TGT limit | live (at fill) |
| `capital.gtt_sl_limit_offset_pct` | 0.03 | GTT SL limit | live (at fill, CNC) |
| `order_monitor.poll_interval_sec / fill_timeout_sec` | 2 / 60 | monitor | live |
| `entry_gate.min_pending_rr` | 1.0 | monitor FIX-141 | live |
| `circuit_breaker.partial_fill_timeout_minutes / force_close_time` | 5 / "15:15" | monitor | live |
| `kill_switch.api_failure_threshold` | 3 | processor→kill switch | live |
| `smart_tgt.enabled` | true | placer alert text only, for LIMIT_TRIPLE (`:1746-1750`) | text only |
| strategy `order_protocol` | CO_PLUS_TGT ×13 / LIMIT_TRIPLE ×3 | schema + dashboard | **cannot change behaviour** |
| strategy `tgt_risk_reward` | 1.5 (all) | processor TGT; placer fill-time TGT | live |

---

## 10. Flags (description only)

**Dormant or unreachable code paths**
- F1 `CO_PLUS_TGT`: the protocol can never be selected. `place()` always uses `_default_protocol` = "LIMIT_TRIPLE" (`order_placer.py:961`). As a result the following are unreachable from `place()`: `CoPlusTgtProtocol` (`orders/order_protocol_co.py`), the CO soft-failure branch (`:1503-1521`), the CO-specific persistence and track branches (`:1624-1627`, `:4662`, `:4671`), and the SmartTgt registration (`:2204-2240`).
- F2 **MARKET entry** (`entry_order_type="MARKET"`): passed only by the retest path, and `wait_for_retest_enabled: false`.
- F3 **BRACKET**: the schema allows only INTRADAY/DELIVERY intents (`strategies/schema.py:152-159`), and `BRACKET_ORDER: ""` would raise `ProductNotSupportedError`.
- F4 **FIX-025 `release_ltp`** (`:905-926`): only the gate path passes it, and nothing calls `EntryGate.add()`.
- F5 **Liquidity check** (`:1291-1305`, `:4066-4151`): the ctor default is False and not wired.
- F6 **FIX-072 16388 retry** (`:1358-1396`) and the `result is None` guard (`:1492-1501`). These compare `kite_status_code` to 16388, but the adapter sets `kite_status_code=getattr(exc,"code")` (`zerodha_adapter.py:316`), and kiteconnect's `.code` is the **HTTP status** (LIB `exceptions.py:12-24`; `connect.py:948`). INFERENCE: the value is never 16388, so both are unreachable. The same pattern appears in the post-fill `16418` check at `:3346-3348`; its keyword fallback is still live.
- F7 **OP3 `_compute_tgt`** (`:934-935`): `tgt_price` is always supplied.
- F8 **SL/TGT track branches at placement** (`:1623-1675`) and **SL/TGT persist specs** (`:4680-4701`): LIMIT_TRIPLE `execute` returns empty sl/tgt ids.
- F9 **Force-intraday coercion** (`zerodha_adapter.py:578-584`): config is false. If it were true, `_persist_entry_orders` would record `product` from the *uncoerced* intent (`order_placer.py:4661`), while the wire product would be MIS.
- F10 **OSM `UNKNOWN_IN_FLIGHT` state**: no production code transitions into it. On a translated timeout the adapter sets OSM `FAILED` (`:657-658`) while the trade row is set to `UNKNOWN_IN_FLIGHT`.
- F11 **BreakevenManager registration** (`:2173-2199`, post-fill): `breakeven_manager` is not passed at `main.py:3061-3087`, and `_FillEntry.__slots__` has no `strategy_obj` (`:498-503`), so `getattr(fill_entry,"strategy_obj",None)` is always None.

**Config keys read that cannot change behaviour:** `entry_gate.liquidity_check_enabled`, `.max_spread_pct`, `.min_depth_qty`; `risk.price_drift_threshold` (the same number as the ctor default); `broker_limits.timeouts.connect_sec`; `broker_limits.backoff_sequence_sec`; strategy `order_protocol` (×16 YAMLs); `entry_gate.slippage_buffer` (dormant path only); `smart_tgt.enabled` on LIMIT_TRIPLE (alert text only).

**Computed or received but not read**
- `PlacedOrder.price/product/status/ts/...` for the ENTRY is discarded by `LimitTripleProtocol.execute`; only the two ids are read (`order_protocol_limit.py:224, :241, :244`).
- `sl_price` and `tgt_price` are passed to `LimitTripleProtocol.execute` but unused (`:192-194`).
- `adapter.place_gtt(tag=...)` is accepted and unused (`zerodha_adapter.py:714`).
- `trades.status='PENDING_FILL'` is overwritten to `PENDING` before the broker call (`order_placer.py:1065`).
- The ENTRY `orders.price`/`trigger_price` are never populated: NULL (`:4667-4675`), with no later UPDATE found.
- `trades.tgt_initial` is the processor's pre-fill TGT. The broker TGT is the fill-recalculated value and lives only on the TGT `orders` row or in `gtt_state`.

**Comments or text that contradict code**
- C1 `order_placer.py:31-33` (OP9) says "order_protocol determined by intent". The code does not consult intent (`:961`).
- C2 `order_placer.py:631` ("None = no tick rounding") and `main.py:3088` ("IC8: tick rounding"): the placer no longer rounds (`:928-931`); its instrument cache now serves sector, `_tick_for` and smart-TGT token.
- C3 `core/schema.sql:331` says `orders.price` is "LIMIT price; null for MARKET", under "Order parameters as sent to broker" (`:325`). The ENTRY LIMIT row stores NULL.
- C4 The ORDER PLACED alert (`order_placer.py:843-869`, sent at `:1743-1763` right after ENTRY submission) prints `Fill: ₹{entry_price}` and `SL: ... ✓ | TGT: ... ✓`. At that moment only the ENTRY LIMIT has been submitted: there is no fill, and SL/TGT or the GTT are placed later. The TGT shown is the pre-fill value, and "Smart TGT monitoring: ACTIVE" is shown for LIMIT_TRIPLE, which never registers with SmartTgtManager.
- C5 `broker_limits.yaml:5` says "On 429 ... apply backoff_sequence_sec then soft_kill". `backoff_sequence_sec` has no runtime reader, and 429s use `rate_limit_backoff`.
- C6 `system_config.yaml:138-141` says `force_intraday_only` forces intent at load time. The adapter comment says that load-time rewrite was removed and coercion now happens at the broker chokepoint (`zerodha_adapter.py:571-577`).
- C7 `zerodha_adapter.py:22-23` (ZA7) says "exception -> FAILED". An exception from `rate_limiter.acquire` (`:622`, outside the `try`) leaves the OSM entry `PENDING`.
- C8 Stale line references: `order_placer.py:1321` "OP-LM1 (~:944)" and `:1331` "(set ~:959)" (actual `:1050`, `:1065`); `order_protocol_co.py:112` "discarded at :949" and "12/15 YAMLs" (actual `:961`; 13 of 16 YAMLs declare CO_PLUS_TGT).
- C9 `core/state_store.py:628-633` describes placed-but-unfilled trades as `PENDING_FILL`, and risk_engine comments say the same (`capital/risk_engine.py:594-598`). The placer leaves them `PENDING` (`order_placer.py:1065`). In-session, the risk engine also counts live reservations (`risk_engine.py:605-607`), which the placer holds until fill. The DB-floor queries (`state_store.py:635, :654`) do not include `PENDING`. The downstream effect was not traced.

**Other observed behaviour (INFERENCE where marked)**
- O1 The slippage guard and drift check are **fail-open** when no LTP is available (`order_placer.py:1109`, `:1203`). In PAPER, `get_quote_raw` returns `{}` (`zerodha_adapter.py:1816-1817`), so both are always skipped.
- O2 A broker 429 on `get_quote_raw` is penalized in the **`order`** bucket: `_CATEGORY_MAP.get("get_quote_raw","order")` (`zerodha_adapter.py:1822-1824`, `:2053`). `_fetch_ltp` swallows the error, and the following `place_order` acquire then waits out that freeze.
- O3 INFERENCE (LIB): a client-side HTTP timeout on `place_order` ends up as FAILED + reservation released, not UNKNOWN_IN_FLIGHT (§4). Whether a broker order that did land is later adopted by the reconciler was not traced.
- O4 Non-BrokerError exceptions from inside `place()` (for example `ValueError` from `_validate_place_order`, or `RateLimitAbortedError`) leave the trade row in `PENDING` with no `_handle_placement_failure`.
- O5 Worst-case configured wait before and at the broker call in LIVE (INFERENCE, not measured): 2 quote calls (each ≤30 s acquire + ≤10 s HTTP), then an order acquire ≤30 s, then HTTP ≤10 s, then up to 3 more 429 attempts gated by penalize delays of 0.2/0.4/0.8 s ± 0.05.
