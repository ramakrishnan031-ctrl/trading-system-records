---
name: fix_184_scanner_ua_403
description: "FIX-184 — startup \"check_scanner returned status None (unreachable)\" was Chartink 403 on urllib default UA"
metadata: 
  node_type: memory
  type: project
  originSessionId: 926bcdec-f5d1-4d8b-ab01-42b2d61dba29
---

FIX-184 (2026-06-18, commit c48d4fd). At every startup the scanner-connectivity
preflight (SC7/P17) logged "check_scanner: <scanner> returned status None
(unreachable)" for all 15 scanners.

**Root cause:** `main._http_fetch` (main.py:189) called `urllib.request.urlopen`
with NO User-Agent, so urllib sent its default `Python-urllib/x.y` UA. Chartink's
Cloudflare edge blocks that UA with **HTTP 403**. `urlopen` RAISES `HTTPError` on
403, and the bare `except Exception` swallowed it into `status=None`, which the
check reads as "unreachable". Verified on VM: default UA → 403 for EVERY url incl.
chartink.com root; any non-urllib UA (browser, or "TradingSystem/2.0 ...") → 200.

**Not a real outage.** Signals arrive via inbound webhook POSTs from Rama's
Chartink account — a separate path that worked throughout. The configured scanner
URLs are valid (return 200 with a proper UA). The 08:30 cron
`preflight_scanner_check.py` was already fine: it sets a custom UA and uses
`requests` (which returns 403 instead of raising), so no false cron alerts.

**Fix:** `_http_fetch` now sends `User-Agent: TradingSystem/2.0 startup-check`
and has a dedicated `except urllib.error.HTTPError` that returns the real status
code (so a genuine 404 is reported as 404, not masked as None). Verified on VM
post-deploy: root→200, valid slug→200, bogus slug→404. 127 tests pass
(test_main + test_startup_checks). Cosmetic — takes effect next startup; did NOT
force-restart the live session for it.

Gotcha for future stdlib HTTP code: `urllib.request.urlopen` raises HTTPError on
4xx/5xx (unlike `requests`), and its default UA is bot-blocked by Cloudflare
sites. Related: [[deploy_requires_restart]], [[feedback_vm_curl_tests]].
