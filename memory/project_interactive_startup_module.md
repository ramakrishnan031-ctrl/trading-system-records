---
name: Interactive Startup module built and locked (SU1-SU20, Module 41)
description: Holiday guard, Zerodha login, interactive startup flow, accounts.csv extended schema; 1394 tests green
type: project
originSessionId: 12ead290-f026-42d3-ba03-9f10c51a1a9c
---
# Module 41 Interactive Startup Flow — BUILT AND LOCKED

**Locked decisions:** SU1-SU20
**Test count:** 1394/1394 green (was 1355; +39 new tests)

## New Files

### utils/holiday_guard.py
- `is_trading_day(today: date, config_dir: Path) -> bool` — weekend + holiday check
- `next_trading_day(from_date: date, config_dir: Path) -> date` — walks forward
- Reads `nse_holidays_<year>.yaml` directly (no Pydantic); handles plain string + dict-with-date formats
- Raises `FileNotFoundError` if YAML absent (main.py swallows this and proceeds)

### scripts/zerodha_login.py
- `is_token_valid(account_id, token_path) -> bool` — file exists + account_id match + today's date + non-empty token
- `load_token(token_path) -> dict | None` — parse JSON or return None
- `exchange_request_token(api_key, api_secret, request_token) -> str` — POST /session/token, sha256 checksum
- `save_token(account_id, broker, api_key, access_token, token_path)` — writes JSON with expires_at
- `run_login_flow(...)` — browser open + request_token input + exchange + save
- CLI: `python scripts/zerodha_login.py --account LFL836`
- Token path default: `data_store/session/zerodha_token.json`

## Updated Files

### core/account_registry.py
New AccountRow fields: `api_key_env`, `api_secret_env`, `totp_secret_env`, `paper_capital: float`, `capital_share_pct: float`, `enabled: bool`
New method: `get_enabled_accounts() -> list[AccountRow]`
New validation: `paper_capital > 0` for enabled accounts (AR11)

### main.py
- `--interactive` flag added to argparse
- **Holiday guard runs BEFORE setup_logging** — zero log creation on non-trading days; returns 0
- Interactive helpers (module-level, testable via `input_fn` param):
  - `_interactive_select_account(registry, input_fn)` — exits 8 on 'q'
  - `_interactive_check_or_login(account, token_path, today, input_fn)` — reuse or fresh login
  - `_interactive_select_mode(account, input_fn)` — paper (default) or live
  - `_interactive_confirm_live(account, broker_adapter, input_fn)` — exact phrase "CONFIRM LIVE"; exits 7 on wrong phrase
  - `_print_welcome_banner(account, mode, capital, today)` — SU13 banner
- Non-interactive: primary account; live mode checks token file (exit 6 if invalid)
- **SU19 capital wiring:** paper mode = `selected_account.paper_capital`; live mode = `broker_adapter.get_margins().net`
- Access token resolved from token file injected into `os.environ["ZERODHA_ACCESS_TOKEN"]`

## Exit Codes (extended)
- 6 — token missing or expired (non-interactive live)
- 7 — live mode confirmation cancelled
- 8 — account selection cancelled

## Deviations from Spec
None. All SU1-SU20 implemented as specified.

## Why
- Holiday guard before logging: zero log file creation on weekends/holidays
- Token file flow: avoids storing access tokens in env; VM cron deletes at 05:00 IST daily
- Interactive mode: morning operator workflow; non-interactive for VM automation
