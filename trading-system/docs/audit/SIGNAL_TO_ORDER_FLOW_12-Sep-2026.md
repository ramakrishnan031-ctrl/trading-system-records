**On 11-Sep, 21,005 stock-alerts became 3,807 signals, 81 passed screening, 21 entry orders reached the broker and 6 filled. Most of the loss happens in two places: the receiver's 5-minute de-duplication (82 %) and the score (97.7 % of scored signals). After 10:15 the score can reach 60 only when the bid-ask spread is ≤ 0.005 %.**

# What the system actually does, from a Chartink signal to the entry order at the broker

- **Date.** Work 11-Sep-2026 22:44 → 12-Sep-2026 IST. The instruction files are the 22:45 file (D1.1, received at session start) and the 23:10 file (delivered mid-session). Their ISSUED headers are author-typed labels, not evidence of time.
- **Scope.** This is the 23:10 instruction file (D1.1, "what happens inside"). It replaces the structure of the 22:45 file: scanner conditions, scanner lateness and data availability are deferred, and none of that work is presented here. The scope runs from signal receipt to the entry order at the broker. The stop and target *values* are included, because they are computed before the entry.
- **Method.** Read-only throughout: no code, config, YAML, scanner, schema, threshold, restart or push.
  - **Source:** read from an extract of git **`970aabf`**. That is `origin/main`, measured with `git ls-remote` at 22:48:16 IST, and it holds the files deployed on production. Production is still *running* **`d3ee69d`** until Monday's 08:15 boot. The two differ in three decision-path files (`main.py`, `screening/secondary_screener.py`, `signals/signal_processor.py`), and a diff shows only evidence-capture additions plus one `reanchored` flag. The decision logic is identical, so this description holds for both. Line numbers are **@970aabf**; in `signal_processor.py` the same lines sit up to ~168 lower at `d3ee69d` (e.g. `_process_one` is `:867` here and `:761` there).
  - **Data:**
    - Production's own tables were streamed over SSH, 22:57–22:58 IST: `signals`, `screener_results`, `trades`, `orders`, `webhook_audit`, `candles`, V3 `would_be.jsonl`, `pb01_watchlist`. SQLite was opened as `file:…?mode=ro` with `PRAGMA query_only`, no project module was imported, and nothing was written on the VM. The `signals.webhook_payload` column was never selected, because it can carry the webhook token.
    - The testing VM's evidence file, DB rows and log for 11-Sep were read the same way.
    - Production's `system_2026-09-*.log` (02-Sep → 11-Sep, the logs on disk) was grepped read-only.
    - The analysis ran locally on those extracts.
  - **Agents.** Four research agents read source in parallel: webhook→queue, sizing/admission, order placement, and the strategy-field inventory. I re-read in source every claim of theirs that this report relies on, including:
    - the per-symbol order in the receiver;
    - the sizing formulas;
    - the risk-check order;
    - the 5 % reserve buffer;
    - `perf_weights`;
    - the throttle;
    - the placer's R:R gate, protocol choice, slippage guard, drift top-up and tick snap;
    - the NULL entry price;
    - the fill timeout, the pending-R:R cancel and the fill-time target;
    - the YAML key counts, recounted by my own script.

    I assembled the report myself in the main thread.
- **Labels.** Numbers come from a command I ran; each table says which. "(inference)" marks anything derived rather than read or measured. Where the source disagreed with an instruction file or an earlier record, the source wins (listed at the end).
- ⛔ **No recommendations, no design, no keep/modify/add/delete, not even provisional.** Where the code does something I cannot explain, I say so.

## 4.2 — THE FUNNEL, MEASURED (first, before any prose)

Production (account LFL836). Every number is a count from a read-only query of production's own tables (`webhook_audit`, `signals`, `screener_results`, `trades`, `orders`), extracted 22:57–22:58 IST 11-Sep. Stages follow the order the code executes them (§1). The three columns use the same query.

| # | Stage (what removes signals here) | **11-Sep (Fri)** | 10-Sep (Thu) | 20 trading days 17-Aug → 11-Sep |
|---|---|---:|---:|---:|
| 1 | HTTP POSTs arrived from Chartink | **3,662** | 3,636 | 76,080 |
| 2 | − refused before the body is read: 403 (entry window / kill switch) | 463 | 604 | 12,626 |
|   | − 401 auth · 404 unknown scanner · 400 malformed · 503 queue full | 0 · 0 · 0 · 0 | 0 · 0 · 0 · 0 | 0 · 0 · 0 · 1 |
|   | − routed to the EOD watchlist (pb01, 17:00) — never enters the order path | 1 | 1 | 20 |
| 3 | Intraday POSTs accepted inside 10:00–15:00 | **3,198** | 3,031 | 63,433 |
| 4 | Stock-alerts inside those POSTs (one POST carries many stocks) | **21,005** | 24,749 | 548,721 |
| 5 | − rejected per stock by the receiver (§1 S6) | 17,198 | 20,265 | 447,934 |
| 6 | **Signals created** (`signals` rows) | **3,807** | 4,484 | 100,787 |
| 7 | − pre-screen rejects (strategy switch off · strategy circuit breaker) | 0 | 0 | 6,536 |
| 8 | Screened | 3,807 | 4,484 | 94,251 |
| 9 | − no quote from the broker (`SKIPPED_QUOTE_UNAVAILABLE`) | 160 | 294 | 3,666 |
| 10 | − circuit-band proximity (`REJECTED_CIRCUIT_PROXIMITY`) | 113 | 384 | 7,612 |
| 11 | Scored (all ten steps run) | 3,534 | 3,806 | 82,973 |
| 12 | − score below 60 (`REJECTED_SCORE_n`) | **3,453** | 3,723 | 81,034 |
| 13 | **Passed screening** | **81** | 83 | 1,939 |
| 14 | − sizing returned qty 0 (concentration · capital · risk) | 32 · 0 · 0 | 27 · 8 · 0 | 481 in total |
| 15 | Sized | 49 | 48 | 1,458 |
| 16 | − admission (strategy cap · one-per-symbol-direction · duplicate symbol · open-position cap · consecutive losses) | 3 · 7 · 1 · 0 · 0 | 4 · 10 · 3 · 0 · 0 | 577 in total |
| 17 | Admitted and capital reserved | 38 | 31 | 881 |
| 18 | − entry throttle (20 s gap · 3 per 60 s · 300 s per symbol) | 16 | 15 | 549 |
| 19 | Dispatched to the order placer | 22 | 16 | 332 |
| 20 | − refused inside the placer / by the broker (`PLACEMENT_FAILED`) | 1 | 3 | 50 |
| 21 | **Entry order reached the broker** (`PROCESSED`) | **21** | 13 | 282 |
| 22 | − LIMIT entry cancelled unfilled | 15 | 5 | 157 |
| 23 | **Entry filled** | **6** | 8 | **125** |

**Reconciliation (the column is closed, not approximate).** Receiver: in-window `signals_accepted` = 3,807 = `signals` rows on 11-Sep, exactly (the only other `accepted` count that day is the 17:00 pb01 POST, 18 stocks, which go to the watchlist). Every `signals` status on each day maps to exactly one row of the table (unmapped statuses: **0** on all three columns). Trades created = dispatched (22 / 16 / 332); entry orders at the broker = `PROCESSED` (21 / 13 / 282). Scope note: `signals` rows that end `REJECTED*` are pruned after ~60 days (the oldest retained rejected row is 09-Jul), so no all-history column is shown.

### Where the population actually collapses (11-Sep)

1. **At the receiver, before a signal exists: 17,198 of 21,005 stock-alerts (81.9 %).** Chartink posts each scanner about once a minute (the intraday scanners made 180–300 POSTs each between 10:00 and 14:59; one a minute would be 300) and re-sends the same stocks while they keep matching; the receiver keeps one per `(scanner, symbol, 5-minute bucket)` — see §1 S6 for the exact rule.
2. **At the score: 3,453 of 3,534 scored signals (97.7 %).** §2 shows why: under the current weights, after 10:15 a signal can reach 60 **only** if the bid-ask spread is ≤ 0.005 %.
3. **Between "passed" and "at the broker": 81 → 21.** Concentration sizing (32) and the entry throttle (16) take most; the one-trade-per-symbol-direction rule (7), the strategy cap (3), the duplicate-symbol check (1) and the placer's slippage guard (1) the rest.
4. **At the fill: 21 → 6.** Every entry is a LIMIT placed 0.1 % (intraday) or 0.2 % (delivery) *better* than the reference price; if price does not come back to it within about a minute it is cancelled. On 11-Sep, 13 of the 15 cancelled entries were ONGC shorts re-sent every few minutes from 12:57 to 14:59 by three different scanners (§3.7).

End to end on 11-Sep: **6 filled entries from 3,807 signals (0.16 %)**, from 21,005 stock-alerts (0.029 %). Over 20 days: 125 from 100,787 signals (0.12 %).

---

## The journey in one paragraph (for a reader new to the codebase)

Every minute, each Chartink scanner POSTs the full list of stocks that currently match it, with Chartink's price for each. The web receiver refuses the whole POST outside 10:00–15:00. Inside that window it splits the POST into stocks and keeps one alert per (stock, scanner) per five minutes. Each kept alert is written as a `signals` row and queued. One of five worker threads then:

1. re-checks the kill switch, the window and the signal's age;
2. finds the strategy the scanner belongs to and checks that the strategy is switched on and not paused by its circuit breaker;
3. fetches one live quote and rejects stocks near their circuit limits;
4. scores ten features of that quote. Four of them never vary. A score below 60 ends the journey, which is what happens to almost everything.
5. For a signal that passes, derives an entry 0.1 % (delivery 0.2 %) better than Chartink's price, a stop a fixed percent away, and a target 1.5 × the stop distance. For ten of the sixteen strategies a second live quote re-bases all three first.
6. Sizes the position; in practice the 10 %-of-capital concentration cap × a 0.5 tier multiplier sets the quantity.
7. Inside a capital lock: checks the per-strategy cap, the one-trade-per-symbol-and-direction-per-day rule and ten risk checks, then reserves margin.
8. Sends a Telegram alert, then checks a 20 s / 300 s entry throttle.
9. Hands the order to the placer. The placer re-checks the price against Chartink's (a slippage guard) and sends one LIMIT order to Zerodha.

Stop and target orders are placed only after that LIMIT fills. If it has not filled within about a minute, it is cancelled. Shadow observers (the V3 chain, the portfolio allocator, the S&R detector) compute things alongside, but nothing reads their output.

---

## 1 — THE STAGES, IN SEQUENCE

Format per stage: **where** · *receives* · *does* · *produces / rejects* (exact status string) · *changes* (price, qty, side, decision) · *reads* (non-signal data) · **LIVE / SHADOW / DORMANT** · *time* · *on missing input or failure*. "Status" means the value written to `signals.status`.

### A. Receipt — `signals/webhook_receiver.py` (identical at both SHAs)

**S1 · HTTP server** · `main.py:3988-4000` (waitress `0.0.0.0:5000`, 8 threads, `connection_limit=100`); route `POST /webhook/<scanner_name>` `webhook_receiver.py:406-408` · **LIVE**
- *Receives:* Chartink's POST. The body carries `stocks` (comma-separated symbols), `trigger_prices` (comma-separated), `triggered_at` (`"2:34 pm"`) and `scan_name`, with `?token=` in the URL.
- *Does:* reads the body (1 MiB limit); per-IP token bucket (60 burst, 5/s) → **429**; service shutting down → **503** (`:485-504`).
- *Time:* Chartink's scan minute → received: median **14.48 s**, p95 24.54 s, max 59.89 s (233,600 signals). Whole receiver per POST (in-window 200s, 11-Sep): p50 0 ms, p90 4 ms, p99 20 ms, max 439 ms (`webhook_audit.duration_ms`).

**S2 · Authentication** · `:547-549` → `_authenticate` `:298-354` · **LIVE**
- *Does:* HMAC header if present; otherwise `?token=` compared with env `WEBHOOK_SECRET` in constant time (`require_hmac: false`, `system_config.yaml:336`).
- *Rejects:* **401** `Invalid token` / `Missing auth…` / `HMAC signature mismatch`. Measured: 0 in the last 20 days.

**S3 · Scanner known? and EOD routing** · `:552-564` · **LIVE**
- *Does:* the path segment must be one of the 16 keys of `config/scan_webhook_map.yaml`, else **404**. `scanner_type: eod` (only `pb01_breakout_retest`) goes to `_handle_eod` (`:751-804`). That route feeds the PB-01 watchlist's own queue, **never `signal_queue`**, and skips every later gate.
- *Changes:* the receiver never reads the map's `strategy` field; `signals.strategy` is written with the scanner name (`:975`). Key = strategy in all 16 entries.

**S4 · Kill switch → queue backpressure → entry window — all before the body is parsed** · `:567-583`; `core/market_windows.py:143-150` · **LIVE**
- *Does:*
  - kill switch SOFT/HARD (in-memory state) → **403** `Kill switch active; signals rejected`;
  - `signal_queue.qsize() ≥ 240` (300 × 0.80, `system_config.yaml:125-126`) → **503**;
  - not a trading day, or the clock outside **[10:00, 15:00)** IST (`:28`, `:47`) → **403** `Outside entry window`.
- *Produces:* on a 403 only a `webhook_audit` row (scanner, time, payload size, code). **The stocks in a refused POST are never recorded.**
- *Measured:*
  - 11-Sep: 463 × 403, of which 103 were before 10:00 and 360 at 15:00 or later.
  - 20 days: 12,626 × 403 and one 503.
  - Every in-window POST on 11-Sep got a 200.

**S5 · Parse and request-level validation** · `:586-674` · **LIVE**
- *Does:*
  - JSON object check; casts top-level numeric fields (`price`, `entry_price`…) that a Chartink payload does not carry (inference);
  - requires `stocks`, `trigger_prices` and `triggered_at`;
  - `scan_name` must equal the path, after lower-casing and stripping an `lfl836-` prefix;
  - `triggered_at` is parsed as `%Y-%m-%d %H:%M:%S`, `%I:%M %p` or `%H:%M`, and a time-only value gets today's date with seconds :00;
  - stocks and prices are split on commas and paired by position.
- *Rejects:* **400** for any of these; the whole POST is dropped. Measured: 0 in 20 days.
- *Changes:* defines the (symbol, price) pairs.

**S6 · Per-stock loop** · `:696-745` and `_process_signal` `:892-1072` · **LIVE**. Checks run in this order, and each returns a per-stock status:
1. **Symbol alias** (`config/symbol_aliases.yaml`: TVSSCS→TVSSRICHAK, SIGMAADV→SIGMAADV-BE), then the excluded list (E2E, GVPIL, BIRLACABLE, SHANKARA, MCLEODRUSS) → `REJECTED_EXCLUDED_SYMBOL`.
2. **Empty symbol** → `INVALID_SYMBOL` (`:906`). There is no format check and no instrument lookup.
3. **Price** not a number or ≤ 0 → `INVALID_PRICE` (`:909-914`).
4. **Age** = now − `triggered_at` > 600 s → `EXPIRED` (`:919-926`).
5. **In-flight claim.** The symbol is already being processed for *any* scanner → `IN_PROCESS` (`:934-935`). The claim is released when the worker finishes, or evicted after ~60 s, because the heartbeat is never wired.
6. **(symbol, scanner) seen in the last 300 s** → `DUPLICATE` (in-memory TTL cache, `:940-946`; `dedup_window_seconds: 300`, `system_config.yaml:337`).
7. **Fingerprint** `sha256(scanner|symbol|floor(epoch/300))` (`:952-954`). `INSERT` a `signals` row with status **`QUEUED`**; a unique-index hit → `DUPLICATE`.
8. **`put_nowait`** of `(signal_id, scanner, symbol, price, triggered_at)` onto `queue.Queue(maxsize=300)`. A full queue → row `QUEUE_FULL`, else `ACCEPTED`.

- *Response and audit:* a response body with per-stock statuses, and one `webhook_audit` row (`:506-534`). The row holds *counts* only, and its `ts` is written at the end of the request.
- **The six rejection statuses above — and `STORE_ERROR` on a failed insert — are sent back to Chartink and stored nowhere: no row, no log line.** On 11-Sep they were **17,198** of 21,005 stock-alerts. The split between them cannot be measured from stored data.
- *Structural evidence:* over the last 20 days, **90.8 %** of consecutive accepted signals for the same scanner+symbol+day are 5–6 minutes apart (only 0.04 % are closer), and on 11-Sep the intraday scanners POSTed 180–300 times each between 10:00 and 14:59 (one a minute is 300). A stock that keeps matching is re-posted every minute and kept once per five minutes. That is consistent with `DUPLICATE` being the bulk (inference).

**S7 · Queue → worker** · `signal_processor.py:377-399` (one `sp-dispatcher` thread, `get(timeout=0.1)`), then a 5-worker pool (`worker_count: 5`, `system_config.yaml:345`), then `_process_one_safe` `:405-480`, then `_process_one` `:867` · **LIVE**
- *Does:* no check at dequeue. `_process_one_safe`'s order-bucket pre-check (`:415-461`) **never runs**: `rate_limiter` is passed only to `ZerodhaAdapter` (`main.py:2383`) and `SmartTgtManager` (`:2973`), not to the processor (`:3575-3622`). The first statement of `_process_one` writes **`PROCESSING`** (`:897`).
- *On failure:* any exception escaping the pipeline → **`PLACEMENT_FAILED`** `unhandled: …` (`:466-477`).

### B. Pre-screen — `signals/signal_processor.py::_process_one`

**S8 · Kill switch · window · age** · `:906-921` · **LIVE**, never observed to fire
- *Rejects:*
  - `REJECTED_KILL_SWITCH` when `is_active("entry")`;
  - `REJECTED_OUTSIDE_ENTRY_WINDOW` when outside [10:00, 15:00);
  - `REJECTED_EXPIRED` when `now − triggered_at > 600 s` (`signal_queue.expiry_sec`, `:127`).
- *Measured:* 0 rows of each in the retained `signals` table. The receiver's identical gates fire first.

**S9 · Shadow-inning guard** · `:928` → `:1976-2008` · **LIVE code, inert since 25-Jul**
- *Rejects:* `REJECTED_SHADOW_INNING_ACTIVE` if the shadow tracker holds a simulated inning on the symbol, or `SHADOW_TRACKER_ERROR` (fail-closed). `shadow_tracker.enabled: false` (`system_config.yaml:504`).
- *Measured:* 4,168 rows, all between 09-Jul and 24-Jul; none since.

**S10 · Scanner → strategy** · `:933-953` · **LIVE**
- *Does:* looks up `scan_webhook_map[scanner].strategy` and the loaded `StrategyConfig`.
- *Rejects:* `REJECTED_UNKNOWN_STRATEGY` (0 ever).

**S11 · Strategy control** · `:959-972` → `strategies/control.py:67-117` · **LIVE**
- *Does:* `enabled: false` → *"WON'T TRADE — switch disabled"*; delivery intent with `force_intraday_only` → blocked; `trade_type` mismatch → blocked. Today `force_intraday_only: false` and `trade_type: BOTH` (`system_config.yaml:142`, `:149`), so only the `enabled` switch acts.
- *Rejects:* `REJECTED_STRATEGY_CONTROL` / `REJECTED_TRADE_TYPE`.
- *Measured:* 23,481 rows; 2,051 in the last 20 days, the last on 04-Sep, when the three delivery strategies were switched off.

**S12 · Per-strategy window** · `:977-982` → `market_windows.py:152-175` · **LIVE, inert**
- *Does:* requires both the global window and the YAML's `entry_start_time`/`entry_end_time` (09:25–15:00; pb01 11:00). The 10:00 floor always wins.
- *Rejects:* `REJECTED_OUTSIDE_ENTRY_WINDOW`.

**S13 · Strategy circuit breaker** · `:985-990` → `capital/strategy_governor.py:49-127` · **LIVE**
- *Does:* before 12:00 (`cutoff_time`), pauses a strategy for the rest of the day if its gross P&L on trades closed today is below **2 ×** its average losing-day P&L over the last 10 calendar days (`system_config.yaml:734-736`). Once paused it stays paused after 12:00 (`:60-61`).
- *Rejects:* `REJECTED_STRATEGY_CIRCUIT_BREAKER` *"strategy paused today by circuit breaker"*.
- *Reads:* `trades`.
- *On failure:* a DB error fails open.
- *Measured:* 9,269 rows on 10 days; 4,485 in the last 20 days, the last on 09-Sep.

### C. Screening — `screening/secondary_screener.py::screen` (`:123-374`)

**S14 · MIS blocklist pre-drop** · `:148-165` · **SHADOW** (`mis_filter.enabled: true`, `shadow: true`, `system_config.yaml:179-180`)
- *Does:* logs a would-drop for symbols the broker recently refused for MIS; the signal falls through.
- `REJECTED_NOT_MIS_TRADABLE`: 0 ever.

**S15 · Quote #1** · `:168-196` → `broker/zerodha_adapter.py:1730-1806` · **LIVE**
- *Does:* `kite.quote("NSE:<symbol>")` through the `quote` rate-limit bucket (burst 3, 3/s, `config/broker_limits.yaml`), then builds the market-data dict (§2).
- *Rejects:* no quote for the symbol, or the fetch raised → **`SKIPPED_QUOTE_UNAVAILABLE`**.
- *Measured:* 160 on 11-Sep; 8,757 all-time across 97 symbols. **24 symbols never returned a quote at all** (5,431 rows), e.g. AMIRCHAND 1,218, GSPL 927, GAUDIUMIVF 629, BHAGERIA 502, SIGMAADV-BE 313. The per-symbol cause was not traced.
- *Time:* adapter-timed including the rate-limiter wait (production 11-Sep, 4,728 calls): p50 **310 ms**, p90 **2,321 ms**, p99 4,669 ms, max 8,662 ms.

**S16 · Circuit-band proximity** · `:213-232` → `screening/hard_gate.py:53-112`; margin `orders/price_math.py:256` (0.02) · **LIVE**
- *Does:* on **Chartink's trigger price**, not the fresh quote. A LONG is rejected if trigger ≥ upper × 0.98 or ≤ lower × 1.02; a SHORT if trigger ≤ lower × 1.02 or ≥ upper × 0.98.
- *Rejects:* `REJECTED_CIRCUIT_PROXIMITY`, with a reason naming the band.
- *On missing data:* a missing band fails open.
- *Measured:* 113 on 11-Sep; 7,612 in 20 days.
- A symmetric ±2 % band makes both limits sit within 0.04 % of the previous close, so a 2 %-band stock is always rejected (inference). Band half-widths observed in snapshots: 20 % (152,699 rows), 10 % (28,331), 5 % (5,133).

**S17 · The ten steps** · `screening/step_executor.py:118-219` · **LIVE** — full treatment in §2.
- *Rejects:* a step that *raised* → `REJECTED_STEP_ERROR` (`secondary_screener.py:266-286`; 0 ever). A timeout scores 0.5.

**S18 · Score · shadow compare · pass mark · age defence · persist** · `:289-374`, `:598-637`
- *Score and tier:* `quality_scorer.py:71-150`.
- *V3 hard-gate shadow compare* (`:310-314`, `v3_hardgate_mode: "shadow"`, `scoring_weights.yaml:39`) · **SHADOW**: logs *"OLD score=… | NEW score=… gate=…"*; nothing reads NEW.
- *Pass mark* (`:317-337`):
  - `effective_min = strategy.min_score if > 0 else 60`; all YAMLs carry 0.
  - Below it → **`REJECTED_SCORE_<n>`**: 3,453 on 11-Sep; 81,034 in 20 days.
- *Age defence* (`:340-354`): `signal_age == 0.0` → `REJECTED_SIGNAL_AGE`. It **cannot fire**: a signal with age 0 scores at most 55 and has already been rejected on score. 0 ever.
- *PASSED* (`:357-374`): 81 on 11-Sep.
- *Persist* (`:598-637`): the `signals` status, plus one `screener_results` row (score, tier, the ten step values, per-step latencies, the whole market-data snapshot). @970aabf a P3 evidence record is added after the DB write.
- *Time:*
  - receipt → screener persist: median **1.36 s**, p90 7.93 s, p99 17.49 s, max 35.98 s (196,586 rows). This includes queue wait and the quote.
  - The steps themselves are sub-millisecond: 0.07–0.55 ms each in the §6 example.

### D. Pricing — back in `_process_one`

**S19 · Entry and stop from the trigger** · `:1028-1030` → `_derive_prices` `:1748-1895` · **LIVE** — §3.2 / §3.4.
- *Rejects:* `REJECTED_INVALID_DERIVED_PRICE`, `REJECTED_ZERO_SL`, `REJECTED_REJECTED_NO_ATR_DATA` (sic). None can fire under the current YAMLs.

**S20 · Retest diverter** · `:1042-1056` · **DORMANT**
- `self._retest_diverter` is None, because `sr_detector.wait_for_retest_enabled: false` (`system_config.yaml:529`).

**S21 · M-S1 re-anchor (quote #2)** · `:1081-1106` · **LIVE** — §3.3. *Changes* entry and stop, and through them target, qty and reserve.

### E. Sizing and the shadow observers

**S22 · Position sizing** · `:1111-1128` → `capital/position_sizer.py:245-809` · **LIVE**
- *Receives:* entry, SL, intent, tier, the YAML's `lot_size` (1 = "use the instrument cache"), and `perf_weight`. `perf_weight` is **always 1.0**, because `perf_weights` is never passed to the processor (the `main.py` constructor call `:3575-3622` has no such argument).
- *Does:* reads `fund_manager.get_snapshot()` **outside** the capital lock: `total` = today's broker-seeded capital, and the intent's bucket `avail`.
  - `qty_by_risk = ⌊total × 0.01 / |entry − sl|⌋` (`:456-457`)
  - `qty_by_capital = ⌊avail ÷ (entry / leverage)⌋`, with leverage 5.0 intraday / 1.0 delivery (`:492-496`)
  - `qty_by_concentration = ⌊total × 0.10 / entry⌋` (`:498-500`)
  - `raw = min(…)`
  - × tier multiplier (HIGH 1.0 / MEDIUM 0.70 / **LOW 0.50**, `system_config.yaml:238-240`) × perf → `max(1, min(⌊raw × mult⌋, 2 × raw))`
  - then lot rounding and guards. The percentages come from `system_config.yaml:225-259`; delivery reads its own keys, which carry the same values.
- *Rejects:* `REJECTED_SIZING_<constraint>` with `qty=0: … exhausted …`:
  - `CONCENTRATION` 32 on 11-Sep and 418 in 20 days;
  - `CAPITAL` 63 in 20 days, all delivery;
  - `RISK` 3 ever;
  - `INVALID_SL_DISTANCE`, `QTY_EXPLOSION_GUARD`, `POSITION_VALUE_CAP`, `BELOW_MIN`, `ZERO_MULTIPLIER`, `REJECTED_LOT_SKEW` are coded; the last four cannot bind under current config (inference, from the arithmetic).
- *Measured on production's last 332 trades:* binding constraint **concentration 332/332**; tier weight 0.5 on 330; perf 1.0 on all; qty 1 (155) or 2 (152); planned value median ₹467.6.
- *Changes:* **qty**.
- *On failure:* a sizer `ValueError` → `PLACEMENT_FAILED`.

**S23 · V3 decision chain** · `:1136-1143` → `v3_chain/runner.py:99-118` · **SHADOW** (`v3_chain_mode: "shadow"`, `system_config.yaml:574`)
- *Does:* `put_nowait` onto a 512-slot queue. A background worker fetches day/60m/30m bars, builds S&R zones, ATR30 and a 1-hour EMA20, and runs its RR/HTF/EXTREME gates.
- *Produces:* one line in `data_store/v3/would_be.jsonl` plus a log line. The runner holds no reference to the processor, fund manager or placer.
- *Cannot affect the order* (runner docstring `:4-5`: *"LOG-ONLY — the verdict never rejects/delays/alters a live signal or order"*).

**S24 · Portfolio allocator** · `:1147-1172` · **SHADOW** (`allocator_mode: "shadow"`, `:565`)
- *Does:* appends a candidate to a regret buffer, then falls through. Never reserves or places.

### F. Admission — `_admit_and_place` `:1277-1561`

**S25 · In-flight count, then the capital lock** · `:1302-1307` · **LIVE**
- *Does:* `_in_flight_count += 1` (feeds the risk engine's open-position count), then `with fund_manager.portfolio_lock:`. S25a, S25b, S26 and S27 run under that lock; the target (S28) is derived after it is released.

**S25a · Per-strategy position cap (H-7)** · `:1311` → `:744-779` · **LIVE**
- *Does:* `max(open/partial trades of this strategy + its live reservations, open/partial/pending rows) + 1 > max_concurrent_positions`. The cap is 3 for gap_*, 2 for the rest.
- *Rejects:* `REJECTED_STRATEGY_POSITION_LIMIT` (3 on 11-Sep, 111 in 20 days).

**S25b · One completed trade per symbol + direction + book per day** · `:1312-1313` → `:802-864` · **LIVE** (`risk.one_trade_per_symbol_direction_per_day: true`, `:302`)
- *Does:* counts today's executed trades for the same symbol and direction in the same book (intraday vs delivery, from the ENTRY order's product).
- *Rejects:* `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` (7 on 11-Sep, 244 in 20 days).

**S26 · Risk engine** · `:1315-1325` → `capital/risk_engine.py`. Ten checks, short-circuit, in this order:
1. `KILL_SWITCH` (`:517`)
2. `SIZING_VALID` (`:522`, cannot fire)
3. `CAPITAL` (`:530`; bucket avail < margin)
4. `OPEN_POSITIONS` (`:544`): intraday counts DB rows + live reservations + in-flight against **5**; delivery counts CNC DB rows only against **3**
5. `DAILY_TRADES` (`:643`): 10 intraday / 5 delivery
6. `CONSECUTIVE_LOSSES` (`:676`, 4 today)
7. `DAILY_LOSS` (`:692`, realized ≥ 3 % of total; the unrealized term is shadow)
8. `SECTOR_EXPOSURE` (`:735`): **observe only**, `sector_cap_mode: observe` (`:322`), logs and never rejects
9. `CONTRARY_POSITION` (`:768`)
10. `DUPLICATE_SYMBOL` (`:789`, any active position in the symbol, any product)

- *Rejects:* `REJECTED_<check>`. Measured in 20 days: OPEN_POSITIONS 136, DUPLICATE_SYMBOL 78, CONSECUTIVE_LOSSES 8. `REJECTED_DAILY_TRADES` fired 5,146 times on 09–10 Jul and never since.

**S27 · Reservation** · `:1327-1344` → `capital/fund_manager.py:521-635` · **LIVE**
- *Does:* reserves `qty × entry / leverage × 1.05` (a 5 % buffer, `:562-563`) from the intent's bucket (70 % intraday / 30 % positional of total; no borrowing).
- *Rejects:* `REJECTED_RESERVE_FAILED` *"Insufficient {bucket} capital: need X, have Y"*. The sizer and the risk engine judged the margin *without* the buffer.
- *Produces:* status **`RESERVED`** and a reservation id.

**S28 · Target** · `:1368` → `_derive_target` `:1901-1953` · **LIVE** — §3.5.
- *Rejects:* `TGT_DISTANCE_TOO_SMALL` / `UNKNOWN_TGT_METHOD`; neither can fire.

**S29 · Telegram "INTRADAY SIGNAL" alert** · `:1371-1380` → `:486-555` · **LIVE side effect**
- *Does:* sends synchronously (bounded by `send_deadline_seconds: 8`). The alert goes out before the late checks and the throttle, so it is sent for entries those later refuse. The title says INTRADAY for delivery entries too.
- *Time:* in the §6 example, 0.68 s elapsed between the risk approval and the alert.

**S30 · Late kill switch · shutdown** · `:1389-1405` · **LIVE**
- *Rejects:* `REJECTED_KILL_SWITCH_LATE` / `REJECTED_SHUTDOWN`, releasing the reservation first.

**S31 · Entry throttle** · `:1410-1418` → `signals/entry_throttle.py:65-115` · **LIVE**
- *Does:* one atomic check-and-record: global gap ≥ **20 s** since the last placed entry, then ≤ **3 per 60 s**, then per-symbol ≥ **300 s** (`system_config.yaml:350-353`). The admission is recorded before `place()` and never rolled back.
- *Rejects:* `REJECTED_ENTRY_THROTTLED` *"Entry throttled: min_gap 10.7s < 20s"* / *"per_symbol ONGC 175s < 300s"*: 16 on 11-Sep, 549 in 20 days.

**S32 · Dispatch** · `:1420-1460` · **LIVE**
- *Does:* an effect counter; @970aabf the P1 evidence record; then `self._placer.place(symbol, side, qty, entry_price, sl_price, intent, signal_id, reservation_id, strategy, tgt_price, signal_trigger_price, sizing_breakdown, tgt_risk_reward)`.
- *Outcomes:* `place()` returns nothing; no exception means placed → status **`PROCESSED`** (`:1543`). `BrokerTimeoutError` → `TIMEOUT`, with the reservation kept for recovery. A client rate-limit error → re-queued up to 3 times. Any other error → **`PLACEMENT_FAILED`**, with the reason text.

### G. The order placer — `orders/order_placer.py::place` (`:871-1763`) and the adapter

**S33 · R:R gate, protocol, trade row, last-mile checks** · **LIVE**
- *R:R gate* (FIX-136, `:937-958`): refuses if `(tgt − entry)/(entry − sl) < 1.0` (`entry_gate.min_effective_rr`, `system_config.yaml:659`). The values are 1.5 by construction, so it cannot fire: `rr_gate_failed` 0 in 8 days of logs.
- *Protocol:* **always `LIMIT_TRIPLE`** (`:960-961`); nothing per strategy is read.
- *Trade row:* `INSERT trades … status PENDING_FILL`, then `PENDING` (`:993-1071`).
- *Last-mile checks:* the kill switch again (`:1049-1058`), then the **15:15** cutoff (`eod_entry_cutoff`, `:48`) → trade `REJECTED`, signal `PLACEMENT_FAILED`.

**S34 · Slippage guard (quote #3)** · `:1099-1192` · **LIVE**
- *Does:* compares a fresh LTP (`get_quote_raw`, `quote` bucket) with **Chartink's trigger price**.
- *Rejects:* if `|LTP − trigger| > min(0.22 × |trigger − SL|, ₹5.00, ₹10.00)` or > 1.0 % of the trigger (`system_config.yaml:655`, `:671-674`) → trade `REJECTED`, signal **`PLACEMENT_FAILED` `slippage_exceeded: trigger=… ltp=… | slippage ₹… > tolerance ₹…`**.
- *On missing data:* no LTP means the guard is skipped (fail-open).
- *Measured:* 134 `entry_slippage_observed` lines in 8 days, 15 of them aborted. `PLACEMENT_FAILED` over 20 days: 29 slippage + 21 broker refusals.

**S35 · Price-drift top-up (quote #4)** · `:1194-1289` · **LIVE, rare**
- *Does:* if a fresh LTP is > 0.5 % *above* the entry and a margin top-up succeeds, **the entry becomes that LTP**; stop and target stay. If the top-up fails → `REJECTED_PRICE_DRIFT`.
- *Measured:* 1 occurrence in 8 days of logs (07-Sep QUICKHEAL, 157.93 → 158.73).

**S36 · Liquidity check** · `:1291-1305` · **DORMANT**
- `liquidity_check_enabled` is not passed to the placer, so the constructor default False applies; the YAML's `true` has no effect.
- *Then:* the kill switch once more immediately before submit (`:1335-1343`).

**S37 · The broker call** · `order_protocol_limit.py:171-248` → `zerodha_adapter.place_order` `:494-689` · **LIVE**
- *Does:*
  - validates;
  - snaps the price to the **nearest** tick (`:1436-1452`; tick from `instruments.csv`, 0.05 fallback);
  - maps the product (MIS/CNC);
  - applies the CNC lock (`delivery_enabled: true`);
  - takes the `order` rate-limit bucket (8/s, waits up to 30 s);
  - calls `kite.place_order(variety="regular", exchange="NSE", …, order_type="LIMIT", price=<snapped>, tag=trade_id[:16])` with a 10 s HTTP timeout. There are no retries except on HTTP 429 (up to 4 attempts).
- *Produces:* success = Kite returned an order id; acceptance by the exchange is **not** verified here. It is learned from the order monitor's 2-second poll. Then an `orders` ENTRY row with **`price` NULL**, fill-map and monitor registration, and the Telegram "ORDER PLACED" alert (which prints the entry as "Fill" and "SL ✓ | TGT ✓" before either exists).
- *Time:* `place_order` p50 **44 ms**, p90 55, max 68 ms (production 11-Sep, 29 calls). Receipt → entry order at the broker (`trades.signal_to_order_ms`, 374 filled trades): median **2.04 s**, p90 6.72 s, p99 14.98 s, max 17.9 s.
- *After placement:* the processor writes `PROCESSED`, then calls the S&R detector (`:1550-1561`) — **SHADOW**, post-placement, gates nothing.

**S38 · From "at the broker" to "filled or cancelled"** (for the values) · `broker/order_monitor.py` · **LIVE**
- The monitor polls every **2 s** (`system_config.yaml:193`).
- *Fill:* the placer recomputes the target from the fill price at 1.5 R (`order_placer.py:2870-2879`). For **MIS** it clamps SL/TGT 2 % inside the circuit band, places the SL as a stop-limit (trigger = SL, limit = trigger ∓ 0.5 %), then the TGT as a LIMIT. For **CNC** it places one OCO GTT (SL limit × 0.97, TGT limit × 0.995; no clamp).
- *No fill within* **60 s** (`fill_timeout_sec`, `:194`) → cancelled, reservation released, trade **FAILED**: 48 such cancels in 8 days of logs.
- *Remaining reward* `(TGT − LTP)/(entry − SL)` < **1.0** while resting → cancelled (FIX-141, `order_monitor.py:1128-1207`): 5 in 8 days.
- *Partial fill:* remainder cancelled at once.
- *15:15:* all resting entries force-cancelled.
- *Time:* order → fill median **9.7 s**, p90 43.8 s, max 60.1 s (374 fills). Fill rate **374 of 769 (48.6 %)**.

---

## 2 — THE TEN SCREENING STEPS, ONE BY ONE

**Where they run.** `screening/step_executor.py:118-219 @970aabf` (`run_all`) runs all ten, in the order below, every time — there is no short-circuit (`:141-154`). Each step is submitted to a single-worker thread pool with a **5.0 s** timeout (`:53`, `:166-167`): a timeout scores **0.5** and is labelled `TIMEOUT` (`:168-181`); an exception scores **0.0**, is labelled `ERROR` and goes into `error_steps` (`:182-195`), which the screener turns into `REJECTED_STEP_ERROR` (`secondary_screener.py:266-286`). A step returning exactly 0.0 is labelled `REJECTED` — **a label only; no step rejects anything by itself.** The only decision is the total.

**Where their inputs come from.** One broker quote per signal, fetched by the screener (`secondary_screener.py:168-196` → `broker_adapter.get_quote`, `broker/zerodha_adapter.py:1730-1806`), rate-limited in the `quote` bucket (burst 3, 3/s — `config/broker_limits.yaml`). `_build_market_data` (`secondary_screener.py:380-418`) maps it to: `ltp` ← `last_price`; `bid`/`ask` ← first level of market depth, **0.0 (not None) when that side of the book is empty** (`zerodha_adapter.py:1776-1782`); `volume` ← day volume so far; `vwap` ← Kite `average_price`; `open`/`day_high`/`day_low` ← Kite `ohlc`; `upper_circuit`/`lower_circuit` ← Kite circuit limits; `circuit_state` ← derived (`ltp >= upper` / `ltp <= lower`). And five slots hard-coded **None**: `atr`, `rsi`, `sector`, `prev_close`, `avg_volume_20d` (`:412-417`). The adapter reads `ohlc.open/high/low` and never `ohlc.close` (`:1784-1795`). The per-strategy thresholds are `min_volume_surge`, `min_adr_pct`, `max_spread_pct` from the strategy YAML (`:235-239`). Validated: the snapshot's `open` equals the first 1-minute candle's open on **4,313 of 4,313** symbol-days that have candles.

**How they become one number.** `screening/quality_scorer.py:86-108`: `total = round(((Σ raw × weight) / Σ weight_present) × 100)`, capped at 100. With all ten present the denominator is 100. Python's `round` is round-half-to-even, and dividing before multiplying makes `57.5` compute as `57.49999999999999` → **57**. Validated: this exact expression, in the model's field order, reproduces the stored score on **175,019 of 175,019** rows that carry all ten steps (the naive `round(Σ)` disagrees on 80,989 — so the check could fail). Weights: `config/scoring_weights.yaml:11-20`. Pass mark: the strategy's `min_score` if > 0, else the global **60** (`secondary_screener.py:317-321`; all 16 YAMLs carry `min_score: 0`). Tier: HIGH ≥ 80, MEDIUM ≥ 65, else LOW (`quality_scorer.py:122-132`; `scoring_weights.yaml:28-29`).

**Observed distributions** are over the 175,019 screener rows with all ten steps (15-Jun → 11-Sep); where the current regime matters, the 161,937 rows with pass mark 60.

| # | Step · weight | Exact calculation (source @970aabf) | Output | Missing input ⇒ | **What it actually measures, in one sentence** | Observed |
|---|---|---|---|---|---|---|
| 1 | `volume_surge` · 15 | `if not avg_volume_20d: return 0.0`; else `1.0 if volume > avg_volume_20d × min_volume_surge else 0.0` (`:247-256`) | binary | **0.0** | Would be "has today's volume already exceeded 1.3–1.5 × the 20-day average?" — but `avg_volume_20d` is hard-coded None, so **it measures nothing**. | **0.0 on 175,019 / 175,019** |
| 2 | `vwap_position` · 10 | LONG `1.0 if ltp > vwap`; SHORT `1.0 if ltp < vwap`; `vwap None` or `ltp 0/None` ⇒ 0.0 (`:258-269`) | binary | **0.0** | "At the second of screening, is the last traded price on the trade's side of today's VWAP?" | 1.0 on 160,434, 0.0 on 14,585 (8.3 %); formula reproduces the stored value on 161,937 / 161,937 |
| 3 | `atr_filter` · 10 | `if not atr or not ltp: return 0.0`; else `1.0 if (atr/ltp)×100 ≥ min_adr_pct` (`:271-281`) | binary | **0.0** | Would be "does the stock move enough per day?" — `atr` is hard-coded None, so **it measures nothing**. | **0.0 on all** |
| 4 | `rsi_range` · 10 | `rsi None ⇒ 0.5`; LONG `1.0 if 40 ≤ rsi ≤ 80`, SHORT `1.0 if 20 ≤ rsi ≤ 60` (`:283-316`) | 0 / 0.5 / 1 | **0.5** | Would be "is momentum in a normal band?" — `rsi` is hard-coded None, so **it is a constant 5 points**. | **0.5 on all** |
| 5 | `price_action` · 15 | `body = abs(ltp − open)`; `range = day_high − day_low + 1e-9`; `min(1.0, 2 × body / range)` (`:318-329`) | **continuous** 0–1, saturates at body ≥ 50 % of range | uses `ltp` as the default only if the key is absent | "How far is the price from today's open, as a share of today's high-low range — the size of today's daily candle body so far, **in either direction**." `abs()` makes it direction-blind: a long on a stock far *below* its open scores the same as one far above. | continuous: median **1.0**, **76.4 % exactly 1.0**, 10th pct 0.619; formula reproduces 161,937 / 161,937. Body against the trade direction on 519 rows; 4 of 3,992 current-regime passes |
| 6 | `sector_strength` · 10 | `1.0 if sector else 0.5` (`:331-336`) | 0.5 / 1 | **0.5** | **No trader sentence can be written from the code**: even when a sector is present it only checks that one exists — it never measures a sector's strength. `sector` is hard-coded None ⇒ a constant 5 points. | **0.5 on all** |
| 7 | `time_of_day` · 5 | minutes since `market_open` 09:15 (`system_config.yaml:103`, injected `main.py:3234-3237`) computed from **the clock at screening**, not from `triggered_at`: < 15 ⇒ 0.5, < 60 ⇒ 1.0, < 180 ⇒ 0.8, else 0.5 (`:338-370`) | 0.5 / 0.8 / 1 | — | "How long after 09:15 is it now?" With entries starting 10:00 this is **1.0 for 10:00–10:14, 0.8 for 10:15–12:14, 0.5 from 12:15**; the "too early" branch is unreachable. | 0.5 on 121,359 · 0.8 on 49,326 · 1.0 on 4,334. Clock buckets reproduce the cut-points exactly (< 10:15 → 3,983 all 1.0; 10:15–12:14 → 46,058 all 0.8; ≥ 12:15 → 111,896 all 0.5) |
| 8 | `spread_check` · 5 | `bid None or ask None ⇒ 0.5`; `mid = (ask+bid)/2`, `mid ≤ 0 ⇒ 0.5`; `spread_pct = (ask−bid)/mid × 100` (**percent**); `1.0 if spread_pct ≤ max_spread_pct` (`:372-395`) | binary in practice | 0.5 — **unreachable**: the adapter returns 0.0, not None, for an empty side | The YAML value is **0.005 in all 16 strategies**, compared against a percent ⇒ the test is **spread ≤ 0.005 % (half a basis point)**. What it measures in practice: "is the stock quoted exactly one tick wide *and* priced high enough that one tick is ≤ 0.005 % of the price?" | **1.0 on 1,446 (0.83 %)**. Their spreads: 0.01 (599), 0.10 (543), 0.05 (73), 0.20 (44), 0.02 (32); one row had ask < bid (negative spread ⇒ passes). Pass rate by price: ₹100–200 **0 %**, ₹200–250 3.8 %, ₹250–500 0.3 %, ₹500–1,000 **0 %**, ₹1,000–2,000 0.6 %, ₹2,000–5,000 4.7 % |
| 9 | `circuit_check` · 10 | `0.0 if circuit_state in (upper_circuit, lower_circuit) else 1.0` (`:397-404`) | binary | 1.0 | "Is the price not sitting on a circuit limit?" — but the circuit-proximity reject (§1 S16) runs first and removes those signals, so **it is constant in practice**. | 0.0 on **1** row; 1.0 on 175,018 |
| 10 | `signal_age` · 10 | `age = now − triggered_at` (seconds, `triggered_at` = Chartink's scan **minute**, seconds always :00); ≤ 30 ⇒ 1.0, ≤ 60 ⇒ 0.5, else 0.0 (`:406-423`) | 0 / 0.5 / 1 | 0.5 | "How many seconds after the Chartink scan minute is the step running?" — this includes Chartink's own delivery delay (median 14.5 s). | 1.0 on 165,629 · 0.5 on 9,306 · 0.0 on 84. Age at screening: median **17.3 s**, p95 29.9 s, p99 37.5 s |

### What the arithmetic allows — the finding this section exists for

Steps 1 and 3 contribute 0 always; steps 4 and 6 contribute 5 + 5 always. So a score is **10 + vwap (0/10) + price_action (0–15) + time (2.5/4/5) + spread (0/2.5/5) + circuit (0/10) + age (0/5/10)**; the ceiling is **65** (the source says so itself: `quality_scorer.py:16-19`, `_G2_CEILING_TRIPWIRE = 65`).

Enumerating every combination of the live discrete steps and solving, with the code's exact expression, for the smallest `price_action` that reaches 60: **8 of 108 combinations can pass.** All need vwap = 1, circuit = 1 and age = 1.0 (or 0.5 with everything else perfect):

| time_of_day (screen clock) | spread_check | signal_age | minimum price_action to reach 60 | max score |
|---|---|---|---|---|
| 1.0 (10:00–10:14) | 0 | 1.0 | **0.9667** (body ≥ 48.3 % of the day's range) | 60 |
| 1.0 | 1 | 1.0 | 0.6334 | 65 |
| 1.0 | 1 | 0.5 | 0.9667 | 60 |
| 0.8 (10:15–12:14) | 1 | 1.0 | 0.7000 | 64 |
| 0.5 (from 12:15) | 1 | 1.0 | 0.8000 | 62 |
| 0.5 / 0.8 / 1.0 | 0.5 *(unreachable, see step 8)* | 1.0 | 0.9667 / 0.8667 / 0.8000 | 60 / 62 / 62 |

⇒ **From 10:15 onwards, a signal whose spread is wider than 0.005 % cannot pass, whatever else is true of it.** The best such signal scores 59 before 12:15 (`10+10+10+10+4+15`) and 57 after (`57.5` → 57.49999… → 57). That is where the score distribution's two towers come from: **57 = 79,082 rows and 59 = 34,383 rows** of the 161,937 in the current regime.

**Measured, current regime (pass mark 60, 161,937 rows, 19-Jun → 11-Sep):**

| screened at | spread_check | rows | passed | pass rate |
|---|---|---:|---:|---:|
| 10:00–10:14 (time 1.0) | 0 | 3,965 | 2,950 | 74.4 % |
| 10:00–10:14 | 1 | 18 | 16 | 88.9 % |
| 10:15–12:14 (time 0.8) | 0 | 45,745 | **0** | **0 %** |
| 10:15–12:14 | 1 | 313 | 252 | 80.5 % |
| from 12:15 (time 0.5) | 0 | 110,935 | **0** | **0 %** |
| from 12:15 | 1 | 961 | 774 | 80.5 % |

**Of 3,992 passes, 2,950 (73.9 %) come from the first fifteen minutes of the entry window and the other 1,042 from rows whose spread was ≤ 0.005 %. Zero of 156,680 rows screened after 10:15 with a wider spread have ever passed.** By half-hour: 10:00–10:29 passed 2,986 of 8,159; every later half-hour passed between 56 and 186 of 10,101–25,536.

What that means for "secondary filtering", stated from the numbers only: the pass decision is set by **which quarter-hour the quote was taken in, and — after 10:15 — by whether the stock was quoted one tick wide at a price near the top of its tick band.** VWAP side, body size, freshness and circuit are necessary but, alone, not sufficient after 10:15. No step reads a candle series, a level, an average volume, a volatility or the previous close.

**Tier.** LOW < 65 ≤ MEDIUM < 80 ≤ HIGH. HIGH is unreachable (ceiling 65); MEDIUM only at exactly 65. The tier's only live consumer is the sizer's multiplier (`system_config.yaml:238-240`: HIGH 1.0 / MEDIUM 0.70 / **LOW 0.50**). Measured on production's last 332 trades: tier weight **0.5 on 330, 0.7 on 2**.

**The pass mark's history.** 13,082 rows carry `eligible_score` 55 (15-Jun → 10-Jul); 8,705 of the 13,030 all-time passes scored 55–59 under it. Every row since 10-Jul carries 60. `PASSED` with a score below its own `eligible_score`: **0**.

---

## 3 — THE THREE PRICES (trigger → entry → the price the broker sees)

### 3.1 The trigger price
Chartink's POST carries `stocks` and `trigger_prices` as parallel lists and `triggered_at` as a clock time (`"2:34 pm"`). The receiver pairs them per stock (§1 S5–S6) and stores each price in `signals.trigger_price` (`core/schema.sql:73`, *"price from Chartink at trigger time"*); `triggered_at` is Chartink's **scan minute** — seconds are :00 on **233,600 of 233,600** rows. It is the only price that survives from the signal: the entry and stop are recomputed from it (or from a later quote) and never stored separately before the order (the processor's own values are logged, not persisted — §3.3).
- Chartink scan minute → the system receives it: median **14.48 s**, p95 24.54 s, max 59.89 s (`received_at − triggered_at`, 233,600 rows).
- Chartink's price vs the screener's own quote a few seconds later (187,925 screened signals, signed in the trade's direction): median **0.00 %**, p5 −0.19 %, p95 +0.18 %, p1/p99 −0.43 % / +0.44 %; identical on 26.2 %; more than 0.5 % apart on 1.45 %.

### 3.2 Entry price derivation — the exact rule
`signals/signal_processor.py:1748-1795 @970aabf` (`_derive_prices`), called at `:1028-1030` with `trigger_price`:
```
entry_method == "LIMIT":  LONG  entry = trigger × (1 − entry_offset_pct)
                          SHORT entry = trigger × (1 + entry_offset_pct)
entry_method == "MARKET": entry = trigger                       (no YAML uses MARKET)
entry ≤ 0  ⇒  REJECTED_INVALID_DERIVED_PRICE                   (:1786-1798)
```
Every YAML is `LIMIT`; `entry_offset_pct` is **0.001** for the 13 intraday strategies and **0.002** for the 3 delivery ones. So a long is bid 0.1 % (0.2 %) **below** the reference price and a short offered the same amount **above** it — the order waits for price to come back. Nothing here rounds to the tick (rounding happens in the adapter, §3.7). No data other than the trigger and the strategy's two fields is read.
Measured: on the 541 trades of the six strategies that do not re-anchor, the stored `entry_target_price` equals this formula exactly on 501; the 40 that do not are all dated 15–23 June (the first live weeks).

### 3.3 The M-S1 re-anchor (FIX-067) — read properly
**What triggers it.** `signal_processor.py:1082`: `if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:`. `quote_fn` is always wired (`broker_adapter.get_quote`, `main.py:3616`), so it runs for every strategy whose YAML says `pullback_wait_enabled: false` — **gap_fade_long/short, gap_go_long/short, the three positional (delivery) strategies, range_breakout_long/short (never fire) and pb01 (disabled)** — and not for the six that say `true` (**first_pullback_long/short, open_high_breakdown_short, open_low_breakout_long, vwap_bounce_long, vwap_rejection_short**). For those six nothing waits either: the comment at `:1074-1075` says *"EntryGate already waits for current price"*, but nothing ever calls `EntryGate.add()` (prior report §11.1) — they simply keep Chartink's price.

**What it does.** A second quote, taken **after screening passed** (`:1085-1087`); if its `last_price > 0` the entry **and** the stop are re-derived with the same formula from that live price (`:1098-1100`) and a log line records both (`:1093-1097`: *"stale=… live=… delta=… — re-anchoring entry/SL/TGT/sizing/reservation"*). If the quote fails or returns nothing, the stale Chartink-based values stand (`:1102-1106`).

**What changes.** Entry and stop directly; then, because everything downstream derives from them, the target (`:1368`), the quantity (sizing, `:1112-1121`), the reserved capital (`:1328-1331`) and the slippage guard's tolerance (placer, §1 S34). `trigger_price` is kept and passed to the placer for that guard (`:1457`).

**The pre-anchor values** are computed at `:1028-1030`, overwritten in place, and survive only in that log line. They are not in any table.

**Is the screening still valid afterwards?** Nothing re-checks it. The screener judged the quote it fetched itself (`secondary_screener.py:170`); the circuit-proximity rule judged `trigger_price` (`:213`); the entry is now built on a third price. Measured on production's trades:
- 293 trades were re-anchored (entry ≠ trigger formula among re-anchoring strategies); another 121 of those strategies' trades kept the trigger formula (quote unavailable or unchanged).
- The live price used, against Chartink's trigger, signed in the trade's direction: median **−0.001 %**, p5 −0.30 %, p95 +0.28 %, range −1.24 % … +1.61 %.
- The re-anchored **entry** sat on the wrong side of the screen-time VWAP in **8 of 293**; the live price itself in **0**; the entry inside the 2 % circuit margin in **0**.
- Twin example (§6): Chartink 1001.70 → screen quote 1001.80 → re-anchor quote **1001.15** → entry 1000.14885.

### 3.4 Stop derivation
`signal_processor.py:1800-1895`. All 16 strategies are `sl_method: FIXED_PCT`: `LONG sl = entry × (1 − sl_pct)`, `SHORT sl = entry × (1 + sl_pct)` (`:1836-1839`). Then a clamp to `[sl_min_pct, sl_max_pct]` that cannot bind (`sl_min ≤ sl_pct ≤ sl_max` is enforced by the schema) and a 09:15–09:30 gap buffer that cannot run under the 10:00 floor. The ATR branch (`:1802-1811`) is never entered. No level, candle or volatility is read.

| sl_pct | strategies |
|---|---|
| 0.008 | vwap_bounce_long, vwap_rejection_short |
| 0.010 | gap_fade_long/short, open_high_breakdown_short, open_low_breakout_long, range_breakout_long/short, pb01 |
| 0.012 | gap_go_long/short |
| 0.015 | first_pullback_long/short |
| 0.020 | positional_momentum_long, positional_sector_rotation, positional_swing_long |

Measured: `sl_initial` = entry × (1 ∓ sl_pct) within 2 bp on **955 of 955** trades. At the broker the MIS stop goes out as an SL (stop-limit) order: trigger = the stop rounded to the nearest tick, limit = trigger ∓ 0.5 % rounded away from the market (`capital.sl_limit_offset_pct` 0.005, `system_config.yaml:204`); the delivery stop goes out inside a GTT with limit = trigger × 0.97 (`gtt_sl_limit_offset_pct` 0.03, `:205`). Both are placed **only after the entry fills** (§1 S38).

### 3.5 Target derivation
`signal_processor.py:1901-1953`, called at `:1368` — **inside admission, after capital is reserved**. All strategies are `tgt_method: RISK_REWARD`, `tgt_risk_reward: 1.5`: `LONG tgt = entry + |entry − sl| × 1.5`, `SHORT tgt = entry − |entry − sl| × 1.5` (`:1930-1936`). A guard rejects a target closer than `tgt_min_pct` 0.3 % (`:1945-1951`; `system_config.yaml:348`) — it cannot bind (the smallest target distance is 0.8 % × 1.5 = 1.2 %).
Measured: 852 of 955 trades have `tgt_initial` = 1.5 R within 2 bp; `tgt_risk_reward_applied` = 1.5 on 842, **2.0 on 36**, NULL on 77 (older configurations).
**The target sent to the broker is not this number.** On fill the placer recomputes it from the fill price with the same 1.5 R (`orders/order_placer.py:2870-2879`, FIX-013), then clamps it 2 % inside the day's circuit band before placing it (`price_math.clamp_exit_into_band`; §6 shows RAYMOND's 1018.15 placed as **1004.10**). `trades.tgt_initial` keeps the pre-fill value.

### 3.6 Is R:R computed in the live path, and does anything act on it?
- **Computed as a measurement — no.** The live path never asks "how much room is there to the next obstacle?" The target is *defined* as 1.5 × the stop distance, so the ratio is an input, and every trade's pre-fill R:R is 1.5 by construction. It is stored as `trades.tgt_risk_reward_applied`.
- **One live check reads it, and it cannot fire:** the placer's FIX-136 gate (`order_placer.py:937-958`) refuses if `(tgt − entry)/(entry − sl) < entry_gate.min_effective_rr` **1.0** (`system_config.yaml:659`). It runs before anything can move the entry, on values that are 1.5 by construction. `rr_gate_failed` log lines on production, 02-Sep → 11-Sep: **0**.
- **One live check uses R:R after placement:** the order monitor cancels a resting entry when `(tgt − LTP)/(entry − sl) < min_pending_rr` **1.0** (`broker/order_monitor.py:1128-1207`; `system_config.yaml:660`) — with a 1.5 R target that is "the price has already run more than 0.5 R past our limit before we were filled". Production logs: **5** such cancels in 8 days (HIKAL, GUJALKALI, XTRANET, MVGJL, GARFIBRES — all BUYs, `pending_rr` 0.62–0.94).
- **After the circuit clamp nothing re-checks it:** RAYMOND's placed target 1004.10 against a stop 12.0 below the fill is **R:R 0.33** (§6).
- **The structural R:R exists only in shadow:** the V3 chain computes `v3_rr` against its S&R zones with `rr_floor` 2.0 (`system_config.yaml:577`) and logs `WOULD_REJECT_RR` (RAYMOND: `v3_rr=0.1119 live_rr=1.5`). Nothing reads it (§1 S23).

### 3.7 The limit price actually sent
- The placer does no rounding (`order_placer.py:928-931`). The adapter snaps every LIMIT price to the **nearest** tick, ties up, **the same for BUY and SELL** (`broker/zerodha_adapter.py:1436-1452`, `_round_nearest_to_tick`); only stop-limit prices are rounded directionally. The tick comes from the instrument cache (`config/instruments.csv`), falling back to **0.05** with a warning when the symbol is missing (`:1383-1407`) — production logged that fallback for XTRANET, RIR, MAFANG, NIFTY1, MONQ50 and MASPTOP50 between 04-Sep and 09-Sep.
- The exact kwargs (`:639-654`): `variety="regular"`, `exchange="NSE"`, `tradingsymbol`, `transaction_type` BUY/SELL, `quantity`, `product` MIS/CNC, `order_type="LIMIT"`, `price=<snapped entry>`, `tag=trade_id[:16]`; `trigger_price`, `validity`, `disclosed_quantity` and `market_protection` are not sent.
- **Offset from the entry price:** zero on the normal path, apart from the snap. One exception, inside the placer: the FIX-075 drift top-up (`order_placer.py:1194-1262`) — if a fresh quote is more than 0.5 % *above* the entry and a margin top-up succeeds, **the entry becomes the raw LTP** (stop and target are not recomputed). Production logs: **1** occurrence in 8 days (07-Sep QUICKHEAL, 157.93 → 158.73). It is effectively reachable only for delivery: for intraday the slippage guard, which runs first against the trigger with a tolerance of 22 % of the stop distance, refuses that move earlier *(arithmetic inference)*.
- **The price sent is not stored anywhere.** The ENTRY `orders` row is written with `price` and `trigger_price` NULL (`orders/order_manager.py:387-388`) — **0 of 769** ENTRY rows on production carry a price; `trades.entry_target_price` is the processor's unsnapped value; `order_execution_log.intended_price` (written only at fill) is also the unsnapped value (twin: 1000.14885 intended, filled 1000.15).
- What the broker did with it, measured: filled entries sat at the limit (median −0.0002 %, p95 +0.0047 % worse; 374 fills). Kite's own refusals in history: 18 *"Tick size … enter price in the multiple of tick size"* (16 between 17 and 23 June, 2 on 01-Sep for ENGINERSIN); *"MIS orders are currently blocked for <symbol>"* on the rest.
- **Life of the resting LIMIT:** cancelled if unfilled after `order_monitor.fill_timeout_sec` **60 s** (`system_config.yaml:194`; production: 48 `order_monitor.fill_timeout` cancels in 8 days; `ENTRY` rows cancelled after a median 61.2 s); cancelled earlier by the pending-R:R rule above; partial fills have the remainder cancelled at once; all resting entries are force-cancelled at 15:15. Fill rate of entries that reached the broker: **374 of 769 (48.6 %)** — pullback-flag strategies LONG 55.2 % / SHORT 34.9 %, re-anchoring strategies LONG 48.8 % / SHORT 25.5 %.

---

## 4 — WHERE A SIGNAL CAN DIE

The measured funnel (4.2) leads this document. Below are 4.1, every rejection point, and 4.3, the split by mechanism.

### 4.1 Every rejection point, in path order

"Fired" is measured on production: 11-Sep / last 20 days (17-Aug → 11-Sep). "—" means never observed in retained data; "cannot" means unreachable under the current config (arithmetic or wiring stated in §1).

| # | Where (@970aabf) | Condition | Outcome string | Fired |
|---|---|---|---|---|
| 1 | receiver `:485-490` | service shutting down | HTTP 503 | — |
| 2 | receiver `:495-504` | > 60 requests burst / 5 per s from one IP | HTTP 429 | — |
| 3 | receiver `:547-549` | bad/missing token or HMAC | HTTP 401 | 0 / 0 |
| 4 | receiver `:552-554` | scanner not in `scan_webhook_map` | HTTP 404 | 0 / 0 |
| 5 | receiver `:562-564` | `scanner_type: eod` (pb01) | HTTP 200, routed to the watchlist; never enters the order path | 1 / 20 POSTs |
| 6 | receiver `:567-568` | kill switch SOFT/HARD | HTTP 403 `Kill switch active; signals rejected` | these two share one code |
| 7 | receiver `:570-578` | queue ≥ 240 | HTTP 503 `Signal queue at capacity` | 0 / 1 |
| 8 | receiver `:581-583` | not a trading day or outside [10:00, 15:00) | HTTP 403 `Outside entry window` | 463 / 12,626 (6 + 8 combined) |
| 9 | receiver `:586-674` | malformed JSON · missing field · `scan_name` ≠ path · bad `triggered_at` · list mismatch | HTTP 400 | 0 / 0 |
| 10 | receiver `:709-716` | symbol in `excluded_symbols` | `REJECTED_EXCLUDED_SYMBOL` (response only) | not stored |
| 11 | receiver `:905-914` | empty symbol · price not a number or ≤ 0 | `INVALID_SYMBOL` / `INVALID_PRICE` (response only) | not stored |
| 12 | receiver `:919-926` | now − `triggered_at` > 600 s | `EXPIRED` (response only) | not stored |
| 13 | receiver `:934-935` | symbol already in flight (any scanner) | `IN_PROCESS` (response only) | not stored |
| 14 | receiver `:940-946`, `:981-1015` | same symbol+scanner within 300 s, or same fingerprint today | `DUPLICATE` (response only) | not stored — #10–#14 total **17,198 / 447,934** |
| 15 | receiver `:1016-1068` | DB insert failed · queue full | `STORE_ERROR` / `QUEUE_FULL` (HTTP 503) | — |
| 16 | processor `:906-907` | kill switch | `REJECTED_KILL_SWITCH` | — |
| 17 | processor `:910-912`, `:977-982` | outside the global or per-strategy window | `REJECTED_OUTSIDE_ENTRY_WINDOW` | — |
| 18 | processor `:915-921` | age > 600 s | `REJECTED_EXPIRED` | — |
| 19 | processor `:1976-2008` | shadow inning active / tracker error | `REJECTED_SHADOW_INNING_ACTIVE` / `_SHADOW_TRACKER_ERROR` | 0 / 0 (4,168 on 09–24 Jul) |
| 20 | processor `:933-953` | no strategy for the scanner | `REJECTED_UNKNOWN_STRATEGY` | — |
| 21 | processor `:959-972` | strategy switched off / trade-type mismatch | `REJECTED_STRATEGY_CONTROL` / `REJECTED_TRADE_TYPE` | 0 / 2,051 |
| 22 | processor `:985-990` | strategy loss > 2 × its average losing day, before 12:00 | `REJECTED_STRATEGY_CIRCUIT_BREAKER` | 0 / 4,485 |
| 23 | screener `:148-165` | MIS-blocked symbol, only if `shadow: false` | `REJECTED_NOT_MIS_TRADABLE` | cannot (shadow) |
| 24 | screener `:168-196` | no quote / quote error | `SKIPPED_QUOTE_UNAVAILABLE` | 160 / 3,666 |
| 25 | screener `:213-232` | trigger within 2 % of a circuit limit | `REJECTED_CIRCUIT_PROXIMITY` | 113 / 7,612 |
| 26 | screener `:266-286` | a step raised | `REJECTED_STEP_ERROR` | — |
| 27 | screener `:317-337` | score < 60 | `REJECTED_SCORE_<n>` | **3,453 / 81,034** |
| 28 | screener `:340-354` | signal_age step = 0 | `REJECTED_SIGNAL_AGE` | cannot (0 ever) |
| 29 | processor `:1786-1846` | entry ≤ 0 · SL pct ≤ 0 · unknown SL method | `REJECTED_INVALID_DERIVED_PRICE` / `_ZERO_SL` | cannot |
| 30 | processor `:1111-1128` | sizer returns qty 0 or fails a guard | `REJECTED_SIZING_<constraint>` | 32 / 481 |
| 31 | processor `:744-779` | strategy at its concurrent cap | `REJECTED_STRATEGY_POSITION_LIMIT` | 3 / 111 |
| 32 | processor `:802-864` | symbol+direction already traded today in this book | `REJECTED_SYMBOL_DIRECTION_DAILY_LIMIT` | 7 / 244 |
| 33 | risk engine `:517-794` | kill · capital · open positions · daily trades · 4 losses · daily loss · (sector, observe) · contrary · duplicate symbol | `REJECTED_<check>` | DUPLICATE_SYMBOL 1 / 78 · OPEN_POSITIONS 0 / 136 · CONSECUTIVE_LOSSES 0 / 8 |
| 34 | fund manager `:562-577` | bucket avail < margin × 1.05 | `REJECTED_RESERVE_FAILED` | — |
| 35 | processor `:1945-1951` | target closer than 0.3 % | `REJECTED_TGT_DISTANCE_TOO_SMALL` | cannot |
| 36 | processor `:1389-1405` | kill switch / shutdown after reservation | `REJECTED_KILL_SWITCH_LATE` / `REJECTED_SHUTDOWN` | — |
| 37 | processor `:1410-1418` | 20 s global gap · 3 per 60 s · 300 s per symbol | `REJECTED_ENTRY_THROTTLED` | 16 / 549 |
| 38 | placer `:937-958` | R:R < 1.0 | `PLACEMENT_FAILED` `RR_GATE_FAILED…` | cannot |
| 39 | placer `:1049-1097`, `:1335-1343` | kill switch (twice) · past 15:15 | `PLACEMENT_FAILED` | — |
| 40 | placer `:1099-1192` | LTP moved from the trigger by > min(22 % of SL distance, ₹5) or > 1 % | `PLACEMENT_FAILED` `slippage_exceeded…` | 29 slippage in 20 days (all-time 100) |
| 41 | placer `:1194-1289` | drift > 0.5 % and top-up refused | `PLACEMENT_FAILED` (trade `REJECTED_PRICE_DRIFT`) | 0 in 8 days of logs |
| 42 | adapter / Kite | broker refuses (tick size, MIS blocked, permission…) | `PLACEMENT_FAILED` `Zerodha rejected order: …` | 21 in 20 days (all-time 81 + 5) |
| 43 | order monitor | unfilled after 60 s · remaining R:R < 1.0 · 15:15 | trade `FAILED` (signal stays `PROCESSED`) | 15 / 157 unfilled |

11-Sep's `PLACEMENT_FAILED` total of 1 (PINELABS) was a slippage abort: *"trigger=186.51 ltp=187.50 | slippage ₹0.99 > tolerance ₹0.25 (…88% of SL)"*.

### 4.3 Whose rejection is it? Counted by mechanism

The code records no notion of fault. The grouping below is mine, by the mechanism that removed the signal.

| Mechanism | What removes it | 11-Sep | 20 days |
|---|---|---:|---:|
| **Scanner stream vs the receiver** | the scanner re-posts the same stock every minute (kept once per 5 min, or refused while in flight); POSTs outside 10:00–15:00 | 17,198 stock-alerts + 463 POSTs | 447,934 stock-alerts + 12,626 POSTs |
| **Market data** | no broker quote for the symbol | 160 | 3,666 |
| **Filter: circuit band** | trigger within 2 % of a limit | 113 | 7,612 |
| **Filter: the score** | < 60 | **3,453** | **81,034** |
| **Strategy controls** | switch off · strategy breaker | 0 | 6,536 |
| **Capital / sizing** | qty 0 under concentration / capital / risk | 32 | 481 |
| **Portfolio and risk limits** | strategy cap · one-per-symbol-direction · open positions · duplicate symbol · consecutive losses | 11 | 577 |
| **Throttle** | 20 s / 300 s spacing | 16 | 549 |
| **Placement** | slippage guard · broker refusal | 1 | 50 |
| **Execution** | LIMIT not filled in time | 15 | 157 |

Of the 3,534 scored signals on 11-Sep, the score removed 97.7 %. Of the 81 that passed, capital, limits and the throttle removed 59 (73 %) before any order existed. Of the 21 orders, the LIMIT's own terms removed 15 (71 %).

---

## 5 — WHAT IS ALIVE AND WHAT IS NOT (entry path)

⛔ Nothing is deleted; each item is a finding.

### 5.1 Runs, but cannot affect the outcome

| Component | Where | Why it cannot act |
|---|---|---|
| V3 decision chain (S&R zones, ATR30, 1h EMA20, RR/HTF/EXTREME gates, 20-step score) | `v3_chain/runner.py`; hook `signal_processor.py:1136-1143` | `v3_chain_mode: "shadow"`; runner holds no reference to the processor or placer; output = `would_be.jsonl` + log |
| Hard-gate V3 re-scale ("NEW score") | `secondary_screener.py:310-314`, `:530-552` | `v3_hardgate_mode: "shadow"`; logs only |
| Portfolio allocator | `signal_processor.py:1147-1172` | `allocator_mode: "shadow"`; regret JSONL only |
| S&R detector V1 | `signal_processor.py:1550-1561` | runs after the order is placed; gates nothing |
| MIS learned blocklist | `secondary_screener.py:148-165` | `mis_filter.shadow: true`; logs a would-drop |
| EntryGate (the "pullback wait") | constructed and started (`main.py:3839-3844`, `:3975`) | nothing calls `EntryGate.add()` |
| Retest diverter / ZoneWarmer | `signal_processor.py:1042-1056`, `:361-375` | not constructed (`wait_for_retest_enabled: false`) |
| Shadow-inning guard | `:1976-2008` | `shadow_tracker.enabled: false` since 25-Jul |
| Order-bucket pre-check (FIX-007) | `:415-461` | `rate_limiter` not passed to the processor |
| Live-margin sizing (FIX-072) | `position_sizer.py:389-423` | no broker adapter passed to the sizer |
| Performance weights | `signal_processor.py:1120` | `perf_weights` never passed ⇒ always 1.0; no `PerformanceAllocator` is built |
| Risk check SECTOR_EXPOSURE | `risk_engine.py:735-763` | `sector_cap_mode: observe` |
| Unrealized term of DAILY_LOSS | `risk_engine.py:692-731` | `daily_loss_include_unrealized: false` |
| Placer liquidity check | `order_placer.py:1291-1305` | flag not passed ⇒ constructor default False |
| Heartbeats / stall detection | `signal_processor.py:664-673` | `in_flight_heartbeat_fn` not passed ⇒ no-ops; claims evicted by age |
| Four scoring steps | `step_executor.py` | volume_surge 0, atr_filter 0, rsi_range 0.5, sector_strength 0.5 on every row |
| `circuit_check` step | `step_executor.py:397-404` | the proximity reject runs first ⇒ 1.0 on 175,018 of 175,019 rows |
| `REJECTED_SIGNAL_AGE` | `secondary_screener.py:340-354` | age 0 ⇒ score ≤ 55 ⇒ already rejected on score |
| Tier HIGH; MEDIUM | `quality_scorer.py:122-132` | ceiling 65 < 80; MEDIUM only at exactly 65 |
| Placer R:R gate | `order_placer.py:937-958` | R:R is 1.5 by construction vs a 1.0 floor |
| Price rejects in `_derive_prices`/`_derive_target` | `:1786-1951` | unreachable with current YAML values |
| Sizer POSITION_VALUE_CAP / BELOW_MIN / ZERO_MULTIPLIER / MULTIPLIER label | `position_sizer.py` | unreachable under current config (inference, arithmetic) |
| CO_PLUS_TGT protocol, SmartTgt registration, BreakevenManager | `order_placer.py:961`, `:2173-2240` | protocol is constant LIMIT_TRIPLE; breakeven manager never passed |

### 5.2 Computed, and nothing reads it

- `StepExecutorResult.rejected_at`; `ScoreResult.step_scores`, `.missing_steps`, `.tier_thresholds` and `.passed`. No non-test reader; the screener recomputes the pass itself.
- `SizingResult.risk_amount`; `ApprovalResult.snapshot` and `.checks_run`, including the `count_in_flight_orders()` query that feeds only the snapshot.
- `SignalProcessor._sector_for()` probes `sector_for` / `get_sector`, but the instrument cache only has `sector()`, so it always returns `"UNKNOWN"`. That value goes only to the V3 and allocator shadows. The twin's RAYMOND trade row shows `sector: UNKNOWN`.
- `PlacedOrder` fields other than the two ids (snapped price, product, status); `signals.expires_at` (dashboard only; expiry uses `triggered_at`); the receiver's numeric casts; the `now` parameter of `_admit_and_place`.
- **The previous close.** The market-data dict reserves a `prev_close` slot and hard-codes it None (`secondary_screener.py:416`). The adapter reads `ohlc.open/high/low` from the Kite quote and not `ohlc.close` (`zerodha_adapter.py:1784-1795`). That Kite's quote carries the previous close in `ohlc.close` is inference; the raw quote is not stored.

### 5.3 Config keys this path reads that change nothing today

- **Strategy YAMLs** — full inventory in §8:
  - 13 of the 35–36 keys in every enabled file are never consulted on the trading path;
  - 9–10 more are read but neutralised: `min_score` (sentinel), `lot_size` (sentinel), `entry_start_time` (floor wins), `entry_end_time` (coincides), `sl_min_pct`/`sl_max_pct` (cannot bind), `sl_gap_buffer_pct` and `tgt_pct` (branches unreachable), `min_volume_surge` and `min_adr_pct` (inputs are None).
- **`system_config.yaml`:**
  - `signal_processor.pipeline_timeout_sec` (no reader);
  - `position_sizing.min_tick_size`, `max_single_order_qty` and `capital.slm_margin_buffer_pct` (not passed; the code defaults happen to equal the YAML);
  - `position_sizing.dynamic_by_winrate`, `min_multiplier`, `max_multiplier`;
  - `max_position_value_pct` and `delivery_max_position_value_pct` (cannot bind);
  - `signal_processor.tgt_min_pct` (cannot bind);
  - `entry_burst_max` (the 20 s gap is checked first; inference);
  - `entry_gate.liquidity_check_enabled`, `max_spread_pct`, `min_depth_qty` (not wired);
  - `risk.price_drift_threshold` (not wired; default equal);
  - `entry_gate.min_effective_rr` (cannot fire);
  - `special_sessions` (empty);
  - `webhook.require_hmac` (the branch it gates is unreachable while false).
- **`config/broker_limits.yaml`:** `timeouts.connect_sec`, `backoff_sequence_sec` (no runtime reader).
- **`config/scoring_weights.yaml`:** `high_score_threshold` 80 (unreachable); the `v3_*` thresholds (shadow).

### 5.4 Looks like a filter, and does not filter

| Looks like | What it actually does |
|---|---|
| `volume_surge`, `atr_filter`, `rsi_range`, `sector_strength` | constants: 0, 0, 0.5, 0.5 on every row. 25 of the 100 weight can never be earned, and 10 are given to every signal |
| `sector_strength` even if a sector were supplied | only checks a sector *exists* (`step_executor.py:331-336`) |
| `price_action` "strong directional body" | direction-blind `abs(ltp − open)`; 4 of 3,992 current-regime passes had the body against the trade |
| `spread_check` "liquidity" | a percent spread vs a fraction threshold (0.005) ⇒ passes only for one-tick spreads near the top of a tick band. **It decides almost every pass after 10:15** |
| `time_of_day` "entry time quality" (weight 5) | decides whether 60 is reachable without the spread: before 10:15 yes, after no |
| per-strategy `min_score` | sentinel 0 ⇒ global 60 for all 16 |
| `pullback_wait_enabled` "wait for a pullback" | only switches the re-anchor off; nothing waits |
| receiver `EXPIRED` / `INVALID_SYMBOL` / `INVALID_PRICE` | a future timestamp passes; only an empty symbol is invalid; `nan`/`inf` prices pass (source) |
| the 600 s expiry | Chartink delivers within 60 s (max 59.89 s measured) ⇒ never binds |
| tier multipliers HIGH/MEDIUM/LOW | effectively LOW (0.5) on every trade |
| the R:R gate, the sector cap, the MIS filter, the V3 gates, the allocator caps | cannot fire (constant R:R) or shadow / observe / null |
| the risk rung in sizing (1 % of capital) | never the binding constraint; concentration binds 332/332 |

**The reverse also exists: a step that does not look like a filter but acts as one.** The entry is a LIMIT placed 0.1 % (delivery 0.2 %) *better* than the reference price. It lives 60 seconds and is also cancelled if price runs 0.5 R past it. Of the 769 entries that reached the broker, **395 were cancelled unfilled** (374 filled). Of those unfilled cancels, production's retained logs (02–11 Sep) show 48 by the 60-second timeout and 5 by the pending-R:R rule.

---

## 6 — ONE REAL SIGNAL, ALL THE WAY THROUGH (and one that died)

Both come from 11-Sep. The traded one is from the **testing VM (the twin, account VBB097)** because only the twin runs the evidence contract today (it loaded there at 09:16:44; production loads it Monday 08:15). Its evidence records were read from `data_store/evidence/signal_evidence_VBB097_2026-09-11.jsonl` (5,618 records: P3 5,468 · P2 127 · P1 23), cross-checked against the twin's `signals`, `screener_results`, `trades`, `orders`, `order_execution_log` rows and its `system_2026-09-11.log`, all read-only. The twin runs the same decision code as production: 11 decision-path files (processor, screener, step executor, scorer, receiver, sizer, risk engine, fund manager, placer, adapter, scoring weights) hash identical to `970aabf` on both VMs, the twin's `webhook_receiver.py` differing only by CRLF line endings.

### 6.1 TRADE — RAYMOND, `gap_go_long`, `sig_63cf7564410449d0985688a7d7e8dd28`

| Stage | Time (IST) | Recorded values |
|---|---|---|
| Chartink scan | 14:53:00 | `triggered_at` 14:53:00; `trigger_price` **1001.70** |
| Receipt | 14:53:07.146 | `received_at`; `expires_at` 15:03:07.146 (+600 s); status QUEUED → PROCESSING |
| Pre-screen gates | — | kill switch off · window 10:00–15:00 open · age 7 s < 600 · no shadow inning · `gap_go_long` enabled · trade_type BOTH · strategy breaker not paused |
| Quote #1 (screener) | 14:53:07.186 | ltp **1001.80** · bid 1001.70 · ask 1001.75 · open 853.85 · high 1024.50 · low 835.05 · vwap 963.61 · volume 14,958,184 · upper 1024.60 · lower 683.10 · atr/rsi/sector/prev_close/avg_volume_20d **null** |
| Circuit proximity | — | LONG: 1001.70 < upper × 0.98 = 1004.108 and > lower × 1.02 = 696.76 ⇒ pass (by 0.24 %) |
| Ten steps | — | volume_surge 0 · vwap_position **1** (1001.80 > 963.61) · atr 0 · rsi 0.5 · price_action **1** (\|1001.80−853.85\| / (1024.50−835.05) = 0.781 → ×2 → capped 1) · sector 0.5 · time_of_day **0.5** (after 12:15) · spread_check **1** ((1001.75−1001.70)/1001.725 × 100 = **0.00499 % ≤ 0.005**) · circuit 1 · signal_age **1** (~7 s) |
| Score | 14:53:07.186 | 0+10+0+5+15+5+2.5+5+10+10 = 62.5 → `round(62.5)` = **62** ≥ 60 ⇒ **PASSED**, tier LOW. Shadow log: *"OLD score=62 tier=LOW \| NEW score=53 tier=LOW gate=PASS"* (nothing reads NEW) |
| Entry / SL (stale) | — | 1001.70 × 0.999 = 1000.6983; SL × (1 − 0.012) — overwritten next |
| **Re-anchor (quote #2)** | 14:53:08.758 | *"stale=1001.70 live=1001.15 delta=-0.55 — re-anchoring"* ⇒ entry **1000.14885** (= 1001.15 × 0.999), SL **988.1470638** (= entry × 0.988) |
| Sizing | — | qty_by_risk **8** · qty_by_capital **35** · qty_by_concentration **1** ⇒ raw 1 × tier 0.5 × perf 1.0 ⇒ **qty 1**; binding **concentration** |
| V3 chain (shadow) | enqueued ~14:53:08.76; verdict logged 14:53:09.388 | *"verdict=WOULD_REJECT_RR v3_rr=0.1119 live_rr=1.5"* — ignored |
| Admission | 14:53:08.760 | strategy cap OK · one-per-symbol-direction OK · `risk_engine.approve … approved=True checks_run=10 margin=200.03` · reservation `0d997221b8d3499c` (margin 1000.14885 × 1 / 5 = **200.03**) · status RESERVED |
| Target | — | 1000.14885 + 1.5 × 12.0017862 = **1018.1515293** |
| Signal alert | 14:53:09.435 | Telegram *"INTRADAY SIGNAL — RAYMOND"* delivered |
| Throttle / kill / shutdown | — | passed |
| P1 evidence | 14:53:09.436 | entry_final 1000.14885 · reanchored **true** · sl 988.1470638 · tgt 1018.1515293 · qty 1 · binding CONCENTRATION |
| Trade row | 14:53:09.439 | `trd_68abb5318a3b403490cd5437175df275`, PENDING_FILL → PENDING |
| Slippage guard (quote #3) | 14:53:12.091 | ltp 1001.90 vs trigger 1001.70 ⇒ ₹0.20 (0.02 %); tolerance 0.22 × 13.55 = **₹2.98** ⇒ not aborted |
| Broker call | 14:53:13.757 → .799 | LIMIT BUY 1 MIS → Kite id **260911170817593**. `orders.price` stored: **NULL** |
| Fill | 14:53:44.933 | 1000.15 (31.1 s after placement); `signal_to_order_ms` 6,653 · `order_to_fill_ms` 31,133 |
| TGT recomputed from fill | 14:53:44.936 | 1000.15 + 1.5 × (1000.15 − 988.147) = **1018.1544** |
| Clamp to circuit band | 14:53:44.949 | *"exit_price_clamped_to_band … tgt_price 1004.1, upper_circuit 1024.6"* ⇒ TGT **1004.10** (= 1024.60 × 0.98, snapped) |
| SL leg | 14:53:44.998 | SL order: trigger 988.1470638 (snapped at the adapter), limit **983.20** (988.147 × 0.995, rounded down) — id 260911170818449 |
| TGT leg | 14:53:45.039 | LIMIT SELL 1004.10 — id 260911170818450; *"exits_verify … TGT clamped to circuit band 1004.10 (intended 1018.15)"* |
| Outcome (out of scope, for completeness) | 14:59:33 | TGT filled 1004.10 · gross +3.95 · charges 1.06 · **net +2.89** |

Total time Chartink minute → entry order at the broker: **13.8 s** (7.1 s of it before the system received the alert).

### 6.2 REJECTED — the same stock, one minute later: RAYMOND, `positional_sector_rotation`, `sig_8190f13b04c74326a9cdfa01e7d2664e`

| Stage | Time | Recorded values |
|---|---|---|
| Chartink / receipt | 14:54:00 / ~14:54:10 | trigger **1000.00** |
| Quote (screener) | 14:54:10.280 | ltp 999.05 · bid **999.25** · ask **999.55** · vwap 963.64 · same open/high/low/circuit as above |
| Ten steps | — | identical to 6.1 **except** spread_check **0**: (999.55 − 999.25)/999.40 × 100 = **0.030 %** > 0.005 |
| Score | 14:54:10.280 | 0+10+0+5+15+5+2.5+**0**+10+10 = 57.5 → `(57.5/100)×100` = 57.49999… → **57** ⇒ **REJECTED_SCORE_57**; shadow NEW 47 |
| End | 14:54:10.283 | *"screener rejected: REJECTED_SCORE_57"*; P3 evidence written; nothing else runs |

**On production, the same minute:** production received RAYMOND from `positional_sector_rotation` and `gap_fade_long` at 14:53 (not from `gap_go_long`; production's gap_go_long alert did not post that day) and screened it at 14:53:14.66 with bid 1001.25 / ask 1001.80 — spread **0.0549 %** ⇒ spread_check 0 ⇒ **57** ⇒ rejected. Same stock, same scan minute, 7.5 seconds apart: the twin traded it because its quote happened to be one tick wide.

### 6.3 A signal that passed screening and still died — LIQUIDBETF, `gap_fade_long`, `sig_8efb220e7359461cb3d3b645237b4256` (twin, 14:52)
Quote: ltp 1098.69, open 1098.14, high 1098.69, low 1098.14 (the whole day's range was ₹0.55), vwap 1098.67, bid/ask 1098.67/1098.69 ⇒ vwap_position 1, price_action 1 (body = range), spread 0.0018 % ⇒ 1, time 0.5 ⇒ **62, PASSED**. Then sizing: *"qty=0: CONCENTRATION exhausted for LIQUIDBETF (risk_qty=9 capital_qty=31 conc_qty=0)"* ⇒ **REJECTED_SIZING_CONCENTRATION**. LIQUIDBETF is a liquid (money-market) ETF; it passed every screening step. Production rejected it the same way at 14:41, 14:47 and 14:59.

---

## 7 — MIS vs GTT: what differs in the entry path

As previously measured: there is **no timeframe split** (one 30m + 1H + 1D list serves both books, and only in shadow code). What *does* differ is below. Every row is from source @970aabf or a production measurement.

| Aspect | MIS (intent INTRADAY) | GTT / CNC (intent DELIVERY) | Where |
|---|---|---|---|
| Strategies (enabled) | 12: first_pullback ×2, gap_fade ×2, gap_go ×2, open_high_breakdown_short, open_low_breakout_long, vwap ×2, range_breakout ×2 (never fire) | 3: positional_momentum_long, positional_sector_rotation, positional_swing_long | strategy YAMLs |
| Receipt, window, de-duplication, queue, pre-screen gates | identical | identical: the delivery scanners are `scanner_type: intraday` and use the same 10:00–15:00 window | receiver; `scan_webhook_map.yaml` |
| Quote, circuit proximity, ten steps, weights, pass mark 60, tier | identical | identical | screener |
| MIS blocklist (shadow) | consulted | skipped (product ≠ MIS) | `secondary_screener.py:565-571` |
| Entry offset | 0.001 | **0.002** | YAML `entry_offset_pct` |
| Re-anchor to a live LTP | gap ×4 and range ×2: yes; first_pullback, open_*, vwap: no | all three: yes | YAML `pullback_wait_enabled` |
| Stop | 0.8 % / 1.0 % / 1.2 % / 1.5 % | **2.0 %** | YAML `sl_pct` |
| Target | 1.5 R | 1.5 R | YAML |
| Concurrent cap per strategy | 2 (gap_*: 3) | 2 | YAML `max_concurrent_positions` |
| Sizing percentages | `risk_per_trade_pct` 0.01 · `max_concentration_pct` 0.10 · `max_position_value_pct` 0.40 | the separate `delivery_*` keys, **same values** | `system_config.yaml:225-259` |
| Leverage (sizing divisor and margin) | **5.0** | **1.0** | `:208`, `:210` |
| Capital bucket | 70 % of total | 30 % of total | `:197-198` |
| Reservation | qty × entry / 5 × 1.05 | qty × entry × 1.05 | `fund_manager.py:562-563` |
| Open-position cap | 5, counting DB rows + reservations + in-flight | **3 CNC**, DB rows only | `risk_engine.py:544-618` |
| Daily-trade cap | 10 | **5 CNC**, DB rows only | `:643-671` |
| Daily loss · consecutive losses · sector | 3 % · 4 (shared) · 40 % observe | 3 % (own key) · 4 (shared) · 40 % observe | `:676-763` |
| One trade per symbol + direction per day | counted within the intraday book | counted within the delivery book | `signal_processor.py:854-856` |
| Product sent | `MIS` | `CNC` (CNC lock: `delivery_enabled: true`) | `product_map`; adapter `:587-602` |
| Entry order | LIMIT via the LIMIT_TRIPLE path | the **same** LIMIT via the same path | placer `:961` |
| Drift top-up inside the placer | effectively unreachable: the slippage guard (22 % of a 0.8–1.5 % stop) refuses first (inference) | reachable in a narrow band, because 22 % of a 2 % stop is wider (inference) | `order_placer.py:1099-1289` |
| Protection, placed after the fill | SL stop-limit (limit = trigger ∓ 0.5 %) + TGT LIMIT, both clamped 2 % inside the circuit band | one OCO **GTT**: SL limit = trigger × 0.97, TGT limit = trigger × 0.995; no circuit clamp; needs a fresh LTP strictly between SL and TGT, ≥ 0.25 % from each | `order_protocol_limit.py:270-525`; `cnc_gtt.py:98-164` |
| Signal alert title | "INTRADAY SIGNAL" | "INTRADAY SIGNAL" (the title does not change) | `signal_processor.py:547` |
| **Measured, 20 days** | 63,797 signals · 170 entry orders | 36,990 signals · 112 entry orders | `signals` |
| **Measured, entry fill rate, all history** | 290 / 576 = **50.3 %** | 84 / 193 = **43.5 %** | `orders` ENTRY |
| Measured, capital-bound rejects (20 days) | `REJECTED_SIZING_CAPITAL` 0 | 63 | `signals` |
| Measured, product actually sent | MIS 576 | CNC 135 · **MIS 58**. All 58 are dated 17-Jun → 10-Jul (the forced-intraday period); none since | `orders` ENTRY |

---

## 8 — THE FIFTEEN STRATEGIES (+ pb01)

### 8.1 Different path, or the same path with different parameters?
**The same path, with different parameters.** No trade-path code branches on a strategy's name. The branches that differ are driven by these fields:
1. `scanner_type: eod`: pb01 only. It never reaches the queue, so none of its keys takes effect (`webhook_receiver.py:562-564`).
2. `intent` (12 intraday vs 3 delivery): bucket, leverage, per-book caps, reservation, product, and GTT-vs-legs after the fill (§7).
3. `pullback_wait_enabled`: whether the M-S1 re-anchor runs (`signal_processor.py:1082`). 10 files say false (re-anchor), 6 say true.
4. `direction`: the same arithmetic with the signs flipped, in pricing, VWAP side, circuit proximity and the contrary-position check.

`entry_method`, `sl_method` and `tgt_method` have the same value in all 16 files, so their branches never diverge.

### 8.2 Every parameter that differs between strategies, and whether the entry path reads it

19 keys differ across the 16 files (not counting `name`, `display_name`, `description`). **Six of them reach a trading decision:**

| Key | Values | Read by the entry path? |
|---|---|---|
| `direction` | LONG ×10 · SHORT ×6 | **yes**: side, price signs, VWAP step, circuit proximity |
| `intent` | INTRADAY ×13 · DELIVERY ×3 | **yes**: §7 |
| `entry_offset_pct` | 0.001 ×13 · 0.002 ×3 (delivery) | **yes**: entry price |
| `sl_pct` | 0.008 vwap ×2 · 0.01 gap_fade ×2, open_* ×2, range ×2, pb01 · 0.012 gap_go ×2 · 0.015 first_pullback ×2 · 0.02 positional ×3 | **yes**: stop, target, slippage tolerance (not qty; concentration binds) |
| `pullback_wait_enabled` | true: first_pullback ×2, open_* ×2, vwap ×2 · false: the other 10 | **yes**: re-anchor on/off |
| `max_concurrent_positions` | 3: gap_* ×4 · 2: the rest | **yes**: H-7 cap |
| `enabled` | false only for pb01 | yes, but pb01 never reaches it |
| `min_volume_surge` | 1.2–2.0 | read, **unreachable** (`avg_volume_20d` is None) |
| `sl_min_pct` / `sl_max_pct` | 0.003/0.05 · delivery 0.005/0.08 | read, **cannot bind** |
| `sl_gap_buffer_pct` | 0.3 in the four gap_* files only | read, **unreachable** (09:15–09:30 only) |
| `entry_end_time` | 15:00 · pb01 11:00 | read, **coincides with the global 15:00**; pb01 unreachable |
| `order_protocol` | CO_PLUS_TGT ×13 · LIMIT_TRIPLE ×3 | **display only**: the placer always uses LIMIT_TRIPLE |
| `pipeline`, `horizon` | INTRADAY/DELIVERY · SAME_DAY/SWING/NEXT_DAY | display only |
| `sl_atr_multiplier`, `tgt_atr_multiplier` | 1.5/2.5 · delivery 2.0/3.0 | **never read** |
| `smart_tgt_enabled` | true ×13 · false ×3 | **never read** |
| `v3_playbook` | true in pb01 only | read by the allocator in enforce mode only (shadow today) |

With the non-deciding keys set aside, the 15 enabled strategies collapse to **13 distinct profiles**. The three positional strategies are identical in everything that decides; they differ only in the unreachable `min_volume_surge` (1.5 / 1.3 / 1.2).

### 8.3 Field inventory, all 16 files
16 files, **565 key instances, 37 distinct keys** (11 files × 35 + 5 × 36; `sl_gap_buffer_pct` only in the 4 gap files, `v3_playbook` only in pb01). I counted these with my own script; the strategy agent's classification of each key rests on readers it traced at 970aabf, and I re-read the load-bearing ones (§1).

| Class | Distinct keys | Instances | Keys |
|---|---:|---:|---|
| Takes effect | 13 | 195 (13 in each enabled file; 0 in pb01) | name, direction, intent, enabled, entry_method, entry_offset_pct, sl_method, sl_pct, tgt_method, tgt_risk_reward, pullback_wait_enabled, max_spread_pct *(in the wrong unit)*, max_concurrent_positions |
| Read but overridden | 3 | 45 | min_score (0 ⇒ global 60) · lot_size (1 ⇒ instrument cache) · entry_start_time (the 10:00 floor wins) |
| Read, unreachable | 5 | 72 | sl_gap_buffer_pct · tgt_pct · min_volume_surge · min_adr_pct · v3_playbook |
| Read, cannot bind | 2 | 30 | sl_min_pct · sl_max_pct |
| Read, coincides | 1 | 15 | entry_end_time |
| Display only | 4 | 64 | display_name · order_protocol · pipeline · horizon |
| Never read | 9 | 144 | description · sl_atr_multiplier · tgt_atr_multiplier · smart_tgt_enabled · smart_tgt_trail_trigger_pct · smart_tgt_trail_step_pct · pullback_wait_tolerance_pct · pullback_wait_timeout_sec · active_days |

⇒ **Defined but never consulted on the trading path: 208 of 565 instances** (13 keys in every file). **Read but neutralised: 162 more.** **Taking effect: 195** (13 per enabled strategy).
- Of those 13 effective keys, five hold the **same value in every file**, so they cannot make one strategy differ from another: `entry_method` LIMIT, `sl_method` FIXED_PCT, `tgt_method` RISK_REWARD, `tgt_risk_reward` 1.5, `max_spread_pct` 0.005. `enabled` is true in every enabled file.
- The six that both differ and take effect are the six in §8.2.
- `pb01_breakout_retest` has no effective key at all.
- The schema also defines four `trailing_sl_*` fields that appear in no YAML; they are unreachable.

### 8.4 What each strategy actually did (production, 20 trading days)

| Strategy | Book | Re-anchor | Signals | Passed screening | Entry orders | Filled |
|---|---|---|---:|---:|---:|---:|
| vwap_bounce_long | MIS | no | 29,575 | 551 (1.86 %) | 59 | 25 |
| positional_sector_rotation | CNC | yes | 22,167 | 432 (1.95 %) | 64 | 24 |
| positional_momentum_long | CNC | yes | 10,478 | 194 (1.85 %) | 36 | 11 |
| first_pullback_long | MIS | no | 9,206 | 165 (1.79 %) | 31 | 22 |
| gap_go_long | MIS | yes | 7,739 | 189 (2.44 %) | 27 | 17 |
| vwap_rejection_short | MIS | no | 6,273 | 72 (1.15 %) | 13 | 4 |
| open_low_breakout_long | MIS | no | 4,416 | 114 (2.58 %) | 12 | 8 |
| positional_swing_long | CNC | yes | 4,345 | 107 (2.46 %) | 12 | 8 |
| first_pullback_short | MIS | no | 2,711 | 45 (1.66 %) | 14 | 1 |
| gap_fade_long | MIS | yes | 1,630 | 27 (1.66 %) | 2 | 1 |
| gap_go_short | MIS | yes | 844 | 13 (1.54 %) | 2 | 1 |
| gap_fade_short | MIS | yes | 746 | 18 (2.41 %) | 7 | 1 |
| open_high_breakdown_short | MIS | no | 657 | 12 (1.83 %) | 3 | 2 |
| range_breakout_long / _short | MIS | yes | 0 | — | — | — |
| **total** | | | **100,787** | **1,939** | **282** | **125** |

Every strategy passes screening at 1.2–2.6 %. The score reads nothing strategy-specific except direction and the (identical) `max_spread_pct`, so it treats every strategy alike.

---

## What could not be measured, and why

1. **The split of the receiver's per-stock rejections** (17,198 on 11-Sep; 447,934 in 20 days) between `DUPLICATE`, `IN_PROCESS`, `EXPIRED`, `INVALID_*` and `REJECTED_EXCLUDED_SYMBOL`. These statuses go back to Chartink only; no row or log line keeps them (§1 S6). There is only the structural evidence: 5–6-minute spacing on 90.8 % of accepted signals.
2. **Which stocks were inside a refused POST.** The 403 is issued before the body is parsed; `webhook_audit` keeps only the payload size.
3. **The exact limit price sent to Kite for any entry.** `orders.price` is NULL for every ENTRY row; `trades.entry_target_price` and `order_execution_log.intended_price` are the unsnapped value; the adapter logs the snap only at DEBUG, and only when it changed the price.
4. **Per-stage latency across all signals.** Only coarse points are stored: `received_at`, the screener `ts`, `trades.signal_to_order_ms` and `order_to_fill_ms`. Per-step latencies sit in `screener_results.latencies` and were not aggregated here. The internal stage timings are shown for one signal (§6).
5. **Whether Kite's quote carries the previous close in `ohlc.close`.** The raw quote is not stored (§5.2, inference).
6. **Why 24 symbols never return a quote.** Not traced.
7. **Any path the retained logs never exercised** (the R:R gate, `REJECTED_PRICE_DRIFT`, the late kill switch, `RESERVE_FAILED`): described from code only.
8. **Log coverage.** Logs before 02-Sep are not on disk, so every log-derived count covers 02–11 Sep. Rejected `signals` rows are pruned after about 60 days (the oldest retained rejected row is 09-Jul); `screener_results` goes back to 15-Jun.
9. **Deferred by 👤 Rama, not attempted:** scanner conditions, scanner lateness and data availability (the 22:45 file's Tasks 1–2).

## Where the source disagreed with the inputs (the source wins)

| The input said | The source / data shows | Where |
|---|---|---|
| 23:10 file §8.3: "gap_fade_long has 37 fields" | 36 top-level keys; 37 is the number of *distinct* keys across all 16 files | §8.3 |
| 23:10 file: "around 15 strategies fire signals" | 16 YAMLs, 15 enabled; **13** produced signals in the last 20 days (range_breakout ×2: 0 ever; pb01 is an EOD scanner that never reaches the order path) | §8.4 |
| 23:10 file §4.2 order "arrived → authenticated → in window → mapped → queued" | auth → scanner name (404) → EOD route → kill switch → queue depth → **then** the window → parse → per-stock checks → queued | §1 S2–S6 |
| 23:10 file §2: "four of them return constants" | true, and in practice a fifth is constant too: `circuit_check` = 1.0 on 175,018 of 175,019, because the proximity reject runs first | §2 |
| 23:10 file §3.3: M-S1 "re-anchors entry, stop, target, quantity and capital on a live LTP" | only for the 10 files with `pullback_wait_enabled: false`; the six pullback-flag strategies keep Chartink's price, and nothing waits for them | §3.3 |
| 23:10 file §3.6: "gate_rr exists but cannot reject" | the V3 `gate_rr` is shadow; separately, the placer has a **live** R:R gate (FIX-136) that cannot fire at 1.5, and the order monitor has a live pending-R:R cancel (FIX-141) that fired 5 times in 8 days | §3.6 |
| 22:45 file: quote bucket "burst 3 / 3 per second" | matches `config/broker_limits.yaml`; the `historical` bucket is 2 / 2 (the forward-shadow docstring says "≤ 3 req/sec") | §1 S15 |
| `signal_processor.py:1074-1075`: "EntryGate already waits for current price" | nothing calls `EntryGate.add()` | §3.3 |
| `webhook_receiver.py:18` "fingerprint dedup at minute precision"; `core/schema.sql:74, :81` "same minute" | `floor(epoch / 300)` — a 5-minute bucket, plus a 300 s in-memory cache | §1 S6 |
| `core/schema.sql:331`: `orders.price` "LIMIT price", under "Order parameters as sent to broker" | NULL on **769 of 769** ENTRY rows | §3.7 |
| `orders/order_placer.py:31-33` (OP9): "order_protocol determined by intent" | constant `LIMIT_TRIPLE` (`:960-961`) | §1 S33 |
| Telegram "ORDER PLACED" text: `Fill: ₹…`, `Smart TGT monitoring: ACTIVE` (`order_placer.py:861-866`) | sent at submission, before any fill; LIMIT_TRIPLE never registers with SmartTgt | §1 S37 |
| `system_config.yaml:347`: `pipeline_timeout_sec` "hard per-signal processing deadline" | declared and validated only (`config_loader.py:568, :602-606`); no runtime reader | §5.3 |
| Strategy YAMLs: `order_protocol: CO_PLUS_TGT` (13 files) | every trade ran `LIMIT_TRIPLE` (955 of 955) | §8.2 |
| Agent-traced, not re-read by me: `schema.sql:583` says `webhook_audit.ts` is the arrival time (it is written at the end of the request) · `scan_webhook_map.yaml:4-6` says strategies are "validated at startup" (the cross-check is not called on the boot path) · `position_sizer.py:295-298` says the entry offset affects margin (it is never passed) · `risk_engine.py:12-13` says `risk_amount` is used (never read) · `fund_manager.py:561` says the SL-M buffer is released by `release_slm_buffer` (no caller) | — | agent findings, evidence folder |

## Observed, not investigated (recorded so they are not lost)

- **RAYMOND, 11-Sep.** The twin received a `gap_go_long` alert for RAYMOND at 14:53 on a day RAYMOND's open (853.85) equalled its circuit-band midpoint (853.85). If that midpoint is the previous close (inference), the stock opened flat, while `gap_go_long`'s own text requires a ≥ 1 % gap-up open. Scanner conditions are deferred.
- **Production's `gap_go_long` made no in-window POST on 11-Sep**, while the twin received gap_go_long alerts that day (SMSPHARMA 10:01, SESHAPAPER 11:14, RAYMOND 14:53).
- **The twin's `signals/webhook_receiver.py` has CRLF line endings** (1,207 CR bytes). With them stripped it is identical to `970aabf`. The other ten decision-path files hashed identical on both VMs.
- **A V3 record's `last_candle_close_ts.day` equals the decision date** (e.g. INDOCO 02-Sep at 14:09). That belongs to the deferred data-availability question.

## Evidence

`docs/audit/SIGNAL_TO_ORDER_EVIDENCE_12-Sep-2026/`, with a `MANIFEST.txt` giving the sha256 of every file:
- every command run in this session, verbatim, extracted from the transcript (`inline_analyses.sh.txt`);
- the analysis scripts (`.py.txt`) and their outputs;
- the four agents' findings files. These are research: every claim this report relies on was re-read in source by me (header list), except the five marked "agent-traced" in the disagreements table.
- The raw data extracts are not copied, because of their size and because they are production data; their sha256 and row counts are in the manifest.

*No recommendations. Rama decides what happens next.*
