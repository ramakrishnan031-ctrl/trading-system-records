---
name: h8_shadow_tracker_strategy_column_06jul
description: "Wave-3 H-8 DONE (06-Jul, commit d2c19d9 unpushed) — ShadowTracker FIX-013 TGT recalc now reads the real `strategy` column (was dead `strategy_name`); closes the last active dead-column bug (H-1/kill_switch:977 siblings)."
metadata: 
  node_type: memory
  type: project
  originSessionId: ef106d19-b4cc-4e37-a32b-1f0eda14286e
---

**Wave-3 H-8 FIXED** (commit `d2c19d9`, main, UNPUSHED — Rama pushes off-market). One fix = one commit (`orders/shadow_tracker.py` + new `tests/unit/test_h8_shadow_tracker_strategy_column.py` ONLY; H-9 untouched). Ref finding H-8 in `docs/audit/full_system_audit_04july2026.md`.

**Root cause (dead-column class, sibling of [[h1_fixed_dead_column_05jul]] + kill_switch:977):** `shadow_tracker._on_position_closed:317` keyed the FIX-013 inning-1 TGT recalc on `trade["strategy_name"]`, but the trades column is **`strategy`** (`core/schema.sql:124` `strategy TEXT NOT NULL`). The row comes from `SELECT * FROM trades` (`:276-277`), so `strategy_name` was NEVER a key; guarded by `"strategy_name" in trade.keys()` it failed **SILENTLY** (always `""` — NOT an OperationalError, unlike H-1), so the `RISK_REWARD` recalc branch (`:320-334`) never ran → inning-1 `tgt_price` persisted as the theoretical DB target, not the fill-recalc'd one → inning analytics computed against the wrong target whenever entry slippage occurred.

**Fix:** one column name — `trade["strategy"] if "strategy" in trade.keys()`. The same function ALREADY reads `trade["strategy"]` at `:402` and `t["strategy"]` at `:624` (the `:601-603` query explicitly selects `strategy`) — only `:317` was wrong (fixed every occurrence on the path; the `strategy_name` local var + kwargs are just names, correct). No new try/except, no fallback.

**Consumer scan:** `tgt_initial` → `Inning.tgt_price` (`:372`) → `insert_inning` (analytics only). The fix only makes the recalc branch RUN for RISK_REWARD strategies with slippage; no downstream contract change. **Analytics-only impact** (ShadowTracker is the shadow/observer path) — no money-path effect.

**Parity:** ShadowTracker is a single shared instance (`main.py:2137`), tick+event driven, mode-agnostic — no paper-specific duplicate.

**Test** (`test_h8_shadow_tracker_strategy_column.py`; REAL `_on_position_closed` + `calc_tgt_price` + REAL StateStore/schema, reusing the existing shadow_tracker harness `_make_tracker`/`_seed_signal`/`_seed_trade`/`_MockStrategy`; only strategy config + time/market/notifier fakes simulated): a RISK_REWARD strategy (rr=2) with entry 2510 / sl 2450 recalculates inning-1 tgt to **2630** (vs theoretical DB 2600); a FIXED_PCT control keeps 2600 (branch correctly gated). RED proven by reverting `:317` to `strategy_name` (tgt stayed 2600). **55 green** (H-8 + full shadow_tracker suite); 0 regressions.

**Residual risk:** closes the LAST active dead-column bug (H-1✓, kill_switch:977✓, H-8✓); impact was analytics-only. **H-6's CNC dead-column remains (delivery-gated, out of scope).** No schema/path/cron/service change.

Related: [[h1_fixed_dead_column_05jul]] · [[h11_invalidate_token_path_06jul]] · [[h13_token_monitor_relatch_06jul]] · [[h12_paper_positions_signed_06jul]]. **Wave-3 status: H-12✓ · H-13✓ · H-11✓ · H-8✓ · H-9 PENDING.** STOP after H-8 (did not start H-9); await review.
