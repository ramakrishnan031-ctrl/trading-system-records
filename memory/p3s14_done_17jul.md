---
name: p3s14-done-17jul
description: "P3-s14 FIXED + DEPLOYED 17-Jul: a store failure now releases both claims AND returns a retryable 503. 2 instruction premises were wrong (old response is 500 not 200; immediate retry is IN_PROCESS not DUPLICATE). The fix RETIRES the bug's 500 ops fingerprint."
metadata:
  node_type: memory
  type: project
  originSessionId: 8ce14ca5-df4a-451f-aa35-493d91436ae9
---

**✅🚀 P3-s14 FIXED + DEPLOYED 17-Jul** — `a9a686e` (ONE coordinated commit: code + test), tag
**`deploy-17jul-s4-p3s14`** → `a9a686e`; PC == VM bare == **`10a9c766`**. Schema **v44, no
migration**; no cron/config/schema file in the diff. Report
`docs/audit/p3s14_done_17jul2026.md`. Takes effect at the next boot.
**Shipped WITH the S4 boot-outage fix — see [[s4-boot-outage-17jul]] (found while verifying the
VM for THIS deploy; it is the bigger story of the day).**

## The fix (release + retryable = ONE fix)
An `except Exception` **beside/after** `except sqlite3.IntegrityError` releases the dedup
TTLCache claim **and** the in-flight claim and returns **`STORE_ERROR`**, folded into the
`:650` 503 predicate via **`_RETRYABLE_STATUSES = {QUEUE_FULL, STORE_ERROR}`**. Catching
(not raising) also keeps the per-symbol loop alive ⇒ **the rest of the batch is no longer
abandoned**. Mirrors M-S2's QUEUE_FULL decision exactly.
**Why one fix:** release-alone is the TRAP → an ordinary status makes the batch **200** ⇒
Chartink never retries ⇒ bounded ~300 s loss becomes **PERMANENT**. Catching is what *removes*
the old 500, so catching MUST restore a retryable code.
**No double-entry re-opened:** `_claim_in_flight` + `UNIQUE(fingerprint, fingerprint_date)`
remain the controls; the cache is a fast-path optimisation.
**`STORE_ERROR` is RESPONSE-ONLY — never reaches `signals.status`** (its INSERT is what
failed) ⇒ **no schema change**; `schema.sql:60-66` CHECK and `daily_trade_review.py:717`
`_KNOWN_OTHER_STATUSES` reconciliation both untouched.

## ⭐ 2 instruction premises were WRONG (proven by the RED run)
1. **Pre-fix the response is `500`, NOT `200`.** The instruction's expected RED ("response
   200") describes the **TRAP** a release-only fix would create, not old behaviour — old code
   raises and escapes to `_handle_webhook:427`. (The investigation had this right in Q4-c.)
2. **An IMMEDIATE retry is bounced as `IN_PROCESS`, not `DUPLICATE`.** Both docs say
   "DUPLICATE" throughout, but **`_claim_in_flight` (`:822`) is checked BEFORE the dedup cache
   (`:829`)** and both claims leak ⇒ the retry never reaches the dedup check. Real sequence:
   **IN_PROCESS ≤120 s** (until the sweeper clears in-flight) → **DUPLICATE → 300 s** → then
   accepted. **The ~300 s bound and "the dedup cache is the binding constraint" still hold.**

## ⚠️ THE OPS FINGERPRINT IS RETIRED (deliberate, inherent to the design)
The investigation's evidence base was **`response_code=500` (0 in 89,794 POSTs)**. **That
fingerprint no longer exists** — a store failure now answers **503**, which `webhook_audit`
cannot distinguish from QUEUE_FULL backpressure (18 such rows). Unavoidable: any retryable
status must yield a retryable code.
**⇒ ALERT ON THE LOG LINE INSTEAD:** `webhook_receiver: signal store FAILED for <scanner>/<symbol>`
— kept at **CRITICAL on purpose** (it used to reach `_handle_webhook`'s CRITICAL; catching must
not make a real incident quieter). Also: a 503 batch audits `accepted=0, rejected=0`
(`_handle_webhook:416` only reads counts from 200s) — pre-existing QUEUE_FULL behaviour, not new.

## Evidence
**RED-on-old 3/3, rc=1** on the TRUE pre-change file (committed first, then
`git checkout 8eb155c -- signals/webhook_receiver.py`, grep-confirmed absent, rc checked —
never `git stash`); dedup leak caught at runtime as
`TTLCache({('TCS','gap_go_long'): True}, currsize=1)`. GREEN 3/3 restored.
**Regression:** P3-s14 alone (in-window) **10F/4852P/4skip**; the DEPLOYED combined tree
(crossed 16:00 ⇒ out-of-window) **11F/4854P/4skip**, rc=1. **Both reconcile exactly**
(4849+3=4852; +3 S4 tests −1 clock-flip = 4854). **0 attributable PROVEN, not name-matched:**
the 2 failing suites that DO reference the receiver were re-run on the true pre-change tree →
identical, diff EMPTY; the 11th (`test_interactive_startup::test_holiday_guard_missing_yaml_proceeds`
— *startup*-named, and S4 touches `startup_checks.py`) was proven twice — passes with
`TS_IGNORE_MARKET_WINDOW=1`, fails identically pre-change ([[pc-test-env-hygiene]] time-gate).
**Parity free:** 0 mode refs in the receiver (grep-confirmed).

## → LOOP (recorded, deliberately NOT fixed here)
**The SAME defect shape survives one line deeper:** inside the IntegrityError handler,
`fetch_one` (`:875`) sits between the claims and the return, and **an exception raised inside
an `except` block is not caught by a sibling `except`** ⇒ it still escapes with both claims
held. Materially narrower (needs the INSERT to raise IntegrityError — proving the DB is
healthy — and *then* the next SELECT to fail; the re-queue UPDATE already has its own
try/except). Not widened beyond the approved design.

Related: [[p3s14-investigation-17jul]] [[s4-boot-outage-17jul]]
[[feedback-verify-the-finding-premise]] [[feedback-verify-rc-not-output]]
[[feedback-webhook-flow-diagnosis]] [[feedback-in-flight-memory]] [[pc-test-env-hygiene]]

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 327 B (budget 300 B). The index now carries a hook and this link.

- ✅🚀 **[P3-s14 FIXED + DEPLOYED 17-Jul — `a9a686e`](p3s14_done_17jul.md)** — a store failure releases BOTH claims + returns retryable **503** (`STORE_ERROR`). **⚠️ OPS FINGERPRINT RETIRED: alert on the CRITICAL `signal store FAILED` line, NOT `response_code=500`.** Loop tail `fetch_one :875`. [[p3s14-done-17jul]]
