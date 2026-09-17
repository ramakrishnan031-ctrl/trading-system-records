---
name: Entry gate module built and locked (EG1-EG15)
description: Module 31 — screening/entry_gate.py price-based pullback gate; 46 tests green; 948 total
type: project
originSessionId: fc58fdb1-62db-42d0-abf8-209c7761d163
---
Files created (NEW module):
- screening/entry_gate.py
- tests/unit/test_entry_gate.py (46 tests)

Locked decisions: EG1-EG15

Key components:
- WatchEntry frozen dataclass (EG3): signal_id, symbol, direction, trigger_price, entry_price,
  sl_price, tgt_price, tolerance_pct, timeout_sec, strategy_name, tier, scanner_name, intent,
  added_at (naive IST), extras (dict)
- EntryGate class: constructor takes quote_fn, logger, state_store, on_release, poll_interval_sec=5.0,
  worker_count=2 (EG2)
- Public API (EG4): add(), remove(), watchlist(), size(), start(), stop(), is_running()
- Poll loop (EG8): main thread snapshots watchlist under lock, workers check entries concurrently
  via ThreadPoolExecutor; futures awaited with timeout=poll_interval_sec+2.0
- _check_one() logic order (EG5/EG6/EG9): 1) idempotency check; 2) TIMEOUT; 3) quote fetch;
  4) price trigger (lower <= ltp <= upper)
- Release reasons -> state_store statuses: PRICE_HIT -> GATE_RELEASED_PRICE_HIT,
  TIMEOUT -> GATE_RELEASED_TIMEOUT, QUOTE_UNAVAILABLE -> GATE_RELEASED_QUOTE_UNAVAILABLE
- _release() is atomic: removes from watchlist under lock before calling on_release (EG11/EG7)
- _MAX_QUOTE_FAILURES = 3; skip 1-2 failures with warning; release on 3rd (EG9)
- quote_failures dict reset on success and on remove() (EG9/EG11)
- No broker import; quote_fn injected (EG13, Layer 5 screening/)

Test design notes:
- Most tests call _check_one() directly for determinism
- 2 integration tests use gate.start()/stop() with poll_interval_sec=0.05 and threading.Event
- _in_zone_quote() / _outside_zone_quote() helpers for price zone testing
- WatchEntry.added_at set via now_ist().replace(tzinfo=None) (naive IST convention)

Deviations: None.

**Why:** Pullback wait mechanism (P11a) — holds signals until price retraces to entry zone,
preventing chasing entries. Timeout and quote-fail paths ensure entries don't stall forever.
**How to apply:** EntryGate is wired by Module 33 (main.py). gate.add(WatchEntry(...)) called
from signal_processor when strategy.pullback_wait_enabled=True. on_release callback resumes
the post-gate pipeline.
