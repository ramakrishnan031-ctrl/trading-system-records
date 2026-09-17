---
name: fix067_ms1_investigation_07jul
description: "FIX-067/M-S1 (Wave-5) BUILT & committed 3f4587f — momentum fresh-LTP re-anchors the FULL placement basis (entry+SL+TGT+qty+reservation) + D1 plumbing root + retest twin; RED→GREEN, 0 regressions"
metadata:
  node_type: memory
  type: project
  originSessionId: df81c82b-0008-4607-9772-4da4d52b138f
---

**Wave-5 · FIX-067 / M-S1 — momentum fresh-LTP re-anchor. ✅ BUILT & COMMITTED `3f4587f` (main, UNPUSHED — off-market push later).** Rama gave GO on Q1-Q4 (see below); completes the 16-May partial `d37ad62` (entry-only fresh quote). One fix = one commit = one validation cycle. Terminal-state guard / M-C1 remain (NOT touched).

## What shipped (`signals/signal_processor.py`)
**Two coupled defects fixed together (Q1=BOTH):**
- **D1 (plumbing, the real root — the fresh branch was INERT):** `_process_one` called `self._quote_fn(symbol)` with a BARE STRING + `.get("last_price")`, but `broker_adapter.get_quote(symbols: list[str]) -> dict[str, Quote]` (frozen dataclass `Quote`, attr `.last_price`, keyed by bare symbol; `NSE:` stripped @zerodha_adapter:1588). String iterated per-char + `Quote` has no `.get` → None → SILENT stale-fallback in BOTH modes → FIX-067 undelivered since 16-May. Precedent: order_placer FIX-180. Twin at `_retest_entry_estimate:2018`.
- **D2 (logic, audit M-S1):** `fresh_entry_price, _ = _derive_prices(...)` DISCARDED the fresh SL → SL/TGT/sizing/reservation stayed stale-anchored (SL drifts out of bounds, R:R skews, reserved capital ≠ order value, adverse move can put a LONG's stale SL ABOVE fresh entry).

**Fix (Q4 = COMPLETE re-anchor, not SL/TGT-only):** fetch the live LTP ONCE, AFTER the retest diverter (its routing zone-check keeps its trigger basis — unchanged) and BEFORE sizing; `entry_price, sl_price = _derive_prices(live_ltp,…)` re-anchors, and downstream `_derive_target` + `sizer.calculate` + `fm.reserve` all consume the fresh entry/SL. D1 convention `quotes=self._quote_fn([symbol]); q=quotes.get(symbol) if quotes else None; live_ltp=float(q.last_price) if q is not None else None` at BOTH sites. Removed the old inert FIX-067 block AND the 3rd `fresh_entry_price` ref in `_sr_observe` (would NameError→PLACEMENT_FAILED — caught in the test run, fixed).

## The 4 open questions — Rama's decisions (RESOLVED)
- **Q1 = BOTH D1+D2 together.** (D2-alone edits inert code; D1-alone arms the latent skew.)
- **Q2 = fix the retest twin in this commit; it's D1-ONLY** (returns an LTP estimate for MARKET-entry sizing; derives no SL — the retest SL is `structure_sl` from zone bands, independent). Confirmed by caller @signal_processor:1843.
- **Q3 = REUSE FIX-128, no new abort.** It owns `delta>SL_budget` and now sizes its tolerance off the CORRECT fresh SL — `_slippage_decision(_scfg, signal_trigger_price, sl_price,…)`@order_placer:1012 consumes the `sl_price` place() now receives (fresh). `trigger_price` preserved for it. Accepted the ≤move tolerance-ref shift (bounded; flat-% + hard-ceiling backstopped).
- **Q4 = COMPLETE the fix** (entry+SL+TGT+qty+reservation ALL on the fresh anchor), fetch BEFORE sizing/reserve, **preserve H-7 atomicity**. **BUILD-GATE CLEARED (no STOP):** H-7's cap-check+approve+reserve inside `portfolio_lock` is count-based, ORTHOGONAL to price — the re-anchor only changes the *values* fed to `reserve()` (computed before the lock); the network fetch stays OUTSIDE the lock. `portfolio_lock` block byte-unchanged.

## Parity
Single shared path; `_make_paper_quote_provider` (main.py:394) returns the same `dict[str, Quote]` keyed by the ORIGINAL symbol with a REAL Kite LTP → identical re-anchor both modes. get_quote paper path @zerodha_adapter:1562 delegates to the provider.

## Tests (`tests/unit/test_fix067_ms1_fresh_anchor.py`, NEW — real pipeline)
REAL `_process_one` + REAL `_derive_prices`/`_derive_target`; only quote/placer/sizer/fm are RECORDING doubles (assert on real derivations). T1 D1 list-convention exercised · T2 fresh SL+TGT (M-S1 core) · T3 sizing inputs + reservation price on fresh anchor · T4 H-7 portfolio_lock section preserved (source: fetch precedes lock; cap-check ×3, single def; both sites `[symbol]`; no bare-string call) · T5 retest twin returns live LTP · T6 paper-provider parity · +pullback-skip guard. **RED→GREEN proven** by `git stash` of the source vs HEAD `2023948`: RED = 6 fail (only the invariant pullback-guard passes), GREEN = 7 pass. `test_sr_v2_continue.py` 3 stubs moved off the old `_quote_fn` shape → `dict[str, Quote]` (D1 fallout, faithful). **320 green affected + 63 adjacent; 0 regressions.**

## Residual (NOTE, Q4-bounded)
qty/reservation now use fresh-anchored inputs (reserved == order value). Only residual = FIX-128 tolerance ref shifts by ≤ the move (bounded). No schema/path/cron/service change.

## State
Repo HEAD `3f4587f` (main, UNPUSHED). SYSTEM_MAP.md changelog entry added (working-tree, rides the pending off-market doc-sync alongside PATHS.md + the H-7/T2/Wave-3/4 leftovers). PATHS.md unchanged (no FIX-067 path change). NOT pushed, NOT deployed.
Related: [[h7_strategy_cap_toctou_07jul]] · [[full_repo_audit_04jul_pending]]
