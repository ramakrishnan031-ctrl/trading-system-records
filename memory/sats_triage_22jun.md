---
name: sats-triage-22jun
description: SATS first Semgrep scan triage (22-Jun-2026) — 23 findings → 22 false positives + 1 real fix (recovery.py 0o700); baseline strategy
metadata: 
  node_type: memory
  type: project
  originSessionId: 0732f4c1-94e3-4fd5-aa1c-b47d2ff1ed94
---

First SATS Semgrep scan (`p/python` + `p/security-audit`) returned **23 findings**; full triage
22-Jun-2026 (read the surrounding code for each — no assumptions). **Outcome: 22 false positives + 1
real fix.** Post-fix full scan = 22; recovery.py = 0.

**The 1 real fix** — `scripts/preflight/checks/recovery.py` `_ensure_dir()` did `os.chmod(dir, 0o755)`
on the `logs/` and `data_store/cron_marks/` dirs → tightened to **0o700** (owner-only; least privilege,
single-user VM). Committed **ab8b12e** (on `main`, LOCAL only — deploys on the next push+restart, not
pushed yet). The file-oriented `insecure-file-permissions` rule STILL flags a *directory* chmod even at
0o700 (it wants 0o644, which would strip the owner traversal bit) → Rama approved a one-line
`# nosemgrep: python.lang.security.audit.insecure-file-permissions.insecure-file-permissions` directly
ABOVE the `os.chmod` line. **nosemgrep placement rule:** rationale comments go ABOVE the nosemgrep
line; the nosemgrep directive must sit on the line IMMEDIATELY above the code (nothing between) or the
suppression silently breaks. The exact `check_id` carries the doubled `.insecure-file-permissions`
suffix — get it from `semgrep --json` if ever reusing.

**The 22 false positives** (no code change): logger-credential-leak rules firing on booleans
(`bool(api_key)`), env-var NAMES not values, masked `totp[:3]***`, account ids, durations, and the
keyword "token" where it means *instrument_token* (market-data id) or the token FILE; dynamic-urllib on
hardcoded / trusted-config / localhost URLs (Chartink scanners, `api.telegram.org`, `127.0.0.1`,
ipify/amazonaws); plus 2 test/safe (`test_webhook.py` `0.0.0.0` is test-only; `TESTING=False` is the
safe prod value). Key verification: the Telegram `exc` logged at `auto_refresh_token.py:290` CANNOT
leak the bot token — `TelegramNotifier._post_with_retry` catches `requests.Timeout` +
`requests.RequestException` internally and never re-raises the token-bearing URL.

**Suppression strategy:** a Semgrep **baseline** at commit `65439ff` (`sats\semgrep_baseline.txt`) —
future scans surface only NEW findings; the 22 reviewed FPs are NOT individually `# nosemgrep`-tagged
(avoids churn on live code). The em-dash "mojibake" Web Claude flagged in
`gemini_data_integrity_check.py` was a FALSE ALARM (bytes `E2 80 94` = valid UTF-8; a viewer artifact).

Also fixed the scan scripts themselves (a `PYTHONUTF8` crash) — see [[sats_tooling]]. Related:
[[feedback_paper_live_parity]] (N/A here — all flagged code is mode-agnostic).
