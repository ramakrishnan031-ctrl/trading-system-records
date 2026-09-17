---
name: daily-entry-policy-22aug
description: SETTLED 22-Aug-2026 — one trade per (symbol, DIRECTION, BOOK) per trading day; PENDING_FILL consumes the slot. Two entries in one stock in one day ARE allowed when the books differ. GTT+MIS exception SHELVED. Never write "one scrip per day" alone.
metadata:
  node_type: memory
  type: project
---

**`docs/DAILY_ENTRY_POLICY.md` on `main` — LOCAL ONLY.** The single authoritative
record; banners in `PATHS.md` + `docs/SYSTEM_MAP.md` corrected in place.

🔴 **ACTIVE RULE = AS DEPLOYED at `4568385`:** one completed trade per
**`(symbol, DIRECTION, BOOK)`** per day (`signal_processor.py:696-758`,
`state_store.py:707-772`, config enabled, fired **20×** on 21-Aug). ⇒ ⭐ **TWO
entries in ONE stock in ONE day ARE ALLOWED when the BOOKS differ** — SOLARA
20-Aug and KRONOX 21-Aug, both MIS→CNC. Enforced atomically inside
`portfolio_lock` at all 3 entry paths; reads **execution history**, ⛔ not
positions, so it survives an exit and a restart.

✅ **SETTLED 22-Aug 04:30 — RULE A ACCEPTED, RULE B REJECTED** (Rama: *"one trade
per symbol + direction + book per day … If yes let it be"*). ⭐ **Reason, so it is
⛔ never rediscovered as a defect: Rule A is the VERIFIED deployed behaviour and
has NO hole; Rule B would be a deliberate TIGHTENING — new policy, code, tests,
deploy — ⛔ not a correction to anything broken.** Cost consciously not adopted:
**−₹22.71** (SOLARA +11.50, KRONOX +11.21).
🗣️ **WORDING RULE: ⛔ NEVER write *"one scrip per day"* alone** — it reads as *one
stock per day*. The formal scoping must appear in the SAME paragraph.

⚠️ **CORRECTS the earlier *"6 blocked, net +₹4.69"* figure** — it conflated PRE-
and POST-rule cases. The four same-book repeats (RALLIS · SENCO · AURIONPRO · FSL)
**predate** the gate (`656b62d`) and would be blocked today under EITHER reading.
⛔ Not evidence about this choice.

⛔ **SHELVED — GTT LONG + MIS SHORT** (Rama, 22-Aug: *"Not worth efforts"*).
Governance history, ⛔ NOT a requirement. **Why:** the guards were never the
constraint — `CONTRARY_POSITION` has fired **ZERO times ever**; the signals DO
co-occur (12 symbol-days) but both legs die upstream (`PROCESSED` = **1** of
~830). ⛔ Two guards block it, not one.

⛔ **UNCHANGED, do not touch:** `CONTRARY_POSITION` · `DUPLICATE_SYMBOL` ·
`PENDING_FILL`'s in-flight role (⛔ do NOT "fix" it) · `portfolio_lock` atomicity ·
restart persistence · partial-fill counting · carried-position protection.
📌 **PARKED, ⛔ not started:** the upstream funnel.

Related: [[pre-build-review-gate-21aug]] · [[paper-cannot-exercise-class-26jul]]
