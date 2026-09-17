---
name: v3_step9_exit_engine_12jul
description: V3 Step 9 — 03.09 Exit Engine VERIFY (FINAL shared-engine module); terminal exits/squareoff/kills COMPLETE + battle-tested → ZERO code change; CNC-exemption ledger (protective EXISTS, active-lifecycle PARKED); shared engine 03.01-03.09 COMPLETE
metadata:
  node_type: memory
  type: project
  originSessionId: e31b6e26-79d0-41d6-b1cc-db98a712e270
---

**V3 Shared-Engine — Step 9: 03.09 Exit Engine (12-Jul-2026). ADAPT = pure VERIFY. The FINAL shared-engine module → ZERO code change (do not churn proven exit/kill). LIVE exits BYTE-IDENTICAL by construction. This COMPLETES the shared engine (03.01–03.09).** Gap-map + delivery-exemption ledger: **`docs/v3/V3_STEP9_EXIT_ENGINE_GAPMAP.md`**. Follows [[v3_step8_trade_mgmt_12jul]].

**Ratified semantics honored:** 15:15 = ENTRY CUTOFF ONLY (`market_windows.is_past_eod_entry_cutoff:177-190`, enforced order_placer.place; NO position flatten); 15:17 = EOD squareoff (MIS/CO). No 15:15 flatten added.

**T1 verdict — every 03.09 requirement PRESENT (source-cited):**
- Terminal exits → `_handle_exit_fill` `close_trade`(double-close-guard) → `_cancel_oco_siblings`(`order_placer.py:4346`) cancels the survivor (no orphan re-fill).
- 15:17 squareoff `orders/eod_squareoff.py` two-pass (cancel resting SL/TGT → exit all MIS/CO with MARKET; CO via bracket-collapse).
- **DELIVERY/CNC EXEMPTION (the Slice-2.5 crux) = CNC filtered OUT** — `p.product in ("MIS","CO")` (`eod_squareoff.py:1023` FIX-015) + holdings-path filter (`:1390`) + EOD6 DB-side. Test `test_open_delivery_positions_not_touched` (G3).
- SYSTEM_OVERSELL `_detect_system_oversell`(`order_reconciler.py:1557`)+`_flatten_system_oversell`(`:1604`) → CHECK2 (RAMCOIND L3) → CRITICAL + auto-flatten.
- Scheduled-vs-emergency kill: `auto_clear_scheduled_kill`(`kill_switch.py:250`, `_is_scheduled_reason`) auto-clears scheduled; **HARD_KILL NEVER auto-clears** (`:256/264`); `clear_stale_state`(`:199`) clears prior-day kills at boot; manual `resume()`.
- HARD-kill cancel-FIRST: `_mark_trade_exiting`(`:956`) → `_cancel_trade_resting_exits`(`:971` FIX-190 Bug E, cancel resting SL/TGT at broker) → marketable-LIMIT flatten (FIX-181) via `_exit_all_trades_indestructible` (retry ≤2h FIX-180).
- Orphan/squareoff-fail: eod two-pass + write-ahead IN_PROGRESS→COMPLETE + reconciler A-1/E-1 recovery + FIX-183 GTT adoption + indestructible HARD retry. RAMCOIND 4-layer intact.

**T2 DELIVERY-EXEMPTION LEDGER (Slice 2.5 input — accuracy over optimism):**
- **EXISTS TODAY (active, PROTECT a carried CNC):** (1) 15:17 CNC filter (eod 1023/1390/EOD6); (2) reconciler delivery-exclusion — active-`gtt_state` trades excluded from CHECK1/G5b/CHECK9, kept in local_symbols so CHECK2 won't orphan-adopt (`order_reconciler.py:785-797`); (3) FIX-183 orphan-GTT adoption prepass (`:754`); (4) FIX-008 CNC overnight bootstrap = WARN only, no exit/soft_kill (`:668`); (5) **CncGttMonitor WIRED** (`main.py:2338/2364` SLICE2.5-P2 4a/4b; tests P1+P2 pass); (6) GTT primitives + get_holdings ungated.
- **MISSING/PARKED (active delivery TRADING; delivery OFF):** (1) CNC ENTRY off (`delivery_enabled false`/`force_intraday_only true`/`trade_type INTRADAY` → no NEW CNC placed; 3 positional_* dormant); (2) live lifecycle proof = T2 canary branch `854112b` (same-day PASSED, **DDPI overnight-carry UNPROVEN** = Mon→Tue `--arm-overnight`); (3) delivery SIZING knobs (Step-5 inert scaffold); (4) next-day carry end-to-end validation.
- **Honest framing:** PROTECTIVE exemptions EXIST+tested; ACTIVE delivery lifecycle PARKED behind `delivery_enabled=false`. Slice 2.5 = activation + overnight proof, NOT constructing the exemptions.

**T4 flagged (NOT changed):** no new exit flag needed (INTRADAY path complete). Carries the Step-8 breakeven∩structure single-SL-owner flag + Step-5/7 ATR-into-LIVE-SL flag. Slice 2.5 activation = Rama's parked decision (T2 ledger is its input).

**Gates:** **G1** — **0 exit-path files (`orders/*.py`, `kill_switch.py`, `market_windows.py`) modified by any V3 step** → LIVE exits byte-identical by construction. **G2 RAMCOIND MANDATORY** — dup-exit + oversell + eod_squareoff + kill_switch + order_reconciler + cnc_gtt_slice25 P1+P2 = **241 pass**. **G3 delivery-exemption** — `test_open_delivery_positions_not_touched` (CNC not squared off) + honest exists-vs-parked ledger. **G4** — no code change → zero new. paper==live. **VERIFY-only; nothing built; only artifact = the gap-map doc.** **★ SHARED ENGINE 03.01–03.09 COMPLETE** (Steps 1-9: Common Utils + S&R + Regime + Hard-Gate/scorer + Sizing + Allocator + Entry + Trade-Mgmt + Exit). NEXT = Web Claude + ChatGPT review → next phase: intraday pipeline plumbing → stateful watchlist + next-morning entry → PB-01 in shadow. Method: source-verified directly (no fan-out [[feedback_sequential_agents_only]]); SYSTEM_MAP read first [[feedback_system_map_first]].
