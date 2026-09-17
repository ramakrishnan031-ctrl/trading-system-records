---
name: Symbol alias system (07-May-2026)
description: Chartink->Zerodha symbol name mapper to handle abbreviations; TVSSCS→TVSSRICHAK working; 123 failed symbols analyzed
type: project
originSessionId: 8d4b49f4-9836-4656-b34b-38dfd2f0f22d
---
## Symbol Alias Mapper — 07-May-2026

### Problem
Chartink webhook sends abbreviated symbol names that don't match Zerodha's official symbols.
Example: Chartink sends `TVSSCS`, Zerodha calls it `TVSSRICHAK` (TVS Supply Chain Solutions).

### Solution (commits ff5bb36 + 3975e75 + 4fcf984)
1. **config/symbol_aliases.yaml** — YAML mapping of chartink_name: zerodha_name
2. **main.py _make_paper_quote_provider()** — translates symbols on fetch, reverse-translates in response
3. **scripts/find_symbol_aliases.py** — bulk discovery tool using fuzzy matching

### Current Aliases
- TVSSCS → TVSSRICHAK (confidence 0.95, prefix match)

### Investigation Results (07-May logs)
- 123 symbols failed quote fetch in 1 hour
- Analysis: 120 are exact matches in instruments.csv (NOT name mismatches)
- Root cause: Mass event during cold start — Kite API partial responses before rate limit fix
- After API serialization fix (commit 69b4fc4): only TVSSCS fails (name mismatch)
- Post-alias deployment: TVSSCS works (tested, LTP ₹3964.9)

### Usage
```bash
# Extract failed symbols from logs
grep "No quote returned for" logs/system_*.log | grep -oP "for \K[A-Z0-9]+" | sort -u > failed.txt

# Find potential matches
python scripts/find_symbol_aliases.py < failed.txt

# Review output and add high-confidence matches to config/symbol_aliases.yaml
```

### Partial Response Logging
Added in ff5bb36: logs when Kite returns fewer quotes than requested, showing missing symbols.

### Paper/Live Parity
UNIFIED — aliases apply to both paper and live quote providers.

### Known Limitations
- Only handles paper mode quote provider currently
- Live mode uses zerodha_adapter.get_quote() which needs separate alias layer
- No aliases for 2 unmatched symbols: AUTOBEES, EMBDL (likely delisted/invalid)

### Next Actions
- Monitor "partial response" warnings for systematic failures
- Add aliases as new mismatches are discovered
- Post-paper: wire aliases into live mode quote path if needed
