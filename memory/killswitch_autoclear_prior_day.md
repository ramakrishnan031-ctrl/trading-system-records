---
name: killswitch-autoclear-prior-day
description: "A prior-day kill ALWAYS auto-clears at the next 08:15 boot; only SAME-day emergency kills need a manual --resume. The journal's \"Manual --resume required\" and the ledger's \"auto-clears at 08:15\" are both correct — different paths."
metadata: 
  node_type: memory
  type: project
  originSessionId: c3f29b72-f271-4cf9-8a94-99c5da225920
  modified: 2026-08-03T13:17:54.036Z
---

**Two DIFFERENT clear paths run at boot (`main.py:1607-1612`) — do not read one's log line as the other's verdict.**

1. `kill_switch.clear_stale_state(today)` (`capital/kill_switch.py:199-248`) — auto-clears **ANY** kill
   triggered on a **PREVIOUS calendar day**, regardless of type (SOFT_KILL / HARD_KILL / emergency /
   loss-limit / operator). This is Rama's 2026-06-20 **HEADLESS GUARANTEE**: a new trading day always
   starts clean; the safety net moved from "block startup" to the EOD report (each clear is audited to
   `system_events` as `KILL_AUTO_CLEARED`). Same-day kills are deliberately untouched
   (`triggered_date >= today` → return False).
2. `kill_switch.auto_clear_scheduled_kill()` (`:250-283`) — **same-day** only, and only for *scheduled*
   reasons (force_close, EOD squareoff). A non-scheduled reason logs **"Kill switch active with EMERGENCY
   reason … Manual --resume required"** and returns False. HARD_KILL is never auto-cleared here.

**Why this matters / the trap:** on 16-Jul the ledger said the operator SOFT_KILL "auto-clears at 08:15
tomorrow" while the VM journal said "Manual --resume required" — an apparent contradiction that decides
whether the system trades the next day. **Both are right.** The journal line came from path 2 on a
*same-day* 10:55 restart attempt; path 1 governs the *next* morning. A kill dated 16-Jul is a prior-day
kill on 17-Jul ⇒ auto-cleared ⇒ the session runs, no operator action needed.

**How to apply:** to answer "will it trade tomorrow?", read the `kill_switch_state` row's `triggered_at`
DATE and compare to the boot date — prior day ⇒ clears; same day ⇒ needs `deploy/resume.sh`. Never infer
it from a journal line alone; the same active kill logs "manual resume required" and still auto-clears
next morning. Verified 16-Jul-2026 against code + the live row
(`SOFT_KILL | 2026-07-16T10:54:28+05:30 | operator`).

**⛔⛔ A THIRD SURFACE GETS THIS WRONG — AND IT IS THE ONE THE OPERATOR READS AT NIGHT (measured 03-Aug-2026).**
`scripts/system_manager.py`'s 18:45 EOD report prints, under TOMORROW READINESS:
`⚠️ Kill switch: SOFT_KILL — needs deploy/resume.sh before market open`
for the **routine 15:15 circuit-breaker kill** — i.e. it instructs the *exact action this file says not to
take*. **REFUTED BY MEASUREMENT, not recollection: the string has been emitted 30×; Friday 31-Jul emitted
it, and Monday 03-Aug then booted `08:15:12` with `ExecMainStatus=0` and traded 4 trades** — wrong across
exactly that transition. **⛔ Do NOT run `resume.sh` on the strength of that line; check `triggered_at`'s
DATE as above.** ⚠️ `docs/expected_alarms.md` does NOT close this: `:31` states the principle but the doc
never mentions `system_manager` (0 hits), so the report gives an *instruction* and the doc a *prohibition*
with nothing linking them. Registered in [[unpushed-pending-deploy-ledger]], **NOT fixed** — it is code in
a daily 18:45 job and needs its own card, the same way #8 (docs) and #8b (executable) were split.

⛔⛔ **AND THE TRAP THAT ALMOST SHIPPED ON AN OPERATOR CARD, 05-Aug: AN *EVENING* READ CANNOT USE THE
DATE AS THE DISCRIMINATOR.** The 15:15 breaker fires at 15:15 **today**, so at 19:00 the routine kill IS a
same-day kill ⇒ a branch table reading *"SOFT_KILL dated today ⇒ STOP"* fires a **certain** false alarm on
the ordinary daily kill. ⭐ **MATCH THE `reason` STRING INSTEAD** — the two scheduled ones are
**`circuit_breaker_force_close_15:15`** and **`EOD_SQUAREOFF`** (`capital/kill_switch.py:120-123`; the first
written at `main.py:695`). **The DATE rule is for a MORNING read; the REASON rule works at any hour.**
✅ **And the auto-clear does NOT depend on open positions** — `SCHEDULED_KILL_REASONS`' comment says
*"safe to auto-clear … when no open positions exist"*, but that is **rationale, not the predicate**:
`clear_stale_state` (`:287-335`) turns on **one** thing — *was it triggered on a PRIOR calendar day* — and
its docstring says *"EVERY prior-day kill is cleared regardless of type… The system never blocks the
next-day startup."* ⇒ **a boot with CNC held still clears it.**

See [[deploy-alertwatcher-f1-done-16jul]] [[morning-verify-16jul]] [[unpushed-pending-deploy-ledger]]
</content>
