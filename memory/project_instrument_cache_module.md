---
name: Instrument cache + account registry module built and locked (IC1-IC15, AR1-AR9)
description: Module 38 complete — InstrumentCache + AccountRegistry + CSV configs + wiring; 62 new tests; 1261 total
type: project
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
Module 38 is built and locked.

**Files created:**
- `core/instrument_cache.py` — InstrumentRow frozen dataclass + InstrumentCache (CSV-backed, O(1) by symbol/token)
- `core/account_registry.py` — AccountRow frozen dataclass + AccountRegistry (validates exactly 1 primary)
- `core/exceptions.py` — added InstrumentNotFoundError(TradingSystemError)
- `config/instruments.csv` — 5 equity stubs: RELIANCE, TCS, INFY, HDFCBANK, SBIN (with sector column)
- `config/accounts.csv` — 1 primary Zerodha account row
- `scripts/refresh_instruments.py` — Kite Connect downloader (IC12); --dry-run mode; atomic write

**Files modified:**
- `utils/startup_checks.py` — instruments.csv + accounts.csv added to required files; clock_skew tolerance_sec param (HIGH #5)
- `capital/position_sizer.py` — IC7: auto-resolves lot_size from cache when caller passes default (1)
- `orders/order_placer.py` — IC8: set_instrument_cache() + _round_to_tick() (floor to tick); product_resolver HIGH #7
- `broker/zerodha_adapter.py` — IC9: optional account_id param (no-op v2)
- `signals/signal_processor.py` — accepts instrument_cache param
- `main.py` — Phase 0e-pre block loads both CSVs; sector_lookup_fn wired (HIGH #2); set_token_map (BLOCKER #11)

**Audit items closed by this module:**
- BLOCKER #11: candle_store.set_token_map(instrument_cache.token_map()) — now wired in main.py Phase 0g
- HIGH #2: sector_lookup_fn=lambda sym: instrument_cache.sector(sym) — replaces useless lambda

**Test files:**
- `tests/unit/test_instrument_cache.py` — 28 tests (IC3-IC15)
- `tests/unit/test_account_registry.py` — 20 tests (AR1-AR9)
- `tests/unit/test_instrument_cache_integration.py` — 14 tests (IC7 position_sizer lot_size, IC8 tick rounding)

**Why:** 62 new tests; total suite 1261 green (was 1199 before Phase C+D).

**How to apply:** InstrumentCache is the authoritative source for symbol→token, lot_size, tick_size, sector lookups. AccountRegistry is loaded in main.py Phase 0e-pre; both CSVs must exist in config/ or startup exits with code 3.
