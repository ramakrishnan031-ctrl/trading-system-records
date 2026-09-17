---
name: agy-automation-status
description: AGY fully automated from 11-Jun-2026. Watchman auto-starts. Cron scripts load .env natively. Model cascade working.
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b860701-6391-4408-be2a-86ea2bdeaf60
---

**AGY fully automated from 2026-06-11.**

**Why:** FIX-162 resolved all three automation blockers — Telegram crashes (dotenv), CLI hang (arg order), watchman not starting (systemd Wants).

**How to apply:** No manual intervention needed for daily AGY operation. Watchman auto-starts with trading-system. All cron scripts load .env natively.

## Model cascade
- Tier 1 (deep): Claude Sonnet 4.6 → Gemini Pro
- Tier 2 (routine/watchman): Gemini Flash Low → Flash Medium → Flash High
- All Gemini models share ONE Google AI Pro quota pool (Flash Low call burns Flash High quota too)
- Lowest tier that gives acceptable quality = most efficient

## Daily automation (no manual steps)
- Watchman: auto-start on trading-system start, exits after 15:30
- Cron scripts: load .env natively via python-dotenv
- Token: auto-refreshed via cron-auto-token

Related: [[fix-162-complete]] [[fix-160-agy-cascade]]
