---
name: Integration smoke tests built and locked (IT1-IT12, Module 37)
description: End-to-end smoke tests for the full signal pipeline; two production bugs fixed; 1187 total tests green
type: project
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
Module 37: End-to-end integration smoke tests (IT1-IT12). 9 new tests across 7 scenarios.

**Files created/modified:**
- `tests/integration/sim_kite.py` — SimKiteClient: scriptable quote provider for paper-mode tests; `set_rich_quote()` yields score~85/HIGH tier for vwap_bounce_long
- `tests/integration/conftest.py` — `wired_system` fixture: full paper-mode system wired in tmp SQLite; now_ist() patched in 4 modules; risk_engine max_open_positions=2
- `tests/integration/test_end_to_end_smoke.py` — 7 scenarios: happy path, screener rejection, risk rejection, dedup, kill switch, EOD squareoff, reconciler manual close
- `screening/step_executor.py` — Fixed `_step_10_signal_age`: naive/aware datetime mismatch before subtraction
- `signals/signal_processor.py` — Fixed direction→side conversion: strategy.direction is "LONG"/"SHORT" but sizer/placer expect "BUY"/"SELL"

**Production bugs fixed during integration testing:**
1. `step_executor._step_10_signal_age`: `now_ist() - triggered_at` raised TypeError when one was naive and one was aware. Fixed by harmonizing tzinfo before subtraction.
2. `signal_processor`: passing "LONG"/"SHORT" to PositionSizer.calculate() (expects "BUY"/"SELL") → ValueError → PLACEMENT_FAILED on every real signal. Unit tests used mock strategies with "BUY"/"SELL" so this was never caught. Fixed: `side = "BUY" if _dir in ("LONG", "BUY") else "SELL"`.

**Key wiring facts:**
- `OrderStateMachine(bus=bus)` — constructor takes bus, NOT logger
- `KillSwitch.resume(reason=..., resumed_by=...)` — kwargs, not positional
- `now_ist()` must be patched in 4 modules: `signals.webhook_receiver`, `signals.signal_processor`, `screening.step_executor`, `screening.secondary_screener`
- Terminal signal status after successful placement: `"PROCESSED"` (not "PLACED")
- `RiskEngine.failed_check="OPEN_POSITIONS"` → signal status `"REJECTED_OPEN_POSITIONS"`

**DB seeding pitfalls:**
- `trades.signal_id` has FK → `signals.signal_id`; `INSERT OR IGNORE` silently swallows FK violations — always insert the parent signal row first
- Trades table requires NOT NULL: `strategy`, `order_protocol`, `updated_at` — omitting them causes silent failure with INSERT OR IGNORE
- Use `with store.transaction() as cur:` for seeded inserts (not `store.execute()` which doesn't commit)

**Why:** These are the first tests that exercise the real YAML strategies (direction="LONG"/"SHORT") rather than mock strategies (direction="BUY"/"SELL"), which is how the direction→side bug was caught.

**How to apply:** When seeding trades for tests, always insert signals first. Terminal status for a successful pipeline run is "PROCESSED". RiskEngine check names map directly to signal rejection statuses: `REJECTED_{failed_check}`.

Total tests: 1187 (9 new integration + fixes)
