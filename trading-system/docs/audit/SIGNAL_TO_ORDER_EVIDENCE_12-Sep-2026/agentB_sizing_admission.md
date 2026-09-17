# Agent B — Sizing · Capital allocation · Reservation · Fused admission

**Source:** `src970/` extract of commit `970aabf3c78d…` (= origin/main). Every file cited below was
byte-compared to `git show 970aabf:<path>`: **all MATCH** (signal_processor, position_sizer,
fund_manager, risk_engine, entry_throttle, main, system_config.yaml, scoring_weights.yaml,
state_store, kill_switch, webhook_receiver, v3_chain/runner+models, portfolio_allocator,
config_loader, quality_scorer, order_placer).

**Provenance labels used below**
- **[SRC]** read directly from source @970aabf (quoted where load-bearing)
- **[CFG]** a config value @970aabf
- **[INF]** inference — arithmetic over quoted source + config, or a timing/ordering deduction; the basis is stated
- **[CMT]** a claim that exists only in a code/config/test *comment* (not verified by me)
- Nothing here was run, measured, or read from a DB/VM/log. **No timing was measured.**

**SHA note (read before using line numbers).** `d3ee69d` (the running SHA) is an **ancestor** of
`970aabf` (`git merge-base --is-ancestor d3ee69d 970aabf` → true). `970aabf` = `d3ee69d` **plus** the
Batch-1 evidence-capture additions. So at d3ee69d the `_evidence_capture(...)` calls, `_iso`,
`_raw_signal_field`, `_AdmitCtx.reanchored` and the `_reanchored` local **do not exist**.
`capital/*`, `signals/entry_throttle.py`, `core/state_store.py`, `orders/*`, `allocation/*`,
`v3_chain/*`, `config/system_config.yaml` are **identical** at both SHAs. `main.py` is identical up
to line 3244 and shifts −33..−35 lines after that. `signals/signal_processor.py` line map:

| site | @970aabf | @d3ee69d |
|---|---|---|
| `def _enforce_strategy_position_cap` | 744 | 638 |
| `def _enforce_one_trade_per_symbol_direction` | 802 | 696 |
| `def _process_one` | 867 | 761 |
| `sizing = self._sizer.calculate(` | 1112 | 1001 |
| `if not sizing.success:` | 1127 | 1016 |
| `self._v3_chain.observe(` | 1138 | 1027 |
| `if self._allocator is not None:` | 1147 | 1036 |
| `self._admit_and_place(` (fused call) | 1182 | 1070 |
| `except _PipelineReject as rej:` | 1193 | 1081 |
| `except Exception as exc:` (outer) | 1233 | 1111 |
| `def _admit_and_place` | 1277 | 1155 |
| H-7 call / `approve(` / `reserve(` | 1311 / 1315 / 1328 | 1189 / 1193 / 1206 |
| `RESERVE_FAILED` | 1338 | 1216 |
| `KILL_SWITCH_LATE` / `SHUTDOWN` | 1396 / 1405 | 1274 / 1283 |
| `self._entry_throttle.admit(` | 1410 | 1288 |
| `self._placer.place(` | 1446 | 1302 |
| `"PROCESSED"` | 1543 | 1399 |

---

## 0. Stage map (execution order, `_process_one` after the screener returns PASSED)

| # | Stage | file:line @970aabf | Decides / changes | Live? |
|---|---|---|---|---|
| (A0) | price derivation (+ M-S1 re-anchor) — **Agent A's scope**; listed only for the reject table | signal_processor.py:1028-1106 | entry, SL | LIVE |
| A | Position sizing | signal_processor.py:1111-1129 → capital/position_sizer.py:245-809 | **qty** (or reject) | LIVE |
| B | Capital state read by sizing | position_sizer.py:357-359 → fund_manager.py:1591-1613 | inputs only | LIVE |
| C | V3 chain observe | signal_processor.py:1136-1143 → v3_chain/runner.py:99-118 | nothing (JSONL) | SHADOW |
| D | Portfolio allocator hook | signal_processor.py:1147-1172 | nothing in `shadow` | SHADOW |
| E1 | FIX-018 in-flight increment | signal_processor.py:1302-1305 | counter | LIVE |
| E2 | `portfolio_lock` critical section | signal_processor.py:1307-1344 | — | LIVE |
| E3 | H-7 per-strategy cap | :1311 → :744-779 | reject | LIVE |
| E4 | one trade / symbol+direction / book / day | :1312-1313 → :802-864 | reject | LIVE |
| E5 | RiskEngine.approve (10 checks) | :1314-1325 → risk_engine.py:248-803 | reject | LIVE (SECTOR = observe) |
| E6 | FundManager.reserve | :1327-1340 → fund_manager.py:521-635 | **capital reserved** (or reject) | LIVE |
| E7 | status `RESERVED` (inside lock) | :1344 | DB write | LIVE |
| E8 | target derivation | :1368 → :1901-1953 | tgt (or reject) | LIVE |
| E9 | Telegram "INTRADAY SIGNAL" alert (synchronous) | :1371-1380 → :486-555 | nothing | LIVE side-effect |
| E10 | late kill-switch re-check | :1389-1396 | reject | LIVE |
| E11 | shutdown check | :1398-1405 | reject | LIVE |
| E12 | entry throttle (min-gap / burst / per-symbol) | :1410-1418 → entry_throttle.py:65-115 | reject | LIVE |
| E13 | effect-telemetry `inc()` + P1 evidence (970aabf only) | :1423-1445 | nothing | observer |
| E14 | `self._placer.place(...)` | :1446-1460 | → order path | LIVE |
| F | exception handlers / finally | :1193-1276 (+ `_process_one_safe` :465-480) | status + release | LIVE |

`_heartbeat()` checkpoints at :1129, :1346, :1382 are **no-ops in production** (see Flags §10.1).

---

## 1. Stage A — the call into the position sizer

### 1.1 Call site [SRC] signal_processor.py:1111-1129
```python
sizing = self._sizer.calculate(
    symbol,
    side,
    entry_price,
    sl_price,
    strategy_obj.intent,
    screen_result.tier,
    strategy_obj.lot_size,
    perf_weight=self._perf_weights.get(strategy_obj.name, 1.0),  # FIX-132 Item 9
)
except BrokerError as be:
    if self._ks:
        self._ks.record_api_failure(be)
    raise _PipelineReject("SIZING_BROKER_ERROR", str(be)) from be

if not sizing.success:
    raise _PipelineReject(f"SIZING_{sizing.constraint}", sizing.reason)
```

### 1.2 Inputs and provenance

| input | value source | notes |
|---|---|---|
| `symbol` | queued signal tuple (:878-886) | logging + `instrument_cache.lot_size(symbol)` |
| `side` | `"BUY" if _dir in ("LONG","BUY") else "SELL"` from `strategy_obj.direction` (:1034-1035) | only used for PS8 validation + PS10 SL-direction WARNING in the sizer |
| `entry_price`, `sl_price` | `_derive_prices(trigger_price, …)` at :1028, **or** re-derived from live LTP at :1098 when `not strategy_obj.pullback_wait_enabled and self._quote_fn is not None` (M-S1) | Agent A's scope |
| `intent` | `strategy_obj.intent` — schema allows only `INTRADAY` / `DELIVERY` (strategies/schema.py:152-157) | picks bucket, leverage, per-book limits |
| `score_tier` | `screen_result.tier` — `"HIGH"` ≥ 80, `"MEDIUM"` ≥ 65, else `"LOW"` (quality_scorer.py:122-132; scoring_weights.yaml:28-29 [CFG]); pass mark 60 (:22) | picks tier multiplier |
| `lot_size` | `strategy_obj.lot_size` = **1** in every strategy YAML [CFG] | because it is 1, the sizer replaces it with `instrument_cache.lot_size(symbol)` (position_sizer.py:309-313); on any exception it stays 1 |
| `entry_offset_pct` | **not passed** → default `0.0` (position_sizer.py:263) | see Flag §10.4 |
| `perf_weight` | `self._perf_weights.get(name, 1.0)`; `perf_weights` is **never passed** to `SignalProcessor` (main.py:3575-3623) and `_perf_weights` is never assigned elsewhere → **always 1.0** [SRC] | see Flag §10.2 |
| `leverage_map` | main.py:2678-2683 from `capital.leverage_map` [CFG] INTRADAY 5.0 · COVER_ORDER 6.0 · DELIVERY 1.0 · BRACKET_ORDER 5.0 | sizer ctor main.py:2842 |
| live broker margin | `self._broker_adapter` — **not passed** at main.py:2840-2863 → `None` → FIX-072 branch (position_sizer.py:389-423) never runs; static leverage always | Flag §10.2 |
| `total_capital`, `avail` | `snap = self._fm.get_snapshot()`; `total_capital = snap.total`; `avail = snap.intraday_avail if bucket == "intraday" else snap.positional_avail` (position_sizer.py:357-359) | read **outside** `portfolio_lock` (the sizer runs before :1307) |
| policy limits | ctor args main.py:2843-2862 (see §9 config table) | |
| `min_tick_size`, `max_single_order_qty` | **not passed** → ctor defaults 0.05 / 10000 (position_sizer.py:164-165) | Flag §10.2 |

### 1.3 Arithmetic, in execution order [SRC] position_sizer.py

1. **lot_size resolve** (:309-313): `if lot_size == 1 and self._instrument_cache is not None: lot_size = self._instrument_cache.lot_size(symbol)` (exception → keep 1).
2. **PS8 validation → `ValueError`** (:316-339): side ∉ {BUY,SELL}; `entry_price <= 0`; `sl_price <= 0`; intent ∉ valid set; tier ∉ {HIGH,MEDIUM,LOW}; `lot_size <= 0`. A `ValueError` is **not** a `_PipelineReject` → falls to the outer handler → **`PLACEMENT_FAILED`** (§7).
3. **PS10** (:342-353): SL on the wrong side → WARNING only.
4. **bucket** (:356): `bucket = "intraday" if intent in _INTRADAY_INTENTS else "positional"`.
5. **per-book limits** (:374-384):
   ```python
   if bucket == "positional":
       eff_risk_pct = self._require_delivery(self._delivery_risk_per_trade_pct, "delivery_risk_per_trade_pct")
       eff_conc_pct = self._require_delivery(self._delivery_max_concentration_pct, "delivery_max_concentration_pct")
       eff_max_position_value_pct = self._require_delivery(self._delivery_max_position_value_pct, "delivery_max_position_value_pct")
   else:
       eff_risk_pct = self._risk_per_trade_pct
       eff_conc_pct = self._max_concentration_pct
       eff_max_position_value_pct = self._max_position_value_pct
   ```
   `_require_delivery` (:216-243) logs CRITICAL and raises `ValueError` if a delivery value is `None` (unreachable in prod: config_loader.py:497-513 makes them required).
6. **leverage** (:388): `leverage = self._leverage_map.get(intent, 1.0)` → 5.0 (INTRADAY) / 1.0 (DELIVERY).
7. **SL distance** (:424): `sl_distance = abs(entry_price - sl_price)`.
8. **Guard 1** (:429-454): `if sl_distance < self._min_tick_size` (0.05) → `constraint="INVALID_SL_DISTANCE"`, `breakdown={}`.
9. **risk qty** (:456-457): `risk_rs = total_capital * eff_risk_pct`; `qty_by_risk = int(math.floor(risk_rs / sl_distance))`.
10. **Guard 2 (input)** (:461-487): `if qty_by_risk > self._max_single_order_qty` (10000) → `constraint="QTY_EXPLOSION_GUARD"`, `breakdown={"qty_by_risk": …}`.
11. **capital qty** (:492-496): `effective_entry_price = entry_price * (1.0 + entry_offset_pct)` (offset always 0.0 → = entry); `margin_per_share = effective_entry_price / leverage`; `qty_by_capital = int(math.floor(avail / margin_per_share)) if margin_per_share > 0 else 0`. **The divisor is leverage**: `qty_by_capital = floor(avail × leverage / entry)`.
12. **concentration qty** (:498-500): `qty_by_concentration = int(math.floor((total_capital * eff_conc_pct) / entry_price))`.
13. **min + binding label** (:503-512):
    ```python
    raw_qty = min(qty_by_risk, qty_by_capital, qty_by_concentration)
    if qty_by_capital <= qty_by_risk and qty_by_capital <= qty_by_concentration:
        constraint = "CAPITAL"
    elif qty_by_risk <= qty_by_concentration:
        constraint = "RISK"
    else:
        constraint = "CONCENTRATION"
    ```
    (CAPITAL wins ties; then RISK wins ties against CONCENTRATION.)
14. **breakdown created** (:515-521): `qty_by_risk, qty_by_capital, qty_by_concentration, raw_qty, tier_multiplier`.
15. **raw_qty ≤ 0** (:524-539) → reject with the label from step 13; reason `f"qty=0: {constraint} exhausted for {symbol} (risk_qty=… capital_qty=… conc_qty=…)"`.
16. **multiplier (ON mode — `position_sizing.enabled: true` [CFG])** (:542-620):
    ```python
    tier_mult = self._tier_multipliers.get(score_tier, 1.0)
    effective_mult = tier_mult * max(0.0, perf_weight)
    if effective_mult <= 0: … constraint="ZERO_MULTIPLIER" …
    tiered_qty = int(math.floor(raw_qty * effective_mult))
    tiered_qty = max(1, min(tiered_qty, raw_qty * 2))        # FIX-133: floor 1, cap 2x
    if tiered_qty > raw_qty:
        breakdown["rung_before_multiplier"] = constraint.lower()
        constraint = "MULTIPLIER"
    ```
    Tier multipliers [CFG] HIGH 1.0 · MEDIUM 0.70 · LOW 0.50; perf_weight 1.0 ⇒ `effective_mult = tier_mult`.
    (OFF/flat branch :621-633 is inert: `enabled: true`, `flat_value_rs` commented out.)
17. **lot rounding** (:639): `final_qty = (tiered_qty // lot_size) * lot_size`.
18. **Guard 2 (output, BUG-NI17)** (:656-684): `if final_qty > self._max_single_order_qty` → `QTY_EXPLOSION_GUARD`.
19. **lot skew** (:688-705): only `if lot_size != 1 and tiered_qty > 0 and final_qty > 0`: `skew = (tiered_qty - final_qty) / tiered_qty`; `> 0.25` → `constraint="REJECTED_LOT_SKEW"`.
20. **position value cap** (:721-752): `position_value = final_qty * entry_price`; `max_position_value = eff_max_position_value_pct * total_capital`; `>` → `constraint="POSITION_VALUE_CAP"` (REJECT, not clamp).
21. **BELOW_MIN** (:754-779): `if final_qty < lot_size or final_qty < self._min_qty_threshold` (1) → `constraint="BELOW_MIN"`.
22. **success** (:781-809): `margin_required = final_qty * margin_per_share`; `risk_amount = final_qty * sl_distance`; `breakdown["binding_constraint"] = constraint.lower()`; `breakdown["actual_position_value_rs"] = round(final_qty * entry_price, 2)`; reason `f"{symbol} qty={final_qty} [{constraint}-bound tier={score_tier}({tier_mult})]: risk_qty=… capital_qty=… conc_qty=… lot_size=…"`.

`calculate()` (:245-252) is a pass-through that increments an effect-telemetry counter after `_calculate` returns.

### 1.4 Outputs
`SizingResult` (frozen, :69-101): `success, qty, margin_required, risk_amount, bucket ("intraday"|"positional"), constraint, reason, breakdown`.

**`sizing.constraint`** — success: `CAPITAL | RISK | CONCENTRATION | MULTIPLIER | FLAT`; failure: `INVALID_SL_DISTANCE | QTY_EXPLOSION_GUARD | CAPITAL | RISK | CONCENTRATION | ZERO_MULTIPLIER | REJECTED_LOT_SKEW | POSITION_VALUE_CAP | BELOW_MIN`.

**`sizing.breakdown`** on success (ON mode): `qty_by_risk, qty_by_capital, qty_by_concentration, raw_qty, tier_multiplier, tier_multiplier_mode="ON", tier_weight_applied, perf_weight_applied, flat_value_rs_used=None, qty_by_flat=None, [rung_before_multiplier], tiered_qty, tier_mult, perf_weight, binding_constraint, actual_position_value_rs`.

**Who reads what downstream [SRC]:**
- `qty` → risk nothing (risk reads `margin_required`); `reserve(…, sizing.qty, …)` :1329; alert :1378; `place(qty=…)` :1449; SR observer :1557.
- `margin_required` → risk CAPITAL (:536) + SECTOR (:737); allocator `ScoredCandidate.margin_required` (:1643).
- `bucket` → risk (:316, :533, :564, :652).
- `breakdown` → `place(sizing_breakdown=…)` :1458 → `order_manager.create_trade` persists **only** `tier_multiplier_mode, tier_weight_applied, perf_weight_applied, flat_value_rs_used, qty_by_risk, qty_by_capital, qty_by_concentration, qty_by_flat, binding_constraint, actual_position_value_rs` (orders/order_manager.py:224-227, 256-259); P1 evidence record @970aabf only (:1443-1444).
- `risk_amount` → **nothing** (Flag §10.1).
- On a **reject**, only `sizing.constraint` (as the status suffix) and `sizing.reason` (as `rejection_reason`) survive; the breakdown is discarded.

### 1.5 qty = 0 / failure handling
Every sizer failure returns `success=False, qty=0` → :1127-1128 raises `_PipelineReject(f"SIZING_{constraint}", reason)` → status **`REJECTED_SIZING_<constraint>`** with `rejection_reason = sizing.reason` (§7). No reservation exists yet, nothing to release. Note the double prefix `REJECTED_SIZING_REJECTED_LOT_SKEW`.

### 1.6 MIS (INTRADAY) vs DELIVERY [SRC]+[CFG]

| aspect | INTRADAY (bucket "intraday") | DELIVERY (bucket "positional") |
|---|---|---|
| risk pct | `risk_per_trade_pct` 0.01 | `delivery_risk_per_trade_pct` 0.01 |
| concentration pct | `max_concentration_pct` 0.10 | `delivery_max_concentration_pct` 0.10 |
| position value cap | `max_position_value_pct` 0.40 | `delivery_max_position_value_pct` 0.40 |
| leverage (divisor) | 5.0 | 1.0 |
| avail | `snap.intraday_avail` | `snap.positional_avail` |
| base of risk & concentration | `snap.total` (TOTAL capital, both books) | same `snap.total` |
| tier/perf, min qty, lot skew, tick, qty cap | shared | shared |
Values are equal today; only leverage and the bucket differ.

### 1.7 Which constraint can bind — [INF] (arithmetic from §1.3 + [CFG])
- **CONCENTRATION vs RISK:** unfloored `qty_by_risk / qty_by_concentration = (0.01/0.10)·(entry/sl_distance)`. `sl_distance/entry ≤ sl_max_pct` after bounds (0.05 intraday, 0.08 delivery YAMLs; the 09:15-09:30 gap buffer cannot apply because `trading_hours.entry_start` is 10:00). So the risk quantity is ≥ 2× (intraday) / ≥ 1.25× (delivery) the concentration quantity; RISK can be the label only through floor ties (e.g. both floors 0 → `REJECTED_SIZING_RISK` when capital ≥ 1; or small-integer ties for delivery). Code comment agrees: position_sizer.py:508-509 "IA-P3-04 — algebraically never today" [CMT].
- **CAPITAL** binds when `floor(avail·lev/entry) ≤ floor(0.10·total/entry)`: intraday ≈ `intraday_avail ≤ 0.02·total`; delivery ≈ `positional_avail ≤ 0.10·total`.
- **MULTIPLIER** label: requires `tiered_qty > raw_qty` ⇒ `effective_mult > 1`; with tier ≤ 1.0 and perf 1.0 it cannot occur (the `max(1, …)` floor equals raw only when raw = 1).
- **POSITION_VALUE_CAP:** `final ≤ tiered ≤ raw ≤ qty_by_concentration` ⇒ `position_value ≤ 0.10·total < 0.40·total` ⇒ cannot fire under current config (config comment says this for delivery only, system_config.yaml:255-258).
- **BELOW_MIN:** with `lot_size` = 1 and ON mode, `tiered_qty ≥ 1` ⇒ `final ≥ 1` ⇒ cannot fire. Reachable only if `instrument_cache.lot_size(symbol)` > 1 (InstrumentRow docstring: "1 for equity", core/instrument_cache.py:65; `instruments.csv` is not in the repo — data not inspected).
- **LOW-tier floor:** a LOW signal with `raw_qty = 1` trades 1 share (`floor(0.5) = 0` → `max(1, …)` = 1).
- **QTY_EXPLOSION_GUARD:** fires only if `total·0.01/sl_distance > 10000`; code comment position_sizer.py:652-655 calls the output guard "LATENT AT TODAY'S CAPITAL" [CMT].

### 1.8 Missing input / dependency failure [SRC]
- `instrument_cache.lot_size` raises → swallowed, `lot_size` stays 1 (:310-313).
- `get_snapshot()` DB error (`get_daily_realized_net_pnl`) → propagates (not `BrokerError`) → `PLACEMENT_FAILED`.
- FundManager not initialised → `get_snapshot()` does **not** assert init; `total=0` → all three quantities 0 → `REJECTED_SIZING_CAPITAL` (unreachable: main initialises at :2761 before the processor starts).
- `SIZING_BROKER_ERROR` requires a `BrokerError` out of `calculate()`; the only broker call (`get_live_margin_pct`, :391) is inside `try/except Exception` and not wired → **unreachable** [INF].

---

## 2. Stage B — capital allocation (fund_manager) at decision time

### 2.1 The split [SRC]+[CFG]
- main.py:2702-2708: `resolve_bucket_allocation(conditional_enabled=cap_cfg.conditional_allocation_enabled, …, intraday_pct=cap_cfg.intraday_bucket_pct, positional_pct=cap_cfg.positional_bucket_pct)`; with `conditional_allocation_enabled: false` [CFG] it returns the fixed split unchanged (fund_manager.py:138-139) → **0.70 / 0.30**.
- FundManager ctor main.py:2718-2736 passes the split, `daily_loss_limit_pct` (0.03), `leverage_map`, breach callback, `kill_switch`. **Not passed:** `slm_margin_buffer_pct` (→ default 0.05, fund_manager.py:309) and `on_critical_failure` (→ None).

### 2.2 What the fields mean [SRC]
- `_total` (fund_manager.py:365): set by `initialize(broker_balance)` (:477). Live seed `compute_live_seed` main.py:2074-2078 = `broker_adapter.get_margins().net - fund_manager.today_realized_pnl_carryover(...)`. Then `rehydrate_from_open_trades` adds the positional carry (:1836-1837 `self._positional_avail += self._positional_carry; self._total += self._positional_carry`) and today's RELEASE_USED `pnl_delta` rows (:1866-1872). `sync_from_broker` (only caller: the 09:15 thread main.py:1014-1016, and only if booted before 09:15) sets `new_total = broker_balance + carry_total` (:1430-1431). Intraday, `_total` moves only by `release_used`: `self._total += pnl` (:1326). `_intraday_carry` is hard-set 0.0 (:1831).
- Bucket base (:2311-2335): `cash = self._total - carry_total`; intraday base = `cash * 0.70 + intraday_carry`; positional base = `cash * 0.30 + positional_carry`.
- `initialize` (:478, :481): `self._intraday_avail = broker_balance * self._intraday_pct`; `self._positional_avail = broker_balance * self._positional_pct`.
- `sync_from_broker` (:1462-1467): `avail = base − reserved − used` per bucket.
- `_apply_reserve` (:2175-2176): `avail -= margin; reserved += margin`, record `_Reservation(... strategy=strategy)`.
- `_apply_release` (:2193-2195): pop; `avail += res.margin; reserved -= res.margin`.
- `_apply_commit` (:2206-2210, on fill): pop; `reserved -= res.margin; used += actual_margin; avail += (res.margin - actual_margin)`.
- `release_used` (:1323-1326, on close): `used -= margin; avail += margin + pnl; _total += pnl`.
- **`avail`** = free margin of that bucket; **`reserved`** = margin held by live reservations (reserve → fill/release); **`used`** = margin of filled positions. Invariant `avail+reserved+used == _total` (global) + per-bucket non-negativity (:2391-2471).
- **No cross-bucket borrowing:** `reserve` consults only `self._bucket_avail(bucket)` for the intent's bucket (:557-577).
- `get_snapshot()` (:1591-1613) returns all of the above **plus** `daily_realized_pnl = self._store.get_daily_realized_net_pnl(today)` (SQL `SUM(pnl_delta) FROM fm_ledger WHERE date = ?`, state_store.py:2674-2679) — read under the FM lock.
- **Divisor:** `required_margin(qty, price, intent, leverage_map) = (qty * price) / leverage` (:248-268); sizer uses `entry/leverage` per share (position_sizer.py:493).

### 2.3 Consequences visible in source [INF]
- Risk and concentration are percentages of **TOTAL** (`snap.total`), not of the bucket; one delivery position at 10% of total uses one-third of the 30% positional bucket (plus the 5% reserve buffer, §5).
- Delivery carry (held CNC at cost) is inside `_total`, so it enlarges the risk/concentration base.

---

## 3. Stage C — V3 chain observe (SHADOW, log-only)

[SRC] signal_processor.py:1136-1143:
```python
if self._v3_chain is not None:
    try:
        self._v3_chain.observe(self._build_v3_signal(
            signal_id, symbol, scanner_name, strategy_name, strategy_obj,
            side, entry_price, sl_price, screen_result,
            trigger_price, triggered_at, now))
    except Exception as _v3_exc:   # the chain must NEVER break admission
        self._log.error("v3_chain observe error (ignored): %s", _v3_exc)
```
- **Wired?** `v3_chain.v3_chain_mode: "shadow"` [CFG] (system_config.yaml:574) → main.py:3673-3694 builds `V3ChainRunner` and calls `signal_processor.set_v3_chain(...)`. LIVE-wired as an observer.
- **Fires for:** every signal that passed sizing (placed after :1127), including those later rejected by risk/reserve/throttle; never for sizing rejects.
- **What is sent** (`_build_v3_signal`, :1578-1603 → `V3Signal`, v3_chain/models.py:23-49): `signal_id, symbol, scanner_name, strategy_name, side, intent, entry_price (post-M-S1), live_sl_price, live_tgt_price` (computed by a synchronous `_derive_target`; **any** exception incl. `_PipelineReject` → `live_tgt = None`, :1587-1590), `trigger_price, score, tier, step_results` (dict copy), `market_data` (dict copy), `sector` (always `"UNKNOWN"`, Flag §10.1), `as_of=now` (the instant captured at :910, **before** screening), `triggered_at, v3_playbook`. `regime_state` stays `None`: `observe` sets it only when a regime runner exists, and `regime.enabled: false` means none is built (main.py:3514-3540).
- **Awaited? No.** runner.py:103-118:
  ```python
  if self.mode != "shadow":
      return
  try:
      ...
      self._q.put_nowait(sig)
  except queue.Full:
      self._safe_log("warning", "v3_chain: queue full, dropping %s/%s", ...)
  except Exception as exc:   # observability must NEVER break admission
      self._safe_log("error", "v3_chain.observe error (ignored): %s", exc)
  ```
  Queue `maxsize = max_queue` = 512 [CFG] (runner.py:67). Background thread `_run` (:121-134).
- **Can it affect the order? No [SRC].** `observe` returns `None` and nothing is assigned from it; `V3ChainRunner` is constructed with only `config, zone_knobs, zone_scoring, fetcher, logger, now_fn, regime_runner` (runner.py:46-56) — no reference to the processor, FundManager, risk engine or placer; its only output is `_persist` (:271-284) appending a `WouldBeRecord` to `data_store/v3/would_be.jsonl` [CFG :617] + an INFO log. Gates are commented "LOG-ONLY — recorded, never enforced" (:207) and there is no path back.
- **What it records:** `WouldBeRecord` (models.py:52-125): V3 gates (RR/HTF/EXTREME), score, v3_sl/tgt/rr vs live entry/sl/tgt/rr, nearest S/R, regime, `v3_verdict`.
- **Hot-path cost:** `_build_v3_signal` is synchronous (pure target maths, two dict copies, a `getattr` probe); fetching happens on the worker via `rate_limiter.acquire("historical")` (main.py:421-438). Not measured.
- **Dependency failure:** full queue → drop + WARNING; any exception → ERROR log; neither changes the pipeline.

## 4. Stage D — portfolio allocator hook (SHADOW)

[SRC] :1147-1172. `portfolio_allocator.allocator_mode: "shadow"`, `enforce_scope: "v3_only"` [CFG] (system_config.yaml:565-566) → main.py:3633-3651 builds and `set_allocator(...)`.
- `if _amode == "enforce" and self._allocator.in_scope(strategy_obj)` → hand-off + `return` — **not taken** (mode is shadow; v3_only scope matches only `v3_playbook: true` = `pb01_breakout_retest`, which is `enabled: false`).
- `if _amode == "shadow": self._allocator.observe(self._build_candidate(... with_payload=False))` → `WindowBuffer.append` (portfolio_allocator.py:88-96), later regret JSONL `data_store/allocator/regret.jsonl`. Never reserves or places.
- `except _PipelineReject: raise` (:1169-1170) — inert in shadow (`_build_candidate` raises no `_PipelineReject`); `except Exception` → ERROR log, fall through.
- Falls through to the fused admission unchanged. The shadow worker's `_capacity_snapshot` calls `self._fm.get_snapshot()` (portfolio_allocator.py:164), which briefly takes the same RLock as `portfolio_lock`.

---

## 5. Stage E — fused admission `_admit_and_place` (signal_processor.py:1277-1561)

### 5.1 `_AdmitCtx` [SRC] :103-120
`__slots__ = ("reservation_id", "requeued", "in_flight_incremented", "placed", "reanchored")` (`reanchored` exists only @970aabf; evidence-only). The caller's inner `try/finally` (:1181-1191) copies `reservation_id`, `requeued`, `in_flight_incremented` back into `_process_one` locals, so the outer `except`/`finally` (:1193-1276) can release on every exit path. `placed` is read only by `admit_prepared` (enforce path, dormant).

### 5.2 E1 — FIX-018 in-flight counter [SRC] :1302-1305
```python
with self._in_flight_lock:
    self._in_flight_count += 1
    ac.in_flight_incremented = True  # FIX-165c
    processor_in_flight = self._in_flight_count
```
Taken **before** `portfolio_lock`; decremented in `_process_one`'s `finally` (:1253-1258). Only reader: risk check 4 intraday branch (`legacy_total`). Counts every candidate between this line and its `finally`, including ones currently inside `place()`.

### 5.3 E2 — the critical section [SRC] :1307-1344
`with self._fm.portfolio_lock:` = the FundManager's own `threading.RLock` (fund_manager.py:426-443). Inside it, in order: H-7 (E3), one-per-day (E4), `approve` (E5), `reserve` (E6), `update_signal_status(signal_id, "RESERVED")` (E7). Counted from source: **15 SQL statements for an intraday entry, 17 for delivery**, all run while holding the capital lock (H-7 1, one-per-day 1, approve 11 [+2 delivery], ledger INSERT 1, RESERVED UPDATE 1). Not timed.

### 5.4 E3 — H-7 per-strategy concurrent cap [SRC] :744-779
```python
max_strat_pos = getattr(strategy_obj, "max_concurrent_positions", 2)
row = self._store.fetch_one(
    "SELECT "
    "SUM(CASE WHEN status IN ('OPEN','PARTIAL') THEN 1 ELSE 0 END) AS open_partial, "
    "SUM(CASE WHEN status IN ('OPEN','PARTIAL','PENDING_FILL') THEN 1 ELSE 0 END) AS active "
    "FROM trades WHERE strategy = ?", (strategy_name,))
...
reserved = self._fm.count_live_reservations_for_strategy(strategy_name)
effective = max(open_partial + reserved, active_incl_pending) + 1
if effective > max_strat_pos:
    raise _PipelineReject("STRATEGY_POSITION_LIMIT", f"{strategy_name} at cap: {effective - 1}/{max_strat_pos} open+in-flight (open_partial=…, reserved=…, active_incl_pending=…)")
```
- Inputs: `trades` (all dates, all products; `EXITING`/`UNKNOWN_IN_FLIGHT` not counted by the SQL), in-memory reservations tagged with this strategy (fund_manager.py:1578-1589), strategy YAML `max_concurrent_positions` [CFG]: 3 for `gap_fade_*`, `gap_go_*`; 2 for every other strategy (schema default 2, strategies/schema.py:127).
- Status: **`REJECTED_STRATEGY_POSITION_LIMIT`**. Missing row → 0.

### 5.5 E4 — one completed trade per symbol+direction per book per day [SRC] :802-864
```python
if not bool(getattr(self._risk, "_one_trade_per_symbol_direction", False)):
    return
direction = "LONG" if str(side).upper() == "BUY" else "SHORT"
today = now_ist().date().isoformat()
pipeline = SignalProcessor._pipeline_for_intent(intent)
n = self._store.count_executed_trades_today_for_symbol_direction(symbol, direction, today, pipeline=pipeline)
if n >= 1:
    book = pipeline or "account-wide"
    raise _PipelineReject("SYMBOL_DIRECTION_DAILY_LIMIT", f"{symbol} {direction} already traded today in the {book} book ({n} executed trade(s)); one completed trade per symbol+direction per day, per pipeline")
```
- Flag: `risk.one_trade_per_symbol_direction_per_day: true` [CFG] (:302) → RiskEngine ctor main.py:2901 → `self._one_trade_per_symbol_direction` (risk_engine.py:203).
- `_pipeline_for_intent` (:781-800): DELIVERY → `"delivery"`, INTRADAY/CO/BO → `"intraday"`, unknown → `None` (account-wide). Import failure → `None`.
- SQL (state_store.py:806-822): `COUNT(DISTINCT t.trade_id)` over `trades LEFT JOIN orders ON leg='ENTRY'`, same symbol+direction, `SUBSTR(created_at,1,10) = today`, status ∈ `PENDING_FILL, OPEN, PARTIAL, EXITING, CLOSED, CLOSED_MANUAL` (:734-736); delivery scope `(o.product IS NULL OR o.product = 'CNC')`, intraday scope `(o.product IS NULL OR o.product <> 'CNC')`.
- Clock: `now_ist()`. DB only — no reservation term. Status **`REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT`**.

### 5.6 E5 — `RiskEngine.approve` [SRC] risk_engine.py:248-803
Call :1314-1325; `BrokerError` → `RISK_BROKER_ERROR` (unreachable [INF]: no broker call in approve); `not approval.approved` → `_PipelineReject(approval.failed_check, approval.reason)` → status `REJECTED_<failed_check>`.

**Reads, once, before any check (:293-375):** `today`; `snap = self._fm.get_snapshot()`; `count_active_positions()` (OPEN/PARTIAL/PENDING_FILL, all products, all dates); `count_open_positions()` (OPEN/PARTIAL); `count_in_flight_orders()` (PENDING_FILL); `count_trades_today(today)` (executed statuses); `count_settled_trades_today(today)` (executed minus PENDING_FILL); **delivery only**: `count_open_delivery_positions()`, `count_daily_delivery_trades(today)` (JOIN orders ENTRY `product='CNC'`, state_store.py:867-893); per-book limits (`_require_delivery` raises for None); `recent_trade_pnls(max_consec+1, today=today)` (closed today, by `exit_time DESC`); sector via `instrument_cache.sector(symbol)` (exception/blank → `"UNKNOWN"`); `sector_exposure(sector)` + `_effective_sector_margin` (DB OPEN/PARTIAL `margin_reserved` + live reservation margins of that sector; failure → DB truth + WARNING); `has_active_position(symbol)`; `get_active_position_direction(symbol)`; `self._ks.is_active()` (default intent `"entry"` → SOFT or HARD, kill_switch.py:510-520).

**Checks, short-circuit, in order:**

| # | failed_check → status | lines | condition (verbatim core) | limit [CFG] |
|---|---|---|---|---|
| 1 | `KILL_SWITCH` | 516-519 | `if kill_active:` → "Kill switch is active; no new trades permitted" | kill state |
| 2 | `SIZING_VALID` | 522-527 | `if not sizing_result.success:` | — (cannot fire here) |
| 3 | `CAPITAL` | 530-541 | `if bucket_avail < sizing_result.margin_required:` → "Insufficient {bucket} capital: available=…, required=…" | bucket avail |
| 4a | `OPEN_POSITIONS` (delivery) | 564-570 | `if open_delivery_count >= eff_max_open_delivery:` → "Delivery position cap reached: …" | `max_open_delivery_positions` 3 |
| 4b | `OPEN_POSITIONS` (intraday) | 585-618 | `legacy_total = active_count + processor_in_flight_count`; `authoritative_total = max(open_count + reserved_inflight, active_count) + 1`; `effective_total = max(legacy_total, authoritative_total)`; `if effective_total > self._max_open:` | `max_open_positions` 5 |
| 5a | `DAILY_TRADES` (delivery) | 652-658 | `if daily_delivery_count >= eff_max_daily_delivery:` | `max_daily_delivery_trades` 5 |
| 5b | `DAILY_TRADES` (intraday) | 660-671 | `authoritative_daily = settled_today + reserved_inflight_daily`; `effective_daily = max(daily_count, authoritative_daily)`; `if effective_daily >= self._max_daily:` | `max_daily_trades` 10 |
| 6 | `CONSECUTIVE_LOSSES` | 676-682 | `if consec >= self._max_consec:` (loss = `net_pnl < -1e-6`, today only) | `max_consecutive_losses` 4 (shared) |
| 7 | `DAILY_LOSS` | 692-731 | `limit = eff_daily_loss_pct * snap.total`; `enforced_pnl = daily_pnl + (unrealized if use_unrealized else 0.0)`; `if enforced_pnl < 0 and snap.total > 0 and abs(enforced_pnl) >= limit:` | 0.03 / 0.03; `daily_loss_include_unrealized: false` ⇒ realized-only |
| 8 | `SECTOR_EXPOSURE` | 735-763 | `projected = effective_sector_margin + margin_required`; `if projected > eff_max_sector_pct * snap.total:` → **reject only if `sector_cap_mode == "enforce"`**, else WARNING `risk_engine.sector_cap_would_reject mode=observe …` and continue | 0.40 / 0.40; `sector_cap_mode: observe` ⇒ **never rejects** |
| 9 | `CONTRARY_POSITION` | 768-786 | active trade in symbol with opposite direction | — |
| 10 | `DUPLICATE_SYMBOL` | 789-794 | `if has_dup:` → "Active position or in-flight order already exists for symbol" | — |

Notes [SRC]/[INF]:
- `count_live_reservations()` (fund_manager.py:1562-1576) counts **all** reservations (both books) in 4b and 5b; carried CNC positions count in the intraday 4b/5b totals (the "A5 asymmetry" the comment at :550-556 describes); intraday entries do not count toward 4a/5a.
- 4a/5a are **DB-only** (no reservation term), and they count a trade only once its ENTRY `orders` row with `product='CNC'` exists — that row is written inside `place()`, after the lock is released [INF on write timing].
- 4b `legacy_total` adds `processor_in_flight_count` to `active_count`; a concurrent candidate that has already created its PENDING_FILL row inside `place()` but not yet reached its `finally` is counted in both terms [INF, timing-dependent]; `max()` keeps the larger.
- 9/10 are product-blind: an active CNC position in X blocks an intraday entry in X. Same-direction/same-day in the **same** book is normally caught earlier by E4.
- 7 vs the post-trade breach: `FundManager.release_used` fires `on_daily_loss_breach` at the same pct (fund_manager.py:1347-1361) → `_make_daily_loss_cb` → EOD `fire_now` + SOFT_KILL (main.py:756-805), so check 1 / the pre-flight kill check normally pre-empts check 7 [INF]. Code comment: "IA-P6-06 — 0 ever" (:723-724) [CMT].
- `ApprovalResult.snapshot`/`checks_run` are not read by the caller (Flag §10.1).

### 5.7 E6 — `FundManager.reserve` [SRC] fund_manager.py:521-635
Call :1327-1335: `reserve(symbol, sizing.qty, entry_price, strategy_obj.intent, signal_id, strategy=strategy_name)`.
```python
bucket = self._bucket_for_intent(intent)
base_margin = required_margin(qty, price, intent, self._leverage_map)
slm_buffer = base_margin * self._slm_buffer_pct          # 0.05 (ctor default)
total_margin = base_margin + slm_buffer
avail_before = self._bucket_avail(bucket)
if total_margin > avail_before:
    return ReservationResult(success=False, reservation_id="", margin=total_margin, bucket=bucket,
        reason_if_failed=(f"Insufficient {bucket} capital: need {total_margin:.2f}, have {avail_before:.2f}"))
rid = uuid.uuid4().hex[:16]
self._write_ledger(... entry_type="RESERVE", amount=total_margin, ..., margin_delta=+total_margin)
self._apply_reserve(reservation_id=rid, bucket=bucket, margin=total_margin, ..., slm_buffer=slm_buffer, strategy=strategy)
self._check_invariant("reserve", rid)
```
- **What / how much / from what:** `qty × entry_price / leverage × 1.05`, from the intent's bucket `avail`. Intraday: `qty × entry / 5 × 1.05`; delivery: `qty × entry × 1.05`.
- Other failure: non-numeric/NaN/inf input → `success=False`, "Invalid numeric input: qty=…, price=…".
- `success=False` → :1337-1338 `_PipelineReject("RESERVE_FAILED", reservation.reason_if_failed)` → **`REJECTED_RESERVE_FAILED`**.
- [INF] Sizing and risk check 3 both use `margin_required` **without** the 5% buffer, so reserve can refuse an entry that check 3 passed when `margin_required ≤ avail < 1.05 × margin_required` (e.g. a capital-bound qty floored up to 1), or when another worker reserved between the sizer's unlocked snapshot and this call.
- Exceptions: not initialised → `RuntimeError`; ledger INSERT error → raised before any in-memory mutation; `CapitalInvariantViolation` → `_handle_invariant_violation` (hard_kill) then raise (:631-634) — here the reservation was already applied but its id is never returned, so the processor cannot release it. All three are non-`BrokerError` → **`PLACEMENT_FAILED`**. `RESERVE_BROKER_ERROR` unreachable [INF].
- Success: `ac.reservation_id = reservation.reservation_id` (:1340) → status **`RESERVED`** (:1344, inside the lock).

### 5.8 E8 — target [SRC] :1368 → :1901-1953
After the reservation. `_PipelineReject` sites: `REJECTED_NO_ATR_DATA` (:1915; status becomes `REJECTED_REJECTED_NO_ATR_DATA`), `UNKNOWN_TGT_METHOD` (:1938), `TGT_DISTANCE_TOO_SMALL` (:1946, `tgt_min_pct` 0.003). Released by the outer handler (reason `rejected_<check>`). [INF] Unreachable under current YAMLs: every strategy is `tgt_method: RISK_REWARD` with 1.5 and `sl_min_pct` ≥ 0.003 ⇒ target distance ≥ 0.0045·entry > 0.003; `atr_fallback_mode` absent from yaml → default `"WARN"` (config_loader.py:572).

### 5.9 E9 — Telegram alert [SRC] :1371-1380 → :486-555
Synchronous `notifier.send(...)` titled `"[{mode}] 🟢 INTRADAY SIGNAL — {symbol}"` for every intent; bounded by `alerts.telegram.send_deadline_seconds: 8` [CFG :393] (enforced telegram_notifier.py:611-614). Exceptions caught and logged. Sent **before** E10-E12, so an alert goes out for entries later refused by the late kill check, shutdown, throttle, or by `place()`.

### 5.10 E10/E11 — late kill switch and shutdown [SRC] :1389-1405
```python
if self._ks and self._ks.is_active("entry"):
    ...
    if ac.reservation_id:
        self._fm.release(ac.reservation_id, "kill_switch_after_pipeline")
        ac.reservation_id = None
    raise _PipelineReject("KILL_SWITCH_LATE", "Kill switch active before placement")
if self._stop_event.is_set():
    ... self._fm.release(ac.reservation_id, "shutdown_before_placement") ...
    raise _PipelineReject("SHUTDOWN", "System shutdown before placement")
```
`is_active("entry")` = SOFT_KILL or HARD_KILL. `release` here is **not** wrapped in try: if it raises, the reservation id is still set and the outer `except Exception` retries it (reason `placement_failed`).

### 5.11 E12 — entry throttle [SRC] :1410-1418 → entry_throttle.py:65-115
Ctor main.py:3596-3599 [CFG]: `min_gap_between_entries_sec` 20, `entry_burst_window_sec` 60, `entry_burst_max` 3, `per_symbol_cooldown_sec` 300. `admit()` is one atomic check-and-record under a lock, global first:
```python
if self._min_gap > 0 and self._last_entry is not None:
    gap = now - self._last_entry
    if gap < self._min_gap: return ThrottleResult(False, f"min_gap {gap:.1f}s < {self._min_gap:.0f}s", "min_gap")
if self._burst_max > 0:
    cutoff = now - self._burst_window
    while self._recent and self._recent[0] < cutoff: self._recent.popleft()
    if len(self._recent) >= self._burst_max: return ThrottleResult(False, f"burst {len(self._recent)} >= {self._burst_max}/{self._burst_window:.0f}s", "burst")
if self._per_symbol > 0 and symbol:
    last = self._per_symbol_last.get(symbol)
    if last is not None and now - last < self._per_symbol: return ThrottleResult(False, f"per_symbol {symbol} {elapsed:.0f}s < {self._per_symbol:.0f}s", "per_symbol")
self._last_entry = now; self._recent.append(now); self._per_symbol_last[symbol] = now
```
Clock `time.monotonic()`; in-memory only (reset on restart). Reject → release `"entry_throttled"`, `entries_throttled` metric, **`REJECTED_ENTRY_THROTTLED`**, reason `"Entry throttled: <gate reason>"`. The admission is recorded **before** `place()` and never rolled back, so a failed/timed-out/re-queued `place()` still uses up the 20 s gap, a burst slot and the 300 s symbol cooldown [SRC: no un-record call exists].

### 5.12 E13/E14 — dispatch and `place()` [SRC] :1420-1460
`self._fx_dispatch.inc()`; @970aabf only: `_evidence_capture("P1_ACCEPT", …)` — synchronous open+write+fsync; evidence_contract.py:495-501 [CMT] measured it on a dev PC at "mean 2.18 ms, p99 3.1 ms" and calls the VM "UNMEASURED". Can't raise (guarded :589-612). Then:
```python
self._placer.place(symbol=symbol, side=side, qty=sizing.qty, entry_price=entry_price, sl_price=sl_price,
    intent=strategy_obj.intent, signal_id=signal_id, reservation_id=ac.reservation_id, strategy=strategy_name,
    tgt_price=tgt_price, signal_trigger_price=trigger_price, sizing_breakdown=sizing.breakdown,
    tgt_risk_reward=getattr(strategy_obj, "tgt_risk_reward", None))
ac.reservation_id = None   # placer owns it now
```
**How the reservation interacts with the placer [SRC]:** the id is written to `trades.reservation_id` (order_placer.py:1009); `trades.margin_reserved = self._fm.required_margin(qty, entry_price, intent)` (base, **no** 5% buffer, :971-973); price drift > `risk.price_drift_threshold` 0.005 → `top_up_reservation` (:1195-1258), failure → `REJECTED_PRICE_DRIFT` trade + `OrderRejectedError`; placer-side failures call `_handle_placement_failure` → `self._fm.release(reservation_id, f"placement_failed: {exc}")` (:4451-4454); on fill `commit_to_used` pops it. If `place()` raises after its own release, the processor's second `release` is a no-op (`release` returns False for an unknown id, fund_manager.py:651-653).

**After `place()` (outside the stretch, for completeness):** `BrokerTimeoutError` → status **`TIMEOUT`**, reservation deliberately **kept** (`ac.reservation_id = None` without release) for the reconciler (:1464-1484). `BrokerRateLimitError` with `retry_count < 3` → re-queue a dict with `retry_count+1`, release reservation `"requeued_transient_error"`, keep the symbol claim (:1486-1525); `queue.Full` or `retry_count >= 3` → re-raise → `PLACEMENT_FAILED`. Other `BrokerError` → `record_api_failure` + re-raise → `PLACEMENT_FAILED`. Success → **`PROCESSED`** (:1543) + SR observer.

---

## 6. Every reject site from "screener PASSED" to `place()` (in order)

`status` = value written to `signals.status` via `update_signal_status(signal_id, f"REJECTED_{rej.check}", rej.reason)` (:1201) unless stated; `rejection_reason` = the reason text. "Resv" = a reservation exists at that point.

| # | line @970aabf | check / condition | status written | reason text | Resv? | reachable @970aabf config |
|---|---|---|---|---|---|---|
| 1 | :1028→:1789 | derived `entry_price <= 0` | `REJECTED_INVALID_DERIVED_PRICE` | "entry_price=… <= 0 (trigger=…, offset=…, method=…). Check strategy.entry_offset_pct < 1.0." | no | Agent A |
| 2 | :1028→:1804 | `sl_method=="ATR"` and mode HALT | `REJECTED_REJECTED_NO_ATR_DATA` | "sl_method=ATR not implemented and atr_fallback_mode=HALT" | no | no (no ATR strategy; WARN) |
| 3 | :1028→:1826 | FIXED_PCT `sl_pct <= 0` | `REJECTED_ZERO_SL` | "sl_pct=… in FIXED_PCT branch …" | no | Agent A |
| 4 | :1028→:1843 | unknown `sl_method` | `REJECTED_INVALID_DERIVED_PRICE` | "Unknown sl_method: …" | no | Agent A |
| 5 | :1098 | rows 1-4 again on the M-S1 live-LTP re-derivation | same | same | no | Agent A |
| — | :1042-1056 | SNR-V2 divert → `return` (no processor status write) | — | — | no | dormant (`wait_for_retest_enabled: false`) |
| 6 | :1122-1125 | `BrokerError` from `calculate()` | `REJECTED_SIZING_BROKER_ERROR` | `str(be)` | no | no [INF] |
| 7a | :1127 / ps:429 | `sl_distance < 0.05` | `REJECTED_SIZING_INVALID_SL_DISTANCE` | "sl_distance=… < min_tick_size=0.05 for SYM …" | no | yes |
| 7b | :1127 / ps:461 | `qty_by_risk > 10000` | `REJECTED_SIZING_QTY_EXPLOSION_GUARD` | "qty_by_risk=… > max_single_order_qty=10000 …" | no | capital-dependent |
| 7c | :1127 / ps:524 | `raw_qty <= 0` | `REJECTED_SIZING_CAPITAL` / `_RISK` / `_CONCENTRATION` | "qty=0: {constraint} exhausted for SYM (risk_qty=… capital_qty=… conc_qty=…)" | no | yes |
| 7d | :1127 / ps:565 | `effective_mult <= 0` | `REJECTED_SIZING_ZERO_MULTIPLIER` | "qty=0: ZERO_MULTIPLIER for SYM — …" | no | no |
| 7e | :1127 / ps:656 | `final_qty > 10000` | `REJECTED_SIZING_QTY_EXPLOSION_GUARD` | "final_qty=… > max_single_order_qty=10000 …" | no | latent [CMT] |
| 7f | :1127 / ps:688-705 | lot≠1 and skew > 0.25 | `REJECTED_SIZING_REJECTED_LOT_SKEW` | "REJECTED_LOT_SKEW for SYM: skew=…" | no | only if lot_size > 1 |
| 7g | :1127 / ps:723 | `qty×entry > 0.40×total` | `REJECTED_SIZING_POSITION_VALUE_CAP` | "position_value=… > max=… (40% of capital …)" | no | no [INF] |
| 7h | :1127 / ps:754 | `final_qty < lot` or `< 1` | `REJECTED_SIZING_BELOW_MIN` | "qty=… below minimum for SYM: tier=…" | no | no with lot 1 [INF] |
| 8 | ps:316-339, :216-243 | `ValueError` (PS8 validation / missing delivery key) | `PLACEMENT_FAILED` (outer `except Exception`) | `str(exc)` | no | no in normal operation |
| — | :1136-1143 | V3 observe | — | — | no | cannot reject |
| — | :1147-1172 | allocator (shadow) | — | — | no | cannot reject |
| 9 | :1311→:774 | H-7 `effective > max_concurrent_positions` | `REJECTED_STRATEGY_POSITION_LIMIT` | "{strategy} at cap: n/max open+in-flight (…)" | no | yes |
| 10 | :1312→:859 | `n >= 1` executed today, same symbol+direction+book | `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` | "SYM LONG already traded today in the intraday book (n executed trade(s)); …" | no | yes |
| 11 | :1319-1322 | `BrokerError` from `approve` | `REJECTED_RISK_BROKER_ERROR` | `str(be)` | no | no [INF] |
| 12 | :1324-1325 | risk checks 1-10 (table §5.6) | `REJECTED_KILL_SWITCH` · `_SIZING_VALID` · `_CAPITAL` · `_OPEN_POSITIONS` · `_DAILY_TRADES` · `_CONSECUTIVE_LOSSES` · `_DAILY_LOSS` · `_SECTOR_EXPOSURE` · `_CONTRARY_POSITION` · `_DUPLICATE_SYMBOL` | `approval.reason` | no | SIZING_VALID never; SECTOR never (observe) |
| 13 | :1332-1335 | `BrokerError` from `reserve` | `REJECTED_RESERVE_BROKER_ERROR` | `str(be)` | no | no [INF] |
| 14 | :1337-1338 | `reservation.success == False` | `REJECTED_RESERVE_FAILED` | "Insufficient {bucket} capital: need X, have Y" / "Invalid numeric input: …" | no | yes |
| 15 | reserve raises | `RuntimeError` / ledger error / `CapitalInvariantViolation` | `PLACEMENT_FAILED` | `str(exc)` | invariant case: applied, id lost | edge |
| — | :1344 | success | `RESERVED` | — | **yes** | — |
| 16 | :1351-1363 | `self._placer is None` | `PROCESSED_NO_PLACER` (released `"no_order_placer"`) | — | released | no (placer always built, main.py:3061) |
| 17 | :1368→:1915/:1938/:1946 | target derivation | `REJECTED_REJECTED_NO_ATR_DATA` / `REJECTED_UNKNOWN_TGT_METHOD` / `REJECTED_TGT_DISTANCE_TOO_SMALL` | as coded | **yes** → released by handler (`rejected_<check>`) | no [INF] |
| 18 | :1389-1396 | kill switch SOFT/HARD | `REJECTED_KILL_SWITCH_LATE` | "Kill switch active before placement" | released first (`kill_switch_after_pipeline`) | yes |
| 19 | :1398-1405 | `self._stop_event.is_set()` | `REJECTED_SHUTDOWN` | "System shutdown before placement" | released first (`shutdown_before_placement`) | yes |
| 20 | :1410-1418 | throttle gate | `REJECTED_ENTRY_THROTTLED` | "Entry throttled: min_gap …" / "burst …" / "per_symbol …" | released first (`entry_throttled`) | min_gap & per_symbol yes; burst practically no [INF] |

The `signals.status` CHECK accepts every `REJECTED*` value via `GLOB 'REJECTED*'` (core/schema.sql:60-70).

---

## 7. The exception handlers (catch every row above) [SRC]

**H1 — `except _PipelineReject as rej:`** signal_processor.py:1193-1231 (**:1081 @d3ee69d**)
```python
self._log.info(f"Signal {signal_id} ({symbol}) rejected at {rej.check}: {rej.reason}")
if rej.check != "ENTRY_THROTTLED":
    self._bump_metric("entries_rejected")
self._store.update_signal_status(signal_id, f"REJECTED_{rej.check}", rej.reason)
self._evidence_capture("P2_REJECT", lambda: {...})        # 970aabf only; never raises
if reservation_id:
    try:
        self._fm.release(reservation_id, f"rejected_{rej.check.lower()}")
    except Exception as rel_exc:
        self._log.error(f"Failed to release reservation {reservation_id}: {rel_exc}")
with self._stats_lock: bucket[rej.check] += 1
if rej.check == "EXPIRED" and self._notifier: ... (rate-limited warning; pre-screen reject only)
```
**H2 — `except Exception as exc:`** :1233-1246 (**:1111 @d3ee69d**)
```python
self._log.error(f"Pipeline exception for {signal_id} ({symbol}): {exc}\n{traceback.format_exc()}")
self._store.update_signal_status(signal_id, "PLACEMENT_FAILED", str(exc))
if reservation_id:
    try: self._fm.release(reservation_id, "placement_failed")
    except Exception as rel_exc: self._log.error(...)
bucket["PLACEMENT_FAILED"] += 1
```
**H3 — `finally:`** :1248-1276: decrement `_in_flight_count` only `if in_flight_incremented`; release the receiver's symbol claim `if not requeued and not handed_off and self._in_flight_release is not None`; add elapsed ms to stats.

**H4 — `_process_one_safe`** :465-480 catches anything escaping `_process_one` (e.g. a failing status write inside H1/H2) → `update_signal_status(signal_id, "PLACEMENT_FAILED", f"unhandled: {exc}")` (wrapped).

[SRC] Ordering inside H1 and H2: the status write comes **before** the release and is not wrapped, so if that DB write raises, the release is skipped (H3 still runs; H4 writes `PLACEMENT_FAILED`).

---

## 8. Other limits touched in `_process_one` after screening — summary

| limit | where | scope | config | can reject? |
|---|---|---|---|---|
| per-strategy concurrent cap (H-7) | :744-779 | strategy; DB all-dates + tagged reservations | YAML `max_concurrent_positions` 2/3 | yes |
| one per symbol+direction+book/day | :802-864 | DB, today, product-scoped | `risk.one_trade_per_symbol_direction_per_day: true` | yes |
| max open positions | risk :543-618 | intraday: global+reservations+processor in-flight; delivery: DB CNC | 5 / 3 | yes |
| daily trades | risk :620-671 | intraday: max(DB, settled+reservations); delivery: DB CNC | 10 / 5 | yes |
| consecutive losses | risk :673-682 | today, shared | 4 | yes |
| daily loss (pre-trade) | risk :684-731 | realized net today vs pct×total | 0.03/0.03; unrealized = shadow | yes (normally pre-empted by kill) |
| sector exposure | risk :733-763 | sector margin + reservations | 0.40/0.40; **observe** | **no** |
| contrary / duplicate symbol | risk :765-794 | DB, product-blind | — | yes |
| capital (risk) / reserve | risk :529-541; fm :567-577 | bucket avail (reserve adds 5%) | 70/30; leverage | yes |
| kill switch | risk :516-519; :1389-1396 | SOFT/HARD | — | yes |
| shutdown | :1398-1405 | stop_event | — | yes |
| entry throttle | entry_throttle.py:65-115 | global gap/burst + per-symbol | 20 s; 3/60 s; 300 s | yes (burst: practically no) |
| receiver symbol claim | webhook_receiver.py:1074-1108 | one in-flight signal per symbol | sweeper 60 s | not in this stretch; released at :1267 |
| FIX-018 in-flight count | :1302-1305 | feeds 4b only | — | indirect |
| strategy circuit breaker / strategy control / windows / expiry | :906-990 | **pre-screen** (not re-checked after screening) | — | n/a here |

---

## 9. Config keys read in this stretch — values @970aabf

| key | value | read at | effect in this stretch | can change behaviour? |
|---|---|---|---|---|
| `capital.intraday_bucket_pct` | 0.70 (yaml :197) | main.py:2706 → FM ctor | intraday base | yes |
| `capital.positional_bucket_pct` | 0.30 (:198) | main.py:2707 | positional base | yes |
| `capital.conditional_allocation_enabled` | false (:199) | main.py:2703 | fixed split | yes |
| `capital.leverage_map.INTRADAY/COVER_ORDER/DELIVERY/BRACKET_ORDER` | 5.0 / 6.0 / 1.0 / 5.0 (:207-211) | main.py:2678-2683 | sizer divisor + reserve margin | yes (bounded [1.0, 10.0] by `leverage_safety`, config_loader.py:389-409) |
| `capital.slm_margin_buffer_pct` | 0.05 (:203) | **not passed** to FundManager (main.py:2718-2736) | reserve uses the ctor default 0.05 | **no** |
| `position_sizing.enabled` | true (:220) | main.py:2855 | ON (tier×perf) mode | yes |
| `position_sizing.flat_value_rs` | absent (commented :223) → None | main.py:2856 | OFF mode only | inert while ON |
| `position_sizing.risk_per_trade_pct` | 0.01 (:225) | main.py:2843 | intraday risk qty | yes (label rarely binds [INF]) |
| `position_sizing.max_concentration_pct` | 0.10 (:226) | main.py:2844 | intraday conc qty | yes |
| `position_sizing.min_qty_threshold` | 1 (:227) | main.py:2845 | BELOW_MIN | yes (moot at 1) |
| `position_sizing.lot_skew_rejection_threshold` | 0.25 (:228) | main.py:2853 | lot skew | only if lot > 1 |
| `position_sizing.min_tick_size` | 0.05 (:229) | **not passed** (sizer default 0.05) | Guard 1 | **no** |
| `position_sizing.max_single_order_qty` | 10000 (:230) | **not passed** (sizer default 10000) | Guard 2 in/out | **no** |
| `position_sizing.max_position_value_pct` | 0.40 (:236) | main.py:2854 | position value cap | cannot bind [INF] |
| `position_sizing.tier_multipliers` | HIGH 1.0 / MEDIUM 0.70 / LOW 0.50 (:237-240) | main.py:2846-2850 | tier multiplier | yes |
| `position_sizing.dynamic_by_winrate` | true (:241) | main.py:2871 (log only) | none | **no** |
| `position_sizing.min_multiplier` / `max_multiplier` | 0.5 / 2.0 (:242-243) | config_auditor / dashboards only | none | **no** |
| `position_sizing.delivery_risk_per_trade_pct` | 0.01 (:253) | main.py:2860 | delivery risk qty | yes |
| `position_sizing.delivery_max_concentration_pct` | 0.10 (:254) | main.py:2861 | delivery conc qty | yes |
| `position_sizing.delivery_max_position_value_pct` | 0.40 (:259) | main.py:2862 | delivery cap | cannot bind [INF; yaml comment agrees] |
| `risk.max_open_positions` | 5 (:271) | main.py:2899 | check 4b | yes |
| `risk.max_daily_trades` | 10 (:272) | main.py:2900 | check 5b | yes |
| `risk.max_open_delivery_positions` | 3 (:283) | main.py:2918 | check 4a | yes |
| `risk.max_daily_delivery_trades` | 5 (:284) | main.py:2919 | check 5a | yes |
| `risk.one_trade_per_symbol_direction_per_day` | true (:302) | main.py:2901 | E4 | yes |
| `risk.max_sector_exposure_pct` / `delivery_max_sector_exposure_pct` | 0.40 / 0.40 (:313-314) | main.py:2902, :2923 | check 8 | **no while `sector_cap_mode: observe`** |
| `risk.max_consecutive_losses` | 4 (:315) | main.py:2903 | check 6 | yes |
| `risk.daily_loss_limit_pct` / `delivery_daily_loss_limit_pct` | 0.03 / 0.03 (:316-317) | main.py:2904, :2924 (+ FM :2727) | check 7 + post-trade breach | yes |
| `risk.sector_cap_mode` | observe (:322) | main.py:2911 | check 8 log-only | yes (it is the switch) |
| `risk.daily_loss_include_unrealized` | false (:324) | main.py:2906 | realized-only | yes (it is the switch) |
| `risk.price_drift_threshold` | 0.005 (:325) | OrderPlacer | top-up inside `place()` | downstream |
| `signal_processor.worker_count` | 5 (:345) | main.py:3590 | concurrency | yes |
| `signal_processor.pipeline_timeout_sec` | 30 (:347) | config_loader.py:568 only — **no reader** | none | **no** |
| `signal_processor.tgt_min_pct` | 0.003 (:348) | main.py:3594 | E8 | cannot bind [INF] |
| `signal_processor.atr_fallback_mode` | absent → "WARN" (config_loader.py:572) | main.py:3593 | rows 2/17 | no ATR strategies |
| `signal_processor.min_gap_between_entries_sec` | 20 (:350) | main.py:3596 | throttle | yes |
| `signal_processor.entry_burst_window_sec` / `entry_burst_max` | 60 / 3 (:351-352) | main.py:3597-3598 | throttle | practically no [INF] |
| `signal_processor.per_symbol_cooldown_sec` | 300 (:353) | main.py:3599 | throttle | yes |
| `kill_switch.api_failure_threshold` / `enable_auto_trip` | 3 / true (:356-357) | KillSwitch | `record_api_failure` counts only `BrokerTimeoutError`/`BrokerRateLimitError` (kill_switch.py:842-850) | yes |
| `portfolio_allocator.allocator_mode` / `enforce_scope` | "shadow" / "v3_only" (:565-566) | main.py:3633 | stage D | yes (switch) |
| `v3_chain.v3_chain_mode` / `max_queue` / `would_be_log_path` | "shadow" / 512 / data_store/v3/would_be.jsonl (:574, :616-617) | main.py:3473, runner | stage C | shadow only |
| `alerts.telegram.send_deadline_seconds` | 8 (:393) | main.py:2640 | E9 blocking bound | timing only |
| `scoring_weights.high_score_threshold` / `medium_score_threshold` / `min_pass_score` | 80 / 65 / 60 | QualityScorer | tier → multiplier | yes |
| strategy YAML `intent` | INTRADAY ×13 (incl. disabled pb01), DELIVERY ×3 (positional_*) — 16 files | loader | bucket/limits | yes |
| strategy YAML `lot_size` | 1 (all 16) | :1119 | replaced by instrument cache | — |
| strategy YAML `max_concurrent_positions` | gap_fade_long/short, gap_go_long/short = 3; all others = 2 | :760 | H-7 | yes |
| strategy YAML `pullback_wait_enabled` | true: first_pullback_long/short, open_high_breakdown_short, open_low_breakout_long, vwap_bounce_long, vwap_rejection_short; false: the rest | :1082 | M-S1 re-anchor → sizing inputs | yes |
| strategy YAML `enabled` | all true except `pb01_breakout_retest` (false) | pre-screen | — | — |

---

## 10. Flags (description only)

### 10.1 Computed but read by nothing
1. `SizingResult.risk_amount` (position_sizer.py:782) — no production reader (grep of `sizing.risk_amount` / `sizing_result.risk_amount` = 0 hits); order_placer computes its own (order_placer.py:965).
2. `ApprovalResult.snapshot` and `.checks_run` (risk_engine.py:378-388, :797-803) — the caller reads only `approved`, `failed_check`, `reason` (0 hits for `approval.snapshot`/`approval.checks_run`); `count_in_flight_orders()` (:305) and `sector_pct` (:372-375) feed only that snapshot (+ the observe-mode log).
3. `SignalProcessor._sector_for` (:1605-1617) probes `sector_for`/`get_sector`; `InstrumentCache` defines only `sector()` (core/instrument_cache.py:257) → always `"UNKNOWN"`. The result goes to `V3Signal.sector` and `ScoredCandidate.sector`, and neither runner reads it (v3_chain reads only `step_results, scanner_name, side, intent, score, tier` + ids/prices; allocation never reads `.sector`).
4. `V3Signal.market_data`, `.trigger_price`, `.triggered_at`, `.v3_playbook`, `.sector` — not read by `V3ChainRunner`.
5. The sizing breakdown on **reject** paths is discarded; on success the keys `raw_qty, tier_multiplier, tiered_qty, tier_mult, perf_weight, rung_before_multiplier` are not persisted by `create_trade` (read only by the P1 evidence record @970aabf; nothing at d3ee69d).
6. The sizer's `get_snapshot()` runs `get_daily_realized_net_pnl` SQL; the sizer uses only `total` and the bucket avail.
7. `_heartbeat()` (:664-673) — `in_flight_heartbeat_fn` is not passed at main.py:3575-3623 (no non-test code passes it, and `webhook_receiver.update_heartbeat` (:1110) has no caller), so all five checkpoints are no-ops; the receiver sweeper evicts claims with no heartbeat for > 60 s (webhook_receiver.py:208, :1189-1198).
8. `_admit_and_place(..., now)` — the `now` parameter is not used in its body.

### 10.2 Config keys read (or present) that cannot change behaviour
- `position_sizing.min_tick_size`, `position_sizing.max_single_order_qty` — loaded (config_loader.py:466-467) but not passed at main.py:2840-2863; the sizer defaults (0.05 / 10000) happen to equal the yaml values.
- `capital.slm_margin_buffer_pct` — loaded (config_loader.py:345), not passed to FundManager; default 0.05 equals the yaml value.
- `position_sizing.dynamic_by_winrate`, `min_multiplier`, `max_multiplier` — no `PerformanceAllocator` is instantiated anywhere in production (only its class and docstring, capital/performance_allocator.py:36-41) and `perf_weights` is never passed → `perf_weight = 1.0`. The boot print at main.py:2873 says "x perf_weights". A test docstring (tests/integration/test_q9_sizing_floors_caps_wired.py:64-67) states the same and claims "perf_weight_applied = 1.0 on 298 of 298 sized production trades" [CMT — not verified].
- `signal_processor.pipeline_timeout_sec: 30` (yaml comment "hard per-signal processing deadline") — no reader.
- FIX-072 live-margin branch — `broker_adapter` not passed to `PositionSizer` → static leverage always.
- FIX-007 rate-limiter pre-check in `_process_one_safe` (:418-461) — `rate_limiter` is not passed to `SignalProcessor` (main.py passes it only to ZerodhaAdapter :2385 and SmartTgtManager :2985) → dead.
- `position_sizing.flat_value_rs` — inert while `enabled: true`.

### 10.3 Looks like a limit but cannot reject (in this path, @970aabf config)
- risk check 2 `SIZING_VALID` — `sizing.success` is checked first at :1127.
- risk check 8 `SECTOR_EXPOSURE` — `sector_cap_mode: observe` → WARNING only (risk_engine.py:746-763).
- DAILY_LOSS unrealized term — `daily_loss_include_unrealized: false` → shadow log only (:711-720).
- `entry_burst_max: 3 / 60 s` [INF]: `min_gap` (20 s) is checked first, so three admitted entries are ≥ 40 s apart and a fourth is ≥ 60 s after the first; the burst gate (pops `< cutoff`) can only fire when that gap is exactly 60.000… s.
- sizer `POSITION_VALUE_CAP`, `ZERO_MULTIPLIER`, `MULTIPLIER` label, `BELOW_MIN` (lot 1), RISK label on success for intraday [INF, §1.7].
- `SIZING_BROKER_ERROR`, `RISK_BROKER_ERROR`, `RESERVE_BROKER_ERROR` — no broker call outside a swallowing `try` in `calculate`/`approve`/`reserve` [INF].
- E8 `TGT_DISTANCE_TOO_SMALL`, `UNKNOWN_TGT_METHOD`, `REJECTED_NO_ATR_DATA` [INF, §5.8].
- `PROCESSED_NO_PLACER` — placer always constructed.
- allocator `_passes_portfolio_rules` caps — `max_portfolio_deployment_pct: null`, `long_short_skew_max: null`, and shadow only.
- V3 gates — log-only by construction.

### 10.4 Comments that contradict (or no longer describe) the code
- position_sizer.py:295-298 — "order_placer places at entry_price * (1 + entry_offset_pct), so margin must account for this": the processor never passes `entry_offset_pct` (→ 0.0), the price it passes is already the offset LIMIT price, and the placer places at the price it receives.
- position_sizer.py:283-285 docstring formula `tiered_qty = floor(raw_qty * tier_multiplier)` leaves out `perf_weight` and the FIX-133 `max(1, min(tiered, 2×raw))` floor/cap (:602-605).
- position_sizer.py:387 "FIX-072: Try live margin from broker API first" — never wired.
- fund_manager.py:561 "Buffer is held until SL-M is accepted, then released via release_slm_buffer()" — `release_slm_buffer` has no production caller; the 5% buffer stays in the reservation until release/commit (at commit it comes back as `excess`).
- risk_engine.py:12-13 (RE2) and :278-281 — "Uses SizingResult.margin_required and SizingResult.risk_amount directly": `risk_amount` is never read.
- risk_engine.py:92-93 — "checks_run … Shorter than 9 on rejection": there are 10 checks.
- signal_processor.py:1074-1076 — "Pullback strategies skip this (EntryGate already waits for current price)": no production code calls `EntryGate.add()` (only its docstring example, screening/entry_gate.py:103; the 970aabf comment at :2236-2238 says the same). Pullback strategies go straight from the trigger-derived prices to sizing/reservation/placement with no re-anchor.
- signal_processor.py:1489 — "Max 3 retries (45s total, 15s each)": the re-queue has no delay (`self._queue.put(signal_dict, timeout=1.0)`), and the retry comes back through the throttle, which recorded the first attempt → it meets `min_gap` 20 s / `per_symbol` 300 s [INF on dispatch timing].
- v3_chain/models.py:45 — `as_of … (= now at emit time)`: the processor passes `now` from :910 (before screening/sizing).
- allocation/portfolio_allocator.py:181 — "per-sector 0.40 is enforced there": the risk gate is in observe mode.
- `_emit_signal_alert` title is always "INTRADAY SIGNAL" (:547), also for DELIVERY; body text "(LIMIT)", "Priority rank: #1 of 1", "Timeout: 10 min" is hardcoded (:533-544).

### 10.5 Other ownership / ordering observations
- `release_slm_buffer` (:744-755) and `top_up_reservation` (:858-869) rebuild `_Reservation` without `strategy=` → the H-7 tag is lost. The top-up runs inside `place()` after `create_trade`, so H-7's DB floor (`active_incl_pending`) still counts that trade.
- The throttle records the admission before `place()`; nothing un-records it on failure (§5.11).
- The Telegram alert is sent before E10-E12 and before `place()` (§5.9).
- A reserve `CapitalInvariantViolation` leaves an applied reservation whose id the processor never gets (§5.7).
- Sizing reads capital outside `portfolio_lock`; risk and reserve re-read inside it. The qty is not re-sized inside the lock.
- No signal-age / expiry re-check after screening (only at :915-921).

---

## 11. Sibling entry paths that reuse these helpers (brief)
- `continue_from_gate` (:2010-2369): same sizing (:2107-2124), H-7 + one-per-day + approve + reserve under the lock (:2138-2171), late kill / shutdown / throttle; no M-S1, no V3, no allocator; target comes from the WatchEntry. Reachable only through `gate_state` rows rehydrated at boot (no `EntryGate.add()` caller).
- `continue_from_retest` (:2375-2640): dormant (`wait_for_retest_enabled: false`); `_derive_target` runs **before** the reservation; MARKET entry.
- `admit_prepared` / `reject_prepared` (:1646-1737): enforce-allocator only; dormant in shadow.
