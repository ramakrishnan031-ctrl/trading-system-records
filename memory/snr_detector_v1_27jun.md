---
name: snr_detector_v1_27jun
description: "SNR-DETECTOR-V1 — shadow S&R detector (pure pkg sr_detector/ + sr_detector_results v37 + default-off flag + async non-gating observer after place()); staged, schema awaiting nod"
metadata: 
  node_type: memory
  type: project
  originSessionId: efdd36b2-7025-4325-9afb-024470b51473
---

**SNR-DETECTOR-V1 (27-Jun, staged, default-OFF, schema v37 .backup-tested AWAITING Rama nod).**
A shadow support/resistance detector: for every PLACED candidate it fetches Daily/60m/30m
structure, scores S/R zones by CONFLUENCE, flags "buying-into-resistance" (+ support/short
mirror), and logs an evidence row for OFFLINE validation. SHADOW-only — never rejects, sizes,
or touches SL/TGT/STM/entry; never blocks/delays/raises into placement.

**3 spec premises were overturned by the investigation (verified in code):** (1) NO shortlist
stage — the hook is PER-SIGNAL; (2) the detector is the FIRST intraday `historical_data`
consumer in the order path; (3) ShadowEngine is dormant → imitate the `screener_results` WRITE
pattern (txn + JSON cols + never-raise), not a live shadow path.

**Architecture:**
- Pure pkg `sr_detector/` (imports only core/+stdlib): `models`, `fetch` (token via
  instrument_cache + 3-TF windows + intra-session cache + fail-safe), `pivots`, `zones`
  (clusters + volume profile), `confluence` (weighted multi-method/multi-TF votes →
  HIGH/MED/LOW + persisted evidence breakdown), `flags` (BUYING_INTO_RESISTANCE / WEAK_BREAKOUT
  / NO_VOLUME_CONFIRMATION / LOW_CONFIDENCE_STRUCTURE / NO_CLEAR_STRUCTURE + retest PROPOSAL),
  `detector` (SINGLE serialized bg worker; observe()/start()/stop()).
- **Confidence = HIGH iff score≥t_high AND ≥2 distinct method-types AND ≥2 timeframes**; else
  MEDIUM≥t_med else LOW. Weights+thresholds are config (visual-review tuning phase).
- Retest = log the PROPOSAL only (would_wait + proposed entry/sl below the zone). Outcome
  simulation = a LATER follow-on (`hypothetical_retest_result` left NULL).

**Key design calls (rationale):**
- ★ **Observer runs AFTER a successful `place()`, NOT at the spec's literal `_emit_signal_alert`
  :842** (which fires BEFORE place) — the spec's cond.(a) "runs only if the order reached
  placement" wins. Hooked BOTH paths: `_process_one` (score=screen_result.score) +
  `continue_from_gate` (score=None), each as the last statement of the try body after
  PROCESSED. `_sr_observe(...)` builds a `Candidate` + enqueues; fully guarded (no-op when
  `sr_detector=None`).
- ★ **Adapter UNTOUCHED** (it is safety-critical; spec rule #1 = never alter placement). The
  rate-limited historical fetch is a CLOSURE in `main.py`: `_make_sr_fetch_fn(market_kite,
  rate_limiter)` → `rate_limiter.acquire("historical")` then `kite.historical_data(...)`.
  In live `market_kite = kite_client` (== adapter._kite); **paper `kite_client` is None**, so
  `_build_market_data_kite` builds a READ-ONLY kite from `data_store/session/zerodha_token.json`
  (api_key from the token file, NOT the hardcoded key in fetch_daily_candles:30) → real
  paper/live parity, orders stay paper-simulated.
- ONE default-off flag `system.sr_detector.enabled` (`SRDetectorConfig` in config_loader;
  `SystemConfig` is extra="forbid" so the YAML block REQUIRED the field — added with a
  default_factory so the block is optional/default-off). Disabled ⇒ detector not constructed
  ⇒ zero pipeline change, no extra thread.

**Schema:** `sr_detector_results` (core/schema.sql TABLE 38, MAIN db, FK→signals(signal_id),
pure addition like v36 gtt_state). `EXPECTED_SCHEMA_VERSION 36→37`. DAO
`insert_sr_detector_result`/`get_sr_results_for_backfill`/`update_sr_outcome`. **Migration
.backup-tested v36→v37 clean on the local dev DB (which is itself at v36 = the live version) —
table+3 indexes created, version bumped, data intact. AWAITING Rama nod before the live DB
applies it (it applies automatically at the next VM boot once deployed).** EOD outcome backfill
`scripts/sr_detector_backfill.py` (join→trades by signal_id; terminal trades only; open→left
NULL; no-trade→NO_TRADE).

**Tests/regression:** 37 new (`tests/unit/test_sr_detector_{units,fetch,observer,backfill}.py`)
incl. ★non-blocking (observe returns <0.25s while the worker fetch is blocked), ★dormancy/parity,
real-store v37 round-trip, the seam. **Full unit suite 3869 pass / 0 regressions** — proven:
`test_main` fails 23 in isolation == 23 in full suite (my main.py edits change nothing; those
fail at a PC-env step before my code). The full-suite 30→31 delta is a ±1 flake in TOTP/NTP
(`test_fix135`/`test_fix129`, network/time-dependent, NOT touched, green on VM).

**Follow-ons (NOT this build):** corp-action adjustment spot-check needs a VM/live session
(`scripts/sr_corp_action_spotcheck.py` ready); `hypothetical_retest_result` simulation; the
visual-review weight/threshold tuning + the V2 HIGH-confidence veto. branch
`snr-detector-v1-27jun` (on main ac127f9), NOT pushed/restarted (Rama owns push+restart).
Related: [[slice25_p2_gtt_durability_25jun]] (the v36 pure-addition pattern imitated),
[[feedback_paper_live_parity]], [[feedback_system_map_first]].
