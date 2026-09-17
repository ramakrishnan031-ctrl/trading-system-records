---
name: no-push-wakeups
description: Never arm a self-wakeup to trigger a time-gated push/deploy — armed wakeups fail silently if the session is down; use the instruction-file handoff.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1ea19fad-6d14-461b-9fc7-dfd016c4f8f3
  modified: 2026-07-23T10:50:07.816Z
---

**Never arm a self-wakeup (ScheduleWakeup / CronCreate) to trigger a time-gated push, deploy, or off-market action.** When the session is powered down across the firing window the wakeup fails **silently** — no alert, no trace, the work simply does not happen.

**Why:** same failure class as the liveness probe and the S4 boot outage ([[s4-boot-outage-17jul]]) — a mechanism that looks healthy because its failure emits no signal; a green path you never watch fail is not evidence it ran ([[verify-check-the-rc-not-the-output]]). Proven 23-Jul-2026: a wakeup armed to push the label-layer batch at ~15:31 IST did not fire (power-down across the window); the miss was caught only because the resume instruction file said to check `git ls-remote origin refs/heads/main` FIRST.

**How to apply:** for anything time-gated, rely on the **instruction-file handoff** — a written file a fresh/resuming session reads and executes — as the reliable path. An in-session blocking wait (a background `until`-loop for a short, attended window) is fine, because a session death is then visible as an incomplete turn. Reserve armed wakeups for polling external state that genuinely cannot notify you — never for the action itself.
