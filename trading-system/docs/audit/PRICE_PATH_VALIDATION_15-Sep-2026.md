# PRICE PATH VALIDATION — REPORT

**Card:** "FOR VS CODE CLAUDE — PRICE PATH VALIDATION — REPORT ONLY", 15-Sep-2026 (pasted into this session).
**Builds on:** `docs/audit/ENTRY_EXECUTION_FACT_FINDING_15-Sep-2026.md`, cited below as **FF-&lt;question&gt;**. Facts that report established are cited, not repeated.
**Date of work:** 15-Sep-2026 (Tue), 15:50–17:12 IST.
**Nature:** REPORT ONLY. No code, config, commit, push, deploy, service action or broker call.
**Production VM:** not contacted. `origin` (production's bare repo) not contacted; git history was read from local objects only.
**Testing VM (130.210.13.114, `trading-sbx`):** read-only against the system — SQLite `mode=ro` + `PRAGMA query_only=1`, `grep`, `md5sum`, `ls`, `find`, `crontab -l`, `systemctl show`. The system's tree, DB, logs, config, crontab and services were not written. **One disclosure:** a query script wrote a scratch file, `/tmp/q1_eq_rows.json` (the 33-case list, created 15:55:55 IST), which later scripts read. I removed it at 17:08 IST with its literal path, and no other scratch file remains.
**How it was done:** one thread, sequential reading, no subagents and no workflow (per the card). The session ran on Opus 5; the card names Sonnet 4.6.
**Per the card:** no proposed fixes, no ranking, nothing implemented. Q10(e) is a description of gaps, as the card asks.

---

## THE ANSWER TO Q1 (THE BLOCKER), FIRST

> **NONE of the 33 cases is established as QUOTE_UNAVAILABLE, QUOTE_MALFORMED or QUOTE_EXCEPTION.**
>
> **15 of 33 are ESTABLISHED as QUOTE_SUCCESS_SAME_PRICE.** In each, M-S1 made its own `kite.quote` call (the live quote path has no cache) and the returned last price was *exactly* the Chartink trigger.
>
> ⚠️ **18 of 33 (17-Aug → 01-Sep) are NOT ESTABLISHED.** No M-S1 log exists for those dates anywhere reachable. The stored trade row is bit-identical whether M-S1 succeeded with LTP = trigger or fell back to the stale price. **For these 18, a silent fallback is NOT EXCLUDED.**
>
> STRATEGY_FLAG_MISREAD is excluded for all 33. QUOTE_SUCCESS_SAME_AFTER_ROUND is excluded for all 33.
>
> Across every log that exists (8 testing-VM days plus a 31-Aug production copy) M-S1 logged **530 successes, 0 "unavailable", 0 "fetch error"**. That is context, not a classification of the 18.

---

## 0. SOURCES, IDENTITY, MARKERS

### 0.1 Sources

| Label | Source | State at measurement |
|---|---|---|
| **WT** | Working tree `D:/Projects/trading-system` | Branch `feat/delivery-config-split` @ `6d24a83` plus uncommitted edits (the same state as FF) |
| **TW** | Deployed tree on the testing VM | Read from the FF snapshot (pulled 10:51 IST). **Re-verified md5-identical to the live VM for all 19 files cited here at 15:54:41 IST.** Service active since 08:15:23. |
| **TW-DB** | `data_store/trading_system.db`, `data_store/analytics.db` on the VM | Read-only |
| **TW-LOG** | `logs/system_*.log`, `logs/debug_*.log` on the VM | Only 03, 04, 07, 08, 09, 10, 11 and 15 Sep exist |
| **LOCAL-LOG** | `D:/Projects/trading-system-evidence/2026-08-31/system_2026-08-31.log` | A production log copy captured 31-Aug 15:23. sha256 `a31fe6a7…` matches its `SHA256SUMS.txt`. |
| **TW-PRES** | `/home/ubuntu/preserved/2026-09-04_cnc_off/*.yaml.bak` on the VM | Production copies of the three positional YAMLs, made 04-Sep 09:34 with file mtimes preserved |
| **TW-EVID** | `data_store/evidence/signal_evidence_VBB097_2026-09-{11,15}.jsonl` on the VM | Batch-1 evidence rows |
| **GIT** | Local git objects | No fetch |

### 0.2 File identity (md5; WT vs TW)

**Identical in both trees:**
- `orders/order_placer.py` c337d5c3
- `broker/order_monitor.py` 60ab959e
- `orders/price_math.py` 8d8ca640
- `broker/slippage_engine.py` 4cb9e8e3
- `core/instrument_cache.py` 3c3185c5
- `broker/rate_limiter.py` 877c335d
- `orders/order_protocol_limit.py` d675d15e
- `orders/full_entry_engine.py` 01060102
- `strategies/loader.py` 1c30f4e1
- `strategies/schema.py` 7d6aa839
- `orders/eod_squareoff.py` 1607e3f5
- `orders/shadow_tracker.py` cd75d0cc
- `scripts/refresh_instruments.py` c70d2749
- `config/broker_limits.yaml` and all 16 strategy YAMLs (FF-A1)

**Different:**

| File | WT | TW |
|---|---|---|
| `signals/signal_processor.py` | 858e2ce3 | da8c6f98 |
| `broker/zerodha_adapter.py` | 124ed3fa | 1a237b8c |
| `capital/fund_manager.py` | da4b3fdd | 9ff45f66 |
| `capital/position_sizer.py` | f3b1361b | a9775db8 |
| `main.py` | 9907c93f | 85219d22 |
| `config/system_config.yaml` | e2add048 | 351bd82e |
| `orders/order_manager.py` | 6ea73f0c | 39edfcbf |
| `core/state_store.py` | e8c24a7d | 45d83a94 |

`screening/secondary_screener.py`, `orders/order_reconciler.py` and `capital/kill_switch.py` also differ.

Line numbers hold only for these states (M3).

### 0.3 Markers

- **Status:** ESTABLISHED · PARTIAL (the open part is written NOT ESTABLISHED) · NOT ESTABLISHED
- **WT↔VM:**
  - MATCH — cited code identical
  - DIFFERS-FILE — the file differs, the cited logic is identical
  - **DIFFERS-LOGIC**
- **Paper↔live:** IDENTICAL · DIFFER
- **Provenance:** MEASURED (code, DB, log) unless marked **EVIDENCE** (a record a person wrote) or **INFERENCE**.
- **Percentiles:** linear interpolation.

### 0.4 Corrections to FF found during this work

1. **FF-C6/H5 say the tick-snap log is "DEBUG with 0 hits".** The `adapter.snap_to_tick` event appears **172 times** in `debug_2026-09-*.log` (03: 26 · 04: 17 · 07: 32 · 08: 21 · 09: 11 · 10: 24 · 11: 28 · 15: 13). The file formatter keeps only the message name, so no price, tick or symbol survives (Q10d).
2. **FF-C6 misses one fallback:** a DEFAULT_TICK fallback for XTRANET on 04-Sep 10:59:16 (Q7d).
3. **FF-B6's "33 equal" used a relative tolerance of 1e-6.** All 33 are exact float equality (Q1).
4. **FF-D5 item 3 did not name the legs.** Its four `unknown_status` lines were on EOD and TGT legs; none was on an ENTRY leg (Q9).

---

## Q1 — THE 33 CASES

**Status:** PARTIAL (15 ESTABLISHED, 18 NOT ESTABLISHED) · **WT↔VM:** DIFFERS-FILE (M-S1 logic identical; TW adds one evidence line) · **Paper↔live:** DIFFER (quote source)

### Q1.1 The population, reproduced

TW-DB: `trades JOIN signals` for `created_at >= '2026-08-15'` gives **331** rows (331 of 331 trades join).

| Group | Measure | Count |
|---|---|---|
| `pullback_wait_enabled` false | derived = stored | **33** |
| `pullback_wait_enabled` false | derived ≠ stored | **147** |
| `pullback_wait_enabled` true | derived = stored | **151** |

- The derived value is `signals.trigger_price × (1 − off)` for LONG and `× (1 + off)` for SHORT.
- `off` is 0.002 for the three `positional_*` strategies and 0.001 for the rest (the YAML values).
- The strategy grouping uses the six YAMLs with the flag set true.
- All rows are `mode='LIVE'`.

**All 33 are exact float equality** (`entry_target_price == derived`), not merely within tolerance.

### Q1.2 How M-S1 can end — the three code outcomes

WT `signals/signal_processor.py` 1129-1152 / TW 1082-1106, `_process_one`:

```
if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:
    live_ltp = None
    try:
        quotes = self._quote_fn([symbol])
        q = quotes.get(symbol) if quotes else None
        live_ltp = float(q.last_price) if q is not None else None
    except Exception as exc:
        self._log.warning(f"FIX-067 momentum fresh quote fetch error for {symbol}: {exc}")
    if live_ltp and live_ltp > 0:
        self._log.info(f"FIX-067 momentum fresh quote: {symbol} stale={trigger_price:.2f} "
                       f"live={live_ltp:.2f} delta={live_ltp - trigger_price:+.2f} — re-anchoring …")
        entry_price, sl_price = self._derive_prices(live_ltp, strategy_obj, now_time=now.time())
        _reanchored = True                # Batch 1 evidence   ← TW only (TW 1101)
    else:
        self._log.warning(f"FIX-067 momentum fresh quote unavailable for {symbol} "
                          f"(ltp={live_ltp}); using stale webhook price")
```

Each outcome writes its own log line:

| Card code | Branch | Log line |
|---|---|---|
| QUOTE_EXCEPTION | `except` | WARNING "…fetch error…", then the "unavailable" WARNING |
| QUOTE_UNAVAILABLE / QUOTE_MALFORMED | `else` (no dict, symbol missing, `last_price` 0, None or NaN) | WARNING "…unavailable…(ltp=…)" |
| QUOTE_SUCCESS_* | `if live_ltp and live_ltp > 0` | INFO "…fresh quote: … live=… delta=…" |

### Q1.3 Why equality excludes SAME_AFTER_ROUND

- `_derive_prices` has no rounding step: `entry_price = trigger_price * (1.0 - offset)` / `* (1.0 + offset)` (WT 1773-1779 / TW 1778-1784).
- `create_trade(entry_target_price=entry_price)` stores it unrounded (`order_placer.py` 1003).
- So under the success branch, exact equality requires `float(q.last_price) == trigger_price`.
- A quote that differed and "became equal after rounding" cannot produce these rows.

### Q1.4 Why a success line means a fresh broker call

**Live `get_quote` has no cache.** `ZerodhaAdapter.get_quote` (TW `broker/zerodha_adapter.py` 1730-1806) runs `self._rl.acquire(_CATEGORY_MAP["get_quote"])` (1757), then `raw = self._kite.quote(*instrument_keys)` (1762), on every call. The adapter's `get_quote` has exactly one `self._kite.quote` and zero mentions of "cache" at every candidate production SHA:
- 742d9da, 75e637c, 18dd6cc, 20061b6, d3ee69d, 970aabf;
- and in WT.

The 3-second quote cache (`_CACHE_TTL_SEC = 3.0`, WT `main.py` 521 / TW 524) belongs to the **paper** provider only.

**Two sequences show the M-S1 call is separate from the screener's call:**

| Case | Screener `get_quote` | Screener PASSED | M-S1 `get_quote` | Success line |
|---|---|---|---|---|
| GARFIBRES 10-Sep (TW-LOG) | 10:04:07.265 → .281 (15 ms) | .284 | .285 → .300 (15 ms) | .300 |
| SPLPETRO 31-Aug (LOCAL-LOG L3292-3299) | 10:05:20.521 → .547 (25 ms) | .551 | .551 → .578 (26 ms) | .578 |

**Not captured:** `Quote` has no last-trade time (TW 1785-1798). So for no case can the log show whether a trade printed between Chartink's scan and the M-S1 quote — **NOT ESTABLISHED**. This does not change the card's code, whose definition is "fresh quote obtained; LTP happened to equal the trigger".

### Q1.5 What code production ran on the no-log dates

- **When the working M-S1 was introduced:** commit `3f4587f` (07-Jul, "momentum fresh-LTP re-anchors the FULL placement basis (+ D1 plumbing …)"). Every candidate SHA above contains it (`git merge-base --is-ancestor`).
- **M-S1 block text** (from the `if not strategy_obj.pullback_wait_enabled` line to "Step 5"):
  - md5 `cf9534606323` at 3f4587f, 742d9da, 75e637c, 18dd6cc, 20061b6, d3ee69d and WT;
  - `2ca60c1cc516` at 970aabf and TW. The only difference is the `_reanchored = True` line.
- **`_derive_prices`** hashes the same (`e067268f8a23`) in all eight states.
- **NOT ESTABLISHED:** which SHA production ran on each no-log date (commit dates are not deploy dates). Every candidate has the same M-S1 behaviour.
- **M-S1 was re-anchoring other trades on every no-log date.** Momentum trades whose stored entry ≠ the trigger-derived value, by date:

| Date | 17-Aug | 18-Aug | 19-Aug | 20-Aug | 21-Aug | 24-Aug | 26-Aug | 27-Aug | 28-Aug | 01-Sep |
|---|---|---|---|---|---|---|---|---|---|---|
| Re-anchored trades | 8 | 6 | 3 | 9 | 9 | 6 | 10 | 9 | 9 | 1 |

  This shows the success branch worked that day. It does not show it worked for the specific case.

### Q1.6 STRATEGY_FLAG_MISREAD is excluded for all 33

1. **The 15 log-proven cases:** the M-S1 body ran, which requires `not strategy_obj.pullback_wait_enabled`. The flag was false in that process.
2. **14 of the 18 no-log cases:** a trade of the **same strategy** was re-anchored in the **same process lifetime** (boot = the latest `system_events` STARTUP before the trade). Strategies load once: `strategies/loader.py` 94, "Strategies are loaded ONCE; no hot reload."
3. **The other 4** (BALUFORGE 24-Aug `positional_swing_long`; MAXESTATES 24-Aug 10:11 `positional_momentum_long`; COSMOFIRST ×2 01-Sep `positional_sector_rotation`):
   - TW-PRES holds production's three positional YAMLs as of 04-Sep.
   - Each reads `pullback_wait_enabled: false` at line 36, with file mtime **2026-07-13 18:33:49** preserved.
   - So the files were unchanged from 13-Jul to 04-Sep, a span covering both dates.
4. **GIT:** `git log --all -G pullback_wait_enabled -- config/strategies strategies` returns only:
   - `bcf03b5` (17-Apr, the initial values);
   - `5a71fb6` (13-Jul, which adds pb01's `false`).

   No committed value change exists for any of the 15 original strategies.

### Q1.7 Two measurements recorded for the 18 (neither can classify)

1. **The screener's own quote.** This is a separate, earlier call made 0.7–6.3 s before the trade row (`screener_results.market_data_snapshot.ltp`).
   - It equalled the trigger in 16 of the 18.
   - Exceptions: MAXESTATES 19-Aug (504.25 vs 504.65) and BALUFORGE 24-Aug (611.20 vs 611.65).
   - Among the 15 proven cases the screener LTP also differed twice (SHAREINDIA 10-Sep 10:05; ONGC 11-Sep) while M-S1's quote matched. So this measure cannot decide a case.
2. **1-minute Kite bars** (`analytics.db.candles`).
   - The trigger was a traded price in the M-S1 minute — inside [low, high], or equal to the prior bar's close — in **31 of 31** cases with bars. MAFANG and MMP on 08-Sep have no bars.
   - **Control:** shifting the trigger ±1% makes the same test fail on 30/31 and 31/31. The test can fire, but it cannot exclude SAME_PRICE for any case.

### Q1.8 Per-case table

Proof-line timestamps are from TW-LOG `system_<date>.log` unless noted. "Same-boot re-anchor" names one same-strategy trade re-anchored in the same process. Prices are ₹.

| # | trade_id | Symbol | Date / created | Strategy | Trigger | Entry target | Classification | Proof |
|---|---|---|---|---|---|---|---|---|
| 1 | trd_7e8f2458b16c47a3815e757398dcd036 | EXPLEOSOL | 17-Aug 10:13:12 | gap_go_long | 913.00 | 912.087 | **OTHER — NOT ESTABLISHED** | No log for 17-Aug; row identical under both branches. Flag false: same-boot re-anchor PURVA 10:02:11. Screener LTP 913.00. |
| 2 | trd_de556515aed849d995aa334df6a383f1 | DBOL | 18-Aug 10:03:15 | positional_swing_long | 127.53 | 127.27494 | **OTHER — NOT ESTABLISHED** | No log. Flag false: DBOL 10:09:18. Screener 127.53. |
| 3 | trd_87bfccc737284a02970d00943ddf31e9 | MAXESTATES | 19-Aug 10:12:15 | positional_momentum_long | 504.65 | 503.6407 | **OTHER — NOT ESTABLISHED** | No log. Flag false: 5PAISA 10:01:13. Screener **504.25 ≠ trigger**. |
| 4 | trd_76fe87516d1e4a5da502a796ec49e1e9 | SILVERIETF | 20-Aug 12:36:12 | gap_go_long | 235.65 | 235.41435 | **OTHER — NOT ESTABLISHED** | No log. Flag false: VERANDA 10:00:21. Screener 235.65. |
| 5 | trd_ef174b2bea4c4187af81a84bdd31bedf | CLSEL | 21-Aug 10:09:16 | positional_swing_long | 290.55 | 289.9689 | **OTHER — NOT ESTABLISHED** | No log. Flag false: JSFB 10:03:15. Screener 290.55. |
| 6 | trd_51716ae0c2d44917b9b6f0d769980f21 | MAXESTATES | 24-Aug 10:02:14 | positional_sector_rotation | 535.50 | 534.429 | **OTHER — NOT ESTABLISHED** | No log. Flag false: KAMATHOTEL 10:05:22. Screener 535.50. |
| 7 | trd_00971394a203459fb6061d0e4c0aff06 | BALUFORGE | 24-Aug 10:03:17 | positional_swing_long | 611.65 | 610.4267 | **OTHER — NOT ESTABLISHED** | No log. Flag false: TW-PRES `.bak` (mtime 13-Jul). Screener **611.20 ≠ trigger**. |
| 8 | trd_06198de3f3ce470d9e0943a1d083cf85 | GUJTHEM | 24-Aug 10:08:12 | gap_go_long | 394.75 | 394.35525 | **OTHER — NOT ESTABLISHED** | No log. Flag false: KRBL 10:00:22. Screener 394.75. |
| 9 | trd_a6ae04c575984f278dc5b031ebfa901e | MAXESTATES | 24-Aug 10:11:16 | positional_momentum_long | 537.00 | 535.926 | **OTHER — NOT ESTABLISHED** | No log. Flag false: TW-PRES `.bak`. Screener 537.00. |
| 10 | trd_0156c272800e4e6495d1793dfe52a739 | KAMATHOTEL | 24-Aug 12:03:19 | gap_go_long | 222.99 | 222.76701 | **OTHER — NOT ESTABLISHED** | No log. Flag false: KRBL 10:00:22. Screener 222.99. |
| 11 | trd_56b5bc2d3d244e1caacb07f0654da303 | GUJTHEM | 26-Aug 10:06:14 | positional_sector_rotation | 424.50 | 423.651 | **OTHER — NOT ESTABLISHED** | No log. Flag false: FMGOETZE 10:07:14. Screener 424.50. |
| 12 | trd_571bdadd380f47d0b28163e971ab47cb | HINDZINC | 26-Aug 10:09:13 | positional_sector_rotation | 621.20 | 619.9576 | **OTHER — NOT ESTABLISHED** | No log. Flag false: FMGOETZE 10:07:14. Screener 621.20. |
| 13 | trd_abbe7a28433f4496bc66b751064871f0 | GIPCL | 26-Aug 14:31:22 | positional_sector_rotation | 200.80 | 200.3984 | **OTHER — NOT ESTABLISHED** | No log. Flag false: FMGOETZE 10:07:14. Screener 200.80. |
| 14 | trd_f119d4cf66b040af93f784c1b2143606 | GIPCL | 27-Aug 13:29:18 | positional_sector_rotation | 204.28 | 203.87144 | **OTHER — NOT ESTABLISHED** | No log. Flag false: JINDALSAW 10:01:14. Screener 204.28. |
| 15 | trd_a9756d0945104e8abd3b1c3a030d20a5 | KAMATHOTEL | 27-Aug 14:52:16 | positional_sector_rotation | 237.51 | 237.03498 | **OTHER — NOT ESTABLISHED** | No log. Flag false: JINDALSAW 10:01:14. Screener 237.51. |
| 16 | trd_9319cb7b62474ecf925d3f82178b9332 | GIPCL | 28-Aug 14:57:16 | positional_momentum_long | 205.86 | 205.44828 | **OTHER — NOT ESTABLISHED** | No log. Flag false: YATHARTH 10:01:14. Screener 205.86. |
| 17 | trd_b131d5bb09df4572abac04f9db805be5 | SPLPETRO | 31-Aug 10:05:21 | positional_sector_rotation | 739.35 | 737.8713 | **QUOTE_SUCCESS_SAME_PRICE** | LOCAL-LOG L3299 10:05:20.578 `FIX-067 momentum fresh quote: SPLPETRO stale=739.35 live=739.35 delta=+0.00`. Own `get_quote` .551→.578. |
| 18 | trd_d8ffa6ed44824a7598ccb1b07cc33ac9 | COSMOFIRST | 01-Sep 10:07:15 | positional_sector_rotation | 983.00 | 981.034 | **OTHER — NOT ESTABLISHED** | No log. Flag false: TW-PRES `.bak`. Screener 983.00. |
| 19 | trd_de73a355bcfc4cad94d14fe4f299f5d3 | COSMOFIRST | 01-Sep 10:14:16 | positional_sector_rotation | 982.00 | 980.036 | **OTHER — NOT ESTABLISHED** | No log. Flag false: TW-PRES `.bak`. Screener 982.00. |
| 20 | trd_62b8ca7e65c543de8be290e8ffa9ce3e | MAFANG | 07-Sep 12:40:31 | positional_sector_rotation | 219.63 | 219.19074 | **QUOTE_SUCCESS_SAME_PRICE** | 12:40:31.054 `…MAFANG stale=219.63 live=219.63 delta=+0.00` |
| 21 | trd_b8dee831b02344819f153f6c1b351b0a | MAFANG | 07-Sep 13:04:20 | gap_go_long | 219.67 | 219.45033 | **QUOTE_SUCCESS_SAME_PRICE** | 13:04:20.153 `…stale=219.67 live=219.67 delta=+0.00` |
| 22 | trd_656498849cd849a0ae1cb42215731a88 | IOLCP | 07-Sep 13:30:28 | gap_go_long | 211.72 | 211.50828 | **QUOTE_SUCCESS_SAME_PRICE** | 13:30:27.354 `…stale=211.72 live=211.72 delta=+0.00` |
| 23 | trd_66e947e0dd824485ad88516fca51f4ac | MAFANG | 07-Sep 14:21:16 | gap_go_long | 220.00 | 219.78 | **QUOTE_SUCCESS_SAME_PRICE** | 14:21:15.632 `…stale=220.00 live=220.00 delta=+0.00` |
| 24 | trd_a519f1771ec8483fa632bb708e2b2245 | MAFANG | 08-Sep 10:02:16 | gap_go_long | 234.99 | 234.75501 | **QUOTE_SUCCESS_SAME_PRICE** | 10:02:15.892 `…stale=234.99 live=234.99 delta=+0.00` |
| 25 | trd_4024e48fd94141fab81cb6575e0249c9 | MMP | 08-Sep 10:06:15 | gap_go_long | 476.80 | 476.3232 | **QUOTE_SUCCESS_SAME_PRICE** | 10:06:14.567 `…stale=476.80 live=476.80 delta=+0.00` |
| 26 | trd_5b3880a41b8747ec96e7befcabb9ffa3 | ORCHPHARMA | 09-Sep 13:38:16 | gap_go_long | 1021.20 | 1020.1788 | **QUOTE_SUCCESS_SAME_PRICE** | 13:38:15.639 `…stale=1021.20 live=1021.20 delta=+0.00` |
| 27 | trd_74dae2fc51284fe2af68f7663fd63703 | EPACKPEB | 09-Sep 14:25:22 | gap_go_long | 248.52 | 248.27148 | **QUOTE_SUCCESS_SAME_PRICE** | 14:25:21.936 `…stale=248.52 live=248.52 delta=+0.00` |
| 28 | trd_0c7368bc80634f1082ad12467db1dc40 | GARFIBRES | 10-Sep 10:04:08 | gap_fade_long | 818.30 | 817.4817 | **QUOTE_SUCCESS_SAME_PRICE** | 10:04:07.300 `…stale=818.30 live=818.30 delta=+0.00`. Own `get_quote` .285→.300. |
| 29 | trd_f3b5f0fee64842d5a1829ab1be1a8771 | SHAREINDIA | 10-Sep 10:05:12 | gap_fade_long | 209.39 | 209.18061 | **QUOTE_SUCCESS_SAME_PRICE** | 10:05:11.406 `…stale=209.39 live=209.39 delta=+0.00` |
| 30 | trd_8d11b9284f444e398b581cb3319548a5 | MUKANDLTD | 10-Sep 10:06:10 | gap_go_long | 143.79 | 143.64621 | **QUOTE_SUCCESS_SAME_PRICE** | 10:06:10.023 `…stale=143.79 live=143.79 delta=+0.00` |
| 31 | trd_93c398c94c554bf0b72e786d70a38b4f | SHAREINDIA | 10-Sep 12:37:12 | positional_sector_rotation | 207.40 | 206.9852 | **QUOTE_SUCCESS_SAME_PRICE** | 12:37:11.858 `…stale=207.40 live=207.40 delta=+0.00` |
| 32 | trd_d5330ac222e54357bfa3be9e47396f55 | SESHAPAPER | 11-Sep 11:14:09 | gap_go_long | 251.95 | 251.69805 | **QUOTE_SUCCESS_SAME_PRICE** | 11:14:09.248 `…stale=251.95 live=251.95 delta=+0.00`. TW-EVID P1 `reanchored: true`. |
| 33 | trd_241e81da40cf400493b90ba3bbe8ef12 | ONGC | 11-Sep 13:10:15 | gap_fade_short | 235.14 | 235.37514 | **QUOTE_SUCCESS_SAME_PRICE** | 13:10:14.889 `…stale=235.14 live=235.14 delta=+0.00`. TW-EVID P1 `reanchored: true`. |

**Totals:** QUOTE_SUCCESS_SAME_PRICE **15** · QUOTE_SUCCESS_SAME_AFTER_ROUND **0** · QUOTE_UNAVAILABLE **0** · QUOTE_MALFORMED **0** · QUOTE_EXCEPTION **0** · STRATEGY_FLAG_MISREAD **0** · OTHER (quote outcome NOT ESTABLISHED) **18**.

### Q1.9 Population checks across all available records

**M-S1 log lines per day (TW-LOG, plus LOCAL-LOG for 31-Aug):**

| Day | success | of which `delta=+0.00` | unavailable | fetch error |
|---|---|---|---|---|
| 31-Aug | 51 | 4 | 0 | 0 |
| 03-Sep | 64 | 6 | 0 | 0 |
| 04-Sep | 5 | 2 | 0 | 0 |
| 07-Sep | 86 | 12 | 0 | 0 |
| 08-Sep | 58 | 5 | 0 | 0 |
| 09-Sep | 16 | 3 | 0 | 0 |
| 10-Sep | 82 | 8 | 0 | 0 |
| 11-Sep | 126 | 89 | 0 | 0 |
| 15-Sep | 42 | 1 | 0 | 0 |

- 85 of 11-Sep's 89 zero-delta lines are one ETF, LIQUIDBETF, whose price sat at 1098.67–1098.69.
- **TW-EVID P1_ACCEPT rows:**
  - momentum strategies: `reanchored: true` on 11 + 3 = **14/14**;
  - pullback strategies: `false` on 12 + 2 = **14/14**.

### Q1.10 What a fallback looks like today

Code facts the design depends on:
- **A fallback is logged at WARNING only.** Nothing in `trades`, `orders` or `signals` distinguishes it from a SAME_PRICE success; both store `trigger × (1 ∓ offset)`.
- **The only persisted discriminator is TW's Batch-1 P1 field `reanchored`** (JSONL, testing VM, from 11-Sep). WT has no equivalent.
- **`self._quote_fn is None` skips the whole block without any log line** (WT 1129 / TW 1082). Measured: `quote_fn=broker_adapter.get_quote` is always passed to SignalProcessor (WT `main.py` 3294 / TW 3616).
- **Non-finite values:**
  - `float('nan') > 0` is False, so NaN takes the fallback branch.
  - `float('inf') > 0` is True, so +inf takes the success branch into `_derive_prices`, whose guard is `if entry_price <= 0` (WT 1781).
  - No occurrence of either in the data.

**Paper↔live:** the code is identical. In paper, `quote_fn` is `_make_paper_quote_provider` with a 3 s TTL cache (WT `main.py` 521 / TW 524), so a paper "success" can be a quote up to 3 s old. All 33 cases are LIVE.

---

## Q2 — THE SIX STRATEGIES THAT BYPASS M-S1

**Status:** ESTABLISHED for (a), (c), (d); PARTIAL for (b) (Chartink's price as-of instant NOT ESTABLISHED) · **WT↔VM:** DIFFERS-FILE · **Paper↔live:** DIFFER

### (a) Price source of the submitted LIMIT, end to end

The six are first_pullback_long/short, open_high_breakdown_short, open_low_breakout_long, vwap_bounce_long and vwap_rejection_short. Their YAMLs have `entry_method: "LIMIT"` and `entry_offset_pct: 0.001`. `sl_pct` is 0.015 for first_pullback ×2, 0.01 for open_high/open_low, and 0.008 for vwap ×2. `sl_min_pct` is 0.003, `sl_max_pct` 0.05, and none sets `sl_gap_buffer_pct` (schema default 0.0).

1. **Chartink price.** `WebhookReceiver._process_signal`: `price = float(price_str)` (WT `signals/webhook_receiver.py` 892 / TW 910). It is stored as `signals.trigger_price` and put in the queue tuple.
2. **Trigger-derived prices.** `SignalProcessor._process_one` → screener (its quote is used for scoring and circuit checks only) → `entry_price, sl_price = self._derive_prices(trigger_price, strategy_obj, now_time=now.time())` (WT 1079-1081 / TW 1028-1030).
   - LONG entry = `trigger × 0.999`; SHORT entry = `trigger × 1.001`.
   - SL = `entry × (1 ∓ sl_pct)`, clamped to [0.3 %, 5 %] of the entry.
3. **M-S1 skipped.** `if not strategy_obj.pullback_wait_enabled and …` is False (WT 1129 / TW 1082). In TW, `_reanchored` stays False.
4. **Sizing, reservation, target, placement call:**
   - `self._sizer.calculate(symbol, side, entry_price, sl_price, …)` (WT 1158 / TW 1112);
   - `_admit_and_place` → `self._fm.reserve(symbol, sizing.qty, entry_price, …)` (WT 1362-1365 / TW 1327-1330);
   - `tgt_price = self._derive_target(entry_price, sl_price, strategy_obj)` (WT 1408 / TW 1368);
   - `self._placer.place(… entry_price=entry_price, sl_price=…, tgt_price=…, signal_trigger_price=trigger_price …)` (WT 1465-1479 / TW 1446-1460).
5. **`OrderPlacer.place`** (`orders/order_placer.py`, identical in both trees):
   - FIX-025 does nothing (`release_ltp` is None, 907).
   - R:R gate (937-958).
   - `create_trade(entry_target_price=entry_price)` (996-1015).
   - **FIX-128** (1103-1192): `_fetch_ltp` → abort if `abs(LTP − trigger)` exceeds `min(0.22 × abs(trigger − sl), ₹5)` or 1 %.
   - **FIX-075** (1197-1289): a second `_fetch_ltp`. If `abs(LTP − entry)/entry > 0.005`, and `qty × (LTP − entry)/leverage > 0` (the LTP is above the entry, whatever the side), and `fm.top_up_reservation` succeeds, then **`entry_price = current_ltp`** (1261).
6. **Protocol and broker submission:**
   - `self._engine.execute(entry_price=…)` (1345-1356) → `FullEntryEngine.execute` → `LimitTripleProtocol.execute`: `_entry_order_price = 0.0 if entry_order_type == "MARKET" else entry_price` (`order_protocol_limit.py` 210).
   - → `ZerodhaAdapter.place_order` → `_validate_place_order` → `_snap_order_to_tick`, LIMIT branch `_round_nearest_to_tick(price, tick)` (TW 1448-1450 / WT 1400-1402).
   - → `kite.place_order(price=…)` (TW 639-654 / WT 604-615).

**So:** the submitted price is **the Chartink trigger × (1 ∓ 0.001), snapped to the nearest tick**. A live LTP replaces it only through FIX-075, when the LTP is more than 0.5 % above the entry and the top-up succeeds.
- In DB history 1 of the 8 top-ups was a pullback-flag strategy: CHEMPLASTS, first_pullback_long, 17-Jun (Q4e).
- There have been 0 top-ups on these strategies since 01-Sep.

**Paper:** FIX-128 and FIX-075 do not run, because `get_quote_raw` returns `{}` (FF-A1). The paper price is always `trigger × (1 ∓ 0.001)`, snapped.

### (b) How stale that price is at submission

**Time.** TW-DB, trades created since 2026-09-01 that have an ENTRY `orders` row.
- `placed_at` is taken after broker ack and DB persist (FF-D3).
- `triggered_at` is Chartink's minute with seconds forced to 0 (FF-D3: 46,070 of 46,070). The interval is therefore measured from the start of that minute.
- The as-of instant of Chartink's price within its minute is **NOT ESTABLISHED** (FF-B7).

| `placed_at − triggered_at` | n | min | p50 | p90 | max |
|---|---|---|---|---|---|
| Six, 01–15 Sep | 53 | 7.48 s | 17.33 s | 23.78 s | 26.35 s |
| Six, LFL836 (01–08 Sep) | 34 | 14.67 s | 17.52 s | 25.30 s | 26.35 s |
| Six, VBB097 (09–15 Sep) | 19 | 7.48 s | 15.91 s | 20.78 s | 22.47 s |
| *The ten, 01–15 Sep (for comparison)* | 63 | 8.35 s | 17.46 s | 28.19 s | 35.23 s |

`placed_at − received_at`: the six 0.76 / 3.41 / 11.56 / 14.20 s (min/p50/p90/max); the ten 0.75 / 4.75 / 11.85 / 18.52 s.

**Price.** Measured from the FIX-128 LTP sample, which is taken after `create_trade` and before FIX-075 and submission. Source: every `order_placer.entry_slippage_observed` line in TW-LOG 03–15 Sep, matched to its trade by symbol and time.

| Measure | Six (n=57) | Ten (n=69) |
|---|---|---|
| `abs(LTP − trigger)` ₹ — min / p50 / p90 / max | 0 / 0.16 / 1.42 / 3.60 | 0 / 0.13 / 0.98 / 6.15 |
| `abs(LTP − trigger)` % of trigger — p50 / p90 / max | 0.063 / 0.228 / 0.586 | 0.043 / 0.225 / 0.731 |
| Fraction of SL distance consumed — p50 / p90 / max | 0.045 / 0.203 / 0.502 | 0.022 / 0.149 / 0.278 |
| Last price vs the submitted (pre-snap) limit, % of entry — min / p50 / p90 / max | −0.352 / +0.100 / +0.259 / +0.687 | −0.061 / +0.137 / +0.200 / +0.416 |
| … cases positive | 43 of 57 | 68 of 69 |

- **Positive** means the last price was beyond the limit in the trade direction (LONG: LTP above the BUY limit). The limit was resting on the passive side at that instant.
- For the ten, FIX-128 still measures against the Chartink trigger (FF-B5), although their entry was re-anchored.

### (c) Every effect of `pullback_wait_enabled`

**Search:** `grep pullback_wait` over
- every file in WT (excluding `.git`);
- all 1,777 files of the TW snapshot;
- the live VM tree (excluding venv, data_store, logs, `__pycache__`, `.git`, docs, tests);
- `/home/ubuntu`.

| # | Where | Effect | Trees |
|---|---|---|---|
| 1 | `signal_processor._process_one` WT 1129 / TW 1082 | **The only runtime read.** It gates M-S1. | both |
| 2 | TW `signal_processor.py` 1081, 1101, 1180, 1440 | P1 evidence `reanchored` is False for the six by construction (it is set True only inside the gated block) | **TW only** |
| 3 | `strategies/schema.py` 111 `pullback_wait_enabled: bool` (no default) | A YAML without the key fails validation. `StrategyLoader.load_all_strategies`: "ANY invalid file raises ConfigSchemaError immediately — no partial loads" (`strategies/loader.py` 111). | both (identical) |
| 4 | `schema.py` 112-113: `pullback_wait_tolerance_pct: float = 0.005`, `pullback_wait_timeout_sec: int = 180`; validators at 237 and 272-276 | These are sibling keys, not the flag. Their only other mentions are comments on `WatchEntry.tolerance_pct` / `timeout_sec` (`screening/entry_gate.py` 69-70). `EntryGate.add` has no caller (FF-A6), so nothing reads them at runtime. | both |
| 5 | Comment block WT 1110-1128 / TW 1059-1080: "Pullback strategies skip this (EntryGate already waits for current price)" | None. The wait it describes does not run (FF-D1). | both |
| 6 | `config/strategies/*.yaml` | Values: true ×6, false ×10 | both |
| 7 | 10 WT test files (e.g. `test_fix067_ms1_fresh_anchor.py`, `test_signal_processor.py`, `test_strategies.py`) | Tests only | both |
| 8 | docs; `.claude/settings.local.json` (an allowlist string); `/home/ubuntu/preserved/*` backups | No runtime effect | — |

**No hits** in `orders/`, `broker/`, `capital/`, `screening/secondary_screener.py`, `v3_chain/`, `allocation/`, `ops_dashboard/`, `scripts/` or `reports/`.

### (d) Fill rate and outcomes against the ten re-anchored strategies

TW-DB, trades created since 2026-09-01; all LIVE.
- **Fill rate** = trades with `qty_filled > 0` ÷ trades with an ENTRY order row.
- **Cancel cause** is joined from TW-LOG by broker order id. The logs start 03-Sep, so cancels on 01–02 Sep have no cause.
- **P&L** is `trades.net_pnl`, realised ₹ per trade after charges.

| Group | Period | Trades | ENTRY placed | Filled | Fill rate | Trade status | ENTRY cancelled (timeout / FIX-141 / no-log day) | Exit reasons (filled) | Net P&L: sum · mean · median | Wins / losses |
|---|---|---|---|---|---|---|---|---|---|---|
| **Six** | 01–15 Sep | 69 | 53 | 21 | **39.6 %** | FAILED 40 · CLOSED 16 · REJECTED 8 · CLOSED_MANUAL 5 | 32 (26 / 4 / 2) | TGT_HIT 8 · SL_HIT 8 · MANUAL 5 | ₹29.89 · ₹1.42 · −₹2.18 | 9 / 12 |
| Six | LFL836 | 47 | 34 | 18 | 52.9 % | FAILED 21 · CLOSED 14 · REJECTED 8 · CLOSED_MANUAL 4 | 16 | TGT 7 · SL 7 · MANUAL 4 | ₹13.96 · ₹0.78 · −₹2.36 | 7 / 11 |
| Six | VBB097 | 22 | 19 | 3 | 15.8 % | FAILED 19 · CLOSED 2 · CLOSED_MANUAL 1 | 16 | MANUAL 1 · SL 1 · TGT 1 | ₹15.93 · ₹5.31 · ₹10.06 | 2 / 1 |
| **Ten** | 01–15 Sep | 76 | 63 | 27 | **42.9 %** | FAILED 45 · CLOSED 27 · REJECTED 4 | 36 (29 / 4 / 3) | GTT_EXIT 15 · SL_HIT 7 · TGT_HIT 5 | ₹4.80 · ₹0.18 · −₹4.75 | 12 / 15 |
| Ten | LFL836 | 43 | 31 | 15 | 48.4 % | FAILED 24 · CLOSED 15 · REJECTED 4 | 16 | GTT 11 · SL 2 · TGT 2 | ₹6.38 · ₹0.43 · −₹0.47 | 7 / 8 |
| Ten | VBB097 | 33 | 32 | 12 | 37.5 % | FAILED 21 · CLOSED 12 | 20 | SL 5 · GTT 4 · TGT 3 | −₹1.58 · −₹0.13 · −₹4.92 | 5 / 7 |

**Composition** (a fact, not a comparison):
- The six in this period: vwap_bounce_long 31, first_pullback_long 16, vwap_rejection_short 9, first_pullback_short 7, open_high_breakdown_short 3, open_low_breakout_long 3. All are INTRADAY.
- The ten: gap_go_long 29, positional_sector_rotation 20, positional_momentum_long 13, gap_fade_long 6, gap_fade_short 5, gap_go_short 2, positional_swing_long 1.
  - 34 of the 76 are DELIVERY (`positional_*`). Their exits are `GTT_EXIT` and can be multi-day.
- Trades with no ENTRY order row: six 16 (REJECTED 8, FAILED 8); ten 13.

---

## Q3 — CAN ONE FUNCTION OWN THE DERIVATION?

**Status:** ESTABLISHED · **WT↔VM:** DIFFERS-FILE (`_derive_prices` identical; host file differs) · **Paper↔live:** IDENTICAL (derivation)

### (a) Every strategy-specific input `_derive_prices` reads, with defaults

WT lines are shown; TW is WT + 5, because `_derive_prices` starts at WT 1743 / TW 1748 and is identical. Defaults are from `strategies/schema.py`; values are the 16 YAMLs.

| Input | Read at (WT) | Schema default | Values in the 16 YAMLs |
|---|---|---|---|
| `strategy.direction` | 1770 | required (58) | LONG ×10 · SHORT ×6 |
| `strategy.entry_method` | 1774 | required (81) | "LIMIT" ×16 |
| `strategy.entry_offset_pct` | 1775 | 0.0 (82) | 0.001 ×13 · 0.002 ×3 (`positional_*`) |
| `strategy.sl_method` | 1796 | required (85) | "FIXED_PCT" ×16 |
| `strategy.sl_pct` | 1809 | 0.0; > 0 required when FIXED_PCT (86) | 0.008 ×2 · 0.01 ×7 · 0.012 ×2 · 0.015 ×2 · 0.02 ×3 |
| `strategy.sl_min_pct` | 1847 | 0.003 (88) | 0.003 ×13 · 0.005 ×3 |
| `strategy.sl_max_pct` | 1857 | 0.05 (89) | 0.05 ×13 · 0.08 ×3 |
| `strategy.sl_gap_buffer_pct` (read with `getattr(…, 0.0)`) | 1872 | 0.0 (90) | 0.3 ×4 (gap_fade ×2, gap_go ×2); absent ×12 |
| `strategy.name` | log text only | required | — |

**Non-strategy inputs:**
- the reference price argument (trigger or M-S1 LTP);
- `now_time` (gap window `_GAP_WINDOW_START/END` 09:15–09:30 inclusive, 1740-1741; never inside the 10:00 entry start, FF-D6);
- `self._atr_fallback_mode` (ctor default "WARN", 151; wired from `sp_cfg.atr_fallback_mode`, WT `main.py` 3266 / TW 3593).

**The target is a separate method, `_derive_target`** (WT 1896-1948 / TW 1901-1953):
- `tgt_method`: required (93); RISK_REWARD ×16.
- `tgt_pct`: default 0.0 (94).
- `tgt_risk_reward`: default **2.0** (95); 1.5 in all 16 YAMLs.
- `self._tgt_min_pct`: 0.003 (config WT `system_config.yaml` 379 / TW 348). It rejects when `abs(tgt − entry)/entry < 0.003`.

### (b) Needs a single parameterised function could not express

**Among the 16 live YAMLs: none.** Every strategy uses the same operations:
- offset sign by direction;
- FIXED_PCT stop;
- min/max clamp;
- optional time-window gap buffer;
- RISK_REWARD target.

The six pullback-flag strategies differ only in *which reference price reaches the function* (trigger vs M-S1 LTP). That choice is made outside the function, by the flag. No strategy has its own rounding rule. The only rounding is the adapter's tick snap (Q7), which is not strategy-specific.

**Paths outside the live strategy set that use a different reference or formula** (all dormant, shadow or post-fill):

| Path | Reference / formula | State |
|---|---|---|
| SNR-V2 retest | `entry_est = self._retest_entry_estimate(symbol, break_level)` (WT 2476); SL = `structure_sl`; `_derive_target(entry_est, structure_sl, …)` (WT 2500 / TW 2467); MARKET entry | dormant (`wait_for_retest_enabled: false`) |
| EntryGate release | `release_ltp` with `slippage_buffer` ₹2.0 min/max adjustment (`order_placer.py` 905-914) | dormant (`EntryGate.add` has no caller) |
| PB-01 | 5-minute bars | shadow / would-be only (FF-G2) |
| `orders/shadow_tracker.py` `_derive_sl_tgt_from_strategy` (813-~870) | a copy that differs: no gap buffer; no `sl_pct ≤ 0` reject; unknown `sl_method` → `sl = entry`; unknown `tgt_method` → 2 × SL distance; no BL-16 guard; no entry offset | shadow innings |
| FIX-013 post-fill target | `calc_tgt_price(direction, avg_fill_price, sl, rr)` (`orders/price_math.py` 100-116), called at `order_placer.py` 2872 | live, after fill |
| ATR SL/TGT | falls back to FIXED_PCT with a WARNING, or rejects when `atr_fallback_mode` is HALT: "not yet implemented" (WT 1797-1806, 1908-1917) | not used by any YAML |

### (c) Every current caller of `_derive_prices`

| Tree / line | Function | Purpose | Reference price |
|---|---|---|---|
| WT 1079-1081 / TW 1028-1030 | `_process_one` step 4 | first derivation, every strategy | Chartink `trigger_price` |
| WT 1145-1147 / TW 1098-1100 | `_process_one` M-S1 | re-derivation when `pullback_wait_enabled` is false | `live_ltp` |

No other non-test caller exists in either tree. The retest, gate and allocator paths do not call it. Four test files do: `test_e4_event_loop_safety.py`, `test_fix067_ms1_fresh_anchor.py`, `test_fix130_sl_gap_buffer.py`, `test_signal_processor.py`.

**Sibling derivations, for completeness:**
- `_derive_target`:
  - WT 627 (funds-short alert text), 1408 (`_admit_and_place`), 1607 (`_build_v3_signal`, shadow), 2500 (retest);
  - TW 1368, 1588, 2467 (TW has no funds-short alert call).
- `calc_tgt_price`: `order_placer.py` 2715, 2872 (FIX-013), 3166, 3565, 4389 (`_compute_tgt`, used when `tgt_price is None`); `shadow_tracker.py` 330, 855.
- `calc_sl_price`: `shadow_tracker.py` 830.

### (d) What prevents one function owning freshness, failure semantics, tick policy and audit fields

1. **Freshness lives outside the function.**
   - The quote fetch and the success/fallback decision sit in `_process_one` (WT 1129-1152); `_derive_prices` receives a bare float.
   - The quote's timestamp (`Quote.ts = now_ist()`, TW adapter 1771) is dropped by `live_ltp = float(q.last_price)`.
   - `Quote` carries no last-trade time.
   - The flag gate is also outside the function.
2. **Failure semantics are split across four policies in three places:**
   - M-S1: catch-all → WARNING → silent fallback (WT 1135-1152);
   - `_derive_prices`: raises `_PipelineReject` (INVALID_DERIVED_PRICE 1784/1838; REJECTED_NO_ATR_DATA 1799; ZERO_SL 1821), a SignalProcessor-private exception;
   - `_derive_target`: `_PipelineReject` (REJECTED_NO_ATR_DATA, UNKNOWN_TGT_METHOD, TGT_DISTANCE_TOO_SMALL);
   - `OrderPlacer._fetch_ltp`: any error → None → FIX-128 and FIX-075 are skipped (`order_placer.py` 4048-4064; 1109; 1203).
3. **The price is changed after derivation, in another module:** FIX-075 `entry_price = current_ltp` (`order_placer.py` 1261) and FIX-025 `entry_price = adjusted_limit` (914).
4. **Tick policy lives at the broker chokepoint.**
   - `ZerodhaAdapter._snap_order_to_tick` runs after validation (TW 560-569).
   - `InstrumentCache` is bound to the adapter (`set_instrument_cache`) and PositionSizer (TW `main.py` 2852), not to SignalProcessor.
   - `calc_sl_limit_price` uses `tick_size=DEFAULT_TICK` whatever the instrument (`price_math.py` 166; no tick passed at `order_protocol_limit.py` 375-379).
   - `_derive_prices` returns unrounded floats.
5. **Audit fields are written by different modules at different moments:**
   - `trades.entry_target_price`: `OrderManager.create_trade`, before FIX-075;
   - `order_execution_log.intended_price`: `SlippageRecorder`, from `OrderFilled.expected_price`, after FIX-075, fills only;
   - `orders.price`: never written (Q10);
   - TW P1 `entry_price_final` and `reanchored`: evidence JSONL.

   No record holds the quote used or the snapped price.
6. **The guard's reference is decoupled from the derivation's.** FIX-128 measures slippage against `signal_trigger_price`, but its tolerance uses the (possibly re-anchored) `sl_price` (`order_placer.py` 1110, 1117-1121; 351).
7. **The target is split.** `_derive_target` runs inside `_admit_and_place` after `fm.reserve`. The placed TGT is recomputed from the fill by `calc_tgt_price` (FIX-013, 2872). That is two formulas in two modules.
8. **Parallel copies exist:**
   - `shadow_tracker._derive_sl_tgt_from_strategy` (differs, see b);
   - `scripts/forward_shadow_record.py` 214: `entry = m.get("ltp") or r["trigger_price"]`;
   - the ops_dashboard / `SlippageRecorder` allowance distance (Q6b);
   - retest `entry_est`.
9. **The host file differs between the trees.** `signal_processor.py` WT 858e2ce3 vs TW da8c6f98: TW adds Batch-1 evidence, WT adds per-pipeline policy.
10. **Every consumer takes `entry_price` as its own argument**, not from one object:
    - sizer (WT 1158);
    - `fm.reserve` (1362);
    - R:R gate (`order_placer.py` 937-958);
    - FIX-075 margin recompute (1224-1225);
    - `trades.margin_reserved` / `risk_amount` (965-973).

---

## Q4 — FIX-075 DEPENDENCIES

**Status:** ESTABLISHED · **WT↔VM:** MATCH (`order_placer.py` identical; `fund_manager.py` differs by file, cited logic identical) · **Paper↔live:** DIFFER (FIX-075 is live-only)

### (a) Everything downstream of `order_placer.py:1261` that reads `entry_price`

| # | Reader | Lines | What it does with the value |
|---|---|---|---|
| 1 | `self._engine.execute(entry_price=entry_price)` | 1345-1356 | `FullEntryEngine.execute` logs `full_entry_engine.execute entry_price` and forwards it. `LimitTripleProtocol.execute` sets `_entry_order_price = entry_price` (`order_protocol_limit.py` 210). `adapter.place_order(price=…)` validates, snaps to nearest tick, and sends Kite `price=`. In paper, `_paper_place_order` / `_synth_fill` use it as the limit. |
| 2 | `limit_triple.entry_placed` log | `order_protocol_limit.py` 230-237 | logs `"price": entry_price` (pre-snap) |
| 3 | `self._order_monitor.track(expected_price=entry_price)` | 1609-1620 | stored as `_WatchEntry.expected_price` (`order_monitor.py` 64, 294-305) |
| 3a | FIX-141 `_check_price_movement_cancel` | `order_monitor.py` 1151-1157, 1183 | `risk_distance = expected_price − sl_price` (BUY) or `sl_price − expected_price` (SELL); `pending_rr = remaining_reward / risk_distance`; logged as `entry_price` |
| 3b | `_handle_complete` | 990, 996, 1008 | fill fallback `final_price = avg_price if avg_price > 0 else entry.expected_price`; `slippage_pct`; `OrderFilled.expected_price` |
| 3c | `_handle_terminal` (partial) | 1034, 1046 | `slippage_pct`; `OrderPartiallyTerminated.expected_price` |
| 3d | `SlippageRecorder._on_order_filled` | `slippage_recorder.py` 123 | `intended = ev.expected_price` → `order_execution_log.intended_price`, `slippage_rs`/`slippage_pct` |
| 3e | Only through 3b's fallback (Kite `average_price` falsy) | 2118-2122 etc. | `OrderPlacer._handle_entry_fill` → `commit_to_used(actual_fill_price=…)`, `record_entry_fill` (`trades.entry_actual_price`), FIX-013 TGT (2872), clamp gate `entry_fill` |
| 4 | `_format_order_placed_body(entry_price=entry_price)` | 1751-1755 → 864-869 | Telegram "ORDER PLACED" body line `Fill: ₹{entry_price}` — the submitted pre-snap entry, labelled "Fill" |

**Not read after 1261:**
- `risk_amount` and `margin_reserved` (965-973, computed before);
- `trades.entry_target_price` / `sl_initial` / `tgt_initial` (1003-1005, written before);
- `_FillEntry` (1590-1607: no price field);
- `_persist_entry_orders` (1525: no price argument);
- `_check_liquidity` (1294: no price argument);
- `sl_price` and `tgt_price` (unchanged).

### (b) Everything that depends on the top-up succeeding

Code: `order_placer.py` 1228-1271; `FundManager.top_up_reservation` TW 781-892 / WT 778-~889.

**Success** (`top_up_result.success` is True):
- `fm_ledger` TOP_UP row (TW 838-849);
- bucket avail −additional, reserved +additional (852-853);
- the reservation is replaced with `margin = res.margin + additional_margin` (857-869);
- then `entry_price = current_ltp` (1261) and INFO `price_drift_top_up_success`. Every reader in (a) now sees the LTP.
- Later, `commit_to_used` computes `excess = res.margin (including the top-up) − actual_margin` (TW 947), and a zero-fill `release` returns the enlarged margin (`_apply_release`, TW 2191-2195).
- `trades.margin_reserved` is **not** updated; it keeps the pre-drift value (971-973).

**Failure** (`success` False, i.e. `additional_margin > bucket avail`, TW 822-833):
- `_handle_placement_failure(final_status="REJECTED_PRICE_DRIFT")` (1254-1257):
  - Telegram "ORDER REJECTED" (not suppressed);
  - trade status `REJECTED_PRICE_DRIFT` (allowed by the trades CHECK `status GLOB 'REJECTED*'`, `core/schema.sql`);
  - reservation released.
- `OrderRejectedError` is re-raised (1258) → signal `PLACEMENT_FAILED`.
- Measured: **0** trades have that status. Status counts in TW-DB: CANCELLED 9 · CLOSED 308 · CLOSED_MANUAL 61 · FAILED 481 · REJECTED 95.

**Exception inside the top-up** (`ValueError` for an unknown reservation; `CapitalInvariantViolation` after `_handle_invariant_violation` has fired hard_kill):
- It is not an `OrderRejectedError`, so `except Exception` (1277-1289) catches it → WARNING `price_drift_check_failed`, "proceeding with original price".
- After a hard_kill, the A-3 last-mile check (1335-1343) rejects the order.

**`additional_margin ≤ 0`** (LTP at or below the entry, either side): no top-up call; the entry is unchanged (comment at 1272).

### (c) What changes if the top-up block (1194-1289) is removed entirely — traced

1. **One broker call per live placement disappears:** one `_fetch_ltp` → `get_quote_raw` → a quote-bucket token and a `kite.quote` call. The FIX-128 fetch at 1108 remains.
2. **Every value in (a) carries the pre-drift entry.** The submitted LIMIT, `expected_price`, `order_execution_log.intended_price`, FIX-141's risk distance, the `limit_triple.entry_placed` log and the Telegram "Fill:" line would always equal `trades.entry_target_price`. Today they differ on the 8 top-up trades (1 of 213 enriched OEL ENTRY rows, FF-H5).
3. **No TOP_UP ledger rows.** The reservation stays at its reserve-time size, `qty × entry / leverage × 1.05` (TW 558-563).
4. **The `REJECTED_PRICE_DRIFT` outcome disappears.** Those orders would reach `engine.execute` at the pre-drift price.
5. **Capital commit uses `excess = res.margin − qty × fill / leverage`** (TW 941-947).
   - A BUY LIMIT fills at or below its limit, so a LONG fill is ≤ `snap(entry)` ≤ `entry + tick/2`.
   - A SELL LIMIT fills at or above its limit, so a SHORT filled above `1.05 × entry` would give a negative `excess`. `_apply_commit` adds it to avail (TW 2209-2210); a negative bucket avail raises `CapitalInvariantViolation` → hard_kill (TW 2427-2440; 986-1040).
   - This path exists today as well for a SHORT, because FIX-075 adds margin only when the LTP rises.
   - Measured: **0 of 368** COMMIT rows had negative excess. Fill ÷ reserve price: SHORT max 1.00224 (n=41); LONG max 1.01136 (n=327, including top-ups).
6. **Orphaned code.**
   - `FundManager.top_up_reservation` would have no caller (the only caller is `order_placer.py` 1230).
   - `OrderPlacer(price_drift_threshold=…)` (585, stored at 668) would be unread.
   - `risk.price_drift_threshold` (WT `system_config.yaml` 356 / TW 325) and `RiskConfig.price_drift_threshold` (WT `core/config_loader.py` 633 / TW 807) are already unwired, because `main.py` never passes them (FF-A1).
   - TW `ops_dashboard/backend/services/config_view.py` 649-652 displays that config value.
7. **Tests that reference the block** (grep only; no tests were run): `tests/unit/test_fix075_price_drift.py`, `test_daily_trade_review.py`, `test_terminal_state_write_guard.py`.
8. **Nothing else branches on the top-up outcome.** No other reader of `price_drift`, `TOP_UP` or `top_up` exists in non-test code in either tree, apart from the dashboard display.

### (d) Is `_price_drift_threshold` read anywhere else?

**No.** It is read only at `order_placer.py` 1207 (`drift_threshold = self._price_drift_threshold`) and set at 668 from the ctor default `price_drift_threshold: float = 0.005` (585). MATCH in both trees. The config key never reaches it.

### (e) Every trade where the top-up fired

- **Source:** `fm_ledger` `entry_type='TOP_UP'`, the complete DB record. The row is written only on the success path, before 1261. The DB spans 2026-06-15 onward.
- **Log cross-check:** in TW-LOG 03–15 Sep plus LOCAL-LOG 31-Aug, `price_drift_detected` 1 and `price_drift_top_up_success` 1 (QUICKHEAL 07-Sep); `rejected_price_drift` 0; `price_drift_check_failed` 0.
- **R:R** = `(TGT − entry)/(entry − SL)` using `trades.sl_initial` / `tgt_initial`, which FIX-075 never moves. All 8 are LONG.

| ledger_id | Time | trade_id | Symbol | Strategy (reserve intent) | Trigger | Pre-drift entry | Post-drift entry | Top-up ₹ | SL | TGT | R:R pre | R:R post | Fill | R:R at fill | Outcome (net ₹) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7078 | 17-Jun 10:00:26 | trd_10a1e76730244090bccc39570694dfa0 | LLOYDSENGG | positional_sector_rotation (INTRADAY) | 83.18 | 83.01 | 83.45 | 0.5280 | 81.35 | 86.33 | 2.0000 | 1.3714 | 83.44 | 1.3828 | CLOSED TGT_HIT +24.53 |
| 7098 | 17-Jun 10:33:17 | trd_179dd9e9896a409283a5ea61ad518352 | CHEMPLASTS | **first_pullback_long** (INTRADAY) | 221.31 | 221.05 | 223.59 | 1.0160 | 217.75 | 227.70 | 2.0152 | **0.7038** | 223.60 | 0.7009 | CLOSED TGT_HIT +22.92 |
| 7201 | 19-Jun 10:00:25 | trd_f8014d0c6ca34ba189503bcd6b0fbddd | THELEELA | positional_sector_rotation (INTRADAY) | 482.50 | 481.50 | 484.60 | 0.6200 | 471.90 | 500.75 | 2.0052 | 1.2717 | 484.60 | 1.2717 | CLOSED_MANUAL −0.95 |
| 7479 | 24-Jun 10:11:12 | trd_68b3b559209648f3913aefc7dbb66bee | HUBTOWN | positional_sector_rotation (INTRADAY) | 217.93 | 217.49414 | 218.72 | 0.4903 | 213.144257 | 226.193906 | 2.0000 | 1.3404 | 218.72 | 1.3404 | CLOSED SL_HIT −11.70 |
| 7537 | 24-Jun 12:40:29 | trd_00aea08a023f4df5aa07511024ccecfa | INDOSTAR | positional_swing_long (INTRADAY) | 260.00 | 259.48 | 261.00 | 0.3040 | 254.2904 | 269.8592 | 2.0000 | 1.3204 | 260.94 | 1.3413 | CLOSED_MANUAL −1.90 |
| 7548 | 24-Jun 14:49:20 | trd_eb81db53c07748e49d63e0467b061365 | PACEDIGITK | positional_swing_long (INTRADAY) | 215.00 | 214.57 | 215.66 | 0.4360 | 210.2786 | 223.1528 | 2.0000 | 1.3924 | 215.66 | 1.3924 | CLOSED_MANUAL −3.70 |
| 7934 | 01-Jul 10:02:13 | trd_f89fe392fd04472ab7a5e432d3d1264b | JTEKTINDIA | positional_sector_rotation (INTRADAY) | 142.87 | 142.58426 | 143.52 | 0.5614 | 139.732575 | 146.861788 | 1.5000 | **0.8823** | 143.52 | 0.8823 | CLOSED TGT_HIT +15.98 |
| 12098 | 07-Sep 10:01:18 | trd_1ce14a6d5e024ffaa0d96fe7b4ef74b4 | QUICKHEAL | positional_sector_rotation (DELIVERY) | 158.52 | 157.9335 | 158.73 | 2.3895 | 154.77483 | 162.671505 | 1.5000 | **0.9965** | 158.73 | 0.9965 | CLOSED GTT_EXIT −13.71 |

- **Arithmetic check:** each top-up equals `qty × (post − pre) / leverage` exactly — leverage 5 for INTRADAY, 1 for DELIVERY. For example, LLOYDSENGG 6 × 0.44 / 5 = 0.528; QUICKHEAL 3 × 0.7965 / 1 = 2.3895.
- **Post-drift source:** the ledger reason (`… → ₹X`, 2 decimals). For QUICKHEAL it is confirmed by `order_execution_log.intended_price` 158.73.
- **Pre-drift source:** `trades.entry_target_price`. On the June rows this value was stored after an order-placer rounding that has since been removed (comment at `order_placer.py` 928-931). The RESERVE reason shows the unrounded value (for example `@ 83.01364…`).
- **June positional intent:** positional strategies reserved as INTRADAY in June. That was the load-time DELIVERY→INTRADAY rewrite, removed 10-Jul (`strategies/loader.py` docstring 114-115).

---

## Q5 — THE RESERVATION CALCULATION

**Status:** ESTABLISHED (broker's real MIS margin NOT ESTABLISHED) · **WT↔VM:** reserve/top-up/commit DIFFERS-FILE (cited formulas identical); sizing **DIFFERS-LOGIC** · **Paper↔live:** IDENTICAL formulas (capital seed differs, FF-G1 D2)

### (a) `fm.reserve` at `_admit_and_place`

**Call:** `reservation = self._fm.reserve(symbol, sizing.qty, entry_price, strategy_obj.intent, signal_id, strategy=strategy_name)` (WT `signal_processor.py` 1362-1365 / TW 1327-1330), inside `portfolio_lock`.

**Price used:** `entry_price` from `_derive_prices`:
- LTP-anchored for the ten; trigger-anchored for the six;
- unrounded;
- taken before `_derive_target`, FIX-128, FIX-075 and the tick snap.

**Formula as written** (TW `capital/fund_manager.py` 557-563 / WT 553-559):

```
bucket       = self._bucket_for_intent(intent)
base_margin  = required_margin(qty, price, intent, self._leverage_map)   # = (qty * price) / leverage_map.get(intent, 1.0)   (TW 248-268)
slm_buffer   = base_margin * self._slm_buffer_pct                          # slm_margin_buffer_pct 0.05 (config TW 203 / WT 168; ctor default 0.05)
total_margin = base_margin + slm_buffer
if total_margin > avail_before: return failure                             # TW 565-577
```

- Ledger RESERVE: `amount=total_margin`, reason `"{symbol} qty={qty} @ {price} intent={intent} (base=… buffer=…)"` (TW 584-595).
- `_apply_reserve`: avail −total, reserved +total (TW 2153-2189).
- `trades.margin_reserved` is a different figure: `fm.required_margin(qty, entry_price, intent)` **without** the buffer (`order_placer.py` 971-973).
- Other `reserve` callers (dormant): WT 2208 / TW 2158 (gate path, `entry_price`); WT 2523 / TW 2491 (retest path, `entry_est`).

### (b) Quantity sizing in PositionSizer

Same `entry_price` argument (WT 1158 / TW 1112).

**TW (deployed)** — `PositionSizer._calculate`, `capital/position_sizer.py` 254-809:

```
sl_distance          = abs(entry_price - sl_price)                              # 424
qty_by_risk          = floor(total_capital * eff_risk_pct / sl_distance)        # 456-457
leverage             = leverage_map.get(intent, 1.0)                            # 388 — live margin only if broker_adapter set (389-423); TW main.py 2840-2863 passes none
effective_entry      = entry_price * (1.0 + entry_offset_pct)                   # 492 — SignalProcessor passes no entry_offset_pct → 0.0
margin_per_share     = effective_entry / leverage                               # 493
qty_by_capital       = floor(avail_bucket / margin_per_share)                   # 494-496
qty_by_concentration = floor(total_capital * eff_conc_pct / entry_price)        # 498-500
raw = min(...); tier/flat (541-636); lot rounding (639)
position_value = final_qty * entry_price  vs  eff_max_position_value_pct * total_capital   # 721-752
margin_required = final_qty * margin_per_share                                   # 781 — no SL-M buffer
```

**WT (not deployed)** — allocation model, `capital/position_sizer.py`:

```
basis                     = pol.planning_basis(total_capital, planning_leverage)          # 425-427
allocation                = basis / allocation_divisor * min(1.0, effective_mult)         # 439, 574-575
qty_by_allocation         = floor((allocation * sl_rupees / entry_price) / sl_rupees)      # 586-589
margin_per_share          = entry_price * (1 + entry_offset_pct) / leverage                # 636-642
qty_by_segment_capital    = floor(avail / (entry_price * (1 + offset) / planning_leverage))# 647-650
qty_by_concentration      = floor(basis * eff_max_concentration_pct / entry_price)         # 658-660
qty_by_max_position_value = floor(basis * eff_max_position_value_pct / entry_price)        # 661-663
```

### (c) The margin top-up in FIX-075

`order_placer.py` 1224-1234:

```
original_margin   = self._fm.required_margin(qty, original_entry_price, intent)
new_margin        = self._fm.required_margin(qty, current_ltp, intent)
additional_margin = new_margin - original_margin      # = qty * (current_ltp - original_entry_price) / leverage
if additional_margin > 0: self._fm.top_up_reservation(reservation_id, additional_margin, …)
```

- **Price:** `current_ltp`, the `last_price` from `_fetch_ltp` → `get_quote_raw`.
- The increment carries **no** 5 % SL-M buffer (TW `fund_manager.py` 857: `new_margin = res.margin + additional_margin`).
- Measured: all 8 ledger top-ups equal `qty × (post − pre)/leverage` (Q4e).

### (d) `commit_to_used` after a fill

TW `capital/fund_manager.py` 894-1040 / WT 892-~1038:

```
actual_margin = required_margin(actual_qty, actual_fill_price, res.intent, self._leverage_map)   # 941-943
excess        = res.margin - actual_margin      # "Allow negative excess: when fill price > reserved price …"  (944-947)
ledger COMMIT (954-968); _apply_commit: reserved -= res.margin; used += actual_margin; avail += excess   (2197-2210)
self._check_invariant("commit_to_used", …)   (978);  any exception → kill_switch.hard_kill (986-1040)
```

**Callers** (`order_placer.py`, identical in both trees):
- `_handle_entry_fill` 2118-2122: `actual_fill_price=event.avg_fill_price, actual_qty=event.filled_qty`;
- `_on_order_partially_terminated` 1849-1853: `avg_price`, `qty_filled`;
- `_on_order_status_changed` partial fallback 2040-2044.

**Price:** `OrderFilled.avg_fill_price`. That is Kite's `average_price` from the last order-history row, or `entry.expected_price` (the submitted pre-snap entry) when that is falsy (`order_monitor.py` 990).

### (e) LONG vs SHORT

**From the formulas:**
- **No reservation formula takes a side.** `required_margin(qty, price, intent, leverage_map)` (TW 248-268) has no side parameter, and `reserve`, `top_up_reservation` and `commit_to_used` pass none. A LONG and a SHORT with the same qty, price and intent reserve identically.
- **For a SHORT, a higher fill price consumes MORE reserved capacity.**
  - `actual_margin = qty × fill / leverage` rises with the fill, so `excess = res.margin − actual_margin` falls.
  - Once `fill > res.margin × leverage / qty` (= 1.05 × the reserve price when there was no top-up), `excess` is negative and `_apply_commit` deducts it from avail (TW 2209-2210).
  - For a LONG, a lower fill consumes less.
- **FIX-075 is also side-blind.** It tops up only when `current_ltp > original_entry_price`, for both sides. The comment at 1272, "drift increased price but less margin needed (e.g., SHORT position)", does not match the formula, which has no side term.
- **Sizing uses the side only in the PS10 direction warning** (TW `position_sizer.py` 342-353).

**Measured** (TW-DB, `fm_ledger` COMMIT joined to RESERVE):

| Direction | Commits | Negative excess | Fill ÷ reserve price (min / p50 / max) | Above 1.0 |
|---|---|---|---|---|
| LONG | 327 | 0 | 0.99521 / 1.00000 / 1.01136 | 145 |
| SHORT | 41 | 0 | 0.99992 / 1.00000 / 1.00224 | 21 |

### (f) Reservation, the MIS leverage map, and effective buying power

**File `capital/fund_manager.py`:**
- `required_margin()` (TW 248-268): margin = `qty × price / leverage_map.get(intent, 1.0)`.
- `FundManager.__init__`: stores `leverage_map`; FM12 requires an entry for every intent (WT 331-334).
- `FundManager.reserve()` (TW 521-635): checks only the intent's bucket (`_bucket_for_intent`, `_bucket_avail`).
- `FundManager._bucket_base()` (TW 2311-2335, "FIX 1"): `(total − carry_total) × pct + own carry`.
- `FundManager.initialize()` (TW ~446-490): `intraday_avail = balance × intraday_pct`, `positional_avail = balance × positional_pct`.

**Wiring** (TW `main.py` 2676-2736):
- `leverage_map = {INTRADAY, COVER_ORDER, DELIVERY, BRACKET_ORDER}` from `capital.leverage_map`: INTRADAY 5.0 · COVER_ORDER 6.0 · DELIVERY 1.0 · BRACKET_ORDER 5.0 (TW config 207-211 / WT 172-176, same values).
- TW only: `leverage_safety` min 1.0 / max 10.0 (212-214).
- Bucket split: `resolve_bucket_allocation(conditional_enabled=cap_cfg.conditional_allocation_enabled, …)` (TW `fund_manager.py` 112-146). The flag is `false` (TW config 199), so the fixed 0.70 / 0.30 split applies (197-198).
- The same `leverage_map` object goes to `PositionSizer` (TW `main.py` 2842).

**Effective buying power, as computed:**
- A MIS order consumes `qty × price / 5 × 1.05` of intraday avail, so notional capacity = intraday avail × 5 / 1.05.
- A CNC order consumes `qty × price × 1.05` of positional avail.
- Sizing's capital rung, `floor(avail / (entry/leverage))` (TW `position_sizer.py` 494-496), allows avail × leverage **without** the 5 % buffer that `reserve` then adds.
- The broker's actual MIS margin for a symbol is never consulted, neither in reserve nor in TW sizing (static leverage). **NOT ESTABLISHED:** the broker's real per-symbol margin.

**WT differences:** `fund_manager.py` lacks TW's FIX-1 carry fields and adds the per-pipeline policy; WT sizing uses `basis = bucket × planning_leverage` (b).

---

## Q6 — THE ALLOWANCE AS IT EXISTS TODAY

**Status:** ESTABLISHED · **WT↔VM:** MATCH (order path); dashboard DIFFERS-FILE · **Paper↔live:** DIFFER (the guard runs only when an LTP is fetched, never in paper; the fraction is recorded in both)

Confirmed: **`min(0.22 × abs(trigger − sl), ₹5.00)`, capped at ₹10.00**, mode `sl_fraction`, override maps empty (FF-A2…A8).

### (a) Every place the value is computed, read or logged

**Computed** (`orders/order_placer.py`, identical in both trees):
1. `resolve_slippage_fraction(cfg, symbol, strategy, price_band)` 251-276 → `(fraction, source)`. Called in `place()` at 983-991 only when `enabled` and `mode == "sl_fraction"`; the band price is `signal_trigger_price` (986-988).
2. `_compute_slippage_tolerance(cfg, signal_price, sl_price, tier_tuples, max_pct, fraction_override)` 325-361.
3. `_slippage_decision(…)` 364-390, called once at 1117-1121 with `signal_trigger_price`, `sl_price`, `_slip_rs = abs(LTP − trigger)` and `_slip_pct`.
4. Legacy branch when `slippage_control` is disabled: `_slip_tol = signal_trigger_price × max_entry_slippage_pct / 100` (1122-1129). Inactive (FF-A5).

**Logged or written as text:**

5. INFO `order_placer.entry_slippage_observed` (1134-1149): `tolerance_rs`, `sl_distance_rs`, `fraction_of_sl_used`, `tolerance_fraction`, `tolerance_source`, `trigger_price`, `current_ltp`, `slippage_rs/pct`, `aborted`.
6. **On abort:**
   - `OrderRejectedError("slippage_exceeded: trigger=… ltp=… | slippage ₹x > tolerance ₹y (mode=…, SL_dist=₹z, n% of SL)")` (1151-1155; reason text 383-386);
   - WARNING `order_placer.slippage_guard_exceeded` (1156-1169);
   - Telegram "SLIPPAGE GUARD" (1170-1185);
   - `_handle_placement_failure` → `fm_ledger` RELEASE reason `placement_failed: {exc}` (4452);
   - SignalProcessor's outer handler → `signals.rejection_reason` (`update_signal_status(..., "PLACEMENT_FAILED", str(exc))`, WT 1273 / TW 1238).

**Persisted (fraction only):**

7. `trades.tolerance_fraction_used`, `trades.tolerance_source` via `create_trade` (`order_placer.py` 1011-1012; `order_manager.py` WT 192-193).
8. `order_execution_log.tolerance_fraction_used` / `tolerance_source`, copied from the parent trade by `SlippageRecorder` (`slippage_recorder.py` 146-147, 276-282).

**Read or recomputed elsewhere:**

9. `ops_dashboard/backend/api/analytics.py` `get_slippage` 33-51 (WT and TW): `tol = min(frac × planned_sl_distance, cap)` (50), used for a breach flag.
10. TW only: `ops_dashboard/backend/services/slippage_analytics.py` `allowed_slippage` 153-173 (not present in WT).
11. `ops_dashboard/backend/services/capacity.py` (WT 306-308 / TW 298-300) and TW `config_view.py` 489-521: display of the config.
12. TW `ops_dashboard/backend/readers/db_reader.py` 1772-1809, 2439: reads the two trade columns.
13. `reports/daily_trade_review.py` 427: reads `tolerance_fraction_used`.
14. `scripts/system_manager.py` WT 982-997 / TW 983-997: reads the config global and counts `tolerance_source`.
15. Config model `SlippageControlConfig` (WT `core/config_loader.py` 1584-1589 / TW 1767-1772): defaults 0.22 / 5.0 / 10.0.

### (b) Is it ever computed from anything other than `abs(signal_price − sl_price)`?

**On the order path, in the deployed mode: no.** In `sl_fraction` the only distance is `sl_dist = abs(signal_price - sl_price)` (351). Two notes:
- `signal_price` is the Chartink trigger.
- `sl_price` is the SL passed to `place()`. For the ten, that SL was derived from the M-S1 LTP, so the distance mixes two reference prices (FF-B5).

Inactive modes use other inputs: `flat_tiers` uses the trigger's price band (355-356); `pct` uses `signal_price × max_pct %` (357-358); an unknown mode uses `absolute_cap_rs` (359-360).

**Outside the order path: yes.**
- `trade_slippage_log.planned_sl_distance = abs(entry_target_price − sl_initial)` (`SlippageRecorder.build_trade_slippage_row`, `slippage_recorder.py` 204).
- The ops_dashboard multiplies that by the fraction to show "allowed slippage" (items 9–10).
- That distance starts from the **derived entry**, not the trigger.

### (c) When `sl_price` is unavailable

`_compute_slippage_tolerance`, `order_placer.py` 350-354, 361:

```
if sl_price is not None and sl_price > 0:
    sl_dist = abs(signal_price - sl_price)
    tol = min(sl_dist * frac, cfg.absolute_cap_rs)
else:
    tol = cfg.absolute_cap_rs        # SL unavailable -> backstop only
...
return min(tol, cfg.hard_max_slippage_rs), sl_dist
```

- The result is ₹5.00 with `sl_dist` None.
- `_slippage_decision` then omits the SL_dist text (384), and the log records `sl_distance_rs` and `fraction_of_sl_used` as null (1140-1143).
- **Reachability:** `place()` requires `sl_price: float`, and `_derive_prices` always returns a positive SL clamped by `sl_min_pct`.
- The dashboard mirror is `tol = … if dist else absolute_cap_rs`.

### (d) Is the value persisted per trade?

- **The fraction and its source: yes** — `trades.tolerance_fraction_used`, `trades.tolerance_source`, and the OEL copy.
- **The rupee allowance itself: no column.** It exists only as text in `signals.rejection_reason` and `fm_ledger.reason` for the 95 aborted trades (FF-H1), and in INFO log lines.

### (e) Measured distribution

TW-DB, all 954 trades. Recomputed from `signals.trigger_price`, `trades.sl_initial` and `tolerance_fraction_used` with the formula as written: `min(min(abs(trigger − sl) × frac, 5.00), 10.00)`. "% of entry" divides by `trades.entry_target_price`.

| Set | n | Span | ₹ min | ₹ p10 | ₹ p50 | ₹ p90 | ₹ max | % min | % p10 | % p50 | % p90 | % max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fraction recorded (0.22, `global`) | 891 | 22-Jun → 15-Sep | 0.0647 | 0.4241 | 0.8255 | 2.3441 | 5.0000 | 0.0176 | 0.1980 | 0.2710 | 0.4841 | 0.7405 |
| Fraction NULL (0.22 assumed) | 63 | 15-Jun → 19-Jun | 0.2024 | 0.3586 | 0.8756 | 2.4112 | 4.3340 | 0.1969 | 0.2412 | 0.2873 | 0.4846 | 0.4862 |
| All | 954 | | 0.0647 | 0.4218 | 0.8269 | 2.3448 | 5.0000 | 0.0176 | 0.1980 | 0.2840 | 0.4841 | 0.7405 |

- The ₹5.00 cap binds on **4** of 954 trades; the ₹10.00 ceiling on 0.
- p50 by month (all): Jun 0.6528 (n=173) · Jul 0.8172 (305) · Aug 0.9137 (331) · Sep 0.8435 (145).
- **Cross-check:** all **126** `entry_slippage_observed` lines (03–15 Sep) match the recomputed `tolerance_rs` and `sl_distance_rs` to ±0.005 (0 mismatched, 0 unmatched).
- **Control:** recomputing with fraction 0.20 matches **0** of 126.

This is the value the formula yields for each trade's stored inputs. The guard evaluated it only when an LTP was fetched (live).

---

## Q7 — TICK ROUNDING DIRECTION

**Status:** PARTIAL — (a)–(c) ESTABLISHED; (d) real tick ≤ 0.01 ESTABLISHED, exact tick NOT ESTABLISHED; (e) pre-09:00 file NOT ESTABLISHED · **WT↔VM:** MATCH (rounding code identical; adapter file DIFFERS-FILE) · **Paper↔live:** IDENTICAL (snap runs in both; TW adapter 564-569)

Rounding helpers (`broker/slippage_engine.py`, identical): `_round_up_to_tick` uses ROUND_CEILING (~145-157), `_round_down_to_tick` uses ROUND_FLOOR (160-171), and `_round_nearest_to_tick` uses ROUND_HALF_UP (174-185). All work on `Decimal(str(value)) / Decimal(str(tick))`. `orders/price_math.py` `round_to_tick` (30-57) maps modes up / down / nearest the same way.

### (a) The derived entry price

- **No rounding.** `_derive_prices` returns `reference × (1 ∓ offset)` unrounded (WT 1773-1779 / TW 1778-1784).
- It is stored unrounded in `trades.entry_target_price` (for example 219.19074).
- **Direction:** not applicable; nothing rounds it before the adapter.

### (b) The submitted LIMIT price

- `ZerodhaAdapter._snap_order_to_tick`, non-SL branch: `new_price = _round_nearest_to_tick(price, tick)` (TW 1448-1450 / WT 1400-1402).
- **Direction:** nearest tick; an exact half tick rounds **up**.
- The tick comes from `_resolve_tick`: the instrument cache, else `DEFAULT_TICK` 0.05 (Q7d).
- The snap runs after `_validate_place_order` (TW 560-569).

**Can it move to the adverse side? Yes, by up to tick/2:**
- a BUY limit rounded up pays more than the derived entry;
- a SELL limit rounded down sells for less;
- at an exact half tick, a BUY moves up (adverse) and a SELL moves up (favourable).

**Measured** (TW-DB, filled trades, excluding the 8 top-ups). *INFERENCE from LIMIT semantics:* a BUY LIMIT cannot fill above its limit and a SELL LIMIT cannot fill below it.
- **137 of 319** LONG fills were above the unrounded derived entry.
- **19 of 41** SHORT fills were below it.
- The largest adverse gap was ₹0.025 (M&MFIN 22-Jul, tick 0.05), exactly tick/2.

### (c) The SL trigger and SL limit on the exit leg (LIMIT_TRIPLE, identical code)

**SL trigger**
- **Path:** `sl_price` (the strategy SL from the derivation; never re-anchored to the fill) → optional `clamp_exit_into_band` (`price_math.py` 284-377). The clamp moves it only if it lies outside `[lower × 1.02, upper × 0.98]`, with the band edges rounded up and down.
- Then the adapter's SL branch: `new_trigger = _round_nearest_to_tick(trigger_price, tick)` (TW 1446-1447).
- **Direction:** nearest, up to tick/2 either way.
  - For a LONG's SELL stop, rounding up moves the stop toward the entry (earlier trigger, smaller planned loss); rounding down moves it away (a larger loss if hit).
  - SHORT is mirrored.

**SL limit**
- `calc_sl_limit_price(exit_side, trigger_price=sl_price, offset_pct=0.005)` (`order_protocol_limit.py` 374-379 → `price_math.py` 162-217):
  - SELL: `sl_price × 0.995`, then `round_to_tick(…, DEFAULT_TICK=0.05, "down")`;
  - BUY: `× 1.005`, then `"up"`.
- The adapter's SL branch rounds the limit again with the instrument tick: SELL `_round_down_to_tick`, BUY `_round_up_to_tick` (TW 1439-1445).
- **Direction:** always further past the trigger. The worst acceptable exit price only widens — by up to one 0.05 step plus one instrument tick.
- The first floor/ceiling uses 0.05 whatever the instrument's tick (no tick is passed at `order_protocol_limit.py` 375-379).

**TGT (for completeness)**
- `calc_tgt_price` from the fill (FIX-013) → clamp → adapter LIMIT nearest, up to tick/2 either way.
- A LONG TGT rounded down means less profit; a SHORT TGT rounded up means less profit.

### (d) The DEFAULT_TICK = 0.05 fallbacks

**Why they fired:**
- None of the five symbols is in `config/reference_data/security_master_file.csv` (0 matches), and that file is the only row source for `config/instruments.csv` (`refresh_instruments.py` `_load_security_master` → `_build_rows`).
- So `InstrumentCache.tick_size(symbol)` raises, and `_resolve_tick` returns 0.05 with one WARNING per process (TW 1391-1406).

**Real tick:** Kite's instrument dump, which would state it, is not stored anywhere, and no broker call was made. It was measured from traded prices instead — a tick must divide every traded price. Sources: 1-minute Kite historical bars (`analytics.db.candles`, September) and logged LTPs.

| Symbol | Fallback WARNINGs (TW-LOG) | Traded-price evidence | Real tick (as observed) | 0.05 vs real |
|---|---|---|---|---|
| RIR | 07-Sep 10:00:28 | 3,000 bar prices (07, 10 Sep); 1,892 not multiples of 0.05 (e.g. 175.04, 183.34) | ≤ 0.01 | **larger** |
| XTRANET | 04-Sep 10:59:16 · 07-Sep 10:51:17 | 6,000 prices (02, 04, 07, 09 Sep); 4,100 not multiples of 0.05 (e.g. 187.19, 186.96) | ≤ 0.01 | **larger** |
| MAFANG | 07-Sep 11:27:21 · 08-Sep 10:02:17 · 11-Sep 14:59:21 | 4,500 prices (07, 09, 11 Sep); 2,830 not multiples of 0.05 (e.g. 212.74); logged LTPs 219.63 / 219.66 / 219.67 | ≤ 0.01 | **larger** |
| NIFTY1 | 08-Sep 11:47:22 | No bars stored; FIX-128 logged `current_ltp` 262.58 at 11:47:18 (trigger 262.58) | ≤ 0.01 | **larger** |
| MONQ50 | 09-Sep 13:40:12 | 4,500 prices (07, 09, 11 Sep); 2,684 not multiples of 0.05 (e.g. 145.47) | ≤ 0.01 | **larger** |

- "≤ 0.01" is the largest tick consistent with the observed prices. Whether the exact tick is smaller is **NOT ESTABLISHED**. The smallest tick in `instruments.csv` is 0.01 (970 rows).
- **Effect as written:** nearest rounding to 0.05 can move an entry by up to ₹0.025, against ≤ ₹0.005 at 0.01. A 0.05 multiple is also a valid 0.01 multiple, so the order is accepted (docstring TW 1387-1389).
- **Related (RI12):** `refresh_instruments.py` 25 and 170-185 write `tick_size = 0.05` for every security-master symbol not matched in Kite's dump.
  - The current file has **205** such rows (token 0), all with tick 0.05.
  - The cron log shows 205–218 unmatched per run.

### (e) Does the 09:00 rewrite leave the process with a stale tick table?

**Loaded once:**
- `InstrumentCache.load(config_dir / "instruments.csv")` at boot (WT `main.py` 2157 / TW 2441), bound to the adapter via `set_instrument_cache` (log: "adapter.set_instrument_cache bound").
- `InstrumentCache.reload()` exists (`core/instrument_cache.py` 187-215, FIX-092) and has **no caller** in either tree.

**Rewritten after boot:** `scripts/refresh_instruments.py` runs at 09:00 Mon–Fri (VM crontab line 70) and replaces the file with `os.replace` (RI6).

**Which file each boot read** (`cron_heartbeat` + boot logs; testing-VM runs only):

| Boot | Rows loaded | File it read |
|---|---|---|
| 15-Sep 08:15:24 | 2,228 | Output of the 11-Sep 09:00:02 run. 14-Sep was SKIPPED ("non-trading day"); the 15-Sep SUCCESS at 09:00:02 came after this boot. |
| 11-Sep 08:15:08 | — | Output of the 10-Sep 09:00 run |
| 11-Sep 09:16:45 (restart) | — | Output of the 11-Sep 09:00 run |
| 10-Sep 08:15:26 | — | The file present before the 10-Sep run, because the 09-Sep 09:00 run FAILED ("SystemExit: 2"; log "token file not found"). **Its origin (clone copy) is NOT ESTABLISHED.** |

**Contents of the pre-09:00 file: NOT ESTABLISHED — not recoverable.** Searched:
- the VM filesystem (`find /home/ubuntu /var/log /tmp -iname "*instrument*"` → only the live file, the script, the cache module and the cron log);
- the script, which writes no backup;
- git (the file is gitignored, `.gitignore` 39);
- the cron log, which records only counts ("Built 2228 rows. Validation passed.", "205 symbols not in Kite data");
- `config_snapshots`, which holds no instrument data.

**What can be said:**
1. The in-memory table for a whole session is the previous refresh's output, one or more sessions old.
2. **Tick sizes change over time.** Nine filled trades (06–31 Jul) have fills that are impossible under **today's** table (INFERENCE from LIMIT semantics):
   - LOTUSDEV 22-Jul: entry 154.65519; today's tick 0.05 snaps the BUY limit to 154.65, but it filled at 154.66.
   - SPANDANA 06-Jul: entry 312.687; today's tick 0.01 gives 312.69, but it filled at 312.70.

   So the tick in force on those dates differed from today's file.
3. Whether any tick changed between a 09:00 refresh and the next 08:15 load is **NOT ESTABLISHED**.

---

## Q8 — ACHIEVABLE QUOTE POLLING CADENCE (MEASURED ONLY)

**Status:** PARTIAL (broker-side limit and headroom NOT ESTABLISHED; unlogged quote calls not counted) · **WT↔VM:** MATCH (`order_monitor.py`, `rate_limiter.py`, `broker_limits.yaml` identical) · **Paper↔live:** DIFFER (paper quotes use the 3 s cache provider without the RateLimiter; FF-G1 D3)

### (a) The mechanism FIX-141 uses

**Loop.** `OrderMonitor._poll_loop` (`order_monitor.py` 594-600): `self._stop_event.wait(timeout=self._poll_interval)` — `poll_interval_sec` 2, config TW 193 / WT 158 — then `_poll_cycle()`.

**Cycle.** `_poll_cycle` (602-630) snapshots **all** tracked orders (ENTRY, SL, TGT, EOD), runs `_check_force_close`, then calls `_process_order` for each order **sequentially in the one monitor thread**.

**Call chain** per order:
- `_process_order` → `adapter.get_order_history(broker_order_id)` → rate-limiter category **`order`** (`_CATEGORY_MAP`, TW adapter 254-269).
- On Kite status OPEN / TRIGGER PENDING / SUBMITTED → `_handle_open` (877-881) → `_check_fill_timeout`, then `_check_price_movement_cancel` (1128-1207).
- → `_ltp_expected_fallback(symbol)` (316-338) → `adapter.get_quote([symbol])` → live: `self._rl.acquire("quote")` (TW 1757), then `self._kite.quote("NSE:SYM")` (1762).
- Any failure returns 0.0 and the check is skipped.

**Cost per ENTRY per poll:**
- 1 `order` token + 1 order-history HTTP call. Measured duration over 81,795 calls: p50 17 ms, p99 34 ms.
- While OPEN, also 1 `quote` token + 1 `kite.quote` HTTP call. Measured duration including the wait for a token: p1 12 ms · p10 14 ms · p25 21 ms · **p50 617 ms**.

**Blocking.** `RateLimiter.acquire` waits for a token for up to `max_wait_sec` — 30 s default (`broker/rate_limiter.py` 152); `main.py` passes only `shutdown_event` (WT 2064 / TW 2348). While it waits, the whole monitor thread waits.

### (b) Achieved interval between consecutive polls of the same ENTRY order

TW-LOG 03–15 Sep: consecutive `get_order_history call_start` lines with the same `broker_order_id`, restricted to ENTRY legs per `orders.leg`.

| Set | n | min | p50 | p90 | p99 | max |
|---|---|---|---|---|---|---|
| All | 1,894 | 2.018 s | 2.046 s | 2.139 s | **4.667 s** | **8.993 s** |
| LFL836 (03–08 Sep) | 855 | 2.018 | 2.060 | 2.118 | 4.313 | 8.993 |
| VBB097 (09–15 Sep) | 1,039 | 2.024 | 2.043 | 2.194 | 4.917 | 7.663 |

- The ten largest intervals: 8.99, 7.66, 6.66, 6.66, 6.35, 6.00, 6.00, 5.99, 5.90, 5.89 s.
- By construction, each interval is 2 s plus the whole previous cycle: every tracked order's calls, including any wait for a quote token.

### (c) Peak concurrent pending entries since 01-Sep

- **Method:** a TW-DB sweep over ENTRY `placed_at` → `updated_at`, where `updated_at` is when the monitor detected the terminal state.
- **Peak: 2**, on 03-Sep (10:03:14), 04-Sep (10:09:17), 08-Sep (10:01:19) and 10-Sep (10:04:09). Every other day peaked at 1.
- Concurrent orders of **all** legs (approximate, same method): peak 8 (04-Sep 10:13:21, 10-Sep 10:07:11, 15-Sep 10:12:15).
- Peak `get_order_history` starts in one second: 8 (04-Sep 10:13:23, :25, :27).

### (d) Quote call volume at peak, and the applicable rate limit

**Logged `get_quote` completions (`call_end`), 10:00–15:00:**

| Day | Calls | Mean per s | Peak minute (calls) | Seconds with ≥ 3 completions (share of 18,000 s) |
|---|---|---|---|---|
| 03-Sep | 5,906 | 0.328 | 13:01 (59) | 1,273 (7.07 %) |
| 04-Sep | 4,170 | 0.232 | 14:57 (50) | 807 (4.48 %) |
| 07-Sep | 8,035 | 0.446 | **14:57 (88)** | 2,002 (11.12 %) |
| 08-Sep | 4,916 | 0.273 | 12:36 (58) | 1,094 (6.08 %; the process stopped at 13:52) |
| 09-Sep | 5,560 | 0.309 | 14:25 (71) | 1,647 (9.15 %) |
| 10-Sep | 7,084 | 0.394 | 12:38 (62) | 1,929 (10.72 %) |
| 11-Sep | 6,201 | 0.344 | 14:36 (82) | 1,633 (9.07 %) |
| 15-Sep | 3,830 | 0.213 | 10:00 (40) | 888 (4.93 %) |

**Across all 45,845 logged calls:**
- Peak completions in one second: **6** (in 4 seconds). Seconds with exactly 3 completions: 9,741.
- **78.6 %** of calls completed in a second that had ≥ 3 completions.
- Call duration including limiter wait: p1 12 ms · p10 14 · p25 21 · **p50 617 · p90 2,657 · p99 5,327 · max 13,621 ms**.
  - ≤ 50 ms: 31.1 %; ≥ 300 ms: 65.1 %; ≥ 1,000 ms: 33.3 %.

**Two counting cautions:**
- `call_start` is logged **before** `_rl.acquire` (TW 1737 vs 1757). Starts per second (peak 11) count arrivals, not broker calls.
- Several quote-bucket calls log no INFO line and are **not counted**:
  - `get_quote_raw` — FIX-128 and FIX-075 `_fetch_ltp` per placement; `SlippageRecorder` per fill; kill-switch flatten;
  - `get_server_time` (TW 1688-1724).

  The figures above are a **floor**.

**Applicable limits:**
- Client-side `quote` bucket: burst 3, refill 3 per second (`config/broker_limits.yaml` 13-15, identical in all trees).
- Client-side `order` bucket: burst 8, refill 8 per second (9-11).
- **Broker-side limit: NOT ESTABLISHED.** It is stated nowhere in code, config or repo docs.

**Quote-bucket consumers** (TW non-test call sites):

| Caller | Line(s) | When |
|---|---|---|
| `secondary_screener` | 170 | every signal |
| `signal_processor` | 1085 | M-S1 |
| `order_monitor` | 327 | FIX-141; MARKET expected price |
| `order_protocol_limit` | 256 | `_circuit_limits`, per fill |
| `order_placer` | 4051 / 4078 | `_fetch_ltp`, `_check_liquidity` |
| `slippage_recorder` | 159 | per fill |
| `order_reconciler` | 1658 / 2315 / 3267 / 3659 | reconciliation |
| `cnc_gtt` / `cnc_gtt_monitor` | 240 / 705 | GTT |
| `eod_squareoff` | 1138 / 1534 | EOD |
| `kill_switch` | 1355 | flatten |
| `smart_tgt_manager` | 855 | CO only |
| `structure_exit_manager` | 638 | disabled |
| `entry_gate` | 437 | dormant |
| `zerodha_adapter` | 1630 / 1720 | internal |

### (e) Headroom

As measured:
- **Averaged** over 10:00–15:00, the logged load is 0.21–0.45 calls per second against a 3-per-second client bucket, about 2.55–2.79 tokens per second unused.
- **In bursts there is none.** 78.6 % of logged calls completed in seconds where the bucket was at or above its refill rate, and the median call waited about 0.6 s for a token (65.1 % waited ≥ 300 ms).
- FIX-141 polls draw from the same bucket, inside the single monitor thread.
- Unlogged quote-bucket calls reduce the headroom further by an unmeasured amount.
- **Broker-side headroom: NOT ESTABLISHED.**

### (f) Any 429 or rate-limit event

**Searched:** `system_*.log` and `debug_*.log` (03–15 Sep) and LOCAL-LOG, for `429_retry`, `429_retries_exhausted`, `BrokerRateLimit429Error`, `BrokerRateLimitError`, `Too many requests`, `frozen for`, `penalize`, `RateLimitAbortedError`, `Rate limit timeout`, `order bucket exhausted`, `FIX-069: re-queuing`, `HTTP 429`, `"kite_status_code":429`.

| Event | Count / detail |
|---|---|
| Broker HTTP 429 | **0** in every file |
| Client limiter | 1 — `RateLimitAbortedError: Rate limiter acquire aborted by shutdown during wait for 1 token(s) in category 'quote'`, 08-Sep 13:52:17.341, screener WHEELS. This happened during the 13:52 shutdown; it is a shutdown abort, not a limit hit. |
| Network timeouts (not rate limits) | `NetworkException … timed out` on 10-Sep 15:06:02 (`get_margins`) and 11-Sep 15:43:41 |

(FF-F5 already measured `429_retry` 0 and `FIX-069: re-queuing` 0.)

---

## Q9 — ORDER LIFETIME AGAINST A BOUNDED WINDOW

**Status:** PARTIAL (item 10 and parts of 1, 5 NOT ESTABLISHED) · **WT↔VM:** `order_monitor.py` MATCH; callbacks identical text (WT `main.py` 685 / 724 / 878 vs TW 688 / 727 / 820); reconciler, state store and kill switch DIFFERS-FILE (cited logic identical) · **Paper↔live:** DIFFER (paper `cancel_order` always succeeds, FF-D5)

All counts in the "Measured" column are from TW-LOG 03–15 Sep. `order_monitor.py` is identical in both trees.

| # | Path | What the system does today (code) | Can the order still be working at the broker afterwards? | Measured |
|---|---|---|---|---|
| **1** | Broker status outside {OPEN, TRIGGER PENDING, SUBMITTED} (and not PARTIAL, COMPLETE, CANCELLED or REJECTED) | `_process_order` logs WARNING `order_monitor.unknown_status` (785-790). No fill-timeout and no FIX-141 run that cycle. The order stays tracked and is polled again next cycle. | **Yes**, for as long as the status stays unmapped. Which other Kite statuses occur is **NOT ESTABLISHED**. | 4 lines, all on non-ENTRY legs: `OPEN PENDING` ×1 (EOD leg, 07-Sep 15:17:05); `CANCEL PENDING` ×3 (TGT legs, 08-Sep 12:18:38; 15-Sep 10:21:05 and 11:53:44). 0 on ENTRY legs. |
| **2** | `BrokerTimeoutError` on the poll | `return` (655-662): the order is skipped this cycle. There is no counter and no cap. The fill-timeout check does not run that cycle. | **Yes**, while consecutive history timeouts continue; code sets no bound. | `order_monitor.timeout_skipped` 0 |
| **3** | Monitor stops after consecutive auth or API errors | Three consecutive `BrokerAuthError`s (640-654), or `max_api_failures` (3) general errors (663-689; counter shared by all orders, reset on any success) → `on_critical` → `_make_api_failure_hard_kill_cb` → `kill_switch.hard_kill` + CRITICAL Telegram (WT `main.py` 724-749) → `_stop_event.set()`. Polling ends for **every** tracked order: no fill timeout, no FIX-141, no force close. The HARD_KILL flatten (`_exit_all_trades_indestructible`, TW `kill_switch.py` 1670-~2000) cancels resting **SL/TGT** only (`_cancel_trade_resting_exits` 1598-1668, `leg IN ('SL','TGT')`) and market-exits OPEN/PARTIAL/PENDING_FILL trades (93) plus broker positions (sweep 1911+). **No step cancels a working ENTRY order**, and a working entry's trade row is `PENDING`, which is not in that status set. | **Yes.** A later fill becomes a broker position, which the flatten's broker-position sweep exits only if its retry loop is still running (bounded by `_HARD_KILL_MAX_RETRY_HOURS = 2.0`, `kill_switch.py` 85). | `circuit_breaker_api_failures` 0 · `auth_error` 0 · `critical_failure` 0 · `api_failure_counted` 4 (one each on 03, 08, 09, 10 Sep; never 3 in a row) |
| **4** | Failed cancel (orphan path) | Fill-timeout cancel returns `success=False` (1115-1126): CRITICAL `orphan_detected` → OSM FAILED → untrack → `on_orphan` → `soft_kill` + CRITICAL Telegram (WT `main.py` 878-901). The FAILED transition publishes `OrderStatusChanged(FAILED, qty_filled=0)` → `OrderPlacer._on_order_status_changed` zero-fill branch: reservation released, trade FAILED, "ORDER REJECTED" alert. `soft_kill` cancels nothing (TW 563-688). | **Yes.** Nothing polls or cancels it again. If it fills, only the reconciler's position checks see the position (not traced here). | `orphan_detected` 0 |
| **5** | Unconfirmed cancel taken from the response | `ZerodhaAdapter.cancel_order` returns `success=True` whenever `kite.cancel_order` raises nothing (TW 1021-~1082 / WT 982-~1045); order state is not read back. Callers then mark CANCELLED and untrack: fill timeout (1108-1114), FIX-141 (1193-1199), force close (832-841), partial (923-930 → `_handle_terminal`). | **Yes**, if the order filled before the cancel took effect or the cancel is still pending. `CANCEL PENDING` has been observed on TGT legs (item 1). Locally the order is CANCELLED, the trade FAILED and the reservation released. Whether any CANCELLED-marked ENTRY later filled at the broker is **NOT ESTABLISHED** (no broker order-book read; FF-H6). | `timeout_cancelled` 55 · `pending_rr_cancelled` 8 |
| **6** | An order never tracked | (i) `BrokerTimeoutError` from `engine.execute` → trade `UNKNOWN_IN_FLIGHT` + `_timeout_recovery_queue`, no broker id (`order_placer.py` 1433-1465). (ii) `_persist_entry_orders` raises → `_handle_placement_failure(broker_order_ids=placed)` cancels (unconfirmed, item 5) + hard_kill (1524-1561). (iii) `track()` raises → cleanup cancels (1676-1731). (iv) Process dies between broker ack and `track()`. The reconciler's `_recover_in_flight_entries` (TW 4169-4252) matches by tag: a broker ENTRY still resting → `_recovery_defer_resting`, "keep capital correct + defer", **no cancel** (4301-4305); terminal and filled → adopt; absent after N polls → FAILED + release. | **Yes** for (i) and (iv): no path cancels a resting untracked entry; it is deferred each cycle until terminal. (ii) and (iii) try to cancel (item 5). | `place_timeout_UNKNOWN_IN_FLIGHT` 0 · `ef2_track_failure_cleanup` 0 |
| **7** | Restart rehydration resetting `placed_at` | `rehydrate_from_store` (386-482) re-tracks orders with `orders.status` IN (PENDING, SUBMITTED, OPEN, PARTIAL, TRIGGER_PENDING) (state_store WT 1066-1103). `placed_at` is parsed from the row, else `now_ist()` (452-456), so the 60 s clock restarts **only if the timestamp cannot be parsed**. Also: `expected_price = float(row["price"] or 0.0)` (469) → 0.0 for ENTRY (`orders.price` NULL); `tgt_price` / `sl_price` are not restored (default 0.0) → **FIX-141 returns early for every rehydrated ENTRY** (1151-1152); the `_handle_complete` fallback price would be 0.0. On a graceful stop, `cancel_all_entry_orders` (530-590; logged as `shutdown_cancel_complete`) cancels tracked ENTRY legs first. | While the process is down nothing polls, so the order works at the broker until the first OPEN poll after restart, when elapsed (from the original `placed_at`) is already > 60 s → cancel. After restart there is no pending-R:R cancel. | 16 boots, each "rehydrated 0 orders". `shutdown_cancel_complete` 15, all "cancelled 0 / total_entry_orders 0". 116/116 ENTRY `placed_at` since 01-Sep parse (FF-D5). |
| **8** | Partial fill where the cancel fails | `_handle_partial` → `cancel_order` fails → CRITICAL `partial_immediate_cancel_failed` → `_fire_orphan` (`on_orphan` soft_kill + Telegram; untrack) (931-939). No terminal transition and no `OrderPartiallyTerminated`. `OrderPlacer._on_order_status_changed` returns unless status is CANCELLED, REJECTED, FAILED or EXPIRED (1938-1940), so nothing commits capital, records the fill or places SL/TGT for the filled quantity. The trade stays `PENDING` with an ENTRY row, which is outside `get_orphaned_pending_trades` (requires no ENTRY row; state_store WT 1105-1136) and outside the timeout queue. | **Yes.** The remainder can keep working and filling; the filled part has no exits from the entry path. | `partial_fill` 0 · `partial_immediate_cancel_failed` 0 (no PARTIAL status ever recorded; FF-F3/H4) |
| **9** | 15:15 force close fails to cancel | `_check_force_close` (794-867) fires once per date. A cancel failure logs CRITICAL `force_close_cancel_failed` (842-849); an exception logs `force_close_cancel_error` (850-858). The entry is **not** untracked, so the next poll's fill-timeout retries the cancel (elapsed is > 60 s by then) and a second failure takes item 4's path. Then `_on_force_close` → `soft_kill` (WT `main.py` 685-721), which cancels nothing. EOD squareoff at 15:17 (`_cancel_pending_entries`, `eod_squareoff.py` 864-~920) selects `WHERE t.status = 'PENDING_FILL' AND o.product IN ('MIS','CO')` (state_store WT 1040-1064 / TW 1015-1039). **A working entry's trade row is `PENDING`**: `create_trade` inserts `PENDING_FILL` (`order_manager.py` WT 240 / TW 236), `order_placer.py` 1065 overwrites it with `PENDING` before the broker call, and no code sets `PENDING_FILL` again. A grep of non-test code in both trees finds the literal written only by `create_trade`'s INSERT; every other occurrence is a query or a comment. `order_placer.py` writes trade status only at 1065, 1449, 2005 and 4448; `record_entry_fill` sets `OPEN`. So EOD5 cannot select it; CNC entries are also outside its product filter. | **Yes**, once force close and the timeout cancel have both failed. After untrack, nothing in code cancels it. | `force_close_triggered` on 7 days · `force_close_entry_cancelled` 0 (no ENTRY was tracked at 15:15 on any day) · `force_close_cancel_failed` / `_error` 0 · EOD Pass 1 "0 orders cancelled" each day |
| **10** | Is a DAY LIMIT left working cancelled by the exchange at session end? | Code never passes `validity` (`LimitTripleProtocol.execute` 211-219; the adapter's Kite call has no `validity` argument, TW 639-654). kiteconnect drops None parameters, so Kite's default applies. **NOT ESTABLISHED from code.** | **EVIDENCE only:** `orders.rejection_reason` on 3 ENTRY rows — SETL 260615170825087, HARIOMPIPE 260615170827437, AVL 260615170827485, all placed 15-Jun 11:34–35 — reads *"FIX-179 remediation: … system crashed pre-fill; unfilled day-order cancelled by broker at EOD; broker confirms 0 fill / 0 position / 0 holding / full cash …"*. That is an operator's record of one day's broker behaviour, not a code guarantee. | — |

---

## Q10 — PERSISTENCE GAPS

**Status:** ESTABLISHED · **WT↔VM:** `order_placer.py` / `order_monitor.py` MATCH; `order_manager.py` DIFFERS-FILE (insert and update text identical: TW `insert_orders_atomic` 339-~391, NULL binding at 387; `update_order_status` 726) · **Paper↔live:** IDENTICAL (the same writers run in both)

### (a) Columns that exist for each price in the chain

Counts are from TW-DB.

| Chain value | Columns that exist | Populated? |
|---|---|---|
| **Quote used to derive the entry (M-S1 LTP)** | None in `trades`, `orders`, `signals` or `order_execution_log`. The nearest is `screener_results.market_data_snapshot.ltp`, the screener's **separate, earlier** quote. TW P1 evidence has `reanchored`, but no LTP. | M-S1 LTP: **nowhere** (an INFO log line only, 2 decimals). Screener LTP: populated (4,900 of the latest 5,000 rows). |
| **Derived entry before tick snap** | `trades.entry_target_price` (pre-FIX-075) · `order_execution_log.intended_price` (post-FIX-075; fills only) · `trade_slippage_log.entry_signal_price` (a copy of `entry_target_price`, written at close) · TW P1 `entry_price_final` (JSONL) | 954/954 · 475/475 ENTRY rows (filled orders only) · 344/344 · testing VM from 11-Sep |
| **After tick snap** | **None** | — |
| **Submitted price** | `orders.price` | **0 of 773** ENTRY rows |
| **Actual fill** | `trades.entry_actual_price` · `order_execution_log.actual_price` · `trade_slippage_log.entry_fill_price` · `orders.avg_fill_price` · `orders.qty_filled` | 368/368 filled trades · 475/475 · 344/344 · **0/773 ENTRY (0/1,452 all)** · **0 rows > 0** |
| Related: fill time | `orders.filled_at` (the poll's detection time) · `order_execution_log.exchange_timestamp` | Populated on COMPLETE · **0/475** |
| Related: market at fill | `market_execution_context.ltp / bid / ask` (captured by `SlippageRecorder` via `get_quote_raw` at `OrderFilled`) | ENTRY 213 rows |

### (b) Why `orders.price` is NULL — the exact code path

1. `OrderPlacer._persist_entry_orders(trade_id, result, symbol, qty, side, intent)` (`order_placer.py` 4637-4706) **receives no price** (its call at 1525 passes none).
2. It builds the ENTRY row spec (4666-4675) with no `price` argument:

   `OrderInsertSpec(broker_order_id=result.entry_broker_order_id, leg="ENTRY", transaction_type=side, order_type="LIMIT", product=product, variety=co_variety, qty_requested=qty)`
3. The dataclass default applies: `price: float = 0.0` (`orders/order_manager.py` 81).
4. `OrderManager.insert_orders_atomic` binds `spec.price if spec.price > 0 else None` (WT 403 / TW 387), so **NULL** is written.
5. **Upstream, the value is dropped before it could arrive.** The adapter returns the snapped price on `PlacedOrder.price` (TW adapter 669-682). `LimitTripleProtocol.execute` does not copy it into `EntryResult` (`order_protocol_limit.py` 239-248), and `EntryResult` has no price field (`orders/entry_engine.py` 38+).

### (c) Why `orders.avg_fill_price` and `orders.qty_filled` are never written

1. **The only writer** is `OrderManager.update_order_status` (WT 742-768 / TW 726), called from `_on_order_status_changed(OrderStatusChanged)` (WT 148-171).
2. **The event is published by `OrderMonitor._safe_transition`** with `qty_filled = entry.filled_qty` and `avg_fill_price = entry.avg_fill_price if entry.avg_fill_price > 0.0 else None` (`order_monitor.py` 1321-1342).
3. **On COMPLETE**, `_handle_complete` computes `final_qty` and `final_price` as local variables (989-990), then calls `self._safe_transition(entry.internal_order_id, "COMPLETE", entry=entry)` (992) **without assigning them to `entry`**.
4. **Only `_handle_partial` sets** `entry.filled_qty` and `entry.avg_fill_price` (895-897), and no PARTIAL status has ever been recorded.
5. So the row is written with `qty_filled 0` and `avg_fill_price NULL`. The fill values travel only in `OrderFilled` (999-1012), which reaches `trades` and `order_execution_log`.

### (d) Does any log line, at any level, record the tick-snapped price?

| Log | Level / file | Records the snapped price? |
|---|---|---|
| `adapter.snap_to_tick` (TW 1454-1462 / WT ~1406-1414), with `price_in` / `price_out` | DEBUG; written only when the price changed; 172 lines in `debug_*.log`, 0 in `system_*.log` | **No value survives** — the debug formatter writes only `ts LEVEL logger — msg` |
| ERROR "Zerodha rejected order …" | ERROR, broker exceptions only | **Yes, on rejection only.** `_translate_broker_exception(exc, context, "place_order")` carries `context["price"]` = the snapped price (TW 624-627, 655-661). Example: MAFANG 07-Sep 13:04:24 `"price":219.45` for entry 219.45033. |
| `place_order call_start` (TW 548-553) | INFO | No price field |
| `limit_triple.entry_placed` (`order_protocol_limit.py` 230-237) | INFO | Logs the **pre-snap** `entry_price` |
| `order_monitor.track` | INFO | No price |
| FIX-128 `entry_slippage_observed` | INFO | Trigger and LTP only |
| `order_monitor.complete` | INFO | Fill and `slippage_pct` against the pre-snap expected price |

**Result:** for an order the broker accepted, the snapped price is recorded **at no log level, with its value**.

### (e) The smallest set of schema or write changes that would make the chain auditable — DESCRIPTION ONLY

Each value below already exists in memory at the named point, and nothing persists it there today. This is an inventory of gaps, with no design, choice or ranking.

**Values whose column exists but is not written (4):**

| Value | Column | Where the value is in scope |
|---|---|---|
| Tick-snapped submitted price (and the tick used) | `orders.price` | After `_snap_order_to_tick` (TW 567-569) and on `PlacedOrder.price` (669-682). It would have to travel through `EntryResult` into `_persist_entry_orders`; `OrderInsertSpec` already has a `price` field. |
| Broker fill quantity and average | `orders.qty_filled`, `orders.avg_fill_price` | `final_qty` / `final_price` in `_handle_complete` (989-990), before `_safe_transition` (992) |
| Exchange fill time | `order_execution_log.exchange_timestamp` | Not read today: `exchange_timestamp` has 0 references in either adapter or in `slippage_recorder.py` |
| Post-FIX-075 entry for orders that never fill | `order_execution_log.intended_price` exists but is written only on fill | `entry_price` after 1261 |

**Values with no column (3):**

| Value | Where it is in scope |
|---|---|
| The M-S1 quote (`live_ltp`), its instant (`q.ts`) and the branch taken (success / unavailable / fetch error) | WT 1132-1152 / TW 1085-1106 |
| Whether `final_price` came from Kite's `average_price` or from the `expected_price` fallback | `order_monitor.py` 990 |
| The rupee allowance and SL distance FIX-128 applied (`_slip_tol`, `_slip_sl_dist`) | `order_placer.py` 1117-1121 (logged at INFO; `trades` stores only the fraction) |

---

## 11. NOT ESTABLISHED — CONSOLIDATED

| Q | Item |
|---|---|
| Q1 | The quote outcome of the 18 cases dated 17-Aug → 01-Sep (no M-S1 log exists; the DB cannot discriminate) |
| Q1 | Which SHA production ran on each of those dates (every candidate's M-S1 is identical) |
| Q1 | Whether a trade printed between Chartink's scan and each M-S1 quote (no last-trade time is captured) |
| Q2 | Chartink's price as-of instant within its minute, so the staleness from the scan instant itself |
| Q5 | The broker's actual MIS margin per symbol (never consulted) |
| Q7 | The tick table the process held on any day (the pre-09:00 file is not recoverable) |
| Q7 | The exact tick below 0.01 for RIR, XTRANET, MAFANG, NIFTY1 and MONQ50 |
| Q7 | Whether any tick changed between a refresh and the next boot |
| Q7 | The origin of the file the 10-Sep 08:15 boot loaded |
| Q8 | The broker-side rate limit and headroom |
| Q8 | The volume of unlogged quote-bucket calls (`get_quote_raw`, `get_server_time`) |
| Q9 | Kite statuses beyond those observed |
| Q9 | Whether any CANCELLED-marked ENTRY later filled at the broker |
| Q9 | Kite's default validity for an order sent without `validity` |
| Q9 | Reconciler behaviour when a fill appears after the orphan path (not traced) |

---

## 12. REPRODUCTION (all read-only; the scripts themselves are session scratch)

**Q1 split.** `SELECT t.trade_id, t.symbol, t.strategy, t.direction, t.entry_target_price, s.trigger_price, t.created_at FROM trades t JOIN signals s ON s.signal_id=t.signal_id WHERE t.created_at >= '2026-08-15'`.
- A row is equal when `entry_target_price == trigger × (1∓off)`, with `off` 0.002 for `positional_*`, else 0.001.
- The six are the YAMLs with `pullback_wait_enabled: true`.

**Q1 logs.**
- `grep -F "FIX-067 momentum fresh quote" logs/system_2026-09-*.log` and the LOCAL-LOG file.
- Per case, symbol lines within ±90 s of `created_at`.
- Branch counts: `grep -c` for "fresh quote: ", "fresh quote unavailable", "fresh quote fetch error".

**Q1 same boot.** `system_events` rows with `event_type LIKE '%START%'`; boot = the latest STARTUP ≤ `created_at`.

**Q1 bars.** `analytics.db candles` with `interval_sec=60`, the minute of (`created_at` − 0.7 s) and the prior minute. Mutation: trigger × 1.01 and × 0.99.

**Q1 code identity.**
- `git show <sha>:signals/signal_processor.py`, the block from `if not strategy_obj.pullback_wait_enabled` to "Step 5: Position sizing", md5.
- `git merge-base --is-ancestor 3f4587f <sha>`.
- `git log --all -G pullback_wait_enabled -- config/strategies strategies`.

**Q2 outcomes.** `trades JOIN signals LEFT JOIN orders (leg='ENTRY')` for `created_at >= '2026-09-01'`. Cancel causes: broker order ids from `order_monitor.fill_timeout` / `pending_rr_cancel PENDING_RR` log lines.

**Q2 price staleness.** Every `order_placer.entry_slippage_observed` line, matched to the trade with the same symbol created 0–10 s earlier.

**Q4.** `SELECT * FROM fm_ledger WHERE entry_type='TOP_UP'`, joined to `trades` and `signals` via `signal_id`, to RESERVE via `reservation_id`, and to OEL.

**Q5.** `fm_ledger` COMMIT reason `qty=… price=… excess_returned=…`, joined to the RESERVE `@ price`.

**Q6.** Recompute `min(min(abs(trigger − sl_initial) × frac, 5), 10)`. Cross-check against `tolerance_rs` / `sl_distance_rs` in the log (±0.005). Control with frac 0.20.

**Q7.**
- Candle prices not divisible by 0.05 (Decimal, paise mod 5).
- `grep snap_to_tick.missing_tick_size`.
- `cron_heartbeat WHERE job_name LIKE '%instrument%'`.
- `grep "InstrumentCache loaded"`.
- Fill-vs-limit: `_round_nearest_to_tick(entry_or_intended, tick_from_today's_csv)` vs `entry_actual_price`.

**Q8.**
- Consecutive `get_order_history call_start` per broker id for ENTRY ids.
- `get_quote call_end` per second and per minute in 10:00–15:00.
- `duration_ms` percentiles.

**Q9.** `grep -c` per marker per day; legs of the `unknown_status` ids from `orders`; `orders.rejection_reason LIKE '%FIX-179%'`.

**Q10.** `COUNT(col)` per column as listed in (a).

---

## 13. INDEX

| Q | Status | WT↔VM | Paper↔live | Headline |
|---|---|---|---|---|
| **Q1** | PARTIAL | DIFFERS-FILE | DIFFER | 15 QUOTE_SUCCESS_SAME_PRICE · **0 fallback established** · **18 NOT ESTABLISHED (fallback not excluded)** · 0 flag misread · 0 after-round |
| Q2 | PARTIAL | DIFFERS-FILE | DIFFER | Price = trigger × (1∓0.001), snapped; LTP only via FIX-075 · placed − triggered p50 17.3 s · the flag's only runtime read is M-S1 · fill 39.6 % (six) vs 42.9 % (ten) |
| Q3 | ESTABLISHED | DIFFERS-FILE | IDENTICAL | 2 callers · no parameter-inexpressible need among the 16 YAMLs · 10 named obstacles |
| Q4 | ESTABLISHED | MATCH | DIFFER | 4 downstream readers (+ monitor chain) · threshold read only at 1207 · 8 top-ups, R:R 1.5–2.0 → 0.70–1.39 |
| Q5 | ESTABLISHED | DIFFERS-LOGIC (sizing) | IDENTICAL | All on unrounded `entry_price` · no side term · SHORT higher fill consumes more · 0 negative excess in 368 |
| Q6 | ESTABLISHED | MATCH | DIFFER | Fraction persisted, rupees not · dashboard uses abs(entry_target − sl) · p50 ₹0.83 / 0.27 % · 126/126 log match |
| Q7 | PARTIAL | MATCH | IDENTICAL | Entry nearest (± tick/2), SL limit always past trigger · 0.05 larger than the ≤ 0.01 real tick on all five · `reload()` has no caller |
| Q8 | PARTIAL | MATCH | DIFFER | Poll p50 2.05 s / p99 4.67 s / max 8.99 s · peak 2 pending entries · quote call p50 617 ms (limiter) · broker limit NOT ESTABLISHED · 0 broker 429 |
| Q9 | PARTIAL | MATCH / DIFFERS-FILE | DIFFER | 8 of 9 paths can leave a working order; EOD5 selects `PENDING_FILL` while a working entry is `PENDING` · DAY expiry NOT ESTABLISHED (one 15-Jun EVIDENCE record) |
| Q10 | ESTABLISHED | MATCH / DIFFERS-FILE | IDENTICAL | `orders.price` / `avg_fill_price` / `qty_filled` empty by traced cause · snapped price logged nowhere · 4 unwritten columns + 3 missing |

**Changed by this work:** this report file, and the session-end entries in `docs/SYSTEM_MAP.md`, `PATHS.md` and the UNPUSHED_PENDING_DEPLOY_LEDGER memory file. No code, config, commit, push, VM write or broker call.
