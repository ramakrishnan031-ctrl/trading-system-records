**§11.7 — WEEKLY DATA IS NEVER FETCHED, for any symbol, in either book. §3's three-timeframe level object is therefore a BUILD, not a config change.**

# The 05-Sep contract, PART TWO minus §10 — the §11 source inventory and the §12 corpus replay

- **Date:** 11-Sep-2026 (Fri) IST. Instruction files: the 13:40 file (delivered 13:40:54) and the 15:10 file (delivered 15:07:27); header times are labels, not evidence.
- **Read-only throughout.** Source pinned to git **`970aabf`** (= origin/main = production's deployed files). Production's running process is `d3ee69d`; the two differ only in the 10 Batch-1 files — where a cited line sits in one of those (`main.py`, `screening/secondary_screener.py`, `signals/signal_processor.py`), `[n]` or `(n)` is the same line at `d3ee69d`.
- **Measurements:** four read-only passes, 13:45–14:08 IST — SQLite opened only as `file:…?mode=ro`, no broker call, no project script on a VM, nothing written. ⚠️ Those passes were run as subagents, which 👤 Rama has since prohibited as a standing rule. This report was assembled by me, in the main thread, from their four findings files (durable copy: `docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/`).
- **Checked by me after drafting:** (1) by script, every number, `path:line` citation, id, time and quote in the draft against the findings folder — the four findings files and the 28 files beside them (the harness, the scans, the VM query outputs, the source exports): 399 numbers, 111 citations, 101 bare line references, 12 hex ids, 41 times, 12 quotes. Outside that folder were only the Q6 figures and the twin's restart time (both in the ledger), the 13:40:54 delivery time (the transcript) and nine citations — all nine confirmed in the source. (2) The load-bearing source, re-read by me with `git show 970aabf:` at 15:36:46 IST: `sr_detector/pivots.py:1-16, :40-44` · `sr_detector/fetch.py:118-128` · `sr_detector/flags.py:123-147` · `sr_detector/detector.py:1-20` · `core/config_loader.py:1243-1256, :1474-1480` · `config/system_config.yaml:506-518, :610-616` · `config/scoring_weights.yaml:8-30, :37-40` · `screening/quality_scorer.py:14-20, :100-110` · `screening/secondary_screener.py:314-324, :408-420` · `screening/step_executor.py:248-300, :330-338, :388-398`; and at 15:38 `strategies/schema.py:108-118`, `signals/signal_processor.py:1072-1084` (`d3ee69d` :964-974), `orders/order_placer.py:2174-2194`. Every line re-read matches what this report says of it.
- ⛔ **No recommendations. No threshold selection — every [A] stays [A]. No design.** Rama decides from measured numbers.

---

## The headline, measured

1. **§11.7 — weekly is never fetched; and there is no MIS/GTT timeframe split at all.** One global list, **30m + 1H + 1D** (`config/system_config.yaml:510`), for both books; the detector never reads the product; all 2,541 recorded V3 requests (1,904 INTRADAY, 637 DELIVERY) asked for exactly those three. The validator refuses `week` (`core/config_loader.py:1246`), so adding it fails config load and the boot exits 5. Only 1-minute candles are stored; nothing resamples. ⇒ §3 is a **build**.
2. **287.80 was invisible to INDOCO's decision for THREE independent reasons** (full treatment in §12.1): (1) no weekly data at all; (2) the weekly highs behind Rama's line fall outside the 180-day window; (3) 287.80 printed at 13:52 and was still inside the last bar of every timeframe at 14:09, and `pivots.py:42` never turns the last five bars into a level — a **locked design decision** (SR-P2), not an accident. §3 fixes only (1); the 400-day lookback [A] fixes (2); nothing in the contract fixes (3) — **so the contract's central example would still fail after §3 is built.**
3. **The scorer's reachable ceiling is 65**, not 80 — two steps dead at 0 and two pinned at half (35 points unreachable); 15 rows have reached it. The passing band is **six values, 60–65**; tier HIGH (80) is unreachable; MEDIUM (65) only at the exact ceiling. INDOCO passed at **62**, two points of headroom, lifted by the spread check.
4. **The contract's own INDOCO/KOTAKBANK facts are wrong in three places**: the entry was 276.83, not ~281.48; the stop hit the same day, not the next; KOTAKBANK was never a trade the system took — so the corpus's "all 56 are system trades" is not true of at least one (registered S11-R26).
5. **Scanners:** I ≡ XV byte-identical; **IV and V have never fired** (0 across 62 audit dates, 0 of 232,113 signals); the duplicates setting is recorded for only **4 of 16** (Duplicate: I, V, XI · Unique: XVI); **12,069 webhook 403s fell inside the entry window**, with no stored reason (registered S11-R27).

---

## §1 — Why §10 is blocked (so nobody re-asks)

§10 applies L3 and structural R:R to the forward-shadow record from 14-Jul and stops if the rejected trades were mostly winners. **It cannot run, and the block is measured, not assumed.** The corpus is a reconstruction, not a capture: Q6 (measured 09-Sep) found **168,290 rows** over 40 dates (13-Jul → 08-Sep), `method_version = fs-v1` throughout, in a fixed 20-key schema with no `_broken_zone`, no ATR, none of the decision's actual inputs, no signal-time entry price and no S&R level identity; `computed_at − ts` runs from **3.28 h** to **13.66 h** (median **5.17 h**), so 168,290 of 168,290 (100.00 %) were computed more than an hour after the signal — an 18:15 batch reconstruction. Outcomes are almost absent: `realized_pnl` exists on **222 of 168,290 rows — 0.132 %, one in 758** — and §10's question needs realized outcomes. And there is no live L3 gate: every L3 match in runtime code is an unrelated decision id, and the V3 gates (confirmation, pullback, R:R, strong-HTF, extreme) are shadow-mode and never reject a live order (`v3_chain/runner.py:5`: *"LOG-ONLY — the verdict never rejects/delays/alters a live signal or order"*). ⇒ **§10 becomes answerable only after the evidence contract accumulates:** Batch 1 loaded on the testing VM at its 09:16:44 restart (first row 10:00:07.50; 5,618 rows by 14:59:21) and loads on production at Monday's 08:15 boot — that is the clock. ⛔ No proxy, reconstruction or sim_R: sim_R cannot replace realized R (ChatGPT's ruling), and using it would recreate the proxy problem that killed the historical backfill.

---

## §11.7 — S&R detector timeframes

| | 👤 Rama believes | Source @970aabf | Production records |
|---|---|---|---|
| MIS (INTRADAY) | 1H + 1D | **30m + 1H + 1D** | `would_be.jsonl` INTRADAY: **1,904 / 1,904** requested exactly {30minute, 60minute, day} |
| GTT (DELIVERY) | 1D + 1W | **30m + 1H + 1D — the same list** | DELIVERY: **637 / 637** requested exactly {30minute, 60minute, day} |
| A per-product split | implied | **none** — one global list; nothing reads the product | the 3 DELIVERY strategies carry the same 3 labels as the 10 INTRADAY ones |
| 1W | fetched for GTT | **never fetched, never resampled, never stored, for any symbol** | **0** weekly labels across 666 detector rows, 2,541 + 214 V3 records and 857 watchlist rows |

**E1 — one list, global, in config.**
```
config/system_config.yaml:510   timeframes: ["day", "60minute", "30minute"]  # structure TFs (one historical fetch each)
config/system_config.yaml:511   lookback_days: 180          # 6 months back (fits one request per interval)
config/system_config.yaml:613   structure_intervals: ["day", "60minute", "30minute"]      (v3_chain block)
```
The model defaults are the same values (`core/config_loader.py:1164` SRDetectorConfig; `:1477-1478` V3ChainConfig). No other structural timeframe list exists in `config/` or any strategy YAML.

**E2 — the validator refuses a weekly entry, and the boot stops.**
```
core/config_loader.py:1243-1255   (SRDetectorConfig._validate_timeframes)
    allowed = {"day", "60minute", "30minute", "15minute", "5minute"}          ← :1246
    raise ValueError("sr_detector.timeframes has unsupported intervals %s; allowed %s" ...)
main.py:2198-2201   app_config = load_all(config_dir) … except → _log.critical("Config load failed …") → return 5
```
A test pins it: `tests/unit/test_sr_detector_units.py:197` `SRDetectorConfig(timeframes=["weekly"])  # unsupported interval rejected`.

**E3 — the set is read once at construction, never per product, strategy or signal.** `sr_detector/zone_builder.py:42`, `sr_detector/detector.py:96` (`self._intervals = list(self._knobs.intervals)`), `:168` (`fetch_timeframes(candidate.symbol, self._intervals)`). The product is carried to the detector and ignored: `sr_detector/models.py:142` `intent: str  # "INTRADAY" | "DELIVERY"` is the only `intent` hit in `sr_detector/`.

**E4 — the fetch path.** Every structural fetch goes through one closure, `main.py:421-438` → `market_kite.historical_data(...)`; `sr_detector/fetch.py:123-125` (`from_dt = now - timedelta(days=lb)`). Caching is in-process only, TTL 1,800 s. `sr_detector/detector.py:18`: *"No long-term candle storage (fetch → analyse → discard + the session cache)."* The only intervals any code path requests are day / 60minute / 30minute (structure), 5minute (anchors — off; the PB-01 poll; the regime engine — off) and minute (V2 — off; the cron scripts). No `week`.

**E5 — nothing aggregates daily bars into weeks.** `core/candle_math.py:378-383` (the only resampler) accepts minutes or `"day"`; `resample(` has 0 production callers; `tests/unit/test_candle_math.py:496` pins `"week"` → ValueError.

**E6 — no stored series is weekly, or even daily.** The only candle table is `analytics.db` `candles`: 1,726,404 rows, 2026-06-19 → 2026-09-10, `interval_sec = 60` on 100,002 / 100,002 sampled rows; both writers hard-code 60. `data_store/candles/` holds 57 one-minute CSVs. The structural 30m/60m/day bars exist only in process memory for ≤ 1,800 s.

**E7 — production requested and labelled only those three.** `sr_detector_results` (666 rows, 29-Jun → 11-Sep): labels `30minute` 11,871 · `60minute` 11,007 · `day` 2,790 · anything else **0**.

**Facts bearing on "config change or build" (stated, not recommended):** the detector cannot take a week (E2); the V3 chain's `structure_intervals` has **no** interval validator (`core/config_loader.py:1477-1478`), so a `week` entry would pass config load and reach `kite.historical_data(interval="week")` via `main.py:432-437` — whether Kite serves that interval **cannot be measured** without a broker call; the daily series is 180 days (`:511`, `:614`) — the contract's 400-day lookback [A] appears nowhere in the S&R path (the only 400 is `regime.daily_lookback_days`, `:551`, the NIFTY index, disabled); `TF_ROLE` (`sr_detector/models.py:180-186`) has no weekly role.

---

## §11.8 — The context-layer inventory

The order path (@970aabf, [d3ee69d]): screen `signal_processor.py:998` [892] → derive entry/SL `:1028` [922] → V2 divert (not built) `:1042` [936] → fresh LTP when `pullback_wait_enabled=false` `:1082-1106` [972…] → sizing `:1118` [1007] → V3 enqueue `:1138` [1027] → admit/reserve `:1182` [1070] → **`self._placer.place(` `:1446` [1302]** → PROCESSED `:1543` [1399] → S&R observe `:1550` [1406].

| Component (status) | What · when | Stored | Recomputed per signal? | **At order time?** | Timeframe | Trust (measured) |
|---|---|---|---|---|---|---|
| **S&R detector V1** (running, shadow) | pivots → zones → confluence → nearest R/S, flags; **after placement** (row p50 0.62 s after the post-placement candidate ts) | `sr_detector_results` (666) | yes, per placed candidate; candles reused ≤ 1,800 s | **NO** | day + 60m + 30m, 180 d, pivot N = 5 | `FETCH_FAILED` 46 / 666 (6.9 %); right-edge blind (last 5 bars of each TF, SR-P2); no as-of truncation (the breakout flags read the forming 30m bar); the broken level (`_broken_zone`, `flags.py:125-135`) is computed then discarded |
| **S&R V2 ZoneWarmer / RetestMonitor** | the same zones, cached for a pre-placement read | memory; `retest_state` 0 rows | n/a | **NO** — not constructed (`main.py:3549` [3515]; `wait_for_retest_enabled: false` `:529`) | day + 60m + 30m | — |
| **V3 decision chain** (running, shadow, LOG-ONLY) | S&R from as-of-truncated series, ATR30, 1h EMA20, gates; async: p50 0.88 s · p90 4.09 s · max 16.31 s after the decision | `data_store/v3/would_be.jsonl` (2,541) | yes, per sized signal; candles reused ≤ 1,800 s | **NO** (never read by the order path) | day + 60m + 30m, 180 d | `nearest_resistance` null on 1,088 / 2,541 (42.8 %); verdicts WOULD_REJECT_RR 2,182 · WOULD_REJECT_HTF 281 · WOULD_PASS_GATES 78 |
| **ATR** | order-time slot hardcoded `None` (`secondary_screener.py:412-415` [410-413]); ATR30 only in V3 / PB-01 (shadow) | `screener_results $.atr`: **0 numeric of 195,109**; `daily_symbol_stats` 0 rows (its writer script does not exist) | slot: constant `None` | **NO** | slot: none | `atr_filter` → 0.0 always (`step_executor.py:275-278`); SL "ATR" falls back to FIXED_PCT (`signal_processor.py:1802-1811` [1634-1643]) |
| **Swing detection** | ±N-bar extreme, inside V1 / V3 / PB-01 | only as zones | per consumer | **NO** | V1 N = 5 all TFs; V3 G-HTF 60m N = 3 | `pivots.py:14-15`: *"The first `left` and last `right` bars can never be pivots"* |
| **Level storage** | zones (V1, V3), PB-01 LEVEL, parked retests | tables / JSONL | per consumer | **NO** | — | **the contract §3 level object is absent** — 0 matches for `reference_level_id · reference_timeframe · reference_type · reference_quality · distance_to_entry/target/stop` |
| **VWAP** (running) | the quote's `average_price` | `$.vwap` numeric on **186,544 / 186,544** | yes (fresh quote) | **YES** | session | `step_executor.py:263-269` |
| **EMA / SMA** | EMA20 on 60m (V3, PB-01); EMA50/200 daily (regime, not built) | not persisted | per consumer | **NO** | 60m; daily (off) | no SMA function exists |
| **Scorer** (running, gates) | 10 weighted steps → 0–100, tier, pass ≥ 60; at screening | `screener_results` | yes | **YES — it gates and it sizes** | quote/session fields + clock; **no candle series** | ceiling 65 (§11.3) |
| **Candle geometry** | day-bar body % (live); breakout flags (V1, post-placement); body_frac on 5m (PB-01, shadow); strong close on 1m (dormant) | `step_results.price_action` | per consumer | **only the day-bar body %** | the forming daily bar | no named-pattern classifier exists (0 functions for engulfing, doji, marubozu, pin, hammer, inside bar, harami) |
| **Regime engine** | NIFTY direction / volatility | — | n/a | **NO** (`regime.enabled: false`, `:548`) | daily 400 d + 5m | — |

**At the order instant the decision holds:** quote fields (ltp, bid, ask, volume, vwap, open, day_high, day_low, circuit), the 10-step score and tier, the trigger price, a fresh LTP for `pullback_wait_enabled=false` strategies, and the strategy's FIXED_PCT SL and R:R target. **No structural input exists before `self._placer.place(`: no level, no ATR, no pivot, no EMA.**

---

## §11.1 — `pullback_wait_enabled / tolerance_pct / timeout_sec`: real or dead?

- **`pullback_wait_enabled` is REAL, but it makes nothing wait.** Its one reader, `signals/signal_processor.py:1082 @970aabf (:972 @d3ee69d)`: `if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:` — `false` ⇒ entry and SL are re-derived from the live LTP (the FIX-067 re-anchor; **384** re-anchor log lines over the 8 logged days); `true` ⇒ no re-anchor. The comment at `:1074-1075 (:968-969)` — *"Pullback strategies skip this (EntryGate already waits for current price)"* — is false at this SHA.
- **`pullback_wait_tolerance_pct` and `pullback_wait_timeout_sec` are DEAD** — zero readers (`strategies/schema.py:112-113` declarations and validators only).
- **The pullback wait has never fired.** `EntryGate` is constructed and started on every boot (`main.py:3839-3844` [3804-3809], `:3975` [3940]), but **nothing calls `EntryGate.add()`** (`screening/entry_gate.py:288`), and `git log -G'entry_gate\.add\('` finds no commit that ever added a call. 0 of 232,208 signals (since 2026-06-12) ever carried a waiting / released status (control on the same index: `REJECTED_SCORE_*` = 160,795); **50,084** EntryGate poll lines in the 8 debug logs, every one `0 entries checked`. Logs on disk go back only to 2026-09-02.
- **§5 WATCHING — which half exists:** EntryGate holds the **consumer half** (hold, persist, poll, confirm, expire, resume via `continue_from_gate`) with **no producer**; the SNR-V2 retest path has **both halves** but is config-disabled and has never been constructed. Neither has §5's candidate identity (`symbol + family + direction + reference_level`), a capacity bound, or invalidation when the alert stream stops.

---

## §11.2 — `gap_fade_long.yaml`: the full field inventory

**36 top-level keys, not 37** (`config/strategies/gap_fade_long.yaml` lines 5–56). No enumeration — keys, leaf scalars (40), lines (41/45), schema fields (41 = 36 + 5 absent) — and no historical version (32, 33, 34, 35, 34, 36 keys across 15 versions) gives 37.

| # | FIELD = value | STATUS | READER @970aabf `(d3ee69d)` | EFFECT |
|---|---|---|---|---|
| 1 | `name` | READ-EFFECTIVE | `strategies/loader.py:149`, `:208` | identity key |
| 2 | `display_name` | READ-DISPLAY-ONLY | `ops_dashboard/backend/readers/config_reader.py:69` | label |
| 3 | `description` | WRITTEN-NEVER-READ | — | none |
| 4 | `direction` = LONG | READ-EFFECTIVE | `signal_processor.py:1034-1035 (:928-929)`, `:1775 (:1607)`, `:1000 (:894)` | side, entry/SL direction |
| 5 | `intent` = INTRADAY | READ-EFFECTIVE | `strategies/control.py:76, :100`; `signal_processor.py:1117 (:1006)` | trade-type gate; MIS margin |
| 6 | `enabled` = true | READ-EFFECTIVE | `strategies/control.py:77, :81-83` | may trade |
| 7 | `order_protocol` = CO_PLUS_TGT | **READ-DISPLAY-ONLY** | only `config_reader.py:79`; the placer picks `self._default_protocol` = `"LIMIT_TRIPLE"` (`orders/order_placer.py:960-961`, `:572`) | **none** — 24 / 24 gap_fade_long trades and 947 / 947 of all trades ran LIMIT_TRIPLE |
| 8 | `pipeline` | READ-DISPLAY-ONLY | `strategies/taxonomy.py:35` ("METADATA + DISPLAY ONLY") | label |
| 9 | `horizon` | READ-DISPLAY-ONLY | same | label |
| 10 | `entry_method` = LIMIT | READ-EFFECTIVE | `signal_processor.py:1779 (:1611)` | enables the offset |
| 11 | `entry_offset_pct` = 0.001 | READ-EFFECTIVE | `:1780-1782 (:1612-1614)` | entry 0.1 % below trigger / live LTP |
| 12 | `sl_method` = FIXED_PCT | READ-EFFECTIVE | `:1801, :1813 (:1633, :1645)` | FIXED_PCT; the ATR branch never entered |
| 13 | `sl_pct` = 0.01 | READ-EFFECTIVE | `:1814, :1837 (:1646, :1669)` | SL = entry × 0.99 (24 trades: 20 exact, 4 within 1.07e-4) |
| 14 | `sl_atr_multiplier` = 1.5 | **WRITTEN-NEVER-READ** | `schema.py:87` + `:222` only | none |
| 15 | `sl_min_pct` = 0.003 | READ-NON-BINDING | `:1852-1861 (:1684-1693)` | cannot bind (schema forces `sl_min_pct ≤ sl_pct`) |
| 16 | `sl_max_pct` = 0.05 | READ-NON-BINDING | `:1862-1871 (:1694-1703)` | same |
| 17 | `sl_gap_buffer_pct` = 0.3 | **READ-UNREACHABLE** | `:1877-1893 (:1709-1725)`, 09:15–09:30 only | the 10:00 entry floor (`system_config.yaml:28`) rejects earlier; 0 widened SLs in 947 trades |
| 18 | `tgt_method` = RISK_REWARD | READ-EFFECTIVE | `:1911, :1930 (:1743, :1762)` | TGT = entry + 1.5 × SL distance |
| 19 | `tgt_pct` = 0.0 | READ-UNREACHABLE | `:1924-1929 (:1756-1761)` | none |
| 20 | `tgt_risk_reward` = 1.5 | READ-EFFECTIVE | `:1932 (:1764)`; `order_placer.py:2872-2878` | applied 1.5 × 20, NULL × 4 |
| 21 | `tgt_atr_multiplier` = 2.5 | **WRITTEN-NEVER-READ** | `schema.py:96` + `:222` | none |
| 22 | `smart_tgt_enabled` = true | **WRITTEN-NEVER-READ** | `schema.py:99` | none — trailing is global and needs CO_PLUS_TGT; `smart_tgt_state` 0 rows |
| 23 | `smart_tgt_trail_trigger_pct` | **WRITTEN-NEVER-READ** | `schema.py:100` + `:236` | the global value is used (`order_placer.py:2230`) |
| 24 | `smart_tgt_trail_step_pct` | **WRITTEN-NEVER-READ** | `schema.py:101` + `:236` | global (`order_placer.py:2231`) |
| 25 | `pullback_wait_enabled` = false | READ-EFFECTIVE (not what the name says) | `signal_processor.py:1082 (:972)` | the re-anchor runs; no wait exists |
| 26 | `pullback_wait_tolerance_pct` | **WRITTEN-NEVER-READ** | `schema.py:112` + `:236-242` | none |
| 27 | `pullback_wait_timeout_sec` | **WRITTEN-NEVER-READ** | `schema.py:113` + `:272-277` | none |
| 28 | `min_score` = 0 | **READ-OVERRIDDEN** (sentinel) | `secondary_screener.py:317-321 (:315-319)` | 0 ⇒ the global 60 |
| 29 | `min_volume_surge` = 1.3 | **READ-UNREACHABLE** | `:236 (:234)` → `step_executor.py:255` | `avg_volume_20d` is hardcoded `None` ⇒ `volume_surge` = 0.0 on 173,761 / 173,761 |
| 30 | `min_adr_pct` = 0.005 | **READ-UNREACHABLE** | `:237 (:235)` → `step_executor.py:280` | `atr` hardcoded `None` ⇒ 0.0 always |
| 31 | `max_spread_pct` = 0.005 | READ-EFFECTIVE, **unit mismatch** | `:238 (:236)` → `step_executor.py:393-395` | a spread in **percent** is compared with 0.005 ⇒ passes only at ≤ 0.005 %: `spread_check` 1.0 on 1,421, 0.0 on 172,340 scored rows |
| 32 | `lot_size` = 1 | **READ-OVERRIDDEN** (sentinel) | `signal_processor.py:1119 (:1008)` → `capital/position_sizer.py:309-311` | defers to the instrument cache |
| 33 | `max_concurrent_positions` = 3 | READ-EFFECTIVE | `signal_processor.py:760, :773-779 (:654, :667-673)` | never reached for this strategy (0 `REJECTED_STRATEGY_POSITION_LIMIT`) |
| 34 | `entry_start_time` = "09:25" | **READ-OVERRIDDEN** | `core/market_windows.py:169, :175` | the global 10:00 floor is checked first |
| 35 | `entry_end_time` = "15:00" | READ-COINCIDENT | `market_windows.py:170, :175` | equals the global 15:00 |
| 36 | `active_days` | **WRITTEN-NEVER-READ** | `schema.py:139` + `:286-296` | none |
| 37–40 | `trailing_sl_*` (absent) | ABSENT → read / unreachable | `order_placer.py:2178`, `:2190-2192` | BreakevenManager never registered |
| 41 | `v3_playbook` (absent) | ABSENT → shadow consumers only | `main.py:3648 (:3613)`; `signal_processor.py:1603 (:1459)` | no live effect |

**Class counts (36 present keys):** READ-EFFECTIVE 13 · READ-COINCIDENT 1 · **READ-OVERRIDDEN 3** · READ-UNREACHABLE 4 · READ-NON-BINDING 2 · READ-DISPLAY-ONLY 4 · **WRITTEN-NEVER-READ 9**. ⇒ **Defined but never read:** 9 with no reader + 4 display-only = 13 with no trading-path reader (among them `order_protocol`). **Read but overridden or neutralised:** 3 overridden + 4 unreachable + 2 non-binding = 9.

---

## §11.3 — `min_score` across all strategies, and the scorer arithmetic

**Enforcement path** (`screening/secondary_screener.py:316-323 @970aabf (:314-321 @d3ee69d)`):
```
effective_min = (strategy.min_score if strategy.min_score > 0 else score_result.min_pass_score)
if total_score < effective_min:
    status = f"REJECTED_SCORE_{total_score}"
```
- **All 16 YAMLs carry `min_score: 0`, not just gap_fade_long**, and in code 0 is a "use global" sentinel (`strategies/schema.py:116`) ⇒ the only operative threshold is the global `min_pass_score` **60** (`config/scoring_weights.yaml:22`; 55 on the 13,082 earliest rows). `screener_results.eligible_score` has only ever held 55, 60 or NULL ⇒ **all 16 per-strategy `min_score` values are inert.** The V3 re-scale path needs `v3_hardgate_mode == "enforce"`; it is `"shadow"` (`scoring_weights.yaml:39`).

**The scorer arithmetic (the 15:10 file §4, checked against the source — the source corrects one figure):**

| Step | Weight (`scoring_weights.yaml`) | Live input (`secondary_screener.py`) | Fixed result (`step_executor.py`) | Max points |
|---|---|---|---|---|
| volume_surge | 15 (`:11`) | `avg_volume_20d: None` (`:417` [415]) | 0.0 (`:251-253`) — 173,761 / 173,761 | **0** |
| atr_filter | 10 (`:13`) | `atr: None` (`:413` [411]) | 0.0 (`:275-278`) | **0** |
| rsi_range | 10 (`:14`) | `rsi: None` | **0.5** (`:296-298`) | **5** |
| sector_strength | 10 (`:16`) | `sector: None` | **0.5** (`:335-336`) | **5** |
| vwap_position · price_action · time_of_day · spread_check · circuit_check · signal_age | 10 · 15 · 5 · 5 · 10 · 10 | live | vary | 55 |
| **Total** | 100 | | `quality_scorer.py:107` `(total_achieved / total_weights_present) * 100.0` — all 10 steps always run, denominator 100 | **65** |

- ⚠️ **The 15:10 file says "FOUR steps are dead … 40 of the 100 weight". The source says two are dead (volume_surge 15 + atr_filter 10 = 25) and two are pinned at half (rsi_range, sector_strength: 20 × 0.5 = 10 lost) — 35 unreachable, ceiling 65.** The code states it itself, `screening/quality_scorer.py:16-19`: *"the G2 achievable ceiling — 25/100 pts dead-at-0 + 20 pinned-at-half make >65 algebraically impossible today."* `_G2_CEILING_TRIPWIRE = 65`.

**The five numbers side by side** (all measured; thresholds `scoring_weights.yaml:22 / :28 / :29`):

| | value | what it means (measured) |
|---|---|---|
| theoretical ceiling | **65** | 35 points unreachable (above) |
| all-time maximum | **65** | 0 of 173,756 scored rows exceed 65; **15 rows sit exactly at 65** ⇒ the ceiling has been reached |
| `medium_score_threshold` | **65** | reachable only at the exact ceiling — MEDIUM **15** of 195,109 rows (LOW 195,094 · HIGH 0) |
| `min_pass_score` | **60** | 5 points below the ceiling |
| `high_score_threshold` | **80** | **mathematically unreachable** — tier HIGH can never be assigned |

- **The usable range is six integer values, 60–65.** Scored-row distribution (n = 173,756 at 13:59 IST): ≤54 41,129 · 55 3,144 · 56 3,335 · **57 84,060** · 58 1,126 · **59 36,661** · **60 3,219 · 61 14 · 62 800 · 63 6 · 64 247 · 65 15** · >65 0. Rows ≥ 60: **4,301 (2.48 %)**; score 57 alone is 48.4 %, 59 is 21.1 %.
- **§8's "fit the threshold from a sensitivity curve" — above the current pass mark the curve has six points.** Admitted rows at thresholds 60 / 61 / 62 / 63 / 64 / 65 = **4,301 / 1,082 / 1,068 / 268 / 262 / 15** (cumulative from the distribution above). Below 60 the curve extends into the rejected mass (59: +36,661; 57: +84,060 more).
- **INDOCO as the concrete illustration:** it passed at **62 against 60** — two points of headroom on a six-value scale — and the only step separating it from its nine neighbouring INDOCO screener rows (13:53–14:17, all 57 or 52) was `spread_check` = 1.0, the unit-mismatched step that passes on 0.82 % of rows (§11.2 item 31; §12).
- ⛔ The scorer is not repaired: it changes which signals pass, and the evidence contract started collecting this morning.

Per strategy (scored rows · max · rows ≥ 60): vwap_bounce_long 53,569 · 65 · 1,335 (2.49 %) · positional_sector_rotation 29,597 · 65 · 659 · first_pullback_long 18,300 · 65 · 423 · vwap_rejection_short 16,711 · 64 · 282 · gap_go_long 12,383 · 65 · 490 · positional_momentum_long 11,523 · 65 · 282 · first_pullback_short 8,253 · 65 · 143 · open_low_breakout_long 7,649 · 65 · 269 · positional_swing_long 6,248 · 65 · 182 · gap_fade_short 2,864 · 64 · 68 · gap_go_short 2,633 · 64 · 61 · **gap_fade_long 2,540 · 64 · 64 (2.52 %)** · open_high_breakdown_short 1,487 · 64 · 43 · range_breakout_long / _short **0** (0 signals ever) · pb01_breakout_retest 0 (disabled).

---

## §11.4 — Strategy-wise SL, all 16

- ⛔ **No clean fallback hierarchy exists — none is invented here.** All **16** strategies declare `sl_method: FIXED_PCT`; `sl_pct` is the sole determinant of the initial SL; ATR SL is unimplemented (`sl_atr_multiplier` has zero readers); **no structural level enters the live SL** for any strategy.
- **What exists is a one-way ladder that ends in FIXED_PCT** (`signals/signal_processor.py @970aabf`, identical block @d3ee69d at −168): (1) `:1801-1811` ATR → WARN *"sl_method=ATR not yet implemented; falling back to FIXED_PCT"*; (2) `:1813-1839` FIXED_PCT: `sl_price = entry_price * (1.0 ∓ sl_pct)`; (3) `:1852-1871` clamp to `[sl_min_pct, sl_max_pct]` — cannot bind (`schema.py:308-312`); (4) `:1877-1893` gap buffer 09:15–09:30 — unreachable under the 10:00 floor.
- **After the fill the SL stays put** (`orders/order_placer.py:2870-2875`, FIX-013); every post-entry mover is off or unreachable (BreakevenManager needs the absent `trailing_sl_enabled`; SmartTgt needs CO_PLUS_TGT, 0 trades; StructureExit `structure_exit_enabled: false`, `:634`).
- **Structural SL definitions exist only in shadow or disabled code:** V3 G-RR (`screening/hard_gate.py:240-282`, LOG-ONLY), PB-01 (`v3_chain/pb01_runner.py:131-135`, disabled), `continue_from_retest` (`signal_processor.py:2437-2442`, never constructed), `sr_detector/detector.py:290` `proposed_retest_sl` (annotation).

The reader, for every row: the FIXED_PCT branch, `signals/signal_processor.py:1813-1839` @970aabf (`:1645-1671` @d3ee69d). Values from `config/strategies/*.yaml` @970aabf (`yaml_table_970aabf.txt` in the evidence folder); `sl_method` and `sl_atr_multiplier` added after the draft, each row's intent, `sl_pct` and bounds checked against that table first.

| Strategy | intent | `sl_method` | `sl_pct` | `sl_atr_multiplier` (0 readers) | `sl_min` / `sl_max` | structural definition (live) | trades | enforced? — planned SL distance vs `sl_pct`: exact / ≤ 1.07e-4 / other |
|---|---|---|---|---|---|---|---|---|
| first_pullback_long | INTRADAY | FIXED_PCT | 0.015 | 1.5 | 0.003 / 0.05 | none | 128 | 108 / 20 / 0 |
| first_pullback_short | INTRADAY | FIXED_PCT | 0.015 | 1.5 | 0.003 / 0.05 | none | 30 | 29 / 1 / 0 |
| gap_fade_long | INTRADAY | FIXED_PCT | 0.01 | 1.5 | 0.003 / 0.05 | none | 24 | 20 / 4 / 0 |
| gap_fade_short | INTRADAY | FIXED_PCT | 0.01 | 1.5 | 0.003 / 0.05 | none | 41 | 35 / 6 / 0 |
| gap_go_long | INTRADAY | FIXED_PCT | 0.012 | 1.5 | 0.003 / 0.05 | none | 117 | 104 / 13 / 0 |
| gap_go_short | INTRADAY | FIXED_PCT | 0.012 | 1.5 | 0.003 / 0.05 | none | 18 | 16 / 2 / 0 |
| open_high_breakdown_short | INTRADAY | FIXED_PCT | 0.01 | 1.5 | 0.003 / 0.05 | none | 13 | 13 / 0 / 0 |
| open_low_breakout_long | INTRADAY | FIXED_PCT | 0.01 | 1.5 | 0.003 / 0.05 | none | 90 | 83 / 7 / 0 |
| pb01_breakout_retest (disabled) | INTRADAY | FIXED_PCT | 0.01 | 1.5 | 0.003 / 0.05 | none | 0 | — |
| positional_momentum_long | DELIVERY | FIXED_PCT | 0.02 | 2.0 | 0.005 / 0.08 | none | 53 | 53 / 0 / 0 |
| positional_sector_rotation | DELIVERY | FIXED_PCT | 0.02 | 2.0 | 0.005 / 0.08 | none | 122 | 105 / 17 / 0 |
| positional_swing_long | DELIVERY | FIXED_PCT | 0.02 | 2.0 | 0.005 / 0.08 | none | 36 | 33 / 3 / 0 |
| range_breakout_long / _short | INTRADAY | FIXED_PCT | 0.01 | 1.5 | 0.003 / 0.05 | none | 0 | — (0 signals ever) |
| vwap_bounce_long | INTRADAY | FIXED_PCT | 0.008 | 1.5 | 0.003 / 0.05 | none | 213 | 204 / 9 / 0 |
| vwap_rejection_short | INTRADAY | FIXED_PCT | 0.008 | 1.5 | 0.003 / 0.05 | none | 62 | 59 / 3 / 0 |

**Enforced:** planned SL on all 947 trades — 862 exact, 85 within 1.07e-4, **0 other, 0 gap-widened**; every broker MIS SL leg's `trigger_price` equals `sl_initial` (321 / 321 trades); 56 / 56 delivery GTT SL triggers within one tick; 0 SL orders superseded; 0 trades trailed.

---

## §11.5 — The three scanner findings, verified (scanners frozen; verified is not changed)

The only readable copy of the scanner condition text is `C:/Users/rama/Downloads/discussion/Chartink_scanners.v2.txt` (sha256 `11c473a4…`; a byte-identical copy in `Downloads/candles/`). The repo at 970aabf holds no condition text (`docs/locked_decisions.yaml:372` P17: *"NOT parsing Chartink scan conditions"*).
- **(a) I vs XV: BYTE-IDENTICAL.** Both 10-line condition blocks hash to sha256 `89b8844633927ac2…c85af92498` (whole bodies `04bd87e0…` both); only the headings differ; the only identical pair of the 16. **Production agrees:** from 13-Jul the two sent identical stock sets in every minute both posted (**2,333 / 2,333**); before 13-Jul in none (0 / 230).
- **(b) IV / V `Max(15)`: CONFIRMED as text — no `1 day ago` offset.** IV L51-52 / V L68-69: `Daily Max(15, Daily High)` / `Daily Min(15, Daily Low)` written bare, while II, III and XVI write `1 day ago Max(…)`. **The zero is measured; the mechanism is inferred — kept apart:** *if* Chartink's bare window includes today's bar, clause 2 of each can never be true (`Max(15, High) ≥ High ≥ Close`); **no readable source documents that rule.**
  **Live hits, IV and V: ZERO everywhere** — 0 `webhook_audit` rows under any response code on all **62** retained dates (2026-06-15 → 09-11); **0 of 232,113 signals; 0 of 947 trades**; no 401 / 404 rows at all (so no POST under an unknown name reached the receiver). The audit table keeps 90 days; 72,583 older rows are gone.
- **(c) XVI: CONFIRMED — no retest condition.** Its 8 clauses are breakout (close above the prior 20-bar high), trend, close > open, volume and price band; 0 hits for retest / pullback / touch / hold / support tokens. The retest lives in the system's pb01 config (`pb01_breakout_retest.yaml:26`, `enabled: false`).

---

## §11.6 — Scanner configuration

**Recorded settings (second-hand transcriptions; live Chartink state cannot be read — login is barred):**

| # | scanner | frequency | after trigger | **duplicates** | recorded in |
|---|---|---|---|---|---|
| I | positional_swing_long | 1 minute | Continue | **Duplicate** | `discussion/TRADING_RULES_FROZEN_SPEC_AND_CROSSCHECK.txt:72-73` |
| V | range_breakout_long | 1 minute | Continue | **Duplicate** (never posted) | `docs/audit/PHASE_A_REPORT_05-Sep-2026.md:70` (untracked) |
| XI | vwap_bounce_long | 1 minute | Continue | **Duplicate** | `PHASE_A_REPORT:71` |
| XVI | pb01_breakout_retest | market close | Continue | **Unique** | `PHASE_A_REPORT:72`; memory `v3_step10b_increment2_complete_12jul.md:33` |
| II, III, IV, VI, VII, VIII, IX, X, XII, XIII, XIV, XV | — | not recorded | not recorded | **not recorded in any readable source** | — |

- ⭐ **The duplicates setting is recorded for only 4 of 16 scanners — Duplicate for I, V and XI, Unique for XVI. §5's liveness signal works only where Duplicate is set: among the 13 scanners that post intraday, a recorded Duplicate exists for I and XI only** (V has never posted). The old "Duplicate on all 13" was inferred from behaviour, not recorded — and it missed XVI = Unique.
- **Observed (behaviour, not a setting):** all 13 intraday scanners post at a median gap of ~60 s (96.5–99.4 % of gaps in 45–75 s); IX (gap_go_long) had not posted on 11-Sep as of 13:55; XVI posts once a day at 17:00:03–17:00:07 (33 dates since 27-Jul).
- ⭐ **403s are not only outside the window.** Of 50,825 rows with code 403: before 10:00 **18,917** · from 15:00 **19,839** · **10:00–14:59 12,069**. The receiver has two 403 paths — kill switch (`signals/webhook_receiver.py:566-568`) and entry window (`:580-583`) — and `webhook_audit` stores no reason. ⛔ Not investigated — **registered as S11-R27**: the standing reading "a 403 is the window boundary" is not supported by the data.

---

## §12 — The corpus replay: INDOCO and KOTAKBANK through the current path

**The current path (common to both):** timeframes day / 60m / 30m only (`system_config.yaml:510`); lookback 180 days (`:511`), fetched from the broker at run time and never stored (`sr_detector/detector.py:18`); it runs **only after an order is placed** and gates nothing (`signal_processor.py:1540-1550`; `detector.py:5-13` *"SHADOW only: no reject, no veto"*); levels are built only from swing pivots with N = 5 (`:513`), and the last N bars can never be pivots (`pivots.py:42`). The detector code that ran on 02-Sep is byte-identical to 970aabf (identical at 52ccb4f, effff24, 39292d3, 2d08436, d3ee69d; last change 132e571, 2026-08-01).

### §12.1 — ⭐ 287.80 was invisible for THREE independent reasons (the finding nobody had stated as one)

**Does 287.80 appear at all? No.** At the decision instant (02-Sep 14:09:26) no resistance level at or above the entry (276.82524) existed in the current path's output on any timeframe. The detector's nearest resistance was **270.00, below the entry** (`sr_detector_results` id 574: `dist_to_resistance_pct −2.46554`), 17.80 (6.185 %) short of 287.80; the V3 shadow reader found `nearest_resistance: null`. 287.80 entered the decision only as the quote's `day_high`, where `price_action` used it as the top of the day's range and scored its maximum, 1.0 — it rewarded the long.

- 🔴 **Reason (1) — no weekly data at all.** Never fetched, for any symbol, in either book (§11.7; `core/config_loader.py:1246`; `config/system_config.yaml:510`). INDOCO was a DELIVERY / GTT trade and still received day / 60m / 30m only.
- 🔴 **Reason (2) — the weekly highs behind Rama's line fall outside the 180-day window.** The window for the 14:09:26 decision ran 2026-03-06 → 2026-09-02 (`system_config.yaml:511` `lookback_days: 180`; `sr_detector/fetch.py:123-125`); the 2025 weekly highs Rama's 287.80 line rests on (the 1W chart, [E]) predate it.
- 🔴 **Reason (3) — 287.80 printed at 13:52 and was still inside the last bar at 14:09.** The 13:52 1-minute bar: O 277.48, **H 287.80**, L 277.48, C 284.15 (the weekly chart's "H 287.80" is that same print). At 14:09:26 it sat in the forming 30m bar (the detector's last 30m bar — its recorded `breakout_volume` 3,981,882 lies between the 1-minute volume sums for 13:45–14:08 and 13:45–14:09), in the forming 60m bar and in the forming day bar. `sr_detector/pivots.py:42` `for i in range(left, n - right):` never considers the last `right` = 5 bars; by 15:30 only 3 more 30m bars and 2 more 60m bars had followed. A synthetic series with its maximum in the last bar yields no pivot until 5 bars follow it (harness [B1]).

**What the contract's elements address (stated, not recommended):**
- **§3's three-timeframe level object addresses only (1).** With a weekly series but the current 180-day window, the 2025 highs stay outside (2) and the 13:52 print stays in the last bar (3) ⇒ **building weekly detection alone would not have produced 287.80 for INDOCO — the contract's central example would still fail after §3 is built**, a material fact about what §3 buys.
- **The contract's 400-day lookback [A] addresses (2) — it is therefore load-bearing for the motivating example, not an optional parameter.** Whether, with a weekly series AND 400 days, the 2025 weekly highs would form a zone at ~287.80 **cannot be measured**: the weekly candles are not stored anywhere and a broker fetch is barred. (If they did, the level would come from those 2025 pivots, not from the 13:52 print.)
- **Nothing in the contract addresses (3).** A price that printed 17 minutes before the decision cannot become a pivot under the current detector, on any timeframe, at any lookback.
- **And the gate is a separate question from the level:** with a synthetic HIGH resistance zone at 287.80 injected, the current flag rule still does **not** flag this entry: 276.83 sits below `band_low − pad` = 284.922, where `pad = zone.center * (proximity_pct / 100.0)` (`sr_detector/flags.py:143-145`; `entry_proximity_pct: 1.0`, `config/system_config.yaml:517`; harness [A3]).

**§3.3 — is a level printing minutes before a decision SUPPOSED to be excluded? Yes — by design.** `sr_detector/pivots.py:9-15`, under *"Locked Design Decisions"*: *"SR-P2 — The first `left` and last `right` bars can never be pivots (no full window) — they are skipped."* A swing high is defined as the extreme over N bars on EACH side (`:5-6`), so it needs N subsequent bars to be confirmed. ⇒ **Rama's "287.80 was the ceiling" and the detector's design are in genuine conflict. That is a judgement question — what counts as a level at decision time — not a defect.** ⛔ `pivots.py` is not changed; no fix is proposed.

### §12.2 — INDOCO (02-Sep-2026)

- **The record:** signal `sig_cf1906208c494704961cb9024eaf7f3e`, positional_sector_rotation, triggered 14:09:00, `PROCESSED`, trigger 278.4. `screener_results` id 617046 (14:09:20.018): score **62**, tier LOW, **PASSED**, eligible 60; steps volume_surge 0.0 · vwap_position 1.0 · atr_filter 0.0 · rsi_range 0.5 · price_action 1.0 · sector_strength 0.5 · time_of_day 0.5 · **spread_check 1.0** · circuit_check 1.0 · signal_age 1.0; snapshot ltp 277.41, bid / ask 277.40 / 277.41, day_high **287.8**, vwap 274.96, atr / rsi / sector / avg_volume_20d null. Trade: entry target 276.82524, **filled 276.83** (order 260902170929307, LIMIT BUY CNC, 14:09:28.546), SL 271.2887, target 285.13, exit **271.02 `GTT_EXIT` at 15:19:08.868**, net **−6.52**. V3 (shadow): `WOULD_REJECT_RR` — *"missing S&R zone (no safe SL or TGT)"*.
- **Test (i), outcome-based — did the gate reject the bad trade? FAIL.** The live rule `secondary_screener.py:316-323` fell back to 60 (min_score 0); 62 ≥ 60 ⇒ PASSED, placed, filled, stopped. No live S&R rule exists in the path. *(Shadow note: V3 would have rejected it because it found NO ceiling — the inverse of Rama's reason; the contract's "rejects for the wrong reason" pattern, in shadow only.)*
- **Test (ii), judgement-based — did the engine produce the price Rama named? FAIL.** 287.80 was not produced (§12.1); nor were the contract's entry prices 253.65 / 267.36 (`would_wait_for_retest` 0, `proposed_retest_entry` NULL; V3 sl / tgt / rr null).

### §12.3 — KOTAKBANK (22-Jul-2026; Rama's weekly line labelled 376.20 — both from the chart filenames, not the contract)

- **The record:** **0** KOTAKBANK signals on 22-Jul (0 in 20–24 Jul, against 3,802 signals that day for other symbols; the table's oldest row is 12-Jun) and **0 KOTAKBANK trades ever**; 0 detector and V3 rows. `webhook_audit` has no symbol column, so whether a KOTAKBANK alert reached the receiver that day cannot be shown.
- **Could the current path have seen the weekly support, the daily breakdown, either, or neither?** **Neither, on 22-Jul** — it never ran for the symbol. The weekly support is invisible by construction (§11.7); whether 376.20 coincides with a day / 60m / 30m zone in the 23-Jan → 22-Jul window cannot be measured without the candles.
- **Test (i): NOT SCORABLE** — no signal existed; the bad short was not taken, but no gate made that decision. **Test (ii): NOT PRODUCED** — no level was computed that day.

### §12.4 — The contract's own facts, corrected (recorded, not softened)

1. **INDOCO's entry was 276.83, not ~281.48.** 281.48 was the live price when Rama captured the chart at **14:43:33** (the 14:43 1-minute bar spans 281.01–281.75) — 34 minutes after the 14:09 decision. The chart's "+4.65" at 276.83 is the open P&L at that moment (281.48 − 276.83), not a risk; 276.83 on the daily chart is the position line, not a structural level.
2. **It was not stopped out the next day — the stop hit the same day.** The only post-entry 1-minute bar with a low at or below the 271.29 trigger is 02-Sep **15:05** (low 270.55); the recorded exit is 271.02 `GTT_EXIT` at 15:19:08.868.
3. **KOTAKBANK was never a trade the system took** (0 signals that day, 0 trades ever; the 1D filename describes a prospective short — *"awaiting for fall for tommorrow"*). The corpus states all 56 charts are system trades; that is not true of this one. ⇒ a question about the **corpus**, not about KOTAKBANK — **registered as S11-R26**; ⛔ the other 55 were not audited.

⛔ Two cases only. MIDHANI, JAICORP, DALMISUG, SIGNPOST, DATAMATICS and IDEAFORGE were not touched; IDEAFORGE (the counter-case to removing one-candle acceptance) waits for measurement.

---

## What could not be measured, and why

- **Weekly from Kite:** whether Kite's historical API serves a weekly interval — a broker call was barred (the vendor library does not validate the interval; `kiteconnect` `connect.py:151, :644`).
- **The forming bar:** whether Kite returns today's forming daily / 60m bar to the V1 fetch — a broker call (only the 30m forming bar is measured, by volume bracketing; either answer yields no pivot at 287.80).
- **A full-fidelity replay of INDOCO or KOTAKBANK:** the detector's 180-day day / 60m / 30m input is never stored; stored candles are 1-minute only (INDOCO: 28-Jul, 26/27/28-Aug, 02-Sep, 10-Sep; KOTAKBANK: 26/27-Aug).
- **Whether the 2025 weekly highs would form a zone at ~287.80 under a weekly series + 400-day lookback:** no weekly candles exist anywhere readable.
- **The complete INDOCO zone list:** the detector persists only the 12 lowest-priced zones of each kind; bands at 267.36 / 253.65 cannot be enumerated.
- **Whether 376.20 coincides with a day / 60m / 30m zone (KOTAKBANK):** needs the candles.
- **Whether a KOTAKBANK alert reached the receiver on 22-Jul:** `webhook_audit` has no symbol column; the rejection paths write no `signals` row.
- **Live Chartink state** (conditions, alert settings, active status) for every scanner: login barred. Frequency / after-trigger / duplicates for 12 of 16 are not recorded anywhere readable; the source screenshots were not opened (reported to embed a live token).
- **Whether bare `Daily Max(15, …)` includes today's bar:** Chartink semantics, undocumented in any readable source.
- **Where IV / V post, and anything before the 90-day audit window:** their webhook paths are not recorded; 72,583 earlier audit rows are gone.
- **Why I and XV differed before 13-Jul and match since:** no readable record of a scanner edit.
- **The cause of the 12,069 in-window 403s:** no reason column.
- **Logs before 2026-09-02:** not on disk (the pullback-wait log evidence covers 8 days; the DB covers all signals since 12-Jun).
- **The origin of "37" fields**, historical per-strategy `min_score` (config snapshots hold no strategy block), score distributions for the 3 never-scored strategies, the cause of the 85 SL distances off `sl_pct` by ≤ 1.07e-4.
- **The running process's in-memory config** (disk = 970aabf; inferred to equal what was loaded).

## Where the source disagreed with the inputs (the source wins)

| The input said | The source shows | Where |
|---|---|---|
| 👤 Rama: MIS = 1H + 1D, GTT = 1D + 1W | one list for both books, 30m + 1H + 1D; no weekly; no product split | §11.7 |
| Instruction files / MEMORY hot entry: scorer ceiling 80 | ceiling 65 (`quality_scorer.py:16-19`) — the MEMORY hot entry was corrected at 14:20 today | §11.3 |
| 15:10 file: "FOUR steps dead, 40 of the 100 weight" | two dead (25) + two pinned at half (10 lost) = 35 unreachable | §11.3 |
| 15:10 file §4.4: "MEDIUM 15 of 188,391" | 15 of 195,109 rows at 13:56 today — the same 15; the table has grown since that earlier count | §11.3 |
| 13:40 file §2.5: the scale "compressed into five points" | six integer values, 60–65 | §11.3 |
| 15:10 file §6.2: "All 2,541 recorded detector requests" | the 2,541 are the V3 shadow chain's records (`would_be.jsonl`); the detector's own table holds 666 rows — both carry only the three labels | §11.7 |
| 13:40 file §1.4: Batch 1 "started recording on the twin at 09:16" | it loaded at the 09:16:44 restart; its first row was written at 10:00:07.50, when entries open | §1 |
| "seven working inputs of ten" | six steps vary | §11.3 |
| "all 15 strategies" | 16 YAMLs (15 enabled + pb01_breakout_retest disabled) | §11.3 / §11.4 |
| "gap_fade_long min_score is 0" | true — and so is every other YAML's; 0 means "use the global 60" | §11.3 |
| "the 37-field inventory" | 36 top-level keys; no version ever had 37 | §11.2 |
| Contract §5: "Chartink runs 1-min, Duplicate mode" | recorded for 3 of 16 (I, V, XI); XVI Unique; 12 unrecorded | §11.6 |
| Old cross-check: "Duplicate on all 13"; "XVI undetermined" | inferred from behaviour; XVI recorded Unique | §11.6 |
| Old cross-check / PHASE_A: IV / V "unsatisfiable" | the text is confirmed; the semantics are asserted, not documented — conditional | §11.5 |
| "403s before 10:00 are the window boundary" | 12,069 of 50,825 are inside 10:00–14:59, unattributable | §11.6 |
| Old cross-check: "Kite has no `week` interval" | never measured | §11.7 |
| Contract §12: INDOCO "actual ~281.48"; "stopped out the following day" | entry 276.83; the stop hit the same day (15:05 bar; exit 15:19:08) | §12.4 |
| Corpus: all 56 charts are system trades | KOTAKBANK was not | §12.4 |
| `config/expected_managers.yaml:179,181` cite `main.py:3318`, `entry_gate.py:283` | EntryGate at `main.py:3839`, `add()` at `entry_gate.py:288` — stale references, meaning unaffected | §11.1 |
| `signal_processor.py:1074-1075`: "EntryGate already waits for current price" | nothing feeds EntryGate | §11.1 |
| `gap_fade_long.yaml` `order_protocol: CO_PLUS_TGT` | every trade runs LIMIT_TRIPLE (947 / 947) | §11.2 |
| `core/schema.sql:722`, `system_config.yaml:628`, `config_loader.py:1544`, `scripts/revert_temp_config.py:91-99` | code does not match the comments (global smart-TGT value; no `candle_math.resample` call; min_score 0, no TEMP marker) | §11.2 / §11.3 / §11.7 |
| The 05-Sep cross-check's line numbers and counts | moved (e.g. `system_config.yaml :529 → :510`; `config_loader.py :1063 → :1246`; detector rows 598 → 666; screener rows 173,592 → 195,109; trades 856 → 947) | throughout |

## Conflicts between the passes (reported, not resolved)

1. `screener_results` total: 195,109 (to 13:56) vs 195,173 (to 13:59) — live tables drift between queries.
2. Rows scoring 62: 799 vs 800 (n = 173,756 at 13:59); the other counts agree (61 × 14, 63 × 6, 64 × 247, 65 × 15).
3. `signals` total: 232,208 vs 232,113 (queries minutes apart).
4. Scope of "the schema forbids a weekly timeframe": the validator covers `sr_detector.timeframes` only; `v3_chain.structure_intervals` has none (`core/config_loader.py:1477-1478`). Both passes agree no code path fetches a weekly series today.
5. Unrelated "week" search hits differ in wording between two passes; both find no weekly interval in the fetch path.
6. The V2 construction gate is cited at `main.py:3549` [3515] and at `:3423 (:3389)` / `:3769 (:3734)` — possibly different blocks; not reconciled here.
7. Measurement windows: 13:48–13:59 · 13:47–14:08 · 13:46–14:05 · 13:45:47–14:04:45 (VM clock).

---

**Registered today from this pass:** S11-R26 (the corpus question) and S11-R27 (the in-window 403s) in `docs/MASTER_PENDING_01-Aug-2026.md` (N 309 → 311). **Memory:** recorded under the marker `RESULT-CONTRACT-S11S12-11SEP2026` — the BOARD, `UNPUSHED_PENDING_DEPLOY_LEDGER.md`, `docs/SYSTEM_MAP.md`, `PATHS.md`. **Evidence:** the four findings files (`s11_7_s11_8.md`, `s11_1_to_4.md`, `s11_5_s11_6.md`, `s12_replay.md`) and everything beside them in the job's `contract/` folder — the §12 harness, the field and YAML scans, the md5 lists, the read-only VM query outputs — are copied to `docs/audit/CONTRACT_S11_S12_EVIDENCE_11-Sep-2026/` (30 files, each sha256-verified and listed in its `MANIFEST.txt`; scripts stored as `.py.txt`; the three `d3ee69d` source exports not copied — `git show d3ee69d:<path>` reproduces them).

*No recommendations. Rama decides what happens next.*
