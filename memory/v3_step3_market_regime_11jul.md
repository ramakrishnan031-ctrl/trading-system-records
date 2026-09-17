---
name: v3_step3_market_regime_11jul
description: "V3 Step 3 — 03.02 Market Regime engine (NEW regime/ package; 3 axes + ordinal confidence + extreme flag; SHADOW, fail-safe, default-OFF, gates nothing); BUILT-but-UNPUSHED"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c01370e-a523-42ed-bcb4-b17cc03d4987
---

**V3 Shared-Engine — Step 3: 03.02 Market Regime (11-Jul-2026). Pure NEW `regime/` package. SHADOW, gates NOTHING, fail-safe, default-OFF. BUILT + TESTED, BUILT-but-UNPUSHED.** Follows [[v3_step2_sr_detection_11jul]] / [[v3_step1_common_utils_11jul]]. Re-confirmed Phase-0 grep negative (no regime anywhere). Reuses Common Utils + existing OHLC fetch (R2).

**TASK 0 index data (KEY FINDING):** the NIFTY index is **NOT in the instrument cache** (`instruments.csv` has NO index rows; token 256265 appears only in test fixtures; not in live_feed/config). So `OhlcFetcher.fetch_interval("NIFTY 50")` (cache-resolved) returns empty. **Resolved by REUSE, not invention:** new `OhlcFetcher.fetch_by_token(token, interval, lookback_days)` fetches the index via the SAME rate-limited `_make_sr_fetch_fn` closure using a CONFIG index_token (256265 default). `fetch_timeframes`/`fetch_interval` untouched. **⚠️ VM must verify live index historical-data access before flipping `regime.enabled`; fail-safe covers absence → UNKNOWN.** (Report this to ChatGPT.)

**New pure indicators (`core/candle_math.py`, reused by regime — substrate, not duplicated):** `ema_series`/`ema` (SMA-seeded, k=2/(p+1)); `adx` (Wilder, reuses `true_range_series`, needs ≥2·period+1 candles → None). +9 tests.

**Engine (`regime/engine.py`, `compute()` NEVER raises):** 3 axes — DIRECTION (BULL/BEAR/SIDEWAYS: price vs EMA50/EMA200 + slope + HH/HL via `find_swing_pivots` + ADX; ≥4 agreeing sub-signals & trending → HIGH), VOLATILITY (HIGH/NORMAL/LOW: cur ATR / baseline-TR ratio vs config bands), DAY-TYPE (TREND_DAY/RANGE_DAY/UNDETERMINED: intraday range/ATR + ADX + one-directionality + position; **early session → UNDETERMINED LOW** via session_progress from MarketWindows). Each axis error → most-uncertain value at TRANSITION (never crash).

**Ordinal confidence → multiplier (`regime/models.py`):** HIGH 1.0 / MEDIUM 0.5 / LOW 0.2 / TRANSITION 0.0. `RegimeState.preference_multiplier` = direction axis (headline); each axis carries its own. Ordinal FIRST (no faked %).

**Extreme flag (TASK 5):** TRUE **only** on CONFIRMED halt/circuit from the injected `exchange_status_fn` (positive confirmation: str HALT/CLOSED/…, bool, or dict{halted/market_status}). **MISSING feed → FALSE + CRITICAL log** (absence ≠ halt). **Emitted + logged, NOT wired to stop trading** (03.03 consumes later).

**Fail-safe (TASK 6, the contract):** missing/insufficient index candles → `unknown_state` (status UNKNOWN, all axes neutral, multiplier 0 — book trades normally, NOT a stop). Any exception → UNKNOWN + neutral. **A broken regime NEVER halts the book.**

**Runner (`regime/runner.py`):** `MarketRegimeShadowRunner` — periodic compute→log→persist `data_store/regime/regime_state.json` (best-effort; for later prior_day_regime). `read_persisted_regime` helper. Default-off (won't start if engine disabled).

**Config/wiring:** `RegimeConfig` in config_loader (enabled:false default; index token/symbol, EMA/ADX/ATR periods, vol ratios; validators intraday-interval + ema_fast<ema_slow) + registered on SystemConfig + `system_config.yaml regime:` block. `main.py` builds+starts the runner ONLY when `regime.enabled` (shares `_sr_fetch_fn`, own OhlcFetcher, `exchange_status_fn=None`); stopped in `_shutdown`. **Inert by default → no live behaviour change.**

**R4 regression (NEW module, no callers):** existing touches = `main.py` (dormant block + shutdown param/hook + `_regime_on` flag), `core/config_loader.py` (+RegimeConfig), `sr_detector/fetch.py` (+fetch_by_token; fetch_timeframes/fetch_interval byte-identical), `core/candle_math.py` (+ema/adx), `config/system_config.yaml` (+regime block). **test_main clean-tree vs dirty-tree failures IDENTICAL (26==26, stash-diff PROVEN) → zero new failures.** The pre-existing PC-env baseline (test_main/fix061/phase17, green on VM [[pc_test_env_hygiene]]) unchanged. Changed-area 251 pass; regime spec `tests/unit/test_market_regime.py` (13: T1 bull/HIGH, T2 choppy/SIDEWAYS≤0.2, T3 early→UNDETERMINED, T4 halt→extreme, T5 dropped-feed→FALSE+CRITICAL, T6 missing-index→UNKNOWN/0, T7 determinism, T8 BULL+HIGH_VOL both, +axis-error/garbage-fetcher fail-safe, mapping, runner). Paper==live (pure, injected collaborators, no mode branch).

**Files:** ?? `regime/{__init__,engine,models,runner}.py`, `tests/unit/test_market_regime.py`; M `core/candle_math.py`(+ema/adx), `core/config_loader.py`, `main.py`, `sr_detector/fetch.py`, `config/system_config.yaml`, `tests/unit/test_candle_math.py`. **BUILT-but-UNPUSHED** (with Steps 1+2). Docs: SYSTEM_MAP.md V3 03.02 section, PATHS.md, ledger. **NEXT = Step 4 (03.03 Hard-Gate extraction + 03.04 scorer re-scale, COUPLED) after Web Claude + ChatGPT review.**
