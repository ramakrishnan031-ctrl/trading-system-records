---
name: kill-ladder-never-fired-28jul
description: "The drift kill ladder has NEVER fired (22 days, 1.54M lines, 2 events both non-escalating). Escalation is SINGLE-SAMPLE, not 3-cycle. Decision #11 CLOSED 28-Jul: absolute, values UNCHANGED, no code change. K1-K3 survive the closure."
metadata: 
  node_type: memory
  type: project
  originSessionId: c4bb72b3-0d74-4f27-bc40-b99f67899e79
  modified: 2026-07-28T09:39:40.995Z
---

# 💀📉 THE DRIFT KILL LADDER — decided posture, unexercised mechanism

## ✅ DECISION #11 IS **CLOSED** (Rama, 28-Jul-2026 15:04) — Option A, LEAVE AS-IS, NO code change.
> *"I'll stick with existing amounts — ₹1,000 (soft kill) and ₹2,500 (hard kill). Point 3 CLOSED."*

Posture **ABSOLUTE** (options C/D closed) **and values UNCHANGED** — 250 / 1,000 / 2,500, cycles 3.
⛔ **The ₹1,500 soft-kill figure proposed earlier that day is WITHDRAWN, not deferred** — nothing to
design, implement or schedule, and **there is NO boot slot** (an earlier note here said "post-4-Aug";
that is struck — it described a change that no longer exists). ⛔ **NO VALUE WAS EVER CHANGED.**
**Reopen ONLY on:** material capital change · the ladder actually firing · a drift distribution
becoming obtainable. Full record: `docs/decisions/11_absolute_kill_ladder.md`.

⭐⭐ **THREE FINDINGS SURVIVE THE CLOSURE — do NOT treat them as closed** (registered as K1–K3 in
`docs/decisions/ACTIONS_not_decisions.md`): **K1** emergency-kill + SAME-DAY restart ⇒ exit 4, and
it is a **CLASS** (26 call sites, only 2 scheduled reasons) — but **MONITORED**: systemd will not
loop (`RestartPreventExitStatus=3 4`) and `liveness_probe` (`*/5 9-15 Mon-Fri`) raises ONE CRITICAL
within ~5 min; ✅ **the DOC half is FIXED 28-Jul (`1b03a64`, unpushed)** — `05_incident_response.md` and
`RUNBOOK.md:101` now name `deploy/resume.sh`, the real symptom (**`failed`, NOT a loop**;
`inactive (dead)` is the healthy night state) and the real cause (a **SAME-DAY emergency kill
of ANY kind**), and warn off BOTH `systemctl restart` and `main.py --resume` (instance-lock
collision). ⛔ **The BEHAVIOUR half of K1 stays OPEN** — gate after 4-Aug. **K2** the 06-Jul ₹10,000 events, unresolved. **K3** the observability gap.

## ⛔⛔ THREE CORRECTIONS TO WHAT EVERYONE (INCLUDING ME) ASSUMED

1. **ESCALATION IS SINGLE-SAMPLE.** `consecutive_cycles_before_escalate: 3` gates **only** the
   LOG_ONLY → SOFT promotion. `TIER_SOFT` and `TIER_HARD` **reset** the counter and dispatch
   immediately ⇒ **one ≥₹1,000 sample soft-kills; one ≥₹2,500 sample hard-kills.**
   ⛔ Do not describe the ladder as "3 cycles before it acts".
2. **Its wall-clock depends on the source.** ≈**45 s** via `fund_manager_self_check` (reconciler
   CHECK7, `poll_interval_sec: 15`, runs every cycle). **UNREACHABLE** via `fund_manager`:
   `sync_from_broker` has exactly **ONE** production caller — `main.py:995`, a **one-shot at 09:15**
   — so that source fires once per process lifetime and the in-memory counter dies at the 17:35 exit.
3. **The persisted-kill HALT is bounded to a SAME-DAY restart**, not overnight. A drift kill's
   reason is not in `SCHEDULED_KILL_REASONS`, so it is an EMERGENCY kill; a same-day restart hits
   `StartupScenario.HALT` ⇒ **exit 4, service does not come back up** ⇒ no exit management and no
   15:15/EOD squareoff until `--resume`. But `clear_stale_state()` is a **HEADLESS GUARANTEE**
   (Rama, 20-Jun) clearing **every** prior-day kill regardless of type. [[persisted-kill-is-halt-21jul]]

## ✅ WHAT THE RUNGS ACTUALLY DO — and Rama's description is ACCURATE
- **SOFT** = blocks new ENTRIES, **genuinely allows exits** — `is_active(intent)`: `exit` is blocked
  **only** on HARD. Alert body: *"New signals: BLOCKED | Open positions: managed to SL/TGT/EOD"*.
- **HARD** = blocks all orders **and dispatches an async FLATTEN** (cancels resting orders, exits
  OPEN/PARTIAL/PENDING_FILL, 2 h retry, per-trade escalation). ⭐ **It does NOT abandon positions.**
  The `exit` block exists because the kill switch's own indestructible flatten owns the close.

## 📉 MEASURED 28-Jul — **THE LADDER HAS NEVER FIRED**
Width: **22 files, `system_2026-06-29`→`2026-07-28`, 1,539,561 lines**, no `.gz`/archive (that is
the whole on-disk history). **Total `drift_handler` lines: 2.** Escalating-source events: **ZERO**.
No log_only/soft/hard trip; no kill `triggered_by=drift_handler`; `HARD_KILL ACTIVATED` = 0 (the 19
`SOFT_KILL ACTIVATED` are the scheduled 15:15/EOD kills).
⭐⭐ **The only drift ever seen at hard magnitude came from a source the ladder IGNORES:** 06-Jul ×2,
`source=order_reconciler`, tier=HARD, **delta ₹10,000** (4× HARD, 200× the ₹50 tolerance), logged
**INFO** by design. ⚠️ `expected=0.00` ⇒ looks like a **seeding artefact**, not a real ₹10k
discrepancy — unresolved, do not cite it as evidence of real drift.

## ⛔ THE LIMIT — a realised-drift DISTRIBUTION IS NOT OBTAINABLE
`TIER_NOISE` logs at **DEBUG** and production runs at INFO ⇒ **every drift below ₹250 is invisible.**
Min/median/p95 of normal drift **cannot be computed from these logs at all**; it needs a code change
(raise the noise tier, or persist samples) and then time. ⇒ **Decision #11's original "cheap and
unblocked" framing was WRONG** — the *trip* question was cheap, the *distribution* question is not.
⚠️ Also `kill_switch_state` is a **single-row CURRENT-STATE table, not a history** — it cannot answer
"has soft ever tripped"; the log grep is the only authority, and only back 22 trading days.
⇒ **Any value chosen now is chosen against an unmeasured background, on a path that has never
fired.** Not an argument against ₹1,500 — the honest statement of what backs it.

⭐ Found by applying the standing rule twice in one search: **an absence is only established by a
check wide enough to have found the thing.** `"capital drift detected"` returned 0 while
`"tier":"HARD"` returned 2 — the log key is `msg`, not `message`, and the real events were under a
different message entirely. [[feedback-verify-the-finding-premise]] [[deploy-record-exists-28jul]]
