---
name: t2_repair_built_07jul
description: "T2 CNC-GTT proof branch fix-t2-repair-07jul. ef442ab=3-drift repair; 8773053 (10-Jul)=MARKET->marketable-LIMIT fix (Zerodha API refuses MARKET; canary NO-GO 10-Jul). LOCAL/UNPUSHED. Re-dry-run clean; VM temp updated; RE-CANARY READY (Rama, real order, likely Mon). Detail in the ledger."
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a31a746-372a-4611-aae1-88d2cfaa183f
---

**T2 repair BUILT 07-Jul-2026 ~11:10 IST.** Supersedes the NOT-READY verdict in [[t2_repair_verify_07jul]] (that was accurate at the time — the weekend repair was never executed). `scripts/t2_cnc_gtt_realtest.py` rebuilt fresh off current main **`eb75731`** per the still-valid spec [[t2_full_repair_scope_03jul]]. Committed to branch **`fix-t2-repair-07jul`@`ef442ab`** (LOCAL, UNPUSHED, NOT merged, NOT deployed). Supersedes the parked partial `fix-t2-import-02jul`@`b826ae0` (drift #1 only — discard).

> **⚠️ UPDATE 10-Jul — MARKET→LIMIT fix `8773053` (branch tip, on top of `ef442ab`).** The 10-Jul supervised live CANARY (IDEA x1) was REJECTED pre-fill by Zerodha: `InputException "Market orders without market protection are not allowed via API."` — NOTHING placed / zero exposure (canary did its job: fail cheap+safe). Root cause = the script placed raw `order_type="MARKET"` for its 4 real placements; Zerodha's API refuses MARKET without market-protection. **Fix (commit `8773053`, built via git-worktree so main@`8116b74` untouched):** all 4 → marketable LIMIT via the live helper `orders.price_math.marketable_limit_price` (fresh LTP ± `EMERGENCY_EXIT_BUFFER_PCT` 1%, tick-snapped; new `_marketable_limit`; missing-LTP aborts, no MARKET fallback). GTT/isolation/ensure_flat/confirm-flag/DDPI unchanged. Re-dry-run CLEAN (exit 0, 0 MARKET/4 LIMIT, throwaway proof, isolation, price-sample ~1% through touch). VM temp `/home/ubuntu/t2_proof_run/…py` updated (SHA `a5779420`) → RE-CANARY READY. DDPI active. Full detail + the re-canary scrip guidance (JIOFIN/NTPC/ONGC/TMPV <₹500) in [[unpushed_pending_deploy_ledger]].

## The 3 drifts — fixed (mirrored to authoritative signatures)
1. **L71 import:** `core.order_state_machine` → `broker.order_state_machine` (main.py:46).
2. **L83 RateLimiter:** `RateLimiter(cfg.broker_limits.rate_limits)` → `RateLimiter(cfg.broker_limits)` — `BrokerLimitsConfig` has no `.rate_limits` (fields: order/quote/historical/margins/…); mirrors main.py:1640.
3. **CncGttPlacer store wiring:** built without `store=` → `None` → `_persist_state` in-memory degrade → NO `gtt_state` row. Now `CncGttPlacer(..., store=<throwaway>)` + `hydrate_from_store()`.

## Throwaway-DB store wiring (ISOLATION — never the live DB)
- Fresh `StateStore` at **`data_store/t2_proof_<YYYYMMDD_HHMMSS>/t2_proof.db`** — in its OWN subdir. This matters: `core.db_connect.analytics_path_for(main_db) = main_db.parent/analytics.db`, so a bare `data_store/t2_proof.db` would ATTACH + init the **LIVE `data_store/analytics.db`**. The subdir isolates the analytics sibling too. An `_assert_isolated()` guard refuses any path resolving to the live main/analytics DB.
- **FK-chain seed — SPEC GAP FOUND:** the 03-Jul spec said "seed one trades row", but `trades.signal_id` is a NOT-NULL FK to `signals(signal_id)` (schema.sql:241) — so the trades INSERT itself FK-fails without a `signals` parent. Seed order: `signals` (trade_id=NULL) → `trades` (trade_id='t2'). Then `gtt_state.trade_id`→trades FK is satisfiable. (PRAGMA foreign_keys=ON, state_store.py.)
- `run_single_session` now also verifies the durable `gtt_state` ACTIVE row (the P2 criterion, not just `kite.get_gtt`) and marks it CANCELLED on cleanup.
- `--dry-run` rewritten: PAPER adapter + injected synthetic `quote_provider` (paper `get_quote` needs one) place a PAPER OCO GTT through the store-wired placer → proves a `gtt_state` row lands in the throwaway DB → verify → cleanup. Places NOTHING real, touches NO live DB.

## Validation — all clean (NO live run / deploy / push)
- **py_compile:** clean.
- **import-smoke (PC):** `_build_live_adapter('LFL836', paper=True)` builds the adapter (the exact call that reproduced drift #1 last session) — drifts #1+#2 gone.
- **`--dry-run` (PC AND VM):** EXIT=0. Throwaway `t2_proof.db` self-migrated to **v41**, got the `gtt_state` row (`gtt_id=9000000000001, trade_id=t2, IDEA, SELL, qty=1, sl=97/tgt=105`, ACTIVE→CANCELLED on cleanup); analytics sibling isolated inside the subdir; **live `trading_system.db` gtt_state 0→0** (VM live cnc_gtt placer independently hydrated count=0 at today's 08:15 boot); NO real order. VM run via base64 transfer to `/tmp/t2dry` (NOT the deployed path) + SHA-verified; temp + throwaway cleaned up after.

## State + next
- Branch `fix-t2-repair-07jul`@`ef442ab` UNPUSHED; main stays `eb75731` (working-tree script there is the OLD one — the fix is branch-only until live-validated).
- Doc updates (SYSTEM_MAP changelog + PATHS t2_proof path) are UNCOMMITTED on main's working tree, riding the next off-market sync alongside the Wave-3 closure doc edits.
- **Next = supervised live run** (Rama triggers, after reviewing the clean dry-run): buy→GTT→verify→square, no-TPIN proof, ends flat. PASS → commit-merge the branch + mark T2 COMPLETE. Live run instruction to follow separately.
