---
name: regime-phase0-17jul
description: "Regime-ranking Phase 0 DONE + DEPLOYED 17-Jul — NIFTY + sector index candles now ingested/stored via the extended fetch_daily_candles cron. DATA ONLY. Phase 1+ (regime compute→weighting) are signal-path careful-loop, NOT built."
metadata: 
  node_type: memory
  type: project
  originSessionId: 26214a92-ac1b-4507-998c-ca000415a4c5
---

# Regime-ranking feature · PHASE 0 — index candle ingestion — DONE + DEPLOYED 17-Jul

Report `docs/audit/regime_phase0_index_ingestion_17jul2026.md`. **Tag `deploy-17jul-regime-phase0`
→ `4e2df39`; PC == origin == VM bare == `c8a2e6c`** (delta tag..HEAD = markdown only). **DATA ONLY
— no regime computed, no weighting, no trading-decision change.**

## Q1 root cause (why index data was empty — BK-1's finding)
Index tokens were **never in EITHER candle path** (not a bug, just out of scope): the LIVE tick
path (`live_feed`→`CandleStore`→`main.py:3162 _persist_candle`) subscribes only the **stock**
universe (`instrument_cache.token_map()`), and the BATCH cron `scripts/fetch_daily_candles.py`
fetches only **traded** symbols (PROCESSED signals). Live `candles` = 285 stock tokens, 0 indices.

## What was built (REUSE, not a parallel pipeline)
Extended the **BATCH** path (the right point: its job is already "historical fetch → candles
table", it's testable offline via `--backfill`, and it's zero-touch to the live scanner/tick path):
- **`config/index_universe.yaml`** (NEW) — data-driven index list (NIFTY 50 + 8 sectors + INDIA
  VIX); resolved to Kite tokens at fetch time, no hardcoded tokens.
- **`fetch_daily_candles.py`**: `_load_index_universe()` + `_fetch_indices()` fetch each index's
  1-min candles via the **same** `kite.historical_data` and store via the **same**
  `_insert_into_candles_db`. Called FIRST in `_fetch_single_day`, before + independent of the stock
  path (regime needs NIFTY every session incl. no-trade days).
- **No migration** — `candles` (in analytics.db) already has `volume DEFAULT 0`; indices store with
  volume=0 (they carry no volume). `trading_system.db` schema **v44 unchanged**.
- **FAIL-SAFE by construction**: missing config / unknown token / failed fetch → logs + continues,
  never raises ⇒ can't break stock ingestion or the boot (tested).

## Index tokens (confirmed live 17-Jul)
NIFTY 50=256265 · BANK=260105 · IT=259849 · AUTO=263433 · PHARMA=262409 · FMCG=261897 · METAL=263689
· ENERGY=261641 · FIN SERVICE=257801 · INDIA VIX=264969. All in `kite.instruments("NSE")` segment
INDICES. `historical_data` returns clean 1-min OHLC, volume=0.

## Proof (deployed backfill of 16-Jul)
10/10 indices × 375 candles = **3,750 rows stored**. **NIFTY 256265: 0 → 375 rows** (09:15→15:29,
sane OHLC, volume=0, interval_sec=60). **Stock ingestion UNCHANGED**: tokens 285→295 (+10 indices),
rows +3,750 = exactly the index rows, **0 stock rows changed** (stock re-fetch = idempotent dupes).
**Going forward the existing 15:40 cron fetches indices daily automatically** (no boot dependency);
wider historical seed available on demand via `--backfill --from --to` if Phase 3 wants it.
Regression 42F/4850P, ZERO attributable (all env-baseline files; [[pc-test-env-hygiene]]).

## The AGREED DESIGN (context; Phase 1+ NOT built)
Reuse the V3 MARKET REGIME module (`regime/`, currently `enabled:false`): NIFTY 09:15-10:00 move →
ORDINAL regime (Bull/Flat/Bear) → a DYNAMIC WEIGHTING layer scaling each strategy's priority.
**PREFERENCE not permission** (never a hard filter; no strategy ever disabled). Data-driven (any
new Long/Short strategy scored without code redesign; no hardcoded strategy names). Ordinal first,
% bands calibrated later from live data. Unknown regime → neutral weights. Log regime+weights daily.
Everything shadow-tested before it influences live.

## ⚠️ PHASED PLAN — Phase 1+ are SIGNAL-PATH CAREFUL-LOOP (design→ChatGPT→implement), NOT batch
- **Phase 0** ✅ DONE (this) — ingest+store index candles. DATA ONLY.
- **Phase 1** — compute the ordinal regime in the V3 module + fail-safe. CAREFUL LOOP.
- **Phase 2** — wire regime → strategy-weight scaling. CAREFUL LOOP.
- **Phase 3** — shadow + daily regime/weight logging + threshold calibration.
- **Phase 4** — secondary factors (sector strength, VWAP, breadth, VIX) one at a time.

## Relations
- **BK-1** ([[bk1-long-short-scanner-17jul]]): the regime confound BK-1 **could not measure** (no
  index candles) is now becoming measurable — Phase 0 stores exactly the NIFTY history that gap
  needed. Phase 3 calibration can use the seeded + going-forward index data.
- **M-S4** (dead scorer, 25/100 constant 0.0): gated on D2 / the regime direction; the regime
  feature is part of what informs it.
- **The `regime/` module** already has `OhlcFetcher.fetch_by_token` for a live on-demand fetch
  (Phase 1's 10:00 decision path) — Phase 0's stored candles are for calibration/backtest, not the
  live decision. `regime.index_token 256265` config exists; `enabled:false`.

Related: [[bk1-long-short-scanner-17jul]] · [[v3_step3_market_regime_11jul]] · [[capital-operational-note]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 423 B (budget 300 B). The index now carries a hook and this link.

- 📊🚀 **[REGIME PHASE 0 — DEPLOYED 17-Jul](regime_phase0_17jul.md)** — `fetch_daily_candles` extended (+`config/index_universe.yaml`) to ingest 10 indices into `candles` via the existing `historical_data` path. **DATA ONLY**, no migration. PROVEN: NIFTY 256265 0→375 rows; stock ingestion unchanged. The 15:40 cron now ingests indices daily ⇒ **the regime clock runs with NO new code.** [[regime-phase0-17jul]]
