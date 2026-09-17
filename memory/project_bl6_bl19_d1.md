---
name: BL-6 + BL-19 / Phase D.1 landed (19-Apr-2026, commit dfc4779)
description: 429 exponential backoff at adapter via penalize(); OrderPlacer narrow retry loop for 429 only; 1585 tests green
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
Phase D.1 (commit dfc4779, 19-Apr-2026) bundles BL-6 + BL-19.

**BL-6 (broker adapter):** Detects HTTP 429 via `getattr(exc, "code", None) == 429` — catches kex.NetworkException / kex.GeneralException / any exc carrying 429. Computes exponential delay (initial 0.2s × multiplier 2.0, capped 5.0s, ± 0.05s jitter) per category via thread-safe `_429_attempts` counter (threading.Lock). Calls `rate_limiter.penalize(category, delay)` then raises `BrokerRateLimit429Error`. ZA11 intact — adapter still never retries; the penalize freeze IS the backoff.

**BL-19 (order_placer):** Narrow retry loop scoped ONLY to `BrokerRateLimit429Error` (max_placer_retries=3 default). On 429: warn + continue (next acquire() blocks on frozen bucket). On exhaustion: `_handle_placement_failure` → trade FAILED + reservation released. Other `BrokerError` subclasses still get single attempt per ZA11/OP7. **No caller-side sleep** — enforced by `test_placer_retry_does_not_sleep_directly`.

**Why:** Pre-work surfaced spec contradiction with ZA11 ("adapter does NOT retry"). User chose Path A: keep ZA11, reuse `rate_limiter.penalize()` hook, move retry to OrderPlacer.

**How to apply:** Future rate-limit work must respect ZA11 — adapter raises, never sleeps/retries. Use `BrokerRateLimit429Error` distinct from `BrokerRateLimitError` (the latter = client-side bucket exhaustion, former = actual broker 429). Access exception kwargs via `exc.context.get("key")` per E5 contract — they are NOT direct attributes.

**New files / key APIs:**
- `core/exceptions.py`: `BrokerRateLimit429Error(BrokerError)` SEVERITY=WARN
- `core/config_loader.py`: `RateLimitBackoffConfig` (initial_delay_sec, max_delay_sec, max_placer_retries, multiplier, jitter_sec) nested under `BrokerLimitsConfig.rate_limit_backoff`
- `config/broker_limits.yaml`: default block
- `broker/zerodha_adapter.py`: `_is_429`, `_compute_429_backoff_delay`, `_reset_429_attempts`, `_translate_broker_exception`; 7 success sites call `_reset_429_attempts`

**Tests:** 1585 green (+9: 5 adapter BL-6, 4 placer BL-19). Integration gate 15/15.

**Windows gotcha encountered:** placer tests using `TemporaryDirectory` + `StateStore` need `try/finally` with `store.close()` + `gc.collect()` — even the "happy-path" store.close() wasn't enough without finally.
