---
name: t2_attempt_02jul
description: T2 CNC live-validation DEFERRED 02-Jul — proof script bit-rotted (≥2 drifts); repair whole script off-market before re-running
metadata: 
  node_type: memory
  type: project
  originSessionId: 3e62fe89-aead-435f-8580-0a242667edcc
---

T2 (delivery CNC→GTT→DDPI-auto-sell proof, `scripts/t2_cnc_gtt_realtest.py`) attempted 02-Jul ~12:00 IST → **DEFERRED, live run NEVER executed** (Rama's call). The script has bit-rotted (never run since the API evolved); repair it PROPERLY as a whole off-market, don't patch line-by-line live. Supersedes/continues [[delivery_slice25_status_30jun]].

**PRE-CHECKS PASSED — still valid, no need to re-verify:**
- STEP 0 deploy: both safety fixes live — HEAD `59f83b5` (main), `f6de000` ancestor; tag guard `zerodha_adapter.py:579`, CHECK9 FACET-1 `_confirm_genuinely_naked` :2107 + FACET-2 oversell `qty=min(qty,live_held)` :2213. Service+token-watcher active; kill-switch INACTIVE.
- STEP 1 delivery-lock gate GREEN (code-verified): (1a) T2 builds its OWN `ZerodhaAdapter(delivery_enabled=True)` (script:89); adapter CNC gate reads the INSTANCE `self._delivery_enabled` (`zerodha_adapter.py:535`, set :398) → system's delivery_enabled=false is a DIFFERENT object, doesn't block. (1b) `force_intraday_only` acts only in the strategy loader; T2 calls `place_order(intent="DELIVERY")` directly. (1c) reconciler CHECK2 `_check2_orphan_adoption` (`order_reconciler.py:1366`) is NON-DESTRUCTIVE for an untracked symbol (no matching closed system trade → human-order branch: log once/day + at most a benign "naked untracked" WARNING; never adopts/protects/flattens).
- Book was FLAT (safest window). DATAMATICS (the task's stale "open long 1") had closed 11:41 SL_HIT (−18.09); today 11 trades/6 filled, net −12.03.

**KNOWN DRIFT to repair in `scripts/t2_cnc_gtt_realtest.py` (align to current `main.py`):**
- line 71: `core.order_state_machine` → `broker.order_state_machine` (OrderStateMachine lives in broker/; main.py:46).
- line 83: `RateLimiter(cfg.broker_limits.rate_limits)` → `RateLimiter(cfg.broker_limits)` (RateLimiter takes the whole `BrokerLimitsConfig`; `.rate_limits` doesn't exist; main.py:1607). `max_wait_sec`/`shutdown_event` are optional kw.
- line 319: `CncGttPlacer(... store=∅)` → **wire a real `store`** so a `gtt_state` row IS written — else the gtt_state-lifecycle pass-criterion can't be validated (this is WHY today's run would've been partial even if it ran).
- **AUDIT the ENTIRE construction + live-order path** against main.py (place_for_fill / get_quote / _resolve_tick + every constructor). A dry-run canNOT exercise the live-order path, so more drift could surface mid-run with a REAL position open — do a full static alignment, not incremental patching. (Verified-OK so far: ProductResolver, CostCalculator, adapter param names, CncGttPlacer kwarg names, cfg.system.capital.{gtt_sl_limit_offset_pct,sl_limit_offset_pct} at 307-308.)

**REPAIR PLAN (off-market, dedicated session):** fix ALL drift as ONE proper change + tests → clean dry-run → commit → Rama pushes OFF-MARKET → then run the COMPLETE T2 (buy → GTT-WITH-gtt_state-row → DDPI square → flat) on the verified script, mid-session window (not open 30 min, not after 14:45), flat book preferred. Pass criteria (runbook): real CNC buy filled · OCO GTT placed + get_gtt shows CNC/2 SELL legs/qty1 · **gtt_state row created** · CNC sell COMPLETE with NO TPIN prompt (the DDPI proof) · GTT deleted only once flat.

**PARKED (do not push):** branch `fix-t2-import-02jul` @ `b826ae0` (line 71 fix ONLY) — INCOMPLETE (script still fails at line 83); leave unpushed; the full repair will SUPERSEDE/discard it. Deployed VM script untouched (both stale lines intact). Temp copy `scripts/t2_run_temp_02jul.py` was created for the dry-run then DELETED (no-go).

**Why deferred:** dry-run passes with 2 fixes but (a) can't exercise the live-order path → risk of more drift surfacing mid-run with real money at stake, and (b) store=None means a run today wouldn't validate the gtt_state lifecycle → partial anyway. Per the permanent-fix principle: repair the whole script once, properly, off-market.
