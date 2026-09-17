---
name: regime-phase1-investigation-18jul
description: "READ-ONLY 18-Jul — regime Phase 1 scoped. A production-grade regime/ module EXISTS but its direction axis answers a DIFFERENT question (daily EMA50/200 trend, not the 09:15-09:59 move); it reads the LIVE Kite API, NOT Phase 0's stored candles; and the V3 chain IS wired to its output (soak-baseline risk)."
metadata: 
  node_type: memory
  type: project
  originSessionId: b9e84959-b70c-4ce6-9521-3db6f6dd3fee
---

**📊🔎 REGIME PHASE 1 — INVESTIGATED 18-Jul-2026 (READ-ONLY; nothing changed/enabled/pushed).**
Report `docs/audit/regime_phase1_investigation_18jul2026.md`. Docs-only commit, **UNPUSHED**.

**⭐⭐ THREE PREMISE CORRECTIONS — all three assumptions in the instruction were partly wrong:**

**1. "Phase 1 may be just feeding it real data + the ordinal window" — NO. The existing
`direction` axis answers a DIFFERENT QUESTION.** It is a **multi-month DAILY trend classifier**:
EMA50 vs EMA200 + slope + swing structure (HH/HL) + ADX over **daily** candles
(`regime/engine.py:142-188`), refusing to compute below **201 daily candles**
(`engine.py:92`, `:109-115`). Rama wants the **NIFTY 09:15–09:59 opening move**. **There is NO
window config at all** — the only intraday knobs are `intraday_interval` + `intraday_lookback_days`,
and the intraday series feeds **only** `day_type`, which consumes the WHOLE session-so-far and
deliberately WAITS OUT the open (`session_progress ≥ 0.2`, `engine.py:237`). ⇒ Phase 1 = **add a NEW
ordinal opening-move axis inside the existing module** (never a parallel one) + window/band config +
an append-only daily log. Not a flag-flip, not a ground-up build.

**2. "Now that Phase 0 stores index candles, can it compute?" — THE ENGINE NEVER READ THE
`candles` TABLE.** It reads the **LIVE Kite historical API**:
`engine._fetch` → `OhlcFetcher.fetch_by_token` (`sr_detector/fetch.py:85-101`) → `_fetch_one` →
`self._fetch_fn(token, from_dt, now, interval)` + `Candle.from_kite` (`fetch.py:125-126`), where
`_fetch_fn` = `_make_sr_fetch_fn(_md_kite, rate_limiter)` (`main.py:2828`, wired `:2859-2864`).
⇒ **Phase 0's stored candles are a BACKTEST/CALIBRATION asset (exactly what Q10 needs), NOT the
engine's feed**; the engine was never blocked on Phase 0. Do NOT "make the regime read stored
candles" — the live path stays on the API.

**3. 🔴 SOMETHING IS WIRED TO ITS OUTPUT — soak-baseline risk (NOT an order-path risk).** The V3
chain (`v3_chain_mode: "shadow"`, deployed/LIVE) consumes regime **twice**:
`gate_extreme(sig.regime_state)` (`v3_chain/runner.py:211`) and **`regime_fraction(...)` = 8 of 40
Context points** (`runner.py:225`, impl `:300-330`); PB-01's would-be scorer likewise
(`pb01_runner.py:153-154`, `:198`, `:214`). All **LOG-ONLY** (shadow never rejects/delays an order;
`gate_extreme` fails **OPEN** — `screening/hard_gate.py:337-345`). **⚠️ BUT:** today `regime_runner`
is None ⇒ `regime_fraction` returns `(None, unavailable=True)`; **flipping `regime.enabled`
mid-soak would change the shadow score distribution being accumulated for the enforce decision and
make pre/post-flip rows non-comparable.** ⇒ **Phase 1 must NOT flip `regime.enabled`.**

**Q2 gate:** `regime.enabled: false` (`config/system_config.yaml:362`; default False
`core/config_loader.py:895`); gate comment "VERIFY live historical access on the VM before flipping"
(`:364`). Phase 0 proved `historical_data` for token 256265 at **1-minute × 1 day** — the engine
needs **`day` interval × 400 days ≥201 candles**, a DIFFERENT call: **strongly implied, NOT proven.**
One command would close it (only matters if the existing 3-axis engine is ever enabled).

**Q5 — ALREADY ORDINAL, and Phase 2's map ALREADY EXISTS:** the direction axis is a **vote count**
(`engine.py:162-179`), and `models.py:37` says *"Ordinal FIRST — a calibrated % is a later,
data-driven step (do NOT fake precision)"* = Rama+ChatGPT's decision, already implemented.
**`regime_pref_direction: {BULL:1.0, SIDEWAYS:0.5, BEAR:0.0}`** at `w_regime_preference: 8.0`/40
(`core/config_loader.py:1086-1091`, `:1058`) **IS a Bull/Flat/Bear tilt** — V3/PB-01-scoped today.

**Q6 fail-safe CONFIRMED** (3 layers): insufficient data → `UNKNOWN`+neutral "(NOT a halt)"
(`engine.py:109-115`); per-axis error → `neutral_axis` (`:344-351`); any exception → `unknown_state`
(`:136-138`); `unknown_state` = "the system would trade normally — this is NOT a halt"
(`models.py:113-125`); runner "must never die/raise" (`runner.py:83`). 13 tests
(`tests/unit/test_market_regime.py:133-263`).

**Q9 — shadow sink:** **NOT** `data_store/regime/regime_state.json` (overwritten every cycle,
`runner.py:89-98` ⇒ latest only, **no history**). Recommend **append-only
`data_store/regime/regime_daily.jsonl`**, matching `forward_shadow_*.jsonl`
(`scripts/forward_shadow_record.py:40`), `pb01_would_be.jsonl`, `allocator/regret.jsonl`. Written by
a **post-close cron sibling of the 15:40 `fetch_daily_candles`** (which already ingests the index) ⇒
no migration, off the live process.

**⭐ Q10 CORE-ASSUMPTION TEST = FEASIBLE, but the data is NOT there yet.** Trades side READY: **155
filled trades / 23 trading days, 15-Jun→16-Jul**, per-day net P&L aggregatable. Index side:
**`candles` has NIFTY 256265 for EXACTLY ONE DAY (16-Jul, 375 rows)** — all 10 index tokens likewise
(overall table 131,527 rows / 295 tokens / 19-Jun→16-Jul). **Prerequisite = a ~23-trading-day
backfill via the ALREADY-PROVEN `scripts/fetch_daily_candles.py --backfill --from --to` (`:9`,
`:132-135`; `_fetch_indices` runs first + fail-safe, `:65`/`:153-158`) — data-only, no migration.**
Then one query: NIFTY 09:15→09:59 move → ordinal bucket → join to that day's outcomes.
**Caveats:** n=23 (3 buckets ⇒ single-digit cells) · stock candles start 19-Jun vs trades 15-Jun ·
**confounded by scanner mix** (BK-1: book is 91% long, losses concentrated in intraday longs) ⇒
control for strategy/direction · tests association, not the counterfactual.

**RECOMMENDED SCOPE: do Q10 FIRST** (data-only backfill + query, proven tooling) — it tests the
thesis Phases 1–3 rest on, before any code. **Then** Phase 1 = new opening-move axis + window config
+ append-only daily log, **without** flipping `regime.enabled`.

Related: [[regime-phase0-17jul]] (supplied the index data + proved API access) ·
[[strategy-direction-registry-17jul]] (Phase 2's direction input) · [[bk1-long-short-scanner-17jul]]
(the 91%-long confound + the regime confound this would finally close) ·
[[feedback-verify-the-finding-premise]] (3 more inverted premises — the rule keeps earning its keep).

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 547 B (budget 300 B). The index now carries a hook and this link.

- 📊🔎 **[REGIME PHASE 1 SCOPED 18-Jul — 3 PREMISES INVERTED](regime_phase1_investigation_18jul.md)** — the existing `direction` axis is a **daily EMA50/200 trend, NOT the 09:15–09:59 move** (no window config) ⇒ Phase 1 = a NEW opening-move axis inside `regime/`; the engine reads the **LIVE Kite API**, never Phase 0's candles (those are the *calibration* asset); **🔴 the V3 chain IS wired to it** (`gate_extreme`+`regime_fraction`, 8/40 Context) ⇒ **do NOT flip `regime.enabled` mid-soak.** [[regime-phase1-investigation-18jul]]
