# Strategy-YAML inventory: every key, its reader, and whether it can change a trade (@970aabf)

**Source:** `scratchpad/src970`, an extract of commit `970aabf` (= origin/main, the deployed files). Every citation is `path:line @970aabf`. The running SHA `d3ee69d` differs only in `main.py`, `screening/secondary_screener.py` and `signals/signal_processor.py` (evidence-capture additions). Line numbers in those three files are only guaranteed at 970aabf.
**Method:** read-only. YAML parsed with PyYAML `safe_load` (a data parse, no project code executed). Every key name was grepped across the tree, excluding `tests/` and `docs/`, and each reader was traced to the live entry path: webhook -> signal_processor -> screener -> pricing -> sizing -> risk/reserve -> order_placer -> adapter.
**Provenance labels:** [SRC] = read from source at 970aabf. [DERIVED] = arithmetic on source values and config. [DOC] = a claim made in a code comment or docstring that I did not independently verify. [INF] = inference.
**Raw per-file key/value dump (with YAML line numbers):** `scratchpad/agentD_yaml_dump.txt`.

**Class legend:** EFF = READ-EFFECTIVE, COI = READ-COINCIDENT, OVR = READ-OVERRIDDEN, UNR = READ-UNREACHABLE, NB = READ-NON-BINDING, DSP = READ-DISPLAY-ONLY, NVR = WRITTEN-NEVER-READ.

---

## 0. Headline numbers [SRC/DERIVED]

| measure | value |
|---|---|
| strategy YAML files | **16** (15 `enabled: true` + `pb01_breakout_retest` `enabled: false`) |
| total key instances (sum of per-file top-level key counts) | **565** (12 files x 35 + 4 files x 36) |
| distinct keys (union) | **37** (35 in every file, `sl_gap_buffer_pct` in the 4 gap_* files, `v3_playbook` in pb01 only) |
| instances never consulted on the trading path (NVR + DSP) | **208** (144 NVR + 64 DSP); 13 per file in every file |
| instances read but neutralised (OVR + UNR + NB + COI) | **162** (45 + 72 + 30 + 15); 9 per non-gap live file, 10 per gap file, 23 for pb01 |
| instances that change behaviour (EFF) | **195** (13 per enabled file, 0 for pb01) |
| distinct-key classes | EFF 13 · COI 1 · OVR 3 · UNR 5 · NB 2 · DSP 4 · NVR 9 |
| per-strategy values that actually differentiate live behaviour | `direction`, `intent`, `entry_offset_pct`, `sl_pct`, `pullback_wait_enabled`, `max_concurrent_positions` (plus `name` as the join key) |
| distinct effective parameter profiles among the 15 enabled strategies | **13**. The three `positional_*` strategies are identical in every behaviour-changing key (T3c) |

---

## 1. Enumeration of the 16 YAML files [SRC]

- **Nested blocks:** there are none apart from `active_days` (a YAML list, `[MON..FRI]` in all 16). No YAML carries a `trailing_sl_*` block, a `v3_playbook` block (it is a scalar bool in pb01 only), or any delivery-specific key.
- **No DELIVERY-specific keys exist.** The 3 DELIVERY YAMLs (`positional_*`) have exactly the same 35 keys as the non-gap INTRADAY YAMLs. Their delivery behaviour comes entirely from `intent: "DELIVERY"` plus global config: `position_sizing.delivery_*`, `risk.*delivery*`, `capital.gtt_sl_limit_offset_pct` and `leverage_map.DELIVERY`.
- **Schema fields that appear in no YAML** (defaults apply, `strategies/schema.py`): `trailing_sl_enabled=False` (:105), `trailing_sl_breakeven_trigger_pct=60.0` (:106), `trailing_sl_partial_lock_trigger_pct=80.0` (:107) and `trailing_sl_partial_lock_sl_pct=40.0` (:108). `sl_gap_buffer_pct` defaults to `0.0` (:90) in the 12 files that omit it, and `v3_playbook` defaults to `False` (:134) in the 15 files that omit it.
- **Schema-required keys (no default; a missing key aborts the boot with `ConfigSchemaError`, `extra="forbid"` at schema.py:50):** `name`, `display_name`, `description`, `direction`, `intent`, `order_protocol`, `pipeline`, `horizon`, `entry_method`, `sl_method`, `tgt_method`, `smart_tgt_enabled` and `pullback_wait_enabled` (schema.py:53-111). Several of these are NVR or DSP. They must be present and valid for the enum validators, but no trading path reads their value.

### T1. Presence matrix — 37 distinct top-level keys × 16 files (X = key present in the YAML)

| # | key | fpl | fps | gfl | gfs | ggl | ggs | ohbs | olbl | pb01 | pml | psr | psl | rbl | rbs | vbl | vrs | files |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `name` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 2 | `display_name` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 3 | `description` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 4 | `direction` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 5 | `intent` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 6 | `enabled` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 7 | `order_protocol` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 8 | `pipeline` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 9 | `horizon` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 10 | `entry_method` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 11 | `entry_offset_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 12 | `sl_method` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 13 | `sl_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 14 | `sl_atr_multiplier` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 15 | `sl_min_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 16 | `sl_max_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 17 | `sl_gap_buffer_pct` | · | · | X | X | X | X | · | · | · | · | · | · | · | · | · | · | 4 |
| 18 | `tgt_method` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 19 | `tgt_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 20 | `tgt_risk_reward` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 21 | `tgt_atr_multiplier` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 22 | `smart_tgt_enabled` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 23 | `smart_tgt_trail_trigger_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 24 | `smart_tgt_trail_step_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 25 | `pullback_wait_enabled` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 26 | `pullback_wait_tolerance_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 27 | `pullback_wait_timeout_sec` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 28 | `min_score` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 29 | `min_volume_surge` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 30 | `min_adr_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 31 | `max_spread_pct` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 32 | `lot_size` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 33 | `max_concurrent_positions` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 34 | `v3_playbook` | · | · | · | · | · | · | · | · | X | · | · | · | · | · | · | · | 1 |
| 35 | `entry_start_time` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 36 | `entry_end_time` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |
| 37 | `active_days` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 16 |

| file | keys |
|---|---|
| `first_pullback_long.yaml` (fpl) | 35 |
| `first_pullback_short.yaml` (fps) | 35 |
| `gap_fade_long.yaml` (gfl) | 36 |
| `gap_fade_short.yaml` (gfs) | 36 |
| `gap_go_long.yaml` (ggl) | 36 |
| `gap_go_short.yaml` (ggs) | 36 |
| `open_high_breakdown_short.yaml` (ohbs) | 35 |
| `open_low_breakout_long.yaml` (olbl) | 35 |
| `pb01_breakout_retest.yaml` (pb01) | 36 |
| `positional_momentum_long.yaml` (pml) | 35 |
| `positional_sector_rotation.yaml` (psr) | 35 |
| `positional_swing_long.yaml` (psl) | 35 |
| `range_breakout_long.yaml` (rbl) | 35 |
| `range_breakout_short.yaml` (rbs) | 35 |
| `vwap_bounce_long.yaml` (vbl) | 35 |
| `vwap_rejection_short.yaml` (vrs) | 35 |
| **TOTAL (sum of per-file key counts)** | **565** |
| **distinct keys (union)** | **37** |

### T2. Keys with ONE value in all 16 files (15 keys)

| key | value (all 16) | class |
|---|---|---|
| `entry_method` | `LIMIT` | READ-EFFECTIVE |
| `sl_method` | `FIXED_PCT` | READ-EFFECTIVE |
| `tgt_method` | `RISK_REWARD` | READ-EFFECTIVE |
| `tgt_pct` | `0.0` | READ-UNREACHABLE |
| `tgt_risk_reward` | `1.5` | READ-EFFECTIVE |
| `smart_tgt_trail_trigger_pct` | `0.005` | WRITTEN-NEVER-READ |
| `smart_tgt_trail_step_pct` | `0.003` | WRITTEN-NEVER-READ |
| `pullback_wait_tolerance_pct` | `0.005` | WRITTEN-NEVER-READ |
| `pullback_wait_timeout_sec` | `180` | WRITTEN-NEVER-READ |
| `min_score` | `0` | READ-OVERRIDDEN |
| `min_adr_pct` | `0.005` | READ-UNREACHABLE |
| `max_spread_pct` | `0.005` | READ-EFFECTIVE |
| `lot_size` | `1` | READ-OVERRIDDEN |
| `entry_start_time` | `09:25` | READ-OVERRIDDEN |
| `active_days` | `[MON,TUE,WED,THU,FRI]` | WRITTEN-NEVER-READ |


---

## 2. Classification of every key in the union (37 keys + 4 schema-only fields)

**pb01 routing note [SRC].** This is why pb01's keys all count as UNR in T4. The only scanner mapped to `pb01_breakout_retest` carries `scanner_type: eod` (`config/scan_webhook_map.yaml:84`). The receiver handles it at `signals/webhook_receiver.py:563-564`: `if getattr(_entry, "scanner_type", "intraday") == "eod":` / `return self._handle_eod(scanner_name, raw_body)`. That branch runs before the only two enqueue sites (`webhook_receiver.py:995`, `:1049`). No other producer writes to `signal_queue` (grep: `signal_processor.py:426` and `:1520` only re-queue items already in the queue). So no per-signal reader ever executes for pb01. `enabled: false` is a second, fail-closed guard behind that routing (`strategies/control.py:81-83` -> `signal_processor.py:963-972`). The PB-01 watchlist does not read pb01's YAML. It uses `watchlist.*` in system_config.yaml:619-631 (its own 09:20-11:00 window, `playbook_scanner`). The class column below is the key-level class for a strategy that reaches the path. T4 applies the pb01 override.

| # | key | class | reader(s) @970aabf (quoted) | what it changes / why it is neutralised |
|---|---|---|---|---|
| 1 | `name` | EFF | `strategies/loader.py:149` `strategies[cfg.name] = cfg`; `signals/signal_processor.py:948` `strategy_obj = self._strategies.get(strategy_name)` (strategy_name comes from scan_webhook_map, :939-942); `:1120` `perf_weight=self._perf_weights.get(strategy_obj.name, 1.0)` | Join key: the map's `strategy:` value must equal a YAML `name`, otherwise the signal is REJECTED_UNKNOWN_STRATEGY (:949-953). The per-strategy cap (`:765` `"FROM trades WHERE strategy = ?"`), the governor (`:986-988`) and `trades.strategy` use the map's string, which equals `name` in all 16 files. The `perf_weights` lookup always returns 1.0 (§6b). The S10 map-vs-YAML cross-check does not run at boot: `main.py:3159-3162` passes no `scan_webhook_map_path` (loader.py:152-153). |
| 2 | `display_name` | DSP | `ops_dashboard/backend/readers/config_reader.py:69` `"display_name": s.get("display_name", name),`; `services/strategy_meta.py:75` | Dashboard labels only. |
| 3 | `description` | NVR | only `strategies/schema.py:55` `description: str` (required) | Must be present; the value is never read. The two dashboard `description` hits (`system_logs.py:223`, `trade_logs.py:602`) are DB-row fields, not strategy fields. |
| 4 | `direction` | EFF | `signal_processor.py:1775` `direction = strategy.direction`; sign branches at `:1781-1784`, `:1836-1839`, `:1858-1871`, `:1885-1888`, `:1926-1936`; `:1034-1035` `side = "BUY" if _dir in ("LONG", "BUY") else "SELL"`; `:1000` `direction=strategy_obj.direction,` -> `screening/step_executor.py:266-269` (VWAP), `screening/hard_gate.py:88` (circuit proximity) | Signs of the entry offset, SL, bounds and TGT; order side; the 10-pt VWAP screen step; the circuit-proximity reject; `CONTRARY_POSITION` (`capital/risk_engine.py:771`); the symbol+direction daily rule (`signal_processor.py:839`). The RSI branch (`step_executor.py:313-316`) is unreachable because `rsi` is always None (secondary_screener.py:414), so that step scores 0.5. |
| 5 | `intent` | EFF | `strategies/control.py:76` `intent = getattr(strategy, "intent", None)`; `signal_processor.py:1117` (sizer), `:1313` (one-trade rule), `:1316` (risk), `:1329` (reserve), `:1452` (placer) | Selects the book: `capital/position_sizer.py:356` `bucket = "intraday" if intent in _INTRADAY_INTENTS else "positional"`. Selects delivery-only sizing limits (:374-384) and leverage (`:388` `self._leverage_map.get(intent, 1.0)`, i.e. 5.0 vs 1.0). Applies the delivery caps and loss/sector twins (`risk_engine.py:316-343`, `:564-570`, `:652-656`) and the reserve bucket (`capital/fund_manager.py:557` `bucket = self._bucket_for_intent(intent)`). Sets the product, MIS vs CNC (`broker/zerodha_adapter.py:586` `broker_code = self._pr.resolve(resolve_intent, "zerodha")`, CNC lock at :593). Sets the exit mechanism: OCO GTT instead of SL+TGT legs (`orders/full_entry_engine.py:151` `if intent == "DELIVERY" and self._cnc_gtt is not None:`). The control-gate branches (`control.py:90,100,107`) are not taken today because force_intraday_only=false and trade_type=BOTH (system_config.yaml:142,149). |
| 6 | `enabled` | EFF | `control.py:77` `enabled = bool(getattr(strategy, "enabled", True))`; `:81-83` `if not enabled:` -> `Verdict(False, "WON'T TRADE — switch disabled", ...)` -> `signal_processor.py:963-972` | The 15 enabled strategies pass. pb01 (false) would be REJECTED_STRATEGY_CONTROL but never arrives (routing note). Also read at boot by the control summary (`main.py:3166-3183`) and by config_auditor A5 (`core/config_auditor.py:268-281`). Neither outcome depends on pb01's value today. |
| 7 | `order_protocol` | DSP | `config_reader.py:79` `"order_protocol": s.get("order_protocol"),` | **The placer ignores it:** `orders/order_placer.py:961` `order_protocol = self._default_protocol`, whose ctor default is `default_order_protocol: str = "LIMIT_TRIPLE"` (:572). `main.py:3061-3087` passes none. 13 files declare `CO_PLUS_TGT`, yet all 16 route to LIMIT_TRIPLE. The enum is validated only by schema.py:161-168. |
| 8 | `pipeline` | DSP | `strategies/taxonomy.py:35` `out[cfg.name] = (cfg.pipeline, cfg.horizon)`; `scripts/strategy_status.py:101`; `reports/daily_report.py:1519` | Labels. The schema calls it "Deliberately INERT" (schema.py:62-68). |
| 9 | `horizon` | DSP | same readers as `pipeline` | Labels. |
| 10 | `entry_method` | EFF | `signal_processor.py:1779` `if strategy.entry_method == "LIMIT":` | LIMIT applies the offset; MARKET would set entry = trigger. The order is sent as LIMIT either way: `place()` defaults to `entry_order_type: str = "LIMIT"` (order_placer.py:888), and the direct path passes no value (signal_processor.py:1446-1460). |
| 11 | `entry_offset_pct` | EFF | `:1780` `offset = float(strategy.entry_offset_pct)`; `:1782` `entry_price = trigger_price * (1.0 - offset)` (LONG), `:1784` `* (1.0 + offset)` (SHORT) | The LIMIT price sits 0.1 % (intraday) or 0.2 % (delivery) on the favourable side of the trigger or live LTP. The value is not passed to the sizer (`signal_processor.py:1112-1121`), so `position_sizer.py:492` uses its default 0.0 (§7 item 1). |
| 12 | `sl_method` | EFF* | `:1801` `sl_method = strategy.sl_method`; `:1802-1811` ATR -> WARNING + `sl_method = "FIXED_PCT"`; `:1813` | Selects FIXED_PCT. *Value-insensitive today:* the only other allowed value (ATR) falls back into the same FIXED_PCT computation under `atr_fallback_mode="WARN"` (`core/config_loader.py:572` default; the key is absent from system_config.yaml). A flip would add only a WARNING, or a reject under HALT. |
| 13 | `sl_pct` | EFF | `:1814` `sl_pct = float(strategy.sl_pct)`; `:1837` `sl_price = entry_price * (1.0 - sl_pct)` | Sets the SL price and the TGT distance (x1.5). It also sets the slippage-abort tolerance, min(abs(trigger - SL) x 0.22, Rs 5) (`order_placer.py:1117-1121` -> `:350-352`), and the GTT SL for DELIVERY. [DERIVED] It does **not** change qty today because the RISK rung never binds (§6a row 5). |
| 14 | `sl_atr_multiplier` | NVR | `schema.py:87`; validator `:222-227` | ATR is not implemented. |
| 15 | `sl_min_pct` | NB | `:1852` `if sl_distance_pct < strategy.sl_min_pct:`; `schema.py:308` `if not (self.sl_min_pct <= self.sl_pct <= self.sl_max_pct):` | FIXED_PCT makes sl_distance_pct = sl_pct, and the schema forces sl_min <= sl_pct <= sl_max, so the branch cannot fire (T3a values: sl_pct 0.008-0.02 inside [0.003, 0.05] or [0.005, 0.08]). |
| 16 | `sl_max_pct` | NB | `:1862` `elif sl_distance_pct > strategy.sl_max_pct:` | Same reason as `sl_min_pct`. |
| 17 | `sl_gap_buffer_pct` (4 files) | UNR | `:1877` `gap_buffer = float(getattr(strategy, "sl_gap_buffer_pct", 0.0))`; `:1878-1882` `... and self._GAP_WINDOW_START <= now_time <= self._GAP_WINDOW_END` with `:1745-1746` = 09:15 / 09:30 | Needs a signal priced between 09:15 and 09:30, but `_process_one` rejects before pricing at `:911` `if not self._mw.is_entry_allowed(now):` (`core/market_windows.py:150` `return self.entry_start <= t < self.entry_end`, entry_start 10:00 at system_config.yaml:28). Unit: `:1883` `factor = gap_buffer / 100.0`, so the value is a **percent** (0.3 means 0.3 %), unlike its fractional `sl_*` siblings. |
| 18 | `tgt_method` | EFF | `:1911` `tgt_method = strategy.tgt_method`; `:1930` `elif tgt_method == "RISK_REWARD":` | Selects the RR target. FIXED_PCT, or ATR (which falls back to FIXED_PCT), would use tgt_pct = 0.0 and then hit TGT_DISTANCE_TOO_SMALL (:1945-1951). |
| 19 | `tgt_pct` | UNR | `:1925` `tgt_pct = float(strategy.tgt_pct)`, only inside `if tgt_method == "FIXED_PCT":` (:1924); schema.py:322-325 applies the same condition | All 16 files use RISK_REWARD. |
| 20 | `tgt_risk_reward` | EFF | `:1932` `ratio = float(strategy.tgt_risk_reward)`; `:1459` `tgt_risk_reward=getattr(strategy_obj, "tgt_risk_reward", None)` -> order_placer.py:1606 -> `:2872-2879` `rr_ratio=self._resolve_fill_rr(fill_entry.tgt_risk_reward, ...)` | Target = entry +/- 1.5 x SL distance, set at the signal and recomputed from the actual fill. The schema default of 2.0 (schema.py:95) is not used by any file. |
| 21 | `tgt_atr_multiplier` | NVR | `schema.py:96`; validator `:222-227` | ATR is not implemented. |
| 22 | `smart_tgt_enabled` | NVR | `schema.py:99` (required) | No reader. |
| 23 | `smart_tgt_trail_trigger_pct` | NVR | `schema.py:100`; validator `:236-242` | The **global** `smart_tgt.trigger_pct` is used instead (order_placer.py:2230), and only in the CO_PLUS_TGT branch, which never runs. |
| 24 | `smart_tgt_trail_step_pct` | NVR | `schema.py:101` | Same situation, via the global `smart_tgt.step_pct` (order_placer.py:2231). |
| 25 | `pullback_wait_enabled` | EFF | `:1082` `if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:` -> `:1085` `quotes = self._quote_fn([symbol])` -> `:1098-1100` re-derive | **The name is misleading.** false (10 files) re-anchors entry, SL, TGT, qty and reservation on a fresh LTP; true (6 files) uses the webhook trigger. No pullback wait exists on the live path: `EntryGate.add()` has no production caller. The only `add(` is the docstring at `screening/entry_gate.py:103`, and the code comment at `signal_processor.py:2236-2238` says "This path is DORMANT today: nothing calls EntryGate.add()". |
| 26 | `pullback_wait_tolerance_pct` | NVR | `schema.py:112`; `entry_gate.py:69` is a comment (`tolerance_pct: float    # strategy.pullback_wait_tolerance_pct`) | No code builds a `WatchEntry` from a strategy. |
| 27 | `pullback_wait_timeout_sec` | NVR | `schema.py:113`; `entry_gate.py:70` is a comment | Same reason as `pullback_wait_tolerance_pct`. |
| 28 | `min_score` | OVR | `screening/secondary_screener.py:317-321` `strategy.min_score if strategy.min_score > 0 else score_result.min_pass_score` | 0 is a sentinel for the global 60 (scoring_weights.yaml:22). The v3-enforce twin (`:500-505`) is not live (§6a). |
| 29 | `min_volume_surge` | UNR | `secondary_screener.py:236` -> `step_executor.py:251-253` `avg_vol = md.get("avg_volume_20d")` / `if not avg_vol:` / `return 0.0` | `secondary_screener.py:417` `"avg_volume_20d": None,` makes the step 0.0 before the threshold (`:255`) is read. The values differ across files (1.2-2.0) with no effect. |
| 30 | `min_adr_pct` | UNR | `secondary_screener.py:237` -> `step_executor.py:275-278` `atr = md.get("atr")` ... `if not atr or not ltp:` `return 0.0` | `secondary_screener.py:413` `"atr": None,`. The step also compares a percent with a fraction (:279-281), which is moot. |
| 31 | `max_spread_pct` | EFF (wrong unit) | `secondary_screener.py:238` -> `step_executor.py:393-395` `spread_pct = ((ask - bid) / mid) * 100.0` / `max_spread = thr.get("max_spread_pct", 0.1)` / `return 1.0 if spread_pct <= max_spread else 0.0` | A percent spread is compared with 0.005, so the step passes only if the spread is <= **0.005 % of mid**. bid/ask are the top of depth (`zerodha_adapter.py:1774-1779`); empty depth gives 0/0, then mid 0, then a neutral 0.5 (`step_executor.py:386-391`). [DERIVED] The step weighs 5 against a 65 ceiling (§6a row 1). A 0 here caps a signal at 60 before 10:15 and at 59 after 10:15, when time_of_day drops from 1.0 to 0.8 (`step_executor.py:364-370`). So after 10:15, a failed spread step alone keeps a signal below the 60 pass mark. |
| 32 | `lot_size` | OVR | `position_sizer.py:309-311` `if lot_size == 1 and self._instrument_cache is not None:` / `lot_size = self._instrument_cache.lot_size(symbol)` | 1 is a sentinel for the instrument-cache value; 1 is kept if the lookup fails (:312-313). |
| 33 | `max_concurrent_positions` | EFF | `signal_processor.py:760` `max_strat_pos = getattr(strategy_obj, "max_concurrent_positions", 2)`; `:773` `if effective > max_strat_pos:` | REJECTED_STRATEGY_POSITION_LIMIT at 2 (11 files) or 3 (the 4 gap_* files), checked inside `portfolio_lock` (`:1307-1311`). |
| 34 | `v3_playbook` (pb01 only) | UNR | `main.py:3648` `v3_scope_fn=lambda s: bool(getattr(s, "v3_playbook", False)),`, consulted only via `signal_processor.py:1150` `if _amode == "enforce" and self._allocator.in_scope(strategy_obj):` (allocator_mode is "shadow", system_config.yaml:565); `:1603` copies it into the shadow `V3Signal` (no reader in `v3_chain/` beyond the field at `v3_chain/models.py:49`) | Also display: `scripts/strategy_status.py:81-82` drops pb01 from the status table. |
| 35 | `entry_start_time` | OVR | `market_windows.py:166` `if not self.is_entry_allowed(now):` then `:169`, `:175` `return time(sh, sm) <= t < time(eh, em)` | 09:25 is earlier than the global 10:00 floor (system_config.yaml:28), so the floor binds. system_config.yaml:29-39 documents this as intended. |
| 36 | `entry_end_time` | COI (15) / UNR (pb01) | `market_windows.py:170`, `:175` | 15:00 equals `trading_hours.entry_end` 15:00 (system_config.yaml:47). pb01's 11:00 is never evaluated. |
| 37 | `active_days` | NVR | `schema.py:139`; validator `:286-296` | Trading days come from `market_windows.py:104` `if d.weekday() >= 5:` plus the holiday list. |
| S1-S4 | `trailing_sl_enabled`, `trailing_sl_breakeven_trigger_pct`, `trailing_sl_partial_lock_trigger_pct`, `trailing_sl_partial_lock_sl_pct` (schema-only, in no YAML) | UNR | `order_placer.py:2177-2178` `and getattr(fill_entry, "strategy_obj", None) is not None` / `and getattr(fill_entry.strategy_obj, "trailing_sl_enabled", False)`; `:2190-2192` | `_FillEntry.__slots__` (:498-503) has no `strategy_obj`, and no `BreakevenManager(` is constructed (only the docstring at `orders/breakeven_manager.py:65`), so `_breakeven_manager` is None. The config_auditor A4 check (`config_auditor.py:228`) runs only when `structure_exit_enabled` (false, system_config.yaml:634; `main.py:3436`). |

Other, non-trading readers (not counted as trading-path readers):
- `orders/shadow_tracker.py:329-334` and `:819-855` read `sl_method`, `sl_pct`, `sl_min_pct`, `sl_max_pct`, `tgt_method`, `tgt_pct` and `tgt_risk_reward`. The tracker is disabled (`shadow_tracker.enabled: false`, system_config.yaml:504; `_on_position_closed` returns early at shadow_tracker.py:273). It is also built without `strategies=` (`main.py:2946-2958`), so `self._strategies` is None (shadow_tracker.py:144) and those branches are dead twice over.
- `scripts/replay_signals.py` (sl_pct, lot_size, min_score), `scripts/strategy_status.py` and `reports/daily_report.py:328` (min_score) are offline or report readers.

---

## 3. Per-strategy value tables (keys whose value differs) [SRC]

T3a and T3b cover the 19 non-identity keys whose values differ. `name`, `display_name` and `description` also differ, trivially. Bold **EFF** marks a key whose differing value the entry path actually reads and acts on.

### T3a. Differing keys that HAVE an entry-path reader (value per strategy; `—` = absent → schema default)

| strategy | `direction` (**EFF**) | `intent` (**EFF**) | `enabled` (**EFF**) | `entry_offset_pct` (**EFF**) | `sl_pct` (**EFF**) | `sl_min_pct` (NB) | `sl_max_pct` (NB) | `sl_gap_buffer_pct` (UNR) | `pullback_wait_enabled` (**EFF**) | `min_volume_surge` (UNR) | `max_concurrent_positions` (**EFF**) | `v3_playbook` (UNR) | `entry_end_time` (COI) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| first_pullback_long | LONG | INTRADAY | true | 0.001 | 0.015 | 0.003 | 0.05 | — | true | 1.3 | 2 | — | 15:00 |
| first_pullback_short | SHORT | INTRADAY | true | 0.001 | 0.015 | 0.003 | 0.05 | — | true | 1.3 | 2 | — | 15:00 |
| gap_fade_long | LONG | INTRADAY | true | 0.001 | 0.01 | 0.003 | 0.05 | 0.3 | false | 1.3 | 3 | — | 15:00 |
| gap_fade_short | SHORT | INTRADAY | true | 0.001 | 0.01 | 0.003 | 0.05 | 0.3 | false | 1.3 | 3 | — | 15:00 |
| gap_go_long | LONG | INTRADAY | true | 0.001 | 0.012 | 0.003 | 0.05 | 0.3 | false | 2.0 | 3 | — | 15:00 |
| gap_go_short | SHORT | INTRADAY | true | 0.001 | 0.012 | 0.003 | 0.05 | 0.3 | false | 2.0 | 3 | — | 15:00 |
| open_high_breakdown_short | SHORT | INTRADAY | true | 0.001 | 0.01 | 0.003 | 0.05 | — | true | 1.3 | 2 | — | 15:00 |
| open_low_breakout_long | LONG | INTRADAY | true | 0.001 | 0.01 | 0.003 | 0.05 | — | true | 1.3 | 2 | — | 15:00 |
| pb01_breakout_retest | LONG | INTRADAY | false | 0.001 | 0.01 | 0.003 | 0.05 | — | false | 1.3 | 2 | true | 11:00 |
| positional_momentum_long | LONG | DELIVERY | true | 0.002 | 0.02 | 0.005 | 0.08 | — | false | 1.5 | 2 | — | 15:00 |
| positional_sector_rotation | LONG | DELIVERY | true | 0.002 | 0.02 | 0.005 | 0.08 | — | false | 1.3 | 2 | — | 15:00 |
| positional_swing_long | LONG | DELIVERY | true | 0.002 | 0.02 | 0.005 | 0.08 | — | false | 1.2 | 2 | — | 15:00 |
| range_breakout_long | LONG | INTRADAY | true | 0.001 | 0.01 | 0.003 | 0.05 | — | false | 1.8 | 2 | — | 15:00 |
| range_breakout_short | SHORT | INTRADAY | true | 0.001 | 0.01 | 0.003 | 0.05 | — | false | 1.8 | 2 | — | 15:00 |
| vwap_bounce_long | LONG | INTRADAY | true | 0.001 | 0.008 | 0.003 | 0.05 | — | true | 1.5 | 2 | — | 15:00 |
| vwap_rejection_short | SHORT | INTRADAY | true | 0.001 | 0.008 | 0.003 | 0.05 | — | true | 1.5 | 2 | — | 15:00 |

### T3b. Differing keys with NO trading-path reader (display-only or never read)

| strategy | `order_protocol` (DSP) | `pipeline` (DSP) | `horizon` (DSP) | `sl_atr_multiplier` (NVR) | `tgt_atr_multiplier` (NVR) | `smart_tgt_enabled` (NVR) |
|---|---|---|---|---|---|---|
| first_pullback_long | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| first_pullback_short | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| gap_fade_long | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| gap_fade_short | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| gap_go_long | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| gap_go_short | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| open_high_breakdown_short | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| open_low_breakout_long | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| pb01_breakout_retest | CO_PLUS_TGT | INTRADAY | NEXT_DAY | 1.5 | 2.5 | true |
| positional_momentum_long | LIMIT_TRIPLE | DELIVERY | SWING | 2.0 | 3.0 | false |
| positional_sector_rotation | LIMIT_TRIPLE | DELIVERY | SWING | 2.0 | 3.0 | false |
| positional_swing_long | LIMIT_TRIPLE | DELIVERY | SWING | 2.0 | 3.0 | false |
| range_breakout_long | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| range_breakout_short | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| vwap_bounce_long | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |
| vwap_rejection_short | CO_PLUS_TGT | INTRADAY | SAME_DAY | 1.5 | 2.5 | true |

### T3c. Effective per-strategy parameter tuple (only READ-EFFECTIVE keys whose value differs; the 15 enabled strategies)

| strategy | `direction` | `intent` | `enabled` | `entry_offset_pct` | `sl_pct` | `pullback_wait_enabled` | `max_concurrent_positions` | profile id |
|---|---|---|---|---|---|---|---|---|
| first_pullback_long | LONG | INTRADAY | true | 0.001 | 0.015 | true | 2 | P1 |
| first_pullback_short | SHORT | INTRADAY | true | 0.001 | 0.015 | true | 2 | P2 |
| gap_fade_long | LONG | INTRADAY | true | 0.001 | 0.01 | false | 3 | P3 |
| gap_fade_short | SHORT | INTRADAY | true | 0.001 | 0.01 | false | 3 | P4 |
| gap_go_long | LONG | INTRADAY | true | 0.001 | 0.012 | false | 3 | P5 |
| gap_go_short | SHORT | INTRADAY | true | 0.001 | 0.012 | false | 3 | P6 |
| open_high_breakdown_short | SHORT | INTRADAY | true | 0.001 | 0.01 | true | 2 | P7 |
| open_low_breakout_long | LONG | INTRADAY | true | 0.001 | 0.01 | true | 2 | P8 |
| positional_momentum_long | LONG | DELIVERY | true | 0.002 | 0.02 | false | 2 | P9 |
| positional_sector_rotation | LONG | DELIVERY | true | 0.002 | 0.02 | false | 2 | P9 |
| positional_swing_long | LONG | DELIVERY | true | 0.002 | 0.02 | false | 2 | P9 |
| range_breakout_long | LONG | INTRADAY | true | 0.001 | 0.01 | false | 2 | P10 |
| range_breakout_short | SHORT | INTRADAY | true | 0.001 | 0.01 | false | 2 | P11 |
| vwap_bounce_long | LONG | INTRADAY | true | 0.001 | 0.008 | true | 2 | P12 |
| vwap_rejection_short | SHORT | INTRADAY | true | 0.001 | 0.008 | true | 2 | P13 |

Distinct effective profiles among the 15 enabled strategies: **13**. Identical in every behaviour-changing strategy key: `positional_momentum_long`, `positional_sector_rotation`, `positional_swing_long`.


Reading T3a/T3c together [DERIVED]:
- The only per-strategy differences that reach behaviour today are `direction`, `intent`, `entry_offset_pct` (0.002 exactly when intent is DELIVERY), `sl_pct` (5 values: 0.008 / 0.01 / 0.012 / 0.015 / 0.02), `pullback_wait_enabled` (re-anchor or not) and `max_concurrent_positions` (2 or 3).
- The following differing values are inert:
  - `min_volume_surge`: 1.2-2.0, unreachable.
  - `sl_min_pct` and `sl_max_pct`: non-binding.
  - `sl_gap_buffer_pct`: unreachable.
  - `entry_end_time` 11:00: pb01, unreachable.
  - `v3_playbook`: unreachable.
  - `order_protocol`, `pipeline`, `horizon`: display only.
  - `sl_atr_multiplier`, `tgt_atr_multiplier`, `smart_tgt_enabled`: never read.
- `positional_momentum_long`, `positional_sector_rotation` and `positional_swing_long` differ only in `min_volume_surge` (1.5 / 1.3 / 1.2, unreachable) and in identity text. They are one behaviour with three name-scoped states: a per-strategy cap of 2 each, governor accounting per name, and `trades.strategy`. The delivery-book cap `risk.max_open_delivery_positions: 3` (system_config.yaml:283) binds across all three.

---

## 4. Branches where a strategy takes a different CODE PATH (not just different values) [SRC]

| # | site @970aabf | selector | today: which strategies take which side | what differs |
|---|---|---|---|---|
| B1 | `signals/webhook_receiver.py:563-564` | `scanner_type` in scan_webhook_map (scan_webhook_map.yaml:84; not a strategy key) | pb01 goes to `_handle_eod` (WatchlistCaptureWorker, shadow); the 15 take the intraday queue | The whole path. pb01 is never enqueued. |
| B2 | `strategies/control.py:81-83` -> `signal_processor.py:963-972` | `enabled` | None of the 15. pb01 would, but is unreachable (B1) | REJECTED_STRATEGY_CONTROL before sizing. |
| B3 | `strategies/control.py:90-113` | `intent` x `force_intraday_only` x `trade_type` | Not taken (false / BOTH) | — |
| B4 | `signal_processor.py:1082-1106` | `pullback_wait_enabled` | **Re-anchor (10):** gap_fade_long/short, gap_go_long/short, range_breakout_long/short, positional_momentum_long, positional_sector_rotation, positional_swing_long (+pb01). **No re-anchor (6):** first_pullback_long/short, open_high_breakdown_short, open_low_breakout_long, vwap_bounce_long, vwap_rejection_short | Re-anchor adds a `get_quote` call and a second `_derive_prices` on the live LTP, so entry, SL, TGT, qty and reservation are all rebased. The slippage guard still measures against the stale `trigger_price` (`:1457`). |
| B5 | `signal_processor.py:1877-1893` | `sl_gap_buffer_pct > 0` and 09:15-09:30 | The 4 gap_* files satisfy the first condition; the time condition is never true (see #17) | — |
| B6 | `signal_processor.py:1779-1784`, `:1801-1846`, `:1911-1941` | `entry_method`, `sl_method`, `tgt_method` | Uniform (LIMIT / FIXED_PCT / RISK_REWARD in all 16) | No divergence. |
| B7 | direction branches: `signal_processor.py:1781-1784`, `:1836-1839`, `:1858-1871`, `:1885-1888`, `:1926-1936`, `:1035`; `step_executor.py:266-269`, `:313-316`; `hard_gate.py:88-...`; `risk_engine.py:769-776`; `signal_processor.py:839` | `direction` | Of the 15 enabled: 9 LONG, 6 SHORT | Mirrored arithmetic and comparisons: the same path with the sign flipped. |
| B8 | `secondary_screener.py:148-165` + `:565-571` | intent -> product (`resolve_product`) | Only MIS-product (INTRADAY) signals can be flagged; DELIVERY resolves to CNC and returns False | Shadow mode: log only (§6a). |
| B9 | `position_sizer.py:356`, `:374-384`, `:388` | `intent` | 12 intraday / 3 delivery | Bucket (intraday_avail vs positional_avail), `delivery_*` vs global limit keys, leverage 5.0 vs 1.0 (system_config.yaml:208,210). |
| B10 | `signal_processor.py:854-856` | intent -> book | per book | The symbol+direction daily rule is counted within the entry's own book. |
| B11 | `risk_engine.py:316-343`, `:564-570`, `:652-656` | `sizing_result.bucket == "positional"` (from intent) | 3 positional | Extra gates: open-delivery cap 3, daily-delivery cap 5, delivery loss and sector twins. |
| B12 | `fund_manager.py:557` (`_bucket_for_intent`, `:2337-2342`) | `intent` | 12 / 3 | Which bucket the money leaves. |
| B13 | `order_placer.py:971-973` | `intent` | 12 / 3 | `required_margin` uses the intent's leverage. |
| B14 | `zerodha_adapter.py:578-600` | intent (+ `force_intraday_only`, `delivery_enabled`) | INTRADAY -> MIS; DELIVERY -> CNC (lock passes: delivery_enabled true, system_config.yaml:155) | Broker product. |
| B15 | `full_entry_engine.py:151-177` | `intent == "DELIVERY"` | 3 positional -> one OCO GTT at fill; 12 intraday -> LIMIT_TRIPLE SL + TGT legs (`order_placer.py:2156-2163`) | Exit mechanism. |
| B16 | `order_placer.py:961` | **not** `order_protocol` | All 16 go LIMIT_TRIPLE | The CO branches never run for any strategy: `:1624-1628`, `:1889-1896`, `:2079-2086`, `:2164-2171`, and SmartTgt registration `:2204-2231`. |
| B17 | `order_placer.py:2174-2193` | `trailing_sl_enabled` (schema-only) | Unreachable (S1-S4) | — |
| B18 | `signal_processor.py:1147-1172` | allocator mode x `in_scope(v3_playbook)` | `shadow`: the enforce hand-off is never evaluated; all strategies take FCFS `_admit_and_place`, plus an `observe()` copy | — |
| B19 | `signal_processor.py:1136-1143`, `:1042` | v3_chain (shadow), retest diverter (None) | Observer only / dormant | — |
| B20 | literal strategy-name branches | — | **None.** A grep of signals/, screening/, capital/, orders/, strategies/, core/, broker/, allocation/ and main.py for all 16 names finds only comments (`signal_processor.py:976`, `market_windows.py:162`, `webhook_receiver.py:117`, `:618`, `order_placer.py:260`) and the watchlist default `playbook_scanner` (`core/config_loader.py:1535`) | — |

Additional notes:
- **Name-scoped state (not branches):** the per-strategy position count (`signal_processor.py:761-772`, `fund_manager.count_live_reservations_for_strategy`), the strategy governor (`strategy_governor.check(strategy_name, ...)`, no intent filter despite its "intraday" label), `trades.strategy`, and slippage `by_strategy` (empty).
- **Display note:** `_emit_signal_alert` titles every entry `INTRADAY SIGNAL` and prints `Smart TGT: enabled | Timeout: 10 min` (signal_processor.py:543-547), including DELIVERY entries and the LIMIT_TRIPLE orders that SmartTgt never tracks.
- **Out of entry-path scope, not traced:** post-entry lifecycle differences by product (MIS square-off vs CNC carry, GTT monitor). The exit-fill cost path derives the product from the protocol, not the intent (`order_placer.py:2328` `product = _PROTOCOL_TO_PRODUCT.get(fill_entry.order_protocol, "")`, which maps LIMIT_TRIPLE to MIS, :425-428). I did not trace whether a DELIVERY GTT exit reaches that handler.

---

## 5. Counts [SRC/DERIVED]

### T4. Per-file classification counts (today; pb01 per its routing — see §2 note)

| file | keys | EFF | COI | OVR | UNR | NB | DSP | NVR | never consulted (NVR+DSP) | read-but-neutralised (OVR+UNR+NB+COI) | effective |
|---|---|---|---|---|---|---|---|---|---|---|---|
| first_pullback_long | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| first_pullback_short | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| gap_fade_long | 36 | 13 | 1 | 3 | 4 | 2 | 4 | 9 | 13 | 10 | 13 |
| gap_fade_short | 36 | 13 | 1 | 3 | 4 | 2 | 4 | 9 | 13 | 10 | 13 |
| gap_go_long | 36 | 13 | 1 | 3 | 4 | 2 | 4 | 9 | 13 | 10 | 13 |
| gap_go_short | 36 | 13 | 1 | 3 | 4 | 2 | 4 | 9 | 13 | 10 | 13 |
| open_high_breakdown_short | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| open_low_breakout_long | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| pb01_breakout_retest | 36 | 0 | 0 | 0 | 23 | 0 | 4 | 9 | 13 | 23 | 0 |
| positional_momentum_long | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| positional_sector_rotation | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| positional_swing_long | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| range_breakout_long | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| range_breakout_short | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| vwap_bounce_long | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| vwap_rejection_short | 35 | 13 | 1 | 3 | 3 | 2 | 4 | 9 | 13 | 9 | 13 |
| **TOTAL** | **565** | **195** | **15** | **45** | **72** | **30** | **64** | **144** | **208** | **162** | **195** |

### T5. Distinct-key (union) classification counts (key-level class for a strategy that reaches the path)

| class | distinct keys | keys |
|---|---|---|
| READ-EFFECTIVE | 13 | `name`, `direction`, `intent`, `enabled`, `entry_method`, `entry_offset_pct`, `sl_method`, `sl_pct`, `tgt_method`, `tgt_risk_reward`, `pullback_wait_enabled`, `max_spread_pct`, `max_concurrent_positions` |
| READ-COINCIDENT | 1 | `entry_end_time` |
| READ-OVERRIDDEN | 3 | `min_score`, `lot_size`, `entry_start_time` |
| READ-UNREACHABLE | 5 | `sl_gap_buffer_pct`, `tgt_pct`, `min_volume_surge`, `min_adr_pct`, `v3_playbook` |
| READ-NON-BINDING | 2 | `sl_min_pct`, `sl_max_pct` |
| READ-DISPLAY-ONLY | 4 | `display_name`, `order_protocol`, `pipeline`, `horizon` |
| WRITTEN-NEVER-READ | 9 | `description`, `sl_atr_multiplier`, `tgt_atr_multiplier`, `smart_tgt_enabled`, `smart_tgt_trail_trigger_pct`, `smart_tgt_trail_step_pct`, `pullback_wait_tolerance_pct`, `pullback_wait_timeout_sec`, `active_days` |
| **total** | **37** | |


- **Total key instances:** 565. **Distinct keys:** 37.
- **Defined but never consulted on the trading path (NVR + DSP):** 208 instances (144 + 64). That is 13 in every one of the 16 files: 9 NVR and 4 DSP.
- **Read but neutralised (OVR + UNR + NB + COI):** 162 instances (45 + 72 + 30 + 15). Per file: 9 for each of the 11 non-gap enabled files, 10 for each of the 4 gap_* files (with `sl_gap_buffer_pct`), and 23 for pb01 (every key with a reader, per the routing note).
- **Effective:** 195 instances, 13 per enabled file. One of the 13 (`sl_method`) is value-insensitive today (#12), and one (`max_spread_pct`) acts in the wrong unit (#31).

---

## 6. Global config keys the ENTRY path reads that cannot change behaviour today [SRC unless marked]

### 6a. Read on the entry path, but at today's values the reader cannot alter an entry decision

| # | key @ file:line | value | reader | why it cannot bind today |
|---|---|---|---|---|
| 1 | `high_score_threshold` scoring_weights.yaml:28 | 80 | `screening/quality_scorer.py:124` `if total_score >= high_thr:` | [DERIVED + DOC] The achievable score ceiling is 65. The code says so at `quality_scorer.py:17-19` ("25/100 pts dead-at-0 + 20 pinned-at-half make >65 algebraically impossible today"). I re-derived it: volume_surge 15 is 0 (avg_volume_20d None) and atr_filter 10 is 0 (atr None); rsi 10 and sector 10 are pinned at 0.5 (None) (`secondary_screener.py:413-417`, `step_executor.py:251-253`, `:275-278`, `:296-298`, `:335-336`). So HIGH is never assigned. `medium_score_threshold` 65 (:29) is reachable only at exactly 65. |
| 2 | `position_sizing.tier_multipliers.HIGH` system_config.yaml:238 | 1.0 | `position_sizer.py:542` `tier_mult = self._tier_multipliers.get(score_tier, 1.0)` | Only used for a HIGH tier, which never occurs (row 1). |
| 3 | `v3_hardgate_mode` scoring_weights.yaml:39 (+ `v3_gate_steps` :40, `v3_freshness_max_sec` :41, `v3_min_pass_score` :42, `v3_high_score_threshold` :43, `v3_medium_score_threshold` :44) | "shadow", [circuit_check, signal_age], 60.0, 50, 75, 56 | `secondary_screener.py:202` `if self._v3_mode == "enforce" and self._hard_gate is not None:` (not taken); `:310-314` shadow = `_log_v3_shadow_compare` | Shadow logs only (`:530-552`); the live path follows the old scorer. |
| 4 | `mis_filter.enabled` / `shadow` / `ttl_days` system_config.yaml:179-181 | true / true / 1 | `secondary_screener.py:148-150` ... `if not self._mis_filter_shadow:` | shadow=true, so the would-drop is logged and the signal falls through. |
| 5 | `position_sizing.risk_per_trade_pct` :225, `delivery_risk_per_trade_pct` :253 | 0.01 / 0.01 | `position_sizer.py:456-457` `risk_rs = total_capital * eff_risk_pct`; binding test `:503-512` | [DERIVED] RISK binds only if the SL distance exceeds eff_risk / eff_conc = 0.01 / 0.10 = 10 % of entry. SL distance = sl_pct <= 0.02 (bounded by sl_max_pct <= 0.08), so the RISK rung never binds and qty = min(capital rung, concentration rung) x tier. The code's own telemetry comment agrees (`position_sizer.py:508-510`, "algebraically never today"). |
| 6 | `position_sizing.max_position_value_pct` :236, `delivery_max_position_value_pct` :259 | 0.40 / 0.40 | `position_sizer.py:721-723` | [DERIVED] final_qty <= raw_qty x effective_mult (tier <= 0.7 reachable; perf_weight 1.0), and raw_qty <= the concentration rung (0.10 x capital / entry). The floor-at-1 (`:605`) also stays below it, because raw_qty >= 1 already implies entry <= 0.10 x capital. The YAML itself notes the delivery twin is "MEASURED UNREACHABLE" (:255-258) [DOC]. |
| 7 | `risk.max_sector_exposure_pct` :313, `delivery_max_sector_exposure_pct` :314, with `sector_cap_mode` :322 | 0.40 / 0.40 / observe | `risk_engine.py:746` `if self._sector_cap_mode == "enforce":` otherwise the WOULD_REJECT log (`:754-763`) | Observe mode never rejects. |
| 8 | `risk.daily_loss_include_unrealized` :324 | false | `risk_engine.py:699` `use_unrealized = self._daily_loss_include_unrealized and mtm_fresh` | The unrealized-inclusive branch is log-only (`:704-718`); realized-only is enforced. The flag gates a shadow branch. |
| 9 | `signal_processor.tgt_min_pct` :348 | 0.003 | `signal_processor.py:1945` `if entry > 0 and abs(tgt_price - entry) / entry < self._tgt_min_pct:` | [DERIVED] The smallest target distance is 1.5 x 0.008 = 0.012 (even 1.5 x sl_min 0.003 = 0.0045), which is above 0.003. |
| 10 | `signal_processor.atr_fallback_mode` (absent from YAML; `config_loader.py:572` default) | "WARN" | `signal_processor.py:1803`, `:1914` | Read only inside the `== "ATR"` branches, and no strategy uses ATR. |
| 11 | `entry_gate.min_effective_rr` :659 | 1.0 | `order_placer.py:938-945` | On the direct path the target comes from the same entry and SL (`signal_processor.py:1934`), so the effective R:R is 1.5 by construction. Only the dormant gate path moves the entry before this check (`order_placer.py:907-914`). |
| 12 | `entry_gate.slippage_buffer` :649 | 2.0 | `order_placer.py:907-914`, only `if release_ltp is not None:` | release_ltp exists only on the EntryGate path, which has no production feeder. |
| 13 | `slippage_control.hard_max_slippage_rs` :673 | 10.0 | `order_placer.py:361` `return min(tol, cfg.hard_max_slippage_rs), sl_dist` | In sl_fraction mode tol <= `absolute_cap_rs` 5.00 (`:352`, yaml :672), so a ceiling of 10 never binds. |
| 14 | `slippage_control.default_max_slippage_rs` :676 and `tiers` :677-681 | 2.00 / table | `order_placer.py:355-356` (flat_tiers mode) | mode is `sl_fraction` (:670). |
| 15 | `slippage_control.overrides` :691-706 | enabled true; `by_price_band`, `by_strategy`, `by_symbol` all `{}` | `order_placer.py:264-276` | Empty maps fall through to the global 0.22 (`return glob, "global"`). |
| 16 | `smart_tgt.trigger_pct` / `step_pct` :643-644 | 0.005 / 0.003 | `order_placer.py:2230-2231` inside `if fill_entry.order_protocol == "CO_PLUS_TGT"` (:2204-2208) | Every order is LIMIT_TRIPLE (`:961`). |
| 17 | `smart_tgt.volume_dependent_trails` / `max_modify_failures` :645-646 | false / 3 | passed to SmartTgtManager (`main.py:2986-2987`) | Its only registration site is the CO branch (`order_placer.py:2222`), so no new trade is ever tracked. [INF] Any pre-existing `smart_tgt_state` rows would be rehydrated at start (`smart_tgt_manager.py:163-200`); DB not inspected. |
| 18 | `portfolio_allocator.*` :565-570 (`allocator_mode`, `enforce_scope`, `candle_interval_seconds`, `drain_tail_seconds`, `max_portfolio_deployment_pct` null, `long_short_skew_max` null) | "shadow", "v3_only", ... | `signal_processor.py:1150` (enforce only), `:1161-1168` observe; `allocation/portfolio_allocator.py:88-96` | Shadow never reserves or places; admission stays FCFS. |
| 19 | `v3_chain.*` :574-617 (`v3_chain_mode` + all gates and weights, incl. `rr_floor` 2.0, `min_pass_score` 60) | "shadow" | `signal_processor.py:1136-1143` | Fire-and-forget observe; errors are swallowed; it never rejects. |
| 20 | `shadow_tracker.enabled` :504 | false | `signal_processor.py:928` -> `:1992` `tracker.is_tracking(symbol)` -> `shadow_tracker.py:213-214` `if not self._enabled:` / `return False` | The SHADOW_INNING_ACTIVE reject can never fire. |
| 21 | `sr_detector.wait_for_retest_enabled` :529 (+ retest knobs :530-540) | false | `main.py:3423` `_v2_on = getattr(_sr_cfg, "wait_for_retest_enabled", False)`; the diverter is built only under it (`:3769`) | `signal_processor.py:1042` `if self._retest_diverter is not None ...` is never true. |
| 22 | `sr_detector.enabled` :509 | true | `signal_processor.py:1550-1561` `_sr_observe` after placement | Non-gating observer (`:614-658`). |
| 23 | `signal_queue.expiry_sec` :127 | 600 | `webhook_receiver.py:925-926`; `signal_processor.py:917-921` | [DERIVED] Any signal older than 60 s is rejected by the screener anyway: `step_executor.py:419-423` returns 0.0 above 60 s, then `secondary_screener.py:340-354` gives REJECTED_SIGNAL_AGE (or REJECTED_SCORE first). A value >= 60 changes only the reject label and stage, never admission. |
| 24 | `trading_hours.eod_entry_cutoff` :48 | "15:15" | `order_placer.py:1076-1097` | [INF] Entries close at 15:00 (:47), so this binds only if more than 15 min passes between the window check and placement. |
| 25 | `position_sizing.max_single_order_qty` :230 | 10000 | `position_sizer.py:461`, `:656` | [DOC] The code comment (`:652-655`) calls it latent at current capital and reachable at about Rs 25,000. It depends on runtime capital; I did not re-verify. |
| 26 | `position_sizing.lot_skew_rejection_threshold` :228 | 0.25 | `position_sizer.py:688` `if lot_size != 1 and ...` | [INF] Skipped when lot_size == 1. NSE-EQ instruments are assumed to carry lot_size 1 (instruments.csv is gitignored and not in the extract). |

### 6b. Loaded from YAML but never passed to the entry-path consumer (the consumer uses its own default)

| key @ file:line | YAML value | consumer and default actually used |
|---|---|---|
| `entry_gate.liquidity_check_enabled` :658, `max_spread_pct` :656, `min_depth_qty` :657 | true / 0.5 / 500 | Not passed at `main.py:3061-3087`, so `order_placer.py:589` `liquidity_check_enabled: bool = False` applies, and `:4075-4076` `if not self._liquidity_check_enabled: return True, ""`. The call at `:1293-1294` is a no-op. |
| `risk.price_drift_threshold` :325 | 0.005 | Not passed, so `order_placer.py:585` default 0.005 applies (coincident; a YAML edit would not propagate). |
| `position_sizing.dynamic_by_winrate` / `min_multiplier` / `max_multiplier` :241-243 | true / 0.5 / 2.0 | `perf_weights` is never passed to SignalProcessor (`main.py:3575-3623`), so the dict is empty (`signal_processor.py:236`) and `.get(name, 1.0)` is always 1.0. `PerformanceAllocator` is never constructed (only a docstring, `capital/performance_allocator.py:41`). |
| (not in YAML) OrderPlacer `default_order_protocol` / `rr_ratio` | — | Ctor defaults `"LIMIT_TRIPLE"` (:572) and `2.0` (:571). 2.0 is used only when a trade has no stored `tgt_risk_reward` (`:4166-4178`). |

### 6c. Declared with zero readers
- `signal_processor.pipeline_timeout_sec` system_config.yaml:347 = 30. The only reference is the config_loader field and validator (`core/config_loader.py:568`, `:602-606`).
- `smart_tgt.enabled` system_config.yaml:642 = true. No reader: SmartTgtManager is built with the literal `enabled=True` (`main.py:2979`). The YAML comment "if false, OrderPlacer skips SmartTgt wiring" has no matching code.

---

## 7. Conflicts between readers, or between documentation and code (both reported) [SRC]

1. **`entry_offset_pct`.** `position_sizer.py:295-297` says "order_placer places at entry_price * (1 + entry_offset_pct)", and `:489-491` repeats it. In the code, the offset is applied once in `signal_processor._derive_prices` (`:1780-1784`, below the trigger for LONG). The placer places at the price it receives (`order_placer.py:1345-1356`). The sizer receives no offset (`signal_processor.py:1112-1121`), so `effective_entry_price = entry_price` (`:492`).
2. **`order_protocol`.** Documentation says the protocol is per-strategy or per-intent: YAML comments ("S6: DELIVERY intent, LIMIT_TRIPLE protocol"), `order_placer.py:31-33` (OP9), and `full_entry_engine.py:15-16` (FEE3, "allows per-strategy override"). The code uses the constructor default only (`order_placer.py:961`), so all 16 strategies go LIMIT_TRIPLE.
3. **Pullback wait.** `signal_processor.py:1074-1075` says "Pullback strategies skip this (EntryGate already waits for current price)". Nothing feeds the EntryGate: there is no `add()` caller, and the comment at `:2236-2238` says so. `pullback_wait_enabled: true` strategies simply use the stale trigger.
4. **Gap buffer.** The gap_* YAML comments say "widen SL 0.3% during 09:15-09:30 gap-risk window". The global entry floor is 10:00, so the buffer never applies. It is also a percent while the sibling `sl_*` keys are fractions.
5. **`max_spread_pct` unit.** The strategy value is 0.005. The step compares a percent (`step_executor.py:393`), its own default is 0.1 (`:394`), and the global `entry_gate.max_spread_pct` is 0.5, labelled "%" (system_config.yaml:656). [INF] 0.005 reads as a fraction meant to be 0.5 %.
6. **Stale window examples.** `market_windows.py:161-164` and `signal_processor.py:976` cite "gap_fade_long cuts off at 11:30" and "defaults are 09:30 / 13:30". In fact every file uses 15:00, the schema defaults are 10:00 / 15:00 (`schema.py:137-138`), and the market_windows constructor defaults are 09:30 / 13:30 (`:23-24`) but are overridden by config (`main.py:2320-2329`).
7. **`smart_tgt.enabled`.** The YAML comment (:642) describes a switch; the code has no reader (6c).
8. **Scan-map validation.** `scan_webhook_map.yaml:2-6` says names are "Validated at startup (P17, S10)". `load_all_strategies` runs S10 only when given a map path, and `main.py:3159-3162` gives none. (I did not check the preflight scripts in `scripts/preflight/checks/`.)

---

## Appendix A. The live entry path in call order (@970aabf)

1. `webhook_receiver._process_request`: auth (:547); unknown scanner 404 (:553-554); **eod route (:563-564)**; kill-switch 403 (:566-568); backpressure 503 (:575-578); global window 403 (:582-583); ...; age > `expiry_sec` -> EXPIRED (:925-926); INSERT + `put_nowait` (:1047-1049).
2. `SignalProcessor._process_one` (:867): kill (:906); global window (:911); expiry (:917); shadow-inning (:928); map -> strategy (:933-953); **control gate (:959-972)**; **per-strategy window (:977-982)**; governor (:985-990); **screener (:998-1004)**; **`_derive_prices` (:1028-1030)**; side (:1034-1035); retest divert (:1042, dormant); **re-anchor (:1082-1106)**; **sizer (:1112-1121)**; v3 observe (:1136-1143); allocator (:1147-1172); `_admit_and_place` (:1182-1187).
3. `_admit_and_place` (:1277): in-flight (:1302-1305); inside `portfolio_lock`: **per-strategy cap (:1311)**, one-trade rule (:1312-1313), **risk.approve (:1315-1325)**, **fm.reserve (:1328-1340)**; then **`_derive_target` (:1368)**; alert (:1371-1380); late kill (:1389); throttle (:1410-1418); **`placer.place` (:1446-1460)**.
4. `OrderPlacer.place` (:871): R:R gate (:938-958); protocol = default (:961); `required_margin(intent)` (:971-973); slippage fraction (:984-991); create_trade (:996-1015); kill (:1050); EOD cutoff (:1076-1097); slippage guard (:1103-1192); drift top-up (:1197-1289); liquidity (:1293-1305, inert); `engine.execute(intent)` (:1345-1356) -> `LimitTripleProtocol.execute` -> `adapter.place_order(intent)` -> product (zerodha_adapter.py:578-600).
5. Fill: `_handle_entry_fill` (:2089) -> LIMIT_TRIPLE exits (:2156-2163) with the TGT recomputed from the fill using `tgt_risk_reward` (:2872-2879) -> `FullEntryEngine.place_deferred_exits`: DELIVERY gets an OCO GTT (full_entry_engine.py:151-177), otherwise SL + TGT legs.
