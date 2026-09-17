# PHASE A — A1 · A2 · A3 AND THE ADDENDA
## READ-ONLY · 05-Sep-2026 · no Phase B

**Repo SHA:** `6d24a83` (branch `feat/delivery-config-split`) · **VM:** `trading-vm`
**Method:** every SQLite opened `?mode=ro`. No script under `scripts/` executed. Nothing written to
the VM. No code, config, YAML, scanner, commit, push or restart. **`pullback_wait_enabled` was neither
flipped nor edited.**

**Provenance:** MEASURED (run this session) · EVIDENCE (a file/image says it) · INFERENCE.

> ### ✅ VERIFICATION STATUS — SUPERSEDED, NOW COMPLETE
> This document originally carried §1.1, §2 and §2.1 as **UNVERIFIED** (their adversarial verifiers
> died on a session usage limit). **All three have since been independently re-derived with positive
> controls and adversarially upheld** — see `PHASE_A_REVERIFICATION_05-Sep-2026.md`.
> Verdicts: §1.1 **VERIFIED** · §2 **VERIFIED** (Part 1 reproduces to the last digit; Part 2 adds a new
> controlled NULL) · §2.1 **VERIFIED** · §1 token mechanism **VERIFIED**. Zero refuted.
> Two numbers in §2.1 and one probe in §1.1 moved without changing a conclusion; the re-verification
> document records the exact old-vs-new and the cause.

---

# A1 — THE TWO CHARTINK QUESTIONS · CLOSED

## §7.1 — Do RANGE BREAKOUT LONG / SHORT exist? → **YES. Present, Active, running, matching nothing.**

Read directly from the account's own alert dashboard (existing session; no login; nothing modified).

| Fact | MEASURED |
|---|---|
| Alerts present | **16 of 16**, all `Active` |
| RANGE BREAKOUT LONG / SHORT last run | **Fri, Sep 4 2026 3:29 PM** — identical to every working scanner |
| PB01 last run | 5:00 PM — independently confirms the once-daily EOD measurement |
| Live scan result, both RANGE BREAKOUT scans | **"No stocks present"** |
| Signals produced, 12-Jun → 04-Sep | **0 of 208,946** |
| Inbound webhooks | **0 of 223,484** |

The account's real conditions (`/screener/range-breakout-long-5`) match the spec file exactly:

```
Daily Max(15, Daily High) − Daily Min(15, Daily Low)  Less than  Daily Close * Number 0.02
Daily Close  Greater than  Daily Max(15, Daily High)        <-- UNSATISFIABLE
```
and the SHORT (`range-breakout-short-10`): `Daily Close Less than Daily Min(15, Daily Low)` — the mirror.
Bare `Daily Max/Min(15, …)` includes today's bar, and High >= Close >= Low, so neither can ever be true.

**Two independent controls eliminate configuration, delivery and plumbing:**

1. **A different author's screener** occupying the unsuffixed `/screener/range-breakout-long` slug
   (SURENDRA RAMCHANDRA RANE) uses `1 day ago`-style offsets and returned **40 stocks on the same day**
   this account's returned zero. Same market, same instant.
2. **Byte-identical alert configuration** to a working scanner — see §7.2. VWAP BOUNCE LONG shares the
   frequency, duplicate mode, after-trigger setting, webhook host and token, and has produced **59,041
   signals**; RANGE BREAKOUT LONG has produced **zero**.

⇒ **The condition is the only difference. Three months of a scanner firing at nothing.**
⇒ **F1 LEVEL BREAK (II · IV · V · XVI): IV and V never fire, XVI is `enabled:false`. F1's live coverage
rests on II alone — a delivery scanner.**

> **Slug hazard, recorded permanently.** The unsuffixed slug belongs to a stranger. This account's slugs
> are suffixed — `range-breakout-long-5`, `range-breakout-short-10`, `vwap-rejection-short-16`.
> An earlier read of the unsuffixed slug nearly reported a stranger's conditions as this account's.
> **Never cite the unsuffixed slug.**

## §7.2 — Alert configuration → **§5's liveness premise CONFIRMED from configuration**

EVIDENCE — from three `Modify Alert` screenshots supplied by Rama.

| Alert | Frequency | Min matches | After trigger | Duplicates | Webhook |
|---|---|---|---|---|---|
| RANGE BREAKOUT LONG | **1 minutes** | 1 | Continue | **Duplicate** | CONFIGURED |
| VWAP BOUNCE LONG | **1 minutes** | 1 | Continue | **Duplicate** | CONFIGURED |
| PB01 BREAKOUT RETEST | **market close** | 1 | Continue | **Unique** | CONFIGURED |

Delivery on all three: `Desktop/Mobile (web)` only; Email / Sms / Whatsapp unchecked. The webhook is a
separate CONFIGURED field pointing at the VM's public endpoint.

⇒ `Duplicate` + `1 minutes` + `Continue` is exactly what produced the measured 60 s modal gap, 79,479
POSTs over 257 scanner-days and 97.3–100% consecutive-minute symbol carryover. **§5's
invalidation-on-stream-stop is usable on the 13 live intraday scanners.**
⇒ PB01 is `Unique` + `market close` — one POST per day. **Stream-stop is NOT a usable signal there.**

> **Operational note (no secret reproduced here).** The webhook URL visible in those screenshots embeds
> a live bearer token and the VM's public IP, and the same token is shared across all scanners. Anyone
> holding it can POST fabricated signals into the live signal pipeline. Rotate it if those images have
> been shared onward.

---

# A2 — THE `pullback_wait` STALE-vs-FRESH DELTA

## A2.0 — What was claimed, and what survived

An earlier pass headlined that staleness "re-routes into the fill decision" and produced adverse
selection. **Adversarial verification destroyed that clause.** MEASURED by the verifier:

* The regressor was the **close of the minute bar in which the order was placed** — a median **71.7%**
  of that bar occurs **after** the order was already live. Look-ahead contamination.
* On a strictly pre-placement price, Fisher Q1-vs-Q4 goes **p=0.0006 → 0.0982** (bar open) → **0.8373**
  (previous bar's close).
* The fill-rate gradient is **equally present in the re-anchoring FRESH cohort** (FAV 76.3% / ADV 19.8%
  vs STALE 75.8% / 24.5%). It is a property of **LIMIT orders**, not of the stale anchor.

⇒ **No outcome harm from staleness is established.** *Measured delta ≠ measured harm.*

## §1.1 — Is there a natural experiment? → **NO.** *(UNVERIFIED)*

`pullback_wait_enabled` is set per strategy, so strategy identity is perfectly collinear with the
treatment. The only escape would be a strategy that changed value mid-period. Five independent probes:

| # | Line of evidence | Result |
|---|---|---|
| 1 | `config_snapshots`, 48 rows, 02-Jul→04-Sep | Stores only the resolved AppConfig (9 top-level keys). **0 of 48 contain the string `pullback_wait`.** `file_hashes` covers 8 top-level YAMLs — **no strategy YAML**. Cannot answer. |
| 2 | Git pickaxe `-G` over **all 40+ refs**, local repo | Exactly **2** commits ever touched such a line: `bcf03b5` (17-Apr, initial 15 files) and `5a71fb6` (13-Jul, `pb01` created). **Every `+`; zero `−`. No value ever edited.** |
| 3 | VM bare repo `/home/ubuntu/trading-system.git`, **all 1,272 commits** on `main` since 01-Jun | **2** distinct flag signatures; the only difference is the 13-Jul *addition* of `pb01_breakout_retest`. All 15 pre-existing strategies: identical on all 1,272 commits. |
| 4 | The **31 actually-deployed SHAs** (from `forward_shadow` `git_commit`, 13-Jul→04-Sep) | All 31 produce a **bit-identical signature** (md5 `fd2c782385`) = **6 true / 10 false**, every day. |
| 5 | Runtime: the FIX-067 log line fires **only** when the flag is FALSE; 243 events, 27-Aug→04-Sep | **185 attribute uniquely to a FALSE-cohort strategy; 58 are price-collisions sharing a FALSE-cohort strategy; 0 attribute to an all-TRUE strategy set.** |

Note the deployed tree is **not** a git repo — the authority is the bare repo. 13 intraday YAMLs share
one mtime (`2026-07-13 18:33:49`); the 3 positional YAMLs are stamped `2026-09-04 10:41:49`, which is
the TEMP delivery disable and changed `enabled`, **not** `pullback_wait_enabled`.

A first pass showed 14 apparent violations; re-joining on the **exact `stale=` price** against
`signals.trigger_price` dissolved all 14 — each is a symbol fired by both a TRUE- and a FALSE-cohort
scanner in the same minute, with the log line belonging to the FALSE one.

The 12 distinct `system_config_sha` and 18 distinct `config_hash` values over the period are **not**
evidence of a flag change: both hash `system_config.yaml` / the resolved AppConfig, which contain
**zero** occurrences of `pullback_wait_enabled` (`strategies/schema.py:111` declares it with no default,
so the 16 strategy YAMLs are its sole source).

⇒ **No within-strategy variation exists. The confound stands. No causal claim about stale pricing is
available from this observational data, and none is made.**

## §2 — Delta as a fraction of the stop → **median 4.6%, and SYMMETRIC** *(UNVERIFIED)*

Three distinct quantities, kept separate because an earlier pass conflated them:

| | Quantity | N | Measures | Does NOT measure |
|---|---|---|---|---|
| **D1** | \|live − stale\| / stale, ÷ stop, from 263 `FIX-067 momentum fresh quote:` log lines | 263 signals (45 became trades) | TRUE pipeline staleness | Anything about the STALE cohort — the logging branch sits inside `if not pullback_wait_enabled` |
| **D2** | recovered anchor − `trigger_price`, ÷ stop, by inverting `entry_target_price` | **234 FRESH trades** | The same quantity as D1, for 5.2x more trades over 8x more days | Same cohort limit |
| **D3** | `entry_actual_price` − `trigger_price`, ÷ stop | 339 filled | **NEAR-VACUOUS** — a LIMIT cannot fill worse than its limit | Staleness; it is also post-placement |

Denominator is `abs(entry_target_price − sl_initial)`, MEASURED per trade — equal to `sl_pct × entry` on
**234/234** of the D2 population.

**D2 — the headline (N=234):**

| metric | mean | median | P75 | P90 | P95 | max |
|---|---|---|---|---|---|---|
| \|delta\| / stop | 0.0895 | **0.0460** | 0.1110 | **0.1871** | **0.3185** | 1.0470 |
| adverse-signed / stop | −0.0059 | 0.0000 | 0.0429 | 0.1289 | 0.1755 | 1.0199 |

**The key number:**

| threshold | share ADVERSE beyond it |
|---|---|
| **> 25% of the stop** | **8 / 234 = 3.42%** |
| > 50% of the stop | 2 / 234 = 0.85% |
| > 100% of the stop | 1 / 234 = 0.43% |

**It is symmetric:** 104 adverse / 101 favourable / 29 exactly zero. Two-sided sign test **p = 0.889**;
mean signed delta −0.0059 of the stop (very slightly *favourable*); median exactly 0.0000.

⇒ **Staleness does not bias entries systematically late.** It is a symmetric widening of the
entry-price distribution, not a directional cost.

By direction: LONG N=211 (signed mean −0.0134), SHORT N=23 (signed mean +0.0631 — do not read a
directional effect from N=23). By strategy, the 3 DELIVERY strategies (`sl_pct` 0.020) sit at roughly
half the fraction of the INTRADAY ones (0.010–0.012), as expected from the wider denominator.

**Validation:** D2 reproduces the logged live price to **< 0.0001 rupee on all 45 overlap trades** and
sits ~40x above its own measured noise floor. **D3 confirmed vacuous** — its median is −0.102 of the
stop, i.e. −`entry_offset_pct`/`sl_pct` to three decimals.

**Standing limit:** D1 and D2 both measure the **FRESH** cohort. Applying their distribution to STALE
stop distances is a cross-cohort extrapolation, and the STALE cohort's true staleness is
**structurally unmeasurable** from logs because the logging branch never runs when the flag is true.

## §2.1 — Is the "fresh" quote actually fresh? → **FRESH** *(UNVERIFIED)*

| Probe | MEASURED |
|---|---|
| Memoisation anywhere on the `_quote_fn` path | **None.** The only cache in the area is the webhook fingerprint TTLCache, which holds signal ids, not prices |
| 37,628 logged `get_quote` calls | minimum wall-clock **10 ms**; **zero** calls at or below 2 ms |
| Two independent `get_quote` calls, same symbol, 81 ms apart | **returned different prices** — rules out memoisation at any TTL down to ~0.1 s |
| The 11.0% zero-move rate (29 / 263) | **genuine no-trade, not a cache.** The `stale=` comparand comes from the external webhook payload, not from Kite at all; the zero-move cohort's median day volume is **3.2x lower** (711k vs 2.28M) |

⇒ The stale-vs-fresh distinction is **real**; A2 is measuring something.

**One thing is not fresh, and is unrecorded:** the **broker-side age** of the quote. Kite returns
`timestamp` and `last_trade_time`, kiteconnect parses both, and the adapter **discards them** —
`Quote.ts` is the local wall clock. So the quote's true age at the broker is not knowable from stored data.

---

# A3 — WHICH CORPUS CASES CAN ACTUALLY BE REPLAYED

## The finding that dissolves the "39 of 56 vs 37 are 1D/1W" tension

MEASURED: `analytics.db.candles` is **`interval_sec=60` on 100% of rows**, spanning 54 trading dates
(2026-06-19 → 09-04) across 1,268 symbols — but **that span is the union over all symbols, not
per-symbol coverage.** Per symbol the store holds only the days that symbol was scanned or traded:
median **4** distinct days for corpus symbols. A covered day is a full 375-bar session.

⇒ **A single daily bar is usually rebuildable; a multi-day daily *pattern* almost never is.**
The binding constraint is per-symbol day sparsity, not the 1-minute interval.

## Final corrected class counts (sum = 56)

| class | count | note |
|---|---|---|
| **FULLY_REPLAYABLE** | **41** | 34 distinct (symbol, anchor-date) pairs across 33 distinct symbols |
| **PARTIAL** | **2** | KALYANJIL-BTST, KVB_Delivery-1D — candles + signals + snapshots but **no trade row** on the anchor day |
| **CHART_ONLY** | **4** | KOLTEPATIL-400D, HUHTAMAKI-1W, INDOCO-1W, KVB_Delivery-1W |
| **NOT_RECONSTRUCTIBLE** | **9** | BANKBARODA ×2, CUB, KOTAKBANK-1D, KOTAKBANK-1W, SHRINGRAMS, SONACOMS, YESBANK-1D, YESBANK-1W |

Counting rule, stated explicitly: one entry per unordered `(symbol, anchor-date)` pair, de-duplicated
across files; a file naming several symbols on one day contributes one pair per symbol; the same symbol
on two anchor dates counts twice (DALMIASUG at 07-01 and 07-06 is the sole source of the 34-vs-33 gap).

## The new column — T3 (live-reference) testability

**47 of 56 corpus files are T3_TESTABLE**: a `screener_results.market_data_snapshot` exists on the anchor
symbol-day and carries **non-null `day_high` AND `day_low`** — 100% of non-empty snapshots do.
**INDOCO's 287.80 is confirmed present in that snapshot.**

⇒ Replayability and T3-testability are **different properties**, and they come apart. KOLTEPATIL is
`CHART_ONLY` (unreplayable) yet **T3_TESTABLE**, with 200 snapshot rows carrying day_high/day_low.

## The five prior errors, corrected

| # | prior claim | verdict | corrected figure |
|---|---|---|---|
| (a) | max corpus candle-days = 9 (DEEPINDS, CYIENT) | **WRONG** | **10 — APOLLOPIPE.** A3 self-contradicted; its own section-1 table printed 10 |
| (b) | "no symbol anywhere exceeds 9 days" | **WRONG** | **All symbols max 36** (10 index symbols). **Equities max 11** — BALUFORGE, MARSONS |
| (c) | "40 files, 24 distinct symbol-days" | **WRONG either way** | **41 files → 34 pairs → 33 symbols.** Even on the old 40-file list the pair count is 33, never 24 |
| (d) | KOLTEPATIL 400-day | **verdict UPHELD, basis corrected** | KOLTEPATIL has 4 candle-days, maxrun 2. But the real ceiling is global: 54 trading days total, deepest single symbol 36, **no daily-bar store at all** (`daily_symbol_stats` = 0 rows). A 400-day lookback is unanswerable by ~7x even at the global ceiling |
| (e) | all 5 weekly files unreconstructible | **verdict UPHELD, basis corrected** | Per-symbol ISO-week completeness on the anchor week: HUHTAMAKI **5/5** (the only complete week in the corpus), KARURVYSYA 3/5, INDOCO 1/5, KOTAKBANK 0/5, YESBANK **0/5 with zero data anywhere**. Four of five cannot form even one weekly bar; HUHTAMAKI forms exactly one, which cannot answer a "last 2 candles" question |

---

# WHAT PHASE A DID NOT ESTABLISH

1. **Any causal harm from stale pricing.** No natural experiment exists; the confound is total.
2. **The STALE cohort's own staleness distribution.** Structurally unmeasurable — the logging branch
   never runs when the flag is true.
3. **The broker-side age of any quote.** Kite supplies it; the adapter discards it.
4. **Whether §1.1 / §2 / §2.1 survive adversarial re-derivation.** Their verifiers died on a session
   limit. Every other section in this document was verified, and that process has already overturned
   one headline — so this gap is not cosmetic.
5. **Whether the Chartink RANGE BREAKOUT scanners were ever edited.** Only their current state was read.

**No recommendations. No Phase B. Rama decides what happens next.**
