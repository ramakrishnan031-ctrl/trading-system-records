---
name: fix-191-false-softkill-23jun
description: "FIX-191 (23-Jun): API-failure breaker now connectivity-only (was tripping on OrderRejectedError/slippage aborts); SOFT_KILL halt alert WARN→CRITICAL; resume caps 5/10/5; Telegram restored (stale token); telegram_alerts table vestigial"
metadata: 
  node_type: memory
  type: project
  originSessionId: adbf3bf4-6a15-4d49-97db-6fbeb4e5f604
---

**23-Jun-2026 LIVE incident — false SOFT_KILL halted ALL signals 10:07→12:28.** Only 2 trades placed (GARUDA, PPLPHARMA — both SL). Then a SOFT_KILL auto-tripped on "3 consecutive API failures" and `signals/webhook_receiver.py` 403'd EVERY incoming signal (~150/hr, 0 accepted) for ~2h. Broker was FINE — a false positive.

**Root cause:** the consecutive-API-failure breaker (FIX-069 intent = transient connectivity outage) was counting BUSINESS rejections. `OrderRejectedError extends BrokerError` (core/exceptions.py); `signals/signal_processor.py` calls `record_api_failure(be)` on ANY `BrokerError` at placement → 1 broker MIS-block reject + **2 client-side slippage-guard aborts** (`orders/order_placer.py` raises `OrderRejectedError` BEFORE any broker call) = 3-in-a-row → trip. NOT consecutive-losses (only 1 loss had closed at trip time).

**Fix (FIX-191, commit 7ff24b2):** `capital/kill_switch.py` `record_api_failure` now **WHITELISTS** — counts ONLY `BrokerTimeoutError` / `BrokerRateLimitError`. `OrderRejectedError` (broker reject OR slippage abort), `SLUnplaceableError`, `ProductNotSupportedError`, generic `BrokerError` no longer count; `BrokerAuthError` still excluded ([[fix_185_hardcap_and_auth_failures]]). Single chokepoint (only caller = signal_processor), no mode branch (paper+live parity).

**Halt-alert severity (commit 6bed838):** `soft_kill()` notified at `severity="WARN"`, which drops silently on a Telegram send-failure with NO email fallback → today's halt reached Rama through ZERO channels. Raised the SOFT_KILL halt notification **WARN→CRITICAL** (routing ONLY — kill stays SOFT_KILL; uses the CRITICAL email-fallback path). Scoped: routine WARN unchanged; `hard_kill` has no notifier send; IP-403/exit alerts already CRITICAL.

**Resume caps (parity; supersedes [[live_test_mode_permanent]]):** max_daily_trades 20→10, live_test_max_open_positions 4→**5**, live_test_max_entries_per_day 6→**10**, max_consecutive_losses 2→**5**.

**Telegram restored:** root cause = **stale bot token** (all 277 historical `logs/failed_alerts.log` "failed to deliver to ['-100…']" were the dead token, not the chat_id). GOTCHA: the `telegram_alerts` DB table is **vestigial** — `alerts/telegram_notifier.py` NEVER writes it (it sends via HTTP + CRITICAL sentinels + failed_alerts.log only). An empty `telegram_alerts` is NOT evidence of a Telegram problem — check `failed_alerts.log` instead.

**Deployed + resumed 12:28** (bare HEAD 6bed838; kill cleared via `scripts/clear_kill_switch.py` / `deploy/resume.sh`; caps 5/10/5 verified live in the running process; signals flowing). Tests: +2 in `test_kill_switch.py` (34/34) + 7/7 `test_fix132_email_fallback.py`. Full detail in `docs/SYSTEM_MAP.md` Changelog (23-Jun).

**`~/tools/claude` heartbeat cron — NOW GOVERNED (23-Jun):** the 4 cron lines `cd /home/ubuntu/tools/claude` first, loading `~/tools/claude/AGENTS.md` (charter) + `~/tools/claude/.claude/settings.json` (hard `permissions.deny`: `Write/Edit(**/*.py)`, `Read/Write/Edit(**/*.db)`+`Bash(sqlite3:*)`, `Bash(systemctl|sudo|service:*)`, `Write/Edit(~/systems/**)`, trading `.env` read, `git push`) — mirrors AGY (no .py/DB/systemctl). Verified: heartbeat works, `.py` write + `.db` read both blocked (the `.db`-read block proves settings.json is loaded). Crontab backup `~/tools/claude/crontab.backup.*`. **Made rebuild-proof (commit 9513b0d, pushed):** the 4 governed heartbeat lines were added to `deploy/cron/trading-system.cron` (live==canonical for claude lines, diff=0), the guardrail files are version-controlled at `deploy/tools/claude/` (AGENTS.md + .claude/settings.json + README), and `docs/disaster_recovery.md` §5 has a restore step — so a VM rebuild keeps the heartbeat governed.

**Still open / related:** F&O/MIS-ban pre-screening absent — TVTODAY reached the broker (its reject no longer trips the kill post-FIX-191, but the pre-screen gap remains). `tgt_retry_manager` 30s `is_within_market_hours` crash → resolved by the NOCIL push. See [[fix_190_incident]].
