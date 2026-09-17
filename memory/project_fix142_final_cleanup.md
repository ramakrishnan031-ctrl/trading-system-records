---
name: project-fix142-final-cleanup
description: FIX-142 — final pre-live cleanup; all deferred items addressed; 2682 tests; commit aaf2a99
metadata: 
  node_type: memory
  type: project
  originSessionId: e51e9270-0d6d-4042-b121-32464f9034f0
---

FIX-142 landed 2026-06-01 (commit aaf2a99, pushed to VM).

**Implemented:**
- L8: smart_tgt.max_modify_failures configurable (was hardcoded 3); SmartTgtConfig field + main.py wiring
- Gemini log review: `scripts/gemini_log_review.py` — cron 16:20 IST; WARNING+ extraction → Gemini API → reports/log_review/
- I.2: CandleStore.get_candles docstring: "Newest-last (chronological order)"

**Verified already-done (no changes needed):**
- H5: SL/TGT legs already tracked by order_monitor; exit legs exempt from fill_timeout (line 1067)
- B.2: _check_hit already falls back to LTP when bid=0 AND ask=0
- L6: KillSwitch.resume already requires (reason, resumed_by) with validation
- A.5: alert_watcher already wraps config load in try/except returning 1
- H8: requests in requirements.txt
- L3: stamp_duty from broker_costs.yaml
- C.3: tick queue full → soft_kill (no silent drops)
- L7: no misleading "placed at broker" messages in paper mode

**Permanently skipped (confirmed not needed for v2):**
- L9: BSE exchange (NSE-only)
- L10: ATR real calculation (FIXED_PCT fallback working)
- Full Decimal migration (round(x,2) working)
- Positional bucket (disabled, no strategies active)
- Schema migration framework (delete-DB-on-upgrade)

**Why:** Comprehensive final pass before micro-live to close all deferred items.

**How to apply:** All pre-live items now addressed. System ready for paper testing → live transition. Only AF-1 TEMP values remain (7 config values to revert before capital increase — see [[project-fix140-audit-fixes]]).

**Test count:** 2682 passed, 0 failures.
