---
name: fno-ban-endpoint-fix-22jun
description: "fetch_fno_ban moved to NSE Clearing CSV + failure downgraded CRITICAL→WARN, fail-open for EQ; ban list has NO runtime consumer"
metadata: 
  node_type: memory
  type: project
  originSessionId: 352c7b01-735b-48d3-8902-0d349b1dfe25
---

`scripts/fetch_fno_ban.py` fixed 22-Jun-2026 (branch `fix-fno-ban-endpoint-22jun`).

**Why:** Monday 08:35 the job emailed a CRITICAL — old endpoint
`nseindia.com/api/live-analysis-banned` is dead (**404**, NSE retired it).

**Key finding:** `is_symbol_fno_banned()` / the `fno_ban` table have **NO runtime
consumer** — referenced only by their own test. The ban list was fetched + stored
daily but never read by any strategy/risk/entry-gate. So the old "F&O signals
BLOCKED" message + fail-closed sentinel were misleading; nothing was ever blocked.
Rama trades NSE-EQ only; job kept for a future F&O era.

**How to apply / what changed:**
- New source = NSE Clearing daily CSV `https://nsearchives.nseindia.com/content/fo/fo_secban.csv`
  (needs browser UA + Accept headers). Parser rewritten JSON→CSV (`parse_secban_csv`):
  header `Securities in Ban For Trade Date DD-MMM-YYYY:` → ISO date; `<serial>,<SYMBOL>`
  rows; HTML-block-page guard; no-ban = header only. Verified live (22-Jun = 1 ban: KAYNES).
- Failure (404/timeout/HTML/stale-date) → **WARN not CRITICAL**, **fail-open**: `log.warning`
  + Telegram WARN (no `critical_alert_*.flag` → **no email**) + heartbeat + **exit 0**
  (Cron Officer shows done, not failed). Stale CSV (date≠today) → WARN, not stored.
- `fno_ban.fail_closed` default **true→false** (knob kept; ON only ever gates F&O via the
  sentinel, never EQ). Removed dead `min_expected_fields`. `system_config.yaml` + `FnoBanConfig`.
- No crontab change (same 08:35 Mon-Fri, same job name). Severity-downgrade plumbing:
  `send_critical`→sentinel→email; `send_alert(level="WARNING")`→`_handle_info_warn`→no sentinel.

Related: [[task_3_cron_officer]], [[smtp_alert_watcher_config]], [[instruments_staleness_incident_21jun]]
(same NSE-archives freshness-assertion pattern), [[feedback_foundation_rules]].
