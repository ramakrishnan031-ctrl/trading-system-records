---
name: project_fix131_p1_batch4
description: FIX-131 P1 batch4 complete -- Items 17/18/20/23/25; 2333 tests; commit 8e884db
metadata: 
  node_type: memory
  type: project
  originSessionId: e10470fa-0a49-4239-9cbe-4a0ec4c4c04b
---

FIX-131 P1 batch4 landed (2026-05-30, commit 8e884db). 2333 tests passing, 12 skipped, 0 failures.

**Why:** Operational hardening — dedup window, Telegram reliability, WAL management, broker costs.

**How to apply:** Baseline test count is now 2333. Schema version bumped to v18.

## Features shipped

### Item 17: Webhook dedup window widened (5-minute epoch bucket)
- webhook_receiver.py: fingerprint now uses `floor(unix_ts / dedup_window_seconds)` epoch bucket
- Old: minute-string (12:59 and 13:00 → different fingerprints → bypass DB dedup)
- New: 5-min epoch bucket (12:55:00-12:59:59 → same bucket → DB UNIQUE constraint catches it)
- Config: webhook.dedup_window_seconds = 300 (also drives TTLCache TTL)
- MagicMock guard: try/except around int() conversion

### Item 18: Telegram rate limiting + improved retry
- alerts/telegram_notifier.py: `_SlidingWindowRateLimiter(max_per_minute)` class
- Rate limiter acquired before every HTTP POST attempt
- Configurable: max_retries=3, retry_backoff_seconds=2.0, rate_limit_per_minute=20
- CRITICAL failures now also write to failed_alerts.log (was only ERROR tier)
- Schema v18: telegram_alerts table for delivery audit
- Config: alerts.telegram.max_retries/retry_backoff_seconds/rate_limit_per_minute

### Item 20: Config drift detection
- Already implemented prior; added 4 confirming tests
- check_config_hash() in startup_checks.py; Telegram alert in main.py
- COLD start: no alert; changed files: WARN + Telegram + DB event

### Item 23: WAL checkpoint cron
- state_store.checkpoint_wal(): PASSIVE mode (new); checkpoint() keeps TRUNCATE for EOD use
- Graceful shutdown now calls checkpoint_wal() (PASSIVE)
- scripts/wal_checkpoint.py: cron-friendly script for 16:00 IST

### Item 25: Broker cost explicit definition
- BrokerCostsConfig @model_validator: rejects negative rates, zero gst_pct
- All ZerodhaRatesConfig fields required (no Pydantic defaults) → ValidationError on missing key
- CostCalculator CC9 confirmed: no hardcoded rate literals

## VM crontab addition needed (not yet applied)
Add to ubuntu crontab:
```
0 10 * * 1-5 /home/ubuntu/systems/venv/bin/python /home/ubuntu/systems/trading-system/scripts/wal_checkpoint.py >> /home/ubuntu/systems/trading-system/logs/wal_checkpoint.log 2>&1
```
(0 10 UTC = 16:00 IST on weekdays)
</content>
</invoke>