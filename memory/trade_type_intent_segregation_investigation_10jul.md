---
name: trade_type_intent_segregation_investigation_10jul
description: "BUILT (Option A, commit 8116b74, LOCAL/UNPUSHED, 10-Jul) — trade_type/intent segregation: declared intent preserved, loader rewrite removed, resolver segregates, product-coercion relocated to broker chokepoint. Default now 12 WILL / 3 WON'T. NOT a safety bug (double-locked). Push OFF-MARKET."
metadata: 
  node_type: memory
  type: project
  originSessionId: af4824f1-41e0-4c1f-b881-49265a715b87
---

**Task:** investigate why the Cron Officer briefing shows all 15 strategies WILL
TRADE under `trade_type=INTRADAY` (incl. the 3 DELIVERY-intent positional ones);
design a fix; STOP (no build). READ-ONLY, market-hours-safe. Model Opus/High.

## Per-strategy intent + enabled (all 15, confirmed from YAMLs)
- **12 INTRADAY, enabled:true:** vwap_rejection_short, vwap_bounce_long,
  range_breakout_long/short, open_low_breakout_long, open_high_breakdown_short,
  gap_go_long/short, gap_fade_long/short, first_pullback_long/short.
- **3 DELIVERY, enabled:true:** positional_momentum_long, positional_sector_rotation,
  positional_swing_long.
- No mislabels; every YAML has both `intent` + `enabled` → NO new operator field needed.

## Config keys + where read
- `system_config.yaml:70 force_intraday_only: true` · `:77 trade_type: INTRADAY` ·
  `:83 delivery_enabled: false`. Loaded in `core/config_loader.py` SystemConfig:
  `force_intraday_only:bool=True` (:1254), `trade_type:str="INTRADAY"` (:1268, validator
  INTRADAY/DELIVERY/BOTH). Read in `main.py` (loader :2365-2368 gets force_intraday_only;
  SignalProcessor :2631-2632 gets trade_type + force_intraday_only).

## Load / filter path map
1. `main.py:2365` → `StrategyLoader.load_all_strategies(dir, force_intraday_only=True)`.
2. `strategies/loader.py:66-72` — **THE REWRITE:** `if force_intraday_only and cfg.intent
   != "INTRADAY": cfg = cfg.model_copy(update={"intent":"INTRADAY"})`. Destructive — the
   3 DELIVERY configs now carry intent=INTRADAY (declared value LOST on the object;
   schema has no preserved-original field). All 15 kept in the active set (nothing dropped).
3. Live gate: `signals/signal_processor.py` **3 sites** (:739 _process_one, :1508
   pullback-resume, :1826) call `strategies/control.strategy_will_trade(strategy_obj,
   trade_type, force_intraday_only)` BEFORE sizing/reservation; reject → `_PipelineReject`
   (CAUSE_TRADE_TYPE→"TRADE_TYPE" label, else "STRATEGY_CONTROL"). strategy_obj = the
   LOADED (rewritten) config.
4. Resolver `strategies/control.py::strategy_will_trade` (single chokepoint, pure, no mode
   branch → **parity holds**): enabled? (LAYER3) → force&intent==DELIVERY? (LAYER0
   FORCE_BREAKER) → trade_type≠intent? (LAYER1×2 TRADE_TYPE) → else WILL TRADE.
5. Status table `scripts/strategy_status.py` re-reads RAW yaml for the true-intent "Type"
   column but computes the verdict on the SAME effective (post-rewrite) intent → table==gate.

## enabled enforcement — WORKS (no bug)
Resolver line 81 short-circuits `if not enabled → WON'T TRADE (DISABLED)`; it runs on the
live path before sizing, in both modes → a `enabled:false` strategy is skipped everywhere.
GUI toggles writing `enabled` will be honored. All 15 currently enabled:true.

## ROOT CAUSE
The loader rewrites the 3 DELIVERY strategies' intent → INTRADAY **before** the resolver's
trade_type×intent gate evaluates them. So by the time `strategy_will_trade` runs, their
effective intent is INTRADAY: the FORCE_BREAKER branch (needs raw DELIVERY) doesn't fire,
and the TRADE_TYPE branch (needs intent≠INTRADAY) doesn't fire → they fall through to WILL
TRADE (as MIS). **The trade_type product-segregation is structurally UNREACHABLE while
force_intraday_only=true (the permanent default).** This directly contradicts the config's
OWN docs — `system_config.yaml:72-76` and `config_loader.py:1264-1267` both state
"trade_type INTRADAY = only intent==INTRADAY strategies trade." force_intraday_only "owns
the rewrite," and that rewrite silently defeats the gate the same comment promises.

## ⚠️ SEVERITY = correctness/transparency, NOT safety (NO CNC leakage — double-locked)
The 3 delivery strategies place **MIS by ENFORCEMENT, not luck** — two independent locks:
(1) loader rewrite → intent INTRADAY → `product_resolver.resolve`→"MIS"; (2) broker
`delivery_lock`: `zerodha_adapter.place_order:535` refuses broker_code=="CNC" while
`delivery_enabled=false` (+ GTT path gated). Even if lock (1) were removed, (2) still blocks
CNC. Confirmed live in the 08:15 boot log ("delivery_lock: delivery_enabled=FALSE — all
CNC/GTTs REFUSED"). Real downside is OPERATIONAL: momentum/swing/sector-rotation strategies
(designed for multi-day holds) are forced to intraday square-off at 15:17 → possibly poor
intraday trades — not a risk event.

## DESIGN (proposed; Rama/Web Claude confirm the SEMANTIC choice + P0-safety review)
**Decision that belongs to Rama:** under force_intraday_only=true + trade_type=INTRADAY,
should the 3 DELIVERY strategies be PROMOTED-to-intraday-and-trade (current) or DORMANT
(requested true segregation)? Requested = a real behavior change: active intraday strategy
count 15→12 (those 3 stop trading until delivery is enabled). The resolver already has BOTH
correct branches — they're just bypassed by the loader rewrite. So the fix = let the resolver
see the DECLARED intent. No new operator YAML field either way.
- **Option A (recommended, cleaner):** stop the loader's destructive rewrite → loaded config
  keeps declared intent → resolver's FORCE_BREAKER (under force) / TRADE_TYPE (under
  INTRADAY) branch dormants the 3 delivery strategies (12 WILL / 3 WON'T). Preserve the P0
  MIS-only guarantee by relocating product-coercion to the product-resolution/placement
  chokepoint (force_intraday_only ⇒ resolve product INTRADAY) — belt-and-suspenders with the
  existing broker delivery_lock. Bonus: strategy_status.py no longer needs its raw-YAML
  re-read (removes a duplication smell). Blast radius touches a P0 path → re-validate MIS-only.
- **Option B (smaller blast radius):** keep the loader rewrite (P0 untouched); capture the
  declared intent at load into an INTERNAL StrategyConfig field (e.g. declared_intent, not an
  operator YAML field); resolver gates trade_type on declared_intent while `intent` (effective)
  still drives product/sizing. Same net behavior; adds one internal field + a resolver tweak.

## Validation strategy (RED→GREEN)
Per-mode resolver counts: trade_type=INTRADAY → 12 WILL / 3 WON'T (RED today = 15/0);
DELIVERY → 3 WILL (the positionals, once delivery lifecycle allows) / 12 WON'T; BOTH → 15;
any `enabled:false` → that strategy WON'T in every mode. Assert table==gate. Existing tests:
`tests/unit/test_slice2_strategy_control.py`, `test_phase4_trade_type_gate.py`.

## Parity + rollback
Parity: loader + resolver are mode-agnostic (pure resolver, no mode branch; one loader) —
paper==live. Rollback (once built): single config/loader revert; delivery stays NO-GO
throughout (delivery_enabled=false unchanged) so no live-delivery risk is introduced by
either option. Do NOT touch T2.

## ✅ BUILT — Option A, commit `8116b74` (LOCAL/UNPUSHED, 10-Jul ~market-hours; push OFF-MARKET)
Rama+ChatGPT approved Option A (un-parks what Phase-4 named "Option B"). 10 files, +245/-89.
- `strategies/loader.py` — DROPPED the `model_copy(intent→INTRADAY)` rewrite; declared intent
  preserved for all 15; per-strategy INFO dormancy log replaces the old WARNING overwrite.
- `strategies/control.py` — logic UNCHANGED (FORCE_BREAKER + TRADE_TYPE now the LIVE dormancy);
  docstrings de-staled. `enabled` (line 81) untouched.
- `broker/zerodha_adapter.py` — NEW `force_intraday_only` ctor param + product-coercion in
  `place_order` (non-INTRADAY intent → MIS before resolve). Second independent MIS lock,
  composes with the `delivery_lock`. `main.py` wires it from `app_config.system.force_intraday_only`.
- `scripts/strategy_status.py` — removed `_effective_intent` sim (gates on declared intent);
  footnote → "DORMANT under the current master/breaker".
- **Behavior change (intended):** default config **12 WILL / 3 WON'T** (positional_* dormant),
  was 15/0. Live-proven via a real-config count print.
- **Tests:** 305 pass across slice2/phase4/p0/loader/product-resolver/signal-processor-gate/
  zerodha-adapter/cnc-gtt-delivery-lock/cron-officer. New: T1 per-mode counts (12/3, 3/12, 15/0),
  T4 Option A adapter DOUBLE-LOCK (coercion + delivery_lock proven independently), T5 declared
  intent preserved. The 4 `test_main.py` fails = pre-existing PC-env baseline (verified identical
  on a clean-main `git stash` of this build — NOT caused by this change).
- **SYSTEM_MAP.md** changelog entry added (10-Jul). **PATHS.md `Default state` line (15 WILL) left
  stale per instruction — update on deploy.**
- **NEXT:** off-market push + `trading-system.service` restart (behavioral only at the next in-window
  boot). Ledger [[unpushed_pending_deploy_ledger]] DEPLOY-PENDING carries `8116b74`.
