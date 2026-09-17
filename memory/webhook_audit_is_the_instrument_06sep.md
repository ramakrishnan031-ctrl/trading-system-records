---
name: webhook_audit_is_the_instrument_06sep
description: "The webhook_audit table answers \"did this scanner connect\" — logs cannot; plus 401 vs 403 and the real per-scanner traffic expectation."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9f103ec2-6ea8-4b32-a0ca-586e0765e2af
  modified: 2026-09-05T18:59:54.018Z
---

🔬 **MEASURED 06-Sep-2026**, `data_store/trading_system.db` → `webhook_audit`
(written by `webhook_receiver._write_audit`, `:1090`; columns `ts, scanner_name,
source_ip, payload_size_bytes, response_code, signals_accepted, signals_rejected,
duration_ms`).

⭐ **USE THIS TABLE, ⛔ NOT THE LOGS, to ask "did scanner X connect?"** 🔬 The logs
record only the FAILURE paths (`:489-491`, `:558-560`), so a `grep` for a scanner
returning **0** means *"no errors"*, ⛔ **not** *"no traffic"* — 🔬 that exact trap
produced a wrong PB01 conclusion on 05-Sep, corrected only by this table.

**🔬 Baseline over 223,484 requests, 12-Jun → 04-Sep-2026:**
`200 = 175,012` · `403 = 48,454` · `503 = 18` · 🔴 **`401` = 0 · `400` = 0 · `404` = 0.**

⛔ **401 ≠ 403 — do not read 403 as an auth failure.**
- 📄 **401** = authentication (`:362`, `:518`). 🔬 **Never once in ~3 months** ⇒ ⭐ any
  401 is an unambiguous "an alert is on the wrong token".
- 📄 **403** = kill switch (`:537`) **or** outside entry window (`:552`). 🔬 Its shape
  says which: 403 peaks **09:00 (17,572)** and **15:00 (18,811)** while 200 peaks
  10:00-14:00 (31.7k-37.2k) and collapses at those hours (248 / 1,285)
  ⇒ ⭐ the **entry-window boundary**, by design. ⭐ 21.7% of traffic is normal.

**🔴 Only 14 of the 16 scanners have EVER posted, and only 13 in the morning:**
- 🔬 `range_breakout_long` + `range_breakout_short` = **0 rows ever** (unsatisfiable)
  ⇒ ⛔ they can never be confirmed by traffic; ⭐ a config fingerprint match is the
  only verification that will ever exist for them.
- 🔬 `pb01_breakout_retest` posts **daily at ~17:00**, ⛔ not in the morning — 29
  requests, **29 × 200**, 19-33 symbols accepted.
⇒ ⭐ **Expect 13 distinct scanner names in the 08:15-10:15 window, ⛔ not 16.**

**📄 PB01 takes the EOD branch, so its `scan_name` is never validated.**
`:531-533` `if getattr(_entry,"scanner_type","intraday")=="eod": return
self._handle_eod(...)` — returns **before** `_process_request`, so the scan_name
check at `:589` is unreachable. 🔬 `scan_webhook_map.yaml` marks pb01
`scanner_type: eod`, ⭐ the **only** one. ⇒ ⭐ Its `scan_name`
*"PB01 BREAKOUT + RETEST (SHADOW)"* → `pb01_breakout_+_retest_(shadow)` **would**
mismatch `pb01_breakout_retest`, ⛔ but cannot fire.
⏸ 🔴 **The spec-13 trigger is flipping `scanner_type` eod→intraday — ⛔ NOT merely
enabling the strategy.** ⭐ Rename the **scan** (⛔ not the alert — the alert name
`PB01 BREAKOUT RETEST` is already correct) before that flip.

**📄 The body fields the receiver actually reads — the complete list:**
`stocks` · `trigger_prices` · `triggered_at` (all three hard-required, `:578`/`:727`)
· `scan_name` (optional, `:589`, validated against the path if present).
⛔ **`webhook_url`, `scan_url` and `alert_name` are NEVER read** — 🔬 `alert_name` has
zero references in the non-test tree; `scan_url` is only *written* by
`scripts/load_test_signals.py:91`; `webhook_url` appears only in the storage
sanitizer. ⚠️ The `webhook_url` in `main.py`/`utils/startup_checks.py` is an
unrelated **local variable** holding `http://127.0.0.1:5000/health`.
🔬 `webhook_url` is present in **208,946 of 208,946** stored payloads ⇒ ⭐ the
credential really does travel twice per request → [[weekend_exit_precedes_every_secret_check_05sep]].

---

**🔴 THE MONDAY READING RULE — ⛔ only ONE signal is actionable.**

- ⭐ **A 401 is the only actionable event.** 🔬 Zero 401s in 223,484 requests over
  three months ⇒ ⭐ a single one is unambiguous: an alert is on the wrong token.
- ⛔ **A 403 is NOT an auth failure** — kill switch or entry window. 🔬 21.7% of all
  traffic, by design.
- 🔴 ⛔ **If FEWER THAN 13 scanners appear, do NOT investigate.** ⭐ A scanner with no
  POST means *either* a bad config *or* no matching signal, ⭐ and those are
  **indistinguishable** from the absence. ⇒ ⭐ Record any absentee as
  **"configuration-verified only"** — ⭐ the same permanent status
  `range_breakout_long`/`_short` hold — ⭐ and move on.
- ⇒ ⭐ Everything except a 401 is **informational**. 👤 Rama's advisor, 06-Sep.
