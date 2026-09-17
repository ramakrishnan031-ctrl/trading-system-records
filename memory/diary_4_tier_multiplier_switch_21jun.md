---
name: diary_4_tier_multiplier_switch_21jun
description: "Tier-multiplier ON/OFF position-sizing switch (Diary #4) — config position_sizing.enabled; OFF = flat Rs/order (Option δ); default ON unchanged; schema v34; shipped 21-Jun"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b70d7c0-75fd-4f0b-9d69-93adc5e82b95
---

**Tier-multiplier ON/OFF switch** (Diary #4, shipped 21-Jun-2026). Lets Rama choose
per trading day whether position size depends on score (ON) or is a flat rupee value
irrespective of score (OFF).

**Config:** `config/system_config.yaml → position_sizing.enabled` (default **true = ON**).
- **ON** = existing score-tier (HIGH/MED/LOW = 1.0/0.7/0.5) × perf-weight sizing — **byte-unchanged**.
- **OFF** = flat Rs/order (Option δ): `position_sizing.flat_value_rs` (Pydantic
  `model_validator` rejects startup if OFF and flat_value_rs ≤ 0). flat_value_rs is **ONE
  MORE ceiling** on top of risk/capital/concentration (those still bind); score + perf NOT
  applied (score-neutral); flat < 1 lot → BELOW_MIN skip.

**Insertion point:** `capital/position_sizer.py calculate()` ON/OFF branch — sits **above
any paper/live split → parity clean**. constraint becomes `FLAT` when flat is the binding
ceiling. breakdown dict carries the audit fields.

**Schema v34** (EXPECTED_SCHEMA_VERSION=34): `trades` gains 10 sizing-audit columns
(tier_multiplier_mode / tier_weight_applied / perf_weight_applied / flat_value_rs_used /
qty_by_{risk,capital,concentration,flat} / binding_constraint / actual_position_value_rs).
Chosen `trades` over order_execution_log (per-leg + fill-time-only) — one sizing decision
per trade; mirrors the [[slippage_override_hierarchy_phase3a]] tolerance_source precedent.
`breakdown` plumbed signal_processor → order_placer.place() → order_manager.create_trade.
v34 = trades 12-step rebuild (MIGRATION_TABLES[34]); **DB-copy tested on the real 64MB live
DB (32→34, data preserved, idempotent, integrity ok)**. Live DB migrates Monday restart
(jumps 32→34 with the [[preflight_system_21jun]] v33 tables in one shot).

**Visibility:** pre-flight Phase A config display (TierMultiplierModeCheck, INFO) + Cron
Officer EOD badge ("Tier multiplier today: ON/OFF").

**Toggle (Rama):** edit `position_sizing.enabled: false` + uncomment/set `flat_value_rs: N`
→ `sudo systemctl restart trading-system` (or next-day natural restart). Startup log prints
the active mode. Flip back = `enabled: true`.

**Monday 22-Jun: ZERO behavioral change** — verified on VM `enabled=True, flat_value_rs=None`.
Commits 4c0ba43 (core) + 3382e55 (v34) + 57d4ead (Phase 5). ~25 tests; full suite 3560 green.

NB on `load_all` there are pre-existing `config_sanity:` cross-field warnings (max_position_value_rs
2500 > daily_loss_limit 300; entry_end within 15min of eod_squareoff) — the holistic **Config
Sanity Auditor** is the NEXT design topic (Rama + Web Claude discuss first; do NOT auto-start).
