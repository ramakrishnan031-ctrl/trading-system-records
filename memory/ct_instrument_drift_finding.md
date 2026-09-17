---
name: ct-instrument-drift-finding
description: TATAMOTORS no longer valid — split into TMPV/TMCV; update test symbol lists; check instrument cache handles splits
metadata: 
  node_type: memory
  type: project
  originSessionId: 747e3a2b-a786-42ac-b981-c972cf1017b4
---

TATAMOTORS no longer valid NSE symbol — split into TMPV (Tata Motors Passenger Vehicles) and TMCV (Tata Motors Commercial Vehicles).

**Impact:**
- Crash test signal_injector burst mode uses TATAMOTORS in default symbol list — gets SKIPPED_QUOTE_UNAVAILABLE
- instruments.csv may still list TATAMOTORS if not refreshed post-split
- Symbol alias system (config/symbol_aliases.yaml) may need TATAMOTORS→TMPV mapping if Chartink still sends old name

**Action items:**
1. Update default test symbol lists in signal_injector.py (replace TATAMOTORS with TMPV or another large-cap)
2. Run refresh_instruments.py to get current security master
3. Check if instrument_cache handles renamed/split symbols gracefully (or if stale cache entries cause silent failures)
4. Consider adding corporate action detection to startup_checks (P2, post-crash-test)

**How to apply:** Fix test symbols before Day 2. Instrument cache refresh is a separate task.
