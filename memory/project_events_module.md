---
name: Events module built and locked (EV1–EV6)
description: core/events.py complete; EV1–EV6 locked in docs/locked_decisions.yaml; 19/19 tests green
type: project
originSessionId: fed36863-cc65-4721-ae69-4940be7f7ec0
---
core/events.py is built and green as of 2026-04-15.

**What was built:**
- `EventDispatchError` added to `core/exceptions.py` (parent: TradingSystemError, SEVERITY: ERROR)
- `core/events.py`: synchronous EventBus, base `Event` dataclass, 4 seeded event types
- `tests/unit/test_events.py`: 19 tests, all passing
- EV1–EV6 locked into `docs/locked_decisions.yaml` under `events_module:` section
- `test_exceptions.py` stays at 14/14 after adding EventDispatchError

**Key design choices (locked):**
- EV1: Synchronous in-process, same thread, no queue/async
- EV2: Explicit `bus.subscribe(EventType, handler)`, no decorator
- EV3: Base `Event` has `event_id` (uuid4 hex, auto), `ts` (IST, auto), `source_module` (caller), `payload: dict`
- EV4: Collect-all-errors-then-raise; every subscriber invoked; logs each failure; raises `EventDispatchError` at end
- EV5: Invocation order = registration order, but not a contract
- EV6: `OrderFilled`, `PositionClosed`, `KillSwitchActivated`, `CapitalDriftDetected` — no others

**Why:** Only fan-out events (3+ subscribers) use the bus per G9. Direct calls everywhere else.

**How to apply:** When wiring the system in main.py, use explicit bus.subscribe() calls. Do not add new event types without a confirmed 3+ subscriber use case.
