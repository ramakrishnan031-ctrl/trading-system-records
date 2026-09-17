---
name: tick-snap-failopen-23jun
description: Recurring silver/ETF tick rejections — adapter _snap_order_to_tick FAILED OPEN on missing tick_size; 3-part fix IMPLEMENTED + deployed 23-Jun (478673f + 1313a08), activates 03:30
metadata: 
  node_type: memory
  type: project
  originSessionId: e1a15ec3-5140-4531-93b5-a58f94e7260a
---

**Recurring Zerodha "enter price in multiple of tick size" rejections (HDFCSILVER, SILVERBETA, IRIS, etc.) — diagnosed + ✅ FIXED + DEPLOYED 23-Jun (commits 478673f + 1313a08, pushed, NO restart → activates at Rama's 03:30 restart).**

**Root cause:** the authoritative tick chokepoint already exists — `broker/zerodha_adapter.py:_snap_order_to_tick` (FIX-181 "GICRE incident"), applied in `place_order` at line 483 **before** the paper branch (so it's parity-correct), covering every `place_order` caller. But it **FAILS OPEN**: when `instrument_cache.tick_size(symbol)` **raises `InstrumentNotFoundError`** (symbol absent from `config/instruments.csv`), the `except Exception: return price, trigger_price` at **zerodha_adapter.py:922-923** returns the price **un-rounded** → off-tick submit → rejection. Same no-op on cache-None (918) and tick≤0 (924-925). `tick_size()` *raises* on a missing symbol (it validates tick>0 at load), it does not return None — so the exception branch is the live trigger.

**Symbol gap (confirmed against VM `instruments.csv`, 2229 rows):** HDFCSILVER **absent**, SILVERBETA **absent** → hit fail-open. IRIS **present** (tick 0.05) → likely a *past* rejection from the 03-May→21-Jun instruments-staleness window, now resolved.

**Second hole:** `zerodha_adapter.modify_order` (line 626) does **NOT** snap at all — `price`/`trigger_price` go straight to Kite; used by `breakeven_manager.py:289` (SL advance) + `smart_tgt_manager.py:588` (TGT modify) → off-tick even for *known* symbols; paper returns early (641) → paper/live divergence.

**Rounding inventory (de-dup target):** 3 impls — `orders/price_math.py:round_to_tick` (proper, Decimal) · `zerodha_adapter._snap_order_to_tick` (the right chokepoint, uses price_math helpers) · `orders/order_placer.py:_round_to_tick` (3695-3711, float-floor, same fail-open, applied 775-779) = **redundant + inferior**.

**✅ FIX IMPLEMENTED + DEPLOYED 23-Jun (scope = all three; pushed to `main`, NO restart → activates 03:30):**
1. **Fail-safe** — new `zerodha_adapter._resolve_tick()` returns `DEFAULT_TICK` (0.05) on cache-None / `InstrumentNotFoundError` / tick≤0 with a throttled per-symbol WARN (`snap_to_tick.missing_tick_size`, FIX-170 visibility); `_snap_order_to_tick` routes through it → NEVER un-rounded. SL round-past-trigger direction unchanged. **(commit 478673f)**
2. **modify_order** — new optional `symbol`; snaps price+trigger BEFORE the paper branch (parity); threaded from `breakeven_manager.py:289` + `smart_tgt_manager.py:588`. NB both callers already pre-snapped (idempotent) so the modify hole was not live-exploited — this centralises it at the chokepoint. **(478673f)**
3. **De-dup** — removed `order_placer._round_to_tick` + its 3 entry calls; the adapter is the sole snap point (`_tick_for` kept for the emergency-exit marketable-LIMIT). Gated on the green no-bypass test. **(commit 1313a08)**
Tests: `tests/unit/test_tick_failsafe_snap.py` (13: missing→0.05+alert never un-rounded · IRIS 0.05 · 0.01-tick symbol-specific · SL direction · modify parity · no-bypass place_order) + 2 updated FIX-181 fail-open tests; **373 then 325 passed** across affected suites. `DEFAULT_TICK` imported from `orders.price_math`; round helpers from `broker.slippage_engine`.

**NO-BYPASS AUDIT — COMPLETE (re-confirmed 23-Jun ~21:00, read-only):** Exactly **TWO** broker-submission primitives — `zerodha_adapter.place_order` (kite call :515) + `modify_order` (:656). Every other `self._kite.*` is read/cancel, no price submitted: cancel_order(603), order_history(718), positions(778), margins(981), order_margins(1068), quote(1190/1232/1290), trades(1315), orders(1370). **No GTT/bracket/CO submission primitive** (CO = `place_order(variety="co")`, so it funnels through place_order). Repo-wide grep: **NO production code calls kite directly** — every `.place_order(`/`.modify_order(` is `self._adapter.…` (order_protocol_limit/_co, order_placer emergency, order_reconciler G5b, eod_squareoff, sl_breach_monitor, kill_switch flatten, breakeven_manager, smart_tgt_manager). **Caveat (surface):** `broker/angelone_adapter.py` has its OWN unsnapped place_order/modify_order — **DORMANT** (Zerodha-only live, LFL836); the snap lives in zerodha_adapter only, so if AngelOne is ever activated it needs the same treatment (or move the snap to a shared base). Fail-open re-confirmed current-tree: 3× `return price, trigger_price` at **:919** (cache-None) / **:923** (`except` → InstrumentNotFoundError) / **:925** (tick≤0). Symbol gap UNCHANGED (instruments.csv mtime 09:00:01, 2229 rows): IRIS 0.05 present; HDFCSILVER + SILVERBETA absent.

**DE-DUP SEQUENCING:** ship (a)+(b) first; do (c) [delete `order_placer._round_to_tick` 3695-3711 + calls 775-779] **ONLY AFTER** a no-bypass test asserts the adapter snap is the sole snap point (NOCIL lesson — don't remove the redundant path until coverage is proven). Push with **NO restart** → activates at Rama's 03:30 restart.

**SEPARATE FOLLOW-UP (FIX-170 — NOT part of this fix, per Rama):** HDFCSILVER + SILVERBETA **absent from `instruments.csv`** (also get token=0/lot=1 via RI12) = instrument-universe gap. The 0.05 fallback makes orders placeable but the missing-tick alert is what surfaces this for instrument-master correction. Track + fix the universe separately.

**Why:** each rejected order = a VALID signal silently lost; fail-open turns a missing-instrument data gap into a trading outage. **How to apply:** when a fresh current-dated instruction authorizes it, implement the 3 parts at the adapter chokepoint (one place, no per-call-site patch), parity in both modes, then push (no self-restart). See [[fix_181_complete]] (the GICRE tick chokepoint), [[instruments_staleness_incident_21jun]] (FIX-170 universe), [[deploy_requires_restart]].
