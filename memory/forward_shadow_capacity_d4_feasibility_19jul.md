---
name: forward-shadow-capacity-d4-feasibility-19jul
description: "19-Jul READ-ONLY: the forward-shadow recorder WILL keep appending (cron installed, monitored, fail-loud, idempotent per date+signal); Monday = OOS day 4. D4 is PARTIALLY testable (OOS 1-min candles survived in analytics.db, unlike D3) but UNDERPOWERED (19 OOS entered / 9 winners) — the 2.93R MFE claim doesn't reproduce (OOS median 1.44R). Facts verified (no engine fired 0/361, dead config). Capacity: D4 needs ~17-34 trading days; cross-regime needs a regime change (unschedulable)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 69886370-a044-4d23-87ae-f3c02b539e6e
  modified: 2026-07-24T18:27:13.868Z
---

**FORWARD-SHADOW CAPACITY + D4 FEASIBILITY (19-Jul-2026, READ-ONLY, docs-only).** Report
`docs/audit/forward_shadow_capacity_and_d4_feasibility_19jul2026.md`. Both artifacts untouched (live DB
`6df0c09a…`; forward-shadow JSONL 7,827 lines @ 16-Jul; analytics.db `bb229f44…` before==after). Recorder NOT run.

## ⭐ THE FORWARD SHADOW WILL KEEP APPENDING — its integrity is now load-bearing (sole confirmation path for D3/D4/#10/D1)
Cron `15 18 * * 1-5` (18:15 Mon-Fri) → `scripts/forward_shadow_record.py`; `cron_registry.yaml:346-364`
(`monitored:true`, `market_day_only:true`, `enabled:true`). **Fail-LOUD** — a crash raises a Telegram sentinel;
done-mark `data_store/cron_marks/forward_shadow_record.done` carries `$rc`. **Idempotent per (date, signal_id)**
(main:151-160 skips already-seen; empty → return 0). 72G free, no locks. ⚠️ **Contamination vector: a
`--date <not-present>` backfill is NOT guarded** — it would mix in-window dates into the OOS file (header:
mutation "voids" the evidence) ⇒ **never run the recorder manually.** **Monday 20-Jul = OOS day 4** if the system
trades + token present (else appends with `sim_R=None`). Currently **3 genuine OOS days** (07-14/15/16); the JSONL
stores only the final `sim_R` under one policy — **no path/MFE/MAE.**

## ⭐ D4 IS PARTIALLY TESTABLE — MORE THAN D3 — but the binding constraint flipped DATA → POWER
**Facts REPLICATE (verified):** no exit engine ever fired — `sl_trail_count>0` on **0/361** (the record's "0/134"
was a subset); `order_protocol` LIMIT_TRIPLE 361/361; `entry_mode` FULL 361/361.
**What survives (unlike D3):** 1-min candles for 13-16 Jul in **`analytics.db`** (⚠️ NOT in the DB snapshot — the
snapshot is `trading_system.db` only; candles live in the ATTACHed analytics.db — a preservation gap) + MFE/MAE in
`trade_excursions` (109 trades) ⇒ the post-entry PATH is reconstructable read-only.
**But POWER is the constraint:** only **19 OOS entered trades / 9 winners.** The **"~2.93R winners' MFE" claim
does NOT reproduce OOS** — uncapped full-path median **1.44R** (n=9), unstable (one in-window day swings the mean
1.75→3.63R) ⇒ **"cannot distinguish," NOT a refutation.** `trade_excursions` MFE (winners 1.56R) is **CAPPED by
the current exit** ⇒ can't answer "money left on the table." **Not re-verifiable on its own data** (no pre-13-Jul
1-min candles; 13-Jul per-trade sims not persisted).

## ⭐ STANDING CONSTRAINT — the 13-Jul studies' PER-SIGNAL basis was NOT persisted (band study + exits study)
Only AGGREGATE report tables + 1-min candles from **13-Jul onward** survive. Any re-examination of that era's
findings (band inversion, exit MFE, expectancy) **cannot re-slice the original per-signal data** — rebuild from
candles (13-16 Jul only) or wait for forward-shadow accumulation. Applies to every 13-Jul finding.

## ⭐ CAPACITY (trading days; grows one per day the system runs)
D3 band relationship: ~powered at 3 days (already non-replicating). **D4 traded-book exits: ~17 days for ~50
winners / ~34 for ~100** (~3 winners/day). #10 "does the score rank": answered negatively so far (rho +0.003 +
D3 OOS non-replication). **⚠️ CROSS-REGIME cannot be bought with days — it needs a regime change (unschedulable).**
Both the discovery and OOS windows are single-regime.

## ⭐ TRIAGE RELIABILITY: 2 of 3 "COMPUTABLE NOW" proved otherwise (opposite reasons)
D3 = data not persisted; D4 = data survives but underpowered. The label conflated "data exists" with "question
answerable." ⇒ **PerformanceAllocator (the 3rd) must be treated as UNVERIFIED until its data + power are checked**
(deferred pending sizing/leverage anyway). A statement about the triage, not the decisions.

## ⭐ SCOPING PASS 24-Jul (READ-ONLY; recorder NEVER run) — `docs/audit/forward_shadow_scoping_2026-07-24.md`
**RECORDING CORRECTLY + UNCONTAMINATED (the decisive check).** `forward_shadow_fs-v1.jsonl` = 17,454 recs over **9 dates 13→24-Jul**; each PROVEN to have run by a `cron_heartbeat` SUCCESS row (`wrote=N` matches counts, not file presence); **append-only holds** — dup=0 every date, 0 malformed JSON, each date computed **same-day under exactly one chronological git_commit** ⇒ no backfill/recompute. **Caveats:** 13-Jul = manual off-cron seed (23:41, pre-deploy `d23239c`) ⇒ **in-sample, exclude**; **17-Jul absent = 0 signals LIVE that day** (service outage; VM crons up 115×) NOT a shadow fault; 16-Jul thin (181, mid-session restart). ⚠️ a 0-signal day writes NO heartbeat (`:162-163`) ⇒ "nothing to record" == "didn't run" in the table (blind spot).
**§4 one record = one SCORED SIGNAL** (`screener_results⋈signals`); `old_score`/`decision` = LIVE, `ms4_score` = **COMPUTED-ONLY never used**, `sim_R` simulated, `realized_pnl` only if traded. ⚠️ `side` NAME-inferred (`_direction :82`); recomputes the **score only, NOT M-S4 admission**. Method `fs-v1` stable, `scoring_weights_sha` constant ⇒ days comparable.
**§6 POWER — bound by REALIZED would-be-trades = 45 OOS** (8 clean days, ~14k scored, ~13.4k `sim_R` but mostly REJECTED signals ≠ would-be-trades). **Not remotely enough**; weeks-to-months; every service-down day = a lost OOS day. **NO performance reported** (§6.4).
**⚠️ THREE shadow artifacts, not one:** `fs-v1` (M-S4 SCORE, the protected OOS path) · `would_be.jsonl` (V3-chain-vs-live, 281 recs: **223 WOULD_REJECT_RR / 54 HTF / 4 PASS**, **regime null 281/281 = INERT**) · **`pb01_would_be.jsonl` ABSENT ⇒ PB-01 module = 0 records = INERT** (4th "present-but-never-reached" this week). The instruction's "shadow exists to test PB-01" is imprecise — fs-v1 tests min_pass/M-S4 scoring.

## ⭐ PB-01 + V3-GATE SCOPING 24-Jul (READ-ONLY; no producer run) — `docs/audit/pb01_and_v3_gate_scoping_2026-07-24.md`
**PB-01 emits nothing = DELIBERATE staged default-off** (`pb01_breakout_retest.yaml:4,30` enabled:false, "REGISTRATION STUB / never trades until spec-13 promotion") **+ 0 `pb01_breakout_retest` signals EVER** ⇒ `pb01_watchlist`=0 rows ⇒ nothing to confirm ⇒ no `pb01_would_be.jsonl`. **"No live twin"** (`pb01_runner.py:207,225`): never trades ⇒ would-be record has NO live outcome ⇒ **un-evaluable as a shadow even if switched on** (needs live trading or a dedicated outcome-sim). **V3 chain `would_be.jsonl` population = POST-SIZING** (`observe()` @ `signal_processor.py:909`, after `sizing.success`) = the live system's near-admission ACCEPTED set (~40/day; **80/281 traded**) ⇒ **it rejects 98.6% of the signals the live system ACCEPTED**, NOT junk it caught. **RR reject NOT on merit:** 46% (103/223) `v3_rr` NULL = **missing S&R zone** (no resistance above breakout entries; `nearest_resistance` null ×88); 54% (120) computed but **median 0.33R, max 1.78R vs `rr_floor` 2.0** ⇒ STRUCTURAL not calibration (`sr_sync_hit` 69.8% ⇒ zones ARE built). **The S&R-RR gate is geometrically incompatible with momentum/breakout entries.** ⭐ **§4: NEITHER entry-evidence path can validate a thesis in reasonable time** — V3 structural (not tunable by days), PB-01 nothing + no-twin. Only **4/281 WOULD_PASS** (v3_rr 2.2–3.6 > live 1.5), itself an upper bound on would-trade (observe is pre-throttle/placement).

## ⭐ PB-01 SIMULATION FEASIBILITY 24-Jul (READ-ONLY; no producer run) — `docs/audit/pb01_simulation_feasibility_2026-07-24.md`
Can PB-01 be evaluated WITHOUT trading it? **PARTIALLY.** The CODE exists + is pure: `simulate_true_path` (`forward_shadow.py:75`; FIXED 1%/1.5R SL/TGT; ⚠️ adverse-first ONLY → both-orderings caveat) + `gate_confirm`/`gate_pullback` (`hard_gate.py:362`; plain-value pure fns, no live state, fetcher injected). **BINDING BLOCKER = the CANDIDATE UNIVERSE:** PB-01's defining event (20-session-high daily breakout) has NO source — Chartink EOD scan NEVER fired (`pb01_watchlist`=0, `pb01_breakout_retest` signals=0) AND the level is UNCOMPUTABLE from held data (candles = **1-min ONLY, 24 trading days 19-Jun→24-Jul, 0/482 symbols have ≥20 days**; NO daily OHLC stored; `daily_symbol_stats`=stats not highs; `sr_detector/fetch.py`=Kite-backed on-demand). ⇒ **DATA blocker** — needs Rama's scan OR a Kite daily-fetch the system doesn't hold. ⚠️ **UNIVERSE BIAS: 1-min stored ONLY for momentum-tracked symbols** ⇒ a held-data backtest only sees retests in stocks the current entries already fired on (the style PB-01 replaces). §2.6: backward-from-held = **~0 candidates**; +Kite-fetch = a handful (biased, ≤24d); forward = the scan + weeks. 5-min IS derivable from clean-aligned 1-min ⇒ the retest gates are NOT the blocker; the universe is. §2.2: detection thresholds in config (repo); the "V3 DECISION CONTENT SPEC" doc is referenced by 7 files but NOT in the repo; the full Chartink filter set is external.

## ⭐ EOD CAPTURE PATH SAFETY 24-Jul (READ-ONLY; NO test POST) — `docs/audit/eod_capture_safety_2026-07-24.md`
Precondition before Rama points a Chartink EOD scan at PB-01 capture (`/webhook/pb01_breakout_retest`, `scanner_type:eod`). **RECEIVER IS SAFE (contained):** `submit()` = **put_nowait to bounded q(256)**; the broker daily-fetch runs in the **BACKGROUND worker (off the request thread)**; multi-layer try/except; returns **200 regardless**; the EOD route `return`s at `webhook_receiver.py:509` **BEFORE the kill/window gates** and never touches `signal_queue` ⇒ **cannot disturb live signals**. Broker fetch is **rate-limited** (`acquire("historical")`, shared bucket, post-close low contention) + **fail-safe** (no/expired token → `{}` → skip capture, logged). **BUT 2 SILENT-FAILURE modes ⇒ NOT-YET per the decision rule:** **(1) TIMING** — safe window **[15:30 `market_close`, 16:00 `SERVICE_WINDOW_END` self-exit)**; target **~15:35–15:50** on a trading day; a POST before 15:30 = SETTLED-ONLY skip, after ~16:00 = refused/lost, both SILENT; `stop()` drains only 3s at shutdown. **(2) OBSERVABILITY** — success = log + `pb01_watchlist` row (**NO Telegram, NO heartbeat**); **failure = LOG-ONLY, no alert** (looks identical to "no breakouts" — the week's 5×-looks-alive pattern). Morning check: `SELECT * FROM pb01_watchlist WHERE trading_date=<today>`. §4 contract: payload requires **stocks(CSV)+trigger_prices+triggered_at**; **same auth** as trading webhooks; unknown scanner→**404**, wrong `scanner_type`→routed to intraday (quiet misconfig). A market-hours POST is accepted(200) but SETTLED-ONLY-skipped ⇒ no pollution. `next_trading_day` holiday/weekend-aware. [[webhook-flow-diagnosis]]

## ⭐ ROOT CAUSE + SERVICE-WINDOW EXTENSION 16:00→17:35 (READ-ONLY 24-Jul) — `docs/audit/service_window_extension_2026-07-24.md`
**ROOT CAUSE FOUND:** the **PB-01 Chartink scan fires at 17:00** (Chartink "market close" freq = **17:00, NOT 15:30**), 10 triggers since 13-Jul (~17 stocks/day) — but the service **self-exits 16:00** (`SERVICE_WINDOW_END`, `main.py:1594`) ⇒ ALL 10 hit a DEAD PORT. Scan/webhook/receiver/capture were never broken. **⚠️⚠️ CORRECTS 2 prior claims of mine:** (1) the EOD-capture "15:35–15:50 safe window" is UNREACHABLE by Chartink's 17:00 preset; (2) the feasibility report's "candidate universe cannot be reconstructed / ~0 candidates" is **WRONG** — the universe EXISTS in **Chartink's trigger history** (10 days, dates+symbol lists, exportable CSV); it was absent from the SYSTEM only because the alerts hit a dead port. Backfill caveats: retrospective ⇒ **BACKTEST not OOS**; outcome overlap UNKNOWN (held 1-min candles cover only the 482 momentum-tracked syms; PB-01 names DIFFERENT stocks — count the overlap one day).
**VERDICT on extending to 17:35 = NOT UNTIL one monitored session.** NO structural blocker: every kill trigger is **market-hours-GATED** (feed watchdog `live_feed.py:715`; token monitor `token_monitor.py:172`, +SOFT not HARD; reconnect-exhaustion off-hours = WARNING-not-kill `:440-461`, the gate built for the "07:07 overnight" false alarm) **or** needs ticks/orders/positions absent post-market (queue-full, consumer-dead, API-failure→hard_kill). Daily reset is **CLOCK-driven 15:17** (`eod_squareoff.py:196`, `_fired_for_date` keyed on date) NOT exit-driven. Crons vs a live DB = the **same WAL reader/writer pattern already proven all market-day** (GUI :8500 + `*/5 09-15` crons); `wal_checkpoint`@16:00 is **PASSIVE**; shutdown moves benignly (cleanup only). **The ONE un-observable residual = the ORDER-RECONCILER** (15s daemon poll, NOT market-gated, broker calls each cycle, SOFT_KILL on a failure run `order_reconciler.py:41`): flat book + 30-min-clean-today support it, but the extra 95 min CANNOT be measured (state never existed) ⇒ a monitored trial, not more code-reading, closes it. Any such soft_kill auto-clears at the next 08:15 boot; **no HARD-kill path found.**

Related: [[d3-band-inversion-robustness-19jul]] [[decision-packages-19jul]] [[e4-w10-outcome-impact-19jul]]
[[capital-vocabulary]] [[db-schema-v28-split]] [[trailing-stop-never-fired-24jul]]
