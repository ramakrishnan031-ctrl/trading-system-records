---
name: t2_repair_verify_07jul
description: "T2 proof-script full repair (planned 03-Jul, supposed to be built off-market) was NEVER EXECUTED — verified 07-Jul: 0/3 known drifts fixed, store wiring never implemented, no clean dry-run possible. NOT READY for a live run."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a31a746-372a-4611-aae1-88d2cfaa183f
---

**[SUPERSEDED 07-Jul ~11:10 — the repair is now BUILT: [[t2_repair_built_07jul]] (branch `fix-t2-repair-07jul`@`ef442ab`, dry-run clean). The finding below was accurate at verification time (~09:40, before the build).]**

**Verdict: NOT READY.** The "full repair built off-market" Rama's instruction referenced did **not** happen — `scripts/t2_cnc_gtt_realtest.py` on main is byte-identical to its pre-repair state audited in [[t2_full_repair_scope_03jul]]. Exhaustive check (all branches/reflog/stash): no repair branch or commit exists beyond what was already known.

## Per-drift status (0/3 fixed)
1. **L71 import — STILL BROKEN.** `from core.order_state_machine import OrderStateMachine`; `core/order_state_machine.py` does not exist (module is `broker/order_state_machine.py`, confirmed main.py:46). **Live-reproduced right now:** calling `_build_live_adapter()` raises `ModuleNotFoundError: No module named 'core.order_state_machine'`.
2. **L83 RateLimiter — STILL BROKEN.** `RateLimiter(cfg.broker_limits.rate_limits)`; `BrokerLimitsConfig` has no `.rate_limits` field (actual fields: order/quote/historical/margins/backoff_sequence_sec/timeouts/rate_limit_backoff). Independently confirmed against the live loaded config: `AttributeError: 'BrokerLimitsConfig' object has no attribute 'rate_limits'`. Correct call (main.py:1640): `RateLimiter(app_config.broker_limits, ...)`.
3. **L318-322 store wiring — STILL BROKEN / NEVER IMPLEMENTED.** `CncGttPlacer(...)` constructed with no `store=` kwarg at all → defaults to `None` (`cnc_gtt.py:67`) → `_persist_state` degrades to in-memory, no `gtt_state` row, P2-lifecycle criterion unverifiable. The 03-Jul-designed throwaway-DB fix (`StateStore("data_store/t2_proof_<date>.db")` + synthetic seed row + `hydrate_from_store()`) was never coded — **zero `StateStore` references anywhere in the file** (full 329-line read).

## Store-wiring status
Not wired to anything, throwaway or otherwise — confirmed absent (see #3 above).

## Dry-run status
**No clean dry-run has occurred, and none could have** — drift #1 kills `_build_live_adapter()` (called main():305) before the dry-run branch (:312-313) is ever reached. Confirmed by directly invoking `_build_live_adapter('LFL836', paper=True)` just now: identical `ModuleNotFoundError`. Any dry-run attempt today fails the same way.

## Commit/branch/push state
- No full-repair branch/commit exists anywhere (all branches + full reflog + stash searched).
- Only artifact: `fix-t2-import-02jul`@`b826ae0` (02-Jul, PRE-DATES the 03-Jul full-repair scope) — fixes **drift #1 ONLY**, one-line diff (`core.`→`broker.order_state_machine`). **Local-only, unpushed** (no matching ref on `origin`), **NOT an ancestor of main/HEAD** — main was never touched. Even if cherry-picked alone, drift #2 would immediately surface next.
- `f009cc7` (ensure-flat, 30-Jun, already merged to main) is unrelated — that's the earlier `finally`-block safety fix, not the 3-drift repair.

## Likely explanation
The weekend (04/05-Jul) that was slated for the T2 repair was spent instead on the security wave (S-1A/S-1B webhook lockdown + Wave-3 H-12/13/11/8/9) per [[MEMORY]] Recent Operations — T2 was superseded, not completed. Deferred-board status in MEMORY.md ("live never run — proof script bit-rotted") remains accurate as-is; this file is the 07-Jul re-verification confirming nothing has changed.

## What's needed before a live run
Rebuild all 3 fixes + store wiring fresh off current main (`eb75731`), per the exact spec in [[t2_full_repair_scope_03jul]] (still valid — one-pass audit found no new drift beyond these 3) → py_compile + import-smoke → clean `--dry-run` on VM → commit → then a supervised live run.
