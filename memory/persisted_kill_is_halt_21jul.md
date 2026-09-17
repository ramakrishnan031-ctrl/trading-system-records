---
name: persisted-kill-is-halt-21jul
description: "A persisted kill = HALT-on-startup (exit 4), NOT 'run with entries blocked'; the in-process form has no operator trigger. And ANY halted day forfeits RESET_PNL (reset_daily_pnl reachable only from eod_squareoff._fire, in-process)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c4770e8-90bb-44e6-90c3-bfe4c179b944
  modified: 2026-07-24T20:43:19.423Z
---

**A persisted kill switch means HALT-ON-STARTUP, not "running with entries blocked."** `is_active()` reads in-memory state (KS12); the DB row loads once at boot (KS3). Writing SOFT_KILL to the DB + restart ⇒ `StartupScenario.HALT` ⇒ `main.py:1791` **exit 4** (proven live 21-Jul 11:37:53, unit `failed`/status 4). The in-process form (which WOULD keep the service running) has **no external operator trigger** — every `soft_kill()` caller is an internal safety path; no signal handler (only SIGINT/SIGTERM), no control endpoint (webhook `:5000`, healthcheck `:8080`, GUI risk API all read-only).

**⭐ GENERAL CONSEQUENCE — any halted day forfeits the daily-loss reset.** `reset_daily_pnl()` (writes the `RESET_PNL` row) is reachable ONLY from `eod_squareoff._fire()`, in-process. A halted afternoon writes no RESET_PNL. Applies to every halt, planned or not (F1 design item, `docs/audit/fix_sprint_21jul2026.md`).

**⚠️ SCOPE CORRECTION (MEASURED 25-Jul, live DB read-only) — "halted day" does NOT mean "a day with a SOFT_KILL row".** The routine **15:15 `circuit_breaker_force_close_15:15`** kill (by `order_monitor`) leaves the service RUNNING, so the 15:17 `_fire()` still happens: Fri 24-Jul had SOFT_KILL at 15:15:01 **and** `RESET_PNL` at 15:19:10 with `pnl_delta = −5.88 == −Σ(day pnl_delta)`. So the forfeit applies to a **HALT** (the exit-4 / service-not-running class), NOT to the ordinary daily circuit breaker — which is the kill state you will actually find on the board most evenings. Conflating them would misread F1's scope and mis-set its priority. (Also re-confirms the E4/W10 contract in prod for a 4th day.)

**Why:** Rama asked to "soft-kill for the day"; the architecture supports *halted* OR *running*, not *running+entries-blocked* (F2 design item). The two goals (block entries / preserve tonight's E4/W10 verification) conflicted ⇒ stopped and asked; Rama kept the verification; service resumed via `deploy/resume.sh`.

**How to apply:** never expect a persisted kill to leave the service running. Blocking entries while running needs a NEW mechanism (F2). `liveness_probe` treats a persisted SOFT_KILL as OPERATOR_HALT (silent), NOT a DOWN alarm.

Related: [[killswitch-autoclear-prior-day]] [[e4-w10-deployed-20jul]] [[phase2-carryover-proven-21jul]] [[monday-first-real-boot-proven-20jul]]
