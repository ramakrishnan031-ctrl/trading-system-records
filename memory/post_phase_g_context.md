---
name: Post-Phase G Context (Sections 1-2)
description: Everything that happened after Phase G completed — deferrals, verdicts, completed tasks, schema changes, and Module 41 scope
type: project
originSessionId: 12ead290-f026-42d3-ba03-9f10c51a1a9c
---
# What Happened After Phase G (1351/1351 green)

**Phase H (chaos tests) DEFERRED** — Run AFTER paper trial, not before. Rationale: paper trial with real data first, then inject failures.

**Phase I (verdict) delivered by Web Claude:**
- 32 fixed, 6 already-fixed, 6 verified-ok, 3 closed, 1 pending, 2 verify, 8 deferred
- Verdict: READY FOR PAPER TRIAL. NOT YET FOR LIVE.
- Full text in memory/audit_closeout_final.md

**Task 1 done** — audit_closeout_final.md written to mempalace + locked_decisions.yaml appended.

**Task 2 done** — accounts.csv replaced with single LFL836 row; .env.example created; .gitignore verified.

**Task 2b done** — Telegram whitelist enforcement. Channels config with enabled flag. 1355/1355 green.

**accounts.csv schema REVISED (final, locked):**
```
account_id,broker,label,is_primary,api_key_env,api_secret_env,totp_secret_env,
paper_capital,capital_share_pct,enabled
```
- 5 rows: 3 real (LFL836 Kandasamy, DR6114 Ramakrishnan, D351962 Dhanalakshmi) + 2 placeholders
- paper_capital = Rs 50,00,000 per account
- Rama will keep final CSV; api_key_env currently has raw keys, Rama will fix to env var names

**.env revised** — Access tokens removed. Token comes from data_store/session/zerodha_token.json (daily browser login, SCP'd to VM, cron deletes at 05:00 IST).

**Interactive startup flow designed (Module 41)** — --interactive flag + account selector + login flow + mode picker + holiday guard.

**Zerodha login port** — scripts/zerodha_login.py (browser-assisted, request_token exchange).

**Username pre-fill** — NOT possible via URL params; use same browser each morning (cookie remembers user).

# Module 41 Status

**BUILT AND LOCKED (SU1-SU20).** 1394/1394 green.

New files:
- `utils/holiday_guard.py` — is_trading_day(), next_trading_day()
- `scripts/zerodha_login.py` — is_token_valid(), load_token(), exchange_request_token(), save_token(), run_login_flow()

Updated files:
- `core/account_registry.py` — AccountRow gained api_key_env, api_secret_env, totp_secret_env, paper_capital, capital_share_pct, enabled; get_enabled_accounts() added
- `main.py` — --interactive flag; holiday guard (BEFORE setup_logging); interactive flow (SU7-SU13); non-interactive token check; SU19 capital wiring (paper uses paper_capital, live uses broker margin)

New tests:
- tests/unit/test_holiday_guard.py — 7 tests
- tests/unit/test_zerodha_login.py — 11 tests
- tests/unit/test_interactive_startup.py — 14 tests
- tests/unit/test_account_registry.py — +7 new tests (now 27 total)

# Next Steps

After 1411 green: Rama begins paper trial.

Remaining build work (after paper trial):
- Phase H: Chaos test suite
- v2.1 features (ATR, AngelOne, multi-account, etc.)

# Why: Key Constraints
- Paper trial first to validate real-market behavior before live trading
- Token file approach avoids storing live credentials in env; VM cron deletes daily
- Interactive mode for morning operator login; non-interactive (--mode paper) for VM automation
