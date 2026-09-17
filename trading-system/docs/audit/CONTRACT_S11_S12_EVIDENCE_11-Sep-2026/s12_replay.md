# §12 corpus replay: INDOCO and KOTAKBANK through the current path @970aabf

Pass: 11-Sep-2026, read-only. Code read only from the 970aabf export
(`C:/Users/rama/.claude/jobs/6e6242ba/tmp/src_970aabf`). Production VM queries ran 13:45:47–14:04:45 IST
(VM clock), all SQLite through `file:...?mode=ro`. No project script was run on the VM, no broker/Kite call
was made, and nothing was changed anywhere. Two cases only.

Provenance tags: **[M]** measured by a command in this pass · **[E]** document or chart evidence ·
**[I]** inference from code · **[R]** Rama's own words. Every line reference is pinned `@970aabf`.

---

## 0. Answers

| | (i) outcome: did the gate REJECT the bad trade? | (ii) judgement: did the engine produce the price Rama named? |
|---|---|---|
| **INDOCO** (02-Sep-2026) | **FAIL.** Not rejected. The score gate PASSED it at 62 against 60, then it was placed, filled at 276.83 and stopped out at 271.02 (net −6.52). No live S&R rule exists in the path. | **FAIL.** 287.80 was not produced. The nearest resistance produced was **270.00, below the entry**; the V3 shadow reader found no resistance at all. The contract §12 entry prices 253.65 and 267.36 were not produced either: no entry was proposed. |
| **KOTAKBANK** (22-Jul-2026) | **NOT SCORABLE.** Production has no KOTAKBANK signal on 22-Jul, so there was no trade for any gate to reject. | **NOT PRODUCED.** The engine computed nothing for KOTAKBANK that day. It also has no weekly timeframe, so it cannot produce a weekly level (376.20) by construction. |

- **Does 287.80 appear at all? No level does.** At the decision instant (02-Sep 14:09:26), no resistance level at or above the entry (276.82524) existed in the current path's output, on any timeframe. The closest level produced, 270.00, is 17.80 (6.185 %) below 287.80. Every resistance top was below 276.82524, which is 10.975 or more below 287.80. That gap is wider than any tolerance the detector uses (cluster 0.5 %, merge 0.4 %, entry proximity 1.0 %).
  - 287.80 existed in the decision record only as the quote field `day_high` in the screener snapshot. There, `price_action` used it as the top of the day's range, and the step scored its maximum, 1.0 (§2.5).
- **KOTAKBANK:** on 22-Jul the path saw **neither** the weekly support nor the daily breakdown, because it never ran for the symbol.
  - The weekly support is invisible by construction.
  - The daily inputs exist only for a *placed* candidate, and none was placed.

---

## 1. The current S&R path (common to both cases)

**Timeframes: `day`, `60minute`, `30minute`. No weekly exists anywhere in the path.**
- **Config value:** `config/system_config.yaml:510 @970aabf`, `timeframes: ["day", "60minute", "30minute"]`. The code default is the same: `sr_detector/zone_builder.py:42 @970aabf`.
- **The schema forbids a weekly timeframe.** `core/config_loader.py:1243-1255 @970aabf`, `_validate_timeframes`, allows only `{"day","60minute","30minute","15minute","5minute"}` and raises `"sr_detector.timeframes has unsupported intervals"` otherwise. Test `tests/unit/test_sr_detector_units.py:196-197` asserts that `SRDetectorConfig(timeframes=["weekly"])` is rejected.
- **The fetcher requests only those intervals:** `sr_detector/detector.py:96,168 @970aabf` and `sr_detector/fetch.py:64-67 @970aabf`.
- **No weekly interval string exists** in any non-test `.py` or config YAML at 970aabf (exact search; the only hits were cron cadences, dashboard periods and file modes) [M].
- **The shared resample cannot build a weekly bar either.** `core/candle_math.py:378-382 @970aabf` accepts only "a positive int (minutes) or 'day'".
- **No product or intent split.** `Candidate.intent` (`sr_detector/models.py:142`) is the only `intent|DELIVERY|INTRADAY|product` match in `sr_detector/`, and no module reads it [M]. MIS and DELIVERY/GTT candidates get the same day/60m/30m set.
  - This disagrees with the belief "GTT = 1D + 1W", and the source wins. INDOCO was a DELIVERY/CNC/GTT trade (`config/strategies/positional_sector_rotation.yaml:10` `intent: "DELIVERY"`; orders row product `CNC`; gtt_state row 334457741) and still received day/60m/30m, with no 1W.

**Lookback: 180 days, from the broker, never stored.**
- `config/system_config.yaml:511` sets `lookback_days: 180`, read at `sr_detector/__init__.py:56`. `sr_detector/fetch.py:122-125` computes `from_dt = now - timedelta(days=lb)` and calls `self._fetch_fn(token, from_dt, now, interval)`.
- `main.py:421-438` shows that `fetch_fn` is `market_kite.historical_data(...)`.
- `sr_detector/detector.py:18` states: "No long-term candle storage (fetch → analyse → discard + the session cache)."

**When it runs: only after an order is placed, and it gates nothing.**
- `signal_processor.py:1540-1550` runs "Step 9: Success": it sets `PROCESSED` and then calls `_sr_observe(...)`. The `_sr_observe` docstring (`:628-636`) says "Called ONLY after the order reached placement".
- `sr_detector/detector.py:5-13` describes it as "SHADOW only: no reject, no veto, no entry/SL/TGT change".

**How a level is formed.**
- **Swing pivots,** N=5 on every timeframe: `config/system_config.yaml:513`; no `pivot_n_by_tf` is set.
- **The last N bars can never be pivots:** `sr_detector/pivots.py:42` `for i in range(left, n - right):` (rule SR-P2, `:14-15`).
- **Clustering:** zones cluster at 0.5 % (`zones.py:44-60`, config `:514`) and merge across timeframes at 0.4 % (`confluence.py:80-101`, config `:515`).
- **Votes add score but never create a level.** Prior-day H/L/C, volume nodes and round numbers only add score to zones built from pivots (`confluence.py:128-138`).

**Nearest-level readers.**
- **Detector:** `flags.py:114-122` prefers zones with `band_high >= entry`; if there are none, it falls back to **all** zones.
- **V3 shadow:** `v3_chain/runner.py:356-359` takes resistance with `band_low > entry`, else `None`. `:350-353` takes support as the highest `band_high < entry`.

**What gets recorded.** Only the first 12 zones of each kind, in ascending-price order (`detector.py:98,252-255`; ordering from `confluence.py:87`). The full zone list is never stored.

**Other S&R consumers in the path.**
- **V3 chain,** shadow, "LOG-ONLY (never rejects/delays/alters a live order)" (`system_config.yaml:574`). It uses the same 3 timeframes over 180 days (`:613-614`; `config_loader.py:1477-1479`) and the same zone builder (`main.py:3686`). It keeps only bars that had **closed** before the signal (`v3_chain/truncate.py:71-98`).
- **WAIT_FOR_RETEST pre-placement divert:** off (`system_config.yaml:529`; guard at `signal_processor.py:1042`).
- **Intraday anchors:** off (`system_config.yaml:542`; `detector.py:190`).

**The code that ran on the case dates is the same code** [M].
- The `sr_detector/` package and the `sr_detector:` config block are byte-identical at 52ccb4f, effff24, 39292d3, 2d08436, d3ee69d and 970aabf. The last change to `sr_detector/` is 132e571 (2026-08-01), an ancestor of all of them. STARTUP rows carry no SHA (`system_events` 3811, 02-Sep 08:15:14: `{"mode": "live", "version": "2.0.0"}`), which is why identity was checked across every candidate SHA.
- The score path is also the same: `quality_scorer.py`, `step_executor.py`, `config/scoring_weights.yaml`, `positional_sector_rotation.yaml`, `v3_chain/runner.py` and `v3_chain/truncate.py` are identical at 39292d3 and d3ee69d versus 970aabf.
- `secondary_screener.py` is the one exception: it is identical at 39292d3 and d3ee69d, and its 970aabf diff only adds `_persist` keyword arguments and an evidence observer. No gate line changed.

---

## 2. INDOCO

### 2.1 Case facts (quoted), and where the source disagrees

**The case as the documents state it.**
- **Contract §3 (line 103):** "INDOCO (weekly resistance at 287.80 invisible to a 1H+1D read)".
- **Contract §6 (169-170):** "INDOCO's trigger **was** a huge bullish engulfing and it was still the wrong trade at 281.48."
- **Contract §12 (297, 313):** "INDOCO — 253.65 (good) / 267.36 (best) vs actual ~281.48" and "1D + 1W · weekly ceiling invisible to a 1H+1D read".
- **SPEC_AMENDMENT_1 §1:**
  - Daily: "O 242.00 · H 287.80 · L 241.34 · C 281.48 · +15.44%". Weekly: "O 248.80 · H 287.80 · L 239.00 · C 277.70 · +11.62%".
  - [R] "the position stopped out the following day".
  - §1.1: "from 281.48, stop under the last cleared level 276.83 ⇒ risk ≈ 4.65".

**The chart images** in `C:/Users/rama/Downloads/candles/` [E].
- **`INDOCO-1D-…Curretly late entry [Good entry-253.65, Best entry-267.36, 50-50 Buy].jpg`:**
  - Kite chart, label LFL836, footer **14:43:33 UTC+5:30**, header `O242.00 H287.80 L241.34 C281.48 +37.64 (+15.44%)`.
  - Lines drawn at 281.48 (the live price), **276.83 carrying a position marker "1 · +4.65"**, 267.36 and 253.65.
- **`INDOCO-1W-resistence [...].jpg`:** TradingView, footer **14:51:05 UTC+5:30**, header `O248.80 H287.80 L239.00 C277.70 +28.92 (+11.62%)`, with a line labelled **287.80**.

**The case date is 02-Sep-2026.** The contract gives no date. The source fixes it: the stored 1-minute bars for 02-Sep reproduce the chart's O 242.00 / H 287.80 / L 241.34 exactly [M].

**Disagreements; the source wins in each.**
- **(a) "actual ~281.48".**
  - The system's actual entry was **276.83**: `trades.entry_actual_price`, filled 14:09:28.546 (order 260902170929307, LIMIT BUY CNC, qty 1).
  - 281.48 is the live price at the 14:43:33 chart capture: the 14:43 1-minute bar spans 281.01–281.75 [M].
  - The chart's "+4.65" at 276.83 is the open P&L at that moment (281.48 − 276.83), not a risk.
  - So the 276.83 "level" on the daily chart is the position line, not a structural level.
- **(b) "stopped out the following day".** The exit was the **same day**.
  - The trade recorded exit 271.02 `GTT_EXIT` with `exit_time` 02-Sep 15:19:08.868; the GTT stop trigger was 271.29 (gtt_state `CLEANED` at 15:19:08.869).
  - In the stored bars, the only 1-minute bar after entry whose low is at or below 271.29 is **02-Sep 15:05** (low 270.55) [M].
- **(c) The 287.80 high printed at 13:52 on 02-Sep,** 17 minutes before the entry.
  - The 13:52 1-minute bar: O 277.48, H 287.80, L 277.48, C 284.15, volume 1,750,208 [M].
  - The weekly "H 287.80" is that same print.
- A minor recording inconsistency, not investigated: the ENTRY row in `orders` shows `COMPLETE` with `qty_filled 0` and `avg_fill_price NULL`, while `trades` shows 1 share filled at 276.83.

### 2.2 DB record [M]

**signals, 02-Sep: 60 INDOCO rows.**
- `positional_sector_rotation`: 30 rows (1 `PROCESSED`, 29 `REJECTED_SCORE_48/52/57/59`). `vwap_bounce_long`: 30 rows (all `REJECTED_SCORE_57/59`).
- The traded signal: `sig_cf1906208c494704961cb9024eaf7f3e`, triggered 14:09:00, received 14:09:13.658, `PROCESSED`, trigger_price 278.4, trade `trd_1f87cca5367c42c7934a19200e01f7af`.

**screener_results id 617046** (14:09:20.018): score **62**, tier LOW, status **PASSED**, eligible_score **60**.
- Steps:

  | Step | Value |
  |---|---|
  | volume_surge | 0.0 |
  | vwap_position | 1.0 |
  | atr_filter | 0.0 |
  | rsi_range | 0.5 |
  | price_action | 1.0 |
  | sector_strength | 0.5 |
  | time_of_day | 0.5 |
  | spread_check | **1.0** |
  | circuit_check | 1.0 |
  | signal_age | 1.0 |

- Snapshot:

  | Field | Value |
  |---|---|
  | ltp | 277.41 |
  | bid / ask | 277.40 / 277.41 |
  | open | 242.0 |
  | day_high | **287.8** |
  | day_low | 241.34 |
  | vwap | 274.96 |
  | atr, rsi, sector, prev_close, avg_volume_20d | null |

- The 9 neighbouring INDOCO screener rows between 13:53 and 14:17 all scored 57 (or 52, where `signal_age` was 0.5), and all had `spread_check` 0.0.
- **So the only step separating the one pass from its neighbours is `spread_check`.**

**trades.** Entry target 276.82524; filled 276.83; SL 271.2887352; target 285.1299972; R:R applied 1.5; exit 271.02 `GTT_EXIT`; net −6.52; `CLOSED`.

**gtt_state 334457741.** SL trigger 271.29 (limit 263.15); target trigger 285.14 (limit 283.71); created 14:09:28.580; last verified 15:03:58; `CLEANED` 15:19:08.

**sr_detector_results id 574** (ts 14:09:26.090, `snr-v1`, after the 14:09:25.406 order placement).

| Field | Value |
|---|---|
| intended_entry | 276.82524 |
| nearest_resistance_zone | 270.00–270.00, HIGH, score 6.0, 3 touches, TFs 30minute/60minute/day |
| nearest_support_zone | 258.22–258.22, LOW, score 2.2155, 1 touch, 30minute |
| dist_to_resistance_pct | **−2.46554** (negative means below the entry) |
| dist_to_support_pct | 6.72093 |
| flags | `[]` |
| would_wait_for_retest | 0 |
| proposed_retest_entry | NULL |
| structure_status | OK |
| breakout_volume | 3,981,882 |
| Listed zones (12 lowest of each kind) | resistance 185.00 … 211.97–212.99; support 162.19 … 205.00 |

**V3 record** (production file `data_store/v3/would_be.jsonl`; 1 line for this signal).

| Field | Value |
|---|---|
| as_of | 14:09:19.696 |
| last_candle_close_ts | `day 2026-09-02T00:00`, `60minute 13:15`, `30minute 13:45` |
| nearest_support | 258.22 |
| **nearest_resistance** | **null** |
| gate RR | failed: `"missing S&R zone (no safe SL or TGT)"`, `tgt_zone_edge: null` |
| gate HTF | passed |
| **v3_verdict** | **`WOULD_REJECT_RR`** (log-only) |
| live_score | 62 |

### 2.3 What the current path computed at that moment

- **Inputs:** `day`, `60minute` and `30minute` bars over 2026-03-06 14:09:26 → 2026-09-02 14:09:26 (180 days). No 1W.
- **Output:** the id 574 record above, produced by code byte-identical to 970aabf (§1).

**Where the 287.80 print sat in those inputs** [M]+[I].
- **30m:** the forming 13:45 bar was the detector's **last** bar.
  - Its recorded `breakout_volume` 3,981,882 lies between the stored 1-minute volume sums for 13:45–14:08 (3,959,737) and 13:45–14:09 (4,028,419). `detector.py:238-243` takes the last bar of the 30minute series.
  - That bar's high so far is 287.80.
  - The same bracketing holds for the detector's 10-Sep and 28-Jul rows.
- **60m and day:** the 13:15–14:15 bar and the 02-Sep bar were both still forming at 14:09:26.
  - Whether the broker returned them or not, they would be the last bar (the request ends at `now`, `fetch.py:125`), so the result is the same either way.
- **`pivots.py:42` never turns the last 5 bars into pivots, so 287.80 could not be a swing on any of the three timeframes.**
- **This held for all of 02-Sep:** by 15:30 only 3 more 30m bars and 2 more 60m bars had followed it, fewer than 5.
- **V3's inputs did not contain the print at all.** It keeps only closed bars (`truncate.py:71-98`), and its record's last closes (30m at 13:45, 60m at 13:15, day = 01-Sep) all predate 13:52.
- **The 2025 weekly highs** that Rama's 287.80 line rests on [E, 1W chart] fall before the window start (2026-03-06), and the path fetches no weekly series.

### 2.4 Replay

**A full-fidelity replay cannot be run without a broker fetch.** The detector's input (180 days of day/60m/30m bars) is never stored (`detector.py:18`). What is stored:
- the candle store (`data_store/candles/`): INDOCO 1-minute bars for 28-Jul, 02-Sep and 10-Sep only;
- the `analytics.db` `candles` table: INDOCO 1-minute bars for 6 sessions (28-Jul, 26/27/28-Aug, 02-Sep, 10-Sep).

**Harness run on the PC.** Files: `contract/harness_s12.py` and `contract/harness_s12_output.txt`.
- **Environment:** Python 3.11.9 (`/c/python311/python`), `PYTHONDONTWRITEBYTECODE=1`, cwd `contract/`, `sys.path[0]` = the export. No DB, no network. `find -newer` showed no file written into the export.
- **What it is:** the detector's own `flags` and `pivots` functions, fed recorded values and synthetic inputs. It is not a replay of the input.

| Check | Input | Result |
|---|---|---|
| **[A1]** | The two recorded nearest zones, re-fed | dist −2.465541 / 6.720933, flags `[]`. **This reproduces production's row.** |
| **[A2]** | `_nearest(prefer_above=True)`: {270.00}, then {270.00 + synthetic 287.80} | 270.00, then 287.80. **So a below-entry pick proves no resistance zone had `band_high` ≥ 276.82524.** |
| **[A3]** | Synthetic HIGH resistance zone at 287.80 | nearest resistance 287.80, dist +3.9645 %, **flags `[]`**. The entry sits below `band_low − 1.0 % pad` = 284.922 (`flags.py:138-146`, config `:517`). |
| **[B1]** | Synthetic series with its maximum in the last bar | No pivot. With 3 or 4 bars after it: no pivot. With 5 bars after it: pivot. |

[A3] is a measured property of the current code, not a recommendation: even with 287.80 visible as a HIGH zone, the current flag rule would not have flagged this entry.

### 2.5 Does 287.80 appear at all?

- **As a RESISTANCE level: no.** Two independent readers of the same zone set agree:
  - the detector's fallback picked 270.00, below the entry (`flags.py:117-122` plus harness [A2]);
  - V3 found `nearest_resistance: null` (`runner.py:356-359`).
- **Tolerance.** The closest level is 270.00, 17.80 below 287.80 (6.185 %). All resistance tops are below 276.82524, which is ≥ 10.975 (3.81 % of 287.80) away. The detector's tolerances at 287.80 are cluster 0.5 % ≈ 1.44, merge 0.4 % ≈ 1.15, band buffer 0.1 % and entry proximity 1.0 % ≈ 2.88.
- **As a SUPPORT level: not directly measured.** Neither record lists support bands that straddle or sit above the entry. The listing shows the 12 lowest supports (top 205.00), and V3 gives the highest support top below the entry as 258.22.
- **Elsewhere in the decision: yes, but only as a quote field.**
  - `day_high: 287.8` appears in every INDOCO screener snapshot from 13:53 onward.
  - It is read only by `price_action` (`screening/step_executor.py:318-329`), which computes body % = |ltp − open| / (day_high − day_low).
  - For this signal: (277.41 − 242.0) / (287.8 − 241.34) = 0.762, so the step returns min(1, 1.524) = **1.0**.
  - 287.80 was the denominator of a step that rewarded the long; it was never used as a level or ceiling.

### 2.6 Test (i), outcome-based: **FAIL**

- **The deciding rule** is `screening/secondary_screener.py:316-323 @970aabf`: `effective_min = strategy.min_score if > 0 else score_result.min_pass_score`.
  - `min_score` is 0 (`positional_sector_rotation.yaml:40`), so the threshold falls back to 60 (`config/scoring_weights.yaml:22`).
  - That path is the live one because `v3_hardgate_mode` is `"shadow"` (`scoring_weights.yaml:39`; `secondary_screener.py:96,202,310`).
  - 62 ≥ 60, so the signal was PASSED (`:356-369`), placed, filled and stopped out.
- **No S&R rule is live.** The detector runs after placement and gates nothing; the divert is off (§1).
- **Shadow note:** V3 would have rejected the trade (`WOULD_REJECT_RR`) because it found **no** ceiling (`tgt_zone_edge: null`). That is the inverse of Rama's reason, a ceiling 10.97 above the entry. It is the contract's "rejects for the wrong reason" pattern, but in shadow only.

### 2.7 Test (ii), judgement-based: **FAIL**

- **287.80 was not produced** (§2.5).
- **The contract §12 prices 253.65 and 267.36** were not produced as an entry either: `would_wait_for_retest` 0, `proposed_retest_entry` NULL, V3 `v3_sl`/`v3_tgt`/`v3_rr` null.
- V3 records no support top between 258.22 and 276.8252, so 267.36 is not the top of any support band.
- Whether a resistance-kind band, or a deeper support band, sits at 267.36 or 253.65 cannot be enumerated from the truncated record.

---

## 3. KOTAKBANK

### 3.1 Case facts (quoted)

**The case as the documents state it.**
- **Contract §3 (103-105):** "KOTAKBANK (daily said breakdown, weekly said support, the weekly was right). The weekly corrects in both directions."
- **Contract §12 (314):** "KOTAKBANK — 1D + 1W · weekly support corrected a daily breakdown".
- **Corpus note (lines 50-51):** [R] "KOTAKBANK-1W (As per 1D chart breaks, but weekly chart shows strong support) - So Pullback after break-down".
- The contract names **no KOTAKBANK price and no date.**

**The chart images** in `C:/Users/rama/Downloads/candles/` [E].
- **`KOTAKBANK-1D (refer last 2 candles)-Today break down yesterday's low-awaiting for fall for tommorrow (Today 22-July-2026).jpg`:** header `O384.30 H390.00 L379.35 C379.85 −6.10 (−1.58%)`, cursor date "22 Jul '26".
- **`KOTAKBANK-1W (As per 1D chartbreaks, but weekly chart shows strong support)-So Pullback after break-down (Today 22-July-2026).jpg`:** header `O382.00 H390.00 L376.10 C379.90 −10.05 (−2.58%)`, with a drawn line **labelled 376.20**.

**What that gives.**
- **Case date: 22-Jul-2026** (filenames).
- **The weekly support price Rama drew: 376.20** (the chart line's label). Neither comes from the contract.

**Disagreement.** The corpus note says the 56 files are "all from trades the system actually took" (lines 8-10).
- Production has **0 KOTAKBANK trades ever**.
- The 1D filename describes a prospective short ("awaiting for fall for tommorrow"), not a trade that was taken.

### 3.2 DB record [M]

- **signals:** **0 KOTAKBANK rows on 22-Jul** (0 in 20–24 Jul), against 3,802 rows that day for other symbols.
  - This is not a retention artefact: the table's oldest `received_at` is 2026-06-12.
- **The only KOTAKBANK signals ever:** 100 rows, on 26-Aug (11) and 27-Aug (89). All are LONG strategies (`vwap_bounce_long`, `gap_go_long`, `positional_sector_rotation`) and all are `REJECTED_SCORE_52/57/59`. They are not this case and were not replayed.
- **trades, sr_detector_results and V3 would_be:** 0 KOTAKBANK rows.
- **webhook_audit, 22-Jul:** 200 × 3,458 requests (3,802 signals accepted, 16,444 rejected individually) and 403 × 785 requests (09:16:19–15:29:15).
- **What that table can and cannot show:**
  - The receiver writes **no** `signals` row for a 403 (`webhook_receiver.py:566-583`).
  - It also writes none for EXPIRED / INVALID_PRICE / IN_PROCESS / DUPLICATE outcomes (`:904-945`, `:1014-1015`).
  - `webhook_audit` has no symbol column, so it cannot show whether a KOTAKBANK alert reached the receiver that day.
- **Measured:** no KOTAKBANK alert became a signal on 22-Jul. None reached the screener, placement or the detector.

### 3.3 What the current path computed at that moment

**Nothing.** The detector runs only for a placed candidate (`signal_processor.py:1548-1550`). Had one been placed, it would have read day/60m/30m bars over 2026-01-23 → 2026-07-22, with no 1W.

### 3.4 Replay

**Cannot be replayed without a broker fetch.** The only stored KOTAKBANK candles are 1-minute bars in `analytics.db`: 360 for 26-Aug and 360 for 27-Aug. The candle store has no KOTAKBANK rows.

### 3.5 Weekly support, daily breakdown, either, or neither?

- **On 22-Jul: neither.** The path never ran for KOTAKBANK.
- **The weekly support as a weekly level: impossible by construction.** No weekly timeframe is fetched, resampled or even accepted by the config schema (`config_loader.py:1243-1255`, `fetch.py:64-67`, `candle_math.py:378-382`).
- **376.20 as a coincident day/60m/30m zone** inside the 180-day window: **cannot be measured** without the candles.
- **The daily breakdown:** the inputs to see it exist, but only for a placed short.
  - The day timeframe is fetched.
  - Prior-day H/L/C enter only as confluence votes (`zone_builder.py:78-82`, `confluence.py:132-134`).
  - A short's break below the support just above entry is tested only as the `WEAK_BREAKOUT` / `NO_VOLUME_CONFIRMATION` shadow flags (`flags.py:101-102,125-135,149-175`).

### 3.6 Test (i): **NOT SCORABLE**

No KOTAKBANK signal existed on 22-Jul, so there was nothing to reject. The bad short was not taken, but no gate made that decision.

### 3.7 Test (ii): **NOT PRODUCED**

No level was computed for KOTAKBANK that day. 376.20 is a weekly level, and the path has no weekly timeframe.

---

## 4. Could not be measured, and why

1. **A full-fidelity replay of either case.** The detector's 180-day day/60m/30m input is never stored (`detector.py:18`). The stored candles are listed in §2.4 and §3.4. A replay would need a broker historical fetch, which was not made.
2. **The complete INDOCO zone list.** The detector persists only the 12 lowest-priced zones of each kind (`detector.py:98,252-255`), and V3 persists only the nearest ones. So these are not enumerable:
   - support bands straddling or above the entry;
   - resistance-kind or deeper support bands at 267.36 or 253.65.

   The resistance-above-entry question is still answered, by two readers.
3. **Which SHA ran on 02-Sep.** STARTUP rows carry no SHA. This is neutralised by byte-identity across every candidate SHA (§1).
4. **Whether a KOTAKBANK alert reached the receiver on 22-Jul.** `webhook_audit` has no symbol column, and the rejection paths listed in §3.2 write no row.
5. **Whether 376.20 coincides with a day/60m/30m zone** between 23-Jan and 22-Jul-2026. This needs the candles.
6. **The 2025 weekly-high cluster at 287.80, the KOTAKBANK weekly support history, and "pullback followed".** These exist only in the chart images and discussion files [E]. No stored data covers them.
7. **For INDOCO, whether the broker returned the forming 60m and daily bars.** Only the 30m forming bar is measured (by `breakout_volume` bracketing). Either answer yields no pivot at 287.80.

Not used: `data_store/v3/forward_shadow_fs-v1.jsonl` (60 INDOCO lines on 02-Sep; 0 KOTAKBANK lines on 22-Jul), per the instruction that (ii) does not depend on forward-shadow data. MIDHANI, JAICORP, DALMISUG, SIGNPOST, DATAMATICS and IDEAFORGE were not touched.

**Artefacts** (all under `contract/`): `vm/trades_rows.txt`, `vm/signals_rows.txt`, `vm/sr_rows_summary.txt`, `vm/sr_rows_full_INDOCO.txt`, `vm/schema_cov_screener.txt`, `vm/screener_INDOCO_0902_1350_1420.txt`, `vm/orders_gtt_analytics.txt`, `vm/gtt_startup_v3.txt`, `vm/v3_would_be_INDOCO_0902.jsonl`, `vm/INDOCO_1m_candlestore.csv`, `harness_s12.py`, `harness_s12_output.txt`.
