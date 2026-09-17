# WEBHOOK_URL REMOVAL — PREP (read-only), 07-Sep-2026

**Status: PREPARED, NOT EXECUTED.** No Chartink alert was edited. No code changed.
Card §5b is after-close work; this is the read-only staging done during the session.

Measured against the live VM at ~10:5x IST, deployed tip `20061b6`.

---

## 1. The payload contract, measured (not assumed)

🔬 One most-recent payload per scanner pulled from `signals.webhook_payload`.
**All 13 scanners that produce signal rows send an identical 7-column set:**

| column | receiver treatment | evidence |
|---|---|---|
| `stocks` | **REQUIRED** — absence ⇒ 400 | `webhook_receiver.py:577-583` |
| `trigger_prices` | **REQUIRED** — absence ⇒ 400 | same loop |
| `triggered_at` | **REQUIRED** — absence ⇒ 400 | same loop |
| `scan_name` | **OPTIONAL but VALIDATED** — if present it is normalized and compared to the path param; mismatch ⇒ 400 | `:586-597` |
| `scan_url` | unread | no consumer found |
| `alert_name` | unread | no consumer found |
| `webhook_url` | unread; **blanked before storage** | `_sanitize_payload_for_storage` |

⇒ **The edit is: delete `webhook_url`, leaving 6 columns. Touch nothing else.**
⛔ Do NOT also drop `scan_name` — it is not inert. Removing it is safe, but *altering* it is a 400.
⛔ Do not bundle `scan_url` / `alert_name` (card §5b).

## 2. Why 16 alerts but only 13 in the data — reconciled

🔬 `signals` has 13 distinct scanners over all history. The 16 Chartink alerts reconcile exactly:

- **13** produce `signals` rows
- **−2** `range_breakout_long` / `range_breakout_short` — 0 rows in 223,484 requests; conditions unsatisfiable
- **−1** `pb01_breakout_retest` — takes the EOD branch (`:533 _handle_eod`), watchlist-only, **never enqueued**, so it writes no `signals` row even though it does POST (~17:00)

⇒ **All 16 still need the edit.** The 3 absentees are invisible in `signals` by design, not by fault.

## 3. The stated rationale is already mitigated — this changes the urgency

The reason to remove `webhook_url` is that Chartink echoes the configured URL, which carries
`?token=<SECRET>`, back inside the body.

🔬 **That leak is already closed at rest** by `_sanitize_payload_for_storage` (S-1B.1, 2026-07-05).
Measured across **209,436** stored payloads spanning **12-Jun → 07-Sep**:

| pattern | count |
|---|---|
| `token=` (any form) | **0** |
| `https://` (any URL) | **0** |
| `webhook_url` stored as `"<REDACTED>"` | all |

🔬 Log-side paths also clean: **0** `token=` strings in retained `logs/system_*.log`;
the werkzeug/access query-string path shows **0** hits.

⇒ §5b is **defense-in-depth, not an active leak fix.** It is not urgent on its own merits.

## 4. The one argument that *does* still justify it — a latent, uncovered path

⚠️ The sanitizer covers the **DB copy only**. The malformed-JSON branch logs the **raw body**:

```
webhook_receiver.py:  self._log.warning(
    "webhook/%s: Malformed JSON: %s | raw=%r", scanner_name, exc, raw_body[:500])
```

`raw_body` here is **unsanitized**. A malformed payload that still contains
`"webhook_url":"...?token=<SECRET>"` would write the secret to the log in plaintext.

🔬 **It has never fired** — `grep -c "Malformed JSON"` over retained logs = **0**. So the hazard is
**latent, not realized**.

⇒ Removing `webhook_url` at source closes this at the origin, which is strictly better than
patching the log line — the field cannot leak through a path that never receives it.

## 5. What this does NOT do — ordering note for §5a

⛔ **Removing `webhook_url` from the body does not remove the token from the request URL.**
Auth uses the `?token=<secret>` query-param bearer (`_authenticate`, option 2), so the secret still
travels in the URL Chartink posts to, and still lives in all 16 Chartink alert configs.

⇒ **Rotating the webhook secret still requires updating all 16 alert URLs.** If both §5a and §5b are
done in the same sitting, do them per-alert in one pass — each alert is opened once anyway.

## 6. Execution checklist (after close, 15:30+)

Per alert, ×16, in the Chartink UI:
1. Open the alert's webhook configuration.
2. Remove **only** the `webhook_url` column.
3. Confirm `stocks`, `trigger_prices`, `triggered_at` remain present.
4. Leave `scan_name`, `scan_url`, `alert_name` exactly as they are.

Verification the next session (not the same evening — the alerts must fire first):
```sql
-- expect 0 once every alert has posted at least once on the new config
SELECT COUNT(*) FROM signals
WHERE webhook_payload LIKE '%webhook_url%'
  AND substr(received_at,1,10) = '<next trading day>';
```
⛔ A 400 spike in `webhook_audit` the next morning is the failure signature — check
`response_code=400` (historically **0**) before assuming success.

---

*Provenance: 🔬 all counts measured read-only against `data_store/trading_system.db` (`mode=ro`) and
`signals/webhook_receiver.py` at deployed tip `20061b6`, 07-Sep-2026. Line numbers hold at that SHA only (M3).*
