---
name: NSE Reference Data Integration built and locked (RI1-RI15, Task 3)
description: refresh_instruments.py rebuilt to merge security master + sector CSVs + Kite API; 1411 tests green
type: project
originSessionId: 12ead290-f026-42d3-ba03-9f10c51a1a9c
---
# Task 3: NSE Reference Data Integration — BUILT AND LOCKED

**Locked decisions:** RI1-RI15
**Test count:** 1411/1411 green (was 1394; +17 new tests)

## What Changed

### scripts/refresh_instruments.py (full rewrite)
Old behavior (IC12a): only refreshed tokens for symbols already in instruments.csv.
New behavior (RI1): builds full ~2800-row instruments.csv from three sources.

**New pure functions:**
- `_load_security_master(path) -> list[str]` — EQ-series symbols from security master; filters out SME/special series; field key `' series'` (leading space) in CSV
- `_load_sector_map(index_dir) -> dict[str, str]` — sector assignments from 12 sector index CSVs; loaded in priority order (PSU_BANK/PRIVATE_BANK last = wins over BANK on conflict, RI5)
- `_load_fno_set(index_dir) -> frozenset[str]` — FNO symbols from fno_symbols.csv; empty frozenset if file absent
- `_build_kite_lookup(kite_instruments) -> dict[str, dict]` — filters to NSE/NSE-EQ segment
- `_build_rows(symbols, sector_map, fno_set, kite_lookup, verbose) -> tuple[list[dict], list[str]]` — merges all sources; missing Kite symbols get token=0, lot=1, tick=0.05 (RI12)

**Kept functions:**
- `_write_csv(csv_path, rows)` — atomic write (RI6)
- `_fetch_kite_instruments(api_key, access_token, exchange)` — Kite API call (RI4)

**New functions:**
- `_resolve_credentials(args)` — with `--account`: loads api_key from api_key_env + access_token from token file; without: env vars ZERODHA_API_KEY/ZERODHA_ACCESS_TOKEN (RI8)

**CLI changes:**
- Added: `--account`, `--verbose`, `--security-master`, `--index-dir`
- Kept: `--csv`, `--dry-run`
- `main()` now takes `argv=None` for testability
- Returns int exit code (0=success, 1=config/sanity error, 2=API/auth error) — RI14
- Sanity check: returns 1 if built rows < 1000 (RI7)

## Source Files
- Security master: `config/reference_data/security_master_file.csv` — 2801 data rows; `' series'` field (leading space)
- Sector indices: `config/reference_data/index_members/` — 12 sector CSVs + 4 market-cap + fno_symbols.csv (17 total)
- Sector priority: BANK → (others) → PRIVATE_BANK → PSU_BANK (ascending priority)

## New Test Fixtures
- `tests/fixtures/reference_data/security_master_small.csv` — 4 EQ + 1 SME row
- `tests/fixtures/reference_data/index_members/nifty_it.csv`
- `tests/fixtures/reference_data/index_members/nifty_bank.csv`
- `tests/fixtures/reference_data/index_members/nifty_private_bank.csv`
- `tests/fixtures/reference_data/index_members/fno_symbols.csv`

## New Test File
`tests/unit/test_refresh_instruments.py` — 17 tests covering all RI1-RI15 decisions.

## core/instrument_cache.py
No changes needed — InstrumentRow already had all 7 fields including sector (IC3).

## Next Steps
Task 3 complete. Rama begins paper trial.
Remaining build work (after paper trial): Phase H chaos tests, v2.1 features.

## Why
- Security master as authoritative source avoids manually curating symbols list
- Sector from index CSVs enables risk bucketing by sector in screener/risk engine
- FNO set from Kite's fno_symbols.csv is more accurate than security master fno_stock column
