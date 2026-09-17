---
name: Temporary paper testing changes (REVERT BEFORE LIVE)
description: CRITICAL - all strategy entry_end_time set to 15:20 + system config overrides; full revert table in pending_skipped_items.txt
type: project
originSessionId: 20e7cadd-4487-4f2d-87c2-551f76dc9808
---
**BEFORE LIVE TRADING: Revert ALL temporary paper config changes.**

Paper rehearsal uses extended entry window 09:20-15:20 which is NOT production config.

## Strategy entry_end_time (ALL set to 15:20 — commit b7704f6, 04-May-2026)

| Strategy | Paper value | Production value |
|----------|------------|-----------------|
| gap_fade_long | 15:20 | 11:30 |
| gap_fade_short | 15:20 | 11:30 |
| gap_go_long | 15:20 | 11:00 |
| gap_go_short | 15:20 | 11:00 |
| first_pullback_long | 15:20 | 13:30 |
| first_pullback_short | 15:20 | 13:30 |
| open_low_breakout_long | 15:20 | 13:30 |
| open_high_breakdown_short | 15:20 | 13:30 |
| vwap_bounce_long | 15:20 | 13:30 |
| vwap_rejection_short | 15:20 | 13:30 |
| range_breakout_long | 15:20 | 13:30 |
| range_breakout_short | 15:20 | 13:30 |
| positional_momentum_long | 15:20 | 14:30 |
| positional_swing_long | 15:20 | 14:30 |
| positional_sector_rotation | 15:20 | 14:30 |

## Other temp overrides (from 28-Apr session)

| File | Parameter | Paper value | Production value |
|------|-----------|------------|-----------------|
| gap_fade_long.yaml | min_score | 30 | 0 (scorer default) |
| system_config.yaml | max_consecutive_losses | 20 | 4 |
| system_config.yaml | daily_loss_limit_pct | 1.00 | 0.05 |
| system_config.yaml | daily_loss_limit | 100000 | 10000 |
| system_config.yaml | capital_drift_tolerance | 100000 | 50 |
| system_config.yaml | drift_handler thresholds | 100K/200K/500K | 250/1000/2500 |
| fund_manager.py | _INVARIANT_TOLERANCE | 100.0 | 0.01 |

**Why:** Paper testing needs extended windows to exercise all strategies throughout the day. Production uses strategy-specific windows tuned to market microstructure.

**How to apply:**
1. Revert ALL values in this table before live Day 1 (target: 11-May-2026)
2. Full checklist: `docs/pending_skipped_items.txt`
3. Each YAML has `# TEMP PAPER: was XX:XX -- REVERT BEFORE LIVE` comment
4. Paper/Live parity: NEEDS-SYNC
