---
name: Four bugs identified 2026-04-29
description: Entry window hardcode, log formatting, missing trades, missing exit alerts - fixes and investigation notes
type: project
originSessionId: b2686c5d-ac77-4544-9f06-8be8428ac9f2
---
## Issue 1: Entry window mismatch (FIXED)

**Symptom:** Config says 09:20 but rejection logs show "09:30-15:00"

**Root cause:** All 15 strategy YAMLs had `entry_start_time: "09:30"` hardcoded, ignoring system config's 09:20.

**Fix applied:** Updated all config/strategies/*.yaml from `entry_start_time: "09:30"` to `entry_start_time: "09:20"`

**Why:** Per-strategy entry window (CFG-5) composes with global window. If strategy says 09:30 but global says 09:20, signals at 09:25 pass global check but fail strategy check.

**How to apply:** Add to ConfigValidator TODO (HIGH PRIORITY): validate strategy entry times fall within system config entry window bounds.

## Issue 2: Stock names not quoted in logs (FIXED)

**Symptom:** Log shows `rejected at OUTSIDE_ENTRY_WINDOW` without symbol quoted

**Fix applied:** signals/signal_processor.py lines 603 and 1008 - changed `({symbol})` to `("{symbol}")`

Now logs: `Signal SIG123 ("RELIANCE") rejected at OUTSIDE_ENTRY_WINDOW: reason`

## Issue 3: No trades after 09:30 (INVESTIGATION NEEDED)

**Symptom:** No trades executing despite signals passing entry window

**Investigation steps (run on VM when accessible):**
```bash
sqlite3 data_store/trading.db "SELECT * FROM kill_switch_state;"
sqlite3 data_store/trading.db "SELECT signal_id, symbol, status FROM signals WHERE created_at > '2026-04-29 09:30:00' LIMIT 20;"
```

**Possible causes:**
- Kill switch active from previous session
- daily_loss_limit triggered
- entry_gate blocking all signals
- No webhook signals received

## Issue 4: No TGT/SL alerts in Telegram (TIED TO #3)

**Symptom:** SL/TGT orders placed but no Telegram alerts for exits

**Analysis:** Alert code exists at order_placer.py:1261-1284 and shadow_tracker.py:606-662. Both use `notifier.send()`.

**Root causes identified:**
1. HARD_KILL at 09:30:40 blocked all processing including alerts
2. With LTP-gating in paper mode, SL/TGT orders only fill when LTP crosses trigger
3. If no trades open (Issue 3), nothing to exit

**No code change needed** - alert infrastructure exists. Once Issue 3 resolved and orders fill, alerts will flow.

## Issue 5: ZERO_SL rejections for ATR strategies (FIXED)

**Symptom:** positional_swing_long rejected with ZERO_SL

**Root cause:** sl_method=ATR strategies had sl_pct=0.0. When ATR data unavailable, signal_processor falls back to sl_pct. Zero sl_pct → ZERO_SL rejection.

**Fix applied:** Set sl_pct=0.02 (2% fallback) in all 3 ATR strategies:
- positional_swing_long.yaml
- positional_momentum_long.yaml
- positional_sector_rotation.yaml
