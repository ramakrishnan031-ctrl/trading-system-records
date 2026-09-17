---
name: slice25_phase3_delivery_caps_conditional_capital_26jun
description: "SLICE2.5-PHASE-3 — separate delivery (CNC) count caps + conditional capital allocation flag; both LOCKED but INERT (flag default false, delivery off); no schema; staged"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4b445dff-c546-4ec1-b292-3ec665699a63
---

**SLICE2.5-PHASE-3 (26-Jun-2026): delivery CAPS + CONDITIONAL CAPITAL.** The "capital"
one of the three delivery differences. TWO features, both built to stay correctly INERT
until deliberately activated. **No schema** (config + count methods + risk/fund logic).
Parity (risk_engine/fund_manager/state_store are shared). delivery_enabled stays **false**.

**FEATURE A — SEPARATE delivery (CNC) count caps:**
- Config `risk.max_open_delivery_positions` (3) + `max_daily_delivery_trades` (5)
  (`core/config_loader.py` RiskConfig + positive-int validator + `system_config.yaml`).
- New product-keyed counts (`core/state_store.py`): `count_open_delivery_positions()`
  (OPEN/PARTIAL/PENDING_FILL) + `count_daily_delivery_trades(date_iso)` (today, executed),
  both JOIN orders ON `leg='ENTRY' AND product='CNC'`, `COUNT(DISTINCT trade_id)`.
- Enforced in `capital/risk_engine.py::_run_checks`: OPEN_POSITIONS + DAILY_TRADES
  **branch on `sizing_result.bucket=="positional"`** (delivery → delivery-scoped cap;
  else → the EXISTING global check, byte-for-byte unchanged). Counts read lazily in
  `approve()` only when `bucket=="positional"` (zero extra DB queries on the intraday
  hot path). CONSECUTIVE_LOSSES deliberately stays SHARED.
- **Keying (from the coercion clarification):** current-entry → `bucket=="positional"`
  (the proven 1:1 proxy for "will be CNC"; resolved product not available pre-trade);
  counting existing → persisted ENTRY `product='CNC'`.
- **A5 — INTENTIONAL asymmetric coupling (documented in code + here):** the intraday/
  global branch is LEFT UNCHANGED, so it still counts ALL positions (incl. delivery) →
  delivery DOES count toward an INTRADAY entry's cap, while intraday does NOT count
  toward the delivery cap. Chosen to keep the LIVE intraday cap byte-for-byte unchanged
  (zero regression on the money path); at current capital, capital binds long before
  these counts → academic. Revisit full count-independence only if delivery scales.

**FEATURE B — CONDITIONAL capital allocation (replaces fixed-70/30-always):**
- Config `capital.conditional_allocation_enabled` (**default false**).
- Pure helper `capital/fund_manager.resolve_bucket_allocation(...)` → effective
  (intraday_pct, positional_pct), always sums to 1.0 (FM12): flag OFF → fixed config
  split (unchanged); flag ON → only-intraday 100/0, only-delivery 0/100, both → config
  split, neither → 100/0 (safe idle).
- `main.py` computes `delivery_active`/`intraday_active` (same predicate as the
  delivery_lock boot log) and passes the EFFECTIVE pcts into the FundManager ctor +
  logs `capital.bucket_allocation`. **FundManager is UNCHANGED** (only receives the
  final pcts; `initialize()` splits broker_balance by them). No-borrow/reject already
  enforced by `reserve()` (consults only the intent's bucket) — delivery 0% ⇒ every
  delivery reserve rejects "Insufficient positional capital", never borrows intraday.

**DORMANCY (deploy is a no-op):** flag default FALSE → 70/30 unchanged; while
force_intraday_only=true every strategy is coerced to intent=INTRADAY (loader, early)
→ bucket=intraday → the positional cap branch is never hit AND
`count_open_delivery_positions()==0`. Provably inert. Monday's boot changes NOTHING live.

**Tests** `tests/unit/test_phase3_delivery_caps_conditional_capital.py` (17): allocation
7 cases + dormancy proof + FM12 sum; delivery count methods (CNC-only); OPEN/DAILY
delivery caps reject; under-cap approves; ★ inertness (intraday bucket ignores delivery
cap; count==0 when only MIS); ★ MIS regression (global cap + message unchanged); no-borrow
reject path. Full unit suite **3854 pass / 12 skip / 0 regressions** (3837 baseline + 17).

**Branch `phase3-delivery-caps-conditional-capital-26jun`** (stacked on main = FIX-183 +
P2). **DEPLOYED to main `37b3db3` 26-Jun ~13:16 IST (one-time authorized batch with FIX-183-log + Phase 4; rule restored after); restart self-exited 0 at the Muharram HOLIDAY guard, real boot Mon 29-Jun 08:15; verified broker-session-free PASS — DORMANT (delivery_enabled=false, conditional_allocation_enabled=false, trade_type=INTRADAY → fixed 70/30, caps inert, Auditor 0 BLOCK).** [orig: NOT pushed; likely batched before Monday with
Phase 4). Phase 4 next; then T2 + C1-watch before delivery_enabled=true.
See [[fix_183_gtt_adoption_26jun]], [[slice25_p2_gtt_durability_25jun]],
[[dual_daily_loss_mechanism]], [[build1_config_authority_fixes_24jun]].
