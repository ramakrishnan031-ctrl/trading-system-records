# EXECUTION MECHANICS — THE REMAINING UNKNOWNS — REPORT

**Card:** "FOR VS CODE CLAUDE — EXECUTION MECHANICS: THE REMAINING UNKNOWNS — REPORT ONLY", 15-Sep-2026 (pasted into this session).

**Builds on:**
- **FF** = `docs/audit/ENTRY_EXECUTION_FACT_FINDING_15-Sep-2026.md`
- **PPV** = `docs/audit/PRICE_PATH_VALIDATION_15-Sep-2026.md`

Items the card's §0 lists are cited, not re-established.

**Date of work:** 15-Sep-2026 (Tue), IST evening.

**Nature:** REPORT ONLY.
- No code, config, commit, push, deploy, service action or broker call.
- No fix is proposed, nothing is ranked, and IOC is not recommended.
- The §1 settled contract is context only and is not re-opened.

**Production VM:** not contacted. `origin` was not contacted either.

**Testing VM (130.210.13.114, `trading-sbx`):** read-only.
- SQLite scripts were fed on stdin (`python3 -B -`) with `mode=ro` and `PRAGMA query_only=1`.
- Other reads used `grep -c`, `sed -n`, `md5sum` and `systemctl show`.
- **No file was created anywhere on the VM, `/tmp` included.** Every result streamed to stdout.

**How it was done:** one thread, direct reading, no subagents and no workflow, per the card. The card names Sonnet 4.6 High; **this session ran on Opus 5**.

---

## THE FOUR ANSWERS THE DESIGN WAITS ON

> **Q2(e).** Yes — the tick snap is the last change to the entry price: nothing after `_snap_order_to_tick` modifies it, kiteconnect forwards it unchanged, and the form-encoded value sent equals the snapped value.
>
> **Q3(e).** No — the system cannot prove that a LIMIT at P is marketable, because at submission it holds only a REST quote already 0.3–13 s old (last price plus top-of-book bid/ask prices, with no sizes and no exchange timestamp), and no entry decision reads bid or ask.
>
> **Q4(c).** No store is authoritative in code for "this entry can still create exposure": each selector reads its own local proxy (`trades.status`, `orders.status`, the monitor's in-memory tracked set, or in-memory FundManager reservations), and only the monitor's per-order broker poll and the reconciler's broker reads see broker truth.
>
> **Q5(e).** No schema change is unavoidable, but existing local data cannot recover everything: stop, target, direction and requested quantity sit in fully populated columns, while the submitted price and the filled quantity sit in existing columns (`orders.price`, `orders.qty_filled`) that are never written for ENTRY rows, so after a restart only the broker's order record holds them.

---

## 0. SOURCES, IDENTITY, MARKERS

### 0.1 Sources

| Label | Source | State at measurement |
|---|---|---|
| **WT** | Working tree `D:/Projects/trading-system` | `feat/delivery-config-split` @ `6d24a83` plus pre-existing uncommitted edits (same state as FF and PPV) |
| **TW** | Deployed tree on the testing VM | Read from the FF snapshot. 13 key files re-hashed on the VM at 19:29:40 IST; all identical to the snapshot. Service `inactive` after its 17:35 self-exit; `ExecMainStartTimestamp` 08:15:23. |
| **TW-DB** | `data_store/trading_system.db` on the VM | Read-only |
| **TW-LOG** | `logs/system_2026-09-*.log` (and `debug_*` where stated) | Only 03, 04, 07, 08, 09, 10, 11 and 15 Sep exist |
| **TW-LIB** | `/home/ubuntu/systems/venv/lib/python3.12/site-packages/kiteconnect/connect.py` (5.1.0, md5 b1bc8ad3) · `…/requests/models.py` (2.33.1, md5 f384ae6f) · VM `python3` 3.12.3 stdlib | Read-only |
| **BOOK** | `docs/incident/2026-09-03_ANANTRAJ_broker_book.json` | Kite order book plus 3 order histories, pulled 2026-09-03T16:51:42. **EVIDENCE:** a broker record for one day. |
| **HARNESS** | Session-scratch `em_q56_harness.py` (§11) | Drives the **unchanged** WT `OrderMonitor` and `OrderStateMachine` (both md5-identical to TW) with a stub broker, bus and store. Local Python 3.11.9, run with `-B`. The `broker/__pycache__` and `core/__pycache__` listings were hashed before and after and are unchanged. No repo file was modified. |

### 0.2 File identity (md5 prefix; WT vs TW)

**Identical in both trees:**

| File | md5 |
|---|---|
| `broker/order_monitor.py` | 60ab959e |
| `broker/order_state_machine.py` | 9cdae67d |
| `orders/order_placer.py` | c337d5c3 |
| `orders/order_protocol_limit.py` | d675d15e |
| `orders/eod_squareoff.py` | 1607e3f5 |
| `screening/step_executor.py` | c13af795 |
| `orders/shadow_tracker.py` | cd75d0cc |
| `orders/structure_exit_manager.py` | 85a65089 |
| `scripts/eod_cleanup.py` | 2ca9cfa8 |
| `core/events.py` | de8306a3 |
| `core/exceptions.py` | b6cf5f0e |
| `core/effect_telemetry.py` | 53fc8ab2 |

**Different:**

| File | WT | TW |
|---|---|---|
| `broker/zerodha_adapter.py` | 124ed3fa | 1a237b8c |
| `orders/order_manager.py` | 6ea73f0c | 39edfcbf |
| `core/state_store.py` | e8c24a7d | 45d83a94 |
| `orders/order_reconciler.py` | 1850b215 | 8a0125bd |
| `capital/fund_manager.py` | da4b3fdd | 9ff45f66 |
| `capital/kill_switch.py` | 3fa519a1 | 90848bfc |
| `capital/risk_engine.py` | 629c7b32 | 37ea201b |
| `orders/slippage_recorder.py` | e6ad4fcd | b9b0ab21 |
| `screening/secondary_screener.py` | 15f0b37d | ae04e45b |
| `signals/signal_processor.py` | 858e2ce3 | da8c6f98 |
| `main.py` | 9907c93f | 85219d22 |
| `core/schema.sql` | 01a040f7 | abe7cb19 (hashed on the VM). The `trades` DDL sits at the same lines; the `orders` DDL is WT 333 / TW 315 with the same cited text. |
| `orders/mis_autosquareoff.py` | absent | bdfab9b2 (TW only) |

**Function-level parity inside the differing files** (AST source hash of each cited function):

**MATCH:**
- **state_store:** `get_open_orders_for_rehydration`, `get_orphaned_pending_trades`, `get_pending_intraday_orders`, `get_pending_all_products`, `get_all_open_trades`, `get_open_intraday_positions`, `get_pending_exit_orders_for_open_positions`, `get_trades_for_date`, `has_active_position`, `get_active_position_direction`, `count_in_flight_orders`, `count_active_positions`, `get_trades_by_status_and_symbol`, `fail_recovery_trade`, `mark_recovery_trade_exiting`, `revert_exiting_to_open`, `cancel_stale_paper_orders`
- **order_manager:** `_on_order_status_changed`, `update_order_status`, `insert_orders_atomic`, `insert_order`, `record_entry_fill`, `update_trade_status`, `close_trade`
- **order_reconciler:** `reconcile_once`, `sweep_stale_orders`, `_check2_inflight_orphan`, `_check2_orphan_adoption`, `_detect_system_oversell`, `_position_is_naked`, `_recover_in_flight_entries`, `_backfill_entry_order_row`, `_check5_position_grew`, `_check6_orphan_orders`, `_mark_order_cancelled_local`, `_cancel_orphaned_orders_for_trade`
- **fund_manager:** `commit_to_used`, `commit_adopted_entry`, `_restore_reserve_from_ledger`, `count_live_reservations`, `release`
- **adapter:** `get_order_history`, `get_quote`, `get_quote_raw`, `cancel_order`, `_snap_order_to_tick`, `_paper_place_order`, `_synth_fill`, `get_open_orders`, `get_all_orders`
- **kill_switch:** `_cancel_trade_resting_exits`, `_exit_all_trades_indestructible`, `_mark_trade_exiting`
- **slippage_recorder:** `_on_order_filled`
- **secondary_screener:** `_build_market_data`

**DIFFERS:**

| Function | What differs; what the cited part says |
|---|---|
| `create_trade` | The `'PENDING_FILL'` INSERT literal is the same (WT 240 / TW 236) |
| `rehydrate_from_open_trades` | Both walk `self._store.get_all_open_trades()` (WT 1844 / TW 1788) |
| `top_up_reservation` | Not cited for logic |
| `_validate_place_order` | Both raise only; no rebinding of `price` |
| `soft_kill` | Neither version contains `cancel_order`, `place_order` or `UPDATE` |
| `place_order` | TW adds only the pass-through `market_protection` |
| Position-cap formula | TW 607 counts `_count_res()` account-wide; WT 669 counts `self._live_reservations(policy)`. **DIFFERS-LOGIC** in scope; same shape. |

The paper quote provider `_make_paper_quote_provider` is text-identical (WT `main.py` 470-606 = TW 473-609).

Line numbers hold only for these states (M3).

### 0.3 Markers

- **Status:** ESTABLISHED · PARTIAL (the open part is written NOT ESTABLISHED) · NOT ESTABLISHED
- **WT↔VM:**
  - MATCH — cited code identical
  - DIFFERS-FILE — the file differs, the cited logic is identical
  - **DIFFERS-LOGIC**
- **Paper↔live:** IDENTICAL · DIFFER
- **Provenance:** MEASURED (code, DB, log, library, harness) unless marked **EVIDENCE** (a record) or **INFERENCE**.
- **Exercised:** whether TW-LOG or TW-DB holds a production artifact of the path.

### 0.4 Additions to PPV and FF found during this work

1. **PPV-Q9 item 7** says rehydrated ENTRY orders are re-tracked, and that "the `_handle_complete` fallback price would be 0.0". The harness shows more:
   - That fallback is reachable only for a persisted `SUBMITTED` row, and no writer ever produces one.
   - For a persisted `PENDING`, `OPEN` or `PARTIAL` row, `rehydrate_from_store` leaves the in-memory OSM at `PENDING`, because the forward transition is illegal and the error is swallowed.
   - If the broker already shows `COMPLETE` or `CANCELLED`, `_safe_transition` raises and nothing is published (Q5(c), Q5(d)).
2. **FF-F5(A)** describes the zero-fill branch for a CANCELLED entry. The same branch is taken when the broker cancels an entry that **has** fills, provided no `PARTIAL` poll came first (Q6(a), harness).

---

## Q1 — IOC

**Status:** PARTIAL — (c) is NOT ESTABLISHED.
**WT↔VM:** DIFFERS-FILE. In the adapter, TW adds only `market_protection`.
**Paper↔live:** DIFFER. Paper never sends an order, and `_synth_fill` models a resting order.

### (a) Does `ZerodhaAdapter.place_order` accept or forward `validity`?

**No, in both trees.** The signature has no `validity` parameter, and the Kite call passes no `validity` argument.

**Signature.** TW 494-506 is shown below. WT 478-489 is the same without the last parameter.

```python
def place_order(
    self,
    symbol: str,
    side: str,
    qty: int,
    price: float,
    order_type: str,
    intent: str,
    tag: Optional[str] = None,
    trigger_price: float = 0.0,
    variety: str = "regular",
    market_protection: Optional[float] = None,
) -> PlacedOrder:
```

**Kite call.** TW 639-654 is shown below, with its comment lines omitted. WT 604-615 is the same without `market_protection`.

```python
kite_order_id = self._kite.place_order(
    variety=variety,
    exchange="NSE",
    tradingsymbol=symbol,
    transaction_type=_KITE_TRANSACTION[side],
    quantity=qty,
    product=broker_code,
    order_type=_KITE_ORDER_TYPES[order_type],
    price=price if order_type in ("LIMIT", "SL") else None,
    trigger_price=trigger_price if trigger_price > 0 else None,
    tag=tag,
    market_protection=market_protection,
)
```

**Upstream.** `LimitTripleProtocol.execute` (`order_protocol_limit.py` 211-219, MATCH) passes `symbol, side, qty, price=_entry_order_price, order_type=entry_order_type, intent, tag=order_tag` and nothing else (FF-C1).

**No code passes an order validity.** A grep of non-test code in both trees finds `validity` only in:
- comments ("day-validity legs": `cnc_gtt.py` 4 and 51, `full_entry_engine.py` 147, `order_protocol_limit.py` 105);
- token-validity code (`healthcheck_server`, `system_manager`).

### (b) What the VM's kiteconnect accepts (TW-LIB, 5.1.0)

| `connect.py` lines | Literal |
|---|---|
| 71-73 | `VALIDITY_DAY = "DAY"` · `VALIDITY_IOC = "IOC"` · `VALIDITY_TTL = "TTL"` |
| 93-95 | `STATUS_COMPLETE = "COMPLETE"` · `STATUS_REJECTED = "REJECTED"` · `STATUS_CANCELLED = "CANCELLED"` (there is no OPEN or PARTIAL constant) |
| 339-370 | `def place_order(self, variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price=None, validity=None, validity_ttl=None, disclosed_quantity=None, trigger_price=None, iceberg_legs=None, iceberg_quantity=None, auction_number=None, tag=None, market_protection=None):` → `params = locals()` → `if params[k] is None: del (params[k])` → `return self._post("order.place", url_args={"variety": variety}, params=params)["order_id"]` |
| 372-396 | `modify_order(…, validity=None, …)` |

What this means:
- The client forwards any non-None `validity` string as a form field.
- It performs no product-, exchange- or order-type-specific check on it.
- With `validity` omitted, as today, the field is absent from the request, so the broker's default applies.

### (c) Is IOC valid for NSE MIS and CNC?

**NOT ESTABLISHED.**

**Library.** It defines `VALIDITY_IOC` and would send it with any product. That shows what the client *sends*, not what the broker or exchange *accepts*.

**Project docs.** IOC appears only as design intent, never as a statement of a broker or exchange rule:
- `docs/design/secondary_filteration/entry-execution/AUTHORITATIVE_ENTRY_EXECUTION_SETTLED.txt` 86: "reasons it is IOC or cancelled inside the same window";
- `…/reviews/CHATGPT_VALUE_ADDED_REPLY_TO_WEB_CLAUDE_ENTRY_EXECUTION_FINAL_REVIEW_14-Sep-2026.txt` 416;
- `…/reviews/CHATGPT_VALUE_ADDED_REPLY_TO_WEB_CLAUDE_ENTRY_EXECUTION_OPTIMAL_SOLUTION_14-Sep-2026.txt` 370.

The `docs/SYSTEM_MAP.md` 1771 match for "IOC" is unrelated (a security audit).

Settling this needs a broker source, and no broker call was made.

### (d) The gap between today's code and an IOC LIMIT reaching Kite — description only

| # | Point in the path | What is there today |
|---|---|---|
| 1 | `LimitTripleProtocol.execute` (`order_protocol_limit.py` 211-219, MATCH) | No validity argument in its adapter call. `EntryResult` (`orders/entry_engine.py` 38+) has no validity field. |
| 2 | `OrderPlacer.place` → `engine.execute` (`order_placer.py`, MATCH) | No validity value carried |
| 3 | `ZerodhaAdapter.place_order` signature (WT 478-489 / TW 494-506) | No `validity` parameter |
| 4 | Kite call (WT 604-615 / TW 639-654) | No `validity=` argument, so the field is omitted |
| 5 | `_validate_place_order` (WT 2012-2046 / TW 2080-2137) | No validity check |
| 6 | `PlacedOrder` (adapter 141+) | No validity field |
| 7 | Paper `_paper_place_order` / `_synth_fill` (WT 2048-2331 / TW 2139-2422, MATCH) | An LTP-gated resting simulation. Its docstring: "If max_wait elapses without a crossing, OSM stays SUBMITTED". There is no immediate-or-cancel outcome. |
| 8 | Persistence (`PRAGMA table_info` on TW-DB) | Neither `orders` nor `order_execution_log` has a validity column |
| 9 | Observing the outcome | `OrderMonitor` polls `get_order_history` every 2 s and reads `history[-1]` (`order_monitor.py` 762). A broker-side `CANCELLED` goes to `_handle_terminal(entry, "CANCELLED")` (779-780), which receives no filled quantity (Q6(a)). |
| 10 | Library | Already accepts `validity` (see (b)) |

### (e) Has any order carried a non-default validity?

**No evidence of one, and the DB cannot record it.**

- **TW-DB:** neither `orders` nor `order_execution_log` has a validity column.
- **TW-LOG:** the `system_*` and `debug_*` logs for 03, 04, 07, 08, 09, 10, 11 and 15 Sep contain 0 lines with `validity` and 0 with `IOC`.
- **BOOK (EVIDENCE):**
  - 30/30 orders show `"validity": "DAY"`, `variety` regular, `validity_ttl` 0 and `market_protection` 0.
  - By (product, type): MIS LIMIT 18 · CNC LIMIT 6 · MIS SL 4 · CNC MARKET 1 · MIS MARKET 1.
  - By status: COMPLETE 16 · CANCELLED 14.
  - All 3 order histories also show DAY.
  - The code never sends `validity`, so DAY on a system-placed order is what the broker applied when the field was absent. The book does not mark which orders the system placed, and this was not re-checked per order.

---

## Q2 — AFTER THE TICK SNAP

**Status:** ESTABLISHED.
**WT↔VM:** DIFFERS-FILE (adapter). The only difference inside `place_order` is TW's pass-through `market_protection`; `_snap_order_to_tick` is MATCH.
**Paper↔live:** DIFFER. Paper stops at step 6 below and sends nothing.

### (a) Every operation between `_snap_order_to_tick` and the bytes sent (live)

| # | WT | TW | Operation | Touches `price`? |
|---|---|---|---|---|
| 0 | 527 | 560 | `self._validate_place_order(...)` — runs **before** the snap | Reads; raises only |
| 1 | 532 | 567 | `price, trigger_price = self._snap_order_to_tick(...)` — the snap (`_round_nearest_to_tick`, Decimal `ROUND_HALF_UP`; PPV-Q7) | **Rebinds `price`** — the last rebinding |
| 2 | 544-551 | 579-586 | `force_intraday_only` coercion | `intent` only |
| 3 | 552 | 587 | `broker_code = self._pr.resolve(resolve_intent, "zerodha")` | No |
| 4 | 558-566 | 593-602 | CNC lock: `if broker_code == "CNC" and not self._delivery_enabled:` raises `OrderRejectedError(..., price=price, ...)` | Reads |
| 5 | 570-571 | 605-606 | `internal_id = new_order_id()` · `self._osm.register(internal_id)` | No |
| 6 | 573 | 608-619 | `if self._paper:` → `_paper_place_order(internal_id, symbol, side, qty, price, ...)`, then return | Reads (paper only) |
| 7 | 587 | 622 | `self._rl.acquire(_CATEGORY_MAP["place_order"])` | No |
| 8 | 589 | 624-627 | `context: dict[str, object] = {...}`, used for exception translation; holds the price | Reads |
| 9 | 601-602 | 636-637 | `if tag: tag = truncate_tag_for_broker(tag)` | No |
| 10 | 604-615 | 639-654 | `self._kite.place_order(... price=price if order_type in ("LIMIT", "SL") else None ...)` | Reads |
| 11 | lib 339-370 | same | `params = locals()`; `None` entries deleted; `self._post("order.place", ...)` | Passes the float object through |
| 12 | lib 874-876, 915-924 | same | `_post(..., is_json=False, ...)` → `self.reqsession.request(method, url, json=params if (method in ["POST", "PUT"] and is_json) else None, data=params if (method in ["POST", "PUT"] and not is_json) else None, ...)` | Passes through as form data |
| 13 | requests `models.py` 109-137 | same | `_encode_params` → `return urlencode(result, doseq=True)`; the VM stdlib `urlencode` serialises each value as `quote_via(str(v), safe, encoding, errors)` | `str(float)` |
| 14 | 628 / 630 | 667 / 669-682 | After the response: `self._osm.transition(internal_id, "SUBMITTED")`; `PlacedOrder(... price=price ...)` | Reads |

- An AST scan of `place_order` in both trees finds exactly one rebinding of `price`: the snap (row 1).
- `modify_order` has three callers, all SL trailing: `breakeven_manager._advance_sl` 289, `smart_tgt_manager._modify_co_sl` 596 and `structure_exit_manager._trail_sl` 569. None of them modifies an ENTRY after placement.

### (b) Any circuit clamp on the ENTRY price?

**None.**
- **The only clamp** is `clamp_exit_into_band` (`orders/price_math.py` 284-). It is called only from the exit placers in `order_protocol_limit.py` (MATCH):
  - `place_exits` — `_circuit_limits` 319, SL clamp 324, TGT clamp 346;
  - `place_tgt_only` — 557-560.
- **`LimitTripleProtocol.execute` (171-248)** has no clamp.
- **Circuit limits are read at screening, and neither read modifies a price:**
  - `screening/hard_gate.py` 79-147 rejects when "no valid SL fits the band" or "no profitable TGT fits the band";
  - `screening/step_executor.py` 402 checks `circuit_state`.
  - These grep lines are identical in both trees.

### (c) Do validate, product resolver, CNC lock or OSM register alter the price?

**No.**

| Step | What it does with `price` |
|---|---|
| `_validate_place_order` | Runs **before** the snap. Raises only. |
| `_pr.resolve` | Is not passed the price |
| CNC lock | Reads `price` into an exception |
| `_osm.register` | Takes only `internal_id` |

The line numbers are in (a).

### (d) Does kiteconnect transform the price?

**No.**
- **kiteconnect** puts the Python float into `params` unchanged (lib 339-370).
- **requests** form-encodes it with `str(v)`.
- **Local check** (Python 3.11.9), using a verbatim copy of `_round_nearest_to_tick` and stdlib `urlencode`:
  - 600,000 random prices at ticks 0.01, 0.05, 0.1, 0.5, 1 and 5 gave **0** cases where the encoded string differs from the snap's Decimal result.
  - Control: an unsnapped float goes out with all its digits (`price=658.35099`).
  - Examples: 219.45033 at tick 0.05 → `price=219.45`; 1020.1788 at tick 0.1 → `price=1020.2`.
- **VM environment** (MEASURED today): `python3` 3.12.3, and its stdlib `urlencode` contains `v = quote_via(str(v), safe, encoding, errors)`.
- **INFERENCE:** `float.__repr__` produces the same shortest round-trip string on 3.11 and 3.12.

### (e) Is the snap the LAST change?

**Yes.**
- **Live:** after `_snap_order_to_tick` (WT 532 / TW 567), nothing in the adapter, kiteconnect or requests changes the entry price, and the form value sent equals the snapped value.
- **Paper:** the same snapped price is passed into `_paper_place_order`. The paper *fill* price is computed separately by `_synth_fill` (FF-F1), and nothing is sent to a broker.

---

## Q3 — THE MARKETABLE-LIMIT DECISION

**Status:** ESTABLISHED.
**WT↔VM:**
- `get_quote`, `get_quote_raw` and `step_executor` are MATCH.
- `_build_market_data` is MATCH (WT 401-439 / TW 380-418).
- `signal_processor` M-S1 reads the same `q.last_price` (TW 1087 / WT 1134).

**Paper↔live:** DIFFER.
- Paper quotes come from `_make_paper_quote_provider`, which fetches real Kite quotes with the same bid/ask mapping.
- Paper takes `ts = now_ist()` **before** the fetch (TW `main.py` 532).
- Paper serves results from a `_CACHE_TTL_SEC = 3.0` cache (TW 524).
- All measurements below are live-mode (FF: every TW-DB trade has mode LIVE).

### (a) Are bid and ask populated? (`screener_results.market_data_snapshot`, TW-DB)

**Written by** `_build_market_data`: `"bid": quote.bid, "ask": quote.ask` (WT 420-421 / TW 399-400).

**The adapter's own fallback** is `bid = float(bids[0]["price"]) if bids else 0.0` (TW 1780-1782).

| Set | Rows | bid > 0 | ask > 0 | both > 0 | Spread % of mid (both > 0) | Other |
|---|---|---|---|---|---|---|
| All | 204,389 (the `bid` key is present in 195,648) | 95.17 % | 92.58 % | 92.03 % | p50 0.0606 · p90 0.1347 · max 3.3875 | ask = 0: 6,421 · bid = 0: 1,138 · LTP inside [bid, ask]: 129,966 rows |
| Since 01-Sep | 46,455 | — | — | 91.34 % | p50 0.0591 | — |
| PASSED since 01-Sep | 904 | 100 % | 100 % | 100 % | p50 0.0448 · p90 0.1151 · max 0.7093 | LTP inside [bid, ask]: 612 of 904 |

Sample (PASSED): GODREJAGRO, 01-Sep 10:00:21 — ltp 673.1, bid 673.05, ask 673.5.

Separately, `market_execution_context` ENTRY rows are captured **at fill time** by `SlippageRecorder` via `get_quote_raw`. All 213 have `bid_price`, `ask_price`, `bid_qty` and `ask_qty` > 0.

### (b) Every entry-path reader of bid/ask

| Reader | Where | What it does |
|---|---|---|
| Screener score step `_step_8_spread_check` | `screening/step_executor.py` 372-395 (MATCH) | `spread_pct = ((ask - bid) / mid) * 100.0` → `return 1.0 if spread_pct <= max_spread else 0.0` — a **score** contribution only |
| `OrderPlacer._check_liquidity` | `order_placer.py` 4066- (MATCH), called at 1294 | `if not self._liquidity_check_enabled: return True, ""` (4075-4076) runs before any quote. When enabled it would read depth prices and quantities (fail-open). **Disabled** (FF-A1). |

**No other reader** on the entry path. `v3_chain`, `capital` and `signals` read no bid or ask.
- M-S1 reads `q.last_price` (TW `signal_processor.py` 1087).
- FIX-128 and FIX-075 read `last_price` through `_fetch_ltp` (`order_placer.py` 4036-4064: `ltp = float(q.get("last_price", 0) or 0)`).

**Readers outside the entry path:**
- `shadow_tracker.py` 248-249 — post-fill shadow;
- `slippage_recorder.py` 156-179 — fill-time context.

### (c) Quote age at order construction (TW-LOG 03–15 Sep)

**Method:** each entry was matched exactly, not by symbol:
- `trade_created` gives (trade_id, signal_id);
- then the M-S1 success line within 5 s;
- then the FIX-128 `entry_slippage_observed` line;
- then `place_order call_start`;
- then `limit_triple.entry_placed`.

104 entries were matched and 0 were unmatched.

**Groups:**
- **TEN** — the ten strategies re-anchored by M-S1.
- **PB6** — the six strategies that bypass M-S1 (PPV-Q2).

| Interval to `place_order call_start` | Group | n | min | p50 | p90 | max |
|---|---|---|---|---|---|---|
| M-S1 quote (FIX-067 success line) | TEN | 58 | 0.671 s | 2.318 s | 5.100 s | 12.667 s |
| FIX-128 raw LTP quote | PB6 | 46 | — | 0.335 s | 2.000 s | 5.341 s |
| FIX-128 raw LTP quote | TEN | 58 | — | 0.337 s | 2.435 s | 3.669 s |
| Screener PASSED (the quote that wrote bid/ask) | PB6 | 46 | — | 1.706 s | 4.333 s | 7.668 s |
| Screener PASSED | TEN | 58 | — | 3.320 s | 6.962 s | 12.993 s |
| `call_start` → `limit_triple.entry_placed` | all | 104 | — | 0.046 s | — | 0.101 s |

- **Log order:** `get_quote` logs `call_start` (TW 1737) **before** `_rl.acquire` (1757), so a log instant precedes the broker round-trip.
- **An earlier symbol-only match** gave a spurious M-S1 maximum of 59 s. The exact match above replaces it.
- **For PB6** the submitted price does not come from a quote at all; it is the Chartink trigger (PPV-Q2(a)–(b)).

### (d) Exchange timestamp or local fetch time?

**Local receive time.** The typed quote carries no exchange time.

**Typed quote.**
- `Quote` has these fields (adapter 209-222): `symbol, last_price, bid, ask, volume, ts, vwap, open_price, day_high, day_low, upper_circuit, lower_circuit`.
- It has no exchange timestamp, no `last_trade_time` and no depth quantities.
- `get_quote` sets `ts = now_ist()` after the REST response (TW 1771).

**Raw quote.**
- kiteconnect `quote()` (lib 580-594) returns Kite's `timestamp` and `last_trade_time`, parsed to datetimes by `_format_response` (408-422).
- `get_quote` drops both.
- `get_quote_raw` (TW 1808-1826) keeps the raw dict, but `_fetch_ltp` reads only `last_price`.
- `order_execution_log.exchange_timestamp` is populated on 0 of 475 rows (PPV-Q10(a)).

**Other readers.** The tick-timestamp reads in `data/live_feed.py` and `main.py` (WT 2725 / TW 2966) belong to the KiteTicker feed, which the entry path does not use.

**Paper.** `ts` is taken before the fetch and may be served from the 3.0 s cache (TW `main.py` 524, 532).

### (e) Can the system prove a limit at P is marketable, or only observe LTP?

**It cannot prove it.** At submission the system holds:
- a REST snapshot whose age at `call_start` is p50 0.34 s (FIX-128) to 2.3 s (M-S1), with a maximum of 12.7 s;
- best bid/ask **prices** from an even earlier screener quote (p50 1.7–3.3 s), with no sizes and no exchange time.

No entry decision reads bid or ask: the only reader is a score step, and the depth check is disabled. The quantities that could show available size exist only at **fill** time (`market_execution_context`).

**Paper:** the same, plus up to 3 s of cache age.

---

## Q4 — A WORKING ENTRY

**Status:** PARTIAL. Kite's status string for a partially filled order and the paper `orders.status` sequence are NOT ESTABLISHED.
**WT↔VM:** the cited functions are MATCH (§0.2). The position-cap reservation scope is **DIFFERS-LOGIC** (WT 669 vs TW 607).
**Paper↔live:** the selectors and status writers are IDENTICAL. The orphan branches are live-only, because paper `cancel_order` always succeeds (FF-D5), and paper never produces PARTIAL (FF-F2/F3).

### (a) Every trade status that can exist while an ENTRY order can still fill at the broker

| `trades.status` | Writer (WT / TW) | When |
|---|---|---|
| **`PENDING`** — the normal working state | `order_placer.py` 1063-1071 (MATCH): `self._om.update_trade_status(trade_id, "PENDING")`, commented "FIX-071 Part A: Transition trade to PENDING before broker call" | Before `engine.execute`; the row stays `PENDING` until a fill handler, recovery or a failure path writes it |
| `PENDING_FILL` | `create_trade` INSERT `'PENDING_FILL'` (WT 240 / TW 236) | Before the broker call. It survives into the working period only if the `PENDING` update fails, which is non-fatal: "# Non-fatal: continue with placement even if status update fails" (1071). TW-LOG `order_placer.pending_status_update_failed`: **0**. No code writes `PENDING_FILL` again. |
| `UNKNOWN_IN_FLIGHT` | `order_placer.py` 1449 | `BrokerTimeoutError` from `engine.execute`; the broker order may exist (PPV-Q9 item 6) |
| `FAILED` | Zero-fill branch `order_placer.py` 2005 (via `OrderStatusChanged` CANCELLED/FAILED with `qty_filled 0`) · `_handle_placement_failure` 4448 · `fail_recovery_trade` (WT 1604-1620 / TW 1616-1632: `WHERE status IN ('UNKNOWN_IN_FLIGHT','PENDING')`) · CHECK6 (WT 2644 / TW 2648; `PENDING_FILL` rows only) | After an **unverified** cancel or an orphan, the broker order may still be live (PPV-Q9 items 4, 5, 6(ii)) |
| `REJECTED*` / `CANCELLED` | `_handle_placement_failure` 4448 · EOD `_cancel_pending_entries` 898 (`PENDING_FILL` rows only) | As above |
| `OPEN` | `record_entry_fill` (WT 409-448 / TW 393-432: `SET status = 'OPEN'`) · `adopt_recovery_trade_to_open` (state_store WT 1522- / TW 1534-: `set_clauses = ["status = 'OPEN'", "recovered_flag = 1", ...]`) | After a partial-then-cancel, where the remainder cancel is unverified (FF-F3) |
| `EXITING` | `kill_switch._mark_trade_exiting` (WT 1469-1505 / TW 1521-1557) · `mark_recovery_trade_exiting` · `structure_exit_manager._mark_exiting` 354 · `order_placer.py` 3823 | Flatten or exit in flight |

**No writer sets `trades.status` to `PARTIAL`**, in either tree (AST scan of every `UPDATE trades` literal).

**Measured:**
- TW-DB now: CANCELLED 9 · CLOSED 308 · CLOSED_MANUAL 61 · FAILED 481 · REJECTED 95.
- TW-LOG 03–15 Sep has 20 "Position cap reached" lines (`risk_engine.py` TW 585-620). On all 20, `pending_fill_rows = db_active − open_partial` is **0**.
  - On 7 of them an ENTRY order was working at that instant (DB `placed_at` → fill or terminal): LAXMIINDIA 09-03 · MVGJL 09-07 ×2 · VSSL 09-10 ×2 · MUKANDLTD 09-10 ×2.
  - On those 7, `live_reservations` was 1–2.
  - So the working entries were **not** `PENDING_FILL`.
- **CHECK2 in-flight lines** (TW-LOG): 2 — GANECOS 04-Sep 10:13:20 and RAYMOND 08-Sep 10:09:51.
  - Both were resolved by the normal fill path about 0.6 s and 1.0 s later (DB `entry_time` 10:13:20.906 and 10:09:52.772).
  - The CHECK2 query covers `PENDING` and `PENDING_FILL`, so these lines do not discriminate between the two.

### (b) Every `orders.status` value in that situation

| `orders.status` | Writer | When |
|---|---|---|
| **No row** | — | Timeout (`UNKNOWN_IN_FLIGHT`, no broker id), or a crash between broker ack and `_persist_entry_orders` |
| **`PENDING`** | `insert_orders_atomic` (WT 355-407 / TW 339-391; literal `'PENDING', 0, NULL,` WT 393 / TW 377) | Written after `engine.execute` returns, and kept until the monitor publishes a transition |
| **`OPEN`** | `update_order_status` (WT 742-768 / TW 726-752) ← `OrderManager._on_order_status_changed` (148-171) ← `OrderStatusChanged` published by `_safe_transition` (`order_monitor.py` 1334) | First `OPEN` poll: SUBMITTED → OPEN |
| `PARTIAL` | Same chain, from `_handle_partial` | A `PARTIAL` poll |
| `CANCELLED` / `FAILED` | Same chain after an unverified cancel or orphan (PPV-Q9 items 4, 5) · `sweep_stale_orders` (trade already terminal) · `scripts/eod_cleanup.py` 149/161 (prior days) · EOD 902 (`PENDING_FILL` trades only) | The broker order may still be live |

**`SUBMITTED` and `TRIGGER_PENDING` are never written** by any writer. They appear only as literals inside selectors.

**Why live rows move from `PENDING` to `OPEN`:**
- The adapter moves the **shared** OSM to `SUBMITTED` after the Kite call (TW 667; one `OrderStateMachine()` is built at TW `main.py` 2346 and passed to the adapter at 2388 and to the monitor at 3000).
- The first `OPEN` poll is therefore a legal SUBMITTED → OPEN, and it publishes.
- The PENDING → OPEN auto-step (`order_monitor.py` 1267-1279) returns `True` **before** the publish block. It is taken only when the OSM is still `PENDING`.
- **MEASURED:** TW-LOG `order_monitor.pending_to_open_auto_step` = 0, so live orders never used the auto-step.
- **HARNESS:** tracked at SUBMITTED, broker OPEN → `OrderStatusChanged(OPEN)` published.

**Paper:**
- `_paper_place_order` also moves the OSM to `SUBMITTED` (TW adapter 2160).
- `_synth_fill` moves it to `COMPLETE` itself (2305-2307) and publishes `OrderFilled` (2393).
- The monitor polls `_paper_fills`.
- The resulting paper `orders.status` sequence was **not traced — NOT ESTABLISHED**.

### (c) Which store is authoritative for "can still create exposure"?

**None.** The code designates no single authority. It states ownership per aspect:

| Source | Quote |
|---|---|
| `order_monitor.py` 397-398, `rehydrate_from_store` docstring | "The reconciler remains the authoritative backstop for capital/DB drift; this method simply restores fill-polling." |
| `order_monitor.py` 1310, `_safe_transition` | "but does not reverse the transition (OSM is authoritative)." The OSM is in-memory and is rebuilt only partly after a restart (Q5(c)). |
| `core/schema.sql`, `orders.status` comment | "OSM STATES (broker/order_state_machine.py) … OrderStateMachine.STATES is the write vocabulary" |
| `fund_manager.py` WT 1789 / TW 1725 and WT 1802 / TW 1738 | "Reconstruct in-memory capital state from the persistence triangle: fm_ledger (capital transitions) + trades (position identity) + orders (entry product)" … "(each table owns what it owns)." |
| `fund_manager.py` WT 2243 / TW 2246, `_restore_reserve_from_ledger` | "(the source of truth)", referring to the fm_ledger RESERVE row |

Each selector (d) reads a different proxy:
- `trades.status` — EOD Pass 1, CHECK6, HARD_KILL, admission guards, CHECK2, capital replay;
- `orders.status` — rehydration, sweeps;
- the monitor's in-memory tracked set — fill timeout, FIX-141, force close, shutdown cancel;
- in-memory FundManager reservations — the position cap.

**Only two paths read broker truth about an entry:**
- `OrderMonitor._process_order`, per tracked order (`get_order_history`);
- the reconciler's broker reads — tag correlation in `_recover_in_flight_entries` for recovery-state trades only, and position snapshots in CHECK1–5.

### (d) Every selector: predicate, and whether it can match a working entry today

| Selector | Where (WT / TW) | Predicate as written | Can it match a working ENTRY today? |
|---|---|---|---|
| **EOD Pass 1** `_cancel_pending_entries` | `eod_squareoff.py` 864-945 (MATCH) via `get_pending_intraday_orders` (WT 1040-1064 / TW 1015-1039) | `t.status = 'PENDING_FILL' AND o.leg = 'ENTRY' AND o.product IN ('MIS','CO')` | **No** — the trade is `PENDING` (PPV-Q9 item 9) |
| EOD Pass 1 `_cancel_pending_exit_legs` | 947-1025 via `get_pending_exit_orders_for_open_positions` (WT 1160-1193 / TW 1135-1168) | Trades OPEN/PARTIAL, MIS/CO, legs SL/TGT, non-terminal | No — exit legs only |
| EOD Pass 2 `_exit_open_positions` | 1027- via `get_open_intraday_positions` (WT 1195-1238 / TW 1207-1250) | Trades OPEN/PARTIAL with a MIS/CO ENTRY, `qty_filled > 0` | No for an unfilled entry; yes for a filled part recorded by `record_entry_fill` |
| EOD residual sweep `_sweep_residual_broker_positions` | 1427- | Broker positions with qty ≠ 0 and product in `EMERGENCY_FLATTEN_PRODUCTS`, flattened when the symbol is in `get_trades_for_date(today)` (any status) | Not an order selector. It flattens a **filled** MIS/CO quantity. |
| **HARD_KILL** `_exit_all_trades_indestructible` | `kill_switch.py` WT 1618-2099 / TW 1670-2151 | `_FLATTEN_LIVE_TRADE_STATUSES = ("OPEN", "PARTIAL", "PENDING_FILL")` (93); `_cancel_trade_resting_exits` legs SL/TGT (WT 1546-1616 / TW 1598-1668); broker-position sweep; `_HARD_KILL_MAX_RETRY_HOURS = 2.0` (85) | **No ENTRY cancel.** `PENDING` is not in the set. A filled quantity is swept as a position. |
| Soft kill `soft_kill` | WT 536-637 / TW 563-689 | No selector; no cancel, place or UPDATE | — |
| 15:15 force close `_check_force_close` | `order_monitor.py` 794-867 | Tracked snapshot, legs not in (SL, TGT, EOD) | Only if tracked |
| Shutdown `cancel_all_entry_orders` | `order_monitor.py` 530-590; called from WT `main.py` 1484 / TW 1768 | Tracked snapshot, `entry.leg in ("", "ENTRY")` | Only if tracked |
| Reconciler `_recover_in_flight_entries` | WT 3909-3992 / TW 4169-4252 | Timeout feed `get_timeout_recovery_trades()` (in-memory, `order_placer.py` 757-763) plus crash feed `get_orphaned_pending_trades` (`t.status = 'PENDING'` with **no** ENTRY row; WT 1105-1136 / TW 1080-1111) | Only a timed-out or never-persisted entry. A resting match is deferred with no cancel (PPV-Q9 item 6). |
| Reconciler CHECK2 in-flight `_check2_inflight_orphan` | Routing WT 935 / TW 939; function WT 2004-2237 / TW 2008-2241 | A broker position with no OPEN/PARTIAL trade, and `get_trades_by_status_and_symbol(("PENDING_FILL", "PENDING"), symbol)` non-empty | **Yes, once it has filled quantity.** Logs WARNING "entry filled at broker, awaiting local fill confirmation (no action; fill path will adopt)", tier COSMETIC. It flattens (intraday) only if HARD_KILL is active. |
| Reconciler CHECK2 `_check2_orphan_adoption` | WT 1792-1881 / TW 1796-1885 | A broker position with no OPEN/PARTIAL/EXITING/PENDING/PENDING_FILL trade for the symbol | A filled quantity whose trade is already `FAILED` or `CANCELLED` is logged "CHECK2 HUMAN_ORDER" at INFO once a day, gets a WARNING Telegram "Naked untracked position" once a day if `_position_is_naked`, and is **not managed** |
| Reconciler CHECK6 `_check6_orphan_orders` | WT 2593-2704 / TW 2597-2708 via `get_pending_all_products` (WT 1863-1888 / TW 1875-1900) | `t.status = 'PENDING_FILL'` with an ENTRY row, compared against broker open orders | **No** — the trade is `PENDING` |
| Reconciler `sweep_stale_orders` | WT 461-525 / TW 472-536; called at boot (WT `main.py` 3568 / TW 3891) and at EOD | `status NOT IN ('COMPLETE','CANCELLED','FAILED','EXPIRED') AND trade_id IN (… status IN ('CLOSED','CLOSED_MANUAL','CANCELLED','FAILED'))` → local `CANCELLED` plus WARNING Telegram | Only after the trade is already terminal; a local mark, no broker cancel. TW-LOG "Sweep: marked" 2 (03-Sep 15:17:04 and 07-Sep 15:19:05), **both SL legs**. |
| Rehydration `get_open_orders_for_rehydration` | WT 1066-1103 / TW 1041-1078 | `o.status IN ('PENDING', 'SUBMITTED', 'OPEN', 'PARTIAL', 'TRIGGER_PENDING')` | **Yes**, at boot, if the row exists with such a status (Q4(f), Q5) |
| MIS auto-squareoff | `orders/mis_autosquareoff.py` (TW only) | Exit legs of OPEN/PARTIAL MIS trades, with broker open-order verification | No |
| Cron `scripts/eod_cleanup.py` `_cleanup_stale_orders` (15:50 Mon–Fri) | MATCH | Prior-day orders IN (OPEN, SUBMITTED, PENDING, TRIGGER_PENDING) with a terminal or missing trade → `CANCELLED`; `PARTIAL` excluded | Prior days only; local mark |
| Admission guards | `has_active_position` (WT 959-973 / TW 934-948), `count_in_flight_orders` (628-637), `count_active_positions` (639-656); `risk_engine.py` TW 585-610 | DB: `status IN ('PENDING_FILL', 'OPEN', 'PARTIAL')` or `status = 'PENDING_FILL'`. Cap: `authoritative_total = max(open_count + reserved_inflight, active_count) + 1` (TW 607), with `reserved_inflight = _count_res()` (TW 606) or `self._live_reservations(policy)` (WT 669) | The DB guards do not count it. The cap counts it only through FundManager live reservations, in the same process. |
| Paper boot `cancel_stale_paper_orders` | WT 1138-1158 / TW 1113-1133; called WT `main.py` 3626 / TW 3949 | `status IN ('PENDING', 'SUBMITTED', 'OPEN', 'PARTIAL', 'TRIGGER_PENDING') AND date(placed_at) < date(?)` | Paper only; prior days only |

### (e) Partial fill: trade status, and which selectors find the exposure and the remainder separately

**Kite's status string for a partially filled order is NOT ESTABLISHED:**
- kiteconnect defines no `PARTIAL` or `OPEN` status constant (lib 93-95);
- BOOK has no partial fill;
- TW-LOG `order_monitor.partial_fill` = 0.

Code handles three shapes. All three were driven through the unchanged monitor with the HARNESS.

**(i) The broker reports `PARTIAL` — the FIX-130 path.**

*Code and HARNESS:*
- published `PARTIAL(qty 1)`, so `orders.status` becomes PARTIAL with `qty_filled 1`;
- immediate `cancel_order` (911-939);
- `OrderPartiallyTerminated(1)` → `_on_order_partially_terminated` → `commit_to_used(actual_qty=1)`, `record_entry_fill` (trade **OPEN**, `qty_filled 1`), SL/TGT for 1;
- published `CANCELLED(1)`.

*Who finds what:*
- **Exposure:** EOD Pass 2, HARD_KILL trade flatten, reconciler CHECK3/4/5 (`local_qty = trade["qty_filled"] or 0`, WT 888 / TW 892), boot capital replay.
- **Remainder:** no order selector; the row is CANCELLED and untracked. If the cancel did not take effect and the remainder fills, the broker position grows. CHECK5 `POSITION_GREW` then raises `CapitalDriftDetected` with no order action (FF-F3), and the HARD_KILL and EOD residual broker-position sweeps see only the quantity.

**(ii) The broker reports `PARTIAL` and the cancel fails.**

*Code:*
- CRITICAL `partial_immediate_cancel_failed` → `_fire_orphan` (soft kill plus Telegram) → untrack;
- no `OrderPartiallyTerminated`;
- the trade stays **`PENDING`**, and the orders row stays `PARTIAL` with `qty_filled 1`.

*Who finds what:*
- **Exposure:** CHECK2 in-flight (WARNING, no action unless HARD_KILL is active), the HARD_KILL broker sweep and the EOD residual sweep.
- **Remainder:** nothing while the process runs. The `PARTIAL` row is picked up only by rehydration after a restart. `sweep_stale_orders` needs a terminal trade, and the cron excludes `PARTIAL`.

**(iii) The broker reports the partially filled order as `OPEN` with fills.**

*Code and HARNESS:*
- `_process_order` routes `OPEN` to `_handle_open` (770-771), which ignores `filled_qty`;
- a later `CANCELLED` — the fill-timeout cancel or a broker cancel — publishes `CANCELLED(qty 0)` → zero-fill branch: reservation released, trade **FAILED**, orders `CANCELLED` with `qty_filled 0`.

*Who finds what:*
- **Exposure:** CHECK2 finds no `PENDING`/`PENDING_FILL` trade, so the position goes to `_check2_orphan_adoption` → HUMAN_ORDER, not managed. The EOD residual sweep still flattens MIS/CO, because `get_trades_for_date` includes FAILED trades. The HARD_KILL broker sweep also applies.
- **Remainder:** no local selector.

**Trade status across (i)–(iii):** the trade is never `PARTIAL`. It is `PENDING`, then `OPEN` in (i), stays `PENDING` in (ii), or becomes `FAILED` in (iii).

### (f) After a restart, which selectors find a working entry?

**Boot order:**

| Step | WT `main.py` | TW `main.py` |
|---|---|---|
| `fund_manager.rehydrate_from_open_trades` | 2575 | 2815 |
| `order_reconciler.reconcile_once()` | 3557 | 3880 |
| `sweep_stale_orders()` | 3568 | 3891 |
| `order_monitor.rehydrate_from_store(store)` | 3629 | 3952 |
| `order_placer.rehydrate_fill_map(store)` | 3632 | 3955 |
| `order_monitor.start()` | 3637 | 3960 |
| `order_reconciler.start()` | 3638 | 3961 |

| Selector | Finds it after restart? |
|---|---|
| Capital replay (`get_all_open_trades`: "status OPEN or PARTIAL") | **No.** The reservation is not re-applied. |
| `_recover_in_flight_entries` | Timeout feed: **no** (the in-memory queue is empty). Crash feed: **only if there is no ENTRY orders row**. |
| CHECK2 in-flight | Only once filled; WARNING, no action (unless HARD_KILL) |
| `sweep_stale_orders` | No — the trade is not terminal |
| **`rehydrate_from_store`** | **Yes**, if the orders row status is PENDING/SUBMITTED/OPEN/PARTIAL/TRIGGER_PENDING |
| `rehydrate_fill_map` | **No.** ENTRY rows are skipped at `order_placer.py` 819-820: `if leg not in (_LEG_SL, _LEG_TGT, _LEG_EOD): continue`. |
| Fill timeout / force close / shutdown cancel | Yes, for a rehydrated entry (it is in the tracked set) |
| FIX-141 pending-R:R cancel | **No.** It returns early (Q5(d)). |
| EOD Pass 1 / CHECK6 / HARD_KILL trade flatten | No, same as without a restart |
| Admission guards | DB guards exclude `PENDING`. `count_live_reservations` no longer includes it, because the reservation was not replayed. `processor_in_flight` starts at 0. |

**What happens to a rehydrated working entry:** Q5(c).

**MEASURED:** all 16 boots in TW-LOG 03–15 Sep logged "order_monitor rehydrated 0 orders from state_store" and `order_placer.rehydrate_fill_map` `rehydrated 0`. **The restart-with-working-entry path is not exercised.**

---

## Q5 — RESTART

**Status:** ESTABLISHED. **Exercised:** no (0 of 16 boots rehydrated anything).
**WT↔VM:** MATCH for every cited function (§0.2).
**Paper↔live:** IDENTICAL code, with one difference:
- After a paper restart, `_paper_fills` is empty, so paper `get_order_history` returns `status = state.get("status", "SUBMITTED")` with fill 0 (TW adapter 1168-1169 / WT 1129-1130). A rehydrated paper ENTRY therefore follows the "broker OPEN" row in (c).
- Paper boot also cancels prior-day rows (`cancel_stale_paper_orders`).

### (a) Stores for intended price, stop, target, direction and outstanding quantity (TW-DB population)

| Value | Store | Written by | Populated (TW-DB) | Read at restart? |
|---|---|---|---|---|
| **Intended price** | `trades.entry_target_price` — pre-FIX-075 and pre-snap; schema "the LIMIT price we want" | `create_trade` (`order_placer.py` 1003) | 954/954 (since 01-Sep 145/145) | Not by `rehydrate_from_store`; only by capital replay, and only for OPEN/PARTIAL |
| | `orders.price` — the submitted price | `_persist_entry_orders` passes none, so NULL (PPV-Q10(b)) | **0/773** ENTRY (since 01-Sep 0/116) | Read by rehydrate → `expected_price = 0.0` |
| | `fm_ledger` RESERVE `reason` | `fm.reserve` — e.g. `'ARVSMART qty=1 @ 559.1586 intent=INTRADAY (base=111.83 buffer=5.59)'` | Every trade since 01-Sep with a `reservation_id` has a RESERVE row (145/145) | No (free text) |
| | `fm_ledger` TOP_UP `reason` — post-FIX-075 LTP, 2 dp | `order_placer.py` 1233: `f"price drift {drift_pct*100:.2f}% → ₹{current_ltp:.2f}"`, only when a top-up fires | 8 rows ever | No |
| | `order_execution_log.intended_price` | `SlippageRecorder`, on `OrderFilled` only (subscription at `slippage_recorder.py` 113) | Filled orders only (PPV-Q10(a)) | No |
| | TW P1_ACCEPT evidence `entry_price_final` (plus `sl_price`, `tgt_price`, `qty`, `trigger_price`) | TW `signal_processor.py` 1427-1445 → `data_store/evidence/signal_evidence_<ARM>_<date>.jsonl` | Testing VM from 11-Sep (PPV) | No |
| | In-memory `_WatchEntry.expected_price` (post-FIX-075, pre-snap) and `_FillEntry` | `order_placer.py` 1590-1620 | — | **Lost** |
| | Broker order row `price` (the snapped price) | Kite | BOOK row keys include `price`, `quantity`, `filled_quantity`, `pending_quantity`, `cancelled_quantity`, `transaction_type`, `tag`, `validity`, `exchange_timestamp` (EVIDENCE) | **Not read:** `OrderHistoryEntry` (adapter 170-177) keeps only `broker_order_id, status, filled_qty, avg_price, rejection_reason, ts` |
| **Stop** | `trades.sl_initial` | `create_trade` | 954/954 | Not by rehydrate (`_WatchEntry.sl_price` stays 0.0) |
| | `orders.trigger_price` (ENTRY) | — | 0/773 (LIMIT) | — |
| **Target** | `trades.tgt_initial` · `trades.tgt_risk_reward_applied` ("strategy R:R frozen at placement", `order_placer.py` 1014) | `create_trade` | 954/954 · 145/145 since 01-Sep | Not by rehydrate (`tgt_price` stays 0.0) |
| **Direction** | `trades.direction` · `orders.transaction_type` | `create_trade` · `insert_orders_atomic` | 954/954 · 773/773; side matches direction on 773/773 | Rehydrate reads `transaction_type` → `side`. `rehydrate_fill_map` reads `direction`, for exit legs only. |
| **Outstanding quantity** | `orders.qty_requested` · `trades.qty_planned` | Insert · create | 773/773 · 954/954; `qty_requested == qty_planned` on 773/773 | Rehydrate reads `qty_requested` |
| | `orders.qty_filled` | Only the published `PARTIAL` path writes > 0 (PPV-Q10(c)) | **0/773 > 0** | Not read (`filled_qty` stays 0) |
| | `trades.qty_filled` | `record_entry_fill`, on fill | 368 filled trades | Not read |
| | Broker `filled_quantity` / `pending_quantity` | Kite | — | The adapter maps `filled_quantity` only (`get_order_history` WT 1118-1180 / TW 1157-1219) |
| Reservation | `trades.reservation_id` · `fm_ledger` RESERVE | `create_trade` · `fm.reserve` | 954/954 · 145/145 | Capital replay skips `PENDING`. `_restore_reserve_from_ledger` exists for recovery trades only. |

The `signals` table holds `trigger_price` only (48,506/48,506 since 01-Sep). It has no stop or target column.

### (b) `trades` vs `orders`: writers and authority

**Writers of `trades.status`:** Q4(a).

**Writers of `orders.status`:**

| Writer | Where (WT / TW) | Leg / condition |
|---|---|---|
| `insert_orders_atomic` / `insert_order` | `order_manager.py` WT 355-407, 305-353 / TW 339-391, 289-337 | Insert `PENDING` |
| `update_order_status` | WT 742-768 / TW 726-752 | `SET status = ?, qty_filled = ?, avg_fill_price = ?, …` from every published `OrderStatusChanged` |
| `_backfill_entry_order_row` | Reconciler WT 4306-4338 / TW 4566-4598 | Recovery: inserts an ENTRY row (`price=float(trade_row["entry_target_price"] or avg_price)`) and then `COMPLETE` |
| `sweep_stale_orders` | WT 461-525 / TW 472-536 | Any leg, when the trade is terminal |
| `_mark_order_cancelled_local` | WT 1761-1780 / TW 1765-1784 | CHECK1 orphan legs (`leg IN ('SL', 'TGT')`) and exit-leg dedupe |
| `_cancel_pending_entries` / `_cancel_pending_exit_legs` | `eod_squareoff.py` 902 / 997 | ENTRY of `PENDING_FILL` trades / SL-TGT |
| `_cancel_trade_resting_exits` | `kill_switch.py` WT 1599 / TW 1651; `structure_exit_manager.py` 399 | SL/TGT |
| `cancel_stale_paper_orders` | WT 1150 / TW 1125 | Paper, prior days |
| Scripts | `eod_cleanup.py` 149 and 161 · `check_vm_state.py` 163 | Local marks |

**Authority:** Q4(c). Neither table is designated authoritative for a working entry. Each is read for a different purpose, and they can disagree, for example:
- after the restart-cancel in (c): orders `CANCELLED`, trade `PENDING`;
- after a cancel that missed fills (Q4(e)(iii)): orders `CANCELLED` with `qty_filled 0`, trade `FAILED`, broker position present.

### (c) Exactly what `rehydrate_from_store` reads and defaults, and what then happens

**Read** — `get_open_orders_for_rehydration` (WT 1066-1103 / TW 1041-1078):

```sql
SELECT o.order_id, o.status, o.transaction_type, o.qty_requested, o.price, o.placed_at,
       t.symbol, o.trade_id, o.leg, t.order_protocol, t.direction
FROM orders o JOIN trades t ON t.trade_id = o.trade_id
WHERE o.status IN ('PENDING', 'SUBMITTED', 'OPEN', 'PARTIAL', 'TRIGGER_PENDING')
ORDER BY o.placed_at
```

**Built** — `order_monitor.py` 386-482 (MATCH):

| Step | Lines | Code |
|---|---|---|
| Orphan detect | 408 | `self._cleanup_orphaned_pending_trades(state_store)` — **detect-only** WARNING `order_monitor.orphaned_pending_trade_detected`, for `PENDING` trades with no orders row |
| Synthetic id | 423 | `synthetic_internal = broker_order_id` |
| OSM register | 432-441 | `self._osm.register(synthetic_internal)` → state `PENDING` (`order_state_machine.py` 159-175) |
| "Bring OSM forward" | 443-450 | `if status in ("OPEN", "PARTIAL", "TRIGGER_PENDING", "SUBMITTED"): try: self._osm.transition(synthetic_internal, status) except Exception: pass`. With `_TRANSITIONS["PENDING"] = ("SUBMITTED", "FAILED", "UNKNOWN_IN_FLIGHT")` (`order_state_machine.py` 100-101), **only `SUBMITTED` succeeds**. OPEN, PARTIAL and TRIGGER_PENDING raise `InvalidTransitionError` and are swallowed, so the OSM stays `PENDING`. |
| `placed_at` | 452-456 | Parsed from the row, else `now_ist()` |
| `_WatchEntry` | 462-471 | `side=row["transaction_type"] or ""`, `qty=int(row["qty_requested"] or 0)`, `expected_price=float(row["price"] or 0.0)` → **0.0** for ENTRY, `leg=row["leg"] or ""` |
| **Defaults** | `_WatchEntry` 58-77 | `filled_qty = 0`, `avg_fill_price = 0.0`, `tgt_price = 0.0`, `sl_price = 0.0`, `status_message = ""`, `partial_since = None` |
| Log | 478-481 | INFO "order_monitor rehydrated %d orders from state_store" (count only) |

`OrderPlacer.rehydrate_fill_map` (773-840, MATCH) rebuilds `_fill_map` only for SL/TGT/EOD. Its docstring:

> "ENTRY legs are intentionally skipped: their reservation_id is gone post-restart and capital state is reconstructed by fund_manager.rehydrate_from_open_trades."

`trades.reservation_id` is persisted (954/954). What is gone is the in-memory reservation, because `rehydrate_from_open_trades` replays only OPEN/PARTIAL trades.

**What then happens** — HARNESS, one poll cycle, unchanged monitor code, `placed_at` 5 minutes old:

| Persisted `orders.status` | OSM after rehydrate | Broker `history[-1]` | Published | Tracked after | Logs ≥ INFO |
|---|---|---|---|---|---|
| PENDING / OPEN / PARTIAL | **PENDING** | `COMPLETE`, filled 3/3 | **nothing** | **yes** | ERROR `order_monitor.process_order_failed` |
| PENDING / OPEN / PARTIAL | PENDING | `OPEN`, filled 0 | `OrderStatusChanged(CANCELLED, qty_filled=0)` after a cancel | no | `pending_to_open_auto_step` · `fill_timeout` · `timeout_cancelled` |
| PENDING / OPEN / PARTIAL | PENDING | `CANCELLED`, filled 1 | **nothing** | **yes** | ERROR `order_monitor.process_order_failed` |
| SUBMITTED (never written) | SUBMITTED | `COMPLETE`, filled 3 | `OrderStatusChanged(COMPLETE, 0)` + `OrderFilled(filled_qty=3)` | no | `order_monitor.complete` |
| SUBMITTED | SUBMITTED | `OPEN`, filled 0 | `OPEN(0)`, then `CANCELLED(0)` | no | `fill_timeout` · `timeout_cancelled` |
| SUBMITTED | SUBMITTED | `CANCELLED`, filled 1 | `CANCELLED(0)` | no | — |

**Why nothing is published** for `COMPLETE` or `CANCELLED` from `PENDING`: `_safe_transition` (1211-1351) catches `InvalidTransitionError`. PENDING → COMPLETE or CANCELLED is not an inversion, not terminal-to-terminal, not the PENDING → OPEN auto-step and not same-state, so it reaches:

```python
if (from_state is not None and from_state not in TERMINAL_STATES) or \
   (to_state_exc is not None and to_state_exc not in TERMINAL_STATES):
    raise
```
(1297-1300)

The exception propagates through `_handle_complete` or `_handle_terminal` and `_process_order` to `_poll_cycle`. There it is logged by `self._log.exception("order_monitor.process_order_failed", ...)` (626-630), and the entry stays tracked, so the same happens on every cycle.

**Downstream in `OrderPlacer`** (MATCH), for the events that *are* published:

| Handler | Lines | Result |
|---|---|---|
| `_on_order_status_changed` | 1943-1946 | `fill_entry = self._fill_map.pop(internal_id, None)` → `if fill_entry is None: return`. No release, no `FAILED` mark, no alert. The trade stays **`PENDING`**. |
| `_on_order_filled` | 1776-1780 | `if fill_entry is None: # Not our trade ... return`. No commit, no `record_entry_fill`, **no SL/TGT**. |
| `_on_order_partially_terminated` | 1811-1815 | Same silent return |

`OrderManager` still writes the published status to `orders` (148-171).

### (d) Log or alert when a protection becomes unavailable, or a silent early return?

| Protection | After a restart | Log / alert |
|---|---|---|
| OSM resumed at the persisted status (`rehydrate_from_store` 443-450) | Fails for OPEN/PARTIAL/TRIGGER_PENDING; OSM stays `PENDING` | **Silent** (`except Exception: pass`) |
| FIX-141 pending-R:R cancel (`_check_price_movement_cancel` 1151-1152) | `if entry.tgt_price <= 0 or entry.sl_price <= 0 or entry.expected_price <= 0: return` — all three are 0 | **Silent** |
| ENTRY in `_fill_map` (`rehydrate_fill_map` 819-820) | Skipped | INFO count of **exit** legs only; nothing per ENTRY |
| Entry fill → commit, OPEN, SL/TGT (`_on_order_filled` 1778-1780) | Returns | **Silent** |
| Partial terminal → commit, OPEN, SL/TGT (1813-1815) | Returns | **Silent** |
| Zero-fill terminal → release, trade FAILED (1945-1946) | Returns; trade stays `PENDING` | **Silent** |
| Fill or cancel detection when the broker is already `COMPLETE` or `CANCELLED` | Exception every poll; nothing published | ERROR `order_monitor.process_order_failed` with traceback, every cycle. **No Telegram:** `core/logger.py` 33 says "Does not send alerts". |
| Capital reservation (`rehydrate_from_open_trades`) | Not re-applied for `PENDING` | **Silent.** Its `anomalies` list covers only replayed OPEN/PARTIAL trades. |
| Once filled: CHECK2 in-flight | "no action; fill path will adopt" | WARNING log every reconcile cycle, tier COSMETIC, no Telegram. Under HARD_KILL: flatten intraday (CRITICAL). |
| Detection of crashed `PENDING` trades with no orders row | `_cleanup_orphaned_pending_trades` | WARNING `order_monitor.orphaned_pending_trade_detected`; recovery is deferred to the reconciler |
| Rehydration itself | — | INFO "rehydrated %d orders" (count only) |

**MEASURED, TW-LOG 03–15 Sep:**

| Line | Count |
|---|---|
| `process_order_failed` | 0 |
| `orphaned_pending_trade_detected` | 0 |
| `pending_to_open_auto_step` | 0 |
| rehydrated > 0 | 0 of 16 boots |

### (e) Recoverable from existing data, or is a schema change unavoidable? (description only)

| Value | Recoverable from existing local data? | Where it exists today |
|---|---|---|
| Stop | **Yes** | `trades.sl_initial`, 954/954, joinable via `orders.trade_id` (773/773 ENTRY rows join) |
| Target | **Yes** | `trades.tgt_initial` 954/954; `trades.tgt_risk_reward_applied` 145/145 since 01-Sep |
| Direction | **Yes** | `trades.direction` 954/954; `orders.transaction_type` 773/773 (side matches on 773/773) |
| Requested quantity | **Yes** | `orders.qty_requested` 773/773 = `trades.qty_planned` |
| Reservation | **Yes**, as data | `trades.reservation_id` 954/954 → `fm_ledger` RESERVE row (145/145 since 01-Sep); `_restore_reserve_from_ledger` reads it for recovery trades |
| Intended price as derived | **Yes**, pre-FIX-075 and pre-snap | `trades.entry_target_price` 954/954 |
| Price actually used after FIX-075 | **Only when a top-up fired** | Free text in TOP_UP `reason`, 2 dp, 8 rows ever |
| Submitted, tick-snapped price | **No** | The column `orders.price` exists and is never written for ENTRY (0/773, PPV-Q10(b)). Broker order row `price` — the adapter's typed history drops it. |
| Filled or outstanding quantity of a working order | **No** | The column `orders.qty_filled` exists and is not written on COMPLETE (0/773 > 0, PPV-Q10(c)). `trades.qty_filled` is set only after a fill handler runs. Broker `filled_quantity` (mapped) and `pending_quantity` (not mapped). |

**Summary:** every one of the five values has an existing column. Two of them (submitted price, filled quantity) are not written, so for orders already placed they exist only at the broker. Nothing in this inventory requires a new column. The OSM state and the in-memory `_FillEntry` fields (`side`, `intent`, `sl_price`, `tgt_price`, `tgt_risk_reward`, `reservation_id`) are rebuilt from nothing at restart; every one has a persisted source listed above.

---

## Q6 — PARTIAL FILL IF EXECUTION IS IMMEDIATE

**Status:** PARTIAL. Whether Kite reports these shapes is NOT ESTABLISHED. The code behaviour is ESTABLISHED by reading and by HARNESS.
**WT↔VM:** MATCH (`order_monitor.py`, `order_placer.py`, `slippage_recorder._on_order_filled`).
**Paper↔live:** DIFFER. Paper `_synth_fill` always fills the full quantity in one event, so (a) and (b) are reachable only live (FF-F2).
**Exercised:** no. TW-LOG `partial_fill` 0 · `partial_terminated` 0 · `partial_entry_terminated_via_status_changed` 0. TW-DB `is_partial = 1` on 0 rows (FF-F2).

### (a) Terminal status with `filled_qty > 0` and no cancel of our own: handled, or falls through?

**It falls through to the zero-fill branch**, unless a `PARTIAL` poll happened earlier.

1. `_process_order` reads `filled_qty = latest.filled_qty` (764), but dispatches:
   - `CANCELLED` → `self._handle_terminal(entry, "CANCELLED")` (779-780);
   - `REJECTED` → `self._handle_terminal(entry, "FAILED")` (782-783).

   Neither call passes `filled_qty`.
2. `_handle_terminal` publishes `OrderPartiallyTerminated` only `if entry.filled_qty > 0:` (1033). `entry.filled_qty` is set only by `_handle_partial` (895-897).
3. `_safe_transition` publishes `OrderStatusChanged(status=CANCELLED, qty_filled=entry.filled_qty)` (1323, 1334), which is **0**.
4. `OrderManager` writes `orders.status = CANCELLED, qty_filled = 0, avg_fill_price = NULL`.
5. `OrderPlacer._on_order_status_changed` → `if event.qty_filled <= 0:` (1963) → WARNING `order_placer.entry_cancelled_zero_fill` → `self._fm.release(... reason=f"entry_{status.lower()}_zero_fill")` → trade **FAILED**.
   - The Telegram "ORDER REJECTED" fires only for FAILED/REJECTED, not CANCELLED.
   - No SL or TGT is placed.
6. The broker position that exists is then seen only by CHECK2 as an untracked (human) position — INFO once a day, plus a Telegram once a day if naked — and by the HARD_KILL and EOD residual broker-position sweeps (Q4(d), Q4(e)(iii)).

**HARNESS** (tracked at SUBMITTED, requested 3):

| Broker history | Published | Cancels sent |
|---|---|---|
| `CANCELLED` filled 1 | `OrderStatusChanged(CANCELLED, 0)` only | 0 |
| `OPEN` filled 1, then `CANCELLED` filled 1 | `OPEN(0)`, `CANCELLED(0)` | 0 |
| `PARTIAL` filled 1 (contrast) | `PARTIAL(1)`, `OrderPartiallyTerminated(1)`, `CANCELLED(1)` | 1 (FIX-130) |

A partial-fill fallback exists in `_on_order_status_changed` (`if event.qty_filled > 0:`, 2023-, logging `partial_entry_terminated_via_status_changed`), but it is reachable only when `entry.filled_qty` was already set by a `PARTIAL` poll.

Any other terminal string, such as `EXPIRED`, has no mapping: WARNING `order_monitor.unknown_status`, and the order stays tracked (PPV-Q9 item 1).

### (b) `COMPLETE` with a partial quantity: what gets recorded?

**The filled quantity is taken as the position, with no comparison against the request.**

| Step | Where | What is recorded |
|---|---|---|
| Monitor | `_handle_complete` 989-1012 | `final_qty = filled_qty if filled_qty > 0 else entry.qty` → `OrderFilled(filled_qty=final_qty, avg_fill_price=final_price, …)`. HARNESS: `COMPLETE` filled 1 of 3 → `OrderFilled(filled_qty=1)`. |
| `orders` | `OrderStatusChanged(COMPLETE, qty_filled=entry.filled_qty)` | `qty_filled 0`, `avg_fill_price NULL` (PPV-Q10(c)) |
| Capital | `_handle_entry_fill` → `commit_to_used(... actual_qty=event.filled_qty)` (`order_placer.py` 2118-2122) | Margin for the filled quantity; `excess = res.margin - actual_margin` is returned (`fund_manager.py` WT 945 / TW 947; docstring "filled quantity (may be < reserved qty)") |
| `trades` | `record_entry_fill(... qty_filled=event.filled_qty)` | `status = 'OPEN'`, `qty_filled` = the filled quantity, `entry_actual_price` |
| Exits | `_place_limit_triple_exits(... qty_filled=int(event.filled_qty))` (2160, 2168) | SL/TGT sized to the filled quantity |
| `order_execution_log` | `SlippageRecorder._on_order_filled` (117-152) | `"qty": qty_req`, `"filled_qty": ev.filled_qty or None`, `"is_partial": 1 if (qty_req and ev.filled_qty and ev.filled_qty < qty_req) else 0`, `"status": "COMPLETE"` |
| Remainder | — | Nothing tracks, cancels or re-orders it (the order is untracked at 1020; FF-F4) |
| Alert | — | None. `order_monitor.complete` INFO logs the price and slippage only. |

### (c) Any comparison of requested vs filled quantity on a terminal ENTRY?

**One, and it only records.**

Search: regex over `broker/ orders/ capital/ signals/ core/ main.py` in both trees for `filled_qty` or `qty_filled` compared with `qty` / `requested` / `planned`, and for `is_partial`.

| Site | Kind | Effect |
|---|---|---|
| `orders/slippage_recorder.py` 142 (both trees) | `ev.filled_qty < qty_req` | Sets `order_execution_log.is_partial`. Record only; subscribed to `OrderFilled` only (113), so partial-then-terminated entries write no OEL row. |

Other results, not requested-vs-filled comparisons on a terminal ENTRY:
- `core/candle_math.py` 445-447 — an unrelated candle-slot `is_partial`;
- `core/state_store.py` WT 2632 / TW 2534 — a column-name list.

Nearby code that uses the two quantities **without comparing** them:
- `order_placer.py` puts `fill_entry.qty` only into log extras (1842, 1970, 2032) and a Telegram body (1902: `f"{event.symbol}: {qty_filled}/{fill_entry.qty} qty filled"`).
- `commit_to_used` recomputes margin from `actual_qty` with no quantity test.

Position-level comparisons, which are not order-level:
- the reconciler's `broker_qty == local_qty` / `broker_qty < local_qty` / else, with `local_qty = trade["qty_filled"] or 0` (WT 888-916 / TW 892-920);
- these compare the broker **position** with `trades.qty_filled` for OPEN/PARTIAL trades, not the requested quantity.

---

## 9. OBSERVED IN PASSING (not asked; no fix proposed)

**The broker's status message never reaches `OrderStatusChanged.rejection_reason`.**
- `_process_order` sets `entry.status_message = getattr(latest, "status_message", "") or ""` (`order_monitor.py` 766).
- `OrderHistoryEntry` (adapter 170-177, frozen) has no `status_message` attribute; the adapter maps Kite's `status_message` into `rejection_reason` (WT 1169 / TW 1208).
- So the `getattr` always returns `""`, and `_safe_transition` publishes `rejection_reason=None` (1328-1332).
- **TW-DB:** `orders.rejection_reason` is non-null on 4 rows only — ENTRY CANCELLED ×3 (the FIX-179 remediation text, PPV-Q9 item 10) and SL CANCELLED ×1.

---

## 10. NOT ESTABLISHED — CONSOLIDATED

| Q | Item |
|---|---|
| Q1(c) | Whether the broker or NSE accepts `validity=IOC` for NSE equity MIS and CNC LIMIT orders (needs a broker source; not called) |
| Q1 | How Kite reports an IOC order's partial execution (status string, filled and pending quantities) |
| Q1(e) | Which orders in BOOK were placed by the system (DAY on 30/30 is EVIDENCE of the default applied that day) |
| Q3 | The exchange time of any quote used at order construction (never captured) |
| Q3 | Top-of-book size at order construction (never captured) |
| Q4(b) | The paper `orders.status` sequence (not traced) |
| Q4(e) / Q6 | Kite's status string for a partially filled order (`PARTIAL` vs `OPEN` with `filled_quantity > 0`); kiteconnect defines neither |
| Q6(a) | Whether a broker- or exchange-initiated cancel with fills occurs for these orders (0 observed) |
| Q6(b) | Whether Kite ever reports `COMPLETE` with `filled_quantity < quantity` |
| Q5 | Behaviour on a real restart with a working entry (0 of 16 boots; established only by code reading and HARNESS) |

---

## 11. REPRODUCTION (read-only; scripts are session scratch)

**Scratch directory:** `C:/Users/rama/AppData/Local/Temp/claude/D--Projects-trading-system/fcb198e3-87be-46d0-9a7e-0be80c67edc4/scratchpad/`

**VM invocation:** every VM script ran as `ssh trading-sbx 'python3 -B -' < <script>`, opening SQLite with `mode=ro` and `PRAGMA query_only=1`. Nothing was written on the VM.

| Script / command | Answers | What it does |
|---|---|---|
| `em_q3.py` | Q3(a) | `screener_results.market_data_snapshot` bid/ask/ltp population and spread percentiles; `market_execution_context` ENTRY population |
| `em_q3c.py` | Q3(c) | Exact log matching `trade_created` → M-S1 line → FIX-128 line → `call_start` → `entry_placed`; percentiles by linear interpolation |
| `em_q4_pending.py` | Q4(a) | "Position cap reached" lines against ENTRY working intervals from `orders.placed_at` → `filled_at`/`updated_at` |
| `em_q5.py` | Q5(a) | `PRAGMA table_info` of `trades`, `orders`, `fm_ledger`, `signals`, `order_execution_log`; population counts; `fm_ledger` reason samples |
| `grep -c` over `system_2026-09-0[3-9]*.log system_2026-09-1[0-5]*.log` | Q1(e), Q4, Q5 | Patterns: `pending_to_open_auto_step`, `order_monitor rehydrated`, `order_placer.rehydrate_fill_map`, `orphaned_pending_trade_detected`, `process_order_failed`, `partial_fill`, `partial_terminated`, `unknown_status`, `entry_cancelled_zero_fill`, `CHECK2 INFLIGHT_ORPHAN`, `Sweep: marked`, `CHECK2 HUMAN_ORDER`, `pending_status_update_failed`, plus `validity` / `IOC` over `system_*` and `debug_*` |
| `em_q56_harness.py` (local) | Q5(c), Q6 | Stubs `broker.zerodha_adapter` in `sys.modules` (a type-only import), constructs `OrderMonitor(adapter, OrderStateMachine(), bus, log, poll_interval_sec=2, fill_timeout_sec=60, min_pending_rr=0.3)` and calls `rehydrate_from_store` / `track` and `_poll_cycle()` with stubbed `get_order_history` rows |
| `em_fn_parity.py` (local) | §0.2 | AST source hash of each cited function, WT vs TW snapshot |
| Q2(d) (local) | Q2(d) | A verbatim copy of `_round_nearest_to_tick` over 600,000 random prices at six ticks, compared with `urllib.parse.urlencode({"price": snapped})`; control with unsnapped floats |
| BOOK (local) | Q1(e), Q5(a) | `json.load` of `docs/incident/2026-09-03_ANANTRAJ_broker_book.json`; order keys, `validity` counts, history rows (no `account_id` printed) |
