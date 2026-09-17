---
name: EOD square-off module built and locked (EOD1–EOD12)
description: orders/eod_squareoff.py + schema v5 + config section + 32 tests green; key decisions on fire sequence, reservation_id lookup, restart recovery, state_machine deviation
type: project
originSessionId: 71b74f9f-f778-4afc-a071-dfc06bd1328c
---
Module 22: `orders/eod_squareoff.py` built and locked. 32 tests green.

**Why:** Closes all intraday (MIS/CO) positions at 15:17 IST before broker RMS auto-squares at 15:20.

**Locked decisions:** EOD1–EOD12 added to docs/locked_decisions.yaml (total_decisions: 38 → 50).

**How to apply:** When building modules that interact with EOD square-off, refer to EOD1–EOD12 verbatim.

## Files changed

- `orders/eod_squareoff.py` — new file; class `EodSquareoff` + `EodFireResult` dataclass
- `core/schema.sql` — TABLE 12 `eod_squareoff_log` (UNIQUE on fired_date); schema bumped v4→v5
- `core/state_store.py` — `EXPECTED_SCHEMA_VERSION=5`; 5 new helpers: `get_pending_intraday_orders`, `get_open_intraday_positions`, `get_reservation_id_for_signal`, `get_eod_squareoff_log_for_date`, `insert_eod_squareoff_log`
- `core/events.py` — `EodSquareoffComplete` dataclass added (EV8)
- `core/config_loader.py` — `EodSquareoffConfig` Pydantic model; `SystemConfig.eod_squareoff` field
- `config/system_config.yaml` — `eod_squareoff` section (inter_order_delay_ms=500, poll_interval_sec=5, auto_resume_kill_switch=true)
- `tests/unit/test_eod_squareoff.py` — 32 tests (new)
- `tests/unit/test_state_store.py` — 9 new EOD tests; table count 11→12; total 21→30 tests
- `tests/unit/test_events.py` — 2 new EV8 tests; total 22→24 tests
- `tests/unit/test_config_loader.py` — 1 new EOD12 test + eod_squareoff block in stub YAML; total 25→26 tests

## Key design decisions (non-obvious)

**EOD10 deviation:** `state_machine.transition()` is NOT called for cancelled ENTRY orders. `internal_order_id` is not in the DB (OMgr3). Direct `trades.status='CANCELLED'` DB update instead; state machine catches up on next order_monitor poll.

**EOD11:** `reservation_id` is NOT in the trades table (FM6). Must query `fm_ledger` for the most recent RESERVE row matching `signal_id` via `get_reservation_id_for_signal()`.

**EOD3 restart recovery:** If restart between 15:17–15:30 and no log row → recovery fire. If past 15:30 and no log row → CRITICAL log only (broker RMS may have already fired).

**EOD4 kill switch:** Track `_we_set_soft_kill` flag. Only resume kill switch if WE set it (not if operator had pre-existing HARD_KILL).

**Product filter:** Uses `orders.product IN ('MIS', 'CO')` JOIN on `leg='ENTRY'` — no `intent` column in trades.

## Test count at module 22 completion

22 suites: 524/524 passing (standalone runners) + test_order_placer.py: 19/29 via pytest (10 pre-existing Windows encoding failures in print statements, unrelated to EOD work).
