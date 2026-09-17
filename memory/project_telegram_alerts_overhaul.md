---
name: Telegram alerts overhaul (23-Apr-2026, commit 9013845)
description: Rich mode-prefixed Telegram alerts across 7 modules; 9 reformatted + 6 new; 1657 green; EOD daily summary added.
type: project
originSessionId: eb145941-994c-4e5f-a96d-b9d1eaef9d9e
---
Telegram alert formatting overhaul landed 23-Apr-2026, commit **9013845**. PC = VM parity confirmed via post-receive hook at 16:02:48 IST.

**Why:** Paper Week 1 is exposing how sparse the original alert text is. Rama wants richer per-event alerts (signal / order / exit / EOD summary) with clear `[PAPER]`/`[LIVE]` mode prefixes so Telegram is usable as the primary ops channel while he's away from the PC.

**How to apply:** When a new event type gains a Telegram alert, follow this shape — `title="[MODE] <emoji> <EVENT> — <symbol>"`, body uses `₹` formatting with `{,.2f}` for rupees, `IST` on timestamps, and `severity` set to INFO/WARN/CRITICAL to match the existing notifier contract. All 7 production modules now accept `mode: str = "LIVE"` in `__init__` and main.py propagates `mode_label = args.mode.upper()` into every one.

## What changed (9 files, +454/-45)

### Production (7 modules)
- `capital/kill_switch.py` — notifier + mode ctor args; `set_notifier()` post-construction setter; SOFT KILL ⚠️ alert
- `main.py` — mode_label propagation; `kill_switch.set_notifier(notifier, mode=mode_label)` after notifier builds; reformatted titles: 🚀 System Active, 🛑 System Stopping, 🚨 Critical Failure, 🚨 Orphan Order Detected, ⚠️ Config Changed
- `orders/eod_squareoff.py` — new **📊 DAILY SUMMARY** alert: net P&L, win rate, best/worst trade, strategy breakdown, Smart TGT split (derived from order_protocol); fired at end of EOD square-off
- `orders/order_placer.py` — new ✅ ORDER PLACED alert (entry/qty/SL/TGT + Smart TGT status); new 🎯 TGT HIT + 🔴 SL HIT alerts at exit (EOD exits intentionally excluded — covered by daily summary)
- `orders/order_reconciler.py` — ⚠️ Capital Drift reformatted (₹ + newlines)
- `orders/shadow_tracker.py` — inning close alerts with 🎯/🔴/🔵 emojis, total ₹ P&L (via qty_filled lookup), pct, exit price; symbol in title not body
- `signals/signal_processor.py` — new `_emit_signal_alert()` helper; 🟢 INTRADAY SIGNAL alert fires before `placer.place()` on both score-path and gate-release-path

### Tests (2 files updated)
- `tests/unit/test_main.py` — assertion follows new "system active" title
- `tests/unit/test_shadow_tracker.py` — symbol now in title, body checks `"Inning: 1"` + comma-formatted price

## Test count
- **1657 green, 0 failed** (baseline 1654 + 3 added across ccde039/81fc86e)
- Pre-existing `broker_clock_skew_probe` MagicMock warning is unrelated

## Design conventions locked
- Mode prefix: `[PAPER]` / `[LIVE]` — always first in title
- Currency format: `₹{:,.2f}` for rupees; `{:+.2f}%` for percentage (signed)
- Emojis used: 🚀 ✅ 🎯 🔴 🔵 🟢 📊 ⚠️ 🚨 🛑
- Notifier is always optional; all sends wrapped in try/except that logs and swallows — notifier failure never crashes the caller
- EOD exits don't emit per-trade Telegram — daily summary replaces them

## Not done (possible follow-ups)
- Broker disconnect / live_feed reconnect alerts (only critical_failure_cb covers these today)
- Webhook ingress error alerts
- Startup-gate failure alerts (currently logged + soft_kill, no dedicated telegram)
- AlertWatcher itself is not mode-labeled — it formats critical_events rows directly
