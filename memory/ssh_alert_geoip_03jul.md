---
name: ssh-alert-geoip-03jul
description: "GeoIP enrichment added to the SSH over-limit alert (03-Jul) — ip-api.com fallback, cached in security_state.json"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b1fa8b6-3ab8-4f25-a39a-0a6806490486
---

**What:** [[ssh_session_alert_03jul]]'s per-IP over-limit alert
(`check_active_sessions` in `scripts/security_monitor.py`) now annotates each
IP with GeoIP: `"<IP> x<n> (<user(s)>, since <HH:MM:SS>, <City>, <CC> —
<ISP/Org>)"`. Live sample after deploy:
`223.237.179.17 x6 (ubuntu, since 17:16:57, Chennai, IN — Bharti Tele Ventures Ltd)`.

**GeoIP source:** no local MaxMind GeoLite2 DB is installed on the VM and none
was available (`geoip2`/`maxminddb` not in the venv, no `.mmdb` file found) —
installing one needs a MaxMind account + free license key, which **Rama would
have to provision** (flagged, not done). Fell back to the free, no-key
`ip-api.com` JSON endpoint (same one used for the Part-1 diagnostic), called
via the already-vendored `requests` lib with a 2s timeout, local-imported like
`auto_refresh_token.py`/`cron_officer.py` do.

**Design:**
- New `geoip_lookup(ip, cache, now)` in `scripts/security_monitor.py`: private/
  loopback/link-local IPs (via `ipaddress`) → `"local"`, no network call.
  Malformed IP or lookup failure → `""` (alert just omits the geo tag — never
  blocks/delays the alert).
- Cached in `state["geoip_cache"]` (persisted to
  `data_store/security_state.json`, same file the monitor already
  read/writes every pass) with a 30-day TTL per IP — a recurring IP is not
  re-queried every ~60s cycle.
- `session_ip_breakdown` (built 03-Jul, same day) unchanged; geo is appended
  per-IP in `check_active_sessions` only.

**Deployed:** main `3a27538 → cf6ecb8`, pushed to the VM bare repo, restarted
`security-watcher.service` only (trader untouched — infra, mode-agnostic).
42 existing unit tests in `tests/unit/test_security_monitor.py` still pass
(none previously covered `check_active_sessions`, so this was a safe,
untested-path addition — same low-risk profile as the per-IP breakdown
change).

**How to apply:** if Rama later wants offline/rate-limit-proof GeoIP (ip-api.com
free tier is ~45 req/min, fine at this alert volume but not guaranteed
uptime), the swap-in point is `geoip_lookup` — replace the `requests.get`
block with a local `geoip2.database.Reader` lookup once Rama provides a
MaxMind GeoLite2-City + GeoLite2-ASN `.mmdb` pair.
