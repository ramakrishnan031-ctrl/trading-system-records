# THE TECHNICAL DECISION CONTRACT — VS CODE CROSS-CHECK
## PART TWO executed · READ-ONLY · 05-Sep-2026

**Repo SHA at measurement:** `6d24a83` (branch `feat/delivery-config-split`)
**VM:** `trading-vm`, deployed tree `/home/ubuntu/systems/trading-system`
**Method:** every SQLite opened `sqlite3.connect("file:<path>?mode=ro", uri=True)`. No script under
`scripts/` executed. Nothing written to the VM. No code, config, YAML or scanner changed. No commit,
no push, no restart. 26 agents, 804 tool calls.

**Provenance labels:** MEASURED (run this session) · EVIDENCE (a file/image says it) · INFERENCE.

> **Line-number caveat.** `signals/signal_processor.py`, `orders/order_placer.py`,
> `config/system_config.yaml` and 7 other files are **dirty in the working tree**. Several agents
> initially cited working-tree line numbers under a `6d24a83` header. Adversarial verification caught
> this; **every line number below is the HEAD `6d24a83` number**, re-derived via `git show 6d24a83:<file>`.

---

# §10 — THE HISTORICAL COUNTERFACTUAL GATE

## 10.0 Headline

| | |
|---|---|
| Gate executable **as written** | **NO** — 0 of 3 operands exist in the named population |
| Population §10 names | 154,408 forward-shadow records from 14-Jul |
| Fraction evaluable | **0.00%** |
| Largest faithful substitute **with outcomes** | **N = 115** |
| Coverage of the target population | **0.07%**, survivorship-filtered twice |
| Rejected-cohort verdict | **MIXED** |
| Recommendation | **CALIBRATE_FIRST** · confidence **LOW** |

## 10.1 The gate as written is not executable — 0 of 3 operands

MEASURED: a full field-union scan of every line of `data_store/v3/forward_shadow_fs-v1.jsonl`
(91,518,314 B, **157,875 records, 0 unparseable — not sampled**) returns **exactly one key-shape**
and **exactly 20 fields**, each on 100.0% of rows:

```
date  signal_id  symbol  strategy  side  ts  old_score  old_band  ms4_score  ms4_band
ms4_stats_ok  decision  reject_reason  sim_R  realized_pnl  computed_at
method_version  git_commit  scoring_weights_sha  system_config_sha
```

**No entry price. No reference/S&R level. No ATR. No stop. No target.**
`L3 = |entry − reference_level| / ATR_tf` is not computable for a single one of the 154,408 target
records, and neither is structural R:R.

ATR is absent everywhere, confirmed four independent ways:

| Check | Result |
|---|---|
| `screener_results.market_data_snapshot["atr"]` (all 173,592 parsed) | key present on 165,672 (95.4%), **non-null 0 / 173,592** |
| `daily_symbol_stats` — the only table with an `atr14` column | **0 rows** |
| Any DB column named `atr*` across 46 tables | none other exists |
| `grep -c "atr30"` over the VM logs | **0** |

INFERENCE: ATR30 was computed live at decision time, consumed by `gate_rr`, and never persisted.

**Missing data is not a pass.** §10 as written is recorded NOT EXECUTABLE.

## 10.2 The substitute — and the correction that matters

`data_store/v3/would_be.jsonl` (2,228 records, 15-Jul → 04-Sep) is **far richer** than the file §10
names: it carries `live_entry`, `nearest_support`, `nearest_resistance`, `v3_sl`, `v3_tgt`, `v3_rr`
on 100% of rows. ATR30 is recoverable algebraically by inverting `screening/hard_gate.py:271`:

```python
buffer = (float(sl_buffer_atr_mult) * float(atr30)) if atr30 else 0.0
```

MEASURED (rebuilt independently by me, joined to `trades.net_pnl`):
**N = 115, 49W / 66L, baseline 42.61%.**

**The first sweep used the wrong reference.** MEASURED: the identity
`risk == ATR30 × (L3_slEdge + 0.20)` holds with **0 violations of 115** — so what was swept was
*normalised stop distance*, algebraically coupled to `v3_rr`. Its sweep is flat (p 0.16–1.00, sign flips).

Re-swept against the **opposing level** instead:

| t | rejected N | rej win% | retained N | ret win% | Fisher p |
|---|---|---|---|---|---|
| 0.25 | 99 | 37.37 | 16 | 75.00 | 0.0063 |
| 0.30 | 94 | 36.17 | 21 | 71.43 | 0.0062 |
| 0.40 | 87 | 35.63 | 28 | 64.29 | 0.0091 |
| **0.50** | **82** | **34.15** | **33** | **63.64** | **0.0063** |
| 0.75 | 58 | 34.48 | 57 | 50.88 | 0.0911 |
| 1.00 | 46 | 32.61 | 69 | 49.28 | 0.0864 |
| 1.50 | 31 | 29.03 | 84 | 47.62 | 0.0907 |
| 2.00–3.00 | 12–16 | 31.3–33.3 | 99–103 | 43.7–44.4 | 0.42–0.55 |

MEASURED: **no sign flip at any threshold.** Robustness at t=0.50: leave-one-day-out **36/36 folds held**;
leave-one-strategy-out **13/13 held**; LONG (N=90) p=0.0173; SHORT (N=25) same direction, p=0.18.
Permutation family-wise p over the best of 10 thresholds (2,000 draws) = **0.0345** — survives multiplicity.

## 10.3 But it is NOT L3, and the direction contradicts G4

MEASURED: in **115 of 115** rows the reference sits **ahead** of entry — it is the **ceiling** (long) /
floor (short), **never the broken level**.

`sr_detector/flags.py:65` persists the resistance *ahead*:
```python
res = _nearest(resistances, entry, prefer_above=True)
```
`_broken_zone` (`flags.py:125`) computes the level the contract actually means and is **never persisted** —
it feeds only the `WEAK_BREAKOUT` / `NO_VOLUME_CONFIRMATION` flags.

**The contract's L3 (lateness from the broken level) is NOT MEASURABLE on any stored data.**
The axis that *is* measurable is **G4's**, and on it the data runs **counter to G4**: entries **closer**
to the opposing level won more (63.6% vs 34.1%).

## 10.4 Decomposition — most of the strength is volatility, not distance

| Quintile (low→high) | Q1 | Q2 | Q3 | Q4 | Q5 | Q1vQ5 p |
|---|---|---|---|---|---|---|
| ATR-normalised distance | 69.6% | 30.4% | 47.8% | 39.1% | 26.1% | 0.0072 |
| RAW % distance (no ATR) | 65.2% | 34.8% | 47.8% | 39.1% | 26.1% | 0.0169 |
| ATR as % of price (volatility alone) | 21.7% | 43.5% | 43.5% | 39.1% | 65.2% | 0.0067 |

2x2 at the medians (distance 1.021%, ATR 1.332% of price):

| | vol LOW | vol HIGH |
|---|---|---|
| **dist LOW** | 37.0% (n=27) | **54.8% (n=31)** |
| **dist HIGH** | **29.0% (n=31)** | 50.0% (n=26) |

Both axes carry signal and are roughly independent, but **volatility carries more of it**
(17.8 and 21.0 pp) than raw distance (8.0 and 4.8 pp).

## 10.5 Structural R:R — the axis is vacuous

MEASURED: `tgt_method: "RISK_REWARD"` on **16/16** strategy YAMLs and `tgt_risk_reward: 1.5` on **16/16**.
Combined with §11.4 (`sl_pct` is the sole SL determinant), **every target in the system is
`entry ± 1.5 × sl_pct × entry`** — fully determined by one config number, with **no market input at any point**.

MEASURED: on the live/planned R:R axis (N=337, baseline 39.17%) the rejected cohort's win rate moves by at
most **0.21 pp** across thresholds 1.5 → 2.5. The variable takes 3 values (1.5 on 743/856 trades).
**An R:R gate cannot discriminate on historical data because R:R is a config constant.**

## 10.6 §10's verdict

**MIXED → CALIBRATE_FIRST, LOW confidence** — but not for the reason first offered.
Not because no separation exists (a robust one does, family-wise p=0.0345), but because
the separating variable **is not the one §10 names**, is **partly volatility**, and the axis it
does measure points **against** G4 rather than for it.

**§10's own question — "are the trades the gate would reject mostly losers?" — remains UNANSWERABLE
for L3**, because the broken level is never persisted. The contract's central assumption is
neither confirmed nor contradicted. It was not tested, because it cannot be, on stored data.

---

# §11 — THE SOURCE INVENTORY

## §11.1 — `pullback_wait_*`: REAL or DEAD? → SPLIT, and the live one is INVERTED

| Key | Production readers | Verdict |
|---|---|---|
| `pullback_wait_enabled` | **1** — `signals/signal_processor.py:979`, read as `not …` | **LIVE, INVERTED** |
| `pullback_wait_tolerance_pct` | **0** (schema + validator only; `entry_gate.py:69` is a *comment*) | **DEAD** |
| `pullback_wait_timeout_sec` | **0** (schema + validator only; `entry_gate.py:70` is a *comment*) | **DEAD** |

The only reader, at HEAD `6d24a83`:
```python
signals/signal_processor.py:979
    if not strategy_obj.pullback_wait_enabled and self._quote_fn is not None:
```
It gates the FIX-067 **fresh-LTP re-anchor**, not a wait. So `true` means: **skip the fresh quote and
place immediately off the STALE webhook `trigger_price`** — the opposite of the name.
6 of 16 strategies set it `true`, covering **495 of 856 trades (57.8%)**.

The premise in the code comment (`signal_processor.py:975-976`) — *"Pullback strategies skip this
(EntryGate already waits for current price)"* — is **false**:

| Evidence channel | Result |
|---|---|
| `gate_state` table (the WatchEntry store) | **0 rows** |
| `retest_state` table | **0 rows** |
| `signals.status GLOB 'GATE_*' OR 'RETEST_*'` | **0 of 208,946** |
| `grep -c "EntryGate.add"` across 14 log files, 27-Aug→04-Sep | **0** |
| `GATE_WAITING` / `GATE_RELEASED` / `PRICE_HIT` | **0** |
| effect-telemetry census | `acted 0 | dormant` on **10 of 10 boots** |
| `EntryGate started` / `stopped` | 10 x started, 10 x stopped, **0 admits** |

**The pullback wait has never fired. §5's WATCHING state is not half-built — it is built, wired,
polling, and starved.**

## §11.2 — `gap_fade_long.yaml` field inventory

MEASURED: **36 top-level keys** (40 leaf scalars, 41 schema fields) — **not 37**; no enumeration
produces 37. Of the 36: **15 read-and-effective**, **9 dead** (no reader anywhere), **12 read but
neutralised** (hardcoded constant, global floor, unit mismatch, or unreachable branch). A further
**5 schema fields the YAML omits** get silent defaults that *do* have live effect.

## §11.3 — `min_score` and the enforcement path

MEASURED: all **16/16** YAMLs carry `min_score: 0`, and **0 is a "use-global" sentinel, not a floor** —
the per-strategy knob is inert everywhere. The only binding floor is
`config/scoring_weights.yaml → min_pass_score: 60`, enforced once at:
```python
screening/secondary_screener.py:338-343
    if total_score < effective_min:
```
MEASURED: it is the dominant rejection layer — **142,224 of 154,726 signals rejected (91.92%)**,
71.6% of them within 3 points of the floor.

**The score-57 pile-up is a floating-point artifact.** MEASURED: 71,792 of 75,385 score-57 rows (95.2%)
carry one identical step vector whose true score is **57.5**. At `screening/quality_scorer.py:113-114`:
```python
final_score = (total_achieved / total_weights_present) * 100.0
total_score: int = min(100, int(round(final_score)))
```
MEASURED: `(57.5/100)*100.0 = 57.49999999999999` → `int(round(...))` = **57**, whereas `round(57.5)` = **58**.
**One full point is lost to float error on 71,792 rows.**

**The screener's real admission rule has nothing to do with the setup.** MEASURED across the 60-era:
`time_of_day == 1.0 OR spread_check == 1.0` is a **NECESSARY** condition with **0 violations in 3,464
passes**; the partition is exact and residual-free — **2,591 (74.8%)** arrived in the 15-minute window
**10:00:00–10:14:59 IST**, and the other **873 (25.2%)** all had `spread_check == 1.0`.
Of the 10 scoring steps, 3 are permanently 0.0, 2 permanently 0.5, and the rest sit at 1.0 on the modal
path. **Nothing about price structure enters the admission decision.**

Caveat: this is a necessary, not sufficient, condition — 1,104 rejections met it and still failed on
another live step. Scope is the 60-era only; the 55-era (13,082 rows) was not re-derived.

## §11.4 — Strategy-wise SL: there is no fallback hierarchy

MEASURED: all **16/16** strategies declare `sl_method: FIXED_PCT` and nothing else. There is only a
one-way degradation ladder (ATR → warn → FIXED_PCT), because **ATR is unimplemented**:
`sl_atr_multiplier` has zero consumers. No structural level ever enters the initial-SL computation.

```python
signals/signal_processor.py:1640   if sl_method == "ATR":
signals/signal_processor.py:1647       ...warn "not yet implemented"
signals/signal_processor.py:1649       sl_method = "FIXED_PCT"
signals/signal_processor.py:1675   sl_price = entry * (1.0 - sl_pct)
```

**The configured `sl_pct` IS the enforced SL:** MEASURED — 771/856 live trades match bit-exactly, all
856 within 1.07e-4, and **313/313 broker MIS SL legs carry `trigger_price` exactly equal to
`trades.sl_initial`**.

The contract's §8 note is confirmed and strengthened: `sl_pct: 0.01` is configuration evidence only,
and it is the *sole* determinant. **No clean fallback hierarchy exists. I have not invented one.**

## §11.5 — The three scanner findings: all three CONFIRMED

| Claim | Verdict | Evidence |
|---|---|---|
| I vs XV byte-identical | **TRUE** | identical condition-set hash `214c887757`; all 10 conditions verbatim; the only duplicate among 16 |
| IV/V `Max(15)` offset | **TRUE — and worse: unsatisfiable** | II, III, XVI use `1 day ago Max(N, …)`. IV/V use bare `Daily Max(15, …)` / `Min(15, …)`, which include today's bar, so `Close > Max(15,High)` and `Close < Min(15,Low)` can never be true (High >= Close >= Low) |
| XVI has no retest condition | **TRUE** | 8 conditions, pure breakout, no retest/pullback/support term despite the name |

**Live hit counts for IV and V: ZERO.** MEASURED: `range_breakout_long` and `range_breakout_short`
produced **0 of 208,946 signals** and **0 of 223,484 inbound webhooks** (12-Jun → 04-Sep), while
`enabled: true`.

MEASURED: they are **fully wired and armed system-side** — present in the 404 allowlist, in the
direction registry, and in the live 04-Sep 08:15:42 boot's `will_trade` list of 15 — yet have never
received a POST. The absence is unambiguously **Chartink-side**. Whether the scanner
exists-but-never-matches or was never created **cannot be determined without Rama's Chartink account**.

MEASURED: **I and XV are the same scanner deliberately dual-wired to two books** — 34 of 52 common days
produce byte-identical symbol sets; on 04-Sep both returned exactly the same 14 symbols.

> **Consequence for the contract.** F1 LEVEL BREAK is specified as **II · IV · V · XVI**.
> IV and V have never fired; XVI is `enabled: false`.
> **F1's live coverage rests on II alone** — a *delivery* scanner.

## §11.6 — Scanner configuration: §5's liveness premise HOLDS

MEASURED: the Chartink UI settings are **not recorded anywhere in the repo** — no schema field for
frequency, after-trigger, or duplicate mode exists. The behaviour they produce is measured decisively:

| Measurement | Result |
|---|---|
| POSTs across 257 scanner-days | **79,479** |
| Gaps in 45–75 s | **98.3%** |
| Minutes carrying two POSTs | **0** |
| Consecutive-minute symbol carryover | **97.3–100%** per scanner |
| Median appearances per symbol per day | **10 – 81.5** |

**DUPLICATE-ON for all 13 live intraday scanners** — the repeating stream is a genuine liveness signal,
so **§5's invalidation-on-stream-stop is usable**. XVI (pb01) is a once-daily 17:00 EOD alert
(duplicate UNDETERMINED); IV/V have never sent a POST (UNDETERMINED).

## §11.7 — S&R detector timeframes: Rama's belief is WRONG on both halves

| Rama's belief | Source verdict |
|---|---|
| MIS = 1H + 1D | **WRONG (incomplete)** — MIS gets **30m + 1H + 1D**; 30-minute is the *dominant* TF |
| GTT = 1D + 1W | **WRONG** — GTT gets **exactly the same 30m + 1H + 1D** |
| (implied) a per-mode TF policy exists | **There is none** — one list, one detector, one warmer |

MEASURED: one global list at `config/system_config.yaml:529`: `["day", "60minute", "30minute"]`.
`Candidate.intent` ("INTRADAY"/"DELIVERY") exists at `sr_detector/models.py:142` and is **read by
nothing** in `sr_detector/`.

**Is 1-week data even fetched? NO — never, for any symbol, either book.** `"week"` is not in the
config, and
```python
core/config_loader.py:1063
    allowed = {"day", "60minute", "30minute", "15minute", "5minute"}
```
makes `timeframes: [..., "week"]` a **boot-blocking ValueError** (`main.py:1914-1917` → `return 5`).

MEASURED across **all 598 rows / 13,472 logged zones**: exactly three labels ever persisted —
`30minute` (10,768), `60minute` (9,966), `day` (2,531). **`week`: 0.** Both books identical in shape.

**§3 is a BUILD, not a config change.** Kite has no `week` interval, and the only resampler
(`core/candle_math.resample()`) accepts int-minutes or `"day"` only and **buckets per date, never
spanning days**.

## §11.8 — Context-layer inventory: what is actually available at order time

| # | Layer | Available AT ORDER TIME? | Verdict |
|---|---|---|---|
| 1 | S&R detector | **NO** — runs *after* the order reaches placement | EXISTS-BUT-NOT-AVAILABLE |
| 2 | ATR | **NO** — `market_data["atr"]` is `None` on 100% of 173,592 rows | NOT-PERSISTED / ABSENT on live path |
| 3 | Swing / pivot detection | **NO** — only inside the post-order detector and shadow workers | EXISTS-BUT-NOT-AVAILABLE |
| 4 | Level storage | **NO** for the live path (`retest_state` = 0 rows); `pb01_watchlist` is persisted but its strategy is `enabled:false` | NOT-PERSISTED |
| 5 | VWAP (broker `average_price`) | **YES** — 165,672 non-null | TRUSTWORTHY+AVAILABLE |
| 6 | EMA / SMA | **NO** — regime engine is a never-constructed component; there is no `sma()` function at all | EXISTS-BUT-NOT-AVAILABLE |
| 7 | The scorer | **YES**, and it binds (tier drives the size multiplier) | AVAILABLE but **SATURATED**: 4 of 10 inputs permanently dead, measured max score **65**, `HIGH` tier **0**, `MEDIUM` **15**, `LOW` **173,577** |
| 8 | Candle geometry / classification | **No named pattern code exists anywhere** — 0 hits for engulfing / doji-as-class / marubozu / pin / inside-bar | **ABSENT** (§6 is greenfield) |

At the decision instant the system holds **a quote snapshot and a saturated score**. Every geometric
input the contract's gates require — level, ATR, pivot, structure — is computed *after* the order,
or not at all.

> **Correction applied.** §11.8 initially reported `spread_check` as "never computed", having queried
> `$.spread`, a key that does not exist. The real key is `$.spread_check`:
> `[(0.0, 153461), (None, 18866), (1.0, 1265)]`. It is one of only **two live discriminators** and
> alone carries **873 of 3,464 (25.2%)** of all admissions.

---

# §12 — THE REPLAY

## §12.1 — INDOCO: does 287.80 appear at all?

### EVIDENCE — what Rama drew (read from the corpus images)

| Image | Header OHLC | Levels drawn |
|---|---|---|
| INDOCO-1D | O242.00 **H287.80** L241.34 C281.48 (+15.44%) | 276.83 · 267.36 · 253.65 |
| INDOCO-1W | O248.80 **H287.80** L239.00 C277.70 (+11.62%) | one line at **287.80** |

### THE ANSWER: NO

| Test | Result |
|---|---|
| Zones collected (nearest_resistance + nearest_support + confluence_evidence, both rows) | **52** (26 R, 26 S) |
| Numeric tolerance 287.00 <= band <= 288.60 (or band spanning 287.80) | **0 HITS** |
| Literal `LIKE '%287.8%'` on all 3 JSON columns | **0 rows** |
| INDOCO lines in `would_be.jsonl` containing "287.8" | **0** |
| **ANSWER** | **287.80 is absent from every stored zone, level and confluence entry, on every timeframe.** |

**What the system did hold:** highest resistance **270.00** (score 6.0, HIGH, 3 touches,
`["30minute","60minute","day"]`). Global band range across all 52 zones: **162.19 … 270.00**.
Timeframes: 30minute x45, 60minute x39, day x11 — **weekly: 0**.

MEASURED: the trade filled at **276.83 — 6.83 points ABOVE the highest resistance the system knew**,
with `nearest_resistance` explicitly **null**. Outcome: GTT_EXIT, **net_pnl −6.52**.

### But 287.80 was inside the system — and was discarded

The screener snapshot for the very signal that became the trade
(`sig_cf1906208c49…`, `screener_results` id 617046, status **PASSED**, score 62) carries:
```json
{"ltp": 277.41, "open": 242.0, "day_high": 287.8, "day_low": 241.34, "atr": null, "rsi": null}
```
The exact number Rama drew as weekly resistance was **in RAM at the decision instant as the day's
high**, never promoted to a level, never handed to the S&R detector, never compared against the entry.

### The real cause is NOT the missing weekly timeframe

```python
sr_detector/pivots.py:42
    for i in range(left, n - right):
```
With `config/system_config.yaml:532 → default_pivot_n: 5` and **no `pivot_n_by_tf` key defined
anywhere** (so `zone_builder.py:95` resolves to 5 on every timeframe), **the last 5 bars of every
fetched series can never become a pivot.** `sr_detector/fetch.py:124-125` fetches `now − 180d … now`,
so the last daily bar **is today**.

MEASURED: 287.80 is the high of **2026-09-02 — the trade date itself**. It is the *current bar's*
high, so it could not become a level on the daily timeframe **and could not on a weekly timeframe
either**, where it is also the last bar. Rama's own two screenshots prove it: 1D and 1W **both** read
H=287.80 — a live right-edge high, not a historical structural level.

**The weekly gap (§11.7) is real, but it is not what would have surfaced 287.80.**

### Right-edge blindness is general, and it collides with the corpus

The blind zone is the last 5 bars of each timeframe: about 2.5 h on 30-minute, about 5 h on 60-minute,
and **the last 5 trading sessions on daily**. Corroborated on live rows: of 562 `structure_status='OK'`
rows, only **37 (6.6%)** have any persisted band edge equal to that day's high.

**22 of 56 corpus files are literally "refer last 2-3 / 3-4 / 5-6 candles" requests.**
The system can only see a level that is already >= 5 bars old; Rama draws levels that are 1–3 bars old.

Caveat: the source argument is proof; the 37-of-562 figure is corroboration, not proof. The detector
was not re-run against a live fetch (that needs a token and is a write-adjacent path).

### The V3 shadow would have rejected this trade — for Rama's own reason

```json
"nearest_resistance": null, "sr_confidence_class": "ANCHOR_ONLY",
"gates": {"RR": {"passed": false, "reason": "RR",
   "evidence": {"detail": "missing S&R zone (no safe SL or TGT)",
                "sl_zone_edge": 258.22, "tgt_zone_edge": null}}},
"live_tgt": 285.13, "live_rr": 1.5, "v3_verdict": "WOULD_REJECT_RR"
```
The target 285.13 is a fixed 1.5 R:R construct, **2.67 points under the 287.80 the stock actually
wicked to and rejected from**. The shadow said reject; the live path took it and lost.

## §12.2 — KOTAKBANK

MEASURED: **100 signals, only on 2026-08-26 (11) and 2026-08-27 (89). ZERO signals on 2026-07-22** —
Rama's annotated day. Zero trades, zero orders, zero `sr_detector_results`, **zero zones on any
timeframe**: it never once passed the screener. The weekly support at 376.20 that Rama says corrected
the daily breakdown was never held, because no level of any kind was ever built for this symbol.

## §12.3 — JAICORPLTD, 21-Aug-2026: why the level was not 105.86

MEASURED: every system price for this trade is **pure arithmetic off the webhook trigger**:
`104.30 → −0.1% entry → −1.5% SL → +1.5R target`. The S&R detector never touched an order price.

MEASURED: 105.86 could not be an S&R level — the detector only ever emits **bar HIGHs from 30m/60m/day
bars**, and 105.86 is the high of **zero 30m bars, zero 60m bars, and neither daily bar** (108.23,
105.60). It fell into the **0.68-wide dead gap** between the 105.30–105.80 and 106.48–106.50 zones.
**No rounding, tick-snap or buffer is applied anywhere in `sr_detector/`.**

## §12.4 — The five labelled correct answers

MEASURED: the system's entry price is derived **only** from the webhook/live-quote trigger times a
fixed per-strategy offset, and **never reads a support or resistance level at all**.

| Case | Rama's named price | System actual | Was the named price in the stored level set? |
|---|---|---|---|
| INDOCO | 253.65 / 267.36 | 276.83 | **NO** |
| MIDHANI | 436 or 441 | 418 | **NO** |
| LAXMIDENTAL | 209 | 202 | **NO** |
| ANTELOPUS | at the 1D resistance | past it | **NO** |
| IDEAFORGE | one 1-min candle later | 829.60 (SL 836.75) | **YES** — 829.60 sat *inside* the stored nearest-resistance band |

MEASURED — **IDEAFORGE counter-case:** waiting the one extra 1-minute candle would **NOT** have saved
the trade; the stop still fires in the same 10:20 bar. The contract's instruction to measure the
confirmation delay rather than resolve it by argument was correct, and the measurement does not
support the one-candle rule.

## §12.5 — The corpus as a regression suite

| Contract claim | Verdict |
|---|---|
| 7 BTST/STBT files | **HOLDS exactly** |
| "28 of 56 describe multi-candle sequences" | **FAILS** — measured **30 strict / 35 loose** |

MEASURED: **39 of 56** files land on symbol-days for which the VM holds a full
signal+trade+S&R+candle record.

MEASURED — **structural ceiling:** 37 of 56 files are 1D or 1W charts, but the VM stores **only
1-minute bars** covering 2026-06-19 → 2026-09-04. KOLTEPATIL's "400D S&R" case and **all 5 weekly
files are not reconstructible at any effort** from stored data.

---

# APPENDIX — what could not be determined

1. **Whether the Chartink scanners IV/V exist but never match, or were never created.** Requires
   Rama's Chartink account. System-side they are fully wired and armed.
2. **The Chartink UI settings** (frequency, after-trigger, duplicate) are recorded nowhere in the repo;
   only their *behaviour* was measured.
3. **§10's actual question for L3** — unanswerable until `_broken_zone` (`sr_detector/flags.py:125`)
   is persisted.
4. **The 55-era admission rule** (2026-06-15 → 07-10, 13,082 rows) was not re-derived; the rule in
   §11.3 is the 60-era only.
5. **The `sl_buffer_atr_mult = 0.20` constancy** across 15-Jul → 04-Sep was read from current config
   and not checked against the 48 `config_snapshots` rows. If that knob was ever retuned, every
   recovered ATR30 before the change scales inversely.

**No recommendations are made in this document. Rama decides what happens next.**
