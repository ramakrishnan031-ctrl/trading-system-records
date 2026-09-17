# ENTRY EXECUTION PATH — FACT-FINDING REPORT

**Card:** `FOR_VSCODE_CLAUDE_15-Sep-2026_ENTRY_EXECUTION_FACT_FINDING.txt` (byte-identical to `docs/design/secondary_filteration/entry-execution/ACTIVE_CARD_FACT_FINDING_15-Sep-2026.txt`)
**Date of work:** 15-Sep-2026 (Tuesday) IST
**Nature:** REPORT ONLY. No code change, no config change, no commit, no push, no deploy.
**Production trading VM:** NOT touched. No ssh to `trading-vm` / 161.118.187.249. No git command that contacts `origin` (which is production's bare repo).
**Per the card (§10):** no fixes proposed, no findings ranked, nothing implemented.

---

## 0. WHAT WAS READ, AND HOW

### 0.1 Sources and the labels used in this report

| Label | Source | State measured |
|---|---|---|
| **WT** | Working tree `D:/Projects/trading-system` | Branch `feat/delivery-config-split` @ `6d24a83`. Uncommitted edits on the entry path: `capital/fund_manager.py`, `capital/kill_switch.py`, `config/system_config.yaml`, `orders/order_placer.py`, `signals/signal_processor.py`. The testing VM's bare-repo HEAD `20061b6` is **not** an ancestor of this HEAD. |
| **TW** | Deployed tree on the **testing VM** 130.210.13.114 (ssh alias `trading-sbx`, hostname `trading-system-sandbox`) | Read-only snapshot pulled 15-Sep 10:51 IST. 1,776 code/config files; no `.env`, data or logs. md5 manifest verified against the VM: all match, and a corrupted-line negative control failed as expected. |
| **TW-LIVE** | Files read directly on the testing VM | e.g. live `config/system_config.yaml` md5 `351bd82e73bb0301d850341191c7b72b`, re-checked after the run |
| **TW-DB** | `data_store/trading_system.db` (+ `analytics.db`) on the testing VM | SQLite `mode=ro` only |
| **TW-LOG** | `logs/system_<date>.log` on the testing VM | Only 2026-09-03 … 2026-09-15 exist |
| **HEAD** | git HEAD blob of the WT | — |
| **ORIGIN** | Local ref `origin/main` = `970aabf` (last fetched 11-Sep) | A local ref. **Not a production measurement.** |

### 0.2 Facts that frame every answer

1. **The testing VM runs LIVE mode.** Service `ExecStart … main.py --mode live`, account **VBB097**, `ExecMainStartTimestamp` 2026-09-15 08:15:23 IST. No paper-mode process was observed, so every PAPER statement below is read from code. No paper-mode data exists on the VM (Group H).
2. **The VM's DB spans two accounts.** The boundary is `config_snapshots` 50 → 51:
   - snapshot 50 = **LFL836**, 2026-09-08T08:15:32+05:30;
   - snapshot 51 = **VBB097**, 2026-09-09T11:15:14+05:30.
   All 954 trades are `mode='LIVE'` (2026-06-15 … 2026-09-15). Whether the pre-boundary rows were written on the production VM or on this VM is **NOT ESTABLISHED** from data.
3. **The running process loaded exactly the deployed config.**
   - `session.last_config_hash` written at STARTUP 2026-09-15T08:15:34 equals the sha256 of all 8 live loader files.
   - The live file's mtime (2026-09-10 13:33) precedes the boot.
   - The loader (`core/config_loader.py load_all`) reads only `config_dir/<8 files>` with `yaml.safe_load`, with no overlay or env override.
4. **Line numbers hold only at the measured state of each tree.** Where a file is md5-identical in WT and TW, one line reference serves both.
5. **The card's terms, mapped to code:**
   - "the 1% check" = `entry_gate.max_entry_slippage_pct: 1.0` (FIX-128).
   - "the 10-minute timeout" = `signal_queue.expiry_sec: 600`, a **signal-age** limit, not an order timeout. The entry-order cancel clock is `order_monitor.fill_timeout_sec: 60`.

### 0.3 Method and verification status

- **Finders.** 8 read-only fact-finding agents ran **one at a time**: Group B first (the chain), then A, C, D, E, F, G, H. Each read both trees and the VM DB/logs read-only.
- **Stages that did NOT run.** The adversarial-verifier, completeness-critic and report-fidelity stages were stopped on instruction after the 8 finders completed.
- **Independent re-check.** In place of the verifier, the load-bearing claims were re-checked by direct read; the list is in §9. Answers not covered by §9 rest on one agent's measured reading with the evidence cited.
- **Cross-group disagreements.** Two log counts disagreed between groups. Both were re-measured and the measured value is used (§9).

### 0.4 Markers used

- **Status:** `ESTABLISHED` · `PARTIAL` (the unanswered sub-part is written as **NOT ESTABLISHED**) · `NOT ESTABLISHED`
- **WT ↔ deployed VM:**
  - `MATCH`
  - `DIFFERS — file only (cited logic identical)`
  - **`DIFFERS — LOGIC/VALUES`**
- **Paper ↔ live:** `IDENTICAL` · `DIFFER` (both paths given)
- **Provenance:** every answer is **MEASURED** from code, config, DB or logs unless a sentence is explicitly marked *INFERENCE*.

---

## 1. GROUP A — DEPLOYED CONFIG VERSUS WORKING TREE

### A1 — Diff the DEPLOYED config on the testing VM against the working tree for every entry-execution key. List every difference.
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS — LOGIC/VALUES** (33 of 326 flattened keys) · **Uncommitted in WT:** YES (the `system_config.yaml` edit is a 20-line comment block, WT 178-197) · **Paper↔live:** DIFFER (see below)

**Definition used:** an "entry-execution key" is any config key read by code on the Group B chain.

**Method:** all four versions (WT, HEAD, ORIGIN, TW) were yaml-parsed and flattened, then compared.
- HEAD values = WT values, because the uncommitted WT edit is comment-only.
- ORIGIN values = TW values, except the `alerts.smtp.*` addresses and comment wording.

**Differences on the entry chain** (WT value @ line / TW value @ line):

| Key | WT | TW (deployed) | Consumer |
|---|---|---|---|
| `position_sizing.max_concentration_pct` | 0.2 @216 | 0.1 @226 | TW `capital/position_sizer.py:499` `(total_capital * eff_conc_pct) / entry_price`; WT `position_sizer.py:659` `(basis * eff_max_concentration_pct) / entry_price` (value AND base differ) |
| `position_sizing.max_position_value_pct` | 0.25 @228 | 0.4 @236 | TW `position_sizer.py:722` `max_position_value = eff_max_position_value_pct * total_capital` |
| `position_sizing.delivery_risk_per_trade_pct` | 0.02 @257 | 0.01 @253 | sizing |
| `position_sizing.delivery_max_position_value_pct` | 0.25 @258 | 0.4 @259 | sizing |
| `position_sizing.delivery_max_concentration_pct` | 0.2 @259 | 0.1 @254 | TW `main.py:2860-2862`; WT `capital/pipeline_policy.py:345-350` |
| `position_sizing.delivery_max_single_order_qty` | 2000 @260 | ABSENT | WT only |
| `position_sizing.delivery_enabled` | true @265 | ABSENT | WT only |
| `position_sizing.delivery_tier_multipliers` | HIGH 1.0 / MEDIUM 0.85 / LOW 0.70 @271-274 | ABSENT | WT `pipeline_policy.py:329-357` |
| `risk.max_open_positions` / `risk.max_daily_trades` | ABSENT | 5 @271 / 10 @272 | TW `main.py:2899-2900` → `risk_engine.py:194-195` |
| `risk.intraday_max_open_positions` / `risk.intraday_max_daily_trades` | 6 @302 / 6 @303 | ABSENT | WT `main.py:2660-2661` → `risk_engine.py:179-180` |
| `risk.max_open_delivery_positions` | 6 @304 | 3 @283 | risk |
| `risk.max_daily_delivery_trades` | 6 @305 | 5 @284 | TW `main.py:2918-2919` |
| `risk.max_consecutive_losses` | 5 @331 | 4 @315 | TW `main.py:2903` |
| `risk.delivery_max_consecutive_losses` | 5 @347 | ABSENT | WT `pipeline_policy.py:364-367` |
| `risk.delivery_max_sector_exposure_pct` | ABSENT | 0.4 @314 | TW `main.py:2923` |
| `signal_queue.delivery_expiry_sec` | `null` @93 | ABSENT | WT `pipeline_policy.py:379-380` (null = no expiry for delivery) |
| `trading_hours.delivery_entry_start` / `delivery_entry_end` | "10:00" @68 / "14:45" @69 | ABSENT | WT `pipeline_policy.py:370-375` |
| `scoring_weights.yaml`: `delivery_min_pass_score` / `delivery_medium_score_threshold` / `delivery_high_score_threshold` | 60 @65 / 60 @66 / 63 @67 | ABSENT | WT `pipeline_policy.py:382-384` |

**Differences NOT on the entry chain:**
- **MIS auto-squareoff (TW only):** `trading_hours.mis_squareoff_cutoff "15:09"`@59 · `mis_squareoff_first_offset "6m"`@90 · `mis_squareoff_second_offset "3m"`@91 · `mis_squareoff_margin_sec 20`@96.
- **Exit path (TW only):** `eod_squareoff.mis_pass_1_market_protection_percent 1.5`@372 · `mis_pass_2_market_protection_percent 2.5`@373. Consumed via TW `main.py:3372-3375` → `orders/mis_autosquareoff.py:281-299`.
- **Load-time validator only (TW only):** `capital.leverage_safety.min_allowed 1.0`@213 · `max_allowed 10.0`@214.
- **Alerting:** the `alerts.smtp.*` addresses differ across WT, ORIGIN and TW.

**Entry-execution keys IDENTICAL in WT, HEAD, ORIGIN and TW** (value, WT line / TW line):
- **`entry_gate`:** `slippage_buffer 2.0` (668/645) · `max_entry_slippage_pct 1.0` (674/651) · `max_spread_pct 0.5` (675/652) · `min_depth_qty 500` (676/653) · `liquidity_check_enabled true` (677/654) · `min_effective_rr 1.0` (678/655) · `min_pending_rr 1.0` (679/656) · `circuit_proximity_reject_enabled true` (680/657).
- **`slippage_control`:**
  - `enabled true` (688/665) · `mode sl_fraction` (689/666) · `max_slippage_fraction 0.22` (690/667)
  - `absolute_cap_rs 5.00` (691/668) · `hard_max_slippage_rs 10.0` (692/669) · `also_apply_pct_check true` (693/670)
  - `default_max_slippage_rs 2.00` (695/672) · tiers `100:1.00 / 200:1.25 / 500:2.00 / 999999:3.00` (696-700/673-677)
  - `overrides.enabled true` (710/687) · `by_price_band {}` (716/693) · `by_strategy {}` (720/697) · `by_symbol {}` (725/702)
- **`signal_queue`:** `expiry_sec 600` (84/127) · `capacity 300` · `backpressure_pct 0.8`.
- **`trading_hours`:** `entry_start 10:00` (28/28) · `entry_end 15:00` (47/47) · `eod_entry_cutoff 15:15` (48/48).
- **`order_monitor`:** `poll_interval_sec 2` (158/193) · `fill_timeout_sec 60` (159/194).
- **`circuit_breaker`:** `partial_fill_timeout_minutes 5` (758/735) · `force_close_time 15:15`.
- **`paper`:** `auto_fill_delay_sec 0.5` (740/717) · `ltp_gating_enabled true` · `ltp_gating_max_wait_sec 21600` · `ltp_gating_poll_sec 5.0`.
- **`capital`:** `sl_limit_offset_pct 0.005` (169/204) · `emergency_exit_buffer_pct 0.01` · `leverage_map INTRADAY 5.0 / DELIVERY 1.0` · `intraday_bucket_pct 0.7` · `positional_bucket_pct 0.3`.
- **`position_sizing`:** `min_tick_size 0.05` (219/229) · `risk_per_trade_pct 0.01` · `max_single_order_qty 10000`.
- **Other flags:** `product_map` INTRADAY MIS / DELIVERY CNC · `force_intraday_only false` · `delivery_enabled true` · `trade_type BOTH` · `signal_processor.worker_count 5` · `portfolio_allocator.allocator_mode "shadow"` (584/561) · `sr_detector.wait_for_retest_enabled false` (548/525).
- **Whole files, md5-identical in all four versions and on the VM:** `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml`, `nse_holidays_2026.yaml`, `symbol_aliases.yaml`, and all 16 `config/strategies/*.yaml`.

**Config values present but not wired** (identical in both trees):
- `entry_gate.liquidity_check_enabled`, `max_spread_pct` and `min_depth_qty` are never passed to `OrderPlacer` (TW `main.py:3061-3087` / WT `2820-2846`). The ctor default `liquidity_check_enabled: bool = False` (`order_placer.py:589`) applies.
- No `price_drift_threshold` is passed; the ctor default is `0.005` (@585).
- No `default_order_protocol` is passed; the ctor default is `"LIMIT_TRIPLE"` (@572).

**Evidence:**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW-LIVE | `config/system_config.yaml` | — | md5sum + stat | `351bd82e73bb0301d850341191c7b72b` · mtime 2026-09-10 13:33:12 |
| TW-LIVE | systemd + /proc | — | systemctl show | `ExecMainStartTimestamp=Tue 2026-09-15 08:15:23 IST` · cmdline `…/main.py --mode live` (no `--config`) |
| TW-DB | `session`, `system_events` | session id 1; event 3853 | ro | `last_config_hash[system_config.yaml]` sha256 = live file sha256; 8/8 loader files match |
| TW-LOG | `logs/system_2026-09-15.log` | 08:15:24.025 | main | `"Config loaded from config (8 files)"` |
| TW | `core/config_loader.py` | 2457-2516 | `load_all` | `path = config_dir / filename … data = yaml.safe_load(raw_bytes) … schema_cls.model_validate(data)` |
| TW | `main.py` | 2099, 2198 | `main` | `config_dir = Path(args.config) if args.config else Path("config")` … `app_config = load_all(config_dir)` |
| HEAD | `config/system_config.yaml` | WT 178-197 | git diff --stat | `20 ++++++++++++++++++++` (comment block "THE TWO MONEY BASES") |

**Paper↔live:** the config values are the same in both modes (one config file). What differs is when they are read:
- `paper.*` keys are used only when `paper_mode` is set.
- `slippage_control` and `max_entry_slippage_pct` are evaluated only after `_fetch_ltp` returns an LTP. In paper, `get_quote_raw` returns `{}` (TW `zerodha_adapter.py:1816-1817` / WT `1748-1749`), so these keys are never evaluated.

---

### A2 — Deployed value of the entry-slippage mode. Is it sl_fraction or flat_tiers?
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (config file; not these lines) · **Paper↔live:** DIFFER

**Answer:** `sl_fraction`. The running process loaded it (boot sha256 match, A1).

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 664-666 | — | `slippage_control:` / `enabled: true` / `mode: sl_fraction              # sl_fraction \| flat_tiers \| pct` |
| WT | `config/system_config.yaml` | 687-689 | — | same |
| TW | `main.py` | 3076 | `main` (OrderPlacer ctor) | `slippage_control=app_config.system.entry_gate.slippage_control,` (WT 2835) |
| TW=WT | `orders/order_placer.py` | 345-347 | `_compute_slippage_tolerance` | `mode = getattr(cfg, "mode", "sl_fraction") … if mode == "sl_fraction":` |
| TW | `core/config_loader.py` | 1768-1769, 1777-1784 | `SlippageControlConfig` | `enabled: bool = False` / `mode: str = "sl_fraction"` … `if v not in ("sl_fraction", "flat_tiers", "pct"): raise ValueError` |
| TW-LOG | `logs/system_2026-09-10/11/15.log` | 44 lines | `order_placer.entry_slippage_observed` | `"mode":"sl_fraction"` on 44/44 |

**Paper↔live:** the value is the same in both. The guard that reads it runs only when an LTP is fetched, which never happens in paper (see A1).

---

### A3 — Deployed value of the sl_fraction percentage.
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (not these lines) · **Paper↔live:** DIFFER

**Answer:** `0.22`. The unit is a **fraction of the SL distance** (22%), not a percent of price.

The fraction is resolved per trade (`order_placer.py:983-991`). All override maps are empty (A8), so it resolves to the global 0.22. Evidence it is in use:
- **TW-LOG:** every `entry_slippage_observed` line on 09-10, 09-11 and 09-15 has `tolerance_fraction 0.22`. For today's 5 lines, `tolerance_rs == round(min(sl_distance_rs*0.22, 5.0, 10.0), 2)` with 0 mismatches.
- **TW-DB:** every trade from 2026-09-01 to 09-15 has `trades.tolerance_fraction_used = 0.22` and `tolerance_source 'global'`. All-time: `global` 891, NULL 63, other 0.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 667 | — | `max_slippage_fraction: 0.22    # sl_fraction: slippage <= 22% of the SL distance` |
| WT | `config/system_config.yaml` | 690 | — | same |
| TW=WT | `orders/order_placer.py` | 347-354 | `_compute_slippage_tolerance` | `frac = (fraction_override if fraction_override is not None else cfg.max_slippage_fraction)` … `sl_dist = abs(signal_price - sl_price)` / `tol = min(sl_dist * frac, cfg.absolute_cap_rs)` |
| TW=WT | `orders/order_placer.py` | 264 | `resolve_slippage_fraction` | `glob = getattr(cfg, "max_slippage_fraction", 0.22)` |

**Paper↔live:** the value is the same. It is recorded on the trade in both modes, but enforced only when an LTP is fetched, which never happens in paper.

---

### A4 — Deployed value of the rupee cap and the hard ceiling.
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (not these lines) · **Paper↔live:** DIFFER

**Answer:**
- Rupee cap: `absolute_cap_rs = 5.00`.
- Hard ceiling: `hard_max_slippage_rs = 10.0`.

Under `sl_fraction` the tolerance is `tol = min(sl_dist * frac, 5.00)`, so the 10.0 ceiling cannot bind (arithmetic from the formula as written).

A third rupee figure, `default_max_slippage_rs 2.00`, is read only in the inactive `flat_tiers` branch.

TW-LOG 09-10/11/15: no line had `sl_distance_rs*0.22 > 5.0`, so the 5.00 cap was not observed binding on those days.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 668-669, 672 | — | `absolute_cap_rs: 5.00          # sl_fraction: hard backstop (smaller of the two wins)` / `hard_max_slippage_rs: 10.0     # absolute ceiling, ALWAYS applied (any mode)` / `default_max_slippage_rs: 2.00` |
| WT | `config/system_config.yaml` | 691-692, 695 | — | same |
| TW=WT | `orders/order_placer.py` | 352-361 | `_compute_slippage_tolerance` | `tol = min(sl_dist * frac, cfg.absolute_cap_rs)` … `tol = cfg.absolute_cap_rs        # SL unavailable -> backstop only` … `return min(tol, cfg.hard_max_slippage_rs), sl_dist` |

**Paper↔live:** the values are the same. They are applied only in the live LTP-fetched guard.

---

### A5 — Deployed value of max_entry_slippage_pct and also_apply_pct_check.
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (not these lines) · **Paper↔live:** DIFFER

**Answer:**
- `max_entry_slippage_pct = 1.0`. The unit is a PERCENT: 1.0 = 1%.
- `also_apply_pct_check = true`.

With `mode sl_fraction` and the flag `true`, the 1% check is ACTIVE as a second abort condition, after the rupee-tolerance test. The legacy flat-% branch runs only when `slippage_control` is absent or disabled, which is true in neither tree.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 651, 670 | — | `max_entry_slippage_pct: 1.0 # FIX-128: abort if current LTP deviates > 1% from signal trigger price` / `also_apply_pct_check: true     # also keep the flat max_entry_slippage_pct (belt + suspenders)` |
| WT | `config/system_config.yaml` | 674, 693 | — | same |
| TW | `main.py` | 3075 | `main` | `max_entry_slippage_pct=app_config.system.entry_gate.max_entry_slippage_pct,  # FIX-128` (WT 2834) |
| TW=WT | `orders/order_placer.py` | 387-389 | `_slippage_decision` | `if (getattr(cfg, "also_apply_pct_check", True) and getattr(cfg, "mode", "") != "pct" and slip_pct > max_pct): return f"slippage {slip_pct:.2f}% > flat limit {max_pct:.1f}%", tol, sl_dist` |

**Paper↔live:** the values are the same. The %-check executes only inside the live LTP-fetched guard.

---

### A6 — Deployed value of slippage_buffer.
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (not these lines) · **Paper↔live:** IDENTICAL

**Answer:** `slippage_buffer = 2.0` rupees.

Its ONLY order-path read is the FIX-025 block in `OrderPlacer.place` (905-914). That block runs only `if release_ltp is not None`.

`release_ltp` is supplied only by the EntryGate release path, and that path is not reached:
- **Code:** `EntryGate.add` has no caller in either tree. The only textual hit is the docstring at `screening/entry_gate.py:103`.
- **Logs:** the block logs `order_placer.slippage_protection` at INFO, and that line appears 0 times in every TW log 2026-09-03..09-15. INFO logging is live in those files (`entry_slippage_observed` INFO lines are present).

So the deployed value is 2.0, but it sits on a path with no observed execution.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 644-645 | — | `entry_gate:                   # FIX-025: gate release slippage protection` / `slippage_buffer: 2.0        # Rs buffer for limit price adjustment at gate release` |
| WT | `config/system_config.yaml` | 667-668 | — | same |
| TW | `main.py` | 3074 | `main` | `entry_gate_slippage_buffer=app_config.system.entry_gate.slippage_buffer,  # FIX-025` (WT 2833) |
| TW=WT | `orders/order_placer.py` | 905-914 | `OrderPlacer.place` | `if release_ltp is not None: if side == "BUY": adjusted_limit = min(entry_price + self._entry_gate_slippage_buffer, release_ltp) else: adjusted_limit = max(entry_price - self._entry_gate_slippage_buffer, release_ltp)` / `entry_price = adjusted_limit` |
| TW=WT | `screening/entry_gate.py` | 103, 468 | docstring / `_check_one` | `gate.add(WatchEntry(...))` (docstring only) · `self._release(entry, "PRICE_HIT", release_ltp=ltp)` |
| TW-LOG | `logs/system_2026-09-03..15.log` | grep -c | — | `order_placer.slippage_protection` = 0 in every file |

**Search width:** `release_ltp=` and `(entry_gate|_gate|gate).add(` over all non-test `*.py` in both trees; readers of `slippage_buffer` in both trees. The zero log count covers 09-03..09-15 only.

**Paper↔live:** the FIX-025 block has no mode condition.

---

### A7 — Deployed state of the flat price-tier table — active or inactive?
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (not these lines) · **Paper↔live:** IDENTICAL

**Answer:** INACTIVE. The table is configured, loaded and schema-validated at boot, but never consulted.
- It is loaded into `self._slippage_tier_tuples` (`order_placer.py:674-677`).
- The only code that uses it is the `elif mode == "flat_tiers":` branch (355-356). That branch is unreachable while `mode == "sl_fraction"`, which is the deployed mode (A2).
- `tier_slippage_tolerance_rs` has only this call site plus its own definition (`orders/price_math.py:60`).
- Runtime: `mode sl_fraction` on 44/44 TW-LOG `entry_slippage_observed` lines.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 671-677 | — | `# --- flat_tiers mode (today's build, kept for A/B) ---` / `default_max_slippage_rs: 2.00` / `tiers:` `{ max_price: 100, max_slippage_rs: 1.00 }` `{ max_price: 200, max_slippage_rs: 1.25 }` `{ max_price: 500, max_slippage_rs: 2.00 }` `{ max_price: 999999, max_slippage_rs: 3.00 }` |
| WT | `config/system_config.yaml` | 694-700 | — | same |
| TW=WT | `orders/order_placer.py` | 355-356 | `_compute_slippage_tolerance` | `elif mode == "flat_tiers": tol = tier_slippage_tolerance_rs(signal_price, tier_tuples, cfg.default_max_slippage_rs)` |

---

### A8 — Deployed state of the three override lists. Empty or populated?
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** YES (not these lines) · **Paper↔live:** DIFFER

**Answer:** all three maps are EMPTY, with the hierarchy switch ON.
- The example entries under each map are YAML comments, not data.
- `yaml.safe_load` of the deployed file yields `{}` for all three.
- `resolve_slippage_fraction` falls through to `return glob, "global"`.

Runtime confirms it:
- `tolerance_source "global"` on 44/44 TW-LOG lines.
- Every trade 09-01..09-15 has `tolerance_source 'global'`.
- All-time: 891 `global`, 63 NULL, 0 `symbol:`/`strategy:`/`band:`.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 686-704 | — | `overrides:` / `enabled: true` … `by_price_band: {}` … `by_strategy: {}` … `by_symbol: {}` |
| WT | `config/system_config.yaml` | 709-727 | — | same (716/720/725) |
| TW=WT | `orders/order_placer.py` | 264-276 | `resolve_slippage_fraction` | `ov = getattr(cfg, "overrides", None)` / `if ov is not None and getattr(ov, "enabled", False): by_symbol = … or {} …` / `return glob, "global"` |
| TW | `core/config_loader.py` | 1731-1734 | `SlippageOverridesConfig` | `enabled: bool = True` / three `Field(default_factory=dict)` |

**Paper↔live:** the fraction is resolved and recorded in both modes. Enforcement is live-only (LTP-fetched guard).

---

### A9 — Git status of every file involved: committed, uncommitted, diverged from the VM?
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS** (18 files) · **Uncommitted in WT:** MIXED · **Paper↔live:** N/A

**Scope:** 63 paths — the Group B file list, `strategies/loader.py`, the 8 loader config files and `symbol_aliases.yaml`.

**Checks per path:** `git status --porcelain`, the HEAD blob and the ORIGIN blob md5, the WT md5, the TW md5, and the live VM md5.
- Every VM md5 equals the TW md5.
- Every VM mtime precedes the 2026-09-15 08:15:23 boot.

**A) Clean in WT and identical in WT, HEAD, ORIGIN, TW and VM (no divergence):**
- `signals/entry_throttle.py`
- `screening/`: `step_executor.py`, `hard_gate.py`, `entry_gate.py`, `retest_monitor.py`
- `orders/`: `full_entry_engine.py`, `entry_engine.py`, `order_protocol_limit.py`, `order_protocol_co.py`, `price_math.py`, `cnc_gtt.py`
- `broker/`: `product_resolver.py`, `order_monitor.py`, `rate_limiter.py`
- `capital/strategy_governor.py`
- `strategies/`: `schema.py`, `control.py`, `loader.py`
- `core/`: `time_authority.py`, `ids.py`
- `config/`: `broker_costs.yaml`, `broker_limits.yaml`, `slippage_model.yaml`, `scan_webhook_map.yaml`, `chartink_scanners.yaml`, `nse_holidays_2026.yaml`, `symbol_aliases.yaml`, and all 16 `config/strategies/*.yaml`
- `orders/slippage_recorder.py`: the WT raw md5 differs only because of CRLF line endings. Content matches after CRLF normalisation.

**B) Uncommitted in WT, and the VM already has the WT content:**
- `orders/order_placer.py`: WT = TW = ORIGIN = `c337d5c3bb5a5414645234eeab30b7aa`; HEAD = `64c156a556d1168eb2133c7ec6df8b15`. The uncommitted hunks are at 235 and 4002-4022 (alert code only).

**C) Clean in WT (WT = HEAD) but diverged from the VM (TW = ORIGIN ≠ HEAD):**
- `main.py`
- `signals/webhook_receiver.py`
- `screening/`: `secondary_screener.py`, `quality_scorer.py`
- `orders/order_manager.py`
- `broker/zerodha_adapter.py`
- `capital/`: `position_sizer.py`, `risk_engine.py`
- `core/`: `market_windows.py`, `config_loader.py`, `state_store.py`
- `config/scoring_weights.yaml`
- `core/schema.sql`: WT = HEAD `01a040f7…`; ORIGIN and the VM live file = `abe7cb19…`. It is not in the snapshot.

**D) Uncommitted in WT and diverged from the VM:**
- `signals/signal_processor.py`: WT `858e2ce3…` / HEAD `152b9bf8…` / ORIGIN = TW `da8c6f98…`
- `capital/fund_manager.py`: WT `da4b3fdd…` / HEAD `4f5db366…` / ORIGIN = TW `9ff45f66…`
- `capital/kill_switch.py`: WT `3fa519a1…` / HEAD `fc2cd4ef…` / ORIGIN = TW `90848bfc…`
- `config/system_config.yaml`: WT `e2add048…` / HEAD `7380780a…` / ORIGIN `f5449553…` / TW `351bd82e…`. All four differ. TW differs from ORIGIN only in the `alerts.smtp` addresses and comment wording.

**E) WT-only file:** `capital/pipeline_policy.py` is clean, WT = HEAD `19a01074…`, and absent from ORIGIN, TW and the VM.

**Notes:**
- ORIGIN `970aabf` (committed 2026-09-11 02:05 +0530) is NOT an ancestor of HEAD.
- In every differing code file, TW equals ORIGIN.
- `config/system_config.yaml` is the one file where TW matches neither ORIGIN nor HEAD.
- For code files, the claim that the process imported these exact bytes rests on mtime-before-boot only. For config, it is also backed by the boot sha256 match.

---

## 2. GROUP B — THE ENTRY PRICE CHAIN

### B1 — The complete chain from Chartink alert to broker submission, every function named in call order.
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS — LOGIC** (same call order, with the exceptions below) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**How the trees differ on this chain**
- The call order is the same in both trees.
- WT only: a per-pipeline window/expiry step inside `_process_one` (WT 999-1024). This is not deployed.
- TW only: account-prefix strip in the webhook (TW 111-137); Batch-1 evidence capture in `signal_processor`; `market_protection` parameter in the adapter.

**Active path (direct webhook → LIMIT_TRIPLE)**

WT = working tree; TW = deployed tree. Where no tree is named, the file is md5-identical in both.

1. **HTTP server thread** `webhook-server`
   `threading.Thread(target=_waitress_serve, args=(webhook_receiver.app,))` — `main.py` WT 3664-3677 / TW 3989.
2. **Flask route** `@app.route("/webhook/<scanner_name>")` `webhook(scanner_name)` — `signals/webhook_receiver.py` WT 387-389 / TW 406-408.
   Calls `WebhookReceiver._handle_webhook` (WT 458-515 / TW 477-534). That handler returns 503 on shutdown and 429 per IP, and writes `webhook_audit` in its `finally`.
3. **`WebhookReceiver._process_request`** (WT 517-727 / TW 536-~745), in order:
   - `_authenticate` → 401
   - scan-map check → 404
   - `scanner_type=='eod'` → `_handle_eod` (never enqueued)
   - kill switch → 403
   - backpressure → 503
   - `self._mw.is_entry_allowed(now)` → 403
   - `json.loads`, then `_cast_numeric_fields`
   - required fields `("stocks","trigger_prices","triggered_at")` (WT 590 / TW 609)
   - `triggered_at` parse (WT 616-635 / TW 640-659)
   - `received_at = now_ist()` (WT 653 / TW 677)
   - `expiry_sec`: WT uses `edge_expiry_provider`; TW uses `sq_cfg.expiry_sec` (TW 679)
   - for each symbol: `_process_signal` (WT 701 / TW 719)
4. **`WebhookReceiver._process_signal`** (WT 874-1067 / TW 892-~1072), in order:
   - `price = float(price_str)` (WT 892 / TW 910)
   - age check
   - `_claim_in_flight`
   - TTL dedup
   - fingerprint
   - `INSERT INTO signals (… trigger_price …)` with status `QUEUED`
   - `entry = (signal_id, scanner_name, symbol, price, triggered_at)` and `self._queue.put_nowait(entry)` (WT 1042-1044 / TW 1047-1049)

   **ASYNC HOP 1:** `queue.Queue(maxsize=…signal_queue.capacity)` — `main.py` WT 3071-3073 / TW 3402-3404.
5. **`SignalProcessor._dispatcher_loop`** (thread `sp-dispatcher`; WT 359-381 / TW 377-399):
   `self._queue.get(timeout=self._drain_poll_sec)` → `_warm_zones` → `self._executor.submit(self._process_one_safe, signal_tuple)`.

   **ASYNC HOP 2:** `ThreadPoolExecutor` with `thread_name_prefix='sp-worker'`; `worker_count` 5.
6. **`SignalProcessor._process_one_safe`** (WT 387-440 / TW 405-~474):
   `rate_limiter.try_acquire('order')` (re-queues if exhausted) → `self._process_one(signal_tuple)`.
7. **`SignalProcessor._process_one`** (WT 880-1311 / TW 867-~1276), in order:
   - unpack `signal_id, scanner_name, symbol, trigger_price, triggered_at`
   - status `PROCESSING`
   - kill switch `is_active('entry')`
   - entry window
   - age check
   - `_reject_if_shadow_inning_active`
   - scan-map lookup, strategy lookup, `strategy_will_trade`
   - (WT only) `_policy_for_strategy`
   - `is_entry_allowed_for_strategy`
   - `strategy_governor.check`
8. **Screener:** `self._screener.screen(signal_id, symbol, scanner_name, trigger_price, triggered_at, …)` (WT 1049 / TW 998).
   Inside `SecondaryScreener.screen`: MIS-blocklist pre-drop → `self._quote_fn([symbol])` → `_build_market_data` → `_circuit_proximity_reason(trigger_price, …)` → `self._executor.run_all` → `scorer.score` → `_persist`.
9. **Price derivation:** `SignalProcessor._derive_prices(trigger_price, strategy_obj, now_time=now.time())` (WT 1079-1081 / TW 1028-1030).
10. **Retest-divert check** (WT 1093 / TW 1042). `wait_for_retest_enabled: false` in both trees.
11. **FIX-067 / M-S1 re-anchor**, only `if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None` (WT 1129 / TW 1082):
    `self._quote_fn([symbol])` → `_derive_prices(live_ltp, …)` (WT 1145-1147 / TW 1098-1100).
12. **Sizing:** `self._sizer.calculate(symbol, side, entry_price, sl_price, …)` (WT 1158 / TW 1112).
13. **Shadow observers:** `v3_chain.observe` and `allocator.observe`. `allocator_mode 'shadow'`.
14. **`SignalProcessor._admit_and_place`** (WT 1312-1585 / TW 1277-~1560), in order:
    - under `self._fm.portfolio_lock`: `_enforce_strategy_position_cap` → `_enforce_one_trade_per_symbol_direction` → `self._risk.approve` → `self._fm.reserve(…)` (WT 1362 / TW 1328)
    - `tgt_price = self._derive_target(entry_price, sl_price, strategy_obj)` (WT 1408 / TW 1368)
    - `_emit_signal_alert`
    - late kill-switch check
    - `self._entry_throttle.admit(symbol)` (WT 1451 / TW 1410)
    - `self._placer.place(… entry_price=entry_price, sl_price=sl_price, tgt_price=tgt_price, signal_trigger_price=trigger_price …)` (WT 1465-1479 / TW 1446-1460)
15. **`OrderPlacer.place`** (`orders/order_placer.py` 871-1765; md5-identical in both trees), in order:
    - FIX-025 block (905-924; `release_ltp` is None on this path)
    - R:R gate (938-955)
    - `order_protocol = self._default_protocol` (961; `'LIMIT_TRIPLE'`)
    - `resolve_slippage_fraction` (979-990)
    - `self._om.create_trade(… entry_target_price=entry_price …)` (996-1017)
    - `link_signal_trade`
    - OP-LM1 kill switch
    - status `PENDING`
    - EOD entry cutoff
    - FIX-128 slippage guard (1103-1195)
    - FIX-075 price drift (1197-1284)
    - liquidity check (1293-1305; a no-op, see A1)
    - retry loop: A-3 kill switch, then `self._engine.execute(… entry_price=entry_price …)` (1345-1356)
16. **`FullEntryEngine.execute`** (`orders/full_entry_engine.py` 72-119) → **`LimitTripleProtocol.execute`** (`orders/order_protocol_limit.py` 171-250):
    `_entry_order_price = 0.0 if entry_order_type == "MARKET" else entry_price`
    `self._adapter.place_order(symbol, side, qty, price=_entry_order_price, order_type=entry_order_type, intent, tag)` (210-219).
17. **`ZerodhaAdapter.place_order`** (`broker/zerodha_adapter.py` WT 478-651 / TW 494-~690), in order:
    - `_validate_place_order` (WT 527 / TW 560)
    - `_snap_order_to_tick` (WT 532 / TW 567)
    - force-intraday coercion
    - `self._pr.resolve`
    - CNC lock
    - `self._osm.register`

    Then it branches:
    - **PAPER:** `if self._paper:` (WT 573 / TW 608) → `_paper_place_order` → ASYNC HOP 3 `threading.Thread(target=self._synth_fill)` (WT 2086-2092 / TW 2177-2183).
    - **LIVE:** `self._rl.acquire(…)` (WT 587 / TW 622) → `self._kite.place_order(…)` (WT 604-615 / TW 639-654; TW adds `market_protection=market_protection`).
18. **After submission, inside `place()`:** `_persist_entry_orders` (4637-4706) → `_fill_map` insert → `self._order_monitor.track(expected_price=entry_price …)` (1604-1617) → Telegram ORDER PLACED.

**Dormant alternate entries** (present in code, unreachable today)

| Path | Chain | Why it is dormant |
|---|---|---|
| (a) EntryGate | `EntryGate._release` → `continue_from_gate(entry, release_ltp=…)` (WT 931 / TW 873) → `SignalProcessor.continue_from_gate` (WT 2061 / TW 2010) → `placer.place(release_ltp=…)` | `EntryGate.add` has no caller in either tree; VM `gate_state` = 0 rows |
| (b) Retest | `continue_from_retest` (WT 2408 / TW 2375) with `entry_order_type="MARKET"` | `wait_for_retest_enabled: false`; VM `retest_state` = 0 rows |

**Paper↔live differences on this chain**
1. `adapter.place_order` branch: paper `_paper_place_order` + `_synth_fill` vs live rate limiter + `kite.place_order`.
2. `quote_fn`: paper uses the `_make_paper_quote_provider` Kite quote with a 3 s TTL cache vs live `kite.quote`.
3. `get_quote_raw` returns `{}` in paper, so the FIX-128 and FIX-075 steps are skipped.
4. `_check_liquidity` is gated `self._mode == "LIVE"`, but it is a no-op in both modes.

---

### B2 — Exactly which price is treated as "the entry price", and where it is computed.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (cited logic identical) · **Uncommitted in WT:** MIXED (not the price code) · **Paper↔live:** DIFFER

**Answer:** the entry price is the variable `entry_price` returned by `SignalProcessor._derive_prices`.

**Formula as written:**
```
entry_price = trigger_price
if strategy.entry_method == "LIMIT":
    offset = float(strategy.entry_offset_pct)
    LONG:  entry_price = trigger_price * (1.0 - offset)
    SHORT: entry_price = trigger_price * (1.0 + offset)
```
- All 16 strategy YAMLs have `entry_method "LIMIT"`.
- `entry_offset_pct` is `0.001` for the 12 intraday strategies and `0.002` for the 3 `positional_*` strategies.

**Where it is computed, and where it can change before submission:**
1. First computed from the Chartink `trigger_price` (WT 1079 / TW 1028).
2. Recomputed from `live_ltp` by the same function, for the 10 strategies with `pullback_wait_enabled: false` (WT 1145-1147 / TW 1098-1100).
3. That value feeds sizing, `fm.reserve`, `_derive_target` and `placer.place(entry_price=entry_price)`.
4. Inside `OrderPlacer.place` it can change twice more:
   - FIX-025 `adjusted_limit`: gate path only, dormant.
   - FIX-075 `entry_price = current_ltp` (1261): when `drift_pct > 0.005` AND `additional_margin > 0` AND the top-up succeeds.
5. It is persisted as `trades.entry_target_price` **before** the drift step (1003).
6. The price Kite receives is `entry_price` after `_snap_order_to_tick` rounds it to the nearest tick.

**Measured example — the persisted "entry price" and the submitted price can differ.** Testing VM, QUICKHEAL 2026-09-07:

| Field | Value |
|---|---|
| `signals.trigger_price` | 158.52 |
| `trades.entry_target_price` | 157.9335 |
| log `price_drift_top_up_success` `adjusted_entry_price` | 158.73 |
| `order_execution_log` ENTRY `intended_price` | 158.73 |

**Evidence**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `signals/signal_processor.py` | 1773-1779 | `_derive_prices` | `entry_price = trigger_price` / `if strategy.entry_method == "LIMIT":` / `offset = float(strategy.entry_offset_pct)` / `entry_price = trigger_price * (1.0 - offset)` / `entry_price = trigger_price * (1.0 + offset)` |
| TW | `signals/signal_processor.py` | 1778-1784 | `_derive_prices` | same text |
| TW=WT | `orders/order_placer.py` | 1003 | `OrderPlacer.place` | `entry_target_price=entry_price,` |
| TW=WT | `orders/order_placer.py` | 1197-1261 | `OrderPlacer.place` | `original_entry_price = entry_price` … `drift_pct = abs(current_ltp - original_entry_price) / original_entry_price` … `if additional_margin > 0:` … `entry_price = current_ltp` |
| WT | `broker/zerodha_adapter.py` | 1400-1402 | `_snap_order_to_tick` | `if price and price > 0: new_price = _round_nearest_to_tick(price, tick)` |
| TW-DB | `trades` / `order_execution_log` | trd_1ce14a6d… | ro | `entry_target_price 157.9335; sl_initial 154.77483; tgt_initial 162.671505; trigger_price 158.52; ENTRY intended_price 158.73 actual_price 158.73` |
| TW-LOG | `logs/system_2026-09-07.log` | 10:01:18.002-.004 | order_placer | `price_drift_detected … current_ltp 158.73, drift_pct 0.00504…, original_price 157.9335, threshold 0.005`; `price_drift_top_up_success … adjusted_entry_price 158.73` |

**Paper↔live:** the derivation and the M-S1 re-derive run in both modes. The FIX-075 override is live-only, because `_fetch_ltp` returns None in paper. The tick snap runs in both.

---

### B3 — How many distinct price variables exist between the alert and the order? Name each and say what each means.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (the same 13 meanings) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer:** **13 distinct price meanings** on the active path.

**Counting rule:** one meaning per entry in the list, however many names it carries. The rule is a stated classification. The enumeration itself is measured.

**Two names are reused and change meaning mid-path:** `entry_price` and `sl_price`.

| # | Meaning | Names / where |
|---|---|---|
| 1 | Chartink trigger price | payload `trigger_prices` → `price_str` → `price` → `signals.trigger_price` → tuple slot → `trigger_price` → `signal_trigger_price` (OrderPlacer) → `_band_price` (986-988). Never re-anchored. |
| 2 | Screener LTP | `market_data['ltp'] = quote.last_price` (`secondary_screener._build_market_data`). Scoring / circuit state only. |
| 3 | Trigger-derived planned entry | `entry_price = trigger_price * (1 ∓ entry_offset_pct)` |
| 4 | Trigger-derived stop | `sl_price = entry_price * (1 ∓ sl_pct)`; clamped to `sl_min_pct`/`sl_max_pct`; widened by `sl_gap_buffer_pct` 09:15-09:30 (WT 1831-1885) |
| 5 | M-S1 live LTP | `live_ltp = float(q.last_price)` (WT 1134 / TW 1087) |
| 6 | LTP-anchored entry | `entry_price` reassigned from `_derive_prices(live_ltp, …)` (same name as #3) |
| 7 | LTP-anchored stop | `sl_price` reassigned by the same call (same name as #4) |
| 8 | Planned target | `tgt_price = _derive_target(…)`; RISK_REWARD `entry ± abs(entry - sl) * tgt_risk_reward` (WT 1926-1931). Persisted `trades.tgt_initial` (SL → `trades.sl_initial`). |
| 9 | Slippage-guard LTP | `_slip_ltp = release_ltp` else `self._fetch_ltp(symbol)` (1104-1108) |
| 10 | Drift-check LTP | `current_ltp = self._fetch_ltp(symbol)` (1202). A separate quote call from #9. |
| 11 | Pre-drift entry snapshot | `original_entry_price = entry_price` (1197). Equals `trades.entry_target_price`. |
| 12 | Drift-overridden entry | `entry_price = current_ltp` (1261) |
| 13 | Submitted order price | `_entry_order_price` (`order_protocol_limit.py:210`) → adapter `price` → `new_price` after `_snap_order_to_tick` → kite `price=` |

**Not counted**
- **Not a price on the entry:** the adapter `trigger_price` for the ENTRY LIMIT is `0.0`, so Kite receives `trigger_price=None`.
- **Derived amounts, not prices:** `_slip_rs`, `_slip_pct`, `_slip_tol`, `_slip_sl_dist`, `sl_distance`, `risk_amount`, `margin_reserved`, `drift_pct`, `additional_margin`, `effective_rr`.
- **Present but disabled:** `_check_liquidity` `ltp`, `best_bid`, `best_ask` (4088-4097).
- **Dormant paths only:** `release_ltp` / `adjusted_limit` (FIX-025); `WatchEntry.trigger_price` / `entry_price` / `sl_price` / `tgt_price`; retest `entry_est`, `break_level`, `structure_sl`.
- **After the order (out of scope):** `avg_fill_price`, `trades.entry_actual_price`, `actual_tgt_price` (FIX-013).

**Paper↔live:** in paper, #9, #10 and #12 are never populated because `_fetch_ltp` returns None, so 10 meanings carry values. #2 and #5 come from the paper quote provider.

---

### B4 — The exact meaning of "trigger" everywhere the word appears in this path.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (same identifier set) · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Answer:** the word carries **MORE THAN ONE meaning** in the codebase — at least six.

**On the entry path before submission,** "trigger" used as a price means **only the Chartink price**. It never names the derived planned entry; that is always `entry_price`.

**(a) Chartink scanner price**
- Payload `trigger_prices`; `signals.trigger_price` (schema comment `-- price from Chartink at trigger time`).
- Locals named `trigger_price` in `webhook_receiver`, `signal_processor`, `secondary_screener`, `hard_gate` and the `step_executor` signal_dict.
- The `_derive_prices` docstring: `entry = trigger * (1 - entry_offset_pct)`.
- `OrderPlacer` `signal_trigger_price` (`# FIX-128: original Chartink trigger for slippage guard`).
- Log fields `trigger_price` in `entry_slippage_observed` and `slippage_guard_exceeded`.
- The abort text `trigger={signal_trigger_price:.2f}` and the Telegram line `Trigger: Rs{signal_trigger_price:.2f}`.
- `WatchEntry.trigger_price # scanner-fired price`.
- Measured TW-LOG 2026-09-15: `"trigger_price":605.0` beside `"current_ltp":605.15`.
- **Ambiguity:** `hard_gate.circuit_proximity_reason` treats this Chartink price as the entry (`entry = _pos_num(trigger_price)`).

**(b) Chartink alert time** — `triggered_at` and its variants. A minute-precision time, not a price.

**(c) Broker-side stop trigger (order field)**
- `ZerodhaAdapter.place_order(trigger_price=0.0)`, docstring `stop trigger price (ZA17; required > 0 for SL/SL-M)`.
- Sent to Kite as `trigger_price=trigger_price if trigger_price > 0 else None`.
- It stays 0.0 on the ENTRY LIMIT.
- It is used by the SL legs placed **after** entry fill: `place_exits` `trigger_price=sl_price` (`order_protocol_limit.py` 377-390).
- `CO_PLUS_TGT` also uses `trigger_price=sl_price`, but that protocol is not selected.

**(d) Broker GTT trigger (DELIVERY, post-fill)** — `place_gtt` / `modify_gtt` `trigger_values`; `CncGtt` `sl_trigger` / `tgt_trigger`.

**(e) Internal thresholds**
- EntryGate `EG5 -- Price trigger: lower <= ltp <= upper` (dormant).
- SmartTgt `trigger_pct`.
- BreakevenManager `breakeven_trigger_pct` / `partial_lock_trigger_pct` (post-fill).

**(f) Event / actor wording** — kill-switch `triggered_by` / `triggered_at`; "15:15 IST trigger"; "trigger token invalidation".

**Evidence**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `core/schema.sql` | 42-72 | signals DDL | `trigger_price       REAL,                        -- price from Chartink at trigger time` |
| TW=WT | `orders/order_placer.py` | 885 | `OrderPlacer.place` | `signal_trigger_price: Optional[float] = None,  # FIX-128: original Chartink trigger for slippage guard` |
| WT | `broker/zerodha_adapter.py` | 486, 504, 613 | `place_order` | `trigger_price: float = 0.0,` … `trigger_price: stop trigger price (ZA17; required > 0 for SL/SL-M)` … `trigger_price=trigger_price if trigger_price > 0 else None,` |
| TW=WT | `orders/order_protocol_limit.py` | 374-390 | `place_exits` | `sl_order_type = "SL"` … `trigger_price=sl_price,` |
| TW=WT | `screening/hard_gate.py` | 81 | `circuit_proximity_reason` | `entry = _pos_num(trigger_price)` |

**Search width:** `grep -oi '[A-Za-z_]*trigger[A-Za-z_]*'` over 14 entry-path files in WT and 6 in TW. The six senses are a floor for the whole codebase and complete for the files listed.

---

### B5 — Which price does the 1% check compare the LTP against?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (`order_placer.py` identical; config values identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer:** against `signal_trigger_price`, **the original Chartink trigger price**. Not the planned entry, not the re-anchored entry, and not the tick-snapped order price.

**What the check computes**
- `_slip_rs = abs(_slip_ltp - signal_trigger_price)`
- `_slip_pct = _slip_rs / signal_trigger_price * 100`

**Order of the two aborts** (with `slippage_control.enabled` true and `mode` `sl_fraction`), inside `_slippage_decision`:
1. Abort if `slip_rs > tol`, where `tol = min(abs(signal_price - sl_price) * frac, absolute_cap_rs)` capped by `hard_max_slippage_rs`.
2. Otherwise abort if `slip_pct > max_pct`, i.e. the 1%.

**What each input is**
- `signal_trigger_price` on the direct path is `trigger_price`, the webhook tuple price (SP WT 1476 / TW ~1457).
- M-S1 re-anchors entry and SL but never changes `trigger_price`.
- So the % reference stays the Chartink price, while the rupee tolerance uses `abs(Chartink price - sl_price)` with the possibly re-anchored SL.
- The LTP is a fresh `adapter.get_quote_raw` call, taken after `create_trade` and before the drift step.

**Measured TW-LOG (09-03..09-15):** 126 `entry_slippage_observed` lines and 9 `slippage_guard_exceeded` lines.

**Evidence**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 651 | — | `max_entry_slippage_pct: 1.0 # FIX-128: abort if current LTP deviates > 1% from signal trigger price` (WT 674) |
| TW=WT | `orders/order_placer.py` | 1103-1111 | `OrderPlacer.place` | `if signal_trigger_price is not None and signal_trigger_price > 0:` / `_slip_ltp = release_ltp  # gate path: already have LTP` / `if _slip_ltp is None:` `_slip_ltp = self._fetch_ltp(symbol)` / `if _slip_ltp is not None:` `_slip_rs = abs(_slip_ltp - signal_trigger_price)` / `_slip_pct = _slip_rs / signal_trigger_price * 100` |
| TW=WT | `orders/order_placer.py` | 380-390 | `_slippage_decision` | `if slip_rs > tol: … return (f"slippage ₹{slip_rs:.2f} > tolerance ₹{tol:.2f} " …` / `if (getattr(cfg, "also_apply_pct_check", True) and getattr(cfg, "mode", "") != "pct" and slip_pct > max_pct):` |
| WT | `signals/signal_processor.py` | 1476 | `_admit_and_place` | `signal_trigger_price=trigger_price,  # FIX-128: for slippage guard` |

**Paper↔live:**
- **Live:** `_fetch_ltp` → `get_quote_raw` → `kite.quote`, so the check runs.
- **Paper:** `get_quote_raw` returns `{}`, so `_fetch_ltp` returns None (`if not raw_quote: return None`) and the whole FIX-128 guard, including the 1% check, is skipped on the direct path.

---

### B6 — Is the entry price ever re-anchored to live LTP? If yes: where, when, and are SL, target and R:R re-anchored with it?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (re-anchor logic identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer:** YES. It happens at **two** points before submission, with different consequences. A third change happens after the fill.

**(1) FIX-067 / M-S1 momentum re-anchor** — `SignalProcessor._process_one` WT 1129-1152 / TW 1082-1105.
- **When:** after screening, the trigger-based `_derive_prices` and the retest-divert check; before sizing, risk approve, reservation and target.
- **Condition:** `not strategy_obj.pullback_wait_enabled and self._quote_fn is not None` and `live_ltp > 0`.
- **What changes:** `entry_price, sl_price = self._derive_prices(live_ltp, …)`. So entry and SL are re-derived.
  - TGT is derived afterwards from the new entry and SL (WT 1408), so **TGT is re-anchored and R:R is preserved** (`tgt_risk_reward 1.5` in all YAMLs).
  - qty and reserved capital also use the new basis.
  - `trigger_price` / `signal_trigger_price` are **not** re-anchored.
- **Scope:** 10 of 16 strategies have `pullback_wait_enabled: false`: gap_fade_long/short, gap_go_long/short, range_breakout_long/short, positional_momentum_long, positional_sector_rotation, positional_swing_long, pb01_breakout_retest [enabled: false].
  The 6 with `true` are NOT re-anchored: first_pullback_long/short, open_high_breakdown_short, open_low_breakout_long, vwap_bounce_long, vwap_rejection_short.
- **Measured (TW-DB, trades since 2026-08-15, all LIVE):**
  - `pullback_wait=true`: 151/151 have `entry_target_price == trigger*(1∓offset)`.
  - `pullback_wait=false`: 147 differ, 33 equal. The cause of those 33 is **NOT ESTABLISHED**.
  - TW-LOG September: 479 `FIX-067 momentum fresh quote:` lines, 0 `unavailable`.

**(2) FIX-075 price-drift override** — `OrderPlacer.place` 1197-1284.
- **When:** after `create_trade` (the trades row is already written), after the FIX-128 guard, before liquidity and `engine.execute`.
- **Condition:** all three must hold:
  - `drift_pct = abs(current_ltp - original_entry_price) / original_entry_price > 0.005` (ctor default; `main.py` does not pass it);
  - `additional_margin = new_margin - original_margin > 0`;
  - `fm.top_up_reservation` succeeds.
- **What changes:** `entry_price = current_ltp` (1261) and nothing else.
  - **SL, TGT, qty, risk_amount and `trades.entry_target_price` / `sl_initial` / `tgt_initial` are NOT re-anchored.**
  - The R:R gate (938-955) already ran on the pre-drift entry.
- **Measured case** trd_1ce14a6d… (QUICKHEAL LONG, 2026-09-07):
  - trigger 158.52; entry_target 157.9335; SL 154.77483; TGT 162.671505; submitted 158.73.
  - Arithmetic on these values: R:R at 158.73 = (162.671505 − 158.73)/(158.73 − 154.77483) = **0.997**, against 1.5 at 157.9335.
  - TW-LOG `price_drift_top_up_success` occurred 1 time (07-Sep) in 09-03..09-15.

**(3) FIX-025 gate-release limit adjust** — `order_placer.py` 905-924. **DORMANT:** `EntryGate.add` has no caller. SL/TGT are not recomputed.

**(4) Retest path** — **DORMANT** (`wait_for_retest_enabled: false`).

**(5) After the fill (not LTP)** — FIX-013 `_place_limit_triple_exits` (2870-2879): `actual_tgt_price = calc_tgt_price(entry_price=avg_fill_price, sl_price=fill_entry.sl_price, rr_ratio=…)`. R:R is restored about the fill price; the SL is unchanged.

**Evidence**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `signals/signal_processor.py` | 1129, 1145-1147 | `_process_one` | `if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:` … `entry_price, sl_price = self._derive_prices(` `live_ltp, strategy_obj, now_time=now.time()` |
| TW | `signals/signal_processor.py` | 1082, 1098-1100 | `_process_one` | same text |
| TW=WT | `orders/order_placer.py` | 1261 | `OrderPlacer.place` | `# Top-up succeeded - use current_ltp for placement` / `entry_price = current_ltp` |
| TW=WT | `orders/order_placer.py` | 2870 | `_place_limit_triple_exits` | `# FIX-013: Recalculate TGT from actual fill price to preserve R:R.` |

**Paper↔live:**
- (1) runs in both modes. The paper LTP may be up to 3 s old (TTL cache).
- (2) is live-only.
- (5) runs in both modes, on the synthesized fill in paper.

---

### B7 — Is the entry price available at SIGNAL_RECEIVED, or only later? Give the as-of timestamp semantics.
**Status:** PARTIAL · **WT↔VM:** **DIFFERS — LOGIC** (`expires_at`) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer**

**`SIGNAL_RECEIVED` is not a code identifier.** It appears only in design docs under `docs/design/secondary_filteration/` (10 hits in WT; 0 in the TW snapshot).

**At webhook receipt, the nearest code event, the entry price is NOT available.**
- The only price at receipt is the Chartink price (`signals.trigger_price`).
- The `signals` table has no entry-price column.

**When the entry price comes into existence, in order:**
1. First computed on an `sp-worker` thread in `_process_one`, after strategy lookup and after the screener's quote fetch and scoring (WT 1079 / TW 1028).
2. Recomputed at M-S1.
3. Possibly overridden at FIX-075.
4. Tick-snapped in the adapter.

**Timestamp semantics as written:**
- **`triggered_at`:** parsed with formats `("%Y-%m-%d %H:%M:%S", "%I:%M %p", "%H:%M")`.
  - Time-only formats become `datetime(today.year, today.month, today.day, parsed.hour, parsed.minute, 0)` with `today = now.date()`. That gives minute precision, seconds forced to 0, and the date taken from receipt.
  - Then `.replace(tzinfo=ist_timezone())`. This attaches IST; it does not convert.
- **`received_at`:** `now_ist()`, taken once per HTTP request and shared by all symbols in the batch.
- **`expires_at`:**
  - **TW (deployed):** `received_at + timedelta(seconds=expiry_sec)`.
  - **WT (not deployed):** `received_at.replace(hour=23, minute=59, second=59, microsecond=0)` when `expiry_sec` is None.
- **Entry computation time:** no dedicated timestamp is persisted.
  - `now = now_ist()` at the start of `_process_one` is used for window/age checks and the gap-buffer.
  - The M-S1 LTP carries `Quote.ts = now_ist()` at fetch, but it is not persisted.
  - The FIX-128 / FIX-075 LTPs carry no timestamp.
- **Persisted:**
  - `trades.created_at = now_ist()` at `create_trade` (`order_manager.py:209`), holding the pre-drift `entry_target_price`.
  - `orders.placed_at` at `_persist_entry_orders`.

**NOT ESTABLISHED:** the as-of instant of Chartink's trigger price relative to `triggered_at`. Chartink is external, and code carries only comments (`-- price from Chartink at trigger time`; `Chartink triggered_at is scan time, not delivery time`).

**Measured example (TW-DB, QUICKHEAL 2026-09-07):**

| Event | Time |
|---|---|
| `triggered_at` | 2026-09-07T10:01:00+05:30 |
| `received_at` | 10:01:13.663080 |
| drift log | 10:01:18.002 |
| ENTRY `placed_at` | 10:01:18.045202 |

**Evidence**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `signals/webhook_receiver.py` | 640-659, 677 | `_process_request` | `for fmt in ("%Y-%m-%d %H:%M:%S", "%I:%M %p", "%H:%M"):` … `triggered_at = datetime(today.year, today.month, today.day, parsed.hour, parsed.minute, 0)` … `triggered_at = triggered_at.replace(tzinfo=ist_timezone())` … `received_at = now_ist()` (WT 616-635, 653) |
| WT | `core/schema.sql` | 42-72 | signals DDL | `triggered_at TEXT NOT NULL, -- ISO IST from Chartink; received_at TEXT NOT NULL, -- ISO IST when we received it; … trigger_price REAL, -- price from Chartink at trigger time` |
| TW | `signals/signal_processor.py` | 910, 1028-1030 | `_process_one` | `now = now_ist()` … `entry_price, sl_price = self._derive_prices(trigger_price, strategy_obj, now_time=now.time()` |

**Paper↔live:** receipt and derivation timing are identical. The M-S1 LTP may come from the 3 s cache in paper. FIX-075 is live-only.

---

## 3. GROUP C — ORDER CONSTRUCTION

### C1 — Exact order type submitted today: limit, SL, SL-M, market, protected market, or other. Quote the API call.
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS — LOGIC** (TW adapter forwards `market_protection`; for entries it is None, so the wire body is identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer:** every entry today is a plain **LIMIT** order.
- `variety "regular"`, exchange NSE.
- Product MIS for today's entries.
- No `trigger_price` on the wire.
- No `market_protection` on the wire.

**How the type is chosen** (these files are md5-identical in both trees):
- `OrderPlacer.place` line 961: `order_protocol = self._default_protocol`.
  - The ctor default is `default_order_protocol: str = "LIMIT_TRIPLE"` (572), and `main.py` passes none.
- `entry_order_type: str = "LIMIT"` is the default at `order_placer.py:888`, `full_entry_engine.py:85` and `order_protocol_limit.py:183`.
- `LimitTripleProtocol.execute` passes no `trigger_price` and no `variety`. The adapter defaults `trigger_price: float = 0.0` and `variety: str = "regular"` therefore apply.
- `_KITE_ORDER_TYPES` maps `"LIMIT"` → `"LIMIT"`.
- `validity` is never passed. The broker's default validity is **NOT ESTABLISHED** from code.

**`market_protection`:**
- WT has 0 occurrences in `zerodha_adapter.py`.
- TW `place_order` takes `market_protection: Optional[float] = None` (TW 505) and forwards it (TW 653). The only non-None caller is `orders/mis_autosquareoff.py` (TW 877), an MIS EOD exit.
- VM `kiteconnect 5.1.0` `KiteConnect.place_order` does `params = locals()` and then deletes every `None` entry. So `None` fields (`market_protection`, `trigger_price`, `validity`) are omitted from the request.

**Other entry shapes in code, not used today:**

| Shape | What it would send | Why it is not used |
|---|---|---|
| (a) `CO_PLUS_TGT` (`order_protocol_co.py` 123-133) | `order_type="SL"`, `trigger_price=sl_price`, `variety="co"` | Nothing selects it. The 16 strategy YAMLs declare `order_protocol` (13 `"CO_PLUS_TGT"`, 3 `"LIMIT_TRIPLE"`), but **no code reads `strategy.order_protocol`** (both trees). |
| (b) MARKET via the retest path | `entry_order_type="MARKET"` | DORMANT. |
| (c) `entry_mode` | only `'FULL'` exists | — |

**Measured — TW-DB:**
- 773 ENTRY rows, all `LIMIT`/`regular` (641 MIS, 132 CNC), `COUNT(trigger_price)=0`.
- Today: 5 ENTRY rows, `LIMIT`/`regular`/MIS.
- Trades: 954/954 `LIMIT_TRIPLE`, `FULL`.

**Measured — TW-LOG 2026-09-15:**
- `place_order call_start`: LIMIT 9, SL 4, MARKET 0.
- `limit_triple.entry_placed`: 5.
- `co_plus_tgt.co_placed`: 0 on 07-15 Sep.
- The 3 MARKET orders on 07-Sep (V2RETAIL 15:03-15:06) were **exits**. Zerodha rejected them with "Market orders without market protection are not allowed via API. Please set market protection or use a Limit order."

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_protocol_limit.py` | 210-219 | `LimitTripleProtocol.execute` | `_entry_order_price = 0.0 if entry_order_type == "MARKET" else entry_price` / `entry_placed = self._adapter.place_order(symbol=symbol, side=side, qty=qty, price=_entry_order_price, order_type=entry_order_type, intent=intent, tag=order_tag,)` |
| TW | `broker/zerodha_adapter.py` | 639-654 | `ZerodhaAdapter.place_order` | `kite_order_id = self._kite.place_order(variety=variety, exchange="NSE", tradingsymbol=symbol, transaction_type=_KITE_TRANSACTION[side], quantity=qty, product=broker_code, order_type=_KITE_ORDER_TYPES[order_type], price=price if order_type in ("LIMIT", "SL") else None, trigger_price=trigger_price if trigger_price > 0 else None, tag=tag, market_protection=market_protection,)` |
| WT | `broker/zerodha_adapter.py` | 604-615 | `ZerodhaAdapter.place_order` | same call without `market_protection` |
| TW-LIVE | `venv/…/kiteconnect/connect.py` (5.1.0) | 339- | `KiteConnect.place_order` | `params = locals()` / `del (params["self"])` / `for k in list(params.keys()): if params[k] is None: del (params[k])` |

**Paper↔live:**
- Identical up to `ZerodhaAdapter.place_order`.
- **Live:** `self._rl.acquire` → `self._kite.place_order`.
- **Paper:** `self._paper_place_order` returns SUBMITTED with id `PAPER_<hex>` and starts `threading.Thread(target=self._synth_fill)` (WT 2086-2092 / TW 2177-2183). With `paper.ltp_gating_enabled: true`, a LIMIT BUY fills when LTP <= price at `min(LTP, price)`. No broker call is made.

---

### C2 — How is the order's price field computed? Give the formula as written.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (cited logic identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer:** the Kite `price` field is `price if order_type in ("LIMIT", "SL") else None`. For today's LIMIT entry, `price` is built in these steps, in order:

1. **Trigger-derived entry.** `_derive_prices` (WT 1773-1779 / TW 1778-1784):
   `entry_price = trigger_price`; if `entry_method == "LIMIT"`, then LONG `trigger_price * (1.0 - offset)`, SHORT `trigger_price * (1.0 + offset)`.
2. **M-S1 re-anchor** (only if `not strategy_obj.pullback_wait_enabled and self._quote_fn is not None`; 10 of 16 strategies).
   The same formula is re-run on `live_ltp` (WT 1145-1147 / TW 1098-1100).
3. **FIX-025** (`order_placer.py` 905-914), only `if release_ltp is not None`. **DORMANT** (C3).
   - BUY: `adjusted_limit = min(entry_price + self._entry_gate_slippage_buffer, release_ltp)`.
   - SELL: `adjusted_limit = max(entry_price - self._entry_gate_slippage_buffer, release_ltp)`.
4. **FIX-075 drift** (`order_placer.py` 1197-1261):
   - `drift_pct = abs(current_ltp - original_entry_price) / original_entry_price`.
   - If `drift_pct > self._price_drift_threshold` (0.005) and `additional_margin = new_margin - original_margin > 0` (`required_margin = (qty * price) / leverage`) and the top-up succeeds, then `entry_price = current_ltp`.
5. **Protocol.** `order_protocol_limit.py:210`: `_entry_order_price = 0.0 if entry_order_type == "MARKET" else entry_price`.
6. **Tick snap.** `ZerodhaAdapter._snap_order_to_tick`, non-SL branch (WT 1400-1402 / TW 1448-1450): `if price and price > 0: new_price = _round_nearest_to_tick(price, tick)`.
   The helper (`broker/slippage_engine.py` 175-187, md5-identical) computes `d_result = (d_value / d_tick).quantize(Decimal('1'), rounding=ROUND_HALF_UP) * d_tick`.
7. **Kite call:** `price=price if order_type in ("LIMIT", "SL") else None`.

**TW-LOG 07-15 Sep:** `price_drift_top_up_success` 1 (07-Sep); `order_placer.slippage_protection` (FIX-025) 0.

**Paper↔live:** steps 1-3 and 5-7 run in both modes. Step 4 is live-only, because `get_quote_raw` returns `{}` in paper.

---

### C3 — Where does slippage_buffer enter the order price, if at all?
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** MIXED (not these lines) · **Paper↔live:** IDENTICAL

**Answer:** in exactly one place: `OrderPlacer.place` FIX-025 (`order_placer.py` 905-924), and only when `release_ltp is not None`.
- LONG: `adjusted_limit = min(entry_price + self._entry_gate_slippage_buffer, release_ltp)`.
- SHORT: `adjusted_limit = max(entry_price - self._entry_gate_slippage_buffer, release_ltp)`.
- Then `entry_price = adjusted_limit`.
- It is an absolute rupee amount: 2.0 (TW config 645 / WT 668), wired at `main.py` TW 3074 / WT 2833.

**Why this path is not reached today:**
- The only producer of `release_ltp` is `SignalProcessor.continue_from_gate` (WT 2294/2305, TW 2251/2262), the EntryGate release callback.
- `EntryGate.add` has **no caller in either tree**.
- The direct path's `placer.place` (WT 1465 / TW 1446) passes no `release_ltp`, so it defaults to None.

**Measured:** `order_placer.slippage_protection` 0 in TW-LOG 07/08/09/10/11/15 Sep; `gate_state` 0 rows.

**Conclusion:** `slippage_buffer` does **not** enter any order price on the active path today. It is not used by the FIX-128 guard.

**Search width:** `grep -i slippage_buffer` over all `*.py`/`*.yaml` (both trees); `gate.add(` variants (both trees).

---

### C4 — Does the system ever place a broker-side order or trigger BEFORE its own internal entry decision is complete?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (sequencing code md5-identical; TW adds an exit-only file) · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Answer — on the active path: NO.** No broker-side SL, SL-M, trigger, GTT, bracket or cover order is placed before or together with the entry. The only broker order sent at entry time is the **ENTRY LIMIT itself** (`variety regular`, no `trigger_price`), and it is the last step of the internal chain.

**What runs before submission** (`order_placer.py`, identical in both trees):
1. webhook → screener → `_derive_prices` → M-S1 → sizing → `fm.reserve` → late kill switch → entry throttle (`signal_processor`)
2. R:R gate (938-955)
3. `create_trade` / `link_signal_trade` (996-1034)
4. OP-LM1 kill switch (1046-1054)
5. EOD cutoff (1072-1093)
6. FIX-128 guard (1103-1195)
7. FIX-075 drift (1197-1284)
8. liquidity check (1293-1305; inert)
9. A-3 kill switch (1334-1343)
10. `self._engine.execute(...)` (1345-1356) → `LimitTripleProtocol.execute`, which places only the ENTRY (210-219)

**SL and TGT are deferred until after a fill:**
- The protocol docstring: "Phase 1 (execute): ENTRY LIMIT at entry_price. Phase 2 (place_exits): SL + TGT … Called by OrderPlacer on ENTRY fill."
- `place_exits` is reached only from `_handle_entry_fill`, `_on_order_partially_terminated` (`qty_filled > 0`) and `_retry_limit_triple_exits`, all via `FullEntryEngine.place_deferred_exits`.
- The CNC OCO GTT is reached only post-fill.

**Every other `place_order` call site is an exit or protection:** kill switch, EOD squareoff, `mis_autosquareoff` (TW only), `_emergency_market_exit`, reconciler flatten/close/SL, `sl_breach_monitor`, `structure_exit_manager`, `place_tgt_only`. `signals/` and `screening/` contain no order placement in either tree.

**What DOES rest in the market and can fill on first touch:** the ENTRY LIMIT itself, after submission. Nothing internal confirms it after that. It is cancelled only by:
- `order_monitor._check_fill_timeout` when elapsed > 60 s (ENTRY legs only), or
- FIX-141 when pending R:R < `min_pending_rr` 1.0.

**Measured, TW-LOG 07-15 Sep:** 46 `fill_timeout`, 5 `pending_rr_cancelled`.

**The 6 `pullback_wait_enabled: true` strategies:** M-S1 is skipped, so their LIMIT is priced from the Chartink trigger (LONG `trigger*(1-offset)`, below the trigger). The code comment says "Pullback strategies skip this (EntryGate already waits for current price)", **but `EntryGate.add` has no caller**. These limits are therefore placed immediately and rest until price touches them.

**Paths that would put a broker trigger at entry — all unselected or dormant today:**
- (a) `CO_PLUS_TGT`: `order_type="SL"`, `trigger_price=sl_price`, `variety="co"`. Not selectable.
- (b) Retest MARKET entry: dormant.
- (c) EntryGate release: dormant.

**Measured, TW-DB:**
- 333 SL rows: 0 placed before their ENTRY `placed_at`, 0 before `trades.entry_time`, 0 before ENTRY `filled_at`. Minimum gap after `entry_time` is 0.074 s.
- 318 TGT rows: the same three zeros.
- 52 `gtt_state` rows: 0 created before `entry_time`.
- 773 ENTRY rows: all `LIMIT`/`regular`, `COUNT(trigger_price)=0`.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_protocol_limit.py` | 5-8, 186-195 | module / `execute` | `Phase 1 (execute):   ENTRY LIMIT at entry_price.` / `Phase 2 (place_exits): SL + TGT … Called by OrderPlacer on ENTRY fill.` … `sl_price and tgt_price are accepted here for signature symmetry … but are NOT used` |
| TW=WT | `orders/order_placer.py` | 2152-2159 | `_handle_entry_fill` | `if fill_entry.order_protocol == "LIMIT_TRIPLE": self._place_limit_triple_exits(trade_id=trade_id, fill_entry=fill_entry, qty_filled=int(event.filled_qty), avg_fill_price=float(event.avg_fill_price), reason="entry_fill",)` |
| TW=WT | `broker/order_monitor.py` | 1085-1106 | `_check_fill_timeout` | `if entry.leg in ("SL", "TGT", "EOD"): return` … `if elapsed <= self._fill_timeout: return` … `result = self._adapter.cancel_order(entry.broker_order_id)` |
| TW | `signals/signal_processor.py` | 1060-1082 | `_process_one` | `Pullback strategies skip this (EntryGate already waits for current price).` … `if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:` |

**Search width:** `.place_order(|.place_gtt(|.modify_gtt(|.modify_order(|kite.place` over all `*.py` in both trees, with each hit's enclosing function classified.

**Caveat:** the DB timing check covers persisted rows only. A broker order placed but never persisted would not appear; none was found by code search on the entry side.

---

### C5 — Is the allowed-slippage check applied before submission, after the fill, or both? Quote the check.
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** MIXED (not these lines) · **Paper↔live:** DIFFER

**Answer: BEFORE SUBMISSION ONLY.** The single allowed-slippage **abort** is FIX-128 in `OrderPlacer.place` (1103-1195). It runs after the EOD cutoff and before FIX-075 and `engine.execute`.

**The check as written:**
```
if signal_trigger_price is not None and signal_trigger_price > 0:
    _slip_ltp = release_ltp
    if _slip_ltp is None: _slip_ltp = self._fetch_ltp(symbol)
    if _slip_ltp is not None:
        _slip_rs = abs(_slip_ltp - signal_trigger_price)
        _slip_pct = _slip_rs / signal_trigger_price * 100
        if _scfg is not None and getattr(_scfg, "enabled", False):
            _abort_reason, _slip_tol, _slip_sl_dist = _slippage_decision(_scfg, signal_trigger_price, sl_price, _slip_rs, _slip_pct, self._slippage_tier_tuples, self._max_entry_slippage_pct, fraction_override=_tol_fraction)
        else: legacy flat %
        ... if _abort_reason is not None: ... raise slip_exc   (trade REJECTED)
```

**Tolerance:**
- `sl_dist = abs(signal_price - sl_price)`
- `tol = min(sl_dist * frac, cfg.absolute_cap_rs)`
- `return min(tol, cfg.hard_max_slippage_rs)`
- Abort if `slip_rs > tol`; else abort if `also_apply_pct_check and mode != "pct" and slip_pct > max_pct`.

**Deployed values:** `max_entry_slippage_pct 1.0` · `enabled true` · `mode sl_fraction` · `max_slippage_fraction 0.22` · `absolute_cap_rs 5.00` · `hard_max_slippage_rs 10.0` · `also_apply_pct_check true` · overrides all `{}` → `(0.22, "global")`.

**After the fill: no allowed-slippage check, and no abort or exit on fill slippage.**
- `order_monitor._handle_complete` computes `slippage = _calc_slippage_pct(entry.side, final_price, entry.expected_price)` and publishes `OrderFilled(… slippage_pct=slippage)`.
- The only consumer of `.slippage_pct` is `orders/slippage_recorder.py:139`, and it only records.

**Between submission and fill (not a slippage check):** FIX-141 cancels a pending ENTRY when `remaining_reward / risk_distance < min_pending_rr` (1.0).

**Measured, TW-LOG (07/08/09/10/11/15 Sep):**
- `entry_slippage_observed`: 24/19/11/16/23/5
- `slippage_guard_exceeded`: 2/3/0/0/0/0

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_placer.py` | 1103-1129 | `OrderPlacer.place` | as quoted above |
| TW=WT | `orders/order_placer.py` | 345-361, 380-390 | `_compute_slippage_tolerance` / `_slippage_decision` | as quoted in A3/A4/A5 |
| TW=WT | `broker/order_monitor.py` | 996-1010 | `_handle_complete` | `slippage = _calc_slippage_pct(entry.side, final_price, entry.expected_price)` … `OrderFilled(… expected_price=entry.expected_price, slippage_pct=slippage, …)` |
| WT | `orders/slippage_recorder.py` | 139 | `SlippageRecorder` | `"slippage_pct": (round(ev.slippage_pct, 4) if ev.slippage_pct else None),` |

**Paper↔live:** the pre-submission check is live-only, because `get_quote_raw` returns `{}` in paper. Post-fill recording happens in both modes.

---

### C6 — Where does tick-size come from — instrument metadata or a constant? If a constant, give it. What happens when tick metadata is missing or invalid?
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** NO (cited files clean) · **Paper↔live:** IDENTICAL (order price)

**Source:** instrument metadata.
- `InstrumentCache.load(config_dir / "instruments.csv")` at boot, with column `tick_size=float(raw["tick_size"])` (`core/instrument_cache.py:147`).
- Wired once: `broker_adapter.set_instrument_cache(instrument_cache)` (`main.py` WT 2238 / TW 2522).
- The single chokepoint is `ZerodhaAdapter._resolve_tick` (WT 1335-1359 / TW 1383-1407), used by `_snap_order_to_tick` for every `place_order` and by `modify_order`.

**Constant fallback:** `DEFAULT_TICK = 0.05` (`orders/price_math.py:27`).

**Missing tick at order time** (cache unwired, symbol absent, tick None, or tick <= 0):
- Logs WARNING `snap_to_tick.missing_tick_size` once per symbol per process.
- Returns `DEFAULT_TICK`; the price is still rounded to a 0.05 multiple.
- The order is **not blocked**.
- Measured TW-LOG fallbacks: RIR, XTRANET, MAFANG (07-Sep); MAFANG, NIFTY1 (08-Sep); MONQ50 (09-Sep); MAFANG (11-Sep).

**Invalid tick at load:**
- `InstrumentCache.load` raises `ConfigSchemaError` for an unparseable value or `tick_size <= 0`.
- `main.py` catches it, logs `InstrumentCache pre-load failed` and leaves `instrument_cache` None.
- Per the `main.py` comment, `run_all_startup_checks` then blocks boot (`instrument_cache_too_small`, return 3). This part is from the comment; `utils/startup_checks.py` was not read.

**NaN / inf ticks:** both pass the `<= 0` checks.
- `_round_nearest_to_tick(100.03, nan)` returns `nan`.
- `_round_nearest_to_tick(100.03, inf)` raises `decimal.InvalidOperation`.
- These were measured by executing the extracted function text outside the repo. The current VM `instruments.csv` has no such value.

**VM `config/instruments.csv`** (mtime 2026-09-15 09:00:02): 2,228 rows, 0 non-positive or unparseable, 0 non-finite. Ticks: 0.01×970 · 0.05×838 · 0.1×355 · 0.5×38 · 1.0×16 · 5.0×11.

**Caveat — which file the running process uses:** this CSV was rewritten at 09:00:02 by cron, **after** the 08:15 boot load, and no reload wiring was found. The tick table in use is the pre-09:00 file, whose content was **NOT ESTABLISHED**.

**Other tick consumers:**
- `calc_sl_limit_price` uses default `tick_size = DEFAULT_TICK`; the adapter then re-snaps with the real tick.
- `OrderPlacer._tick_for`: `return tick if tick and tick > 0 else DEFAULT_TICK`.
- `CncGttPlacer._safe_tick`: `return t if t > 0 else DEFAULT_TICK`.
- Paper `SlippageEngine.apply` rounds only `if tick is not None and tick > 0`.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `broker/zerodha_adapter.py` | 1343-1359 | `_resolve_tick` | `tick = self._instrument_cache.tick_size(symbol)` … `except Exception: tick = None` … `if tick is None or tick <= 0:` … `self._log.warning("snap_to_tick.missing_tick_size", …)` … `return DEFAULT_TICK` |
| TW=WT | `orders/price_math.py` | 27 | module | `DEFAULT_TICK = 0.05` |
| TW=WT | `core/instrument_cache.py` | 147, 171-177 | `InstrumentCache.load` | `tick_size=float(raw["tick_size"])` … `if row.tick_size <= 0: raise ConfigSchemaError(…)` |

---

### C7 — Is price rounding done before or after the validity checks?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (same order; TW validation adds `market_protection` bounds) · **Uncommitted in WT:** NO · **Paper↔live:** IDENTICAL

**Answer: AFTER.** At the broker chokepoint the order is:
1. `self._validate_place_order(...)` (WT 527 / TW 560-562).
2. `price, trigger_price = self._snap_order_to_tick(...)` (WT 532-534 / TW 567-569).

Nothing re-validates after the snap.

**What `_validate_place_order` checks:** symbol non-empty; side in {BUY, SELL}; qty a positive int; `order_type` in {MARKET, LIMIT, SL, SL-M}; `price <= 0` for LIMIT/SL; `trigger_price <= 0` for SL/SL-M.

**Every upstream entry check also uses unrounded prices:** the R:R gate, FIX-128, FIX-075, sizing and `fm.reserve`. The code comment (`order_placer.py` 928-931) says: "the adapter is now the sole snap point (no per-call-site rounding)". The unrounded `entry_price` is what is persisted as `trades.entry_target_price` and passed as `expected_price`.

**Exceptions — rounding before a check (exit/GTT legs, not the entry):**
- (a) SL leg: `calc_sl_limit_price` rounds with `round_to_tick(limit, tick_size, mode="down"/"up")` before adapter validation.
- (b) CNC GTT: triggers are rounded (`cnc_gtt.py` 115-118) before `_validate_trigger_distance` (121).
- (c) `modify_order` rounds and does not validate.

*INFERENCE (not measured):* since there is no post-snap re-check, a positive price below tick/2 would snap to 0.0 after passing `price > 0`.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `broker/zerodha_adapter.py` | 560-569 | `place_order` | `self._validate_place_order(symbol, side, qty, price, order_type, trigger_price, market_protection)` … `# FIX-181 (GICRE incident): authoritative tick-snap. Runs in BOTH paper and live (parity)` … `price, trigger_price = self._snap_order_to_tick(symbol, order_type, side, price, trigger_price)` |
| WT | `broker/zerodha_adapter.py` | 2040-2049 | `_validate_place_order` | `if order_type in ("LIMIT", "SL") and price <= 0: raise ValueError(…)` / `if order_type in ("SL", "SL-M") and trigger_price <= 0:` |

---

### C8 — Are any broker-side constraints on trigger-versus-limit separation enforced or validated anywhere?
**Status:** PARTIAL · **WT↔VM:** DIFFERS — file only (SL snap identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Answer: NOT VALIDATED ANYWHERE for day orders.** The separation is only constructed by formula. For today's ENTRY the question does not arise, because the entry LIMIT carries no trigger. It applies to the SL exit leg placed after the fill.

1. **How the separation is constructed:**
   - `LimitTripleProtocol.place_exits` (374-391): `sl_order_type = "SL"`; `sl_limit_price = calc_sl_limit_price(exit_side=exit_side, trigger_price=sl_price, offset_pct=self._sl_limit_offset_pct)`; `place_order(… price=sl_limit_price, order_type="SL", … trigger_price=sl_price)`.
   - `calc_sl_limit_price`: SELL `trigger_price * (1.0 - offset_pct)` rounded down; BUY `trigger_price * (1.0 + offset_pct)` rounded up. `sl_limit_offset_pct` 0.005.
   - The adapter SL snap rounds the limit directionally and the trigger to nearest. Its docstring says "Trigger rounds to nearest (offset >> tick, so limit stays past trigger)". That is an assertion, not a check.
2. **What `_validate_place_order` checks:** only `price <= 0` and `trigger_price <= 0`. No price-vs-trigger comparison and no trigger-vs-LTP comparison.
3. **Measured probe** of the as-written sequence over triggers 1.000-200.000 in 0.001 steps, both sides:
   - tick 0.05: limit never crossed the trigger; limit == trigger in 1,600 cases (760 SELL, 840 BUY), all at triggers <= 4.975.
   - tick 0.01: 0 equal, 0 crossed.
4. **Broker trigger-vs-LTP rule:** not pre-validated. It is handled reactively by `OrderPlacer._is_ltp_validation_error` (3344-3357): True on `kite_status_code 16418` or on the message keywords `["trigger price", "ltp cannot be validated"]`. The exit then goes to the FIX-061 LTP retry queue.
5. **Modify paths** (`breakeven_manager`, `structure_exit_manager`, `smart_tgt_manager`): no separation validation.
6. **The only trigger pre-validation in code** is for CNC OCO GTTs: `CncGttPlacer._validate_trigger_distance` (`cnc_gtt.py` 250-262). It checks trigger vs LTP, **not** trigger vs limit:
   - `if not (sl_trigger < ltp < tgt_trigger): raise BrokerError(…)`
   - a minimum distance of `_MIN_TRIGGER_DISTANCE_PCT = 0.0025`.

**NOT ESTABLISHED:** Kite's actual numeric trigger-vs-limit rule, if any. It is not stated in code or config; only comments reference broker rejects.

---

## 4. GROUP D — TIMING AND WINDOWS

### D1 — After a signal qualifies, does the system order immediately, or wait?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — logic (WT-only per-pipeline window check before screening; not deployed) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer: it orders immediately.** Nothing on the active path deliberately waits between a signal passing screening and broker submission. The elapsed time is processing and I/O only.

**Steps between qualification and submission, in order:**
1. Queue hop to a worker
2. Screener quote fetch
3. M-S1 fresh-LTP quote (for `pullback_wait_enabled: false` strategies)
4. Sizing
5. Reserve, inside `portfolio_lock`
6. `EntryThrottle.admit`
7. Live-only FIX-128 and FIX-075 quote fetches in `OrderPlacer.place`
8. Adapter rate-limiter `acquire`
9. `kite.place_order`

**The only blocking step is step 8.** The rate-limiter `acquire` sleeps up to `max_wait_sec` (ctor default 30 s), then raises.

**Things that reject or re-queue, but never hold a signal:**
- `EntryThrottle` **rejects**: min-gap < 20 s, a burst of ≥ 3 per 60 s, or the same symbol within 300 s. Rejected signals get status `REJECTED_ENTRY_THROTTLED`; 212 rows since 01-Sep on the VM.
- A signal is **re-queued** when the order token bucket is empty.

**No sleeps before submission.** The only `time.sleep` calls in these files are in paper `_synth_fill`, which runs after submission.

**The 6 `pullback_wait_enabled: true` strategies do NOT wait either.** The flag's only entry-path effect is to skip the M-S1 re-anchor. `EntryGate.add` has no caller.

**Measured on TW-DB** (116 LIVE ENTRY orders, `placed_at >= 2026-09-01`):

| Interval | min | p50 | p90 | max |
|---|---|---|---|---|
| `placed_at − received_at` | 0.75 s | 4.38 s | 11.88 s | 18.52 s |
| `placed_at − triggered_at` | 7.48 s | 17.38 s | — | 35.23 s |
| `trades.signal_to_order_ms` (n=48 populated) | — | 2731 ms | — | 12083 ms |

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `signals/signal_processor.py` | 1111-1129 | `_process_one` | `# Momentum strategies (pullback_wait_enabled=false) place immediately; … Pullback strategies skip this (EntryGate already waits for current price). … if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:` |
| TW=WT | `signals/entry_throttle.py` | 78-107 | `EntryThrottle.admit` | `if gap < self._min_gap: … return ThrottleResult(False, …)` … `if len(self._recent) >= self._burst_max:` … `if elapsed < self._per_symbol:` |
| TW=WT | `broker/rate_limiter.py` | 152, 177-246 | `TokenBucketRateLimiter.acquire` | `max_wait_sec: float = 30.0` … `deadline = start + self._max_wait_sec` … `time.sleep(sleep_for)` |

**Paper↔live:** neither mode has a deliberate wait. Paper branches before the live rate-limiter acquire and skips the FIX-128/FIX-075 quote fetches.

---

### D2 — If it waits, for what — a 5-minute candle, a 1-minute candle, a tick condition, a fixed delay, or something else?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Answer:** on the active entry path there is **no wait** — no 5-minute candle, no 1-minute candle, no tick condition and no fixed delay before submission. The active screener uses no intraday candle. It builds `ltp`, `bid`, `ask`, `volume`, `vwap`, `open`, `day_high` and `day_low` from one Kite quote.

**Four wait mechanisms exist in code; none is active on the order path:**

| # | Mechanism | What it waits for | Why it is not active |
|---|---|---|---|
| (a) | EntryGate (`screening/entry_gate.py`) | LTP tick condition `lower <= ltp <= upper`, polled; hard timeout `pullback_wait_timeout_sec` 180, compared with `elapsed_sec >= entry.timeout_sec` | **DORMANT**: `EntryGate.add` has no caller; `gate_state` 0 rows |
| (b) | SNR-V2 RetestMonitor | 1-minute candles, poll 20 s, `confirm_strong_close_frac 0.6`, `retest_timeout_sec 1800` | **DORMANT**: `wait_for_retest_enabled: false`; `retest_state` 0 rows |
| (c) | PB-01 watchlist entry stage | 5-minute bars, window 09:20-11:00, poll 20 s | **ANALYSIS ONLY, no order path** (see G2) |
| (d) | After submission only | order monitor polls every 2 s; paper fill synthesizer waits for an LTP crossing | Not a pre-order wait |

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `screening/secondary_screener.py` | 401-439 | `_build_market_data` | `ltp = quote.last_price … "vwap": getattr(quote, "vwap", None), "open": getattr(quote, "open_price", None), "day_high": …, "day_low": …, "atr": None, "rsi": None` |
| TW=WT | `screening/entry_gate.py` | 15-16, 29 | module docstring | `EG5  -- Price trigger: lower <= ltp <= upper … EG6  -- Timeout: hard, per entry.timeout_sec. Default 180s. … Does not implement candle-based triggers (LTP only per P11a)` |

---

### D3 — The 10-minute timeout: exact duration, what starts it, what it does on expiry.
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS — LOGIC** (WT: per-pipeline expiry — MIS 600 s, CNC none; TW: 600 s for every signal) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER (cancel mechanics)

**Answer:** on the deployed entry path there is exactly **one** 10-minute clock: the **signal-age limit** `signal_queue.expiry_sec: 600` (TW config 127, comment `WR6: 10 min`). **It is not an order timeout.**

**Duration:** 600 s. It is passed to `SignalProcessor` as `signal_expiry_sec` (TW `main.py` 3614), overriding the ctor default of 60. The webhook reads `sq_cfg.expiry_sec` directly (TW 679).

**What starts it:** Chartink `triggered_at`, not `received_at` and not `placed_at`.
- Time-only formats are built with seconds = 0 and IST attached.
- Measured: 46,070 of 46,070 signals since 01-Sep have zero seconds and a `+05:30` offset.

**Where it is checked, and what expiry does.** It is checked twice, both times as `age_sec > expiry_sec`:

| Check | Location | On expiry |
|---|---|---|
| (1) Webhook edge | `_process_signal` (TW 919-926) | Returns `{"status": "EXPIRED"}` for that symbol; **no signals row is inserted** |
| (2) Processing start | `_process_one` (TW 910-921), after the queue hop | Raises `_PipelineReject('EXPIRED')`; `signals.status = REJECTED_EXPIRED`; Telegram warning, at most one per 60 s |

**No age check runs after processing start.** A signal that passes there is not re-aged before or after submission.

`signals.expires_at = received_at + 600 s` is written (TW 960) but **read by no decision**. Measured: `expires_at − received_at = 600.0` on 5000/5000 sampled rows.

**Other clocks on the path — the entry-order timeout is 60 s, not 10 min:**
- **Entry-order fill timeout** `order_monitor.fill_timeout_sec: 60` (TW config 194).
  - Starts at `placed_at = now_ist()`, taken in `OrderPlacer.place` after broker ack and DB persist (`order_placer.py` 1575).
  - Evaluated on each 2 s poll while the Kite status is in {OPEN, TRIGGER PENDING, SUBMITTED}, as `if elapsed <= self._fill_timeout: return` (`order_monitor.py` 1097).
  - On expiry: `adapter.cancel_order`. Success → CANCELLED + untrack. Failure → FAILED + untrack + `on_orphan` (soft_kill + CRITICAL alert).
  - Measured, TW-LOG 03-15 Sep: 55 `fill_timeout`, each followed by `timeout_cancelled`; 0 `orphan_detected`.
- **Screener freshness** (step_10): age ≤ 30 s → 1.0; ≤ 60 s → 0.5; > 60 s → 0.0.
  - A 0.0 gives `REJECTED_SIGNAL_AGE`, applied after the score threshold. `v3_hardgate_mode "shadow"`.
  - Measured: 0 `REJECTED_SIGNAL_AGE` rows ever; screener `ts − triggered_at` max 55.3 s.
- **Partial fill:** an ENTRY leg is cancelled on the first PARTIAL poll. `partial_fill_timeout_minutes: 5` applies only to non-ENTRY/SL/TGT/EOD legs.
- **FIX-141** pending-R:R cancel, evaluated on each OPEN poll.
- **Force close at 15:15:** cancels tracked ENTRY legs, once per day.
- **`eod_entry_cutoff` 15:15:** rejects placement when `now.time() >= cutoff`.
- **`pipeline_timeout_sec: 30`** is config-validated but has **no consumer** in either tree.
- The only other "10 min" is a hard-coded Telegram string: `f"Smart TGT: enabled | Timeout: 10 min"` (TW `signal_processor.py` 543 / WT 557). No clock is behind it.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `config/system_config.yaml` | 127 | — | `expiry_sec: 600             # WR6: 10 min - Chartink triggered_at is scan time, not delivery time` |
| TW | `signals/webhook_receiver.py` | 925 | `_process_signal` | `if age_sec > expiry_sec:` |
| TW | `signals/signal_processor.py` | 917 | `_process_one` | `if age_sec > self._signal_expiry_sec:` |
| TW | `config/system_config.yaml` | 193-194 | — | `poll_interval_sec: 2        # poll broker every 2s for fill updates (>= 1)` / `fill_timeout_sec: 60        # cancel unfilled OPEN/SUBMITTED order after 60s (>= 5)` |
| TW=WT | `broker/order_monitor.py` | 1087-1098 | `_check_fill_timeout` | `if entry.leg in ("SL", "TGT", "EOD"): return` … `elapsed = max(0.0, elapsed_raw)` … `if elapsed <= self._fill_timeout: return` |
| TW-LOG | `logs/system_2026-09-15.log` | 10:12:12.317 | order_monitor | `"order_monitor.fill_timeout" … "elapsed_sec":61.0` → `"order_monitor.timeout_cancelled"` |

**WT difference (not deployed):**
- The WT webhook uses `edge_expiry_provider`. With `delivery_expiry_sec: null` it returns None, and the edge then applies **no** age limit (`if expiry_sec is not None and age_sec > expiry_sec`, WT 911).
- `expires_at` becomes 23:59:59.
- The authoritative WT check is per pipeline: MIS 600 s, CNC none (WT 1018).

**Paper↔live:** the signal expiry and screener freshness are mode-independent. The fill-timeout code is the same in both modes, but paper `cancel_order` always returns `success=True`.

---

### D4 — Is the confirmation wait INSIDE the 10-minute timeout or in addition to it? Give the total elapsed time from alert to cancellation.
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS — LOGIC** (signal-age clock, see D3) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer: no confirmation wait exists on the active path** (D1, D2). So it is neither inside nor in addition to the 10-minute clock.

**The two clocks are sequential and do not overlap:**
1. **600 s signal-age clock.** Starts at `triggered_at` (minute floor). Checked with `>` at receipt and once at processing start. It then never runs again and never cancels an order.
2. **60 s fill-timeout clock.** Starts at `placed_at` after broker ack. Fires on the first 2 s poll where elapsed > 60, and only while the Kite status is OPEN / TRIGGER PENDING / SUBMITTED.

The screener's 60 s freshness reject is a third clock, measured from `triggered_at`, and sits between the two.

**Total alert-to-cancellation, as a code bound:**
- (a) `triggered_at` → processing start: ≤ 600 s by the processor check. In practice tighter, because of the 60 s screener freshness reject on a passing score.
- (b) processing → broker ack: no timing gate, only `eod_entry_cutoff`.
- (c) > 60 s, plus up to one 2 s poll, plus `get_order_history` and cancel latency.
- Kite-side delay before the order shows as OPEN is **not bounded by code**.

**Measured on TW-DB — 68 LIVE ENTRY orders CANCELLED since 01-Sep:**

| Interval | min | p50 | p90 | max |
|---|---|---|---|---|
| `updated_at − placed_at` | 1.46 s | 61.19 s | 62.59 s | 66.09 s |
| `updated_at − triggered_at` (alert to cancellation) | 9.81 s | 79.6 s | 87.06 s | 94.58 s |

- Example trd_c431b94a: triggered 10:01:00, received 10:01:13.89, placed 10:01:16.29, cancelled 10:02:17.32.
- Cancels under 60 s come from other paths, e.g. FIX-141 pending-R:R.
- For comparison, 48 COMPLETE ENTRY orders filled at `filled_at − placed_at` p50 5.96 s, max 58.34 s.
- `updated_at` is the monitor's detection time, not the exchange cancel time.

---

### D5 — Can an order survive past its window? Under what circumstances?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only for the order clock (WT adds a per-pipeline window) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer: yes.** Code shows these circumstances.

**A. Past the signal / entry window, at placement**
1. The entry window is checked on receive time at the webhook (`entry_start <= t < entry_end`) and again once at processing start. The age check also runs once there. **Nothing re-checks window or age after that.** So a signal passing at 14:59:59.9 can be submitted after 15:00, and one aged 599 s can be submitted older than 600 s. The only later time gate is `eod_entry_cutoff` (`now.time() >= 15:15` rejects in `OrderPlacer.place`).
2. Once placed, an ENTRY order stays open for up to 60 s plus poll lag, so it can outlive 15:00.
   Measured: the last accepted signal each day was received 14:59:07-14:59:19; `placed_at − received_at` max 18.52 s.

**B. Past the 60 s fill timeout**
3. **Status outside the timeout set.** The timeout is evaluated only when the polled Kite status is in {"OPEN", "TRIGGER PENDING", "SUBMITTED"}. Any other status is logged `order_monitor.unknown_status` with no timeout evaluation that cycle. Measured TW-LOG 03-15 Sep: **4** such lines — `OPEN PENDING` ×1 (07-Sep 15:17:05) and `CANCEL PENDING` ×3 (08-Sep 12:18:38; 15-Sep ×2, one at 10:21:05). See §9 for the reconciled count.
4. **Broker timeout on the poll.** `get_order_history` raising `BrokerTimeoutError` skips the order for that cycle. Auth and general API errors also return early.
5. **Monitor stop.** After 3 consecutive auth errors, or `max_api_failures` (3) API errors, the monitor sets `_stop_event`. Polling ends for **every** tracked order, and `on_critical` fires.
6. **Failed cancel.** `cancel_order` returns `success=False` → marked FAILED locally and untracked → `on_orphan` (soft_kill + CRITICAL). The broker order may still be live, and nothing re-polls it.
7. **Unconfirmed cancel.** `cancel_order` `success=True` is taken from the broker response. The row is set CANCELLED and untracked with no confirmation that the cancel took effect.
8. **Never tracked.** An order that is never tracked has no fill-timeout clock. Examples: a `place()` `BrokerTimeoutError` leaves the trade `UNKNOWN_IN_FLIGHT` in `_timeout_recovery_queue` with no broker id; or the track() failure rollback path.
9. **Restart.** `rehydrate_from_store` re-tracks orders with status IN ('PENDING','SUBMITTED','OPEN','PARTIAL','TRIGGER_PENDING'). If `placed_at` fails to parse, `placed_at = now_ist()` and the 60 s clock restarts. Measured: all 116 ENTRY `placed_at` since 01-Sep parse as `+05:30`.
10. **Partial fill.** The remainder is cancelled on the first PARTIAL poll. If that cancel fails, the orphan path fires.
11. **Force close at 15:15.** Cancels tracked ENTRY legs once per day. A cancel failure is logged `force_close_cancel_failed`.

**Measured occurrence, TW-LOG 03-15 Sep:**
- `fill_timeout` 55 · `timeout_cancelled` 55 · `orphan_detected` 0
- `partial_immediate_cancel` 0 · `rejected_past_eod_cutoff` 0
- `unknown_status` 4 · `order_monitor.force_close_triggered` 6 (§9)
- All 68 CANCELLED ENTRY orders since 01-Sep were marked within 66.09 s of `placed_at`.

**NOT ESTABLISHED:**
- Whether the kill-switch callbacks cancel broker orders once the monitor has stopped (kill_switch internals not read).
- Whether Kite itself expires a DAY LIMIT order at session end.
- Whether any CANCELLED-marked order later filled at the broker (broker order book not queried).

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 85, 655-662, 770-791 | `_process_order` | `_KITE_STATUS_OPEN = {"OPEN", "TRIGGER PENDING", "SUBMITTED"}` … `except BrokerTimeoutError as exc: # OM11: skip this order this cycle, retry next` … `self._log.warning("order_monitor.unknown_status", …)` |
| TW=WT | `broker/order_monitor.py` | 1107-1126 | `_check_fill_timeout` | `result = self._adapter.cancel_order(entry.broker_order_id)` / `if result.success: … "CANCELLED" … self.untrack(…)` / `else: … "order_monitor.orphan_detected" … "FAILED" … self._on_orphan(…)` |
| TW=WT | `broker/order_monitor.py` | 452-456 | `rehydrate_from_store` | `placed_at = datetime.fromisoformat(placed_at_str)` / `except Exception: placed_at = now_ist()` |
| TW | `core/market_windows.py` | 150, 188-190 | `is_entry_allowed` / `is_past_eod_entry_cutoff` | `return self.entry_start <= t < self.entry_end` … `return now.time() >= self.eod_entry_cutoff_t` |

**Paper↔live:** paper `cancel_order` always returns `success=True`, so (6) cannot occur in paper. Paper order history is local. A paper order cancelled locally cannot later fill, because the OSM refuses the COMPLETE transition.

---

### D6 — What happens to an event landing exactly on a window boundary?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (operators identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

| # | Boundary | Operator as written | Exactly on the boundary |
|---|---|---|---|
| 1 | Global entry window (webhook + processing start) | `self.entry_start <= t < self.entry_end` (10:00/15:00), on `now_ist()` not `triggered_at` | 10:00:00.000 **ADMITTED**; 15:00:00.000 **REJECTED** (HTTP 403 / `REJECTED_OUTSIDE_ENTRY_WINDOW`) |
| 2 | Per-strategy window | `time(sh, sm) <= t < time(eh, em)` | start inclusive, end exclusive; a malformed window returns True |
| 3 | EOD entry cutoff | `now.time() >= self.eod_entry_cutoff_t` (15:15) | 15:15:00 **REJECTED**; a holiday returns True |
| 4 | Signal age | `age_sec > expiry_sec` | exactly 600.0 s **PASSES**; 600.000001 s EXPIRED (age measured from the start of Chartink's minute) |
| 5 | Screener freshness | `age_sec <= 30` → 1.0; `age_sec <= 60` → 0.5; else 0.0 | exactly 30.0 → 1.0; exactly 60.0 → 0.5 (not rejected) |
| 6 | Fill timeout | `if elapsed <= self._fill_timeout: return` | exactly 60.0 s **NOT cancelled**; cancel needs > 60 s, and lands on the first 2 s poll after (measured `elapsed_sec` 61.0) |
| 7 | Partial-fill timeout (non-ENTRY legs) | `elapsed > self._partial_fill_timeout_sec` (300) | exactly 300 not cancelled |
| 8 | Force close | `if now.time() < self._force_close_time_t: return` | exactly 15:15:00 **FIRES**, once per IST date |
| 9 | Entry throttle | `gap < self._min_gap` / evict `< cutoff` / `len >= burst_max` / `elapsed < self._per_symbol` | exactly 20.0 s ADMITTED; an entry exactly `burst_window` old still counted; exactly 300.0 s ADMITTED |
| 10 | Webhook dedup cache | `TTLCache(ttl=300)`; cachetools 7.1.2 `__contains__` → `self.timer() < link.expires` | at exactly 300.0 s the key has EXPIRED, so the signal is not a duplicate |
| 11 | DB fingerprint bucket | `int(triggered_at.timestamp() // self._dedup_window_seconds)` | an event exactly on a 300 s epoch multiple starts the NEW bucket; buckets align to IST :00/:05 (19800 s is a multiple of 300) |
| 12 | FIX-130 SL gap buffer | `_GAP_WINDOW_START <= now_time <= _GAP_WINDOW_END` (09:15-09:30, both inclusive) | never runs under the 10:00 entry start |
| 13 | Time-only `triggered_at` | dated with the webhook's `now.date()` | an `HH:MM` alert is assigned the IST date at receipt |

**Measured `webhook_audit` on 10-Sep and 11-Sep** (the global window boundaries):
- 09:59 posts arrived 09:59:06-08 → 403.
- 10:00 posts arrived 10:00:07 → 200.
- 14:59 posts arrived 14:59:06-08 → 200.
- 15:00 posts arrived 15:00:07-10 → 403.

*INFERENCE:* an exact float boundary is practically unobservable with microsecond `now_ist()`. The operators above define the outcome if it does happen.

---

### D7 — Which timezone is used at each step? Any conversion that could move an event into an adjacent candle?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Answer: one clock source.** `core.time_authority.now_ist()` = `datetime.now(tz=timezone(timedelta(hours=5, minutes=30), name="IST"))`.
- It is a fixed `+05:30` offset on the system UTC clock, independent of the VM TZ setting.
- There is **no `astimezone()` or UTC conversion anywhere on the active entry path**.

**Datetime construction and handling on the path, step by step:**
1. **Webhook window check:** `now_ist()`, compared as `now.time()`.
2. **`triggered_at` parse:** `strptime`, with formats that have no `%z`. For time-only formats the date comes from `now.date()` and seconds are dropped. `.replace(tzinfo=ist_timezone())` then **attaches** IST (not a conversion), so whatever wall time Chartink sent is taken as IST.
3. **`received_at`:** `now_ist()`. `expires_at = received_at + 600 s`.
4. **Webhook age:** `now_ist() − triggered_at_aware`, both `+05:30`.
5. **Fingerprint:** `.timestamp() // 300`. This is the UTC epoch, but it aligns to IST 5-minute boundaries.
6. **Persisted timestamps:** `isoformat()` with `+05:30`. Measured: 46,070/46,070 signals since 01-Sep carry `+05:30` on both columns, and every `triggered_at` has seconds == 0.
7. **Processor:** `now_ist()`; `triggered_at.replace(tzinfo=ist_timezone())` does not shift an already-IST-aware value. The docstring "`triggered_at: naive datetime (IST)`" is stale relative to the actual tuple content.
8. **Strategy window / governor / `_derive_prices`:** use the same processing-start `now.time()`.
9. **`OrderPlacer` EOD cutoff, `placed_at` and `orders.placed_at`:** all `now_ist()`. Measured: 116/116 ENTRY `placed_at` carry `+05:30`.
10. **`order_monitor`:** `now_ist()` per poll. `filled_at = now_ist()` at detection, i.e. poll time, not exchange fill time.

**Candle shift:** the active path uses **no intraday candle** (D2), so no conversion can move an event into an adjacent candle. Code facts that bear on alignment:
- (a) `triggered_at` is floored to `:00`. Measured `received_at − triggered_at`: min 5.66 s, p50 13.67 s, max 43.41 s. Every age is therefore measured from the minute start.
- (b) A time-only `triggered_at` borrows the date at receipt.
- (c) In the dormant RetestMonitor, 1-minute candles are filtered with tzinfo **stripped, not converted** (`ts = c.ts.replace(tzinfo=None)`; `if ts >= since_naive`).

**NOT ESTABLISHED:** whether Kite candle timestamps are IST, and whether a candle timestamp marks the candle start. These are broker-API properties.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `core/time_authority.py` | 55-59, 94-104 | `now_ist` / `ist_timezone` | `_IST_OFFSET = timedelta(hours=5, minutes=30)` / `_IST = timezone(_IST_OFFSET, name="IST")` … `return datetime.now(tz=_IST)` |
| TW=WT | `screening/retest_monitor.py` | 216-225 | `_fetch_recent_1m` | `since_naive = since.replace(tzinfo=None)` … `ts = c.ts.replace(tzinfo=None) if c.ts.tzinfo else c.ts` / `if ts >= since_naive:` |

**Paper↔live:** all timestamps come from `now_ist()` in both modes. The fill instant differs: paper uses the synth-thread instant, live uses the poll-detection instant.

---

## 5. GROUP E — PRE-ENTRY CHECKS

### E1 — Does anything today check whether the planned STOP was touched before entry? If yes, quote it.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (cited logic identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER (the nearest check is live-only; neither mode has a stop-touched check)

**Answer: NO.** Nothing before submission compares a market price (LTP, quote, candle high or low) with the planned STOP to find out whether the stop traded between the Chartink alert and the order.

**Pre-submission gates read, in order, in both trees:**

1. **Screener** (`SecondaryScreener.screen` + 10 steps). It runs **before any SL exists**: the screen call is at WT 1049 / TW 998, while `_derive_prices` is later at WT 1079 / TW 1028.
   - Its only price-vs-limit rule is `circuit_proximity_reason`. That rule compares the **Chartink trigger** with the circuit band, not with an SL.
2. **`_derive_prices`** computes the SL from geometry only: `sl_price = entry_price * (1.0 - sl_pct)` (WT 1832).
   - The M-S1 block fetches `live_ltp` and **overwrites** the SL. It never compares `live_ltp` with the SL it replaces.
3. **PositionSizer PS10** compares the direction of SL vs entry only, and only logs a WARNING.
4. **R:R gate** (`order_placer.py` 937-955): entry/SL/TGT geometry only.
5. **FIX-128 slippage guard** (1103-1195). This is the **only** pre-submission check that uses both a current LTP and `sl_price`, and it is **not a stop-touched test**.
   - It measures `abs(LTP − Chartink trigger)` against a fraction of the trigger-to-SL distance.
   - It has no direction: a move toward the target aborts the same way.
6. **FIX-075 drift** compares LTP with entry only. It may set `entry_price = current_ltp` without recomputing the SL.
7. **`_check_liquidity`** is a no-op.
8. **`LimitTripleProtocol.execute`** sends the entry only. Its docstring says "`sl_price` … accepted here for signature symmetry … but are NOT used".

**After submission,** nothing checks the stop side either. The only pending-entry price check (FIX-141, E2) looks at the target side. For a LONG, an LTP falling toward or through the SL raises `remaining_reward` and never cancels.

**SL checks that happen only after the entry fill:**
- `clamp_exit_into_band` (SL vs fill).
- `cnc_gtt._validate_trigger_distance` (`if not (sl_trigger < ltp < tgt_trigger)`), at DELIVERY GTT placement.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `signals/signal_processor.py` | 1049, 1079-1081 | `_process_one` | `screen_result = self._screener.screen(…)` … `entry_price, sl_price = self._derive_prices(trigger_price, strategy_obj, now_time=now.time())` |
| TW=WT | `screening/hard_gate.py` | 53-111 | `circuit_proximity_reason` | `entry = _pos_num(trigger_price)` … `if lower_floor is not None and entry <= lower_floor: return (f"LONG entry {entry} <= lower-floor {lower_floor:.2f} " … "no valid SL fits the band")` |
| TW=WT | `orders/order_placer.py` | 1103-1111 | `OrderPlacer.place` | `_slip_rs = abs(_slip_ltp - signal_trigger_price)` |
| TW=WT | `orders/order_protocol_limit.py` | 193-196 | `execute` | `sl_price and tgt_price are accepted here for signature symmetry with CoPlusTgtProtocol but are NOT used` |

**Search width:**
- End-to-end read of the screener, the 10 steps, `hard_gate`, `_process_one` through sizing, `_derive_prices`, `_derive_target`, PS10, `OrderPlacer.place` 871-1360 and the protocol `execute`, in both trees.
- Regex grep for `(sl|stop|target|tgt)(already|touched|hit|breach|crossed|invalid)` and for `ltp|last_price|day_high|day_low` near `sl_price|tgt_price`.
- AST scan of every function in both trees for one line holding a comparison + a high/low token + a stop/target token. The only hit was `v3_chain/forward_shadow.py::simulate_true_path`, which is offline (E5).
- Independent re-check (§9): a comparison regex over 8 entry-path files in both trees → 0 hits.

---

### E2 — Does anything check whether the planned TARGET was touched before entry?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (`order_monitor.py` identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer**

**BEFORE SUBMISSION: NO.**
- No pre-submission gate compares LTP, quote or candle data with the planned target.
- `_derive_target` and the R:R gate are geometry only.
- The FIX-128 guard does abort on a large move toward the target, because it uses `abs(LTP − trigger)`. But its tolerance is referenced to the SL distance, not to the target.

**AFTER SUBMISSION, BEFORE FILL: YES, one check.** It is FIX-141 `order_monitor._check_price_movement_cancel` (`broker/order_monitor.py` 1128-1207, identical in both trees).
- It runs from `_handle_open` on every poll while the ENTRY's broker status is OPEN / TRIGGER PENDING / SUBMITTED.
- It tests how close price is to the target. It cancels once remaining reward falls below `min_pending_rr` × risk.
- By the formula, an LTP at or beyond the target gives `remaining_reward <= 0`, which cancels.

**Wiring:** `min_pending_rr=app_config.system.entry_gate.min_pending_rr` (`main.py` WT 2770 / TW 3011); config `min_pending_rr: 1.0` (WT 679 / TW 654).

**Measured TW-LOG:** cancel events on 03-Sep 2, 04-Sep 1, 07-Sep 1, 10-Sep 2, 11-Sep 2; 0 on 08, 09 and 15 Sep. Example:
```
2026-09-03T10:07:57.291  order_monitor.pending_rr_cancel PENDING_RR_BELOW_THRESHOLD
HIKAL  entry_price 224.78499  ltp 225.82  pending_rr 0.924  sl_price 222.98671008  tgt_price 227.48240987999998
```

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 1128-1207 | `_check_price_movement_cancel` | `if self._min_pending_rr <= 0: return` … `if entry.leg != "ENTRY": return` … `ltp = self._ltp_expected_fallback(entry.symbol)` … `if entry.side == "BUY": remaining_reward = entry.tgt_price - ltp` … `pending_rr = remaining_reward / risk_distance` … `if pending_rr >= self._min_pending_rr: return` … `result = self._adapter.cancel_order(entry.broker_order_id)` |
| TW=WT | `broker/order_monitor.py` | 877-881 | `_handle_open` | `self._check_fill_timeout(entry, now)` / `self._check_price_movement_cancel(entry)` |
| TW | `config/system_config.yaml` | 654 | — | `min_pending_rr: 1.0         # FIX-141: cancel pending entry if remaining R:R drops below this (0=disabled)` |

**Paper↔live:** the FIX-141 code runs in both modes. Paper unfilled orders report `SUBMITTED`. The LTP source is live `kite.quote` vs the paper provider's Kite quote behind a 3 s TTL cache.

---

### E3 — If either exists, does it use the close only, or the full high/low path?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer: NEITHER.** Both price checks near the planned levels use **one last-traded-price sample** from a REST quote, taken at the moment of the check. They use no candle close and no high/low path. What happens between samples is never looked at.

- **(a) FIX-128 slippage guard** (pre-submission):
  - `_slip_ltp = self._fetch_ltp(symbol)`.
  - `_fetch_ltp` (4036-4064) does `raw_quote = self._adapter.get_quote_raw([f"NSE:{symbol}"])` … `ltp = float(q.get("last_price", 0) or 0)`.
  - Evaluated once. Skipped in paper.
- **(b) FIX-141 pending-entry cancel** (post-submission, pre-fill):
  - `ltp = self._ltp_expected_fallback(entry.symbol)`.
  - The helper (`order_monitor.py` 316-338) does `quotes = self._adapter.get_quote([symbol])` … `last_price = float(getattr(quote, "last_price", 0.0) or 0.0)`.
  - Re-sampled on each 2 s poll.

The quote also carries session-to-date `day_high` / `day_low`, but neither check reads them. On the entry path those fields are read only by the screener's `_step_5_price_action` body% score.

---

### E4 — What market-data resolution is available to the decision engine at that moment — ticks, 1-minute OHLC, 5-minute OHLC?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (wiring and flags identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer: none of the three reaches the live entry decision.** The entry path has only **REST quote snapshots** (`kite.quote`).

**What a snapshot holds:**
- `last_price`
- top-of-book bid/ask
- cumulative volume
- `vwap` (from `average_price`)
- `open` / `day_high` / `day_low` from the quote's `ohlc` dict. These are session-to-date values, not a bar.
- upper/lower circuit
- `atr`, `rsi`, `sector`, `prev_close` and `avg_volume_20d` are hard-set to `None` in `_build_market_data`.

**Measured** TW-DB `screener_results.market_data_snapshot`, 2026-09-15T10:00:08:
- `ltp 605.0`, `bid 605.0`, `ask 605.1`, `vwap 599.42`
- `open 569.6`, `day_high 614.65`, `day_low 567.85`
- `atr` / `rsi` / `avg_volume_20d` None

That is a 45-minute session range.

**Snapshot call points on the entry path:**
1. Screener `self._quote_fn([symbol])`
2. M-S1 re-anchor `self._quote_fn([symbol])`
3. `OrderPlacer._fetch_ltp` → `get_quote_raw` (live only)
4. After submission, `OrderMonitor._ltp_expected_fallback` on each 2 s poll

**Ticks:**
- `LiveFeedManager` (KiteTicker, `MODE_LTP`) is constructed and connected in live.
- The only caller of `live_feed.subscribe` in either tree is OrderPlacer's **exit-retry** path (`order_placer.py` 3404).
- TW-LOG 03-15 Sep: "connected to KiteTicker" every day; `LiveFeedManager: subscribed batch` 0; `exit_retry_subscribed_to_ltp` 0.

**1-minute OHLC:**
- `CandleStore(candle_interval_sec=60)` builds bars from ticks. Its only reader is post-fill CO trailing.
- The `analytics.db` `candles` table (interval 60 only; 1,728,381 rows; 2026-06-19..2026-09-11; 0 rows for 2026-09-15) is written by the EOD cron and read only by offline jobs.

**5-minute and other OHLC:**
- `kite.historical_data` is reached via `_make_sr_fetch_fn`. None of its consumers feeds the live entry decision:
  - `sr_detector` V1 is a post-placement observer.
  - `v3_chain` runs in `"shadow"` (log-only).
  - PB-01 watchlist is analysis-only.
  - RetestMonitor is not built (flags false).
  - `regime` is disabled.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `broker/zerodha_adapter.py` | 1694-1731 | `get_quote` | `raw = self._kite.quote(*instrument_keys)` … `ohlc = data.get("ohlc", {})` … `day_high=float(ohlc["high"]) if ohlc.get("high") else None,` |
| WT | `screening/secondary_screener.py` | 401-439 | `_build_market_data` | `"day_high": getattr(quote, "day_high", None), "day_low": getattr(quote, "day_low", None),` … `"atr": None, "rsi": None, "sector": None, "prev_close": None, "avg_volume_20d": None,` |
| WT | `data/live_feed.py` | 172-191 | `subscribe` | `# … (only latent caller: order_placer exit-retry — IA-P1-06)` … `self._ticker.set_mode(KiteTicker.MODE_LTP, batch)` |

**Paper↔live:**
- **Live:** `kite.quote` on every call; KiteTicker connects but has no subscriptions.
- **Paper:** the Kite quote comes via a 3 s TTL cache; `get_quote_raw` returns `{}`; `live_feed.connect` returns early.
- In **neither** mode does 1-minute or 5-minute OHLC reach the entry decision.

---

### E5 — If only 1-minute OHLC is available, the engine cannot know the order of events inside a bar. Does any existing code assume an intrabar sequence it cannot establish?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (cited functions identical) · **Uncommitted in WT:** NO · **Paper↔live:** IDENTICAL

**Answer: YES, in OFFLINE research code only.** Nothing on the live entry path makes this assumption, because no OHLC bar reaches the entry decision (E4).

**Found (offline):**

**(1) `v3_chain/forward_shadow.py` `simulate_true_path` (lines 75-105, identical in both trees).** It explicitly assumes an intrabar order.
- Docstring: *"Walk the true 1-min path from entry to session end, HONOURING candle ordering (conservative: the adverse extreme is assumed hit before the favourable within a candle)."*
- The loop checks the SL before the TGT on every bar:
  - LONG: `if l <= sl: return -1.0` then `if h >= tg: return tgt_r`.
  - SHORT: the mirror.
- So a bar whose range holds both SL and target is always scored −1R.
- A unit test pins this: `tests/unit/test_forward_shadow.py:73` `assert simulate_true_path(100.0, "LONG", [(102.0, 98.9, 99.0)]) == -1.0`.
- Its only caller is `scripts/forward_shadow_record.py`, run from the VM crontab `15 18 * * 1-5`, long after the session. Output: `data_store/v3/forward_shadow_fs-v1.jsonl`.

**(2) The same caller assumes where the entry sits inside a bar.**
- `en = str(r["triggered_at"])[11:16]`; `path = [(c["high"], c["low"], c["close"]) for c in cand if str(c["ts"])[11:16] >= en]`; entry = `m.get("ltp") or r["trigger_price"]`.
- The bar labelled with the trigger minute is included whole. Its high and low are therefore treated as reachable after entry, although part of that minute traded before the alert.
- *INFERENCE layered on MEASURED data:* candle ts labels on the VM run 09:15:00..15:29:00, which fits bar-start labels.

**Related, but not an ordering assumption (offline):** `core/state_store.py` `compute_trade_excursions` (cron 15:50).
- It uses order-free extremes `max(highs)` / `min(lows)` over bars with `entry_dt <= cdt <= exit_dt`.
- With bar-start labels, this includes the whole exit-minute bar and leaves out the whole entry-minute bar.

**Examined; no unknowable intrabar order is resolved:**
- `sr_detector/retest_confirm.evaluate` (dormant): close-based; one state transition per bar.
- `v3_chain/pb01_entry._evaluate` (would-be only): invalidation precedes confirmation; both are close-based.
- `hard_gate.gate_confirm` / `gate_pullback`: single-bar or aggregate predicates.
- `breakeven_manager` (not constructed in `main.py`) and `smart_tgt_manager` (CandleStore gets no ticks): post-fill.
- `structure_exit_manager`: disabled.
- Tick/LTP single-price monitors, including paper `_gtt_triggered_leg`, which is SL-first on one LTP.

**Doc evidence (EVIDENCE):** `docs/audit/pb01_simulation_feasibility_2026-07-24.md:39` says the walker is "hardwired **adverse-first**".

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `v3_chain/forward_shadow.py` | 75-105 | `simulate_true_path` | `for h, l, _cl in candles: if long: if l <= sl: return -1.0 / if h >= tg: return tgt_r / else: if h >= sl: return -1.0 / if l <= tg: return tgt_r` |
| WT | `scripts/forward_shadow_record.py` | 214, 222-224 | `main` | `entry = m.get("ltp") or r["trigger_price"]` … `en = str(r["triggered_at"])[11:16]` / `path = [(c["high"], c["low"], c["close"]) for c in cand if str(c["ts"])[11:16] >= en]` (TW 222, 230-232) |
| TW-LIVE | crontab -l | 85 | cron | `15 18 * * 1-5 … scripts/forward_shadow_record.py >> logs/cron-forward-shadow.log 2>&1` |

---

## 6. GROUP F — FILLS

### F1 — Is the actual broker fill price captured in a field separate from the intended order price? Give both field names.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (cited logic identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer: YES, in two tables.** The `orders` table has columns for both, but fills neither for ENTRY orders.

**Intended-price fields**

| Field | Written by | When it is written |
|---|---|---|
| `trades.entry_target_price` (schema `-- the LIMIT price we want`) | `create_trade` (`entry_target_price=entry_price`, `order_placer.py:1003`) | Before the FIX-075 drift override and before the tick snap |
| `order_execution_log.intended_price` = `OrderFilled.expected_price` | `order_monitor.track(expected_price=entry_price)` (`order_placer.py:1615`) | After any drift override, before the tick snap |

**Actual-price fields**

| Field | Written by |
|---|---|
| `trades.entry_actual_price` (schema `-- actual fill price (may differ)`) | `OrderManager.record_entry_fill` from `OrderFilled.avg_fill_price` |
| `order_execution_log.actual_price` = `ev.avg_fill_price` | `SlippageRecorder._on_order_filled` |

**Where the actual value comes from (live)**
1. `OrderMonitor` polls `get_order_history` every 2 s.
2. The adapter sets `avg_price=float(row.get("average_price", 0.0))`.
3. `_process_order` takes `history[-1]`.
4. `_handle_complete` sets `final_price = avg_price if avg_price > 0 else entry.expected_price`.

So if Kite reports a falsy `average_price` on COMPLETE, the "actual" field silently holds the intended price.

**Not captured**
- `orders.price` stays NULL for ENTRY rows. `_persist_entry_orders` passes no price, and the `OrderInsertSpec` default is `0.0`, stored as NULL.
- `orders.avg_fill_price` and `orders.qty_filled` are never filled. `_handle_complete` never assigns `entry.avg_fill_price` or `entry.filled_qty`.

**Population on TW-DB** (all trades mode LIVE)
- **`trades`:** 368/368 rows with `qty_filled > 0` have `entry_actual_price` non-NULL and > 0. 349 of those 368 differ from `entry_target_price`.
- **`orders`:** 0/1452 have `avg_fill_price`; 0/1452 have `qty_filled > 0`. ENTRY `COUNT(price)` = 0/773.
- **`order_execution_log` ENTRY:** 475 rows, all with `intended_price` and `actual_price` set.
  - Only 213 have a `parent_trade_id`. The 262 NULL rows are July and earlier.
  - For trades created since 2026-09-03: 41/41 filled trades have an OEL row. `actual_price` equals `trades.entry_actual_price` in all 41. `intended_price` differs from `entry_target_price` in 1 (QUICKHEAL drift).
- **Example** ARVSMART 2026-09-15: entry_target 559.1586, intended 559.1586, actual 559.15.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| WT | `core/schema.sql` | 130-131, 349, 366, 1078-1079 | DDL | `entry_target_price  REAL NOT NULL,               -- the LIMIT price we want` · `entry_actual_price  REAL,                        -- actual fill price (may differ)` · `price REAL, -- LIMIT price; null for MARKET` · `avg_fill_price REAL,` · `intended_price REAL, -- expected/planned price` · `actual_price REAL, -- avg fill price` |
| TW=WT | `broker/order_monitor.py` | 762-765, 989-1012 | `_process_order` / `_handle_complete` | `latest = history[-1]` … `final_price = avg_price if avg_price > 0 else entry.expected_price` … `OrderFilled(… avg_fill_price=final_price, expected_price=entry.expected_price, …)` |
| WT | `orders/order_manager.py` | 409-436 | `record_entry_fill` | `UPDATE trades SET status = 'OPEN', entry_actual_price = ?, entry_time = ?, qty_filled = ?, updated_at = ? WHERE trade_id = ?` (TW 393-420) |
| WT | `orders/slippage_recorder.py` | 117-150 | `_on_order_filled` | `intended = ev.expected_price or None` / `actual = ev.avg_fill_price or None` … `"intended_price": intended, "actual_price": actual,` |

**NOT ESTABLISHED**
- No DB column holds the exact tick-snapped submitted price.
- Whether any of the 368 "actual" values came from the `expected_price` fallback cannot be told from the DB.

**Paper↔live**
- **Live:** Kite `average_price` via `OrderMonitor`.
- **Paper:** `_synth_fill` computes the fill (LTP-gated, then `SlippageEngine`) and publishes `OrderFilled` itself with `expected_price=price`.
- Both modes write the same DB fields.

---

### F2 — Is average fill price recorded for multi-fill orders?
**Status:** PARTIAL · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer.** The system records **one** average per entry order: the broker-reported `average_price`. It never aggregates individual fills itself, and never reads the per-fill trade book on the entry path.

**Full COMPLETE**
- `history[-1].avg_price` (Kite `average_price`) becomes `OrderFilled.avg_fill_price`, falling back to `expected_price` if falsy.
- That value lands in `trades.entry_actual_price` and `order_execution_log.actual_price`.

**Partial-then-cancel**
- `_handle_partial` stores `entry.avg_fill_price = avg_price` only when `filled_qty > entry.filled_qty`, on the poll that first sees PARTIAL.
- The immediate cancel then publishes `OrderPartiallyTerminated` with that stored value.
- History is not re-read after the cancel. Fills that land between that poll and the cancel taking effect are not reflected.

**Per-fill data**
- `adapter.get_trades()` has only two callers, both for exit-price resolution: `order_reconciler._resolve_exit_price` and `cnc_gtt_monitor`.
- No per-fill table exists.

**NOT ESTABLISHED**
- Whether Kite's order-level `average_price` is a quantity-weighted average across multiple fills. This is external API semantics.
- How many exchange fills any order had. Nothing in the DB shows it.

**Data (TW-DB and TW-LOG)**
- 152 of 368 filled trades had `qty_planned > 1` (max 6).
- `order_execution_log.is_partial = 0` on all 635 rows.
- 0 trades have `0 < qty_filled < qty_planned`.
- TW-LOG 03-15 Sep: `order_monitor.partial_fill` = 0.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 894-904 | `_handle_partial` | `if filled_qty > entry.filled_qty: entry.filled_qty = filled_qty / entry.avg_fill_price = avg_price` |
| WT | `broker/zerodha_adapter.py` | 1164-1172 | `get_order_history` | `filled_qty=int(row.get("filled_quantity", 0)), avg_price=float(row.get("average_price", 0.0)),` (TW 1203-1211) |

**Paper↔live**
- **Paper:** `_synth_fill` always fills the whole qty in one synthetic event, so it never produces a multi-fill.
- **Live:** whatever Kite reports.

---

### F3 — Partial fill lifecycle: what happens to the unfilled remainder?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (`order_monitor.py`, `order_placer.py` identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer.** In live code, the unfilled remainder of an ENTRY order is **cancelled at the broker on the first poll that sees PARTIAL**. It is never re-ordered.

**Sequence**
1. `_process_order` maps Kite status `PARTIAL` to `_handle_partial`. This updates filled qty/avg if the qty increased, stamps `partial_since`, and transitions the OSM to PARTIAL.
2. **FIX-130 (Item 16) Option A:** `if first_partial and entry.leg == "ENTRY":` → `self._adapter.cancel_order(entry.broker_order_id)`.
3. **Cancel succeeds.** `CancelResult success=True` means only that `kite.cancel_order` raised no exception; the broker effect is not verified. Then `_handle_terminal(entry, "CANCELLED")`:
   - publishes `OrderPartiallyTerminated(filled_qty, avg_fill_price, reason="CANCELLED")`;
   - moves the OSM to CANCELLED;
   - untracks the order.
4. **`OrderPlacer._on_order_partially_terminated`:**
   - `fm.commit_to_used(actual_qty=qty_filled)` returns the excess margin;
   - `record_entry_fill` sets the trade OPEN with `qty_filled`;
   - `_place_limit_triple_exits(qty_filled=…)` sizes SL/TGT to the filled qty;
   - Telegram: "… | unfilled portion cancelled".
5. **Cancel fails.** CRITICAL `partial_immediate_cancel_failed`, then `_fire_orphan` → `kill_switch.soft_kill` plus Telegram, and the order is untracked.
   - **No `OrderPartiallyTerminated` is published on this branch.** OrderPlacer therefore does not commit capital, record the fill or place exits through the fill handlers.
6. The non-ENTRY stuck-partial timeout (`partial_fill_timeout_minutes: 5`) skips ENTRY legs.
7. **Backstops** (read, not traced end to end):
   - reconciler `_check5_position_grew` only publishes `CapitalDriftDetected` ("manual intervention required");
   - in-flight recovery adopts a terminal order at its `filled_quantity`;
   - neither re-orders the remainder.

**Measured**
- TW-LOG 03-15 Sep: `partial_fill`, `partial_immediate_cancel`, `partial_terminated` and `partial_entry_terminated` are all 0.
- TW-DB: 0 partial trades; `is_partial=1` on 0 rows.
- **This branch has no production artifact in the data. It is NOT exercised.**

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 910-940 | `_handle_partial` | `# FIX-130 (Item 16) Option A: cancel ENTRY leg immediately on first PARTIAL.` / `if first_partial and entry.leg == "ENTRY":` … `result = self._adapter.cancel_order(entry.broker_order_id)` / `if result.success: … self._handle_terminal(entry, "CANCELLED")` / `else: … "order_monitor.partial_immediate_cancel_failed" … self._fire_orphan(entry)` / `return  # handled; skip timeout path below` |
| WT | `broker/zerodha_adapter.py` | 1019-1032 | `cancel_order` | `self._kite.cancel_order(variety=variety, order_id=broker_order_id,)` / `result = CancelResult(broker_order_id=broker_order_id, success=True, reason="")` / `except Exception as exc: … success=False,` |
| TW=WT | `orders/order_placer.py` | 1846-1907 | `_on_order_partially_terminated` | `self._fm.commit_to_used(reservation_id=…, actual_fill_price=avg_price, actual_qty=qty_filled,)` … `self._place_limit_triple_exits(… qty_filled=qty_filled …)` … `f"SL placed for {qty_filled} shares \| unfilled portion cancelled"` |

**Paper↔live**
- **Paper** never produces PARTIAL; `_synth_fill` fills the full qty.
- This lifecycle is reachable only in **live**.

---

### F4 — Is a fresh order ever created for a remainder?
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (TW has one extra exit-only `place_order` file) · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Answer: NO, in both trees.**
- No code path creates an ENTRY-side order for the unfilled remainder of a partially filled entry.
- Every partial path ends in **cancel + protect the filled qty** (F3).
- The `OrderMonitor` docstring says "Does not retry cancelled orders".

**Where an ENTRY-side order is submitted:** only `LimitTripleProtocol.execute` (and the unselected `CoPlusTgtProtocol.execute`), reached only via `OrderPlacer.place`. Neither partial handler calls `place()`.

**The only re-executions of an entry** are inside `OrderPlacer.place`'s loop. They use the **same `trade_id` and the FULL qty**, before any broker order exists:
- `BrokerRateLimit429Error`: up to `max_placer_retries` (default 3);
- a one-time retry when `kite_status_code == 16388` (see F5 for reachability).

Neither is a remainder order.

**Every other `place_order` site is an exit, flatten or SL-restore:**
- `_emergency_market_exit`
- reconciler flatten / emergency close / SL restore
- `kill_switch`
- `eod_squareoff`
- `sl_breach_monitor`
- `structure_exit_manager`
- TW-only `orders/mis_autosquareoff.py`

**TW-DB (all history)**
- 0 trades with more than one ENTRY row (773 ENTRY rows).
- 0 `signal_id`s with more than one trade.
- 0 partial trades.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 29-34 | module docstring | `What This Module Does NOT Do: … - Does not retry cancelled orders` |
| TW=WT | `orders/order_placer.py` | 1306-1319, 1344-1378 | `OrderPlacer.place` | `# BL-19: retry the engine only on BrokerRateLimit429Error. …` … `for attempt in range(max_429_retries + 1): … result = self._engine.execute(… trade_id=trade_id, …)` … `if kite_code == 16388 and not retried_16388:` |

**Search width**
- `grep -i 'remain\w*_qty|unfilled_qty|qty_remaining|remaining_qty|qty - filled|qty - qty_filled|pending_qty'` over `broker/ orders/ signals/ capital/ screening/ main.py`: 0 hits in each tree.
- Every `.place_order(` call site enumerated in both trees.

---

### F5 — On rejection or cancellation, is any re-entry attempted anywhere?
**Status:** ESTABLISHED · **WT↔VM:** **DIFFERS — LOGIC** (daily re-entry gate: TW counts per pipeline/book, WT counts account-wide) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**Answer.** No automatic re-entry follows a broker **REJECTED** or **CANCELLED** entry. Resubmission paths do exist for failures raised **at submit**, and new alerts for the same symbol are allowed after a failed entry.

**(A) Broker-side rejection or cancellation after placement — no re-entry**
- Kite REJECTED → OSM FAILED. Kite CANCELLED, fill timeout, pending-R:R cancel and 15:15 force close → CANCELLED.
- `OrderPlacer._on_order_status_changed` zero-fill branch: releases the reservation, sets the trade FAILED, and sends Telegram "ORDER REJECTED" for FAILED/REJECTED. It does **not** re-place or re-queue.
- Reconciler recovery for a REJECTED/CANCELLED entry: FAILED + release.
- TW-LOG 03-15 Sep: `entry_cancelled_zero_fill` 63 · `fill_timeout` 55 · pending-R:R cancel 8 events · `order_monitor.force_close_triggered` 6.

**(B) Synchronous failures inside `OrderPlacer.place`** (same `trade_id`, full qty)
- `BrokerRateLimit429Error`: the engine is re-executed up to `max_placer_retries` (config_loader default 3).
- `OrderRejectedError` with `kite_status_code == 16388`: one retry after `invalidate_margin_cache`.
- Every other rejection or `BrokerError`: single attempt → `_handle_placement_failure` → raise.
- **The 16388 comparison reads `kite_status_code=getattr(exc, "code", None)`.** In the VM venv, kiteconnect raises `exp(data["message"], code=r.status_code)`, which is an **HTTP status**. So a value of 16388 is not produced by this translator.

**(C) `signal_processor` re-queue (FIX-069)**
- On `BrokerRateLimitError` (client-side bucket; the live adapter calls `_rl.acquire` before `kite.place_order`), the same `signal_id` is re-queued with `retry_count+1`, up to 3.
- `OrderPlacer.place` has already marked that trade FAILED. A re-queued signal therefore re-runs `_process_one` from the start.
- `_process_one_safe` also re-queues when `try_acquire("order")` fails, before any processing.

**(D) New alerts for the same symbol/direction**
- A later Chartink alert can place a new entry the same day.
- The daily gate counts only `_EXECUTED_TRADE_STATUSES` = ("PENDING_FILL", "OPEN", "PARTIAL", "EXITING", "CLOSED", "CLOSED_MANUAL"). Docstring: *"a broker-REJECTED or FAILED entry never opened exposure and must not consume the day's slot"*.
- `one_trade_per_symbol_direction_per_day: true` in both trees.
- **Scope of the count differs:** TW passes `pipeline=_pipeline_for_intent(intent)` (per book); WT counts account-wide.

**Measured**
- TW-LOG 03-15 Sep: `16388_margin_rejection_retry` 0 · `429_retry` 0 · `FIX-069: re-queuing` 0 · `order bucket exhausted` 0 · `orphan_detected` 0.
- TW-DB: 0 `signal_id`s with more than one trade.
- Since 2026-09-03, 50 FAILED/REJECTED/CANCELLED trades were followed the same day by 51 later trades on the same symbol and direction, **all with a different `signal_id`**. Example: ANTELOPUS LONG REJECTED 10:00:24, then CLOSED 10:06:14. These are new signals, not system re-entries.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_placer.py` | 1963-2014 | `_on_order_status_changed` | `if event.qty_filled <= 0:` … `title=f"[{self._mode}] ORDER REJECTED — {fill_entry.symbol}"` … `self._fm.release(reservation_id=…, reason=f"entry_{status.lower()}_zero_fill",)` … `self._om.update_trade_status(trade_id=…, status="FAILED",)` … `return` |
| WT | `broker/zerodha_adapter.py` | 296-302 | `_translate_kite_exception` | `return OrderRejectedError(f"Zerodha rejected order: {exc}", rejection_reason=str(exc), kite_status_code=getattr(exc, "code", None),` (TW 316) |
| TW-LIVE | `venv/…/kiteconnect/connect.py` | 948 | `KiteConnect._request` | `raise exp(data["message"], code=r.status_code)` |
| WT | `signals/signal_processor.py` | 1505-1552, 401-417 | `_admit_and_place` / `_process_one_safe` | `except BrokerRateLimitError as transient_err: … if retry_count >= 3: … raise … retry_count += 1 … self._queue.put(signal_dict, timeout=1.0)` … `if not self._rate_limiter.try_acquire("order"): … self._queue.put(signal_tuple, timeout=1.0)` |
| WT | `core/state_store.py` | 683-685 | `_EXECUTED_TRADE_STATUSES` | `("PENDING_FILL", "OPEN", "PARTIAL", "EXITING", "CLOSED", "CLOSED_MANUAL",)` (TW 734-736) |

**Paper↔live**
- Order-status handling (A) and the daily gate (D) are the same code in both modes.
- **Live only:**
  - `BrokerRateLimitError` from `place_order`, and so the FIX-069 re-queue — paper returns before `_rl.acquire`;
  - broker HTTP 429;
  - the orphan branch — paper `cancel_order` always succeeds.

---

### F6 — Does any decision branch read the actual fill price? If yes, name it.
**Status:** ESTABLISHED · **WT↔VM:** DIFFERS — file only (some sites not diffed line-by-line; see caveat) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER (value source)

**Answer: YES.** These branches read the actual entry fill (`avg_fill_price` or `trades.entry_actual_price`):

1. **TGT placement.** `OrderPlacer._place_limit_triple_exits`: `actual_tgt_price = calc_tgt_price(direction, entry_price=avg_fill_price, sl_price=fill_entry.sl_price, rr_ratio=…)`. The SL stays at the strategy level.
2. **Exit placeability gate.** `clamp_exit_into_band(entry_fill=avg_fill_price)`, run only when circuit limits are available: `if entry_fill and entry_fill > 0:`.
   - TGT: `wrong = (clamped <= entry_fill) if is_long else (clamped >= entry_fill)`.
   - SL: `wrong = (clamped >= entry_fill) if is_long else (clamped <= entry_fill)`.
   - SL wrong → `SLUnplaceableError` → `_emergency_market_exit` + `_fire_hard_kill_for_unprotected_position`.
   - TGT wrong → SL-only placement plus TGT retry.
3. **TGT retry.** `OrderPlacer.retry_tgt_for_trade`: `entry_price = float(trade["entry_actual_price"] or 0.0)`; `if entry_price > 0 and sl_price > 0:` recompute TGT, else fall back to `tgt_initial`. `_retry_limit_triple_exits` does the same from `avg_fill_price`.
4. **Capital commit.** `FundManager.commit_to_used`: `actual_margin = required_margin(actual_qty, actual_fill_price, …)`; `excess = res.margin - actual_margin`. Then `_check_invariant`: a negative per-bucket value raises `CapitalInvariantViolation`, and the except path calls `kill_switch.hard_kill`.
5. **Realised P&L and the daily-loss gate.** `_handle_exit_fill` reads `entry_price = trades.entry_actual_price` → `gross_pnl` → `fm.release_used(entry_price=…)` → `daily_realized_pnl`. `RiskEngine` DAILY_LOSS rejects when `enforced_pnl < 0 and snap.total > 0 and abs(enforced_pnl) >= limit`. Reconciler CHECK1/CHECK4 and `cnc_gtt_monitor` use `entry_actual_price` in conditionals and P&L as well.
6. **Unrealised MTM.** `order_reconciler._refresh_unrealized_mtm`: `avg = float(t["entry_actual_price"] or 0.0)`; `if ltp <= 0 or avg <= 0 or qty <= 0: continue`; `fm.update_unrealized_mtm((ltp - avg) * qty * sign)`. This enters DAILY_LOSS only when `daily_loss_include_unrealized` is on and the MTM is fresh.
7. **Boot rehydrate.** `FundManager` rehydrate uses `price = entry_actual_price` if non-NULL and non-zero, else `entry_target_price`.

**Present but not reached**
- `BreakevenManager.register_trade` is gated on `strategy_obj`, which `_FillEntry.__slots__` lacks; `main.py` never constructs a BreakevenManager.
- `SmartTgtManager` applies only to `CO_PLUS_TGT`.

**Not decision branches (records/alerts only):** `OrderMonitor` `slippage_pct`, `SlippageRecorder`, the EOD summary, `shadow_tracker`. The pre-submit FIX-128 and FIX-075 steps read LTP, not the fill.

**Measured TW-LOG 03-15 Sep:** `tgt_recalc_from_fill_price` 41 = `fill_received` 41 = `entry_fill_recorded` 41. Branch 1 ran on every recorded fill in that window.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_placer.py` | 2870-2910 | `_place_limit_triple_exits` | `# FIX-013: Recalculate TGT from actual fill price to preserve R:R.` / `# SL stays anchored to original strategy level.` / `actual_tgt_price = calc_tgt_price(direction=fill_entry.direction, entry_price=avg_fill_price, sl_price=fill_entry.sl_price, …` … `entry_fill=avg_fill_price,  # NOCIL placeability gate reference` |
| TW=WT | `orders/price_math.py` | 100-116, 356-373 | `calc_tgt_price` / `clamp_exit_into_band` | `risk = abs(entry_price - sl_price)` / `return entry_price + risk * rr_ratio` … `if entry_fill and entry_fill > 0:` |
| WT | `capital/fund_manager.py` | 939-945, 986-1030 | `commit_to_used` | `actual_margin = required_margin(actual_qty, actual_fill_price, res.intent, self._leverage_map)` … `excess = res.margin - actual_margin` … `self._kill_switch.hard_kill(reason=reason, triggered_by="fund_manager.commit_to_used",)` (TW method diff-identical) |
| WT | `orders/order_reconciler.py` | 3549-3554 | `_refresh_unrealized_mtm` | `avg = float(t["entry_actual_price"] or 0.0)` … `if ltp <= 0 or avg <= 0 or qty <= 0: continue` (TW 3671) |
| WT | `capital/risk_engine.py` | 761-799 | DAILY_LOSS | `enforced_pnl = daily_pnl + (unrealized_mtm if use_unrealized else 0.0)` … `if enforced_pnl < 0 and snap.total > 0 and abs(enforced_pnl) >= limit:` (TW 700, 722) |

**Caveats**
- `order_reconciler` CHECK1/CHECK4 lines were not diffed between trees.
- `cnc_gtt_monitor` has 2 `entry_actual_price` reads in WT and 1 in TW, so the stranded-exit read may be WT-only.
- Items 5-7 read the persisted fill. Any `expected_price` fallback (F1) therefore flows into them.

---

## 7. GROUP G — PARITY AND EXISTING CONFIRMATION

### G1 — State every difference between the paper and live entry paths. If they are identical, say so explicitly.
**Status:** ESTABLISHED · **WT↔VM:** MATCH (the cited paper/live code is identical; the files differ elsewhere) · **Uncommitted in WT:** MIXED · **Paper↔live:** **NOT IDENTICAL**

**Answer: the paper and live entry paths are NOT identical.**

There is no separate paper adapter class. Both modes use **one** `ZerodhaAdapter` constructed with `paper_mode=is_paper` (`main.py` TW 2384-2410 / WT 2100-2126). Every difference lives in one of two places:
- the adapter's `if self._paper` branches, or
- `main.py` boot wiring.

`OrderPlacer` has exactly one branch on `self._mode`, and it is inert (D5 below).

**Files with no mode branch.** The mode is used only as a label, or not at all:
- `webhook_receiver`, `signal_processor`, `entry_throttle`
- `secondary_screener`, `step_executor`, `hard_gate`, `quality_scorer`
- `full_entry_engine`, `entry_engine`, `order_protocol_limit`, `order_manager`
- `position_sizer`, `risk_engine`, `kill_switch`, `strategy_governor`
- `market_windows`, `product_resolver`, `rate_limiter`

**Differences, in pipeline order:**

| # | Step | PAPER | LIVE |
|---|---|---|---|
| D1 | Boot broker handle | `kite_client = None` (TW 2352-2353 / WT 2068-2069) | Token file + account API key env var loaded (return 6 if missing) → `_build_kite_client` (TW 2354-2375 / WT 2070-2091) |
| D2 | Capital seed for FundManager | `_startup_capital = selected_account.paper_capital` (TW 2755-2756 / WT 2515-2516); `set_paper_capital(_fm_total)` after rehydrate; `get_margins` returns `net=available=self._paper_capital, used=0.0` | `compute_live_seed(broker_adapter, fund_manager, _start_of_today_iso)` (TW 2757-2760 / WT 2517-2520); `kite.margins(segment="equity")` |
| D3 | Quotes for the screener and M-S1 (`quote_fn=broker_adapter.get_quote`) | `_make_paper_quote_provider` (TW 473-605 / WT 470-602): a real `kite.quote` from the token file, alias translation, `_CACHE_TTL_SEC = 3.0`, `_MIN_CALL_INTERVAL_SEC = 0.35`, no RateLimiter, returns `{}` on API failure | `self._rl.acquire("get_quote")` + `kite.quote`; raises a translated exception on failure |
| D4 | Pre-submit LTP guards | `get_quote_raw`: `if self._paper: return {}` (TW 1816-1817 / WT 1748-1749), so `_fetch_ltp` returns None and **FIX-128 slippage abort and FIX-075 drift override do not run** | Both run (`kite.quote`) |
| D5 | Liquidity check | code branches `if self._mode == "LIVE" and self._adapter is not None:` (`order_placer.py:1293`) | **same effect in both modes**: `_check_liquidity` returns `(True, "")` because `liquidity_check_enabled` defaults to False (589, 4075) and is not passed |
| D6 | Submission | After shared validate / tick-snap / force-intraday / product resolve / CNC lock / OSM register: `_paper_place_order` (TW 608-619 / WT 573-584). Fake id `"PAPER_"+uuid`, no RateLimiter, no kite call, no broker exception | `self._rl.acquire(place_order)` → `truncate_tag_for_broker(tag)` → `kite.place_order` (TW 622-654 / WT 587-615) |
| D7 | Fill | Daemon thread `_synth_fill`: sleeps 0.5 s; with `ltp_gating_enabled: true` (max wait 21600 s, poll 5.0 s) a LIMIT BUY fills only when LTP ≤ price, at `min(LTP, price)`; rejects a fill deviating > 50%; applies `SlippageEngine` (wired only `if is_paper`, TW 2512-2516); publishes `OrderFilled(source_module="zerodha_adapter_paper")` | Exchange fill observed by `OrderMonitor._poll_cycle` → `get_order_history` → kite; publishes `OrderFilled(source_module="order_monitor")` |
| D8 | Positions | `_paper_positions` keyed by **symbol only** | Kite positions per **(symbol, product)** |
| D9 | Sizing leverage | `get_live_margin_pct` raises `BrokerError` in paper | **same effect in both modes**: PositionSizer is built without `broker_adapter`, so static leverage is used |
| D10 | Beside the entry path | `LiveFeedManager` skips the WebSocket; TokenMonitor `profile_fn` is `lambda: None`; `store.cancel_stale_paper_orders` at boot; historical-data handle rebuilt from the token file; notifier `send_in_paper_mode` | `BrokerClockSkewProbe` runs only in live |

**Deployed mode (measured):** TW-LOG 2026-09-15 08:15:23.961 `"Trading System v2.0.0 starting (mode=live)"`. Every boot 03..15-Sep logged `mode=live`.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW | `main.py` | 2377-2394 | `main` | `is_paper = (args.mode == "paper")` … `paper_mode=is_paper,` … `quote_provider=(_make_paper_quote_provider() if is_paper else None),` |
| TW | `main.py` | 2754-2761 | `main` | `if args.mode == "paper": _startup_capital = selected_account.paper_capital` / `else: _startup_capital = compute_live_seed(broker_adapter, fund_manager, _start_of_today_iso)` |
| TW=WT | `orders/order_placer.py` | 1291-1293 | `OrderPlacer.place` | `# Paper mode skips (simulated fills). Best-effort: failure = proceed.` / `if self._mode == "LIVE" and self._adapter is not None:` |

**NOT ESTABLISHED:** whether paper publishes a second `OrderFilled` (one from the synth thread, one from the `OrderMonitor` poll of `_paper_fills`). This was not traced.

---

### G2 — Does a deterministic 5-minute confirmation rule exist? If yes, report: function name · inputs · as-of semantics · exact pass/fail output · side effects · whether it reads any data after the confirming candle.
**Status:** ESTABLISHED · **WT↔VM:** MATCH (PB-01 modules md5-identical) · **Uncommitted in WT:** NO · **Paper↔live:** IDENTICAL

**Answer: YES, exactly one exists** — the **PB-01 next-morning entry stage**, a 5-minute retest-confirmation rule.

**⚠ It is NOT part of the order-placing entry path.** It is SHADOW / analysis-only and places nothing (see Wiring below). Its files, `v3_chain/pb01_entry.py` and `screening/hard_gate.py`, are md5-identical in both trees, so the line numbers below serve both.

**Function name**
- `Pb01EntryStage.poll_once` (144-166), run on daemon thread `pb01-entry` every `poll_interval_sec`.
- It calls `Pb01EntryStage._evaluate` (169-233).
- `_evaluate` calls `screening.hard_gate.gate_pullback` (422-466) and `gate_confirm` (369-419).
- On a pass, it calls `Pb01EntryStage._confirm` (235-261).

**Inputs**
- (a) **Watchlist rows** from `store.get_pb01_watchlist_for_date(today, pending_only=True)`: `symbol`, `level`, `trading_date`. They are written the previous evening by `WatchlistCaptureWorker` from the EOD webhook `pb01_breakout_retest`.
- (b) **Today's 5-minute candles**, re-fetched every poll via `self._fetcher.fetch_interval(symbol, "5minute", lookback_days=1)` (OhlcFetcher, `cache_ttl_sec=0.0`, kite `historical_data`).
- (c) **Session-static values**, memoized per (symbol, trading_date):
  - `atr30` = ATR(14) of 30-minute candles, truncated to the session open;
  - `baseline_5m_volume` = mean of the last 20 prior daily volumes ÷ 75.
- (d) **Config**:
  - `confirm_min_body_frac 0.50` · `confirm_volume_mult 1.20`
  - `pullback_proximity_pct 0.005` · `pullback_proximity_atr_mult 0.50` · `hold_buffer_atr_mult 0.20`
  - `gap_guard_pct 0.03` · `entry_start "09:20"` · `entry_end "11:00"` · `poll_interval_sec 20.0`
  - The config key `entry_tf: "5minute"` is read by no non-test code. The interval is hard-coded `_TF_5 = "5minute"` (`pb01_entry.py:44`).

**As-of semantics**
- A candle is used only if `close_ts = bar-start + 5 min <= now` (`truncate_to_asof`) and it is dated today. A still-forming bar is never evaluated.
- Candles are walked chronologically from the open. The first terminal event wins, and every poll re-derives the verdict from the open.
- The decision instant is `as_of = close_ts(confirming candle, "5minute")`.
- Polls before 09:20 return without evaluating.
- A poll at or after 11:00 wall clock marks every remaining PENDING row `EXPIRED_WINDOW`, without evaluating candles.

**Exact pass/fail output**
1. Before the walk: if `closed[0].open > level * (1.0 + 0.03)`, the row becomes **`SKIPPED_GAP`**.
2. For each candle c, in order:
   - a. **`INVALIDATED`** if `hold_floor is not None and c.close < hold_floor`, where `hold_floor = level - 0.20*atr30`. This check precedes confirmation.
   - b. `gate_pullback` passes iff `session_low <= level + max(0.005*level, 0.50*atr30)` AND `lowest_5m_close >= level - 0.20*atr30`. Any missing input, including `atr30` None, fails.
   - c. `gate_confirm` passes iff `close > level` AND `abs(close-open)/(high-low) >= 0.50` AND `volume >= 1.20*baseline_5m_volume`. Any None, `high-low <= 0`, or `baseline <= 0` fails. The rule is LONG-only.
   - d. If both gates pass: **`CONSUMED`** with `Pb01Confirmation(entry_price = confirming candle close, as_of, session_low, lowest_5m_close, atr30, baseline)`.
3. With no terminal event, the row stays **`PENDING`**. Each gate returns `GateVerdict(passed, gate_name, evidence)`.

**Side effects**
- `store.update_pb01_watchlist_status(row id, status, outcome_json, consumed_at)`. For CONSUMED this is written before `on_confirm`.
- An effect-telemetry counter and a log line.
- `on_confirm = Pb01WouldBeRunner.record`, which appends one JSON line to `data_store/v3/pb01_would_be.jsonl`.
- **No order, no reservation, no queue side effect.** `Pb01WouldBeRunner` holds no fund_manager, placer, broker or queue reference.

**Does it read any data after the confirming candle?**
- The pass/fail uses only candles up to and including the confirming candle, plus prior-session static inputs.
- The poll-time fetch can contain later candles, but they are not consulted for that verdict.
- Measured on 213 CONSUMED rows, `consumed_at − as_of`: min 0.04 s, p50 16.6 s, p90 37.5 s, max 68.6 s.

**Determinism limits (from code)**
- (i) `EXPIRED_WINDOW` depends on when the poll runs, not on candle time.
- (ii) The memoized static values persist even when a fetch raised. A missing `atr30` fails `gate_pullback` for the rest of the session, while a restart re-fetches.
- (iii) Only today's rows are loaded: 31 PENDING rows from `trading_date` 2026-08-10 remain.
- (iv) Candle values are whatever Kite returns at each re-fetch. Whether Kite revises a closed bar is **NOT ESTABLISHED**.

**Wiring and deployed state**
- `watchlist.enabled: true` (TW config 616).
- It is started only `if _watchlist_on` (TW `main.py` 3713-3749), with `on_confirm=_pb01_would_be.record`.
- TW-LOG 2026-09-15 08:15:32.061: `"V3 Step 10b PB-01 watchlist: ENABLED — capture + entry stage started (SHADOW / ANALYSIS-ONLY, NO order path)"`.
- TW-DB `pb01_watchlist` 839 rows: CONSUMED 213 · EXPIRED_WINDOW 124 · INVALIDATED 115 · PENDING 31 · SKIPPED_GAP 356. `pb01_would_be.jsonl` has 213 lines.

**Why it is not on the entry path**
- Strategy `pb01_breakout_retest` has `enabled: false`.
- `scan_webhook_map` gives `scanner_type: eod`, and `_handle_eod` never enqueues.
- TW-DB: `trades WHERE strategy LIKE 'pb01%'` = 0.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `screening/hard_gate.py` | 406-418 | `gate_confirm` | `if c <= lvl: … return GateVerdict(False, GATE_CONFIRM, ev)` / `body_frac = abs(c - o) / rng` … `if body_frac < float(min_body_frac):` … `if vol < float(volume_mult) * base:` … `return GateVerdict(True, None, ev)` |
| TW=WT | `screening/hard_gate.py` | 444-465 | `gate_pullback` | `proximity = max(float(proximity_pct) * lvl, float(proximity_atr_mult) * a)` / `hold_floor = lvl - float(hold_buffer_atr_mult) * a` / `touched = slow <= lvl + proximity` / `held = lclose >= hold_floor` |
| TW=WT | `v3_chain/truncate.py` | 55-100 | `close_ts` / `truncate_to_asof` | `return ts + timedelta(minutes=mins)` … `if close_ts(c, interval, as_of) <= as_of: out.append(c)` |
| TW | `config/scan_webhook_map.yaml` | 84 | — | `scanner_type: eod   # DAILY/EOD alert → routed to the watchlist ONLY, never the intraday order path` |
| TW | `config/strategies/pb01_breakout_retest.yaml` | 30 | — | `enabled: false              # FAIL-CLOSED: never trades until the spec-13 promotion gate` |

---

### G3 — Does any other confirmation or recovery mechanism exist under a different name?
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER (R6 only)

**Answer: yes, several.** None is a 5-minute candle confirmation on the order-placing path.

**Confirmation / wait mechanisms**

| ID | Mechanism | What it is | State |
|---|---|---|---|
| C1 | SNR-V2 WAIT_FOR_RETEST: `RetestDiverter.maybe_divert` → `RetestMonitor` → `sr_detector/retest_confirm.evaluate` | **1-minute** fold `WAIT_BREAKOUT → WAIT_RETEST → WAIT_CONFIRM → CONFIRMED \| REJECT`; confirm close in the strong `confirm_strong_close_frac 0.6`; timeout 1800 s; `on_confirm=continue_from_retest` places MARKET | **DISABLED**: `wait_for_retest_enabled: false`; `retest_state` 0 rows |
| C2 | EntryGate (`screening/entry_gate.py`) | **price-band** wait `lower <= ltp <= upper` with `pullback_wait_tolerance_pct` / `pullback_wait_timeout_sec` | Constructed and started every boot ("EntryGate started: poll_interval=5.0s workers=2"), **never fed**: no `EntryGate.add` caller; `gate_state` 0 rows. `pullback_wait_enabled: true` only skips M-S1. |
| C3 | V3 decision chain 10a (`V3ChainRunner`) | G-RR / G-HTF / G-EXTREME verdicts, LOG-ONLY to `data_store/v3/would_be.jsonl` (2582 lines) | `v3_chain_mode: "shadow"` — never alters orders |
| C4 | SNR-DETECTOR-V1 observer | post-place, non-gating zone observer | not an entry gate (from config/main.py comments — EVIDENCE) |
| C5 | Structure exit confirmed-break | exit-side only | `structure_exit_enabled: false` |
| C6 | Screener step 5 "price action" | score input `body_pct = \|ltp - day open\| / (day_high - day_low)`, `min(1.0, body_pct*2.0)` from the session quote | active, but a score input — not a closed-candle confirmation |

**Recovery / retry mechanisms on the entry path**

| ID | Mechanism | What it does |
|---|---|---|
| R1 | FIX-067 / M-S1 re-anchor | For `pullback_wait_enabled: false` strategies, re-derives entry and SL from live LTP |
| R2 | `_process_one_safe` rate-limit re-queue | Puts the tuple back when `try_acquire("order")` fails |
| R3 | FIX-069 `BrokerRateLimitError` handler | Re-queues with `retry_count + 1`, up to 3 |
| R4 | A-2 `BrokerTimeoutError` handler | Sets signal TIMEOUT, no retry; trade stays `UNKNOWN_IN_FLIGHT`; resolved later by `OrderReconciler._recover_in_flight_entries` |
| R5 | BL-19 | Retries `engine.execute` only on `BrokerRateLimit429Error` |
| R6 | FIX-128 abort / FIX-075 drift top-up | Live only |
| R7 | `OrderMonitor` on a pending entry | 60 s fill-timeout cancel; FIX-141 pending-R:R cancel; partial-fill handling |
| R8 | FIX-061 `_pending_exit_retry` | LTP-validation errors on **exit** orders only |

**No file on the order path fetches candles.** A grep for `historical_data|fetch_interval|fetch_timeframes|truncate_to_asof|gate_confirm|candle` over the order-path files gives 0 code hits in both trees. The only hits are 2 comments in `order_placer.py` (about the exit path) and 1 docstring in `step_executor.py`.

---

### G4 — If no such rule exists, say so plainly. Do not describe the nearest thing as though it were one.
**Status:** ESTABLISHED · **WT↔VM:** MATCH · **Uncommitted in WT:** MIXED · **Paper↔live:** IDENTICAL

**Plainly:**

1. **Across the codebase, a deterministic 5-minute confirmation rule DOES exist:** the PB-01 entry stage. It is enabled on the testing VM, but it only writes `pb01_watchlist` status rows and `pb01_would_be.jsonl` lines. It places no order, reserves no capital, and its strategy is `enabled: false`.
2. **On the ENTRY EXECUTION path that actually sends orders, NO 5-minute confirmation rule exists.** No candle-close confirmation of any timeframe is active there. The path is:
   webhook → `SignalProcessor._process_one` → `_admit_and_place` → `OrderPlacer.place` → `LimitTripleProtocol` → `ZerodhaAdapter.place_order`
   - The path fetches no candles.
   - The only candle-based confirmation that could feed placement is SNR-V2 WAIT_FOR_RETEST. It is 1-minute and disabled.
   - EntryGate is a price-band wait with no `add()` caller.
   - `pullback_wait_enabled: true` does not create a wait.

Neither the PB-01 rule, SNR-V2, EntryGate nor the V3 shadow chain is a confirmation rule on the order path.

**Search width:** case-insensitive grep over all non-test `*.py` in both trees for `confirm|5minute|5min|five_min|5-min|5m\b|minute=5|retest|pullback_wait|watchlist` (90+ files per tree). This was followed by targeted greps for `gate_confirm|gate_pullback`, which are called only in `v3_chain/pb01_entry.py` and `v3_chain/pb01_runner.py`. Config flag blocks were read in both trees.

---

## 8. GROUP H — HISTORICAL EVIDENCE FROM PAPER

**Applies to every H answer.**

**PAPER: NOT ESTABLISHED** — no paper-mode data exists anywhere on the testing VM. Tables and files searched:
- All 46 tables in `trading_system.db` and all 4 in `analytics.db`, checking every mode/paper/account-like column:
  - `trades.mode` LIVE 954 · `config_snapshots.mode` LIVE 55 · `eod_broker_reconciliation.mode` LIVE 45
  - `session.mode` LIVE · `sr_detector_results.mode` 'live' 678
- All 39 DBs under `data_store/backups`, opened immutable read-only.
- All 82 files in `logs/`, grepped for paper markers: 0 hits.

The code also shows that paper cannot produce several of these records on the direct path: `get_quote_raw` returns `{}`, so FIX-128 is skipped, and paper never emits `PARTIAL`.

**LIVE figures follow, clearly labelled LIVE**, split at the account boundary **2026-09-09T11:15:14+05:30**:
- **LFL836** = `config_snapshots` 1-50, last one 2026-09-08T08:15:32.
- **VBB097** = `config_snapshots` 51-55, first one 2026-09-09T11:15:14.
- Corroborated by `system_events` (SHUTDOWN 2026-09-08T13:52:21; CONFIG_DIFF + STARTUP COLD 2026-09-09T11:15:14/17) and by account markers in the logs.

---

### H1 — How many entries have been aborted on the slippage check so far?
**Status:** PARTIAL · **WT↔VM:** DIFFERS — file only (the writer statement is identical) · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**PAPER: NOT ESTABLISHED** (no paper data; the guard is skipped in paper).

**LIVE: 95 entries aborted on the slippage check.**
- All 95 fall in the LFL836 period, first 2026-06-23T10:06:11+05:30, last 2026-09-08T10:13:14+05:30.
- **0 fall in the VBB097 period** (2026-09-09T11:15:14 … 2026-09-15).

**What writes the record** (`OrderPlacer.place`, FIX-128 block, `order_placer.py` 1099-1195):
1. `_slippage_decision` returns an `abort_reason`.
2. The code builds `OrderRejectedError("slippage_exceeded: trigger=... ltp=... | <reason>")`.
3. It logs WARNING `order_placer.slippage_guard_exceeded`.
4. It calls `_handle_placement_failure(final_status="REJECTED")`, which sets the trade REJECTED, releases the reservation with `placement_failed: {exc}`, and re-raises.
5. `SignalProcessor`'s outer handler writes `signals.status='PLACEMENT_FAILED'` with `rejection_reason=str(exc)` (WT 1268-1273 / TW 1233-1238).
6. The trade row already exists: `create_trade` runs before the guard.

**Three independent DB records agree on 95:**

| Record | Query | Count |
|---|---|---|
| `signals` | `rejection_reason LIKE 'slippage_exceeded%'` (all `PLACEMENT_FAILED`, `trade_id` populated 95/95) | 95 |
| `fm_ledger` | `entry_type='RELEASE' AND reason LIKE 'placement_failed: slippage_exceeded%'` | 95 |
| `trades` | `status='REJECTED'` (95/95 linked to those signals) | 95 |

**Log cross-check** (TW-LOG exists only for 09-03..09-15):
- `slippage_guard_exceeded` appears 9 times (09-03: 1 · 09-04: 3 · 09-07: 2 · 09-08: 3). These are exactly the 9 DB aborts on those dates.
- VBB097 days show `entry_slippage_observed aborted=false` 55 times (09-09: 11 · 09-10: 16 · 09-11: 23 · 09-15: 5) and `aborted=true` 0 times.

**Loaded config:** all 55 `config_snapshots` carry `slippage_control enabled=True, mode=sl_fraction, max_slippage_fraction 0.22, absolute_cap_rs 5.0, hard_max_slippage_rs 10.0`.

**Caveats**
- Before 09-03 the count rests on the three DB records alone; there are no logs.
- Which code version ran on each LFL836 day is **NOT ESTABLISHED**. Commit dates are not deploy dates.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_placer.py` | 1103-1195 | `OrderPlacer.place` | `slip_exc = OrderRejectedError(f"slippage_exceeded: trigger={signal_trigger_price:.2f} " f"ltp={_slip_ltp:.2f} \| {_abort_reason}", …)` … `self._handle_placement_failure(trade_id, reservation_id, signal_id, slip_exc, final_status="REJECTED", symbol=symbol, suppress_alert=True)` … `raise slip_exc` |
| TW-DB | `signals` | — | ro | `PLACEMENT_FAILED 95; range 2026-06-23T10:06:11.981227+05:30 .. 2026-09-08T10:13:14.918421+05:30; rows >= 2026-09-09T11:15:14: 0` |

---

### H2 — For those, the distribution of SL distance in rupees.
**Status:** PARTIAL · **WT↔VM:** MATCH · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**PAPER: NOT ESTABLISHED.**

**LIVE:** all 95 aborts are LFL836. **The VBB097 period has n = 0.**

**Definition** (`_compute_slippage_tolerance`, mode `sl_fraction`): `sl_dist = abs(signal_price - sl_price)`.
- `signal_price` = the Chartink trigger (`signals.trigger_price`).
- `sl_price` = the value persisted as `trades.sl_initial`.
- On abort, `_slippage_decision` writes it into the reason text as `SL_dist=₹{sl_dist:.2f}`.

**Measurement**
- `SL_dist` was parsed from all 95 `rejection_reason` strings (95/95 carry the field).
- It was cross-checked against `abs(signals.trigger_price − trades.sl_initial)`: max absolute difference 0.004988 (message rounding).

**Distribution (Rs; linear-interpolation percentiles):**

| Set | n | min | p10 | p25 | median | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|
| ALL | 95 | 0.29 | 1.454 | 1.985 | 3.32 | 6.29 | 10.106 | 24.25 | 4.7055 |
| LONG | 84 | 0.80 | 1.443 | 1.97 | 3.265 | 6.135 | 10.132 | 24.25 | 4.6777 |
| SHORT | 11 | 0.29 | 1.69 | 2.825 | 4.96 | 6.29 | 7.81 | 10.88 | 4.9173 |

**Notable rows**
- UTLSOLAR 2026-07-10: `SL_dist` 0.29 (slippage was 969% of SL).
- DBOL 2026-08-18: 0.80 (260%).
- IIFL 2026-08-21: 22.76.
- RAYMOND 2026-09-08: 24.25.
- The two largest hit the absolute cap (`tolerance ₹5.00`).

**Sample reason text:** `slippage_exceeded: trigger=446.50 ltp=444.80 | slippage ₹1.70 > tolerance ₹1.57 (mode=sl_fraction, SL_dist=₹7.15, 24% of SL)`.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `orders/order_placer.py` | 383-386 | `_slippage_decision` | `extra = f", SL_dist=₹{sl_dist:.2f}, {slip_rs / sl_dist * 100:.0f}% of SL" if sl_dist else ""` |

---

### H3 — How many orders timed out unfilled?
**Status:** PARTIAL · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**PAPER: NOT ESTABLISHED.**

**What writes the record** (identical in both trees):
- `OrderMonitor._check_fill_timeout` logs WARNING `order_monitor.fill_timeout` → `cancel_order`.
- On success it logs `order_monitor.timeout_cancelled` and sets CANCELLED; on failure it logs `orphan_detected` and sets FAILED.
- `OrderPlacer._on_order_status_changed` (`qty_filled <= 0`) logs `entry_cancelled_zero_fill`, releases the reservation, and sets the trade FAILED.
- **No DB column records the cause of a cancel.** `orders.rejection_reason` is empty on 36/36 VBB097 and 366/369 LFL836 cancelled ENTRY rows. FIX-141 cancels write the same record. A count therefore needs the log event joined to the broker order id.

**Loaded config:** `order_monitor.fill_timeout_sec 60` in all 55 `config_snapshots`.

**LIVE, VBB097 period (09-09..09-15): 32 ENTRY orders timed out unfilled.**
- By day: 09-09: 9 · 09-10: 8 · 09-11: 14 · 09-15: 1.
- Each `fill_timeout` line has a matching `timeout_cancelled`. All 32 broker ids are ENTRY rows, status CANCELLED, trade FAILED. `orphan_detected` = 0.
- Of 51 VBB097 ENTRY orders: 15 COMPLETE, 36 CANCELLED (32 timeout + 4 pending-R:R).

**LIVE, LFL836 inside the log window (09-03..09-08): 23** (09-03: 5 · 09-04: 4 · 09-07: 4 · 09-08: 10), all ENTRY, CANCELLED, trade FAILED.

**LIVE, LFL836 full history (2026-06-15..09-08): NOT ESTABLISHED** from a cause record, because there are no logs before 09-03.
- The DB holds 369 CANCELLED ENTRY orders.
- *INFERENCE-only proxy (not a count):* `updated_at − placed_at` in (60, 70] s gives 328. Over 09-03..09-15 this proxy matched perfectly: all 55 logged timeouts fell in 60-70 s, and all 8 logged pending-R:R cancels were ≤ 55 s.

**What "unfilled" means here:** "recorded as zero-fill by the monitor".
- The timeout path uses `entry.filled_qty`, which only `_handle_partial` updates (Kite status literally `PARTIAL`).
- `_handle_open` never reads the broker's `filled_qty`.
- The cancel is accepted on the `cancel_order` response without re-reading broker state.
- Broker-side cross-checks for VBB097: `reconciliation_log` has no ORPHAN_ADOPTION / POSITION_GREW rows; `eod_broker_reconciliation` is VERIFIED for 09-09, 09-10 and 09-11.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 1087-1110 | `_check_fill_timeout` | `if elapsed <= self._fill_timeout: return` … `self._log.warning("order_monitor.fill_timeout", …)` / `result = self._adapter.cancel_order(entry.broker_order_id)` / `if result.success: … self._safe_transition(entry.internal_order_id, "CANCELLED", entry=entry)` |
| TW-LOG | `logs/system_2026-09-03..15.log` | — | grep | `fill_timeout 09-03 5, 09-04 4, 09-07 4, 09-08 10, 09-09 9, 09-10 8, 09-11 14, 09-15 1 (total 55) = timeout_cancelled per day; orphan_detected 0` |

---

### H4 — How many partial fills, and what proportion of requested quantity?
**Status:** PARTIAL · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**PAPER: NOT ESTABLISHED.** Code fact: the paper adapter never emits a `PARTIAL` status (`grep 'PARTIAL'` in `zerodha_adapter.py`: 0 hits in both trees).

**LIVE: 0 partial fills recorded, in every record class.**
- The proportion of requested quantity is **NOT ESTABLISHED**, because no partials are recorded.
- All 368 filled trades have `qty_filled = qty_planned` (100%).

**Measured**

| Source | Result |
|---|---|
| `trades` | `qty_filled` populated 954/954; `> 0` on 368; `0 < qty_filled < qty_planned` 0; `qty_filled > qty_planned` 0 |
| `order_execution_log` | `is_partial=1` on 0 of 635; `filled_qty < qty` on 0 |
| `orders` | `qty_filled > 0` on 0 of 1452; `avg_fill_price` NULL on all 1452 — unpopulated, not usable |
| TW-LOG 09-03..09-15 | 0 events of `order_monitor.partial_fill`, `partial_immediate_cancel(led/_failed)`, `partial_terminated`, `partial_stuck_cancel`, `order_placer.partial_entry_terminated` |

**Why a recorded zero may not mean a real zero**
- The system records a partial only if the broker status string is exactly `PARTIAL`.
- A history row with status OPEN and `filled_qty > 0` goes to `_handle_open`. That handler ignores `filled_qty`. At 60 s the timeout transitions to CANCELLED using `entry.filled_qty` (still 0), and the placer books a zero-fill FAILED trade.
- Whether Kite ever reports status `PARTIAL` is **NOT ESTABLISHED** from code or data.
- The LFL836-period `reconciliation_log` holds ORPHAN_ADOPTION 2,647 and POSITION_GREW 14 rows. These were **not** attributed to partial fills.

| Tree | File | Lines | Function | Literal |
|---|---|---|---|---|
| TW=WT | `broker/order_monitor.py` | 85-89, 764-777 | `_process_order` | `_KITE_STATUS_OPEN = {"OPEN", "TRIGGER PENDING", "SUBMITTED"}` / `_KITE_STATUS_PARTIAL = {"PARTIAL"}` … `if kite_status in _KITE_STATUS_OPEN: self._handle_open(entry, now)` / `elif kite_status in _KITE_STATUS_PARTIAL: self._handle_partial(entry, filled_qty, avg_price)` |
| WT | `orders/slippage_recorder.py` | 142 | `_on_order_filled` | `"is_partial": 1 if (qty_req and ev.filled_qty and ev.filled_qty < qty_req) else 0,` |

---

### H5 — Distribution of (actual fill − intended order price), signed.
**Status:** PARTIAL · **WT↔VM:** MATCH · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**PAPER: NOT ESTABLISHED.**

**Source and sign (code)**
- `order_execution_log.intended_price` = `OrderFilled.expected_price` = `entry_price` passed to `order_monitor.track`. This is **after** any FIX-075 drift and **before** the tick snap.
- `actual_price` = `OrderFilled.avg_fill_price` = `avg_price if avg_price > 0 else entry.expected_price`. A missing broker average therefore yields a difference of 0.
- The stored `slippage_rs` is adverse-positive: BUY `actual−intended`, SELL `intended−actual` (verified on 635/635 rows).
- **The figures below are the RAW signed `actual_price − intended_price`.** Negative = filled below the intended price, whatever the side.

**Row selection**
- 262 rows (`fill_timestamp` 2026-06-22..2026-07-16) have a NULL `parent_trade_id` and `leg='ENTRY'`, 131 BUY / 131 SELL. They predate the enrichment fix `fd77f80` (local git 2026-07-17), and their leg is unreliable, so they are **excluded**.
- The 373 enriched rows run 2026-07-20..2026-09-15: ENTRY 213 · SL 90 · TGT 63 · EOD 7.

**ENTRY (Rs)**

| Set | n | min | p10 | p25 | median | p75 | p90 | max | mean | neg-zero-pos |
|---|---|---|---|---|---|---|---|---|---|---|
| LFL836 ALL | 198 | −0.8850 | −0.0267 | −0.0102 | −0.0009 | 0.0045 | 0.0178 | 0.9332 | −0.0209 | 106-1-91 |
| LFL836 BUY | 172 | −0.8850 | −0.0640 | −0.0127 | −0.0011 | 0.0042 | 0.0156 | 0.0250 | −0.0334 | 94-1-77 |
| LFL836 SELL | 26 | −0.0236 | −0.0070 | −0.0033 | 0.0012 | 0.0205 | 0.1396 | 0.9332 | 0.0617 | 12-0-14 |
| VBB097 ALL | 15 | −1.3100 | −0.0368 | −0.0221 | −0.0019 | 0.0027 | 0.0127 | 0.0185 | −0.0938 | 9-0-6 |
| VBB097 BUY | 14 | −1.3100 | −0.0389 | −0.0226 | −0.0013 | 0.0032 | 0.0140 | 0.0185 | −0.0999 | 8-0-6 |
| VBB097 SELL | 1 | −0.0086 | | | | | | | | |

**ENTRY (% of intended)**
- LFL836 ALL: min −0.4788 · p10 −0.0120 · median −0.0003 · p90 0.0039 · max 0.2236 · mean −0.0082.
- VBB097 ALL: min −0.1427 · p10 −0.0158 · median −0.0003 · p90 0.0034 · max 0.0067 · mean −0.0114.

**Exit legs, enriched rows only (Rs)**

| Set | n | min | p10 | p25 | median | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|---|
| LFL836 SL BUY | 11 | −0.0221 | −0.0186 | 0.0122 | 0.2546 | 0.4596 | 1.6614 | 2.6100 | 0.5330 |
| LFL836 SL SELL | 73 | −2.1558 | −0.6383 | −0.2966 | −0.1272 | −0.0096 | 0.0185 | 2.6720 | −0.1678 |
| LFL836 TGT BUY | 14 | −0.0369 | −0.0208 | −0.0028 | 0.0032 | 0.0161 | 1.5760 | 3.3730 | 0.4001 |
| LFL836 TGT SELL | 44 | −0.0240 | −0.0102 | −0.0038 | 0.0002 | 0.0054 | 0.0142 | 0.0250 | 0.0013 |
| LFL836 EOD SELL | 7 | 1.24 | 1.714 | 2.065 | 2.22 | 2.65 | 2.694 | 2.70 | 2.2271 |
| VBB097 SL BUY | 1 | 0.0315 | | | | | | | |
| VBB097 SL SELL | 5 | −0.6525 | −0.5143 | −0.3071 | −0.2162 | −0.0688 | −0.0247 | 0.0046 | −0.2480 |
| VBB097 TGT SELL | 5 | −0.0085 | −0.0076 | −0.0064 | −0.0004 | 0.0000 | 0.0057 | 0.0095 | −0.0011 |

**Secondary source: all 368 COMPLETE ENTRY trades** (includes the pre-07-20 era). Metric: `trades.entry_actual_price − trades.entry_target_price`, where the target is the **pre-drift** planned price.

| Set | n | min | p10 | p25 | median | p75 | p90 | max | mean | neg-zero-pos |
|---|---|---|---|---|---|---|---|---|---|---|
| LFL836 ALL | 353 | −0.8850 | −0.0400 | −0.0100 | 0.0000 | 0.0047 | 0.0192 | 3.1000 | 0.0113 | 174-19-160 |
| LFL836 BUY | 313 | −0.8850 | −0.0661 | −0.0127 | 0.0000 | 0.0045 | 0.0176 | 3.1000 | 0.0058 | |
| LFL836 SELL | 40 | −0.0236 | −0.0054 | −0.0035 | 0.0008 | 0.0189 | 0.0837 | 0.9332 | 0.0546 | |
| VBB097 | 15 | identical to the `order_execution_log` figures | | | | | | | | |

**Consistency on the enriched ENTRY rows:** `intended_price` differs from `entry_target_price` on 1 of 213 (the drift override). `actual_price` equals `trades.entry_actual_price` on 213/213.

**NOT ESTABLISHED**
- **Actual minus the submitted (tick-snapped) price.** The submitted price is not persisted (`orders.price` is NULL on all 773 ENTRY rows, and the snap log is DEBUG with 0 hits), so the differences above include tick rounding.
- **True zeros vs fallback zeros.** A zero difference cannot be told apart from the `avg_price<=0 → expected_price` fallback: 12 LFL836 zeros in the unenriched set, 1 in the enriched set, 0 in VBB097.
- **What `expected_price` holds on exit legs** (SL trigger vs limit) was not traced.

---

### H6 — Any case where an order survived its intended window.
**Status:** PARTIAL · **WT↔VM:** DIFFERS — file only · **Uncommitted in WT:** MIXED · **Paper↔live:** DIFFER

**PAPER: NOT ESTABLISHED.**

**Intended window (code + loaded config):**
- `OrderMonitor` cancels a non-exit order at the first poll where `elapsed > 60 s`, measured from the tracked `placed_at` (taken after broker placement).
- Polls run every 2 s.
- Both values (60 and 2) appear in all 55 `config_snapshots`.
- SL/TGT/EOD legs are exempt by design.

**LIVE — YES, in three measured senses:**

**(a) Every logged timeout's cancel decision fired after 60 s, up to 66.0 s.**
- Across the 55 `order_monitor.fill_timeout` lines (09-03..09-15), `elapsed_sec` runs min 60.1, median 61.4, max 66.0.
- Buckets: 60-61: 20 · 61-62: 22 · 62-64: 11 · 64-70: 2.
- **13 exceed 62 s** (more than one poll past the window):
  - VBB097 (11): 09-09 66.0, 62.2, 62.6 · 09-10 62.3, 64.3 · 09-11 63.5, 62.2, 62.1, 62.3, 63.8, 63.5.
  - LFL836 (2): 09-03 62.6 · 09-08 62.4.
- Every one was followed by `timeout_cancelled`. `orphan_detected` = 0.

**(b) Five CANCELLED ENTRY orders had their terminal DB write more than 70 s after `placed_at`.** All are LFL836, June 2026:

| Symbol | placed_at | terminal write | gap |
|---|---|---|---|
| SETL | 2026-06-15T11:34:27 | 2026-06-16T09:04:19 | 77,392 s |
| HARIOMPIPE | 2026-06-15T11:35:18 | — | 77,341 s |
| AVL | 2026-06-15T11:35:19 | — | 77,340 s |
| GICRE | 2026-06-16T10:00:16 | 2026-06-16T20:43:18 | 38,583 s (trade CLOSED_MANUAL; no reason text) |
| INDOFARM | 2026-06-18T11:13:16 | 2026-06-18T22:47:44 | 41,668 s (trade CANCELLED; no reason text) |

- SETL, HARIOMPIPE and AVL carry the reason text: `FIX-179 remediation: placed Live Day 1 11:34-35 IST, system crashed pre-fill; unfilled day-order cancelled by broker at EOD; broker confirms 0 fill / 0 position / 0 holding / full cash; fm_ledger RESERVE-only, no COMMIT`.
- VBB097 has 0 such rows; its maximum CANCELLED `updated_at − placed_at` is 66.09 s.

**(c) One fill was recorded after the window:** COMSYN 2026-07-30 (LFL836), `filled_at − placed_at` = 60.05 s (`trades.order_to_fill_ms` max 60,056).
- 0 COMPLETE ENTRY orders exceed 62 s.
- VBB097 COMPLETE max 58.34 s (n=15). LFL836 COMPLETE n=353, median 9.70 s, p90 43.79 s.
- These are DB write times at the poll, not exchange times: `exchange_timestamp` is NULL on all 635 execution rows.

**No ENTRY order in the DB is in a non-terminal status:** all 773 are CANCELLED or COMPLETE.

**NOT ESTABLISHED:** whether any timeout-cancelled order was later filled broker-side after an accepted cancel. The cancel is marked on the response without re-reading broker state, so such a fill would not appear in these records.

---

## 9. INDEPENDENT RE-CHECK (in place of the adversarial verifier) AND RECONCILED DISAGREEMENTS

Everything below was re-read or re-run directly, after the finders reported. **All matched the finder reports** unless noted.

**Code and config (both trees where applicable)**

| # | Claim re-checked | Result |
|---|---|---|
| V1 | md5 identity: `order_placer.py` c337d5c3 · `order_protocol_limit.py` d675d15e · `full_entry_engine.py` 01060102 · `order_monitor.py` 60ab959e · `entry_gate.py` 44d76479 · `pb01_entry.py` 7e1278fc · `hard_gate.py` dd195d55 identical WT=TW; `signal_processor.py`, `zerodha_adapter.py`, `webhook_receiver.py`, `main.py`, `system_config.yaml` differ | confirmed |
| V2 | `_derive_prices` entry formula WT 1773-1779 / TW 1778-1784 | confirmed |
| V3 | M-S1 condition + re-derive WT 1129/1145-1147, TW 1082/1098-1100 | confirmed |
| V4 | FIX-025 `slippage_buffer` block `order_placer.py` 905-914 | confirmed |
| V5 | FIX-128 guard 1103-1111 (LTP vs `signal_trigger_price`) | confirmed |
| V6 | `_compute_slippage_tolerance` 345-361 / `_slippage_decision` 380-390 | confirmed |
| V7 | FIX-075 `entry_price = current_ltp` at 1261 | confirmed |
| V8 | `LimitTripleProtocol.execute` 210-219 (LIMIT, no trigger) | confirmed |
| V9 | TW `kite.place_order` 639-654 forwards `market_protection`; WT adapter has 0 occurrences of `market_protection` | confirmed |
| V10 | `get_quote_raw` paper `return {}` TW 1816-1817 / WT 1748-1749 | confirmed |
| V11 | `EntryGate.add(` callers: only the docstring `entry_gate.py:103` in both trees (+ a TW comment "DORMANT today") | confirmed |
| V12 | validate then snap, TW 560-569 | confirmed |
| V13 | `if elapsed <= self._fill_timeout: return` (`order_monitor.py` 1097) | confirmed |
| V14 | partial ENTRY immediate cancel 910-913 | confirmed |
| V15 | FIX-141 `_check_price_movement_cancel` 1128 (target-referenced) | confirmed |
| V16 | `final_price = avg_price if avg_price > 0 else entry.expected_price` (`order_monitor.py` 990) | confirmed |
| V17 | FIX-013 TGT recalc from fill (`order_placer.py` 2870) | confirmed |
| V18 | TW config `entry_gate` / `slippage_control` / tiers / overrides lines 644-704 | confirmed |
| V19 | TW `expiry_sec: 600` @127; `poll_interval_sec: 2`, `fill_timeout_sec: 60` @193-194 | confirmed |
| V20 | pb01 `scanner_type: eod` (`scan_webhook_map.yaml:84`); `pb01_breakout_retest.yaml` `enabled: false` @30; `wait_for_retest_enabled: false` @525 | confirmed |
| V21 | the six `pullback_wait_enabled: true` strategies | confirmed |
| V22 | OrderPlacer ctor defaults 572/585/589; TW `main.py` passes none of `liquidity_check_enabled` / `price_drift_threshold` / `default_order_protocol` | confirmed |
| V23 | `age_sec > expiry_sec` TW `webhook_receiver.py:925`; `age_sec > self._signal_expiry_sec` TW `signal_processor.py:917` | confirmed |
| V24 | `order_placer.py` compares `kite_code == 16388` (1359); VM kiteconnect `connect.py:948` `raise exp(data["message"], code=r.status_code)` | confirmed |
| V25 | E1 absence probe: comparison regex of `ltp/last_price/day_low/day_high` vs `sl_price/stop` over 8 entry-path files, both trees | 0 hits |

**Testing-VM data (read-only)**

| Claim re-checked | Result |
|---|---|
| H1: `signals rejection_reason LIKE 'slippage_exceeded%'` | 95 · first 2026-06-23T10:06:11.981227 · last 2026-09-08T10:13:14.918421 · 0 at/after the boundary · all `PLACEMENT_FAILED` |
| H1: `fm_ledger` RELEASE `placement_failed: slippage_exceeded%` / `trades` REJECTED | 95 / 95 |
| Account boundary `config_snapshots` 49-52 | 49 LFL836 2026-09-07T08:15:34 · 50 LFL836 2026-09-08T08:15:32 · 51 VBB097 2026-09-09T11:15:14 · 52 VBB097 2026-09-10T08:15:34 |
| F1: `orders` `COUNT(avg_fill_price)` / `SUM(qty_filled>0)` / total | 0 / 0 / 1452 · ENTRY `COUNT(price)` 0/773 |
| F1: trades filled / with `entry_actual_price` | 368 / 368 |
| H4: `0 < qty_filled < qty_planned` | 0 |
| C4: SL / TGT legs placed before their ENTRY `placed_at` | SL 333 → 0 · TGT 318 → 0 |
| C1: ENTRY `order_type`/`variety` | LIMIT / regular 773, `COUNT(trigger_price)` 0 |
| `trades.mode` | LIVE 954 |
| H3: `order_monitor.fill_timeout` on VBB097 days | 09-09: 9 · 09-10: 8 · 09-11: 14 · 09-15: 1 = 32 |
| A1: live `config/system_config.yaml` md5 after the run | `351bd82e73bb0301d850341191c7b72b` (unchanged) |
| Service start | `ExecMainStartTimestamp=Tue 2026-09-15 08:15:23 IST` |

**Two cross-group disagreements, re-measured on the VM logs (09-03..09-15):**

| Count | Group reports | Measured | Explanation |
|---|---|---|---|
| `order_monitor.force_close_triggered` | D5: 14 · F5: 6 | **6 events** (1 per day on 03, 04, 07, 09, 10, 11 Sep) | "14" counted every line containing the string; each event also writes `circuit_breaker.force_close_triggered: soft_kill, …` and appears again inside kill-switch messages |
| `order_monitor.unknown_status` | D5: 3 · H4: 4 | **4 lines** (07-Sep 1, 08-Sep 1, 15-Sep 2); kite values `CANCEL PENDING` ×3, `OPEN PENDING` ×1 | D5 undercounted the 15-Sep file |

**Not re-checked by the verifier pass:** every other figure and line citation above rests on one finder agent's measured reading, with evidence cited in place.

---

## 10. INDEX

Markers: **WT↔VM** = MATCH / DIFFERS-FILE (file differs, cited logic identical) / **DIFFERS-LOGIC**.

| Q | Status | WT↔VM | Paper↔live |
|---|---|---|---|
| A1 | ESTABLISHED | **DIFFERS-LOGIC** (33 keys; entry-slippage block identical) | DIFFER |
| A2 | ESTABLISHED | MATCH | DIFFER |
| A3 | ESTABLISHED | MATCH | DIFFER |
| A4 | ESTABLISHED | MATCH | DIFFER |
| A5 | ESTABLISHED | MATCH | DIFFER |
| A6 | ESTABLISHED | MATCH | IDENTICAL |
| A7 | ESTABLISHED | MATCH | IDENTICAL |
| A8 | ESTABLISHED | MATCH | DIFFER |
| A9 | ESTABLISHED | **DIFFERS** (18 files) | N/A |
| B1 | ESTABLISHED | **DIFFERS-LOGIC** (WT-only pipeline step; TW-only prefix strip/evidence) | DIFFER |
| B2 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| B3 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| B4 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| B5 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| B6 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| B7 | PARTIAL | **DIFFERS-LOGIC** (`expires_at`) | DIFFER |
| C1 | ESTABLISHED | **DIFFERS-LOGIC** (TW forwards `market_protection`=None) | DIFFER |
| C2 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| C3 | ESTABLISHED | MATCH | IDENTICAL |
| C4 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| C5 | ESTABLISHED | MATCH | DIFFER |
| C6 | ESTABLISHED | MATCH | IDENTICAL |
| C7 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| C8 | PARTIAL | DIFFERS-FILE | IDENTICAL |
| D1 | ESTABLISHED | **DIFFERS-LOGIC** (WT-only pipeline window) | DIFFER |
| D2 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| D3 | ESTABLISHED | **DIFFERS-LOGIC** (signal expiry per pipeline in WT) | DIFFER |
| D4 | ESTABLISHED | **DIFFERS-LOGIC** | DIFFER |
| D5 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| D6 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| D7 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| E1 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| E2 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| E3 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| E4 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| E5 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| F1 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| F2 | PARTIAL | DIFFERS-FILE | DIFFER |
| F3 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| F4 | ESTABLISHED | DIFFERS-FILE | IDENTICAL |
| F5 | ESTABLISHED | **DIFFERS-LOGIC** (daily gate per book in TW) | DIFFER |
| F6 | ESTABLISHED | DIFFERS-FILE | DIFFER |
| G1 | ESTABLISHED | MATCH | NOT IDENTICAL (10 differences) |
| G2 | ESTABLISHED | MATCH | IDENTICAL |
| G3 | ESTABLISHED | MATCH | DIFFER |
| G4 | ESTABLISHED | MATCH | IDENTICAL |
| H1 | PARTIAL (paper NOT ESTABLISHED) | DIFFERS-FILE | DIFFER |
| H2 | PARTIAL (paper NOT ESTABLISHED) | MATCH | DIFFER |
| H3 | PARTIAL (paper + LFL836 full history NOT ESTABLISHED) | DIFFERS-FILE | DIFFER |
| H4 | PARTIAL (paper + proportion NOT ESTABLISHED) | DIFFERS-FILE | DIFFER |
| H5 | PARTIAL (paper + vs-submitted NOT ESTABLISHED) | MATCH | DIFFER |
| H6 | PARTIAL (paper NOT ESTABLISHED) | DIFFERS-FILE | DIFFER |

**Totals:** 52 questions · 43 ESTABLISHED · 9 PARTIAL · 0 wholly NOT ESTABLISHED · 8 DIFFERS-LOGIC (A1, B1, B7, C1, D1, D3, D4, F5) · plus A9's 18-file divergence list.

---

*End of report. Read-only throughout: no file in the working tree was modified other than this report, nothing on the testing VM was modified (temporary `/tmp` query scripts were removed after each run), and the production trading VM was not contacted.*
