---
name: prune-09-design-20jul
description: "Prune #09 Option B design written 20-Jul (awaits review) — the naive diff makes the 15:50 job a permanent no-op because EXPIRED/DUPLICATE are never persisted, and keeping rejects costs ~9.9 MB/trading day unbounded."
metadata: 
  node_type: memory
  type: project
  originSessionId: d010c6e6-1e94-4ed6-9e89-609c3f52dda7
  modified: 2026-07-20T17:18:24.030Z
---

**DESIGN ONLY, written 20-Jul-2026, awaits ChatGPT review.** Option B (keep `REJECTED_*`) is Rama's
decision; the design implements it and does not re-argue it. No code/config/cron changed;
`eod_cleanup.py` was **never executed** in any form. Doc: `docs/decisions/DESIGN_09_prune_retention.md`.

**⭐ THE HEADLINE: the naive diff makes the job a PERMANENT NO-OP.** Remove `GLOB 'REJECTED*'` and the
predicate is `status IN ('EXPIRED','DUPLICATE')` — **neither is ever persisted.**
`signal_processor.py:696` raises `_PipelineReject("EXPIRED")` which stores as **`REJECTED_EXPIRED`**;
`webhook_receiver.py:827/846` return **HTTP dicts before the INSERT**. Live table: **0 of them in
36,004 rows.** A hygiene cron that runs daily at 15:50 and cannot delete anything = a check that cannot
fail. [[feedback-verify-rc-not-output]]

**⚠️ CORRECTS the inherited "accident of the predicate" framing.** Git: the *intent* to prune rejects
was always deliberate (bare `'REJECTED'` was in the original `IN`-list); the accident was the predicate
not matching the vocabulary, so rejects were **RETAINED** by accident. `2e61fad` (14-Jul) deliberately
fixed that. **⇒ Option B is a deliberate reversal of P10, not a correction.**

**STORAGE, measured via `dbstat`:** **1,908 B per retained reject** = 1,070 (signals) + 235 (indexes) +
**603 (screener_results cascade — 32% of the cost, which a signals-only estimate misses)**.
~5,445 rejects/trading day ⇒ **+9.9 MB/trading day, ~2.5 GB/yr, UNBOUNDED** (status quo is bounded
~644 MB by the 90-day window). **Rejects are ALREADY 69% of the 91.58 MB live DB.**
**Disk: the amplifier is BACKUPS** — a full daily copy on the *same* disk, 15 dailies retained ⇒ **~15×**.
After a year ≈ 39 GB of dailies vs 72 GB free. Puts a number on Rama's item #9.

**NO DEADLINE:** the prune deletes **0 rows until ~10-Sep-2026** (cutoff 2026-04-21 vs earliest row
2026-06-12), so the live DB already reflects "no pruning".

**Regression map — nothing assumes old rejects are absent.** Every consumer is date- or id-scoped; the
one unscoped-looking query is a **docstring example** (`state_store.py:161`). The dedup path P10 named
is **structurally immune**: unique key `(fingerprint, fingerprint_date)` + a date-scoped recovery query,
so a >90-day row cannot collide. P10's concern was index **size**, not correctness.

**Queued, found while mapping:** `ops_dashboard/.../db_reader.py:170` counts `status='DUPLICATE'` —
never exists ⇒ returns **0 always**, and its residual-bucket subtraction is a no-op. **Third instance of
the dead-status class.** Also `SKIPPED_QUOTE_UNAVAILABLE` (2,667 rows) matches no clause and is retained
forever today.

**Deploy:** off-market, careful loop, **after E4/W10 is confirmed** — never both in flight.
Parity verified: `eod_cleanup.py` has no mode branch at all. Related: [[e4-w10-deployed-20jul]]
