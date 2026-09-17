---
name: slice25_phase4_trade_type_gate_26jun
description: "SLICE2.5-PHASE-4 — trade_type reject-by-intent gate was ALREADY built (Slice 2 strategy_will_trade); Phase 4 = confirm + split a distinct TRADE_TYPE reject label + go-live scenario tests; Option B parked; staged, dormant"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b445dff-c546-4ec1-b292-3ec665699a63
---

**SLICE2.5-PHASE-4 (26-Jun-2026): trade_type reject-by-intent gate — CONFIRM + HARDEN.**
The last Slice 2.5 build. **Key finding:** the gate Phase 4 set out to add ALREADY EXISTS
and is live — Slice 2's `strategies/control.strategy_will_trade` LAYER 1×2 (`:82-94`) already
does: trade_type=INTRADAY → reject DELIVERY-intent; DELIVERY → reject INTRADAY-intent; BOTH →
accept both — keying on the EFFECTIVE (post-coercion) `strategy_obj.intent`, wired into BOTH
`signal_processor` paths (`_process_one` ~:625, `continue_from_gate` ~:1330) BEFORE sizing,
metric'd via `entries_rejected`, dormant under the current config. So Phase 4 did NOT add a gate.

**What Phase 4 actually built (Option A):**
- **Observability label split (the only live-path touch):** a trade_type×intent mismatch now
  rejects with a DISTINCT label `TRADE_TYPE` (→ signal status `REJECTED_TRADE_TYPE` + its own
  `_stats["rejected"]["TRADE_TYPE"]` tally), so at delivery go-live Rama can SEE trade_type
  rejects apart from other strategy-control rejects. Mechanism: a machine-readable
  `Verdict.cause` field (`strategies/control.py` — `CAUSE_OK`/`CAUSE_DISABLED`/
  `CAUSE_FORCE_BREAKER`/`CAUSE_TRADE_TYPE`, default OK), set at each return site; the gate maps
  `cause==CAUSE_TRADE_TYPE → "TRADE_TYPE"`, everything else (disabled switch, force-breaker)
  stays `"STRATEGY_CONTROL"`. **Keyed on cause, never on the message string; reason strings
  UNCHANGED; accept/reject logic UNCHANGED.** Same change at both gate sites (byte-identical).
- **Go-live scenario tests** (`tests/unit/test_phase4_trade_type_gate.py`, 9): cause-per-layer
  + reason-strings-unchanged guard; INTRADAY/DELIVERY/BOTH (force=false) accept/reject matrix;
  ★ dormancy no-op (INTRADAY+force=true → WILL TRADE); ★ signal_processor label split
  (DELIVERY+INTRADAY → `REJECTED_TRADE_TYPE`); ★ label-bleed regression (disabled →
  `REJECTED_STRATEGY_CONTROL`, no bleed); contradictory DELIVERY+force=true → Config Auditor
  group-A BLOCK (confirm, not re-implemented — full fail-fast locked in test_config_auditor).
- Updated ONE Slice-2 test assertion (`test_master_intraday_blocks_delivery_at_process_one`:
  the trade_type-mismatch case now expects `REJECTED_TRADE_TYPE`, the intended relabel) +
  extended `test_signal_processor._make_proc` with optional `trade_type`/`force_intraday_only`.

**Dormancy:** under current config (trade_type=INTRADAY + force_intraday_only=true) every
strategy is coerced to INTRADAY at load → the gate accepts all → 0 rejects → the label split
never fires. ZERO Monday behaviour change. **No schema; parity** (shared gate module).

**OPTION B — PARKED (strategy-track question, NOT Slice 2.5):** gating on the DECLARED
(pre-coercion) intent would reject the 3 declared-DELIVERY `positional_*` strategies under the
current config (they trade LIVE as coerced-intraday today — `positional_sector_rotation` was
24-Jun's most active). That is a STRATEGY/product-performance decision, and **disabling those 3
via `strategy.enabled` would be the cleaner mechanism** if Rama ever wants it. The declared
intent is recoverable by re-validating the raw YAML (`scripts/strategy_status.py:74`), not on
the loaded object. Decide on the strategies' merit, separately from the delivery durability arc.

Full PC unit suite **3863 passed / 12 skipped / 0 regressions** (3854 baseline + 9). Branch `phase4-trade-type-gate-26jun` (stacked
on phase3 → FIX-183 → P2). **DEPLOYED to main `37b3db3` 26-Jun ~13:16 IST (one-time authorized batch with FIX-183-log + Phase 3; standing Rama-owns rule RESTORED after); restart self-exited 0 at the Muharram HOLIDAY guard, real boot Mon 29-Jun 08:15; verified broker-session-free PASS — DORMANT (trade_type gate no-op under INTRADAY+force=true, label split present, Auditor 0 BLOCK).** [orig: one push carried
FIX-183-deploy-log + Phase 3 + Phase 4). This COMPLETES Slice 2.5 (build side); remaining before
delivery_enabled=true: T2 (market-hours real-API/TPIN) + C1-watch (Monday).
See [[slice25_phase3_delivery_caps_conditional_capital_26jun]], [[fix_183_gtt_adoption_26jun]],
[[slice2_strategy_control_24jun]], [[slice25_p2_gtt_durability_25jun]].
