---
name: tiered_slippage_abort
description: "Entry-slippage abort = %-of-SL-distance (20-Jun, commits d464f33→3ddb774). entry_gate.slippage_control mode=sl_fraction (default): tolerance=min(SL_dist×0.22, Rs5 cap), Rs10 hard ceiling; flat_tiers+pct modes for A/B. Pre-order guard in order_placer.place(); calibrate via fraction_of_sl_used logs. THELEELA aborts; LLOYDSENGG aborts at 0.22 (raise to ~0.27 to allow)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e7a6af13-236a-41d8-aca5-213b591647fd
---

**ENTRY-SLIPPAGE ABORT — now %-of-SL-distance (20-Jun, evolved d464f33 → 3ddb774).** Started as flat-Rs
price-band tiers; **same day Rama switched the default to % of the SL distance** (the
[[slippage_calibration_data_20jun]] investigation showed SL is FIXED/signal-based while TGT recalcs from
the fill — FIX-013 — so entry slippage directly inflates the risk budget). Config is now
`entry_gate.slippage_control` (NOT `slippage_tiers`), **mode-selectable**:
- **`sl_fraction` (DEFAULT):** `tolerance = min(SL_dist × max_slippage_fraction(0.22), absolute_cap_rs(₹5))`
  where `SL_dist = |signal_trigger − sl_price|`. Auto-scales with price AND strategy SL%. Cap-only if SL
  missing.
- **`flat_tiers`** (the original per-band Rs, kept for A/B) and **`pct`** (signal×max_entry_slippage_pct).
- **`hard_max_slippage_rs(₹10)`** = absolute ceiling in EVERY mode. `also_apply_pct_check` = flat-%
  belt-and-suspenders. `enabled:false` → legacy flat %.
Pure helpers `_compute_slippage_tolerance` + `_slippage_decision` (orders/order_placer.py). Verified live
(5 spec examples: THELEELA@481 tol ₹2.12 → ₹3.10 ABORT; vwap@200 ₹0.35; gap_fade@500 ₹1.10; positional@2000
backstop ₹5; CHEMPLASTS@221 ₹0.73 ABORT). **CALIBRATION FINDING:** LLOYDSENGG (₹0.43 = 26% of its 2% SL)
**ABORTS at 0.22** — raise `max_slippage_fraction` to ~0.27 to allow it; tune from `entry_slippage_observed`
logs (`fraction_of_sl_used`). **Step 7.3 (LIMIT=signal+tolerance) deliberately NOT done** (no-op when the
guard passes — `release_ltp` cap dominates; risks non-fills when planned-entry≠trigger; doesn't fix the
CO/SL gap). The historical flat-tiers notes below are superseded but the mechanics still apply.

---
**(historical) TIERED ENTRY-SLIPPAGE ABORT (per-price-band, in RUPEES) — commit d464f33.** Augments
the flat `entry_gate.max_entry_slippage_pct` (1%) with a calibratable RUPEE tolerance by price band.
Born from THELEELA: trigger 481.50, ~₹2.60 slip (0.54%) PASSED the flat 1% (=₹4.81); Rama wanted
tighter, band-specific control.

## How it works
Pre-order guard in `order_placer.place()` (the existing FIX-128 LTP-vs-trigger check): computes
`slip_rs = |LTP − signal_trigger|` + `slip_pct`, then `_slippage_abort_reason()` (orders/order_placer.py,
pure/testable) aborts if `slip_rs > band.max_slippage_rs` (tiered, when enabled), THEN the flat
`max_entry_slippage_pct` (kept as belt-and-suspenders when `also_apply_pct_check`, the SOLE gate when
tiers disabled → backward compat). Abort → `OrderRejectedError`, trade REJECTED, WARNING alert (Telegram
+ email fallback). Band lookup `tier_slippage_tolerance_rs` (orders/price_math.py): first band with
`price < max_price` — **lower bound EXCLUSIVE** (₹100.00 → 100-200 band).

## Config (system_config.yaml → `entry_gate.slippage_tiers`) — EDIT to calibrate, restart to apply
Starter: `<100→₹1.00, 100-200→₹1.25, 200-500→₹2.00, >500→₹3.00`; `default_max_slippage_rs: 2.00`;
`enabled: true`; `also_apply_pct_check: true`. Models `EntrySlippageTiersConfig`/`SlippageTier` in
core/config_loader.py (`extra="forbid"`). `enabled: false` → flat % only.

## Calibration data
EVERY entry logs `order_placer.entry_slippage_observed` (symbol/trigger/LTP/slippage_rs/slippage_pct)
even when ALLOWED → grep logs to see the real slippage distribution per band and tune `max_slippage_rs`.
Aborts log `order_placer.slippage_guard_exceeded` with the reason. **Follow-up NOT done** (noted to Rama):
a dedicated `/metrics` `entries_rejected_slippage` counter + an EOD-report slippage-abort count — the
logs carry the data for now.

## Verified live (deployed)
THELEELA (481.50, ₹2.60) → `slippage ₹2.60 > tier tolerance ₹2.00 (band for ₹481.50)` ABORT; ₹1.50 →
allow; 600 (>500 band) ₹2.80 → allow. Config loads on the VM. **Parity:** the guard runs in `place()`
for paper + live; config mode-agnostic. +18 tests (`test_slippage_tiers.py`); 142 slippage+order_placer
tests pass. Activates next restart (Mon 08:30). **Abort-only = safe direction** (never places a worse
order; over-abort is just a missed trade, calibratable). NB editing system_config.yaml changed its hash
→ the Phase-1 security-watcher emits one WARNING "system_config changed" (expected for a config deploy).
Related: [[task_8_config_guide]], [[fix_190_incident]].
