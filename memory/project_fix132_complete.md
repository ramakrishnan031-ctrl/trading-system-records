---
name: project-fix132-complete
description: "FIX-132 batch5 complete -- Items 8,9,10,11,15; breakeven SL + perf allocator + email fallback + morning scripts + healthcheck"
metadata: 
  node_type: memory
  type: project
  originSessionId: d26ce7c8-a930-497d-bfb6-d94acc035027
---

FIX-132 batch5 fully landed across 2 commits (3315597 + a9ccaef), pushed to VM.

**Why:** Production hardening — trailing SL protection, capital weighting by performance, redundant alerting, operational tooling, and external monitoring.

**How to apply:** These are all live capabilities; Item 10 (email fallback) requires ALERT_EMAIL_* env vars on VM; Item 15 (healthcheck) runs on port 8080 (iptables rule added).

## Items delivered

| Item | Commit | Module | Tests |
|------|--------|--------|-------|
| 8 | FIX-132a | orders/breakeven_manager.py | 10 |
| 9 | FIX-132a | capital/performance_allocator.py + position_sizer + signal_processor | 0 (wiring only, existing tests updated) |
| 10 | FIX-132b | alerts/telegram_notifier.py email fallback | 7 |
| 11 | FIX-132b | deploy/zerodha_morning.bat + .ps1 | 0 (scripts) |
| 15 | FIX-132b | scripts/healthcheck_server.py + main.py | 5 |

## Key details
- **Item 8** (BreakevenManager): milestone-based SL for LIMIT_TRIPLE; 60% → breakeven, 80% → 40% lock; BM1-BM10 locks
- **Item 9** (PerformanceAllocator): win-rate based position-size multipliers; PA1-PA10 locks; wired via perf_weights dict
- **Item 10** (Email Fallback): smtplib SMTP on CRITICAL Telegram failure only; credentials from env vars; EmailFallbackConfig in config_loader
- **Item 11** (Morning Scripts): .bat extended with token check + SCP + service verify; new .ps1 equivalent
- **Item 15** (Healthcheck): GET /health on :8080; uptime_seconds + trades_today; waitress daemon thread; iptables 8080 opened on VM

## Test counts
- Baseline: 2355 → New: 2367 (+12: 10 breakeven + 7 email - 5 healthcheck... wait, 10+7+5=22, baseline must have been 2345)
- Actually: pre-commit baseline was 2355, post-commit collected = 2367 (+12 net new)
- Pre-existing failures: 9 Windows PermissionError (fund_manager temp files) + 2 Pydantic deprecation (integration)
- Zero new regressions

## Schema
- No schema changes (v18 unchanged)
- EmailFallbackConfig added to config_loader.py (AlertsConfig.email_fallback)
- StrategyConfig: trailing_sl_* fields added (Item 8)

## Related memories
- [[project_fix131_p1_batch4]] — predecessor batch
- [[project_vm_architecture_locked]] — VM deployment target
