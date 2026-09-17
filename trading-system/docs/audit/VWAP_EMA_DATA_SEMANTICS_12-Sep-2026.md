# VWAP & 20-DAY EMA — DATA-SEMANTICS MEASUREMENT
### 12-Sep-2026 (Sat) evening IST · READ-ONLY · nothing built, nothing changed

**Scope.** The two questions that gate scanners **X, XI, XII, XIII** (`vwap_rejection_short`,
`vwap_bounce_long`, `first_pullback_short`, `first_pullback_long`). No code, config, YAML,
scanner, schema, threshold, restart or push. No design, no recommendation.

**Measured against** the DEPLOYED tree `/home/ubuntu/systems/trading-system` @ **`970aabf`**
(`git --git-dir=/home/ubuntu/trading-system.git … rev-parse HEAD`; **zero tracked diffs**).
⚠️ **M3** — every line number below holds at `970aabf` ONLY. The local worktree is dirty on
`feat/delivery-config-split`; 5 of 9 cited files differ from deployed, so local line numbers do
**not** apply.

**Sources.** `data_store/trading_system.db` and `data_store/analytics.db`, both opened
`file:…?mode=ro`; `data_store/v3/would_be.jsonl`; `logs/cron-candle-fetch.log`; `crontab -l`.
Every figure below came from a command that was run. Provenance: 🔬 MEASURED · 📄 EVIDENCE ·
💭 INFERENCE · 👤 RAMA'S.

---

## 1. ⭐⭐ §1.2 FIRST — DERIVED VWAP vs THE QUOTE'S VWAP

**The difference is a median of 0.0202 % of the quote's VWAP.** 🔬

`n = 22,253` comparisons · **529 symbol-days** · 5 sessions **07–11 Sep 2026** · 96–116 symbols/day.
Derived = `Σ(typical × volume) / Σ(volume)`, `typical = (H+L+C)/3`, over Kite-historical
**1-minute** bars from 09:15 to the last bar that had **closed** at the capture instant.
Compared against `market_data_snapshot.vwap` captured at that same instant.

| statistic | \|derived − quote\| as % of quote VWAP | in rupees |
|---|---|---|
| median | **0.0202 %** | ₹0.1076 |
| mean | 0.0418 % | ₹0.2657 |
| p75 | 0.0482 % | — |
| p90 | 0.1016 % | — |
| p95 | 0.1448 % | — |
| p99 | 0.3909 % | — |
| **max** | **0.9539 %** | ₹6.4452 |

Signed (derived − quote): mean **+0.0140 %**, median **+0.0115 %** — a small upward bias.

| within | share of comparisons |
|---|---|
| 0.05 % | 75.91 % |
| 0.10 % | 89.69 % |
| 0.25 % | 98.25 % |
| 0.50 % | 99.91 % |
| 1.00 % | **100.00 %** |

⭐ Including the still-forming minute makes it **worse**, not better: median 0.0244 %, max 0.9971 %.

### Per session 🔬
| date | n | median | p90 | p99 | max |
|---|---|---|---|---|---|
| 2026-09-07 | 6,336 | 0.0273 % | 0.0865 % | 0.2070 % | 0.5194 % |
| 2026-09-08 | 3,843 | 0.0150 % | 0.0866 % | 0.2626 % | 0.6315 % |
| 2026-09-09 | 4,237 | 0.0242 % | 0.1161 % | 0.2623 % | 0.4233 % |
| 2026-09-10 | 4,190 | 0.0239 % | 0.1248 % | 0.4080 % | 0.9539 % |
| 2026-09-11 | 3,647 | 0.0149 % | 0.0831 % | 0.2664 % | 0.6795 % |

### Several symbols, as the instruction asked 🔬
| symbol | n | median | p90 | max | median ₹ diff |
|---|---|---|---|---|---|
| RAYMOND | 517 | 0.0079 % | 0.0168 % | 0.6795 % | ₹0.067 |
| MONQ50 | 473 | 0.1184 % | 0.1851 % | 0.3299 % | ₹0.209 |
| MAFANG | 417 | 0.0897 % | 0.1195 % | 0.1555 % | ₹0.204 |
| WHEELS | 401 | 0.0368 % | 0.0941 % | 0.2274 % | ₹0.708 |
| NOVARTIND | 397 | 0.0839 % | 0.0973 % | 0.1700 % | ₹2.002 |
| VENUSPIPES | 348 | 0.0079 % | 0.0206 % | 0.1047 % | ₹0.138 |
| KABRAEXTRU | 313 | 0.0342 % | 0.0404 % | 0.0465 % | ₹0.220 |
| MON100 | 284 | 0.0126 % | 0.0359 % | 0.0578 % | ₹0.042 |
| **BHAGYANGR** | 282 | **0.3929 %** | 0.4096 % | 0.4192 % | ₹1.688 |
| MMP | 262 | 0.0302 % | 0.0436 % | 0.0546 % | ₹0.143 |
| HLEGLAS | 237 | 0.0123 % | 0.0736 % | 0.1072 % | ₹0.045 |
| RAYMONDLSL | 231 | 0.0989 % | 0.1053 % | 0.1075 % | ₹0.696 |

⚠️ **BHAGYANGR carries a ~0.39 % offset on all 282 of its captures** — a per-symbol systematic,
not noise. 🔬 Recorded; cause not established.

### Worked examples — one liquid name per session, actual values 🔬
| symbol | date | time | bars | quote VWAP | derived VWAP | diff ₹ | diff % |
|---|---|---|---|---|---|---|---|
| TALBROAUTO | 2026-09-07 | 11:15 | 120 | 430.74 | 431.01 | +0.266 | +0.0617 % |
| APOLLO | 2026-09-08 | 11:15 | 120 | 416.78 | 416.81 | +0.033 | +0.0078 % |
| MONQ50 | 2026-09-09 | 11:15 | 120 | 224.10 | 224.43 | +0.334 | +0.1489 % |
| KROSS | 2026-09-10 | 11:15 | 120 | 230.38 | 230.39 | +0.013 | +0.0058 % |
| METROBRAND | 2026-09-11 | 11:15 | 120 | 940.09 | 940.70 | +0.608 | +0.0647 % |

### The eight largest disagreements, named 🔬
| symbol | date | time | bars | quote VWAP | derived | diff |
|---|---|---|---|---|---|---|
| SHIVAUM | 2026-09-10 | 14:38 | 133 | 420.23 | 424.24 | **+0.954 %** |
| SHIVAUM | 2026-09-10 | 14:38 | 133 | 420.23 | 424.24 | +0.954 % |
| SHIVAUM | 2026-09-10 | 14:43 | 138 | 420.20 | 423.73 | +0.839 % |
| SHIVAUM | 2026-09-10 | 14:44 | 139 | 420.18 | 423.38 | +0.761 % |
| RAYMOND | 2026-09-11 | 10:45 | 90 | 941.72 | 935.32 | −0.679 % |
| CORDSCABLE | 2026-09-08 | 11:41 | 146 | 325.92 | 323.86 | −0.631 % |
| CORDSCABLE | 2026-09-08 | 11:41 | 146 | 325.77 | 323.86 | −0.586 % |
| MVGJL | 2026-09-07 | 12:27 | 192 | 202.14 | 201.09 | −0.519 % |

### Three controls — ⭐ this check could have come out red 🔬
1. **Volume.** Quote cumulative day volume ÷ summed bar volume: median **1.0032**, p10 1.0005,
   p90 1.0161; **93.79 %** within 2 %, 98.78 % within 5 %. The bars and the quote agree on
   volume, so the time alignment is right.
2. **Day extremes.** Bar-derived running high/low vs the quote's own `day_high`/`day_low`:
   median **0.0000 %** on both; 99.13 % / 99.92 % within 0.10 %. The bars reproduce the quote's
   extremes exactly.
3. **Alignment error.** Screening latency (quote fetch → row written): median **1 ms**, p90 2 ms,
   p99 4 ms, max 93 ms. The stored `ts` *is* the quote instant.

**The +0.0140 % bias.** 💭 Not established. The volume excess is **not** constant in shares
(median 8,918 at 10:00 → 3,614 at 14:00), which tracks the intraday volume U-curve, so it is the
**current forming minute**, not a fixed pre-open block. Two candidates remain — the
`(H+L+C)/3` proxy, and pre-open-auction volume (which the exchange average includes and the
09:15+ bars do not, and which in this `Close > Open` universe sits below the day's VWAP).
Magnitude is ~1½ basis points; no further work done.

### §1.1 — what the quote's `vwap` actually is 🔬
- **Source:** Kite quote field **`average_price`** → `Quote.vwap`, `broker/zerodha_adapter.py:1792`
  → `market_data["vwap"]`, `screening/secondary_screener.py:408`.
- **Presence:** non-null on **22,253 of 23,090** screener rows over the 5 sessions (96.4 %).
  **Every** null row has status `SKIPPED_QUOTE_UNAVAILABLE` and `market_data_snapshot = {}` —
  837 rows, no quote at all rather than a missing field.
- **What it means:** ⭐ the measurement above settles it. It tracks a **session-cumulative VWAP**
  to a median of 0.0202 %. A previous-close average, or anything but session VWAP, would differ
  by whole percent, not by two basis points.
- ⚠️ **Latent, never fired:** the guard is `if data.get("average_price")` — a genuine `0.0`
  would be stored as `None`. 🔬 **0 of 147,473** rows since 01-Aug have `vwap = 0` or `ltp = 0`.

### §1.3 — bar size 🔬 ⭐ a coarser bar is NOT free
| bars | price | median | p90 | p99 | max |
|---|---|---|---|---|---|
| **1-minute** | typical | **0.0202 %** | 0.1016 % | 0.3909 % | 0.9539 % |
| 5-minute | typical | 0.0423 % | 0.1868 % | 0.5214 % | 3.0670 % |
| 15-minute | typical | 0.0922 % | 0.3394 % | 1.0642 % | 4.3209 % |
| 1-minute | close | 0.0470 % | 0.1673 % | 0.4866 % | 0.6885 % |
| 5-minute | close | 0.1157 % | 0.4216 % | 0.9199 % | 4.5739 % |
| 15-minute | close | 0.2645 % | 0.7566 % | 1.9043 % | 6.0344 % |

⇒ 5-minute costs **≈ 2.1×** the 1-minute error; 15-minute **≈ 4.6×**. Typical price beats close
at every bar size. **And it is not an artefact of truncating the in-progress bucket** — measured
only where the capture falls exactly on a bucket boundary, the coarse-vs-1-minute gap is
essentially unchanged: 5 m **0.0317 %** (n=4,181), 15 m **0.0823 %** (n=2,073).

---

## 2. §1.4 — DOES CHARTINK'S "Daily VWAP" MEAN THE SAME LINE?

**The agreement rate for scanner XI (`vwap_bounce_long`) is 97.94 %** (n = 5,689). 🔬

Clause 1 of XI and XIII is `Daily Close Greater than Daily VWAP`; of X and XII,
`Less than` (📄 `D:/system_files/system_manual/Chartink_scanners.v2.txt`,
md5 `8f619972219adfac4eff2010a0b84f55`).

| # | scanner | VWAP clause | n | ltp > vwap | ltp < vwap |
|---|---|---|---|---|---|
| **XI** | `vwap_bounce_long` | **Greater** | 5,689 | **97.94 %** | 1.99 % |
| **XIII** | `first_pullback_long` | **Greater** | 2,272 | **97.98 %** | 1.98 % |
| **X** | `vwap_rejection_short` | **Less** | 1,403 | 2.71 % | **97.22 %** |
| **XII** | `first_pullback_short` | **Less** | 434 | 5.07 % | **94.70 %** |
| VII | `gap_fade_long` | Greater | 506 | 98.22 % | 1.78 % |
| IX | `gap_go_long` | Greater | 1,761 | 99.03 % | 0.97 % |
| XV | `open_low_breakout_long` | Greater | 873 | 98.51 % | 1.49 % |
| I | `positional_swing_long` | Greater | 883 | 97.73 % | 2.15 % |
| VI | `gap_fade_short` | Less | 135 | 0.00 % | 100.00 % |
| VIII | `gap_go_short` | Less | 161 | 1.24 % | 98.14 % |
| XIV | `open_high_breakdown_short` | Less | 172 | 1.16 % | 98.84 % |
| **II** | `positional_sector_rotation` | **NONE** | 5,368 | **73.99 %** | 25.89 % |
| **III** | `positional_momentum_long` | **NONE** | 2,596 | **75.81 %** | 24.08 % |

⭐ **II and III are the control, and they make the result non-vacuous.** Their clause lists carry
**no VWAP term at all** (📄 verified in the scanner text: II clauses 1-7, III clauses 1-8). They
sit at **74–76 % above VWAP** — the unconditional base rate in this bullish-scanned universe.
Every scanner that *does* assert `Greater` sits at **97.7–99.0 %**; every one that asserts `Less`
inverts to **94.7–100 % below**. The test could have returned ~75 % and did not.

### The limits, stated
- **The capture is not the scan minute.** Lag from Chartink's `triggered_at` to capture: median
  **18.3 s**, p90 28.0 s, p99 35.9 s, max 48.1 s. 🔬 Price moves in that window, so some of the
  2 % disagreement is latency, not definition.
- **Chartink's own VWAP value is never recorded** — only its pass/fail. This test can detect a
  definition difference only if it is large enough to **flip the inequality**. A systematic
  offset smaller than the typical close-to-VWAP distance would pass unseen.
- The population is **filtered by the clause itself**; this is an agreement rate, not an
  independent sample.
- **Nothing is concluded beyond the rate.**

---

## 3. ⭐ §2.2 — HOW FAR THE 20-DAY EMA MOVES IN A SESSION

**Largest observed: 3.3152 % of price. Median 0.5818 %. It does not collapse the problem.** 🔬

`k = 2/(20+1) = 0.095238`. The identity is exact:
`EMA_live(t) = k·P(t) + (1−k)·EMA_{D−1}` ⇒ **within-session movement = k × intraday range**,
which needs no 20-day history to measure.

### Every symbol-day in the store (n = 4,339) 🔬
| | median | p90 | p99 | **MAX** |
|---|---|---|---|---|
| EMA movement, % of price | **0.5818 %** | 1.1518 % | 1.7771 % | **3.3152 %** |
| underlying intraday range | 6.11 % | 12.09 % | 18.66 % | 34.81 % |

| EMA moves ≤ | share of symbol-days |
|---|---|
| 0.05 % | 0.16 % |
| 0.10 % | 0.78 % |
| 0.25 % | 6.68 % |
| 0.50 % | 38.58 % |
| 1.00 % | 85.02 % |

### Restricted to the symbol-days X/XI/XII/XIII actually fired on 🔬
| scanner | n | median | p90 | p99 | MAX |
|---|---|---|---|---|---|
| `first_pullback_long` (XIII) | 1,138 | 0.6376 % | 1.2845 % | 1.8787 % | 2.4486 % |
| `first_pullback_short` (XII) | 529 | 0.5855 % | 1.2245 % | 2.1337 % | **3.3152 %** |
| `vwap_bounce_long` (XI) | 3,089 | 0.6116 % | 1.1869 % | 1.7996 % | **3.3152 %** |
| `vwap_rejection_short` (X) | 1,023 | 0.4992 % | 1.0701 % | 1.8847 % | **3.3152 %** |

### The largest cases, named 🔬
| symbol | date | high | low | EMA movement |
|---|---|---|---|---|
| WEL | 2026-08-27 | 179.20 | 124.74 | **3.3152 %** |
| DJML | 2026-08-24 | 115.25 | 86.92 | 2.6689 % |
| PANAMAPET | 2026-08-12 | 599.60 | 456.45 | 2.5767 % |
| TURTLEMINT | 2026-08-17 | 157.68 | 122.00 | 2.4486 % |
| BODALCHEM | 2026-09-02 | 151.89 | 119.00 | 2.3331 % |
| STYLAMIND | 2026-07-22 | 4150.00 | 3288.30 | 2.2789 % |

### ⭐ Where the instruction's estimate parts company with the data
The arithmetic in the instruction file is right — *"a 2 % intraday move should shift the line by
roughly 0.19 %"* is exactly `k × 2 %`. **The input is wrong for this universe.** 🔬 The MEASURED
median intraday range across the scanner universe is **6.11 %**, not 2 %. So the median shift is
**0.58–0.64 %**, about **3×** the estimate, and the largest is **3.32 %** — roughly 17× it.

### Measured directly, where a real 20-day daily series exists 🔬
Only the 10 index instruments have ≥ 21 daily observations in the store (see §4). 210 index-days:

| | median | p90 | p99 | MAX |
|---|---|---|---|---|
| within-session movement | 0.0921 % | 0.3600 % | 1.5769 % | 2.3907 % |
| offset: EMA including today's close vs the fixed line | 0.1110 % | 0.3405 % | 0.8455 % | **1.0171 %** |

By instrument — the equity indices are calm and INDIA VIX is the outlier:

| index | days | median | p90 | MAX |
|---|---|---|---|---|
| NIFTY 50 | 41 | 0.0547 % | 0.0863 % | 0.1071 % |
| NIFTY BANK | 41 | 0.0701 % | 0.1290 % | 0.1603 % |
| NIFTY FIN SERVICE | 41 | 0.0740 % | 0.1096 % | 0.1702 % |
| NIFTY ENERGY | 41 | 0.0744 % | 0.1154 % | 0.1455 % |
| NIFTY PHARMA | 41 | 0.0970 % | 0.1405 % | 0.1719 % |
| NIFTY FMCG | 41 | 0.1003 % | 0.1413 % | 0.2717 % |
| NIFTY AUTO | 41 | 0.1005 % | 0.2053 % | 0.2807 % |
| NIFTY METAL | 41 | 0.1144 % | 0.1800 % | 0.2139 % |
| NIFTY IT | 41 | 0.1590 % | 0.2513 % | 0.2800 % |
| INDIA VIX | 41 | 0.8766 % | 1.5986 % | 2.4470 % |

⚠️ **Two different numbers, do not conflate them.** *Movement* is how far the line travels within
the session (`k ×` range). *Offset* is how far the line including today sits from the
completed-bar line (`k × (P − EMA_{D−1})`). Treating the completed-bar EMA as a fixed proxy
incurs the **offset**, which is the larger of the two on the indices.

### §2.1 — does the system compute this EMA? **No.** 🔬
| where | what it computes | timeframe | live @ `970aabf`? |
|---|---|---|---|
| `core/candle_math.py:165` `ema_series` / `:184` `ema` | pure helper, period is a parameter | — | library only |
| `regime/engine.py:145-146` | EMA **50** and **200** | **daily**, on the *index* | `regime.enabled: false` — not running |
| `v3_chain/runner.py:201`, `pb01_runner.py:148` | `ema(closes(c60), htf_ema_period=20)` | **60-minute** | ✅ `v3_chain_mode: "shadow"` — running, log-only |

⭐ `htf_ema_period: 20` is a **20-period 60-minute** EMA ≈ 3 sessions — **not** the 20-**day**
EMA that XII/XIII are defined against. 📄 Running: 49 signals enriched on 11-Sep
(`v3_chain_runner: acted 49 | active`), `gates.HTF.evidence` carries `{close, ema}` per signal.
⇒ **The daily EMA20 the scanners are written against is computed nowhere in this system.**

---

## 4. §2.3 — THE EMA AGREEMENT RATE: **NOT MEASURED**

**No 20-day daily-close series exists for any traded stock in any stored source.** 🔬

| candidate source | what it holds |
|---|---|
| `analytics.db.candles` | 59 trading days, 1,304 symbols — but **only 10 symbols have ≥ 21 days**, and all 10 are indices. **1,280 of 1,304 have ≤ 9 days.** |
| `daily_symbol_stats` (has `prev_close`) | **0 rows** |
| Kite `day` bars | fetched live by `sr_detector` / `regime`, **never persisted** |

The store only ever fetches a symbol's minute bars on days that symbol produced signals
(`fetch_daily_candles._get_traded_symbols` → PROCESSED signals), so the daily series is
structurally sparse. ⇒ The test needs one `day`-interval historical call per symbol — i.e. a
broker token (§6).

---

## 5. §3 — WHAT THE INTRADAY BARS ACTUALLY GIVE

### §3.1 coverage 🔬
**After the session — confirmed.** `scripts/fetch_daily_candles.py:187` requests
`interval="minute"`, `from 09:00`, `to 15:31`, under cron **`40 15 * * 1-5`**.
Across **all 59 trading days** in the store: **first bar exactly `09:15:00`, last bar exactly
`15:29:00`, max 375 bars per symbol-day** — zero days deviate. ⭐ Coverage starts at **09:15**
even though 09:00 was requested.

**During the session — confirmed.** `sr_detector.enabled: true`; `sr_detector/fetch.py:125`
requests `from = now − 180 d` to **`to = now`** for `day`/`60minute`/`30minute`.
🔬 **628 OK vs 46 FETCH_FAILED** over 62 dates, succeeding at request times from **10:00 to 14:59**.
⭐ Stronger: in **2,389 of 2,389** V3 shadow records (15-Jul → 11-Sep), the last 30-minute bar
that had *closed* at the decision instant was **exactly** the latest 09:15-anchored 30-minute grid
point ≤ that instant — which requires the API to have supplied **today's** bars up to that point.

> **CORRECTION — a field that looks like an answer and is not.**
> `would_be.jsonl.last_candle_close_ts` is **not** API recency. `v3_chain/truncate.py` defines
> `close_ts = bar start + interval` (daily: the next midnight) and deliberately drops any bar
> still forming at the decision instant — the anti-lookahead guard. 🔬 **0 of 2,389** records used
> today's daily bar, which is *correct behaviour* and says nothing about what the API offers.
> An earlier read of this field as "76 % of in-session fetches returned today's daily bar" was
> **wrong** and is withdrawn.

### §3.2 count and latency 🔬
- **375 one-minute bars** per symbol-day (09:15:00 … 15:29:00, labelled by **open** time).
- **Latency:** 18–22 `historical_data` calls of 375 bars each, **plus** the
  `kite.instruments("NSE")` map load, complete in **6.88–9.38 s** wall clock (`cron_heartbeat`,
  04–11 Sep, all `SUCCESS`). Of that, `0.35 s × n` is a mandated sleep ⇒ net ≈ **1.5–1.8 s** for
  18–22 calls. That is an upper bound per call: it still carries the instrument-map load and the
  DB inserts.
- **Recency of the last bar relative to request time: NOT MEASURED** — see §6.

### §3.3 volume — ⭐ **present, real, and the project's own note is about a different source** 🔬
- **1,760,221** bars in `analytics.db.candles`; **1,510,336 (85.8 %) carry volume > 0.**
- **Every zero is explained:** 10 index instruments × 375 bars/day (indices carry no volume by
  construction — `index_universe.yaml` says so, and `fetch_daily_candles.py:74` documents it),
  plus genuine no-trade minutes in illiquid names (e.g. SARLAPOLY 169 of 375 on 11-Sep).
- **Control:** summed bar volume reproduces the quote's own cumulative day volume to a median
  ratio of **1.0032**.
- ⭐ **The "volume = 0 always" deferred note is correct — about the OTHER candle path.**
  `data/candle_store.py` builds bars from LTP ticks; `data/live_feed.py:191` subscribes
  **`MODE_LTP` only**, which carries no `volume_traded` (`:299`), so the accumulator adds 0
  (`candle_store.py:63`). 🔬 **0 of 1,760,221 rows in the table came from that writer** — every
  row carries the space-separated `ts` of the historical fetcher, none the `isoformat()` of
  `main.py:3927`'s `_persist_candle`. (SYSTEM_MAP records this at 0 of 275,129 on 25-Jul; it is
  now 0 of 1,760,221.) ⇒ **The note must never be applied to the `candles` table.**
- ⚠️ **M-D1 still stands and this measurement re-confirms it.** `candle_store.py:63` does
  `self.volume += volume`, where `volume` is Kite's **cumulative** `volume_traded`. It is latent
  only because MODE_LTP delivers nothing. A MODE_FULL flip would start writing a
  tick-count-weighted sum into that column — neither cumulative nor per-minute.

---

## 6. WHAT COULD NOT BE MEASURED, AND WHY

| # | question | why not |
|---|---|---|
| 1 | §2.3 — EMA20 agreement rate for XIII | No 20-day daily-close series for any traded stock (§4). Needs one `day`-interval call per symbol. |
| 2 | §3.2 — how stale the last bar is vs request time | The only field that looked like it answered this measures the V3 chain's own truncation (§5). Needs one live in-session call. |
| 3 | Whether the API returns the still-**forming** intraday bar | Same — the production caller deliberately discards it, so production evidence cannot show it. |
| 4 | Chartink's own VWAP / EMA **values** at its scan minute | Never recorded anywhere; only the indirect pass/fail test of §2 exists. |
| 5 | Cause of the +0.0140 % VWAP bias and of BHAGYANGR's 0.39 % offset | Two candidates each; not pursued. |

⭐ **All of 1–3 need a Kite access token, and there is none.**
🔬 `data_store/session/zerodha_token.json` **does not exist** — cron `0 5 * * *` deletes it daily
(the session dir's mtime is 12-Sep **05:00**), and the refresh cron `15 8 * * 1-5` is **Mon–Fri**,
so nothing recreates it on a Saturday. Obtaining one means running a **live broker login** with
credentials and writing a session file.

**I did not do that, and I am not asking to inside this pass.** The instruction is READ-ONLY;
⭐ Monday 08:15 is Batch 1's first production load and outranks this; and the token path touches
that boot. 👤 Rama's call, not mine.

---

## 7. §4 — THE THREE DESIGN POSITIONS

📄 Recorded verbatim from the instruction file as **👤 Rama's positions**, for completeness of the
record. Nothing in this pass tests, supports or contradicts them, and I offer no view.

1. **One activation rule for every setup** — the start of the CURRENT UNBROKEN EPISODE; breakout
   and pullback differ only in what bounds the episode. One rule, sixteen inputs.
2. **Activation, freshness and extension stay three numbers and one gate** — three distinct facts,
   one question ("am I early or late?"), one verdict, one reject reason.
3. **The secondary must not re-implement the scanner** — the adapter's invalidation test is small
   and derived; not a Python re-run of the scan.

---

## 8. PROVENANCE

- **DB reads:** `sqlite3 -readonly` / `file:…?mode=ro` on the VM. Nothing written to either DB.
- **Harnesses:** six throwaway Python scripts piped to the VM over **ssh stdin** — no file was
  created in the deployed tree. Local copies in this session's scratchpad.
- **Local worktree:** `feat/delivery-config-split`, dirty, `6d24a83`. Untouched by this pass.
- **Deployed:** `970aabf`, zero tracked diffs, service `inactive` (Saturday — correct, down by design).
- ⚠️ The bars used for §1 are the **production store's** Kite-historical bars (already fetched by
  the 15:40 cron through the very same API call the instruction describes), not a fresh call made
  today. That is why n = 22,253 rather than a handful — and why no token was needed.
