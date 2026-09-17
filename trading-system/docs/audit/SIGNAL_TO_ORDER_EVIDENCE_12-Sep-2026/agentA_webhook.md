# Agent A: Chartink webhook POST → SignalProcessor dequeue (source trace @970aabf)

**Scope.** From the moment an HTTP request reaches the process until `SignalProcessor._process_one` begins (the per-signal function). Description only.

**Source.** Extract of commit `970aabf` (= origin/main, the files deployed on production) at `scratchpad/src970`. Every `path:line` is **@970aabf** unless stated.

**Provenance.**
- Plain statements were read directly from source @970aabf.
- **INFERENCE** marks anything not read directly from repo source:
  - library/stdlib behaviour, checked against locally installed copies: Flask 3.1.3 and waitress 3.0.2 match the pins in `requirements.txt`; Werkzeug 3.1.8 is **not pinned** and the VM's version is unknown; CPython 3.14 stdlib, VM version unknown;
  - behaviour of Chartink;
  - consequences derived from combining code facts.

**SHA note (running `d3ee69d` vs deployed `970aabf`)**
- `git diff --stat d3ee69d 970aabf` is **empty** for all of these: `signals/webhook_receiver.py`, `core/market_windows.py`, `core/time_authority.py`, `core/state_store.py`, `core/schema.sql`, `core/config_loader.py`, `core/ids.py`, `core/account_registry.py`, `capital/kill_switch.py`, `v3_chain/watchlist_capture.py`, `config/system_config.yaml`, `config/scan_webhook_map.yaml`, `config/symbol_aliases.yaml`, `config/accounts.csv`.
- `main.py` differs only by the Batch-1 EvidenceRecorder wiring: +33 lines at ~3245, plus one kwarg each on the screener and the SignalProcessor. Later line numbers shift. Examples:

  | Item | @970aabf | @d3ee69d |
  |---|---|---|
  | queue | main.py:3402 | :3368 |
  | receiver ctor | :3407 | :3373 |
  | SignalProcessor ctor | :3575 | :3541 |
  | `signal_processor.start()` | :3974 | :3939 |
  | waitress kwargs | :3994 | :3959 |

- `signals/signal_processor.py` differs by evidence-capture additions. In the in-scope region (dispatcher and `_process_one_safe`) the only change is an evidence capture inside the rate-limiter QUEUE_FULL branch. That branch is unreachable in production (S24).
  - Line numbers @d3ee69d: `start` :271, `_dispatcher_loop` :344, `_process_one_safe` :372, `_process_one` :761.

---

## 0. Gate order at a glance

```
TCP → waitress 0.0.0.0:5000 (threads=8) → Flask route POST /webhook/<scanner_name>
  [413 if body > 1 MiB — raised inside request.get_data(), no audit row]            (INFERENCE, library)
  _handle_webhook:  shutting-down 503 → per-IP 429
  _process_request: auth 401 → unknown scanner 404 → EOD route (_handle_eod → 200/400, NEVER enqueued)
                    → kill switch 403 → backpressure 503 → entry window 403
                    → JSON 400 → not-object 400 → numeric cast 400 → missing field 400
                    → scan_name mismatch 400 → triggered_at 400 → stocks/prices not str 400 → length mismatch 400
  per symbol:       alias → REJECTED_EXCLUDED_SYMBOL → INVALID_SYMBOL → INVALID_PRICE → EXPIRED → IN_PROCESS
                    → DUPLICATE (TTL cache) → INSERT signals(status QUEUED)
                         ├ IntegrityError: existing row QUEUE_FULL → re-queue it (ACCEPTED) | else DUPLICATE
                         └ other exception: STORE_ERROR
                    → queue.put_nowait → QUEUE_FULL | ACCEPTED
  response 200 (or 503 if any QUEUE_FULL/STORE_ERROR) → webhook_audit row (finally)
queue.Queue(maxsize=300) → 1 thread "sp-dispatcher" → ThreadPoolExecutor(5 "sp-worker")
  → _process_one_safe → _process_one   ◀── boundary
```

---

## 1. Stages, in execution order

### S0. Boot wiring: queue, receiver, processor, HTTP server (main.py)
- **(a)** `main.py:3402-3404`, `:3407-3415`, `:3575-3623`, `:3974`, `:3979-4000`, `:4002-4054`, `:3747`. MarketWindows is built at `main.py:2317-2329`.
- **(b) Inputs**
  - `app_config`, from `load_all()` at `main.py:2198`.
  - `store` (StateStore) and `kill_switch`.
  - `market_windows`, built from `trading_hours`.
  - env `WEBHOOK_SECRET`.
- **(c) Computation**
  ```python
  signal_queue: queue.Queue = queue.Queue(
      maxsize=app_config.system.signal_queue.capacity
  )
  webhook_receiver = WebhookReceiver(
      signal_queue=signal_queue, state_store=store, config=app_config,
      market_windows=market_windows, kill_switch=kill_switch,
      logger=get_logger("webhook_receiver"),
      secret_token=os.environ.get("WEBHOOK_SECRET"),
  )
  ```
  - `eod_capture` is not passed to the ctor, so it defaults to `None`. It is late-bound by `webhook_receiver.set_eod_capture(pb01_capture_worker)` at `main.py:3747`, inside the watchlist wiring block `main.py:3714-3755`. That block runs because `watchlist.enabled: true` (`system_config.yaml:620`). If the block raises, the worker stays `None`.
  - SignalProcessor ctor (`main.py:3575-3623`) arguments relevant here:
    - `signal_queue=signal_queue`
    - `worker_count=sp_cfg.worker_count` (5)
    - `drain_poll_sec=sp_cfg.drain_poll_sec` (0.1)
    - `in_flight_release_fn=webhook_receiver.release_in_flight`
    - `signal_expiry_sec=app_config.system.signal_queue.expiry_sec` (600)
    - `scan_webhook_map=app_config.scan_webhook_map.scanners`
    - **Not passed:** `rate_limiter`, which defaults to `None` (`signal_processor.py:189`), and `in_flight_heartbeat_fn`, which defaults to `None` (`:172`).
  - Start order:
    1. `order_reconciler.reconcile_once()` (`main.py:3880`); kill-switch abort check at `:3894-3899`.
    2. `signal_processor.start()` (`:3974`).
    3. `entry_gate.start()` (`:3975`).
    4. Waitress thread (`:3988-4000`).
    5. `time.sleep(2)`, then the `/health` self-check (`:4003-4005`).

    So workers are running before the port is bound.
  - Waitress call:
    ```python
    webhook_thread = threading.Thread(
        target=_waitress_serve, args=(webhook_receiver.app,),
        kwargs={"host": wh_cfg.bind_host, "port": wh_cfg.bind_port,
                "threads": 8, "connection_limit": 100},
        name="webhook-server", daemon=True)
    ```
- **(d) Output.** An HTTP listener on `0.0.0.0:5000` served by 8 waitress worker threads.
- **(e) Reject.** None at this stage. Service-level bounds on whether the port exists at all:
  - Holiday/weekend guard returns 0 before any of this (`main.py:2098-2150`).
  - Start window `[08:00, 18:15)` (`main.py:2154-2176`; `SERVICE_START_CUTOFF` `:2001`).
  - Self-exit after `service_window_end` "17:35" (`main.py:4123-4142`; `system_config.yaml:112`).
- **(f)** No decision variables touched.
- **(g) Config and external data**
  - `signal_queue.capacity`=300
  - `webhook.bind_host`="0.0.0.0" and `bind_port`=5000
  - `signal_processor.worker_count`=5 and `drain_poll_sec`=0.1
  - `signal_queue.expiry_sec`=600
  - `watchlist.enabled`=true
  - env `WEBHOOK_SECRET`. It is required at startup via `required_startup_secrets` (`main.py:219-232`) and `main.py:2430`.
- **(h)** LIVE.
- **(i)** No timing measured. Fixed 2 s sleep before the self-check.
- **(j) Failures**
  - The self-check failing does **not** stop the service: CRITICAL log plus sentinel, then "DEGRADED" (`main.py:4006-4054`).
  - **INFERENCE:** an exception inside `_waitress_serve` (e.g. port busy) ends the daemon thread uncaught. The self-check then takes the DEGRADED path.
  - **INFERENCE (waitress 3.0.2 `adjustments.py`), defaults not overridden here:**
    - `channel_timeout=120`
    - `max_request_body_size=1073741824`
    - `backlog=1024`
    - `trusted_proxy=None`
    - `REMOTE_ADDR = channel.addr[0]`, i.e. the TCP peer (`waitress/task.py:528`).

### S1. WebhookReceiver construction (once, at boot)
- **(a)** `signals/webhook_receiver.py:152-252`. Alias loader `:258-292`. Sweeper thread started `:216-220`.
- **(b) Inputs.** The ctor args, plus `config.system.webhook` resolved shape-tolerantly (`:171-176`).
- **(c) Resulting values @970aabf**
  - `_require_hmac = bool(getattr(_webhook_cfg, "require_hmac", False))` gives **False** (`:176`, `:200`).
  - `_in_flight = {}`, `_in_flight_timeout_sec = 60.0`. Hard-coded, not config (`:206-208`).
  - `_dedup_window_seconds = max(60, int(dedup_window_seconds))` gives **300**. `TTLCache(maxsize=10000, ttl=300)` (`:232-238`).
  - Rate limiter `_PerIpRateLimiter(burst=int(60 or 60), refill=float(5.0 or 5.0))`, with `max_ips=8192` (`:241-247`, `:79`).
  - `app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024` (`:251`).
  - Alias map comes from the cwd-relative path `Path("config/symbol_aliases.yaml")`. The unit sets `WorkingDirectory=/home/ubuntu/systems/trading-system` (`deploy/systemd/trading-system.service:10`). Keys and values are upper-cased. Result: `{TVSSCS: TVSSRICHAK, SIGMAADV: SIGMAADV-BE}` (`config/symbol_aliases.yaml:9-10`).
- **(d) Output.** A configured receiver and the Flask `app`.
- **(e) Reject.** The ctor raises `ValueError` only when `require_hmac=True` and there is no secret (`:177-182`). Not the case @970aabf.
- **(f)** Aliases later rewrite the symbol (S18).
- **(g)** `webhook.require_hmac`, `webhook.dedup_window_seconds`, `webhook.per_ip_*`, and `config/symbol_aliases.yaml`.
- **(h)** LIVE.
- **(i)** None.
- **(j) Failures**
  - Alias file missing: WARNING and `{}` (`:266-271`). Parse error: ERROR and `{}` (`:287-292`).
  - Non-int dedup window: 300 is used (`:232-235`).
  - `per_ip_refill_per_sec ... or 5.0` (`:244`): a configured 0.0 is replaced by 5.0, even though the validator accepts `>= 0` (`config_loader.py:637-642`).

### S2. Waitress to Flask routing and body read
- **(a)** Routes are registered at `webhook_receiver.py:360-413`. Handler entry is `:477-481`.
- **(b) Inputs.** HTTP method and path; `request.remote_addr`; raw body.
- **(c) Computation**
  ```python
  @app.route("/webhook/<scanner_name>", methods=["POST"])
  def webhook(scanner_name: str):
      return receiver._handle_webhook(scanner_name)
  ...
  start_mono = time.monotonic()
  source_ip: str = request.remote_addr or "unknown"
  raw_body: bytes = request.get_data()
  payload_size: int = len(raw_body)
  ```
  - The only other route is `GET /health` (`:364-404`). It shares the per-IP limiter and `_authenticate(b"")`.
  - `@app.errorhandler(500)` logs CRITICAL and returns `{"error": "Internal server error"}` (`:410-413`).
  - No `before_request` hooks or blueprints exist; grep over `main.py`, `signals/`, `ops/`, `utils/` and `core/`.
- **(d) Output.** `scanner_name`, which can be any path segment without `/` and is not validated here, plus `source_ip`, `raw_body` and `payload_size`.
- **(e) Rejects before the handler (INFERENCE, library)**
  - A body over MAX_CONTENT_LENGTH makes `request.get_data()` at `:480` raise `RequestEntityTooLarge`, giving **413**. This happens before the `try/finally` at `:510`, so **no webhook_audit row** is written and this module logs nothing. Checked against Flask 3.1.3 `Request.max_content_length` and Werkzeug 3.1.8 `get_input_stream`/`LimitedStream`.
  - Non-matching method or path (e.g. `GET /webhook/x`, `/webhook/a/b`) gets 405/404 from Flask without entering `_handle_webhook`, so no audit row.
- **(f)** None.
- **(g)** MAX_CONTENT_LENGTH (a code constant).
- **(h)** LIVE.
- **(i)** `start_mono` is captured here; it feeds `duration_ms` in S21.
- **(j)** See (e).

### S3. Shutting-down gate
- **(a)** `webhook_receiver.py:485-490`. The flag is set by `stop()` (`:1166-1176`), which `main.py:1684-1688` calls before `signal_proc.stop()` (`:1689-1692`).
- **(b) Input.** `self._shutting_down` (threading.Event).
- **(c) Computation**
  ```python
  if self._shutting_down.is_set():
      duration_ms = int((time.monotonic() - start_mono) * 1000)
      self._write_audit(scanner_name, source_ip, payload_size, 503, 0, 0, duration_ms)
      return jsonify({"error": "Service shutting down; retry later"}), 503
  ```
- **(d)/(e)** HTTP **503** `{"error": "Service shutting down; retry later"}`, with an audit row (503, 0, 0).
- **(f)** None.
- **(g)** None.
- **(h)** LIVE.
- **(i)** `duration_ms`.
- **(j)** Audit failure is swallowed (S21).

### S4. Per-IP rate limiter (token bucket)
- **(a)** Gate at `webhook_receiver.py:495-504`. Class at `:69-108`.
- **(b) Input.** `source_ip`; `time.monotonic()`.
- **(c) Computation**
  ```python
  if b is None:
      if len(self._buckets) >= self._max_ips: self._evict_idle(ts)
      self._buckets[ip] = [self._burst - 1.0, ts]; return True
  tokens = min(self._burst, b[0] + (ts - b[1]) * self._refill)
  if tokens < 1.0: b[0], b[1] = tokens, ts; return False
  b[0], b[1] = tokens - 1.0, ts; return True
  ```
  - A new IP starts with 59 tokens. Refill is 5.0 per second, capped at 60.
  - Eviction runs only when a new IP arrives and at least 8192 buckets exist. It removes only buckets idle for more than 60 s (`:102-108`).
- **(d)/(e)** Deny gives **429** `{"error": "Rate limit exceeded; slow down"}`, an audit row (429, 0, 0), and a WARNING log `"webhook/%s: per-IP rate limit exceeded for %s -> 429"`.
- **(f)** None.
- **(g)** `webhook.per_ip_rate_limit_enabled`=true, `per_ip_burst`=60, `per_ip_refill_per_sec`=5.0.
- **(h)** LIVE.
- **(i)** Uses monotonic time; nothing is recorded.
- **(j)** No exception path of note.
- **Notes**
  - One token is spent per HTTP request, whatever the number of symbols.
  - The same limiter instance gates `GET /health` (`:379`), so one IP's `/health` calls and POSTs share a bucket.
  - The key is the TCP peer. **INFERENCE (waitress):** no proxy trust is configured.

### S5. Authentication (401)
- **(a)** Call at `webhook_receiver.py:547-549`. `_authenticate` at `:298-354`.
- **(b) Inputs**
  - `self._secret`, from env `WEBHOOK_SECRET` (`main.py:3414`).
  - Header `X-Webhook-Signature`.
  - Query `?token=`.
  - `raw_body`.
- **(c) Computation**
  ```python
  if not self._secret: return True, ""
  sig_header = request.headers.get("X-Webhook-Signature", "")
  token_param = request.args.get("token", "")
  if sig_header.startswith("sha256="):
      expected_hex = _hmac.new(self._secret.encode(), hmac_payload, hashlib.sha256).hexdigest()
      if not _hmac.compare_digest(sig_header[7:], expected_hex): return False, "HMAC signature mismatch"
      return True, ""
  if self._require_hmac: return False, ("HMAC signature required (require_hmac=True); token param is not accepted")
  if token_param:
      if not _hmac.compare_digest(token_param, self._secret): return False, "Invalid token"
      return True, ""
  return False, "Missing auth: provide X-Webhook-Signature header or ?token= param"
  ```
  - A header that does not start with `sha256=` is ignored, and the token path is used.
  - A bad signature is **not** rescued by a valid token.
  - The `require_hmac` branch cannot be reached @970aabf (`require_hmac: false`).
- **(d)/(e)** Failure gives **401** `{"error": <one of the reason strings above>}`.
- **(f)** None.
- **(g)**
  - `webhook.require_hmac`=false (`system_config.yaml:336`).
  - The secret, from env. `required_startup_secrets` makes it mandatory at boot, so `not self._secret` is a test-only path (comment `:326-329`).
- **(h)** LIVE.
- **(i)** None.
- **(j)** **INFERENCE (stdlib):** `hmac.compare_digest` raises TypeError for non-ASCII `str`. That propagates to `_handle_webhook`'s `except Exception`, giving **500**, not 401.

### S6. Unknown scanner (404)
- **(a)** `webhook_receiver.py:552-554`.
- **(b) Input.** `scanner_name` from the URL path; `self._config.scan_webhook_map.scanners`, a dict of `ScannerEntry`.
- **(c) Computation**
  ```python
  known_scanners = self._config.scan_webhook_map.scanners
  if scanner_name not in known_scanners:
      return jsonify({"error": f"Unknown scanner: {scanner_name!r}"}), 404
  ```
  Exact, case-sensitive key match.
- **(d)/(e)** **404** `{"error": "Unknown scanner: '<name>'"}`.
- **(f)** None.
- **(g)** `config/scan_webhook_map.yaml`: 16 keys, listed in §2.
- **(h)** LIVE.
- **(i)/(j)** None.

### S7. EOD routing → `_handle_eod` (never reaches the order path)
- **(a) Locations**
  - Route: `webhook_receiver.py:562-564`.
  - `_handle_eod`: `:751-804`.
  - `_parse_eod_triggered_at`: `:836-851`.
  - `_record_eod_heartbeat`: `:806-834`.
  - Worker: `v3_chain/watchlist_capture.py:106-118` (submit), `:121-134` (loop), `:136-189` (capture).
- **(b) Inputs.** The scanner entry's `scanner_type`; `raw_body`; `self._eod_capture`.
- **(c) Computation**
  ```python
  _entry = known_scanners.get(scanner_name)
  if getattr(_entry, "scanner_type", "intraday") == "eod":
      return self._handle_eod(scanner_name, raw_body)
  ```
  Only `pb01_breakout_retest` has `scanner_type: eod` (`scan_webhook_map.yaml:81-84`). Inside `_handle_eod`:
  1. `json.loads`. Failure gives 400 `"Malformed JSON: <exc>"`. A non-dict gives 400 `"Request body must be a JSON object"`.
  2. Keys `stocks`, `trigger_prices`, `triggered_at` must all be present. Otherwise 400 `"Missing required field: '<f>'"`.
  3. `triggered_at` is tried with `"%Y-%m-%d %H:%M:%S"`, `"%Y-%m-%d"`, `"%I:%M %p"`, `"%H:%M"`. Time-only values get today's IST date. The result is IST-aware. Failure gives 400 `"Invalid triggered_at"`.
  4. `stocks` must be a `str`. Otherwise 400 `"stocks must be a comma-separated string"`. Then `symbols = [s.strip() for s in stocks_raw.split(",") if s.strip()]`.
  5. If `self._eod_capture is None`: WARNING log, heartbeat `FAILED`/`func=DISABLED`, and **200** `{"accepted": 0, "captured": 0, "detail": "watchlist disabled"}`.
  6. Otherwise, per symbol: alias lookup, then `self._eod_capture.submit(scanner_name=…, symbol=…, triggered_at=…)`. That is a `put_nowait` onto the worker's **own** `queue.Queue(maxsize=256)` (`watchlist_capture.py:68,81,111`). It returns True/False and increments `captured`.
  7. Heartbeat `record_heartbeat("pb01_capture", status="SUCCESS", functional_status="EMPTY_NO_DATA" if captured == 0 else None)`. This opens a StateStore and inserts a `cron_heartbeat` row, and never raises (`utils/cron_heartbeat.py:80-95`).
  8. Return **200** `{"accepted": len(symbols), "captured": captured}`.
- **(d) Output.** Items on the capture worker's queue. The worker later writes one `pb01_watchlist` row per symbol, on its own thread, only for a settled session and with the LEVEL computed from its own daily candles (`watchlist_capture.py:143-189`).
- **(e) Rejects.** Only the 400s above. **Not applied on this route:** kill switch, backpressure, entry window, numeric cast, `scan_name` check, `excluded_symbols`, in-flight claim, dedup cache, `signals` INSERT, `signal_queue`.
- **(f)** The payload `trigger_prices` is required but **never read**. LEVEL comes from candles (`watchlist_capture.py:153-155`).
- **(g)**
  - `watchlist.enabled`=true, which wires the worker (`main.py:3714-3749`).
  - `watchlist.level_lookback_sessions`=20.
  - `market_windows.market_close` (15:30), used by the settled-only rule.
  - DB tables `pb01_watchlist` (worker) and `cron_heartbeat`.
- **(h)** SHADOW / analysis-only. `_handle_eod` contains no reference to `self._queue`.
  - `WatchlistCaptureWorker`, `Pb01EntryStage` and `Pb01WouldBeRunner` are constructed at `main.py:3728-3746`. Their only arguments are config, store, fetcher, market_windows, logger, now_fn, zone knobs/scoring, regime_runner and `on_confirm`. None of them receives an order_placer, fund_manager, broker adapter or signal_queue.
  - An EOD alert therefore **never reaches `signal_queue` or the SignalProcessor**.
- **(i)** None measured. The audit row's `duration_ms` covers it (S21).
- **(j) Failures**
  - Submit exceptions are caught and logged (`:797-798`).
  - Heartbeat failures are swallowed (`:824-834`).
  - Worker errors are swallowed per item (`watchlist_capture.py:131-134`).
  - A full capture queue makes `submit` return False: "fail-safe miss".
- **Audit effect.** `_handle_webhook` reads `accepted = len(symbols)` and `rejected = 0` from the 200.

### S8. Kill switch (403)
- **(a)** `webhook_receiver.py:567-568`. `KillSwitch.is_active` at `capital/kill_switch.py:510-526`.
- **(b) Input.** The KillSwitch **in-memory** state.
- **(c) Computation**
  ```python
  if self._ks and self._ks.is_active():
      return jsonify({"error": "Kill switch active; signals rejected"}), 403
  ```
  With the default `intent="entry"`, `is_active` returns `self._state in (KillState.SOFT_KILL, KillState.HARD_KILL)`.
- **(d)/(e)** **403** `{"error": "Kill switch active; signals rejected"}`.
- **(f)** None.
- **(g)** The in-memory state, read under a lock. It was loaded from `kill_switch_state` at construction (`kill_switch.py:1004-1041`) and is updated by the mutators. There is no DB read per request.
- **(h)** LIVE.
- **(i)/(j)** None.

### S9. Queue backpressure (503)
- **(a)** `webhook_receiver.py:570-578`.
- **(b) Inputs.** `sq_cfg` = `config.system.signal_queue`; `self._queue.qsize()`.
- **(c) Computation**
  ```python
  capacity: int = sq_cfg.capacity                                          # 300
  q_size = self._queue.qsize()
  bp_threshold = int(capacity * sq_cfg.backpressure_pct)                   # int(300*0.80) = 240
  warn_threshold = int(capacity * getattr(sq_cfg, "warning_pct", 0.60))    # int(300*0.60) = 180 (used only in S20 header)
  if q_size >= bp_threshold:
      resp = jsonify({"error": "Signal queue at capacity; retry later"})
      resp.headers["X-Queue-Depth"] = f"{q_size}/{capacity}"
      return resp, 503
  ```
- **(d)/(e)** **503** `{"error": "Signal queue at capacity; retry later"}` with header `X-Queue-Depth`.
- **(f)** None.
- **(g)** `signal_queue.capacity`=300, `backpressure_pct`=0.80, `warning_pct`=0.60.
- **(h)** LIVE.
- **(i)/(j)** None.
- **Note (INFERENCE, stdlib):** `qsize()` counts only items the dispatcher has not yet taken. The dispatcher (S23) moves each item straight into ThreadPoolExecutor's **unbounded** `queue.SimpleQueue` (`concurrent/futures/thread.py:190`), so a backlog waiting for the 5 workers is not visible to this gate.

### S10. Entry window (403)
- **(a)** Gate at `webhook_receiver.py:581-583`. `MarketWindows.is_entry_allowed` at `core/market_windows.py:143-150`. `is_trading_holiday` at `:93-106`. Construction at `main.py:2317-2329`. Holidays and special sessions come from `main.py:441-470`.
- **(b) Input.** `now = now_ist()`, which is `datetime.now(tz=IST)` with IST a fixed `timezone(+05:30)` (`core/time_authority.py:58-59,94-99`), i.e. the VM system clock.
- **(c) Computation**
  ```python
  # webhook_receiver.py
  now = now_ist()
  if not self._mw.is_entry_allowed(now):
      return jsonify({"error": "Outside entry window"}), 403
  # market_windows.py
  def is_entry_allowed(self, now):
      if self.is_trading_holiday(now): return False
      t = now.time()
      return self.entry_start <= t < self.entry_end
  def is_trading_holiday(self, now):
      d = now.date()
      if d in self.special_sessions: return False
      if d.weekday() >= 5: return True
      return d in self.holidays
  ```
  - `entry_start` = 10:00 (`system_config.yaml:28`) and `entry_end` = 15:00 (`:47`). Allowed window: **[10:00:00, 15:00:00) IST, Mon–Fri**, excluding the 15 dates in `config/nse_holidays_2026.yaml:18-46`:
    - 2026-01-26, 03-03, 03-26, 03-31, 04-03, 04-14, 05-01, 05-28, 06-26, 09-14, 10-02, 10-20, 11-10, 11-24, 12-25.
  - The file is chosen by `nse_holidays_{_date.today().year}.yaml` (`config_loader.py:2449`).
  - `special_sessions`: every line under the key is commented out (`system_config.yaml:117-122`), so the value is None and `_load_special_sessions` returns `{}` (`main.py:456-458`).
  - `is_entry_allowed` uses the global entry times even on a special-session date; only the holiday test consults `special_sessions`.
  - `market_open`, `market_close` and `eod_entry_cutoff` are not read by this method.
- **(d)/(e)** **403** `{"error": "Outside entry window"}`.
- **(f)** The same `now` later supplies the date for time-only `triggered_at` (S15).
- **(g)** Clock; `trading_hours.entry_start`/`entry_end`; holiday file; `special_sessions`.
- **(h)** LIVE.
- **(i)** None.
- **(j)** No exception path. Config ordering is validated at load (`config_loader.py:139-189`).

### S11. JSON parse and object check (400)
- **(a)** `webhook_receiver.py:586-596`.
- **(c) Computation**
  ```python
  try:
      body: dict = json.loads(raw_body)
  except (json.JSONDecodeError, ValueError) as exc:
      self._log.warning("webhook/%s: Malformed JSON: %s | raw=%r", scanner_name, exc, raw_body[:500])
      return jsonify({"error": f"Malformed JSON: {exc}"}), 400
  if not isinstance(body, dict):
      return jsonify({"error": "Request body must be a JSON object"}), 400
  ```
- **(e)** **400** `"Malformed JSON: …"` or `"Request body must be a JSON object"`.
  - **INFERENCE (stdlib):** undecodable bytes raise UnicodeDecodeError, a ValueError subclass, so they land in the same 400.
  - The raw body (first 500 bytes) is logged **unsanitized**.
- **(f)/(g)** None.
- **(h)** LIVE.
- **(i)/(j)** None.

### S12. Numeric cast (400)
- **(a)** `webhook_receiver.py:600-606`. `_cast_numeric_fields` at `:419-471`.
- **(b) Input.** Top-level keys of `body`.
- **(c) Computation**
  - Critical keys `["price", "entry_price"]`: if present and not None, `float(...)`. Failure returns `(False, "critical field {field}={value!r} cannot be cast to float: {exc}")`.
  - Non-critical `["trigger_price", "sl_pct", "target_pct"]`: `float(...)`, or None plus a WARNING.
  - `["qty"]`: `int(...)`, or None plus a WARNING.
- **(d)** `body` is mutated in place.
- **(e)** Failure gives a WARNING log and **400** `{"error": "Invalid payload: <cast_err>"}`.
- **(f)** The cast values are **never read** later. The receiver reads only `stocks`, `trigger_prices`, `triggered_at` and `scan_name`.
- **(g)** None.
- **(h)** LIVE.
- **INFERENCE.** Chartink's payload keys (`stocks`, `trigger_prices`, `triggered_at`, `scan_name`, `scan_url`, `alert_name`, `webhook_url`) contain none of these names. On a Chartink payload this stage is therefore a no-op.

### S13. Required fields (400)
- **(a)** `webhook_receiver.py:609-615`.
- **(c) Computation**
  ```python
  for field in ("stocks", "trigger_prices", "triggered_at"):
      if field not in body:
          self._log.warning("webhook/%s: Missing field %r | body_keys=%r", ...)
          return jsonify({"error": f"Missing required field: {field!r}"}), 400
  ```
  Only key presence is checked; the value can be anything, including null.
- **(e)** **400** `"Missing required field: '<f>'"`.
- **(f)/(g)** None.
- **(h)** LIVE.

### S14. `scan_name` check and account-prefix strip (400)
- **(a)** `webhook_receiver.py:620-633`. `_strip_account_prefix` at `:111-138`. `primary_account_tag` at `core/account_registry.py:273-318`.
- **(b) Inputs.** `body.get("scan_name")` (optional); `scanner_name` (path); the primary account tag from `config/accounts.csv`.
- **(c) Computation**
  ```python
  body_scan_name = body.get("scan_name")
  if body_scan_name is not None:
      normalized_body = body_scan_name.lower().replace(" ", "_")
      compared = _strip_account_prefix(normalized_body)
      if compared != scanner_name:
          self._log.warning(...)
          return jsonify({"error": "scan_name in body does not match scanner_name path param"}), 400
  # _strip_account_prefix:
  tag = (primary_account_tag() or "").strip().lower()
  if not tag or tag == "unknown": return normalized
  for sep in ("-", "_"):
      if normalized.startswith(tag + sep): return normalized[len(tag + sep):]
  return normalized
  ```
  - Only spaces are replaced; hyphens are not.
  - The tag @970aabf is the primary row `LFL836` (`config/accounts.csv:2`), so `"lfl836"`.
  - The tag is cached after the first read. It is read from `<code dir>/../config/accounts.csv`, not the cwd. It never raises and falls back to "UNKNOWN".
- **(e)** **400** `"scan_name in body does not match scanner_name path param"`. A missing or null `scan_name` skips the check.
- **(f)** None.
- **(g)** `accounts.csv`, via `primary_account_tag`.
- **(h)** LIVE.
- **(j)** A **non-string** `scan_name` (e.g. a number) raises AttributeError on `.lower()`. That is caught by `_handle_webhook` and answered **500** "Internal server error" with a CRITICAL log, not 400.

### S15. `triggered_at` parse (400)
- **(a)** `webhook_receiver.py:637-662`.
- **(b) Inputs.** `str(body["triggered_at"]).strip()`; `now` from S10.
- **(c) Computation**
  ```python
  for fmt in ("%Y-%m-%d %H:%M:%S", "%I:%M %p", "%H:%M"):
      try:
          parsed = datetime.strptime(triggered_at_raw, fmt)
          if fmt in ("%I:%M %p", "%H:%M"):
              today = now.date()
              triggered_at = datetime(today.year, today.month, today.day, parsed.hour, parsed.minute, 0)
          else:
              triggered_at = parsed
          if triggered_at.tzinfo is None:
              triggered_at = triggered_at.replace(tzinfo=ist_timezone())
          break
      except ValueError:
          continue
  if triggered_at is None:
      ... return jsonify({"error": "Invalid triggered_at; expected HH:MM am/pm or YYYY-MM-DD HH:MM:SS"}), 400
  ```
- **(d) Output.** An IST-aware datetime.
  - Time-only formats use today's IST date and seconds=0, so they understate the scan second by 0–59 s (derived).
  - The full format keeps the given date and seconds.
- **(e)** **400** as above. ISO `"YYYY-MM-DDTHH:MM:SS"` matches no format, so it gets 400.
  - **No check here** for a future time or a different date. The only age check is per symbol (S19.3), where a future time gives a negative age and **passes**.
  - **INFERENCE (stdlib `_strptime.py:446-486`):**
    - `%p` matching is case-insensitive (subject to locale am/pm strings).
    - A space in the format requires at least one whitespace, so `"10:15am"` fails every format and gets 400.
    - `%I` accepts 1–2 digits.
- **(f)** `triggered_at` becomes tuple element 5 and `signals.triggered_at`, and drives the fingerprint bucket.
- **(g)** Clock.
- **(h)** LIVE.
- **(i)** None.
- **(j)** Only ValueError is expected; it is handled per format.

### S16. `stocks` / `trigger_prices` split (400)
- **(a)** `webhook_receiver.py:665-674`.
- **(c) Computation**
  ```python
  if not isinstance(stocks_raw, str) or not isinstance(prices_raw, str):
      return jsonify({"error": "stocks and trigger_prices must be comma-separated strings"}), 400
  symbols = [s.strip() for s in stocks_raw.split(",")]
  price_strs = [p.strip() for p in prices_raw.split(",")]
  if len(symbols) != len(price_strs):
      return jsonify({"error": "stocks and trigger_prices list length mismatch"}), 400
  ```
  - Pairing is purely positional: `zip(symbols, price_strs)` at `:696`.
  - Empty items are kept. For example, a trailing comma yields a `""` symbol, which becomes INVALID_SYMBOL in S19.
  - **Derived:** a price string containing a comma would be split, and would mis-pair if the counts still matched. Whether Chartink ever sends such values is unknown (**INFERENCE**).
  - There is no cap on the symbol count beyond the 1 MiB body.
- **(e)** **400** with either of the two messages above. The whole request is rejected and no rows are written.
- **(f)** Defines the symbol/price pairs.
- **(g)** None.
- **(h)** LIVE.

### S17. Batch-level values (shared by every symbol in the request)
- **(a)** `webhook_receiver.py:677-690`. Sanitizer at `:857-886`.
- **(c) Computation**
  ```python
  received_at = now_ist()                          # 2nd clock read of the request
  today_iso: str = received_at.date().isoformat()  # -> signals.fingerprint_date
  expiry_sec: int = sq_cfg.expiry_sec              # 600
  stored_payload = self._sanitize_payload_for_storage(raw_body.decode("utf-8", errors="replace"))
  ```
  The sanitizer:
  1. Replaces the literal secret with `<REDACTED>`.
  2. Applies `re.sub(r"token=[^&\"'\s]+", "token=<REDACTED>", …)`.
  3. Blanks the value of the `"webhook_url"` JSON field.
- **(d)** `received_at`, `today_iso`, `expiry_sec` and `stored_payload` are identical for every symbol in the batch.
- **(e)/(f)** None.
- **(g)** Clock; `signal_queue.expiry_sec`=600; the secret.
- **(h)** LIVE.
- **(j)** Cannot raise realistically (`errors="replace"`).

### S18. Per-symbol loop: alias and excluded symbols
- **(a)** `webhook_receiver.py:696-728`.
- **(c) Computation**
  ```python
  for raw_symbol, price_str in zip(symbols, price_strs):
      symbol = self._alias_map.get(raw_symbol.upper(), raw_symbol)
      excluded_symbols = getattr(self._config.system, "excluded_symbols", [])
      if symbol.upper() in [s.upper() for s in excluded_symbols]:
          results.append({"symbol": symbol, "status": "REJECTED_EXCLUDED_SYMBOL"}); rejected_count += 1; continue
      item = self._process_signal(scanner_name, symbol, price_str, triggered_at, received_at, today_iso, expiry_sec, webhook_payload=stored_payload)
      results.append(item)
      if item["status"] == "ACCEPTED": accepted_count += 1
      else: rejected_count += 1
  ```
  - `excluded_symbols` = E2E, GVPIL, BIRLACABLE, SHANKARA, MCLEODRUSS (`system_config.yaml:131-136`).
  - The check is case-insensitive and runs **after** alias resolution.
- **(d)/(e)** `REJECTED_EXCLUDED_SYMBOL` is response-only: DEBUG log, no DB row.
- **(f)** The alias rewrites the symbol for every later use: in-flight key, dedup key, fingerprint, DB row and queue tuple. Non-aliased symbols keep their original case; nothing is upper-cased.
- **(g)** `excluded_symbols`; the alias map.
- **(h)** LIVE.
- **(j)** The loop has **no try/except** (acknowledged in the comment at `:1040-1041`). An exception escaping `_process_signal` abandons the remaining symbols and yields **500** (S21). Symbols already ACCEPTED stay queued.

### S19. `_process_signal` (one symbol)
- **(a)** `webhook_receiver.py:892-1072`. `_claim_in_flight` at `:1074-1091`. `_release_in_flight` at `:1093-1096`.
- **(b) Inputs.** `scanner_name`, `symbol`, `price_str`, `triggered_at`, `received_at`, `today_iso`, `expiry_sec`, `webhook_payload`.
- **(c)–(e) Steps, in order.** Every status is returned in the response `results`.
  1. **Symbol** (`:905-906`): `if not symbol: return {"symbol": symbol, "status": "INVALID_SYMBOL"}`. Only the empty string is rejected. There is **no** format check and **no instrument-cache lookup**; the file's only "instrument" mention is the comment at `:700`.
  2. **Price** (`:909-914`): `price = float(price_str)`. ValueError/TypeError gives `INVALID_PRICE`; `price <= 0` gives `INVALID_PRICE`.
     - Derived: `"nan"` and `"inf"` pass, since `nan <= 0` is False.
     - **INFERENCE (SQLite):** a NaN bound to a REAL column is stored as NULL, so `trigger_price` would be NULL while the tuple carries `nan`.
  3. **Expiry** (`:919-926`):
     ```python
     now = now_ist()
     age_sec = (now - triggered_at_aware).total_seconds()
     if age_sec > expiry_sec: return {"symbol": symbol, "status": "EXPIRED"}
     ```
     - `expiry_sec`=600 and the test is strict `>`.
     - Future `triggered_at` (negative age) passes.
     - This is a third clock read, one per symbol.
  4. **In-flight claim** (`:934-935`): `if not self._claim_in_flight(symbol): return {…"IN_PROCESS"}`.
     - Keyed by **symbol only**, across all scanners.
     - The claim stores `{'acquired_at': mono, 'heartbeat_at': mono}` under `_in_flight_lock`.
  5. **TTL dedup cache** (`:940-947`):
     ```python
     dedup_key = (symbol, scanner_name)
     with self._dedup_lock:
         if dedup_key in self._dedup_cache:
             self._release_in_flight(symbol); return {…"DUPLICATE"}
         self._dedup_cache[dedup_key] = True
     ```
     **INFERENCE (cachetools):** TTL is 300 s from insertion, on a monotonic timer.
  6. **Fingerprint** (`:952-954`):
     ```python
     epoch_bucket = int(triggered_at.timestamp() // self._dedup_window_seconds)   # // 300
     fp_raw = f"{scanner_name}|{symbol}|{epoch_bucket}"
     fingerprint = hashlib.sha256(fp_raw.encode()).hexdigest()
     ```
     Derived: the IST offset of 19,800 s is a multiple of 300, so buckets align to IST 5-minute clock boundaries (hh:mm0–hh:mm4:59).
  7. **IDs and timestamps** (`:957-961`):
     - `signal_id = new_signal_id()`, i.e. `"sig_" + uuid.uuid4().hex` (`core/ids.py:50-52`).
     - `expires_at_dt = received_at + timedelta(seconds=expiry_sec)`.
  8. **INSERT** (`:963-980`): a `signals` row with status `'QUEUED'` (columns in §3). It runs inside `store.transaction()`, which is BEGIN IMMEDIATE, commit or rollback (`core/state_store.py:505-543`). Each thread has its own connection with `busy_timeout=30000` and `synchronous=FULL` (`state_store.py:107-113, 232-237`), and the write is **synchronous on the request thread**.
  9. **`sqlite3.IntegrityError`** (`:981-1015`): the unique index `idx_signals_fingerprint_today ON signals(fingerprint, fingerprint_date)` (`schema.sql:82-83`).
     - First: `SELECT signal_id, status FROM signals WHERE fingerprint=? AND fingerprint_date=?`.
     - If the existing status is **`QUEUE_FULL`**:
       - `put_nowait((existing signal_id, scanner_name, symbol, price, triggered_at))`.
       - If the queue is still full: pop the cache key, release the in-flight claim, return `QUEUE_FULL`.
       - Otherwise run `UPDATE signals SET status='QUEUED' WHERE signal_id=?` (a failure is logged ERROR and swallowed) and return **`ACCEPTED`** with the existing `signal_id`.
     - Otherwise release the in-flight claim and return **`DUPLICATE`**; the cache key is **not** popped.
     - No new row is written in either case.
  10. **Any other exception** on the INSERT (`:1016-1044`): pop the cache key, release the in-flight claim, log CRITICAL `"webhook_receiver: signal store FAILED for %s/%s: %s -- claims released, returning STORE_ERROR so the sender retries"`, and return **`STORE_ERROR`**. No row survives the rollback.
  11. **Queue put** (`:1047-1068`):
      ```python
      entry = (signal_id, scanner_name, symbol, price, triggered_at)
      try:
          self._queue.put_nowait(entry)
      except queue.Full:
          # UPDATE signals SET status = 'QUEUE_FULL' WHERE signal_id = ?   (error logged if it fails)
          # pop dedup cache key; release in-flight
          return {"symbol": symbol, "status": "QUEUE_FULL"}
      ```
  12. **Success** (`:1072`): `{"symbol": symbol, "status": "ACCEPTED", "signal_id": signal_id}`.
      - The in-flight claim is **kept**. It is released by the processor's `_process_one` finally (`signal_processor.py:1267-1269`, outside this trace) or evicted by the sweeper (S22).
- **(f)**
  - `price` is `float(trigger price string)`, with no rounding or adjustment.
  - `symbol` is post-alias.
  - `triggered_at` is as parsed in S15.
  - No qty or side exists at this layer.
  - In the re-queue path (step 9) the tuple carries the **retry's** `price`/`triggered_at`, while the DB row keeps the original values.
- **(g)**
  - DB: `signals` INSERT/SELECT/UPDATE.
  - Clock.
  - `expiry_sec`=600 and `dedup_window_seconds`=300.
  - In-memory in-flight dict and TTL cache.
- **(h)** LIVE.
- **(i)** None measured.
- **(j)** Covered by steps 9–11.
  - The `fetch_one` inside the IntegrityError handler is not wrapped. If it raises, the exception reaches `_handle_webhook` (500), and this symbol's in-flight claim and cache key are **not** released:
    - the cache key expires after 300 s;
    - the in-flight claim stays until the sweeper evicts it.

### S20. Response assembly
- **(a)** `webhook_receiver.py:730-745`. `_RETRYABLE_STATUSES = frozenset({"QUEUE_FULL", "STORE_ERROR"})` at `:66`.
- **(c) Computation**
  ```python
  any_retryable = any(r["status"] in _RETRYABLE_STATUSES for r in results)
  http_status = 503 if any_retryable else 200
  resp = jsonify({"accepted": accepted_count, "rejected": rejected_count, "results": results})
  current_depth = self._queue.qsize()
  resp.headers["X-Queue-Depth"] = f"{current_depth}/{capacity}"
  if current_depth >= warn_threshold:            # 180
      resp.headers["X-Queue-Warning"] = "high"
  return resp, http_status
  ```
- **(d) Output.** Body `{"accepted": int, "rejected": int, "results": [{"symbol", "status"[, "signal_id"]}, …]}`.
  - `rejected` counts every non-ACCEPTED status, including REJECTED_EXCLUDED_SYMBOL.
- **(e)**
  - **503** if any symbol is QUEUE_FULL or STORE_ERROR, else **200**.
  - A batch where every symbol is DUPLICATE, EXPIRED, INVALID or IN_PROCESS still answers **200**.
- **(f)/(g)** `qsize`; `warning_pct` (header only).
- **(h)** LIVE.

### S21. `_handle_webhook` wrap-up and `webhook_audit` row
- **(a)** `webhook_receiver.py:506-534`. `_write_audit` at `:1126-1154`. Schema at `core/schema.sql:581-602`.
- **(c) Computation**
  ```python
  try:
      resp = self._process_request(scanner_name, raw_body)
      response_code = resp[1] if isinstance(resp, tuple) else 200
      if response_code == 200 and isinstance(resp, tuple):
          data = resp[0].get_json(silent=True) or {}
          accepted_count = data.get("accepted", 0); rejected_count = data.get("rejected", 0)
      if response_code == 400:
          self._log.warning("webhook/%s: 400 response | raw_body=%r", scanner_name, raw_body[:1000])
      return resp
  except Exception as exc:
      self._log.critical(f"Unhandled exception processing /webhook/{scanner_name}: {exc}")
      response_code = 500
      return jsonify({"error": "Internal server error"}), 500
  finally:
      duration_ms = int((time.monotonic() - start_mono) * 1000)
      self._write_audit(scanner_name, source_ip, payload_size, response_code, accepted_count, rejected_count, duration_ms)
  ```
  The row is an INSERT of the webhook_audit columns in §3, with `ts = now_ist().isoformat()` taken inside `_write_audit`.
- **(d) Output.** One `webhook_audit` row per request that reaches `_handle_webhook`. S3/S4 write their own rows; every other outcome writes through this `finally`.
- **(e)** Unhandled exceptions give **500** `{"error": "Internal server error"}`.
- **(f)** None.
- **(g)** DB `webhook_audit`; clock.
- **(h)** LIVE, observational.
- **(i)** `duration_ms` is truncated to an int. It covers the request up to just before the audit INSERT, so it **excludes** the audit write itself.
- **(j)** An audit INSERT failure logs ERROR `"Failed to write webhook_audit row: …"` and is swallowed.
- **Notes**
  - Counts are extracted **only for 200**. A batch-level **503** (QUEUE_FULL/STORE_ERROR) is audited as `0/0` even if some symbols were ACCEPTED and queued.
  - An EOD 200 audits `accepted = number of symbols`.
  - The `scanner_name` column holds whatever path segment arrived, including unknown or unauthenticated names.

### S22. In-flight sweeper (background thread; governs S19.4 IN_PROCESS)
- **(a)** `webhook_receiver.py:1182-1207`. Started at `:216-220`; stopped by `stop()` at `:1173`.
- **(c) Computation**
  ```python
  while not self._sweeper_stop.wait(timeout=60.0):
      ... if now_mono - entry['heartbeat_at'] > self._in_flight_timeout_sec: evict   # 60.0
      self._log.critical("in_flight_sweeper: evicted STALLED symbol %s (held=%.0fs, no heartbeat for %.0fs); ...")
  ```
- **Wiring fact.** `heartbeat_at` changes only via `update_heartbeat()` (`:1110-1120`). Its sole production caller would be SignalProcessor's `in_flight_heartbeat_fn`, which **main.py does not pass** (`main.py:3575-3623`). So `SignalProcessor._heartbeat` is a no-op (`signal_processor.py:664-673`), and `heartbeat_at` stays equal to `acquired_at`.
- **Derived.** Any claim still held at a sweep tick more than 60 s after it was taken is evicted with a CRITICAL log, whether or not processing is still running. That means eviction roughly 60–120 s after the claim.
- **(h)** LIVE: it changes which later same-symbol signals get IN_PROCESS.

### S23. Consumer: dispatcher thread
- **(a)** `signals/signal_processor.py:304-324` (start) and `:377-399` (loop).
- **(c) Computation**
  ```python
  self._executor = ThreadPoolExecutor(max_workers=self._worker_count, thread_name_prefix="sp-worker")   # 5
  self._dispatcher_thread = threading.Thread(target=self._dispatcher_loop, name="sp-dispatcher", daemon=True)
  ...
  while not self._stop_event.is_set():
      try:
          signal_tuple = self._queue.get(timeout=self._drain_poll_sec)   # 0.1
      except Exception:  # queue.Empty
          continue
      self._warm_zones(signal_tuple)
      if self._executor is not None:
          self._executor.submit(self._process_one_safe, signal_tuple)
  while True:   # after stop: drain
      try:
          signal_tuple = self._queue.get_nowait()
          if self._executor is not None: self._executor.submit(self._process_one_safe, signal_tuple)
      except Exception: break
  ```
- **(b)/(d)** The consumer is **one** dispatcher thread feeding a pool of **5** workers. The Futures returned by `submit` are discarded.
- **Ordering**
  - The FIFO `queue.Queue` is submitted FIFO into the executor's FIFO work queue.
  - Up to 5 signals run concurrently, so completion order is not guaranteed (**INFERENCE**, stdlib).
- **Blocking**
  - `get(timeout=0.1)`. **INFERENCE (stdlib):** it returns as soon as an item is put, so 0.1 s only bounds the stop-flag re-check latency.
  - `submit` does not block; the executor queue is unbounded.
  - There is **no per-task timeout**: `signal_processor.pipeline_timeout_sec` is read nowhere.
- **(e)** No expiry/age check, no kill-switch/window check and no DB status write at dequeue.
- **`_warm_zones` (`:361-375`)** is a **no-op**. `zone_warmer` is None because the ZoneWarmer block at `main.py:3549` runs only if `sr_detector.wait_for_retest_enabled` (false, `system_config.yaml:529`) or `structure_exit.structure_exit_enabled` (false, `:634`).
- **Other producers onto the same queue**
  - FIX-069 re-queue of a dict `{…, "retry_count"}` on transient broker errors (`signal_processor.py:1510-1520`, inside `_admit_and_place`, out of scope).
  - The rate-limiter re-queue in `_process_one_safe` (`:426`), which is dead (S24).
- **Crash and restart.** Grep of non-test code finds no path that re-enqueues `QUEUED` or `QUEUE_FULL` rows from the DB. The `'QUEUED'` literals occur only at `webhook_receiver.py:977,1005`, in the schema, in reports and in ops_dashboard. Items still in the in-memory queue at a crash are lost, and their rows stay `QUEUED` (derived).
- **(h)** LIVE.
- **(i)** None measured at this stage.
- **(j)** Any `get` exception is treated as empty.

### S24. `_process_one_safe` → boundary (`_process_one`)
- **(a)** `signal_processor.py:405-480`.
- **(c) Computation**
  1. Extract `signal_id` and `symbol` for logs only, from tuple positions [0] and [2] or dict `.get`.
  2. `if self._rate_limiter is not None:` (`:418-461`) is **never entered in production**, because `rate_limiter` is not passed (`main.py:3575-3623`) and defaults to None.
     - That branch contains: `try_acquire("order")`, then `put(signal_tuple, timeout=1.0)`, and on `queue.Full` `update_signal_status(signal_id, "REJECTED", "QUEUE_FULL")`, an evidence capture (970aabf only), and in-flight release.
  3. `_active_workers += 1`, then:
     ```python
     try:
         self._process_one(signal_tuple)
     except Exception as exc:
         self._log.error(f"Unhandled exception in pipeline for {signal_id} ({symbol}): {exc}\n{traceback.format_exc()}")
         try: self._store.update_signal_status(signal_id, "PLACEMENT_FAILED", f"unhandled: {exc}")
         except Exception: pass
     finally:
         with self._active_lock: self._active_workers -= 1
     ```
- **Boundary.** `_process_one` starts at `signal_processor.py:867`. Its first statement is `self._store.update_signal_status(signal_id, "PROCESSING")` (`:897`).
  - Its step 1 re-checks kill switch ("entry"), entry window and age (`triggered_at` + 600 s) at `:905-921`; the next trace covers that.
  - The tuple unpack at `:886` is `signal_id, scanner_name, symbol, trigger_price, triggered_at = signal_tuple`.

---

## 2. Scanner → strategy mapping (`config/scan_webhook_map.yaml:16-84`)

- **Loading.** Loaded as `AppConfig.scan_webhook_map` (`config_loader.py:2447`).
- **Schema.** `ScannerEntry` (`config_loader.py:2347-2371`):
  - `extra="forbid"`;
  - `strategy: str`;
  - `chartink_url: str`, which must start `http(s)://`;
  - `scanner_type: str = "intraday"`, which must be `intraday` or `eod`.
- **Readers**
  - The receiver reads only the **keys** (404, S6) and `scanner_type` (S7).
  - The mapped `strategy` is **not** read by the receiver; `signals.strategy` is written with `scanner_name`.
  - `chartink_url` is read only by the startup connectivity check (`utils/startup_checks.py:651-700`, warning-only).
- **Strategy-YAML columns in the table below** are context only; the receiver does not read them. All 16 YAMLs exist @970aabf.

| # | Scanner key (= URL path) | strategy | scanner_type | chartink_url | strategy YAML @970aabf (context) |
|---|---|---|---|---|---|
| 1 | open_low_breakout_long | open_low_breakout_long | intraday (default) | https://chartink.com/screener/open-low-breakout-long | enabled true, INTRADAY |
| 2 | first_pullback_long | first_pullback_long | intraday (default) | …/first-pullback-long | enabled true, INTRADAY |
| 3 | vwap_bounce_long | vwap_bounce_long | intraday (default) | …/vwap-bounce-long | enabled true, INTRADAY |
| 4 | gap_go_long | gap_go_long | intraday (default) | …/gap-go-long | enabled true, INTRADAY |
| 5 | gap_fade_long | gap_fade_long | intraday (default) | …/gap-fade-long | enabled true, INTRADAY |
| 6 | range_breakout_long | range_breakout_long | intraday (default) | …/range-breakout-long | enabled true, INTRADAY |
| 7 | open_high_breakdown_short | open_high_breakdown_short | intraday (default) | …/open-high-breakdown-short | enabled true, INTRADAY |
| 8 | first_pullback_short | first_pullback_short | intraday (default) | …/first-pullback-short | enabled true, INTRADAY |
| 9 | vwap_rejection_short | vwap_rejection_short | intraday (default) | …/vwap-rejection-short | enabled true, INTRADAY |
| 10 | gap_go_short | gap_go_short | intraday (default) | …/gap-go-short | enabled true, INTRADAY |
| 11 | gap_fade_short | gap_fade_short | intraday (default) | …/gap-fade-short | enabled true, INTRADAY |
| 12 | range_breakout_short | range_breakout_short | intraday (default) | …/range-breakout-short | enabled true, INTRADAY |
| 13 | positional_momentum_long | positional_momentum_long | intraday (default) | …/positional-momentum-long | enabled true, **DELIVERY** |
| 14 | positional_sector_rotation | positional_sector_rotation | intraday (default) | …/positional-sector-rotation | enabled true, **DELIVERY** |
| 15 | positional_swing_long | positional_swing_long | intraday (default) | …/positional-swing-long | enabled true, **DELIVERY** |
| 16 | pb01_breakout_retest | pb01_breakout_retest | **eod** (explicit, `:84`) | …/pb01-breakout-retest | enabled **false**, INTRADAY |

- In all 16 entries the key equals its strategy value.
- The three DELIVERY strategies use `scanner_type` intraday, so they take the same intraday webhook path and window (S10).

---

## 3. Row, tuple and response schemas

**`signals` INSERT** (`webhook_receiver.py:966-979`; table `schema.sql:42-79`):

| Column | Value written | Source |
|---|---|---|
| signal_id | `"sig_" + uuid4().hex` | `new_signal_id()` `core/ids.py:50-52` |
| symbol | post-alias symbol | S18 `:701` |
| scanner | `scanner_name` | URL path |
| strategy | `scanner_name` (not the map's `strategy`) | `:975` |
| triggered_at | `triggered_at.isoformat()`, e.g. `2026-09-11T10:15:00+05:30` | S15 |
| received_at | `received_at.isoformat()` (one per batch) | S17 `:677` |
| expires_at | `(received_at + 600 s).isoformat()` | `:960` |
| status | `'QUEUED'` | `:977` |
| fingerprint | `sha256(f"{scanner}|{symbol}|{floor(ts/300)}")` hex | `:952-954` |
| fingerprint_date | `received_at.date().isoformat()` | `:678` |
| trigger_price | `float(price_str)` | `:910` |
| webhook_payload | sanitized raw body (identical for every symbol in the batch) | S17 |
| rejection_reason, trade_id | not set (NULL) | — |

**Other `signals` writes by the receiver**
- `UPDATE … SET status='QUEUE_FULL'` (`:1053-1056`).
- `UPDATE … SET status='QUEUED'` in the re-queue path (`:1003-1007`).
- Response-only statuses that write **no** row: REJECTED_EXCLUDED_SYMBOL, INVALID_SYMBOL, INVALID_PRICE, EXPIRED, IN_PROCESS, DUPLICATE, STORE_ERROR.

**Queue item.** `(signal_id: str, scanner_name: str, symbol: str, price: float, triggered_at: datetime IST-aware)` on `queue.Queue(maxsize=300)` (`main.py:3402-3404`). The re-queue path puts the same shape with the old `signal_id`.

**`webhook_audit` INSERT** (`webhook_receiver.py:1141-1151`; table `schema.sql:581-593`):

| Column | Value | Source |
|---|---|---|
| id | AUTOINCREMENT | DB |
| ts | `now_ist().isoformat()` at write time, i.e. the end of the request | `:1136` |
| scanner_name | URL path segment, any string | route |
| source_ip | `request.remote_addr or "unknown"` (TCP peer; INFERENCE, waitress) | `:479` |
| payload_size_bytes | `len(raw_body)` | `:481` |
| response_code | status actually returned (503/429/401/404/403/400/200/500) | S3/S4/S21 |
| signals_accepted | `data["accepted"]` only when the code is 200, else 0 | `:514-517` |
| signals_rejected | `data["rejected"]` only when the code is 200, else 0 | `:514-517` |
| duration_ms | `int((monotonic - start_mono) * 1000)`, excluding the audit write | `:530` |
| date | generated: `substr(ts,1,10)` | schema |

**HTTP response**
- 200 or 503.
- JSON body `{"accepted", "rejected", "results": [{"symbol", "status", "signal_id"?}]}`.
- Headers: `X-Queue-Depth: <qsize>/300`; `X-Queue-Warning: high` when `qsize >= 180`.

---

## 4. Config keys read on this path (values @970aabf)

| Key | Location @970aabf | Value | Read at | Changes behaviour? |
|---|---|---|---|---|
| webhook.bind_host | system_config.yaml:328 | "0.0.0.0" | main.py:3992 | Yes: listen interface |
| webhook.bind_port | :335 | 5000 | main.py:3993, 4004 | Yes |
| webhook.require_hmac | :336 | false | webhook_receiver.py:176 | Yes: token fallback allowed; ctor does not demand a secret; the "HMAC required" branch is unreachable |
| webhook.dedup_window_seconds | :337 | 300 | webhook_receiver.py:233-237 | Yes: TTL-cache TTL **and** fingerprint bucket width; floored at 60 |
| webhook.per_ip_rate_limit_enabled | :340 | true | :241 | Yes |
| webhook.per_ip_burst | :341 | 60 | :243 | Yes |
| webhook.per_ip_refill_per_sec | :342 | 5.0 | :244 | Yes. A value of 0 could never apply (`or 5.0`) |
| signal_queue.capacity | :125 | 300 | main.py:3403 (maxsize); receiver :571; /health :397 | Yes |
| signal_queue.backpressure_pct | :126 | 0.80 | :573 | Yes: 503 at qsize ≥ 240 |
| signal_queue.warning_pct | :128 | 0.60 | :574 | Header only (`X-Queue-Warning` at ≥ 180) |
| signal_queue.expiry_sec | :127 | 600 | receiver :679 (EXPIRED check + expires_at); main.py:3614 (processor) | Yes |
| excluded_symbols | :131-136 | E2E, GVPIL, BIRLACABLE, SHANKARA, MCLEODRUSS | :709 | Yes |
| trading_hours.entry_start | :28 | "10:00" | main.py:2321 → market_windows.py:150 | Yes |
| trading_hours.entry_end | :47 | "15:00" | main.py:2322 → market_windows.py:150 | Yes |
| trading_hours.market_close | :104 | "15:30" | EOD capture settled-only check (watchlist_capture.py:220-225) | EOD route only |
| special_sessions | :117-122 | None (all commented) | main.py:2318, 456-458 | No effect today |
| nse_holidays_2026.yaml | :18-46 | 15 dates | main.py:2317, 441-443 | Yes: holiday gives 403 |
| scan_webhook_map.scanners (keys) | scan_webhook_map.yaml:16-84 | 16 keys | webhook_receiver.py:552; processor main.py:3585 | Yes: 404 |
| scan_webhook_map.*.scanner_type | :84 (pb01 only) | eod / default intraday | :562-563 | Yes: EOD routing |
| scan_webhook_map.*.strategy | per entry | = key | not read by the receiver | No (on this path) |
| scan_webhook_map.*.chartink_url | per entry | Chartink URLs | startup check only | No (on this path) |
| watchlist.enabled | :620 | true | main.py:3477-3478 | Yes: EOD capture worker wired |
| watchlist.level_lookback_sessions | :623 | 20 | watchlist_capture.py:155 | EOD worker only |
| signal_processor.worker_count | :345 | 5 | main.py:3590 → sp:311 | Yes |
| signal_processor.drain_poll_sec | :346 | 0.1 | main.py:3591 → sp:385 | Only the stop-flag latency (INFERENCE, stdlib) |
| signal_processor.pipeline_timeout_sec | :347 | 30 | **nowhere** (validated only, config_loader.py:602-607) | **No** |
| sr_detector.wait_for_retest_enabled | :529 | false | main.py:3423 | Makes `_warm_zones` a no-op |
| structure_exit.structure_exit_enabled | :634 | false | main.py:3427 | Same |
| config/symbol_aliases.yaml | :9-10 | TVSSCS→TVSSRICHAK, SIGMAADV→SIGMAADV-BE | webhook_receiver.py:265-292 | Yes: symbol rewrite |
| config/accounts.csv (is_primary row) | :2 | LFL836 → tag "lfl836" | account_registry.py:277-299 via :129 | Only for `scan_name` values carrying that prefix |
| env WEBHOOK_SECRET | .env | (secret) | main.py:3414 | Yes: auth and sanitizer |
| Code constants | webhook_receiver.py:251, :208, :237, :79; main.py:3994-3995; watchlist_capture.py:68 | MAX_CONTENT_LENGTH 1 MiB; in-flight timeout 60 s; TTLCache maxsize 10000; max_ips 8192; waitress threads 8 / connection_limit 100; capture queue 256 | — | Yes (not config) |

**Keys not read on this path**, even though they sit near it:
- `trading_hours.eod_entry_cutoff`, `market_open`;
- `trade_type`, `force_intraday_only`, `delivery_enabled`;
- `kill_switch.*`;
- `portfolio_allocator.allocator_mode` ("shadow") and `v3_chain.v3_chain_mode` ("shadow"). These last two act inside `_process_one`, after the boundary.

---

## 5. Flags (description only)

### 5A. Looks like a filter but cannot reject (or cannot take effect)
1. **Numeric cast (S12)** can reject only if a top-level `price`/`entry_price` exists and is uncastable. Its cast outputs are never read. **INFERENCE:** a no-op on Chartink payloads.
2. **`INVALID_SYMBOL`** rejects only the empty string. There is no format or instrument-cache validation.
3. **`INVALID_PRICE`** does not reject `"nan"`/`"inf"` (Python float semantics).
4. **`EXPIRED`** cannot reject a future `triggered_at` (negative age). The `triggered_at` parser has no date or future check.
5. **`require_hmac=false`** makes the "HMAC required" branch (`webhook_receiver.py:343-349`) unreachable.
6. **`_strip_account_prefix`** is, per its own comment (`:121-123`), a no-op on production alert names. That no alert carries the prefix is **INFERENCE** from the comment.
7. **`special_sessions`** is empty, so the holiday-exemption branch is inert.
8. **`per_ip_refill_per_sec: 0`** could never take effect: `or 5.0` at `:244`.
9. **`signal_processor.pipeline_timeout_sec: 30`** ("hard per-signal processing deadline") is not read by any runtime code.
10. **`_warm_zones`** is a no-op (zone_warmer None).
11. **`_process_one_safe` rate-limiter branch**, including its QUEUE_FULL → `REJECTED`/`QUEUE_FULL` write, is unreachable because `rate_limiter` is not passed.
12. **FIX-011 heartbeat** (`update_heartbeat`) is never called in production. The sweeper therefore evicts claims by age (>60 s), not by stall.
13. **`X-Queue-Warning` / `warning_pct`** produces a header only; it gates nothing.
14. **EOD route `trigger_prices`** is required to be present, but its value is never read.
15. **Backpressure (S9) / `QUEUE_FULL` (S19.11)** — **INFERENCE (stdlib):** because the dispatcher empties `signal_queue` into an unbounded executor queue, `qsize()` does not include the worker backlog. `put_nowait` can raise `Full` only if the queue climbs from below 240 (the value checked at request start) to 300 while symbols are being processed. That needs 61 or more items added, from one request or concurrent ones, faster than the dispatcher drains them, which in practice means the dispatcher is stalled (derived).

### 5B. Computed but not read by any decision
1. **`signals.expires_at`** (`received_at` + 600) is read only by ops_dashboard (`backend/readers/db_reader.py:826`, `frontend/templates/signals.html:441`). Expiry decisions use `triggered_at` + 600 (receiver `:924-925`; processor `:914-921`).
2. **Values cast by `_cast_numeric_fields`**: never read afterwards.
3. **`signals.strategy`** is populated with `scanner_name`. The map's `strategy` field is not consulted by the receiver; the two are identical for all 16 entries @970aabf.
4. **`warn_threshold`** is used only for a response header.
5. **The per-symbol `results` list** goes only to the HTTP client. None of its statuses except QUEUED/QUEUE_FULL reach the DB.

### 5C. Comments that contradict the code
1. `webhook_receiver.py:18` "WR7 — SHA-256 fingerprint dedup at **minute precision**". Code uses a **300 s** epoch bucket (`:952`).
   - `schema.sql:74` "hash(scanner+symbol+**trigger_minute**)" and `schema.sql:81` "same **minute** on same day = duplicate" contradict it the same way.
2. `webhook_receiver.py:21-22` WR10 lists `OUTSIDE_HOURS`, which is never produced (outside the window is a request-level 403). It omits `REJECTED_EXCLUDED_SYMBOL`, which is produced (`:715`).
3. `webhook_receiver.py:23` WR11 "each Flask request in its own thread". Production serves through a waitress pool of 8 threads (`main.py:3994`). **INFERENCE** on waitress semantics.
4. `webhook_receiver.py:25` WR13 "webhook_audit row per POST regardless of outcome". Not written for:
   - 413 oversize bodies, raised at `:480` before the `try` (**INFERENCE**, library);
   - Flask-level 404/405;
   - a failed audit INSERT, which is swallowed.
5. `webhook_receiver.py:146-149`: the class docstring usage shows `receiver.app.run(...)`. Production uses `waitress.serve` (`main.py:3987-4000`).
6. `webhook_receiver.py:64-65` "Response-only — these never reach signals.status". `QUEUE_FULL` does reach `signals.status` via the UPDATE at `:1053-1056`; the comment's own parenthetical acknowledges this.
7. `webhook_receiver.py:608` "scan_name optional - derive from URL if missing". Nothing is derived; the check is skipped.
8. `webhook_receiver.py:686-687` and `:865` "auth (:410-432)". Stale line references: auth is `_authenticate` at `:298-354`, called at `:547`.
9. `webhook_receiver.py:681-682`: the sanitizer exists "so the webhook secret never lands at rest". The raw body is logged **unsanitized** on every 400 (`:519-523`, first 1000 bytes) and on malformed JSON (`:589-592`, first 500 bytes).
   - Per the code's own comment at `:683-684`, Chartink echoes the `?token=` URL in `webhook_url`. **INFERENCE** that this holds for every payload.
10. `schema.sql:36-39` "Immutable log of EVERY incoming webhook signal … every signal has a final status". Rows are updated (receiver `:1003-1007`, `:1053-1056`; processor). Seven response-only statuses get **no row** at all.
11. `schema.sql:583`: `webhook_audit.ts` "when request arrived". It is written at the end, inside `finally` (`:1136`).
12. `schema.sql:43` "signal_id … UUID4". The format is `"sig_" + uuid4 hex` (`ids.py:52`).
13. `config_loader.py:196` "expiry_sec … (default 60)". The field has no default, and config sets 600. The SignalProcessor ctor default is 60 (`signal_processor.py:175`), but main passes 600.
14. `config_loader.py:619-620`: `bind_host` "(default "127.0.0.1")" and `bind_port` "(default 5000)". Both fields are required, with no default; config sets 0.0.0.0/5000.
15. `system_config.yaml:331-334` says the all-interfaces bind "relies on require_hmac=true". The adjacent `:336` sets `require_hmac: false`.
16. `system_config.yaml:347` `pipeline_timeout_sec` "hard per-signal processing deadline". Nothing enforces it (5A.9).
17. `system_config.yaml:567` "short vs the **60s** signal expiry" (allocator section). `expiry_sec` is 600.
18. `signal_processor.py:874` (`_process_one` docstring) "triggered_at: naive datetime (IST)". The receiver enqueues an **IST-aware** datetime (`:653`, `:1047`).
19. `config/scan_webhook_map.yaml:4-6` "Validated at startup (S10): every strategy name must have a YAML … Duplicate scanner names -> CRITICAL". Neither check runs on the boot path:
    - `main.py:3159-3162` calls `load_all_strategies` without `scan_webhook_map_path`, so the S10 cross-check at `strategies/loader.py:151-153` is skipped.
    - `ScanWebhookMapConfig` has no duplicate check. **INFERENCE (PyYAML):** duplicate keys silently keep the last value.
    - All 16 strategy YAMLs do exist @970aabf.

### 5D. Other ordering and behaviour facts
1. **Gate precedence**
   - Kill switch (403) and backpressure (503) run **before** the entry window (403).
   - Auth and the unknown-scanner check precede everything except shutdown and the rate limiter.
   - The **EOD route bypasses** the kill switch, backpressure and entry window.
2. **Cross-scanner in-flight claim.** The claim is per **symbol across scanners**. A same-symbol signal from another scanner while the first is still in flight gets `IN_PROCESS`: response-only, non-retryable, HTTP 200.
3. **One accept per `(symbol, scanner)` per 300 s** (derived).
   - The TTL cache admits at most one per 300 s, counted from the moment the key was inserted (S19.5, after the symbol, price, expiry and in-flight checks pass). A QUEUE_FULL or STORE_ERROR pops the key, which restarts the window.
   - Replays with the same `triggered_at` bucket after the cache expires, on the same received date, hit the DB unique index and get DUPLICATE.
   - The cache is in-memory, so it is empty after every restart; only the DB index remains then.
4. **Re-queue path ordering (S19.9)**
   - `put_nowait` runs **before** the unconditional `UPDATE … SET status='QUEUED' WHERE signal_id=?`. **INFERENCE:** a worker that starts quickly could have its `PROCESSING` status overwritten by `QUEUED`.
   - The row keeps its original `trigger_price`/`triggered_at`/`received_at`/`expires_at`, while the re-queued tuple carries the retry's `price` and `triggered_at`.
5. **Audit counts on 503.** A batch-level 503 is audited `0/0` even when some symbols were queued (S21).
6. **Partial batch then 500.** An exception after some symbols were accepted returns 500 while those symbols stay queued. The failing symbol's cache key persists for 300 s, and its in-flight claim persists until the sweeper evicts it (S19 j).
7. **Non-string `scan_name`** gives 500, not 400 (S14). **INFERENCE (stdlib):** non-ASCII token/signature strings also give 500 (S5).
8. **Synchronous DB work on the request thread.** Each symbol costs one `BEGIN IMMEDIATE` transaction on the waitress request thread (`busy_timeout` 30 s, `synchronous` FULL), plus the audit INSERT.
9. **No re-drive after a crash.** Nothing re-drives `QUEUED`/`QUEUE_FULL` rows. The in-memory queue is lost on a crash; `QUEUE_FULL` rows are re-queued only by a matching webhook retry in the same fingerprint bucket and date (S19.9).
10. **Clock reads.** Four `now_ist()` reads per request: window check and date (`:581`), `received_at` (`:677`), per-symbol age (`:919`), audit `ts` (`:1136`). The entry window and kill switch are evaluated once per request, not per symbol.
