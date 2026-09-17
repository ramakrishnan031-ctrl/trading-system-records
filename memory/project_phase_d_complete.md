---
name: PHASE D COMPLETE (19-Apr-2026, commit a401f81)
description: Broker robustness phase done; 2 commits (BL-6+BL-19, BL-21); 1597 tests; 4 architectural locks
type: project
originSessionId: c93f2369-8504-410f-b1e7-f229aa13bcb0
---
Phase D ("Broker robustness") completed 19-Apr-2026 with commit **a401f81**.

**Commit chain:**
- `dfc4779` — BL-6 + BL-19 (D.1): 429 exponential backoff at adapter + narrow retry in OrderPlacer
- `a401f81` — BL-21 (D.2): periodic driver for `time_authority.record_broker_skew()` (Path X)

**Test count:** 1576 → 1597 (+21). Integration gate 15/15 green.

**Architectural locks established (do NOT relitigate in Phase E+):**

1. **BL-6** — ZerodhaAdapter detects HTTP 429 via `getattr(exc, "code", None) == 429` (catches any kiteconnect exception carrying `.code == 429`). On 429: calls `rate_limiter.penalize(category, delay)` with exponential backoff (initial 0.2s × 2.0 multiplier, capped 5.0s, ± 0.05s jitter) then raises `BrokerRateLimit429Error`. Per-category `_429_attempts` counter (threading.Lock). Success path resets counter via `_reset_429_attempts`. **ZA11 preserved — adapter still never retries; the penalize freeze IS the backoff.**

2. **BL-19** — OrderPlacer runs a narrow retry loop scoped ONLY to `BrokerRateLimit429Error` (max_placer_retries=3 default). On 429: warn + continue (next `acquire()` blocks on frozen bucket). On exhaustion: `_handle_placement_failure` → trade FAILED + reservation released. **Other `BrokerError` subclasses still get a single attempt per ZA11 / OP7.** No caller-side sleep — enforced by `test_placer_retry_does_not_sleep_directly`.

3. **E5 contract (general, not BL-19-specific)** — typed exception subclasses carry structured data in `self.context` dict, NOT as direct attributes. `TradingSystemError.__init__(self, message: str, **context)` stores kwargs in `self.context`. **Consumers must use `exc.context.get(key)`, not `exc.key`.** Discovered during BL-19 implementation: `rl_exc.delay_sec` raised AttributeError. Phase E callers handling typed exceptions should follow the same pattern.

4. **BL-21 Path X** — `BrokerClockSkewProbe` daemon is a thin driver. It does NOT implement tier logic, thresholds, or callback dispatch. It calls `adapter.get_server_time()` on schedule, measures RTT, and hands the result to `time_authority.record_broker_skew(broker_ts, local_ref_ts=mid)`. The existing G4 4-tier infrastructure (NORMAL/WARN/ALERT/HALT + rolling deque(10) + `on_critical_skew → kill_switch.soft_kill` wired by `main._init_time_authority`) owns everything else. `record_broker_skew()` gained optional `local_ref_ts` kwarg (default None = legacy `now_ist()` behavior). Skipped in paper mode at the main.py wire site.

**Honest caveat locked:** `adapter.get_server_time()` currently returns local time AFTER a broker round-trip (via `kite.margins()` ping), NOT a parsed broker response timestamp. BL-21 therefore measures network-path wall-clock consistency via RTT anomalies, not true broker clock skew. Adequate for paper trial anomaly surfacing. **Phase E or F may upgrade** to parse HTTP Date headers or NTP cross-check for true broker skew measurement.

**Phase D surprises (for the record):**
- Four spec revisions in a row caught by pre-work (B.6, C.3, D.1 ZA11, D.2 G4-already-built). Pre-work pattern is load-bearing — keep it for Phase E.
- D.1: SQLite file-lock issue on Windows required `try/finally` + `store.close()` + `gc.collect()` for TemporaryDirectory cleanup in 4 placer retry tests.
- D.2: G4 infrastructure was ~80% already built; the real gap was "no production caller invokes `record_broker_skew()` periodically," not "we need new tier logic."

**EF statuses still open for Phase E:**
- EF-1: WebhookReceiver config shape mismatch
- EF-2: track-after-persist race in OrderPlacer
- EF-4: paper_capital loose getattr
- EF-5: trades.reservation_id column absent
(EF-3 closed earlier in Phase A.3.d.)

**Next phase pointer:** Phase E (26 H + 5 M + 4 EF = 35 findings). Expected 5-8 themed commits: logging hygiene / time_authority holes / config tightening / paper correctness / deferred EF cleanup. Notable items: `reports/daily_review.py` time_authority bypass; `get_server_time` precision upgrade (optional); accounts.csv paper_capital 5M → 50k (H-26) lives in Phase F commit.
