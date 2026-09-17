---
name: main.py orchestrator built and locked (MAIN1-MAIN25)
description: main.py top-level orchestrator + continue_from_gate() + get_server_time(); 58 new tests; 1107 total
type: project
originSessionId: 657b84bc-8102-4180-b1a5-946a01b3f62f
---
Module: main.py orchestrator (MAIN1-MAIN25)
New tests: 58 (test_main.py)
Running total: 1107 across 38 suites
Schema: unchanged (v8)

**Cross-module extensions:**
- `signals/signal_processor.py`: added `continue_from_gate(entry: object)` — resumes post-screening pipeline (Steps 5-8: sizing, risk, reserve, place) for a WatchEntry released by EntryGate; skips Steps 1-4; re-checks kill-switch + market-window as last-mile gate; typed `object` to avoid circular import
- `broker/zerodha_adapter.py`: added `get_server_time() -> datetime` — paper mode returns `now_ist()` directly; live mode pings `kite.margins()` then returns `now_ist()`; required by `startup_checks.check_clock_skew()`

**Startup phase sequence (MAIN3):**
0a (logging) → 0b (config) → 0c (store+bus+killswitch+timeauth+scenario) → 0d (startup checks) → 0e (21 subsystems) → 0f (startup reconciliation) → 0g (start threads) → 0h (mark complete)

**Key implementation details:**
- `_shutdown_event = threading.Event()` module-level; `_install_signal_handlers` mock sets it to unblock `wait()` in tests
- `_write_session()` private helper uses `store.transaction()` raw SQL (`INSERT OR REPLACE INTO session`) — StateStore has no `upsert_session()` method
- `_init_time_authority()` private helper wraps `time_authority.configure()` — no `initialize_time_authority()` function exists
- broker_adapter built in Phase 0d (before startup checks) then reused in Phase 0e
- `_make_gate_release_cb(signal_processor)` → calls `signal_processor.continue_from_gate(entry)` only on `reason == "PRICE_HIT"`; TIMEOUT/QUOTE_UNAVAILABLE log-only
- `EodSquareoff.start_polling(poll_interval_sec)` daemon thread satisfies MAIN14 directly

**Deviations from spec:**
- `app_config.system` (SystemConfig) — spec said `app_config.system_config`; actual attribute is `.system`
- `StateStore` has no `upsert_session()` — used `_write_session()` with raw SQL via `store.transaction()`
- No `initialize_time_authority()` function — wrapped as `_init_time_authority()` calling `time_authority.configure()`
- `FundManager` has no `on_order_filled`/`on_position_closed` event handler methods — MAIN9 subscriptions for those skipped; only `KillSwitchActivated` and `CapitalDriftDetected` subscribed
- Public `reconcile_once()` used (not private `_reconcile()` as spec said); `reconciler.start()` also calls it internally → two passes at startup, harmless

**Test infrastructure:**
- `_FAKE_ENV` dict with ZERODHA_API_KEY, ZERODHA_ACCESS_TOKEN, TELEGRAM_BOT_TOKEN, WEBHOOK_SECRET
- `_run()` helper: `patch.dict("os.environ", _FAKE_ENV)` + `patch.multiple("main", **patches)` with bare attribute keys (no "main." prefix)
- `_install_signal_handlers` mock side_effect immediately sets `_shutdown_event` to unblock runtime wait

**Why:** Top-level orchestrator wires all 21 subsystems and phases; needed for system to actually run end-to-end.
**How to apply:** main.py is the single entry point; all phase/wiring decisions above are locked; do not add `upsert_session` or `initialize_time_authority` — use the private helpers already in place.
