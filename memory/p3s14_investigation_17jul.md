---
name: p3s14-investigation-17jul
description: "P3-s14 investigated (read-only, 17-Jul): the webhook dedup claim is SEPARATE from the INSERT txn ⇒ the fix must explicitly release. Bounded to 300s, never fired (0/89,794). The obvious fix is a TRAP."
metadata: 
  node_type: memory
  type: project
  originSessionId: b8e3571f-ea7d-4863-b873-b303871b1932
---

**P3-s14 INVESTIGATED 17-Jul — READ-ONLY, nothing fixed, docs-only commit `8eb155c` UNPUSHED.**
Report `docs/audit/p3s14_investigation_17jul2026.md`. Investigate-first step of the careful
loop; **design (Web Claude) → ChatGPT → implement** follows.

## ⭐ THE STEER (what the design step needs)

**The claim is SEPARATE, not transactional ⇒ the fix MUST explicitly release it.**
In-memory `TTLCache` (`webhook_receiver.py:197`) vs a SQLite txn that *"rolls back on any
exception"* (`state_store.py:509`). A rollback cannot touch an in-memory dict.

**Shape: claim-before + release-on-failure. NOT claim-after-insert.**
- The idiom **already exists TWICE in this file** for QUEUE_FULL (`:874-876`, `:913-915`) —
  reuse existing machinery.
- **Releasing does NOT re-open double-entry**: two independent guards remain — `_claim_in_flight`
  (`:811`) serialises same-symbol concurrency, and **`UNIQUE(fingerprint, fingerprint_date)`**
  (`schema.sql:82-83`) is the authoritative within-window dedup (a retry inside the same 300s
  bucket recomputes the SAME fingerprint ⇒ IntegrityError ⇒ DUPLICATE). **The cache is a
  fast-path optimisation, not the control** — that is what makes releasing it safe.
- claim-after-insert would restructure a signal-ENTRY path (the `:869-890` re-accept and the
  `:913` pop both depend on the current ordering) for no added safety.

## ⚠️⚠️ THE TRAP — the obvious fix is INSUFFICIENT and can make it WORSE

Releasing the claim is necessary but **not sufficient**. If the handler catches and returns an
ordinary per-symbol status, the batch answers **200** (`:650` — only QUEUE_FULL yields 503) ⇒
**Chartink never retries** ⇒ a bounded 300s loss becomes **PERMANENT**. The release only helps
if a retry actually arrives.
**⇒ Pair the release with a retryable 5xx**, folded into the `:649-650` predicate
(`any_queue_full` → `any(retryable)`), exactly mirroring **M-S2's QUEUE_FULL→503**. That also
lets the loop continue past the failure instead of abandoning the batch.

## CONFIRMED (the bug is real)

`_process_signal` claims dedup at **`:824`** and in-flight at **`:811`**, then guards the INSERT
with **`except sqlite3.IntegrityError` ONLY** (`:858`). Every *enumerated* reject path releases
correctly (`:821`, `:877`, `:891`, `:915`) — **the gap is the path nobody enumerated**: any other
exception escapes with **BOTH claims held** ⇒ that `(symbol, scanner)` is DUPLICATE-bounced ⇒
silently dropped.

## 2 corrections to the finding
1. **WORSE than "one signal"**: `:637` calls `_process_signal` inside the per-symbol loop **with
   no try/except** ⇒ a raise **abandons the REST of the payload batch**. Those recover on retry
   (never claimed); only the raising symbol stays stuck.
2. **The dedup key is `(symbol, scanner_name)`** (`:817`) — NOT symbol+strategy+bucket. The
   bucket belongs to the separate DB-side layer.

## Blast radius — bounded, and it has NEVER fired
- **One `(symbol, scanner)` pair, ≤300s** (the TTLCache self-expires). Not a symbol/strategy poison.
- In-flight leak bounded to **≤120s — not 60s**: evictable at heartbeat+60s but the sweeper only
  **ticks** every 60s (`:1037`, `:1043`). **No restart needed** — the FIX-011 sweeper covers what
  [[feedback-in-flight-memory]] says needs one.
- **✅ 0 × HTTP 500 in 89,794 audited POSTs (12-Jun→16-Jul)** — `webhook_audit` is authoritative
  ([[feedback-webhook-flow-diagnosis]]): 200×63816 · 403×25960 (the known pre-10:00 `entry_start`
  gate) · 503×18 (handled backpressure) · **500×0**.
- Why so rare: **WAL + `busy_timeout=30000` (30s) + `BEGIN IMMEDIATE`** ⇒ an OperationalError
  needs a **>30s writer stall**; **disk-full / IO error is the likelier trigger**. Heavy writers
  (backup 01:00, wal_checkpoint 16:00) barely overlap webhook hours (09:15-15:30).
- **⇒ Real defect on an unprotected path, ZERO occurrences. That sets PRIORITY, not correctness.**
- It is **loud when it happens** (CRITICAL `:428` + a durable `response_code=500` audit row) and
  silent only in its EFFECT ⇒ the 0/89,794 is evidence, not missing instrumentation.
- ⚠️ The sweeper's CRITICAL (`:1050-1055`) would blame **signal_processor** ("worker likely
  crashed or deadlocked") for what is actually a receiver-side INSERT failure — a misleading
  cause to know about before that line is read in anger.

## Regression surface / parity
`_process_signal` `:769-920` · claims `:811`/`:824`/`:922-944` · sweeper `:175-180`+`:1030-1055` ·
the batch loop + 503 predicate `:614-661` · escape `_handle_webhook:412-436` + `errorhandler(500)`
`:312-315` · `schema.sql:74-83`. **Primary test: `tests/unit/test_webhook_receiver.py` (109
dedup/in-flight/QUEUE_FULL assertions)** + integration `test_full_signal_flow` /
`test_end_to_end_smoke` / `test_hardening_scenarios` (M-S2).
**NO test anywhere injects a non-IntegrityError INSERT failure** ⇒ that is why a 100%-unprotected
path sits under a green suite; the fix needs a **RED-on-old `OperationalError`-injection test**
asserting: both claims released · an immediate retry is **ACCEPTED not DUPLICATE** · the response
is **retryable 5xx, not 200**.
**Parity free** (Rule #5): the receiver has **0 mode references** — signal ENTRY, upstream of any
paper/live branch.

Related: [[feedback-webhook-flow-diagnosis]] [[feedback-in-flight-memory]]
[[feedback-verify-the-finding-premise]] [[batch1-done-16jul]] (where P3-s14 was escalated)

## Index line relocated from `MEMORY_ARCHIVE_2026H1.md` — 22-Aug-2026 (NI-8 line-budget pass)

Verbatim, as it stood at 933 B (budget 300 B). The index now carries a hook and this link.

- 🔎✅ **[P3-s14 INVESTIGATED 17-Jul (read-only; `8eb155c` docs-only, UNPUSHED) — design step next](p3s14_investigation_17jul.md)** — **STEER: the dedup claim is SEPARATE, not transactional** (in-memory `TTLCache` vs a txn that rolls back) ⇒ **the fix MUST explicitly release**; **claim-before + release** (the idiom exists twice already at `:874-876`/`:913-915`; double-entry stays blocked by `_claim_in_flight` + `UNIQUE(fingerprint,fingerprint_date)`). **⚠️ THE TRAP: releasing alone is NOT enough** — a normal return makes the batch **200** ⇒ Chartink never retries ⇒ a bounded 300s loss goes **PERMANENT**; must pair with a **retryable 5xx** (mirror M-S2's QUEUE_FULL→503). Bounded: one `(symbol,scanner)` ≤300s; in-flight ≤120s (not 60 — the sweeper only ticks every 60s). **✅ NEVER FIRED: 0×500 in 89,794 POSTs.** No test injects a non-IntegrityError INSERT failure. [[p3s14-investigation-17jul]]
